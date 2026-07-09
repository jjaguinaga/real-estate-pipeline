# ETL Real Estate Pipeline with SQL Analytics

---

## Motivation 

This project was built to help a real estate agency answer questions about their agents, sales and revenue. This project uses csv files to build a database and relational tables, then uses SQL to answer those questions.

---

## What this Project Does

This pipeline extracts data from four csv files consisting of agents, clients, properties and transactions. It stores it all in a relational database and produces SQL views that allow analysts to explore findings. 

---

## Key Findings 

**Which cities had the most listings** The 'city_listing_rank' view shows us that San Francisco has the most listings with 36 as a combination of rental and sale.


**Percentage of closed listings** the 'status_percents' view shows us that only 24% of the listings are closed, 36% are cancelled and 38% are pending. 


**Which agents are top performers** the 'top_closing_agents' view shows us that Madison Ortiz has closed on 5 properties making her the top agent. 


**How much commission was made** the 'total_commission' view shows us the total amount of commission that was made in the agency which was over 5.2 million dollars.

---

## Architecture 

```
CSV Files (faker-generated synthetic data)
↓
transform.py → Pandas (data cleaning and validation)
↓
load.py → PostgreSQL (relational database with 5 tables)
↓
analytics.sql → SQL views (business insights)
```

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python | Core pipeline logic |
| Pandas | Data cleaning and transformation |
| PostgreSQL | Relational database |
| Psycopg2 | PostgreSQL connection |
| SQL | Analytics views |
| Git | Version control |

---

## Project Structure 

```
real-estate-pipeline/
├── raw-data
      ├── raw_agents.csv
      ├── raw_clients.csv
      ├── raw_properties.csv
      └── raw_transactions.csv
├── transform.py
├── load.py
├── analytics.sql
└── README.md
```

---

## How to Run

1. Clone the repo 
2. Install dependencies:
```bash
pip install pandas psycopg2-binary
```
3. Make sure PostgreSQL is running locally
4. Create the PostgreSQL database:
```sql
CREATE DATABASE real_estate;
```
5. Run the pipeline:
```bash
python3 load.py
```
6. Open TablePlus or any SQL client, connect to the `real_estate` database, and run the views in `analytics.sql`
