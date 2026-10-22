# Product Design — v0.2

**Status:** Design draft, approved direction with open decisions  
**Date:** 2026-10-16  
**Product:** Analytics AI Evaluation Lab  
**Phase:** Phase 0 instrument calibration (Build 001) · **Revised:** 2026-10-21

> **Amendment 001 (2026-10-21):** the primary experimental factor is now **architecture** (generated SQL, approved tools, hybrid) on a conversion mix-shift benchmark, with governed context held constant and models added in Phase 3. Where sections 6 and 10 conflict with this note, this note governs. See `decisions.md` Amendment 001. The first benchmark uses a single row-level `trials` table; the invoice-based schema in section 5 is deferred.

## 1. Vision and positioning

Analytics AI Evaluation Lab is a vendor-neutral professional evaluation platform for determining when AI-powered **analytical workflows** produce accurate, evidence-backed and reviewable results. It is **not** a generic text-to-SQL leaderboard, a production certification authority or an AI assistant for end users.

**Research question:** Which AI models and analytical workflows can be trusted to produce accurate, evidence-backed business insights, under what conditions, with what human oversight, and at what cost?

“Trusted” is a **task-specific and policy-dependent** claim about a *configuration under tested conditions*, not a property of a model's brand. Lab findings must not imply production readiness.

> An AI-generated explanation remains a hypothesis until the evidence supports it.

## 2. Users and jobs to be done

**Primary: analytics engineers, data scientists and technical AI practitioners.** They want to compare AI workflows, reproduce outcomes, inspect SQL and evidence, diagnose failures, and learn the effects of context, tools, governance and validation. Success means being able to trace a conclusion to executable tests rather than trusting persuasive prose.

**Secondary: data and analytics leaders.** Their job is to **get evidence-based guidance on where human oversight is needed** and what reliability/cost tradeoffs a deployment introduces. Each technical report will include a compact **“What this means for adopting AI in analytics”** section based on the same results; no separate leader-oriented app in the MVP.

## 3. Evaluation object and scope

Unit of evaluation: **model/deployment + task + supplied context + permitted data/tools + output protocol + validation/recovery + review policy**. This is a workflow configuration. Comparisons should isolate a variable where feasible and name what cannot be controlled (reasoning defaults, model architecture, host/quantization, caching).

Two core capabilities:

1. **Analytical correctness** — metric interpretation, approved definitions, executable SQL, joins/grain, numeric answers, clarification and assumption management.
2. **Evidence-based investigation** — diagnosing a discrepancy, quantifying affected records, testing alternative explanations, presenting exact SQL and results, separating known causes from hypotheses, recognizing when to request human review.

**Operational trust** is a cross-cutting lens, not a third standalone engineering subsystem: correctness, confidently wrong rate, evidence validity and reviewability, security boundaries, consistency, latency and costs.

## 4. Research progression and release stories

**Engineering calibration (Release 01: foundation).** “Here's how we built and verified our evaluation framework.” Build one small, independently verified calculation case; demonstrate that execution, scoring and evidence capture are correct. This validates the *instrument*, not claims about comparative model reliability.

**Investigation case study (Release 02: distinctive public research).** “We tested whether AI could identify the real cause of a revenue discrepancy. Here's what happened, what the models got wrong, and what the evidence showed.” Inject a defect with privately known truth and require the AI to investigate using allowed data and SQL. Publish traces, limitations and findings without extrapolating from a single case.

**Future extensions:** additional trap families, contradictory/stale metric context, robustness across languages (English and Spanish), alternative tool interfaces, reviewability and human error-detection experiments, more datasets and models.

## 5. Benchmark domain and minimum data model

**Leading candidate:** fully synthetic fictional B2B SaaS/API business, with customers, subscriptions/plans, invoices, invoice lines, usage charges, credits and refunds. Start with the **minimum schema necessary for chosen questions**, not a fictional enterprise warehouse. Synthetic fixtures allow precisely known answers and injected join/date/status/data-quality defects. Generate realistic-but-controlled distributions and hide reference answers from evaluated models.

**Alternative for later assessment:** public Olist Brazilian e-commerce data, valuable for real-world variation but not a direct replacement for subscription/API concepts. Dataset selection remains formally open until tradeoffs (realism, setup, edge cases, ground truth, publishing rights) are discussed.

Initial proposed three-table calibration model: `customers` (customer_id, segment), `invoices` (invoice_id, customer_id, invoice_date, status), `invoice_lines` (line_id, invoice_id, line_type, amount). Actual design needs currency, date/timezone, sign, granularity and uniqueness conventions specified before implementation. Distinguish **net billed revenue** from GAAP recognized revenue.

## 6. Candidate models and experiment conditions

Four candidate systems: **GLM-5.1**, **Qwen3.6-27B** (provisional), **Claude Sonnet 5.5**, **GPT-6.1 Sol**. Exact API IDs, snapshot availability, hosts, model parameters, prices and access paths require verification and freeze before scored evaluation. API-based execution is the leading option; self-hosting is deferred. The terms “ChatGPT” and “Claude” are product/model-family labels, not sufficient identifiers for reproducible runs.

**Revised matrix (2026-10-21):** Phases 0-2 use one model and vary architecture (Arm A generated SQL, Arm B approved tools, Arm C hybrid) with governed context held constant; Phase 3 crosses four models with the three arms. The earlier calibration matrix (four models × two contexts × one question = eight cells) is superseded. The raw and governed context definitions below are retained for a later ablation.

- **Raw schema:** business question plus authorized table/column/schema information, with no governed metric definition supplied.
- **Governed context:** identical question, schema, permissions and output requirements, plus approved metric definition and relevant modeling documentation; never the hidden answer.

If the raw condition is genuinely underspecified, asking for clarification may be appropriate and should not be graded as the same failure as inventing a definition. Controlled pilot outputs are for connectivity and scoring calibration, not confirmatory claims.

**Tool protocol choice remains open:** a uniform JSON/SQL response loop maximizes experimental control but may underuse native tool strengths; native function calling is more realistic but changes the measured configuration. A small diagnostic subset can later compare protocols. Avoid claiming identical reasoning-effort settings across incompatible providers; document provider-specific settings and resource ceilings.

## 7. Trust and intended-use tiers

Risk tiers describe **intended deployment use**, not inherent difficulty of a question. The same case could be exploratory or consequential depending on how outputs are used.

- **T1 — Assisted exploration:** ad hoc metrics and first-pass analysis; analyst reviews outputs.
- **T2 — Operational reporting:** recurring internal KPIs; defined review and governance controls.
- **T3 — High-consequence analysis:** audited finance, production incidents or costly downstream action; **no autonomous qualification** under this project's proposed policy; require explicit human approval. Evaluate evidence quality and whether a reviewer could identify incorrect claims.

Thresholds are policy choices and **not yet approved**. Early campaigns compare observed performance; they do not certify trust. See `evaluation-framework.md`.

## 8. Technical principles and tool candidates

- Keep benchmark engine independent of **model vendors and presentation vendors**.
- Separate **case specification** (problem, hidden reference) from **experiment configuration** (model, context, host, tools and policy), and from **recorded run** (inputs, outputs, queries, results, score, costs).
- Generate reproducible versioned datasets and immutable run evidence (with redacted secrets and no real personal information).
- Prefer deterministic reference SQL and independently implemented cross-checks; use rubric-based, masked human review only where deterministic scoring is inadequate.
- Run only authorized, read-only SQL against sandboxed data; record violations and blocked actions.
- Preserve small dependencies and a low operating cost. Avoid a complex agent platform or production deployment in the MVP.

**Candidates, not selections:** Python, SQL, DuckDB, pytest, dbt, Dash, Streamlit, Hex. DuckDB + Python may be enough for calibration; dbt must justify its additional overhead. Hex can be an optional analyst workspace, **not a requirement**. A static report with precomputed results may be the simplest public artifact; an interactive Dash/Streamlit interface should add genuine exploration value rather than just polish. Confirm publishing/hosting terms before committing.

## 9. User experience and reporting

Readers should be able to understand the benchmark, compare configurations on identical cases, inspect SQL and evidence, view uncertainty, identify trap/failure categories and retrieve reproducibility instructions. Each report should show methods, limitations, real measured outcomes and a leader-facing adoption/oversight summary.

Cost/performance visuals may plot accuracy with intervals against measured cost, optionally on a log cost axis. Mark zero-marginal-API-cost deployments separately and report their compute costs. A **descriptive Pareto frontier** is not a trust certification; qualified cost comparison is allowed only after the relevant criteria have been met.

## 10. MVP and non-goals

**First engineering vertical slice (revised 2026-10-21):** one synthetic conversion dataset family, one primary factor (architecture: generated SQL, approved tools, hybrid), one model for Phases 0-2 and four models in Phase 3, governed context held constant, reference SQL + independent cross-check, controlled response format, query/evidence capture, deterministic grading where possible, timing, token/price data, basic safety/assumption logging, GitHub documentation and a simple static or minimal interactive results view.

**First distinctive research extension:** one known injected defect causing a revenue discrepancy (illustratively +8%), its hidden defect manifest and impact, approved diagnostic access, evaluated investigations and complete evidence traces.

**Not now:** 25-question grid, broad model leaderboard, T1/T2 certification, T3 automation, reviewer-simulation study, real customer/WhatsApp data, multi-tenant SaaS, required Hex dependency, full production security infrastructure, online public execution with unbounded API spend, or the Negocio Inteligente UI.

## 11. Success and evidence standards

A milestone succeeds when independent reference calculations are validated; a second person can reproduce a run; cases/configurations/results and evidence are versioned; claims correspond to executed data; incorrect and confidently incorrect behavior can be distinguished; known uncertainty and failure modes are explained; no invented rankings or unsupported production claims are made.

Cross-check reference answers via **hand-checked micro-fixtures plus a logically independent route** (e.g., pandas group-by compared with SQL) rather than merely rerunning the same logic.

At a one-case MVP scale, comparative accuracy and trust qualification are **inconclusive by design**. Treat it as an instrument calibration and learning artifact.

## 12. Research integrity and authorship

Pre-specify the analysis before a confirmatory full campaign. Publish case templates/generators and public tests where feasible, while maintaining a versioned held-out evaluation subset to mitigate contamination; disclose reproducibility limitations of private holdouts. Treat repeated trials and shared traps as correlated. Classify critical versus minor safety issues. Record deviations, human adjudication and development-assistant involvement. The human author defines business concepts, traps and research interpretation; disclose actual assistant contributions without overstating independence.

## 13. Decisions remaining before coding

1. Final synthetic SaaS model and definitions versus alternative dataset.
2. Exact four API/deployment IDs (not aliases), snapshot/weights, hosts and pricing verification.
3. Uniform structured response loop versus native tool calling; permitted SQL tools.
4. Spending ceiling, caching policy and logging/secret redaction.
5. First case outputs and rules for partial/abstaining answers.
6. Formal primary pairwise comparisons and confirmatory sample plan.
7. Whether dbt adds enough value to the first slice.
8. Static report versus Dash/Streamlit for public release.
9. Repo license, public benchmark contamination mitigation and held-out access policy.

Keep these open in documentation; discuss tradeoffs before making architecture commitments.
