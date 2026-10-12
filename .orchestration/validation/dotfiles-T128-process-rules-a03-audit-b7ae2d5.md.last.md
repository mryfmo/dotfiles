[P2] high specification home/dot_agents/skills/agmsg-orchestration/SKILL.md:71 — The interim task-file review must verify that a `closed:` test exists in the implementation PR before implementation begins. With no schema present, tasks introducing new tests cannot satisfy this timing requirement; acceptance’s dismissal of thread 4240646082 does not resolve it.

[P2] high implementation home/dot_agents/skills/agmsg-orchestration/SKILL.md:201 — The new ten-minute Codex-review trigger relies on queries matching any `Bot`. A CodeRabbit review satisfies those queries, suppressing `@codex review` and ending the wait without a Codex review; independently reproduced with a CodeRabbit fixture.

[P2] high conformance tests/unit/test_agmsg_orchestration_docs.py:259 — All 36 tests still pass after independently removing the S1/S2 decision sentence or the threat-table test-existence, owner-membership, and minimum-reason requirements. These gaps contradict the task’s sentence-removal requirement and threat row 2’s claimed control.

[P2] high orchestration .orchestration/validation/dotfiles-T128-process-rules-a03-pr-feedback.json:80 — All 90 dispositions are empty, including unresolved thread 4243369347. Step 10.1 requires completed dispositions before the audit; prose replies and historical acceptance summaries do not populate the gate’s required fields.

INV-1: holds .orchestration/tasks/dotfiles-T128-process-rules-a03.md:44 — Review-tier routing and all three dispatched task-copy hashes verified within this task’s scope.

INV-2: holds .github/workflows/test.yaml:58 — At the audited head, main carries design `4520b8f0…` and the merged workflow changes; the diff fits the caps: three files, 19 non-test additions, 202 test additions.

INV-6: holds .orchestration/acceptance/dotfiles-T128-process-rules-a02-design-reset.md:18 — Independent redesign messages and hashes verified; a03 has no reached threshold.

INV-12: violated tests/unit/test_agmsg_orchestration_docs.py:291 — Required rule removals remain undetected.

Orchestration findings: 1

📝 まとめ: Read-only audit of [PR #318](https://github.com/mryfmo/dotfiles/pull/318) completed with four findings. All 36 docs tests and final-head Actions passed; nothing was modified.

Not checked: local Bats, the integration gate, or runtime permission logs; the findings remain integration risks.
Verdict: incorrect