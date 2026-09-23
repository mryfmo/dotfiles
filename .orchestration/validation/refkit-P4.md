# refkit-P4: 検証記録

## git diff --stat（コミット前、追跡対象ファイルのみ。新規 2 ファイルは別掲）

```
 references/adr/ADR-0001-ai-authority-boundary.md | 4 ++--
 references/adr/ADR-0002-decision-consistency.md  | 4 ++--
 references/adr/ADR_GUIDE.md                      | 4 ++--
 3 files changed, 6 insertions(+), 6 deletions(-)
```

新規ファイル（`git status --short`）：

```
?? references/adr/ADR-0003-ai-authority-boundary.md
?? references/adr/ADR-0004-decision-consistency.md
```

`ADR_TEMPLATE.md` は変更していない（理由は report ファイルの「task_file の指示から意図的に外した点」§1 を参照）。

## git diff（ADR-0001／ADR-0002／ADR_GUIDE.md、verbatim, full）

ADR-0001・ADR-0002 はどちらも front matter の `status` と `superseded-by` の 2 行のみが変更されている（本文・他のキーは無変更）。ADR_GUIDE.md は「front matter」行と「9 変えるとき」行の 2 箇所のみ。

```diff
diff --git a/references/adr/ADR-0001-ai-authority-boundary.md b/references/adr/ADR-0001-ai-authority-boundary.md
index 908ea11..38d9ea9 100644
--- a/references/adr/ADR-0001-ai-authority-boundary.md
+++ b/references/adr/ADR-0001-ai-authority-boundary.md
@@ -3,14 +3,14 @@ doc_type: adr
 sample: true
 id: "ADR-0001"
 title: "AI処理主体には決裁インターフェースの資格を発行しない"
-status: accepted
+status: superseded
 date: "2026-09-19"
 decision-makers: ["（架空）技術責任者", "（架空）セキュリティ責任者"]
 consulted: ["（架空）AI責任者", "（架空）運用責任者"]
 informed: ["（架空）製品責任者", "（架空）品質責任者"]
 addresses: ["FR-008", "FR-010", "FR-024"]
 supersedes: []
-superseded-by: null
+superseded-by: "ADR-0003"
 confidence: "中"
 ---
 # ADR-0001：AI処理主体には決裁インターフェースの資格を発行しない
diff --git a/references/adr/ADR-0002-decision-consistency.md b/references/adr/ADR-0002-decision-consistency.md
index 68ef71e..63355c1 100644
--- a/references/adr/ADR-0002-decision-consistency.md
+++ b/references/adr/ADR-0002-decision-consistency.md
@@ -3,14 +3,14 @@ doc_type: adr
 sample: true
 id: "ADR-0002"
 title: "決裁・監査記録・アプリ内通知・再送結果を同じデータベーストランザクションで確定する"
-status: accepted
+status: superseded
 date: "2026-09-19"
 decision-makers: ["（架空）技術責任者"]
 consulted: ["（架空）運用責任者", "（架空）品質責任者"]
 informed: ["（架空）製品責任者", "（架空）セキュリティ責任者"]
 addresses: ["FR-014", "FR-015", "FR-016", "FR-017", "NFR-005"]
 supersedes: []
-superseded-by: null
+superseded-by: "ADR-0004"
 confidence: "中"
 ---
 # ADR-0002：決裁・監査記録・アプリ内通知・再送結果を同じデータベーストランザクションで確定する
diff --git a/references/adr/ADR_GUIDE.md b/references/adr/ADR_GUIDE.md
index 77b2d91..79b7c93 100644
--- a/references/adr/ADR_GUIDE.md
+++ b/references/adr/ADR_GUIDE.md
@@ -46,13 +46,13 @@ stateDiagram-v2
 | 6 決定を書く | 「採用：**案X**。…ため。」と、どの決め手を優先したかを書く | 「総合的に優れる」で終わっていない |
 | 7 確認方法を決める | 実装がこの判断に従っているかを、何でいつ誰が確かめるか | 「テストで確認」で終わっていない |
 | 8 受理する | 決定権者が受理し status を accepted にする | 決定権者・日付が front matter にある |
-| 9 変えるとき | 新しい ADR を proposed で起票し `supersedes` に旧IDを書く。受理されたら旧 ADR の status を superseded、`superseded-by` を新IDにする | 双方向に結ばれている（リンター E086） |
+| 9 変えるとき | 新しい ADR を proposed で起票し `supersedes` に旧IDを書く。受理されたら旧 ADR の status を superseded、`superseded-by` を新IDにする。**現在のリンター（E086）は新 ADR の status に関わらず、旧 ADR 側の `superseded-by`・`status: superseded` を即時に要求する一方向の検査であり、proposed の間だけ許す猶予はまだ無い（リンターの状態依存化は次版）。それまでは新 ADR を起票する時点で旧 ADR 側も同時に書き換える** | 双方向に結ばれている（リンター E086） |

 ## 4. 章ごとの書き方

 | 章 | 書くこと | 不合格の例 |
 |---|---|---|
-| front matter | MADR 4.0.0 の5項目（status・date・decision-makers・consulted・informed）に、id・title・addresses・supersedes・superseded-by・confidence を加えたもの | 決定権者が空。AI が生成した氏名 |
+| front matter | MADR 4.0.0 の5項目（status・date・decision-makers・consulted・informed。MADR 4.0.0 テンプレート原文の front matter はこの5項目のみ。[02_RESEARCH_AND_DECISIONS.md](../02_RESEARCH_AND_DECISIONS.md) の S03 参照）に、id・title・addresses・supersedes・superseded-by・confidence を加えたもの。`proposed-on`（起票日）はキットが追加を検討している拡張だが、既存の accepted／superseded な ADR の front matter に新しいキーを追加できないため、`ADR_TEMPLATE.md` にはまだ加えていない。`status` が `proposed` でない文書では任意キーとして扱えるようリンターを直してから（次版）テンプレートへ追加する | 決定権者が空。AI が生成した氏名 |
 | 1 背景と課題 | どの要件・制約のもとで何を決めるか。2〜5文、最後は疑問文。判断に関係する境界だけの図 | 製品の一般的な説明。全体構成図 |
 | 2 判断の決め手 | 必須と比較の区別、出所、確かめ方 | 「速さを重視」だけ |
 | 3 検討した選択肢 | `- **案A**：…` の形で2つ以上 | 採用案だけが詳しい |
```

## kit_lint.py check（verbatim）

```json
{
  "status": "failed",
  "errors": [
    "E151 uat/UAT_SAMPLE.md: ACT-006: ペルソナも対象外の理由もない",
    "E120 04_TRACEABILITY.md: 追跡表が正本と不一致（trace を再生成）",
    "E103 mermaid_render.json: 描画証跡（Mermaid 11.14.0）が現行の図と不一致＝証跡が古い。再描画が必要",
    "E103 mermaid_render.json: 描画証跡（Mermaid 12.0.0）が現行の図と不一致＝証跡が古い。再描画が必要"
  ],
  "warnings": [],
  "stats": {
    "steps": 172,
    "unique_step_patterns": 66,
    "unique_step_ratio": 0.384,
    "relative_links": 147,
    "mermaid_blocks": 22,
    "documents": 33,
    "fr": 29,
    "nfr": 9,
    "rules": 23,
    "scenarios": 41,
    "expanded_cases": 68,
    "adr": 4,
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
  "executed_at_utc": "2026-09-23T10:46:58+00:00",
  "scope": "文書検査のみ。製品試験・承認ではない"
}
```

`adr: 4`（0001〜0004 すべて認識・検査対象）で、ADR 関連エラー（E080〜E094、E020〜E024）は 0 件。task_file が許容する E120/E121 のほか、E151（round 前から既知、UAT 側フォローアップ）と E103×2（本タスクで新設した Mermaid 図により発生。理由は report ファイル参照）が残る。E121 は発生していない。

## selftest（verbatim、30 件すべて `detected`。E086 の変異は既存 0 件のまま）

```json
{
  "status": "failed",
  "baseline": "failed",
  "mutations": [
    { "mutation": "FRを2文にする", "expect": "E034", "status": "detected" },
    {
      "mutation": "FRの型と構文の不一致",
      "expect": "E033",
      "status": "detected"
    },
    { "mutation": "存在しない根拠ID", "expect": "E037", "status": "detected" },
    { "mutation": "NFRの検証計画欠落", "expect": "E043", "status": "detected" },
    { "mutation": "必須節の改名", "expect": "E020", "status": "detected" },
    { "mutation": "Gherkin構文破壊", "expect": "E050", "status": "detected" },
    { "mutation": "SCN重複", "expect": "E064", "status": "detected" },
    { "mutation": "未知の要件タグ", "expect": "E070", "status": "detected" },
    {
      "mutation": "PRD受入とBDDタグの不一致",
      "expect": "E072",
      "status": "detected"
    },
    { "mutation": "試験用語の混入", "expect": "E060", "status": "detected" },
    {
      "mutation": "ADR採用案が一覧にない",
      "expect": "E090",
      "status": "detected"
    },
    { "mutation": "ADR addresses不正", "expect": "E083", "status": "detected" },
    { "mutation": "ADR status語彙外", "expect": "E080", "status": "detected" },
    { "mutation": "リンク切れ", "expect": "E016", "status": "detected" },
    { "mutation": "表の列数不揃い", "expect": "E011", "status": "detected" },
    {
      "mutation": "図を変えると描画証跡が古くなる",
      "expect": "E103",
      "status": "detected"
    },
    { "mutation": "追跡表の手修正", "expect": "E120", "status": "detected" },
    { "mutation": ".feature の手修正", "expect": "E121", "status": "detected" },
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
    }
  ],
  "executed_at_utc": "2026-09-23T10:47:35+00:00"
}
```

`status: "failed"` は既知の許容済みベースライン不合格（E151/E120/E103×2）によるもので、いずれの変異も見逃し（`MISSED`）は無い。**E086 を対象とする変異は元から 0 件であり、本タスクでは追加していない**（`tools/kit_lint.py` を編集できないため。report ファイル「task_file の指示から意図的に外した点」§2 参照。E086 の変異試験 3 件の追加は refkit-P4b で`tools/kit_lint.py`が編集可能になってから行う）。

## contextdb memory add（decision、verbatim ID）

```
8070abe6-9ce1-43a6-a67d-8e1ba13118f6  ADR-0003 Option C wording incl. ACT-006, addresses narrowed to FR-008
0b7665d0-318b-4749-a14d-994d52689361  ADR-0004 FR-017 mechanism choice (periodic scan), 悪い点/関連 fixes
28b5bcdb-aade-46cc-8479-4a6d10a41c36  E086 state rule: current one-directional behavior, deferred to P4b
da5b4773-ce9f-4139-b2b6-990fe4770dd7  proposed-on deviation: documented in guide prose, not added to template
```

## git show --stat HEAD（コミット後、verbatim）

```
commit 6d96d9606ddb6d0a979241314afc53ddd91b7310
Author: Fumio Moriya <moriya.fumio@technopro.com>
Date:   Wed Sep 23 19:50:27 2026 +0900

    docs(references/adr): supersede ADR-0001/0002 with ADR-0003/0004 (proposed)
    
    Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>

 .orchestration/autoskill/runs/refkit-P4.md       |   3 +
 .orchestration/learning/refkit-P4.md             |  23 +++
 .orchestration/reports/refkit-P4.md              |  50 +++++
 .orchestration/sandboxes/refkit-P4.md            |   7 +
 .orchestration/validation/refkit-P4.md           | 250 +++++++++++++++++++++++
 references/adr/ADR-0001-ai-authority-boundary.md |   4 +-
 references/adr/ADR-0002-decision-consistency.md  |   4 +-
 references/adr/ADR-0003-ai-authority-boundary.md | 108 ++++++++++
 references/adr/ADR-0004-decision-consistency.md  | 118 +++++++++++
 references/adr/ADR_GUIDE.md                      |   4 +-
 10 files changed, 565 insertions(+), 6 deletions(-)
```
