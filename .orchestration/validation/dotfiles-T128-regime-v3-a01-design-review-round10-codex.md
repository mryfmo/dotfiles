---
reviewed_at: 2026-10-10T22:48:50Z
reviewer: codex-review-dot-h001 (headless)
profile: review
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@8f71c6a8b048e12d23133a58eda626b0674712686df662e24d98372e7e2e919b
round: 10
previous: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round9-codex.md
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

INV-12: rejected: contract-first tests that “fail when the rule is removed” cannot be merged before implementation for waves modifying existing scripts, because `skipUnless the script exists` will not skip them and required CI will correctly fail. Make contract PR tests dormant under ordinary contract-PR CI, then have the already-main-pinned `main-tests` job require every applicable contract to run—not skip—against implementation PRs; test removal of the rule must then fail.

premise 1: unverifiable — grep confirms the stated PyYAML call sites and absence of `jsonschema`, but dependency resolution could not be rerun because this read-only sandbox cannot initialize the `uv` cache; the pasted versions are plausible.

premise 2: holds — GitHub documents that `pull_request_target` uses the base default branch’s workflow and checkout by default and can produce required checks; the organization-only limitation applies to required-workflow rules, not ordinary required status checks.

premise 3: holds — local `codex-cli 0.161.0` exposes `--output-schema`; the prior exit-2 results for unsupported `--full-auto` and `-a` are plausible and consistent with the CLI surface.

premise 4: holds — the cited Claude headless behavior for bare credentials, hook loading, structured output, and budget caps is internally consistent with the current documented interface.

premise 5: holds — the pasted vendor recommendation to restart after more than two corrections is plausible and matches the cited best-practices guidance.

premise 6: unverifiable — local timestamps confirm the four audit artifacts at 11:48, 13:55, 15:52, and 17:23, but the claimed per-run durations and 11.1-hour interval cannot be reconstructed in this read-only seat.

premise 7: holds — the documented continuation behavior supports treating both Stop hooks as soft signals and the merge gate as the mandatory backstop.

premise 8: holds — the named transcript is readable, contains the stated usage fields, and has 5,168 usage-bearing records.

premise 9: unverifiable — the pasted 20/256 counts are plausible, but `history.sh` requires temporary writes unavailable in this sandbox.

premise 10: holds — GitHub documents that `workflow_dispatch` runs only when its workflow file exists on the default branch.

premise 11: holds — Claude’s documented `--add-dir` exception makes the `.claude/skills/` refusal necessary; v10 now places the broader `.claude/**` exit-2 refusal directly in INV-5.

premise 12: holds — GitHub currently documents evaluate mode, enforcement on November 2, 2026, and explicit allowlisting through an applicable Actions event policy. [GitHub security documentation](https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target)

## Findings

[P1] .orchestration/tasks/dotfiles-T128-regime-v3-a01.md:57 Contract-first tests are only skipped when the target script is absent, but V2b, V3a, V3b, V3c, V3d, V4, and V5b modify scripts already present by their wave; tests that genuinely fail before those rules exist therefore cannot pass required CI and merge ahead of implementation.

[P2] .orchestration/tasks/dotfiles-T128-regime-v3-a01.md:173 V0 establishes the job and ordering, but does not specify a two-mode contract protocol that permits dormant contract tests to land while requiring them to execute, without skips, on the subsequent implementation PR.

## Residual

Operator authentication remains impossible under the stated one-user and one-account constraint. Native permission prompts and externally stored waiver records provide friction and visibility, not authenticated attribution.

The `pull_request_target` architecture remains dependent on the operator configuring an explicit applicable Actions event policy before November 2, 2026. The design now states that dependency accurately; failure to configure it removes the main-pinned CI gate.

Commands requiring writable caches or agmsg-history temporary state were not run. No files were modified, and no implementation tests were executed.

Design verdict: reject