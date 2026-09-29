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

---

## Round 2 (task revision 3), worker claude-standard-dot-a005

Invalid UTF-8 byte sequences, where `head -c 300` in the 6(a) script cut a multibyte character, are shown as U+FFFD. Scratch paths are shown as `$S` (the session scratchpad, `/tmp/claude-1000/-home-moriya-Workspace-dotfiles/09f873c6-64b4-4b31-b88a-621530276e29/scratchpad`). Every scratch-HOME run uses `env -i HOME=<scratch>`, so none touches the real HOME. Pre-rebase SHAs in the baselines map to the final SHAs as the report lists them.

### Branch, final diff against origin/main, commit list
```
$ git rev-parse --short origin/main; git rev-parse HEAD
5ea0d9d
55faae062d34b7b8f9dc06203069982547540d50
$ git -C /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c diff origin/main --stat
 .../runs/dot-agmsg-upstream-sync-T19-a01.md        |   9 +
 .../learning/dot-agmsg-upstream-sync-T19-a01.md    |  69 +++
 .../reports/dot-agmsg-upstream-sync-T19-a01.md     | 271 ++++++++++
 .../sandboxes/dot-agmsg-upstream-sync-T19-a01.md   |  15 +
 .../dot-agmsg-upstream-sync-T19-a01-crit.json      |  17 +
 ...t-agmsg-upstream-sync-T19-a01-review-receipt.md |  11 +
 .../validation/dot-agmsg-upstream-sync-T19-a01.md  | 456 ++++++++++++++++
 README.md                                          | 125 ++++-
 home/.chezmoiremove                                |   1 +
 home/.chezmoitemplates/codex-config-managed.toml   |   2 +-
 home/dot_agents/agent-config.yaml                  |  36 +-
 .../dot_agents/skills/agmsg-orchestration/SKILL.md |  11 +-
 home/dot_agents/skills/agmsg/SKILL.md              | 136 -----
 home/dot_agents/skills/agmsg/agents/openai.yaml    |   5 -
 home/dot_agents/skills/agmsg/db/.keep              |   1 -
 home/dot_agents/skills/agmsg/run/.keep             |   1 -
 .../skills/agmsg/scripts/executable_actas-claim.sh |  78 ---
 .../skills/agmsg/scripts/executable_check-inbox.sh | 166 ------
 .../skills/agmsg/scripts/executable_config.sh      | 176 -------
 .../skills/agmsg/scripts/executable_delivery.sh    | 577 ---------------------
 .../skills/agmsg/scripts/executable_history.sh     |  41 --
 .../skills/agmsg/scripts/executable_hook.sh        |  26 -
 .../skills/agmsg/scripts/executable_identities.sh  |  48 --
 .../skills/agmsg/scripts/executable_inbox.sh       |  48 --
 .../skills/agmsg/scripts/executable_init-db.sh     |  28 -
 .../skills/agmsg/scripts/executable_join.sh        | 104 ----
 .../skills/agmsg/scripts/executable_leave.sh       |  45 --
 .../skills/agmsg/scripts/executable_rename-team.sh |  62 ---
 .../skills/agmsg/scripts/executable_rename.sh      |  59 ---
 .../skills/agmsg/scripts/executable_reset.sh       | 137 -----
 .../skills/agmsg/scripts/executable_send.sh        |  43 --
 .../skills/agmsg/scripts/executable_session-end.sh |  66 ---
 .../agmsg/scripts/executable_session-start.sh      | 187 -------
 .../skills/agmsg/scripts/executable_team.sh        |  53 --
 .../skills/agmsg/scripts/executable_watch.sh       | 194 -------
 .../skills/agmsg/scripts/executable_whoami.sh      | 134 -----
 .../skills/agmsg/scripts/lib/actas-lock.sh         | 241 ---------
 .../skills/agmsg/scripts/lib/identifier.sh         |  21 -
 .../dot_agents/skills/agmsg/scripts/lib/storage.sh |  33 --
 .../scripts/release/executable_sync-version.sh     |  94 ----
 home/dot_agents/skills/agmsg/teams/.keep           |   1 -
 .../skills/agmsg/templates/cmd.antigravity.md      | 136 -----
 .../skills/agmsg/templates/cmd.claude-code.md      | 349 -------------
 .../dot_agents/skills/agmsg/templates/cmd.codex.md | 136 -----
 .../skills/agmsg/templates/cmd.copilot.md          | 136 -----
 .../skills/agmsg/templates/cmd.gemini.md           | 136 -----
 home/dot_claude/commands/symlink_agmsg.md.tmpl     |   1 -
 .../skills/agmsg/agents/symlink_openai.yaml.tmpl   |   1 -
 .../agmsg/scripts/lib/symlink_actas-lock.sh.tmpl   |   1 -
 .../agmsg/scripts/lib/symlink_identifier.sh.tmpl   |   1 -
 .../agmsg/scripts/lib/symlink_storage.sh.tmpl      |   1 -
 .../scripts/release/symlink_sync-version.sh.tmpl   |   1 -
 .../agmsg/scripts/symlink_actas-claim.sh.tmpl      |   1 -
 .../agmsg/scripts/symlink_check-inbox.sh.tmpl      |   1 -
 .../skills/agmsg/scripts/symlink_config.sh.tmpl    |   1 -
 .../skills/agmsg/scripts/symlink_delivery.sh.tmpl  |   1 -
 .../skills/agmsg/scripts/symlink_history.sh.tmpl   |   1 -
 .../skills/agmsg/scripts/symlink_hook.sh.tmpl      |   1 -
 .../agmsg/scripts/symlink_identities.sh.tmpl       |   1 -
 .../skills/agmsg/scripts/symlink_inbox.sh.tmpl     |   1 -
 .../skills/agmsg/scripts/symlink_init-db.sh.tmpl   |   1 -
 .../skills/agmsg/scripts/symlink_join.sh.tmpl      |   1 -
 .../skills/agmsg/scripts/symlink_leave.sh.tmpl     |   1 -
 .../agmsg/scripts/symlink_rename-team.sh.tmpl      |   1 -
 .../skills/agmsg/scripts/symlink_rename.sh.tmpl    |   1 -
 .../skills/agmsg/scripts/symlink_reset.sh.tmpl     |   1 -
 .../skills/agmsg/scripts/symlink_send.sh.tmpl      |   1 -
 .../agmsg/scripts/symlink_session-end.sh.tmpl      |   1 -
 .../agmsg/scripts/symlink_session-start.sh.tmpl    |   1 -
 .../skills/agmsg/scripts/symlink_team.sh.tmpl      |   1 -
 .../skills/agmsg/scripts/symlink_watch.sh.tmpl     |   1 -
 .../skills/agmsg/scripts/symlink_whoami.sh.tmpl    |   1 -
 home/dot_claude/skills/agmsg/symlink_SKILL.md.tmpl |   1 -
 .../templates/symlink_cmd.antigravity.md.tmpl      |   1 -
 .../templates/symlink_cmd.claude-code.md.tmpl      |   1 -
 .../agmsg/templates/symlink_cmd.codex.md.tmpl      |   1 -
 .../agmsg/templates/symlink_cmd.copilot.md.tmpl    |   1 -
 .../agmsg/templates/symlink_cmd.gemini.md.tmpl     |   1 -
 .../dot_config/claude/rules/agmsg-orchestration.md |   1 +
 .../dot_local/bin/common/executable_agmsg-dispatch |  26 +-
 home/dot_local/bin/common/executable_herdr-agents  |  80 ++-
 scripts/check-agent-runtime.py                     |   6 +-
 scripts/check-tools.sh                             |  30 ++
 scripts/update-agent-assets.sh                     | 179 +++++++
 scripts/validate-agent-assets.py                   | 140 +++--
 tests/install/common/check_tools.bats              |  28 +
 tests/unit/test_agmsg_dispatch.py                  |  43 +-
 tests/unit/test_agmsg_orchestration_docs.py        |  39 ++
 tests/unit/test_agmsg_send.py                      | 347 -------------
 tests/unit/test_asset_manifest.py                  |   3 +-
 tests/unit/test_check_agent_runtime.py             |  29 ++
 tests/unit/test_chezmoiremove_agmsg.py             |  61 +++
 tests/unit/test_herdr_agents.py                    |  91 +++-
 tests/unit/test_runtime_health.py                  | 444 +++++++++++++++-
 tests/unit/test_validate_agent_assets.py           | 226 +++++---
 95 files changed, 2252 insertions(+), 4274 deletions(-)
$ git log --oneline origin/main..HEAD
55faae0 fix(doctor): treat the installer-owned agmsg skill and state backups as accounted
5623e83 fix(agmsg): stop the state guard from failing fresh installs; tighten ownership rules
7c0e1d7 fix(agmsg): spell the post-install VERSION check as an if (SC2015)
c39e4d1 fix(agmsg-dispatch): run on upstream 1.5.0 libs; keep it as the herdr wake path
13e6d6b docs(agmsg): ground registration, delivery, and wake rules in verified 1.5.0 behaviour
ad7338d fix(agmsg): declare assets.agmsg as source agmsg-installer per the spec
aa5c038 fix(agmsg): never --update a marker-less dir; back up and verify live state
e00b477 chore(orchestration): T19 revision 2 artifacts (report/validation/sandbox/learning/crit)
f9005cc docs(agmsg): drop pane-status inference from SKILL.md, document poke exit codes
ea9452a fix(agmsg): register worker identities with AGMSG_RESOLVE_PROJECT=0
326500f fix(agmsg): add ext-tools writable root, correct SKILL.md delivery claim
e29697c fix(chezmoi): remove the retired agmsg skill symlink farm from live hosts
42f2426 fix(validate): enforce agmsg provenance fields instead of accepting them decoratively
64b21c2 fix(agmsg): always guard live state across install/update, harden set -e
5480a8a fix(tests): stub update_agmsg in the gh-extension main() fixture
349c4bb docs(herdr-agents): document verified ancestor-path identity matching
118e339 fix(agmsg): realign with task revision 2 (v1.5.0, both mode, KEEP_ALIVE)
972a57c feat(herdr-agents): default agmsg bootstrap to upstream monitor mode
2a60601 docs(agmsg): describe upstream poke.sh/send.sh --body-file delivery
db6447f feat(agmsg): retire the vendored skill snapshot and agmsg-dispatch
93f36bd feat(agmsg): install the skill from the pinned upstream commit
```

### Rebase: main-side lines preserved in the ten overlapping files
```
$ (python) for each overlapping file: lines main added since the round-1 base 3375fb0 (git diff -U0 3375fb0 origin/main -- FILE) that are absent from `git show HEAD:FILE`
origin/main = 5ea0d9d  HEAD = 55faae0
README.md: main added 109 non-blank lines; missing at HEAD: 0
home/dot_agents/agent-config.yaml: main added 19 non-blank lines; missing at HEAD: 0
home/dot_agents/skills/agmsg-orchestration/SKILL.md: main added 10 non-blank lines; missing at HEAD: 0
home/dot_local/bin/common/executable_herdr-agents: main added 415 non-blank lines; missing at HEAD: 0
scripts/check-tools.sh: main added 36 non-blank lines; missing at HEAD: 0
scripts/update-agent-assets.sh: main added 51 non-blank lines; missing at HEAD: 0
scripts/validate-agent-assets.py: main added 83 non-blank lines; missing at HEAD: 0
tests/unit/test_herdr_agents.py: main added 1264 non-blank lines; missing at HEAD: 0
tests/unit/test_runtime_health.py: main added 11 non-blank lines; missing at HEAD: 0
tests/unit/test_validate_agent_assets.py: main added 129 non-blank lines; missing at HEAD: 0
```

### Upstream v1.5.0 source archive (pin check)
```
$ curl -fsSL https://github.com/fujibee/agmsg/archive/c487be269c1973aeb01ca831806eb3f65ff3366d.tar.gz -o agmsg.tgz && shasum -a 256 agmsg.tgz && cat v150/VERSION
9201cb5ff23ddd9ddaa19ff821dce0d0f2d58c6c292aade252a8d824b3dfc059  agmsg.tgz
1.5.0
```

### Finding 5/11(ii) + 6(a)/6(d): project resolution in a scratch HOME with a real v1.5.0 install (script $S/t19-6a.sh)
```
# HOME=$S/t19-home (scratch); agmsg source = c487be2 (v1.5.0, tarball sha256 9201cb5f...)

$ env -i HOME=$S/t19-home PATH=/usr/local/bin:/usr/bin:/bin TERM=dumb LANG=C.UTF-8 bash $S/agmsg-src/v150/install.sh --cmd agmsg --agent-type claude-code

  agmsg — Agent Messaging
  ────────────────────────

  Installing to ~/.agents/skills/agmsg/ ...
  shared SKILL.md stays codex: claude-code has its own skill file
  ~ 0 file(s) backed up to .trash/ (cleared on next upgrade)
  + installed Antigravity TUI shim (~/.agents/bin/agy-tui)
  + created default config at db/config.yaml
  + installed /agmsg command to ~/.claude/commands/

  ✓ Installed to ~/.agents/skills/agmsg/ (version 1.5.0)

  Next steps:
    1. Restart your agent (Claude Code / Codex / Gemini CLI / Antigravity / OpenCode) to pick up the new skill
    2. Run the command to join a team:
       Claude Code:  /agmsg
       Codex:        $agmsg
       Gemini CLI:   $agmsg
       Antigravity:  $agmsg
       Copilot CLI:  /agmsg
       OpenCode:     $agmsg
       It will prompt for team name and agent name on first run.

  Docs: https://agmsg.cc/

[exit 0]

$ cat $S/t19-home/.agents/skills/agmsg/VERSION
1.5.0
[exit 0]
MAIN=$S/t19-home/work/proj
WT=$S/t19-home/work/proj/.claude/worktrees/wt

## 1. orchestrator registers at MAIN (explicit path, resolution off)

$ env -i HOME=$S/t19-home PATH=/usr/local/bin:/usr/bin:/bin TERM=dumb LANG=C.UTF-8 AGMSG_RESOLVE_PROJECT=0 bash $S/t19-home/.agents/skills/agmsg/scripts/join.sh t19 orch claude-code $S/t19-home/work/proj
Created team: t19
Joined team t19 as orch
[exit 0]

## 2. join.sh from inside WT WITHOUT AGMSG_RESOLVE_PROJECT=0 (no marker: AGMSG_AGENT_PID='')

$ bash -c cd '$S/t19-home/work/proj/.claude/worktrees/wt' && env -i HOME=$S/t19-home PATH=/usr/local/bin:/usr/bin:/bin TERM=dumb LANG=C.UTF-8 AGMSG_AGENT_PID= bash '$S/t19-home/.agents/skills/agmsg/scripts/join.sh' t19 w-resolved claude-code '$S/t19-home/work/proj/.claude/worktrees/wt'
Joined team t19 as w-resolved
[exit 0]

## 3. join.sh from inside WT WITH AGMSG_RESOLVE_PROJECT=0

$ bash -c cd '$S/t19-home/work/proj/.claude/worktrees/wt' && env -i HOME=$S/t19-home PATH=/usr/local/bin:/usr/bin:/bin TERM=dumb LANG=C.UTF-8 AGMSG_RESOLVE_PROJECT=0 bash '$S/t19-home/.agents/skills/agmsg/scripts/join.sh' t19 w-worktree claude-code '$S/t19-home/work/proj/.claude/worktrees/wt'
Joined team t19 as w-worktree
[exit 0]

## registrations per path (identities.sh is a pure lookup)

$ env -i HOME=$S/t19-home PATH=/usr/local/bin:/usr/bin:/bin TERM=dumb LANG=C.UTF-8 bash $S/t19-home/.agents/skills/agmsg/scripts/identities.sh $S/t19-home/work/proj claude-code
t19	orch
t19	w-resolved
[exit 0]

$ env -i HOME=$S/t19-home PATH=/usr/local/bin:/usr/bin:/bin TERM=dumb LANG=C.UTF-8 bash $S/t19-home/.agents/skills/agmsg/scripts/identities.sh $S/t19-home/work/proj/.claude/worktrees/wt claude-code
t19	w-worktree
[exit 0]

## 4. whoami.sh inside WT, NO marker (AGMSG_AGENT_PID='')

$ bash -c cd '$S/t19-home/work/proj/.claude/worktrees/wt' && env -i HOME=$S/t19-home PATH=/usr/local/bin:/usr/bin:/bin TERM=dumb LANG=C.UTF-8 AGMSG_AGENT_PID= bash '$S/t19-home/.agents/skills/agmsg/scripts/whoami.sh' '$S/t19-home/work/proj/.claude/worktrees/wt' claude-code
agent=w-worktree teams=t19 type=claude-code project=$S/t19-home/work/proj/.claude/worktrees/wt
[exit 0]

## fake agent pid 111671 (comm=claude)

## 5. session-start.sh baked with WT, hook cwd = WT (a seat launched inside the nested worktree)

$ bash -c cd '$S/t19-home/work/proj/.claude/worktrees/wt' && printf '{"session_id":"s-wt","cwd":"$S/t19-home/work/proj/.claude/worktrees/wt"}' | env -i HOME=$S/t19-home PATH=/usr/local/bin:/usr/bin:/bin TERM=dumb LANG=C.UTF-8 AGMSG_AGENT_PID=111671 bash '$S/t19-home/.agents/skills/agmsg/scripts/session-start.sh' claude-code '$S/t19-home/work/proj/.claude/worktrees/wt' | head -c 300; echo; echo "marker: $(cat '$S/t19-home/.agents/skills/agmsg/run/proj.111671.project' 2>/dev/null || echo none)"

marker: none
[exit 0]

## 5b. whoami.sh inside WT with no marker for the agent pid

$ bash -c cd '$S/t19-home/work/proj/.claude/worktrees/wt' && env -i HOME=$S/t19-home PATH=/usr/local/bin:/usr/bin:/bin TERM=dumb LANG=C.UTF-8 AGMSG_AGENT_PID=111671 bash '$S/t19-home/.agents/skills/agmsg/scripts/whoami.sh' '$S/t19-home/work/proj/.claude/worktrees/wt' claude-code
agent=w-worktree teams=t19 type=claude-code project=$S/t19-home/work/proj/.claude/worktrees/wt
[exit 0]

## 6. session-start.sh baked with MAIN, hook cwd = MAIN (a seat launched from the main checkout), then whoami inside WT under the same agent pid

$ bash -c cd '$S/t19-home/work/proj' && printf '{"session_id":"s-main","cwd":"$S/t19-home/work/proj"}' | env -i HOME=$S/t19-home PATH=/usr/local/bin:/usr/bin:/bin TERM=dumb LANG=C.UTF-8 AGMSG_AGENT_PID=111671 bash '$S/t19-home/.agents/skills/agmsg/scripts/session-start.sh' claude-code '$S/t19-home/work/proj' | head -c 300; echo; echo "marker: $(cat '$S/t19-home/.agents/skills/agmsg/run/proj.111671.project' 2>/dev/null || echo none)"
AGMSG terminal: plain (no addressable pane) capabilities=spawn despawn peek poke; notes: $S/t19-home/.agents/skills/agmsg/scripts/drivers/terminals/plain/README.md
AGMSG team.sh <team>: shows every teammate
marker: $S/t19-home/work/proj
[exit 0]

$ bash -c cd '$S/t19-home/work/proj/.claude/worktrees/wt' && env -i HOME=$S/t19-home PATH=/usr/local/bin:/usr/bin:/bin TERM=dumb LANG=C.UTF-8 AGMSG_AGENT_PID=111671 bash '$S/t19-home/.agents/skills/agmsg/scripts/whoami.sh' '$S/t19-home/work/proj/.claude/worktrees/wt' claude-code
multiple=true agents=orch,w-resolved teams=t19 type=claude-code project=$S/t19-home/work/proj
[exit 0]

## 6b. marker = MAIN, whoami inside WT with AGMSG_RESOLVE_PROJECT=0

$ bash -c cd '$S/t19-home/work/proj/.claude/worktrees/wt' && env -i HOME=$S/t19-home PATH=/usr/local/bin:/usr/bin:/bin TERM=dumb LANG=C.UTF-8 AGMSG_AGENT_PID=111671 AGMSG_RESOLVE_PROJECT=0 bash '$S/t19-home/.agents/skills/agmsg/scripts/whoami.sh' '$S/t19-home/work/proj/.claude/worktrees/wt' claude-code
agent=w-worktree teams=t19 type=claude-code project=$S/t19-home/work/proj/.claude/worktrees/wt
[exit 0]

## 6c. marker = MAIN, join.sh from inside WT without and with AGMSG_RESOLVE_PROJECT=0

$ bash -c cd '$S/t19-home/work/proj/.claude/worktrees/wt' && env -i HOME=$S/t19-home PATH=/usr/local/bin:/usr/bin:/bin TERM=dumb LANG=C.UTF-8 AGMSG_AGENT_PID=111671 bash '$S/t19-home/.agents/skills/agmsg/scripts/join.sh' t19 w-marker claude-code '$S/t19-home/work/proj/.claude/worktrees/wt'
Joined team t19 as w-marker
[exit 0]

$ bash -c cd '$S/t19-home/work/proj/.claude/worktrees/wt' && env -i HOME=$S/t19-home PATH=/usr/local/bin:/usr/bin:/bin TERM=dumb LANG=C.UTF-8 AGMSG_AGENT_PID=111671 AGMSG_RESOLVE_PROJECT=0 bash '$S/t19-home/.agents/skills/agmsg/scripts/join.sh' t19 w-marker-off claude-code '$S/t19-home/work/proj/.claude/worktrees/wt'
Joined team t19 as w-marker-off
[exit 0]

## 7. session-start.sh baked with WT but hook cwd = MAIN (delivery.sh set targets the worktree path; pane cwd outside .claude/worktrees)

$ bash -c cd '$S/t19-home/work/proj' && printf '{"session_id":"s-wt2","cwd":"$S/t19-home/work/proj"}' | env -i HOME=$S/t19-home PATH=/usr/local/bin:/usr/bin:/bin TERM=dumb LANG=C.UTF-8 AGMSG_AGENT_PID=111671 bash '$S/t19-home/.agents/skills/agmsg/scripts/session-start.sh' claude-code '$S/t19-home/work/proj/.claude/worktrees/wt' | head -c 300; echo; echo "marker: $(cat '$S/t19-home/.agents/skills/agmsg/run/proj.111671.project' 2>/dev/null || echo none)"
AGMSG terminal: plain (no addressable pane) capabilities=spawn despawn peek poke; notes: $S/t19-home/.agents/skills/agmsg/scripts/drivers/terminals/plain/README.md
AGMSG team.sh <team>: shows every teammate
marker: $S/t19-home/work/proj/.claude/worktrees/wt
[exit 0]

$ bash -c cd '$S/t19-home/work/proj/.claude/worktrees/wt' && env -i HOME=$S/t19-home PATH=/usr/local/bin:/usr/bin:/bin TERM=dumb LANG=C.UTF-8 AGMSG_AGENT_PID=111671 bash '$S/t19-home/.agents/skills/agmsg/scripts/whoami.sh' '$S/t19-home/work/proj/.claude/worktrees/wt' claude-code
multiple=true agents=w-marker-off,w-worktree teams=t19 type=claude-code project=$S/t19-home/work/proj/.claude/worktrees/wt
[exit 0]

## final registrations

$ env -i HOME=$S/t19-home PATH=/usr/local/bin:/usr/bin:/bin TERM=dumb LANG=C.UTF-8 bash $S/t19-home/.agents/skills/agmsg/scripts/identities.sh $S/t19-home/work/proj claude-code
t19	orch
t19	w-marker
t19	w-resolved
[exit 0]

$ env -i HOME=$S/t19-home PATH=/usr/local/bin:/usr/bin:/bin TERM=dumb LANG=C.UTF-8 bash $S/t19-home/.agents/skills/agmsg/scripts/identities.sh $S/t19-home/work/proj/.claude/worktrees/wt claude-code
t19	w-marker-off
t19	w-worktree
[exit 0]

## 6(d). team.sh --json for the scratch team

$ env -i HOME=$S/t19-home PATH=/usr/local/bin:/usr/bin:/bin TERM=dumb LANG=C.UTF-8 bash $S/t19-home/.agents/skills/agmsg/scripts/team.sh t19 --json
[
{"member":"orch","type":"claude-code","project":"$S/t19-home/work/proj","terminal":"unknown","pane":"unknown:no_placement_record","container":"unknown:no_placement_record","activity":"unknown:no_placement_record","delivery":"off (unrecognized: no settings file found at $S/t19-home/work/proj/.claude/settings.local.json -- this project may not be registered)","pane_label":{"status":"unknown","reason":"no_placement_record"},"agent_key":{"status":"unknown","reason":"no_placement_record"},"cli_session":{"status":"unknown","reason":"no_placement_record"},"consistency":"unverified","reach":{"status":"cannot","reason":"no_placement_record"},"tool":null},
{"member":"w-marker","type":"claude-code","project":"$S/t19-home/work/proj","terminal":"unknown","pane":"unknown:no_placement_record","container":"unknown:no_placement_record","activity":"unknown:no_placement_record","delivery":"off (unrecognized: no settings file found at $S/t19-home/work/proj/.claude/settings.local.json -- this project may not be registered)","pane_label":{"status":"unknown","reason":"no_placement_record"},"agent_key":{"status":"unknown","reason":"no_placement_record"},"cli_session":{"status":"unknown","reason":"no_placement_record"},"consistency":"unverified","reach":{"status":"cannot","reason":"no_placement_record"},"tool":null},
{"member":"w-marker-off","type":"claude-code","project":"$S/t19-home/work/proj/.claude/worktrees/wt","terminal":"unknown","pane":"unknown:no_placement_record","container":"unknown:no_placement_record","activity":"unknown:no_placement_record","delivery":"off (unrecognized: no settings file found at $S/t19-home/work/proj/.claude/worktrees/wt/.claude/settings.local.json -- this project may not be registered)","pane_label":{"status":"unknown","reason":"no_placement_record"},"agent_key":{"status":"unknown","reason":"no_placement_record"},"cli_session":{"status":"unknown","reason":"no_placement_record"},"consistency":"unverified","reach":{"status":"cannot","reason":"no_placement_record"},"tool":null},
{"member":"w-resolved","type":"claude-code","project":"$S/t19-home/work/proj","terminal":"unknown","pane":"unknown:no_placement_record","container":"unknown:no_placement_record","activity":"unknown:no_placement_record","delivery":"off (unrecognized: no settings file found at $S/t19-home/work/proj/.claude/settings.local.json -- this project may not be registered)","pane_label":{"status":"unknown","reason":"no_placement_record"},"agent_key":{"status":"unknown","reason":"no_placement_record"},"cli_session":{"status":"unknown","reason":"no_placement_record"},"consistency":"unverified","reach":{"status":"cannot","reason":"no_placement_record"},"tool":null},
{"member":"w-worktree","type":"claude-code","project":"$S/t19-home/work/proj/.claude/worktrees/wt","terminal":"unknown","pane":"unknown:no_placement_record","container":"unknown:no_placement_record","activity":"unknown:no_placement_record","delivery":"off (unrecognized: no settings file found at $S/t19-home/work/proj/.claude/worktrees/wt/.claude/settings.local.json -- this project may not be registered)","pane_label":{"status":"unknown","reason":"no_placement_record"},"agent_key":{"status":"unknown","reason":"no_placement_record"},"cli_session":{"status":"unknown","reason":"no_placement_record"},"consistency":"unverified","reach":{"status":"cannot","reason":"no_placement_record"},"tool":null}
]
[exit 0]
```

### Finding 3: .chezmoiremove patterns in a scratch HOME (script $S/t19-chezmoi.sh)
```
# .chezmoiremove: .claude/skills/agmsg/**

$ find $S/t19-cz/home -mindepth 1 -printf %P %y\n
.claude d
.claude/skills d
.claude/skills/agmsg d
.claude/skills/agmsg/scripts d
.claude/skills/agmsg/scripts/send.sh l
.claude/skills/agmsg/scripts/lib d
.claude/skills/agmsg/scripts/lib/storage.sh l
.claude/skills/agmsg/SKILL.md l
.claude/skills/other d
.claude/skills/other/SKILL.md f
.claude/commands d
.claude/commands/agmsg.md l
[exit 0]

$ chezmoi --source $S/t19-cz/src --destination $S/t19-cz/home --config $S/t19-cz/cfg/chezmoi.yaml --persistent-state $S/t19-cz/cfg/state.boltdb --no-tty apply --dry-run --verbose
diff --git a/.claude/skills/agmsg b/.claude/skills/agmsg
deleted file mode 40775
index e69de29bb2d1d6434b8b29ae775ad8c2e48c5391..0000000000000000000000000000000000000000
--- a/.claude/skills/agmsg
+++ /dev/null
[exit 0]

$ chezmoi --source $S/t19-cz/src --destination $S/t19-cz/home --config $S/t19-cz/cfg/chezmoi.yaml --persistent-state $S/t19-cz/cfg/state.boltdb --no-tty apply --force
[exit 0]

$ find $S/t19-cz/home -mindepth 1 -printf %P %y\n
.claude d
.claude/skills d
.claude/skills/other d
.claude/skills/other/SKILL.md f
.claude/commands d
.claude/commands/agmsg.md l
[exit 0]
# .chezmoiremove: .claude/skills/agmsg

$ find $S/t19-cz/home -mindepth 1 -printf %P %y\n
.claude d
.claude/skills d
.claude/skills/agmsg d
.claude/skills/agmsg/scripts d
.claude/skills/agmsg/scripts/send.sh l
.claude/skills/agmsg/scripts/lib d
.claude/skills/agmsg/scripts/lib/storage.sh l
.claude/skills/agmsg/SKILL.md l
.claude/skills/other d
.claude/skills/other/SKILL.md f
.claude/commands d
.claude/commands/agmsg.md l
[exit 0]

$ chezmoi --source $S/t19-cz/src --destination $S/t19-cz/home --config $S/t19-cz/cfg/chezmoi.yaml --persistent-state $S/t19-cz/cfg/state.boltdb --no-tty apply --dry-run --verbose
diff --git a/.claude/skills/agmsg b/.claude/skills/agmsg
deleted file mode 40775
index e69de29bb2d1d6434b8b29ae775ad8c2e48c5391..0000000000000000000000000000000000000000
--- a/.claude/skills/agmsg
+++ /dev/null
[exit 0]

$ chezmoi --source $S/t19-cz/src --destination $S/t19-cz/home --config $S/t19-cz/cfg/chezmoi.yaml --persistent-state $S/t19-cz/cfg/state.boltdb --no-tty apply --force
[exit 0]

$ find $S/t19-cz/home -mindepth 1 -printf %P %y\n
.claude d
.claude/skills d
.claude/skills/other d
.claude/skills/other/SKILL.md f
.claude/commands d
.claude/commands/agmsg.md l
[exit 0]
```

### send.sh --body-file in 1.5.0 (scratch HOME)
```
$ send.sh t19 orch w-worktree --body-file body.txt
Sent to w-worktree in team t19
[exit 0]
$ inbox.sh t19 w-worktree
1 new message(s):

  [2026-09-29T00:32:02Z] orch: body with `backtick` and $(echo x)

[exit 0]
$ grep -n body-file send.sh (usage lines)
6:#   send.sh <team> <from> <to> --body-file <path> [--force]     # body read from a file
9:# --body-file matches poke.sh, for the same reason (#507) AND to close #1101: a caller
10:# who learned --body-file from poke used to have send take the literal string
11:# "--body-file" as the message and exit zero (the flag has different meanings on the two
15:# --, and is not --body-file/--body) is now REFUSED rather than sent, and a mistyped flag
$ grep -n body-file poke.sh
7:#   poke.sh <team> <name> --body-file <path>   # body read from a file (preferred)
11:# --body-file is the form the type templates teach, and the reason is #507's
65:USAGE="Usage: poke.sh <team> <name> [--retries N] [--retry-delay SECONDS] [--backoff fixed|exponential] --body-file <path> | --body - | <text>"
```

### Upstream issue states cited in the docs
```
$ for n in 149 151 1236 133 367 92 378 1101 1321 1322 1317 1307; do gh issue view $n -R fujibee/agmsg --json number,title,state,closedAt; done
149 OPEN - Codex bridge: no teardown on session end → orphaned bridge/app-server/watch-once that also blocks relaunch
151 OPEN - Codex monitor: enabling mode monitor doesn't start the bridge in a live session (needs restart)
1236 OPEN - codex monitor: a bridge that cannot deliver restarts forever while status reports it alive
133 CLOSED 2026-07-18T12:11:09Z delivery.sh set does not auto-re-register hooks after skill upgrade
367 CLOSED 2026-07-18T22:23:19Z monitorモードのSessionStart hookが.claude/worktreesのサブセッションにも発火し、永続watcherが親�
92 CLOSED 2026-06-14T23:11:52Z agmsg commands register a new project when invoked from a subdir, instead of using the CC session's real project
378 OPEN - send.sh: add a stdin/file input mode so message bodies survive shell quoting
1101 OPEN - send takes --body-file as the message body; poke takes it as a flag
1321 CLOSED 2026-09-19T04:59:26Z poke.sh can type over a live pane's own half-typed draft
1322 MERGED 2026-09-19T04:59:25Z fix(poke): refuse to type over a live draft, and cover the whole team on rearm
1317 OPEN - `terminal_peek` reads herdr's error from stdout, but herdr 0.9.1 writes it to stderr — every confirmed-gone pane comes back as rc 11 (un
1307 OPEN - herdr driver ignores the AGMSG_TERMINAL {cmd} template: no way for a layout-managing skill to place the pane itself
```

### Finding 1 E2E: origin/main vendored tree + live state -> real update_agmsg + real archive (script $S/t19-migrate.sh)
```
# legacy layout: marker=no VERSION=none

$ ls $S/t19-mig-home/.agents/skills/agmsg/scripts/lib
actas-lock.sh
identifier.sh
storage.sh
[exit 0]

$ bash -c cd '$S/t19-mig-home/.agents/skills/agmsg' && sha256sum teams/dotfiles/config.json db/messages.db run/watch.dotfiles.pid
02a017c76d22f66e39af5ae92d672f7fb440e420348899c5c4af89baccca4e05  teams/dotfiles/config.json
6817f4bde4405bc58b3afdcc25bd5f8dd8aea88dec62639bb8f184e03d076b12  db/messages.db
3b607b49bcec86ae6cfad6716f66bb5444ef30388922d49889e02227a266e726  run/watch.dotfiles.pid
[exit 0]

$ env -i HOME=$S/t19-mig-home PATH=/usr/local/bin:/usr/bin:/bin LANG=C.UTF-8 DOTFILES_SOURCE_DIR=/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c bash -c source '/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/scripts/update-agent-assets.sh'; update_agmsg

==> agmsg
agmsg: live state copied to $S/t19-mig-home/.agents/backups/agmsg-state-20260929T012739Z before install.sh --cmd agmsg --agent-type claude-code
[exit 0]
# after: marker=yes VERSION=1.5.0

$ bash -c cd '$S/t19-mig-home/.agents/skills/agmsg' && sha256sum teams/dotfiles/config.json db/messages.db run/watch.dotfiles.pid
02a017c76d22f66e39af5ae92d672f7fb440e420348899c5c4af89baccca4e05  teams/dotfiles/config.json
6817f4bde4405bc58b3afdcc25bd5f8dd8aea88dec62639bb8f184e03d076b12  db/messages.db
3b607b49bcec86ae6cfad6716f66bb5444ef30388922d49889e02227a266e726  run/watch.dotfiles.pid
[exit 0]

$ bash -c ls -d '$S/t19-mig-home'/.agents/backups/agmsg-state-*/*
$S/t19-mig-home/.agents/backups/agmsg-state-20260929T012739Z/agents
$S/t19-mig-home/.agents/backups/agmsg-state-20260929T012739Z/db
$S/t19-mig-home/.agents/backups/agmsg-state-20260929T012739Z/run
$S/t19-mig-home/.agents/backups/agmsg-state-20260929T012739Z/teams
[exit 0]

$ bash -c ls '$S/t19-mig-home/.agents/skills/agmsg/scripts/lib/identifier.sh' '$S/t19-mig-home/.agents/skills/agmsg'/.trash/*/lib/identifier.sh 2>&1 | sed 's#$S/t19-mig-home#<HOME>#'
ls: '<HOME>/.agents/skills/agmsg/scripts/lib/identifier.sh' にアクセスできません: そのようなファイルやディレクトリはありません
ls: '<HOME>/.agents/skills/agmsg/.trash/*/lib/identifier.sh' にアクセスできません: そのようなファイルやディレクトリはありません
[exit 0]

## agmsg-dispatch (origin/main) against the upgraded skill

$ env -i HOME=$S/t19-mig-home PATH=/usr/local/bin:/usr/bin:/bin LANG=C.UTF-8 DOTFILES_SOURCE_DIR=/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c bash $S/t19-mig-home/agmsg-dispatch.origin-main dotfiles orch worker w1:p1 hello
$S/t19-mig-home/agmsg-dispatch.origin-main: line 25: $S/t19-mig-home/.agents/skills/agmsg/scripts/lib/identifier.sh: No such file or directory
[exit 1]

## second update_agmsg run (VERSION == pin, marker present) is a no-op

$ env -i HOME=$S/t19-mig-home PATH=/usr/local/bin:/usr/bin:/bin LANG=C.UTF-8 DOTFILES_SOURCE_DIR=/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c bash -c source '/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/scripts/update-agent-assets.sh'; update_agmsg

==> agmsg
[exit 0]
```

### Finding 1 E2E after the review fix: fresh HOME and legacy dir without messages.db (script $S/t19-fresh.sh)
```

## case: fresh (skill dir present: no; db/messages.db: no)

$ env -i HOME=$S/t19-fresh-home PATH=/usr/local/bin:/usr/bin:/bin LANG=C.UTF-8 DOTFILES_SOURCE_DIR=/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c bash -c source '/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/scripts/update-agent-assets.sh'; update_agmsg

==> agmsg
[exit 0]
# after: marker=yes VERSION=1.5.0 messages.db=yes

## case: legacy-keep (skill dir present: yes; db/messages.db: no)

$ env -i HOME=$S/t19-legacy-keep-home PATH=/usr/local/bin:/usr/bin:/bin LANG=C.UTF-8 DOTFILES_SOURCE_DIR=/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c bash -c source '/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/scripts/update-agent-assets.sh'; update_agmsg

==> agmsg
agmsg: live state copied to $S/t19-legacy-keep-home/.agents/backups/agmsg-state-20260929T012717Z before install.sh --cmd agmsg --agent-type claude-code
[exit 0]
# after: marker=yes VERSION=1.5.0 messages.db=yes
```

### agmsg-dispatch E2E against a real 1.5.0 install (fake herdr)
```
# agmsg-dispatch (this branch) against the real upstream 1.5.0 install in the scratch HOME $S/t19-home; herdr is a fake that marks unread messages read on wake
$ cat $HOME/.agents/skills/agmsg/VERSION
1.5.0
$ command ls .../scripts/lib/validate.sh .../scripts/lib/storage.sh; command ls .../scripts/lib/identifier.sh
$S/t19-home/.agents/skills/agmsg/scripts/lib/storage.sh
$S/t19-home/.agents/skills/agmsg/scripts/lib/validate.sh
ls: '$S/t19-home/.agents/skills/agmsg/scripts/lib/identifier.sh' にアクセスできません: そのようなファイルやディレクトリはありません
$ agmsg-dispatch t19 orch w-worktree w1:p1 'AGMSG-TASK v1 task_id=e2e'
[exit 0]
$ fake herdr calls
herdr pane run w1:p1 agmsg: new message 2 for w-worktree — run ~/.agents/skills/agmsg/scripts/inbox.sh t19 w-worktree
$ sqlite3 messages.db 'select id,team,from_agent,to_agent,body,read_at from messages'
1|t19|orch|w-worktree|body with `backtick` and $(echo x)|2026-09-29T00:32:02Z
2|t19|orch|w-worktree|AGMSG-TASK v1 task_id=e2e|read
$ agmsg-dispatch t19 "o'brien" w-worktree w1:p1 x   # SQL-unsafe sender
Usage: agmsg-dispatch <team> <from> <to> <pane_id> <message...> (identifiers must match ^[a-z0-9][a-z0-9_-]{0,63}$)
[exit 1]
```

### Mutation baseline: installer tests against the pre-round-2 script (HEAD f7c6d60 at the time)
```
update-agent-assets.sh == HEAD f7c6d60 (pre-change)
$ python3 -m unittest tests.unit.test_runtime_health -k agmsg
...FEFFF.
======================================================================
ERROR: test_agmsg_migration_reports_an_installer_that_mutates_live_state (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_migration_reports_an_installer_that_mutates_live_state)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_runtime_health.py", line 923, in test_agmsg_migration_reports_an_installer_that_mutates_live_state
    backup = next((home / ".agents/backups").glob("agmsg-state-*"))
StopIteration

======================================================================
FAIL: test_agmsg_migrates_marker_less_legacy_dir_without_losing_live_state (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_migrates_marker_less_legacy_dir_without_losing_live_state)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_runtime_health.py", line 865, in test_agmsg_migrates_marker_less_legacy_dir_without_losing_live_state
    self.assertEqual(1, len(backups))
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
AssertionError: 1 != 0

======================================================================
FAIL: test_agmsg_refuses_to_install_when_the_state_snapshot_is_empty (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_refuses_to_install_when_the_state_snapshot_is_empty)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_runtime_health.py", line 957, in test_agmsg_refuses_to_install_when_the_state_snapshot_is_empty
    self.assertIn("hashed fewer live-state files than exist", output)
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'hashed fewer live-state files than exist' not found in '\n==> agmsg\nagmsg checksum mismatch for https://github.com/fujibee/agmsg/archive/c487be269c1973aeb01ca831806eb3f65ff3366d.tar.gz.\nagmsg installer failed; see stderr above for details.\n'

======================================================================
FAIL: test_agmsg_refuses_to_install_without_tar (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_refuses_to_install_without_tar)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_runtime_health.py", line 986, in test_agmsg_refuses_to_install_without_tar
    self.assertIn("agmsg: tar not found; nothing was installed", output)
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'agmsg: tar not found; nothing was installed' not found in '\n==> agmsg\nscripts/update-agent-assets.sh: 行 940: tar: コマンドが見つかりません\nagmsg extraction failed for https://github.com/fujibee/agmsg/archive/c487be269c1973aeb01ca831806eb3f65ff3366d.tar.gz\nagmsg installer failed; see stderr above for details.\n'

======================================================================
FAIL: test_agmsg_update_aborts_when_install_corrupts_live_state (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_update_aborts_when_install_corrupts_live_state)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_runtime_health.py", line 893, in test_agmsg_update_aborts_when_install_corrupts_live_state
    self.assertIn("changed during install.sh --update", result.stdout + result.stderr)
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'changed during install.sh --update' not found in '\n==> agmsg\nagmsg update touched live runtime state under teams/db/run; aborting\nagmsg installer failed; see stderr above for details.\n'

----------------------------------------------------------------------
Ran 9 tests in 0.808s

FAILED (failures=4, errors=1)
```

### Mutation baseline: validator tests against the pre-change validator (54f25df)
```
validate-agent-assets.py == HEAD 54f25df (pre-change)
$ python3 -m unittest tests.unit.test_validate_agent_assets -k agmsg
.FFFFEEEEEEEEE.
======================================================================
ERROR: test_agmsg_ownership_accepts_the_installer_layout (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_accepts_the_installer_layout)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_validate_agent_assets.py", line 418, in test_agmsg_ownership_accepts_the_installer_layout
    self.module.validate_agmsg_is_installer_owned()
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: module 'validate_agent_assets' has no attribute 'validate_agmsg_is_installer_owned'

======================================================================
ERROR: test_agmsg_ownership_rejects_a_managed_claude_command (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_rejects_a_managed_claude_command) (name='symlink_agmsg.md.tmpl')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_validate_agent_assets.py", line 434, in test_agmsg_ownership_rejects_a_managed_claude_command
    self.assert_agmsg_ownership_rejected(f"{path} must not exist")
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_validate_agent_assets.py", line 411, in assert_agmsg_ownership_rejected
    self.module.validate_agmsg_is_installer_owned()
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: module 'validate_agent_assets' has no attribute 'validate_agmsg_is_installer_owned'

======================================================================
ERROR: test_agmsg_ownership_rejects_a_managed_claude_command (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_rejects_a_managed_claude_command) (name='agmsg.md')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_validate_agent_assets.py", line 434, in test_agmsg_ownership_rejects_a_managed_claude_command
    self.assert_agmsg_ownership_rejected(f"{path} must not exist")
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_validate_agent_assets.py", line 411, in assert_agmsg_ownership_rejected
    self.module.validate_agmsg_is_installer_owned()
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: module 'validate_agent_assets' has no attribute 'validate_agmsg_is_installer_owned'

======================================================================
ERROR: test_agmsg_ownership_rejects_a_vendored_skill_copy (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_rejects_a_vendored_skill_copy) (vendored='home/dot_agents/skills/agmsg')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_validate_agent_assets.py", line 425, in test_agmsg_ownership_rejects_a_vendored_skill_copy
    self.assert_agmsg_ownership_rejected(f"{vendored} must not exist")
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_validate_agent_assets.py", line 411, in assert_agmsg_ownership_rejected
    self.module.validate_agmsg_is_installer_owned()
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: module 'validate_agent_assets' has no attribute 'validate_agmsg_is_installer_owned'

======================================================================
ERROR: test_agmsg_ownership_rejects_a_vendored_skill_copy (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_rejects_a_vendored_skill_copy) (vendored='home/dot_claude/skills/agmsg')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_validate_agent_assets.py", line 425, in test_agmsg_ownership_rejects_a_vendored_skill_copy
    self.assert_agmsg_ownership_rejected(f"{vendored} must not exist")
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_validate_agent_assets.py", line 411, in assert_agmsg_ownership_rejected
    self.module.validate_agmsg_is_installer_owned()
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: module 'validate_agent_assets' has no attribute 'validate_agmsg_is_installer_owned'

======================================================================
ERROR: test_agmsg_ownership_rejects_removing_installer_owned_paths (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_rejects_removing_installer_owned_paths) (pattern='.agents/skills/agmsg')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_validate_agent_assets.py", line 448, in test_agmsg_ownership_rejects_removing_installer_owned_paths
    self.assert_agmsg_ownership_rejected(f"entry {pattern!r} would remove")
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_validate_agent_assets.py", line 411, in assert_agmsg_ownership_rejected
    self.module.validate_agmsg_is_installer_owned()
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: module 'validate_agent_assets' has no attribute 'validate_agmsg_is_installer_owned'

======================================================================
ERROR: test_agmsg_ownership_rejects_removing_installer_owned_paths (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_rejects_removing_installer_owned_paths) (pattern='.agents/skills/agmsg/**')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_validate_agent_assets.py", line 448, in test_agmsg_ownership_rejects_removing_installer_owned_paths
    self.assert_agmsg_ownership_rejected(f"entry {pattern!r} would remove")
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_validate_agent_assets.py", line 411, in assert_agmsg_ownership_rejected
    self.module.validate_agmsg_is_installer_owned()
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: module 'validate_agent_assets' has no attribute 'validate_agmsg_is_installer_owned'

======================================================================
ERROR: test_agmsg_ownership_rejects_removing_installer_owned_paths (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_rejects_removing_installer_owned_paths) (pattern='.claude/commands/agmsg.md')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_validate_agent_assets.py", line 448, in test_agmsg_ownership_rejects_removing_installer_owned_paths
    self.assert_agmsg_ownership_rejected(f"entry {pattern!r} would remove")
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_validate_agent_assets.py", line 411, in assert_agmsg_ownership_rejected
    self.module.validate_agmsg_is_installer_owned()
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: module 'validate_agent_assets' has no attribute 'validate_agmsg_is_installer_owned'

======================================================================
ERROR: test_agmsg_ownership_requires_retiring_the_symlink_farm (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_requires_retiring_the_symlink_farm)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_validate_agent_assets.py", line 440, in test_agmsg_ownership_requires_retiring_the_symlink_farm
    self.assert_agmsg_ownership_rejected("must retire .claude/skills/agmsg/**")
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_validate_agent_assets.py", line 411, in assert_agmsg_ownership_rejected
    self.module.validate_agmsg_is_installer_owned()
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: module 'validate_agent_assets' has no attribute 'validate_agmsg_is_installer_owned'

======================================================================
FAIL: test_agmsg_installer_requires_the_full_tag_commit (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_installer_requires_the_full_tag_commit) (changes={'ref_commit': None})
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_validate_agent_assets.py", line 393, in test_agmsg_installer_requires_the_full_tag_commit
    self.assertIn("ref_commit", self.assert_agmsg_asset_rejected(**changes))
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'ref_commit' not found in "ERROR: assets.agmsg has an unknown source: 'agmsg-installer'\n"

======================================================================
FAIL: test_agmsg_installer_requires_the_full_tag_commit (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_installer_requires_the_full_tag_commit) (changes={'ref_commit': 'c487be2'})
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_validate_agent_assets.py", line 393, in test_agmsg_installer_requires_the_full_tag_commit
    self.assertIn("ref_commit", self.assert_agmsg_asset_rejected(**changes))
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'ref_commit' not found in "ERROR: assets.agmsg has an unknown source: 'agmsg-installer'\n"

======================================================================
FAIL: test_agmsg_installer_requires_the_npm_bootstrap_integrity (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_installer_requires_the_npm_bootstrap_integrity) (changes={'bootstrap_integrity': None})
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_validate_agent_assets.py", line 401, in test_agmsg_installer_requires_the_npm_bootstrap_integrity
    self.assertIn(
    ~~~~~~~~~~~~~^
        "bootstrap_integrity", self.assert_agmsg_asset_rejected(**changes)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
AssertionError: 'bootstrap_integrity' not found in "ERROR: assets.agmsg has an unknown source: 'agmsg-installer'\n"

======================================================================
FAIL: test_agmsg_installer_requires_the_npm_bootstrap_integrity (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_installer_requires_the_npm_bootstrap_integrity) (changes={'bootstrap_integrity': 'sha256-not-an-npm-integrity-string'})
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_validate_agent_assets.py", line 401, in test_agmsg_installer_requires_the_npm_bootstrap_integrity
    self.assertIn(
    ~~~~~~~~~~~~~^
        "bootstrap_integrity", self.assert_agmsg_asset_rejected(**changes)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
AssertionError: 'bootstrap_integrity' not found in "ERROR: assets.agmsg has an unknown source: 'agmsg-installer'\n"

----------------------------------------------------------------------
Ran 9 tests in 0.060s

FAILED (failures=4, errors=9)
```

### Mutation baseline: chezmoiremove test with the agmsg entry removed
```
$ (baseline: home/.chezmoiremove without the agmsg entry) python3 -m unittest tests.unit.test_chezmoiremove_agmsg
    self.assertFalse(farm.exists() or farm.is_symlink())
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: True is not false

----------------------------------------------------------------------
Ran 1 test in 0.009s

FAILED (failures=1)
```

### Mutation baseline: agmsg-dispatch tests against origin/main's dispatch
```
agmsg-dispatch == origin/main b008d84 (pre-change)
$ python3 -m unittest tests.unit.test_agmsg_dispatch
FF.F.FFFFFFF
======================================================================
FAIL: test_default_store_uses_shared_helper (tests.unit.test_agmsg_dispatch.AgmsgDispatchTest.test_default_store_uses_shared_helper)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_agmsg_dispatch.py", line 147, in test_default_store_uses_shared_helper
    self.assertEqual(result.returncode, 0, result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 1 != 0 : /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/home/dot_local/bin/common/executable_agmsg-dispatch: 行 25: /tmp/tmp9cfq53b9/.agents/skills/agmsg/scripts/lib/identifier.sh: そのようなファイルやディレクトリはありません


======================================================================
FAIL: test_idle_wakes_once_and_reads (tests.unit.test_agmsg_dispatch.AgmsgDispatchTest.test_idle_wakes_once_and_reads)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_agmsg_dispatch.py", line 110, in test_idle_wakes_once_and_reads
    self.assertEqual(result.returncode, 0, result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 1 != 0 : /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/home/dot_local/bin/common/executable_agmsg-dispatch: 行 25: /tmp/tmprbz2t4_p/.agents/skills/agmsg/scripts/lib/identifier.sh: そのようなファイルやディレクトリはありません


======================================================================
FAIL: test_missing_pane_inserts_nothing (tests.unit.test_agmsg_dispatch.AgmsgDispatchTest.test_missing_pane_inserts_nothing)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_agmsg_dispatch.py", line 181, in test_missing_pane_inserts_nothing
    self.assertIn("pane", result.stderr)
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'pane' not found in '/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/home/dot_local/bin/common/executable_agmsg-dispatch: 行 25: /tmp/tmpzwnsykec/.agents/skills/agmsg/scripts/lib/identifier.sh: そのようなファイルやディレクトリはありません\n'

======================================================================
FAIL: test_retry_does_not_wake_newly_working_pane (tests.unit.test_agmsg_dispatch.AgmsgDispatchTest.test_retry_does_not_wake_newly_working_pane)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_agmsg_dispatch.py", line 167, in test_retry_does_not_wake_newly_working_pane
    self.assertEqual(len(self.calls.read_text().splitlines()), 1)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 0 != 1

======================================================================
FAIL: test_timeout_is_one_shared_budget (tests.unit.test_agmsg_dispatch.AgmsgDispatchTest.test_timeout_is_one_shared_budget)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_agmsg_dispatch.py", line 175, in test_timeout_is_one_shared_budget
    self.assertIn("sent message 1;", result.stderr)
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'sent message 1;' not found in '/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/home/dot_local/bin/common/executable_agmsg-dispatch: 行 25: /tmp/tmphbhdqs53/.agents/skills/agmsg/scripts/lib/identifier.sh: そのようなファイルやディレクトリはありません\n'

======================================================================
FAIL: test_unread_retries_once_then_fails (tests.unit.test_agmsg_dispatch.AgmsgDispatchTest.test_unread_retries_once_then_fails)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_agmsg_dispatch.py", line 129, in test_unread_retries_once_then_fails
    self.assertIn("unread", result.stderr)
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'unread' not found in '/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/home/dot_local/bin/common/executable_agmsg-dispatch: 行 25: /tmp/tmpcbt23afk/.agents/skills/agmsg/scripts/lib/identifier.sh: そのようなファイルやディレクトリはありません\n'

======================================================================
FAIL: test_wake_failure_identifies_sent_message (tests.unit.test_agmsg_dispatch.AgmsgDispatchTest.test_wake_failure_identifies_sent_message)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_agmsg_dispatch.py", line 189, in test_wake_failure_identifies_sent_message
    self.assertIn("sent message 1;", result.stderr)
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'sent message 1;' not found in '/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/home/dot_local/bin/common/executable_agmsg-dispatch: 行 25: /tmp/tmpy0d36k08/.agents/skills/agmsg/scripts/lib/identifier.sh: そのようなファイルやディレクトリはありません\n'

======================================================================
FAIL: test_worker_becoming_idle_after_send_is_woken (tests.unit.test_agmsg_dispatch.AgmsgDispatchTest.test_worker_becoming_idle_after_send_is_woken)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_agmsg_dispatch.py", line 160, in test_worker_becoming_idle_after_send_is_woken
    self.assertEqual(result.returncode, 0, result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 1 != 0 : /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/home/dot_local/bin/common/executable_agmsg-dispatch: 行 25: /tmp/tmp5sig6y4e/.agents/skills/agmsg/scripts/lib/identifier.sh: そのようなファイルやディレクトリはありません


======================================================================
FAIL: test_working_does_not_wake (tests.unit.test_agmsg_dispatch.AgmsgDispatchTest.test_working_does_not_wake)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_agmsg_dispatch.py", line 122, in test_working_does_not_wake
    self.assertEqual(result.returncode, 0, result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 1 != 0 : /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/home/dot_local/bin/common/executable_agmsg-dispatch: 行 25: /tmp/tmpt85mnhoh/.agents/skills/agmsg/scripts/lib/identifier.sh: そのようなファイルやディレクトリはありません


======================================================================
FAIL: test_working_unread_never_wakes (tests.unit.test_agmsg_dispatch.AgmsgDispatchTest.test_working_unread_never_wakes)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_agmsg_dispatch.py", line 137, in test_working_unread_never_wakes
    self.assertIn("unread", result.stderr)
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'unread' not found in '/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/home/dot_local/bin/common/executable_agmsg-dispatch: 行 25: /tmp/tmp9q655hjz/.agents/skills/agmsg/scripts/lib/identifier.sh: そのようなファイルやディレクトリはありません\n'

----------------------------------------------------------------------
Ran 12 tests in 0.165s

FAILED (failures=10)
```

### Mutation baseline: guard tests against the pre-review guard (e0674d1)
```
update-agent-assets.sh == HEAD e0674d1 (guard before the review fix)
$ python3 -m unittest tests.unit.test_runtime_health -k agmsg
F..FFF..FF.
======================================================================
FAIL: test_agmsg_accepts_a_store_the_installer_creates_and_notes_run_changes (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_accepts_a_store_the_installer_creates_and_notes_run_changes)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_runtime_health.py", line 969, in test_agmsg_accepts_a_store_the_installer_creates_and_notes_run_changes
    self.assertNotIn("installer failed", output)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'installer failed' unexpectedly found in '\n==> agmsg\nagmsg: live state copied to /tmp/runtime-health-test-o608xqzr/agmsg-home/.agents/backups/agmsg-state-20260929T012655Z before install.sh --cmd agmsg --agent-type claude-code\nagmsg: live state under teams/, run/ or db/messages.db changed during install.sh --cmd agmsg --agent-type claude-code; pre-install state copy: /tmp/runtime-health-test-o608xqzr/agmsg-home/.agents/backups/agmsg-state-20260929T012655Z\nagmsg installer failed (installed: none); see the reason above.\n'

======================================================================
FAIL: test_agmsg_fresh_install_populates_skill_and_records_manifest (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_fresh_install_populates_skill_and_records_manifest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_runtime_health.py", line 766, in test_agmsg_fresh_install_populates_skill_and_records_manifest
    self.assertNotIn("installer failed", result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'installer failed' unexpectedly found in '\n==> agmsg\nagmsg: live state under teams/, run/ or db/messages.db changed during install.sh --cmd agmsg --agent-type claude-code; pre-install state copy: none\nagmsg installer failed (installed: none); see the reason above.\n'

======================================================================
FAIL: test_agmsg_migrates_marker_less_legacy_dir_without_losing_live_state (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_migrates_marker_less_legacy_dir_without_losing_live_state)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_runtime_health.py", line 866, in test_agmsg_migrates_marker_less_legacy_dir_without_losing_live_state
    self.assertNotIn("installer failed", result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'installer failed' unexpectedly found in '\n==> agmsg\nagmsg: live state copied to /tmp/runtime-health-test-rlaectqw/agmsg-home/.agents/backups/agmsg-state-20260929T012655Z before install.sh --cmd agmsg --agent-type claude-code\nagmsg: live state under teams/, run/ or db/messages.db changed during install.sh --cmd agmsg --agent-type claude-code; pre-install state copy: /tmp/runtime-health-test-rlaectqw/agmsg-home/.agents/backups/agmsg-state-20260929T012655Z\nagmsg installer failed (installed: none); see the reason above.\n'

======================================================================
FAIL: test_agmsg_migration_reports_an_installer_that_mutates_live_state (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_migration_reports_an_installer_that_mutates_live_state)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_runtime_health.py", line 935, in test_agmsg_migration_reports_an_installer_that_mutates_live_state
    self.assertIn(
    ~~~~~~~~~~~~~^
        "install.sh --cmd agmsg --agent-type claude-code changed or removed "
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        f"existing live state (the installer or a concurrent writer); pre-install state copy: {backup}",
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        output,
        ^^^^^^^
    )
    ^
AssertionError: 'install.sh --cmd agmsg --agent-type claude-code changed or removed existing live state (the installer or a concurrent writer); pre-install state copy: /tmp/runtime-health-test-qi9m9r77/agmsg-home/.agents/backups/agmsg-state-20260929T012655Z' not found in '\n==> agmsg\nagmsg: live state copied to /tmp/runtime-health-test-qi9m9r77/agmsg-home/.agents/backups/agmsg-state-20260929T012655Z before install.sh --cmd agmsg --agent-type claude-code\nagmsg: live state under teams/, run/ or db/messages.db changed during install.sh --cmd agmsg --agent-type claude-code; pre-install state copy: /tmp/runtime-health-test-qi9m9r77/agmsg-home/.agents/backups/agmsg-state-20260929T012655Z\nagmsg installer failed (installed: none); see the reason above.\n'

======================================================================
FAIL: test_agmsg_reports_an_installer_that_leaves_the_wrong_version (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_reports_an_installer_that_leaves_the_wrong_version)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_runtime_health.py", line 990, in test_agmsg_reports_an_installer_that_leaves_the_wrong_version
    self.assertIn(
    ~~~~~~~~~~~~~^
        "agmsg: install.sh --cmd agmsg --agent-type claude-code left VERSION 9.9.9 (want 1.5.0)",
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        output,
        ^^^^^^^
    )
    ^
AssertionError: 'agmsg: install.sh --cmd agmsg --agent-type claude-code left VERSION 9.9.9 (want 1.5.0)' not found in '\n==> agmsg\nagmsg: live state under teams/, run/ or db/messages.db changed during install.sh --cmd agmsg --agent-type claude-code; pre-install state copy: none\nagmsg installer failed (installed: none); see the reason above.\n'

======================================================================
FAIL: test_agmsg_update_aborts_when_install_corrupts_live_state (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_update_aborts_when_install_corrupts_live_state)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_runtime_health.py", line 903, in test_agmsg_update_aborts_when_install_corrupts_live_state
    self.assertIn("install.sh --update --cmd agmsg --agent-type claude-code changed or removed existing live state", output)
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'install.sh --update --cmd agmsg --agent-type claude-code changed or removed existing live state' not found in '\n==> agmsg\nagmsg: live state copied to /tmp/runtime-health-test-r95aswd9/agmsg-home/.agents/backups/agmsg-state-20260929T012656Z before install.sh --update --cmd agmsg --agent-type claude-code\nagmsg: live state under teams/, run/ or db/messages.db changed during install.sh --update --cmd agmsg --agent-type claude-code; pre-install state copy: /tmp/runtime-health-test-r95aswd9/agmsg-home/.agents/backups/agmsg-state-20260929T012656Z\nagmsg installer failed (installed: 1.0.0); see the reason above.\n'

----------------------------------------------------------------------
Ran 11 tests in 0.753s

FAILED (failures=6)
```

### Mutation baseline: doctor test against the pre-change check-agent-runtime.py (cca3e6b)
```
check-agent-runtime.py == HEAD cca3e6b (pre-change)
$ python3 -m unittest tests.unit.test_check_agent_runtime -k installer_owned_agmsg
F
======================================================================
FAIL: test_installer_owned_agmsg_skill_and_backups_are_not_orphans (tests.unit.test_check_agent_runtime.CheckAgentRuntimeTest.test_installer_owned_agmsg_skill_and_backups_are_not_orphans)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_check_agent_runtime.py", line 346, in test_installer_owned_agmsg_skill_and_backups_are_not_orphans
    self.assertEqual(
    ~~~~~~~~~~~~~~~~^
        [f"WARN: orphaned agent asset: {agents / 'orphan-root'}; manual review required"],
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        warnings,
        ^^^^^^^^^
    )
    ^
AssertionError: Lists differ: ['WAR[72 chars]ents/orphan-root; manual review required'] != ['WAR[72 chars]ents/backups; manual review required', 'WARN: [243 chars]msg']

First differing element 0:
'WARN[49 chars]test-r1lqfrmi/home/.agents/orphan-root; manual review required'
'WARN[49 chars]test-r1lqfrmi/home/.agents/backups; manual review required'

Second list contains 2 additional elements.
First extra element 1:
'WARN: orphaned agent asset: /tmp/check-agent-runtime-test-r1lqfrmi/home/.agents/orphan-root; manual review required'

  ['WARN: orphaned agent asset: '
+  '/tmp/check-agent-runtime-test-r1lqfrmi/home/.agents/backups; manual review '
+  'required',
+  'WARN: orphaned agent asset: '
   '/tmp/check-agent-runtime-test-r1lqfrmi/home/.agents/orphan-root; manual '
-  'review required']
?                   ^

+  'review required',
?                   ^

+  'WARN: stale agent asset: '
+  '/tmp/check-agent-runtime-test-r1lqfrmi/home/.agents/skills/agmsg; suggested: '
+  'remove-agent-asset update_agmsg']

----------------------------------------------------------------------
Ran 1 test in 0.007s

FAILED (failures=1)
```

### make validate-agent-assets (final tree)
```
$ make validate-agent-assets
uv run --with pyyaml scripts/validate-agent-assets.py
agent asset validation ok
exit=0
```

### make unit-test (final tree; head and tail)
```
$ make unit-test
uv run python -m unittest discover -s tests/unit -v
test_bounded_scan_finishes_under_wall_limit (test_agent_session_staleness.AgentSessionStalenessTest.test_bounded_scan_finishes_under_wall_limit) ... ok
...

----------------------------------------------------------------------
Ran 533 tests in 88.499s

OK (skipped=1)
exit=0
```

### shellcheck / shfmt / CI ShellCheck step (final tree)
```
$ shellcheck -x home/dot_local/bin/common/executable_herdr-agents home/dot_local/bin/common/executable_agmsg-dispatch scripts/update-agent-assets.sh scripts/check-tools.sh
exit=0
$ shfmt --indent 4 --space-redirects --diff home/dot_local/bin/common/executable_herdr-agents home/dot_local/bin/common/executable_agmsg-dispatch scripts/update-agent-assets.sh scripts/check-tools.sh
exit=0
$ git ls-files -z 'setup.sh' 'install/*.sh' 'install/**/*.sh' 'scripts/*.sh' | xargs -0 shellcheck -x   # the CI ShellCheck step
exit=0
```

### CI on 7bd66ac (failed: SC2015 in CI's shellcheck)
```
$ gh pr checks 184
test (ubuntu-latest, client)	fail	29s	https://github.com/mryfmo/dotfiles/actions/runs/36506550479/job/109209186485	
CodeRabbit	pass	0		Review skipped: manual review required for this OSS repository
build	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/36506550491/job/109209155999	
build (client)	pass	3s	https://github.com/mryfmo/dotfiles/actions/runs/36506550588/job/109209156696	
build (server)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/36506550588/job/109209156449	
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/36506550479/job/109209155808	
private-bootstrap (macos-14, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/36506550696/job/109209156894	
private-bootstrap (ubuntu-latest, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/36506550696/job/109209156677	
private-bootstrap (ubuntu-latest, server)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/36506550696/job/109209156965	
test (macos-14, client)	fail	1m32s	https://github.com/mryfmo/dotfiles/actions/runs/36506550479/job/109209186418	
public-bootstrap (ubuntu-latest, client)	pass	9m20s	https://github.com/mryfmo/dotfiles/actions/runs/36506550696/job/109209156885	
public-bootstrap (ubuntu-latest, server)	pass	6m39s	https://github.com/mryfmo/dotfiles/actions/runs/36506550696/job/109209157037	
validate	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/36506550558/job/109209156346	
nix	skipping	0	https://github.com/mryfmo/dotfiles/actions/runs/36506550479/job/109209187706	
public-bootstrap (macos-14, client)	pass	8m52s	https://github.com/mryfmo/dotfiles/actions/runs/36506550696/job/109209156838	
test (ubuntu-latest, server)	fail	44s	https://github.com/mryfmo/dotfiles/actions/runs/36506550479/job/109209186412	
exit=1
$ gh pr view 184 --json headRefOid -q .headRefOid
7bd66acb39b56c7cf968a26e2608bb35c77c0835
```

### CI on e0674d1 (after the SC2015 fix)
```
$ gh pr checks 184
CodeRabbit	pass	0		Review skipped: manual review required for this OSS repository
build	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/36507430318/job/109211905782	
build (client)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/36507430277/job/109211905677	
build (server)	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/36507430277/job/109211905975	
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/36507430214/job/109211905312	
private-bootstrap (macos-14, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/36507430300/job/109211906903	
private-bootstrap (ubuntu-latest, client)	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/36507430300/job/109211906750	
private-bootstrap (ubuntu-latest, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/36507430300/job/109211907003	
public-bootstrap (macos-14, client)	pass	8m37s	https://github.com/mryfmo/dotfiles/actions/runs/36507430300/job/109211906900	
public-bootstrap (ubuntu-latest, client)	pass	9m55s	https://github.com/mryfmo/dotfiles/actions/runs/36507430300/job/109211907001	
public-bootstrap (ubuntu-latest, server)	pass	7m16s	https://github.com/mryfmo/dotfiles/actions/runs/36507430300/job/109211906890	
test (macos-14, client)	pass	3m24s	https://github.com/mryfmo/dotfiles/actions/runs/36507430214/job/109211937800	
validate	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/36507430273/job/109211905699	
nix	skipping	0	https://github.com/mryfmo/dotfiles/actions/runs/36507430214/job/109211938910	
test (ubuntu-latest, client)	pass	6m26s	https://github.com/mryfmo/dotfiles/actions/runs/36507430214/job/109211937834	
test (ubuntu-latest, server)	pass	3m2s	https://github.com/mryfmo/dotfiles/actions/runs/36507430214/job/109211937877	
exit=0
$ gh pr view 184 --json headRefOid -q .headRefOid
e0674d133609c6c418a45d83ed1575cbd4b949b5
```

### CompactionDB
```
$ python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "agmsg is installed by the upstream installer at a pinned tag verified by commit sha, recorded in the asset manifest; the vendored snapshot and agmsg-dispatch are retired; wake uses upstream poke, health uses team/doctor/peek. T19 revision 3 refinement (operator ruling 2026-09-29, option A): the pin is verified by the sha256 of the source archive of ref_commit (accepted change request), install.sh --update runs only when the .agmsg marker exists, live state is backed up and must stay byte-identical, worker identities register at their worktree with AGMSG_RESOLVE_PROJECT=0, and agmsg-dispatch (on upstream lib/validate.sh) stays the wake path for herdr-agents workers until seating writes placement records; poke.sh is for spawn-seated members only."
8e20faa2-1754-42ab-a816-07663434e095
```

### Round 2 — independent review (subagent, separate context; its report on the pre-fix head)

The reviewer's report, condensed to its findings and verdict (its full method notes are summarized in the report file):

```
Findings (most severe first)
P1 high  scripts/update-agent-assets.sh:933/:1014  fresh install (and a marker-less legacy dir without db/messages.db) always reports failure: agmsg_state_snapshot includes db/messages.db, upstream install.sh creates it via init-db.sh, so before/after differ; the agmsg_fixture install.sh never creates it, hiding the defect.
P2 med-high  scripts/update-agent-assets.sh:932/:1014  strict set-equality over run/ misfires with live seats (watcher pidfiles, proj markers GC, --update's own `remote.sh sync restart` pidfiles under SKILL_DIR/run); a file vanishing between find and sha256sum fails the after-snapshot with a misleading message.
P2 high  scripts/check-agent-runtime.py:38  ~/.agents/backups reported "orphaned agent asset"; ~/.agents/skills/agmsg reported "stale agent asset ... suggested: remove-agent-asset update_agmsg" (would delete the live skill).
P2 med  README.md:405, SKILL.md:123, rules:14, agmsg-dispatch header  "poke.sh exits 1 for every herdr-agents worker" only until the worker acts: send.sh:77 / inbox.sh:23 agmsg_self_name_on_action records the acting pane's placement (#1109).
P3 high  README.md:420, SKILL.md:123  exit-13 wording true only for the claude-code->claude-code branch.
P3 high  SKILL.md:123  placement filename: 1.5.0 also uses id-keyed spawn.<key>.
P3 high  SKILL.md:123 vs :188, README.md:398 vs :412  --body-file rule vs positional agmsg-dispatch contradiction.
P3 high  README.md:351  "Every failure names what changed and where the copy is" not true.
P3 high  scripts/update-agent-assets.sh:937  names with \ or newline (escaped with a leading \) and unreadable subtrees (find errors silenced) break or undercount the snapshot.
P3 med  scripts/validate-agent-assets.py:575-586  ownership targets omit .agmsg/VERSION/SKILL.md/scripts; attribute-prefixed vendored copies evade the exact-path check.
P3 med  tests  dispatch tests use stub libs; pin/ref tests accept any SystemExit; no VERSION != pin test.
Checked and correct: --update path (1.4.0 -> 1.5.0), mode choice, errexit handling, symlink replacement by mv -f, macOS primitives, agmsg-dispatch SQL guard and agmsg_db_path, upstream facts cited in the docs, chezmoiremove/manifest/validator consistency.
Verdict: incorrect
```

Disposition: every finding is resolved in 5623e83 (pre-rebase cca3e6b) and 55faae0, with one crit record each in `.orchestration/validation/dot-agmsg-upstream-sync-T19-a01-round2-crit.json` (receipt `…-round2-review-receipt.md`).

### CI on the final head 55faae0 (green)
```
$ gh pr checks 184
CodeRabbit	pass	0		Review skipped: manual review required for this OSS repository
build	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/36509041495/job/109216886226	
build (client)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/36509041491/job/109216886064	
build (server)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/36509041491/job/109216886153	
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/36509041508/job/109216886318	
private-bootstrap (macos-14, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/36509041496/job/109216886649	
private-bootstrap (ubuntu-latest, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/36509041496/job/109216886462	
private-bootstrap (ubuntu-latest, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/36509041496/job/109216886497	
public-bootstrap (macos-14, client)	pass	9m15s	https://github.com/mryfmo/dotfiles/actions/runs/36509041496/job/109216886251	
public-bootstrap (ubuntu-latest, client)	pass	8m50s	https://github.com/mryfmo/dotfiles/actions/runs/36509041496/job/109216886478	
public-bootstrap (ubuntu-latest, server)	pass	7m36s	https://github.com/mryfmo/dotfiles/actions/runs/36509041496/job/109216886452	
test (macos-14, client)	pass	3m43s	https://github.com/mryfmo/dotfiles/actions/runs/36509041508/job/109216915900	
validate	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/36509041494/job/109216886942	
nix	skipping	0	https://github.com/mryfmo/dotfiles/actions/runs/36509041508/job/109216917132	
test (ubuntu-latest, client)	pass	5m26s	https://github.com/mryfmo/dotfiles/actions/runs/36509041508/job/109216915875	
test (ubuntu-latest, server)	pass	2m53s	https://github.com/mryfmo/dotfiles/actions/runs/36509041508/job/109216915852	
exit=0
$ gh pr view 184 --json headRefOid -q .headRefOid
55faae062d34b7b8f9dc06203069982547540d50
```
