# U251b round 2 of U251: every write root named and denied, no dsh execution outside srt, an atomic settings file, strict modes, the missing failure injections, the threat table

GOAL
The Codex audit of PR 687 at aa0001bd (`verdicts/U251-aa0001bd.md`, 08:2xZ) returned `incorrect` on three P1 and four P2, all in `scripts/orchestrator/dsh-srt` and its tests. P1 (f10 s6, `:296`): srt 0.0.81 itself adds writable `/tmp/claude`, `/private/tmp/claude` and `~/.npm/_logs`, none denied, so the promised confinement to three write roots does not hold. P1 (f2 s10, `:214`): the launcher executes `<DSH_HOME>/bin/dsh --version` outside containment to check the runtime, so a dsh that replaced its own binary from inside the sandbox runs host code on the next launch (reproduced with a fake runtime). P1 (f2 s10, `:297`): the settings file is written through a predictable `settings.tmp` path by redirection, which follows a planted symlink and overwrites its target before containment (reproduced). P2 (f2 s8, `:194`): existing sandbox, scratch and Claude-state directories at mode 0777 pass the ownership check unchanged. P2 (f10 s3, `:333`): `env -i` runs before srt, and srt adds its own runtime and proxy variables and replaces `TMPDIR` with `/tmp/claude`, so the real dsh environment is not what the Contract and the fake-runtime test assert. P2 (f10 s4, `test_dsh_srt.py:316`): no failure injection for the JSON-reader failure, the canary-process failure and a probe-leftover file (the eight tests pass with those guards removed). P2 (f10 s3): the body's threat table lacks the mandated form. This round closes all seven at one head.

SCOPE
Continue on branch `feat/dsh-srt-profile` from its head aa0001bdc1336496d5b9ac339d1477d8c498ea6b in the tree `/tmp/dotfiles-wt/U251` (clean, idle). May write: `scripts/orchestrator/dsh-srt`, its deployed copy `home/dot_local/bin/common/executable_dsh-srt` (identical), `tests/unit/test_dsh_srt.py`, the pin row in `home/dot_agents/agent-config.yaml` and `scripts/generated-agent-outputs.json` (regenerated), `docs/deepseek-harness.md` (the paragraph), and the body `../U251-pr-body.md` (amend: the threat table in the mandated form, `## Round 2`, Verification). Not: `hcom-seat`, the plugin, the profile rows.

CONTEXT
`hcom-seat` faces the same srt 0.0.81 facts; read how it treats the srt-added write paths and `TMPDIR` (`scripts/orchestrator/hcom-seat:1349-1760`, grep `claude` under `/tmp`, `_logs`, `TMPDIR`) and copy its answer with the citation, or state why DSH differs. The sandbox-runtime's own settings schema (`~/.local/lib/node_modules/@anthropic-ai/sandbox-runtime`, README and `src/` for `denyWrite`, the defaults it adds, and the environment it injects) is the source for the exact paths and names. The lever's existing structure: the table of lists at the top, `render_settings`, the ownership check, the canary, the exec.

DATA SHAPE
Five changes to the same shape. (1) Write roots: the table gains a `deny_write` row for every path srt adds by default that the kit does not want (`/tmp/claude`, `/private/tmp/claude`, `~/.npm/_logs`, and any other the schema reveals), or, where srt needs one of them to run at all, the Contract names it as the fourth root with the reason; the Contract and the table agree. (2) Runtime: the launcher never executes anything from `DSH_HOME` or the scratch root outside srt; the pre-check becomes a stat (regular file, this user's, mode without group or other write, under `home_real`) and the version is read under srt as the first contained command, or not at all. (3) Settings file: written into a directory the launcher creates with mode 0700 (`mkdir -m 0700`, refused if it exists with another mode or owner), through `mktemp` in that directory (unpredictable name, O_EXCL), then `mv` onto the final name; the final name is refused if it exists and is not a regular file of this user. (4) Modes: every directory the launcher relies on (sandbox, scratch, Claude state) is created 0700 and, when it exists, refused unless owner is this user and mode has no group or other bits (`stat -f %Lp` on macOS, `stat -c %a` on Linux; the repository has a helper for both, find it). (5) Environment: the Contract says what srt adds (its runtime and proxy variables, `TMPDIR=/tmp/claude` or whatever the schema says) and the launcher passes its reduced list to srt; the test asserts the names the launcher passes to `srt` (the fake srt records them) and separately documents the names srt itself adds, read from the schema, not asserted as absent. Tests gain the three missing failure injections: a JSON reader (`python3`) that exits non-zero, a canary process that exits non-zero or prints another line, and a probe-leftover file present after the canary; each must refuse with exit 2 and start nothing; plus the replaced-runtime case (a dsh binary that is writable by group, or a symlink, is refused before anything runs), the 0777 directory case, and the planted `settings.tmp` symlink case (nothing outside the sandbox directory changes).

CHANGE
1. The lever per DATA SHAPE (1) to (5); shdoc header and the table citations updated; `lever_self_check` unchanged.
2. Tests per DATA SHAPE; the eight existing tests stay or are retargeted; the auditor's mutation claim (guards removed, tests still pass) must fail now: paste one run with the JSON guard removed in a scratch copy showing the new test failing.
3. Deployed copy identical; pin regenerated; `make render-check` clean.
4. The body: `## Threat table` in the `AGENTS.md:70` form (row | risk | status | evidence; every changed path, every list as a non-path control, the orchestrator effects: the exec under srt, the environment, the write roots), the Contract corrected (the write roots as they really are, the environment srt adds), `## Round 2` naming the seven findings and their closing forms (`fixed: <sha>`), Verification re-run.

ACCEPTANCE
1. `uv run python -m unittest tests.unit.test_dsh_srt tests.unit.test_scratch_git tests.unit.test_generate_agent_configs` OK (paste the count; the new tests named).
2. `make shellcheck` exit 0; `scripts/ci/run-on-lint-files.sh shell shfmt -i 4 -sr -d` exit 0; `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check` exit 0; `scripts/ci/run-on-lint-files.sh markdown prettier --check` exit 0.
3. `cmp scripts/orchestrator/dsh-srt home/dot_local/bin/common/executable_dsh-srt` exit 0; `uv run --with pyyaml scripts/generate-agent-configs.py && make render-check` exit 0.
4. Under real srt with a scratch `DSH_HOME` under `/tmp` (as in round 1): `-- --version` prints `0.2.1-rc.5`; the canary words; a write to `/tmp/claude/u251b` and to `~/.npm/_logs/u251b` from inside (`-- bash -c` form, or the canary form) is denied or, if the Contract names one as a root, lands there and nowhere else; paste each.
5. The mutation run of CHANGE 2 pasted.
6. `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed` exit 0.

VERIFY
ACCEPTANCE pasted into the body's Verification section (round-2 lines).

CLOSURE
allowlist

TRUST
TRUST: the unit trusts srt 0.0.81's documented settings schema and defaults and `hcom-seat`'s answers to the same facts as the reviewed containment; it reads no credential, opens no network of its own, changes no seat lever and does not decide the profile rows or the plugin.

TIMEBOX
75 minutes.

FORBIDDEN
No edit of `hcom-seat`, the plugin or the profile rows; no `/v1/messages` request to the real omp; no read of credential files beyond the measured denial; no write under `~/.dsh`, `~/.omp`, `~/.agents` or `~/Workspace`; no `allowNestedUserNamespaces`; no local bats; no network; no push; no `gh` call; no pipe `|` in any bash command (standing order 46: output to a file under `/tmp/u251b/`, then read it).

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 58)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/tmp/dotfiles-wt/U251` and the coordinator fetches it by path.
- Progress line beside your tree (`../U251b-progress.txt`) every ten minutes at most; first edit within ten minutes.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Comments explain a non-obvious why only, no phase narration. Shell comments are English shdoc.
- Follow `~/.agents/pstack/skills/poteto-mode/SKILL.md` (Boundary Discipline; Make Operations Idempotent).

REPORT
Status, head sha (40 hex), files changed (`git diff --stat aa0001bd`), the ACCEPTANCE result lines, deviations. Under 14 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 27, 29, 34, 35, 37, 41, 44, 45, 46); `AGENTS.md:70-72`; `verdicts/U251-aa0001bd.md`; `briefs/U251-dsh-runs-under-srt-by-a-kit-launcher.md`.
