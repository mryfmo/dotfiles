# AGMSG-TASK refkit-P4: ADR 是正（ADR-0003／ADR-0004 による置換、テンプレート・指示書・E086 の状態依存化）

Covers plan tasks P4-01 … P4-04 (第 2 部 §6). Findings C-01 … C-07 and the ADR halves of B-01/B-02/B-06. Plan: `/home/moriya/Workspace/dotfiles/.agents/worklog/claude/ai-references-vivid-sparrow.md`. Sources: `/home/moriya/Workspace/dotfiles/.orchestration/reports/P0-04-sources.md` §10 (MADR 4.0.0 front matter and sections) and §11 (Azure WAF: append-only, supersede). Prerequisite: read `.orchestration/reports/refkit-P3.md` (in this worktree) — its 「下流への波及」 section lists the PRD changes (ACT-006, FR-028 order incl. 再送, FR-029, FR-017 Must, FR-005/FR-022 rewrites) that these ADRs must reference. Work in `/home/moriya/Workspace/dotfiles-w2` on branch `feat/references-kit-v4-p3` (P3 is already on it); `tools/kit_lint.py` is owned by a parallel worker — do not touch it.

Lint: `uv run --python 3.12 --with gherkin-official --with PyYAML python tools/kit_lint.py check` — E120/E121 (stale generated artefacts) are the only tolerated errors until P9.

## Scope (allowed_files)
`references/adr/ADR-0003-*.md` (new), `references/adr/ADR-0004-*.md` (new), `references/adr/ADR-0001-ai-authority-boundary.md` (front matter `status`/`superseded-by` ONLY), `references/adr/ADR-0002-decision-consistency.md` (same two keys ONLY), `references/adr/ADR_TEMPLATE.md`, `references/adr/ADR_GUIDE.md`, `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/refkit-P4.md`.

## Required changes
1. **C-02 / C-03 → ADR-0003 (supersedes ADR-0001).** Same question as ADR-0001 (where is the AI-cannot-decide prohibition enforced and how is it verifiable). `status: proposed`, `supersedes: ["ADR-0001"]`, `addresses: ["FR-008"]` only — state in 1 章 that FR-010 and FR-024 are requirements this ADR does not decide (they are satisfied by any option and verified by BDD RULE-007/RULE-020). Option C wording: 「決裁の受付口は人の対話セッション由来の主体だけを受け付ける。ACT-006（予定処理）の状態遷移は決裁ではなく期限処理として別の受付口を持ち、同じく AI 処理主体の資格を受け付けない」。Keep the 4-option comparison, all options with 短所, 4.2 確認方法 rows for both receiving points. ADR-0001: set `status: superseded`, `superseded-by: ADR-0003` — no other byte changes (append-only; cite Azure WAF).
2. **C-01 / C-04 / C-05 → ADR-0004 (supersedes ADR-0002).** Same question; `supersedes: ["ADR-0002"]`, `addresses: ["FR-014","FR-015","FR-016","FR-017","NFR-005"]`. Add the missing mechanism for FR-017: compare at least (a) a periodic scan of the notification table that moves >5-minute-old undisplayed notifications to the 要対応一覧, (b) client-side acknowledgement with server timeout, (c) dropping FR-017 from this ADR into a separate ADR. Decide with reasons; the 必須 driver row for FR-017 must name the chosen mechanism. In 4.1 悪い点 add: 保存済み結果の 24 時間後の掃除と、掃除後の再送が FR-028 の順序で「競合」になること。「関連」 must list only rules for the addressed FRs (RULE-011〜RULE-014; drop RULE-010). Mention the 冪等キーの構成（要求者・申請・操作・要求識別子）as decided in PRD 0.5.0. ADR-0002: `status: superseded`, `superseded-by: ADR-0004` only.
3. **C-07 → template/guide.** Add `proposed-on: "{{YYYY-MM-DD}}"` to ADR_TEMPLATE front matter (keep `date` as 「最後に決定が更新された日」); update the key list in ADR_GUIDE 4 章 and the MADR mapping sentence (cite §10: MADR 4.0.0's own five front-matter fields; `proposed-on` is a kit extension, say so). Add `proposed-on` to ADR-0003/0004 (2026-09-23) and to ADR-0001/0002? — NO: accepted ADR bodies/front matter must not gain keys; instead make the linter treat `proposed-on` as optional for documents whose `status` is not `proposed` (see 4).
4. **C-06 → E086 state-aware.** NOT in this task (kit_lint.py is being edited by a parallel task). Do this in refkit-P4b later. For now, keep the supersede links bidirectional (ADR-0001 `superseded-by: ADR-0003` while ADR-0003 is `proposed`) so the current linter passes, and write in ADR_GUIDE §3 手順 9 the intended state rule as a note 「（リンターの状態依存化は次版）」. Original spec for P4b follows — In kit_lint: when ADR X has `supersedes: [Y]` and X.status == proposed, require only Y to exist (no `superseded-by` on Y yet); when X.status == accepted, require Y.status == superseded and Y.superseded-by == X (bidirectional). Also enforce: a superseded ADR must point to an existing successor; a proposed successor may not yet be referenced by `superseded-by`?? — decide the least surprising rule consistent with ADR_GUIDE §3 手順 9 and write it down in both the guide and the linter message. Add selftest mutations: proposed successor without back-link (no E086), accepted successor without back-link (E086), `superseded-by` pointing to a missing file (E086). Update ADR_GUIDE §3 手順 9 to match exactly.
5. Template parity: ADR-0003/0004 must pass E020–E025 against the updated template (sections, tables, front-matter keys incl. `proposed-on`).

## Validation file must contain verbatim
`git diff --stat`; `kit_lint.py check` (only E120/E121 tolerated); `selftest` output including the three new E086 mutations; `git show --stat HEAD`; contextdb memory-add output (`[memory:decision]` for: ADR-0003 option C wording incl. ACT-006, ADR-0004 FR-017 mechanism choice, E086 state rule).

## Editing discipline
Apply edits so that `git diff` contains only the intended hunks; ADR-0001/0002 diffs must be exactly two front-matter lines each. Inspect `git diff` before committing.

## Commit
`docs(references/adr): supersede ADR-0001/0002 with ADR-0003/0004 (proposed)`.

## Forbidden
push; pr-create; editing ADR-0001/0002 beyond the two keys; editing PRD/BDD/tests; regenerating 04/features/evidence; weakening checks.

max_turns=40
