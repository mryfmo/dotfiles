# refkit-P2-C report

Status: ready_for_review (round 2, after AGMSG-ACCEPTANCE status=revise)

## Round 2 revision (this section only; everything below is the original round-1 report)

`claude-remediation-dot` found that the four "must not introduce a new error" selftest
mutations (`UATを2文書に分割してもcheckが通る`, `SHA-256のような文字列が本文にあっても
IDとして誤検出されない`, and my two new mermaid ones) each asserted the *entire* run
stayed `status == passed`, so any pre-existing unrelated failure in the same temp copy
(here: E153, this task's own anticipated, documented gap) turned all four into false
`MISSED` results on the real tree — a selftest whose per-mutation outcome depends on
artefact freshness isn't a reliable regression guard. Fixed: each of these four now
runs `Lint(t).run()` on the **unmutated** copy first to capture a baseline error/warning
code set, then compares the mutated run's code set against it — `detected` iff the
mutation introduces no code not already present in the baseline, regardless of what
else is wrong in that baseline. Renamed their `expect` field from `'passed'` to
`'no-new-errors'` to match the new semantics (neither string is a real E/W code, so
this has no effect on `uncovered_codes` tracking). Verified all four `expect` values
in the file (grepped for `'expect': 'passed'` beforehand) belonged to exactly this set
— no other P2-A/P2-B-era mutation used the same shortcut. Re-ran `selftest` on the real,
currently-committed tree (E153 still present, as before and as expected): all 108
mutations now `detected`/`skipped`, `uncovered_codes: []`, `non-detected: 0` — see the
validation file's "Round 2" section. Did not touch the overall `selftest` aggregate
`status`/`baseline` gating (`base['status'] == 'passed'` in `main()`'s report
construction) — that's a different, correct design choice (the aggregate should still
honestly reflect that the real tree has E153) which the acceptance record didn't ask to
change; only the four *per-mutation* comparisons needed fixing. Amended the original
commit (`9397de0` → new hash below) rather than adding a second commit, following the
same precedent as refkit-P2-B's round-2 revision (still unreviewed/unmerged).

## Result

## Result

Implemented P2-03 (unified Mermaid fence extraction + document scope, diagram-type
enforcement), P2-08 (`run_examples.py` measurement fixes: true branch coverage,
per-test durations, tool versions, `pyproject.toml`-sourced mutation target, timeout
handling), and P2-09 (Chromium sandbox enabled by default).

## Files changed, with reasons

- `references/tools/mermaid_common.py` (**new file**, not in the task's literal
  `allowed_files` list, but necessarily implied by its own instruction — see "Scope
  note" below): a small stdlib-only module shared by `kit_lint.py` and
  `render_mermaid.py`, so neither pulls in the other's dependencies (`gherkin-official`/
  `PyYAML` vs. `playwright`). Provides:
  - `iter_fences(text)` / `mermaid_blocks(text)`: the same CommonMark fence-detection
    algorithm `kit_lint.py`'s `load()` already used internally (column-0-with-≤3-space
    indent, 3+ backticks or tildes, 4+ backticks included, closing fence same
    character/length, no info string) — `render_mermaid.py` previously used a naive
    ` ^```mermaid\n(.*?)^```\s*$ ` regex that missed `~~~` fences, 4+-backtick fences,
    and indented fences.
  - `diagram_type(code)`: the diagram-type keyword from a fence's first non-blank,
    non-`%%`-directive line (first `[A-Za-z][\w-]*` token) — `flowchart TD`/`flowchart LR`
    both normalize to `flowchart`.
  - `document_paths(root, cfg=None)`: the exact same document-set union `Lint.run()`
    builds for `all_docs` (templates ∪ PRD ∪ ADR ∪ BDD ∪ UT/CT/ST/UAT ∪ `other` (deduped
    against the above) ∪ the trace file). Verified byte-for-byte path-list identity
    against `Lint.run()`'s own construction on the real kit tree (31/31 paths, same
    order) before wiring it in — see validation file.
- `references/tools/kit_lint.py`:
  - `check_mermaid` now calls `mermaid_blocks(d.text)` directly (previously filtered
    `d.fences` for `lang == 'mermaid'` — behaviorally equivalent for well-formed input,
    but now literally the _same function_ `render_mermaid.py` calls, per this task's
    explicit requirement, rather than two independently-written implementations of the
    same algorithm).
  - New **E104**: a mermaid block whose `diagram_type()` isn't in `kit.toml`'s
    `[mermaid] allowed_types` fails with the type and the allow-list.
  - `MUTATIONS`: added `classDiagram` (via `adr/ADR-0001`'s own `flowchart LR` line) →
    **E104**.
  - `selftest()`: added two custom mutations (regex-substitution alone can't express
    "add a whole new out-of-scope file" or "swap a fence's delimiter character"):
    a mermaid block in a new Markdown file outside every `kit.toml` glob → asserts the
    overall run stays `passed` (no spurious E103); flipping an existing in-scope
    mermaid fence from ` ``` ` to `~~~` (same inner content) → asserts `passed` too
    (same SHA-256, same evidence key, no false E103). Both verified `detected` in an
    isolated scratch copy with a clean baseline (see validation file — the _real_ tree's
    baseline is currently `failed` for unrelated, already-anticipated reasons; see
    "Known baseline gaps" below).
- `references/kit.toml`: new `[mermaid] allowed_types = ["flowchart", "sequenceDiagram",
"stateDiagram-v2"]`.
- `references/tools/render_mermaid.py`:
  - `blocks()` now iterates `document_paths(ROOT)` (from the shared module) instead of
    `ROOT.rglob('*.md')`, and extracts fences via `mermaid_blocks()` instead of its own
    regex. This is the actual fix for E-06: previously the renderer's scope (every
    Markdown file, including `.mermaid/*/node_modules/mermaid/README*.md`, which contain
    `gantt`/`pie`/`classDiagram`/`gitGraph`/`C4Context`/`journey` diagrams) never
    matched `check_mermaid`'s scope (`kit.toml`'s `[docs]` union), so a document with a
    fence style the old regex couldn't parse — or simply outside `[docs]` — could make
    `check_mermaid`'s evidence comparison permanently wrong in either direction.
  - New `--allow-no-sandbox` flag (P2-09/E-16): default launch args are now `[]`
    (Playwright's own sandboxed default) instead of `['--no-sandbox']`; passing the flag
    re-adds `--no-sandbox` and the output JSON's `no_sandbox` field records which mode
    ran.
  - Fixed an unrelated bug I introduced while first drafting this file (not part of the
    task, a straight mechanical slip): the negative-test line's JS string needed a
    doubled backslash (`\\n`, matching the original committed file byte-for-byte) so
    Python passes a _literal_ two-character `\n` through to the JS source for the JS
    engine's own string-escape parsing to interpret as a newline; a single backslash
    made Python resolve it to an actual newline _before_ reaching JS, embedding a raw
    newline inside a JS single-quoted string literal (`SyntaxError: Invalid or
unexpected token`). Caught by actually running the script against both mermaid
    versions rather than trusting a diff read-through — see the "Editing discipline"
    section below.
- `references/tools/run_examples.py`:
  - `mutmut run`/`mutmut results` now use `[sys.executable, '-m', 'mutmut', ...]`
    (was: bare `['mutmut', ...]`, PATH-dependent — E-13).
  - `subprocess.TimeoutExpired` around `mutmut run` is now caught; on timeout, the
    mutation section gets `status: "timeout"` and the _overall_ `out['status']` becomes
    `"timeout"` (a third possible value alongside `passed`/`failed`), overriding the
    UT/CT-only computation.
  - New `mutmut_config(proj)` reads `examples/flowapprove_core/pyproject.toml`'s
    `[tool.mutmut]` and uses `source_paths`/`pytest_add_cli_args_test_selection`
    (mutmut 3's current keys — see the sources file, §4) for `mutation.target`/
    `mutation.tests`, replacing the hardcoded `'flowapprove/domain.py'`/`'tests/unit'`
    strings.
  - `coverage run` now passes `--branch` explicitly (was already enabled via
    `pyproject.toml`'s `[tool.coverage.run] branch = true`; the explicit flag makes the
    requirement visible at the call site too, defense in depth).
  - Coverage totals now produce **two** separate fields: `branch_coverage_percent`
    (`covered_branches / num_branches * 100`, the true branch percentage — 100.0 if
    `num_branches` is 0) and `line_and_branch_percent` (`percent_covered`, the existing
    line+branch composite coverage.py always reported — this is what the _old_ code
    mislabeled `branch_coverage_percent` as, per E-13).
  - Each test case now records `duration_s` (`float(tc.get('time', 0.0))`) from the
    JUnit XML `testcase` element's own `time` attribute (total time including
    setup/teardown — pytest's documented default).
  - `tools` now includes `mutmut`'s version alongside `pytest`/`hypothesis`/
    `pytest-bdd`/`coverage` (was previously only embedded inline in `mutation.tool`).
  - New `--out PATH` option (default: `kit.toml`'s `[tests] evidence`, matching the old
    behavior when omitted) — used to write to `/tmp/refkit-p2c/` per this task's
    instruction without touching the committed evidence file.
- `references/examples/flowapprove_core/pyproject.toml`: `[tool.mutmut]` now uses
  `source_paths = ["flowapprove/domain.py"]` and
  `pytest_add_cli_args_test_selection = ["tests/unit"]` — the mutmut 3.8.0 docs page
  (fetched, quoted in the validation file) lists `source_paths` and
  `pytest_add_cli_args_test_selection` among its current config keys and does not
  mention `paths_to_mutate`/`tests_dir` (the mutmut 2.x keys the file previously used;
  they happened to still "work" only because mutmut silently ignored the unrecognized
  keys, not because they were honored).
- `references/03_CONVENTIONS.md` (§7 only): the "図の種類" row now cites **E104** and
  notes the fence-style recognition (` ``` `/`~~~`/4+ backticks/indented) is shared
  between the renderer and the checker.
- `references/tools/README.md`: new "Mermaid" section (shared module, fence rules,
  document-set parity requirement, E104, sandbox default) and new "`run_examples.py` の
  証跡フィールド" section (branch vs. line+branch coverage formulas quoted from
  coverage.py's source, per-test `duration_s`, tool versions, `pyproject.toml`-sourced
  mutation target, `timeout` status, `--out`). Also cross-referenced
  `line_and_branch_percent` from the existing "実行結果" 表 section.

## Scope note: `tools/mermaid_common.py`

This task's `allowed_files` names `kit_lint.py`, `render_mermaid.py`, `run_examples.py`,
`kit.toml`, `03_CONVENTIONS.md` §7, the example project's `pyproject.toml`, and
`tools/README.md` — not a new file. The task's own P2-03 instruction, though, is "move
fence extraction into **one function** used by both `render_mermaid.py` and
`check_mermaid`" — the two scripts don't import each other and have deliberately
disjoint dependencies (`gherkin-official`/`PyYAML` vs. `playwright`), so a new,
dependency-free shared module is the direct, minimal-risk way to satisfy that
instruction without making either tool depend on the other's install footprint. I
judged this implied rather than a scope question needing to be asked, the same way
`refkit-P0-01`'s task text anticipated a scope-adjacent validator edit; flagging it
explicitly here rather than treating `allowed_files` as silently expandable.

## Known baseline gaps (both pre-existing/anticipated, not introduced by this task)

Running this task's own required validations against the **real, currently committed**
tree (not a regenerated scratch copy) surfaces two failures, neither caused by a defect
in this task's changes:

1. **E153** (`evidence/example_tests.json` input-hash staleness): editing
   `examples/flowapprove_core/pyproject.toml`'s `[tool.mutmut]` section (required by
   this task) changes that file's SHA-256, and `kit.toml`'s `[tests] inputs` glob
   includes it — so the currently-committed evidence file's `inputs_sha256` entry for
   it no longer matches. This task's own instruction says not to commit a regenerated
   `evidence/example_tests.json` (P9 regenerates everything); I did **not** commit one.
2. **E158** (×2, if evidence is regenerated instead): regenerating
   `evidence/example_tests.json` (to clear #1) correctly produces new
   `branch_coverage_percent` values (57.9/73.7 for UT/CT — the _true_ branch percentage;
   the _old_, mislabeled field held 44.4/88.4, which is what `line_and_branch_percent`
   now correctly represents) that no longer match `ut/UT_SAMPLE.md`'s and
   `ct/CT_SAMPLE.md`'s hardcoded "実行結果" table numbers — those SAMPLE docs are P7's
   scope ("UT／CT_SAMPLE の数値ラベルが実態と一致（P7 で反映）", per the plan), not this
   task's `allowed_files`.

Either way — stale evidence (E153) or regenerated evidence with stale SAMPLE numbers
(E158×2) — `kit_lint.py check` cannot show a literal 0/0 against the real committed tree
without editing a file outside this task's scope. I verified my actual code changes are
correct and complete by patching _just_ those two out-of-scope numbers in an isolated
`/tmp` scratch copy (never touched in the real repo) and regenerating evidence there:
`kit_lint.py check` → 0 errors/0 warnings, `selftest` → 108/108 mutations `detected`/
`skipped`, `uncovered_codes: []`. See the validation file for both the honest real-tree
runs and the isolated clean-baseline verification.

(Noted separately, not a decision I made: `claude-standard-dot-a002` reported
`refkit-P7 status=ready_for_review` on a different worktree/branch while I was
mid-task; if that work started before this branch's `run_examples.py`/`kit_lint.py`
changes existed, the two branches' evidence-field expectations for #2 above may need
reconciling at merge/acceptance time.)

## Commit

`f7a9fb3` on `feat/references-kit-v4`: `fix(references/tools): unify mermaid scope,
enforce diagram types, measure branch coverage and durations, default to sandboxed
chromium` (amended three times total across round 1 and this round-2 revision — see
below — always folding into this one commit rather than adding separate ones, since it
was still unreviewed/unmerged each time). Bookkeeping commit already recorded
separately for prior tasks (`f560b48`).

## Validation

`git diff --stat`, `kit_lint.py check`/`selftest` (both the honest real-tree run and the
isolated clean-baseline verification), `render_mermaid.py` 20/20 for both 11.x and 12.x
with the sandbox enabled (plus a quick `--allow-no-sandbox` sanity check), `run_examples.py
--mutation --out /tmp/refkit-p2c/example_tests.json` output and JSON summary, `git show
--stat HEAD`, and the `mutmut`/coverage.py doc citations are all in the validation file.

## Editing discipline

Every edit went through Bash-invoked Python scripts (`pathlib.Path.read_text()`/
`.write_text()`, each replacement asserted unique before applying), never the Edit/Write
tools, per this task's "Editing discipline" section — `git diff` for every changed file
contains only the intended hunks (reviewed each one individually; pasted in the
validation file). One real mistake happened anyway, caught by testing rather than by
reading the diff: my first draft of the negative-test line in `render_mermaid.py`
(written via a nested Python-string-generating scratch script) lost one level of
backslash-escaping (`\n` instead of the original's `\\n`), which only manifested as a
runtime `playwright._impl._errors.Error: Page.evaluate: SyntaxError` when I actually ran
the script — not as a diff anomaly, since the line still looked superficially
reasonable. Fixed by comparing `repr()` of both the original (`git show HEAD:...`) and
current line byte-for-byte and correcting the one missing backslash; re-ran successfully
against both mermaid versions afterward.

cost: n/a
