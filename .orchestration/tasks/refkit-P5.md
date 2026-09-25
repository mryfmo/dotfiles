# AGMSG-TASK refkit-P5: BDD 是正（PRD 0.5.0 との整合、語彙表の登録簿化、網羅表、Discovery 正本）

Covers plan tasks P5-01 … P5-07 (第 2 部 §7). Findings D-01 … D-10 and the BDD halves of B-02/B-03/B-07/B-08/B-09/D-06. Plan: `/home/moriya/Workspace/dotfiles/.agents/worklog/claude/ai-references-vivid-sparrow.md`. Sources: `/home/moriya/Workspace/dotfiles/.orchestration/reports/P0-04-sources.md` §1 (Gherkin Reference: Rule, tags, Scenario Outline). Prerequisites: P3 (PRD 0.5.0) and P4 are on your branch `feat/references-kit-v4-p3` in `/home/moriya/Workspace/dotfiles-w2`; read `.orchestration/reports/refkit-P3.md` 「既知の未解消の不整合」. `tools/kit_lint.py` and `kit.toml` are owned by a parallel worker — do not touch them.

Lint: `uv run --python 3.12 --with gherkin-official --with PyYAML python tools/kit_lint.py check`. In this task you MAY run `extract` so that E121 clears for the BDD you change, but do NOT commit `features/*.feature`, `04_TRACEABILITY.md` or `evidence/` (P9 regenerates them; note in the report which E120/E121/E153 remain for that reason).

## Scope (allowed_files)
`references/bdd/BDD_SAMPLE.md`, `references/bdd/BDD_TEMPLATE.md`, `references/bdd/BDD_GUIDE.md`, `references/prd/PRD_SAMPLE.md` (ONLY the 受入 cell of the FR-029 row: replace `NVT-010` by the RULE IDs that gain FR-029 scenarios, keeping NVT-010), `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/refkit-P5.md`.

## Required changes
1. **D-01 audit expectations backed by requirements.** With FR-014 generalised and FR-029 added in PRD 0.5.0: tag SCN-029/034 (履歴に取消・自動取消) with `@FR-014` in addition to their FR; SCN-038 (参考意見 0 件) with `@FR-014`. Add scenarios for FR-029 under RULE-003 (他組織の拒否が対象申請の組織の履歴に残る), RULE-009 (自己決裁の拒否が履歴に残る), RULE-010 and RULE-017 (one each), and add FR-029 to those rules' PRD 受入 correspondence (the PRD side was done in P3; verify E071–E073 both directions). New SCN IDs continue from SCN-043; never reuse SCN-039.
2. **B-02 replay precedence.** Update RULE-012/RULE-023 scenarios to the new FR-028 order: SCN-023 (再送→最初の結果) stays; SCN-024 (失効後の再送→対象なし) stays; SCN-025 (25 時間後→競合) stays; add SCN for 「再送だが別の主体が同じ要求識別子を使った→通常評価（自己決裁／競合など）」 under RULE-012 tagged `@FR-015 @FR-028`.
3. **D-02 fault injection out of Gherkin.** Remove SCN-022 from FEAT-004. RULE-011 keeps one business-observable example: 運用者が「監査保存停止」を宣言している状態（PRD 13 章の縮退）で決裁を要求すると 「一時的に処理不可」 and no state change. (Adding 「障害が起きている」 to `[gherkin].forbidden_terms` is done in refkit-P4b; do not edit kit.toml here.) Update 5 章 row 「依存先の停止・時間切れ・途中の失敗」 to name NVT-010 for the injection case and the new SCN for the declared-degradation case.
4. **D-03** front matter: `evidence: ../evidence/example_tests.json` (P2-B made it mandatory; confirm E155 passes).
5. **D-04 vocabulary registry.** Enumerate every distinct step pattern actually used in 4 章 (normalise numbers and quoted strings to `<…>`), and make 3 章's ステップ語彙表 list all of them (grouped 前提／もし／ならば). (E063 — the linter check that every step pattern is registered — is implemented in refkit-P4b, not here; you must still make the sets equal and show it with the python snippet in the validation file.) Update BDD_GUIDE §3 「ステップ語彙」 and BDD_TEMPLATE 3 章 note to say the table is a complete registry.
6. **D-05 / D-06 / D-07 / D-08.** 5 章: 「無認証」→ 「認証基盤の受入で確認（本キットの範囲外）」 instead of NVT-002. SCN-007: replace the 検索 example with 「検索結果に申請 "APP-001" は含まれない」 (FR-002 注記 per P3). SCN-018: add `ならば 要求は "入力不備" として拒否される` for the 0/1001 rows (use a second outline or split rows). RULE-018: add rows/scenario for 90 日当日 and 96 日 (deletion window per NFR-009: 7 days) — state exactly what is observable on each day.
7. **B-08 / B-09 alignment.** RULE-019 scenarios: SCN-034 outline rows only DRAFT・RETURNED; add a scenario 「SUBMITTED の申請は 180 日経過しても取り消されない」 tagged `@FR-022`. 3 章 用語表 「内容版」→ reference PRD 10 章の定義 (no独自定義); 「更新」 likewise.
8. **B-07 priority column.** 5 章の網羅表 or a new column in 2 章 ルール表: 優先度 (from PRD) so Could-only scenarios are identifiable; BDD_GUIDE §4 explains the G2 exemption for Could.
9. **D-09 / D-10.** 2 章 ルール表 lists all rules (23 + new), no delegation to 04. 7 章 実行結果 column restricted to `not_run|partial|passed|failed`; template note added. Bump `version: "0.5.0"`, `requirements: "../prd/PRD_SAMPLE.md 版0.5.0"`, `updated: 2026-09-23`, 7 章 row.

## Validation file must contain verbatim
`git diff --stat`; `kit_lint.py check` (list remaining E120/E121/E153 with the reason); a table SCN → RULE → FR for every added/changed scenario; the normalised step pattern list vs 語彙表 (must be equal sets); `git show --stat HEAD`; contextdb output.

## Editing discipline
Only intended hunks in `git diff`; template↔sample header parity must hold (E020–E025).

## Commit
`docs(references/bdd): align scenarios with PRD 0.5.0, register step vocabulary, remove fault injection from Gherkin`.

## Forbidden
push; pr-create; editing PRD/ADR/tests; committing regenerated features/04/evidence; deleting scenarios other than SCN-022 (re-home its intent as described); weakening expectations.

max_turns=50
