## Findings

- P2 (high) [f10 s2] home/dot_dsh/plugins/omp-gateway/test/use-cases.test.mjs:1: The PR body's Threat table omits this added path, violating the standing requirement for one row per changed path.
- P2 (high) [f1 s5] home/dot_dsh/plugins/omp-gateway/proof/run-proof.mjs:80: The fix for carried dc336b67 P2 (proof/run-proof.mjs, line 59) drops exit-status validation: a child printing pong then exiting 7 makes the proof exit 0.
- P2 (high) [f1 s4] home/dot_dsh/plugins/omp-gateway/test/use-cases.test.mjs:778: The listener check treats failed lsof output as an empty result; an injected permission error with status 1 and empty stdout passes, violating the failed-read rule.
- P2 (high) [f1 s4] home/dot_dsh/plugins/omp-gateway/translate.mjs:74: A nonempty content array containing only unsupported or null blocks bypasses EMPTY_RESPONSE and emits finish without any assistant content, defeating the claimed bad-reply control.
- P2 (high) [f1 s4] home/dot_dsh/plugins/omp-gateway/gateway-client.mjs:231: Forgetting the child before confirmed termination loses a process that ignores SIGTERM; abort reports completion and close() returns undefined while the child remains alive.

## Reproduced

- Homebrew git verified clean head 6bc0c2cbd44a76901c33acc36458518a300cb2ab; the scoped diff adds 16 files and 2311 lines. System git was unavailable because xcrun is missing.
- git diff --check passed; final git status remained clean.
- Plain node --test was blocked by the sandbox's OpenSSL configuration read restriction; setting OPENSSL_CONF only for the parent still left six child-process tests failing for that environmental reason.
- An in-memory bootstrap adding --openssl-config=/dev/null to test child launches ran 87 tests: 42 passed, 45 skipped because DSH is absent from the isolated home, zero failed.
- python3 -m unittest tests.unit.test_dsh_profile tests.unit.test_dsh_hook_coverage passed all 11 tests using the installed Python binary.
- scripts/lint-retired-terms.py exited 0.
- run-proof.mjs --dsh /usr/bin/true --case pong exited 1, confirming the original no-output false pass is fixed.
- Proof subprocess failure injection used a real child printing pong and exiting 7; the proof nevertheless exited 0.
- The unchanged g2 test callback passed with injected lsof status 1, permission-denied stderr and empty stdout.
- toChunks probes with unsupported-only or null-only content emitted finish without content or an error; missing text fields also passed validation.
- Lifecycle fake-child probes showed a request during close reused the closing child and received GATEWAY_EXIT; a failed kill left no tracked child.
- A real child ignoring SIGTERM remained alive after ABORTED while client.pid and close() returned undefined; the probe explicitly killed and reaped it.

## Notes

Offline assessment completed with no P0/P1 findings. Real-login composition and remote CI claims were not independently verified. Findings with weight below 10 are filed under the standing rules.

Blocking: 0
Filed: 4
Verdict: correct
