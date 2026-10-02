# Acceptance: dot-ccstatusline-ubuntu26-hang-T59-a01

- **Decision:** ACCEPTED. PR #230 squash-merged to `main` as `07442713` (head `cc19dd4c84e500ec617b95752032e3b3c86c424a`, base `750cc4a9`). Merged without `--delete-branch` while worker-c holds `fix/ccstatusline-ubuntu26-hang`.
- **Worker:** `claude-standard-dot-a005` (worker-c). task_rev `7e090867…`, then `be02c71f…` after PONG decision 1 (both matched by the worker).
- **Exemption declared:** acceptance and final integration (gate, merge, records); orchestrator mutated no repository code.

## What was accepted

- `.github/workflows/test.yaml` (+13/−1): the statusline smoke puts `$(mise -C <statusline-mise> where node)/bin` first on the smoke `PATH` and asserts `node` resolves from mise's pinned install; the 5 s budget, `sudo unshare --net` / `sandbox-exec` isolation and `scripts/check-statusline-tools.py` are unchanged.
- `tests/unit/test_runtime_health.py` (+3/−2): the no-tar `PATH` guard is `not (link.exists() or link.is_symlink())`, nothing caught, skipped or deduplicated (PONG decision 1, orchestrator-approved scope addition after verifying the `FileExistsError` for the dangling `/usr/bin/grub-ntldr-img` in job 111054323730).
- Three `ci(diag): TEMPORARY` commits (6e0faeba, 1e280118, 50588cfc) are fully reverted by the head; `git diff origin/main..cc19dd4c` touches only the two files above.

## Orchestrator adversarial review (independent re-derivation)

- **Mechanism demonstrated.** From the diagnostics job logs (runs 37072287780, 37073281320, 37074296650): mise trace `shim[node] SYSTEM /usr/local/bin/node` and the strace `execve("/usr/local/bin/node", …)` show the smoke ran the image's system node, not the pinned 26.10.0; `fincore` showed 0 of 126,595,440 bytes resident before the first run and 54 MB faulted in by it; the cold strace has no `connect`/`sendto`/DNS syscall. The diagnostics ran under the same `sudo unshare --net` and env array as the smoke (verified in commit 50588cfc's step). With the pinned node first on `PATH` the same cold, no-network `--version` took 0.22 s.
- **ccstatusline not at fault.** Verified in the local 2.2.30 bundle (`dist/ccstatusline.js`, `main()`): `--version` prints `getPackageVersion()` and exits before `initConfigPath` and any network code. No pin bump; none needed.
- **Residual, accepted with note.** The >5 s magnitude of the original failure (run 37064146970) was not reproduced: measured cold durations were 0.62 s plain and 2.80 s under strace. The mechanism (SYSTEM fallback + cold read) is shown, the magnitude is attributed to runner-disk variance. The fix removes both the shim hop and the system node from the smoke's resolution path, and the new `case` assertion turns any recurrence on the pinned node into a distinguishable failure. The test.yaml comment's "0.6 s to over 5 s" range therefore mixes a measurement with the inferred original figure; accepted as is.
- **Latent defect corrected.** The smoke previously exercised the image's node rather than the pinned toolchain; it now tests what users get through mise.
- **Report accuracy.** Diff stat, commit list, 718 unit tests, canary and all required checks green on cc19dd4c: all re-verified (`gh pr checks 230`, run 37076377562 success).

## Audit

- `herdr-agents --audit cc19dd4c` → `.orchestration/validation/dot-ccstatusline-ubuntu26-hang-T59-a01-audit.md`, **Verdict: correct**, no findings (high confidence). The approval rationale names both fix hunks (`test.yaml:227`, `test_runtime_health.py:1032`) and the CI run for the exact SHA, so coverage is of the fix, not only the removed diagnostics. Disposition: no findings to disposition.

## PR feedback sweep (head cc19dd4c)

- `.orchestration/validation/dot-ccstatusline-ubuntu26-hang-T59-a01-pr-feedback.json`: 5 items, 0 failure/warning. 3 × macOS arm64 capacity notices (GitHub runner service, not-applicable), CodeRabbit skip comment and skip status (automatic reviews disabled by operator decision, not-applicable). No Codex bot review threads on #230.

## Gate

- Run in `.claude/worktrees/orchestrator-review` at cc19dd4c with evidence copies: `BASE=origin/main PR_FEEDBACK_EVIDENCE=… AGENT_REVIEWED=1 REVIEW_EVIDENCE=… make require-crit-review` → "PR feedback evidence accepted" and "Review requirement satisfied by AGENT_REVIEWED=1 with REVIEW_EVIDENCE". Copies removed afterwards; originals verified present.
- Review evidence: `-crit.json` (r_t59_01, resolved) and `-review-receipt.md`.

## CompactionDB

- Decision `e547c5a4-c593-47a6-bb13-3eff3f99ea7d` already in the main-checkout DB (the worker ran `memory add` unsandboxed from the main checkout, confirmed by `memory search T59`); cited here instead of a duplicate add.

## Follow-ups (not in this task)

- Learning candidates 1–3 (cold page cache on fresh images, mise shim SYSTEM fallback outside its config, `lexists` for symlink farms) are candidates for the next codification task; candidate 4 (formatter hook rewriting scoped edits) recurs from T57 and should be codified.
