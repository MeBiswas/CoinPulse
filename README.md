# CoinPulse: End-to-End Crypto Data Engineering Pipeline

## 📌 Overview

CoinPulse is a production-style data pipeline that ingests cryptocurrency price and coin data from the CoinGecko API, processes it through a robust ETL workflow, and stores it in a structured PostgreSQL database. The pipeline is orchestrated using Apache Airflow running in Docker.

## 🚀 Features

* **API Data Ingestion** — Fetches crypto prices and coin metadata from CoinGecko API
* **Raw Data Storage** — Lake-style JSON storage in `data/raw/`
* **Data Transformation** — Pandas-based cleaning and transformation
* **PostgreSQL Storage** — Structured relational storage with schema initialization
* **Airflow Orchestration** — Dockerized Airflow cluster with scheduled DAGs
* **Analytics Engine** — Pre-built SQL queries for insights (top movers, daily averages, rankings)
* **Error Handling & Logging** — Comprehensive logging throughout the pipeline

## 🏗️ Architecture

```
CoinGecko API → Extraction → Raw JSON → Transformation → PostgreSQL → Analytics → CSV Results
                                    ↓
                              Airflow DAG (scheduled daily)
```

## 📂 Project Structure

```
CoinPulse/
├── airflow-docker/          # Dockerized Airflow setup
│   ├── docker-compose.yaml  # Airflow cluster config
│   ├── dags/               # ETL DAG definitions
│   ├── config/             # Airflow config
│   ├── logs/               # DAG execution logs
│   └── plugins/           # Custom plugins
├── data/
│   ├── raw/               # Raw JSON data (crypto_price/, coin_data/)
│   └── processed/        # Transformed CSV data
├── result/                # Analytics query results (CSV)
├── sql/                   # SQL queries for analytics
│   ├── top_movers.sql
│   ├── daily_average.sql
│   ├── rank_by_price.sql
│   └── latest_prices_query.sql
├── src/
│   ├── extraction.py      # Data extraction from API
│   ├── transformation.py # Data transformation logic
│   ├── load.py           # Database loading & schema
│   ├── run_analytics.py  # Analytics query runner
│   ├── crypto_coins/     # Coin dimension data handling
│   ├── crypto_prices/    # Price fact data handling
│   └── utils/            # Shared utilities
└── requirements.txt      # Python dependencies
```

## ⚙️ Setup Instructions

### 1. Clone and navigate to project

```bash
cd CoinPulse
```

### 2. Create virtual environment

```bash
python -m venv venv
```

### 3. Activate environment

```bash
# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Start Airflow in Docker

```bash
cd airflow-docker
docker-compose up -d
```

Access Airflow UI at `http://localhost:8080` (credentials: airflow/airflow)

## ▶️ Running the Pipeline

### Option 1: Via Airflow UI

1. Open `http://localhost:8080`
2. Find `coinpulse_etl_pipeline` DAG
3. Trigger manually or wait for daily schedule

### Option 2: Manual ETL execution

```bash
# Extract data
python -m src.extraction

# Transform data
python -m src.transformation

# Load to database
python -m src.load
```

### Option 3: Run analytics queries

```bash
python -m src.run_analytics
```

Results are exported to `result/` directory as CSV files.

## 📊 Analytics Queries

| Query | Description | Output |
|-------|-------------|--------|
| `top_movers` | Top gaining/losing cryptos | `result/top_movers.csv` |
| `daily_avg` | Daily average prices | `result/daily_avg.csv` |
| `rank_by_price` | Cryptos ranked by price | `result/rank_by_price.csv` |
| `latest_prices` | Most recent price data | `result/latest_prices.csv` |

## 🧠 Skills Demonstrated

* Python ETL pipeline development
* SQL & PostgreSQL data modeling
* Apache Airflow workflow orchestration
* Docker containerization
* Data engineering best practices
* API integration (CoinGecko)
* Analytics & reporting

## 📦 Dependencies

- pandas, numpy — Data processing
- psycopg2-binary — PostgreSQL connector
- SQLAlchemy — Database ORM
- requests — HTTP client
- tabulate — Table formatting
- Apache Airflow — Workflow orchestration
