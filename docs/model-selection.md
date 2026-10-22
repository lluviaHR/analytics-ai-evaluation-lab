# Model Selection & Access Policy — v0.2

**Status:** Four candidate families agreed; exact deployment selection remains open (2026-10-16).

## Selected candidates

| Candidate | Intended comparison role | Required verification before scoring |
|---|---|---|
| Claude Sonnet 5.5 | Proprietary mid-tier comparison | Official API name/ID, snapshot, availability, price, reasoning/token limits |
| GPT-6.1 Sol | Proprietary mid-tier comparison | Official API name/ID, snapshot, availability, price, reasoning/token limits |
| GLM-5.1 | Larger open-weight general-purpose system | Genuine weight/model revision, stable API host, price, tool/JSON support, quantization |
| Qwen3.6-27B | Provisional smaller open-weight general system | Confirm official model naming/weights/license, exact serving host/ID, price, quantization |

**Caution:** These are names supplied and selected during product planning; **this document does not assert that any particular API identifier, release date, price or vendor feature is verified**. Check provider first-party documentation and a live, non-scored connectivity test; record evidence in a dated model manifest before calling the lineup frozen. Do not substitute rolling `latest` aliases. If any model is unavailable or uneconomical, document the adjustment **before seeing scored responses**.

## Four selection gates

1. **Research contrast:** What does this candidate uniquely help compare? Avoid interpreting size or marketing tier as measured quality.
2. **Stable identity:** Can the precise model ID, host, weight revision, quantization and run date be captured?
3. **Output compatibility:** Can it return required JSON/SQL and expose necessary usage metadata? Pilot checks only connectivity/format, not case correctness.
4. **Bounded expense:** Is total expected spending, including worst-case retries and tools, within the run budget?

## Pilot vs. scored run

A connectivity-only pilot tests authentication, JSON formatting, model-ID reporting, token reporting, rate limits and host behavior using **non-benchmark prompts**. It must not be used to choose whichever candidate happens to solve the scored questions best. Freeze lineup and configuration in version control **before the first scored comparison**.

## Protocol and reasoning tradeoffs

A **common structured response** (SQL + answer + assumptions + evidence + status) may be simplest for the first calibration. Native function calling might better reflect provider-recommended workflows but introduces protocol differences; run that as a separately labeled workflow comparison or subset diagnostic if warranted. Keep permissions and resource ceilings comparable, but do not assume provider `medium`/`high` reasoning modes are identical. Report actual provider settings and resulting usage.

## Proposed pairwise contrasts

- **Primary candidate:** Claude Sonnet 5.5 vs. GPT-6.1 Sol, same cases and governed context, assuming access and comparable operating conditions.
- **Exploratory:** Qwen and GLM vs. proprietary counterparts; actual cost/evidence tradeoffs, not a priori assumptions of “cheapest” or “strongest.”

With four models there are six pairwise comparisons. Do not turn all six into confirmatory claims after results are visible.

## Minimum run manifest

`run_timestamp_utc`, `case_id`, `dataset_hash`, `experiment_id`, `provider`, `api_model_id`, `reported_model_id`, `host`, `model_revision`, `quantization` (if known), `prompt_hash`, `context_condition`, `tool_protocol`, `temperature`, `seed` (when supported), `reasoning_settings`, `max_output_tokens`, `tool_permissions`, `caching_policy`, `input_tokens`, `output_tokens`, `cached_tokens` (if available), `attempt_count`, `latency`, `pricing_snapshot_date`, `actual_or_estimated_cost`, `sql`, `query_result`, `grade`, `trace_location`.

Do not publish tokens, secrets, customer records or private held-out answers merely because they were logged internally. API model aliases and opaque host deployments can limit reproducibility: disclose those limits.
