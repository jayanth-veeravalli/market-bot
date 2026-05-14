import os
import psycopg

DATABASE_URL = os.environ["DATABASE_URL"]


async def add_ticker(ticker: str) -> str:
    ticker = ticker.upper().strip()
    async with await psycopg.AsyncConnection.connect(DATABASE_URL) as conn:
        try:
            await conn.execute("INSERT INTO tickers (ticker) VALUES (%s)", (ticker,))
            return f"✅ Added **{ticker}** to the watchlist."
        except psycopg.errors.UniqueViolation:
            return f"**{ticker}** is already in the watchlist."


async def remove_ticker(ticker: str) -> str:
    ticker = ticker.upper().strip()
    async with await psycopg.AsyncConnection.connect(DATABASE_URL) as conn:
        cursor = await conn.execute("DELETE FROM tickers WHERE ticker = %s", (ticker,))
        if cursor.rowcount == 0:
            return f"**{ticker}** is not in the watchlist."
        return f"✅ Removed **{ticker}** from the watchlist."


async def get_tickers() -> list[str]:
    async with await psycopg.AsyncConnection.connect(DATABASE_URL) as conn:
        cursor = await conn.execute("SELECT ticker FROM tickers ORDER BY ticker")
        rows = await cursor.fetchall()
        return [row[0] for row in rows]


async def fetch_all() -> str:
    tickers = await get_tickers()
    if not tickers:
        return "Your watchlist is empty. Use `/watchlist add` to add stocks."
    lines = "\n".join(f"• {t}" for t in tickers)
    return f"**Watchlist ({len(tickers)} stocks):**\n{lines}"
