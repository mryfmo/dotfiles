# U276b round 2 of U276: the asset step stays inside the kit boundary, every read fails closed, roots are physical

GOAL
The round-1 audit of PR 698 (U276, head 49108595; `verdicts/U276-49108595.md`) found two P1 and two P2. P1 f8: `make deploy-kit` ends by running `./scripts/update-agent-assets.sh` whole, whose `main` also converges Claude Code and Codex plugins, force-applies `~/.codex/*config.toml` (`refresh_codex_hook_trust`), installs herdr integrations and upgrades npm CLIs through mise; the auditor ran the real Codex modifier in a scratch HOME and it removed an operator notify line, the very G-26 drift the target exists to avoid. P1 f2: a failed here-string redirection in the status parsing block was read as an empty listing and the apply proceeded (fail-open, order 21). P2 f1: the kit roots are compared textually, so a root that is a symbolic link lets the apply write through it outside the boundary. P2 f2: `chezmoi managed` and `chezmoi status` without a target expand every external (fonts, Spacemacs) and can reach the network from a cold cache, in `--dry-run` too. P3: no failure injection for the `dirname` read. This round keeps the target's contract and closes all five.

SCOPE
The existing branch `feat/make-deploy-kit` at 491085954cbb16c1aac1b7bfd7ab2f477bfa1d36 in `/tmp/dotfiles-wt/U276` (the PR is 698). May write: `scripts/deploy-kit.sh`, `tests/unit/test_deploy_kit.py`, `scripts/update-agent-assets.sh` only to extend the single-function dispatch list in its `main` (the `case "$#:$1"` whitelist) with the kit functions this unit names, `README.md` (the deploy-kit paragraph), and the body `../U276-pr-body.md` (a Round 2 section). Not: the `update` target, any updater function's body, any `home/` file.

CONTEXT
Read the verdict's Findings and Reproduced sections whole, then `scripts/update-agent-assets.sh` `main` and each `update_*` function it calls, and classify every function by the paths it writes: inside the kit roots (`~/.local/bin`, `~/.agents`, `~/.dsh`, and the mise-managed install paths only if the kit root table includes them, which it does not) or outside (`~/.claude`, `~/.codex`, herdr, npm globals, mise tool installs). The updater already runs one function when called with its name (`1:update_pi_claude_bridge | 1:update_security_audit_skill | 1:update_deepseek_harness | ...`); the kit step of `deploy-kit` calls the updater once per kit function by name, never `main`. chezmoi: `chezmoi managed <target>...` and `chezmoi status <target>...` accept target paths and restrict their work to them (confirm on this host with `--help`); `chezmoi managed --exclude externals` exists too; the externals the kit roots contain, if any, are listed in the body. Physical roots: `cd -P` / `pwd -P` on each root, refuse a root whose physical path differs from its spelling (a link) or that is missing, and compare physical paths.

DATA SHAPE
Two tables in the script header and code: the kit root table (unchanged three roots, now physical) and the kit asset function table (the updater functions whose writes are inside the roots, each with its write path in the comment column). The status parsing reads chezmoi through a status-checked producer into a variable (`out=$(chezmoi status -- "${roots[@]}") || refuse`) and iterates the variable; no here-string, no process substitution without a status read. Every producer the script reads (managed, status, verify, dirname, pwd -P, the updater per function) refuses on a non-zero status with the producer named (order 21), and each has a failure-injection test.

CHANGE
1. The asset step per DATA SHAPE: the function table, the per-function updater calls, and the updater's whitelist extended with exactly those names; the body's Contract gains the sentence that `deploy-kit` never runs the updater's `main`.
2. Status parsing and every producer read fail closed; the `dirname` read included.
3. Physical roots and target-restricted chezmoi reads (`managed` and `status` with the roots as arguments; verify after apply with the applied names); a root that is a link, or missing, refuses with its path.
4. Tests, each with a recorder fake: the asset step calls the updater once per kit function by name and never without an argument; a here-string or producer failure refuses (inject by making the fake `chezmoi` exit 3 on `status`, and by a `dirname` stub that fails); a linked root refuses before any apply; `managed` and `status` are called with the three roots as arguments; the existing tests stay.
5. Measurement on this host, read-only: `scripts/deploy-kit.sh --dry-run` pasted; `scripts/update-agent-assets.sh` with each kit function name and `--help`-like misuse is NOT run (the functions write); instead paste the write-path classification table with the `file:line` of each function's writes. In a scratch HOME fixture (copy the operator's `~/.codex/config.toml` notify line form into it), run the round-1 script's asset step against the fake updater to show the old call shape, then the new step; the notify line stays in the new run (paste the diff of the fixture before and after).
6. The body's Round 2 section: the five findings quoted, each with its change and test; ACCEPTANCE pasted.

ACCEPTANCE
1. `uv run python -m unittest tests.unit.test_deploy_kit tests.unit.test_scratch_git` OK (paste the count; the new tests named).
2. `make shellcheck` exit 0; `scripts/ci/run-on-lint-files.sh shell shfmt -i 4 -sr -d` exit 0; `scripts/ci/run-on-lint-files.sh markdown prettier --check` exit 0; `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check` exit 0.
3. `grep -c '<<<' scripts/deploy-kit.sh` prints 0; `grep -nE 'update-agent-assets.sh"?\s*$' scripts/deploy-kit.sh` prints nothing (no bare call of the updater).
4. The CHANGE 5 measurements pasted.
5. `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed` exit 0.

VERIFY
ACCEPTANCE pasted into the body's Verification section. The coordinator runs `make deploy-kit` after the merge and records the applied list and the Codex config's unchanged digest in `decisions.tsv`.

CLOSURE
allowlist

TRUST
TRUST: the unit trusts chezmoi's target-restricted status as the drift oracle and the two tables as the boundary; it applies nothing on this host (dry run only), reads no credential and opens no network.

TIMEBOX
60 minutes.

FORBIDDEN
No `chezmoi apply` without `--dry-run` on this host; no run of any `update_*` function on this host; no edit under `home/`; no change to the `update` target or to any updater function body; no write under `~/.local`, `~/.agents`, `~/.dsh`, `~/.codex`, `~/.claude`; no local bats; no network; no push; no `gh` call; no pipe `|` in any bash command you run yourself (standing order 46: output to a file under `/tmp/u276b/`, then read it); inside the script a pipe only with `set -o pipefail` and the status read.

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 62)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/tmp/dotfiles-wt/U276` and the coordinator fetches it by path.
- Progress line at `../U276b-progress.txt` every ten minutes at most; first edit within ten minutes. Final report to `../U276b-report.txt` before you end.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Comments explain a non-obvious why only, no phase narration. Shell comments are English shdoc.
- Follow `~/.agents/pstack/skills/poteto-mode/SKILL.md` (Boundary Discipline; Fix Root Causes: the updater's whole-run shape is the cause, not the notify line).

REPORT
Status, head sha (40 hex), files changed (`git diff --stat origin/main`), the kit asset function table in one line, the dry-run's pending count, the fixture diff result, the ACCEPTANCE result lines, deviations. Under 14 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 27, 29, 30, 34, 44, 46, 48); `gates.md` G-26; `verdicts/U276-49108595.md`; `AGENTS.md` (Test Policy).
