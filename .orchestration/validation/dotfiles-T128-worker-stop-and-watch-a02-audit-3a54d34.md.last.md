Audited [PR #323](https://github.com/mryfmo/dotfiles/pull/323) at `3a54d340e9078ba3565237f6d73a00d8fc2d75e9`.

[P2] 0.98 implementation home/dot_agents/skills/agmsg-orchestration/SKILL.md:165 — The watcher counts only fixes following P0/P1 findings, although A2 stops after the third Bot round regardless of priority. This PR’s documented second fix round, `2c8dce27 → 040b32f9`, followed only P2 findings and disappears from that count. Repeated P2-only fixes can therefore evade the watch’s cap.

[P2] 0.99 orchestration .orchestration/tasks/dotfiles-T128-worker-stop-and-watch-a02.md:57 — Disposition `4244248692` incorrectly restricts threat-table coverage to paths: SKILL:71 explicitly includes orchestrator-controlled effects. Its alternative “human-only permission gate” control is also unsupported: the manifest uses `defaultMode: auto` with `ask: []`. Neither control verifies task/PR/worktree binding before forced removal.

[P2] 0.99 orchestration .orchestration/acceptance/dotfiles-T128-worker-stop-and-watch-a02.md:39 — Disposition `4244378809` claims a mismatched RESULT head is revised and “never counted,” but `scripts/regime-counters.sh:114` permanently selects the first RESULT. Replaying a wrong head, a revise, and a corrected RESULT retained the wrong baseline. The actual head matches here; that does not establish the claimed mismatch control.

[P3] 1.00 specification .orchestration/tasks/dotfiles-T128-worker-stop-and-watch-a02.md:30 — Premise 1 claims six reviewed heads after 03:09Z, but its own timestamp evidence contains four. Correct the premise and its “holds” assessment.

Verification: all 45 documentation tests passed against the head’s Git objects; all five fixtures match their sections; all 33 token-removal checks failed both the relevant token test and whole-section test. GitHub confirms successful final-head workflows. The task-copy hash matches dispatch.

The ledger covers all 24 Bot findings. Dispositions `4244128846` and `4244175775` are supported by the final worker/orchestrator division of responsibility; `4244248692` and `4244378809` are not. The first three audit findings belong to existing classes `fix-round-definition`, `threat-row-outside-paths`, and `result-head-binding`.

INV-1: holds .orchestration/tasks/dotfiles-T128-worker-stop-and-watch-a02.md:95 — task copy and review-tier audit requirements satisfied.
INV-6: violated .orchestration/acceptance/dotfiles-T128-worker-stop-and-watch-a02.md:39 — the claimed invalid-baseline exclusion does not work.
INV-12: holds tests/unit/test_agmsg_orchestration_docs.py:240 — fixture and removal checks verified.

Orchestration findings: 2

📝 まとめ: 読み取り専用で監査し、4件の指摘を確認しました。Bats と実際の worker 停止は未実施で、誤停止・停止漏れのリスクが残ります。
Verdict: incorrect