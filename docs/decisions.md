# Design Decisions and Open Questions

**Maintained as of 2026-10-16.** “Agreed” means project direction discussed, **not** an implemented or validated technical choice.

| Area | Decision / position | Status | Rationale |
|---|---|---|---|
| Product | Vendor-neutral AI analytics workflow evaluation, not a leaderboard | Agreed | Compare evidence-based analytical trust |
| Sequencing | Build Analytics AI Evaluation Lab before Negocio Inteligente | Agreed | Senior analytics/engineering career relevance; reuse later only where justified |
| Audience | Analytics engineers/data scientists primary; leaders served in report summaries | Agreed | One useful technical product, not two experiences |
| Capabilities | Analytical correctness + evidence-based investigation | Agreed | Test both numerical answers and justified conclusions |
| Operational trust | Cross-cutting correctness/evidence/safety/reliability/cost lens | Agreed | Avoid artificial separate third subsystem |
| Initial candidates | GLM-5.1, Qwen3.6-27B (provisional), Claude Sonnet 5.5, GPT-6.1 Sol | Agreed shortlist | Two proprietary and two open-weight reference systems |
| Initial matrix | 4 models × raw/governed contexts × one calibration case | Agreed plan | Eight cells before repeats, engineering validation only |
| Research sequence | Calibration foundation, then seeded discrepancy investigation | Agreed | Second release differentiates product |
| Economic analysis | Cost/correct task, caching, retries, human review; gate-first qualification | Agreed principle | Low cost cannot compensate for failing safety/correctness |
| Trust labels | No production certification from MVP; tier-sensitive future requirements | Agreed | Small samples imply inconclusive results |
| Publication | Public report first; interface independent of core engine | Agreed principle | Avoid deployment cost/platform lock-in |
| Dataset | Synthetic B2B SaaS leading, Olist alternative | Open | Weigh realism, defect control and complexity |
| Tooling | Python/SQL/DuckDB/pytest/dbt, Dash/Streamlit/Hex candidates | Open | Choose smallest justified dependencies |
| Open model APIs | Providers, deployments, exact IDs and quantization | Open | Must verify provenance/access before scoring |
| Tool access | Uniform SQL/JSON loop vs. native tool calling | Open | Controlled comparability vs. real-world workflow behavior |
| Inference | Reasoning settings, repeated-run count, ceilings and caching | Open | Providers not directly equivalent |
| Statistical plan | Cluster units, interval method, primary contrasts, sample size | Draft; freeze later | Defensible inference, not fake confidence |
| Threshold policy | T1/T2 thresholds, evidence gates and safety rubrics | Open | Policy choice, not data-derived winner selection |
| Risk/privacy | Public vs. private fixtures, redaction, secrets and contamination | Open implementation | Transparency vs. held-out testing tradeoff |
| Economics | Spending cap, local compute accounting, reviewer-rate assumption | Open | Bound worst-case expense |
| Publishing | Repo license, hosting, frontend | Open | Confirm reproducibility and community access |

## Rule for later decisions

For any consequential choice, record the alternatives considered, scope of the decision, reasons/tradeoffs, date and effects on previous experiments. Changes after experiment freeze need a dated amendment and new result group if comparability changes.
