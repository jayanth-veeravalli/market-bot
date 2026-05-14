import os
import re
from datetime import date, timedelta

from alpaca.data.historical import StockHistoricalDataClient, OptionHistoricalDataClient
from alpaca.data.requests import StockLatestQuoteRequest, StockLatestTradeRequest, OptionChainRequest

from models.options import PutOption, OptionsResult

API_KEY = os.environ["ALPACA_API_KEY"]
API_SECRET = os.environ["ALPACA_API_SECRET"]

stock_client = StockHistoricalDataClient(API_KEY, API_SECRET)
option_client = OptionHistoricalDataClient(API_KEY, API_SECRET)


def _parse_symbol(symbol: str) -> tuple[date, float]:
    # OCC format: ROOT + YYMMDD + C/P + 8-digit strike (strike * 1000)
    match = re.match(r'[A-Z]+(\d{2})(\d{2})(\d{2})[CP](\d{8})', symbol)
    if not match:
        raise ValueError(f"Cannot parse option symbol: {symbol}")
    yy, mm, dd, strike_raw = match.groups()
    expiry = date(2000 + int(yy), int(mm), int(dd))
    strike = int(strike_raw) / 1000
    return expiry, strike


def _next_friday(from_date: date) -> date:
    days = (4 - from_date.weekday()) % 7 or 7
    return from_date + timedelta(days=days)


def _get_current_price(ticker: str) -> float:
    req = StockLatestTradeRequest(symbol_or_symbols=ticker)
    trade = stock_client.get_stock_latest_trade(req)[ticker]
    return trade.price


def _fetch_puts(ticker: str, price: float, expiry: date) -> list[PutOption]:
    req = OptionChainRequest(
        underlying_symbol=ticker,
        type="put",
        expiration_date_gte=expiry,
        expiration_date_lte=expiry,
        strike_price_gte=round(price * 0.70, 2),
        strike_price_lte=round(price * 0.80, 2),
        feed="indicative",
    )
    chain = option_client.get_option_chain(req)

    puts = []
    for symbol, snapshot in chain.items():
        expiry, strike = _parse_symbol(symbol)
        bid = snapshot.latest_quote.bid_price if snapshot.latest_quote else 0.0
        ask = snapshot.latest_quote.ask_price if snapshot.latest_quote else 0.0
        last_price = snapshot.latest_trade.price if snapshot.latest_trade else None
        delta = snapshot.greeks.delta if snapshot.greeks else None
        iv = snapshot.implied_volatility

        puts.append(PutOption(
            symbol=symbol,
            strike=strike,
            expiry=expiry,
            bid=bid,
            ask=ask,
            midpoint=round((bid + ask) / 2, 4),
            last_price=last_price,
            delta=delta,
            iv=iv,
        ))

    return sorted(puts, key=lambda p: p.strike, reverse=True)


def fetch_puts_for_ticker(ticker: str) -> OptionsResult:
    try:
        ticker = ticker.upper().strip()
        price = _get_current_price(ticker)
        today = date.today()
        current_friday = _next_friday(today)
        next_friday = _next_friday(current_friday + timedelta(days=1))

        return OptionsResult(
            ticker=ticker,
            current_price=price,
            current_week=_fetch_puts(ticker, price, current_friday),
            next_week=_fetch_puts(ticker, price, next_friday),
        )
    except Exception as e:
        return OptionsResult(
            ticker=ticker,
            current_price=0.0,
            current_week=[],
            next_week=[],
            error=str(e),
        )
