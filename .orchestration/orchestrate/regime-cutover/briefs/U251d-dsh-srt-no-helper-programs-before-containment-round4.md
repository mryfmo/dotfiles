# U251d round 4 of U251 under the mechanism-change row: no helper program runs before containment

GOAL
Three audits of PR 687 returned `incorrect` in one class (`verdicts/U251-aa0001bd.md`, `U251b-f46a72b8.md`, `U251c-d49a5349.md`): each round found a new way code under the caller's or another user's control ran before srt contained anything: the `dsh --version` probe, the srt interpreter resolved on the caller's PATH, the mise `python3` shim used as the JSON reader (round 3 P1 f1 s10, `:541`), group-writable helpers accepted by the owner rule (round 3 P1 f2 s10, `:330`), caller PATH entries not resolved physically (P2 f1 s3, `:451`), a traversable non-sticky ancestor (P2 f1 s10, `:359`), plus the owner_of failure injections missing (P2 f10 s4, `test_dsh_srt.py:804`) and the Linux fixture lacking bwrap, socat and rg (P2 f1 s4, `:170`). The mechanism-change row of 09:5xZ names the form: remove every helper program from the pre-containment path. This round is the last for this shape: a round-5 P1 of the class withdraws the launcher for a dsh mode inside `hcom-seat`.

SCOPE
Continue on branch `feat/dsh-srt-profile` from its head d49a53497501e2181228e6a818ad1aeb275880af in the tree `/tmp/dotfiles-wt/U251` (clean, idle). May write: `scripts/orchestrator/dsh-srt` and its deployed copy (identical), `tests/unit/test_dsh_srt.py`, the pin row in `home/dot_agents/agent-config.yaml` and `scripts/generated-agent-outputs.json` (regenerated), and the body `../U251-pr-body.md` (amend: Contract, threat table, `## Round 4`, Verification). Not: `hcom-seat`, the plugin, the profile rows, `docs/`.

DATA SHAPE
Before containment the launcher runs exactly two kinds of program: absolute system binaries from a fixed list (`/usr/bin/stat`, `/usr/bin/readlink`, `/bin/ls`, `/usr/bin/id`, `/bin/mkdir`, `/bin/rm`, `/usr/bin/mktemp`, `/bin/mv`; each existence-checked, root-owned and not group or other writable, checked with `/usr/bin/stat` itself as the first and only bootstrap trust), and the pinned `node` and `srt` pair as `hcom-seat` runs them. Nothing else: no `python3`, no `env`, no `head`, no `cut`, no `awk`, no program found on PATH. The settings file is rendered by bash string building from the table's constants into a directory the launcher created with `mkdir -m 0700` (refused if it existed), written with `set -o noclobber` into a `mktemp` name and renamed; its JSON shape is srt's to reject (srt refuses a malformed settings file and the launcher reads srt's status). Every pathname the launcher trusts (srt, node, their directories, each caller PATH entry handed to the inner dsh, `DSH_HOME`, the scratch root) is resolved physically (`cd -P`, `/usr/bin/readlink`), and the trust rule walks every ancestor up to `/`: each component owned by root or this user, no group or other write bit unless sticky with root owner (`/tmp` and `/private/tmp` style), else refusal naming the component. `owner_of` and every `stat` read fail closed (a non-zero status or an empty answer is a refusal, exit 2, nothing started), with a test per producer. The Linux test fixture provides fake `bwrap`, `socat` and `rg` so the Linux branch reaches the canary.

CHANGE
1. The lever per DATA SHAPE; the header's contract names the two kinds of pre-containment program and the ancestor rule; the table cites `hcom-seat`'s lines for the node and srt pinning.
2. Tests: the python3 removal (no `python3` in any argv the fake tools record), a planted interpreter named by a helper's shebang (no helper has one now: the test asserts the list is absolute system binaries), the group-writable helper case (a 0775 copy of `stat` first on PATH never runs: the launcher uses `/usr/bin/stat` by absolute path), the symlinked caller PATH entry pointing into `DSH_HOME/bin` (excluded after physical resolution), the traversable ancestor (a 0777 non-sticky parent under the fixture: refusal naming it), the `owner_of` and `stat` producer failures (one test each), the Linux fixture tools; the existing tests stay or are retargeted.
3. Deployed copy identical; pin regenerated; `make render-check` clean.
4. The body: Contract rewritten to the two kinds of program and the ancestor rule; the threat table row per changed path and per control; `## Round 4` naming the six findings with `fixed: <sha>` and the mechanism-change row; Verification re-run.

ACCEPTANCE
1. `uv run python -m unittest tests.unit.test_dsh_srt tests.unit.test_scratch_git tests.unit.test_generate_agent_configs` OK (paste the count; the new tests named).
2. `make shellcheck` exit 0; `scripts/ci/run-on-lint-files.sh shell shfmt -i 4 -sr -d` exit 0; `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check` exit 0; `scripts/ci/run-on-lint-files.sh markdown prettier --check` exit 0.
3. `cmp scripts/orchestrator/dsh-srt home/dot_local/bin/common/executable_dsh-srt` exit 0; `uv run --with pyyaml scripts/generate-agent-configs.py && make render-check` exit 0.
4. `grep -c 'python3' scripts/orchestrator/dsh-srt` prints 0 (or only inside the self-check that every lever shares: say which lines and why).
5. Under real srt with a scratch `DSH_HOME` under `/tmp` holding a planted `bin/node`, a planted `bin/python3` and a planted `bin/stat` (each writing a marker): `-- --version` prints `0.2.1-rc.5`, no marker appears, the canary answers; paste.
6. `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed` exit 0.

VERIFY
ACCEPTANCE pasted into the body's Verification section (round-4 lines).

CLOSURE
remove

TRUST
TRUST: the unit trusts the absolute system binaries of the fixed list (root-owned, checked by `/usr/bin/stat` as the bootstrap) and the pinned node and srt pair as `hcom-seat` runs them; it trusts nothing found on PATH before containment, reads no credential, opens no network of its own and changes no seat lever.

TIMEBOX
60 minutes.

FORBIDDEN
No `python3`, `env`, `head`, `cut`, `awk`, `sed` or any PATH-resolved program before containment; no edit of `hcom-seat`, the plugin, the profile rows or `docs/`; no write under `~/.dsh`, `~/.omp`, `~/.agents` or `~/Workspace`; no `allowNestedUserNamespaces`; no local bats; no network; no push; no `gh` call; no pipe `|` in any bash command (standing order 46: output to a file under `/tmp/u251d/`, then read it).

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 58)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/tmp/dotfiles-wt/U251` and the coordinator fetches it by path.
- Progress line beside your tree (`../U251d-progress.txt`) every ten minutes at most; first edit within ten minutes.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Comments explain a non-obvious why only, no phase narration. Shell comments are English shdoc.
- Follow `~/.agents/pstack/skills/poteto-mode/SKILL.md` (Subtract Before You Add; Boundary Discipline). Write your final report to `../U251d-report.txt` before you end.

REPORT
Status, head sha (40 hex), files changed (`git diff --stat d49a5349`), the ACCEPTANCE result lines, deviations. Under 12 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 27, 29, 33, 34, 35, 36, 37, 41, 44, 45, 46); `AGENTS.md:70-72`; the three verdicts; the `decisions.tsv` mechanism-change row for U251 of 2026-11-06T09:5xZ; `briefs/U251-*.md`, `U251b-*.md`, `U251c-*.md`.
