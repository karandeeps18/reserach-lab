import os, pandas as pd
from datetime import date, timedelta
from pathlib import Path
from qsentia.vendors.polygon import PolygonClient
from qsentia.utils import watermark as wm

ROOT = Path(os.getenv("DATA_ROOT", "./data"))

def month_slices(start: str, end: str):
    s = pd.Timestamp(start, tz="UTC").date()
    e = pd.Timestamp(end, tz="UTC").date()
    cur = date(s.year, s.month, 1)
    while cur <= e:
        nxt = (pd.Timestamp(cur) + pd.offsets.MonthEnd(0)).date()
        yield max(s, cur).isoformat(), min(e, nxt).isoformat()
        cur = (pd.Timestamp(cur) + pd.offsets.MonthBegin(1)).date()

def load(symbol: str, start: str, end: str, timespan: str="day") -> int:
    cli = PolygonClient()
    total = 0
    for s, e in month_slices(start, end):
        rows = list(cli.agg_bars(symbol, 1, timespan, s, e))
        if not rows: continue
        df = pd.DataFrame(rows)
        df["symbol"] = symbol
        df["ingestion_ts"] = pd.Timestamp.utcnow()
        df["ts_utc"] = pd.to_datetime(df["t"], unit="ms", utc=True)
        df["dt"] = df["ts_utc"].dt.date.astype(str)
        for d, g in df.groupby("dt"):
            out = ROOT / "bronze" / "aggregates" / f"dt={d}" / f"symbol={symbol}" / "part.parquet"
            out.parent.mkdir(parents=True, exist_ok=True)
            g.to_parquet(out, engine="pyarrow", index=False)
            total += len(g)
    wm.set_("aggregates", symbol, end)
    return total