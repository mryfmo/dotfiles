---
reviewed_at: 2026-10-11T02:41:16Z
reviewer: codex-review-dot-h001 (headless)
profile: review
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@58b95ba4e39ad2e422fa2cf80e218c76880f4847dd0510ce5e7aef5b2e8f6355
round: 14
previous: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round13-codex.md
---

INV-1: accepted

INV-2: accepted

INV-3: accepted

INV-4: accepted

INV-5: accepted

INV-6: accepted

INV-7: accepted

INV-8: accepted

INV-9: accepted

INV-10: accepted

INV-11: accepted

INV-12: accepted

premise 1: unverifiable — Local references remain consistent, but the read-only sandbox prevents reproducing the `uv` resolution result; the recorded versions remain plausible.

premise 2: holds — The required-check design keeps workflows unconditional and makes the changes job report a terminal result; it does not rely on workflow-level path filtering that could leave checks pending.

premise 3: holds — The recorded Codex CLI behavior and strict schema path remain consistent with the previously accepted evidence.

premise 4: holds — The Claude headless-mode, hook, structured-output, and budget-cap claims remain consistent with the previously accepted evidence.

premise 5: holds — The two-correction reset guidance remains correctly represented.

premise 6: unverifiable — The repository timestamps remain consistent with the claim, but agmsg history cannot be independently reproduced in this read-only environment.

premise 7: holds — Both Stop mechanisms remain correctly treated as soft signals, with the merge gate as the mandatory enforcement point.

premise 8: holds — The named transcript evidence supports the stated per-message usage fields and record count.

premise 9: unverifiable — The history limits cannot be independently reproduced because the storage helper requires writable temporary state; the recorded counts remain plausible.

premise 10: holds — The default-branch prerequisite for `workflow_dispatch` is correctly reflected in the rollout sequence.

premise 11: holds — The Claude fallback correctly accounts for skills loaded from an `--add-dir` tree by refusing affected `.claude/` changes.

premise 12: holds — The native `permissions.ask` prompt is accurately treated as friction rather than authenticated operator identity.

premise 13: holds — The dated `pull_request_target` policy transition is explicitly carried as a prerequisite and residual.

## Findings

None.

The per-run nonce is the strongest completion authentication available while retaining an in-process oracle. Supplying it through an inherited pipe and closing that channel before loading PR-controlled tests removes environment, argument, and open-descriptor disclosure paths; returning the nonce with the observed counts binds the completion report to that invocation. Perfect secrecy is impossible once the trusted runner and adversarial imported code share a Python process, and INV-12 accurately identifies frame introspection as the remaining forgery path.

That residual is placed at an existing mechanical review point: every design-tier change receives the trusted-root audit, which reads the diff and treats weakened conformance as a finding. Requiring the same residual in each design-tier acceptance record also prevents it from disappearing operationally.

The `.orchestration`-only optimization is safe for required checks as designed. The workflows remain triggered for every PR; the changes job reaches a successful terminal state and suppresses expensive bootstrap or test work inside the workflow. It does not use workflow-level path filters, which are the configuration that can leave an expected required check pending. A201’s verification requires `gh pr checks` to show every required context on an actual boundary PR before completion.

## Residual

Adversarial PR code can inspect Python frames and recover the in-memory nonce. Eliminating that path requires process isolation and would no longer be an in-process oracle; the trusted-root audit is therefore a necessary model-backed control, not cryptographic prevention.

The CI-skip guarantee still depends on A201 implementing job-internal success reporting without renaming or omitting required check contexts. Its live `gh pr checks` verification is required before acceptance.

Operator authentication and the forthcoming `pull_request_target` policy change remain the previously accepted residuals. I did not execute implementation or CI and modified no files.

Design verdict: accept