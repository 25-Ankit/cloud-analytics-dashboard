# Architecture

## Layers

1. **Stream** — durable local event log backed by SQLite/WAL.
2. **Processor** — checkpointed incremental materialization.
3. **Runtime + Policy** — validates/authorizes events before ingestion.
4. **SDK** — stable event and extension contracts.
5. **Adapters** — example integrations for e-commerce, fitness, and library workloads.
6. **API/Dashboard** — reads derived state only.
7. **Benchmarks** — reproducible measurements for full rescan versus incremental processing.

## Transaction invariant

For every processor batch:

```text
read new events
    ↓
update materialized aggregates
    ↓
advance checkpoint
    ↓
COMMIT
```

The checkpoint is never advanced in a separate connection. If the transaction fails, aggregate changes and checkpoint changes roll back together.

## Deployment

Docker Compose runs generator, processor, and dashboard against one persistent volume. The application itself has no cloud-provider dependency.
