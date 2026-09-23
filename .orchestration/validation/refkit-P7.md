# refkit-P7: 検証

## git diff --stat

```
 references/ct/CT_GUIDE.md    |  2 +-
 references/ct/CT_SAMPLE.md   |  2 +-
 references/st/ST_SAMPLE.md   | 60 ++++++++++++++++++++++++++++++++++++++------
 references/uat/UAT_GUIDE.md  |  1 +
 references/uat/UAT_SAMPLE.md |  8 +++---
 references/ut/UT_SAMPLE.md   |  6 ++---
 6 files changed, 64 insertions(+), 15 deletions(-)
```

## node --check（抽出した k6 スクリプト）

```
$ node --check /tmp/.../nvt_001.mjs
（出力なし＝構文エラーなし）
```

## npx tsc --noEmit（抽出した Playwright TS）

typescript／@playwright/test はこの環境に未インストール。`npx --no-install tsc --version` と `npx --no-install playwright --version` はいずれも
`npm error npx canceled due to missing packages and no YES option` で失敗した。`npm ls -g --depth=0` にも入っていない。
インストールには mise／npm によるワークツリー外への書き込みが必要になるため、task_file の条件（"without writes outside the worktree"）を満たせず、
**tsc --noEmit は未実行**。

## k6 inspect

`which k6` は何も返さない（未インストール）。同様にインストールはワークツリー外に書き込むため、**k6 inspect は未実行**。

## kit_lint.py check（E151 が解消していることの確認）

```json
{
  "status": "failed",
  "errors": [
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
    "relative_links": 149,
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
  "executed_at_utc": "2026-09-23T11:46:01+00:00",
  "scope": "文書検査のみ。製品試験・承認ではない"
}
```

E151 は出力に含まれておらず、解消を確認した。残る E120／E121／E103(×2) は task_file が明示的に許容している生成物の陳腐化（trace／extract／mermaid の再生成待ち、P9 予定）のみで、他のエラークラス（E020〜E025 テンプレート整合、E071／E072 相互整合等）は 0 件。

## git show --stat HEAD（コミット前の直前の受入済みコミット。参考）

```
commit dcb6b1cb696c93fa780dca0cc760e3864584c35f
docs(references/bdd): align scenarios with PRD 0.5.0, register step vocabulary, remove fault injection from Gherkin
 .orchestration/autoskill/runs/refkit-P5.md |   3 +
 .orchestration/learning/refkit-P5.md       |  17 ++
 .orchestration/reports/refkit-P5.md        |  56 +++++++
 .orchestration/sandboxes/refkit-P5.md      |   7 +
 .orchestration/validation/refkit-P5.md     | 182 +++++++++++++++++++++
 references/bdd/BDD_GUIDE.md                |   4 +-
 references/bdd/BDD_SAMPLE.md               | 243 ++++++++++++++++++++++++-----
 references/bdd/BDD_TEMPLATE.md             |  11 +-
 references/prd/PRD_SAMPLE.md               |   4 +-
 9 files changed, 477 insertions(+), 50 deletions(-)
```

（本タスクのコミット自体の `git show --stat HEAD` は、コミット後に本ファイルへ追記する。）

## contextdb 出力（memory add の結果 UUID）

```
48d4908f-42dc-4142-8ba5-e5e4dc612e1f  k6 負荷モデルの変更
28561c5f-1596-4e95-ae7a-a0339c255b65  認証方針の統一とテスト専用入口の明記
426efd69-2fbd-4f96-ab63-80385cbba1dd  PT実施者の是正
7d3b1e6b-5737-4c2a-bbbd-8ce322bc4635  CT_GUIDE §1 の無出典文の削除
6ad9ac75-e429-4594-a5a0-6fa4b88bb850  ACT-006／F-06 の記載場所と durations の未実装
```
