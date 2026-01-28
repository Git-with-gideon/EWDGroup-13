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
