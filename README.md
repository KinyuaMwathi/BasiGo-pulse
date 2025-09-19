# BasiGo Pulse — Insights Platform

BasiGo Pulse is an end-to-end data product built on AWS that ingests operational and financial data from Nairobi's electric bus operators. It stores the data in **Amazon Redshift Serverless** and powers insights through **Amazon QuickSight** dashboards.

---

## Features
- Mock datasets for 6 Nairobi operators (Citi Hoppa, East Shuttle, Super Metro, OMA, MetroTrans, Embassava)
- Covers **routes, trips, telematics, financials, and maintenance**
- Serverless setup on AWS (S3, Redshift, QuickSight)
- Business-ready dashboards for passenger trends, revenue vs forecast, and cost efficiency

---

## Tech Stack
- **AWS S3** → Raw data storage (CSV files)
- **Amazon Redshift Serverless** → Scalable data warehouse
- **AWS IAM** → Access and security management
- **Amazon QuickSight** → BI dashboards and visualization
- **Python (Pandas, Faker, NumPy)** → Mock data generation
- **SQL (DDL/DML)** → Schema creation and data loading

---

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/KinyuaMwathi/BasiGo-pulse.git
cd BasiGo-pulse
```

### 2. Generate mock data
```bash
bashpython src/data_gen/data_generator.py
```

This creates CSVs in the ./data/ folder.

### 3. Create Redshift tables
Run the DDL scripts from src/db/schema.sql in Amazon Redshift Query Editor v2 to set up the raw schema (routes, trips, telematics, financials, maintenance).

### 4. Load CSV data into Redshift
Use Redshift COPY commands to load your CSVs from S3 into the tables.

### 5. Build dashboards
Connect Amazon QuickSight to Redshift and build interactive dashboards for:

- Executive Pulse (KPI Summary)
- Passenger trends
- Cost & efficiency
- Maintenance Overview


## License
MIT License