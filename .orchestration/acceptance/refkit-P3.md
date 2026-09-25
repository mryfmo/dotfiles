# refkit-P3 acceptance record

status: accepted (2026-09-23T10:4xZ) after two revise rounds; final commit ef5a0bf on feat/references-kit-v4-p3
reviewer: claude-remediation-dot (orchestrator, adversarial review)

## Refuted / blocking
1. **Formatter noise dominates the commit.** `git show --stat f16e143`: 01_ADVERSARIAL_REVIEW.md 82 lines, 02_RESEARCH_AND_DECISIONS.md 123 lines, PRD_GUIDE.md 130, PRD_TEMPLATE.md 155, PRD_SAMPLE.md 327. The task allowed one line in 01 and one row in 02; the rest is table realignment and inserted spaces between Latin/digits and CJK (e.g. the H1 title `FlowApprove（社内ソフトウェア利用申請とAI審査補助）` became `…と AI 審査補助）`, `版1.0.0` → `版 1.0.0`). These are content changes to files outside the intended hunks, make substantive review impossible, and will conflict with every later task touching 01/02/PRD_GUIDE. The task file said 「out-of-scope-edits」 are forbidden; whole-file reformatting is an out-of-scope edit even inside an allowed file.
2. **`04_TRACEABILITY.md` regenerated and committed** (5 lines) although `regenerate-04-features-evidence` was a forbidden action. P9 regenerates all generated artefacts once, after BDD/ADR/tests are consistent.

## Accepted on the merits (keep in the revised commit)
- All 13 substantive items as listed in the report table; FR-029 受入 = NVT-010 (extended) is an acceptable interim because the BDD rules gain FR-029 scenarios only in P5 (P5 will then move 受入 to the RULEs).
- The two deviations from the task file are well reasoned (NVT-010 extension; appending rather than replacing the FR-028 note).
- Follow-ups recorded for P5 (RULE-019/SCN-034 SUBMITTED row) and P7 (ACT-006 line in UAT_SAMPLE so E151 clears).

## Required revision
1. Rebuild the change so that `git diff d3281de -- references/` contains only intended hunks: start from the d3281de version of each of the five kit files, re-apply the intended edits with a method that does not trigger the post-write formatter (Bash heredoc / python writes), keep original table alignment and original CJK spacing everywhere you did not intend to change.
2. Drop `references/04_TRACEABILITY.md` from the commit (restore d3281de bytes).
3. Squash into one commit `docs(references/prd): resolve PRD contradictions and unmeasurable metrics (0.5.0)` on `feat/references-kit-v4-p3` (rewriting your own branch is fine; never touch main or feat/references-kit-v4). `.orchestration/**` files may stay in the commit.
4. Validation: paste `git diff d3281de --stat -- references/` (expect roughly: 01 ≤ 2 lines, 02 ≤ 3 lines, PRD_GUIDE small, PRD_TEMPLATE moderate, PRD_SAMPLE only the intended rows), the full `git diff d3281de -- references/01_ADVERSARIAL_REVIEW.md references/02_RESEARCH_AND_DECISIONS.md`, and `kit_lint.py check` (only E151 for ACT-006 and E120 for the now-stale 04 are tolerated).

cost: n/a (worker reported n/a)

## Round 2 (2026-09-23T10:3xZ): revise (narrow)
- Rebuilt commit 3b5a3d6 verified: `git diff d3281de --stat -- references/` = 01 (2), 02 (1), PRD_GUIDE (4), PRD_TEMPLATE (14), PRD_SAMPLE (66); no formatter noise; 04 restored; check shows only E151 (ACT-006 in UAT) and E120 (stale 04), both tolerated.
- Substantive review of the PRD diff: items 1–8, 10–13 of the task are correctly applied (ACT-006, GRD-002, FR-005/011/014/017/022/023/026/028 rewrites, FR-029, FR-002 note, NVT-010 extension, G1/G2/G4, 13 章, RISK-004, 15 章 0.4.0/0.5.0, template placeholders, guide E030〜E039).
- **One defect remains (B-09):** the new 10 章 用語集 defines 内容版 as 「申請内容が修正されるたびに1つ増える番号」 — this is the BDD's contradictory wording, not the definition the task specified. It contradicts FR-019 (increment only on RETURNED→修正して保存) and SCN-006 (SUBMITTED keeps 内容版 1). Required text: 「提出のたびに確定する番号。RETURNED から修正して保存したときに1増える。DRAFT 中の編集では増えない」.
- Minor (not blocking, record for P8): KPI-002 計測手段 still cites FR-003 alongside FR-026; PRD_GUIDE 3 章の 10 章行 does not yet mention the 用語集.

## Round 3: accepted
- ef5a0bf: 内容版 definition now 「提出のたびに確定する番号。RETURNED から修正して保存したときに1増える。DRAFT 中の編集では増えない」; diff stat unchanged (5 files, +58/−29). Merge into feat/references-kit-v4 deferred until worker 1 is idle (branch ref must not move under an active worktree).
