# AGMSG-TASK refkit-P8-a: 共通文書の是正・第 1 弾（00、01 追補、02、05、06、90 骨格、PRD の 2 セル）— 03_CONVENTIONS は第 2 弾（P8-b）

Covers plan tasks P8-01 … P8-06 (第 2 部 §10) and the deferred notes collected during P1–P7. Findings F-01 … F-08, E-02 (prose side), F-05. Plan: `/home/moriya/Workspace/dotfiles/.agents/worklog/claude/ai-references-vivid-sparrow.md`. Sources: `/home/moriya/Workspace/dotfiles/.orchestration/reports/P0-04-sources.md` (§16 versions; §2/§3/§4/§5/§6/§7/§14 for tool facts). Prerequisite: P3, P4, P5, P7 are on your branch `feat/references-kit-v4-p3` (`/home/moriya/Workspace/dotfiles-w2`). Reports for tasks that ran in the other worktree are readable at `/home/moriya/Workspace/dotfiles-w1/.orchestration/reports/refkit-*.md` (P0-01, P1, P2-A, P2-B, P0-06, P0-07) and acceptance records at `/home/moriya/Workspace/dotfiles/.orchestration/acceptance/`. `03_CONVENTIONS.md` is owned by a parallel task right now — do NOT edit it (item 1 moves to P8-b).

## Scope (allowed_files)
`references/00_README.md`, `references/01_ADVERSARIAL_REVIEW.md` (append-only 「v4 での追補」 section), `references/02_RESEARCH_AND_DECISIONS.md`, `references/05_AI_AGENT_INSTRUCTIONS.md`, `references/06_TEST_STRATEGY.md`, `references/90_VALIDATION_REPORT.md` (structure and non-numeric prose only; numbers are filled by P9), `references/prd/PRD_GUIDE.md` (3 章の 10 章行, KPI-002 note), `references/prd/PRD_SAMPLE.md` (KPI-002 計測手段 cell only), `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/refkit-P8.md`.

## Required changes
1. **F-01** (moved to P8-b; do not touch 03_CONVENTIONS.md here).
2. **F-02 / F-04** 01: append 「v4 での追補」 that (a) maps each of the 91 第 1 部 findings to its refkit task and status (済／予定（refkit-P6・P9・P4b・P8-b）／設計判断により不採用＋理由 — take 済 only from existing acceptance records; anything else is 予定), (b) corrects F-02/F-14 statements now that `[ids] prefix` and multi-PRD exist. 06 §5: state the test-name check as implemented (Python function-name match; other languages need `[tests] code` patterns) — or, if P2-B/P2-C made it configurable, describe that.
3. **F-03** 02 判断表 「Gherkin の置き場」 (03 §2 in P8-b): describe `extract`/`mirror` and the one-way rule per mode (take wording from refkit-P2-A report 「02 への反映案」).
4. **F-05 / E-02** 02: change the 確認 column vocabulary to 「取得して確認／概要のみ／継承」 and reclassify S16, S19, S25 (and any other row whose notes admit partial access). Add S-rows for every primary source newly used in P0–P7 (ruff force-exclude behaviour, prettier ignore semantics if cited, mutmut 3 scope, coverage.py fields, Hypothesis settings, pytest strict markers, k6 executors, Playwright auth, Python tomllib/PEP 723, ISTQB syllabus PDF, MADR 4.0.0 tag) with URL + retrieval date from P0-04. 06 §6: update every version from P0-04 §16 (mark npm rows whose publish date is 「not stated」 accordingly; do not invent dates) and mark 「実行」 only for tools P9 will actually run. 90 §3 環境表: explain the gherkin-official 29.0.0 vs 42.0.1 split (pytest-bdd pin) and state which interpreter/venv each check runs in — values themselves come from P9.
5. **F-06** 06 §5: add the reverse rule (Must requirement without a test condition or NVT is a warning, W160) and reference UT_SAMPLE §1's treatment of FR-005/FR-009/FR-026.
6. **F-07 / F-08** 05 §2 role line (add テスト設計書・テストコード); 00 §使い方 removal steps (include `[vocab.*]`, `[templates]` rows). 00: version 4.0.0, structure table gains ADR-0003/0004, tools/README.md, archive/.
7. Deferred minor items: PRD_SAMPLE KPI-002 計測手段 → `FR-026`（提出・確定時刻）only; PRD_GUIDE 3 章 10 章行 mentions the 用語集; CT_GUIDE §1 S-row if P7 proposed one.
8. 90: rewrite as the v4 validation report skeleton — sections 1–5 as in v3, with every numeric cell containing the literal placeholder `{{P9}}` and every claim phrased so P9 can fill it from `.orchestration/validation/refkit-P9.md`; keep the 「実施していないこと」 section truthful for v4 (ST/UAT still not executed).

## Validation file must contain verbatim
`git diff --stat`; `kit_lint.py check` (E120/E121/E103/E153 tolerated only for generated artefacts); the 91-row mapping table; `git show --stat HEAD`; contextdb output.

## Editing discipline
Bash/python writes; intended hunks only; keep the v3 table style (no realignment).

## Commit
`docs(references): update sources, strategy, README and validation skeleton for kit v4 (part 1)`.

## Forbidden
push; pr-create; editing PRD/ADR/BDD/tests/tools beyond the two named cells; inventing versions, dates or results; regenerating generated artefacts.

max_turns=50
