import sqlite3
from pathlib import Path

DB_PATH = Path("watchlist.db")


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS tickers (ticker TEXT PRIMARY KEY)"
    )
    conn.commit()
    return conn


def add_ticker(ticker: str) -> str:
    ticker = ticker.upper().strip()
    with _connect() as conn:
        try:
            conn.execute("INSERT INTO tickers VALUES (?)", (ticker,))
            conn.commit()
            return f"✅ Added **{ticker}** to the watchlist."
        except sqlite3.IntegrityError:
            return f"**{ticker}** is already in the watchlist."


def remove_ticker(ticker: str) -> str:
    ticker = ticker.upper().strip()
    with _connect() as conn:
        cursor = conn.execute("DELETE FROM tickers WHERE ticker = ?", (ticker,))
        conn.commit()
        if cursor.rowcount == 0:
            return f"**{ticker}** is not in the watchlist."
        return f"✅ Removed **{ticker}** from the watchlist."


def get_tickers() -> list[str]:
    with _connect() as conn:
        rows = conn.execute("SELECT ticker FROM tickers ORDER BY ticker").fetchall()
        return [row[0] for row in rows]


def fetch_all() -> str:
    tickers = get_tickers()
    if not tickers:
        return "Your watchlist is empty. Use `/watchlist add` to add stocks."
    lines = "\n".join(f"• {t}" for t in tickers)
    return f"**Watchlist ({len(tickers)} stocks):**\n{lines}"
