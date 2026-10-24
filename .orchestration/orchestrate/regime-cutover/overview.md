# Overview (append-only PR and issue DB)

## Existing PRs and branches the program builds on (gh, 2026-10-23T01:09Z)

- #406 draft `tools/omp-config-render` head 2e978db7 "feat(agents): render omp's default model role from the manifest (T129 omp-config-render a01)": files `home/.chezmoitemplates/omp-config-managed.yml`, `home/dot_omp/agent/modify_config.yml`, `scripts/generate-agent-configs.py`, `home/dot_agents/agent-config.yaml`, `home/dot_agents/README.md`, `home/dot_agents/model-profiles.env`, tests. Picked up by U4.
- #407 draft `tools/hcom-dispatch-bus-a01` head dfa9001b: records only (a01 findings). The a02 worktree branch `tools/hcom-dispatch-bus-a02` (d961efa3) is records only. U5 starts a fresh branch `feat/hcom-dispatch-bus` and reads both reports.
- Open PRs of the former regime (19, per the project map 2026-10-23 08:31 JST) are not touched by this program; close-or-carry is a coordinator decision at the end (gates).

## Program PRs

| unit | PR | branch | head | state | verdict |
| --- | --- | --- | --- | --- | --- |
| U3 | #458 | feat/openai-siwc-extension | 0f9cfdf5 → main 8846f34b | landed 2026-10-23T03:48:01Z | unit-test-verified (round 2) |
| U4 | #406 | tools/omp-config-render | d661a9f4 → main 34e216e9 | landed 2026-10-23T03:48:01Z | unit-test-verified |
| U5 | #460 | feat/hcom-dispatch-bus | 940d05b7 → main a39ce5d6 | landed 2026-10-23T02:00:14Z | unit-test-verified |
| U6 | #459 | feat/omp-seat-policy | f201d2fe → main 6f154b60 | landed 2026-10-23T02:49:41Z | unit-test-verified |
| U8 | #463 | feat/omp-run | d4dd2b16 → main | landed 2026-10-23T03:55:09Z | unit-test-verified |
| U2 | #461 | feat/pi-claude-bridge-asset | c4d18653 → main a729702e | landed 2026-10-23T04:23Z | live-verified (operator install + PONG) |
| U13 | #462 | feat/regime-ci-program-marker | 62f0f15d → main 3953e9cf | landed 2026-10-23T03:06:51Z | unit-test-verified |
| U7 | (pending) | feat/hcom-seat | | in-flight | |
| U10 | #465 | feat/omp-pstack-skills | 50a11a7c → main | landed 2026-10-23T04:36:23Z | unit-test-verified |
| records | #464 | records/program-store-1 | 54644817 → main 0f0fe4c6 | landed 2026-10-23T04:03Z | n/a (records only) |
| records 2 | #467 | records/program-store-2 | b8742836 | auto-merge armed (the store itself, missed by #464) | n/a (records only) |
| U14 | #468 | feat/omp-role-overlays | 99ddf5cc → main | landed 2026-10-23T05:35:30Z | unit-test-verified |
| U7 | #466 | feat/hcom-seat | ccc40eae → main c67d4d0b | landed 2026-10-23T05:58:55Z | unit-test-verified |
| U9 | #469 | feat/orchestrator-seat | af35fd50 → main | landed 2026-10-23T05:57:12Z | unit-test-verified |
| U7c | #470 | fix/hcom-seat-go | d7ea7262 → main 8e55aedd | landed 2026-10-23T06:40:24Z | unit-test-verified; live: hcom-seat started the seats at X7 relaunch and final X |
| U6b | #471 | fix/audit-seat-reply-route | f95738b4 → main 844b047e | landed 2026-10-23T07:3xZ | unit-test-verified; live: audit VERDICT row 47 |
| U9b | #472 | fix/stop-gate-audit-verdict | 12b27b3d (U9c) → main a3526828 | landed 2026-10-23T08:40:55Z | unit-test-verified; gate rule not yet live-measured |
| U10b | #473 | feat/pstack-skills-asset | 81a48c2a → main f0bbb5d6 | landed 2026-10-23T10:50:09Z | unit-test-verified; live: 82 skills, poteto-mode hidden in both profiles |
| U9d | #475 | fix/audit-worktree-positioning | a4d1045f → main 4f004231 | landed 2026-10-23T12:30Z | unit-test-verified; live: the positioning step moved the audit tree before rows 122 |
| U14b | #476 | fix/omp-overlays-no-wizard | ac7a4e0f → main 28b2855c | landed 2026-10-23T12:1xZ | unit-test-verified; live: 0 wizard lines in the three relaunched panes |
| U6c | #477 | fix/audit-policy-name | 3809e407 (U6d) → main 994c3616 | landed 2026-10-23T13:57Z | unit-test-verified; live: audit VERDICT row 122 through hcom-reply |

## Done predicate, measured (U44, 2026-10-24T13:3xZ, worker-2-rosa)

The predicate is `decisions.tsv` row 2 (file line 3, 2026-10-23T01:05:00Z, frame): "12 units verified; final check on the real artifact (3 omp seats on hcom, one TASK→RESULT→verdict round trip, claude-bridge and openai-siwc turns, pstack listed, Claude Code/Codex seats 0)". Every line below was measured on this host by U44; the store files were read in the coordinator's checkout (`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/`, standing order 20), the bus with `HCOM_DIR=~/.local/state/hcom-regime`.

| clause | result | measurement (pasted) |
| --- | --- | --- |
| 12 units verified | met (41 landed) | `awk -F'\t' '$3=="landed"' units.tsv \| wc -l` → `41` (coordinator store, 13:34:54Z; 3 more rows are `done`: U1, U11, U12) |
| 3 omp seats on hcom | met (5 seats, all omp, one per role at least) | `hcom list --json \| jq -r '.[] \| [.name,.tool,.status,.directory] \| @tsv'` → `worker-2-rosa omp active ~/.local/state/omp-seats/worker-2`, `audit-kana omp active ~/.local/state/omp-seats/audit`, `worker-logo omp active ~/.local/state/omp-seats/worker`, `worker-3-mure omp active ~/.local/state/omp-seats/worker-3`, `orchestrator-sari omp active ~/Workspace/dotfiles` |
| one TASK→RESULT→verdict round trip | met (U43, verdict correct, merged) | `bus-history.sh regime --limit 2000` rows: `6252 sari→nova AGMSG-TASK task_id=U43`; `6312 nova AGMSG-RESULT task_id=U43 pr=…/pull/497 head=67029e60…`; `6331 sari→kimi AGMSG-TASK task_id=U43-audit head=67029e60…`; `6353 kimi AGMSG-VERDICT task_id=U43-audit verdict=correct head=67029e60… findings=0`; ledger.tsv:62 `2026-10-24T12:05:00Z U43 497 67029e60 correct`; `6619 sari MERGED task_id=U36 sha=c84070db… note=PR #497 squash…`. Under the post-U35 kinds the latest trip is U28: `7131 AGMSG-TASK task_id=U28` → `7668 RESULT task_id=U28 pr=…/pull/504 head=6191b1b9…` → `7683 TASK task_id=U28-audit` → `7856 VERDICT task_id=U28-audit verdict=incorrect findings=6` (a verdict, not a landing) |
| a claude-bridge turn | met | nova (worker of the U43 trip; `hcom list --stopped nova` → `Tool: omp`, `Directory: ~/.local/state/omp-seats/worker-2`): `jq -r 'select(.message.role=="assistant") \| "\(.message.provider)/\(.message.model)"' <its transcript> \| sort \| uniq -c` → `1203 claude-bridge/claude-opus-5-5`; profiles: `worker.yml:3 default: claude-bridge/claude-opus-5-5`, `orchestrator.yml:3 default: claude-bridge/claude-fable-5-1` |
| an openai-siwc turn | met | kimi (audit of the U43 trip; `hcom list --stopped kimi` → `Tool: omp`, `Directory: ~/.local/state/omp-seats/dotfiles/audit`): same jq → `170 openai-siwc/gpt-6-astra`; profile `audit.yml:3 default: openai-siwc/gpt-6-astra` |
| pstack listed | met | `scripts/update-agent-assets.sh check_pstack` → `pstack skills reach omp/18.11.3: 80 skills listed, poteto-mode among them.` exit 0. pstack is a skill set, not a binary: `command -v pstack` exits 1 by design (manifest `assets.pstack`, `home/dot_agents/agent-config.yaml:639`) |
| Claude Code/Codex seats 0 | met | `hcom list --json \| jq -r '.[].tool' \| sort \| uniq -c` → `5 omp`; the stopped seats read above are `Tool: omp` as well |

All seven clauses are met on this host at 2026-10-24T13:3xZ. Open units at the time (`units.tsv` state ≠ landed/done): U19, U21 to U24 `gate`; U20, U28, U38b, U44 `in-flight`.

## Residuals index (open at the program's close-out, 2026-10-24)

Each row is open; standing order 22 applies (a scheduled unit or the operator's own acceptance in `decisions.tsv`).

| residual | source | owner | state |
| --- | --- | --- | --- |
| the `uninstall_*` installer functions have no caller in the test suite (none ever asserted them) | U41: units.tsv:50, decisions.tsv:144, ledger.tsv:63 | orchestrator seat (no unit scheduled) | open: needs a unit or an operator acceptance |
| U38's inherited rows: the step-to-target pin test (`tests/unit/test_shellcheck_target.py`), the dirname checker's multi-line and heredoc gap (`scripts/ci/masked-dirname-check.sh`), the default group's xargs form that passes silently on an empty list under BSD xargs | U38b brief row units.tsv:47 | U38b, worker-3-mure, PR #505 | in-flight: RESULT bus row 7921 (head 1462f1e5) reports the xargs form gone and still names (a) the pin test and (b) the multi-line and heredoc gap as residuals; audit VERDICT row 8108 `incorrect findings=2` at 1462f1e5, both on the checker (row 8119: F1 heredoc delimiter quote removal, F2 the inner opener split from `dirname` across lines) |
| the `.ua` index refresh: `.ua/meta.json` `lastAnalyzedAt 2026-10-02T14:12:51Z`, `gitCommitHash 940a3a2b` (before every program unit) | U40: units.tsv:49, ledger.tsv:66 ("`.ua` left as the index residual") | orchestrator seat (no unit scheduled) | open |
| the one-time store move of the dotfiles program (`~/.local/state/hcom-regime` → `~/.local/state/hcom/dotfiles`, seat worktrees under `~/.local/state/omp-seats/dotfiles/`) | README.md:984-991 "Run a program in another repository"; scripts/orchestrator/README.md:224 | orchestrator seat, at deployment, every dotfiles seat stopped | open; the stopped kimi worktree `~/.local/state/omp-seats/dotfiles/audit` sits on the move's audit target (clean-up table, U44 rows) |
| the Ubuntu host's first `make update` after U31 | handouts/U31-ubuntu-make-update.md rows 2 to 8 (the brief says 2 to 9; the handout has 8 rows, lines 7-14) | operator, on the Ubuntu host | open: operator-only |
