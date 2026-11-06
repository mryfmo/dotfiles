# U276 `make deploy-kit`: the kit's own paths deployed by the coordinator, the operator's host state untouched

GOAL
Every lever that landed on main today (pr-merge gate for all units, brief-check CI gate, the graphify asset, the thak profile rows, the hcom-seat roles) reaches the laptop only through `make update`, which standing order 30 makes an operator handout because `chezmoi apply` is whole-home: the G-26 gate records that a full apply would drop the operator's live Codex allow rules and the Codex app's notify line (two-sided drift), and `update` also upgrades tools and reloads herdr. The operator asked (2026-11-06, order 48) that human work be cut to what only a human can do. This unit adds `make deploy-kit`: a chezmoi apply scoped to the kit's own target paths, refusing when any of those targets carries local edits, followed by `./scripts/update-agent-assets.sh`. The coordinator can then deploy a merged unit itself under order 30's existing letter (`chezmoi apply --exclude=scripts` and `update-agent-assets.sh` are already agent-runnable; this is a narrower subset of the first), and `make update` stays the operator's periodic whole-home step.

SCOPE
A new branch `feat/make-deploy-kit` from `origin/main` (your tree is `/tmp/dotfiles-wt/U276`). May write: `Makefile` (the target and its help line), a new `scripts/deploy-kit.sh` (the logic, so it is testable and shellcheck-covered), `tests/unit/test_deploy_kit.py`, `README.md` (one paragraph beside `make update`), `docs/` only if a document already describes `make update` (then one paragraph there), and the body `../U276-pr-body.md`. Not: `chezmoi` source files under `home/`, the `update` target's behaviour, any host file.

CONTEXT
`Makefile` `update` and `update-tree` (read them whole): pull, externals prefetch, `chezmoi apply --verbose`, private source apply, `upgrade-tools.sh`, `update-agent-assets.sh`, herdr reload. `chezmoi apply [target]...` applies only the named targets (verify in `chezmoi apply --help` on this host); `chezmoi managed --path-style absolute` lists every managed target; `chezmoi status` or `chezmoi diff <target>` shows drift per target; `chezmoi verify <target>` exits non-zero when the target differs from the source state. The kit's paths are the targets under `~/.local/bin`, `~/.agents`, `~/.dsh`, `~/.config/chezmoi` is not one, and the Codex, Claude Code and shell rc targets are the operator's; read `home/` top-level entries and the manifest `home/dot_agents/agent-config.yaml` to settle the list and state it as a table in the script header and the body. Order 21 (fail closed on every producer) applies to every `chezmoi` call the script reads.

DATA SHAPE
A fixed table of kit target roots in `scripts/deploy-kit.sh` (one array, each an absolute path under `$HOME`, with a one-word reason column in the header comment). The script: (1) lists managed targets under those roots (`chezmoi managed --path-style absolute`, filtered by the roots, status checked); (2) for each, `chezmoi verify` against the source; a target that differs is `pending`; (3) refuses if a pending target has local edits the source does not have (two-sided drift: the target's current content differs from both the last-applied state and the source; chezmoi's `status` first column `M` with second column `M` is that case, confirm on this host) and prints the paths; (4) applies the pending targets by name (`chezmoi apply --verbose <targets>`), then runs `./scripts/update-agent-assets.sh`; (5) prints the applied list and exits 0; `--dry-run` prints the pending list and the refusals without applying. A `make deploy-kit` target runs the script; `make deploy-kit DRY=1` passes `--dry-run`.

CHANGE
1. The script per DATA SHAPE, shdoc header rows, every chezmoi read status-checked (order 21), no pipe between a producer and a decision without `set -o pipefail` and the status read.
2. The Makefile target and help line; the README paragraph.
3. Tests with a fake `chezmoi` on PATH (a recorder script) covering: the filter to kit roots, a pending target applied by name, a two-sided drift refused with the path printed, a failing `chezmoi managed` refuses (failure injection, order 21), `--dry-run` applies nothing, `update-agent-assets.sh` runs only after a successful apply.
4. Measurement on this host, read-only: `scripts/deploy-kit.sh --dry-run` output pasted (the pending kit targets today, the refusals if any; this is the deploy the coordinator will run after merge).
5. The body: Summary, Contract (what the target guarantees: no target outside the kit roots is touched, two-sided drift refuses), Threat table (changed paths), Verification (ACCEPTANCE pasted).

ACCEPTANCE
1. `uv run python -m unittest tests.unit.test_deploy_kit` OK (paste the count).
2. `make shellcheck` exit 0; `scripts/ci/run-on-lint-files.sh shell shfmt -i 4 -sr -d` exit 0; `scripts/ci/run-on-lint-files.sh markdown prettier --check` exit 0; `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check` exit 0.
3. `make -n deploy-kit` prints the script invocation; `make -n deploy-kit DRY=1` prints it with `--dry-run`.
4. The CHANGE 4 dry-run output pasted.
5. `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed` exit 0.

VERIFY
ACCEPTANCE pasted into the body's Verification section. The coordinator runs `make deploy-kit` after the merge and records the applied list in `decisions.tsv`.

CLOSURE
allowlist

TRUST
TRUST: the unit trusts chezmoi's own verify and status as the drift oracle and the kit root table as the boundary; it applies nothing itself (the dry run is its only host read), reads no credential and opens no network.

TIMEBOX
60 minutes.

FORBIDDEN
No `chezmoi apply` without `--dry-run` on this host; no edit under `home/`; no change to the `update` target; no write under `~/.local`, `~/.agents`, `~/.dsh`, `~/.codex`, `~/.claude`; no local bats; no network; no push; no `gh` call; no pipe `|` in any bash command you run yourself (standing order 46: output to a file under `/tmp/u276/`, then read it); inside the script a pipe is allowed only with `set -o pipefail` and the status read.

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 62)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/tmp/dotfiles-wt/U276` and the coordinator fetches it by path.
- Progress line beside your tree (`../U276-progress.txt`) every ten minutes at most; first edit within ten minutes. Write your final report to `../U276-report.txt` before you end.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Comments explain a non-obvious why only, no phase narration. Shell comments are English shdoc.
- Follow `~/.agents/pstack/skills/poteto-mode/SKILL.md` (Boundary Discipline: the kit root table is the boundary; Make Operations Idempotent: a second run applies nothing and exits 0).

REPORT
Status, head sha (40 hex), files changed (`git diff --stat origin/main`), the kit root table in one line, the dry-run's pending count and refusals, the ACCEPTANCE result lines, deviations. Under 14 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 27, 29, 30, 34, 44, 46, 48); `gates.md` G-26; `AGENTS.md` (Test Policy); `Makefile` `update-tree`.
