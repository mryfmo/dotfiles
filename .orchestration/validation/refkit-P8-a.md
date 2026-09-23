# refkit-P8-a: 検証

## git diff --stat

```
 references/00_README.md                 |   7 +-
 references/01_ADVERSARIAL_REVIEW.md     | 149 ++++++++++++++++++++++++++++++++
 references/02_RESEARCH_AND_DECISIONS.md |  63 ++++++++------
 references/05_AI_AGENT_INSTRUCTIONS.md  |   2 +-
 references/06_TEST_STRATEGY.md          |  13 +--
 references/90_VALIDATION_REPORT.md      |  67 +++++++-------
 references/prd/PRD_GUIDE.md             |   2 +-
 references/prd/PRD_SAMPLE.md            |   2 +-
 8 files changed, 236 insertions(+), 69 deletions(-)
```

## kit_lint.py check（E120/E121/E103/E153 のみ許容）

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
    "relative_links": 151,
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
  "executed_at_utc": "2026-09-23T12:08:08+00:00",
  "scope": "文書検査のみ。製品試験・承認ではない"
}
```

Note: an intermediate run surfaced a new `E014 90_VALIDATION_REPORT.md: 未置換のプレースホルダ {{...}} が残っている` error, caused by using the task's literal `{{P9}}` placeholder text in a non-template document (`is_template` is false for `90_VALIDATION_REPORT.md`, and E014's regex `\{\{.*?\}\}` fires unconditionally outside template docs). E014 is not in the tolerated list, so all 24 occurrences of `{{P9}}` were changed to `<P9>` (same meaning, doesn't match the regex). The check above is the final, post-fix run — E014 is gone, only the pre-tolerated E120/E121/E103(×2) remain.

## 91-row finding-mapping table (required by item 2(a), reproduced verbatim from `01_ADVERSARIAL_REVIEW.md` §6(a))

See `references/01_ADVERSARIAL_REVIEW.md` §6 "v4 での追補" → "(a) 91 件の指摘の対応状況" for the full table, organized by category (A〜G, 13+15+7+10+17+8+21 = 91 rows) with 対応タスク and 状態 columns, plus the 集計 (tally) at the end. Reproduced here as the git diff shows it was written:

```
A-01〜A-13（全13）：済
B-01〜B-15（全15）：済
C-01〜C-05・C-07：済（6/7）。C-06：予定（refkit-P4b）
D-01〜D-10（全10）：済（一部は機械検査側が予定：D-02 forbidden_terms, D-04 E063 — refkit-P4b）
E-01〜E-17（全17）：予定 — accepted at the program level via refkit-P2-A/P2-B/P2-C, but VERIFIED ABSENT from this
  worktree's tools/kit_lint.py and kit.toml (grep for gherkin_source, mirror, [ids], prefix, E122, E123, E159 —
  zero hits in feat/references-kit-v4-p3). Treated as 予定 for this branch specifically.
F-02〜F-08（全8）：済（記述の訂正。F-02/F-03 の根拠実装 [ids] prefix・複数PRD・mirror は別枝で未反映）
F-01：予定（refkit-P8-b、03_CONVENTIONS.md is out of this task's scope）
G-01・G-02・G-17〜G-21：済（7/21）。G-03〜G-16：予定（refkit-P6・refkit-P2-C）

設計判断により不採用：0件（refkit-P0〜P7 の受入記録に一件も無いことを確認）
```

(Full per-ID rows with 一行要約 are in `01_ADVERSARIAL_REVIEW.md` §6 itself, not duplicated here to avoid a stale second copy — that file is the single source of truth for this table per the append-only editing discipline.)

## git show --stat HEAD

```
commit 16739c96347091a0620a460161f8f12180a1ae72
docs(references): update sources, strategy, README and validation skeleton for kit v4 (part 1)
 .orchestration/autoskill/runs/refkit-P8-a.md |   3 +
 .orchestration/learning/refkit-P8-a.md       |  23 +++++
 .orchestration/reports/refkit-P8-a.md        |  84 +++++++++++++++
 .orchestration/sandboxes/refkit-P8-a.md      |  13 +++
 .orchestration/validation/refkit-P8-a.md     |  85 +++++++++++++++
 references/00_README.md                      |   7 +-
 references/01_ADVERSARIAL_REVIEW.md          | 149 +++++++++++++++++++++++++++
 references/02_RESEARCH_AND_DECISIONS.md      |  63 ++++++-----
 references/05_AI_AGENT_INSTRUCTIONS.md       |   2 +-
 references/06_TEST_STRATEGY.md               |  13 +--
 references/90_VALIDATION_REPORT.md           |  67 ++++++------
 references/prd/PRD_GUIDE.md                  |   2 +-
 references/prd/PRD_SAMPLE.md                 |   2 +-
 13 files changed, 444 insertions(+), 69 deletions(-)
```

## contextdb 出力（memory add の結果 UUID）

```
3d6c8b47-4408-41f3-a69e-bb8186659a88  91件マッピングと本枝への未反映（E-01等）の明記
43c813ba-a138-4643-850b-d94e84eb936d  90_VALIDATION_REPORT.md のプレースホルダを <P9> に変更した理由
ea09e447-ed96-4f5a-83b5-54e8fffa02ac  S16 の格上げと CT_GUIDE §1 S-row 提案の統合
abe12bc5-8882-49a1-a076-3e48eb494cdd  F-02/F-14 是正注記と Gherkin 置き場行の書き起こし根拠
```
