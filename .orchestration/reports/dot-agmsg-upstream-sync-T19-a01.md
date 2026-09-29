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

---

## Round 2 (task revision 3), worker claude-standard-dot-a005

- **Worker and worktree.** worker `claude-standard-dot-a005` in `.claude/worktrees/worker-c`. Round 1 was done by a004 in worker-b.
- **Task revisions.** `task_rev` was verified by sha256 against `origin/main` at each ruling:
  - r3 `54f12a56…` at fb11017;
  - addendum 1 `bdb79730…` at b008d84;
  - addendum 2 `a454e2e3…` at 5ea0d9d.
- **Branch.** `feat/agmsg-upstream-sync`, recreated per ruling with `git switch -C feat/agmsg-upstream-sync origin/feat/agmsg-upstream-sync` (579bafe, the PR head). The local-only `1aefa58` (withdrawn supplement 2) was not carried. The branch is rebased onto `origin/main` 5ea0d9d and pushed with `--force-with-lease` on my own branch, as authorized.
- **PR.** https://github.com/mryfmo/dotfiles/pull/184, head `55faae062d34b7b8f9dc06203069982547540d50`. CI is green: every check passes, and nix is skipped. Run history: 7bd66ac failed on SC2015 in CI's shellcheck, e0674d1 was green, and 55faae0 is green. The verbatim output is in the validation file.
- **Round-2 commits, final SHAs** (pre-rebase SHAs in brackets, as cited in the crit replies and baselines):
  - `aa5c038` [54f25df]: installer migration and state guard (findings 1, 6).
  - `ad7338d` [5999c76]: manifest spec and validator ownership rules (finding 2).
  - `13e6d6b` [8fcc681]: registration, delivery and wake docs, plus the parity and chezmoi tests (findings 3, 4, 7, 11).
  - `c39e4d1` [d069161]: agmsg-dispatch on the upstream 1.5.0 libs (ruling addendum 1, option A).
  - `7c0e1d7` [e0674d1]: SC2015 fix; CI's shellcheck flagged `A && B || C`.
  - `5623e83` [cca3e6b]: review fixes (guard P1/P2, validator, docs).
  - `55faae0` [7546cc4]: doctor allowlists (ruling addendum 2, option A).

### Rebase (ten overlapping files)

The rebase replayed round 1's 14 commits. Conflicts came up in three files only, and the other seven auto-merged:
- `tests/unit/test_validate_agent_assets.py`, conflicting twice:
  - The first time, the branch deleted the vendored-command parity tests and main appended T33i's `MaskSecretsModeTest` after them. Resolution: drop the parity tests, keep `MaskSecretsModeTest`.
  - The second time, it was the same region against a8bb307 (the validator's provenance rules). Resolution: keep main's side.
- `home/dot_agents/skills/agmsg-orchestration/SKILL.md`, conflicting twice (f53c7de, 1dc861c). Resolution: take the branch's delivery bullets and keep main's T33a interim inbox-discipline bullet.
- `scripts/validate-agent-assets.py`, once (a8bb307). The branch only reformatted one `fail()` call, while main added the `worker_profile` and advisor checks. Resolution: keep main's side.

`README.md`, `home/dot_agents/agent-config.yaml`, `executable_herdr-agents`, `scripts/check-tools.sh`, `scripts/update-agent-assets.sh`, `tests/unit/test_herdr_agents.py` and `tests/unit/test_runtime_health.py` auto-merged.

A mechanical check found that every line main added to the ten files since the round-1 base `3375fb0` is present at HEAD, with **0 missing in each file**. That output and `git diff --stat origin/main` are pasted in the validation file.

### Findings closed

1. **Migration path (MAJOR).**
   - `update_agmsg` selects the mode from the upstream `.agmsg` marker: `install.sh --update` only when the marker exists, and the plain installer otherwise. The marker-less legacy vendored directory therefore never gets `--update`.
   - Before any installer run, `teams/`, `db/`, `run/` and `agents/` are copied to `~/.agents/backups/agmsg-state-<UTC>/`. That copy is the rollback.
   - Installer stderr is captured and printed on failure.
   - Afterwards every *pre-existing* file under `teams/`, and `db/messages.db`, must be byte-identical. New files are allowed, because upstream creates a missing `messages.db`. `VERSION` must equal the pin with the marker present.
   - `run/` changes are reported, not failed. This deviation from the literal "run/ untouched" is accepted in ruling addendum 2. Upstream evidence: `--update` runs `remote.sh sync restart`, whose pidfiles live under `SKILL_DIR/run` (`remote.sh:42,1779`), and live watchers rewrite `run/`.
   - Failure messages name what failed. The live-state failure lists the changed paths and the copy.
   - Tests: a fake installer that mutates state fails both the `--update` path and the migration path. There are also tests for the store the installer creates plus a `run/` note, VERSION ≠ pin, an empty snapshot, and missing `tar`.
   - E2E in scratch HOMEs with the real pinned archive:
     - the origin/main vendored tree plus live state kept byte-identical sha256s, the marker, VERSION 1.5.0, and the backup;
     - a fresh HOME and a legacy directory holding only `.keep` files both succeed;
     - a second run is a no-op.
2. **Manifest spec (MAJOR).**
   - `assets.agmsg` fields: `source: agmsg-installer`, `pin: "1.5.0"`, `ref: v1.5.0`, `ref_commit: c487be2…` (40 chars), `sha256` of GitHub's archive for `ref_commit` (the accepted change request), and `bootstrap_integrity` (npm sha512, for provenance). The renderer maps `AGMSG_PIN_COMMIT←ref_commit` and `AGMSG_PIN_VERSION←pin`.
   - Validator: `validate_agmsg_installer_asset` requires a release pin, `ref == v<pin>`, a full `ref_commit`, and an npm sha512 integrity.
   - `validate_agmsg_is_installer_owned` rejects:
     - a vendored `dot_agents`/`dot_claude` agmsg skill, including attribute-prefixed ones;
     - any chezmoi-managed `~/.claude/commands/agmsg.md`;
     - a missing `.claude/skills/agmsg/**` removal;
     - `.chezmoiremove` entries that would delete installer-owned paths (the skill dir, `.agmsg`, `VERSION`, `SKILL.md`, `scripts/`, `db`, `teams`, the command file).
   - Eight named tests replace the seven deleted in round 1.
3. **Dangling chezmoi symlinks (MAJOR).**
   - `home/.chezmoiremove` retires `.claude/skills/agmsg/**`. A scratch-HOME `chezmoi apply` with both the `**` form and the plain form removes the whole stale symlink tree and keeps unrelated skills. The repo test `test_chezmoiremove_agmsg` applies the real `.chezmoiremove` and checks that installer-owned paths survive.
   - `~/.claude/commands/agmsg.md` is deliberately not removed: upstream's fresh install renders to a temp file and `mv -f`s it over the stale link, which replaces the link and does not write through it. A `.chezmoiremove` entry would delete upstream's file on every apply.
   - The other deleted targets under `~/.agents/skills/agmsg` are installer-owned. Upstream prunes the vendored scripts that 1.5.0 does not ship, on the plain install path too (install.sh:929).
   - Documented in README.
4. **Codex seats (MAJOR).**
   - Upstream's README contradicts itself on the Codex default: line 63 says `monitor`, while its delivery table says `turn`. The SKILL, README and herdr-agents now state this repo's explicit `turn` choice. The reason is three Codex monitor-bridge issues, all verified still **open** with `gh issue view`: #149, #151 and #1236.
   - The four writable roots, including `ext-tools`, in the manifest, the template and the validator match upstream `configure_codex_sandbox`. That function greps for each root and reports "already configured", so it makes no edit and no drift follows.
5. **Deliverable 6.**
   - (a) Redone verbatim per 11(ii) in a scratch HOME with a real v1.5.0 install. Output is in the validation file.
   - (b)(c) stay orchestrator-side at acceptance (shared live herdr server).
   - (d) `team.sh t19 --json` output is pasted.
   - No upstream issues were filed by me. Observed gaps for the operator:
     - (i) `session-start.sh` exits before starting a watcher or writing a marker for any session whose cwd is under `.claude/worktrees/` (#367). A resident Claude seat launched inside a nested worktree gets no Monitor delivery. Repro: case 5 in the 6(a) output.
     - (ii) The vendored `send.sh` on live hosts takes `--body-file` as the message body (the #1101 behaviour). This session's message 461 arrived with the literal body `--body-file`. 1.5.0 fixes it in code, but #1101 is still OPEN on GitHub.
     - (iii) `poke.sh` refuses a hand-joined member until it has acted from its own pane (no placement record).
6. **`install_pinned_agmsg` (MINOR).**
   - `curl` and `tar` are checked explicitly, and hashing uses `sha256sum`, or `shasum -a 256` on macOS, through one helper that fails when neither exists.
   - Every step checks its own status, because this function runs on the left of `||` where `set -e` is inert.
   - The snapshot fails when `find` cannot list a subtree, or when it hashed fewer files than exist, so an empty snapshot can no longer compare equal.
7. **SKILL wording (MINOR).**
   - The pane-status gate and raw `herdr pane run` wakes are gone.
   - Wake selection goes by seating: agmsg-dispatch for herdr-agents panes, `poke.sh --body-file` for spawn-seated members, `send.sh --body-file` for pane-less ones.
   - Exit 13 is documented with its three messages, and "never retry as send.sh" is stated.
   - README documents the `--update` watcher stand-down and the post-update `delivery.sh set` re-run that upstream prints (#133).
8. **Contract (MINOR).** The RESULT carries all five artifact paths. The validation file pastes verbatim unittest, validator, shellcheck and CI output. The CompactionDB command and its id are below.
9. **allowed_files (MINOR).** Every path touched in round 2 is listed below, and all are within r3 plus addenda 1 and 2.
11. **Identity resolution (MAJOR, design).**
    - (i) The documented operator procedure (SKILL, rule, README) registers a worker with `AGMSG_RESOLVE_PROJECT=0 join.sh <team> <name> <type> <worktree>` and points `delivery.sh set` at the worktree. herdr-agents' printed join hints carry the opt-out, and every worker pane it creates exports the opt-out (round 1). herdr-agents itself performs no joins, and seating was not redesigned.
    - (ii) Verified verbatim:
      - a join from inside the worktree without the opt-out registers at the main checkout; with it, at the worktree;
      - `whoami.sh` inside the worktree without a marker resolves to the worktree registration;
      - with a marker naming the main checkout (a seat launched from the main path), `whoami.sh` inside the worktree answers `multiple=true agents=orch,w-resolved … project=<main>`; the opt-out restores the worktree;
      - a marker naming the worktree (delivery baked with the worktree path) resolves to the worktree.
    - (iii) Documented in README, the SKILL and the rule with #92 and docs/design.md, including the full order (marker → ancestor → git common dir) and the `.claude/worktrees` skip. The herdr-agents identity-count comment is corrected: it now names all three signals and drops the history note.

### Deliverable 4 reconciled with the regime (rulings)

- **agmsg-dispatch is kept.** Upstream 1.5.0 has no `lib/identifier.sh`, and the plain install prunes it. `agmsg_db_path` now requires a team selector. So `origin/main`'s dispatch fails after the upgrade (E2E: `line 25: …/lib/identifier.sh: No such file or directory`).
- **Ruling option A:**
  - It now sources upstream `lib/validate.sh`, validating the team name and both agent names.
  - It keeps the strict `^[a-z0-9][a-z0-9_-]{0,63}$` grammar, because the identifiers are interpolated into SQL and upstream's deny-lists allow `'`.
  - It passes the team to `agmsg_db_path`.
  - The shdoc states it is the sanctioned wake path for herdr-agents worker panes until seating writes placement records.
- **E2E against a real 1.5.0 install** with a fake herdr: the message was sent, the pane woken, `read_at` set, and an SQL-unsafe sender refused.

### Independent review

A subagent in a separate context adversarially reviewed the four original round-2 commits:
- It found 1 P1, 3 P2 and 5 P3 findings, with the verdict **incorrect** on the pre-fix head.
- The P1 was mine: the guard falsely failed every fresh install, and my fixture hid it.
- All 9 findings are resolved (fixes 5623e83, 55faae0), with crit evidence `…-round2-crit.json` and receipt `…-round2-review-receipt.md`.
- The review text is pasted in the validation file.

### Files touched in round 2 (all within r3 + addenda)

- Code:
  - `scripts/update-agent-assets.sh`
  - `scripts/validate-agent-assets.py`
  - `scripts/check-agent-runtime.py`
  - `home/dot_agents/agent-config.yaml`
  - `home/dot_local/bin/common/executable_herdr-agents`
  - `home/dot_local/bin/common/executable_agmsg-dispatch`
- Docs:
  - `home/dot_agents/skills/agmsg-orchestration/SKILL.md`
  - `home/dot_config/claude/rules/agmsg-orchestration.md`
  - `README.md`
- Restored:
  - `home/dot_local/bin/common/executable_agmsg-dispatch`
  - `tests/unit/test_agmsg_dispatch.py`
- Tests:
  - `tests/unit/test_runtime_health.py`
  - `tests/unit/test_validate_agent_assets.py`
  - `tests/unit/test_herdr_agents.py`
  - `tests/unit/test_check_agent_runtime.py`
  - `tests/unit/test_agmsg_dispatch.py`
  - new `tests/unit/test_agmsg_orchestration_docs.py`
  - new `tests/unit/test_chezmoiremove_agmsg.py`
- Round 1's deletions (`home/dot_agents/skills/agmsg/**`, `home/dot_claude/skills/agmsg/**`, `home/dot_claude/commands/symlink_agmsg.md.tmpl`, `tests/unit/test_agmsg_send.py`) and `tests/install/common/check_tools.bats` are carried unchanged.
- Artifacts (main checkout): the five task files, plus `…-round2-crit.json` and `…-round2-review-receipt.md`.

### Effects

`effects=agmsg-state-backup`. When `make update` next runs on a host, it creates `~/.agents/backups/agmsg-state-<UTC>/`. Reverse mapping: remove it with the documented `rm -rf ~/.agents/backups/agmsg-state-*`. I made no writes to the real HOME; all E2E ran in scratch HOMEs under the session scratchpad.

### CompactionDB

[memory:decision] agmsg is installed by the upstream installer at a pinned tag verified by commit sha, recorded in the asset manifest; the vendored snapshot and agmsg-dispatch are retired; wake uses upstream poke, health uses team/doctor/peek. It is refined by the r3 rulings recorded in the command below. Id `8e20faa2-1754-42ab-a816-07663434e095`; the command and output are in the validation file.

### Not done / for acceptance

- CodeRabbit full review and the pr-feedback sweep need the orchestrator-assigned slot.
- 6(b)(c) live herdr poke/peek stay orchestrator-side.
- `make require-crit-review` is the orchestrator's step.
- The `.ua` knowledge graph was not rebuilt; that is out of scope, since graph builds are separate tasks.

cost: n/a (the Claude Code runtime does not expose session token/cost figures to the worker)
