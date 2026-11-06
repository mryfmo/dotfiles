# U224b round 2: the deleted lever and rule copies retire on hosts, and the threat table has one row per changed path

GOAL
The U224 round-1 audit (`verdicts/U224-5a9793d4.md`, verdict correct) found two P2 above the weight threshold. [f8 s2] `home/.chezmoiremove` has no row for the deleted `ua-symbol-coverage` executable, so a host that already has `~/.local/bin/common/ua-symbol-coverage` keeps it after `chezmoi apply` (the auditor's scratch apply showed it). [f10 s3] the PR body's threat table groups changed paths and omits `home/dot_local/bin/common/executable_remove-agent-asset`; the standing requirement is one threat row per changed path. This round adds the missing host retirement rows and rewrites the body's threat table with one row per changed path. Nothing else changes.

SCOPE
The same branch `feat/remove-understand-anything-graphify-in` in your tree, on top of 5a9793d4 (your HEAD). May write: `home/.chezmoiremove` (added rows only) and the body file `/tmp/claude/U224/U224-pr-body.md`. Nothing else.

CONTEXT
The round-1 head deleted `home/dot_local/bin/common/executable_ua-symbol-coverage` (deployed as `~/.local/bin/common/ua-symbol-coverage`) and `home/dot_config/claude/rules/understand-anything.md` (deployed as `~/.config/claude/rules/understand-anything.md`); the generator added the rendered rule's row `.claude/rules/understand-anything.md`. chezmoi removes a deployed file only through a `.chezmoiremove` row. The changed-path list is `git diff --stat origin/main --name-only` at your HEAD (27 paths at 5a9793d4, 28 with `.chezmoiremove` already among them).

CHANGE
1. `home/.chezmoiremove`: add `.local/bin/common/ua-symbol-coverage` and `.config/claude/rules/understand-anything.md` if absent (one row each, same style as the neighbouring rows).
2. The body: replace the Threat table with one row per path in `git diff --name-only origin/main` (each row `path | risk | status | evidence`, status `closed`, the evidence an ACCEPTANCE command of the round-1 body or of this round), plus the `orchestrator effect` row; add a `## Round 2` section naming the two P2 and the fix; keep every other section.
3. Commit unsigned; the body file rewritten in place.

ACCEPTANCE
1. `grep -c '^\.local/bin/common/ua-symbol-coverage$\|^\.config/claude/rules/understand-anything\.md$' home/.chezmoiremove` prints 2.
2. `git diff --stat 5a9793d4` names `home/.chezmoiremove` alone.
3. `git diff --name-only origin/main | wc -l` and the number of path rows in the body's Threat table (excluding `orchestrator effect`) are equal (paste both).
4. `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed` exit 0.

VERIFY
The ACCEPTANCE commands in your tree with their result lines pasted into the body's Verification section under `## Round 2`.

CLOSURE
allowlist

TRUST
TRUST: the round trusts chezmoi's `.chezmoiremove` as the retirement mechanism and the round-1 head's file set as measured by git; it adds two rows and rewrites prose, reads no network, and changes no other file.

TIMEBOX
15 minutes.

FORBIDDEN
No change outside `home/.chezmoiremove` and the body file; no amend of the round-1 commit; no local bats; no network read; no push; no `gh` call; no mention of any private design directory; none of the words in `.orchestration/orchestrate/regime-cutover/redact-words.txt` and no absolute home directory in tracked files or the PR body (write `~/...`).

WORKER RULES (standing orders 27, 29, 31, 34; read `preferences.md` lines 23 to 45 in the store)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in your tree. Never `git stash`. Before you report, `git -C ~/Workspace/dotfiles status --porcelain=v1 --untracked-files=all -- . ':!.orchestration/orchestrate' | shasum` must print the value the TASK line carries.
- Progress line in `/tmp/claude/U224/U224-progress.txt`.
- Commit unsigned: `git -c commit.gpgsign=false commit`. The message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Comments explain a non-obvious why only.

REPORT
Status, head sha (40 hex), `git diff --stat 5a9793d4`, the ACCEPTANCE result lines, deviations. Under 10 lines, ending with `head=<40 hex>`.

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` (standing orders 27, 29, 34, 35); `verdicts/U224-5a9793d4.md`; `briefs/U224-remove-understand-anything-graphify-in.md`.
