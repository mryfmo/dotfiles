# U283b round 2 of U283: a failed sync leaves no record, the pruner refuses a non-file manifest, every new producer has its injection test

GOAL
The round-1 audit of PR 701 (U283, head b2467ae6; `verdicts/U283-b2467ae6.md`, correct) filed three P2 and two P3. P2 `:2818`: a partial failed sync keeps the older manifest record, so the doctor reports no finding while the payload is missing. P2 `:2834`: the library pruner returns success for a directory or a dangling link at the manifest path, and a failed here-string allocation leaves retired records intact, so the new `prune_retired_manifest_steps` wrapper does not guarantee strict pruning. P2 `:141`: the two new physical-path producers (`pwd -P` of the destination's parent and of the asset root) have no failure-injection test; the helper's nine tests cover path shapes only. P3 `:1648`: the threat table closes the bridge and omp destination risks with a test that calls only the helper, so removing a call-site guard leaves the cited test passing. P3 `tests/unit/test_update_agent_assets.py:1`: the threat table has no row for the test module. This round closes all five.

SCOPE
The existing branch `fix/updater-single-function-fails-closed` at b2467ae6ac7ad375d124165cbb461b11d12c2cc8 in `/tmp/dotfiles-wt/U283` (the PR is 701). May write: `scripts/update-agent-assets.sh`, `tests/unit/test_update_agent_assets.py`, `scripts/lib/*.sh` only where the pruner the wrapper calls lives (its own tests then move with it), and the body `../U283-pr-body.md` (a Round 2 section, the threat table rows). Not: the manifest, any `home/` file.

DATA SHAPE
Three rules, each in one place: (1) a sync step records its manifest row only after the payload is verified present (the record is the last write, and a failed sync removes the stale record or marks it failed so the doctor reports it); (2) the pruner's manifest path must be a regular file (not a directory, not a link), read through a status-checked producer into a variable (no here-string), and anything else refuses naming the path; (3) every `pwd -P` and `cd -P` the helper runs is a producer with its own injection test (a `BASH_ENV` function or a stub directory that makes it fail), and the call-site tests assert the guard at each call site by removing the guard in a copy and seeing the test fail (one mutation test per call site, or a test that runs the real step against a linked destination and asserts no sync call).

CHANGE
1. The three rules; the wrapper and the pruner per rule 2.
2. Tests: the partial-sync case (rsync fails after the destination exists) leaves no record and the doctor reports it; a directory and a dangling link at the manifest path refuse; a failed `pwd -P` of the parent refuses and of the root refuses (two injections); each of the four call sites refuses a linked destination before any sync call (recorder shows none).
3. The body: a Round 2 section quoting the five findings with each one's fix and test; the threat table gains the test module row and names, for the destination rows, the call-site tests.

ACCEPTANCE
1. `uv run python -m unittest tests.unit.test_update_agent_assets` OK (paste the count; the new tests named).
2. `make shellcheck` exit 0; `scripts/ci/run-on-lint-files.sh shell shfmt -i 4 -sr -d` exit 0; `scripts/ci/run-on-lint-files.sh markdown prettier --check` exit 0; `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check` exit 0.
3. `grep -c '<<<' scripts/update-agent-assets.sh` and the same over the pruner's library file: paste the counts, and name any remaining here-string that feeds a safety decision (there should be none).
4. `uv run --with pyyaml scripts/validate-agent-assets.py` exit 0.
5. `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed` exit 0.

VERIFY
ACCEPTANCE pasted into the body's Verification section.

CLOSURE
allowlist

TRUST
TRUST: the unit trusts the updater's fakes and fixtures as the test bed and closes five filed findings of a correct round; it runs no function on this host, reads no credential and opens no network.

TIMEBOX
45 minutes.

FORBIDDEN
No run of any `update_*` function on this host; no change to the manifest; no edit under `home/`; no write under `~/.local`, `~/.agents`, `~/.dsh`, `~/.codex`, `~/.claude`; no local bats; no network; no push; no `gh` call; no pipe `|` in any bash command you run yourself (standing order 46: output to a file under `/tmp/u283b/`, then read it).

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 62)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/tmp/dotfiles-wt/U283` and the coordinator fetches it by path.
- Progress line at `../U283b-progress.txt` every ten minutes at most; first edit within ten minutes. Final report to `../U283b-report.txt` before you end.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Comments explain a non-obvious why only, no phase narration. Shell comments are English shdoc.
- Follow `~/.agents/pstack/skills/poteto-mode/SKILL.md` (Fix Root Causes; Test Behavior, Not Implementation: the call-site tests assert the refusal a caller observes).

REPORT
Status, head sha (40 hex), files changed (`git diff --stat origin/main`), the ACCEPTANCE result lines, deviations. Under 10 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 27, 29, 34, 44, 46); `verdicts/U283-b2467ae6.md`; `AGENTS.md` (Test Policy, the threat table rule).
