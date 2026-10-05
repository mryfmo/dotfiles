# AGMSG-TASK dotfiles-T87-live-e2e-matrix-a01

Drafted 2026-10-05 by the orchestrator seat from the approved correction plan (Phase 7, dotfiles-T87). Depends on T70, T82, T83, T84, T85 and T86 on `main`, deployed on each host with `make update`. This task produces evidence files only (no product change); its Linux legs run from the orchestrator's host under the acceptance exemption with the operator present for the legs that need another account or a Mac; the macOS legs are the operator's.

## Objective

Principles 4 and 5: both hosts, both runtimes, both directions, with live evidence.

Per host (`uname -s` recorded), in this order, each result pasted verbatim into the host's evidence file:

1. **Lifecycle:** `sudo -K; script -q /dev/null make update` exits 0 with no "password" line (Linux: the apparmor profile step must have been done once with `sudo -v`); `make doctor` exits 0 with `Doctor summary: tools=passed; runtime=passed`.
2. **CompactionDB Codex legs:** after the one-time `/hooks` trust (README operator phase), a Codex session in the repository runs `/compact` and exits; `sqlite3 .claude/contextdb/state/context.db "select event_type,session_id,ingested_from from events where ingested_from='codex' order by id desc limit 3"` shows `pre_compact`, `post_compact` and `session_end` rows with a non-empty session id and no new `unknown` rows; `uv run .claude/hooks/contextdb_cli.py prune` exits 0 and `du -m .claude/contextdb/state/context.db` ≤ 512.
3. **claude→claude and claude→codex:** with the pair seated, `leave.sh` the current worker identity, `HERDR_AGENTS_WORKER_KIND=<claude|codex> herdr-agents --restart-worker` (env override for the leg; the manifest is not edited), record the `linkage=` line and the PONG, dispatch a one-command task (`make render-check` → RESULT), record the RESULT, restore the manifest kind with another `--restart-worker`. `make check-regime-boundary` exits 0 after each leg (the seat holds exactly one identity: exchange only through `leave.sh` → `join.sh`).
4. **codex→claude and codex→codex:** seat the worker as in 3, then `HERDR_AGENTS_ORCHESTRATOR_KIND=codex codex-orchestrate --max-turns 3 --team dotfiles "<the same one-command task>"`; record the transcript path, the exchanged and restored identities (`identities.sh <repo> claude-code` before and after), and whether `CODEX_ORCHESTRATE_DELIVERY=hook` works (the T86 VERIFY: does the trusted project Stop hook consume the delivery under `codex exec`?). Restore the Claude orchestrator identity and its `both` delivery.
5. **GitHub roles (after the operator provisions the second account and applies the two rulesets per README):** the scratch-PR table from the T90b README section, every response recorded; the launcher's worker panes answer `gh api user --jq .login` with the worker login.
6. **macOS installers:** `bats tests/install/macos` and `make doctor` on the Mac, pasted into `e2e-macos-installers.md`.

Evidence files (written by the orchestrator or operator, committed in the next boundary PR): `.orchestration/validation/e2e-{claude-claude,claude-codex,codex-claude,codex-codex}-{macos,linux}.md`, `e2e-macos-installers.md`, `e2e-lifecycle-{macos,linux}.md`, `e2e-github-roles.md`. Each names `uname -s`, the deployed `main` sha, the doctor summary line, `pong=yes` or the RESULT, the messages.db PING/PONG rows (`read_at` non-null), and `regime-boundary:` absence.

Forbidden: product changes (this task is evidence only; defects found become new tasks); editing the manifest for a leg (env overrides only); any merge.

[memory:decision] dotfiles-T87 (operator 2026-10-03): the live matrix (claude→claude, claude→codex, codex→claude, codex→codex on macOS and Linux, the unattended lifecycle, the Codex CompactionDB legs, the GitHub role rulesets and the macOS installers) is recorded as evidence files under `.orchestration/validation/`; a failed leg opens a task, never a patch inside this one.

## Who runs what

- Linux legs 1–4: the orchestrator seat, under the acceptance exemption (evidence sync; no repository mutation beyond `.orchestration/validation/`), with `herdr-agents` and `codex-orchestrate` as deployed by `make update`.
- Leg 5 and every macOS leg: the operator (second GitHub account, ruleset PUTs, the Mac).

### Sequencing note (orchestrator, 2026-10-05 09:50Z)

Leg 2 (Codex CompactionDB) runs only after T81b (vendor 2.0.0+dotfiles.9) is merged and deployed on the host; the `/hooks` trust step is performed at that point, never before.

## Orchestrator note (2026-10-05 10:15Z) — Linux legs

- `e2e-claude-claude-linux.md` and `e2e-claude-codex-linux.md`: written from the live regime (a005 in worker-c, a007 in worker-e), with unattended `make update` (0 prompts), `Doctor summary: tools=passed; runtime=passed`, bus rows with `read_at`, and the session-end `make check-regime-boundary` line.
- `e2e-codex-claude-linux.md` and `e2e-codex-codex-linux.md`: not runnable from a Claude-orchestrated session. `codex-orchestrate` reads `HERDR_AGENTS_ORCHESTRATOR_KIND` only from the rendered profile env (the task's environment override is ignored by design), and switching the manifest to `codex` makes `herdr-agents` refuse the Claude-pair modes, so the Claude orchestrator must be stopped first (README). Each file holds the operator procedure (manifest switch task, `make update`, stop the Claude seat, run `codex-orchestrate --max-turns 3`, paste evidence, revert). Leg 2 (`/compact` rows) still waits on the operator trusting the Codex hooks in `/hooks` (T81b deployed 2.0.0+dotfiles.9).
