# Market Research Bot

A Discord bot for researching sell put premiums on watchlist stocks using the Alpaca API.

## What It Does

- Manage a shared stock watchlist via Discord slash commands
- Fetch put option premiums for strikes 20–30% below the current stock price
- Returns contracts for the **current week** and **next week** expiries
- Filters out contracts with an effective premium below **0.5% of the strike price**
- Large results are automatically split into multiple Discord messages to avoid truncation
- Data sourced from Alpaca's free indicative feed (suitable for research, not execution)

## Prerequisites

- Python 3.9+
- `uv` package manager
- [Alpaca account](https://alpaca.markets) (free, paper trading)
- [Discord bot](https://discord.com/developers/applications) invited to your server
- [Supabase](https://supabase.com) project (free tier is sufficient)

## Setup

1. **Clone and install dependencies**
   ```bash
   uv sync
   ```

2. **Fill in `.env`** (copy from `.env.sample`)
   ```
   ALPACA_API_KEY=your_key
   ALPACA_API_SECRET=your_secret
   ALPACA_BASE_URL=https://paper-api.alpaca.markets/v2
   DISCORD_BOT_TOKEN=your_bot_token
   DATABASE_URL=postgresql://postgres.[ref]:[password]@aws-0-[region].pooler.supabase.com:5432/postgres
   ```

3. **Run database migrations**
   ```bash
   uv run alembic upgrade head
   ```

4. **Run the bot**
   ```bash
   uv run python main.py
   ```
   You should see: `✅ Logged in as <BotName> — slash commands synced.`

## Database

The bot uses **Supabase PostgreSQL** for persistent storage. The schema is managed with **Alembic** migrations. The `watchlist` service uses `psycopg3` async connections; `env.py` automatically rewrites the `postgresql://` URL to the `postgresql+psycopg://` dialect that SQLAlchemy requires.

### Current Schema

```sql
CREATE TABLE tickers (
    ticker   TEXT PRIMARY KEY,
    added_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

### Common Migration Commands

```bash
# Apply all pending migrations
uv run alembic upgrade head

# Roll back the most recent migration
uv run alembic downgrade -1

# Show current revision applied to the database
uv run alembic current

# Show full migration history
uv run alembic history --verbose
```

### Adding a New Table

1. **Generate a migration file**

   ```bash
   uv run alembic revision -m "create_alerts_table"
   ```

   This creates `migrations/versions/<rev>_create_alerts_table.py`.

2. **Write the `upgrade` and `downgrade` functions**

   ```python
   from alembic import op
   import sqlalchemy as sa

   def upgrade() -> None:
       op.create_table(
           "alerts",
           sa.Column("id", sa.Integer, primary_key=True),
           sa.Column("ticker", sa.Text, sa.ForeignKey("tickers.ticker"), nullable=False),
           sa.Column("threshold", sa.Numeric, nullable=False),
           sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.func.now()),
       )

   def downgrade() -> None:
       op.drop_table("alerts")
   ```

3. **Apply it**

   ```bash
   uv run alembic upgrade head
   ```

### Adding a Column to an Existing Table

```python
def upgrade() -> None:
    op.add_column("tickers", sa.Column("notes", sa.Text, nullable=True))

def downgrade() -> None:
    op.drop_column("tickers", "notes")
```

### Raw SQL Migrations

For cases where SQLAlchemy's DDL helpers are awkward (e.g. enabling extensions, custom types), use `op.execute` directly — as the initial `tickers` migration does:

```python
def upgrade() -> None:
    op.execute("""
        CREATE TABLE IF NOT EXISTS tickers (
            ticker   TEXT PRIMARY KEY,
            added_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
        )
    """)

def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS tickers")
```

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
- **Premium filter**: Contracts where the effective price (last traded, or mid if unavailable) is below 0.5% of the strike are excluded
- Watchlist is stored in Supabase PostgreSQL; schema is managed via Alembic migrations

## Deployment (GCP)

The bot runs as a systemd service on a GCP e2-micro VM. Deployments are triggered manually via GitHub Actions.

### First-Time VM Setup

SSH into a fresh Debian/Ubuntu VM and run:

```bash
sudo bash deploy/setup.sh
```

This installs dependencies, clones the repo to `/opt/market-bot`, and registers the systemd service. After setup, write your `.env` to `/opt/market-bot/.env` and start the service:

```bash
sudo systemctl start market-bot
sudo systemctl status market-bot
```

### GitHub Actions Deploy

The `Deploy to GCP` workflow (`deploy.yml`) is triggered manually from the **Actions** tab. It:

1. SSHs into the VM using secrets
2. Writes the `.env` from GitHub Secrets
3. Pulls the latest code
4. Runs `uv sync` and `alembic upgrade head`
5. Restarts the `market-bot` systemd service

**Required GitHub Secrets:**

| Secret | Description |
|--------|-------------|
| `GCP_SSH_PRIVATE_KEY` | Private SSH key for the VM |
| `GCP_VM_HOST` | VM external IP |
| `GCP_VM_USER` | SSH username |
| `ALPACA_API_KEY` | Alpaca API key |
| `ALPACA_API_SECRET` | Alpaca API secret |
| `ALPACA_BASE_URL` | Alpaca base URL |
| `DISCORD_BOT_TOKEN` | Discord bot token |
| `DATABASE_URL` | Supabase PostgreSQL connection string |

## Project Structure

```
market_bot/
├── main.py                    # Entry point
├── bot.py                     # Discord bot + /help command
├── commands/
│   ├── watchlist.py           # /watchlist commands
│   └── premiums.py            # /premiums commands
├── services/
│   ├── watchlist.py           # PostgreSQL watchlist CRUD
│   ├── alpaca.py              # Alpaca API integration + premium filter
│   └── formatter.py           # Discord message formatting + chunking
├── models/
│   └── options.py             # PutOption, OptionsResult models
├── migrations/                # Alembic migration versions
├── deploy/
│   ├── setup.sh               # GCP VM first-time setup script
│   └── market-bot.service     # systemd service unit file
├── deploy.yml                 # GitHub Actions deploy workflow
└── alembic.ini                # Alembic configuration
```
