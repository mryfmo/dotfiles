# refkit-P7 acceptance record

status: accepted (2026-09-23T12:0xZ)
reviewer: claude-remediation-dot

## Verified independently (2196ba7 in dotfiles-w2)
- Lint: E151 gone; only E120/E121/E103×2 (generated artefacts, P9). `node --check` on the extracted k6 script passes (orchestrator run).
- k6: four operations, `ramping-arrival-rate` warm-up (0→20/s, 5 min) then `constant-arrival-rate` 20/s for 30 min with `startTime: '5m'`, per-op p95 thresholds, `dropped_iterations` kept, decide uses a fresh request id and the `revision` from the detail call. Playwright seed now goes through the real submit operation; auth policy unified (per-worker storageState, per-test organisations); G2/G3 gate notes; PT executors are real users; CT_GUIDE §1 unsourced sentence removed (S-row proposal kept in the report); UT/CT prose numbers replaced by evidence references; FR-005/009/026 treatment stated in UT_SAMPLE §1.
- Deviations justified: ACT-006 placed in the existing §1 「対象外の主体」 cell (there is no 4 章 in UAT_SAMPLE); k6 inspect / tsc not run (tools not installed; installing would write outside the worktree).

## Notes (non-blocking, for P8/P9)
- k6 sample: the detail/decide branches issue an extra `op:list` request, so the effective mix is not exactly 25% each; the `submit` branch tags the test-support seed call as `op:submit`. P8 may add one sentence acknowledging this or P9 may leave as is (sample, 未実行).
- UT_SAMPLE §5 / CT_SAMPLE §8 now reference an evidence key `durations` that P2-C must emit under that name.

cost: n/a
