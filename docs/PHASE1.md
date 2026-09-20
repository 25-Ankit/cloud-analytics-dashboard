# Phase 1 — Local-First Deployable Analytics Pipeline

## Deliverables

1. Stream layer with SQLite WAL.
2. Input validation.
3. Incremental processor.
4. Processor checkpoint.
5. Materialized aggregate tables.
6. Flask API.
7. Live dashboard without full-page reload.
8. Configurable data generator.
9. Docker image.
10. Docker Compose stack.
11. Automated tests.
12. Documentation.

## Data flow

```text
producer -> events -> processor -> aggregates -> API -> dashboard
```

The event table remains the source event log. Aggregate tables are derived state.

## Checkpoint model

The processor stores the ID of the latest successfully processed event in:

```text
processor_state.last_event_id
```

A batch is processed inside one database transaction. The checkpoint is advanced only after aggregate updates in that transaction.

## Materialized state

- `analytics_totals`
- `city_sales`
- `category_sales`

The dashboard reads these precomputed aggregates instead of recalculating the entire raw event history on every request.

## Operational model

Docker Compose starts three long-running services:

- `generator`
- `processor`
- `dashboard`

They share a Docker volume containing the SQLite database.

The design is intentionally simple so that the same application can later be moved to another runtime without changing the analytics contract.

## Known Phase 1 limits

SQLite is intentionally used as the local event store for this phase. It is not intended to be treated as a distributed production event broker.

The processor currently runs as a single worker. Scaling to multiple workers requires an explicit concurrency/partitioning design and is therefore deferred.
