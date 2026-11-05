"""Known-correct and known-wrong challenges for Build 002."""
import copy
import json
import pytest

from evaluation_lab.generator import generate_case
from evaluation_lab.grader import (
    DENOMINATOR, METRIC_ID, GradingPolicy, grade_answer, parse_answer,
)
from evaluation_lab.reference import decompose, summarize_pandas
from evaluation_lab.scenarios import SCENARIOS


@pytest.fixture(scope="module", params=SCENARIOS, ids=lambda c: c.identifier)
def example(request):
    case = request.param
    ref = decompose(summarize_pandas(generate_case(case)))
    answer = dict(ref, metric_id=METRIC_ID, denominator=DENOMINATOR,
                  direction="increase" if ref["total_change_pp"] > 1e-7 else "no_change",
                  evidence_ids=["sql_001"], explanation="Verified from the stored SQL output.")
    return ref, answer


def score(answer, ref):
    return grade_answer(json.dumps(answer), ref, available_evidence_ids={"sql_001"})


def test_positive_controls_all_four_scenarios(example):
    ref, answer = example
    outcome = score(answer, ref)
    assert outcome["correct"], outcome
    assert outcome["needs_human_review"]  # Prose is not automatically certified


@pytest.mark.parametrize("corruption,reason", [
    (lambda a: a.update(metric_id="gross_sales"), "metric_definition_mismatch"),
    (lambda a: a.update(denominator="all_visitors"), "metric_definition_mismatch"),
    (lambda a: a.update(total_change_pp=a["total_change_pp"] + 0.3), "incorrect_total_change_pp"),
    (lambda a: a.update(direction="decrease" if a["direction"] != "decrease" else "increase"), "wrong_direction"),
    (lambda a: a.update(evidence_ids=["made_up_999"]), "missing_or_unverified_evidence_ids"),
    (lambda a: a.update(mix_pp=a["mix_pp"] + 0.3, within_pp=a["within_pp"] - 0.3), "incorrect_mix_pp"),
])
def test_negative_controls(example, corruption, reason):
    ref, pristine = example
    answer = copy.deepcopy(pristine)
    corruption(answer)
    result = score(answer, ref)
    assert not result["correct"], result
    assert reason in result["reasons"]


def test_swapped_mix_and_within_combined():
    reference = decompose(summarize_pandas(generate_case(SCENARIOS[2])))
    answer = dict(reference, metric_id=METRIC_ID, denominator=DENOMINATOR,
                  direction="increase", evidence_ids=["sql_001"], explanation="")
    answer["mix_pp"], answer["within_pp"] = answer["within_pp"], answer["mix_pp"]
    result = score(answer, reference)
    assert not result["correct"]
    assert "incorrect_mix_pp" in result["reasons"]


@pytest.mark.parametrize("raw", [
    "not json", "[]", "{}", '{"mix_pp": NaN}', '{"x": 1, "x": 2}',
])
def test_invalid_json_or_shape_rejected(raw):
    ref = decompose(summarize_pandas(generate_case(SCENARIOS[0])))
    result = grade_answer(raw, ref, available_evidence_ids={"sql_001"})
    assert not result["correct"]
    assert result["checks"] == {"schema": False}


def test_invalid_numeric_and_duplicate_evidence(example):
    ref, answer = example
    for key, value in [("mix_pp", True), ("mix_pp", "1.4"), ("evidence_ids", ["sql_001", "sql_001"])]:
        bad = dict(answer, **{key: value})
        assert not score(bad, ref)["correct"]


def test_no_evidence_log_not_a_pass(example):
    ref, answer = example
    assert not grade_answer(answer, ref)["correct"]


def test_rounding_tolerance_declared(example):
    ref, answer = example
    rounded = dict(answer)
    for key in ("baseline_rate_pct", "after_rate_pct", "total_change_pp", "mix_pp", "within_pp"):
        rounded[key] = round(rounded[key], 1)
    assert score(rounded, ref)["correct"]


def test_magnitude_cannot_hide_bad_definition(example):
    ref, answer = example
    answer = dict(answer, denominator="total_accounts")
    assert not score(answer, ref)["correct"]


def test_parser_rejects_extra_fields(example):
    _, answer = example
    with pytest.raises(ValueError):
        parse_answer(dict(answer, hidden_truth="pure_mix"))
