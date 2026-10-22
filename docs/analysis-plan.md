# Analysis Plan — v0.1 (DRAFT; NOT FROZEN)

**Date drafted:** 2026-10-16  
**Status:** To be finalized and Git-committed before first **confirmatory** campaign. Engineering calibration and API connectivity pilots may happen before freeze but are not confirmatory evidence.

## Question and scope

How do four selected AI workflow configurations differ in analytical correctness, confidently wrong claims, evidence quality, safety and cost when given the **same cases** under raw-schema versus governed-context conditions? The first one-case pilot primarily verifies evaluation instrumentation, not inferential effects.

## Design

- Candidate families: GLM-5.1, Qwen3.6-27B, Claude Sonnet 5.5 and GPT-6.1 Sol. Exact, stable API/host IDs **pending verification and freeze**.
- Conditions: raw schema vs. governed metric context; authorized data and SQL tools held constant inside a controlled-comparison campaign.
- Case-level unit: benchmark task, including fixed dataset snapshot; `template_id` and `trap_type` identify shared designs. Independent templates/cases, **not repeated calls**, determine effective inferential sample size.
- Record all scheduled trials and responses, including failures, refusals, retries, clarification requests and blocked tool attempts. Do not discard failures without documented pre-specified rules.
- Repeat trials to characterize stochastic behavior; final repetition count and settings to be chosen **before confirmatory runs**, not after observing correctness.

## Outcomes

**Primary:** task correctness (numerical + semantic), confidently wrong rate, evidence validity, critical safety violation count. **Secondary:** attempts per task, consistency across repetitions, tokens, end-to-end latency, cost/task, cost/correct task, review minutes where measured.

Definitions and rubrics are in `evaluation-framework.md`, with case-specific expected outputs in benchmark manifests. Clarification/abstention is a separate recorded outcome; scoring depends on whether the case was sufficiently specified.

## Comparisons

1. **Within-model, paired raw vs. governed context**, on identical cases, descriptive in one-case pilot.
2. **Primary proprietary pair proposal:** Claude Sonnet 5.5 vs. GPT-6.1 Sol in governed context, pending access/price verification.
3. **Exploratory:** open-weight vs. proprietary systems, GLM vs. Qwen, all additional model pairs; investigate cost, failure types and evidence rather than six unplanned winner claims.

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
- [ ] Timeout, retry, error and missing-data policies finalized
- [ ] Spending cap and publication/contamination policy documented
- [ ] Git commit hash and freeze date recorded in experiment metadata

**Changes after freeze:** amend with timestamp/rationale; label affected analyses exploratory where appropriate. Never silently rewrite the original plan to match results.
