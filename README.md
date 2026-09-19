# Cloud Analytics Dashboard — Complete Local-First Project

A cloud-agnostic event analytics platform demonstrating **stream ingestion → policy/runtime → incremental processing → materialized analytics → REST API → live dashboard**, plus benchmarks, an extension SDK, and three application adapters.

No AWS/Azure/GCP account or cloud credentials are required.

## Project phases

| Phase | Included |
|---|---|
| 1 | SQLite/WAL stream, incremental checkpoint processor, API, dashboard, tests, Docker Compose |
| 2 | Full-rescan vs incremental benchmark harness |
| 3 | Runtime + JSON policy engine + rate limiting |
| 4 | Versioned extension SDK + lifecycle runtime |
| 5 | E-commerce, fitness, and library adapters |

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
python scripts/e2e_smoke.py
```

Initialize and run components manually:

```bash
python -m stream.stream
python -m processor.processor
python data-generator/producer.py
python dashboard/app.py
```

Open `http://localhost:5000`.

## Docker

```bash
docker compose up --build
```

Dashboard: `http://localhost:5000`

Stop:

```bash
docker compose down
```

## Benchmark

```bash
python -m benchmarks.benchmark --events 5000
```

## Runtime example

```bash
python -m runtime.demo
```

## Key design property

The processor uses one transaction for aggregate updates and checkpoint advancement. This prevents the SQLite `database is locked` failure that occurs when checkpointing through a second connection while the aggregate transaction is still open.

## Security

Do not commit `.env`, credentials, API keys, private certificates, database files, or runtime logs. `.gitignore` covers common secret/runtime artifacts.

## Documentation

- `docs/ARCHITECTURE.md` — architecture and transaction invariants
- `docs/EXPERIMENTS.md` — benchmark methodology
- `docs/ROADMAP.md` — phases and future work
