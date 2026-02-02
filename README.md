# MoMo SMS Data Processing Application

![Status](https://img.shields.io/badge/Status-in%20development-yellow.svg)
![Version](https://img.shields.io/badge/Assignment_Version-1.0-blue)
![Due](https://img.shields.io/badge/Current_Due_Date-13th_of_January,2026-8A2BE2)
## Team Information

**Team Name:** EWDGroup-13

**Team Members:**

- Okechukwu Wisdom Ikechukwu
- Erioluwa Gideon Olowoyo
- Cyuzuzo Germain
- Igor Ntwali
- Kellen Ashley Mutoni

## Project Description

This is an enterprise-level fullstack application designed to process MoMo (Mobile Money) SMS transaction data in XML format. The system performs comprehensive data processing including parsing, cleaning, normalization, categorization, and storage in a relational database. The application provides a frontend dashboard interface for analyzing and visualizing transaction data, enabling insights into mobile money usage patterns, transaction types, and financial trends.

Task Sheets for Week 2 Database Design and Implementation: https://docs.google.com/spreadsheets/d/1rCpYeL-neYF9pLjIJMFF84ge2ypylhV_DcXbMgolmWc/edit?usp=sharing

Task Sheets for Building and Securing the REST API: https://docs.google.com/spreadsheets/d/1M_vmswK8btt72Yz7fxbQSUbU3D80fuD3k_snTog9Qks/edit?usp=sharing

### Key Features

- **XML Data Processing**: Parse and extract transaction data from MoMo SMS XML files
- **Data Cleaning & Normalization**: Standardize amounts, dates, phone numbers, and other transaction fields
- **Transaction Categorization**: Automatically classify transactions into meaningful categories
- **Relational Database Storage**: Store processed data in SQLite for efficient querying and analysis
- **Interactive Dashboard**: Visualize transaction data with charts, tables, and analytics
- **ETL Pipeline**: Automated Extract, Transform, Load process for batch data processing
- **RESTful API** (Optional): FastAPI-based backend for programmatic data access

## Architecture Diagram

**System Architecture:** 

<img width="2782" height="5499" alt="EWDgroup" src="https://github.com/user-attachments/assets/b7571798-4290-48be-b478-b8a79247c84a" />


_Note: The architecture diagram will be created using Draw.io and linked here. It will illustrate the main system components, data flow, and interactions between the ETL pipeline, database, API, and frontend._

## Scrum Board

**Project Management Board:** [https://trello.com/invite/b/6965caedbace0c4c87328f2f/ATTI2ae459685ab0520df14daaedaf08e14348AEB6CA/ewdgroup-13-scrum-board]

_Note: The Scrum board is set up using Trello with columns for To Do, In Progress, and Done. All project tasks are tracked and managed through this board._

## Project Structure

```
.
├── README.md                         # Project documentation and setup guide
├── architecture.html                 # System architecture diagram
├── .env.example                      # Environment variables template (DATABASE_URL or SQLite path)
├── requirements.txt                  # Python dependencies (lxml/ElementTree, dateutil, FastAPI optional)
├── index.html                        # Dashboard entry point (static HTML)
├── docs/
│   └── erd_diagram.png               # Entity Relationship Diagram
├── database/
│   └── database_setup_sql.sql        # MySQL database setup script
├── examples/
│   └── json_schemas.json             # JSON schema examples
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
│   └── schemas.py                    # Pydantic models
├── scripts/                          # Utility scripts
└── tests/                            # Test files
```

 ### MoMo SMS Transaction API

A RESTful API built with Python (Flask) that parses Mobile Money (MoMo) SMS data from an XML file, stores it in a MySQL database, and exposes secure CRUD endpoints for managing transactions.

This system is designed for financial data extraction, storage, and analytics — making it ideal for fintech experiments, reconciliation systems, and transaction dashboards.

 ### Features

SMS Data Parsing
Automatically extracts:

Transaction Reference

Amount

Fee

Date
from modified_sms_v2.xml

Database Persistence
All transactions are stored in MySQL.

Secure API
All endpoints are protected with Basic Authentication.

Soft Deletion
Records are marked as deleted instead of being permanently removed.

Performance Testing (DSA)
Includes a script comparing Linear Search vs Dictionary Lookup.

 ### Prerequisites

Python 3.8+

MySQL Server

pip (Python package manager)

 Installation & Setup
1️⃣ Install Dependencies
pip install Flask Flask-HTTPAuth mysql-connector-python werkzeug

2️⃣ Database Setup

Log in to MySQL

Run the provided SQL script to create:

Database: momo_sms_db

Required tables

Update database credentials in your Python file:

DB_CONFIG = {
    'host': 'localhost',
    'user': 'your_root_user',
    'password': 'your_password',
    'database': 'momo_sms_db'
}

3️⃣ Parse XML & Seed Database

Load transactions from the XML file into MySQL:

python parse_to_db.py

4️⃣ Run the API Server
python app.py


The server will start at:

http://127.0.0.1:5000

 Authentication

All endpoints require Basic Authentication.

Field	Value
Username	admin
Password	momo_secure_2025

If authentication fails, the API returns:

401 Unauthorized

 API Endpoints
🔹 Get All Transactions
curl -u admin:momo_secure_2025 http://127.0.0.1:5000/transactions

🔹 Add a New Transaction
curl -X POST http://127.0.0.1:5000/transactions \
     -u admin:momo_secure_2025 \
     -H "Content-Type: application/json" \
     -d '{
           "transaction_ref": "12345",
           "category_id": 1,
           "amount": 5000,
           "fee": 50,
           "raw_sms": "Sample SMS"
         }'

🔹 Update a Transaction
curl -X PUT http://127.0.0.1:5000/transactions/1 \
     -u admin:momo_secure_2025 \
     -H "Content-Type: application/json" \
     -d '{"amount": 7500}'

🔹 Delete a Transaction (Soft Delete)
curl -X DELETE http://127.0.0.1:5000/transactions/1 \
     -u admin:momo_secure_2025

 ### DSA Performance Comparison

This project includes a script that compares:

Linear Search

Dictionary Lookup

To run the test:

python dsa_test.py