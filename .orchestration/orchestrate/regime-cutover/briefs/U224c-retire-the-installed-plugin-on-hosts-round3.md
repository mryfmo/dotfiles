# U224c round 3: the updater retires the installed Understand-Anything plugin and its marketplace on every host

GOAL
Codex review thread 4488887081 on PR 673 (P2, frequency 10, severity 3, weight 30) is right: the round-1 and round-2 heads delete the plugin's cache and marketplace checkout through `.chezmoiremove`, but `~/.claude/plugins/installed_plugins.json` and the `enabledPlugins` entry in `~/.claude/settings.json` keep the plugin, `modify_private_settings.json` preserves that key on purpose, and `manifest_prune_retired` drops the record `remove-agent-asset` could have used. So every upgraded host keeps an enabled plugin whose files are gone and `make doctor` reports it on every run. The official mechanism is Claude Code's own: `claude plugin marketplace remove <name>` "uninstalls every plugin you installed from it and removes their `enabledPlugins` entries from your settings files" (code.claude.com/docs/en/plugins/install, Manage marketplaces, read 2026-11-06), and `claude plugin uninstall <id>` acts on user scope by default and takes `--scope`. This round adds one retirement step to the updater that runs those commands when the records show the plugin or its marketplace present, converging the host before the manifest prune.

SCOPE
The same branch `feat/remove-understand-anything-graphify-in` in your tree, on top of the U224b head. May write: `scripts/update-agent-assets.sh` (one new function and one call line in `main()`), `tests/unit/test_update_agent_assets.py` (new tests), `README.md` only if the retirement steps are listed there (read it; add one line in the same list if they are), and the body file `/tmp/claude/U224/U224-pr-body.md`. Nothing else.

CONTEXT
Measured at 5a9793d4. `main()` runs `retire_shared_pstack_copies`, `retire_marketplace_dev_workflows` and `retire_agmsg_shim` first (`update-agent-assets.sh:2721-2723`), then the plugin convergence, and `manifest_prune_retired` near the end (`:2747`). `claude_plugin_installs <id>` (`:392`) prints one `<scope>\t<version>\t<project path>` line per installation from `installed_plugins.json` and exits 1 when the file exists but cannot be parsed (a failed read is never "not installed", standing order 21). `remove-agent-asset:296-297` is the precedent for calling `claude plugin uninstall` when `claude` is on PATH. The plugin id is `understand-anything@understand-anything`; its marketplace name is `understand-anything`. `claude plugin marketplace list` prints the registered marketplaces (shell form, per the same doc page). The existing DeepseekHarness and retire tests in `tests/unit/test_update_agent_assets.py` show how a step is run in isolation with stubbed commands written to a calls file.

CHANGE
1. Add `retire_understand_anything` before `retire_agmsg_shim` in `main()` (the retire group), with an shdoc comment stating the why above in two or three sentences. Behaviour, in order, each read fail-closed: (a) if `claude` is not on PATH, print one skip line and return 0 (a host without Claude Code has no records to clear); (b) `claude_plugin_installs understand-anything@understand-anything`: a read failure returns 1 naming the file; for each installation line run `claude plugin uninstall understand-anything@understand-anything --scope <scope>` (user, project and local scopes as the record names them; a project or local scope needs the project path as cwd); a non-zero exit returns 1 with the command named; (c) read `claude plugin marketplace list`; if it names `understand-anything`, run `claude plugin marketplace remove understand-anything`; a non-zero exit returns 1; (d) print one line per command run, or `already retired` when nothing was present. A second run finds nothing and changes nothing.
2. Tests (stubbed `claude` function writing its arguments to a calls file, a fixture `installed_plugins.json`): (a) a user-scope installation and a registered marketplace produce exactly the uninstall and the marketplace remove calls, in that order; (b) nothing installed and no marketplace produces no `claude` call and the `already retired` line; (c) an unparsable `installed_plugins.json` returns 1, names the file, and runs no `claude` command; (d) a failing `claude plugin uninstall` returns 1 and the marketplace remove does not run; (e) `claude` absent from PATH returns 0 with the skip line.
3. The body: add a `## Round 3` section (the thread id, the mechanism, the doc sentence quoted), move the host uninstall from "Leaves out" to the guarantee, add a threat row for the new function, and paste the ACCEPTANCE lines under Verification.

ACCEPTANCE
1. `grep -n 'retire_understand_anything' scripts/update-agent-assets.sh` shows the function and its single call in `main()` before `retire_agmsg_shim`.
2. `uv run python -m unittest tests.unit.test_update_agent_assets -k retire_understand_anything -v` runs the five tests OK (paste).
3. `make shellcheck` exit 0 and `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed` exit 0.
4. `grep -c 'understand' scripts/update-agent-assets.sh` is pasted (the function and its comment are the only matches; name them).
5. `git diff --stat <U224b head>` names `scripts/update-agent-assets.sh`, `tests/unit/test_update_agent_assets.py` and, if touched, `README.md`.

VERIFY
The ACCEPTANCE commands in your tree with their result lines pasted into the body. The host proof (the laptop's `make doctor` after `make update` no longer reports the plugin) is the coordinator's step after the merge, recorded in the store.

CLOSURE
allowlist

TRUST
TRUST: the round trusts Claude Code's `claude plugin` commands as the owner of `installed_plugins.json` and `enabledPlugins` and their documented behaviour at the installed version; it never edits those files itself, reads no network at test time, and changes no other updater step.

TIMEBOX
40 minutes.

FORBIDDEN
No direct edit of `installed_plugins.json`, `settings.json` or `enabledPlugins` by the step (the commands own them); no change to `modify_private_settings.json`, `manifest_prune_retired` or any other step; no amend of earlier commits; no local bats; no network read; no push; no `gh` call; no mention of any private design directory; none of the words in `.orchestration/orchestrate/regime-cutover/redact-words.txt` and no absolute home directory in tracked files or the PR body (write `~/...`).

WORKER RULES (standing orders 21, 27, 29, 31, 34; read `preferences.md` lines 23 to 45 in the store)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in your tree. Never `git stash`. Before you report, `git -C ~/Workspace/dotfiles status --porcelain=v1 --untracked-files=all -- . ':!.orchestration/orchestrate' | shasum` must print the value the TASK line carries.
- Progress line in `/tmp/claude/U224/U224-progress.txt`.
- Commit unsigned: `git -c commit.gpgsign=false commit`. The message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Comments explain a non-obvious why only, no phase narration.

REPORT
Status, head sha (40 hex), the diff stat against the U224b head, the ACCEPTANCE result lines, deviations. Under 12 lines, ending with `head=<40 hex>`.

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` (standing orders 21, 27, 29, 32, 34, 35); PR 673 review comment 4488887081; `briefs/U224-remove-understand-anything-graphify-in.md`; `briefs/U224b-host-retirement-rows-and-threat-rows-per-path-round2.md`.
