# MoMo SMS Data Processing Application

## Team Information

**Team Name:** EWDGroup-13

**Team Members:**

- Okechukwu Wisdom Ikechukwu
- Cyuzuzo Germain
- Igor Ntwali
- Bior Majok
- Dianah Gasasira Shimwa
- kellen Ashley Mutoni

## Project Description

This is an enterprise-level fullstack application designed to process MoMo (Mobile Money) SMS transaction data in XML format. The system performs comprehensive data processing including parsing, cleaning, normalization, categorization, and storage in a relational database. The application provides a frontend dashboard interface for analyzing and visualizing transaction data, enabling insights into mobile money usage patterns, transaction types, and financial trends.

### Key Features

- **XML Data Processing**: Parse and extract transaction data from MoMo SMS XML files
- **Data Cleaning & Normalization**: Standardize amounts, dates, phone numbers, and other transaction fields
- **Transaction Categorization**: Automatically classify transactions into meaningful categories
- **Relational Database Storage**: Store processed data in SQLite for efficient querying and analysis
- **Interactive Dashboard**: Visualize transaction data with charts, tables, and analytics
- **ETL Pipeline**: Automated Extract, Transform, Load process for batch data processing
- **RESTful API** (Optional): FastAPI-based backend for programmatic data access

## Architecture Diagram

**System Architecture:** [ARCHITECTURE_DIAGRAM_LINK] -> will upload when push to avoid resizing issues.

_Note: The architecture diagram will be created using Draw.io and linked here. It will illustrate the main system components, data flow, and interactions between the ETL pipeline, database, API, and frontend._

## Scrum Board

**Project Management Board:** [https://trello.com/invite/b/6965caedbace0c4c87328f2f/ATTI2ae459685ab0520df14daaedaf08e14348AEB6CA/ewdgroup-13-scrum-board]

_Note: The Scrum board is set up using Trello with columns for To Do, In Progress, and Done. All project tasks are tracked and managed through this board._

## Project Structure

```
.
├── README.md                         # Project documentation and setup guide
├── .env.example                      # Environment variables template (DATABASE_URL or SQLite path)
├── requirements.txt                  # Python dependencies (lxml/ElementTree, dateutil, FastAPI optional)
├── index.html                        # Dashboard entry point (static HTML)
├── web/
│   ├── styles.css                    # Dashboard styling and CSS
│   ├── chart_handler.js              # JavaScript for fetching and rendering charts/tables
│   └── assets/                       # Images, icons, and other static assets
├── data/
│   ├── raw/                          # Provided XML input files (git-ignored)
│   │   └── momo.xml                  # Source XML data file
│   ├── processed/                    # Cleaned/derived outputs for frontend
│   │   └── dashboard.json            # Aggregated data for dashboard consumption
│   ├── db.sqlite3                    # SQLite database file
│   └── logs/
│       ├── etl.log                   # Structured ETL processing logs
│       └── dead_letter/              # Unparsed/ignored XML snippets for debugging
├── etl/
│   ├── __init__.py                   # Python package initialization
│   ├── config.py                     # Configuration: file paths, thresholds, categories
│   ├── parse_xml.py                  # XML parsing logic (ElementTree/lxml)
│   ├── clean_normalize.py            # Data cleaning: amounts, dates, phone normalization
│   ├── categorize.py                 # Transaction type categorization rules
│   ├── load_db.py                    # Database operations: create tables + upsert to SQLite
│   └── run.py                        # CLI entry point: parse -> clean -> categorize -> load -> export JSON
├── api/                              # Optional (bonus feature)
│   ├── __init__.py                   # Python package initialization
│   ├── app.py                        # Minimal FastAPI application with /transactions, /analytics endpoints
│   ├── db.py                         # SQLite connection helpers and database utilities
│   └── schemas.py                    # Pydanti
```

readme## Database Design (Week 2)

### Overview

We designed a MySQL database to store MoMo SMS transaction data. The database has 6 main tables that work together to organize the data.

### Tables

| Table                    | What it stores                   |
| ------------------------ | -------------------------------- |
| `users`                  | People who send or receive money |
| `transactions`           | The actual transaction records   |
| `transaction_categories` | 9 types of transactions we found |
| `system_logs`            | Logs from processing the XML     |
| `tags`                   | Labels for transactions          |
| `transaction_tags`       | Links transactions to tags (M:N) |

### Transaction Categories

We analyzed the XML and found 9 types of transactions:

| Name              | Direction | How we detect it         |
| ----------------- | --------- | ------------------------ |
| Incoming Transfer | CREDIT    | "You have received"      |
| P2P Transfer      | DEBIT     | "*165*S\*"               |
| Bank Deposit      | CREDIT    | "*113*R\*A bank deposit" |
| Cash Withdrawal   | DEBIT     | "withdrawn"              |
| Payment to Code   | DEBIT     | "TxId:"                  |
| Airtime Purchase  | DEBIT     | "to Airtime"             |
| Bundle Purchase   | DEBIT     | "to Bundles and Packs"   |
| Utility Payment   | DEBIT     | "to MTN Cash Power"      |
| Third Party       | DEBIT     | "*164*S\*"               |

### How to Set Up

1. Make sure MySQL is installed
2. Run the setup script:

```bash
mysql -u root -p < database/database_setup.sql
```

3. Check it worked:

```sql
USE momo_sms_db;
SHOW TABLES;
```

### Sample Queries

Get all transactions with details:

```sql
SELECT * FROM v_transaction_summary LIMIT 10;
```

Get daily statistics:

```sql
SELECT * FROM v_daily_stats;
```

### Documentation Files

- [docs/erd_diagram.md](docs/erd_diagram.md) - ERD with diagram
- [docs/data_dictionary.md](docs/data_dictionary.md) - Table descriptions
- [examples/json_schemas.json](examples/json_schemas.json) - JSON examples
- [examples/sql_json_mapping.md](examples/sql_json_mapping.md) - SQL to JSON mapping
