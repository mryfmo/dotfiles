# dot-ubuntu-parity-T3-a01 — worker report

status: ready_for_review
worker: claude-standard-dot
branch: feat/ubuntu-parity (worktree: /home/moriya/Workspace/worktrees/chezmoi-ubuntu-parity)

## Summary

All 9 work items completed and committed, one commit per item, plus one
necessary fixup commit (see below). `make format`, `make validate-agent-assets`,
and `make unit-test` are all green. Nothing outside `allowed_files` was touched.

## Commits (oldest to newest of this task's additions)

- `bb6e0f3` B7 fix(ubuntu): guard server sourcing in client bashrc and remove stale server bin
- `07b8e3f` B8 fix(zsh): only add existing homebrew dirs to PATH
- `990c0bd` B9 feat(usage): schedule usage snapshot via systemd user timer on linux
- `04a73fe` B10 fix(fonts): ship JetBrainsMono on both OS and LINE Seed JP on linux
- `6df6aa1` fixup fix(mise): update supply-chain checksum-block count for the B10 font externals
- `63ca8f3` B11 fix(ubuntu): wire orphaned server timezone setup script
- `3add060` B12 fix(gpg): configure pinentry on linux
- `480b008` B12b fix(git): correct hardcoded user.name
- `9871106` B0b style(bin): satisfy shfmt on contextdb-codex-notify and herdr-agents
- `e7f1e9e` B2b fix(mise): finish yq backend migration in lock and tests

### About the extra fixup commit (`6df6aa1`)

Not one of the task's named items. While finishing B2b I ran the full
`tests/unit/test_supply_chain_policy.py` suite and found
`test_externals_use_fixed_urls_and_checksums` failing: it hardcoded "3
checksummed archive blocks" in `common.yaml.tmpl`, but B10 (this same task)
raised that to 5 (JetBrainsMono added, LINE Seed JP moved in) and I hadn't
updated the assertion when B10 landed. Fixed it in its own commit rather than
amending B10, per this repo's "always create new commits, don't amend"
convention. `tests/**` is in this task's `allowed_files`, so this is in scope.

## Per-item notes

**B7** — Two unguarded `source .local/bin/server/{history,cache}.sh` lines in
the client bashrc (the only two; lines that reference `common/dev` and
`common/git-delete-merged-branches` are not server paths and were left
alone). Guarded both with the same `[ -r ... ] &&` pattern as the neighboring
`prompt.sh`/`aliases.sh`/`secrets.sh` lines. Added the `.chezmoiremove` entry
exactly as specified; verified the guard renders true on this
client/linux machine via `chezmoi execute-template`.

**B8** — Added zsh's `(N-/)` glob qualifier to the 4 specified PATH entries.
Verified empirically (see validation) that on this Linux host, the two
`/opt/homebrew/*` entries are now correctly dropped (directories don't
exist) while `/usr/local/{bin,sbin}` (which do exist here) are kept — this is
exactly the bug being fixed: literal nonexistent dirs no longer pollute PATH.
Did not touch `agent-config.yaml`'s Codex PATH literal, per the task's own
note that it's zero-harm and doesn't need a commit-message mention.

**B9** — New systemd user service+timer, a client-gated `run_onchange`
script, and the macOS plist templatized. The service `ExecStart`/`PATH` and
the timer's `OnCalendar`/`Persistent` match the task spec exactly. The
run_onchange script embeds both units' `sha256sum` as comments so editing
either unit re-triggers it (chezmoi run_onchange only re-fires on its own
rendered content changing — see CompactionDB decision `20114ee0...` below),
and it gracefully no-ops when no user systemd instance is reachable. I never
executed `systemctl` myself (forbidden_action) — only authored the unit/script
content. `.config/systemd` added to the macOS ignore list.
`home/.chezmoiexternal.yaml.tmpl`-equivalent discovery: confirmed via
`chezmoi execute-template` that `Library` is already globally ignored on
Linux, so the renamed `.plist.tmpl` never applies there — no extra ignore
entry needed for it.

**B10** — Added JetBrainsMono to `common.yaml.tmpl` reusing the existing
`$nerdFontsBaseURL`/`$nerdFontsVersion` (already pinned to v3.4.0 for
RobotoMono/Hack). Fetched the real release asset and its real checksum
rather than reusing a guessed value (see validation for the exact commands
and the cross-check against the release's own `SHA-256.txt`). Moved LINE
Seed JP from `macos.yaml.tmpl` to `common.yaml.tmpl` unchanged. Left
`macos.yaml.tmpl` as an existing empty file instead of deleting it:
`home/.chezmoiexternal.yaml.tmpl` (out of this task's `allowed_files`) still
does `{{ template "chezmoiexternal.d/macos.yaml.tmpl" . }}` on darwin, and an
empty template renders to nothing without error, so deleting the file would
break that include while changing nothing I'm allowed to fix.

**B11** — New server-gated `run_once_50-server-setup-timezone.sh.tmpl`,
copy of the existing `run_once_50-server-*.sh.tmpl` include pattern, plus a
minimal bats test (`tests/install/ubuntu/server/setup_timezone.bats`)
mirroring the existing `setup_locale.bats` style: mocks `sudo`, asserts the
script targets `Asia/Tokyo` and installs `tzdata`, and asserts the template
wires the include to the server role only. Per this repo's test policy I did
not run bats locally; I verified the test's logic by hand-tracing the mocked
`sudo` calls against `setup_timezone.sh`'s actual `main()` body (reproduced
in validation) instead.

**B12** — Added `pinentry-curses` to `dependencies.sh`'s `PACKAGES` (kept
alphabetical, between `perl` and `sudo`, matching the existing list's sort
order) and updated the bats package-count/list expectation (14 → 15).
Rendered `gpg-agent.conf.tmpl` to confirm the new linux branch produces
`pinentry-program /usr/bin/pinentry-curses` and darwin is untouched.

**B12b** — One-line literal fix, `name = Shunsuke KITADA` → `name = Fumio
Moriya`. Left `email` templated as-is (already was) and did not templatize
`name`, per the task's own rationale: it's invariant across machines, so a
template variable adds indirection without solving a real problem. Confirmed
no other file references the old name string.

**B0b** — Pure `shfmt`-only reformatting of the two named files (heredoc
`then` placement in contextdb-codex-notify; case-arm indentation in
herdr-agents). No logic changed; confirmed both files' shell syntax is still
valid (`bash -n`) and `shfmt --diff` now reports no drift on either file.

**B2b** — This task's `allowed_files` now include `tests/**` and
`home/dot_mise/mise.lock`, so I finished what T2 could not: updated
`test_supply_chain_policy.py`'s platform-coverage check from
`github:mikefarah/yq` to `aqua:mikefarah/yq`, and deleted the now-orphaned
`[[tools."github:mikefarah/yq"]]` block (29 lines) from `mise.lock` — nothing
in `config.toml` references that backend anymore. Chose a precise manual
block deletion over a full `mise lock` re-run since the lockfile only needed
one stale block removed and a full re-lock risked unrelated diff/network
calls; verified the result is still valid TOML and the full test suite
(including `test_mise_lock_matches_config_and_supported_platforms`) passes.

## CompactionDB decisions registered

```
python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "chezmoi's include/template path resolution in this repo is relative to the chezmoiroot-adjusted source dir (home/), not to the calling .tmpl file's own directory. ..."
-> caa48801-c710-49c9-916e-8075a992929d

python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "run_onchange_* chezmoi scripts only re-run when their own rendered content changes. To react to edits in a separate managed file ... embed that file's content hash as a comment via '{{ include \"path\" | sha256sum }}' ..."
-> 20114ee0-f0a9-4be1-930d-b1f3fdf8922b
```

(Exact commands and full output are in the validation artifact.)

## Verification

- `make format`: clean, exit 0.
- `make validate-agent-assets`: `agent asset validation ok`, exit 0.
- `make unit-test`: 376 tests, OK (1 pre-existing skip, unrelated to this task).
- `uv run python -m unittest tests.unit.test_supply_chain_policy -v`: 17 tests, OK.
- Working tree is clean; no push, no PR, no `chezmoi apply`, no `$HOME` writes,
  no `systemctl` execution.

## Scope check

Nothing outside `allowed_files` was modified. Files touched, all within
scope: `home/dot_bash/client/bashrc`, `home/.chezmoiremove`,
`home/dot_zshenv`, `home/dot_config/systemd/user/usage-snapshot.{service,timer}.tmpl`
(new), `home/.chezmoiscripts/ubuntu/run_onchange_60-enable-usage-snapshot-timer.sh.tmpl`
(new), `home/.chezmoitemplates/chezmoiignore.d/macos`,
`home/Library/LaunchAgents/com.mryfmo.dotfiles.usage-snapshot.plist` → `.plist.tmpl`
(renamed), `home/.chezmoitemplates/chezmoiexternal.d/{common,macos}.yaml.tmpl`,
`home/.chezmoiscripts/ubuntu/run_once_50-server-setup-timezone.sh.tmpl` (new),
`install/ubuntu/common/dependencies.sh`, `home/private_dot_gnupg/gpg-agent.conf.tmpl`,
`home/dot_config/git/config.tmpl`, `home/dot_local/bin/common/executable_contextdb-codex-notify`,
`home/dot_local/bin/common/executable_herdr-agents`, `home/dot_mise/mise.lock`,
`tests/files/{ubuntu,macos}.bats`, `tests/install/ubuntu/server/setup_timezone.bats` (new),
`tests/install/ubuntu/common/dependencies.bats`, `tests/unit/test_supply_chain_policy.py`,
plus this task's own `.orchestration/**` artifact paths.

## cost

n/a (token/cost figures are not exposed to this runtime).
