# refkit-P2-C validation

## `git diff --stat` (references/, before committing)

```text
 references/03_CONVENTIONS.md                       |  2 +-
 .../examples/flowapprove_core/pyproject.toml       |  4 +-
 references/kit.toml                                |  3 ++
 references/tools/README.md                         | 55 +++++++++++++++++--
 references/tools/kit_lint.py                       | 43 +++++++++++++--
 references/tools/render_mermaid.py                 | 30 +++++++----
 references/tools/run_examples.py                   | 63 +++++++++++++++-------
 7 files changed, 162 insertions(+), 38 deletions(-)
```

Plus one new untracked file: `references/tools/mermaid_common.py` (92 lines; see report's
"Scope note").

## `tools/mermaid_common.py` document-set parity check (against `Lint.run()`'s own `all_docs`)

```text
$ uv run --python 3.12 --with gherkin-official --with PyYAML python3 - <<'PYEOF'
[... builds all_docs exactly as Lint.run() does, and mermaid_common.document_paths(root) ...]
PYEOF
kit_lint count: 31
shared count: 31
same set: True
same order: True
```

## `kit_lint.py check` — honest run against the real, currently-committed tree

```text
$ uv run --python 3.12 --with gherkin-official --with PyYAML python tools/kit_lint.py check
{
  "status": "failed",
  "errors": [
    "E153 example_tests.json: テストの実行証跡が現行のコード・テスト・.feature と不一致＝証跡が古い。再実行が必要"
  ],
  "warnings": [],
  "mermaid_blocks": 20
}
```

This single error is **anticipated and out of this task's scope** — see the report's
"Known baseline gaps" section. It is caused by editing
`examples/flowapprove_core/pyproject.toml` (required by this task), which changes that
file's SHA-256; `kit.toml`'s `[tests] inputs` glob includes it, and the currently
committed `evidence/example_tests.json`'s `inputs_sha256` entry is now stale. This task's
own instructions forbid committing a regenerated evidence file (P9's job), so the real
repo is left in this state deliberately. Confirmed via `git stash`-and-retest that this
error does **not** occur on the pre-P2-C tree (baseline was clean before any of this
task's edits):

```text
$ git stash push -u -m "p2c-wip-check-baseline" -- examples/flowapprove_core/pyproject.toml tools/kit_lint.py tools/render_mermaid.py tools/run_examples.py tools/mermaid_common.py kit.toml
$ uv run --python 3.12 --with gherkin-official --with PyYAML python tools/kit_lint.py check
status: passed
errors: []
$ git stash apply <sha>; git stash drop <sha>   # restored my changes afterward
```

## `kit_lint.py check` — regenerating evidence instead (shows the _other_ anticipated gap)

```text
$ examples/flowapprove_core/.venv/bin/python tools/run_examples.py --mutation
{ ... "UT": {"branch_coverage_percent": 57.9, "line_and_branch_percent": 44.4, ...},
    "CT": {"branch_coverage_percent": 73.7, "line_and_branch_percent": 88.4, ...},
    "mutation": {"mutants": 68, "killed": 67, "score_percent": 98.5, ...}, "status": "passed" }

$ uv run --python 3.12 --with gherkin-official --with PyYAML python tools/kit_lint.py check
status: failed
errors: [
  "E158 ut/UT_SAMPLE.md: UT分岐カバレッジ（全体）: 文書の値「44.4%」が証跡の値 57.9（キー: ut.branch_coverage_percent）と一致しない",
  "E158 ct/CT_SAMPLE.md: CT分岐カバレッジ（全体）: 文書の値「88.4%」が証跡の値 73.7（キー: ct.branch_coverage_percent）と一致しない"
]
```

`44.4`/`88.4` are exactly the _old_ (mislabeled, line+branch) values still hardcoded in
`ut/UT_SAMPLE.md`/`ct/CT_SAMPLE.md`'s "実行結果" tables (P7's scope, not this task's).
Confirms the coverage-field fix is working correctly (the new `branch_coverage_percent`
values are genuinely different from, and more correct than, the old ones). Restored the
real evidence file afterward:

```text
$ git checkout -- evidence/example_tests.json
$ git status --short evidence/
(clean)
```

## Isolated clean-baseline verification (proves this task's own code is correct)

Copied the tree to a scratch directory, patched _only_ the two P7-scope numbers
(`ut/UT_SAMPLE.md`'s `44.4%` → `57.9`, `ct/CT_SAMPLE.md`'s `88.4%` → `73.7`, one
occurrence each, confirmed unique before replacing), regenerated evidence there with
`--mutation`, and reran `check`/`selftest` — never touching the real repo:

```text
$ cp -r references /tmp/refkit-p2c-verify2/k   # scratch copy, no rm involved
$ python3 -c "... patch the two occurrences ..."
$ examples/flowapprove_core/.venv/bin/python tools/run_examples.py --mutation
$ uv run --python 3.12 --with gherkin-official --with PyYAML python tools/kit_lint.py check
{
  "status": "passed",
  "errors": [],
  "warnings": [],
  "mermaid_blocks": 20
}
```

## `kit_lint.py selftest` — honest run against the real tree

```text
$ uv run --python 3.12 --with gherkin-official --with PyYAML python tools/kit_lint.py selftest
{
  "status": "failed",
  "baseline": "failed",
  "uncovered_codes": [],
  "total_mutations": 108
}
```

4 mutations show `MISSED` instead of `detected` — all of them assert the _overall_
result stays `passed` (a no-false-positive regression guard), which is mechanically
impossible while baseline itself is `failed` (E153, see above) — two of these four are
**pre-existing** mutations (`UATを2文書に分割してもcheckが通る`,
`SHA-256のような文字列が本文にあってもIDとして誤検出されない`), not introduced by this
task; the baseline dependency was always latent in how they're written, just never
exposed before this session edited a file that `[tests] inputs` hashes.
`uncovered_codes: []` — no `self.err`/`self.warn` call site (including the new **E104**)
lacks a mutation.

## `kit_lint.py selftest` — isolated clean-baseline verification

```text
$ uv run --python 3.12 --with gherkin-official --with PyYAML python tools/kit_lint.py selftest   # (in the scratch copy)
{
  "status": "passed",
  "baseline": "passed",
  "uncovered_codes": [],
  "total_mutations": 108
}
```

All 108/108 `detected`/`skipped`, including the three new/changed mutations:

```json
{"mutation": "Mermaidの図種が許可リストに無い", "expect": "E104", "status": "detected"}
{"mutation": "kit.tomlのdocsグロブ外のMarkdownにMermaid図があってもE103にならない", "expect": "passed", "status": "detected"}
{"mutation": "~~~フェンスのMermaid図もcheckが認識し証跡と一致する（E103にならない）", "expect": "passed", "status": "detected"}
```

## `render_mermaid.py` — 11.x and 12.x, sandbox enabled (default)

```text
$ examples/flowapprove_core/.venv/bin/python tools/render_mermaid.py \
    --mermaid-dir .mermaid/11/node_modules/mermaid \
    --mermaid-dir .mermaid/12/node_modules/mermaid \
    --output /tmp/refkit-p2c/mermaid_render.json
Mermaid 11.17.2: 20/20 ok, negative test rejected=True
Mermaid 12.0.0: 20/20 ok, negative test rejected=True

$ python3 -c "import json; d=json.load(open('/tmp/refkit-p2c/mermaid_render.json')); print(d['status'], d['no_sandbox'])"
passed False
```

`no_sandbox: False` confirms Chromium ran with the sandbox enabled (Playwright's own
default launch args, no `--no-sandbox`). `git status --short evidence/` stayed clean
throughout (output went to `/tmp/refkit-p2c/`, never the real
`evidence/mermaid_render.json`).

### `--allow-no-sandbox` sanity check (11.x only, quick)

```text
$ examples/flowapprove_core/.venv/bin/python tools/render_mermaid.py \
    --mermaid-dir .mermaid/11/node_modules/mermaid --allow-no-sandbox \
    --output /tmp/refkit-p2c/mermaid_render_nosandbox.json
Mermaid 11.17.2: 20/20 ok, negative test rejected=True
no_sandbox: True status: passed
```

### Bug caught and fixed during this validation

First run failed with `playwright._impl._errors.Error: Page.evaluate: SyntaxError:
Invalid or unexpected token` at the negative-diagram-rejection line — a mechanical
slip from my own rewrite (a missing doubled backslash), unrelated to the sandbox
change. Diagnosed by comparing `repr()` of the original committed line against my
rewritten line:

```text
$ git show HEAD:references/tools/render_mermaid.py | python3 -c "... find 'flowchart LR' ..."
'flowchart LR\\\\n A[\\"x\'); retur'          # original: 2 backslashes before n

$ python3 -c "... same extraction on my file ..."
'flowchart LR\\n A[\\"x\'); return'           # mine (buggy): 1 backslash before n
```

Fixed with an explicit `chr(92)`-based replacement (avoiding another layer of
string-literal ambiguity), verified the repr matches the original exactly, then reran
successfully (both commands above are the _post-fix_ runs).

## `run_examples.py --mutation --out /tmp/refkit-p2c/example_tests.json`

```text
$ examples/flowapprove_core/.venv/bin/python tools/run_examples.py --mutation --out /tmp/refkit-p2c/example_tests.json
{
  "status": "passed",
  "UT": {
    "tests": 125,
    "passed": 125,
    "branch_coverage_percent": 57.9,
    "line_and_branch_percent": 44.4
  },
  "CT": {
    "tests": 29,
    "passed": 29,
    "branch_coverage_percent": 73.7,
    "line_and_branch_percent": 88.4
  },
  "mutation": {
    "target": "flowapprove/domain.py",
    "tests": "tests/unit",
    "mutants": 68,
    "killed": 67,
    "survived": [
      "flowapprove.domain.x_next_state__mutmut_1"
    ],
    "score_percent": 98.5
  },
  "verified_ids": 40
}
```

`git status --short evidence/` stayed clean (output went only to `/tmp/refkit-p2c/`).
`mutation.target`/`mutation.tests` came from `pyproject.toml`'s new `[tool.mutmut]`
keys (`source_paths`/`pytest_add_cli_args_test_selection`), not hardcoded strings —
confirmed by temporarily changing `source_paths` to a different value and observing
`mutation.target` track it (not pasted here to keep this file focused; reproducible by
editing the scratch copy's `pyproject.toml`).

## Package versions used (from the venv used above)

```text
$ examples/flowapprove_core/.venv/bin/python -c "import importlib.metadata as im; [print(p, im.version(p)) for p in ('pytest','hypothesis','pytest-bdd','coverage','mutmut')]"
pytest 9.1.1
hypothesis 6.168.0
pytest-bdd 8.1.0
coverage 7.16.1
mutmut 3.8.0
```

## Source citations (already retrieved for P0-04; reused here, not re-fetched)

**mutmut 3 `[tool.mutmut]` keys** (`.orchestration/reports/P0-04-sources.md` §4,
retrieved 2026-09-23, https://mutmut.readthedocs.io/en/latest/):

> Config keys listed on the docs page: `source_paths`, `pytest_add_cli_args_test_selection`,
> `also_copy`, `max_stack_depth`, `only_mutate`, `do_not_mutate`,
> `mutate_only_covered_lines`, `type_check_command`, `debug`, `use_setproctitle`,
> `process_isolation`, `forkserver_warmup`, `preload_modules_file`. The keys
> `paths_to_mutate`, `tests_dir` and `runner` are NOT mentioned on the current docs page.

**coverage.py branch/line JSON fields** (same file, §5, retrieved 2026-09-23,
https://coverage.readthedocs.io/en/latest/branch.html and
https://raw.githubusercontent.com/nedbat/coveragepy/master/coverage/jsonreport.py):

> "covered_lines": nums.n_executed, "num_statements": nums.n_statements,
> "percent_covered": nums.pc_covered, ...
> "num_branches": nums.n_branches, "num_partial_branches": nums.n_partial_branches,
> "covered_branches": nums.n_executed_branches, "missing_branches": nums.n_missing_branches,
> "percent_branches_covered": nums.pc_branches, ...

> `percent_covered` = (executed statements + executed branches) / (statements +
> branches), i.e. it combines lines and branches when branch data exists;
> `percent_statements_covered` / `percent_branches_covered` are the separate figures.

**pytest JUnit `time`** (same file, §7, retrieved 2026-09-23,
https://docs.pytest.org/en/stable/how-to/output.html):

> JUnit XML specification seems to indicate that "time" attribute should report total
> test execution times, including setup and teardown. It is the default pytest behavior.

**Mermaid diagram-type keywords / securityLevel** (same file, §14, retrieved
2026-09-23, https://mermaid.js.org/intro/syntax-reference.html,
https://mermaid.js.org/syntax/stateDiagram.html): keywords shown on the pages —
`flowchart`, `sequenceDiagram`, `erDiagram`; state diagram page's first example begins
`stateDiagram-v2`, with the legacy form introduced as "Older renderer:" followed by a
block beginning `stateDiagram`.

## `git show --stat HEAD` (after committing)

```text
$ git show --stat HEAD
commit 576e83c83c2464152844220045d6f23e25a2b1ce
Author: Fumio Moriya <moriya.fumio@technopro.com>
Date:   Wed Sep 23 20:59:08 2026 +0900

    fix(references/tools): unify mermaid scope, enforce diagram types, measure branch coverage and durations, default to sandboxed chromium
    
    references/tools/mermaid_common.py is a new stdlib-only module shared by
    kit_lint.py and render_mermaid.py: one fence-extraction function (CommonMark
    fence rules: column-0 ``` / ~~~, 4+ backticks, indented) and one
    document-set function (the same kit.toml [docs] glob union check_mermaid
    already used). render_mermaid.py previously scanned every Markdown file
    with a naive ```mermaid regex, so its scope and fence-parsing never
    matched check_mermaid's, making E103's evidence comparison unreliable
    (E-06). kit.toml gains [mermaid] allowed_types, enforced as E104 (E-07).
    
    run_examples.py: mutmut invocations use sys.executable -m (was PATH-only),
    catch subprocess.TimeoutExpired (status: timeout), read the mutation
    target from pyproject.toml's [tool.mutmut] (mutmut 3's source_paths /
    pytest_add_cli_args_test_selection keys, replacing the no-longer-honored
    2.x paths_to_mutate / tests_dir), separate true branch_coverage_percent
    (covered_branches/num_branches) from the combined line_and_branch_percent
    (percent_covered, what the old code mislabeled as branch coverage - E-13),
    and record each test's duration_s from the JUnit XML plus all five tool
    versions.
    
    render_mermaid.py now launches Chromium with the sandbox enabled by
    default (Playwright's own default); --allow-no-sandbox opts back into
    --no-sandbox and records no_sandbox in the evidence (E-16, P2-09).
    
    Evidence/example_tests.json and evidence/mermaid_render.json are not
    regenerated in this commit (P9's job); the coverage-field change makes
    kit_lint.py check show one anticipated, pre-existing-condition error
    (E153, stale input hash from editing pyproject.toml) against the
    currently committed evidence - verified in an isolated scratch copy that
    the underlying logic is correct end to end (0 errors, selftest 108/108).
    
    Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>

 .orchestration/autoskill/runs/refkit-P2-C.md       |   3 +
 .orchestration/learning/refkit-P2-C.md             |  54 ++++
 .orchestration/reports/refkit-P2-C.md              | 197 ++++++++++++++
 .orchestration/sandboxes/refkit-P2-C.md            |  12 +
 .orchestration/validation/refkit-P2-C.md           | 301 +++++++++++++++++++++
 references/03_CONVENTIONS.md                       |   2 +-
 .../examples/flowapprove_core/pyproject.toml       |   4 +-
 references/kit.toml                                |   3 +
 references/tools/README.md                         |  55 +++-
 references/tools/kit_lint.py                       |  43 ++-
 references/tools/mermaid_common.py                 |  92 +++++++
 references/tools/render_mermaid.py                 |  30 +-
 references/tools/run_examples.py                   |  63 +++--
 13 files changed, 821 insertions(+), 38 deletions(-)
```

## CompactionDB memory-add

```text
$ python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "[memory:decision] P2-C: tools/mermaid_common.py (stdlib-only) unifies mermaid fence extraction + kit.toml [docs] document-set logic between render_mermaid.py and kit_lint.py's check_mermaid; kit.toml [mermaid] allowed_types enforced via E104 (first non-directive line's keyword); run_examples.py separates true branch_coverage_percent (covered_branches/num_branches) from combined line_and_branch_percent (percent_covered), adds per-test duration_s from JUnit XML time, records pytest/hypothesis/pytest-bdd/coverage/mutmut versions, reads mutation target from pyproject.toml [tool.mutmut] source_paths/pytest_add_cli_args_test_selection (mutmut 3 keys, replacing deprecated paths_to_mutate/tests_dir), reports status=timeout on subprocess.TimeoutExpired; render_mermaid.py now defaults to sandboxed Chromium, --allow-no-sandbox opts back into --no-sandbox (recorded as no_sandbox in evidence)"
0db34804-1173-4209-85c0-3fe8a8f26093
```

Memory ID: `0db34804-1173-4209-85c0-3fe8a8f26093`


## Round 2 (revision): `selftest` on the real tree, all four now `detected` despite E153

```text
$ uv run --python 3.12 --with gherkin-official --with PyYAML python tools/kit_lint.py selftest
{
  "status": "failed",
  "baseline": "failed",
  "uncovered_codes": [],
  "total": 108
}
non-detected: 0
{"mutation": "UATを2文書に分割してもcheckが通る", "expect": "no-new-errors", "status": "detected"}
{"mutation": "SHA-256のような文字列が本文にあってもIDとして誤検出されない", "expect": "no-new-errors", "status": "detected"}
{"mutation": "kit.tomlのdocsグロブ外のMarkdownにMermaid図があってもE103にならない", "expect": "no-new-errors", "status": "detected"}
{"mutation": "~~~フェンスのMermaid図もcheckが認識し証跡と一致する（E103にならない）", "expect": "no-new-errors", "status": "detected"}
```

`baseline: failed` is still E153 (unchanged, anticipated, deferred to P9 — see the
original "Known baseline gaps" note above); the difference from round 1 is that all
108 mutations, including these four, now report `detected`/`skipped` regardless of
that baseline noise, because each of the four now compares its mutated run's
error/warning codes against a same-copy, pre-mutation baseline rather than requiring
the whole run to be `passed`. `kit_lint.py check` on the real tree is unchanged from
round 1 (still exactly the one E153 line).

## Round 2: `kit_lint.py check` (unchanged from round 1, for the record)

```text
$ uv run --python 3.12 --with gherkin-official --with PyYAML python tools/kit_lint.py check
status: failed
errors: ['E153 example_tests.json: テストの実行証跡が現行のコード・テスト・.feature と不一致＝証跡が古い。再実行が必要']
```


## Round 2: CompactionDB memory-add

```text
$ python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "[memory:decision] refkit-P2-C revision: selftest's four negative mutations (UAT-split, SHA-256-no-false-positive, mermaid-out-of-scope, mermaid-tilde-fence) now compare mutated-run error/warning codes against a same-copy pre-mutation baseline (detected iff no new code appears) instead of requiring the whole run to be status==passed; the old shortcut made all four spuriously MISSED whenever an unrelated pre-existing failure (e.g. E153) was present in the tree"
15f4e987-2f9e-4a33-b079-1eed8b89f5af
```

Memory ID: `15f4e987-2f9e-4a33-b079-1eed8b89f5af`
