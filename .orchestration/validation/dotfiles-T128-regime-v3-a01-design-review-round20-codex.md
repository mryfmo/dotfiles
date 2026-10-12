reviewed_at: 2026-10-12T11:41:07Z (headless run started 11:40Z after the 11:11Z run hung on stdin, M-20261012-12)
reviewed_at: 2026-10-12T11:41:07Z  
reviewer: codex-review-dot-h001 (headless)  
profile: review  
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@7f007ec41c9b0dedded66c964ba8e858d1d604e40b10a0ab278966f7eb2a2ae6  
round: 20  
previous: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round19-codex.md

INV-2: accepted

INV-12: accepted

## Findings

- P3 high — `home/dot_agents/skills/agmsg-orchestration/SKILL.md:69`: the task-file-review stop condition still requires a `-contract-a01` mapping. This is the sole operative sentence found that depends on the retired contract scheme. Owner: `dotfiles-T128-v1b-pr-caps-a01`, whose V1b scope includes the corresponding SKILL sentence. Its PR should replace this with the ordinary implementing-task/invariant mapping check.
- P3 high — `.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:222`: dormant contracts, `REGIME_CONTRACT`, and contract PRs remain only in the historical review narrative. Owner: the design record itself; this is historical evidence, not an operative contract dependency, and should remain unchanged.
- P3 high — `.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:224`: the v18 delta statement names the removed mechanisms to document their retirement. Owner: the design record itself; this is explanatory history, not an operative dependency.
- No matching sentence exists in `AGENTS.md`.

The narrowed INV-12 still closes its mapped undeclared-change threat: `main-tests` runs main’s test module against every script changed outside `allowed_files`, so an undeclared script change is exercised by main-pinned tests. An intentional change to a script declared in `allowed_files` is now judged by the PR’s own tests, the orchestrator’s diff review, and the trusted-root audit, including its check for deleted or weakened fails-when-removed tests.

Both new mappings are correct:

- `dotfiles-T128-v0-main-tests-a02: [INV-12]` owns the replacement undeclared-change regression guard.
- `dotfiles-T128-gate-evidence-a01: [INV-6]` owns the gate evidence grammar and S6 refusal at INV-6’s mandatory enforcement point.

The independently computed SHA-256 matches the requested hash. The diff against `HEAD` supports the stated v18 delta: it removes the operative dormant-contract machinery, updates INV-2’s required-job formulation, aligns the enforcement and wave rows, and adds the two correctly mapped tasks.

No implementation or tests were executed, and no files were modified. Residual risk remains the design’s stated in-process test-forgery limitation and the temporarily stale SKILL sentence until V1b lands.

📝 まとめ: v18 のハッシュと main 差分を検証し、INV-2 と INV-12、および二つの implementing-task mapping を受理しました。唯一の現行 dormant-contract 依存は V1b 所有の SKILL 文です。

Design verdict: accept