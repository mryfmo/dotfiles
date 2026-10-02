# AGMSG-TASK dot-mise-pin-test-sync-T53-a01

Drafted 2026-10-02 by the orchestrator (`claude-remediation-dot`, wR:p1).
Worker-c (`claude-standard-dot-a005`), branch `fix/mise-pin-test-sync` from
`origin/main` (4a75924 or later). Verify the dispatched task_rev sha256
against this file; else stop and PONG blocked.

## Objective

`main` is red. Commit 4a75924 (`chore(tools): make upgrade …`) was pushed
directly by the orchestrator without the expected-version sync that T37
(#209) performed alongside the previous pin bump. The Unit test workflow's
"Run Python unit tests" step fails on `origin/main`:

```
FAIL: test_mise_lock_matches_config_and_supported_platforms
AssertionError: 'v2026.9.12' != 'v2026.9.13'
```

Restore green by syncing every live expected-version assertion to the pins
4a75924 landed. Known touch points (confirm, do not assume they are the only
ones):

- `tests/unit/test_supply_chain_policy.py:314` — `v2026.9.12` → `v2026.9.13`
  (`install/common/mise.sh` `MISE_VERSION`).
- `tests/install/common/mise.bats:33` — same value. Keep the test name; the
  Linux arm64 aqua bin-path fix predates v2026.9.13, so the assertion
  remains truthful.

Sweep for every old value the bump replaced and fix each **live** assertion
(one that reads a repository file or rendered output and compares to a
literal). Leave self-contained fixtures alone (for example the
`test_release_asset_pins.py` and `test_generate_agent_configs.py` fixture
data, which carry their own versions and never read the repo):

```
grep -rnE 'v2026\.9\.12|2\.36\.50|v0\.3\.4|v0\.11\.1|v1\.21\.0|12\.5\.1|0\.12\.17|2\.29\.0|2\.1\.284|0\.158\.0' tests scripts .github Makefile
```

Paste that grep and, for each hit, one line saying `live → fixed` or
`fixture → untouched` in the validation file.

Do **not** change any pin itself (`home/dot_mise/**`, `install/**`,
`scripts/lib/installer-pins.sh`, `home/dot_agents/agent-config.yaml`); the
pins are the source of truth, the tests follow them.

`[memory:decision]` T53: a `make upgrade` pin bump is complete only with its
expected-version sync in `tests/**`; the two pin assertions
(`test_supply_chain_policy.py`, `tests/install/common/mise.bats`) follow
`install/common/mise.sh` `MISE_VERSION`. Orchestrator direct push of 4a75924
skipped this and broke `main` (2026-10-02).

## Allowed files

- `tests/**` (only the live assertions the sweep identifies)
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dot-mise-pin-test-sync-T53-a01.md`
- `.agents/worklog/**` waived.

## Forbidden actions

Editing any pin or installer file; editing `.orchestration/acceptance/**`;
merge; force-push; `--delete-branch`; local `bats` (CI runs it); `make
update`/`upgrade`; dependency changes; touching the Understand-Anything
graph (record "hook fired; not acted on" if the UA hook prompts).

## Validation (verbatim output)

`git switch -c fix/mise-pin-test-sync origin/main` (show `git log -1
--oneline` = 4a75924 or later), the sweep grep with per-hit disposition,
`make unit-test`, `make validate-agent-assets` (real exit status), `git diff
--stat origin/main`, `gh pr view <n> --json url,headRefOid,mergeStateStatus`,
`gh pr checks <n>` final state for every job (Linux and macOS, including the
bats `Run unit test` step that 4a75924 skipped), and the CompactionDB
`memory add --kind decision --scope project` command.

## Completion

English PR to `main` titled `test: sync pinned mise version expectations to
v2026.9.13`, CI green, artifacts at the expected paths, `AGMSG-RESULT v1`
with `cost:` in the report, delivered with `agmsg-dispatch dotfiles
claude-standard-dot-a005 claude-remediation-dot wR:p1 "<single line>"`.
max_turns=20.
