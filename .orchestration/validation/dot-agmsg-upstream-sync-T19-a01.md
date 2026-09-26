# Validation: dot-agmsg-upstream-sync-T19-a01

## Task integrity

`task_rev=e7515aaaa75491fc` from the AGMSG-TASK ping matched the sha256 of the ORIGINAL
task file exactly (`e7515aaaa75491fc97d20d13165ed9e8db357b1e79e910b416d3f5d5450eae34`,
verified before starting). The task was later revised in place (revision 2, commit
`3bee1cf`, human-authored) — see the report file for how that was handled.

## Pin verification (v1.5.0) — independently re-derived, not trusted from the task or any subagent

```
$ gh api repos/fujibee/agmsg/git/refs/tags/v1.5.0 --jq .object.sha
c487be269c1973aeb01ca831806eb3f65ff3366d
$ curl -fsSL https://github.com/fujibee/agmsg/archive/c487be269c1973aeb01ca831806eb3f65ff3366d.tar.gz -o agmsg-150.tar.gz
$ sha256sum agmsg-150.tar.gz
9201cb5ff23ddd9ddaa19ff821dce0d0f2d58c6c292aade252a8d824b3dfc059  agmsg-150.tar.gz
$ tar xzf agmsg-150.tar.gz agmsg-c487be269c1973aeb01ca831806eb3f65ff3366d/VERSION -O
1.5.0
$ tar tzf agmsg-150.tar.gz | grep -c '/scripts/send.sh$\|/install.sh$'
2
$ npm view agmsg@1.5.0 dist.integrity
sha512-n6057L93AE+tnItTkBnClv3QvgsOlI6AO1SwodvKFJvqqTJqITHg/2O6jjHZZfh0nKbq49VKQv6F3t2d/62gyg==
```

All four values (commit, sha256, version, bootstrap_integrity) match exactly what's
committed in `home/dot_agents/agent-config.yaml` and rendered into
`scripts/update-agent-assets.sh`.

(The earlier v1.4.2 pin, from before the task's revision, was verified the identical way:
commit `e94ca9e0f4c40ebf3115dee8eb639f303c7f7a3f` via `gh api`, sha256
`a882ebc76dd140514c4996784ecdd90cff983d813421899682c0a533faa2a7f4` via direct
`curl`+`sha256sum` — both confirmed exactly matching a Plan agent's independently
reported values before I trusted them for a security-relevant pin.)

## Upstream documentation verification

```
$ curl -fsSL https://raw.githubusercontent.com/fujibee/agmsg/v1.5.0/README.md | grep -n "default on Claude Code"
63: ... pick a delivery mode (default on Claude Code and Codex: `monitor` ...
$ curl -fsSL https://raw.githubusercontent.com/fujibee/agmsg/v1.5.0/scripts/session-start.sh | grep -n KEEP_ALIVE
443: AGMSG_CC_MONITOR_KEEP_ALIVE, default OFF: timeout_ms: 1800000 always stays
456: if [ -n "${AGMSG_CC_MONITOR_KEEP_ALIVE:-}" ]; then
$ curl -fsSL https://raw.githubusercontent.com/fujibee/agmsg/v1.5.0/scripts/send.sh | head -8
...
#   send.sh <team> <from> <to> --body-file <path> [--force]     # body read from a file
# --body-file matches poke.sh, for the same reason (#507) AND to close #1101 ...
```

Confirms: upstream's own documented default really is `monitor` (so this repo's `both`
choice is a deliberate policy, not a correction to make); `AGMSG_CC_MONITOR_KEEP_ALIVE` is
real, with the documented unconditional-rearm semantics; `send.sh --body-file` exists in
v1.5.0, motivated by #507 (the shell-injection hazard) and closing #1101 (send.sh
previously took the literal string `--body-file` as a message body).

## Local checks

- `uv run --with pyyaml scripts/generate-agent-configs.py --check` → up to date.
- `uv run --with pyyaml scripts/validate-agent-assets.py` → `agent asset validation ok`.
- `uv run python -m unittest discover -s tests/unit -v` → **409 tests, OK (skipped=1)**.
  Test-file diff vs origin/main: `test_agmsg_dispatch.py` deleted (-11 tests, the retired
  dispatch script's own suite), `test_agmsg_send.py` deleted (tested the vendored
  `send.sh` copy directly — no longer a local fork to test), `test_validate_agent_assets.py`
  -74 lines (the two retired agmsg-specific validators' tests), `test_asset_manifest.py`
  +1 line (`update_agmsg` added to the single-manifest-record-call-site invariant list),
  `test_herdr_agents.py` +95/-? (bootstrap_agmsg's doctor.sh/both-mode/KEEP_ALIVE
  coverage), `test_runtime_health.py` +191 (the new `update_agmsg` fixture and its 4
  tests). Net reduction reflects retiring the vendored-tree's own test surface, not a
  coverage gap — that behavior is now upstream's responsibility, not a local fork's.
- `shellcheck -x scripts/update-agent-assets.sh scripts/check-tools.sh
home/dot_local/bin/common/executable_herdr-agents` → clean, exit 0.

## Live E2E (required by the task; real network, real upstream `install.sh`, scratch `$HOME` only)

```
$ DOTFILES_SOURCE_DIR="$PWD" HOME=<scratch> bash -c 'source scripts/update-agent-assets.sh; update_agmsg'
  ✓ Installed to ~/.agents/skills/agmsg/ (version 1.5.0)
$ cat <scratch>/.agents/skills/agmsg/VERSION
1.5.0
$ python3 -c "import json; print(json.load(open('<scratch>/.agents/.installed-manifest.json'))['steps']['update_agmsg'])"
{'kind': 'installer', 'source_version': '1.5.0', 'paths': [...SKILL.md, scripts, VERSION]}
```

**Idempotent re-run** (no fetch):

```
$ time HOME=<scratch> bash -c 'source scripts/update-agent-assets.sh; update_agmsg'
real 0m0.014s
```

**Forced update preserves live state** (VERSION rolled back to `0.0.0` to force a real
`install.sh --update`, not a fresh install):

```
before: messages.db sha256=44cc13b9...  teams/testteam/config.json sha256=deb196e7...
$ HOME=<scratch> bash -c 'source scripts/update-agent-assets.sh; update_agmsg'
after:  messages.db sha256=44cc13b9...  teams/testteam/config.json sha256=deb196e7...  (byte-identical)
VERSION after: 1.5.0
```

**`check_agmsg` / `doctor.sh` against the real install**:

```
$ HOME=<scratch> bash -c 'source scripts/check-tools.sh; check_agmsg'
found:   agmsg -> <scratch>/.agents/skills/agmsg (version 1.5.0, matches pin)
$ HOME=<scratch> bash <scratch>/.agents/skills/agmsg/scripts/doctor.sh --project <repo>
doctor: no registrations match this scope   (exit 2, before joining a team)
$ HOME=<scratch> bash <scratch>/.agents/skills/agmsg/scripts/join.sh testteam claude-code claude-code <repo>
Joined team testteam as claude-code
$ HOME=<scratch> bash <scratch>/.agents/skills/agmsg/scripts/doctor.sh --project <repo>
1 team(s), 1 registration(s), 0 warning(s) ... no warnings.   (exit 0)
```

## Deliverable 6 evidence

**(a) Ancestor-path identity matching** (scratch `$HOME`, real v1.5.0 install):

```
$ join.sh restest claude-main claude-code /home/moriya/Workspace/dotfiles
$ join.sh restest claude-wt claude-code /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-b
$ join.sh restest claude-unrelated claude-code /tmp/totally-unrelated-path
$ join.sh restest claude-sibling claude-code /home/moriya/Workspace/dotfiles-sibling-not-nested
$ identities.sh /home/moriya/Workspace/dotfiles claude-code
restest	claude-main
restest	claude-wt
$ identities.sh /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-b claude-code
testteam	claude-code
testteam	claude-code-a002
```

Querying the main-checkout path returns both the main-checkout's own registration
(`claude-main`) and the nested worktree's (`claude-wt`) — but not `claude-unrelated`
(no path relationship) or `claude-sibling` (string-prefix-only, not a real subdirectory).
Querying the nested worktree's own path does not return anything registered at the
parent. Directory-hierarchy-aware ancestor matching, confirmed one-directional.

**(b)/(c)**: not attempted (shared live herdr server; see report for rationale).

**(d) `team.sh --json`**:

```
$ team.sh testteam --json
[
{"member":"claude-code", ..., "consistency":"unverified","reach":{"status":"cannot","reason":"no_placement_record"},"tool":null},
{"member":"claude-code-a002", ...}
]
```

Well-formed JSON, exit 0.

## Not validated (blocker, operator-acknowledged, unchanged from T17)

`pr-feedback.py <n>` disposition output — script only exists on unmerged PR #182
(`feat/pr-feedback-gate`), not on `main` or this worktree. Skipped per the same operator
decision as T17.

## CI — https://github.com/mryfmo/dotfiles/pull/184 (head `79b2c5b`)

All checks passed, including the real installer exercise on fresh CI runners:

```
public-bootstrap (macos-14, client)      pass  6m17s
public-bootstrap (ubuntu-latest, client) pass  7m59s
public-bootstrap (ubuntu-latest, server) pass  7m29s
test (macos-14, client)                  pass  1m47s
test (ubuntu-latest, client)              pass  4m32s
test (ubuntu-latest, server)              pass  2m2s
validate                                  pass
build / build (client) / build (server)   pass
private-bootstrap (*)                     pass
nix                                       skipping (as on main)
```

This is the first real exercise of `update_agmsg` outside the local scratch-HOME
sandbox — a genuinely fresh `chezmoi apply` on three clean runners (macOS + two Ubuntu
variants), confirming the fetch-verify-install-record flow works end to end without any
of the sandbox assumptions from local testing (real network, real filesystem, real
upstream `install.sh`, no pre-seeded state).
Run: https://github.com/mryfmo/dotfiles/actions/runs/36211774234

## Revision 2 (round 2, head `1fe462e`..`16a967e`..final) — AGMSG-ACCEPTANCE 2026-09-26T02:37:13Z + supplement

Rebased `feat/agmsg-upstream-sync` onto `origin/main` at `3375fb0` (#183 merged;
`scripts/check-tools.sh` and `tests/unit/test_runtime_health.py` both touched by both
branches). Both conflicted files resolved by keeping BOTH T17's and T19's non-overlapping
additions in sequence — confirmed clean (`grep -n '^<<<<<<<\|^=======\|^>>>>>>>'` empty on
both files) before `git add` + `git rebase --continue`. One post-rebase fixture gap found
and fixed: `test_agent_asset_update_runs_gh_extension_ensure`'s `main()` stub list was
missing `update_agmsg() { :; }`, so it ran for real and polluted the test's stdout
assertion — added the stub (commit `1fe462e`).

### Fix 1 — unconditional live-state snapshot, surfaced stderr, truthful failure message

```
$ uv run python -m unittest tests.unit.test_runtime_health -v -k agmsg
test_agmsg_already_pinned_skips_download ... ok
test_agmsg_checksum_mismatch_fails_closed ... ok
test_agmsg_fresh_install_populates_skill_and_records_manifest ... ok
test_agmsg_migrates_marker_less_legacy_dir_without_losing_live_state ... ok
test_agmsg_update_aborts_when_install_corrupts_live_state ... ok
test_agmsg_update_never_touches_teams_db_run ... ok

----------------------------------------------------------------------
Ran 6 tests in 0.5s

OK
```

Two new tests close the exact gaps the finding named: a marker-less legacy dir (no
`VERSION`, no `.agmsg`) with real `teams/db/run` data now has its state snapshotted and
verified unchanged even though `installed == "none"` (previously skipped entirely); and a
fake `install.sh` that actually mutates a `teams/` file during `--update` now exercises the
abort branch (`touched live runtime state`, `installer failed`) for the first time — the
pre-existing "never touches state" test's fake `install.sh` never wrote anything, so that
branch had zero coverage before this round.

### Fix 6 — `set -e` hardening, `shasum` portability

`shellcheck -x scripts/update-agent-assets.sh` → clean, exit 0, after adding explicit
`|| return 1` to every previously-bare command inside `install_pinned_agmsg` (`mktemp` x2,
the checksum substitution, `tar xzf`, both `agmsg_state_snapshot` calls) and switching
`agmsg_state_snapshot`'s `find -exec sha256sum` to `find -exec shasum -a 256`, matching
every other checksum call in this file (`grep -n shasum scripts/update-agent-assets.sh`
now shows every hashing call site using the same tool, zero `sha256sum` remaining).

### Fix 2 — agmsg provenance-field enforcement (change request, not deliverable 1's literal schema)

```
$ uv run --with pyyaml scripts/validate-agent-assets.py
agent asset validation ok
$ uv run python -m unittest tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_each_incomplete_declaration tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_accept_complete_declarations_and_rendered_versions -v
test_assets_reject_each_incomplete_declaration ... ok
test_assets_accept_complete_declarations_and_rendered_versions ... ok

----------------------------------------------------------------------
Ran 2 tests in 0.016s

OK
```

Change request (explicit, recorded here since this task file's own Revision history is
orchestrator-owned): kept `source: git-commit`/`verify: sha256` (a byte-for-byte tarball
hash, strictly stronger than deliverable 1's bare `git rev-parse HEAD == ref_commit`
comparison) instead of inventing `source: agmsg-installer`. What was missing — and is now
fixed — is that the validator accepted `ref`/`bootstrap_integrity` as decorative keys it
never checked. `validate_assets` now requires, specifically for the `agmsg` asset: `ref`
non-empty, `pin` a full 40-character git commit sha (`GIT_COMMIT_SHA` regex — rejects a
truncated `c487be2`), and `bootstrap_integrity` a well-formed `sha512-<base64>` npm
integrity string (`NPM_SHA512_INTEGRITY` regex). Four new subtest cases added (missing
ref, short pin, missing/malformed bootstrap*integrity), plus an `agmsg` entry in the shared
asset-manifest test fixture so the happy-path acceptance test also exercises it. The seven
tests deleted with the two retired vendoring-only validators
(`validate_claude_command_parity`, `validate_agmsg_script_modes`) are not restored as such
— those validators' purpose (enforcing chezmoi `executable*` prefixes and a hand-maintained
command symlink) genuinely no longer applies once agmsg is installer-owned, matching
crit/zed/tode; the four new provenance tests are this round's replacement coverage for the
one thing actually still worth validating about this asset's own fields.

### Fix 3 — dangling `~/.claude/skills/agmsg/**` cleanup

```
$ mkdir -p <scratch-home>/.claude/skills/agmsg/scripts
$ echo '# stale vendored skill' > <scratch-home>/.claude/skills/agmsg/SKILL.md
$ echo stale > <scratch-home>/.claude/skills/agmsg/scripts/send.sh
$ CI=true chezmoi apply --config <scratch-config>/chezmoi.yaml --destination <scratch-home> --dry-run --verbose 2>&1 \
    | awk '/^diff --git a\/\.claude\/skills\/agmsg /{flag=1} flag{print; exit_after_next}'
diff --git a/.claude/skills/agmsg b/.claude/skills/agmsg
deleted file mode 40775
index e69de29bb2d1d6434b8b29ae775ad8c2e48c5391..0000000000000000000000000000000000000000
--- a/.claude/skills/agmsg
+++ /dev/null

$ CI=true chezmoi apply --config <scratch-config>/chezmoi.yaml --destination <scratch-home> --exclude=scripts
$ [ -e <scratch-home>/.claude/skills/agmsg ] && echo STILL PRESENT || echo REMOVED
REMOVED
```

(`--exclude=scripts` only to skip an unrelated sudo-gated `00-setup-ssh.sh`
`.chezmoiscripts/ubuntu` step in this sandbox — irrelevant to file-state cleanup, which is
what this evidence is about.) Fix: one line added to `home/.chezmoiremove`
(`.claude/skills/agmsg/**`), following the file's existing convention (three prior entries
for other retired paths).

### Fix 4 — `ext-tools` writable root; Codex delivery-mode change request

Verified directly against upstream v1.5.0's `install.sh` (`_configure_codex_sandbox_file`,
`configure_codex_sandbox`): `writable_paths=("$SKILL_DIR/db" "$SKILL_DIR/teams"
"$SKILL_DIR/run" "$SKILL_DIR/ext-tools")` — always four roots, both on the `--update` and
fresh-install paths, regardless of delivery mode. This repo's manifest/template/validator
only declared the first three.

```
$ uv run --with pyyaml scripts/generate-agent-configs.py
generated agent configs updated
$ uv run --with pyyaml scripts/generate-agent-configs.py --check
generated agent configs are up to date
$ uv run --with pyyaml scripts/validate-agent-assets.py
agent asset validation ok
$ uv run python -m unittest tests.unit.test_validate_agent_assets -v -k codex_sandbox
test_codex_sandbox_workspace_write_accepts_matching_manifest ... ok
test_codex_sandbox_workspace_write_must_match_manifest ... ok
test_codex_sandbox_workspace_write_requires_all_agmsg_roots ... ok

----------------------------------------------------------------------
Ran 3 tests in 0.021s

OK
```

Change request for the other half of deliverable 5: Codex stays on `turn`, not upstream's
shim-based `monitor` bridge. Independently verified against the live upstream tracker (not
assumed from the task's own citation, which named issue #133 -- unrelated, see Fix 7):

```
$ gh api repos/fujibee/agmsg/issues/149 --jq '"#\(.number): \(.state) — \(.title)"'
#149: open — Codex bridge: no teardown on session end, orphaning the bridge/app-server/watch-once and blocking relaunch
$ gh api repos/fujibee/agmsg/issues/151 --jq '"#\(.number): \(.state) — \(.title)"'
#151: open — Codex monitor: enabling mode monitor doesn't start the bridge in a live session (needs restart)
$ gh api repos/fujibee/agmsg/issues/1236 --jq '"#\(.number): \(.state) — \(.title)"'
#1236: open — codex monitor: a bridge that cannot deliver restarts forever while status reports it alive
```

All three open as of this round. SKILL.md:37-38's self-contradiction (line 37 said Codex
gets `turn`; line 38 claimed herdr-agents "sets each identity to its upstream default
delivery mode", false for Claude Code's `both`) rewritten to state the actual per-type
modes and this reasoning instead of the incorrect blanket claim.

### Fix 5 — `AGMSG_RESOLVE_PROJECT=0` on every worker pane; corrected doctor comment

Redid deliverable 6(a) against a REAL, freshly-installed v1.5.0 (`install.sh --cmd agmsg
--agent-type claude-code`, scratch `$HOME`), running the actual agent-driven entry points
(`join.sh`, `whoami.sh`, `session-start.sh`), not `identities.sh` with hand-typed paths (the
prior round's mistake — `identities.sh` is a pure exact-match lookup with no ancestor logic
at all; verified directly from `scripts/identities.sh` + `scripts/lib/resolve-project.sh`'s
`agmsg_project_sql_in_list`/`agmsg_project_path_variants`, which only generate
spelling-normalized variants of the SAME path).

```
$ MAIN=<scratch>/main; WORKTREE="$MAIN/.claude/worktrees/worker-x"; mkdir -p "$WORKTREE"
$ join.sh demo orchestrator claude-code "$MAIN"
Created team: demo
Joined team demo as orchestrator
$ ( cd "$WORKTREE" && join.sh demo worker-x claude-code "$(pwd)" )            # resolution ON (default)
Joined team demo as worker-x
$ identities.sh "$WORKTREE" claude-code                                       # exact lookup at the worktree
                                                                                (empty — not found here)
$ identities.sh "$MAIN" claude-code                                           # exact lookup at the main checkout
demo	orchestrator
demo	worker-x                                                               # <- silently landed here instead
$ leave.sh demo worker-x
Left team demo
$ ( cd "$WORKTREE" && AGMSG_RESOLVE_PROJECT=0 join.sh demo worker-x claude-code "$(pwd)" )
Joined team demo as worker-x
$ identities.sh "$WORKTREE" claude-code
demo	worker-x                                                               # <- now registered where it should be
$ identities.sh "$MAIN" claude-code
demo	orchestrator                                                           # <- unaffected
```

This is the exact P2 collision mechanism the task exists to close, reproduced against real
upstream code, not inferred. `whoami.sh`'s marker-vs-ancestor-walk ordering also confirmed
with a live process disguised as `claude` (`exec -a claude sleep 300`, since
`agmsg_read_project_marker` does a real liveness+argv check the `AGMSG_AGENT_PID`
test-override alone does not bypass): `session-start.sh` writes a per-process marker
pointing at the worktree, and a subsequent `whoami.sh` call from a deep subdirectory of that
worktree (with the worktree's own registration removed, so the ancestor walk would
otherwise climb past it to the main checkout) still reports "not joined" rather than the
orchestrator's identity — the marker won.

Separately discovered while running this: `session-start.sh` (upstream #367) unconditionally
skips (`exit 0`, no marker, no directive) whenever the hook's own reported `cwd` contains a
literal `.claude/worktrees` path segment — a guard for Claude Code's own short-lived
background-task sub-sessions that happens to pattern-match this repo's unrelated, long-lived
resident-worker convention of the same name. This live session's own SessionStart hook did
fire its Monitor directive despite running from exactly such a path, so the two do not
appear to collide in practice — but the precise reason (what `cwd` Claude Code's hook JSON
reports for a resident worker pane vs. what a plain script sees) was not resolved this
round. Flagged, not asserted; see the report's open-questions note.

```
$ uv run python -m unittest tests.unit.test_herdr_agents -v
[... 82 tests ...]
----------------------------------------------------------------------
Ran 82 tests in ~15s

OK
```

`distinct_agmsg_identity_count`'s doc comment corrected (it described `identities.sh` doing
an ancestor walk; it does not — that logic lives in `join.sh`/`whoami.sh` et al., not
`identities.sh`). All three `split_agent_pane` worker-pane call sites now also pass
`--env AGMSG_RESOLVE_PROJECT=0` (both `worker_kind` values); two `test_herdr_agents.py`
tests whose exact pane-split command string predated this env var updated to match, plus a
new explicit assertion alongside the existing `AGMSG_CC_MONITOR_KEEP_ALIVE=1` check.
Documented in README.md and the agmsg-orchestration skill, citing upstream #92 and
`docs/design.md`'s "Project resolution" section per this round's instruction.

### Fix 7 — pane-status inference removed; poke exit codes documented; #133 claim independently re-verified and declined

SKILL.md step 6's "wake it with `herdr pane run` ... if its status isn't already `working`"
removed: inferring pane/agent status to pick the next action is prohibited (rule G1), and it
duplicates `poke.sh`'s own herdr driver (`terminal_poke` → `herdr agent prompt` sends text
and submits in one call regardless of pane state; verified directly from
`scripts/drivers/terminals/herdr/ops.sh`) plus `poke.sh`'s own input-box safety check
(upstream #1321/#1322). Documented `poke.sh`'s exit-code taxonomy (10/12/13/14/15, read
directly from `scripts/poke.sh`'s own decision logic) and made explicit that 13 must never
be retried as `send.sh` — `poke.sh` has already either delivered through its own narrow
same-team agmsg-message fallback or printed a precise reason plus a pointer to the type's
native channel.

Independently re-verified and DECLINED: this round's "document that `--update` stops
in-flight `watch.sh` (upstream #133)" does not hold for the pinned v1.5.0.

```
$ gh api repos/fujibee/agmsg/issues/133 --jq '"#\(.number): \(.state) — \(.title)"'
#133: closed — delivery.sh set does not auto-re-register hooks after skill upgrade
```

That is an unrelated, already-closed issue. The actual behavior described (watch.sh exiting
when `install.sh` changes the code under it) was upstream issue #1320 ("watch.sh: restart on
the new code instead of exiting on an install change"), closed 2026-09-19 — before v1.5.0.
Confirmed directly in the real v1.5.0 `scripts/watch.sh` source (VERSION-gated restart logic
around line 674 onward: watch.sh now waits for the install to finish and `exec`s onto the
new code rather than exiting). Documenting the old "stops in-flight watch.sh" behavior would
be writing something false about the version this repo actually installs, so no doc change
was made for this specific item — recorded here instead of silently omitted.

### Full suite after all round-2 fixes

```
$ shellcheck -x scripts/update-agent-assets.sh scripts/check-tools.sh home/dot_local/bin/common/executable_herdr-agents
(clean, exit 0)
$ uv run --with pyyaml scripts/generate-agent-configs.py --check
generated agent configs are up to date
$ uv run --with pyyaml scripts/validate-agent-assets.py
agent asset validation ok
$ uv run python -m unittest discover -s tests/unit -v
----------------------------------------------------------------------
Ran 413 tests in ~31s

OK (skipped=1)
```

### CompactionDB

```
$ python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "agmsg is installed by the upstream installer at a pinned tag verified by a byte-for-byte sha256 of the tag's source archive ..."
90b08f9f-b1a7-4866-99b0-233b51e97230
```

### CodeRabbit / review gate

Per AGMSG-NOTE (2026-09-26T03:00:41Z, `claude-remediation-dot`): CodeRabbit removed from the
PR gate; the 04:36Z slot and every `@coderabbitai` request are cancelled; the bot-review gate
becomes Codex review (T16 revision 2). No CodeRabbit request was made on the final head per
this note.
