# U227c round 3 of U227: the plugin link step resolves its paths physically, refuses an external plugin target, and never leaves the profile without its plugin

GOAL
The Codex audit of PR 686 at 385bd1a1 (`verdicts/U227b-385bd1a1.md`, 08:15Z) returned `correct` with three P2 on the updater's new link step in `scripts/update-agent-assets.sh` (U227b's CHANGE 3): (f1 s5, `:1973`) the relative link target `../../../plugins/omp-gateway` assumes `profiles/` sits physically under `DSH_HOME`; a symlinked `profiles/` parent passes the checks and leaves a dangling link with exit 0; (f1 s6, `:2032`) the `-d` check follows symlinks, so a `plugins/omp-gateway` that is itself a link to a directory outside `DSH_HOME` is accepted, and the body's threat row that claims the external-target closure is not established; (f2 s4, `:1973`) `ln -sfn` unlinks the existing link before it fails, so a failure between the unlink and the new link leaves the live profile without its plugin, and the failure-injection test injects only before the unlink. This round closes the three at one head.

SCOPE
Continue on branch `feat/dsh-profile-login-route` from its head 385bd1a1e169dc6f2fcef31f521036e69b6eb24d in the tree `/tmp/dotfiles-wt/U227b` (clean, idle). May write: `scripts/update-agent-assets.sh` (the link step only), `tests/unit/test_update_agent_assets.py`, and the body `../U227b-pr-body.md` (amend: the threat rows of the link step, a `## Round 3` section, Verification). Not: the generator, the manifest, the rendered profile, the plugin.

CONTEXT
The link step as U227b wrote it (`scripts/update-agent-assets.sh` around `:1960-2040`, read it whole): `mkdir -p <DSH_HOME>/profiles/thak/node_modules`, a `-d` check of `<DSH_HOME>/plugins/omp-gateway`, then `ln -sfn ../../../plugins/omp-gateway <DSH_HOME>/profiles/thak/node_modules/dsh-omp-gateway`, recorded in the receipt; the tests in `test_update_agent_assets.py` (U227b added four: created, idempotent, refused when the plugin directory is missing, relative target). The updater's transaction rules (U178 to U178d: a state is named after a failed step; nothing live is removed before its replacement exists) are the standard the auditor applied. The U240 plugin's real location after `chezmoi apply` is `~/.dsh/plugins/omp-gateway` (a real directory, `home/dot_dsh/plugins/omp-gateway/`), and `DSH_HOME` is `~/.dsh` by the kit's default.

DATA SHAPE
Three facts computed before any write, each by a physical path: `home_real` = `DSH_HOME` resolved (`cd -P`/`pwd -P` or `realpath`, status read), `plugin_real` = the plugin directory resolved the same way, `profile_modules_real` = the profile's `node_modules` directory resolved after `mkdir -p`. Refusals (exit 1, one line naming the path): `plugin_real` is not a directory, or does not start with `home_real/`; `profile_modules_real` does not start with `home_real/`. The link target is computed from the two physical paths (`realpath --relative-to` if available, else a shell-computed relative path from `profile_modules_real` to `plugin_real`, tested), so a symlinked `profiles/` parent gets a target that resolves. The write is atomic: `ln -s <target> <link>.tmp.$$` then `mv -T` (`mv -f` on macOS; the repository already handles both, find how) onto `<link>`, so a failure before the rename leaves the old link in place; an existing `<link>` that is not a symlink (a real directory or file) is a refusal naming it, never removed.

CHANGE
1. The link step per DATA SHAPE; the receipt records the physical target.
2. Tests: (a) a symlinked `profiles/` parent (the fixture's `DSH_HOME/profiles` a symlink to a directory elsewhere under the fixture) ends with a link that resolves to the plugin; (b) a `plugins/omp-gateway` that is a symlink to a directory outside `DSH_HOME` is refused with the path named, and nothing under the profile changed; (c) a failure injected at the rename (make the `node_modules` directory read-only, or stub `mv`) leaves the previous link intact and the step exit non-zero naming the state; (d) an existing real directory at the link name is refused and left alone; the four U227b tests stay.
3. The body: the threat rows of the link step rewritten with the new closures (test selectors); `## Round 3` naming the three findings (ids, lines) and `fixed: <sha>`.
4. The gates (ACCEPTANCE).

ACCEPTANCE
1. `uv run python -m unittest tests.unit.test_update_agent_assets tests.unit.test_scratch_git` OK (paste the count; the four new tests named).
2. `make shellcheck` exit 0; `scripts/ci/run-on-lint-files.sh shell shfmt -i 4 -sr -d` exit 0; `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check` exit 0; `scripts/ci/run-on-lint-files.sh markdown prettier --check` exit 0.
3. `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed` exit 0.
4. `make validate-agent-assets` exit 0 and `make render-check` exit 0 (nothing rendered changes).

VERIFY
ACCEPTANCE pasted into the body's Verification section (round-3 lines).

CLOSURE
allowlist

TRUST
TRUST: the unit trusts the physical path resolution of the shell and the updater's transaction rules as the standard; it reads no network, changes no rendered file and does not decide the plugin's location.

TIMEBOX
40 minutes.

FORBIDDEN
No change outside the link step and its tests; no `sudo`; no write under `~/.dsh`; no network; no push; no `gh` call; no pipe `|` in any bash command (standing order 46: output to a file under `/tmp/u227c/`, then read it).

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 58)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/tmp/dotfiles-wt/U227b` and the coordinator fetches it by path.
- Progress line beside your tree (`../U227c-progress.txt`) every ten minutes at most; first edit within ten minutes.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Comments explain a non-obvious why only, no phase narration. Shell comments are English shdoc.
- Follow `~/.agents/pstack/skills/poteto-mode/SKILL.md` (Make Operations Idempotent; Boundary Discipline).

REPORT
Status, head sha (40 hex), files changed (`git diff --stat 385bd1a1`), the ACCEPTANCE result lines, deviations. Under 12 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 27, 29, 34, 35, 37, 41, 44, 45, 46); `AGENTS.md`; `verdicts/U227b-385bd1a1.md`; `briefs/U227b-*.md`; `briefs/U178d-*.md` (the transaction rules).
