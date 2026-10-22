# Analytics AI Evaluation Lab

**Status:** Design v0.2 · pre-implementation · 16 October 2026  
**License:** Not yet selected. **Do not assume reuse permissions until a license is added.**

> **Central question:** Which AI models and analytical workflows can be trusted to produce accurate, evidence-backed business insights, under what conditions, with what human oversight, and at what cost?

Analytics AI Evaluation Lab is a proposed, vendor-neutral evaluation environment for AI-powered analytics. It evaluates **configurations**, not model brands in isolation: model/deployment + business context + authorized tools + validation + evidence and review policy. The project aims to show *why* configurations succeed or fail through inspectable SQL, executed results, reference answers and investigation traces.

**Principle:** An AI-generated explanation is a hypothesis until evidence supports it.

## Who it is for

**Primary:** analytics engineers, data scientists and technical AI practitioners who need reproducible runs, auditable SQL, metric-definition tests and failure analysis. **Secondary:** analytics and data leaders who need evidence-based guidance about where human oversight remains necessary. Each research report will include **“What this means for adopting AI in analytics.”** There will not be a separate executive application for the MVP.

## Two capabilities and a shared trust lens

1. **Analytical correctness:** business questions, governed metrics, SQL, numerical/semantic correctness, ambiguity and uncertainty.
2. **Evidence-based investigation:** injected discrepancies, diagnostic SQL, verified vs. hypothetical causes, misleading decoys and reviewable evidence.
3. **Trust lens applied to both:** confidently wrong claims, evidence integrity, security, repeatability, latency, cost and human oversight.

## Two release stories

- **Release 01 — Engineering foundation:** “Here's how we built and verified our evaluation framework.” A small calibration case demonstrates that the evaluation machinery works; it is **not** a model leaderboard.
- **Release 02 — Investigation research:** “We tested whether AI could identify the real cause of a revenue discrepancy. Here's what happened, what the models got wrong, and what the evidence showed.” First substantial case study, with appropriately limited claims.

## Initial model candidates

Four **selected candidates**, pending API availability, exact pinned deployment identifiers and a connectivity-only pilot:

| Candidate | Role | Status |
|---|---|---|
| GLM-5.1 | Larger open-weight model | Candidate; serving provider to verify |
| Qwen3.6-27B | Smaller general-purpose open-weight model | Provisional replacement for Qwen2.5-Coder-32B-Instruct; model/host details to verify |
| Claude Sonnet 5.5 | Proprietary comparison | Candidate; exact API ID to verify |
| GPT-6.1 Sol | Proprietary comparison | Candidate; exact API ID to verify |

**These names are research selections, not claims of verified API IDs, current availability, prices, or comparable default reasoning settings.** Record the exact API response/deployment metadata and date before any scored run. Do not use auto-updating `latest` aliases for confirmatory campaigns.

## Initial engineering MVP

One synthetic business dataset, **one calibration question × four models × two context conditions** (raw schema and governed semantic documentation), eight experimental cells before repetitions. Use a common structured SQL-output protocol as a *candidate*, not yet a decision. Independently validate reference SQL (e.g., hand-checked fixture + second calculation path). Store all attempts and evidence. Early comparisons are descriptive: **one case cannot rank models or qualify trust**.

Next: one injected-revenue-discrepancy investigation with a hidden defect manifest and verified impact; inspect hypotheses, queries and findings. No real personal/customer data or real WhatsApp integration.

## Repo documentation

- [`docs/product-design.md`](docs/product-design.md) — full product plan, audience, scope, roadmap, tradeoffs and decisions.
- [`docs/evaluation-framework.md`](docs/evaluation-framework.md) — trust dimensions, task-risk tiers, scoring, safety and research integrity.
- [`docs/analysis-plan.md`](docs/analysis-plan.md) — **draft pre-specified** analysis plan; requires protocol freeze before any confirmatory run.
- [`docs/model-selection.md`](docs/model-selection.md) — four candidates, stable IDs, hosts, output/tool protocols and selection controls.
- [`docs/cost-methodology.md`](docs/cost-methodology.md) — run cost, caching, review time, uncertainty and Pareto/gate-first comparisons.
- [`docs/decisions.md`](docs/decisions.md) — agreed choices versus open architecture decisions.
- [`benchmarks/case-001-spec.md`](benchmarks/case-001-spec.md) — proposed first calibration case and ground-truth contract.
- [`config/tier-policy.example.yaml`](config/tier-policy.example.yaml) — **illustrative policy, not approved certification thresholds**.

## Research transparency

The author directs the analytical problem design, business definitions, benchmark traps, interpretation and methodological decisions, informed by professional analytics experience. AI assistants may help draft documentation or code, potentially including assistants from providers evaluated here. Their roles will be disclosed in published research. Deterministic or independently verified reference answers, masked human rubric grading where needed, controlled inputs and versioned experiments reduce—but do not eliminate—bias.

This repository currently contains **design documents only**; no experiments have been run, performance claims established, code implemented, costs incurred or production certifications issued by this repository.

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
