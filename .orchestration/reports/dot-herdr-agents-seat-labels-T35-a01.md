# Report: dot-herdr-agents-seat-labels-T35-a01 (revision 1)

- **Worker and worktree:** worker `claude-standard-dot-a005` in `.claude/worktrees/worker-c`.
- **Branch:** `fix/herdr-agents-seat-labels` from `origin/main` b790ee0. T34 (#206) is not merged, so this branch is independent of its worktree-seat code; the only link is that it reads the same `HERDR_AGENTS_WORKER_WORKTREE` env value if present.
- **task_rev:** sha256 `2e8aa0d2…`, verified against `origin/main`.
- **PR:** https://github.com/mryfmo/dotfiles/pull/207, head `903c9fad9901198acf585465c9b684a820c00994`. Commits: `549b257` (fix) and `903c9fa` (review fixes). CI is green on both, with every check passing and nix skipped; the verbatim output is in the validation file.

## Diagnosis (read-only; verbatim evidence in the validation file)

- **Upstream renames panes and agents.** agmsg 1.5.0 self-naming (`lib/self-name.sh`; a seat names its pane when it acts, via `send.sh:77`/`inbox.sh:23` `agmsg_self_name_on_action`) performs two renames in the herdr driver (`drivers/terminals/herdr/ops.sh` ~1240-1260, 1369, 1382):
  - `herdr pane rename <id> <team>:<agent>`, the visible label;
  - `herdr agent rename <id> <key>`, where the herdr agent name becomes the hash key `a<sha256[0:24]>`.
- **The live pair shows both.** Live `wJ` panes are labeled `dotfiles:claude-remediation-dot` and `dotfiles:claude-standard-dot-a005`, and its agents are named `a449a05f…` and `a46054f8…`. So both the legacy pane labels and the `<kind>-worker-<ws>` agent names that herdr-agents used are gone.
- **Workspace label.** No agmsg 1.5.0 script renames a workspace (grep of the installed scripts: 0 matches). A herdr workspace exposes only `label`, not env (`herdr workspace list` keys). The live `wJ` label is `dotfiles`. herdr-agents recognized that workspace only through its `claude-orchestrator` pane label, because attach mode keeps a workspace's own label, so self-naming made it invisible. I could not determine definitively whether `wJ` ever carried `dotfiles agents`. No source I could read renames it, and the fix does not depend on the label.
- **Self-naming stays on.** It was not disabled: poke, despawn and team rely on it.

## Change (`home/dot_local/bin/common/executable_herdr-agents`)

- **Seat labels.** `load_seat_labels` reads the pair's seats at the repository's main checkout, resolved from the git common dir so a linked worktree resolves too:
  - the orchestrator is the non-worker (no `-aNNN`) `claude-code` identity there;
  - the worker is the pair's own worker-type seat: the identity at `HERDR_AGENTS_WORKER_WORKTREE` (from model-profiles.env, T34), or for the legacy seat an `-aNNN` identity at the main checkout;
  - other team members are never the worker;
  - `$HOME` is skipped.
- **Normalization.** Every pair pane list, in workspace detection and in the attach, restart and full-mode paths, goes through `normalize_seat_labels`, which maps `<team>:<orchestrator>` to `claude-orchestrator` and the worker seat to `<kind>-worker`. The existing detection, ambiguity refusal and repair logic is unchanged, and the legacy labels keep working. `HERDR_AGENTS_LAYOUT=managed` cannot be used, because herdr exposes no workspace or pane env.
- **No relabeling.** `rename_pane_unless_seat_named` replaces every pair-label rename (orchestrator start, worker start, attach, and restart's legacy repair), so a `<team>:<name>` pane is never relabeled.
- **Attach.** Attach falls back to the worker's seat label, since its herdr agent name is gone. The worker's own attach exits when its pane is the worker by label.
- **Audit.** The tab semantics are unchanged; only the workspace lookup, which now uses the normalized labels, changed.
- **Docs.** A README herdr paragraph on recognition under self-naming, and one SKILL sentence in "Parallel workers".

## Tests

- **549b257:** 6 tests on a workspace labeled `dotfiles` with self-named panes and no agent-get result:
  - `--audit` finds it;
  - attach from the orchestrator or worker pane does no rename, swap or split;
  - `--restart-worker` finds the worker by seat label;
  - a healthy full mode changes nothing;
  - two workspaces still refuse.

  Baseline against unmodified `origin/main`: 6 of 6 fail.
- **903c9fa** (after the independent review): 4 more tests. 3 of them fail on 549b257:
  - another team member's pane is not a second worker;
  - an orchestrator attach completes, reaching bootstrap;
  - the worker label comes from the worker-worktree registration.

  The mixed legacy/seat labels test passes on both and is kept as a regression guard.
- **Totals:** herdr-agents tests 136 OK; `make unit-test` 543 OK; validate ok; shellcheck, shfmt and the CI ShellCheck command are clean.

## Independent review (subagent, separate context)

The verdict on 549b257 was **incorrect**: 2 P2 and 5 P3, all resolved in 903c9fa. The crit evidence is `.orchestration/validation/dot-herdr-agents-seat-labels-T35-a01-crit.json`, with the receipt `…-review-receipt.md`.

- **P2:** every team member was mapped to the worker, so another member's pane caused a duplicate worker on heal and a refusal on restart.
- **P2:** the orchestrator's attach refused because it looked the worker up by the renamed agent name.
- **P3:**
  - a worktree seat's labels were read at the worktree;
  - the member type was ignored;
  - team.sh cost on every attach;
  - a file-mode flip;
  - test gaps.

The same file-mode flip (100644 to 100755) exists on the T34 branch (#206); I will fix it in the T22 revision.

## Notes for acceptance

- **Merge order with T34.** On this branch alone, the live worker `a005` is recognized as the pair's worker only once `HERDR_AGENTS_WORKER_WORKTREE` is rendered, which comes from T34's manifest field. Otherwise the legacy `-aNNN`-at-main rule applies, and that currently names `a006`, not `a005`. Merging T34 and T35 together, then `chezmoi apply`, covers the live pair.
- **Live E2E** is orchestrator-side: `--audit` and `--restart-worker` on the relabeled pair.
- **Files touched:**
  - `home/dot_local/bin/common/executable_herdr-agents`
  - `tests/unit/test_herdr_agents.py`
  - `README.md`
  - `home/dot_agents/skills/agmsg-orchestration/SKILL.md`
  - the artifacts.
- **Effects:** none. Only read-only herdr list commands ran against the live server.

## CompactionDB

`[memory:decision]` T35 (task text + diagnosis note). Id `ad0dbc1a-d2f7-4b0e-9649-df4dc8b8a8a3`; the command and output are in the validation file.

cost: n/a (the Claude Code runtime does not expose session token/cost figures to the worker)

## Revision 2 (AGMSG-ACCEPTANCE status=revise, 2026-09-29T04:54:25Z)

The headless Codex audit of 903c9fa returned **incorrect**, with two P2 findings that the auditor reproduced. Fix: `72a0a14`.

1. **A solo worker seat was not recognized.** Worker selection filtered on the `-aNNN` suffix, so a solo worker identity such as `codex-standard-dot` was not the worker: restart could not find it, and heal started a duplicate. The worker is now:
   - any worker-type seat at the worker worktree; or
   - at the main checkout, any worker-type identity that is not the orchestrator, solo or `-aNNN` alike, compared by `<team>:<name>` against the orchestrator labels.
2. **Explicit worker env was clobbered.** `load_seat_labels` sourced `~/.agents/model-profiles.env` in the caller's scope. That overwrote an explicit `HERDR_AGENTS_WORKER_KIND` or `HERDR_AGENTS_WORKER_PROFILE` (codex became claude, express became standard), so bootstrap skipped the Codex hooks while the resolved kind still launched codex. The file is now read in a subshell, the same way `write_spawn_options` reads it; `resolve_worker_kind` uses function-local variables for the same purpose.
3. **Tests.** Three new tests; all 3 fail on 903c9fa:
   - a solo codex worker is found by `--restart-worker`;
   - full mode does not duplicate a solo codex worker;
   - an explicit codex/express env survives seat-label loading, with the Codex hooks set.

   After the fix: herdr-agents 139 OK, unit 546 OK, validate ok, shellcheck, shfmt and the CI ShellCheck command clean. The file mode stays 100644.
4. **PR.** #207, head `72a0a14d7459c53ccaff72b27d0c1d6e88ceb7d4`. CI is green (every check passes, nix skipped); the verbatim output is in the validation file.
