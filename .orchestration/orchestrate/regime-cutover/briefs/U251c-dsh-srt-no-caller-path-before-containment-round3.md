# U251c round 3 of U251: nothing under DSH_HOME or the scratch root is executable before containment, the srt probe runs under the reduced environment, the missing failure injections, the table row

GOAL
The Codex audit of PR 687 at f46a72b8 (`verdicts/U251b-f46a72b8.md`, 09:0xZ) returned `incorrect` on one P1 and three P2. P1 (f2 s10, `dsh-srt:290`): the launcher checks srt's path but srt is a `/usr/bin/env node` script, so the interpreter resolves on the caller's PATH; with `DSH_HOME/bin` (or the scratch root) on PATH a planted `node` ran outside containment and wrote outside every declared write root before the canary (reproduced with the real installed srt). P2 (f10 s3, `:325`): the srt version probe runs before the environment reduction and receives the caller's variables (a planted `SECRET_OF_THE_CALLER` reached it), against the Contract's ENV_NAMES guarantee. P2 (f10 s4, `test_dsh_srt.py:545`): the new `stat` mode reads and the `readlink` trust checks have no failure-injection tests (failed or empty producer output). P2 (f10 s3): the threat table omits the changed path `tests/unit/test_generate_agent_configs.py`. This round closes the four at one head.

SCOPE
Continue on branch `feat/dsh-srt-profile` from its head f46a72b888efc6d638eb055466b2f1ea13e83c83 in the tree `/tmp/dotfiles-wt/U251` (clean, idle). May write: `scripts/orchestrator/dsh-srt` and its deployed copy (identical), `tests/unit/test_dsh_srt.py`, the pin row in `home/dot_agents/agent-config.yaml` and `scripts/generated-agent-outputs.json` (regenerated), and the body `../U251-pr-body.md` (amend: the table row, `## Round 3`, Verification). Not: `hcom-seat`, the plugin, the profile rows, `docs/`.

CONTEXT
How `hcom-seat` runs srt: it pins srt's path (`pin_exec srt`, `:1597-1600`) and builds the pane's PATH itself; read how it sets PATH and the environment for the `srt` invocation and whether it runs srt through an explicit interpreter (`node <srt.js>`) or with a PATH it composes. The launcher today: `lever_self_check`, the table of lists, `render_settings`, the ownership and mode checks, the srt line probe (`srt --version` under the caller's environment, `:325`), the canary, the `env -i ... srt --settings ...` exec (`:333` region). Node on this host: `~/.local/share/mise/shims/node` and the mise-installed binary; `which -a node` from the launcher's own PATH; srt's shebang (`head -1 "$(command -v srt)"`).

DATA SHAPE
One environment, built once, used for everything that runs. The launcher computes `RUN_PATH` before any external command: the directories of the pinned `srt` and of the `node` it resolves (both resolved physically with `pwd -P`, both refused when they sit under `DSH_HOME`, the scratch root or any path that is not root-owned or this user's with no group or other write), plus the system directories (`/usr/bin:/bin:/usr/sbin:/sbin`), and nothing from the caller's PATH. Every external command the launcher runs after that line (the srt line probe, the canary, the exec) runs as `env -i <ENV_NAMES from the caller, values copied> PATH=<RUN_PATH> <command>`; the srt line probe moves after the environment reduction, so it is the first command under the reduced environment. `srt` is invoked through its resolved interpreter explicitly (`<node_real> <srt_real>`) when its shebang is `/usr/bin/env node`, so no PATH lookup happens inside the sandbox launcher either. Tests gain: a planted `DSH_HOME/bin/node` and a planted `node` on the caller's PATH that must never run (a marker file that stays absent) while the launcher proceeds with the pinned interpreter; the probe's environment recorded by the fake srt holds only ENV_NAMES; `stat` and `readlink` producers that fail (exit non-zero) or print nothing refuse with exit 2 before anything runs.

CHANGE
1. The lever per DATA SHAPE; the header's contract sentence names the one environment and that nothing under `DSH_HOME` or the scratch root is executed before containment.
2. Tests per DATA SHAPE (the planted-interpreter cases, the probe environment, the four producer failure injections); the existing tests stay or are retargeted.
3. Deployed copy identical; pin regenerated; `make render-check` clean.
4. The body: the threat table gains the `tests/unit/test_generate_agent_configs.py` row (and any other changed path missing), `## Round 3` names the four findings with `fixed: <sha>`, Verification re-run.

ACCEPTANCE
1. `uv run python -m unittest tests.unit.test_dsh_srt tests.unit.test_scratch_git tests.unit.test_generate_agent_configs` OK (paste the count; the new tests named).
2. `make shellcheck` exit 0; `scripts/ci/run-on-lint-files.sh shell shfmt -i 4 -sr -d` exit 0; `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check` exit 0; `scripts/ci/run-on-lint-files.sh markdown prettier --check` exit 0.
3. `cmp scripts/orchestrator/dsh-srt home/dot_local/bin/common/executable_dsh-srt` exit 0; `uv run --with pyyaml scripts/generate-agent-configs.py && make render-check` exit 0.
4. Under real srt with a scratch `DSH_HOME` under `/tmp` that holds a planted `bin/node` (a script that writes a marker file): `-- --version` prints `0.2.1-rc.5`, the marker file stays absent, the canary words print; paste.
5. `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed` exit 0.

VERIFY
ACCEPTANCE pasted into the body's Verification section (round-3 lines).

CLOSURE
allowlist

TRUST
TRUST: the unit trusts the pinned srt and the node interpreter it resolves outside `DSH_HOME` as the only code that runs before containment, and `hcom-seat`'s PATH composition as the precedent; it reads no credential, opens no network of its own and changes no seat lever.

TIMEBOX
60 minutes.

FORBIDDEN
No edit of `hcom-seat`, the plugin, the profile rows or `docs/`; no `/v1/messages` request to the real omp; no write under `~/.dsh`, `~/.omp`, `~/.agents` or `~/Workspace`; no `allowNestedUserNamespaces`; no local bats; no network; no push; no `gh` call; no pipe `|` in any bash command (standing order 46: output to a file under `/tmp/u251c/`, then read it).

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 58)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/tmp/dotfiles-wt/U251` and the coordinator fetches it by path.
- Progress line beside your tree (`../U251c-progress.txt`) every ten minutes at most; first edit within ten minutes.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Comments explain a non-obvious why only, no phase narration. Shell comments are English shdoc.
- Follow `~/.agents/pstack/skills/poteto-mode/SKILL.md` (Boundary Discipline).

REPORT
Status, head sha (40 hex), files changed (`git diff --stat f46a72b8`), the ACCEPTANCE result lines, deviations. Under 12 lines, ending with `head=<40 hex>`. Write the report also to `../U251c-report.txt` before you end.

STANDING
`preferences.md` (standing orders 21, 27, 29, 34, 35, 37, 41, 44, 45, 46); `AGENTS.md:70-72`; `verdicts/U251-aa0001bd.md`, `verdicts/U251b-f46a72b8.md`; `briefs/U251-*.md`, `briefs/U251b-*.md`.
