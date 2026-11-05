"""Build 003C: no-model SQL -> logged evidence -> independently checked answer.

Use: inspect eval evals/build003c_pipeline.py --model none \\
       --log-dir /tmp/analytics-ai-lab-003c-logs
Requires generated exact CSVs in /tmp/analytics-ai-lab-demo/public.
This is integration calibration, NOT model evaluation or a security certificate.
"""
from __future__ import annotations

import hashlib
import json
import os
import tempfile
from pathlib import Path

import pandas as pd
from inspect_ai import Task, task
from inspect_ai.dataset import Sample
from inspect_ai.model import ModelOutput
from inspect_ai.scorer import CORRECT, INCORRECT, Score, Target, accuracy, scorer
from inspect_ai.solver import Generate, TaskState, solver

from evaluation_lab.grader import DENOMINATOR, METRIC_ID, grade_answer
from evaluation_lab.reference import decompose, summarize_pandas
from evaluation_lab.sql_evidence import execute_and_record

# Only the script, never an AI model, gets the source paths and hidden targets.
# Deliberately narrow query supported by Build 003B: no CTEs or joins.
QUERY = (
    "SELECT period, segment, COUNT(*) AS eligible, "
    "SUM(converted) AS conversions FROM trials "
    "GROUP BY period, segment ORDER BY period, segment"
)
DATA_ROOT = Path(os.environ.get("EVAL_LAB_DATA_ROOT", "/tmp/analytics-ai-lab-demo"))
NUMERIC = ("baseline_rate_pct", "after_rate_pct", "total_change_pp", "mix_pp", "within_pp")


def expected_from_evidence(record: dict, *, source_path: Path) -> dict:
    """Independently derive the five numeric claims from recorded query results.

    This verifier is intentionally scoped to the single known aggregation query.
    It does not generally prove that arbitrary SQL supports arbitrary claims.
    """
    if record.get("sql") != QUERY:
        raise ValueError("Evidence came from an unexpected SQL query")
    expected_hash = hashlib.sha256(source_path.read_bytes()).hexdigest()
    if record.get("source_sha256") != expected_hash:
        raise ValueError("Evidence source hash does not match the trusted CSV")
    rows = record.get("rows")
    if not isinstance(rows, list) or len(rows) != 6 or record.get("row_count") != 6:
        raise ValueError("Expected six aggregated period/segment rows")
    content = {"sql": QUERY, "rows": rows, "source_sha256": expected_hash}
    evidence_id = "sql_" + hashlib.sha256(
        json.dumps(content, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()[:16]
    if evidence_id != record.get("evidence_id"):
        raise ValueError("Evidence ID does not match logged content")
    keys = {(row.get("period"), row.get("segment")) for row in rows}
    if len(keys) != 6 or keys != {
        (period, segment)
        for period in ("2026-08", "2026-09")
        for segment in ("SMB", "Mid-market", "Enterprise")
    }:
        raise ValueError("Expected exactly one row per period/segment")
    for row in rows:
        if set(row) != {"period", "segment", "eligible", "conversions"}:
            raise ValueError("Unexpected aggregate columns")
        n, k = row["eligible"], row["conversions"]
        if (isinstance(n, bool) or not isinstance(n, int) or n <= 0
            or isinstance(k, bool) or not isinstance(k, (int, float))
            or k < 0 or k > n):
            raise ValueError("Invalid aggregate count")
    return decompose(pd.DataFrame(rows))


def verify_logged_support(raw_answer: str, *, evidence_path: Path, source_path: Path) -> bool:
    """Require one genuine logged aggregate, then compare all five claims to it."""
    from evaluation_lab.grader import parse_answer

    answer = parse_answer(raw_answer)
    entries = [json.loads(line) for line in evidence_path.read_text().splitlines()]
    if len(entries) != 1:
        return False
    record = entries[0]
    evidence_values = expected_from_evidence(record, source_path=source_path)
    if answer["evidence_ids"] != [record["evidence_id"]]:
        return False
    return all(abs(answer[key] - evidence_values[key]) <= 0.05000001 for key in NUMERIC)


@solver
def scripted_sql_control():
    async def solve(state: TaskState, generate: Generate) -> TaskState:
        source_path = Path(state.metadata["trusted_csv_path"])
        # An independent evidence file for each scripted sample.
        with tempfile.TemporaryDirectory(prefix="eval-lab-003c-") as tmp:
            evidence_path = Path(tmp) / "evidence.jsonl"
            record = execute_and_record(
                QUERY, csv_path=source_path, evidence_path=evidence_path,
                timeout_seconds=10, max_rows=20,
            )
            reference_from_rows = expected_from_evidence(record, source_path=source_path)
            answer = {
                **reference_from_rows,
                "metric_id": METRIC_ID,
                "denominator": DENOMINATOR,
                "direction": (
                    "increase" if reference_from_rows["total_change_pp"] > 1e-7
                    else "decrease" if reference_from_rows["total_change_pp"] < -1e-7
                    else "no_change"
                ),
                "evidence_ids": [record["evidence_id"]],
                "explanation": "Scripted calibration only; interpretation is not evaluated.",
            }
            if state.metadata["control"] == "wrong_denominator":
                answer["denominator"] = "all_website_visitors"
            elif state.metadata["control"] == "wrong_number":
                answer["mix_pp"] += 1.0
            elif state.metadata["control"] != "correct":
                raise ValueError("Unknown control")
            raw = json.dumps(answer)
            # Read evidence back from the file, not just from the in-memory record.
            state.metadata["real_evidence_id"] = record["evidence_id"]
            state.metadata["backed_by_log"] = verify_logged_support(
                raw, evidence_path=evidence_path, source_path=source_path
            )
            state.metadata["evidence_record"] = record
            state.output = ModelOutput.from_content(model="scripted-sql/no-model", content=raw)
        return state
    return solve


@scorer(metrics=[accuracy()])
def sql_evidence_grader():
    async def score(state: TaskState, target: Target) -> Score:
        reference = json.loads(target.text)
        grade = grade_answer(
            state.output.completion, reference,
            available_evidence_ids={state.metadata["real_evidence_id"]},
        )
        evidence_supported = state.metadata["backed_by_log"]
        passed = grade["correct"] and evidence_supported
        return Score(
            value=CORRECT if passed else INCORRECT,
            answer=state.output.completion,
            explanation=json.dumps({"grade": grade, "supported_by_logged_rows": evidence_supported}),
            metadata={
                "control": state.metadata["control"],
                "expected_pass": state.metadata["control"] == "correct",
                "evidence_id": state.metadata["real_evidence_id"],
                "source_sha256": state.metadata["evidence_record"]["source_sha256"],
            },
        )
    return score


@task
def build003c_pipeline() -> Task:
    samples = []
    for number in range(1, 5):
        case = f"case_{number:03d}"
        csv_path = (DATA_ROOT / "public" / f"{case}.csv").resolve(strict=True)
        reference = decompose(summarize_pandas(pd.read_csv(csv_path)))
        for control in ("correct", "wrong_denominator", "wrong_number"):
            samples.append(Sample(
                id=f"{case}-{control}",
                input="Calibration-only: quantify conversion change and segment mix/within contributions.",
                target=json.dumps(reference),
                metadata={"trusted_csv_path": str(csv_path), "control": control},
            ))
    return Task(dataset=samples, solver=scripted_sql_control(), scorer=sql_evidence_grader())
