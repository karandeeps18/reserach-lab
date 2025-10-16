import sqlite3, os
from pathlib import Path

ROOT = Path(os.getenv("DATA_ROOT", "./data"))
DB = ROOT / "meta" / "watermarks.sqlite"
DB.parent.mkdir(parents=True, exist_ok=True)

def _conn():
    c = sqlite3.connect(DB)
    c.execute("""CREATE TABLE IF NOT EXISTS watermarks(
        dataset TEXT, symbol TEXT, last_to TEXT,
        PRIMARY KEY(dataset, symbol)
    )""")
    return c

def get(dataset: str, symbol: str) -> str | None:
    with _conn() as c:
        cur = c.execute("SELECT last_to FROM watermarks WHERE dataset=? AND symbol=?",
                        (dataset, symbol))
        row = cur.fetchone()
        return row[0] if row else None

def set_(dataset: str, symbol: str, last_to: str):
    with _conn() as c:
        c.execute("INSERT OR REPLACE INTO watermarks(dataset, symbol, last_to) VALUES(?,?,?)",
                  (dataset, symbol, last_to))