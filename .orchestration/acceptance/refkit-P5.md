# refkit-P5 acceptance record

status: accepted (2026-09-23T11:5xZ) after one narrow revise; final commit dcb6b1c on feat/references-kit-v4-p3
reviewer: claude-remediation-dot

## Round 1 (revise): see history — FR-014 tags, SCN-047 version, RULE-012 row, vocabulary form.
## Round 2 (accepted)
- Orchestrator lint on dcb6b1c: only E151 / E120 / E121 / E103×2 remain (all expected until P7/P9); E071/E072 pass with FR-014 受入 = RULE-011/015/019/021 + NVT-010 and `@FR-014` on the 履歴-asserting scenarios; RULE-012 row no longer lists FR-028; SCN-047 states the version it uses.
- Vocabulary registry: quoted values are now `<…>` placeholders; bare numbers stay literal with a documented reason (unquoted `<N>` would collide with Scenario Outline placeholders such as `<文字数>`). Accepted: E063 (P4b) must normalise both sides identically (quoted → `<…>`; numbers → a fixed token), so literal numbers in the registry remain valid.
- Substance as recorded in round 1 (SCN-043〜053, SCN-022 replaced, full 2 章 rule table with 優先度, 7 章 vocabulary, evidence key, 内容版 reference).

## Follow-ups
- P4b: implement E063 with the normalisation above; add 「障害が起きている」 to forbidden_terms.
- P7: UAT_SAMPLE ACT-006 line (E151). P9: regenerate features/04/evidence.

cost: n/a
