# AGMSG-TASK refkit-P3: PRD 是正（prd/PRD_SAMPLE.md → 0.5.0、PRD_TEMPLATE、PRD_GUIDE）

Covers plan tasks P3-01 … P3-11 (第 2 部 §5). Findings B-01 … B-15, plus the PRD-side halves of C-03, D-01, D-06, G-01, G-02. Plan: `/home/moriya/Workspace/dotfiles/.agents/worklog/claude/ai-references-vivid-sparrow.md` — read 第 1 部 §B fully and the referenced C/D/G items before editing. Sources: `/home/moriya/Workspace/dotfiles/.orchestration/reports/P0-04-sources.md` §12 (EARS templates). Work in `/home/moriya/Workspace/dotfiles-w1`, branch `feat/references-kit-v4`, in `references/`.

Language: all kit content is Japanese; keep the existing register. Requirements must satisfy the linter's EARS regexes (`EARS` dict in `tools/kit_lint.py`) and E030–E039/W045; run `uv run --python 3.12 --with gherkin-official --with PyYAML python tools/kit_lint.py check` after each step. E121/E120 (features/04 stale) are expected until P9 — every other error class must be zero. Do not edit BDD/ADR/tests in this task; where a PRD change requires downstream changes, list them in the report under 「下流への波及」 with the exact IDs (P4/P5/P6 will consume that list).

## Scope (allowed_files)
`references/prd/PRD_SAMPLE.md`, `references/prd/PRD_TEMPLATE.md`, `references/prd/PRD_GUIDE.md`, `references/02_RESEARCH_AND_DECISIONS.md` (判断表に行を追加するのみ), `references/01_ADVERSARIAL_REVIEW.md` (F-05 行の検査 ID 表記のみ), `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/refkit-P3.md`.

## Required changes (each item names the finding it closes)
1. **B-01 / C-03 system actor.** 4 章に `ACT-006 | システム（予定処理）：期限の到来による自動取消・予告・削除対象化を行う | 期限到来時の FR-021〜FR-023 の遷移と通知 | 決裁、参考意見、権限変更`。GRD-002 の定義を「人の操作でも ACT-006 の予定処理でもない状態変化の件数」に。6 章の状態表の 180 日行の主体を ACT-006 に。
2. **B-02 / C-04 / G-02 replay precedence.** FR-028 の順序を `対象なし・再送・自己決裁・競合・決裁できない状態・入力不備` に改訂（再送＝24 時間以内に同じ要求者・申請・操作・要求識別子の組で送られた要求。認可の再検査は対象なしの判定として再送より先に行う）。FR-015 に「同じ決裁要求とは要求者・申請・操作・要求識別子の組が一致する要求」を定義として追記（1 文 1 ID を守るため、定義は 10 章の用語欄に置き FR-015 からは参照）。FR-028 直後の注記を「24 時間を過ぎた再送は新しい要求として評価され、版不一致なら競合になる」に更新。
3. **B-03 / D-01 audit scope.** FR-014 を「システムは、申請の状態遷移（提出・決裁・修正・取消・自動取消）と参考意見の提示について、その事実と監査記録を、両方とも成立するか両方とも成立しないかのいずれかにしなければならない。」に一般化。新設 `FR-029 | 異常 | もし要求が対象なし・自己決裁・競合・決裁できない状態のいずれかとして拒否されたならば、システムは要求者・対象申請・拒否理由・時刻を対象申請の組織の監査記録に残さなければならない。| Must | GRD-001 | RULE-003、RULE-009、RULE-010、RULE-017（P5 で SCN を追加）`。GRD-001 の計測手段を `FR-014・FR-029 の監査記録` に。10 章の監査の最小記録に「拒否理由」を追加。
4. **B-04 / B-11 KPI baseline.** 13 章「段階導入」を「第 1 段階：人の審査経路のみ（AI 参考意見は停止）で 4 週間・100 件以上を運用し KPI-001／KPI-002 の基準値を FR-026 の記録から算出する。第 2 段階：AI 参考意見を限定した審査者から拡大」に書き換え。3 章の基準値欄を「未測定（第 1 段階で FR-026 の記録から算出）」、判定を「第 2 段階の 4 週間・100 件以上と第 1 段階の比較」に。FR-026 を「システムは、提出・審査着手・決裁確定の時刻を申請ごとに記録しなければならない。」に。9 章 G1 の「基準値の計測が完了」を「基準値の計測手順（第 1 段階）が合意」に、G4 を第 1／第 2 段階の比較に基づく判断に。RISK-004 の対処を第 1 段階に合わせる。
5. **B-05 / B-10 versions.** 1 章「いま求める判断」を「版 0.5.0 のレビュー（G1 実装着手の可否）」に。15 章 0.4.0 行の影響 ID に `G3` を追加。15 章に 0.5.0 行（日付 2026-09-23、本タスクの変更の要約、影響 ID 全列挙、未承認）を追加し front matter `version: "0.5.0"`、`updated: "2026-09-23"`。
6. **B-06 priority.** FR-017 を Must に変更。02 の判断表に行「FR-017 の優先度 | ①Should のまま NFR-005 と ADR の必須決め手から外す ②Must | ② | NFR-005 の合格基準と ADR-0002 の必須決め手が FR-017 を前提にしており、運用者の把握は GRD-001 の追跡性に効くため」。
7. **B-07 Could and G2.** 9 章 G2 の通過条件に「優先度 Could の要件だけを具体化するシナリオは G2 の必須対象から除く（実行はするが、不合格でも判定者が記録して通過できる）」を追記。PRD_TEMPLATE の G2 行にも同じ趣旨の placeholder 文を反映。
8. **B-08 FR-022 scope.** FR-022／FR-023 の対象を「DRAFT または RETURNED の申請が 180 日間（166 日間）申請者による更新を受けなかったとき」に限定し、「更新」を 10 章の用語欄で「申請者による内容の保存・提出・修正」と定義。6 章の状態表の該当行から SUBMITTED を外す。7 章末尾の FR-022 の注記を更新。
9. **B-09 content version.** 10 章に用語欄（表）を新設：`内容版 | 提出のたびに確定する番号。RETURNED から修正して保存したときに 1 増える。DRAFT 中の編集では増えない`、`更新`（上記）、`同じ決裁要求`（上記）。
10. **B-12 / B-13 / G-01 input rules.** 10 章の入力規則表に `決裁理由 | 必須。正規化後 1〜1000 コードポイント` を追加し、FR-011 を「申請者本人でない有効な審査者が SUBMITTED の申請に理由区分と入力規則を満たす理由を添えて承認・却下・差戻しを要求したとき、…」に短縮。提供元 URL の単位を「2048 コードポイント以内」に。FR-005 を「申請が DRAFT・RETURNED 以外の状態である間、システムは申請内容の編集を拒否しなければならない。」に一般化（G-01 の要件側）。
11. **D-06 search.** FR-002 の直後に注記「検索・一覧では、権限のない申請は結果に含めないことをもって拒否とする（個別の拒否結果は返さない）」を追加。
12. **B-14 / B-15 guide and gate.** PRD_GUIDE §2 手順 4 の検査範囲を `E030〜E039、W045` に統一し、01_ADVERSARIAL_REVIEW.md F-05 行の検査 ID も同じ表記に。9 章 G1 に「対象スライスの 12 章に未起票の ADR が無い」を追加（RISK-001 の ADR は G1 の前提になる）。
13. **P3-11 template parity.** 上記のうち構造に影響するもの（10 章の用語表の新設、入力規則表の行、G1／G2 の文言）を PRD_TEMPLATE に反映し、E020〜E024 を通す。PRD_GUIDE の該当節（3 章の 10 章行、4 章の例文、5 章）を整合させる。

## Validation file must contain verbatim
`git diff --stat`; `kit_lint.py check` full output（E120/E121 以外が 0 であること。E040〜E044 を含む）; a table 「要件 ID → 変更種別（新設／改訂／文言のみ）→ 閉じた指摘 ID」; the 「下流への波及」 list (BDD rules/SCN to add or change, ADR items, tests); `git show --stat HEAD`; contextdb memory-add output with the decisions (ACT-006, FR-028 順序, FR-029, KPI 基準値の第 1 段階方式) marked `[memory:decision]`.

## Commit
`docs(references/prd): resolve PRD contradictions and unmeasurable metrics (0.5.0)`.

## Editing discipline
Your Edit/Write tools may run a post-write formatter that rewrites whole files (table realignment, CJK spacing) and can break template↔sample exact-match checks. Apply edits so that `git diff` contains only the intended hunks (e.g. Bash/python writes), and inspect `git diff --stat` and `git diff` before committing. Never commit formatter noise.

## Forbidden
push; pr-create; editing files outside scope; regenerating 04/features/evidence; deleting or weakening existing requirements to satisfy the linter; inventing measurements or approvals.

max_turns=50
