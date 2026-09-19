# Experiments

Run:

```bash
python -m benchmarks.benchmark --events 5000
```

The benchmark records:

- workload size
- one full SQL aggregation timing
- incremental processor timing
- number of events processed
- resulting aggregate snapshot

Results are written to `benchmarks/results/latest.json`, which is ignored by Git so local measurements do not become source-of-truth repository data.

The benchmark is an engineering smoke experiment, not a statistical performance study. For rigorous comparisons, repeat workloads, control hardware, warm/cold caches, and report distributions.
