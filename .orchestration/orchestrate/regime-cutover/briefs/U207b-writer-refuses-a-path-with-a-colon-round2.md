# U207b the verdict writer refuses a finding path that holds a colon or whitespace, so the readers' first-token rule can misplace nothing (round 2 of U207)

GOAL
Round 1 of U207 (PR 666, head 2d0a93e4, `verdicts/U207-2d0a93e4.md`, Codex thread 4482792582) was incorrect on one P1: the readers now take the first colon-free token as the path, but the writer, `pr-audit.sh`'s reader of codex's `verdict.json`, still serializes the model's `path` field as it comes (`at = f"{path}:{int(line)}"`, `pr-audit.sh:1565-1570`), so a path such as `file:1: real.sh` with line 9 becomes the line `... file:1: real.sh:9: ...`, which the new readers take as `file` line 1, a location the writer did not mean, whose disposition row could then satisfy the gate; main's greedy readers refused that line as malformed. The ambiguity must be refused where the path is still a field: the writer refuses a `path` that holds a colon or whitespace (or is empty) as a malformed verdict, exit 2, naming the finding, and writes no `verdict.md`; the JSON schema codex is given states the same rule (`pattern`), so a conforming model never produces one. A P2 asks that `tests/unit/test_audit_carry.py` `test_render_refuses_a_store_it_cannot_read_as_data` follow the grammar change (its `a path with a colon` case and the diagnostic text, red on CI's Linux legs). After this head the writer refuses such a path, the schema states it, the audit-carry test's malformed-path case uses a line the readers still refuse (a first token followed by whitespace) and its diagnostic text is the new sentence, and the thread is answered.

SCOPE
The PR branch `fix/finding-path-grammar`, continued from 2d0a93e4 (your tree's `origin/main` is that head). May write: `scripts/orchestrator/pr-audit.sh` (and its generated copy and pin through the generator only), `tests/unit/test_pr_audit.py`, `tests/unit/test_audit_carry.py`, `tests/unit/test_pr_levers.py` only if a fixture there needs the writer's new refusal. Nothing else; the two readers stay as round 1 left them.

CONTEXT
Measured 2026-11-05 at 2d0a93e4. `pr-audit.sh` embeds the JSON schema codex must answer (`:1311` `"path": { "type": "string", "description": "The file, relative to the repository." }`, `:1312-1316` `line` as an integer from 1) and the Python reader that turns `verdict.json` into `verdict.md` (`:1565-1570`): `priority, confidence, path, line`, `at = f"{path}:{int(line)}"`, `one_line(at)` and `one_line(rationale)`; the reader already refuses a JSON number that is not an integer (U106 rounds) with exit 2 and no `verdict.md` (written whole or not at all, `:108-112`); `tests/unit/test_pr_audit.py` holds the reader's cases (36 reader cases per the U106 verdict row, injected I/O failures, the number cases). `tests/unit/test_audit_carry.py:513-540` `test_render_refuses_a_store_it_cannot_read_as_data` iterates malformed stores, among them `("a path with a colon", lambda: self.verdict(self.earlier, finding("P2", "file:1: real.sh", 9, "boom")), f"{verdict_file}:3: not a Findings line")` and a case whose expected text ends `... a path free of colons and whitespace: - P2 (high) a.txt:1: shouts` (`:538-539`); the readers' grammar sentence now ends `and whitespace; the path is the first such token; the rationale after the line's ': ' is free text`. The round-1 verdict's reproduction: the writer plus both readers on a structured path made `file:1`, and the extracted disposition functions accepted the unrelated `file:1` row at head and refused it at base.

CHANGE
1. The writer (`pr-audit.sh`'s Python reader of `verdict.json`): a finding whose `path` is not a non-empty string of characters outside whitespace and `:` is a malformed verdict: the reader exits 2 with a message naming the finding index and the path (never printing a secret: the path as given), and writes no `verdict.md`; the same for a `rationale` that is not a string (if not already refused). Keep `one_line` on the rationale.
2. The schema (`:1311`): `"path"` gains `"pattern": "^[^\\s:]+$"` and `"minLength": 1`, and its description says `no colon, no whitespace`; the prompt text that describes `path` (`:1270`) says the same in words.
3. Tests, `test_pr_audit.py`: a `verdict.json` whose finding has `path` `file:1: real.sh` and one with `path` `a b.sh` each exit 2 naming the finding and leave no `verdict.md`; a path `file.sh` with the rationale `see other.sh:9: text` is written and read back by `audit-carry.py`'s `findings_of` as path `file.sh` (the round-table of writer and readers). `test_audit_carry.py`: the `a path with a colon` case becomes `a first token followed by whitespace` (`finding("P2", "a b.txt", 1, "x")` rendered as a line, or a hand-written line `- P2 (high) [f1 s1] a b.txt:1: x`) with the expectation `not a Findings line`, and the diagnostic text of the second case gains the new sentence tail.
4. The body (`../U207b-pr-body.md`, from `../U207-pr-body.md`, read-only): the Contract gains the writer's rule and says where the ambiguity is refused (the field, not the text); the Threat table gains rows for `pr-audit.sh`, its generated copy, the pin, `test_pr_audit.py` and `test_audit_carry.py`, and the `orchestrator effect` row says a verdict of a model that answers a path with a colon is refused and the audit rerun, never read; Verification gains `Round 2 (U207b)` with the ACCEPTANCE lines; `Program-Unit: regime-cutover/U207` stays.

ACCEPTANCE
1. `uv run --no-project python -m unittest tests.unit.test_pr_audit tests.unit.test_audit_carry tests.unit.test_filed_findings tests.unit.test_pr_levers tests.unit.test_pr_merge` prints `OK` (skips allowed; paste the line). 2. `bash -n`, `shellcheck -x`, `scripts/ci/run-on-lint-files.sh shell shfmt -i 4 -sr -d`, `scripts/ci/git-invocation-check.sh scripts/orchestrator/git-isolated.sh scripts/orchestrator/pr-audit.sh`, `scripts/ci/producer-status-check.sh scripts/orchestrator/pr-audit.sh` exit 0; `uv run --no-project ruff format --check` and `ruff check` on the changed test files exit 0 (pre-existing findings on untouched lines named as such); `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed` exit 0. 3. The generator write run then `make render-check` exit 0; `cmp` of `pr-audit.sh` and its generated copy exit 0. 4. The red proof at a `git archive origin/main` tree (2d0a93e4): the two writer refusal tests fail (the writer there writes the line), and the retargeted audit-carry case passes at both (say so). 5. `git diff --stat origin/main` names SCOPE files alone.

VERIFY
The commands of ACCEPTANCE in the worker's tree with their result lines pasted into the PR body's Verification section.

CLOSURE
parser-module

TRUST
TRUST: the unit trusts the JSON the model returns as data the writer validates before it writes a line, the readers of round 1 as the one grammar of the written line, and the shared fixtures of the two readers; it changes no gate rule, no disposition rule and no verdict file, and reads no network.

TIMEBOX
45 minutes.

FORBIDDEN
No edit of any file under `verdicts/`; no change to the readers' regexes; no hand edit of the generated copy or pin; no network read; no push; no `gh` call; no local bats; no mention of any private design directory in files, commits or the PR body; none of the words in `.orchestration/orchestrate/regime-cutover/redact-words.txt` and no absolute home directory in tracked files or the PR body (write `~/...`).

WORKER RULES (standing orders 27, 29, 31, 34; read `preferences.md` lines 23 to 45 in the store)
- Never run git or edit files in `~/Workspace/dotfiles` (the coordinator's checkout), never push, never open or edit a PR, never edit the live store; you stop at a committed head in your tree and the coordinator fetches it by path and pushes. Your tree is the one the coordinator names in your task, a repository of its own under `$TMPDIR/dotfiles-wt/U207b`; every command runs with it as cwd; if you believe it is absent, stop and report, never make another. Never `git stash`. No `/tmp` literal in tracked files. Before you report, `git -C ~/Workspace/dotfiles status --porcelain=v1 --untracked-files=all -- . ':!.orchestration/orchestrate' | shasum` must print `7a5f435887f613fe2be5b9f6f4a01d2b9a39a48e  -`.
- Run every test in the foreground with a timeout and paste its result line; no backgrounded test run; progress line beside your tree (`../U207b-progress.txt`) every ten minutes at most; first edit within ten minutes.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Write the whole new PR body beside your tree (`../U207b-pr-body.md`) per CHANGE 4.
- Comments explain a non-obvious why only, no phase narration. Tests assert behaviour the user observes.

REPORT
Status, head sha (40 hex), files changed (`git diff --stat origin/main`), the ACCEPTANCE result lines, the red proof, deviations. Under 14 lines, ending with `head=<40 hex>`.

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` (standing orders 21, 33); `verdicts/U207-2d0a93e4.md`; `briefs/U207-finding-line-path-is-the-first-colon-free-token.md`; `AGENTS.md` Audit section.
