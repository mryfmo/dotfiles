# refkit-P8-b: 検証

## git log --oneline -3

```
1d5b093 merge: integrate tooling and hook remediation (refkit-P2-A/B/C, P0-06, P0-07) into feat/references-kit-v4-p3
57885bd docs(references): update sources, strategy, README and validation skeleton for kit v4 (part 1)
126e465 merge: integrate PRD/ADR/BDD/test-doc remediation (refkit-P3, P4, P5, P7, P0-05) into feat/references-kit-v4
```

## grep -c gherkin_source references/tools/kit_lint.py

```
13
```

## git diff --stat

```
 references/00_README.md                 |  8 +++----
 references/01_ADVERSARIAL_REVIEW.md     | 40 ++++++++++++++++-----------------
 references/02_RESEARCH_AND_DECISIONS.md |  2 +-
 references/03_CONVENTIONS.md            | 17 ++++++--------
 references/90_VALIDATION_REPORT.md      |  2 +-
 references/st/ST_SAMPLE.md              |  2 ++
 references/ut/UT_SAMPLE.md              |  2 +-
 7 files changed, 35 insertions(+), 38 deletions(-)
```

## kit_lint.py check（E120/E121/E103/E153 のみ許容）

```json
{
  "status": "failed",
  "errors": [
    "E153 example_tests.json: テストの実行証跡が現行のコード・テスト・.feature と不一致＝証跡が古い。再実行が必要",
    "E120 04_TRACEABILITY.md: 追跡表が正本と不一致（trace を再生成）",
    "E121 features/FEAT-002.feature: .feature が Markdown の Gherkin と不一致（extract を再実行。編集は片方向のみ）",
    "E121 features/FEAT-004.feature: .feature が Markdown の Gherkin と不一致（extract を再実行。編集は片方向のみ）",
    "E121 features/FEAT-006.feature: .feature が Markdown の Gherkin と不一致（extract を再実行。編集は片方向のみ）",
    "E121 features/FEAT-007.feature: .feature が Markdown の Gherkin と不一致（extract を再実行。編集は片方向のみ）",
    "E121 features/FEAT-008.feature: .feature が Markdown の Gherkin と不一致（extract を再実行。編集は片方向のみ）",
    "E103 mermaid_render.json: 描画証跡（Mermaid 11.14.0）が現行の図と不一致＝証跡が古い。再描画が必要",
    "E103 mermaid_render.json: 描画証跡（Mermaid 12.0.0）が現行の図と不一致＝証跡が古い。再描画が必要"
  ],
  "warnings": [],
  "stats": {
    "steps": 208,
    "unique_step_patterns": 70,
    "unique_step_ratio": 0.337,
    "relative_links": 155,
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
  "executed_at_utc": "2026-09-23T12:19:34+00:00",
  "scope": "文書検査のみ。製品試験・承認ではない"
}
```

All error codes present (E120, E121×5, E103×2, E153) are within the task's tolerated list. This matches the expected post-merge generated-artefact staleness the refkit-P2-C acceptance record predicted verbatim ("Merged-tree lint shows only generated-artefact staleness (E103×2, E120, E121×5, E153)"). No new error classes introduced by this task's edits.

## grep proving no stale branch-relative wording remains

```
$ grep -rln "この枝\|未反映\|feat/references-kit-v4-p3\|feat/references-kit-v4\b" \
    *.md prd/*.md bdd/*.md adr/*.md ut/*.md ct/*.md st/*.md uat/*.md
(no output — 0 files matched)
```

## git show --stat HEAD

```
commit 96f09b303ac4e3f6a34c39731ada2679f5c8ed9f
docs(references): reconcile conventions and common docs with the integrated kit v4 (part 2)
 .orchestration/autoskill/runs/refkit-P8-b.md |  3 +
 .orchestration/learning/refkit-P8-b.md       | 17 ++++++
 .orchestration/reports/refkit-P8-b.md        | 75 +++++++++++++++++++++++
 .orchestration/sandboxes/refkit-P8-b.md      |  7 +++
 .orchestration/validation/refkit-P8-b.md     | 90 ++++++++++++++++++++++++++++
 references/00_README.md                      |  8 +--
 references/01_ADVERSARIAL_REVIEW.md          | 40 ++++++-------
 references/02_RESEARCH_AND_DECISIONS.md      |  2 +-
 references/03_CONVENTIONS.md                 | 17 +++---
 references/90_VALIDATION_REPORT.md           |  2 +-
 references/st/ST_SAMPLE.md                   |  2 +
 references/ut/UT_SAMPLE.md                   |  2 +-
 12 files changed, 227 insertions(+), 38 deletions(-)
```

## contextdb 出力（memory add の結果 UUID）

```
b0e44b4b-5d2e-4006-a457-5f6324391627  01/02/00の「この枝には未反映」を「済」へ書き換え
51f1c970-522e-435b-897e-5a6c029c9c64  03 §6ゲート表の削除とF-01解消、§3/§5/§7・06§5の変更不要判断
38ad565a-7f54-4269-a675-85d447a613a8  durations→duration_sの修正とCT_SAMPLE.mdが変更不要だった理由
```
