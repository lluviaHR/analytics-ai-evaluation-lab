# Design Decisions and Open Questions

**Maintained as of 2026-10-21** (see Amendment 001 below). “Agreed” means project direction discussed, **not** an implemented or validated technical choice.

| Area | Decision / position | Status | Rationale |
|---|---|---|---|
| Product | Vendor-neutral AI analytics workflow evaluation, not a leaderboard | Agreed | Compare evidence-based analytical trust |
| Sequencing | Build Analytics AI Evaluation Lab before Negocio Inteligente | Agreed | Senior analytics/engineering career relevance; reuse later only where justified |
| Audience | Analytics engineers/data scientists primary; leaders served in report summaries | Agreed | One useful technical product, not two experiences |
| Capabilities | Analytical correctness + evidence-based investigation | Agreed | Test both numerical answers and justified conclusions |
| Operational trust | Cross-cutting correctness/evidence/safety/reliability/cost lens | Agreed | Avoid artificial separate third subsystem |
| Initial candidates | GLM-5.1, Qwen3.6-27B (provisional), Claude Sonnet 5.5, GPT-6.1 Sol | Agreed shortlist | Two proprietary and two open-weight reference systems |
| Initial matrix | ~~4 models × raw/governed contexts × one calibration case~~ | **Superseded 2026-10-21** (Amendment 001) | Replaced by the phased architecture comparison below |
| Primary experimental factor | Architecture: generated SQL (Arm A), approved tools (Arm B), hybrid (Arm C); governed context held constant | Agreed direction (2026-10-21) | Isolates one variable; fits available build time |
| Phasing | Phase 0 instrument calibration → Phase 1 Arm A baseline (one model) → Phase 2 add Arms B and C → Phase 3 four models | Agreed direction (2026-10-21) | No performance claims until the instrument is verified and scoring contracts are stable |
| First benchmark | Trial-to-paid conversion rate; attribute change to customer mix vs. within-segment behavior using the symmetric (Kitagawa) decomposition | Agreed direction (2026-10-21) | Mathematically verifiable ground truth; realistic product-analytics question |
| Fixtures | Exact fixtures first (clean integer counts, no sampling noise) for instrument calibration; seeded stochastic fixtures later, scored against realized data | Agreed direction (2026-10-21) | Exact fixtures isolate bugs; stochastic data sets the noise threshold |
| Reporting | Covered (tool-catalog) questions and out-of-coverage questions reported separately | Agreed direction (2026-10-21) | A blended accuracy figure would hide the main architectural finding |
| Research sequence | Calibration foundation, then seeded discrepancy investigation | Agreed | Second release differentiates product |
| Economic analysis | Cost/correct task, caching, retries, human review; gate-first qualification | Agreed principle | Low cost cannot compensate for failing safety/correctness |
| Trust labels | No production certification from MVP; tier-sensitive future requirements | Agreed | Small samples imply inconclusive results |
| Publication | Public report first; interface independent of core engine | Agreed principle | Avoid deployment cost/platform lock-in |
| Dataset | First benchmark: synthetic row-level trial/conversion data (SMB, Mid-market, Enterprise). Invoice/revenue schema and Olist deferred | Agreed for first benchmark; open for later cases | Weigh realism, defect control and complexity |
| Tooling | Python/SQL/DuckDB/pytest/dbt, Dash/Streamlit/Hex candidates | Open | Choose smallest justified dependencies |
| Open model APIs | Providers, deployments, exact IDs and quantization | Open | Must verify provenance/access before scoring |
| Tool access | Uniform SQL/JSON loop vs. native tool calling | Open | Controlled comparability vs. real-world workflow behavior |
| Inference | Reasoning settings, repeated-run count, ceilings and caching | Open | Providers not directly equivalent |
| Statistical plan | Cluster units, interval method, primary contrasts, sample size | Draft; freeze later | Defensible inference, not fake confidence |
| Threshold policy | T1/T2 thresholds, evidence gates and safety rubrics | Open | Policy choice, not data-derived winner selection |
| Risk/privacy | Public vs. private fixtures, redaction, secrets and contamination | Open implementation | Transparency vs. held-out testing tradeoff |
| Economics | Spending cap, local compute accounting, reviewer-rate assumption | Open | Bound worst-case expense |
| Publishing | Public research repository; all rights reserved for now. Hosting and frontend undecided | Licensing position agreed 2026-10-21; hosting open | Preserve future commercial product options while sharing work for review |

## Rule for later decisions

For any consequential choice, record the alternatives considered, scope of the decision, reasons/tradeoffs, date and effects on previous experiments. Changes after experiment freeze need a dated amendment and new result group if comparability changes.

## Amendment 001 — 2026-10-21: architecture is the primary experimental factor

**Decision.** Phases 1-2 compare three architectures on identical cases with governed context held constant: generated SQL with governed definitions and read-only execution (Arm A), approved parameterized analytical tools with no arbitrary SQL (Arm B), and a hybrid of approved tools plus controlled read-only SQL for out-of-coverage questions (Arm C). Phase 3 extends the comparison to the four candidate models once evaluation contracts and scoring methods are stable. No arm is presumed superior; positive, negative and inconclusive findings will be reported.

**Alternatives considered.** (1) Varying raw vs. governed context as the primary factor. Deferred as a later ablation. (2) Starting with all four models. Deferred to Phase 3. (3) Starting with the net-billed-revenue case in `benchmarks/case-001-spec.md`. Deferred; the conversion mix-shift benchmark is used first.

**Reasons.** One variable at a time; verifiable ground truth from a symmetric decomposition; the standardized-primitives vs. free-form SQL question is practically important for analytics teams; the phasing fits available build time.

**Effects on earlier documents.** The earlier eight-cell matrix (four models × two contexts × one case) is superseded for the first benchmark. Documents dated 2026-10-16 are historical snapshots where they conflict with this amendment. No experiments had been scored when this amendment was made.

**Still open.** Decomposition convention wording and numerical tolerances (to be fixed and committed before scored evaluation), the Arm B tool catalog and coverage labels (to be versioned before scoring), grader design, SQL sandbox enforcement, and the noise threshold for "no real change" (to be calibrated from stochastic runs).

**Naming note.** `case-001-spec.md` (net billed revenue) and `case_001`-`case_004` in the code (conversion fixtures) are different things. Consider renaming one family to avoid confusion.

## Amendment 002 — 2026-10-21: licensing deferred

**Decision.** The project is publicly viewable for portfolio and research purposes, but no open-source license is granted at this stage. The README states “All rights reserved”; no `LICENSE` file is included.

**Alternatives considered.** MIT for code and CC BY 4.0 for documentation, or a single permissive repository license. These remain options for later.

**Reason.** Preserve flexibility to use the evaluation technology in future business analytics products. This does not prevent later licensing of code controlled by the author.
