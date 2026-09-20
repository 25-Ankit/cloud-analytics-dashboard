# Project Roadmap

## Phase 1 — Local-first foundation
- [x] Better stream
- [x] Incremental processor
- [x] Checkpoint
- [x] Materialized analytics
- [x] API
- [x] Live dashboard
- [x] Tests
- [x] Docker Compose

## Phase 2 — Experimental results
- benchmark full rescan vs incremental processing
- measure throughput
- measure processing latency
- measure API latency
- document resource usage
- define reproducible workloads

## Phase 3 — Runtime + Policy Engine
- define runtime interfaces
- policy/configuration model
- failure handling
- observability

## Phase 4 — Extension SDK
- stable event schema
- extension interface
- versioning
- compatibility tests

## Phase 5 — Multiple real applications
- integrate additional real-world workloads
- compare extension behavior
- document deployment patterns

## Cloud migration is optional

Cloud infrastructure should be evaluated after local benchmarks and architecture decisions, rather than introducing provider-specific services into the foundation prematurely.
