# U136 brief-check reads the lever list from the manifest block it names

GOAL
U130 merged as fc478ced with three parser findings filed under the threshold (`verdicts/U130-3e02511b.md`): `:109` the first `levers:` block is taken without checking its `claude:` parent, so an unrelated block earlier in the file is read as the lever list; `:114` a blank line or a YAML comment between two pins ends the list early, so a three-lever brief can pass; `:103` a manifest missing both the block and the self pin reports the pin refusal instead of the promised `no claude.levers.sha256 block` line. The manifest is generated today and holds neither case, so these are refusal gaps, not live defects; the reader should still read what it names.

SCOPE
One branch `fix/brief-check-reads-the-levers-block` from `origin/main`. May write: `scripts/orchestrator/brief-check.py`, `tests/unit/test_brief_check.py`, `scripts/orchestrator/README.md` (the brief-check row), `home/dot_agents/agent-config.yaml` (the pin, by the generator), `scripts/generated-agent-outputs.json` (by the generator), `home/dot_local/bin/common/executable_brief-check.py` (by the generator).

CHANGE
1. The block reader walks the manifest's top-level keys by indentation and takes `levers:` then `sha256:` only under the `claude:` mapping; a `levers:` block under another key is not the list. The script stays standard library only (`python3 -I -S`, no PyYAML), as its header requires.
2. Inside the `sha256:` mapping, blank lines and lines whose first non-space character is `#` are skipped; the list ends at the first line with less indentation than its entries. A pin line that is not `<name>: <64 hex>` refuses with exit 2 naming the line.
3. The order of refusals: the missing-block diagnostic is checked before the self pin, so a manifest lacking both prints `brief-check.py: refused: no claude.levers.sha256 block in <manifest>`.
4. Tests, behaviour only, each a scratch manifest: an unrelated `levers:` block before `claude:` and no `claude.levers` is exit 2 with the block line; a comment then a blank between the first and second pin still counts every pin (a three-lever brief is refused); a malformed pin line is exit 2 naming it; block and pin both missing prints the block line. The existing 43 tests keep passing.
5. Red proof on a `git archive` of `origin/main`: the comment-between-pins manifest passes a three-lever brief; the unrelated-block manifest passes it; both refuse on this head.

ACCEPTANCE
1. `uv run --no-project --with pyyaml python -m unittest tests.unit.test_brief_check tests.unit.test_hcom_seat_skills tests.unit.test_scratch_git` OK (paste the Ran line). 2. Every brief under `.orchestration/orchestrate/regime-cutover/briefs/` gives the same exit code on this head as on `origin/main` (list the counts: passed, refused, exit 2). 3. ruff format check; `scripts/lint-comparisons.py --changed` exit 0; the generator check up to date; `python3 -I -S scripts/orchestrator/brief-check.py <this brief>` exit 0 with no PyYAML on the path. 4. The PR body's Contract states the block grammar read and what is left out: no YAML beyond the one mapping path, no anchors, no flow style.

CLOSURE
parser-module: one indentation-walking reader for the one mapping path `claude.levers.sha256`, in one function, with the refusals named above.

TRUST
TRUST: the unit trusts the generated manifest `home/dot_agents/agent-config.yaml` (or the deployed `~/.agents/agent-config.yaml`) as the one list of levers and the generator as its writer; it does not read YAML in general and trusts the coordinator to split a refused brief rather than rename paths.

TIMEBOX
35 minutes.

FORBIDDEN
No PyYAML or other import beyond the standard library in the lever; no change to the lever-count threshold, the trigger-term table or the CLOSURE and TRUST rules; no `gh` call; no edit outside SCOPE.

WORKER RULES (standing orders 27, 29, 31, 34; read `preferences.md` lines 23 to 45 in the store)
- Never run git or edit files in `~/Workspace/dotfiles` (the coordinator's checkout; no `git worktree add`, no commit there), never push, never open or edit a PR, never edit the live store; you stop at a committed head in your tree and the coordinator fetches it by path and pushes. Your tree is the one the coordinator names in your task, a repository of its own under `$TMPDIR/dotfiles-wt/`; every command runs with it as cwd; if you believe it is absent, stop and report, never make another. Never `git stash`. No `/tmp` literal in tracked files.
- Run every test in the foreground with a timeout and paste its result line; progress line beside your tree (`../U136-progress.txt`) every ten minutes at most; `grep -n` then bounded reads; first edit within fifteen minutes.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Before you report: the modules named in ACCEPTANCE; `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check`; `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed`; `uv run --no-project --with pyyaml scripts/generate-agent-configs.py --check`.
- Write the PR body beside your tree (`../U136-pr-body.md`) with `## Summary`, `## Contract` (with a `Trusted:` sentence), `## Threat table` (`row | risk | status | evidence`, one row per changed path and per finding), `## Verification` (the result lines, the brief census and the red proof), the line `Program-Unit: regime-cutover/U136`, a blank line, then `🤖 Generated with [Claude Code](https://claude.com/claude-code)`.

REPORT
Status, head sha (40 hex), files changed, the result lines, the census, the red proof, deviations. Under 15 lines, ending with `head=<40 hex>`.

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md`; `verdicts/U130-ff55f3a0.md` and `verdicts/U130-3e02511b.md`; the follow-up candidates row of 2026-10-31T12:21:10Z.
