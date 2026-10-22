# Analysis Plan — v0.2 (DRAFT; NOT FROZEN)

**Date drafted:** 2026-10-16 · **Revised:** 2026-10-21 (architecture is the primary factor; phased execution; see `decisions.md` Amendment 001)  
**Status:** To be finalized and Git-committed before first **confirmatory** campaign. Engineering calibration and API connectivity pilots may happen before freeze but are not confirmatory evidence.

## Question and scope

For AI-assisted product analytics, how do three architectures differ in analytical correctness, confidently wrong claims, evidence quality, consistency, safety and cost when given the **same cases** with governed context held constant: generated SQL (Arm A), approved parameterized tools (Arm B), and a hybrid (Arm C)? The first benchmark asks whether an AI analyst can attribute a change in a conversion rate to customer mix versus within-segment behavior, and whether the evaluation system detects when it gets that attribution wrong. Phase 0 verifies the evaluation instrument and makes no performance claims.

## Design

- Candidate families (evaluated in Phase 3; Phases 0-2 use one model): GLM-5.1, Qwen3.6-27B, Claude Sonnet 5.5 and GPT-6.1 Sol. Exact, stable API/host IDs **pending verification and freeze**.
- Primary factor: **architecture** (Arm A generated SQL with governed definitions and read-only execution; Arm B approved parameterized operations, no arbitrary SQL; Arm C approved operations for supported measurements plus controlled read-only SQL for unsupported exploratory analysis). Governed context, data snapshot, permissions, resource ceilings and output contract are held constant across arms. Raw vs. governed context is a deferred, exploratory ablation.
- Coverage: each question is labeled **covered** (answerable with the versioned Arm B tool catalog) or **out-of-coverage** before scoring. Report the two groups separately; do not blend them into one accuracy figure.
- Decomposition convention (symmetric Kitagawa: mix = Σ(w1−w0)(r0+r1)/2; within = Σ(r1−r0)(w0+w1)/2), numerical tolerances and the "no real change" threshold are fixed and committed **before** scored evaluation.
- Case-level unit: benchmark task, including fixed dataset snapshot; `template_id` and `trap_type` identify shared designs. Independent templates/cases, **not repeated calls**, determine effective inferential sample size. In the conversion benchmark the independent unit is a scenario family or dataset instance, not a phrasing or trial: four scenario families (pure mix, pure within, combined, no change) with many phrasings and trials are still four independent clusters, so Phase 1-2 results are descriptive. Confirmatory inference requires multiple dataset instances per scenario (different seeds, effect sizes and segment structures).
- Record all scheduled trials and responses, including failures, refusals, retries, clarification requests and blocked tool attempts. Do not discard failures without documented pre-specified rules.
- Repeat trials to characterize stochastic behavior; final repetition count and settings to be chosen **before confirmatory runs**, not after observing correctness.

## Phases

- **Phase 0 — Verify the instrument.** One model, a handful of cases, reference computations, deterministic grader, trace logging. Exact fixtures first. No performance claims.
- **Phase 1 — Generated-SQL baseline (Arm A).** One model, four scenario families, up to 20 phrasings and five trials each; novel out-of-coverage questions included from the start. Feasibility, variation and initial failure taxonomy.
- **Phase 2 — Architecture comparison.** Add Arms B and C on the same cases; paired evaluation.
- **Phase 3 — Cross-model comparison.** Expand to the four candidate models after contracts and scoring are stable.

Deterministic verification is the grading foundation. Human rubric labels support qualitative evaluation. An LLM judge may be introduced only after a reference-labeled subset exists, and never as sole authority.

## Outcomes

**Primary:** task correctness (numerical + semantic), confidently wrong rate, evidence validity, critical safety violation count. **Secondary:** attempts per task, consistency across repetitions, tokens, end-to-end latency, cost/task, cost/correct task, review minutes where measured.

Definitions and rubrics are in `evaluation-framework.md`, with case-specific expected outputs in benchmark manifests. Clarification/abstention is a separate recorded outcome; scoring depends on whether the case was sufficiently specified.

## Comparisons

1. **Primary (Phases 1-2): paired architecture comparison** on identical cases with governed context held constant: A vs. B, A vs. C, B vs. C. Report covered and out-of-coverage questions separately. Descriptive unless enough independent scenario instances exist.
2. **Phase 3 proposal:** Claude Sonnet 5.5 vs. GPT-6.1 Sol under the architecture(s) of interest, pending access/price verification. Do not finalize after viewing scored results.
3. **Exploratory:** open-weight vs. proprietary systems, GLM vs. Qwen, raw vs. governed context ablation, all additional model pairs; investigate cost, failure types and evidence rather than unplanned winner claims.

**Do not finalize the primary pair after viewing scored results.** If the proposed pair changes for access/compatibility reasons, freeze and document the reason first.

## Uncertainty and reporting

- One-case calibration: show raw outcomes, no population accuracy confidence intervals or trust qualification.
- Multi-case campaigns: report denominator, correct/incorrect/clarify/failed counts by case and trap. For independent binary cases, show a specified binomial interval such as Wilson; for templated/repeated designs, use a defensible cluster-aware procedure or explicitly decline inferential precision when too few independent clusters exist.
- Within-case repeats: summarize per case first, report variability separately. Paired model/context comparisons require the same cases; do not treat every run as an independent task.
- Report effect sizes with uncertainty where meaningful; do not call an observed difference significant unless the pre-specified approach supports it. Mark any post hoc comparisons **exploratory**.
- Avoid claiming no difference from lack of power.

## Costs, missingness and exceptions

All inference attempts and retry costs count. Report actual observed charges if available, otherwise clearly labeled price-card estimates and snapshot date; account for caching and provider-specific reasoning/usage. Cost/correct task = **all attempted-task spend / correct completed tasks** (undefined if zero correct). Bootstrap interval only where adequate independent sample structure supports one. Report review minutes as measured, and any labor conversion as an assumption.

Timeouts, SQL execution errors, invalid JSON, aborted calls and refusals remain visible in the denominator/report. Define maximum retry budget, timeout, token ceiling and any provider outage exclusion **before confirmatory execution**. Record all protocol deviations and show original versus sensitivity analyses where possible.

## What counts as a finding

- **Calibration observation:** indicates whether harness and grader behave correctly; cannot rank models.
- **Exploratory observation:** model/trap patterns worth follow-up; descriptive, clearly limited.
- **Supported comparative finding:** matches a frozen hypothesis/contrast, has adequate independent cases, transparent uncertainty and no undisclosed exclusions.
- **Qualification:** **outside the initial campaign**; future tier-specific policy requires enough evidence, safety/evidence gates, and explicit intended use.

## Freeze checklist (unresolved before confirmatory run)

- [ ] Exact API model IDs, host, deployment/weights and prices pinned
- [ ] Sample size, independent template families and trial count fixed
- [ ] Cases/dataset snapshots, hidden truth and rubrics versioned
- [ ] Primary contrasts, interval/resampling method finalized
- [ ] Prompt/tool/caching/reasoning configuration recorded
- [ ] Decomposition convention, numerical tolerances and "no real change" threshold fixed and committed
- [ ] Arm B tool catalog and covered/out-of-coverage labels versioned
- [ ] Known-wrong answer set passes (all rejected) and known-correct answers accepted by the grader
- [ ] Timeout, retry, error and missing-data policies finalized
- [ ] Spending cap and publication/contamination policy documented
- [ ] Git commit hash and freeze date recorded in experiment metadata

**Changes after freeze:** amend with timestamp/rationale; label affected analyses exploratory where appropriate. Never silently rewrite the original plan to match results.
