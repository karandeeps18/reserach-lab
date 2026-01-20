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
<img width="1066" height="552" alt="image" src="https://github.com/user-attachments/assets/b76b7e4d-a108-4ef8-a1f5-91fab17c9f4a" />





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
