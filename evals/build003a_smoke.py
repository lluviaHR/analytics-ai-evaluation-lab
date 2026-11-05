"""Build 003A: model-free Inspect integration smoke test.

Scripted correct/wrong answers calibrate the orchestration adapter only.
No model, generated SQL, tool execution or real evidence is involved.
"""
from __future__ import annotations

import json

from inspect_ai import Task, task
from inspect_ai.dataset import Sample
from inspect_ai.model import ModelOutput
from inspect_ai.scorer import CORRECT, INCORRECT, Score, Target, accuracy, scorer
from inspect_ai.solver import Generate, TaskState, solver

from evaluation_lab.generator import generate_case
from evaluation_lab.grader import DENOMINATOR, METRIC_ID, grade_answer
from evaluation_lab.reference import decompose, summarize_pandas
from evaluation_lab.scenarios import SCENARIOS


@solver
def scripted_control():
    """Place a prewritten response in the output slot; never call a model."""

    async def solve(state: TaskState, generate: Generate) -> TaskState:
        payload = state.metadata["scripted_answer"]
        state.output = ModelOutput.from_content(
            model="build003a/scripted-control", content=json.dumps(payload)
        )
        return state

    return solve


@scorer(metrics=[accuracy()])
def conversion_grader():
    """Adapt the Build 002 grader to Inspect's Score contract."""

    async def score(state: TaskState, target: Target) -> Score:
        # Reference is held in Inspect's target, not in the presented question.
        # There are no evaluated models in this smoke test.
        reference = json.loads(target.text)
        result = grade_answer(
            state.output.completion,
            reference,
            available_evidence_ids=set(state.metadata["trusted_evidence_ids"]),
        )
        return Score(
            value=CORRECT if result["correct"] else INCORRECT,
            answer=state.output.completion,
            explanation=json.dumps(result, sort_keys=True),
            metadata={"control_expected_to_pass": state.metadata["expected_to_pass"]},
        )

    return score


@task
def build003a_smoke() -> Task:
    samples = []
    for case in SCENARIOS:
        reference = decompose(summarize_pandas(generate_case(case)))
        good_answer = {
            **reference,
            "metric_id": METRIC_ID,
            "denominator": DENOMINATOR,
            "direction": (
                "increase" if reference["total_change_pp"] > 1e-7
                else "decrease" if reference["total_change_pp"] < -1e-7
                else "no_change"
            ),
            "evidence_ids": ["sql_001"],
            "explanation": "Scripted calibration answer; not evidence-backed analysis.",
        }
        bad_answer = {**good_answer, "denominator": "all_website_visitors"}
        for label, answer, expected_pass in (
            ("correct", good_answer, True),
            ("wrong_denominator", bad_answer, False),
        ):
            samples.append(
                Sample(
                    id=f"{case.identifier}-{label}",
                    input=(
                        "Calibration-only: identify conversion change and "
                        "mix vs within-segment contribution."
                    ),
                    target=json.dumps(reference),
                    metadata={
                        "scripted_answer": answer,
                        "trusted_evidence_ids": ["sql_001"],
                        "expected_to_pass": expected_pass,
                    },
                )
            )
    return Task(dataset=samples, solver=scripted_control(), scorer=conversion_grader())
