# CASE-001 — Net Billed Revenue Calibration

**Status:** Specification proposal; not executable or scored.  
**Capability:** Analytical correctness  
**Scenario type:** Metric definition / invoice status / adjustments  
**Suggested risk context:** T1 assisted exploration for initial evaluation; intended use tier is configurable.

## Business prompt

> What was our net billed revenue in September 2026, and how did it compare with August 2026?

This is deliberately **net billed revenue**, *not GAAP-recognized revenue*. The latter would require different service-period and accounting rules.

## Proposed minimal schema

- `customers(customer_id PK, segment, created_at)`
- `invoices(invoice_id PK, customer_id FK, invoice_date, status)`
- `invoice_lines(line_id PK, invoice_id FK, line_type, amount)`

**Before implementation, specify** date timezone and inclusive/exclusive reporting boundaries; currency and FX exclusions; eligible statuses; line amount sign conventions; credit/refund representation; null/duplicate policies; and whether payments or invoice dates define “billed.” These are intentional unresolved decisions, not defaults inferred by a model.

## Candidate governed definition

> Net billed revenue for a calendar reporting month = sum of eligible subscription/usage invoice-line amounts minus eligible credits/refunds on **finalized** invoices assigned to that reporting month; exclude draft/void invoices. Use a documented single-currency/sign and date policy.

A raw-schema condition omits this governed definition. The model must not be penalized identically for **proper clarification** and **unsupported invented assumptions** when missing context makes the answer genuinely ambiguous.

## Hand-checkable illustrative fixture (NOT final generated dataset)

| Invoice | Month | Status | Positive charges | Credits/refunds signed | Net eligible |
|---|---|---|---:|---:|---:|
| INV-101 | Aug | finalized | 1000 | 0 | 1000 |
| INV-102 | Aug | finalized | 500 | -50 | 450 |
| INV-103 | Sep | finalized | 1200 | 0 | 1200 |
| INV-104 | Sep | finalized | 800 | -100 | 700 |
| INV-105 | Sep | void | 900 | 0 | 0 |

Illustrative expected values: **August $1,450**, **September $1,900**, **absolute change +$450**, **percentage change +31.0344827586%** relative to August. A result of $2,900 includes the void invoice; $2,000 ignores the September refund. These are **constructed examples** and must not be published as model results.

## Ground-truth construction

1. Freeze dataset, metric definition and fixture hashes.
2. Execute an independently reviewed reference SQL query with exact month boundaries and status/line rules.
3. Compute a logically independent answer, e.g. pandas aggregation, and manually confirm the tiny fixture.
4. Test invariants: adding a void invoice should not change net billed revenue; a signed credit should decrease it by exactly its eligible amount; splitting a line without changing its total should preserve the result.
5. Keep reference SQL/values in a grader-only manifest not passed to evaluated models.

## Inputs, permitted tools and controlled contexts

Model receives question + schema, and in the governed condition approved definition/documentation. Both conditions use the same snapshot, read-only sandbox, execution limits, structured response contract and model settings. Never pass the truth manifest. Tool-calling protocol remains to be selected before building.

## Proposed output contract (subject to review)

- `status`: answered / needs_clarification / unable_to_verify
- `sql`: runnable read-only SQL or null with reason
- `answer`: reported August/September/difference/percentage or null
- `metric_interpretation`: explicitly applied business definition
- `assumptions`: list
- `evidence`: executed query references and actual results
- `uncertainty`: unresolved definitions and hypotheses

## Grading and classification

Score SQL-execution success, numeric agreement within a **pre-specified** tolerance, semantic compliance (eligible statuses/adjustments/date definition), consistency of explanation with results, justified clarification/abstention, confidently wrong claims and safety violations. A correct number via invalid SQL semantics is **not** automatically semantically correct. Logging blocked unauthorized write attempts is distinct from claiming they succeeded.

## Experiment position

Four candidate models × raw/governed context = eight initial cells before repeat trials. This **calibrates the harness**; it cannot support model rankings, uncertainty intervals on across-task accuracy or T1/T2 qualification. A later seeded discrepancy investigation will be a separate case type with a hidden defect manifest including affected rows, quantified impact, plausible decoys and acceptable verified conclusions.

## Open case decisions

- Final dataset domain/schema/version and numeric scale
- Currency, date, status and sign conventions
- Exact model-access identities and output/tool protocol
- Permitted clarification/retry cycle and timeout
- Numeric tolerance, SQL semantic checks and human adjudication rubric
- Publishable fixture vs. held-out case separation
