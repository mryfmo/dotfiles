# Report: dot-agmsg-upstream-sync-T19-a01

- Worker: claude-standard-dot-a004
- Worktree: `.claude/worktrees/worker-b`, branch `feat/agmsg-upstream-sync` from origin/main
- **PR: https://github.com/mryfmo/dotfiles/pull/184**, head `79b2c5b`, CI all green (including real `public-bootstrap` installs on macOS + 2 Ubuntu variants), not merged
- **Commits:**
  - `595065f` feat(agmsg): install the skill from the pinned upstream commit
  - `b36216f` feat(agmsg): retire the vendored skill snapshot and agmsg-dispatch
  - `a20c972` docs(agmsg): describe upstream poke.sh/send.sh --body-file delivery
  - `c371ba8` feat(herdr-agents): default agmsg bootstrap to upstream monitor mode
  - `06d91f7` fix(agmsg): realign with task revision 2 (v1.5.0, both mode, KEEP_ALIVE)
  - `79b2c5b` docs(herdr-agents): document verified ancestor-path identity matching
- Evidence: `.orchestration/validation/dot-agmsg-upstream-sync-T19-a01.md`

## Task revision handled mid-flight

The task file (`.orchestration/tasks/dot-agmsg-upstream-sync-T19-a01.md`) was revised
(revision 1 → revision 2, commit `3bee1cf`, "grounded in upstream agmsg 1.5.0 sources")
**after** the first three commits above were already implemented and tested against
revision 1's design. Revision 2 explicitly states it replaces revision 1 entirely and
discards the npm-tarball+rsync design (the npm package turned out to be a bootstrapper
only, ships no scripts — confirmed independently before revision 2 even landed, by
downloading and inspecting the real tarball). Commits `06d91f7` and `79b2c5b` realign the
work with revision 2: re-pinned to v1.5.0, delivery mode reverted from `monitor` to
`both` (revision 2's explicit, deliberate policy — independently confirmed upstream's own
documented default really is `monitor`, so `both` is this repo's own choice, not a
correction to accept uncritically), and `AGMSG_CC_MONITOR_KEEP_ALIVE=1` wired into
resident Claude worker panes.

Every factual claim in both the original task and its revision was independently
re-verified against the real upstream repo/registry/CLI output before being relied on —
see the validation file for the specific evidence (commit SHAs, sha256 hashes, tree
listings, `doctor.sh` exit codes, `README.md`/`docs/design.md` quotes).

## Summary of changes

1. **Manifest** (`home/dot_agents/agent-config.yaml`): `assets.agmsg` changed from
   `source: vendored, pin: unknown, verify: none` to `source: git-commit, pin:
c487be269c1973aeb01ca831806eb3f65ff3366d` (the commit behind tag `v1.5.0`), `verify:
sha256` of the tag's source archive, plus `ref: v1.5.0` and `bootstrap_integrity`
   (the npm bootstrapper's own `dist.integrity`, recorded for provenance only, not used
   by the installer) — the extra fields the task revision's schema asked for, layered on
   top of the existing `git-commit`/`sha256` vocabulary rather than inventing a new
   source type, since a byte-for-byte tarball hash is a strictly stronger check than the
   bare commit-hash comparison the revision describes and needed zero validator changes.
2. **Installer** (`scripts/update-agent-assets.sh`): `update_agmsg` fetches
   `https://github.com/fujibee/agmsg/archive/<pin>.tar.gz`, verifies its sha256, extracts,
   and delegates to upstream's own `install.sh --update --cmd agmsg --agent-type
claude-code` (falling back to a fresh, non-`--update` install on the very first run),
   which owns `SKILL.md`/`VERSION`/`scripts/` in place. A before/after sha256 snapshot of
   `teams/db/run` (skipping any that don't exist yet, since a fresh install has none to
   preserve) proves the update never touches live runtime state, rather than only
   trusting a reading of `install.sh`'s source. Idempotent (skips the fetch entirely once
   `VERSION` matches the pin and `scripts/send.sh` is executable) and, like
   `update_terminal_code`/`update_terminal_browser`, tolerates installer failure by
   warning and keeping the existing install rather than aborting the whole `make update`
   run — every step in `main()` after it still runs even if agmsg's fetch fails.
3. **Retired**: the vendored `home/dot_agents/skills/agmsg/` tree (34 files), its
   generated Claude symlink farm (`home/dot_claude/skills/agmsg/`, caught only by running
   the validator — not listed in the task's own blast-radius estimate),
   `symlink_agmsg.md.tmpl`, `executable_agmsg-dispatch` and its test, `test_agmsg_send.py`
   (tested the vendored `send.sh` copy directly), and two agmsg-specific validators
   (`validate_claude_command_parity`, `validate_agmsg_script_modes`) that only existed to
   enforce chezmoi-vendoring conventions (`executable_` prefixes, a hand-maintained
   command symlink) an installer-owned directory doesn't need — matching how
   crit/zed/tode/terminal-browser already work.
4. **Doctor** (`scripts/check-tools.sh`): `check_agmsg` reports the installed `VERSION`
   against the manifest pin, mirroring the existing `check_crit_cli` pattern.
5. **`herdr-agents --bootstrap-agmsg`**: Claude Code seats default to `both` delivery
   (this repo's explicit policy — see below); identity health uses `doctor.sh --project
   <dir> --type <type>` instead of raw `identities.sh` output parsing; the T14 guard
   (`require_distinct_worker_identity`) is untouched. Resident Claude worker panes (all
   three `split_agent_pane` call sites, gated on `worker_kind == claude`, never the
   orchestrator's own root pane) get `AGMSG_CC_MONITOR_KEEP_ALIVE=1` in their pane
   environment.
6. **Docs**: `agmsg-orchestration/SKILL.md` step 6 rewritten for upstream `poke.sh
--body-file`/`send.sh --body-file`, citing #378 (shell-injection hazard) and #1101/#1199
   (`send.sh`'s `--body-file` support) — not the task's own "poke #507" citation, which
   independent research found refers to a different, still-unmerged PR. README updated
   (asset-manifest paragraph, asset-refresh description, `both`+`KEEP_ALIVE` policy).
   `home/dot_config/claude/rules/agmsg-orchestration.md`, the Codex mirror, and `AGENTS.md`
   confirmed (by direct grep, not assumption) to need no changes.

## Deliverable 6 — verification of undocumented behavior

- **(a) Project resolution, main checkout + nested worktree both registered**: verified
  directly against a real, pinned v1.5.0 install in a scratch `$HOME` (three `join.sh`
  calls: a main-checkout path, its nested `.claude/worktrees/worker-b` path, and an
  unrelated sibling path sharing only a string prefix). Finding: `identities.sh`/
  `distinct_agmsg_identity_count` (the T14 guard's actual mechanism) do
  directory-hierarchy-aware ancestor matching — a query for the main checkout's path also
  matches registrations under any of its subdirectories (including a nested worktree),
  not the reverse, and correctly excludes a sibling path sharing only a string prefix.
  Documented as a doctor-comment caveat on `distinct_agmsg_identity_count`; no logic
  changed, since the guard is normally called with a worker's own specific workdir, which
  this finding does not affect.
- **(b) `poke.sh` through the herdr driver** and **(c) `peek.sh` rc on a closed pane**:
  **not attempted.** This sandbox's only herdr server (confirmed running, `herdr 0.9.1`)
  is the live, shared one this very session and other real sessions run in; creating or
  closing panes there to test would risk disrupting actual concurrent work, and no
  isolated herdr sandbox is available. Recorded as not verified rather than fabricated or
  risked against shared infrastructure.
- **(d) `team.sh --json` output**: verified — well-formed JSON with per-member
  placement/reach/consistency metadata against the real scratch install (see validation
  file for the verbatim output).

## Known blocker (unchanged from T17)

`pr-feedback.py <n>` disposition output is part of this task's validation requirement,
but that script only exists on the open, unmerged PR #182 (`feat/pr-feedback-gate`) — not
on `main` or this branch. Skipped per the same operator decision as T17; not touching
PR #182 or `main`.

`[memory:decision]`: "agmsg is installed by the upstream installer at a pinned tag
verified by commit sha, recorded in the asset manifest; the vendored snapshot and
agmsg-dispatch are retired; wake uses upstream poke, health uses team/doctor/peek."

## Revision round 2 (rebase + 5 commits, head `9581bb3`)

- **AGMSG-ACCEPTANCE (2026-09-26T02:37:13Z + round-1 supplement, from
  `claude-remediation-dot`):** status=revise on head `79b2c5b`. 5 MAJOR + 4 MINOR findings,
  all independently re-derived by the orchestrator against the branch, this host, and
  upstream v1.5.0 sources, plus a supplement (finding 11) re-deriving deliverable 6(a) from
  upstream `docs/design.md`. Every finding re-verified independently before fixing (not
  applied on trust) — see the validation file for the specific evidence per fix.
- **Rebase**: onto `origin/main` `3375fb0` (#183 merged). Both `tests/install/common/check_tools.bats` and `tests/unit/test_runtime_health.py` conflicted (both branches added adjacent test infrastructure); resolved by keeping both sides' additions in sequence, then found and fixed one post-rebase fixture gap (a `main()` stub list missing `update_agmsg`).
- **Commits:**
  - `cc560c8` (rebase of `595065f`) / `1fe462e` fix(tests): stub `update_agmsg` in the gh-extension `main()` fixture
  - `f9a5314` fix(agmsg): always guard live state across install/update, harden `set -e` (Fix 1 + Fix 6)
  - `a8bb307` fix(validate): enforce agmsg provenance fields instead of accepting them decoratively (Fix 2)
  - `5df1272` fix(chezmoi): remove the retired agmsg skill symlink farm from live hosts (Fix 3)
  - `1dc861c` fix(agmsg): add ext-tools writable root, correct SKILL.md delivery claim (Fix 4)
  - `16a967e` fix(agmsg): register worker identities with `AGMSG_RESOLVE_PROJECT=0` (Fix 5)
  - `9581bb3` docs(agmsg): drop pane-status inference from SKILL.md, document poke exit codes (Fix 7)

### Fix 1 (MAJOR) — migration path

`install_pinned_agmsg` now snapshots `teams/db/run` unconditionally (not gated on
`installed != "none"`), surfaces `install.sh --update`'s stderr instead of discarding it,
and `update_agmsg`'s failure message no longer falsely claims "existing install unchanged".
Two new tests close the exact gap: a marker-less legacy dir with real `teams/db/run` data
now proves the snapshot protects it; a fake `install.sh` that actually mutates state now
proves the abort branch fires (previously untested — the existing test's fake script never
wrote anything).

### Fix 2 (MAJOR) — validator provenance enforcement (change request)

Kept `source: git-commit`/`verify: sha256` (a change request, already accepted per the
round-1 decision) instead of deliverable 1's literal `source: agmsg-installer` schema, but
the validator no longer treats `ref`/`bootstrap_integrity` as decorative: it now requires
`ref` present, `pin` a full 40-character commit sha, and `bootstrap_integrity` a
well-formed npm `sha512-<base64>` string, specifically for the `agmsg` asset (Homebrew's
and understand-anything's own `git-commit` assets are untouched — neither declares `ref`).
Four new subtest cases replace targeted coverage for this asset's provenance; the seven
tests deleted with the two retired vendoring-only validators are not restored as such,
since those validators' own purpose (chezmoi `executable_` conventions) genuinely no
longer applies to an installer-owned directory.

### Fix 3 (MAJOR) — dangling `~/.claude/skills/agmsg/**`

Added `.claude/skills/agmsg/**` to `home/.chezmoiremove`. Verified against a scratch
`$HOME` pre-populated with a stale `SKILL.md`/`scripts/send.sh`: `chezmoi apply --dry-run
--verbose` reports the directory as deleted, and a real (non-dry-run) apply removes it from
disk. See validation file for the exact commands and output.

### Fix 4 (MAJOR) — `ext-tools` writable root; Codex delivery change request

Added `ext-tools` to the manifest, the generated `codex-config-managed.toml` (via
`generate-agent-configs.py`, not hand-edited), and `REQUIRED_AGMSG_WRITABLE_ROOTS` —
verified directly against upstream `install.sh`'s `configure_codex_sandbox`, which always
adds `db/teams/run/ext-tools` regardless of delivery mode. Change request for the other
half of deliverable 5: Codex stays on `turn`, not upstream's shim-based `monitor` bridge,
because that bridge has three open reliability defects as of v1.5.0 (upstream #149, #151,
#1236 — independently checked via `gh api`, all still `open`) that an unattended resident
worker cannot risk. Fixed SKILL.md:37-38's self-contradiction about herdr-agents' actual
per-type delivery modes.

### Fix 5 (MAJOR) — `AGMSG_RESOLVE_PROJECT=0` (round-1 supplement, finding 11)

Redid deliverable 6(a) against a real, freshly-installed v1.5.0, running the actual
agent-driven entry points (`join.sh`, `whoami.sh`, `session-start.sh`) instead of
`identities.sh` with hand-typed paths — the prior round's mistake, since `identities.sh` is
a pure exact-match lookup with no ancestor logic at all (that logic lives in `join.sh`
et al.). Reproduced the exact P2 collision this task exists to close: a `join.sh` from
inside a nested worktree, with agmsg's default project resolution left on, silently
registers at the orchestrator's already-registered main-checkout path instead of the
worktree's own; `AGMSG_RESOLVE_PROJECT=0` fixes it. Every worker pane herdr-agents creates
now exports it. `distinct_agmsg_identity_count`'s doc comment corrected to describe what
`identities.sh` actually does. Documented the rule (citing upstream #92 and
`docs/design.md`) in README.md and the agmsg-orchestration skill.

Also separately discovered while reproducing this: upstream's own `session-start.sh` skip
for `.claude/worktrees` paths (#367, meant for Claude Code's own short-lived background-task
sub-sessions) happens to pattern-match this repo's unrelated, long-lived resident-worker
worktree convention of the same name. This live session's own SessionStart hook did fire its
Monitor directive despite running from such a path, so the two do not appear to collide in
practice, but the exact reason was not resolved this round — flagged as an open question
rather than asserted either way; a dedicated follow-up (live-verification task, per the
orchestrator's own round-1 waiver of 6(b)/(c)) would be the right place to pin it down with
a live Claude Code session rather than a scratch scripted repro.

### Fix 6 (MINOR) — `set -e` hardening, `shasum` portability

Every previously-bare command inside `install_pinned_agmsg` (which runs on the left of `||`
in `update_agmsg`, making `set -e` inert throughout its body) now has explicit
`|| return 1`. `agmsg_state_snapshot` switched from `sha256sum` to `shasum -a 256`,
matching every other checksum call in this file (macOS lacks GNU coreutils by default).

### Fix 7 (MINOR) — pane-status inference removed; poke exit codes; #133 declined

SKILL.md step 6's manual pane-status check before `poke.sh` removed (prohibited per G1,
and redundant with poke's own herdr driver and input-box safety check). Documented
`poke.sh`'s exit-code taxonomy and the rule that a 13 must never be retried as `send.sh`.

Independently re-verified and **declined**: the round's "document that `--update` stops
in-flight `watch.sh` (upstream #133)" instruction does not hold for v1.5.0. #133 is an
unrelated, closed issue; the actual behavior was fixed upstream in #1320 (closed
2026-09-19, before v1.5.0) — confirmed directly in the real v1.5.0 `scripts/watch.sh`
source: it now waits and restarts onto the new code rather than exiting. Documenting the
old behavior in the README would be false for the version this repo pins, so no doc change
was made for this specific item; see the validation file for the exact evidence.

### Fix 8/9 (MINOR) — contract and file-change completeness

All changed paths across the whole branch (`git diff origin/main...HEAD --name-status`),
including everything omitted from the round-1 report:

```
D  home/dot_agents/skills/agmsg/** (34 files: SKILL.md, agents/openai.yaml, db/.keep,
   run/.keep, teams/.keep, scripts/{executable_*.sh, lib/*.sh, release/executable_sync-version.sh},
   templates/cmd.*.md)
D  home/dot_claude/commands/symlink_agmsg.md.tmpl
D  home/dot_claude/skills/agmsg/** (31 files: the generated Claude symlink farm)
D  home/dot_local/bin/common/executable_agmsg-dispatch
D  tests/unit/test_agmsg_dispatch.py
D  tests/unit/test_agmsg_send.py
M  README.md
M  home/.chezmoiremove
M  home/.chezmoitemplates/codex-config-managed.toml
M  home/dot_agents/agent-config.yaml
M  home/dot_agents/skills/agmsg-orchestration/SKILL.md
M  home/dot_local/bin/common/executable_herdr-agents
M  scripts/check-tools.sh
M  scripts/update-agent-assets.sh
M  scripts/validate-agent-assets.py
M  tests/install/common/check_tools.bats
M  tests/unit/test_asset_manifest.py
M  tests/unit/test_herdr_agents.py
M  tests/unit/test_runtime_health.py
M  tests/unit/test_validate_agent_assets.py
```

`report=.orchestration/reports/dot-agmsg-upstream-sync-T19-a01.md`
`validation=.orchestration/validation/dot-agmsg-upstream-sync-T19-a01.md`

CompactionDB: `python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope
project --content "..."` → `90b08f9f-b1a7-4866-99b0-233b51e97230` (see validation file for
the full content).

### CodeRabbit / review gate

Per AGMSG-NOTE (2026-09-26T03:00:41Z, `claude-remediation-dot`): CodeRabbit is removed from
the PR gate; the previously-assigned 04:36Z slot and every `@coderabbitai` request are
cancelled; the bot-review gate becomes Codex review (T16 revision 2, forthcoming). No
CodeRabbit review was requested on this round's final head, per that note.

`[memory:decision]` (round 2 addendum): "Codex agmsg delivery stays on `turn` (change
request: upstream's shim-based `monitor` bridge has three open reliability defects as of
v1.5.0 — #149/#151/#1236); every worker pane exports `AGMSG_RESOLVE_PROJECT=0` so
join.sh/whoami.sh/watch.sh register at the worker's own worktree path instead of the
orchestrator's ancestor-resolved main checkout (upstream #92)."
