# refkit-P2-C acceptance record

status: accepted (2026-09-23T12:2xZ) after one narrow revise; final commit 5f29164 on feat/references-kit-v4
reviewer: claude-remediation-dot

## Round 1 (revise): negative selftest mutations asserted status==passed and were MISSED on the real tree because of the expected E153.
## Round 2: accepted
- 5f29164: negative mutations now compare error-code sets against the unmutated baseline of the same temp copy. Orchestrator run on the real tree: 108/108 detected, uncovered []; overall selftest status is "failed" only because the baseline itself fails (E153, stale evidence) — honest and expected until P9 regenerates evidence.
- Everything else as verified in round 1 (mermaid_common.py, E104, sandbox default, run_examples measurement fields, mutmut 3 config keys, 03 §7, README).

## Integration
- Orchestrator merged feat/references-kit-v4-p3 @2196ba7 into feat/references-kit-v4 in dotfiles-w1 (merge commit 126e465). Two conflicts resolved: ct/CT_SAMPLE.md §8 (kept the P2-B 実行結果 table; P7's prose row is superseded, P9 fills values) and bdd/BDD_TEMPLATE.md (kept P2-B's evidence: line). Merged-tree lint shows only generated-artefact staleness (E103×2, E120, E121×5, E153).
- Follow-ups: 「所要時間は証跡 `durations`」 wording in UT_SAMPLE §5 → `duration_s` (P8-b); true branch coverage values refilled by P9.

cost: n/a
