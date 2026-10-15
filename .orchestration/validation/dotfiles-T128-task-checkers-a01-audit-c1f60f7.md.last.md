[P2] high implementation scripts/orchestrator/ledger-check.py:23 — Any bot’s inline comment creates a required ledger ID; the gate accepts only the Codex Bot’s. Reproduced with a CodeRabbit comment: gate IDs were empty, checker reported one gap. This can block an audit through PR feedback without modifying the orchestrator checkout. Amendment 2’s parity test should catch this negative case; it currently covers review bodies only. This inherited mismatch causes false rejection, so I downgrade the local P1.

[P2] high implementation scripts/orchestrator/orch-audit.sh:52 — Default invocation skips tracking verification and executes the sibling checker at line 54. A locally replaced checker can bypass the ledger check or execute before the read-only audit starts. This requires control of the orchestrator’s checkout; the audited PR does not supply that executable. Also, the explicit override checks tracking only—not equality with HEAD. The validator has both checks. I downgrade the local P1 because no PR-controlled execution path was established.

[P2] high orchestration .orchestration/acceptance/dotfiles-T128-task-checkers-a01.md:51 — The record reports two amendments and two questions but contains no required `regime-counters.sh` output, source fallbacks, or threshold disposition. The standing SKILL requires this evidence before acceptance actions. Calling the questions correct does not exempt them from INV-6’s counts; S2 compliance remains undocumented.

Verified against `c1f60f73`:

- Task hash `a309b394…` and copied worker evidence match the branch.
- Replay: **15/86 pass**; the other **309** files retain their original exceptions.
- Ten historical failing sets match. Four additional C4 lines affect exactly the three reported files; their entries and disposition text match the evidence.
- Ledger fixtures produce **36** and **2** findings.
- SKILL and pinned fixture contain exactly the same two sentence replacements, committed together. Superseded forms remain in the docs tests.
- All changed paths are allowed. Supplied CI evidence contains 12 successful checks plus one successful status, with all 11 feedback items dispositioned.

The task declares no front-matter invariant set; these assessments cover its referenced cap and recorded counter obligation.

INV-2: holds .orchestration/tasks/dotfiles-T128-task-checkers-a01.md:144 — 12 files outside orchestration; 194 added plus 10 deleted outside tests; 752 test additions.
INV-6: violated .orchestration/acceptance/dotfiles-T128-task-checkers-a01.md:51 — Required counter and threshold-decision evidence is absent.
Orchestration findings: 1

Not checked: live GitHub status was unavailable; filesystem-writing tests were not rerun. In-memory replays and shellcheck passed; nothing was modified.
Verdict: incorrect