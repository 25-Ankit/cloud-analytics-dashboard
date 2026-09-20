# Cloud Analytics Dashboard

A **local-first, cloud-agnostic streaming analytics project** built with Python, SQLite, Flask, Docker, and Docker Compose.

The project demonstrates a small event-driven analytics pipeline without requiring AWS, cloud credentials, or managed cloud services.

## Architecture

```text
                    ┌─────────────────────┐
                    │   Data Generator    │
                    │ random sales events │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   SQLite Event Log  │
                    │      events table   │
                    │        WAL mode     │
                    └──────────┬──────────┘
                               │
                         new events only
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Incremental         │
                    │ Processor            │
                    │ checkpointed batches │
                    └──────────┬──────────┘
                               │
                               ▼
             ┌─────────────────────────────────┐
             │ Materialized Analytics Tables   │
             │ totals / city / category        │
             └────────────────┬────────────────┘
                              │
                              ▼
                    ┌─────────────────────┐
                    │ Flask REST API      │
                    │ /api/analytics      │
                    │ /api/health         │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Live Web Dashboard  │
                    │ Chart.js polling    │
                    └─────────────────────┘
```

## Phase 1 goals

- SQLite-backed event stream
- WAL mode for better concurrent read/write behavior
- Basic event validation
- Incremental processing instead of rescanning the whole event table
- Durable processor checkpoint
- Materialized aggregate tables
- REST API
- Live dashboard updates without page reloads
- Configurable environment variables
- Docker image
- Docker Compose for the complete local stack
- Automated tests
- No cloud-provider lock-in

## Run locally

Create an environment if desired:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Initialize the database:

```bash
python -m stream.stream
```

Start the processor:

```bash
python -m processor.processor
```

In another terminal, start the generator:

```bash
python data-generator/producer.py
```

In another terminal, start the dashboard:

```bash
python dashboard/app.py
```

Open:

```text
http://localhost:5000
```

## Run tests

```bash
pytest -q
```

## Docker Compose

```bash
docker compose up --build
```

Then open:

```text
http://localhost:5000
```

Stop:

```bash
docker compose down
```

## API

### Health

```text
GET /api/health
```

### Analytics snapshot

```text
GET /api/analytics
```

### City aggregates

```text
GET /api/analytics/cities
```

### Category aggregates

```text
GET /api/analytics/categories
```

## Configuration

Copy `.env.example` to `.env` if you want local environment configuration.

Important variables:

- `ANALYTICS_DB_PATH`
- `PROCESSOR_INTERVAL`
- `PROCESSOR_BATCH_SIZE`
- `GENERATOR_INTERVAL`

No credentials are required.

## Why incremental processing?

The original implementation repeatedly scanned the complete event table to calculate totals. That becomes increasingly expensive as the event history grows.

Phase 1 introduces a processor checkpoint:

```text
last_event_id
```

Each processor run reads only:

```text
events WHERE id > last_event_id
```

and updates materialized aggregates. This makes the processing model incremental and gives the project a foundation for later scaling.

## Phase 1 scope

This phase intentionally stays local-first.

It does **not** require:

- AWS
- Azure
- Google Cloud
- Kubernetes
- Terraform
- managed queues
- cloud databases
- cloud credentials

Those can be evaluated in later phases after the local architecture and experiments are stable.

## Security

Do not commit:

- `.env` files
- database files
- logs
- credentials
- API keys
- private certificates

The repository's `.gitignore` excludes common runtime and secret files.
