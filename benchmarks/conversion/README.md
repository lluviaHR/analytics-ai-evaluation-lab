# Trial-to-paid conversion decomposition — Build 001

**Status:** Implemented calibration fixtures and reference calculations; not an AI benchmark result.

One eligible trial per synthetic customer, with conversion defined as paid conversion within 30 days of starting a fully matured trial. `period` is cohort start month (2026-08 or 2026-09). Each case has 20,000 trials per period across SMB, Mid-market, Enterprise. There are no real customers.

Four private case specifications are defined in `src/evaluation_lab/scenarios.py` (pure mix, pure within, combined, and exact no-change). **Do not expose that module to a model under test.** Public CSV filenames use opaque case IDs. For a real agent execution, mount only the corresponding CSV and governed analytical definitions, not the full repository.

## Exact expected decomposition (percentage points)

| Case | Baseline | After | Total | Mix | Within |
|---|---:|---:|---:|---:|---:|
| case_001 | 14.5% | 16.0% | +1.5 | +1.5 | 0.0 |
| case_002 | 14.5% | 15.8% | +1.3 | 0.0 | +1.3 |
| case_003 | 14.5% | 17.1% | +2.6 | +1.4 | +1.2 |
| case_004 | 14.5% | 14.5% | 0.0 | 0.0 | 0.0 |

Uses symmetric Kitagawa: mix = sum((w1-w0)*(r0+r1)/2); within = sum((r1-r0)*(w0+w1)/2). All rates and contributions are computed from **observed row-level counts**, including in sampled mode.

## Run

```bash
python -m pip install -e '.[dev]'
python -m evaluation_lab.generator --output data/generated/exact --mode exact
python -m evaluation_lab.generator --output data/generated/sampled --mode sampled --seed 12345
pytest -q
```

The public CSVs contain no explicit scenario labels. The manifest and hashes are stored in the private output folder; the full repository is not an agent-visible workspace. This protects against accidental prompt exposure, not training contamination or indirect inference.

## Limitations

Phase 0 exact data intentionally uses clean integer counts. Do not score models or report model superiority using these calibration fixtures. The sampled mode is a reproducible starting point for future noise calibration, **not** an established practical-significance threshold. Row-level conversion indicators are simulated outcomes; no real conversion timestamps are modeled yet. Dataset hashing assumes identical generator/runtime/serialization versions. Cross-machine bit-identical outputs still require verification in a clean pinned environment.
