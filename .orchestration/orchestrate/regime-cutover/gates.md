# Human gates (parked; each has a default applied when no answer arrives)

| id | gate | moment | options | default |
| --- | --- | --- | --- | --- |
| G1 | Claude login for the bridge child: the host's Claude Code login is used by the Agent SDK; if U1 reports a Keychain or login prompt, the operator runs the exact command U1 writes to `handouts/U1-operator-steps.md` | when U1 reports | run the command / abandon the bridge route (fallback `anthropic/` API key) | run | PASSED 2026-10-23T01:31:20Z: PONG via the host login (pilot-facts #G1) |
| G2 | `/login openai-siwc` in the three audit-side omp profiles (audit, audit-r2, security), browser consent, agent name `omp-dotfiles` (decision 28) | at X2 of the runbook (after make update) | 3 logins / fewer profiles | 1 login now (audit), audit-r2 and security when first used | PASSED 2026-10-23T06:17:05Z (X2/X3) |
| G3 | Adoption of plan 025 v15 (v14 + the R12R-10 correction) as the program's reference | after wave 1 lands (v15 = v14 + R12R-10 correction, coordinator bookkeeping) | adopt / amend | adopt |
| G4 | X cutover steps that need the operator (herdr panes, `make update`, closing the agmsg seats) | after U7, U8, U9, U10 land | per plan §7 | per plan | passed 2026-10-23T10:56:40Z: X0 (three times: initial, after U6b, after U10b), X1, X2/X3, X5 (after U7c), X6, X7 (after U6b), X8, X9 (worktree-path form), final X; pilot-facts X0..X final | relaunch round trip after the fix units passed 2026-10-23T14:06:39Z (rows 117/122) |
| G5 | Dropping the `openai-codex` fallback (decision 29 default E1) | at E1 | E1 / X step 1 | E1 |
| G6 | The `omp-dotfiles-probe` agent registration left in the ChatGPT account by #S0 | any time | delete in ChatGPT settings / keep | keep until U12 passes | U12 passed: the operator may delete the `omp-dotfiles-probe` entry in ChatGPT settings at any time |
