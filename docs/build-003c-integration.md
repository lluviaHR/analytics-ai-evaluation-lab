# Build 003C — Model-free, real-evidence integration

**Status:** Prepared for local verification. Not a scored model evaluation.

This Inspect AI task runs 12 scripted controls: for each of the four exact conversion benchmark CSVs, one correct answer, one incorrect denominator, and one incorrect mix contribution. The solver invokes the restricted Build 003B SQL executor and records one real aggregation to a temporary JSONL evidence log. It recomputes decomposition values from the **logged aggregation rows**, separately from the reference values in Inspect's target. The scorer requires both the existing Build 002 grade and a numerical comparison against those logged rows.

Expected: **12 samples, four accepted and eight rejected**; Inspect's pass fraction is ~0.333. This is an intentionally planted control ratio, **not an AI accuracy measurement**. No AI model is used, and no API keys are required.

## Run locally

First, from the repository root with `eval-lab` activated, confirm the four exact CSVs are present from Build 001:

```bash
ls /tmp/analytics-ai-lab-demo/public/case_*.csv
python -m pytest tests/test_build003c.py -v
python -m pytest -q
inspect eval evals/build003c_pipeline.py --model none --log-dir /tmp/analytics-ai-lab-003c-logs
inspect view --log-dir /tmp/analytics-ai-lab-003c-logs
```

Use `EVAL_LAB_DATA_ROOT=/path/to/generated` when using another generated dataset root; don't expose a private manifest as model context. Inspect logs may include **sample targets, dataset paths, SQL and evidence rows**. Keep logs outside the public repository and never publish a scored-run log with hidden targets accessible to evaluated models.

## What this checks

- The SQL aggregates **actual data** from one permitted `trials` table using the existing executor.
- The returned evidence carries the source SHA-256, SQL, six aggregation rows, and a deterministic content-derived ID.
- The verifier reloads the evidence log and rejects mismatched IDs, source hashes, structural anomalies, and incorrect numeric claims; it derives decomposition values from aggregate counts.
- The Build 002 grader separately rejects incorrect metric definitions and reference values.
- Inspect records each control and its score.

## What this does **not** establish

- No LLM-generated SQL, model reasoning, model accuracy, or production safety is tested here.
- The evidence verifier supports **only the frozen aggregation query**; it is not a general proof that arbitrary SQL supports arbitrary analytical narratives.
- The SHA-256-based evidence ID protects against accidental or naive alteration, **not a malicious actor who can rewrite the evidence log and recalculate hashes**. Protect evidence storage and process boundaries separately.
- A numeric answer supported by logged rows does not establish causal interpretation or narrative truth.
- The Build 003B SQL executor is a restricted prototype, **not** a robust security sandbox for hostile SQL. Before permitting an AI model to execute SQL, revisit process isolation, file/path trust boundaries, parser allowlist bypasses, resource quotas, output budgets, and any remaining sandbox controls.

## Note on the benchmark mapping

The scenario-to-result mapping is used only in this model-free calibration task. Future scored evaluations must keep hidden targets inaccessible to evaluated agents. Publishing these calibration cases makes them unsuitable as novel held-out test cases.
