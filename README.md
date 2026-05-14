# Market Research Bot

A Discord bot for researching sell put premiums on watchlist stocks using the Alpaca API.

## What It Does

- Manage a shared stock watchlist via Discord slash commands
- Fetch put option premiums for strikes 20–30% below the current stock price
- Returns contracts for the **current week** and **next week** expiries
- Data sourced from Alpaca's free indicative feed (suitable for research, not execution)

## Prerequisites

- Python 3.9+
- `uv` package manager
- [Alpaca account](https://alpaca.markets) (free, paper trading)
- [Discord bot](https://discord.com/developers/applications) invited to your server

## Setup

1. **Clone and install dependencies**
   ```bash
   uv install
   ```

2. **Fill in `.env`**
   ```
   ALPACA_API_KEY=your_key
   ALPACA_API_SECRET=your_secret
   ALPACA_BASE_URL=https://paper-api.alpaca.markets/v2
   DISCORD_BOT_TOKEN=your_bot_token
   ```

3. **Run the bot**
   ```bash
   uv run python main.py
   ```
   You should see: `✅ Logged in as <BotName> — slash commands synced.`

## Discord Bot Setup (One-Time)

1. Go to [discord.com/developers/applications](https://discord.com/developers/applications) → New Application
2. **Bot** tab → Add Bot → copy the Token → paste into `.env`
3. **OAuth2 → URL Generator**: check scopes `bot` + `applications.commands`, permission `Send Messages`
4. Open the generated URL in a browser → select your server → Authorize

## Commands

| Command | Description |
|---------|-------------|
| `/watchlist fetch` | Show all stocks in the watchlist |
| `/watchlist add [ticker]` | Add a stock to the watchlist |
| `/watchlist remove [ticker]` | Remove a stock from the watchlist |
| `/premiums fetch` | Fetch put premiums for all watchlist stocks |
| `/premiums stock [ticker]` | Fetch put premiums for a specific ticker |
| `/help` | Show available commands |

## Output Example

```
AAPL @ $211.50  (strikes $148–$169)

Current Week:
  Strike    Expiry        Bid     Ask     Mid     Delta     IV
  ──────────────────────────────────────────────────────────────
  169.00    2025-05-16    1.20    1.40    1.300   -0.182   28.4%
  165.00    2025-05-16    0.85    1.05    0.950   -0.143   27.1%
  ...

Next Week:
  Strike    Expiry        Bid     Ask     Mid     Delta     IV
  ──────────────────────────────────────────────────────────────
  169.00    2025-05-23    2.10    2.35    2.225   -0.198   27.8%
  ...
```

## Data Notes

- **Stock price**: Real-time via Alpaca IEX feed (may differ slightly from consolidated price)
- **Options data**: Indicative feed (estimated, not official OPRA) — use for research only, verify prices on your broker before placing orders
- Watchlist is stored locally in `watchlist.db` (SQLite)

## Project Structure

```
market_bot/
├── main.py               # Entry point
├── bot.py                # Discord bot + /help command
├── commands/
│   ├── watchlist.py      # /watchlist commands
│   └── premiums.py       # /premiums commands
├── services/
│   ├── watchlist.py      # SQLite watchlist CRUD
│   ├── alpaca.py         # Alpaca API integration
│   └── formatter.py      # Discord message formatting
└── models/
    └── options.py        # PutOption, OptionsResult models
```
