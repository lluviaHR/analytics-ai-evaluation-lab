# Cost Measurement and Reporting — v0.2

**Status:** Design policy; no measured costs yet (2026-10-16).

## Two separate questions

1. **Configuration economics:** What does an answer or evidence-supported investigation cost, including failed calls, retries, tools and human review?
2. **Project economics:** What does it cost to build, rerun, host and maintain the Lab? Separate cash expenses, estimated costs and labor/time not monetized.

## Mandatory run-level records

Model/host/ID, UTC date, **pricing snapshot date**, region or processing tier if relevant, input/output tokens, reasoning tokens where separately exposed, cached input/cache write/read, provider-reported charges (if available), SQL/tool compute, number of attempts/retries/timeouts, latency, review minutes, price currency and whether cost was actual or estimated. Record the full rate-card assumptions as versioned metadata; never hard-code unverified prices in the published design.

**Prompt caching:** Provider behavior varies. Record whether caching was enabled; disclose where control is unavailable. Governed context may be reused and caching can materially change cost. Report actual billed/estimated caching-aware cost and, if feasible, an explicitly hypothetical uncached list-price estimate. Don't imply that equal caching efficiency can be imposed across vendors.

**Self-hosted models:** “$0 API fee” is **not $0 inference cost**. Report GPU/CPU hours, hardware/rental/electricity assumptions, fixed-vs-marginal treatment and any hosting overhead. Do not compare local zero API spending against hosted fully-loaded pricing as if they were equivalent.

## Definitions

- **Cost per attempted task:** total run spend (including unsuccessful attempts and retries) / number of assigned task attempts under the declared accounting unit.
- **Cost per correct task:** total spend on **all** attempts, failures and retries / number of **correct completed tasks**. If none correct, **undefined** (not $0 or infinity presented as observed monetary price). Report counts; at low denominators this ratio is unstable.
- **Evidence-supported investigation cost:** all attempts and tool costs for investigations meeting the predefined correctness **and** evidence criteria / number of such successful investigations; undefined if zero.
- **Workflow cost estimate:** model inference + tool/infrastructure + review time × stated hourly labor rate (if and only if a rate is declared). Always also report actual review minutes without wage assumptions.

Keep billed cost and theoretical list-price cost distinct. Cost-per-correct uncertainty: cluster-aware bootstrap of case-level outcomes and spend only when enough independent cases/families support inference; report descriptive totals for the initial one-case pilot.

## Accuracy-versus-cost charts

Plot model **configurations**, not abstract brands. Show denominators and confidence intervals/uncertainty where estimable; a point without adequate independent cases is **descriptive only**. Use a log-scale cost axis when values span orders of magnitude; show true zero-marginal-API-cost results separately, not at arbitrary positive pseudocost. Report quantile/tail costs where multi-step retries create heavy tails.

**Pareto frontier:** A configuration is descriptively non-dominated if no other observed configuration is both no more expensive and at least as correct, with strict improvement on one. With uncertain estimates, observed frontier membership is **not proof of superiority** or trust.

## Gate first, then compare cost

1. Define intended-use tier and mandatory correctness, evidence, safety, review controls **before** seeing results.
2. Classify each configuration (in future adequately powered studies) as meets / inconclusive / does not meet criteria.
3. Among those **meeting** applicable criteria, compare costs and latency. Never recommend a cheap but failing configuration as efficient for consequential work.
4. In the first MVP, show descriptive cost and correctness for **all** configurations without any qualification claim.

## Public expense ledger (to populate later)

| Category | Actual spent | Estimate / assumption | Notes |
|---|---:|---:|---|
| Model API calls | Not measured | Not yet estimated | Price snapshots required |
| SQL/computing | Not measured | Not yet estimated | Local vs. hosted distinguish |
| Public hosting | Not measured | Not yet selected | Static vs. app hosting |
| Development subscriptions | Not measured | Not yet recorded | Disclose relevant AI assistants |
| Human review | Not measured | Rate not selected | Record minutes first |
| Maintenance | Not measured | Not yet estimated | Recurring, separate from experiment |

This table reports **no expenditures because none have been provided or measured for this documentation package**; it does not claim the author's real-world spending was zero.
