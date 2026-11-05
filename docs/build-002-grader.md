# Build 002 — Deterministic Grader and Challenge Suite

**Status:** implemented locally; validate in your own environment before claiming complete instrument calibration.

## Scope

The grader takes (1) a strict JSON answer, (2) independently computed reference values, and (3) IDs of actual permitted SQL executions from a trusted log. It reports an overall mechanical pass/fail and per-check reasons. Its inputs are separate from model prompts; never expose the reference object to an evaluated model.

Required JSON fields: `baseline_rate_pct`, `after_rate_pct`, `total_change_pp`, `mix_pp`, `within_pp`, `metric_id`, `denominator`, `direction`, `evidence_ids`, `explanation`.

- `metric_id`: `trial_to_paid_30d_conversion_rate`
- `denominator`: `eligible_trial_customers`
- `direction`: `increase`, `decrease`, or `no_change`
- Numerical units: percent for rates, **percentage points** for changes and contributions.
- Numeric tolerance: **±0.05000001 pp**, a deliberately provisional rounding tolerance for one-decimal outputs. Freeze before scored model runs.
- Direction deadband: **1e-7 pp** for exact fixture arithmetic. **Not** a statistical significance threshold.

## What is checked automatically

Valid JSON, unique keys, required fields, field types, finite numbers, correct metric and denominator labels, reference agreement for each numeric field, additivity of contributions, direction, and existence of cited IDs in a trusted evidence log. All curated positive controls must pass, and all curated negative controls must fail.

The grader **does not** determine that narrative explanations are supported, that the correct SQL was used, or that a causal claim is valid. Existence of an evidence ID only checks trace linkage, not relevance. An answer with nonempty narrative receives `needs_human_review: true`. Never describe that as an automated evidence-quality pass.

## Challenge categories

The automated suite includes altered denominators and metric labels, wrong totals and component allocation, swapped mix and within effects (combined case), wrong direction, fabricated evidence references, malformed JSON, nonfinite or string numbers, duplicate evidence IDs, duplicate JSON keys, and no trusted evidence log. A separate human rubric is needed for right-number/wrong-explanation and unsupported causal claims.

## Run

```bash
python -m pytest -q tests/test_build002.py
python -m pytest -q
```

## Still required before using model-generated SQL

- Database-level read-only enforcement and restricted file/network access.
- Explicit row/time/memory limits and hostile-query tests.
- Human-label rubric for semantic claims and evidence relevance.
- A frozen scored-run analysis plan, tolerances, case-coverage labels and model configurations.
