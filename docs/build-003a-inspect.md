# Build 003A — Inspect AI integration smoke test

**Purpose:** Verify that Inspect can run a dataset, a custom model-free solver and the existing Build 002 grader, and write evaluation logs.

**Not an AI evaluation.** The eight answers are scripted: four known-correct and four known-wrong. They are deliberately constructed by the fixture code from reference data. `sql_001` is a *placeholder* evidence ID, not a verified SQL result. Consequently no accuracy rate reported by this smoke run should appear as AI model performance. This is a wiring check only.

## Local setup (Mac, existing `eval-lab` Conda environment)

From the root of `analytics-ai-evaluation-lab`:

```bash
conda activate eval-lab
python -m pip install inspect-ai
python -m pip show inspect-ai
inspect eval evals/build003a_smoke.py --model none --log-dir /tmp/analytics-ai-lab-inspect-logs
```

Expected shape: eight samples, with four marked correct and four marked incorrect. A displayed accuracy of 50% is **intentional calibration composition**, not a model result. Inspect's command and API may evolve; record the installed Inspect version with the run.

View the records using:

```bash
inspect view --log-dir /tmp/analytics-ai-lab-inspect-logs
```

If a command fails, capture the exact error before changing source code. No generated SQL, network model provider, API keys or safe execution layer is involved in this step.

## Next gates

1. Verify actual Inspect run completes; record version and observed scores.
2. Add assertions that inspect scores match the expected labels, rather than relying only on aggregate 50% accuracy.
3. Build controlled read-only SQL execution and bind evidence IDs to actual tool logs before live model experiments.
4. Remove scripted fixtures from the model-facing task and keep private reference answers inaccessible to evaluated models.

**Engineering choice:** This integration is isolated under `evals/` and does not change Build 001 or Build 002 interfaces or the existing GitHub Actions dependency set.
