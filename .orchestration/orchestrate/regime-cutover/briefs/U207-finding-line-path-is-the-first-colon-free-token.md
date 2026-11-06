# U207 the two readers of a verdict's Findings section take the path as the first colon-free token, so a rationale may hold a `path:line:` of its own

GOAL
The U190 round-5 verdict (`verdicts/U190-6f66ffdc.md`, the auditor's output, kept as written) carries finding lines of the form `- P2 (high) [f1 s8] scripts/orchestrator/hcom-seat:1548: Carried P2 at hcom-seat:1548: operator paths inherit ...`. Both readers of the leading `## Findings` section, `findings_of` in `scripts/orchestrator/audit-carry.py` (`FINDING`, the path group `(.+)`) and `pr-merge.sh` (`finding_re`, the same group), match the path greedily, so the path becomes `scripts/orchestrator/hcom-seat:1548: Carried P2 at hcom-seat` and fails the path grammar: `filed-findings.py` exits 2 on the store (measured 2026-11-05), the sync 38 audit filed it, and `pr-merge.sh` would refuse the merge of PR 664 at that head as a malformed verdict. The grammar the levers state (`<path>:<line>: <rationale>` with a path free of colons and whitespace) already fixes the reading: the path is the first colon-free, whitespace-free token, the line the digits after it, and the rationale everything after the following `: `, free text that may hold any `path:line:` of its own. After this head both readers read the line that way, the test that runs the two readers over one fixture set holds a rationale with an inner `path:line:` as a finding and not as malformed, and the comment in `pr-merge.sh` that defended the greedy group (`:248`, a shorter path and an earlier line satisfying another location's disposition row) is replaced by the reason the first token is the location: the writer's grammar puts it first, and a disposition row names that first location, so no other location can satisfy it.

SCOPE
A new branch `fix/finding-path-grammar` from `origin/main` ba051b0d. May write: `scripts/orchestrator/audit-carry.py`, `scripts/orchestrator/pr-merge.sh` (and its generated copy and pin through the generator only), `scripts/orchestrator/filed-findings.py` only if its docstring repeats the grammar sentence, `tests/unit/test_pr_levers.py`, `tests/unit/test_pr_merge.py` if a fixture there states the grammar, `scripts/orchestrator/README.md` (the sentence that states the grammar, if it does). Nothing else.

CONTEXT
Measured 2026-11-05 on ba051b0d. `audit-carry.py:183` `FINDING = re.compile(r"^- (P[0-3]) \((high|medium|low)\) \[f([^\]]*) s([^\]]*)\] (.+):([1-9][0-9]*): ")` and `:186` `PATH = re.compile(r"^[^\s:]+$")`, applied to group 5 after the match (`:426-428`); `pr-merge.sh:249` `finding_re='^- (P[0-3]) \((high|medium|low)\) \[f([^]]*) s([^]]*)\] (.+):([1-9][0-9]*): '` with `path_re='^[^[:space:]:]+$'` (`:251`) and the comment at `:248`; `findings_grammar` (`:256`) and `FINDINGS_GRAMMAR` (`audit-carry.py:178-182`) state the sentence; `filed-findings.py` imports `findings_of` (`:11-12`) and parses no line itself; `tests/unit/test_pr_levers.py:1809` `test_the_merge_gate_and_audit_carry_read_the_findings_grammar_alike` runs both readers over one fixture set. The failing line, verbatim from the store: `- P2 (high) [f1 s8] scripts/orchestrator/hcom-seat:1548: Carried P2 at hcom-seat:1548: operator paths inherit the own-directory exemption, so CLAUDE_CONFIG_DIR=$checkout passes the orchestrator overlap check instead of refusing.` With a non-greedy or colon-free path group it reads path `scripts/orchestrator/hcom-seat`, line `1548`, rationale `Carried P2 at hcom-seat:1548: operator paths ...`. A line whose first token holds a colon or whitespace (`a b:1: x`, `a:b:1: x` where `a:b` is meant as the path) stays malformed, as today.

CHANGE
1. `audit-carry.py`: the path group becomes `([^\s:]+)` (the grammar's own character class), the `PATH` check stays as a second statement of the same rule or goes if it is now redundant (say which in the body); the docstring of `findings_of` says the path is the first token and the rationale is free text.
2. `pr-merge.sh`: `finding_re`'s path group becomes `([^[:space:]:]+)`; the comment at `:248` is replaced by the reason above; `path_re` stays or goes as in 1, the same choice in both readers.
3. Tests: `test_the_merge_gate_and_audit_carry_read_the_findings_grammar_alike` gains the store's line (a rationale holding `hcom-seat:1548:`) as a finding both readers accept with path, line and rationale as stated, and a line whose first token holds a colon (`a:b:1: text`) and one with whitespace (`a b:1: text`) as malformed for both; `filed-findings.py` over a scratch store holding that verdict prints its row (path, line, rationale) and exits 0.
4. The grammar sentence (`FINDINGS_GRAMMAR`, `findings_grammar`, the README if it repeats it) gains the words `the path is the first such token; the rationale after the line's `: ` is free text`.
5. The PR body (`../U207-pr-body.md`): Summary, Contract (what the readers accept and refuse after this head), a Threat table with four columns `row | risk | status | evidence` and one row per changed path plus an `orchestrator effect` row (the merge of PR 664 at 6f66ffdc becomes readable; no verdict file changes), Verification with the ACCEPTANCE lines, the footer `Program-Unit: regime-cutover/U207`.

ACCEPTANCE
1. `uv run --no-project python -m unittest tests.unit.test_pr_levers tests.unit.test_pr_merge` prints `OK` (skips allowed; paste the line). 2. `uv run --no-project python -I scripts/orchestrator/filed-findings.py <scratch store holding a copy of verdicts/U190-6f66ffdc.md and the store's ledger header>` exits 0 and prints the five rows of that file (paste them). 3. `bash -n`, `shellcheck -x`, `scripts/ci/run-on-lint-files.sh shell shfmt -i 4 -sr -d`, `scripts/ci/git-invocation-check.sh scripts/orchestrator/git-isolated.sh scripts/orchestrator/pr-merge.sh`, `scripts/ci/producer-status-check.sh scripts/orchestrator/pr-merge.sh` exit 0; `uv run --no-project ruff format --check` and `ruff check` on the changed Python files exit 0; `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed` exit 0. 4. The generator write run then `make render-check` exit 0; `cmp` of `pr-merge.sh` and its generated copy exit 0. 5. The red proof: at a `git archive origin/main` tree the new test case fails for both readers (paste the lines). 6. `git diff --stat origin/main` names SCOPE files alone.

VERIFY
The commands of ACCEPTANCE in the worker's tree with their result lines pasted into the PR body's Verification section.

CLOSURE
parser-module

TRUST
TRUST: the unit trusts the verdict file as the auditor wrote it (it changes no verdict), the grammar sentence the two readers already state as the definition of a finding line, and the shared fixture set as the proof that both readers agree; it changes no gate rule, no disposition rule and no other lever, and reads no network.

TIMEBOX
45 minutes.

FORBIDDEN
No edit of any file under `verdicts/`; no change to what a disposition row must name; no hand edit of the generated copy or pin; no network read; no push; no `gh` call; no local bats; no mention of any private design directory in files, commits or the PR body; none of the words in `.orchestration/orchestrate/regime-cutover/redact-words.txt` and no absolute home directory in tracked files or the PR body (write `~/...`).

WORKER RULES (standing orders 27, 29, 31, 34; read `preferences.md` lines 23 to 45 in the store)
- Never run git or edit files in `~/Workspace/dotfiles` (the coordinator's checkout), never push, never open or edit a PR, never edit the live store; you stop at a committed head in your tree and the coordinator fetches it by path and pushes. Your tree is the one the coordinator names in your task, a repository of its own under `$TMPDIR/dotfiles-wt/U207`; every command runs with it as cwd; if you believe it is absent, stop and report, never make another. Never `git stash`. No `/tmp` literal in tracked files. Before you report, `git -C ~/Workspace/dotfiles status --porcelain=v1 --untracked-files=all -- . ':!.orchestration/orchestrate' | shasum` must print `7a5f435887f613fe2be5b9f6f4a01d2b9a39a48e  -`.
- Run every test in the foreground with a timeout and paste its result line; no backgrounded test run; progress line beside your tree (`../U207-progress.txt`) every ten minutes at most; first edit within ten minutes.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Write the whole PR body beside your tree (`../U207-pr-body.md`) per CHANGE 5.
- Comments explain a non-obvious why only, no phase narration. Tests assert behaviour the user observes.

REPORT
Status, head sha (40 hex), files changed (`git diff --stat origin/main`), the ACCEPTANCE result lines, the red proof, deviations. Under 14 lines, ending with `head=<40 hex>`.

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` (standing orders 21, 33); `verdicts/U190-6f66ffdc.md` (the file that must read); `verdicts/U20-370b6f49.md` (the finding that named it); `AGENTS.md` Audit section.
