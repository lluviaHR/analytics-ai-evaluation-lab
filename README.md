# Analytics AI Evaluation Lab

**Status:** Design v0.3 · Phase 0 instrument calibration in progress · 21 October 2026  
**License:** Not yet selected. **Do not assume reuse permissions until a license is added.**

> **Central question:** Which AI models and analytical workflows can be trusted to produce accurate, evidence-backed business insights, under what conditions, with what human oversight, and at what cost?

Analytics AI Evaluation Lab is a proposed, vendor-neutral evaluation environment for AI-powered analytics. It evaluates **configurations**, not model brands in isolation: model/deployment + business context + authorized tools + validation + evidence and review policy. The project aims to show *why* configurations succeed or fail through inspectable SQL, executed results, reference answers and investigation traces.

**Principle:** An AI-generated explanation is a hypothesis until evidence supports it.

## At a glance

**What:** An open-source lab for reproducible, evidence-backed evaluation of AI analytics workflows.

**Status:** Phase 0 instrument calibration underway; no AI model performance results published.

**Next:** Complete DuckDB verification, the known-wrong grader suite, and SQL safety tests before Arm A runs.

## Current focus

- **First benchmark:** can an AI analyst attribute a change in a conversion rate to customer mix vs. within-segment behavior, and can the evaluation system detect when it gets that wrong?
- **Design:** compare three architectures on identical cases: generated SQL, approved analytical tools, and a hybrid. Governed context is held constant.
- **Status:** Phase 0 (verify the evaluation instrument) in progress. No model has been scored and no performance claims exist.

## Who it is for

**Primary:** analytics engineers, data scientists and technical AI practitioners who need reproducible runs, auditable SQL, metric-definition tests and failure analysis. **Secondary:** analytics and data leaders who need evidence-based guidance about where human oversight remains necessary. Each research report will include **“What this means for adopting AI in analytics.”** There will not be a separate executive application for the MVP.

## Two capabilities and a shared trust lens

1. **Analytical correctness:** business questions, governed metrics, SQL, numerical/semantic correctness, ambiguity and uncertainty.
2. **Evidence-based investigation:** injected discrepancies, diagnostic SQL, verified vs. hypothetical causes, misleading decoys and reviewable evidence.
3. **Trust lens applied to both:** confidently wrong claims, evidence integrity, security, repeatability, latency, cost and human oversight.

## Planned public releases

- **Release 01 — Engineering foundation:** “Here's how we built and verified our evaluation framework.” Phase 0 verifies the conversion-decomposition dataset, reference computations, and grader; it is **not** a model leaderboard.
- **Release 02 — Architecture comparison:** “We tested whether AI could distinguish customer-mix shifts from within-segment changes using generated SQL, approved tools, and a hybrid. Here is what worked, what failed, and what the evidence showed.” Start with Arm A, then compare A/B/C on matched cases; include uncovered exploratory questions.
- **Later investigation study:** “We tested whether AI could identify the real cause of a revenue discrepancy. Here's what happened, what the models got wrong, and what the evidence showed.” The seeded revenue incident is retained but is not the first architecture study.

## Initial model candidates

Four **selected candidates**, pending API availability, exact pinned deployment identifiers and a connectivity-only pilot:

| Candidate | Role | Status |
|---|---|---|
| GLM-5.1 | Larger open-weight model | Candidate; serving provider to verify |
| Qwen3.6-27B | Smaller general-purpose open-weight model | Provisional replacement for Qwen2.5-Coder-32B-Instruct; model/host details to verify |
| Claude Sonnet 5.5 | Proprietary comparison | Candidate; exact API ID to verify |
| GPT-6.1 Sol | Proprietary comparison | Candidate; exact API ID to verify |

**These names are research selections, not claims of verified API IDs, current availability, prices, or comparable default reasoning settings.** Record the exact API response/deployment metadata and date before any scored run. Do not use auto-updating `latest` aliases for confirmatory campaigns.

## Planned execution (revised 21 October 2026)

- **Phase 0 — Verify the evaluation instrument.** No model required, a handful of cases, reference computations, deterministic grader, trace logging. No performance claims.
- **Phase 1 — Generated-SQL baseline (Arm A).** One model, four scenario families, multiple phrasings and trials; includes novel out-of-coverage questions.
- **Phase 2 — Architecture comparison.** Add approved-tool (Arm B) and hybrid (Arm C) arms on the same cases; paired evaluation. Covered and out-of-coverage questions are reported separately.
- **Phase 3 — Cross-model comparison.** Extend to the four candidate models once evaluation contracts and scoring are stable.

Early comparisons are descriptive: four scenario families are four independent cases, so they cannot rank architectures or qualify trust. See `docs/decisions.md` (Amendment 001) for the rationale and the alternatives considered. The earlier four-model, two-context, one-case matrix is superseded.

Later: one injected-revenue-discrepancy investigation with a hidden defect manifest and verified impact. No real personal/customer data or real WhatsApp integration.

## Repo documentation

- [`docs/product-design.md`](docs/product-design.md) — full product plan, audience, scope, roadmap, tradeoffs and decisions.
- [`docs/evaluation-framework.md`](docs/evaluation-framework.md) — trust dimensions, task-risk tiers, scoring, safety and research integrity.
- [`docs/analysis-plan.md`](docs/analysis-plan.md) — **draft pre-specified** analysis plan; requires protocol freeze before any confirmatory run.
- [`docs/model-selection.md`](docs/model-selection.md) — four candidates, stable IDs, hosts, output/tool protocols and selection controls.
- [`docs/cost-methodology.md`](docs/cost-methodology.md) — run cost, caching, review time, uncertainty and Pareto/gate-first comparisons.
- [`docs/decisions.md`](docs/decisions.md) — agreed choices versus open architecture decisions.
- [`benchmarks/case-001-spec.md`](benchmarks/case-001-spec.md) — net-billed-revenue calibration specification (deferred; not the current first benchmark). Not to be confused with `case_001`-`case_004` in the code, which are conversion fixtures.
- ``config/tier-policy.example.yaml`` (planned; not yet in repository) — **illustrative policy, not approved certification thresholds**.

## Research transparency

The author directs the analytical problem design, business definitions, benchmark traps, interpretation and methodological decisions, informed by professional analytics experience. AI assistants may help draft documentation or code, potentially including assistants from providers evaluated here. Their roles will be disclosed in published research. Deterministic or independently verified reference answers, masked human rubric grading where needed, controlled inputs and versioned experiments reduce—but do not eliminate—bias.

This repository contains design documents and Phase 0 calibration code (Build 001). No model experiments have been run, no performance claims are established, no costs have been measured, and no production certifications have been issued.

## Later, independent product

**Negocio Inteligente** is a separate Spanish-first AI/data readiness and operational analytics concept for microbusinesses in Mexico and Latin America. It may reuse carefully separated adapters, telemetry and evaluation interfaces, but must not share this product's business-specific logic or become a single monolithic application.


## Implementation status — Build 001 (21 October 2026)

The row-level synthetic conversion generator and two reference-calculation paths now exist under `src/evaluation_lab/`; see [conversion benchmark documentation](benchmarks/conversion/README.md). This is **instrument calibration only**, not a scored AI study. Initial Python/SQLite tests were executed; DuckDB verification is pending in an environment where DuckDB can be installed. See the verification note below. Previous pre-implementation statements in older design documents are historical snapshots.

```bash
python -m pip install -e '.[dev]'
python -m evaluation_lab.generator --output data/generated/exact --mode exact
pytest -q
```

The exact expected ground truth and case-to-scenario mapping must remain inaccessible to evaluated agents.
