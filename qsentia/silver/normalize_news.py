import os, duckdb, pandas as pd
from pathlib import Path

ROOT = Path(os.getenv("DATA_ROOT", "./data"))

def normalize(dt_start: str, dt_end: str, symbols: list[str]) -> int:
    src = f"{ROOT}/bronze/news/dt=*/symbol=*/part.parquet"
    con = duckdb.connect()
    con.execute(f"""
        CREATE OR REPLACE VIEW v_src AS
        SELECT * FROM read_parquet('{src}')
        WHERE dt BETWEEN '{dt_start}' AND '{dt_end}'
    """)
    df = con.execute("""
        SELECT
          symbol,
          ts_utc,
          title,
          article_url,
          source,
          tickers,
          dt
        FROM v_src
    """).df()
    if symbols:
        df = df[df["symbol"].isin([s.upper() for s in symbols])]
    df = df.dropna(subset=["ts_utc"]).sort_values(["symbol","ts_utc"])
    df = df.drop_duplicates(subset=["symbol","ts_utc","title"])
    n = 0
    for (d, sym), g in df.groupby(["dt","symbol"], sort=False):
        out = ROOT / "silver" / "news" / f"dt={d}" / f"symbol={sym}" / "part.parquet"
        out.parent.mkdir(parents=True, exist_ok=True)
        g.to_parquet(out, engine="pyarrow", index=False)
        n += len(g)
    return n