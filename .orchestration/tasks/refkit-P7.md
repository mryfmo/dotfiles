# AGMSG-TASK refkit-P7: テスト設計書の是正（ST／UAT、UT／CT の残り、ACT-006）

Covers plan tasks P7-01 … P7-04 (第 2 部 §9). Findings G-17 … G-21, G-14 (doc side), F-06 (doc side), plus the P3 follow-up (ACT-006 in UAT_SAMPLE → E151). Plan: `/home/moriya/Workspace/dotfiles/.agents/worklog/claude/ai-references-vivid-sparrow.md`. Sources: `/home/moriya/Workspace/dotfiles/.orchestration/reports/P0-04-sources.md` §8 (k6 constant-arrival-rate, thresholds with tags, dropped_iterations, ramping/warm-up), §9 (Playwright isolation, storageState per worker), §15 (ISTQB levels). Prerequisites: P3 (PRD 0.5.0) on the branch; the orchestrator gives the base commit.

## Scope (allowed_files)
`references/st/ST_SAMPLE.md`, `references/st/ST_GUIDE.md`, `references/uat/UAT_SAMPLE.md`, `references/uat/UAT_GUIDE.md`, `references/ct/CT_GUIDE.md` (§1 sentence only), `references/ut/UT_SAMPLE.md` §1/§4/§5 prose only (numbers → evidence keys; reproducibility claim), `references/ct/CT_SAMPLE.md` §8 prose only, `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/refkit-P7.md`.

## Required changes
1. **G-17 k6.** Rewrite the ST_SAMPLE k6 example to NFR-001: four operations (一覧・詳細・提出・決裁) at 25% each chosen per iteration, `constant-arrival-rate` rate 20/s for 30 min, a preceding warm-up scenario (5 min, `ramping-arrival-rate` or a lower constant rate — cite §8 for the option names), thresholds per operation `http_req_duration{op:list|detail|submit|decide}: p(95)<800`, `http_req_failed: rate<0.001`, `dropped_iterations: count==0`; decide requests must carry a fresh request id and a valid `seen_rev` fetched from the detail call so NVT-005 (通知遅延) can be measured in the same run. Validate with `node --check`; if k6 is installable via mise/npx without writes outside the worktree, also paste `k6 inspect`; else state it was not run.
2. **G-18 / G-19 Playwright and gates.** One consistent auth policy: per-worker `storageState` reuse for setup, per-test isolation of data (§9 quotes); list every test-support endpoint (`clock`, `seed`) in §3 as non-production and state that seeded applications go through the real state machine (`create`→`submit`), not a direct `state: 'SUBMITTED'`. §7: G2 requires a non-暫定 NVT-001 result on the production-scale environment, or an explicit judge-recorded deviation; §8: NVT-004 first execution is a G3 precondition, quarterly thereafter.
3. **G-20 / G-21.** UAT_SAMPLE §5: PT sessions performed by 実際の利用者／業務代表 (品質担当 may facilitate, not execute); UAT_GUIDE §2/§9 unchanged in substance, make the wording consistent. CT_GUIDE §1: either add a primary source for the 「結合テスト」 remark (add an S-row to 02 is NOT in your scope → put the proposed S-row text in the report; use ISTQB/JSTQB glossary if you find an official page via WebFetch and quote it) or delete the sentence.
4. **ACT-006 / E151.** UAT_SAMPLE 4 章 (主体の扱い): add 「ACT-006（システムの予定処理）は人が操作しないため受入シナリオ・ペルソナの対象外。期限処理の確認は UT-017/UT-018・CT・NVT-009 で行う」 so E151 clears.
5. **Numbers and claims.** UT_SAMPLE §4: reproducibility claim now true only after P6 (derandomize + database); phrase it conditionally on `conftest.py` profile `kit` and cite §6. UT_SAMPLE §5 「10秒以内」 and CT_SAMPLE §8 「1秒未満」: replace by 「所要時間は証跡 `durations` を参照」 (P2-C records durations). Any remaining coverage/mutation numbers in prose → refer to the 実行結果 table keys.
6. **F-06 doc side.** UT_SAMPLE §1: for FR-005, FR-009, FR-026 either name the test condition that now covers them (FR-005 gets UT from P6) or state the level that verifies them (FR-009 → CT with a stubbed AI timeout, FR-026 → NVT-011) so the reverse check W160 (P8) has an answer.

## Validation file must contain verbatim
`git diff --stat`; `node --check` on the extracted k6 and the Playwright `tsc --noEmit` if the toolchain from 90 §5 is available (else say so); `kit_lint.py check` showing E151 gone (E120/E121/E153 tolerated); `git show --stat HEAD`; contextdb output.

## Editing discipline
Bash/python writes only; intended hunks only; template↔sample parity (E020–E025) must hold.

## Commit
`docs(references/tests): fix ST/UAT samples (k6 model, auth policy, gates, PT actors) and record ACT-006 exclusion`.

## Forbidden
push; pr-create; editing PRD/BDD/ADR/tools/examples/02; inventing execution results.

max_turns=40
