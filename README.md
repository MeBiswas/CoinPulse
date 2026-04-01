# CoinPulse: End-to-End Crypto Data Engineering Pipeline

## 📌 Overview

CoinPulse is a production-style data pipeline that ingests cryptocurrency price data from the CoinGecko API, processes it, and stores it in a structured PostgreSQL database. The pipeline is orchestrated using Apache Airflow.

## 🚀 Features

* API-based data ingestion (CoinGecko)
* Raw data storage (data lake style)
* Data transformation using Pandas
* Structured storage in PostgreSQL
* Workflow orchestration using Airflow
* Error handling and logging

## 🏗️ Architecture

API → Python ETL → Raw Storage → Processed Data → PostgreSQL → Airflow

## 📂 Project Structure

data/
raw/
processed/

src/
ingestion.py
transformation.py
load.py

airflow/
dag.py

sql/
schema.sql

## ⚙️ Setup Instructions

### 1. Create virtual environment

python -m venv venv

### 2. Activate environment

venv\Scripts\activate   # Windows
source venv/bin/activate # Mac/Linux

### 3. Install dependencies

pip install -r requirements.txt

## ▶️ Running the Pipeline

### Run ingestion

python src/ingestion.py

### Run transformation

python src/transformation.py

### Load into database

python src/load.py

## 📊 Future Improvements

* Add Airflow scheduling
* Implement incremental loading
* Add data validation checks
* Dockerize the pipeline

## 🧠 Skills Demonstrated

* Python ETL
* SQL & Data Modeling
* Workflow Orchestration (Airflow)
* Data Engineering Best Practices
