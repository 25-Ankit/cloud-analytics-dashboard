# Cloud Analytics Dashboard

> Real-time sales analytics pipeline with synthetic data generation, local event streaming (SQLite-based Kinesis simulation), and a live Flask + Chart.js dashboard.

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.1.3-black?logo=flask)
![Docker](https://img.shields.io/badge/Docker-ready-blue?logo=docker)
![License](https://img.shields.io/badge/License-MIT-green)
![GitHub](https://img.shields.io/badge/GitHub-ankit--25-black?logo=github)
![Repo](https://img.shields.io/badge/Repo-cloud--analytics--dashboard-blue)

##  Overview

**Cloud Analytics Dashboard** simulates a cloud-native real-time analytics pipeline locally without requiring AWS services.

It generates synthetic e-commerce transactions (product, category, city, price) using `Faker`, streams them into a local Kinesis-like store backed by SQLite (`stream/events.db`), and visualizes aggregated metrics (total orders, total sales, average order, sales by city/category) via:

1.  **CLI Processor** — `processor/processor.py` for terminal analytics
2.  **Web Dashboard** — `dashboard/app.py` Flask app with REST API + interactive Chart.js UI (auto-refreshes every 3s)

Ideal for learning/demonstrating streaming architectures, ETL patterns, and real-time dashboards.

##  Features

- **Synthetic Data Generation** — 8 products across 3 categories (`Electronics`, `Accessories`, `Wearables`) and 6 Indian cities
- **Local Streaming Layer** — `stream/stream.py` mimics AWS Kinesis with `create_stream()`, `put_event()`, `get_events()` on SQLite
- **Real-time Analytics** — Aggregates total sales, average order value, city-wise and category-wise breakdowns
- **Interactive Dashboard** — Flask + Chart.js (Bar chart for cities, Doughnut for categories), responsive design
- **REST API** — `GET /api/analytics` returns JSON analytics
- **Docker Ready** — Slim `python:3.11` image, exposes port 5000

## Tech Stack

| Layer | Technology |
|-------|------------|
| **Language** | Python 3.11 |
| **Web Framework** | Flask 3.1.3 |
| **Data Generation** | Faker |
| **Streaming / Storage** | SQLite (`events.db`) - Local Kinesis simulation |
| **Frontend** | HTML, CSS, Chart.js (CDN) |
| **Container** | Docker |

## Architecture

```
                +---------------------+
                | data-generator/     |
                | producer.py         |  Generates random sales every 2s
                | (Faker + random)    |
                +----------+----------+
                           | put_event(sale)
                           v
                +---------------------+
                | stream/             |
                | stream.py +         |  SQLite Table: events (id, event_data JSON, created_at)
                | events.db           |  API: create_stream(), put_event(), get_events()
                +----------+----------+
                           |
              +------------+------------+
              |                         |
   +------------------+      +------------------+
   | processor/       |      | dashboard/       |
   | processor.py     |      | app.py           |
   | CLI Aggregation  |      | Flask: /         |
   |                  |      | Flask: /api/     |
   +------------------+      | templates/index.html |
                             +--------+---------+
                                      |
                                      v
                             Browser (Charts auto-reload every 3s)
```

**Data Model** (`producer.py:41-50`):
```json
{
  "transaction_id": "uuid",
  "timestamp": "2024-...",
  "product": "Laptop",
  "category": "Electronics",
  "quantity": 3,
  "price": 55000,
  "total_amount": 165000,
  "city": "Mumbai"
}
```

##  Project Structure

```
cloud-analytics-dashboard/
├── dashboard/
│   ├── app.py                 # Flask app: get_analytics(), /api/analytics, /
│   └── templates/
│       └── index.html         # Chart.js dashboard (cards + 2 charts)
├── data-generator/
│   └── producer.py            # generate_sale() + infinite loop with put_event()
├── stream/
│   └── stream.py              # create_stream(), put_event(), get_events()
├── processor/
│   └── processor.py           # CLI aggregation and pretty-print
├── database/                  # (reserved/empty)
├── requirements.txt           # Flask==3.1.3, Faker
├── Dockerfile                 # python:3.11-slim, copies dashboard+stream, port 5000
└── README.md                  # Project documentation
```

## Installation

### Prerequisites
- Python 3.11+
- `pip` and `venv`
- Git (optional)
- Docker (optional, for containerized run)

### 1. Clone / Navigate
```bash
git clone https://github.com/ankit-25/cloud-analytics-dashboard.git
cd cloud-analytics-dashboard
# or if already downloaded:
cd /home/kali/Downloads/cloud-analytics-dashboard
```

### 2. Create Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
# requirements.txt contains:
# Flask==3.1.3
# Faker
```

### 4. Initialize Stream
```bash
python stream/stream.py
# Output: Local Kinesis stream is ready!
```
This creates `stream/events.db` with table `events` if not exists (`stream/stream.py:9-21`).

##  Usage

You need **2-3 terminals** for full pipeline demo.

### Terminal 1: Start Data Generator
```bash
source .venv/bin/activate
python data-generator/producer.py
```
- Generates a synthetic sale every 2 seconds (`producer.py:71`)
- Prints JSON to console and inserts into SQLite via `put_event()` (`stream/stream.py:24-36`)

### Terminal 2: Run CLI Processor (Optional)
```bash
source .venv/bin/activate
python processor/processor.py
```
Output example:
```
========== CLOUD ANALYTICS ==========
Total Orders      : 42
Total Sales       : ₹1,245,000.00
Average Order     : ₹29,642.86

Sales by City:
  Mumbai: ₹345,000.00
  ...

Sales by Category:
  Electronics: ₹890,000.00
  ...
======================================
```

### Terminal 3: Launch Dashboard
```bash
source .venv/bin/activate
python dashboard/app.py
```
- Starts Flask on `http://0.0.0.0:5000` (`dashboard/app.py:70`)
- Open browser: **http://localhost:5000**
- Dashboard shows 3 KPI cards + Bar (city) + Doughnut (category) charts
- Auto-refreshes every 3 seconds (`index.html:187-189`)

### API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Renders dashboard (`dashboard/app.py:59-61`) |
| `GET` | `/api/analytics` | Returns aggregated JSON (`dashboard/app.py:64-66`) |

Example `GET /api/analytics` response:
```json
{
  "total_orders": 42,
  "total_sales": 1245000,
  "average_order": 29642.85,
  "city_sales": {
    "Mumbai": 345000,
    "Delhi": 280000
  },
  "category_sales": {
    "Electronics": 890000,
    "Accessories": 230000
  }
}
```
Logic: `dashboard/app.py:16-56` and `processor/processor.py:13-60`

##  Docker

Build and run (includes only `dashboard` + `stream` per `Dockerfile:11-13`):

```bash
docker build -t cloud-analytics-dashboard .
docker run -p 5000:5000 cloud-analytics-dashboard
# Open http://localhost:5000
```

> Note: `data-generator` and `processor` are not copied in current Dockerfile. To include them, add:
> ```dockerfile
> COPY data-generator ./data-generator
> COPY processor ./processor
> ```

##   Configuration

No env vars required. Paths are relative:

- DB Path in dashboard: `dashboard/app.py:8-13` → `../stream/events.db`
- DB Path in processor: `processor/processor.py:5-10` → `../stream/events.db`
- DB Path in stream: `stream/stream.py:6` → `stream/events.db`

To reset data:
```bash
rm stream/events.db events.db
python stream/stream.py
```

##   Testing the Stream Directly

```python
from stream.stream import create_stream, put_event, get_events

create_stream()
put_event({"product": "Laptop", "total_amount": 55000, "city": "Pune", "category": "Electronics"})
print(get_events())
```

##  Contributing

1. Fork the repo
2. Create branch: `git checkout -b feature/my-feature`
3. Commit: `git commit -m 'Add my feature'`
4. Push: `git push origin feature/my-feature`
5. Open a Pull Request

## License

MIT License - see `LICENSE` file if present.
Copyright (c) 2026 [ankit-25](https://github.com/ankit-25)

## Author

**Ankit** — [@ankit-25](https://github.com/ankit-25)

- GitHub: [github.com/ankit-25](https://github.com/ankit-25) (5 public repos since 2015)
- Project Repo: `https://github.com/ankit-25/cloud-analytics-dashboard`
- Achievements: Arctic Code Vault Contributor, Pull Shark

## Acknowledgments

- [Faker](https://faker.readthedocs.io/) for synthetic data
- [Flask](https://flask.palletsprojects.com/)
- [Chart.js](https://www.chartjs.org/) for visualization
- Inspired by AWS Kinesis + Real-time Dashboard patterns
