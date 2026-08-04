# ETL Real Estate Pipeline

---

## Overview

This pipeline extracts data from four CSV files, transforms it, and loads it into PostgreSQL. This ETL pipeline validates rows that are empty and moves bad rows to quarantine files for later inspection, and uses Docker for one-command execution. This was made for a real estate agency analyst. 

---

## Architecture Diagram

```
CSV Files 
↓
Extract → Raw DF
↓
Transform → Clean DF → Quarantine (bad rows)
↓
Load → Staging
↓
PostgreSQL
```

---

## Tech Stack 

| tools | Purpose | Version |
|---|---|---|
| Python | Core logic | 3.11 |
| Pandas | Data manipulation | 2.2.3 |
| PostgreSQL | Database | 15 |
| psycopg2-binary | PostgreSQL driver | 2.9.12 |
| pytest | Testing | 9.1.1 |
| Docker | Containerization | 29.x |
| Docker Compose | Multi-container orchestration | 5.x |

--- 

## Project Structure 

```
real-estate-pipeline/
├── config/
│   ├── __init__.py
│   └── settings.py          # Environment-based configuration
├── src/
│   ├── __init__.py
│   ├── extract.py           # Raw data extraction
│   ├── transform.py         # Data cleaning, validation, quarantine
│   ├── load.py              # Bulk load with staging tables
│   └── logger.py            # Structured logging
├── tests/
│   ├── __init__.py
│   └── test_transform.py    # pytest suite
├── data/
│   ├── raw/                 # Source CSVs
│   ├── processed/           # Cleaned outputs
│   └── quarantine/          # Bad rows for review
├── logs/                    # Pipeline execution logs
├── Dockerfile               # Container definition
├── docker-compose.yml       # Multi-container orchestration
├── requirements.txt         # Python dependencies
├── run_pipeline.py          # Entry point
└── README.md
```

---

## Key Features

| Feature | Description |
|---|---|
| **Environment-based config** | All settings via env vars, no hardcoded credentials |
| **Structured logging** | Timestamps, severity levels, module names to console + file |
| **Data validation** | Schema checks, business rules, referential integrity |
| **Quarantine pattern** | Bad rows saved to CSV with rejection reason |
| **Bulk loading** | PostgreSQL COPY for 100x performance vs row-by-row |
| **Staging + atomic swap** | No partial data visible to queries |
| **Transaction safety** | Full rollback on any failure |
| **Automated testing** | pytest with parameterized tests |
| **Docker containerization** | One command runs entire stack |

---

## How to Run

### Local Development:
1. Install dependencies 
```bash
pip install -r requirements.txt
```
2. Set environment variables (or use defaults)
```bash
export DB_PASSWORD=your_password
```
3. Run pipeline
```bash
python -m run_pipeline
```

### Docker (Recommended):
1. Start PostgreSQL + pipeline 
```bash
docker compose up --build
```
2. Verify data loaded 
```bash
docker compose exec postgres psql -U naga -d real_estate -c "SELECT COUNT(*) FROM agents;"
```

---

## Testing 

```bash 
python -m pytest tests/ -v
```

## Data Quality

| Table | Issue | Count | Action |
|---|---|---|---|
| Agents | Null license | 8 | Quarantined | 
| Clients | Null budget | 89 | Quarantined | 
| Clients | Duplicate IDs | 2 | Removed | 
| Properties | Orphan agent_id | 51 | Removed |
| Properties | Null address | 21 | Quarantined |
| Properties | Null sqft | 76 | Quarantined |
| Transactions | Orphan property_id | 231 | Removed |
| Transactions | Orphan agent_id | 66 | Removed |
| Transactions | Orphan client_id | 112 | Removed |
| Transactions | Null commission | 94 | Quarantined |

---