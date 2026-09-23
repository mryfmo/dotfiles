# refkit-P2-A validation

## git diff --stat (before commit, showing the scope of this change)

```text
$ git diff --stat
 references/00_README.md                |   2 +-
 references/03_CONVENTIONS.md           |   6 +-
 references/05_AI_AGENT_INSTRUCTIONS.md |   2 +-
 references/bdd/BDD_GUIDE.md            |   2 +-
 references/bdd/BDD_TEMPLATE.md         |   2 +-
 references/tools/kit_lint.py           | 219 +++++++++++++++++++++++++++++++--
 6 files changed, 214 insertions(+), 19 deletions(-)
```

## uv run --python 3.12 --with gherkin-official --with PyYAML python tools/kit_lint.py check

```json
$ uv run --python 3.12 --with gherkin-official --with PyYAML python tools/kit_lint.py check
{
  "status": "passed",
  "errors": [],
  "warnings": [],
  "stats": {
    "steps": 172,
    "unique_step_patterns": 66,
    "unique_step_ratio": 0.384,
    "relative_links": 136,
    "mermaid_blocks": 20,
    "documents": 31,
    "fr": 28,
    "nfr": 9,
    "rules": 23,
    "scenarios": 41,
    "expanded_cases": 68,
    "adr": 2,
    "feature_files": 8,
    "test_items": {
      "ut": 18,
      "ct": 6,
      "st": 5,
      "uat": 11
    },
    "personas": 6
  },
  "tools": {
    "python": "3.12.3",
    "gherkin-official": "42.0.1",
    "PyYAML": "6.0.3"
  },
  "executed_at_utc": "2026-09-23T09:57:58+00:00",
  "scope": "文書検査のみ。製品試験・承認ではない"
}
EXIT=0
```

## uv run --python 3.12 --with gherkin-official --with PyYAML python tools/kit_lint.py selftest

```json
$ uv run --python 3.12 --with gherkin-official --with PyYAML python tools/kit_lint.py selftest
{
  "status": "passed",
  "baseline": "passed",
  "mutations": [
    {
      "mutation": "FRを2文にする",
      "expect": "E034",
      "status": "detected"
    },
    {
      "mutation": "FRの型と構文の不一致",
      "expect": "E033",
      "status": "detected"
    },
    {
      "mutation": "存在しない根拠ID",
      "expect": "E037",
      "status": "detected"
    },
    {
      "mutation": "NFRの検証計画欠落",
      "expect": "E043",
      "status": "detected"
    },
    {
      "mutation": "必須節の改名",
      "expect": "E020",
      "status": "detected"
    },
    {
      "mutation": "Gherkin構文破壊",
      "expect": "E050",
      "status": "detected"
    },
    {
      "mutation": "SCN重複",
      "expect": "E064",
      "status": "detected"
    },
    {
      "mutation": "未知の要件タグ",
      "expect": "E070",
      "status": "detected"
    },
    {
      "mutation": "PRD受入とBDDタグの不一致",
      "expect": "E072",
      "status": "detected"
    },
    {
      "mutation": "試験用語の混入",
      "expect": "E060",
      "status": "detected"
    },
    {
      "mutation": "ADR採用案が一覧にない",
      "expect": "E090",
      "status": "detected"
    },
    {
      "mutation": "ADR addresses不正",
      "expect": "E083",
      "status": "detected"
    },
    {
      "mutation": "ADR status語彙外",
      "expect": "E080",
      "status": "detected"
    },
    {
      "mutation": "リンク切れ",
      "expect": "E016",
      "status": "detected"
    },
    {
      "mutation": "表の列数不揃い",
      "expect": "E011",
      "status": "detected"
    },
    {
      "mutation": "図を変えると描画証跡が古くなる",
      "expect": "E103",
      "status": "detected"
    },
    {
      "mutation": "追跡表の手修正",
      "expect": "E120",
      "status": "detected"
    },
    {
      "mutation": ".feature の手修正",
      "expect": "E121",
      "status": "detected"
    },
    {
      "mutation": "NVTの割当が1つでない",
      "expect": "E146",
      "status": "detected"
    },
    {
      "mutation": "テスト項目の由来が存在しない",
      "expect": "E142",
      "status": "detected"
    },
    {
      "mutation": "設計書のテスト名がコードにない",
      "expect": "E152",
      "status": "detected"
    },
    {
      "mutation": "テストコードを変えると実行証跡が古くなる",
      "expect": "E153",
      "status": "detected"
    },
    {
      "mutation": "目的に受入シナリオがない",
      "expect": "E150",
      "status": "detected"
    },
    {
      "mutation": "機能がどの水準にも割り当てられていない",
      "expect": "E148",
      "status": "detected"
    },
    {
      "mutation": "front matter の語彙外",
      "expect": "E025",
      "status": "detected"
    },
    {
      "mutation": "合格と書いて実行証跡がない",
      "expect": "E155",
      "status": "detected"
    },
    {
      "mutation": "ペルソナの主体が存在しない",
      "expect": "E145",
      "status": "detected"
    },
    {
      "mutation": "1章の由来が本文に出てこない",
      "expect": "E157",
      "status": "detected"
    },
    {
      "mutation": "文書の実行結果が証跡と食い違う",
      "expect": "E158",
      "status": "detected"
    },
    {
      "mutation": "旅程が通るシナリオが存在しない",
      "expect": "E143",
      "status": "detected"
    },
    {
      "mutation": "gherkin_source: feature で extract → E123",
      "expect": "E123",
      "status": "detected"
    },
    {
      "mutation": "markdown モードでマーカーなし .feature が存在 → E122・削除されない",
      "expect": "E122",
      "status": "detected"
    },
    {
      "mutation": "feature モードで mirror 後にフェンスを手編集 → E121",
      "expect": "E121",
      "status": "detected"
    },
    {
      "mutation": "ルート外への相対リンク → E018",
      "expect": "E018",
      "status": "detected"
    }
  ],
  "executed_at_utc": "2026-09-23T09:57:59+00:00"
}
EXIT=0
```

## /tmp demonstration transcript

Ran under a throw-away copy (`/tmp/refkit-p2a-v2/k`; `/tmp/refkit-p2a` itself was not
writable/removable in this sandbox, so a sibling throw-away path under `/tmp` was used
instead — same kit tree, same procedure). Steps: switch `BDD_SAMPLE.md` to
`gherkin_source: feature`, hand-edit `features/FEAT-008.feature`, run `extract`
(must fail E123, file untouched — sha256sum before/after shown), run `mirror`, then
`check` (must pass), then hand-edit the fence directly and `check` again (must fail E121).

```text
=== Step 1: switch BDD_SAMPLE.md to gherkin_source: feature ===
replacements: 1
11:gherkin_source: feature

=== Step 2: hand-edit features/FEAT-008.feature ===
sha256 before:
07f2d0f383b009c19f37b68b51efc2539c3054753d284632765d2e712f690192  features/FEAT-008.feature
sha256 after hand-edit:
2797d1a26f5cd95bbc0a2aa93688ddcc04a1ec98cd8c5476dca1587b744f33cd  features/FEAT-008.feature

=== Step 3: run extract (expect E123, file untouched) ===
{
  "status": "failed",
  "errors": [
    "E123 features/FEAT-001.feature: gherkin_source: feature のため extract できない（mirror を実行）",
    "E123 features/FEAT-002.feature: gherkin_source: feature のため extract できない（mirror を実行）",
    "E123 features/FEAT-003.feature: gherkin_source: feature のため extract できない（mirror を実行）",
    "E123 features/FEAT-004.feature: gherkin_source: feature のため extract できない（mirror を実行）",
    "E123 features/FEAT-005.feature: gherkin_source: feature のため extract できない（mirror を実行）",
    "E123 features/FEAT-006.feature: gherkin_source: feature のため extract できない（mirror を実行）",
    "E123 features/FEAT-007.feature: gherkin_source: feature のため extract できない（mirror を実行）",
    "E123 features/FEAT-008.feature: gherkin_source: feature のため extract できない（mirror を実行）",
    "E121 features/FEAT-008.feature: Markdown のフェンスが .feature と不一致（mirror を再実行。編集は片方向のみ）"
  ],
  "warnings": [],
  "stats": {
    "steps": 172,
    "unique_step_patterns": 66,
    "unique_step_ratio": 0.384,
    "relative_links": 136,
    "mermaid_blocks": 20,
    "documents": 31,
    "fr": 28,
    "nfr": 9,
    "rules": 23,
    "scenarios": 41,
    "expanded_cases": 68,
    "adr": 2,
    "feature_files": 8,
    "test_items": {
      "ut": 18,
      "ct": 6,
      "st": 5,
      "uat": 11
    },
    "personas": 6
  },
  "tools": {
    "python": "3.12.3",
    "gherkin-official": "42.0.1",
    "PyYAML": "6.0.3"
  },
  "executed_at_utc": "2026-09-23T09:57:41+00:00",
  "scope": "文書検査のみ。製品試験・承認ではない"
}
EXIT=1
sha256 after extract attempt (must be unchanged from 'after hand-edit'):
2797d1a26f5cd95bbc0a2aa93688ddcc04a1ec98cd8c5476dca1587b744f33cd  features/FEAT-008.feature

=== Step 4: run mirror ===
{
  "status": "passed",
  "changed": [
    "bdd/BDD_SAMPLE.md"
  ],
  "errors": [],
  "executed_at_utc": "2026-09-23T09:57:42+00:00"
}
EXIT=0

=== Step 5: run check (expect pass) ===
{
  "status": "passed",
  "errors": [],
  "warnings": [],
  "stats": {
    "steps": 172,
    "unique_step_patterns": 66,
    "unique_step_ratio": 0.384,
    "relative_links": 136,
    "mermaid_blocks": 20,
    "documents": 31,
    "fr": 28,
    "nfr": 9,
    "rules": 23,
    "scenarios": 41,
    "expanded_cases": 68,
    "adr": 2,
    "feature_files": 8,
    "test_items": {
      "ut": 18,
      "ct": 6,
      "st": 5,
      "uat": 11
    },
    "personas": 6
  },
  "tools": {
    "python": "3.12.3",
    "gherkin-official": "42.0.1",
    "PyYAML": "6.0.3"
  },
  "executed_at_utc": "2026-09-23T09:57:42+00:00",
  "scope": "文書検査のみ。製品試験・承認ではない"
}
EXIT=0

=== Step 6: hand-edit the Markdown fence directly (diverge from .feature), then check (expect E121) ===
{
  "status": "failed",
  "errors": [
    "E121 features/FEAT-008.feature: Markdown のフェンスが .feature と不一致（mirror を再実行。編集は片方向のみ）"
  ],
  "warnings": [],
  "stats": {
    "steps": 172,
    "unique_step_patterns": 66,
    "unique_step_ratio": 0.384,
    "relative_links": 136,
    "mermaid_blocks": 20,
    "documents": 31,
    "fr": 28,
    "nfr": 9,
    "rules": 23,
    "scenarios": 41,
    "expanded_cases": 68,
    "adr": 2,
    "feature_files": 8,
    "test_items": {
      "ut": 18,
      "ct": 6,
      "st": 5,
      "uat": 11
    },
    "personas": 6
  },
  "tools": {
    "python": "3.12.3",
    "gherkin-official": "42.0.1",
    "PyYAML": "6.0.3"
  },
  "executed_at_utc": "2026-09-23T09:57:42+00:00",
  "scope": "文書検査のみ。製品試験・承認ではない"
}
EXIT=1
```

## python3.10 guard check

```text
$ uv run --python 3.10 --with gherkin-official --with PyYAML python tools/kit_lint.py check
kit_lint.py: Python 3.11 以上が必要（tomllib が標準ライブラリに加わったのは 3.11: https://docs.python.org/3/library/tomllib.html）。現在: 3.10.21
EXIT=2
```

## git show --stat HEAD

```text
commit 03a4215f0802dfc4a78d516d254056a334efd163
Author: Fumio Moriya <moriya.fumio@technopro.com>
Date:   Wed Sep 23 18:58:43 2026 +0900

    fix(references/tools): implement gherkin_source modes and stop extract from deleting features
    
    kit_lint.py never read the BDD front-matter key gherkin_source; extract
    always treated Markdown as the source and unconditionally unlinked and
    regenerated every features/*.feature, which would delete hand-maintained
    .feature files after a team migrated to gherkin_source: feature (E-01).
    
    - extract now honors gherkin_source per BDD document: markdown-mode
      fences still generate features/*.feature (now with a marker comment
      line so generated files are identifiable), but it refuses to touch
      feature-mode features (new E123, pointing at the new `mirror`
      subcommand) and never deletes an unmarked, unmatched .feature (new
      E122; only marker-carrying orphans from renamed/removed fences are
      pruned).
    - New `mirror` subcommand rewrites Markdown fences from features/*.feature
      (stripping the marker line) for feature-mode documents, leaving
      everything else untouched.
    - `check` compares fence <-> .feature ignoring the marker line, so v3's
      existing unmarked features/*.feature and evidence/* stay valid without
      regenerating or committing new bytes here.
    - New E124 for a missing/invalid gherkin_source value.
    - `_check_links` raised an uncaught ValueError for a relative link that
      resolves outside the kit root; it now reports E018 instead of crashing
      (E-08).
    - Added a Python-version guard (kit_lint.py needs 3.11+ for tomllib) that
      prints one line and exits 2 before any import that would otherwise fail
      with a less helpful traceback (E-14). render_mermaid.py/run_examples.py/
      portability_test.py are out of scope for this task.
    - selftest restores the v2 rule that a mutation's regex must match exactly
      once; matching more than once now reports FIXTURE_AMBIGUOUS as a
      selftest failure instead of silently mutating only the first hit
      (E-17). Three pre-existing mutations whose patterns matched multiple
      times under this stricter rule were re-anchored to a unique target
      so they stay meaningful. Added selftest coverage for E123, E122, the
      new feature-mode E121 direction, and E018.
    - New references/tools/README.md documents prerequisites (Python 3.11+
      with citation, uv-based install), each subcommand and its errors, the
      two gherkin_source modes, and the marker line format. Linked from
      00_README.md and 03_CONVENTIONS.md; 03_CONVENTIONS.md's command table
      gained the `mirror` row; BDD_GUIDE.md's migration-guidance row and
      BDD_TEMPLATE.md's gherkin_source comment now mention `mirror`;
      05_AI_AGENT_INSTRUCTIONS.md's render_mermaid.py line now includes the
      required --mermaid-dir flag.
    
    `kit_lint.py check` is 0 errors/0 warnings on the tree; 04_TRACEABILITY.md,
    features/, and evidence/ remain v3's committed bytes.
    
    Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>

 references/00_README.md                |   2 +-
 references/03_CONVENTIONS.md           |   6 +-
 references/05_AI_AGENT_INSTRUCTIONS.md |   2 +-
 references/bdd/BDD_GUIDE.md            |   2 +-
 references/bdd/BDD_TEMPLATE.md         |   2 +-
 references/tools/README.md             |  73 +++++++++++
 references/tools/kit_lint.py           | 219 +++++++++++++++++++++++++++++++--
 7 files changed, 287 insertions(+), 19 deletions(-)
```

## python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project

```text
$ python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "[memory:decision] kit_lint.py gherkin_source: markdown (Markdown fence is source, extract generates marked .feature) vs feature (.feature is source, mirror generates the Markdown fence copy); extract refuses (E123) and never deletes unmarked .feature (E122) in feature mode; check compares fence<->.feature ignoring the marker line"
a724bbe5-b13c-4905-bdd9-c3a4e1131026
```
