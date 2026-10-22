# Cross-Chat Alignment and Remaining Decisions — 2026-10-20

**Status:** Working alignment record. This is a consolidation of the existing Analytics AI Evaluation Lab design and the recovered conclusions from the “Compared AI Courses” discussion. It does **not** freeze new architecture or expand the MVP by itself.

## Update — 2026-10-21

- **First benchmark family selected:** mix-shift vs. within-segment decomposition on trial-to-paid conversion. Cohort/retention, experiment interpretation and correlation-vs-causation remain candidates.
- **Primary experimental factor:** architecture (generated SQL, approved tools, hybrid), governed context held constant. Phased execution: Phase 0 instrument calibration, Phase 1 generated-SQL baseline, Phase 2 add approved-tool and hybrid arms, Phase 3 four models. See `decisions.md` Amendment 001.
- **Product Analytics Investigator** remains a workflow under test. A hybrid design is the preferred direction for it, but it is tested as one arm; no arm is presumed superior.
- **Course status:** the author has decided to take Maven's Build an AI Analyst (Nov 2026 cohort). It remains a learning accelerator, not an architecture authority.

## Agreed strategic direction

- One coherent **Trustworthy AI Analytics** portfolio story, centered on **Analytics AI Evaluation Lab**.
- The Lab remains the reusable evaluation foundation; it precedes other applied products.
- A future **Product Analytics Investigator** is an *agent/workflow under test* powered and evaluated by the Lab, **not a new standalone platform to build immediately**.
- **Negocio Inteligente** remains a separate future Spanish-first small-business application; share infrastructure only where justified.
- Maven's **Build an AI Analyst** course is a possible development accelerator using the same ongoing project, **not an architecture authority**. The user has decided to take the course (Nov 2026 cohort); completion has not occurred and the course does not set the architecture. The user has already enrolled in Hex's Enterprise Context Management for Analytics workshop. Neither requires Hex to be the public frontend.

## Crosswalk: existing documents vs. course-discussion ideas

| Idea | Current coverage | Addition / disposition |
|---|---|---|
| Golden dataset with independently verified answers | `case-001-spec.md`, evaluation framework | **Make explicit:** versioned golden-case registry with reference SQL, expected values, ambiguity rules, known traps, and hidden grader-only answers |
| Human labels and benchmark rubrics | Evaluation framework covers limited masked human adjudication | **Make explicit:** curated human reference labels, adjudication protocol, and disagreement log for non-deterministic attributes |
| LLM-as-judge and judge calibration | Existing docs prioritize deterministic scoring and say no evaluated model is sole judge | **Investigate, not commit:** optional rubric-based LLM judge as *assistant*, calibrated against human labels; never sole authority, never replace deterministic checks |
| Regression testing | Existing docs log repeatability and versioned runs | **Add explicitly:** rerun fixed golden tests after changes to prompts, tools, context, code or models; compare deltas and catch regressions |
| Analytics failure taxonomy | Existing docs include trap types and several dimensions | **Make explicit:** maintain case/response-level error taxonomy (definition error, join/grain, time boundary, leakage, unsupported cause, false certainty, invalid evidence, safety attempt, etc.) |
| Agentic analytical investigation | Existing seeded discrepancy benchmark | **Extend later:** Product Analytics Investigator as an evaluated workflow with query planning, tool use, evidence and human approval—not part of initial calibration implementation |
| Causal reasoning and product analytics | Only indirectly represented in future investigative scope | **Mix-shift vs within-segment change selected (2026-10-21) as the first benchmark family**; cohort/retention, experiment interpretation and correlation vs causation remain candidates |
| Semantic-layer ablation | Raw vs governed experiment already covered | Existing baseline; further ablations are exploratory, not a new confirmed roadmap commitment |
| Enterprise Context Management (Hex) | Hex listed as optional investigation/presentation layer | Keep as learning input on context design; no platform dependency or paid Hex publishing requirement |
| Course and portfolio workflow | Not described in repo | Learning can support building the same project; protect senior-role job-search priority and resist course-driven scope creep |

## Boundaries: what has *not* been decided

- Whether to use any LLM judge, its identity, evaluation rubric, calibration size, agreement measure and cost.
- Whether a Product Analytics Investigator will become a discrete demo, how agent orchestration works, or when it is built.
- (Updated 2026-10-21) Mix-shift vs. within-segment decomposition is the first benchmark family; whether causal inference or retention follows is undecided.
- Dataset choice, API hosts, model version freeze, SQL-tool protocol, dashboard, caching settings, budgets and analysis-plan freeze.
- (Updated 2026-10-21) The earlier four-model, two-context, one-case calibration scope is superseded for the first benchmark by `decisions.md` Amendment 001.

## Suggested staged implementation (proposal, not approved schedule)

1. **Current design close-out:** choose dataset, case semantics, scoring boundaries, APIs and spend ceiling.
2. **Calibration foundation:** four models × two contexts × one correctness case, trace and deterministic grading.
3. **Evaluation maturity:** small golden-case set, repeatable regression runs, analytics failure taxonomy, targeted human annotation; research optional judge calibration only when grading needs warrant it.
4. **Distinctive research:** seeded discrepancy and evidence-based root-cause investigation.
5. **Future agent test subject:** Product Analytics Investigator evaluated by the Lab, potentially informed by the Maven course and Hex workshop.
6. **Separate future product:** Negocio Inteligente adapts suitable generic infrastructure, without importing the Lab's user experience or business logic.

## Questions to resolve before writing significant code

1. Synthetic SaaS (leading candidate) or Olist for the first reference dataset?
2. Monthly net billed revenue calibration case as specified, or another first analytical task?
3. Which provider/host exposes pinned versions of the four selected models reliably and within budget?
4. What is the maximum initial experimental spend, and what restrictions apply to API keys and public deployment?
5. What counts as the canonical result/evidence record for an evaluation run? Design first, implementation later.

**Interpretation:** This document records additions from the course conversation without claiming a course syllabus was independently verified or that exploratory agent ideas have already been approved for the MVP.
