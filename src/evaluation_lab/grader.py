"""Build 002: deterministic scoring of structured conversion-decomposition answers.

Not a semantic/causal or safety certificate. Never expose reference values to a model.
"""
from __future__ import annotations

import json
import math
from dataclasses import dataclass
from typing import Mapping

NUMERIC_FIELDS = (
    "baseline_rate_pct", "after_rate_pct", "total_change_pp", "mix_pp", "within_pp"
)
REQUIRED_FIELDS = set(NUMERIC_FIELDS) | {
    "metric_id", "denominator", "direction", "evidence_ids", "explanation"
}
METRIC_ID = "trial_to_paid_30d_conversion_rate"
DENOMINATOR = "eligible_trial_customers"
DIRECTIONS = {"increase", "decrease", "no_change"}


@dataclass(frozen=True)
class GradingPolicy:
    # +/- 0.05 percentage points permits one-decimal display rounding.
    numeric_tolerance_pp: float = 0.05000001
    # Operational classification of *observed* change, not a statistical test.
    direction_deadband_pp: float = 0.0000001
    require_evidence: bool = True


def _reject_constant(value: str):
    raise ValueError(f"Non-finite JSON constant: {value}")


def _unique_pairs(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise ValueError(f"Duplicate JSON key: {key}")
        out[key] = value
    return out


def parse_answer(raw: str | Mapping) -> dict:
    """Validate schema, types and finite numbers; raise ValueError on invalid input.

    A Mapping is intended for test fixtures only; live models must send JSON text.
    """
    try:
        obj = json.loads(raw, parse_constant=_reject_constant,
                         object_pairs_hook=_unique_pairs) if isinstance(raw, str) else raw
    except (json.JSONDecodeError, ValueError, TypeError) as exc:
        raise ValueError(f"Invalid JSON: {exc}") from exc
    if not isinstance(obj, Mapping):
        raise ValueError("Top-level answer must be a JSON object")
    missing = REQUIRED_FIELDS - obj.keys()
    extra = obj.keys() - REQUIRED_FIELDS
    if missing:
        raise ValueError(f"Missing required fields: {', '.join(sorted(missing))}")
    if extra:
        raise ValueError(f"Unexpected fields: {', '.join(sorted(extra))}")
    for field in NUMERIC_FIELDS:
        number = obj[field]
        if isinstance(number, bool) or not isinstance(number, (int, float)) or not math.isfinite(number):
            raise ValueError(f"{field} must be a finite JSON number")
    for field in ("metric_id", "denominator", "direction", "explanation"):
        if not isinstance(obj[field], str):
            raise ValueError(f"{field} must be a string")
    if obj["direction"] not in DIRECTIONS:
        raise ValueError("direction must be increase, decrease, or no_change")
    ids = obj["evidence_ids"]
    if not isinstance(ids, list) or any(not isinstance(item, str) or not item for item in ids):
        raise ValueError("evidence_ids must be a list of nonempty strings")
    if len(ids) != len(set(ids)):
        raise ValueError("evidence_ids must be unique")
    return dict(obj)


def expected_direction(delta: float, deadband: float) -> str:
    if abs(delta) <= deadband:
        return "no_change"
    return "increase" if delta > 0 else "decrease"


def grade_answer(raw: str | Mapping, reference: Mapping[str, float], *,
                 available_evidence_ids: set[str] | None = None,
                 policy: GradingPolicy = GradingPolicy()) -> dict:
    """Return an auditable per-dimension grade, never crash on malformed responses.

    `available_evidence_ids` must come from the trusted tool-execution log, not the
    model's answer. ID existence is NOT evidence relevance or claim support.
    """
    reasons = []
    try:
        answer = parse_answer(raw)
    except (ValueError, TypeError) as exc:
        return {"correct": False, "checks": {"schema": False},
                "reasons": [f"invalid_schema: {exc}"], "needs_human_review": False}

    checks = {"schema": True}
    checks["metric_definition"] = answer["metric_id"] == METRIC_ID and answer["denominator"] == DENOMINATOR
    if not checks["metric_definition"]:
        reasons.append("metric_definition_mismatch")

    for key in NUMERIC_FIELDS:
        if key not in reference or not isinstance(reference[key], (int, float)) or not math.isfinite(reference[key]):
            raise ValueError(f"Invalid trusted reference: {key}")
        good = abs(answer[key] - reference[key]) <= policy.numeric_tolerance_pp
        checks[key] = good
        if not good:
            reasons.append(f"incorrect_{key}")

    checks["decomposition_identity"] = abs(
        answer["mix_pp"] + answer["within_pp"] - answer["total_change_pp"]
    ) <= policy.numeric_tolerance_pp
    if not checks["decomposition_identity"]:
        reasons.append("decomposition_does_not_reconcile")

    checks["direction"] = answer["direction"] == expected_direction(
        reference["total_change_pp"], policy.direction_deadband_pp)
    if not checks["direction"]:
        reasons.append("wrong_direction")

    ids = answer["evidence_ids"]
    checks["evidence_ids"] = (not policy.require_evidence or bool(ids)) and (
        available_evidence_ids is not None and all(e in available_evidence_ids for e in ids)
    )
    if not checks["evidence_ids"]:
        reasons.append("missing_or_unverified_evidence_ids")

    # Claim relevance, causal overreach and narrative contradictions need a rubric.
    # We never mark them automatically 'verified' from ID existence alone.
    return {"correct": all(checks.values()), "checks": checks,
            "reasons": reasons, "needs_human_review": bool(answer["explanation"].strip())}
