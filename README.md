# Analytics AI Evaluation Lab

**Can we trust AI-generated analytics? And how would we know?**

Companies are starting to ask AI tools questions about their data, like *“Why did sales go up last month?”* The answers can sound confident even when the calculation is wrong or the explanation isn't supported by evidence.

**Analytics AI Evaluation Lab is a public research and engineering project testing whether AI-generated analytical answers are accurate, consistent, and backed by verifiable evidence.**

**Status:** Phase 0 — building and validating the evaluation setup. No AI models have been scored yet.  
**Next:** Complete the reference and DuckDB checks, build the deterministic grader, then run the first generated-SQL baseline.  
**License:** All rights reserved. No open-source license has been granted at this time.

## The first question I'm testing

**When a business metric changes, is it because different kinds of customers showed up, or because the same kinds of customers behaved differently?**

Imagine a SaaS company's trial-to-paid conversion rate increases. Did more trials come from customer segments that typically convert at higher rates? Did customers within each segment convert more often? Did both happen? Or might the observed movement be ordinary random variation?

These distinctions guide what a team investigates next, though they do not by themselves establish *what caused* the change.

I create **synthetic datasets (made-up but realistic data)** with deliberately planted patterns and independently calculated answers. That lets me check whether an AI identifies and quantifies the patterns correctly, supports its conclusions, and produces consistent answers.

## What I'm comparing

Three ways of letting AI analyze company data:

1. **Generated SQL:** AI writes database queries using governed business definitions (agreed-upon rules for calculating metrics).
2. **Approved analytical tools:** AI uses pre-approved functions whose calculations have already been tested.
3. **Hybrid:** AI uses approved tools where available and controlled SQL for questions the tools don't cover.

The goal is to learn where each approach succeeds, where it fails, and what it costs. **No approach is presumed best.**

## Why it matters

Teams are deciding how much analytical work to delegate to AI. They need to know when a result is correct, when an explanation is unsupported, and where human review remains necessary.

**They need evidence, not just demos.**

## About the author

I'm a data and analytics leader with 14+ years of experience, including leading Data Science & Analytics at GIPHY. I also work as an advisor. This project brings together my experience in metric governance, data science, analytics engineering, and translating technical findings into business decisions.

## Start exploring

- [Design decisions and tradeoffs](docs/decisions.md) — why we're comparing different analytical architectures.
- [Conversion benchmark walkthrough](benchmarks/conversion/README.md) — the first test case and how its answers are verified.
- [Evaluation framework](docs/evaluation-framework.md) — how correctness, evidence, uncertainty and safety will be assessed.

*I'd welcome feedback from analytics and AI practitioners. [Connect with me on LinkedIn](https://www.linkedin.com/in/lluviahernandez).*

---

## Technical design and methodology

**Research question:** Which AI models and analytical workflows can be trusted to produce accurate, evidence-backed business insights, under what conditions, with what human oversight, and at what cost?

This Lab evaluates **configurations**, not model brands alone: deployment, analytical context, authorized tools, validation, evidence and review requirements. Its guiding principle is **an AI-generated explanation remains a hypothesis until evidence supports it.**

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
- A task-tier policy configuration may be added later; no qualification thresholds are approved yet.

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

## License

This project is publicly available for portfolio, research, and educational visibility.

**All rights reserved.** No open-source license has been granted at this time. Licensing options are under consideration.
