# refkit-P2-B report

Status: ready_for_review (round 2, after AGMSG-ACCEPTANCE status=revise)

## Round 2 revision (this section only; everything below is the original round-1 report)

claude-remediation-dot found that E158's evidence-key resolver silently skipped any
`証跡のキー` it couldn't resolve — `have = evidence_value(key); if have is None: continue` —
so a typo like `ut.pased` (instead of `ut.passed`) made a table row unverifiable without
any signal, the same class of problem E158 was rewritten to close. Fixed: when the
document's own `doc_type` level exists in the evidence file (the same condition already
gating entry into the per-row loop), an unresolved key is now **E159** naming the row and
key, instead of a silent `continue`. Skipping remains correct only when the document's own
level is absent from evidence (ST/UAT `not_run`), which was already handled by the
existing outer guard and needed no change. Reproduced the reviewer's exact scratch
scenario (`| UT合格 | 999 | ut.pased |`) and confirmed it now fails with E159 (see
validation file, "round 2" section). Added a selftest mutation for E159 (typo'd key on a
resolvable level) and confirmed `uncovered_codes` stays `[]` (105 mutations now, up from
104). Updated `tools/README.md`'s key-resolution section to state the E159 condition.
Amended the original commit (`ef7f611` → `8520649`) rather than adding a second commit,
since the acceptance record explicitly asked for an amend and the original commit was
still unreviewed/unmerged.

## Result

Implemented P2-02 (configurable IDs + multi-PRD), P2-04 (evidence-bound `passed`/`failed`),
P2-05 (structured, evidence-checked `実行結果` table replacing E158's prose-scanning), and
P2-06 (fully self-auditing `selftest` coverage + an honest `portability_test.py` that uses
the real `kit.toml`).

## Files changed, with reasons

- `references/tools/kit_lint.py`:
  - `ID_KINDS`/`ITEM_KINDS` explicit allow-lists replace the old `[A-Z]+-\d{3,4}` catch-all.
    `Lint.__init__` builds `self.ID`/`self.ITEM` from `kit.toml`'s new `[ids] prefix` (default
    `""`). Every method that referenced the old module-level `ID`/`ITEM` now uses `self.ID`/
    `self.ITEM`.
  - `run()`: supports `≥1` PRDs (was: exactly 1, else E110). Parses each individually via
    `check_prd`, merges `fr`/`nfr`/`goals`/`kpis`/`nvt`/`ids` for the cross-checks
    (`check_cross`/`check_adr`/`check_tests`, which need the union to resolve references
    that may live in a sibling PRD), and separately detects ID collisions across PRDs
    (new E030 case). `check_cross`'s `prd: Doc` parameter became `prds: list[Doc]` (an
    `E071`/`E072` "where" label listing all PRD paths).
  - `build_trace`: takes `list[tuple[Doc, dict]]` instead of one `(prd, pm)`. With exactly
    one PRD the FR/NFR section headers are unchanged (`## 機能要件`/`## 非機能要件`) —
    verified `04_TRACEABILITY.md`'s committed bytes still match (no `E120`). With `>1` PRD
    each gets its own labelled section.
  - `check_tests`'s UAT loop: evaluates `E150`/`E151` over the union of `docs['uat']` (was:
    per document), with a `where` label listing all UAT doc paths.
  - `check_vocab`: dropped the `'evidence' in d.meta` gate — `last_run: passed`/`failed`
    now requires a real `evidence` file regardless of doc type.
  - `check_tests`'s old E158 block (substring-scanning `d.prose` for `f"{lv['tests']}件"`
    etc.) replaced with a parser for a fixed `| 項目 | 値 | 証跡のキー |` table: each row's
    "証跡のキー" (e.g. `ut.total`, `mutation.killed`) resolves against the evidence JSON via
    a small `evidence_value()` closure (`total` is an alias for `tests`/`mutants` depending
    on section; everything else is looked up by its real JSON field name), and the cell
    value is compared numerically. Rows whose key doesn't resolve (no matching evidence,
    e.g. ST/UAT) are silently skipped — matches `not_run` samples needing no live evidence.
  - `selftest()`/`main()`: computes `emitted` (every `self.err('Exxx'`/`self.warn('Wxxx'`
    call site's code, via regex over the script's own source) vs `covered` (the `expect`
    field of every mutation result) and reports `uncovered_codes`; a non-empty list fails
    `selftest`. Added ~70 new `MUTATIONS` entries (and a few custom procedural mutations for
    cases regex-substitution alone can't express) to reach full coverage; re-anchored the
    two P2-A-era BDD mutations and the mirror-scenario custom mutation from hardcoded sample
    prose to a structural `@SCN-001` anchor + wildcard, per this task's "generic, located by
    structure" requirement. Added a `DELETE` sentinel so a mutation can delete a file (used
    for the two evidence-file-missing warnings, W102/W154) instead of only regex-substituting
    its content.
  - Unrolled the one dynamic-code `self.err(code, ...)` call (E144/E145 shared a loop) into
    two literal calls — needed so the coverage-scanning regex (which only sees literal
    `'Exxx'` string arguments) can find both codes.
- `references/tools/portability_test.py`: rewritten per this task's step 9 — see the
  commit body. Read the real `kit.toml`, rewrote only path-bearing lines (verified each
  substitution matches exactly once), left `[vocab.*]`/`[ids]`/`[adr]`/`[gherkin]`
  (`max_unique_step_ratio` included)/`[evidence]` untouched. Generalized `fill()`'s
  placeholder handling: `{{a｜b｜c}}` now picks the first alternative programmatically
  (previously only one such placeholder, ADR's `confidence`, had a hand-written override).
  Generates `examples/mini_project/test_mini.py` (one `test_name` function — the literal
  name both UT-001 and CT-001's template placeholder resolves to) so `[tests]`' checks,
  E152 included, actually run. Copies `tools/render_mermaid.py` and conditionally runs it
  against `references/.mermaid/11/node_modules/mermaid` when that directory exists and
  `playwright` is importable from the running interpreter; otherwise records an explicit
  skip reason in the output's new `mermaid` field. Added two BDD step-text fixes so the
  filled template's step-vocabulary reuse ratio clears the real `0.60` threshold (a tiny,
  2-scenario document has little repetition to work with otherwise). Templates copied into
  `tpl/` have only their `> 記入方法は [X_GUIDE.md](X_GUIDE.md)。` intro line stripped (not a
  full `fill()`) — copying the actual GUIDE files was tried first but made `render_mermaid.py`
  see extra Mermaid blocks kit_lint's own `all_docs` didn't (since `other` was simplified to
  `[]`), producing a false E103; stripping the one dead-link line was simpler and avoided
  reintroducing GUIDE files (and their own further link chains) at all.
- `references/kit.toml`: new `[ids]` section (`prefix = ""`).
- `references/03_CONVENTIONS.md` (§3, §5 only): §3 now describes `[ids] prefix` and the
  "unset prefix ⇒ unrecognized ID, not silence" behavior instead of telling readers to edit
  `kit_lint.py`. §5's evidence row states the requirement is unconditional and cites E155.
- `references/bdd/BDD_TEMPLATE.md`/`BDD_SAMPLE.md` (front matter only): added `evidence:`.
- `references/{ut,ct,st,uat}/*_TEMPLATE.md` (実行結果 table shape only) and the matching
  `*_SAMPLE.md` (same table only): added/replaced with the `| 項目 | 値 | 証跡のキー |`
  table. UT_SAMPLE/CT_SAMPLE values are copied from the current
  `evidence/example_tests.json`; ST_SAMPLE/UAT_SAMPLE get `not_run` values (no evidence to
  check against, by design).
- `references/tools/README.md`: documents `[ids] prefix`, multi-PRD support, the
  unconditional evidence requirement, the `実行結果` table/key format, `selftest`'s
  coverage-completeness self-check, and `portability_test.py`'s "real kit.toml, paths only"
  contract and Mermaid skip condition.
- `references/evidence/portability_test.json`: regenerated by running the rewritten
  `portability_test.py` (see note below — this is the script's own output file, not part of
  the v3 baseline that came in with the kit import).

## Numbers with no table-key equivalent (P2-05, flagged per the task's own instruction)

`ut/UT_SAMPLE.md`'s prose still says "`domain.py` の分岐カバレッジ 100%" and
`ct/CT_SAMPLE.md`'s prose still says "`service.py` の分岐カバレッジ 94.4%" — both are
per-file entries from the evidence's `coverage_by_file` map, which doesn't fit the table's
two-level `<section>.<field>` key scheme (the file path itself contains `/` and `.`).
Left as prose-only, per the task's instruction to keep untable-able numbers out of the
table and mention them here; a later task (P7, per the task file) can decide whether to
extend the key scheme or drop these numbers from the prose.

## `evidence/portability_test.json` regeneration

This task's forbidden-actions list says `regenerate-04-features-evidence`. Read narrowly (as
in refkit-P1's README: "04_TRACEABILITY.md, features/, and evidence/example_tests.json /
evidence/mermaid_render.json remain v3's committed bytes"), `portability_test.json` isn't
part of that set — it's `portability_test.py`'s own output, and this task's step 9 is
entirely about changing that script's behavior and requires its "full output" in the
validation file. Running it necessarily rewrites its designated output file. Verified the
new content is deterministic (running it twice, with and without playwright, in either
order produces the same final committed bytes for the "with playwright" case — see
validation file).

## Validation

`kit_lint.py check`: 0 errors/0 warnings. `selftest`: 105/105 mutations `detected` or
`skipped`, **`uncovered_codes: []`** (every `self.err`/`self.warn` call site now has at
least one mutation). `portability_test.py`: `status: passed` both without playwright (Mermaid
step records an explicit skip note) and with it (Mermaid actually renders via
`references/.mermaid/11`). ID regex demonstration confirms `E2E-001`/`FR-001` match with no
prefix, `SHA-256`/`APP-001`/`SPEC-001`/unprefixed-`PAY-FR-001` don't, and `PAY-FR-001`
matches once `[ids] prefix = "PAY-"` is set.

## Commit

`85206497a1d76eaeacd00fc91c1da6ef127c1d6b` (amended from `ef7f611`) on `feat/references-kit-v4`:
`fix(references/tools): configurable ids, multi-doc lint, evidence-bound results, complete selftest`
(16 files changed, 558 insertions, 130 deletions).

## CompactionDB

`[memory:decision] kit_lint.py ID/ITEM regex now built from an explicit kind allow-list plus
kit.toml [ids] prefix (no more [A-Z]+-\d{3,4} false-positives like SHA-256/APP-001);
multiple PRDs supported with cross-doc E030 dedup and per-PRD trace sections; E155
evidence-required applies to all doc types including BDD; E158 parses a fixed
実行結果|値|証跡のキー table instead of prose-scanning; selftest self-audits E/W code
coverage and fails on any gap; portability_test.py copies the real kit.toml (paths only
rewritten)`

Memory ID: `f3104c28-6a9d-44b8-bc5f-d213c494cbd9`

Round 2 (E159 fix): `[memory:decision] refkit-P2-B revision: E158's evidence-key resolution
now errors (E159) when a table row's 証跡のキー fails to resolve but the document's own
doc_type level exists in the evidence file (was: silently skipped, letting a typo'd key
like ut.pased pass unverified); skipping stays legitimate only when the doc's own level is
absent from evidence (ST/UAT not_run)`

Memory ID: `7b3ff146-b159-48ae-9203-450aa77eef83`

Exact commands and output in `.orchestration/validation/refkit-P2-B.md`.

## A note on tool output formatting (same hazard as refkit-P2-A)

Every edit in this task went through `Bash`/`python` file writes, never the Edit/Write
tools, per this task's own "Editing discipline" section. One lapse mid-task (a single
2-line addition made via the Edit tool to fix a selftest mutation) reformatted the entire
2200+-line file; caught it via `git diff --stat` before committing, reverted to the prior
commit, and replayed the full sequence of saved Bash/python patch scripts to reach the same
state cleanly (final diff: 308 lines, matching the actual functional change).

cost: n/a
