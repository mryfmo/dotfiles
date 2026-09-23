# refkit-P5: 検証記録（round 2 / revise 後の再提出）

## round 1 からの累積 git diff --stat（HEAD~1 = ef5a0bf、refkit-P4 の子コミット直後の状態との比較。verbatim）

```
 references/bdd/BDD_GUIDE.md    |   4 +-
 references/bdd/BDD_SAMPLE.md   | 331 +++++++++++++++++++++++++++++++++--------
 references/bdd/BDD_TEMPLATE.md |  11 +-
 references/prd/PRD_SAMPLE.md   |   4 +-
 4 files changed, 274 insertions(+), 76 deletions(-)
```

`git status --short` はこの 4 ファイルのみ（`features/`・`04_TRACEABILITY.md`・`evidence/` に変更なし）。

## round 2 で追加した差分（PRD FR-014 受入セル、verbatim）

```diff
diff --git a/references/prd/PRD_SAMPLE.md b/references/prd/PRD_SAMPLE.md
--- a/references/prd/PRD_SAMPLE.md
+++ b/references/prd/PRD_SAMPLE.md
@@ -122,7 +122,7 @@
-| <a id="FR-014"></a>FR-014 | 常時 | システムは、申請の状態遷移（提出・決裁・修正・取消・自動取消）と参考意見の提示について、その事実と監査記録を、両方とも成立するか両方とも成立しないかのいずれかにしなければならない。 | Must | GRD-001 | RULE-011、NVT-010 |
+| <a id="FR-014"></a>FR-014 | 常時 | システムは、申請の状態遷移（提出・決裁・修正・取消・自動取消）と参考意見の提示について、その事実と監査記録を、両方とも成立するか両方とも成立しないかのいずれかにしなければならない。 | Must | GRD-001 | RULE-011、RULE-015、RULE-019、RULE-021、NVT-010 |
```

BDD_SAMPLE.md 側の round 2 差分は次の 4 点（他は round 1 のまま）：

1. `@SCN-029 @FR-018` → `@SCN-029 @FR-018 @FR-014`
2. `@SCN-034 @FR-022` → `@SCN-034 @FR-022 @FR-014`
3. `@SCN-038 @FR-025` → `@SCN-038 @FR-025 @FR-014`
4. SCN-047 の もし step：「審査者 C が審査者 A と同じ要求識別子を使って申請 "APP-001" を却下する」→「審査者 C が審査者 A と同じ要求識別子を使い、現行の版を指定して申請 "APP-001" を却下する」
5. 2 章 RULE-012 行の要件列：`FR-015・FR-001・FR-028` → `FR-015・FR-001`
6. 3 章ステップ語彙表：78 行すべてを実例のリテラル値表記からプレースホルダ表記（`<ID>`・`<理由>`等）に書き直し（引用符内のみ。引用符外の生数値は変更せず）

## SCN → RULE → FR 表（追加・変更したシナリオすべて、round 2 で更新）

| SCN               | RULE     | FR             | 変更種別                                                      | 対応する指摘 |
| ----------------- | -------- | -------------- | ------------------------------------------------------------- | ------------ |
| SCN-007           | RULE-003 | FR-002         | 改訂（検索の例を除外）                                        | D-06         |
| SCN-018           | RULE-008 | FR-011         | 改訂（1〜1000 文字の正常系のみに）                            | D-07         |
| SCN-022 → SCN-048 | RULE-011 | FR-014         | 置換（障害注入 → 宣言的縮退。ID は再利用せず新規発番）        | D-02         |
| SCN-029           | RULE-015 | FR-018・FR-014 | 改訂（round 2 で `@FR-014` を追加）                           | D-01         |
| SCN-034           | RULE-019 | FR-022・FR-014 | 改訂（SUBMITTED を対象から除外。round 2 で `@FR-014` を追加） | B-08・D-01   |
| SCN-038           | RULE-021 | FR-025・FR-014 | 改訂（round 2 で `@FR-014` を追加）                           | D-01         |
| SCN-043           | RULE-003 | FR-029         | 新設                                                          | D-01         |
| SCN-044           | RULE-009 | FR-029         | 新設                                                          | D-01         |
| SCN-045           | RULE-010 | FR-029         | 新設                                                          | D-01         |
| SCN-046           | RULE-017 | FR-029         | 新設                                                          | D-01         |
| SCN-047           | RULE-012 | FR-015         | 新設（round 2 で もし step を版指定込みに改訂、決定性を確保） | B-02         |
| SCN-049           | RULE-003 | FR-002         | 新設                                                          | D-06         |
| SCN-050           | RULE-008 | FR-011         | 新設                                                          | D-07         |
| SCN-051           | RULE-018 | FR-021         | 新設                                                          | D-08         |
| SCN-052           | RULE-018 | FR-021         | 新設                                                          | D-08         |
| SCN-053           | RULE-019 | FR-022         | 新設                                                          | B-08         |

## ステップ語彙の登録簿等価性（python スニペット、round 2・プレースホルダ表記後、verbatim）

````python
import re
with open("bdd/BDD_SAMPLE.md", encoding='utf-8') as f:
    text = f.read()
gherkin_blocks = re.findall(r'```gherkin\n(.*?)\n```', text, re.S)
norm = lambda s: re.sub(r'\d+', 'N', re.sub(r'<[^>]+>', '<>', re.sub(r'"[^"]*"', '""', s)))
step_kw = ('前提', 'もし', 'ならば', 'かつ', 'しかし')
used_steps = set()
for block in gherkin_blocks:
    for line in block.split('\n'):
        line = line.strip()
        for kw in step_kw:
            if line.startswith(kw + ' '):
                used_steps.add(norm(line[len(kw):].strip()))
                break
vocab_section = re.search(r'\| 種別 \| 再利用するステップ文型 \| 意味・前提 \|\n\|---\|---\|---\|\n(.*?)\n\n', text, re.S)
registered = set()
for row in vocab_section.group(1).split('\n'):
    m = re.match(r'\| (前提|もし|ならば|かつ|しかし) \| (.*?) \| .*? \|$', row)
    if m:
        registered.add(norm(m.group(2)))
print(f"used={len(used_steps)} registered={len(registered)} missing={len(used_steps-registered)} extra={len(registered-used_steps)}")
print("SETS EQUAL:", used_steps == registered)
````

出力（verbatim）:

```
used=78 registered=78 missing=0 extra=0
SETS EQUAL: True
```

正規化ロジック（`norm`）は `tools/kit_lint.py` の E074 と同一の式（`"[^"]*"`→`""` → `<[^>]+>`→`<>` → `\d+`→`N` の順、内側から適用）。件数は round 1 と同じ 78 件のまま変わらない。理由：この正規化は引用符の中身をすべて`""`に、引用符の外の角括弧をすべて`<>`に、数字をすべて`N`に変換するだけで、それ以外の文字列差異（例えば背景の「組織 A に申請者 A と審査者 A がいる」と「組織 A に申請者 A と審査者 A と審査者 C と監査者 A がいる」のような、置換不能な語彙差）は正規化しても一致しない。したがってプレースホルダ表記に書き直しても、正規化後の集合（=規約上の「文型」の数）は変わらない。引用符の外にある無引用の数値（`25`・`97`・`180`など）は、`<N>`のような角括弧表記にすると`<[^>]+>`規則で`<>`に変換されてしまい、実際のコーパスの生数値（`N`に変換される）と一致しなくなるため、リテラルの数字のまま残した（BDD_SAMPLE.md 冒頭の登録簿の注記に明記）。

## kit_lint.py check（round 2、verbatim, 最終状態）

```json
{
  "status": "failed",
  "errors": [
    "E151 uat/UAT_SAMPLE.md: ACT-006: ペルソナも対象外の理由もない",
    "E120 04_TRACEABILITY.md: 追跡表が正本と不一致（trace を再生成）",
    "E121 features: .feature が Markdown の Gherkin と不一致（extract を再実行。編集は片方向のみ）",
    "E103 mermaid_render.json: 描画証跡（Mermaid 11.14.0）が現行の図と不一致＝証跡が古い。再描画が必要",
    "E103 mermaid_render.json: 描画証跡（Mermaid 12.0.0）が現行の図と不一致＝証跡が古い。再描画が必要"
  ],
  "warnings": [],
  "stats": {
    "steps": 208,
    "unique_step_patterns": 70,
    "unique_step_ratio": 0.337,
    "relative_links": 148,
    "mermaid_blocks": 22,
    "documents": 33,
    "fr": 29,
    "nfr": 9,
    "rules": 23,
    "scenarios": 51,
    "expanded_cases": 75,
    "adr": 4,
    "feature_files": 8,
    "test_items": { "ut": 18, "ct": 6, "st": 5, "uat": 11 },
    "personas": 6
  },
  "tools": {
    "python": "3.12.3",
    "gherkin-official": "42.0.1",
    "PyYAML": "6.0.3"
  },
  "executed_at_utc": "2026-09-23T11:19:31+00:00",
  "scope": "文書検査のみ。製品試験・承認ではない"
}
```

E071/E072 が FR-014・FR-028 とも両方向で合格していることを確認済み（上記 check 結果に E072 が含まれないことがその証拠。round 1 で発生した FR-028 の E072、および今回の FR-014 拡張後の E072 はいずれも 0 件）。残存する 5 件は round 1 から変わらず、全て生成物の陳腐化または既知の下流課題（E151・E120・E121・E103×2、詳細は round 1 の記載を参照）。

## extract 実行結果（round 2、E121 が一時的に解消したことの確認、verbatim 要約）

```
$ python tools/kit_lint.py extract
（E121が消える。E153が一時的に出現：FEAT-004・FEAT-008の変更後の.featureがexample_tests.jsonの実行証跡と不一致のため）
$ git checkout -- references/features/FEAT-002.feature references/features/FEAT-004.feature references/features/FEAT-006.feature references/features/FEAT-007.feature references/features/FEAT-008.feature
（.featureを元の内容に復元。round 1ではFEAT-008の復元を忘れていたため、round 2で追加で復元した。E121は再度出現するが意図的）
```

## git show --stat HEAD（コミット後、verbatim）

```
commit 560e6c89a8c96004a039120f6415d01063182199
Author: Fumio Moriya <moriya.fumio@technopro.com>
Date:   Wed Sep 23 20:11:49 2026 +0900

    docs(references/bdd): align scenarios with PRD 0.5.0, register step vocabulary, remove fault injection from Gherkin
    
    Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>

 .orchestration/autoskill/runs/refkit-P5.md |   3 +
 .orchestration/learning/refkit-P5.md       |  17 ++
 .orchestration/reports/refkit-P5.md        |  56 +++++++
 .orchestration/sandboxes/refkit-P5.md      |   7 +
 .orchestration/validation/refkit-P5.md     | 157 +++++++++++++++++++
 references/bdd/BDD_GUIDE.md                |   4 +-
 references/bdd/BDD_SAMPLE.md               | 243 ++++++++++++++++++++++++-----
 references/bdd/BDD_TEMPLATE.md             |  11 +-
 references/prd/PRD_SAMPLE.md               |   4 +-
 9 files changed, 452 insertions(+), 50 deletions(-)
```

## contextdb memory add（decision、verbatim ID）

round 1 で登録した 5 件に加え、round 2 で 3 件追加した：

```
208f26c0-039c-40e8-a795-ddb707bcba17  round2: FR-014受入拡張とSCN-029/034/038への@FR-014付与
4832ac80-3928-4062-9a7e-a79044736ad0  round2: SCN-047決定性修正、RULE-012表のFR-028誤記削除
66b25cf0-b8b4-4981-a2cb-bcc09f4e5cc9  round2: 語彙表のプレースホルダ表記化、78件不変の理由
```

```
c20c6886-1f9e-4546-be00-281b6307b9f2  D-01: FR-029 audit scenarios (RULE-003/009/010/017), PRD受入更新, @FR-014の非付与（round1時点）
e330217a-ebf9-4a06-9ee4-92355abce1d0  D-02: SCN-022→SCN-048 (fault injection -> declared degradation)
6796c739-51de-4671-bfc3-e58fc5fbe9b3  self-caught: @FR-028 tag removal from SCN-047/050 after E072
3faa5393-9c0b-4852-93ba-db873294cab9  D-04: 78-pattern step-vocabulary registry, normalization gotcha
6334548e-0d5f-4e02-9e88-7cf5c39059c6  B-08: SCN-034 SUBMITTED removal, SCN-053 addition
```
