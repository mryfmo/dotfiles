# U216c round 3 of U216: the shfmt JSON contract table names the third library, only a brace block may end in `return`, rule b reads the function context too, and the test module gets its Threat row

GOAL
The round-2 audit of PR 732 (verdicts/U216-a7f9ccdb.md, class lint-grammar) found one P1, two P2 and one P3 on the lint change of U216b. (1) P1 producer-status-check.sh:395: `LIBRARY_FILES` gained `/regime-env`, but `scripts/ci/shfmt_json_contract.py`'s `TABLE` (the literals and fields a walker reads, per node kind, each pinned by `tests/fixtures/shfmt-json/contract.sh`) was not told, so `tests/unit/test_shfmt_json_contract.py::ContractTableTest::test_every_field_and_literal_a_walker_reads_is_in_the_table_for_its_kind` fails and the unit-test legs of CI are red at a7f9ccdb. (2) P2 producer-status-check.sh:1588: the new terminator accepts `x=$(false) || ( echo failed >&2; return 1 )` inside a function, where `return` ends the subshell alone and the function goes on; the second terminator is for a brace block (`Block`) only, never a `Subshell`. (3) P2 producer-status-check.sh:1547: the new `enclosed` parameter defaults to false and `empty_test`'s caller (:2093, rule b) never passes the function context, so a function's `[[ ! -s err ]] || { echo failed >&2; return 1; }` is refused under rule b while rule a accepts the same block; both rules read the same context. (4) P3: the Threat table has no row for `tests/unit/test_producer_status_check.py`.

SCOPE
The same branch `feat/pr-levers-anchor-the-store-at-the-derived-root` and PR 732; the tree is `/tmp/dotfiles-wt/U216` at a7f9ccdb (clean). May write: `scripts/ci/producer-status-check.sh`, `scripts/ci/shfmt_json_contract.py`, `tests/fixtures/shfmt-json/contract.sh` and the captured fixtures beside it if the contract regenerates them (read how `tests/unit/test_shfmt_json_contract.py` and `test_producer_status_check.py` build or pin them), `tests/unit/test_producer_status_check.py`, `tests/unit/test_shfmt_json_contract.py`, `scripts/orchestrator/README.md` (the producer-status rule sentences only), and the PR body `/tmp/dotfiles-wt/U216-pr-body.md`. Non-goals: no file under `scripts/orchestrator/` but `README.md`; no `# producer-status: allow` comment anywhere.

CONTEXT
At a7f9ccdb: `producer-status-check.sh` `LIBRARY_FILES` (:395 region), the `enclosed` parameter and where `refusal_break`/`terminator_shape` read it (:1547, :1588), `empty_test` and its caller (:2093); `scripts/ci/shfmt_json_contract.py` `TABLE` (the `SglQuoted`/`Lit` rows that name the two library literals, the comment at :86 "The lint reads a literal's value for the one `source` shape rule f accepts (U112 round 14): the two libraries") and `parse`; `tests/fixtures/shfmt-json/contract.sh` (the fixture whose tree must hold every literal the table names) and the captured JSON beside it; `tests/unit/test_shfmt_json_contract.py` `ContractTableTest` (what it asserts, how a fixture is captured or compared); the round-2 tests U216b added in `test_producer_status_check.py` (the function-body cases). `verdicts/U216-a7f9ccdb.md` lines 16 and 17 describe the auditor's two probes (the subshell case bash continued past; the rule b false refusal).

DATA SHAPE
One contract table that names every literal a walker reads, `/regime-env` beside the two libraries, with its fixture holding the literal; one terminator rule: inside a function body a `Block` (braces) may end in `return <1-255>`, a `Subshell` may not (its `return` ends the subshell alone), at the top level neither may; one function-context flag read by rule a and rule b alike.

CHANGE
1. Tests first, red at a7f9ccdb: (a) `test_shfmt_json_contract.py`'s table test green only once the table and fixture carry `/regime-env` (it is red at a7f9ccdb today: paste that); (b) in `test_producer_status_check.py`: `x=$(a) || ( echo no >&2; return 1 )` inside a function is a finding naming the subshell; the same with braces passes (the round-2 case, kept); (c) a function body holding `git ls-files > l 2> err; [[ ! -s err ]] || { echo failed >&2; return 1; }` (rule b's shape) passes, and the same at the top level is a finding. 2. `shfmt_json_contract.py`: the table row for the library literals names `/regime-env`; the fixture `contract.sh` gains a `. "${LEVER_DIR}/regime-env"` line (and its captured JSON is regenerated the way the module regenerates it, with its status read); the `TABLE` comment says three libraries. 3. `producer-status-check.sh`: the terminator inside a function is accepted for a `Block` and refused for a `Subshell` (the message names the subshell and that `return` ends it alone); `empty_test`'s caller passes the enclosing-function context; the header sentences say so. 4. README: the rule a and rule b sentences updated. 5. Green: `uv run --offline --with pyyaml python -m unittest tests.unit.test_producer_status_check tests.unit.test_shfmt_json_contract tests.unit.test_pr_levers tests.unit.test_lever_self_check -v` to `/tmp/u216c/full.txt` (shfmt on PATH, the mise pin); the enforced-set lint command of the U216b brief exits 0 with no output; the lints through `run-on-lint-files.sh` (shellcheck, shfmt, ruff, prettier), `lint-comparisons --changed`, `make render-check`. 6. One commit on a7f9ccdb; the body gains `## Round 3 (U216c)` (the four findings) and a `### Round 3, U216c, head <sha>` subsection under the existing `## Verification` heading (kept once) with ACCEPTANCE pasted; the Threat table gains rows for `tests/unit/test_producer_status_check.py`, `scripts/ci/shfmt_json_contract.py` and the fixture; `Program-Unit: regime-cutover/U216` once at the end; the body under 65536 bytes.

ACCEPTANCE
1. Tests (a), (b), (c) named with their red lines at a7f9ccdb (`/tmp/u216c/red.txt`) and green lines at the head. 2. The four modules OK with counts under `python -m unittest`. 3. The enforced-set lint command exits 0 with no output, pasted; every other lint 0 (`run-on-lint-files.sh`, `lint-comparisons --changed`, `make render-check`). 4. `git diff --stat a7f9ccdb HEAD` pasted; no file under `scripts/orchestrator/` but `README.md` in it. 5. `grep -c regime-env scripts/ci/shfmt_json_contract.py tests/fixtures/shfmt-json/contract.sh` is 1 or more for each, pasted.

VERIFY
ACCEPTANCE pasted into the body's Verification section and the report; the coordinator pushes to PR 732's branch, and the one audit (round 3), the sweep and CI follow.

CLOSURE
remove

TRUST
TRUST: the unit trusts the contract table and its fixture as the specification of what the walker may read (U112 round 14), bash's rule that `return` in a subshell ends the subshell alone as the reason the terminator is a brace block's, and the lint's test module as the grammar's pinned cases.

TIMEBOX
45 minutes.

FORBIDDEN
No change to any lever (no file under `scripts/orchestrator/` but `README.md`); no `# producer-status: allow` comment; no weakening beyond the brace-block terminator inside a function body; no network; no push; no rebase; no pipe `|` in any bash command (standing order 46: output to a file under `/tmp/u216c/`, then read it).

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46, 49; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 56)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/tmp/dotfiles-wt/U216`. The worktree is yours alone; your final line is the Task return.
- Progress line at `../U216c-progress.txt` at every step; final report to `../U216c-report.txt`.
- Commit unsigned: `git -c commit.gpgsign=false commit`. The commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.

REPORT
Status, head sha (40 hex), the tests with red and green lines, the ACCEPTANCE lines, deviations. Under 12 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 24, 27, 29, 34, 36, 44, 46, 49); `verdicts/U216-a7f9ccdb.md`; `verdicts/U216-0db1bc03.md`; the U216 and U216b briefs.
