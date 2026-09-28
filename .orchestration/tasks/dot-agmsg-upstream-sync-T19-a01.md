---
task_id: dot-agmsg-upstream-sync-T19-a01
revision: 3
supersedes: 1
created_at: 2026-09-26T01:55:00Z
---
# AGMSG-TASK dot-agmsg-upstream-sync-T19-a01 (revision 2): adopt upstream agmsg 1.5.0 through the documented installer, retire the vendored snapshot and agmsg-dispatch (plan v2 Stage 2a)

Revision 2 replaces revision 1 entirely. Revision 1 assumed an npm tarball with scripts and sha512 integrity; upstream primary sources show otherwise (see Facts). Repo: `/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-b`, branch `feat/agmsg-upstream-sync` from origin/main. You are `claude-standard-dot-a004`. Read-only inventory from revision 1 stays valid; discard any installer design based on tarball/rsync.

## Facts (upstream v1.4.2/v1.5.0, verified from tag sources; local copies in the orchestrator scratchpad are NOT for you — fetch upstream yourself)
- Latest: npm `agmsg` dist-tags.latest = **1.5.0** (2026-09-25); `VERSION` on main = 1.5.0.
- Install (README "Install"): `npx agmsg@<ver>` — `bin/agmsg.js` pins `AGMSG_REF=v<ver>` and runs `setup.sh`, which `git clone --depth 1 --branch v<ver>` (tarball fallback) and runs `install.sh`. The npm package ships **no scripts** (`files: bin/, README, CHANGELOG, LICENSE`). Update: `git pull && ./install.sh --update` ("DB and team configs are preserved. Only scripts and assets are updated."); `--update` overwrites/prunes `scripts/` (drivers excluded #1249), backs up changed files to `.trash/`. No `agmsg update` subcommand. No checksum verification of the cloned tree is documented; npm publishes with SLSA provenance. Vendoring the skill is **not documented**.
- Layout: `~/.agents/skills/<cmd>/{SKILL.md, agents/, scripts/, plugins/, db/messages.db, teams/, run/, VERSION}`; `SKILL.md` is rendered per type at install (placeholders `__SKILL_NAME__` etc.); Claude slash command at `~/.claude/commands/<cmd>.md`; Codex `~/.codex/config.toml` writable_roots (`db`, `teams`, `run`, `ext-tools`) added by `install.sh`.
- Delivery: `delivery.sh set <monitor|turn|both|off> <type> <project>`; Claude Code monitor = SessionStart directive → Monitor(`watch.sh <sid> <project> <type> [role]`, `timeout_ms: 1800000`); re-arm is done by the seat's own model on expiry; `AGMSG_CC_MONITOR_KEEP_ALIVE=1` makes re-arm unconditional (default since 1.4.0: re-arm only when the expired watch delivered events). "Monitor priming": a fresh session reacts to its first inbound only after one turn. Turn mode: Stop hook `check-inbox.sh`, 60 s cooldown (`delivery.turn.check_interval`); serves only the first registered seat per (project,type) (#967 open). Codex monitor: `delivery.sh set monitor codex <project>` + `codex()` shim (`codex-shim-install.sh install`), `codex_hooks = true`; bridge via app-server (`docs/codex-monitor-beta.md`; known #149/#151/#1236).
- Wake: `poke.sh <team> <name> --body-file <path> [--retries N --retry-delay S --backoff exponential]`; herdr driver uses `herdr agent prompt <pane>`; exit 10/12/13/14/15 semantics (13 = never fall back to send silently). Placement record `run/spawn.<team>__<name>` written by `spawn.sh` or by the seat itself via `fix.sh`; **no leader-side registration exists by design** (#1152).
- Seating: `spawn.sh <type> <name> --project <worktree> [--terminal-driver herdr] [--boot-prompt …]` blocks until `status=ready` (Claude) / `launched-unconfirmed` (Codex); despawn graceful/`--force`.
- Health (read-only): `team.sh <team> --json`, `peek.sh <team>`, `doctor.sh --project <p>` (exit 1 on warnings), `watch-once.sh <project> <type> --team <t> --name <n> --timeout 0` (unread gate), `delivery.sh status <type> <project> [<sid>]`.
- Identity: `actas <name>` exclusive lock `run/actas.<team>__<name>.session`; Codex actas is send-side only; names `<base>-<role><n>`, never bare tool names.
- Project resolution (docs/design.md): marker → ancestor → `git rev-parse --git-common-dir` → pwd; `.claude/worktrees/<name>` sub-sessions are skipped by session-start (#367). Behaviour when main checkout AND a sibling/nested worktree are both registered is **not documented** — must be tested.
- herdr caveats (open): #1317 (herdr 0.9.1 stderr → peek rc 11), #1307 (driver ignores `{cmd}` placement), `ops.sh` header marks `herdr agent prompt`/`agent rename` argv "ASSERTED, NOT measured".

## Deliverables
1. **Manifest**: `assets.agmsg` → `source: agmsg-installer`, `upstream: https://github.com/fujibee/agmsg`, `pin: 1.5.0`, `ref: v1.5.0`, `ref_commit: <sha of tag v1.5.0>`, `bootstrap_integrity: <npm dist.integrity of agmsg@1.5.0>`, `install_path: ~/.agents/skills/agmsg`, `installer: scripts/update-agent-assets.sh#update_agmsg`. Validator: this source requires `ref`, `ref_commit`, `bootstrap_integrity`.
2. **Installer step `update_agmsg`** (the only sanctioned path): if `~/.agents/skills/agmsg/VERSION` ≠ pin → `git clone --depth 1 --branch v<pin> https://github.com/fujibee/agmsg <tmp>`; verify `git -C <tmp> rev-parse HEAD == ref_commit` (fail closed); run `<tmp>/install.sh --update` (preserves db/teams/run); record `manifest_record` with `VERSION`. First install on a machine without the skill: `install.sh` (non-update) with the same verification. Never write `scripts/` by hand. Document that `npx agmsg@<pin>` is equivalent but unverifiable, hence the clone+commit check.
3. **Retire the vendored copy**: delete `home/dot_agents/skills/agmsg/**` from chezmoi; ensure apply neither removes nor overwrites the installer-owned dir (check `.chezmoiignore`/`remove_` semantics); July local fixes → upstream issue/PR if not already upstream (cite).
4. **Retire `agmsg-dispatch`** (+ its test): orchestrator sends with `send.sh --body-file` (verify it exists in 1.5.0; if not, `send.sh` with a positional body only for shell-safe text) and wakes an idle seat with `poke.sh --body-file`; document exit-code handling (13 never falls back to send). Update agmsg-orchestration SKILL steps 4/6, `agmsg-orchestration.md`, README.
5. **Delivery defaults**: Claude seats `both`; resident Claude worker panes get `AGMSG_CC_MONITOR_KEEP_ALIVE=1` in their pane env (herdr-agents passes it; document in README); Codex seats `monitor` via shim + `codex_hooks = true` (installer ensures writable_roots). herdr-agents `--bootstrap-agmsg` calls `delivery.sh` accordingly and uses `doctor.sh --project` for identity/watcher health instead of the heuristic (keep the T14 guard until Stage 2b).
6. **Local verification of undocumented behaviour** (required, verbatim): (a) project resolution with main checkout + `.claude/worktrees/<x>` both registered (does `whoami.sh`/`session-start.sh` in the worktree resolve to the worktree registration?); (b) `poke.sh` through the herdr driver against a scratch herdr pane (does `herdr agent prompt` work with 0.9.1; exit codes); (c) `peek.sh` rc on a closed pane (#1317); (d) `team.sh --json` output for the scratch team. Report each as verified/failed with output; failures become upstream issues (URLs in report) and repo-side mitigations only where documented (e.g., the poke retry flags).
7. **Doctor**: `check-tools.sh` prints installed agmsg `VERSION` vs manifest pin.
8. **Docs/tests**: README agmsg section rewritten from these facts; unit tests for the installer step (fake git/clone, commit mismatch → fail, VERSION match → skip), validator rules, SKILL/rules parity; pr-feedback sweep + CodeRabbit full review on the final head (slot assigned by the orchestrator).

## allowed_files
`home/dot_agents/agent-config.yaml`, `scripts/update-agent-assets.sh`, `scripts/validate-agent-assets.py`, `scripts/generate-agent-configs.py` (if rendering is needed), `scripts/check-tools.sh`, deletions of `home/dot_agents/skills/agmsg/**`, `home/dot_local/bin/common/executable_agmsg-dispatch`, `tests/unit/test_agmsg_dispatch.py`; new/updated unit tests; `home/dot_agents/skills/agmsg-orchestration/SKILL.md`, `home/dot_config/claude/rules/agmsg-orchestration.md` (+ Codex mirror), `home/dot_local/bin/common/executable_herdr-agents` (bootstrap + KEEP_ALIVE env only), `README.md`, `AGENTS.md`, `.chezmoiignore`, artefacts.

## forbidden_actions
`make update`/`make upgrade`/`chezmoi apply` on the real HOME; touching `~/.agents/skills/agmsg/{teams,db,run,agents}`; running `install.sh` against the real HOME (use a scratch HOME for E2E); merging; local bats; force-push; keeping any local fork of upstream scripts; vendoring.

## Artefacts / Done signal
Standard five + pr-feedback JSON + crit evidence JSON. `[memory:decision]`: "agmsg is installed by the upstream installer at a pinned tag verified by commit sha, recorded in the asset manifest; the vendored snapshot and agmsg-dispatch are retired; wake uses upstream poke, health uses team/doctor/peek". RESULT via `send.sh dotfiles claude-standard-dot-a004 claude-remediation-dot "<message>"`. max_turns=60.

## Revision history
- r1 (09-25): npm tarball + sha512 + rsync design — withdrawn (npm package has no scripts; no upstream checksum; vendoring undocumented).
- r2 (09-26 01:55Z): grounded in upstream v1.4.2/v1.5.0 sources (README, docs/design.md, docs/actas.md, docs/codex-monitor-beta.md, CHANGELOG, scripts headers, bin/agmsg.js, setup.sh, install.sh).

---

# Revision 3 (2026-09-28) — round 2: rebase onto current main, close round-1 findings, reconcile with the post-T31 regime

Revision 3 keeps revision 2's Facts, Deliverables 1–8, forbidden_actions and artefacts, and adds the following. Branch `feat/agmsg-upstream-sync` (PR #184, head 579bafe) is DIRTY against `origin/main`; the round-1 acceptance record (`.orchestration/acceptance/dot-agmsg-upstream-sync-T19-a01.md`) lists findings 1–9 and 11; supplement 2 is withdrawn.

## Rebase first

- `git fetch origin` and rebase `feat/agmsg-upstream-sync` onto `origin/main`. Files changed on both sides since the merge base: `README.md`, `home/dot_agents/agent-config.yaml`, `home/dot_agents/skills/agmsg-orchestration/SKILL.md`, `home/dot_local/bin/common/executable_herdr-agents`, `scripts/check-tools.sh`, `scripts/update-agent-assets.sh`, `scripts/validate-agent-assets.py`, `tests/unit/test_herdr_agents.py`, `tests/unit/test_runtime_health.py`, `tests/unit/test_validate_agent_assets.py`. Main gained, since the base: `herdr-agents --audit` (T32/T32b/T33b/T33e: exec channel, verdict gate, quoting), `--restart-worker` name-wait (T27), T33a rule text (inbox discipline, fail-closed, batch pre-screen, crit alignment), T33f/T33g core build in `update-agent-assets.sh`, T33d/T33h permgate tests. Keep ALL of it; your changes layer on top. If a clean rebase is impractical, re-apply your three commits by cherry-pick onto a fresh branch from `origin/main` with the same name and publish with `git push --force-with-lease` on your own branch (authorized, as in T31).
- The ten overlapping files must end up containing both sides; paste `git diff --stat origin/main` and a per-file note on how each conflict was resolved.

## Findings to close (each needs its own evidence in the validation file)

1. Migration path (MAJOR): handle `installed=none` (no VERSION, no `.agmsg` marker) explicitly — take a state snapshot of `teams/db/run/agents` BEFORE any installer run, never call `install.sh --update` when not installed, run the plain installer with stderr captured, and compare the snapshot AFTER (byte-identical `teams/`, `db/messages.db` sha, `run/` untouched); print a truthful message on failure. Unit test with a fake `install.sh` that mutates state → the step must fail and report it.
2. Manifest spec (MAJOR): `assets.agmsg` → `source: agmsg-installer`, `pin: 1.5.0`, `ref: v1.5.0`, `ref_commit: <sha>`, `bootstrap_integrity: <value or documented n/a>`; validator rule requiring `ref`, `ref_commit`, `bootstrap_integrity` for this source; restore or replace the seven deleted validator tests with equivalents.
3. Dangling chezmoi symlinks (MAJOR): `home/.chezmoiremove` entries (or `remove_` targets) for `~/.claude/skills/agmsg/**` and every other target the PR deletes; test that `chezmoi apply` in a scratch HOME removes the stale symlink tree; document in README.
4. Codex seats (MAJOR): resolve the `delivery.sh set turn codex` vs "upstream default" contradiction in SKILL.md and herdr-agents; reconcile `writable_roots` with upstream `configure_codex_sandbox` (`ext-tools/`) in manifest + validator so `make update` produces no drift.
5. Deliverable 6 (MAJOR): (a) redo verbatim per finding 11 (ii) below; (b)(c) stay orchestrator-side at acceptance (shared live herdr server) — state that in the report; (d) keep; file no upstream issues yourself — list the observed gaps with reproduction so the operator can file them.
6. `install_pinned_agmsg` (MINOR): check `tar` and `sha256sum`/`shasum` explicitly; do not rely on `set -e` on the left of `||`; empty snapshots must fail, not compare equal.
7. SKILL.md wording (MINOR): remove the pane-status gate; make poke-vs-send selection coherent; document exit 13 and the `--update` watcher stop (upstream #133) in README.
8. Contract (MINOR): RESULT line carries all five artefact paths; validation pastes verbatim unittest/validator/shellcheck output; the CompactionDB `memory add` command and its id are shown.
9. `allowed_files` (MINOR): the four omitted paths are now listed below; report every file you touch.
11. Identity resolution (MAJOR, design-level): (i) every worker join performed by herdr-agents or documented for operators registers the identity at the WORKTREE path with `AGMSG_RESOLVE_PROJECT=0` (or `spawn.sh --project`), and `delivery.sh set` for a worker targets the worktree path so `session-start.sh` bakes it into the marker; (ii) redo 6(a) verbatim in a scratch HOME: `whoami.sh` and `session-start.sh` inside a nested worktree registration, once with the marker present and once without, plus `join.sh` with and without `AGMSG_RESOLVE_PROJECT=0`; (iii) document the rule in README and the agmsg-orchestration skill citing upstream #92 and docs/design.md; correct the doctor comment that describes ancestor matching. This item is the foundation of the later seating task (T34): do not redesign seating here, only registration and delivery semantics.

## Reconcile deliverable 4 with the current regime

Retiring `agmsg-dispatch` changes how the orchestrator wakes workers. In the same PR: replace every `agmsg-dispatch` reference in `home/dot_config/claude/rules/agmsg-orchestration.md`, the SKILL (Playbook step 6 and the Pitfalls), README and `home/dot_config/codex/AGENTS.md` (if present) with the upstream `poke.sh <team> <name> --body-file <path>` flow and its exit-code semantics, and keep the T33a "inbox.sh at each milestone" interim rule (it is orthogonal). Keep the `agmsg-dispatch` executable and its test until the orchestrator confirms the poke path live at acceptance — mark it deprecated in its shdoc header instead of deleting it in this round; deletion is a one-line follow-up after the live check.

## Acceptance plan (orchestrator, for your information)

Merge is followed by `make update` on this host at a session boundary because the installer replaces the scripts the orchestrator's own watcher runs; the pre-update state snapshot from finding 1 is the rollback. Live E2E after that: `whoami.sh`, `history.sh`, `identities.sh` per worktree, one `poke.sh` round trip, one `delivery.sh status`.

## allowed_files (revision 3 = revision 2 list plus)

`home/dot_claude/commands/symlink_agmsg.md.tmpl`, `home/dot_claude/skills/agmsg/**` (deletions), `tests/install/common/check_tools.bats`, `tests/unit/test_agmsg_send.py`, `home/.chezmoiremove`, `home/dot_config/claude/rules/agmsg-orchestration.md`, `home/dot_config/codex/AGENTS.md` (agmsg-dispatch references only), `home/dot_local/bin/common/executable_agmsg-dispatch` (shdoc deprecation note only), `tests/unit/test_agmsg_dispatch.py` (only if the deprecation note needs a test change), `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dot-agmsg-upstream-sync-T19-a01.md` (main checkout; append a "Round 2" section rather than rewriting round 1).

## Completion (revision 3)

PR #184 updated (same branch), CI green, all five artefacts appended with round-2 sections, CompactionDB decision added from the main checkout with the command and id pasted, `inbox.sh dotfiles claude-standard-dot-a005` at each milestone, `AGMSG-RESULT v1 revision=3` with all artefact paths and a `cost:` line.

## Revision history (continued)
- r3 (09-28): round 2 — rebase onto current main (ten overlapping files), close findings 1–9 and 11, reconcile deliverable 4 with the T33a rules and the live regime (deprecate, do not delete, agmsg-dispatch), acceptance plan for the live installer switch.
