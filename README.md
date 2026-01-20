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
- Medallion Architecture (Bronze/Silver/Gold): this clearly seperates raw data, cleaned data and analysis ready datasets.
- Point-in-time correctness: Explicit handling of timestamps, publication delays, and calendar-based feature engineering to prevent lookahead bias
- Multiple data streams: Equity price aggregates (Polygon), Options data with derived features (IV, RV, Black-Scholes references), News data with watermark-based idempotency, Company fundamentals (Financial Modeling Prep)
