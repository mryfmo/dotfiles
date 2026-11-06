# U224e round 5: every `claude plugin` command of the retirement step names `--scope user`

GOAL
The U224 round-3 audit (`verdicts/U224-56985c89.md`, incorrect) found one P1: `claude plugin marketplace remove understand-anything` at `scripts/update-agent-assets.sh:2452` runs without `--scope`, and Claude Code 2.1.316 then removes the marketplace declaration from every scope, deleting project-scope and local-scope installation records (the auditor reproduced it in isolated fixtures; `claude plugin marketplace remove --help` says omitting `--scope` removes from every scope). That breaks the user-scope-only guarantee round 4 wrote into the Contract. The project-scope test used an absent marketplace and never reached the remove branch. This round makes every `claude plugin` command of the step carry `--scope user` (the mechanism-change row of 2026-11-06T05:05:50Z, closing form allowlist) and adds the test that reaches the branch. Nothing else changes.

SCOPE
The branch `feat/remove-understand-anything-graphify-in` in your tree, on top of 56985c89 (your HEAD). May write: `scripts/update-agent-assets.sh` (`retire_understand_anything` only), `tests/unit/test_update_agent_assets.py` (the retire tests), and the body file `/tmp/claude/U224/U224-pr-body.md`. Nothing else.

CONTEXT
`retire_understand_anything` at 56985c89 (`:2386-2486`): `claude plugin uninstall <id> --scope user` (`:2426`) and `claude plugin disable <id> --scope user` (`:2471`) already name the scope; `claude plugin marketplace remove <name>` (`:2452`) does not. The auditor's reproduction: an explicit `--scope user` removal refuses an undeclared user marketplace (exit non-zero), so the step must treat that refusal as its own precondition failing (the marketplace was not declared at user scope) and not as a destructive-command failure that fails the run: read `claude plugin marketplace list --json` for the scope field of the registered marketplace if the listing carries one (read the installed `claude plugin marketplace list --help` and the JSON shape in `tests/unit/claude_plugin_fixture.py`), and run the removal only when the declaration is at user scope; a declaration at another scope is a WARN naming the scope and left in place. The tests stub `claude` as a shell function recording its arguments.

CHANGE
1. `:2452`: `claude_outside_projects plugin marketplace remove "${marketplace}" --scope user`, run only when the registered declaration is at user scope (per CONTEXT); another scope is a WARN naming it and the removal does not run.
2. Tests: (a) a project-scope installation record beside a user-scope registered marketplace: the uninstall does not run, the remove call carries `--scope user`, the project record is untouched (assert the stubbed `installed_plugins.json` after the step equals before); (b) a marketplace declared at project scope only: no remove call, a WARN naming `project`; (c) the existing tests updated so every expected `marketplace remove` call carries `--scope user`; (d) a grep assertion over the function's text in the test module: every `claude_outside_projects plugin` call line within `retire_understand_anything` contains `--scope user` (the allowlist made checkable).
3. The body: a `## Round 5` section naming the P1, the reproduction and the fix; the step's threat row updated; ACCEPTANCE pasted.

ACCEPTANCE
1. `uv run python -m unittest tests.unit.test_update_agent_assets -k retire_understand_anything -v`: every test OK (paste the count and names).
2. `awk '/^function retire_understand_anything/,/^}/' scripts/update-agent-assets.sh | grep -n 'claude_outside_projects plugin' ` prints only lines containing `--scope user` (paste).
3. `uv run python -m unittest tests.unit.test_runtime_health -k gh_extension_ensure -v` OK.
4. `make shellcheck` exit 0; `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed` exit 0.
5. `git diff --stat 56985c89` names `scripts/update-agent-assets.sh` and `tests/unit/test_update_agent_assets.py` alone.

VERIFY
The ACCEPTANCE commands in your tree with their result lines pasted into the body.

CLOSURE
allowlist

TRUST
TRUST: the round trusts Claude Code's `claude plugin` commands and their documented `--scope` semantics at the installed version; the step names the user scope on every command, never edits the plugin records itself, and no other step changes.

TIMEBOX
25 minutes.

FORBIDDEN
No `claude plugin` command without `--scope user` in the step; no direct edit of `installed_plugins.json`, `settings.json` or `enabledPlugins`; no change to any other step; no amend of earlier commits; no local bats; no network read; no push; no `gh` call; no mention of any private design directory; none of the words in `.orchestration/orchestrate/regime-cutover/redact-words.txt` and no absolute home directory in tracked files or the PR body (write `~/...`).

WORKER RULES (standing orders 21, 27, 29, 31, 34; read `preferences.md` lines 23 to 46 in the store)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in your tree. Never `git stash`. Before you report, `git -C ~/Workspace/dotfiles status --porcelain=v1 --untracked-files=all -- . ':!.orchestration/orchestrate' | shasum` must print the value the TASK line carries.
- Progress line in `/tmp/claude/U224/U224-progress.txt`.
- Commit unsigned: `git -c commit.gpgsign=false commit`. The message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Comments explain a non-obvious why only.

REPORT
Status, head sha (40 hex), `git diff --stat 56985c89`, the ACCEPTANCE result lines, deviations. Under 10 lines, ending with `head=<40 hex>`.

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` (standing orders 21, 27, 29, 34, 35, 36); `verdicts/U224-56985c89.md`; the mechanism-change row of 2026-11-06T05:05:50Z; `briefs/U224d-retirement-step-fail-closed-and-ownership-first-round3.md`.
