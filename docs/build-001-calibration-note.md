# Build 001 — local verification note

**Status:** Partial validation; documentation and test-suite update 21 October 2026. This is an engineering calibration, **not a model benchmark**.

Implemented: deterministic shuffled row-level exact/sampled synthetic data, four conversion scenarios, pandas reference calculation, and separate SQL-based decomposition. SQLite was used to locally execute the SQL reference because DuckDB could not be installed in this runtime (no outbound package registry access).

Local `pytest -q`: **8 passed, 4 skipped**. The skipped tests are the DuckDB-specific comparison checks. Expected exact results were verified for all four scenarios using independent pandas-versus-SQL logic. Seed-repeat equality, changed-seed variation, sampled-case reconciliation, and basic CSV scenario-label leakage checks passed.

**Not yet verified:** DuckDB execution, cross-machine hash equivalence, resource-limited/read-only SQL sandbox, grader challenge suite, model outputs, or statistical-noise interpretation calibration. Those are not Build 001 completion claims.

No model APIs were called and no model performance results were produced. This build did not surface test failures requiring repairs beyond implementation iteration; do not interpret that as proof of bug-free behavior.

Run on a machine with DuckDB installed: `python -m pip install -e '.[dev]' && pytest -q`. All 12 tests should run; investigate any failure rather than modifying expected values to force a pass.

## Follow-up checks (not yet verified on the target Mac)

The test suite now includes: a genuine missing-segment and zero-denominator check; a `summarize_sql` parity check against pandas; and checks for exported filenames and schema columns. These new tests require execution in the user's environment before they can be marked passed.

DuckDB remains **unverified in this runtime**. Do not change this note to claim DuckDB passed without a `pytest -q` run, `python -c "import duckdb; print(duckdb.__version__)"`, and the environment's Python/pandas version recorded. SQL read-only sandbox and timeouts remain future Build 002 work.

Planned offsetting-effects case: a later scenario with small total movement but large, opposing mix and within contributions; **not** included in the initial four-case calibration suite.
