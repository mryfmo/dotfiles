# refkit-P2-B validation

## git diff --stat HEAD~1..HEAD (this task's commit)

```text
 references/03_CONVENTIONS.md              |   4 +-
 references/bdd/BDD_SAMPLE.md              |   1 +
 references/bdd/BDD_TEMPLATE.md            |   1 +
 references/ct/CT_SAMPLE.md                |   7 +-
 references/ct/CT_TEMPLATE.md              |   5 +-
 references/evidence/portability_test.json |  15 +-
 references/kit.toml                       |   3 +
 references/st/ST_SAMPLE.md                |   6 +-
 references/st/ST_TEMPLATE.md              |   5 +-
 references/tools/README.md                |  57 ++++++
 references/tools/kit_lint.py              | 308 +++++++++++++++++++++++++-----
 references/tools/portability_test.py      | 241 +++++++++++++++++------
 references/uat/UAT_SAMPLE.md              |   6 +-
 references/uat/UAT_TEMPLATE.md            |   5 +-
 references/ut/UT_SAMPLE.md                |  10 +-
 references/ut/UT_TEMPLATE.md              |   5 +-
 16 files changed, 549 insertions(+), 130 deletions(-)
```

## uv run --python 3.12 --with gherkin-official --with PyYAML python tools/kit_lint.py check

```json
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
  "executed_at_utc": "2026-09-23T10:57:05+00:00",
  "scope": "文書検査のみ。製品試験・承認ではない"
}
```

## uv run --python 3.12 --with gherkin-official --with PyYAML python tools/kit_lint.py selftest

```json
{
  "status": "passed",
  "baseline": "passed",
  "uncovered_codes": [],
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
      "mutation": "BDDがpassedなのにevidenceがない",
      "expect": "E155",
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
      "mutation": "PRD内でIDが重複する",
      "expect": "E030",
      "status": "detected"
    },
    {
      "mutation": "BDDのルールがどの要件にも結び付かない",
      "expect": "E073",
      "status": "detected"
    },
    {
      "mutation": "gherkin_sourceが不正な値",
      "expect": "E124",
      "status": "detected"
    },
    {
      "mutation": "UATのペルソナが存在しない",
      "expect": "E144",
      "status": "detected"
    },
    {
      "mutation": "全FRがMustになる",
      "expect": "W045",
      "status": "detected"
    },
    {
      "mutation": "末尾に改行がない",
      "expect": "E001",
      "status": "detected"
    },
    {
      "mutation": "front matterが壊れている",
      "expect": "E002",
      "status": "detected"
    },
    {
      "mutation": "コードフェンスが閉じていない",
      "expect": "E003",
      "status": "detected"
    },
    {
      "mutation": "アンカー重複",
      "expect": "E010",
      "status": "detected"
    },
    {
      "mutation": "H1が複数になる",
      "expect": "E012",
      "status": "detected"
    },
    {
      "mutation": "見出し階層を飛ばす",
      "expect": "E013",
      "status": "detected"
    },
    {
      "mutation": "未置換のプレースホルダが残る",
      "expect": "E014",
      "status": "detected"
    },
    {
      "mutation": "許可しないリンク種別",
      "expect": "E015",
      "status": "detected"
    },
    {
      "mutation": "アンカーが存在しない",
      "expect": "E017",
      "status": "detected"
    },
    {
      "mutation": "テンプレートにない節",
      "expect": "E021",
      "status": "detected"
    },
    {
      "mutation": "節の順序が異なる",
      "expect": "E022",
      "status": "detected"
    },
    {
      "mutation": "テンプレートの表が無い",
      "expect": "E023",
      "status": "detected"
    },
    {
      "mutation": "front matterのキーがテンプレートと異なる",
      "expect": "E024",
      "status": "detected"
    },
    {
      "mutation": "FRの明示アンカーが無い",
      "expect": "E031",
      "status": "detected"
    },
    {
      "mutation": "FRの型がEARSの6種でない",
      "expect": "E032",
      "status": "detected"
    },
    {
      "mutation": "FRの優先度が語彙外",
      "expect": "E035",
      "status": "detected"
    },
    {
      "mutation": "FRの根拠が無い",
      "expect": "E036",
      "status": "detected"
    },
    {
      "mutation": "FRの受入が無い",
      "expect": "E038",
      "status": "detected"
    },
    {
      "mutation": "FRの受入NVTが検証計画に無い",
      "expect": "E039",
      "status": "detected"
    },
    {
      "mutation": "GOALがどのFRからも参照されない",
      "expect": "E040",
      "status": "detected"
    },
    {
      "mutation": "KPIの計測手段が無い",
      "expect": "E041",
      "status": "detected"
    },
    {
      "mutation": "KPIの計測手段が存在しないFRを指す",
      "expect": "E042",
      "status": "detected"
    },
    {
      "mutation": "NFRの合格基準に数値が無い",
      "expect": "E044",
      "status": "detected"
    },
    {
      "mutation": "PRDの受入にBDDに無いRULEを書く",
      "expect": "E071",
      "status": "detected"
    },
    {
      "mutation": "Gherkinの言語がkit.toml設定と異なる",
      "expect": "E051",
      "status": "detected"
    },
    {
      "mutation": "languageの明示が無い",
      "expect": "E052",
      "status": "detected"
    },
    {
      "mutation": "FEATタグが複数になる",
      "expect": "E053",
      "status": "detected"
    },
    {
      "mutation": "Ruleに属さないシナリオ",
      "expect": "E054",
      "status": "detected"
    },
    {
      "mutation": "RULEタグが複数になる",
      "expect": "E055",
      "status": "detected"
    },
    {
      "mutation": "RULE_IDが重複する",
      "expect": "E056",
      "status": "detected"
    },
    {
      "mutation": "Ruleにシナリオが無い",
      "expect": "E057",
      "status": "detected"
    },
    {
      "mutation": "SCNタグが複数になる",
      "expect": "E058",
      "status": "detected"
    },
    {
      "mutation": "シナリオに要件タグが無い",
      "expect": "E059",
      "status": "detected"
    },
    {
      "mutation": "もしステップが無い",
      "expect": "E061",
      "status": "detected"
    },
    {
      "mutation": "ならばの後にもしが再登場",
      "expect": "E062",
      "status": "detected"
    },
    {
      "mutation": "ADRのidがADR-nnnn形式でない",
      "expect": "E081",
      "status": "detected"
    },
    {
      "mutation": "ADRのファイル名がidで始まらない",
      "expect": "E082",
      "status": "detected"
    },
    {
      "mutation": "ADRのaddressesが空",
      "expect": "E084",
      "status": "detected"
    },
    {
      "mutation": "ADRのsupersedesが存在しない",
      "expect": "E085",
      "status": "detected"
    },
    {
      "mutation": "supersedesが双方向でない",
      "expect": "E086",
      "status": "detected"
    },
    {
      "mutation": "supersededなのにsuperseded-byが無い",
      "expect": "E087",
      "status": "detected"
    },
    {
      "mutation": "confidenceが語彙外",
      "expect": "E088",
      "status": "detected"
    },
    {
      "mutation": "選択肢が2つ未満",
      "expect": "E089",
      "status": "detected"
    },
    {
      "mutation": "決定に理由が無い",
      "expect": "E091",
      "status": "detected"
    },
    {
      "mutation": "選択肢の長所短所が丸ごと無い",
      "expect": "E092",
      "status": "detected"
    },
    {
      "mutation": "短所の記載が無い",
      "expect": "E093",
      "status": "detected"
    },
    {
      "mutation": "確認方法が無い",
      "expect": "E094",
      "status": "detected"
    },
    {
      "mutation": "Mermaidにclickが混入",
      "expect": "E100",
      "status": "detected"
    },
    {
      "mutation": "accTitleが無い",
      "expect": "E101",
      "status": "detected"
    },
    {
      "mutation": "PRDを1件も指定しない",
      "expect": "E110",
      "status": "detected"
    },
    {
      "mutation": "ステップの語彙再利用率の上限を割る",
      "expect": "E074",
      "status": "detected"
    },
    {
      "mutation": "ステップ数上限を1にする",
      "expect": "W063",
      "status": "detected"
    },
    {
      "mutation": "テスト項目IDが重複する",
      "expect": "E140",
      "status": "detected"
    },
    {
      "mutation": "テスト項目の由来が空",
      "expect": "E141",
      "status": "detected"
    },
    {
      "mutation": "CTのNVTがPRDの検証計画に無い",
      "expect": "E147",
      "status": "detected"
    },
    {
      "mutation": "acceptedのADRを由来とするテスト項目が無い",
      "expect": "E149",
      "status": "detected"
    },
    {
      "mutation": "UATにACT対象外の理由が無い",
      "expect": "E151",
      "status": "detected"
    },
    {
      "mutation": "実行証跡のstatusが不合格",
      "expect": "E156",
      "status": "detected"
    },
    {
      "mutation": "参考実装のMermaid描画証跡が無い",
      "expect": "W102",
      "status": "detected"
    },
    {
      "mutation": "実行証跡ファイルが無い",
      "expect": "W154",
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
    },
    {
      "mutation": "kit.tomlのprefix未設定でPAY-FR-001を書くと無視されず不合格になる",
      "expect": "E070",
      "status": "detected"
    },
    {
      "mutation": "2つのPRDにまたがるFR-001の重複 → E030",
      "expect": "E030",
      "status": "detected"
    },
    {
      "mutation": "UATを2文書に分割してもcheckが通る",
      "expect": "passed",
      "status": "detected"
    },
    {
      "mutation": "SHA-256のような文字列が本文にあってもIDとして誤検出されない",
      "expect": "passed",
      "status": "detected"
    }
  ],
  "executed_at_utc": "2026-09-23T10:54:48+00:00"
}
```

## ID regex unit demonstration

```text
--- prefix unset (real kit.toml) ---
'E2E-001'            fullmatch(self.ID) = True
'FR-001'             fullmatch(self.ID) = True
'SHA-256'            fullmatch(self.ID) = False
'APP-001'            fullmatch(self.ID) = False
'SPEC-001'           fullmatch(self.ID) = False
'PAY-FR-001'         fullmatch(self.ID) = False
--- prefix = "PAY-" ---
'PAY-FR-001'         fullmatch(prefixed ID) = True
'FR-001'             fullmatch(prefixed ID) = False
'E2E-001'            fullmatch(prefixed ID) = False
```

## portability_test.py — without playwright (uv run --with gherkin-official --with PyYAML)

```json
{
  "status": "passed",
  "errors": [],
  "warnings": [
    "W154 example_tests.json: テストの実行証跡がない（tools/run_examples.py を実行）",
    "W102 mermaid_render.json: Mermaid 描画証跡がない（tools/render_mermaid.py を実行）"
  ],
  "stats": {
    "steps": 7,
    "unique_step_patterns": 4,
    "unique_step_ratio": 0.571,
    "relative_links": 2,
    "mermaid_blocks": 9,
    "documents": 15,
    "fr": 1,
    "nfr": 1,
    "rules": 1,
    "scenarios": 2,
    "expanded_cases": 3,
    "adr": 1,
    "feature_files": 1,
    "test_items": {
      "ut": 1,
      "ct": 1,
      "st": 1,
      "uat": 2
    },
    "personas": 1
  },
  "mermaid": "skipped: playwright is not importable from this interpreter",
  "note": "PRD・ADR・BDD・UT・CT・ST・UAT の全テンプレートのプレースホルダを機械的に埋め、PRD の任意節を全て削除した、別名・別ディレクトリ構成のプロジェクト。kit.toml は実物のコピー（パスのみ書き換え）。[tests] は最小のテストコード（test_name 関数1つ）で E152 まで検査する"
}
```

## portability_test.py — with playwright (flowapprove_core venv, mermaid rendered)

```json
{
  "status": "passed",
  "errors": [],
  "warnings": [
    "W154 example_tests.json: テストの実行証跡がない（tools/run_examples.py を実行）"
  ],
  "stats": {
    "steps": 7,
    "unique_step_patterns": 4,
    "unique_step_ratio": 0.571,
    "relative_links": 2,
    "mermaid_blocks": 9,
    "documents": 15,
    "fr": 1,
    "nfr": 1,
    "rules": 1,
    "scenarios": 2,
    "expanded_cases": 3,
    "adr": 1,
    "feature_files": 1,
    "test_items": {
      "ut": 1,
      "ct": 1,
      "st": 1,
      "uat": 2
    },
    "personas": 1
  },
  "mermaid": "rendered via /home/moriya/Workspace/dotfiles-w1/references/.mermaid/11/node_modules/mermaid",
  "note": "PRD・ADR・BDD・UT・CT・ST・UAT の全テンプレートのプレースホルダを機械的に埋め、PRD の任意節を全て削除した、別名・別ディレクトリ構成のプロジェクト。kit.toml は実物のコピー（パスのみ書き換え）。[tests] は最小のテストコード（test_name 関数1つ）で E152 まで検査する"
}
```

## git show --stat HEAD

```text
commit ef7f61182403e4a4d78fe4c14dd1c23e22ca7c8e
Author: Fumio Moriya <moriya.fumio@technopro.com>
Date:   Wed Sep 23 19:56:42 2026 +0900

    fix(references/tools): configurable ids, multi-doc lint, evidence-bound results, complete selftest
    
    P2-02 (F-02, E-11, E-12): kit_lint.py's ID regex was `[A-Z]+-\d{3,4}`, which
    matched incidental strings like SHA-256 and APP-001 as if they were tracked
    IDs, and didn't match multi-letter/digit kinds like E2E-001 at all. ID and
    ITEM are now built from an explicit kind allow-list plus an optional
    `[ids] prefix` (kit.toml), so multi-product setups can require e.g.
    `PAY-FR-001` without hand-editing the linter. `[docs] prd` now accepts more
    than one PRD: each is checked individually, IDs are required unique across
    all of them (new duplicate-across-docs case for E030), and `trace` emits a
    labelled FR/NFR section per PRD (a single PRD still gets the old unlabelled
    sections, so 04_TRACEABILITY.md's committed bytes are unaffected). E150/E151
    (UAT goal/actor coverage) now evaluate over the union of all UAT documents
    instead of failing a document for coverage another UAT document provides.
    
    P2-04 (E-04/D-03): the `'evidence' in d.meta` escape hatch is gone — any
    document with `last_run: passed` or `failed` must have an `evidence:` key
    pointing at a real file, BDD included. Added `evidence:` to BDD_TEMPLATE.md
    and BDD_SAMPLE.md's front matter to match.
    
    P2-05 (E-10): UT/CT/ST/UAT templates and samples gained a fixed
    `| 項目 | 値 | 証跡のキー |` table; E158 parses it and compares each value
    numerically against the evidence JSON (`<level>.total`/`.passed`/
    `.branch_coverage_percent`, `mutation.total`/`.killed`/`.score_percent`)
    instead of substring-scanning free prose. Two per-file coverage numbers in
    UT_SAMPLE/CT_SAMPLE (domain.py 100%, service.py 94.4%) have no table-key
    equivalent and were left in prose only — noted in the report for a later
    task.
    
    P2-06 (E-03, E-09, E-15): selftest now scans its own source for every
    `self.err('Exxx', ...)`/`self.warn('Wxxx', ...)` call and fails if any code
    has no mutation (`uncovered_codes`); it also enforces the v2 rule that a
    default mutation's regex match the corpus exactly once (already restored in
    refkit-P2-A). Added mutations for every previously-uncovered code (E001-E256
    range), re-targeted several at structural anchors (BDD Rule/Scenario tags,
    PRD ID rows, kit.toml thresholds) rather than sample-specific prose, and
    added the P2-02 mutations this task itself calls for (prefix-unset silence
    becomes a real error, cross-PRD duplicate ID, UAT split across two files,
    SHA-256-shaped prose causing no error). portability_test.py now copies the
    real kit.toml and rewrites only the path-bearing lines, keeping
    [vocab.*]/[ids]/[adr]/[gherkin] (including max_unique_step_ratio) and
    [tests]/[evidence] as shipped; it generates a one-function test_*.py so
    [tests] checks (E152 included) actually run, and conditionally renders
    Mermaid via references/.mermaid/11 when present and playwright is
    importable, recording an explicit skip note otherwise. Verified both ways
    (uv run with just gherkin-official/PyYAML, and the flowapprove_core venv
    with playwright) exit 0.
    
    `kit_lint.py check` stays 0 errors/0 warnings on the tree; 04_TRACEABILITY.md,
    features/, and evidence/example_tests.json/mermaid_render.json remain v3's
    committed bytes. evidence/portability_test.json is regenerated by design
    (it's this script's own output, not part of the v3 baseline it was imported
    alongside).
    
    Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>

 references/03_CONVENTIONS.md              |   4 +-
 references/bdd/BDD_SAMPLE.md              |   1 +
 references/bdd/BDD_TEMPLATE.md            |   1 +
 references/ct/CT_SAMPLE.md                |   7 +-
 references/ct/CT_TEMPLATE.md              |   5 +-
 references/evidence/portability_test.json |  15 +-
 references/kit.toml                       |   3 +
 references/st/ST_SAMPLE.md                |   6 +-
 references/st/ST_TEMPLATE.md              |   5 +-
 references/tools/README.md                |  57 ++++++
 references/tools/kit_lint.py              | 308 +++++++++++++++++++++++++-----
 references/tools/portability_test.py      | 241 +++++++++++++++++------
 references/uat/UAT_SAMPLE.md              |   6 +-
 references/uat/UAT_TEMPLATE.md            |   5 +-
 references/ut/UT_SAMPLE.md                |  10 +-
 references/ut/UT_TEMPLATE.md              |   5 +-
 16 files changed, 549 insertions(+), 130 deletions(-)
```

## python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project

```text
$ python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "..."
f3104c28-6a9d-44b8-bc5f-d213c494cbd9
```

---

# refkit-P2-B round 2 (revision): E158 unresolvable-key hole → E159

## uv run --python 3.12 --with gherkin-official --with PyYAML python tools/kit_lint.py check (after fix)

```json
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
  "executed_at_utc": "2026-09-23T11:04:50+00:00",
  "scope": "文書検査のみ。製品試験・承認ではない"
}
```

## Reviewer's exact scratch demonstration: UT_SAMPLE.md "| UT合格 | 125 | ut.passed |" → "| UT合格 | 999 | ut.pased |"

```text
$ (on a throw-away copy) replace "| UT合格 | 125 | ut.passed |" with "| UT合格 | 999 | ut.pased |"
$ uv run --python 3.12 --with gherkin-official --with PyYAML python tools/kit_lint.py check
failed
E159 ut/UT_SAMPLE.md: UT合格: 証跡のキー 'ut.pased' を証跡から解決できない
```

## uv run --python 3.12 --with gherkin-official --with PyYAML python tools/kit_lint.py selftest (after fix)

```json
{
  "status": "passed",
  "baseline": "passed",
  "uncovered_codes": [],
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
      "mutation": "BDDがpassedなのにevidenceがない",
      "expect": "E155",
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
      "mutation": "証跡のキーが誤記で解決できない",
      "expect": "E159",
      "status": "detected"
    },
    {
      "mutation": "PRD内でIDが重複する",
      "expect": "E030",
      "status": "detected"
    },
    {
      "mutation": "BDDのルールがどの要件にも結び付かない",
      "expect": "E073",
      "status": "detected"
    },
    {
      "mutation": "gherkin_sourceが不正な値",
      "expect": "E124",
      "status": "detected"
    },
    {
      "mutation": "UATのペルソナが存在しない",
      "expect": "E144",
      "status": "detected"
    },
    {
      "mutation": "全FRがMustになる",
      "expect": "W045",
      "status": "detected"
    },
    {
      "mutation": "末尾に改行がない",
      "expect": "E001",
      "status": "detected"
    },
    {
      "mutation": "front matterが壊れている",
      "expect": "E002",
      "status": "detected"
    },
    {
      "mutation": "コードフェンスが閉じていない",
      "expect": "E003",
      "status": "detected"
    },
    {
      "mutation": "アンカー重複",
      "expect": "E010",
      "status": "detected"
    },
    {
      "mutation": "H1が複数になる",
      "expect": "E012",
      "status": "detected"
    },
    {
      "mutation": "見出し階層を飛ばす",
      "expect": "E013",
      "status": "detected"
    },
    {
      "mutation": "未置換のプレースホルダが残る",
      "expect": "E014",
      "status": "detected"
    },
    {
      "mutation": "許可しないリンク種別",
      "expect": "E015",
      "status": "detected"
    },
    {
      "mutation": "アンカーが存在しない",
      "expect": "E017",
      "status": "detected"
    },
    {
      "mutation": "テンプレートにない節",
      "expect": "E021",
      "status": "detected"
    },
    {
      "mutation": "節の順序が異なる",
      "expect": "E022",
      "status": "detected"
    },
    {
      "mutation": "テンプレートの表が無い",
      "expect": "E023",
      "status": "detected"
    },
    {
      "mutation": "front matterのキーがテンプレートと異なる",
      "expect": "E024",
      "status": "detected"
    },
    {
      "mutation": "FRの明示アンカーが無い",
      "expect": "E031",
      "status": "detected"
    },
    {
      "mutation": "FRの型がEARSの6種でない",
      "expect": "E032",
      "status": "detected"
    },
    {
      "mutation": "FRの優先度が語彙外",
      "expect": "E035",
      "status": "detected"
    },
    {
      "mutation": "FRの根拠が無い",
      "expect": "E036",
      "status": "detected"
    },
    {
      "mutation": "FRの受入が無い",
      "expect": "E038",
      "status": "detected"
    },
    {
      "mutation": "FRの受入NVTが検証計画に無い",
      "expect": "E039",
      "status": "detected"
    },
    {
      "mutation": "GOALがどのFRからも参照されない",
      "expect": "E040",
      "status": "detected"
    },
    {
      "mutation": "KPIの計測手段が無い",
      "expect": "E041",
      "status": "detected"
    },
    {
      "mutation": "KPIの計測手段が存在しないFRを指す",
      "expect": "E042",
      "status": "detected"
    },
    {
      "mutation": "NFRの合格基準に数値が無い",
      "expect": "E044",
      "status": "detected"
    },
    {
      "mutation": "PRDの受入にBDDに無いRULEを書く",
      "expect": "E071",
      "status": "detected"
    },
    {
      "mutation": "Gherkinの言語がkit.toml設定と異なる",
      "expect": "E051",
      "status": "detected"
    },
    {
      "mutation": "languageの明示が無い",
      "expect": "E052",
      "status": "detected"
    },
    {
      "mutation": "FEATタグが複数になる",
      "expect": "E053",
      "status": "detected"
    },
    {
      "mutation": "Ruleに属さないシナリオ",
      "expect": "E054",
      "status": "detected"
    },
    {
      "mutation": "RULEタグが複数になる",
      "expect": "E055",
      "status": "detected"
    },
    {
      "mutation": "RULE_IDが重複する",
      "expect": "E056",
      "status": "detected"
    },
    {
      "mutation": "Ruleにシナリオが無い",
      "expect": "E057",
      "status": "detected"
    },
    {
      "mutation": "SCNタグが複数になる",
      "expect": "E058",
      "status": "detected"
    },
    {
      "mutation": "シナリオに要件タグが無い",
      "expect": "E059",
      "status": "detected"
    },
    {
      "mutation": "もしステップが無い",
      "expect": "E061",
      "status": "detected"
    },
    {
      "mutation": "ならばの後にもしが再登場",
      "expect": "E062",
      "status": "detected"
    },
    {
      "mutation": "ADRのidがADR-nnnn形式でない",
      "expect": "E081",
      "status": "detected"
    },
    {
      "mutation": "ADRのファイル名がidで始まらない",
      "expect": "E082",
      "status": "detected"
    },
    {
      "mutation": "ADRのaddressesが空",
      "expect": "E084",
      "status": "detected"
    },
    {
      "mutation": "ADRのsupersedesが存在しない",
      "expect": "E085",
      "status": "detected"
    },
    {
      "mutation": "supersedesが双方向でない",
      "expect": "E086",
      "status": "detected"
    },
    {
      "mutation": "supersededなのにsuperseded-byが無い",
      "expect": "E087",
      "status": "detected"
    },
    {
      "mutation": "confidenceが語彙外",
      "expect": "E088",
      "status": "detected"
    },
    {
      "mutation": "選択肢が2つ未満",
      "expect": "E089",
      "status": "detected"
    },
    {
      "mutation": "決定に理由が無い",
      "expect": "E091",
      "status": "detected"
    },
    {
      "mutation": "選択肢の長所短所が丸ごと無い",
      "expect": "E092",
      "status": "detected"
    },
    {
      "mutation": "短所の記載が無い",
      "expect": "E093",
      "status": "detected"
    },
    {
      "mutation": "確認方法が無い",
      "expect": "E094",
      "status": "detected"
    },
    {
      "mutation": "Mermaidにclickが混入",
      "expect": "E100",
      "status": "detected"
    },
    {
      "mutation": "accTitleが無い",
      "expect": "E101",
      "status": "detected"
    },
    {
      "mutation": "PRDを1件も指定しない",
      "expect": "E110",
      "status": "detected"
    },
    {
      "mutation": "ステップの語彙再利用率の上限を割る",
      "expect": "E074",
      "status": "detected"
    },
    {
      "mutation": "ステップ数上限を1にする",
      "expect": "W063",
      "status": "detected"
    },
    {
      "mutation": "テスト項目IDが重複する",
      "expect": "E140",
      "status": "detected"
    },
    {
      "mutation": "テスト項目の由来が空",
      "expect": "E141",
      "status": "detected"
    },
    {
      "mutation": "CTのNVTがPRDの検証計画に無い",
      "expect": "E147",
      "status": "detected"
    },
    {
      "mutation": "acceptedのADRを由来とするテスト項目が無い",
      "expect": "E149",
      "status": "detected"
    },
    {
      "mutation": "UATにACT対象外の理由が無い",
      "expect": "E151",
      "status": "detected"
    },
    {
      "mutation": "実行証跡のstatusが不合格",
      "expect": "E156",
      "status": "detected"
    },
    {
      "mutation": "参考実装のMermaid描画証跡が無い",
      "expect": "W102",
      "status": "detected"
    },
    {
      "mutation": "実行証跡ファイルが無い",
      "expect": "W154",
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
    },
    {
      "mutation": "kit.tomlのprefix未設定でPAY-FR-001を書くと無視されず不合格になる",
      "expect": "E070",
      "status": "detected"
    },
    {
      "mutation": "2つのPRDにまたがるFR-001の重複 → E030",
      "expect": "E030",
      "status": "detected"
    },
    {
      "mutation": "UATを2文書に分割してもcheckが通る",
      "expect": "passed",
      "status": "detected"
    },
    {
      "mutation": "SHA-256のような文字列が本文にあってもIDとして誤検出されない",
      "expect": "passed",
      "status": "detected"
    }
  ],
  "executed_at_utc": "2026-09-23T11:02:48+00:00"
}
```

## git show --stat HEAD (amended commit)

```text
commit 85206497a1d76eaeacd00fc91c1da6ef127c1d6b
Author: Fumio Moriya <moriya.fumio@technopro.com>
Date:   Wed Sep 23 19:56:42 2026 +0900

    fix(references/tools): configurable ids, multi-doc lint, evidence-bound results, complete selftest
    
    P2-02 (F-02, E-11, E-12): kit_lint.py's ID regex was `[A-Z]+-\d{3,4}`, which
    matched incidental strings like SHA-256 and APP-001 as if they were tracked
    IDs, and didn't match multi-letter/digit kinds like E2E-001 at all. ID and
    ITEM are now built from an explicit kind allow-list plus an optional
    `[ids] prefix` (kit.toml), so multi-product setups can require e.g.
    `PAY-FR-001` without hand-editing the linter. `[docs] prd` now accepts more
    than one PRD: each is checked individually, IDs are required unique across
    all of them (new duplicate-across-docs case for E030), and `trace` emits a
    labelled FR/NFR section per PRD (a single PRD still gets the old unlabelled
    sections, so 04_TRACEABILITY.md's committed bytes are unaffected). E150/E151
    (UAT goal/actor coverage) now evaluate over the union of all UAT documents
    instead of failing a document for coverage another UAT document provides.
    
    P2-04 (E-04/D-03): the `'evidence' in d.meta` escape hatch is gone — any
    document with `last_run: passed` or `failed` must have an `evidence:` key
    pointing at a real file, BDD included. Added `evidence:` to BDD_TEMPLATE.md
    and BDD_SAMPLE.md's front matter to match.
    
    P2-05 (E-10): UT/CT/ST/UAT templates and samples gained a fixed
    `| 項目 | 値 | 証跡のキー |` table; E158 parses it and compares each value
    numerically against the evidence JSON (`<level>.total`/`.passed`/
    `.branch_coverage_percent`, `mutation.total`/`.killed`/`.score_percent`)
    instead of substring-scanning free prose. A row whose 証跡のキー can't be
    resolved is now itself an error (**E159**) whenever the document's own
    doc_type level exists in the evidence file — added after review found the
    original version silently skipped an unresolvable key (e.g. a typo'd
    `ut.pased`), reopening the same "unverified number looks verified" hole
    E158 was rewritten to close. Skipping stays legitimate only when the
    document's own level is absent from evidence (the ST/UAT `not_run` case).
    Two per-file coverage numbers in UT_SAMPLE/CT_SAMPLE (domain.py 100%,
    service.py 94.4%) have no table-key equivalent and were left in prose only
    — noted in the report for a later task.
    
    P2-06 (E-03, E-09, E-15): selftest now scans its own source for every
    `self.err('Exxx', ...)`/`self.warn('Wxxx', ...)` call and fails if any code
    has no mutation (`uncovered_codes`); it also enforces the v2 rule that a
    default mutation's regex match the corpus exactly once (already restored in
    refkit-P2-A). Added mutations for every previously-uncovered code (including
    the new E159), re-targeted several at structural anchors (BDD Rule/Scenario
    tags, PRD ID rows, kit.toml thresholds) rather than sample-specific prose,
    and added the P2-02 mutations this task itself calls for (prefix-unset
    silence becomes a real error, cross-PRD duplicate ID, UAT split across two
    files, SHA-256-shaped prose causing no error). portability_test.py now
    copies the real kit.toml and rewrites only the path-bearing lines, keeping
    [vocab.*]/[ids]/[adr]/[gherkin] (including max_unique_step_ratio) and
    [tests]/[evidence] as shipped; it generates a one-function test_*.py so
    [tests] checks (E152 included) actually run, and conditionally renders
    Mermaid via references/.mermaid/11 when present and playwright is
    importable, recording an explicit skip note otherwise. Verified both ways
    (uv run with just gherkin-official/PyYAML, and the flowapprove_core venv
    with playwright) exit 0.
    
    `kit_lint.py check` stays 0 errors/0 warnings on the tree; 04_TRACEABILITY.md,
    features/, and evidence/example_tests.json/mermaid_render.json remain v3's
    committed bytes. evidence/portability_test.json is regenerated by design
    (it's this script's own output, not part of the v3 baseline it was imported
    alongside).
    
    Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>

 references/03_CONVENTIONS.md              |   4 +-
 references/bdd/BDD_SAMPLE.md              |   1 +
 references/bdd/BDD_TEMPLATE.md            |   1 +
 references/ct/CT_SAMPLE.md                |   7 +-
 references/ct/CT_TEMPLATE.md              |   5 +-
 references/evidence/portability_test.json |  15 +-
 references/kit.toml                       |   3 +
 references/st/ST_SAMPLE.md                |   6 +-
 references/st/ST_TEMPLATE.md              |   5 +-
 references/tools/README.md                |  60 ++++++
 references/tools/kit_lint.py              | 314 +++++++++++++++++++++++++-----
 references/tools/portability_test.py      | 241 +++++++++++++++++------
 references/uat/UAT_SAMPLE.md              |   6 +-
 references/uat/UAT_TEMPLATE.md            |   5 +-
 references/ut/UT_SAMPLE.md                |  10 +-
 references/ut/UT_TEMPLATE.md              |   5 +-
 16 files changed, 558 insertions(+), 130 deletions(-)
```

## python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project (round 2)

```text
$ python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "[memory:decision] refkit-P2-B revision: E158s evidence-key resolution now errors (E159)..."
7b3ff146-b159-48ae-9203-450aa77eef83
```
