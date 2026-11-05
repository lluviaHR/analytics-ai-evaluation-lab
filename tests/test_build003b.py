"""Build 003B regression and security-controls tests (run on Mac with deps)."""
import json

import pytest

pytest.importorskip("duckdb")
pytest.importorskip("sqlglot")

from evaluation_lab.sql_evidence import (
    QueryExecutionError, QueryRejected, execute_and_record, validate_sql,
)


@pytest.fixture
def source(tmp_path):
    csv = tmp_path / "trials.csv"
    csv.write_text(
        "trial_id,customer_id,period,segment,converted\n"
        "1,1,2026-08,SMB,0\n"
        "2,2,2026-08,SMB,1\n"
        "3,3,2026-09,Enterprise,1\n",
        encoding="utf-8",
    )
    return csv


@pytest.mark.parametrize(
    "sql",
    [
        "DROP TABLE trials",
        "DELETE FROM trials",
        "UPDATE trials SET converted = 0",
        "SELECT * FROM trials",
        "SELECT period FROM read_csv_auto('/tmp/private/manifest.json')",
        "SELECT * FROM '/etc/passwd'",
        "SELECT * FROM trials; SELECT * FROM trials",
        "SELECT current_setting('home_directory') FROM trials",
        "SELECT read_text('/etc/passwd') FROM trials",
        "SELECT period FROM trials JOIN other USING (period)",
        "SELECT period FROM trials UNION SELECT period FROM trials",
        "WITH t AS (SELECT * FROM trials) SELECT period FROM t",
        "SELECT (SELECT COUNT(*) FROM trials) FROM trials",
        "PRAGMA database_list",
        "ATTACH '/tmp/something.db' AS other",
        "COPY trials TO '/tmp/leak.csv'",
    ],
)
def test_unsafe_sql_rejected(sql):
    with pytest.raises(QueryRejected):
        validate_sql(sql)


def test_real_aggregate_and_provenance(source, tmp_path):
    query = "SELECT period, COUNT(*) AS trials, SUM(converted) AS conversions FROM trials GROUP BY period"
    log = tmp_path / "evidence.jsonl"
    first = execute_and_record(query, csv_path=source, evidence_path=log)
    by_period = {r["period"]: r for r in first["rows"]}
    assert by_period["2026-08"]["trials"] == 2
    assert by_period["2026-08"]["conversions"] == 1
    assert by_period["2026-09"]["conversions"] == 1
    assert first["evidence_id"].startswith("sql_")
    assert len(log.read_text().splitlines()) == 1
    assert json.loads(log.read_text().splitlines()[0])["evidence_id"] == first["evidence_id"]
    second = execute_and_record(query, csv_path=source, evidence_path=log)
    assert first["evidence_id"] == second["evidence_id"]


def test_reject_result_row_cap(source, tmp_path):
    with pytest.raises(QueryExecutionError, match="Result row limit"):
        execute_and_record(
            "SELECT trial_id FROM trials",
            csv_path=source,
            evidence_path=tmp_path / "audit.jsonl",
            max_rows=1,
        )


def test_unknown_column_rejected():
    with pytest.raises(QueryRejected):
        validate_sql("SELECT private_label FROM trials")


def test_private_manifest_is_not_a_source(tmp_path):
    manifest = tmp_path / "manifest.json"
    manifest.write_text("{}")
    with pytest.raises(ValueError):
        execute_and_record(
            "SELECT COUNT(*) FROM trials",
            csv_path=manifest,
            evidence_path=tmp_path / "log.jsonl",
        )
