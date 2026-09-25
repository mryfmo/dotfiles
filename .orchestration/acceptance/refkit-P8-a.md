# refkit-P8-a acceptance record

status: accepted (2026-09-23T12:3xZ) with follow-ups assigned to refkit-P8-b
reviewer: claude-remediation-dot

## Verified independently (57885bd on feat/references-kit-v4-p3)
- Lint: only E120/E121/E103×2 (generated artefacts). 01 appendix is append-only (149 added, 0 removed) with the 91-row status table; 02 gains the 3-value 確認 vocabulary, S16 upgraded on the strength of the P0-04 PDF fetch, S30〜S36 added with dates; 06 §6 versions match P0-04 §16 and npm rows without dates are marked; 90 is a skeleton with `<P9>` placeholders (E014-safe); PRD KPI-002 cell and PRD_GUIDE 10 章 note; 05 role line; 00 version 4.0.0.
- Deviations justified: tools/README.md row omitted because the file did not exist on that branch; `{{P9}}`→`<P9>` to avoid E014; no ruff/prettier S-rows (not in P0-04).

## Defects to fix in P8-b (the task ran on the -p3 branch before integration, so several statements describe a branch, not the kit)
1. 02 判断表「Gherkin の置き場」, 06 §5 テスト名 row, 01 追補 (b) F-02/F-14 and the 「本枝には未反映」 wording: after the merge the integration branch contains `gherkin_source`/`mirror`/E122/E123/E159/`[ids] prefix`/multi-PRD — rewrite as kit facts (済), keep W160/E063 as 予定 until P4b lands.
2. 00_README archive row says 「v1〜v3」; only v2 and v3 kits exist in archive/ (v1 was never received here) — fix.
3. 90 §1 and UT_SAMPLE §5 reference `durations`; the evidence field is per-case `duration_s`.
4. 00 structure table: add `tools/README.md` and `tools/mermaid_common.py` now that they exist on the merged branch.

cost: n/a
