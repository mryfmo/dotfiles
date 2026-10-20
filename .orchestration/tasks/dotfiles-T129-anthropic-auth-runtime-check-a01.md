---
format: 2
task_id: dotfiles-T129-anthropic-auth-runtime-check-a01
kind: code
security: true
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
allowed_files:
  - scripts/check-tools.sh
  - tests/install/common/check_tools.bats
  - tests/unit/test_runtime_health.py
  - .orchestration/dotfiles-T129-anthropic-auth-runtime-check-a01/**
after: [dotfiles-T129-assets-omp-hcom-a01]
threat_table:
  - control: "the PR edits scripts/check-tools.sh in two places (the function check_anthropic_auth_route and its one call in main after check_hcom)"
    disposition: "closed: tests/install/common/check_tools.bats::[common] check_anthropic_auth_route refuses ANTHROPIC_OAUTH_TOKEN and an Anthropic OAuth credential in omp's auth store"
  - control: the PR edits tests/install/common/check_tools.bats only for the new cases
    disposition: "residual: new @test blocks beside the existing thirteen, which stay byte-identical; every fixture lives under BATS_TEST_TMPDIR"
  - control: the PR edits tests/unit/test_runtime_health.py only in the environment its doctor fixture builds (item 3)
    disposition: "residual: the fixture at test_runtime_health.py:1229 spreads os.environ into the run's environment; the edit removes ANTHROPIC_OAUTH_TOKEN and PI_CODING_AGENT_DIR from it, so the pinned required-failure and warning counts (lines 1240 to 1243) no longer depend on the host; the module's other tests stay byte-identical"
  - control: "omp's auth store and the process environment as inputs (a credential database and ANTHROPIC_OAUTH_TOKEN, both the operator's)"
    disposition: "residual: the store is opened with sqlite3 -readonly for one count, the variable is tested for presence only, and no value, row or token ever reaches stdout or stderr (the test asserts the fixture secret is absent from the output)"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T129-anthropic-auth-runtime-check-a01/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T129-anthropic-auth-runtime-check-a01/ (report.md, validation.md, sandbox.md, learning.md)
    disposition: "residual: prose and pasted command output; the sandbox record lists every permission-gated command; the audit reads them"
  - control: "task metadata (the front matter of the task copy: kind, security, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: in-process effects
    disposition: "residual: bats sources the script in a subshell with HOME under BATS_TEST_TMPDIR, as the module's other cases do, and tests/unit/test_runtime_health.py runs main with a fake HOME and, after item 3, an environment without ANTHROPIC_OAUTH_TOKEN and PI_CODING_AGENT_DIR, so no test reads the host's token or opens the host's store; every bats run unsets ANTHROPIC_OAUTH_TOKEN and PI_CODING_AGENT_DIR and sets HOME under BATS_TEST_TMPDIR, run (d) setting PI_CODING_AGENT_DIR there"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter file is in allowed_files; the script runs under bash as today, bats runs through scripts/run_unit_test.sh in the test workflow (premise 2) and shellcheck -x over scripts/*.sh there; a fixture case skips when the runner has no sqlite3 instead of installing one"
  - control: new or renamed scripts
    disposition: "residual: no new or renamed script (one function in the existing check); any other new or renamed script is an undeclared change the audit fails"
  - control: orchestrator effect merge
    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
premises:
  - claim: PR A (#388) is merged, so check-tools.sh is no longer PR A's file and its last change on origin/main is that merge
    command: git log --oneline -1 origin/main -- scripts/check-tools.sh
    output: |-
      f32c02b8 feat(agents): pin verified omp and hcom assets (#388)
  - claim: check-tools.sh on origin/main has no Anthropic probe yet, and the test workflow's runner executes every module under tests/install/common/ (bats is CI-only here, Test Policy)
    command: a=$(git show origin/main:scripts/check-tools.sh | /usr/bin/grep -c ANTHROPIC || true); b=$(git show origin/main:scripts/run_unit_test.sh | /usr/bin/grep -c 'bats -r "tests/install/common/"'); echo "$a $b"
    output: |-
      0 1
---

# AGMSG-TASK dotfiles-T129-anthropic-auth-runtime-check-a01 — check-tools refuses the Anthropic OAuth route at run time (plan 023 PR D, run-time half)

Written 2026-10-18 by the orchestrator seat as the run-time half of plan 023's PR D, deferred at 2026-10-17T11:05Z until PR A merged because `scripts/check-tools.sh` was PR A's file (premise 1). The repository half is PR #389 (`dotfiles-T129-anthropic-auth-route-check-a01`) and its follow-up. The operator's decision stands: Anthropic through `ANTHROPIC_API_KEY` only; Anthropic OAuth in omp is forbidden by its terms (plan 023, Decision, line 8); secrets only through the environment or omp's auth store. Plan 023 records the store as `~/.omp/agent/agent.db` (SQLite; `PI_CODING_AGENT_DIR` moves it) and omp's lookup order as `ANTHROPIC_OAUTH_TOKEN` then `ANTHROPIC_API_KEY` (facts line 15); on the orchestrator's Mac the file exists and `file` reports SQLite 3.x.

## Goal

`make doctor` (Makefile `doctor`, which runs `scripts/check-tools.sh` and fails on a required failure) fails when `ANTHROPIC_OAUTH_TOKEN` is set in the environment or omp's auth store holds an Anthropic OAuth credential, prints `found:` lines when neither is the case, and reports `not applicable` when the store is absent. No value is ever printed.

## Files

1. `scripts/check-tools.sh`: `check_anthropic_auth_route()` after `check_hcom`, called from `main` right after `check_hcom` (inside the "Agent tools" section; no new section), with the shdoc block its neighbours carry. Store path `"${PI_CODING_AGENT_DIR:-${HOME%/}/.omp/agent}/agent.db"` (VERIFY 2). Two rules, in this order, both always evaluated:
   - (E) `ANTHROPIC_OAUTH_TOKEN` set at all (`${ANTHROPIC_OAUTH_TOKEN+set}`, an empty value counts): `required failed: ANTHROPIC_OAUTH_TOKEN is set; Anthropic goes through ANTHROPIC_API_KEY only (unset it)` on stderr and `((required_failures += 1))`, as `check_apparmor_userns` reports; otherwise `found:   ANTHROPIC_OAUTH_TOKEN -> unset`.
   - (S) store absent: `not applicable: omp auth store (<path> absent)` and return 0. Present: one `n=$(sqlite3 -readonly "<path>" "select count(*) from auth_credentials where provider='<anthropic id>' and credential_type='oauth'" 2>/dev/null) || n=`, the table and columns of VERIFY 1 (the `|| n=` keeps `set -Eeuo pipefail` from ending `main` when sqlite3 fails) and the provider literal of VERIFY 1b; sqlite3's stderr is discarded because a schema mismatch echoes the query text. A command that fails or prints anything but digits (`[[ $n =~ ^[0-9]+$ ]]`: no sqlite3, a locked or foreign file, a schema the query does not fit) is `required failed: omp auth store at <path> could not be verified (sqlite3 missing or its schema changed); remove the Anthropic login in omp or make the store readable` and `((required_failures += 1))`: an existing store that cannot be checked is never a pass (plan 023 D). Count 0: `found:   omp auth store -> <path> (no Anthropic OAuth credential)`. Count above 0: `required failed: omp auth store holds <n> Anthropic OAuth credential(s) at <path>; remove the Anthropic login in omp and use ANTHROPIC_API_KEY` (VERIFY 3) and `((required_failures += 1))`.
   - The function prints paths, names and counts only: never the token, never a row, never the query's output beyond the count. `set -Eeuo pipefail` stays; the two `required failed` paths return 0 like the rest of the script (the summary line and `main`'s final test carry the exit status).
2. `tests/install/common/check_tools.bats`: `@test "[common] check_anthropic_auth_route refuses ANTHROPIC_OAUTH_TOKEN and an Anthropic OAuth credential in omp's auth store"`, in the module's form (`run env -u ANTHROPIC_OAUTH_TOKEN -u PI_CODING_AGENT_DIR HOME="${BATS_TEST_TMPDIR}…" bash -c 'source "$1"; check_anthropic_auth_route; [ "$required_failures" -eq <n> ]' bash "${SCRIPT_PATH}"`), five runs, each asserting that `never-printed` is absent from the merged output: (a) `ANTHROPIC_OAUTH_TOKEN=never-printed` with an empty HOME: `required_failures` 1, output holds `required failed: ANTHROPIC_OAUTH_TOKEN is set` and `not applicable: omp auth store`, and does not hold `never-printed`; (b) `env -u ANTHROPIC_OAUTH_TOKEN` with an empty HOME: `required_failures` 0, output holds `found:   ANTHROPIC_OAUTH_TOKEN -> unset`; (c) a fixture store at `${BATS_TEST_TMPDIR}/.omp/agent/agent.db`, created with `sqlite3` from the `CREATE TABLE auth_credentials` statement of VERIFY 1, holding one row with `provider` the Anthropic id of VERIFY 1b, `credential_type` `oauth` and `data` `never-printed`: `required_failures` 1, output holds `required failed: omp auth store holds 1` and does not hold `never-printed`; (d) the same store holding only an OpenAI `oauth` row and an Anthropic `api_key` row, both with `data` `never-printed`, reached through `PI_CODING_AGENT_DIR` with an empty HOME: `required_failures` 0, output holds `found:   omp auth store`; (e) an empty file at the store path: `required_failures` 1, output holds `could not be verified`. Runs (c) and (d) `skip` when `command -v sqlite3` fails (VERIFY 5), so the module stays green on a runner without it; the RESULT says whether CI ran or skipped them. The existing thirteen `@test` blocks stay byte-identical.

3. `tests/unit/test_runtime_health.py`: the doctor fixture that runs `main` (line 1229, `{**os.environ, …}`) drops `ANTHROPIC_OAUTH_TOKEN` and `PI_CODING_AGENT_DIR` from the environment it builds, so its pinned `required failures: 0` and `optional warnings: 3` hold on a host where either is exported; no other change in the module.

## Out of scope

The repository half (the validator's rules over `home/` and `install/`: PR #389 and `dotfiles-T129-anthropic-auth-route-check-followup-a01`); the secret masker and the CI grep over the tree and the generated files (PR D's CI items); any rendered omp file (`models.yml`, `config.yml`: PR B); any workflow file; any installer; `check_omp` and `check_hcom` themselves.

## Check

Pasted in the validation file: `make render-check` (exit 0; this task renders nothing, the standing check), `shellcheck -x scripts/check-tools.sh` (CI's form, `.github/workflows/test.yaml` step "Run ShellCheck", line 310) and `shfmt --indent 4 --space-redirects --diff scripts/check-tools.sh` (the `format` target's form) both clean, `uv run python -m unittest tests/unit/test_runtime_health.py -v` green (its doctor fixture runs `main` with a fake HOME and still expects `required failures: 0` and `optional warnings: 3`: the new probe adds neither when the token is unset and the store is absent), and `git diff --numstat origin/main...HEAD`. Bats is not run locally (Test Policy): CI runs `bats -r tests/install/common/` through `scripts/run_unit_test.sh` (premise 2) and the RESULT names that run. Caps for this task: under 60 changed lines (added plus deleted) in `scripts/check-tools.sh`, under 120 in the bats module and under 10 in `tests/unit/test_runtime_health.py`, within the standing 200 outside `tests/` and `.orchestration/` (plan 021 step 7.2) and 1000 added under `tests/` (INV-2).

## Completion

One PR from a fresh branch off `origin/main`. PR #398 (`dotfiles-T129-assets-omp-hcom-followup-a01`, pending-integration) names both of this task's code files in its `allowed_files` although its diff touches neither (`git diff --stat origin/main...origin/tools/assets-hcom-receipt -- scripts/check-tools.sh tests/install/common/check_tools.bats` is empty on 2026-10-18); the Parallelism rule holds, so this branch rebases onto `origin/main` after #398 merges and before its RESULT (or starts after it). PR #394 (`dotfiles-T129-doctor-sleep-disabled-a01`, staged, first in the morning merge order) edits three other tests of `tests/unit/test_runtime_health.py`, none of them the doctor fixture item 3 touches; its worker is finished, so the two edits are not concurrent, and this branch rebases onto `origin/main` after #394 merges and before its RESULT (or starts after it), as for #398; that holds only while #394 opens no further fix round on that module, else this task waits for its merge; a textual conflict is a `PONG status=blocked`, never a hand merge. No other open task names these files (the grep of 2026-10-18 in the orchestrator's notes). The Completion clause of `.orchestration/tasks/dotfiles-T129-anthropic-auth-route-check-a01.md` applies as written, with `dotfiles-T129-anthropic-auth-runtime-check-followup-a01` as the owner of any advisory P2 (written by the orchestrator when the first one appears, before the PR's dispositions, C-51) and `task_copy=<sha256 of .orchestration/dotfiles-T129-anthropic-auth-runtime-check-a01/task.md>` in the RESULT, which also names the bats test and whether CI ran or skipped runs (c) and (d).

## VERIFY (the orchestrator closes each before dispatch; a closed item becomes Amendment 1 text, an open one a decided default)

- VERIFY 1 (closed 2026-10-17T17:5xZ by the orchestrator, no amendment; round 1 of the review asked for the columns and the literals): the store is `~/.omp/agent/agent.db` (`getAgentDbPath()` of `@oh-my-pi/pi-utils`; `.tables` on the orchestrator's Mac lists `auth_credentials`, `auth_credential_blocks`, `auth_credential_refresh_leases`, `auth_credential_block_mirror_guard`, `auth_change_revision`, `auth_schema_version`, read as table names only; the column-level `.schema` of the live store was refused by the auto-mode classifier as credential exploration and is never read). The pinned source, `https://raw.githubusercontent.com/can1357/oh-my-pi/v18.11.3/packages/ai/src/auth/sqlite-credential-store.ts` (the tag of `assets.omp` pin 18.11.3; WebFetch output pasted in the acceptance record), defines `CREATE TABLE IF NOT EXISTS auth_credentials (id INTEGER PRIMARY KEY AUTOINCREMENT, provider TEXT NOT NULL, credential_type TEXT NOT NULL, data TEXT NOT NULL, disabled_cause TEXT DEFAULT NULL, identity_key TEXT DEFAULT NULL, created_at INTEGER NOT NULL DEFAULT (CAST(strftime('%s','now') AS INTEGER)), updated_at INTEGER NOT NULL DEFAULT (CAST(strftime('%s','now') AS INTEGER)))` and stores `credential_type` as `"api_key"` or `"oauth"` (`serializeCredential`, `deserializeCredential`). VERIFY 1b (the worker, before writing the query): the Anthropic provider identifier is not in that file (it comes from the imported `Provider` type); the literal is `anthropic` (plan 023 B names the `anthropic` provider: the decided default); the worker confirms it from the same pinned tree through the WebFetch tool on a raw GitHub path under `packages/ai/src/` (the provider registry; never the npm tarball, a 14.7 MB archive WebFetch cannot read, and never `curl`), pastes the defining line in report.md or states that no file confirmed it, and uses the literal in the query and the fixtures; only a contradiction (the pinned tree naming Anthropic differently, or defining the table differently from the statement above) stops the worker with `AGMSG-PONG v1 status=question` naming what it read, for the orchestrator to decide.
- VERIFY 2: whether `PI_CODING_AGENT_DIR` replaces `~/.omp/agent` or `~/.omp` (plan 023 facts line 15 says only "moves it"). Default: it replaces `~/.omp/agent`, as item 1 writes.
- VERIFY 3: omp's command for removing a provider login (the failure hint). Default: the hint names no command ("remove the Anthropic login in omp").
- VERIFY 4: omp is not installed on the orchestrator's Mac today (`~/.local/bin/omp` is a dangling symlink into a Tern install; the operator's `make update` after PR A is pending), so `omp --help` and `omp auth --help` were not consulted. After that `make update`, check whether omp offers a read-only listing of its logins; if it does, Amendment 1 may replace the sqlite3 query with it and run (c) and (d) against a stub `omp` as `check_omp`'s test stubs the binary.
- VERIFY 5: `sqlite3` on the `ubuntu-latest` runner of the test workflow (macOS has `/usr/bin/sqlite3`; `herdr-agents` already requires it on managed machines). The skip guard in item 2 makes this informational.

## Checks (pasted by the orchestrator before each send)

```
dotfiles-T129-anthropic-auth-runtime-check-a01.md: <pending>
premise 1: <pending>
premise 2: <pending>
masked <n> match(es) in .orchestration/tasks/dotfiles-T129-anthropic-auth-runtime-check-a01.md
```
