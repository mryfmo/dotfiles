# AGMSG-TASK refkit-P8-b: 共通文書の是正・第 2 弾（03_CONVENTIONS、統合後の事実への書き換え、00／90／UT_SAMPLE の残り）

Prerequisite: your branch `feat/references-kit-v4-p3` now contains the full integration (merge commit 1d5b093: P2-A/B/C tools incl. `gherkin_source`/`mirror`/E122/E123/E159/E104/`[ids] prefix`/multi-PRD/`mermaid_common.py`/`tools/README.md`, P0-06/P0-07, and P3–P8-a). Verify with `git log --oneline -3` and `grep -c gherkin_source references/tools/kit_lint.py` before editing. Plan: `/home/moriya/Workspace/dotfiles/.agents/worklog/claude/ai-references-vivid-sparrow.md` (第 2 部 §10). Acceptance notes to honour: `/home/moriya/Workspace/dotfiles/.orchestration/acceptance/refkit-P8-a.md` (4 defects), `refkit-P2-C.md` (duration_s), `refkit-P7.md` (k6 mix note), `refkit-P2-A.md` (02 mirror wording lives in the P2-A report under 「02 への反映案」 — if that section is absent, write the row from the implemented behaviour in tools/README.md).

## Scope (allowed_files)
`references/03_CONVENTIONS.md`, `references/00_README.md`, `references/01_ADVERSARIAL_REVIEW.md` (only inside 「## 6. v4 での追補」), `references/02_RESEARCH_AND_DECISIONS.md` (判断表 rows and 確認 column only), `references/06_TEST_STRATEGY.md` (§5 rows only), `references/90_VALIDATION_REPORT.md` (wording only, no numbers), `references/ut/UT_SAMPLE.md` (§5 実行時間 row only), `references/st/ST_SAMPLE.md` (§9 one sentence after the k6 block, optional), `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/refkit-P8-b.md`.

## Required changes
1. **F-01** 03 §6: replace the gate table body with 「ゲートの通過条件の正本は PRD 9 章。ここではゲート名（G1 実装着手／G2 受入／G3 本番導入／G4 成果評価）だけを定義する」— no conditions duplicated.
2. **F-03** 03 §2 「Gherkin」 row and 02 判断表「Gherkin の置き場」: describe both modes as implemented (markdown → `extract` writes marked `.feature`; feature → `mirror` rewrites the fences; E121 both directions; E122 unmarked orphan; E123 extract refused in feature mode). Remove every 「この枝には未反映」 / branch-name mention.
3. 03 §3: confirm it already describes `[ids] prefix` (P2-B) and remove any leftover instruction to edit `kit_lint.py`; §4 supersedes row: note that E086 becomes state-aware in P4b (予定) — one clause; §5: confirm the unconditional evidence rule (P2-B) is stated once; §7: confirm E104 wording (P2-C) and that the 図の種類 list equals `[mermaid] allowed_types`; §8: command table lists `mirror`, `--out`, `--allow-no-sandbox`, and links tools/README.md.
4. 01 追補 (a)/(b) and 06 §5 テスト名 row: rewrite branch-relative statements as kit facts on the merged branch (P2-A/B/C items are 済; W160 and E063 remain 予定 → refkit-P4b; P6/P9 remain 予定). Keep the table append-only in spirit: edit only rows/sentences that are now false.
5. 00: archive row 「v2〜v3」 (no v1); structure table gains `tools/README.md` and `tools/mermaid_common.py` descriptions; 使い方 step 4 mentions sandbox default and `--allow-no-sandbox`.
6. 90 §1 and UT_SAMPLE §5: `durations` → 「各テストの `duration_s`（JUnit XML の time）」.
7. Optional: ST_SAMPLE §9 one sentence acknowledging that detail/decide iterations issue an extra `op:list` request and the seed call is tagged `op:submit` (sample, 未実行).

## Validation file
verbatim: `git log --oneline -3`, `grep -c gherkin_source references/tools/kit_lint.py`, `git diff --stat`, `kit_lint.py check` (only E120/E121/E103/E153 tolerated), grep proving no 「未反映」/「本枝」/「feat/references-kit-v4-p3」 remains in references/ (except archive/README.md history), `git show --stat HEAD`, contextdb output.

## Editing discipline
Bash/python writes; intended hunks only.

## Commit
`docs(references): reconcile conventions and common docs with the integrated kit v4 (part 2)`.

## Forbidden
push; pr-create; editing PRD/ADR/BDD/tools/examples; numbers in 90; regenerating generated artefacts.

max_turns=40
