# Build 003B — constrained SQL and real evidence (prototype)

**Scope:** This is a narrow, *local proof-of-concept*, not a production-grade SQL sandbox. It does **not** call an AI model and does **not** connect to Inspect yet.

## What it adds

- `src/evaluation_lab/sql_evidence.py` validates **one simple SELECT** using `sqlglot`, permitting only approved `trials` columns and a small aggregation-function list.
- A separate process loads the trusted synthetic CSV into a named in-memory DuckDB table and **then** disables DuckDB external access before running the submitted SQL.
- A timeout terminates the worker. DuckDB has a memory budget, and result rows/columns are bounded.
- Successful queries create JSONL evidence records containing SQL, returned rows, source-file SHA-256 and a content-derived evidence ID.
- `tests/test_build003b.py` includes positive controls and common unsafe-query attempts.

## Deliberately unsupported

CTEs, joins, subqueries, windows, set operations, arbitrary functions and arbitrary table sources. **Full Kitagawa decomposition queries are not yet supported**; this build validates a simpler period-level aggregate before expanding the SQL interface.

## Security caveats

- Parsing and SQL allowlisting plus DuckDB `enable_external_access=false` reduce exposure but do **not** constitute a hardened operating-system sandbox.
- The *trusted caller* controls CSV and log paths. Do not expose them to the evaluated model.
- The log is not tamper-proof; content-addressed IDs are not signatures. Evidence IDs prove linkage to a recorded tool result, **not** the validity of a narrative interpretation.
- A process timeout and DuckDB memory limit do not guarantee containment of all CPU, filesystem, or resource abuse.
- This implementation has not been run against adversarial untrusted models. Expand only after code review and explicit threat-model tests.

## Local validation

Install a parser (DuckDB should already be installed with Build 001):

```bash
python -m pip install sqlglot
python -m pytest tests/test_build003b.py -v
python -m pytest -q
```

The SQL validator uses `sqlglot` as a **new dependency**. Pin an exact version after verifying compatibility in the local environment and record it in `pyproject.toml`.

## Manual example

Run this **from a .py file** (not `python - <<'PY'`), because Python multiprocessing `spawn` needs an importable `__main__`:

```python
from evaluation_lab.sql_evidence import execute_and_record

if __name__ == "__main__":
    result = execute_and_record(
        "SELECT period, COUNT(*) AS trials, SUM(converted) AS conversions FROM trials GROUP BY period",
        csv_path="/tmp/analytics-ai-lab-demo/public/case_001.csv",
        evidence_path="/tmp/analytics-ai-lab-evidence/build003b.jsonl",
    )
    print(result)
```

**Do not commit generated CSVs, raw evidence logs, hidden manifests or model API secrets.**

## Acceptance criterion

The tests should run on the author's Mac with DuckDB and sqlglot installed; unsafe queries should fail closed, while approved aggregations produce recorded evidence. A green test result does not justify giving this prototype unrestricted model-generated SQL.
