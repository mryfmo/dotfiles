# Measured baseline (agmsg history + GitHub, 2026-10-11)

| task | PR | files | +lines | TASK sends | amendments | PONG questions | RESULTs | revises | audits (incorrect) | audit findings | Bot threads (heads) | Bot P0/P1 | wall |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| T114 canonical-clone | - | - | - | 1 | 0 | 0 | 5 | 6 | 3 (3) | 10 | - | - | 21.5h |
| T115 worker-audit-xhigh | 305 | 7 | 18 | 1 | 1 | 0 | 2 | 2 | 1 (0) | 0 | 1 (1) | 0 | 1.0h |
| T116 on-demand-workers | 306 | 11 | 529 | 1 | 1 | 0 | 2 | 3 | 1 (0) | 0 | 2 (1) | 2 | 3.4h |
| T117 upgrade-outside | 308 | 8 | 156 | 1 | 2 | 0 | 2 | 3 | 1 (0) | 0 | 6 (2) | 0 | 2.1h |
| T118 rolling-tools | 310 | 35 | 881 | 2 | 7 | 0 | 10 | 20 | 8 (7) | 16 | 16 (7) | 0 | 10.6h |
| T119 rolling-release | 312 | 37 | 3191 | 10 | 8 | 8 | 6 | 5 | 4 (4) | 12 | 25 (11) | 7 | 11.1h |
| T120 npm-provenance | 315 | 19 | 1489 | 8 | 6(8 in file) | 1 | 0 | 0 | 0 | 0 | 15 (5) | 8 | 4.9h, reset |
| T124 W1 validator | 313 | 20 | 2642 | 10 | 8 | 6 | 2 | 2 | 0 | 0 | 52 (10) | 31 | 5.7h, halted |
| T124 W3b audit | 314 | 9 | 1462 | 10 | 5 | 0 | 1 | 0 | 0 | 0 | 24 (4) | 2 | 4.0h, halted (reset (d) fired) |

Audit timing (T119, four headless audits): files written 11:48, 13:55, 15:52, 17:23 local; each run ~15-25 min; 4 audits ≈ 1.3 h of an 11.1 h task. The audit is not the wall-clock bottleneck; rounds are.
Where defects were found (T118/T119): Bot threads 41, audit findings 28, operator corrections of premise 2 (T119 Amendments 7-8). Audit `incorrect` verdicts: 11 of 12 runs on T114/T118/T119.
Every acceptance record: cost n/a (tokens never measured). Session JSONL carries per-message usage (cache_read_input_tokens etc.), so cost is measurable offline.
Bespoke code on the halted branches: validate-task.py 503 + high_risk_paths.py 316 + tests 695 (PR 313); audit-head.sh 555 + schema 47 + tests 756 (PR 314). 33 of 52 Bot threads on PR 313 are on validate-task.py (own YAML parser, own glob NFA): bypass findings on a hand-written trust-boundary parser.
Thresholds T126 INV-6 applied to its own program: W1 8 amendments (>4), 2 revises (=2) -> reset; W3b Bot P1 on two post-RESULT heads -> reset. The orchestrator was preparing a waiver instead.
