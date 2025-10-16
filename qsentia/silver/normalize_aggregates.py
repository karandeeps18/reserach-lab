import os, duckdb, pandas as pd
from pathlib import Path

ROOT = Path(os.getenv("DATA_ROOT", "./data"))

def normalize(dt_start: str, dt_end: str, symbols: list[str]) -> int:
    src = f"{ROOT}/bronze/aggregates/dt=*/symbol=*/part.parquet"
    con = duckdb.connect()
    con.execute(f"""
        CREATE OR REPLACE VIEW v_src AS
        SELECT * FROM read_parquet('{src}')
        WHERE dt BETWEEN '{dt_start}' AND '{dt_end}'
    """)
    df = con.execute("""
        SELECT
          symbol,
          to_timestamp(t/1000) AT TIME ZONE 'UTC' AS ts_utc,
          CAST(o AS DOUBLE) AS open,
          CAST(h AS DOUBLE) AS high,
          CAST(l AS DOUBLE) AS low,
          CAST(c AS DOUBLE) AS close,
          CAST(v AS DOUBLE) AS volume,
          CAST(n AS BIGINT) AS num_trades,
          dt
        FROM v_src
    """).df()
    # filter to requested symbols if provided
    if symbols:
        df = df[df["symbol"].isin([s.upper() for s in symbols])]
    df = df.sort_values(["symbol","ts_utc"]).drop_duplicates(["symbol","ts_utc"])
    n = 0
    for (d, sym), g in df.groupby(["dt","symbol"], sort=False):
        out = ROOT / "silver" / "aggregates" / f"dt={d}" / f"symbol={sym}" / "part.parquet"
        out.parent.mkdir(parents=True, exist_ok=True)
        g.to_parquet(out, engine="pyarrow", index=False)
        n += len(g)
    return n