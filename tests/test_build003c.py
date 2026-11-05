"""Build 003C integration tests; no model calls or API keys."""
import copy
import json

import pytest

pytest.importorskip("duckdb")
pytest.importorskip("sqlglot")
pytest.importorskip("inspect_ai")

from evaluation_lab.sql_evidence import execute_and_record
from evals.build003c_pipeline import QUERY, expected_from_evidence, verify_logged_support
from evaluation_lab.grader import DENOMINATOR, METRIC_ID


@pytest.fixture
def evidence(tmp_path):
    csv = tmp_path / "trials.csv"
    lines = ["trial_id,customer_id,period,segment,converted"]
    row_id = 0
    for period in ("2026-08", "2026-09"):
        for segment in ("SMB", "Mid-market", "Enterprise"):
            for outcome in (0, 1):
                row_id += 1
                lines.append(f"t{row_id},c{row_id},{period},{segment},{outcome}")
    csv.write_text("\n".join(lines) + "\n")
    log = tmp_path / "evidence.jsonl"
    record = execute_and_record(QUERY, csv_path=csv, evidence_path=log)
    ref = expected_from_evidence(record, source_path=csv)
    answer = {
        **ref,
        "metric_id": METRIC_ID,
        "denominator": DENOMINATOR,
        "direction": "no_change",
        "evidence_ids": [record["evidence_id"]],
        "explanation": "Scripted test",
    }
    return csv, log, record, answer


def test_real_logged_rows_support_correct_claim(evidence):
    csv, log, _, answer = evidence
    assert verify_logged_support(json.dumps(answer), evidence_path=log, source_path=csv)


def test_wrong_number_not_supported(evidence):
    csv, log, _, answer = evidence
    answer["mix_pp"] += 1
    assert not verify_logged_support(json.dumps(answer), evidence_path=log, source_path=csv)


def test_forged_evidence_id_not_supported(evidence):
    csv, log, _, answer = evidence
    answer["evidence_ids"] = ["sql_forged"]
    assert not verify_logged_support(json.dumps(answer), evidence_path=log, source_path=csv)


def test_tampered_logged_row_rejected(evidence):
    csv, log, record, _ = evidence
    altered = copy.deepcopy(record)
    altered["rows"][0]["conversions"] += 1
    log.write_text(json.dumps(altered) + "\n")
    with pytest.raises(ValueError, match="Evidence ID"):
        expected_from_evidence(json.loads(log.read_text()), source_path=csv)


def test_wrong_source_hash_rejected(evidence):
    csv, _, record, _ = evidence
    csv.write_text(csv.read_text().replace(",0\n", ",1\n", 1))
    with pytest.raises(ValueError, match="source hash"):
        expected_from_evidence(record, source_path=csv)
