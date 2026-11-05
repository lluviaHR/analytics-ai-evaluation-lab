"""Build 003B: a deliberately narrow SQL/evidence prototype.

Not a production security boundary. The worker process reads only one named
synthetic CSV. User SQL is parsed and restricted to simple SELECT aggregations.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


class QueryRejected(ValueError):
    """SQL did not satisfy the narrow query contract."""


class QueryExecutionError(RuntimeError):
    """The query failed or exceeded its execution budget."""


_COLUMNS = {"period", "segment", "trial_id", "customer_id", "converted"}
_FUNCTIONS = {"COUNT", "SUM", "AVG", "ROUND", "MIN", "MAX"}


def validate_sql(sql: str) -> None:
    """Fail closed unless SQL is one simple SELECT on the trials table."""
    from sqlglot import exp, parse

    if not isinstance(sql, str) or not sql.strip() or len(sql) > 4000:
        raise QueryRejected("SQL must be nonempty and at most 4000 characters.")
    try:
        statements = parse(sql, read="duckdb")
    except Exception as exc:
        raise QueryRejected("Invalid SQL.") from exc

    if len(statements) != 1 or not isinstance(statements[0], exp.Select):
        raise QueryRejected("Only one SELECT statement is allowed.")
    statement = statements[0]
    # No joins, subqueries, CTEs, set operations, windows, or source functions.
    disallowed = (
        exp.Join, exp.Subquery, exp.CTE, exp.Union, exp.Intersect,
        exp.Except, exp.Window, exp.Command, exp.Insert, exp.Update,
        exp.Delete, exp.Create, exp.Drop, exp.Alter,
    )
    for node in statement.walk():
        if isinstance(node, disallowed):
            raise QueryRejected("Complex statements are not supported in 003B.")
    if len(list(statement.find_all(exp.Select))) != 1:
        raise QueryRejected("Nested SELECT is not supported.")
    tables = list(statement.find_all(exp.Table))
    if len(tables) != 1 or tables[0].name.lower() != "trials":
        raise QueryRejected("Only the approved 'trials' table is accessible.")
    if tables[0].args.get("db") or tables[0].args.get("catalog"):
        raise QueryRejected("Qualified table names are not allowed.")
    for col in statement.find_all(exp.Column):
        if col.name.lower() not in _COLUMNS:
            raise QueryRejected(f"Column is not approved: {col.name}")
        if col.table and col.table.lower() != "trials":
            raise QueryRejected("Only unqualified columns or trials.column are allowed.")
    for fn in statement.find_all(exp.Func):
        if fn.sql_name().upper() not in _FUNCTIONS:
            raise QueryRejected(f"Function is not approved: {fn.sql_name()}")
    if any(isinstance(node, exp.Star) for node in statement.walk()):
        stars = list(statement.find_all(exp.Star))
        for star in stars:
            if not isinstance(star.parent, exp.Count):
                raise QueryRejected("SELECT * is not allowed.")
    # Prevent ORDER BY field positions or aliases from circumventing the
    # permitted column checks? Aliases contain only approved expressions.
    # Output still receives a strict row/column cap.
    if statement.args.get("with_") or statement.args.get("with"):
        raise QueryRejected("CTEs are not supported in 003B.")


def _worker(csv_path: str, sql: str, out: Any, max_rows: int) -> None:
    try:
        import duckdb
        con = duckdb.connect(":memory:", config={"threads": "1", "memory_limit": "256MB"})
        # The CSV load happens before external access is disabled. The model
        # never sees or controls the CSV path.
        con.execute(
            "CREATE TABLE trials AS SELECT trial_id, customer_id, period, segment, converted "
            "FROM read_csv_auto(?)", [csv_path]
        )
        con.execute("SET enable_external_access = false")
        cur = con.execute(sql)
        if len(cur.description) > 20:
            raise QueryExecutionError("Too many result columns.")
        rows = cur.fetchmany(max_rows + 1)
        if len(rows) > max_rows:
            raise QueryExecutionError("Result row limit exceeded.")
        column_names = [d[0] for d in cur.description]
        result = [dict(zip(column_names, r)) for r in rows]
        # JSON serialization converts database scalar types; non-JSON types
        # are intentionally stringified for the prototype.
        out.put(("ok", json.loads(json.dumps(result, default=str))))
        con.close()
    except Exception as exc:
        out.put(("error", f"{type(exc).__name__}: {exc}"))


def execute_and_record(
    sql: str,
    *,
    csv_path: str | Path,
    evidence_path: str | Path,
    timeout_seconds: float = 5,
    max_rows: int = 100,
) -> dict[str, Any]:
    """Run permitted SQL in a time-limited child and append real evidence.

    The caller, never the model, must provide the trusted CSV and evidence
    locations. Append-only is an application convention, not tamper-proofing.
    """
    validate_sql(sql)
    csv_path = Path(csv_path).resolve(strict=True)
    if not csv_path.is_file() or csv_path.suffix.lower() != ".csv":
        raise ValueError("Trusted source must be an existing CSV.")
    if not (0 < timeout_seconds <= 30):
        raise ValueError("timeout_seconds must be in (0, 30].")
    if not (0 < max_rows <= 1000):
        raise ValueError("max_rows must be in 1..1000.")

    started = time.monotonic()

    try:
        completed = subprocess.run(
            [sys.executable, "-m", "evaluation_lab.sql_worker"],
            input=json.dumps({
                "csv_path": str(csv_path),
                "sql": sql,
                "max_rows": max_rows,
            }),
            text=True,
            capture_output=True,
            timeout=timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise QueryExecutionError("Query timed out.") from exc

    if completed.returncode != 0:
        raise QueryExecutionError(
            f"Query worker exited with code {completed.returncode}: "
            f"{completed.stderr[-500:]}"
        )

    try:
        status, payload = json.loads(completed.stdout)
    except (ValueError, TypeError) as exc:
        raise QueryExecutionError(
            "Query worker returned an invalid response."
        ) from exc

    if status != "ok":
        raise QueryExecutionError(str(payload))

    record = {
        "sql": sql,
        "rows": payload,
        "row_count": len(payload),
        "duration_ms": round((time.monotonic() - started) * 1000, 2),
        "source_sha256": hashlib.sha256(csv_path.read_bytes()).hexdigest(),
    }
    # This is a content-derived evidence identifier: identical SQL/result/source
    # yields the same ID, independent of execution time.
    content = {"sql": sql, "rows": payload, "source_sha256": record["source_sha256"]}
    record["evidence_id"] = "sql_" + hashlib.sha256(
        json.dumps(content, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()[:16]
    evidence_path = Path(evidence_path)
    evidence_path.parent.mkdir(parents=True, exist_ok=True)
    with evidence_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, sort_keys=True) + "\n")
    return record
