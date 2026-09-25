# refkit-P8-b acceptance record

status: accepted (2026-09-23T12:4xZ)
reviewer: claude-remediation-dot

## Verified independently (3af64f0 on feat/references-kit-v4-p3, post-integration)
- 03 §6 gate table replaced by the PRD-9 章 pointer; §2 Gherkin row and 02 判断表 describe both `gherkin_source` modes as implemented; §4 notes the E086 state rule as 予定 (P4b); §8 lists `--out`/`--allow-no-sandbox`.
- 00: archive row v2〜v3, tools row names `mermaid_common.py` and `tools/README.md`, step 4 mentions the sandbox default.
- 01 追補: all 「この枝には未反映」 rows rewritten as kit facts; grep for 未反映／本枝／references-kit-v4-p3 under references/ (excluding archive/) returns nothing. 90 and UT_SAMPLE use `duration_s`. ST_SAMPLE §9 note added.
- Lint unchanged: only generated-artefact staleness.

cost: n/a
