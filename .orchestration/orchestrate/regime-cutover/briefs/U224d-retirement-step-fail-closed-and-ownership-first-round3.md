# U224d round 4: the retirement step tolerates a host without a working `claude` the way its neighbours do, checks ownership before it uninstalls, handles user scope only, and clears a stale enabled entry

GOAL
Three inputs on `retire_understand_anything` (U224c, head 7992f1f5). (1) CI on that head: the `test (ubuntu-24.04)` legs fail in `test_runtime_health.test_agent_asset_update_runs_gh_extension_ensure` (`AssertionError: 0 != 1 : mise ERROR claude is not a valid shim`) and `public-bootstrap (ubuntu-24.04, client)` fails in `06-install-agent-assets.sh` with `ERROR: claude plugin marketplace list --json failed; the understand-anything marketplace is not retired.` On a fresh host `claude` is a mise shim with no version yet, and every neighbouring plugin step treats that as a WARN (`was not installed: its marketplace cannot be verified on this host ... Run make update once "claude plugin marketplace list" works`) and exits 0; the new step returned 1 and failed the whole apply. (2) The round-2 audit (`verdicts/U224-7992f1f5.md`, correct): [f10 s2] no failure-injection test for a failing or malformed `marketplace list` or a failing `marketplace remove`; [f1 s5] ownership is checked after the uninstall, so a same-name plugin from another marketplace is uninstalled first; [f1 s3] with no installation and no marketplace record but a stale `enabledPlugins` entry, the step reports success and leaves the key. (3) The sweep of that head (`sweeps/U224-7992f1f5/summary.txt`, candidate `retire-understand-anything:project-scope-cwd`): for a project-scope record the step runs `claude` inside the recorded project directory, outside the kit's user-scope boundary. This round makes the step converge on a host where `claude` works, warn and change nothing where it does not, act on user scope only, check ownership first, clear a stale enabled entry through the documented command, and test every one of those decisions.

SCOPE
The branch `feat/remove-understand-anything-graphify-in-r3` in your tree, on top of 7992f1f5 (your HEAD; the coordinator pushes your head onto the pull request's branch). May write: `scripts/update-agent-assets.sh` (`retire_understand_anything` only), `tests/unit/test_update_agent_assets.py` (the retire tests), and the body file `/tmp/claude/U224/U224-pr-body.md` (the current body of PR 673 is there). Nothing else.

CONTEXT
`retire_understand_anything` at 7992f1f5 (`scripts/update-agent-assets.sh`, the function and its call in the retire group of `main()`); the neighbouring WARN form is in the plugin steps (search `cannot be verified on this host`). Claude Code's commands (code.claude.com/docs/en/plugins/install, read 2026-11-06): `claude plugin marketplace remove <name>` uninstalls every plugin installed from that marketplace and removes their `enabledPlugins` entries; `claude plugin uninstall <id>` acts on user scope by default; `claude plugin disable <id>` acts on the most specific scope whose settings list the plugin. The step must not edit `installed_plugins.json` or `settings.json` itself. `claude_plugin_installs <id>` prints `<scope>\t<version>\t<project path>` lines and exits 1 on an unparsable file. The tests stub `claude` as a shell function writing its arguments to a calls file; `test_runtime_health` runs the whole updater with its own fake `claude` (`FAKE_MARKETPLACE_LIST`), so the step's reads must accept that fake's answers (a `plugin marketplace list` without `--json` returning the fixture listing) or treat an unexpected shape as the WARN case, never as exit 1.

CHANGE
1. Order and shape. First `command -v claude` (absent: one skip line, return 0). Then `claude plugin marketplace list --json` once: a non-zero exit or an output that is not a JSON array of objects with a `name` field is the WARN case: print one WARN in the neighbours' form naming the command and that the retirement waits for the next `make update`, run no destructive command, return 0. From a good listing decide whether `understand-anything` is registered.
2. Ownership and scope. Read `claude_plugin_installs understand-anything@understand-anything` (an unparsable file: return 1 naming the file, no destructive command). For each `user` record whose id's marketplace suffix is a registered marketplace of that name, run `claude plugin uninstall understand-anything@understand-anything` (user scope, the default). A `project` or `local` record is not acted on: one WARN naming the scope and the project path, left to the operator (the kit's boundary is user scope; the sweep candidate). A same-name plugin whose marketplace is not `understand-anything` is left alone with a WARN naming the marketplace.
3. Marketplace. When the listing names `understand-anything`, run `claude plugin marketplace remove understand-anything`; a non-zero exit returns 1 naming the command (the uninstalls before it stand).
4. Stale enabled entry. When no user record and no marketplace were present, read `claude plugin list` (the shell form; cite its output shape from the doc page or the installed `claude plugin list --help`) and, when it lists `understand-anything@understand-anything` as enabled, run `claude plugin disable understand-anything@understand-anything`; a non-zero exit returns 1. Print `already retired` only when the three reads found nothing.
5. Tests, each with the stubbed `claude`: (a) list exits non-zero: WARN line, exit 0, no uninstall, remove or disable call; (b) list prints a non-JSON line: the same; (c) a user record and a registered marketplace: uninstall then remove, in that order; (d) remove exits non-zero: exit 1 after the uninstall; (e) a `project` record: no uninstall, a WARN naming the project path, exit 0; (f) a user record whose marketplace is `other` and `other` registered: no uninstall, a WARN naming `other`; (g) nothing installed, no marketplace, `plugin list` shows the plugin enabled: one `disable` call, exit 0; (h) nothing anywhere: `already retired`, exit 0; (i) unparsable `installed_plugins.json`: exit 1 naming the file, no `claude` call after the list. Run `tests.unit.test_runtime_health -k gh_extension_ensure` to show the whole-updater test passes with the fixture `claude`.
6. The body: a `## Round 4` section naming the CI failures, the three audit findings and the sweep candidate with the fix for each; the step's threat row updated; ACCEPTANCE pasted.

ACCEPTANCE
1. `uv run python -m unittest tests.unit.test_update_agent_assets -k retire_understand_anything -v`: nine or more tests OK (paste the names).
2. `uv run python -m unittest tests.unit.test_runtime_health -k gh_extension_ensure -v`: OK (paste).
3. `make shellcheck` exit 0; `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed` exit 0.
4. `git diff --stat 7992f1f5` names `scripts/update-agent-assets.sh` and `tests/unit/test_update_agent_assets.py` alone.
5. `grep -c 'ERROR: claude plugin marketplace list' scripts/update-agent-assets.sh` prints 0 (the list failure is a WARN now).

VERIFY
The ACCEPTANCE commands in your tree with their result lines pasted into the body. The CI legs on the new head are the full-suite evidence (the coordinator reads them).

CLOSURE
allowlist

TRUST
TRUST: the round trusts Claude Code's `claude plugin` commands as the owner of the plugin records and their documented behaviour at the installed version, and the neighbouring plugin steps' WARN form as the kit's rule for a host without a working `claude`; the step never edits those files itself, every read is checked for status and shape before a destructive command, it acts on user scope only, and no other step changes.

TIMEBOX
45 minutes.

FORBIDDEN
No direct edit of `installed_plugins.json`, `settings.json` or `enabledPlugins` by the step; no `cd` into a recorded project path; no change to any other step; no amend of earlier commits; no local bats; no network read; no push; no `gh` call; no mention of any private design directory; none of the words in `.orchestration/orchestrate/regime-cutover/redact-words.txt` and no absolute home directory in tracked files or the PR body (write `~/...`).

WORKER RULES (standing orders 21, 27, 29, 31, 34; read `preferences.md` lines 23 to 46 in the store)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in your tree. Never `git stash`. Before you report, `git -C ~/Workspace/dotfiles status --porcelain=v1 --untracked-files=all -- . ':!.orchestration/orchestrate' | shasum` must print the value the TASK line carries.
- Progress line in `/tmp/claude/U224/U224-progress.txt`.
- Commit unsigned: `git -c commit.gpgsign=false commit`. The message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Comments explain a non-obvious why only.

REPORT
Status, head sha (40 hex), `git diff --stat 7992f1f5`, the ACCEPTANCE result lines, deviations. Under 12 lines, ending with `head=<40 hex>`.

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` (standing orders 21, 27, 29, 34, 35); `verdicts/U224-7992f1f5.md`; `sweeps/U224-7992f1f5/summary.txt`; `briefs/U224c-retire-the-installed-plugin-on-hosts-round3.md`.
