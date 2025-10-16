import os, pandas as pd
from pathlib import Path
from qsentia.vendors.polygon import PolygonClient
from qsentia.utils import watermark as wm

ROOT = Path(os.getenv("DATA_ROOT", "./data"))

def load(symbol: str, start: str, end: str, max_rows: int = 2000000) -> int:
    cli = PolygonClient()
    recs = []
    for row in cli.news(symbol, start, end):
        recs.append({
            "symbol": symbol,
            "published_utc": row.get("published_utc"),
            "title": row.get("title", ""),
            "article_url": row.get("article_url", ""),
            "source": row.get("source", ""),
            "tickers": ",".join(row.get("tickers", []) or []),
            "ingestion_ts": pd.Timestamp.utcnow()
        })
        if len(recs) >= max_rows:
            break
    if not recs:
        wm.set_("news", symbol, end)
        return 0
    df = pd.DataFrame(recs)
    df["ts_utc"] = pd.to_datetime(df["published_utc"], utc=True, errors="coerce")
    df = df.dropna(subset=["ts_utc"])
    df["dt"] = df["ts_utc"].dt.date.astype(str)
    written = 0
    for d, g in df.groupby("dt"):
        out = ROOT / "bronze" / "news" / f"dt={d}" / f"symbol={symbol}" / "part.parquet"
        out.parent.mkdir(parents=True, exist_ok=True)
        g.to_parquet(out, engine="pyarrow", index=False)
        written += len(g)
    wm.set_("news", symbol, end)
    return written