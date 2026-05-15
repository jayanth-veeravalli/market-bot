# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
uv sync

# Run the bot
uv run python main.py

# Run database migrations
uv run alembic upgrade head

# Create a new migration
uv run alembic revision -m "description"
```

Always use `uv` — never `pip` or `python` directly.

## Environment

Copy `.env.sample` to `.env.local` for local development. `main.py` loads `.env.local` first if it exists, then falls back to `.env`.

Required variables:
- `ENV` — `local` or `prod`
- `ALPACA_API_KEY` / `ALPACA_API_SECRET` — Alpaca Markets credentials
- `DISCORD_BOT_TOKEN` — Discord bot token
- `DISCORD_GUILD_ID` — required only when `ENV=local` (for fast guild-scoped slash command sync)
- `DATABASE_URL` — PostgreSQL connection string (use `postgresql://` prefix; Alembic rewrites it to `postgresql+psycopg://` internally)

## Architecture

The bot is a Discord slash command bot that fetches options (put) data from Alpaca and surfaces it in Discord.

**Entry point:** `main.py` sets `TZ=America/New_York` (critical for correct Friday expiry logic), then starts the bot via `bot.py`.

**Request flow for `/premiums`:**
1. `commands/premiums.py` receives the Discord interaction
2. Calls `services/alpaca.py:fetch_puts_for_ticker()` — fetches current stock price, then queries the Alpaca option chain for puts at strikes 20–30% below spot, for the current and next Friday expiry
3. Filters results to a minimum premium rate of 0.5% of collateral (`MIN_PREMIUM_RATE = 0.005`)
4. `services/formatter.py:format_result()` converts `OptionsResult` → list of Discord messages (chunked to 15 rows each to stay under Discord limits)

**Watchlist:** Stored in a PostgreSQL `tickers` table (managed by Alembic). `services/watchlist.py` uses `psycopg` async connections directly — no ORM.

**Slash command sync:** When `ENV=local`, commands sync to the specific guild immediately on startup. In prod, they sync globally (can take up to 1 hour to propagate).

**Deployment:** GCP VM running a systemd service (`deploy/market-bot.service`). `deploy/setup.sh` handles provisioning. A dev container is available in `.devcontainer/` for local development.

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

Rules:
- ALWAYS read graphify-out/GRAPH_REPORT.md before reading any source files, running grep/glob searches, or answering codebase questions. The graph is your primary map of the codebase.
- IF graphify-out/wiki/index.md EXISTS, navigate it instead of reading raw files
- For cross-module "how does X relate to Y" questions, prefer `graphify query "<question>"`, `graphify path "<A>" "<B>"`, or `graphify explain "<concept>"` over grep — these traverse the graph's EXTRACTED + INFERRED edges instead of scanning files
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).
