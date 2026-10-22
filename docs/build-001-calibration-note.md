# Build 001 — local verification note

**Status:** Partial validation, 21 October 2026. This is an engineering calibration, **not a model benchmark**.

Implemented: deterministic shuffled row-level exact/sampled synthetic data, four conversion scenarios, pandas reference calculation, and separate SQL-based decomposition. SQLite was used to locally execute the SQL reference because DuckDB could not be installed in this runtime (no outbound package registry access).

Local `pytest -q`: **8 passed, 4 skipped**. The skipped tests are the DuckDB-specific comparison checks. Expected exact results were verified for all four scenarios using independent pandas-versus-SQL logic. Seed-repeat equality, changed-seed variation, sampled-case reconciliation, and basic CSV scenario-label leakage checks passed.

**Not yet verified:** DuckDB execution, cross-machine hash equivalence, resource-limited/read-only SQL sandbox, grader challenge suite, model outputs, or statistical-noise interpretation calibration. Those are not Build 001 completion claims.

No model APIs were called and no model performance results were produced. This build did not surface test failures requiring repairs beyond implementation iteration; do not interpret that as proof of bug-free behavior.

Run on a machine with DuckDB installed: `python -m pip install -e '.[dev]' && pytest -q`. All 12 tests should run; investigate any failure rather than modifying expected values to force a pass.
