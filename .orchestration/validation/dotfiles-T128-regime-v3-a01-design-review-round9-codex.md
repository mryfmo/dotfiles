---
reviewed_at: 2026-10-10T22:43:49Z
reviewer: codex-review-dot-h001 (headless)
profile: review
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@015e32530307a3fe65b8f9a328a85ce99a8beda72602f790c6822d17ad34cb30
round: 9
previous: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round8-codex.md
---

INV-1: accepted

INV-2: accepted

INV-3: accepted

INV-4: accepted

INV-5: rejected: the Claude fallback still passes the untrusted worktree through `--add-dir` without refusing heads that modify `.claude/skills/**`; add that refusal to INV-5, its enforcement map, runner, and tests before invoking Claude. The official documentation confirms that bare mode loads skills from an added directory. [Claude Code headless documentation](https://code.claude.com/docs/en/headless)

INV-6: accepted

INV-7: accepted

INV-8: accepted

INV-9: accepted

INV-10: accepted

INV-11: accepted

INV-12: rejected: the main-pinned `main-tests` harness lands in V5c, after V1–V5b have implemented almost every rule it is intended to protect. Round 8 required the trusted invariant contract or mutation cases to be on `main` before implementation. Land the `main-tests` workflow and per-wave main-pinned contract tests before the corresponding implementation PRs, then run those tests against each PR’s scripts in PR context.

premise 1: unverifiable — the grep rerun confirmed PyYAML use at Makefile lines 189/203 and `agent-assets.yml` lines 35/39, but `uv` could not initialize its cache in the read-only sandbox, so dependency resolution and the stated versions could not be reproduced.

premise 2: holds — GitHub documents ruleset workflows as organization/enterprise features, lists `pull_request_target` among events eligible for required checks, and states that its workflow and default checkout come from the base default branch. [Ruleset documentation](https://docs.github.com/en/enterprise-cloud%40latest/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets), [required-check troubleshooting](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks), [`pull_request_target` security](https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target)

premise 3: holds — local `codex-cli 0.161.0` exposes `--output-schema`; `codex exec --full-auto` and `codex exec -a never` both exited 2 as unexpected arguments. Official OpenAI documentation shows Codex using `--output-schema`, while Structured Outputs uses strict JSON-schema formatting. [Codex repair-loop example](https://developers.openai.com/cookbook/examples/codex/build_iterative_repair_loops_with_codex), [Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs)

premise 4: holds — current Claude documentation confirms bare mode’s credential behavior, ordinary `-p` project-hook loading, `structured_output`, and `--max-budget-usd`; it also warns that spending can exceed the cap slightly. [Claude Code headless documentation](https://code.claude.com/docs/en/headless)

premise 5: holds — current vendor guidance says to start fresh after correcting Claude more than twice on the same issue. [Claude Code best practices](https://code.claude.com/docs/en/best-practices)

premise 6: unverifiable — `stat` confirmed four audit artifacts at 11:48, 13:55, 15:52, and 17:23 local, but the stated per-run durations and 11.1-hour history interval could not be independently reconstructed because `history.sh` requires forbidden temporary writes in this read-only sandbox.

premise 7: holds — Claude documents the eight-consecutive-continuation cap with reset after tool use; OpenAI documents that a Codex Stop `block` decision creates a continuation prompt rather than rejecting the completed turn. [Claude hooks](https://code.claude.com/docs/en/hooks), [OpenAI hooks](https://developers.openai.com/de-DE/docs/hooks)

premise 8: holds — the named transcript was readable; its last usage object contained input, output, cache-creation, and cache-read token fields, and the rerun counted 5,168 usage entries.

premise 9: unverifiable — both history invocations reached the storage facade but failed because its shell implementation attempted temporary writes forbidden by the review sandbox; the claimed 20/256 counts could not be reproduced.

premise 10: holds — GitHub states that `workflow_dispatch` triggers only when the workflow file exists on the default branch. [GitHub Actions events](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#workflow_dispatch)

premise 11: holds — Claude documents that bare mode loads `.claude/skills/` from directories supplied through `--add-dir`; this validates the premise and simultaneously exposes INV-5’s missing enforcement. [Claude Code headless documentation](https://code.claude.com/docs/en/headless)

premise 12: holds — Claude documents that `permissions.ask` rules are evaluated before the classifier and always force a prompt in auto mode; the repository rule says only the human operator may answer permission prompts. [Claude auto-mode configuration](https://code.claude.com/docs/en/auto-mode-config)

## Findings

[P1] .orchestration/tasks/dotfiles-T128-regime-v3-a01.md:50 INV-5 still lacks the required `.claude/skills/**` head-change refusal, leaving the Claude fallback able to load instructions controlled by the audited PR.

[P1] .orchestration/tasks/dotfiles-T128-regime-v3-a01.md:182 V5c installs the main-pinned test oracle only after the implementation waves it must independently constrain; move the harness and applicable contract tests ahead of each protected implementation wave.

[P2] .orchestration/tasks/dotfiles-T128-regime-v3-a01.md:211 Section 10 claims that v9 placed the `.claude/**` refusal inside INV-5, but no such refusal appears in the invariant, enforcement map, or V2 runner scope.

[P2] .orchestration/tasks/dotfiles-T128-regime-v3-a01.md:211 Section 10 says round 8’s independent-oracle finding was answered by V5c, but the wave order leaves V1–V5b without that main-pinned protection.

## Residual

Operator authentication remains impossible under the stated one-user and one-GitHub-account constraint. The native permission prompt and visible waiver records are accepted as friction and auditability, not authenticated attribution.

GitHub now documents a public-repository policy that will block `pull_request_target` by default beginning November 2, 2026 unless an applicable policy explicitly allows it. The implementation and operating documentation must account for that before enforcement. [GitHub security documentation](https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target)

The local `uv` and agmsg-history premise commands could not complete because this independent seat is read-only. No files were modified, and implementation tests were not run.

📝 まとめ: v9 resolves four round-8 rejections, but INV-5’s missing skills refusal and INV-12’s late oracle deployment remain release-blocking.

Design verdict: reject