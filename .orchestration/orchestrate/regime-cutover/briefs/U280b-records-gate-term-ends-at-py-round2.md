# U280b round 2 of U280: the records gate term ends at `.py`, and the threat table names every pinned path

GOAL
The round-1 audit of PR 699 (U280, head e8c85c2d; `verdicts/U280-e8c85c2d.md`) filed two P2, and the Codex review thread (comment 4492381429, `scripts/orchestrator/brief-check.py:252`) raises the first of them independently: the new `records-check` term ends in `\b`, so `python3 -I tests/check-tables.py.bak`, `python3 -I tests/check-tables.py.sh` and `python3 -I check-tables.py/run.py` all count as the test gate, although the contract admits only a `check-<name>.py` as the last path component. The second P2: the body's threat table lacks a row for each path the head changes beside the script (`home/dot_agents/agent-config.yaml`, the installed `executable_brief-check.py`, `scripts/generated-agent-outputs.json`); a sentence under the script's row is not the required per-path coverage. This round closes both and answers the thread.

SCOPE
The existing branch `fix/brief-check-records-gate` at e8c85c2d56791e0cf47ba7e95d9e35329f369b02 in `/tmp/dotfiles-wt/U280` (the PR is 699). May write: `scripts/orchestrator/brief-check.py` (the one term), `tests/unit/test_brief_check.py`, the three pinned outputs by regeneration (`uv run --with pyyaml scripts/generate-agent-configs.py`), and the body `../U280-pr-body.md` (the threat table rows and a Round 2 section). Not: any other rule, any brief in the store.

DATA SHAPE
The term requires, after `.py`, the end of the text or a whitespace character (or a closing backtick, since ACCEPTANCE lines quote commands), never another path character: `(?:$|\s|`)` in place of `\b`. Nothing else in the GATES row changes.

CHANGE
1. The term per DATA SHAPE; regenerate the pinned outputs.
2. Tests: `check-tables.py.bak`, `check-tables.py.sh` and `check-tables.py/run.py` are each refused with `names no test gate`; the backticked form `` `python3 -I tests/check-tables.py` `` passes; the existing tests stay.
3. The body: the threat table gains one row per changed path with its control (the self-check refuses an unpinned lever; `make render-check` proves the generated outputs); a Round 2 section quoting the two findings and the thread, with the fix and its test; ACCEPTANCE pasted.
4. Write the thread answer to `../U280b-thread-reply.md` (three sentences: the fix, the test that pins it, the head), for the coordinator to post.

ACCEPTANCE
1. `uv run python -m unittest tests.unit.test_brief_check tests.unit.test_generate_agent_configs` OK (paste the count; the three new refusal cases named).
2. `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check` exit 0; `scripts/ci/run-on-lint-files.sh markdown prettier --check` exit 0; `make render-check` exit 0.
3. `python3 -I scripts/orchestrator/brief-check.py` over every brief in the store's `briefs/` directory: the same set of refusals as at e8c85c2d (paste both counts).
4. `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed` exit 0.

VERIFY
ACCEPTANCE pasted into the body's Verification section. The coordinator posts the thread reply at the new head.

CLOSURE
remove

TRUST
TRUST: the unit trusts the GATES table as the rule's single home and tightens one term; it changes no brief and reads no network.

TIMEBOX
20 minutes.

FORBIDDEN
No change to any other rule or term; no change to any brief in the store; no push; no `gh` call; no pipe `|` in any bash command (standing order 46: output to a file under `/tmp/u280b/`, then read it).

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 62)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/tmp/dotfiles-wt/U280` and the coordinator fetches it by path.
- Progress line at `../U280b-progress.txt`; final report to `../U280b-report.txt` before you end.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Follow `~/.agents/pstack/skills/poteto-mode/SKILL.md` (Laziness Protocol: one term, three tests, three table rows).

REPORT
Status, head sha (40 hex), files changed, the term, the ACCEPTANCE result lines, deviations. Under 8 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 27, 29, 34, 44, 46); `verdicts/U280-e8c85c2d.md`; PR 699 thread 4492381429; `AGENTS.md:70-72` (the threat table rule).
