# Report: dot-herdr-agents-add-worker-T22-a01

## Revision 4 (T34), worker claude-standard-dot-a005

- **Worktree:** `.claude/worktrees/worker-c`, branch `feat/herdr-agents-worker-seat` from `origin/main` 2c1b304. It was moved onto e0b7fb9, the ruling-addendum commit, which changes only `.orchestration`.
- **task_rev:** verified by sha256 against `origin/main`: `b81b1b63…` at 2c1b304, then `c3645fc7…` at e0b7fb9 after the ruling addendum.
- **Cleanup:** the merged local `feat/agmsg-upstream-sync` was deleted.
- **PR:** https://github.com/mryfmo/dotfiles/pull/206, head `e226c27a756fcdc921d831bec320db37b2dc1c3a`. CI is green on 3eeaeee, 9d5cf7c and e226c27: every check passes and nix is skipped. The verbatim output is in the validation file.
- **Commits:**
  - `3eeaeee` deliverable A (pair worker seated in its worktree);
  - `9d5cf7c` deliverable B (`--add-worker`/`--remove-worker` on agmsg spawn/despawn);
  - `e226c27` fixes for the independent-review findings.

### Rulings, all approved (ruling addendum e0b7fb9)

1. `home/dot_agents/model-profiles.env` was added to allowed_files, regenerated only.
2. **Identity naming:**
   - reuse the single seat registered at the worktree;
   - otherwise derive `<kind>-<profile>-<suffix>-aNNN` from the orchestrator's non-worker (no `-aNNN`) identity at the main checkout, with its team, its suffix (last dash segment) and the next free NNN;
   - refuse on ambiguity.
3. **#367 turn-only delivery is accepted as fact.** Upstream `session-start.sh` skips sessions under `.claude/worktrees/`. So the worktree-seated pair worker (started with `herdr agent start`, no actas boot) has no Monitor watch. Delivery arrives through the worktree's Stop hook (`check-inbox.sh` has no such skip) at turn end, e.g. after agmsg-dispatch's wake prompt starts a turn. The acceptance criterion stands: a PING arrives without `inbox.sh`.
4. `leave.sh dotfiles claude-standard-dot-a006` at the main checkout is the orchestrator's at acceptance. Until then, `bootstrap_agmsg` warns that the main checkout's claude-code identity is ambiguous: it now expects only the orchestrator there.
5. The design notes and the spawn-options route were approved.

### Deliverable A: the pair worker is seated in its worktree

1. **Manifest.** `worker_worktree: .claude/worktrees/worker-c` renders into `model-profiles.env` as `HERDR_AGENTS_WORKER_WORKTREE`, through the same manifest→env path as `worker_kind`/`worker_profile`. herdr-agents reads it from the env file only, with no ad-hoc override. The generator, the validator and herdr-agents all accept exactly one path segment under `.claude/worktrees/` (no `.`/`..`).
2. **herdr-agents seat preparation** (`prepare_worker_seat`) runs before every worker agent start: full mode (new workspace, heal split, heal of an agentless labeled pane, heal of a reused empty pane), attach repair, and `--restart-worker`.
   - **Applicability** (`worker_seat_applies`, decided before any side effect). The seat applies only when DIR is a git main checkout whose worker worktree exists, or that has `origin/main` and at least one orchestrator identity. Anywhere else the legacy main-path seat stays unchanged, with the T14 guard. That covers an unregistered repository, a linked worktree and a non-git directory.
   - **Identity.** Derived first (refusal leaves nothing behind), then the worktree is created detached at `origin/main` when missing, or an existing path is validated as a worktree of this repository (its checkout is never changed). Then comes `AGMSG_RESOLVE_PROJECT=0 join.sh <team> <name> <type> <worktree>`, unless a seat already exists.
   - **Delivery.** `delivery.sh set both claude-code <worktree>` or `set turn codex <worktree>`, when the worktree's Stop hook is missing.
   - **Pane.** The worker pane is split with `--cwd <worktree>` and keeps `AGMSG_RESOLVE_PROJECT=0`, plus `AGMSG_CC_MONITOR_KEEP_ALIVE=1` for claude, which is inert per #367.
   - **Reused panes** (restart after `/exit`, heal of an agentless pane) are moved in with `herdr pane run <pane> 'cd -- <worktree>'`, because `herdr agent start` has no cwd option. When the pane never reaches a shell prompt, herdr-agents refuses with exit 1.
   - **Self-attach.** The worker's own SessionStart `--attach` exits quietly when its cwd is the configured worktree.
   - **T14 guard.** `require_distinct_worker_identity` now runs only for the legacy seat. `bootstrap_agmsg` expects only the orchestrator at the main checkout when the seat applies. `--bootstrap-agmsg` also adds the worker's delivery hook when the worktree exists.
3. **Rules, SKILL and README.**
   - The interim milestone `inbox.sh` rule is retired for worktree-seated workers. It still applies to a worker acting from a main-path pane until `--restart-worker` re-seats it.
   - The delivery statement now says: worker panes run in their worktree, and turn delivery reaches them directly through the worktree's Stop hook (#367 stated).
   - The Codex AGENTS.md has no interim-rule sentence, so it has no mirror change.
4. **Tests** (all pass; mutation baseline against unmodified `origin/main`: 6 of 7 fail):
   - reseat of a main-path worker (worktree auto-created, `join … resolve=0` at the worktree, delivery at the worktree, `/exit` < `cd` < agent start);
   - reuse of an existing seat and hook;
   - full mode splits in the worktree;
   - a path that is not a worktree is refused;
   - an ambiguous orchestrator is refused;
   - the quiet worker attach;
   - generator and validator `worker_worktree` accept/reject cases.

### Deliverable B: parallel workers on upstream seating

5. **Verification gate: passed, no PONG needed.** spawn CAN carry the full profile args. `spawn.sh` splices every token of `$AGMSG_SPAWN_OPTIONS_FILE`'s per-type section into the boot command for every terminal driver (spawn.sh:322-328, 586-591; lib/spawn-options.sh), and every `MODEL_PROFILE_*_ARGS` is a `--flag value` pair. The evidence is pasted in the validation file.
   - `herdr-agents --add-worker <worktree> [--kind] [--profile] [DIR]` works only from a main checkout, with `<worktree>` under `.claude/worktrees/`. It refuses an undefined profile before any change. It derives the identity without joining (spawn pre-joins), creates or validates the worktree, points delivery at it, and creates or reuses the workspace `<repo> worker <name>`. That workspace is created with `HERDR_AGENTS_LAYOUT=managed`, `AGMSG_RESOLVE_PROJECT=0`, and `AGMSG_CC_MONITOR_KEEP_ALIVE=1` for claude.
   - It then runs `spawn.sh <type> <name> --project <worktree> --team <team> --terminal-driver herdr --window` with `HERDR_WORKSPACE_ID` set, so upstream's `terminal_spawn` opens a tab there. `AGMSG_SPAWN_OPTIONS_FILE` is a generated YAML: `MODEL_PROFILE_<P>_CLAUDE_ARGS` for claude, and `--profile <p> --sandbox workspace-write` for codex.
   - A workspace that already has an agent is a no-op.
   - The actas boot starts a Monitor in `both` mode, so spawn's readiness wait is expected to succeed despite #367. That is upstream behaviour, not verified live here.
6. **`--remove-worker <worktree> [--force] [DIR]`.**
   - It refuses a dirty worktree unless `--force`.
   - It runs `despawn.sh <team> <orchestrator> <name>`, with `--force` passed through, and always forced for a codex seat, which never holds the actas lock. A graceful despawn that fails stops the teardown with a hint.
   - Then `delivery.sh set off <type> <worktree>`, `leave.sh` (tolerated, since despawn may already have dropped the registration) and `herdr workspace close`. The worktree is kept.
7. **README and SKILL "Parallel workers".** The two modes are the only sanctioned way to add or remove workers, with the ~3-worker ceiling and raw herdr topology commands still forbidden (T21 G7).
8. **Tests** (mutation baseline against the deliverable-A script: 8 of 8 fail):
   - add creates the workspace and spawns with the options YAML;
   - codex options;
   - reuse of a seated workspace;
   - invalid paths are rejected;
   - remove runs in order;
   - dirty refusal;
   - `--force` pass-through;
   - a graceful despawn failure stops the teardown.

### Independent review (subagent, separate context) and fixes (e226c27)

The verdict on 9d5cf7c was **incorrect**: 1 P1, 3 P2, 6 P3, all fixed in e226c27 with 9 new tests (7 of 9 fail on 9d5cf7c).

- **P1:** the heal path reused an empty pane in the main checkout, which recreated the defect. It now goes through `seat_pane_shell`.
- **P2:**
  - the host-global `worker_worktree` created or nested worktrees in unrelated or linked checkouts, or half-built workspaces. `worker_seat_applies` now decides first, and the identity is derived before creation;
  - codex remove needed `--force`, which doubled as the dirty override. Codex despawn is now always forced;
  - an unknown `--profile` silently used the CLI default. It is now refused.
- **P3:**
  - the Monitor claim is scoped, and the add-worker workspace env is added;
  - a stale README inbox.sh sentence is fixed;
  - a silent `cd` skip now refuses;
  - one name in several teams counts as one seat;
  - codex hooks print the trust notice;
  - test gaps are closed.

Crit evidence is in `.orchestration/validation/dot-herdr-agents-add-worker-T22-a01-crit.json` (all records resolved), with the receipt `…-review-receipt.md`.

### Not done / for acceptance

- **Live E2E is orchestrator-side per the task:**
  - after merge and `chezmoi apply`, `herdr-agents --restart-worker` on wJ;
  - a PING via agmsg-dispatch must arrive by the Stop hook without `inbox.sh`;
  - `identities.sh <worktree> claude-code` should show one seat;
  - `doctor.sh --project <worktree>`.
  - Deliverable B fresh and restore in a scratch repo.
  - Revision 3's deliverable 6 (live poke/peek) rides with it.
- `leave.sh … a006`, the CodeRabbit slot and `make require-crit-review` are the orchestrator's.
- **Files touched**, all within rev-4 allowed_files plus the ruling:
  - `home/dot_local/bin/common/executable_herdr-agents`
  - `home/dot_agents/agent-config.yaml`, `home/dot_agents/model-profiles.env`
  - `scripts/generate-agent-configs.py`, `scripts/validate-agent-assets.py`
  - `tests/unit/test_herdr_agents.py`, `tests/unit/test_generate_agent_configs.py`, `tests/unit/test_validate_agent_assets.py`
  - `README.md`, `home/dot_agents/skills/agmsg-orchestration/SKILL.md`, `home/dot_config/claude/rules/agmsg-orchestration.md`
  - the artifacts.
- **Effects:** none outside the repository. All tests used fake herdr and agmsg in temp HOMEs; no real pane or registration was touched.

### CompactionDB

`[memory:decision]` T34/T22 r4: the herdr-agents worker pane is seated in its own worktree (manifest `worker_worktree` → `HERDR_AGENTS_WORKER_WORKTREE`), its identity is registered there with `AGMSG_RESOLVE_PROJECT=0`, and delivery is set on that path, so task delivery reaches the worker as turn/Monitor events. Parallel workers are added and removed only through `herdr-agents --add-worker/--remove-worker` on upstream `spawn.sh`/`despawn.sh` (operator 2026-09-29), plus the ruling notes. Id `f568614e-a324-499c-85f9-88a134a57c90`; the command and output are in the validation file.

cost: n/a (the Claude Code runtime does not expose session token/cost figures to the worker)

## Revision 4b (AGMSG-ACCEPTANCE status=revise, 2026-09-29T03:56:27Z), reply as RESULT revision=5

- **Audit.** The headless Codex audit of e226c27 returned **incorrect**, with one P2 (confirmed from the upstream despawn semantics).
- **The defect.** `--remove-worker` forced every codex despawn. After a failed spawn, the identity exists but no placement record does. Upstream graceful despawn then returns `status=ok … note=no-live-lock`, but `despawn.sh --force` dies with "no placement record … nothing to force" (despawn.sh:118). Removal therefore aborted before delivery off, leave and workspace close, and a `--force` retry failed the same way.
- **Fix: `16d095f`.** `despawn_worker_seat` is now graceful-first:
  - a graceful success is done, including a member with no placement record;
  - `status=needs-force` (a record but no live actas lock, as for codex seats; despawn.sh:163-169) or an operator `--force` retries with `--force`;
  - anything else stops removal with a hint and runs no cleanup, since the pane may still be alive;
  - every completed despawn runs the full cleanup: `delivery.sh set off`, `leave.sh`, `herdr workspace close`.
- **Interpretation.** "Preserve the full cleanup sequence in every path" is read as every path in which the despawn completes. A despawn that cannot complete keeps the seat, and so its record and registration, so the retry authority survives, as upstream intends.
- **Tests** (5 new or rewritten):
  - a codex seat without a placement record cleans up without forcing;
  - needs-force, then force, then full cleanup;
  - `--force` after a failed graceful call (timeout);
  - `--force` skipped when the graceful call succeeds;
  - a forced retry that also fails stops without cleanup.

  Mutation baseline against e226c27: 4 of the 5 fail. The last passes on both and is kept as a regression guard. After the fix: herdr-agents 151 OK, unit 564 OK, validate ok, shellcheck, shfmt and the CI ShellCheck command clean.
- **Also fixed.** The file mode of `executable_herdr-agents` is restored to 100644. It had been flipped to 100755 by a baseline swap in 3eeaeee; found during the T35 review.
- **PR.** #206, head `16d095f182e5f8085965ce61f1d8058933e95f75`. CI: the first run failed in public-bootstrap on all three OSes. The ubuntu-client log shows `curl: (22) The requested URL returned error: 500`, an external download during bootstrap, before any repo code ran. `gh run rerun 36523890490 --failed` is green; both runs are in the validation file.

## Revision 6: rebase onto origin/main 2e0c6f4 (T35 #207 merged), per ruling PING 05:23Z

- **Rebase.** I rebased onto `2e0c6f4` and published with `--force-with-lease` on my own branch (lease `16d095f`). The new head is `9da17b9`; the commit mapping is 3eeaeee→019ee6d, 9d5cf7c→8c16ef6, e226c27→fd0b050, 16d095f→02768d9, plus `9da17b9`.
- **One textual conflict**, in `home/dot_agents/skills/agmsg-orchestration/SKILL.md`: both PRs added the first "Parallel workers" bullet. Both are kept, T34's then T35's, as ruled. The script, tests and README auto-merged.
- **One semantic interaction, found by the full unit suite and fixed in `9da17b9`.** T35's `load_seat_labels` ran before T34's quiet early exit for the worktree-seated worker's own `--attach`. So every worker SessionStart did two to three read-only `identities.sh` lookups before exiting, which `test_attach_from_the_worker_worktree_exits_quietly` caught. The load now runs right after that exit, and still before `worker_seat_applies`, the T14 guard and every pair mode that reads the labels.
- **Merged-code check.** Each of the ten key functions from both PRs is defined exactly once: `load_seat_labels`, `normalize_seat_labels`, `managed_pane_list`, `rename_pane_unless_seat_named`, `worker_seat_applies`, `prepare_worker_seat`, `seat_pane_shell`, `despawn_worker_seat`, `ensure_worker_identity`, `write_spawn_options`. The only remaining raw `herdr pane rename` calls are inside the guard helper and on the audit pane. The file mode matches main (100644).
- **Totals:** unit 577 OK (1 skipped), validate ok, shellcheck, shfmt and the CI ShellCheck command clean.
- **Audit.** The 16d095f audit stays as evidence for the despawn fix; the orchestrator audits the rebased head before merge.
- **PR.** #206, head `9da17b9d263638937cb25bdc26893a13c06a4d60`, MERGEABLE. CI is green: every check passes and nix is skipped.
