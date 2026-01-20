# Research Lab
## Data infrasturcture for quantitative research and backtesting 
The biggest problem faced by analyst is to ingest and clean data from multiple sources and optimizing for data storage and processing. Models perform good during backtests but fail when deployed not only because of bad assumptions, bad models but also due to robust data handling (point-in-time, look-ahead bias and survivorship bias). This repository contains a research-focused financial data pipeline designed to ingest, normalize, and store market data in a point-in-time correct and backtest-safe manner.
The goal is not just to fetch data, but to build trustworthy research infrastructure that avoids lookahead bias, scales cleanly, and mirrors how data would behave in real trading systems.

## Why Robust Data Infrastructure
Bad data assumption is the biggest issue and which creeps through:
1. Using information that was not avaiable at decision time (look-ahead bias)
2. Mixing timestamps, timezones, or reporting delays
3. inefficient storage and fecting the data cause large backtest impracticle

This project sought to solve these problems by using data design principles
## Key Features
- **Medallion Architecture (Bronze/Silver/Gold):** this clearly seperates raw data, cleaned data and analysis ready datasets.
- **Point-in-time correctness:** Explicit handling of timestamps, publication delays, and calendar-based feature engineering to prevent lookahead bias
- **Multiple data streams:** Equity price aggregates (Polygon), Options data with derived features (IV, RV, Black-Scholes references), News data with watermark-based idempotency, Company fundamentals (Financial Modeling Prep)
- **Efficient storage:** Parqet format, hive-style partitioning: `dt=YYYY-MM-DD / symbol=SYMBOL` for efficent query for backtests and reserach notebooks
- **Idempotent and Restart Safe:** Used SQLite backed watermark tracking for the safe reruns without duplication
- **Prallel ETL Orchestration:** Threaded igestion balanced against API ratelimits
- **Reproducible:** Dockerized environment

## Architecture Design 
<img width="1207" height="422" alt="image" src="https://github.com/user-attachments/assets/5f9dafcd-9b40-44e9-8332-5ff4b16059c8" />

## Data Flow
<img width="1066" height="552" alt="image" src="https://github.com/user-attachments/assets/3ce1bf0c-f531-4bd4-bfcf-c5d623be8467" />


## Project Structure 
`Datalab/
├── cli.py                  # CLI entry point (Typer orchestration)
├── pyproject.toml          # Project metadata and dependencies
├── README.md               # Project overview and quickstart
├── DESIGN.md               # Architecture and design rationale
│
├── vendors/                # External data source clients
│   ├── polygon.py          # Polygon API client with retry logic
│   └── fmp.py              # Financial Modeling Prep client
│
├── utils/                  # Shared utilities
│   ├── watermark.py        # SQLite-backed watermark tracking
│   └── time.py             # Timestamp and calendar helpers
│
├── bronze/                 # Bronze layer (raw, immutable data)
│   ├── load_aggregates.py  # Equity aggregates ingestion (month-sliced)
│   ├── load_options.py     # Options raw ingestion
│   ├── load_news.py        # News ingestion with idempotency
│   └── load_fmp.py         # Fundamentals raw ingestion
│
├── silver/                 # Silver layer (normalized, typed)
│   ├── normalize_aggregates.py  # DuckDB-based normalization
│   ├── compact_options.py       # Options feature engineering
│   ├── normalize_news.py        # News deduplication and typing
│   └── compact_fmp.py           # Fundamentals schema normalization
│
├── gold/                   # Gold layer (analysis-ready datasets)
│   ├── make_price_panels.py     # Time-series panels for backtesting
│   ├── make_option_features.py  # Model-ready option features
│   └── make_fmp_gold.py         # Snapshot and panel fundamentals
│
├── meta/                   # Pipeline state
│   └── watermarks.sqlite   # Dataset-level processing state
│
├── data/                   # Data lake storage (generated)
│   ├── bronze/
│   │   └── aggregates/
│   │       └── dt=YYYY-MM-DD/
│   │           └── symbol=SYMBOL/
│   │               └── part.parquet
│   ├── silver/
│   └── gold/
│
└── roadmap/                # Planned extensions (not active)
    └── alpaca.md            # Live trading integration design (future)
`

## Example usage
- Load daily equity aggregates for a symbol:
`python -m Datalab.cli load-aggregates AAPL \
  --start 2024-01-01 \
  --end 2024-12-31`

- Run the full pipeline in parallel:
`python -m Datalab.cli run-all-parallel AAPL,MSFT,GOOGL \
  --start 2024-01-01 \
  --end 2024-12-31`

## Design principles (high level)
- Data correctness 
- Explicit timestamps everywhere
- Storage optimized for time-series research
- Reproducibility over cleverness
- Backtest parity with live trading assumptions

## Future roadmap
- Alpaca live-trading integration (shared gold layer for backtest & live)
- Incremental daily ingestion using watermarks
- Real-time streaming ingestion
- ML feature store integration
- Backtest execution engine
