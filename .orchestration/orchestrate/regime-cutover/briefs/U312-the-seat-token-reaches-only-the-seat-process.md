# U312 the seat token reaches only the seat process: no shell exports CLAUDE_CODE_OAUTH_TOKEN and no caller value is an input

GOAL
`~/.config/claude-code/oauth-token` is the kit's seat login (U37, U190, U190b): on `origin/main` 2b2415f6 the seat shim of `hcom-seat` gives every seat's child its own `CLAUDE_CONFIG_DIR` and reads the file's first line into `CLAUDE_CODE_OAUTH_TOKEN` when the caller has not set the variable (`home/dot_local/bin/common/executable_hcom-seat:2206-2215`, the guard at `:2208`), and `seat-login-preflight` refuses a host whose only Claude login is the Keychain (`home/dot_local/bin/common/executable_seat-login-preflight:276-301`). But `home/dot_zshenv:15-28` and `home/dot_profile:10-18` still export the file into every zsh and every login shell, so on a host that holds the file (the laptop since 2026-11-06 10:54 JST, measured) the operator's interactive Claude Code, every hook and every child process log in with the seat token instead of the claude.ai Keychain login and lose the claude.ai connectors (the operator's report of 2026-11-06T22:5xZ; decisions.tsv rows 22:5xZ and 23:08Z). A credential meant for one process is delivered to all of them, against the login-only frame (decisions.tsv 2026-11-06T05:46:33Z) and the sandbox clause of the goal. Design, closing form `remove`: the variable stops being an input anywhere in the kit. The rc exports go; the shim always reads the file; the dsh role stops forwarding a caller's variable (`:2443-2445`); the preflight's env branch (`:245-248`) retires. The file stays the one seat login on every host, read by the shim alone.

SCOPE
Branch `fix/seat-token-reaches-only-the-seat-process` from `origin/main`; the tree is `/tmp/dotfiles-wt/U312` (created by the coordinator). May write: `home/dot_zshenv`, `home/dot_profile`; `scripts/orchestrator/hcom-seat` and its generated copy `home/dot_local/bin/common/executable_hcom-seat` (byte-identical, regenerated); `home/dot_local/bin/common/executable_seat-login-preflight`; the lever pins by regeneration (`home/dot_agents/agent-config.yaml` sha256 rows under `claude.levers`, `scripts/generated-agent-outputs.json`); `tests/unit/test_remote_host_logins.py`, `tests/unit/test_hcom_seat.py`, `tests/unit/test_hcom_seat_dsh.py`, `tests/install/common/check_tools.bats` (the expectation text only; never run locally); `README.md:111-123` and `:716-720`, `docs/remote-host-logins.md` (the Claude row and the Pieces bullets on the rc files and the token file), `docs/pi-claude-bridge.md` (Operator login), `home/dot_agents/README.md:33`; the body `../U312-pr-body.md`. Not: the managed Claude settings deny of the variable and the file (`home/.chezmoitemplates/claude-settings-managed.json`, defence in depth, unchanged), `scripts/check-tools.sh`, the omp policies, any other lever.

CONTEXT
Read the shim text and its tests first: the shim exports the token into the seat's environment and the tests prove the value reaches omp, never stdout, stderr, the shim text or the settings (`tests/unit/test_hcom_seat.py:719-748`), that a caller's value wins today (`:750-759`, to invert), and that an unreadable file refuses (`:762-782`, to keep). The dsh role's environment list is explicit (`executable_hcom-seat:2267-2275`) and appends a caller's token at the real launch (`:2443-2445`); `tests/unit/test_hcom_seat_dsh.py:347-353` and `:448` assert that forward (to invert: the role passes the file's value through the same read as the omp roles, or nothing). The preflight's `claude_state` order on origin/main: env variable (`:245-248`), the token file as the shim reads it (`:249-275`), credentials file or Keychain, both `host login only`, return 1 (`:276-301`); the `@env` row at `:41` and the header at `:14` name the variable. `TokenExportTest` (`tests/unit/test_remote_host_logins.py:215-266`) asserts the rc exports; invert it to assert that no non-comment line of either rc file names the variable. The `env token` expectations at `:439-441`, `:656-658`, `:805-807` and `tests/install/common/check_tools.bats:182-185` become the token-file line. The herdr pane does not inherit the caller's environment (hcom 0.7.31 `terminal.rs:2368-2399`; HCOM_TEAM measured absent), which is why the shim, not the shell, is the only place the token can be delivered to a seat; the rc export never served the seat and only ever served every other process.

DATA SHAPE
One source of the seat token, the 0600 file, read by one reader, the seat shim, into one consumer, the seat's child process environment. The variable has no other producer in the kit: no rc file, no caller passthrough, no preflight branch. A test per former producer asserts its absence, and the shim's existing tests prove the delivery.

CHANGE
1. `home/dot_zshenv:15-28` and `home/dot_profile:10-18`: delete the export blocks and their comments.
2. `scripts/orchestrator/hcom-seat`: in the shim drop the caller-set guard so the file always wins (`:2208`); delete the dsh forward of the caller's variable (`:2443-2445`) and route the dsh role through the same file read if the role's child needs the login (measure: the gateway child under `OMP_PROFILE=dsh` is an omp process, so it needs it); update the header (`:106-107`, `:2257`). Regenerate the copy and the pins (`uv run --with pyyaml scripts/generate-agent-configs.py`).
3. `executable_seat-login-preflight`: retire the env branch (`:245-248`), the `@env` row (`:41`) and the header sentence (`:14`); the file branch, credentials and Keychain branches unchanged.
4. Tests as CONTEXT names: the inverted rc test, the inverted caller-wins test, the dsh forward tests, the preflight expectations, the bats expectation text.
5. Docs: README (the Ubuntu login paragraph and the sandbox sentence), `docs/remote-host-logins.md`, `docs/pi-claude-bridge.md` Operator login, `home/dot_agents/README.md:33`: the token file is the seat login on every host and only the seat shim reads it; interactive Claude Code uses the Keychain on macOS or its own credentials file; no shell exports the token.
6. The body: Summary (the operator's symptom and the measured cause), Contract (the one-source one-reader one-consumer sentence; Left out: the managed-settings deny unchanged; the file's placement stays the operator's), Threat table `row | risk | status | evidence` with one row per changed path, one for the shim's read (an unreadable or empty file refuses, the existing test), one for the orchestrator effect (a laptop without the file refuses seat launches, by design, named in the README), Verification (ACCEPTANCE pasted).

ACCEPTANCE
1. `uv run python -m unittest tests.unit.test_hcom_seat tests.unit.test_hcom_seat_dsh tests.unit.test_remote_host_logins tests.unit.test_generate_agent_configs tests.unit.test_scratch_git -v` OK (counts pasted; the inverted tests named).
2. `cmp scripts/orchestrator/hcom-seat home/dot_local/bin/common/executable_hcom-seat` exit 0; `make render-check` exit 0; `uv run --with pyyaml scripts/validate-agent-assets.py` exit 0.
3. `make shellcheck` exit 0; `scripts/ci/run-on-lint-files.sh shell shfmt -i 4 -sr -d` exit 0; `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check` exit 0; `scripts/ci/run-on-lint-files.sh markdown prettier --check` exit 0.
4. `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed` exit 0.
5. `zsh -f -c 'source home/dot_zshenv; print -r -- "${CLAUDE_CODE_OAUTH_TOKEN-unset}"'` under a scratch HOME that holds a fake token file prints `unset`; the same for `home/dot_profile` under bash (pasted).
6. `grep -n CLAUDE_CODE_OAUTH_TOKEN home/dot_zshenv home/dot_profile home/dot_local/bin/common/executable_seat-login-preflight` prints nothing (pasted); in `executable_hcom-seat` the only remaining producer is the shim's file read (the lines pasted).

VERIFY
ACCEPTANCE pasted into the body's Verification section. After the merge the coordinator deploys with `make update` on the laptop (order 30), opens a new shell and measures `printenv CLAUDE_CODE_OAUTH_TOKEN` empty, `seat-login-preflight --check` naming the token file, o14 and d21 of the test tables, and one seat launch.

CLOSURE
remove

TRUST
TRUST: the unit trusts the operator's 0600 token file as the seat login and the seat shim as its one reader; it never prints, logs or copies the token, reads no other credential, changes no deny of the managed settings, and widens no seat's boundary.

TIMEBOX
75 minutes.

FORBIDDEN
No read of the real token file's contents or of any credential store; no write under the real `~/.omp`, `~/.dsh`, `~/.agents`, `~/.local`, `~/Workspace`; no seat launch; no local bats; no network; no push; no `gh` call; no pipe `|` in any bash command (standing order 46: output to a file under `/tmp/u312/`, then read it).

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 62)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/tmp/dotfiles-wt/U312` and the coordinator fetches it by path.
- Progress line at `../U312-progress.txt` after every step; first edit within ten minutes. Final report to `../U312-report.txt` before you end.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Comments explain a non-obvious why only; shell comments are English shdoc.
- Follow `~/.agents/pstack/skills/poteto-mode/SKILL.md` (Boundary Discipline: one reader at the boundary; Subtract Before You Add: producers deleted, nothing added).

REPORT
Status, head sha (40 hex), files changed (`git diff --stat` against the merge base, no fetch), how the dsh role's child gets the login after the change, the ACCEPTANCE result lines, deviations. Under 12 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 27, 29, 30, 34, 41, 42, 44, 46, 47); `decisions.tsv` 2026-11-06T22:5xZ and 23:08Z; `briefs/U190*.md` and `briefs/U37*.md` if present; `docs/remote-host-logins.md`; `AGENTS.md` Audit (trust boundary: credentials).
