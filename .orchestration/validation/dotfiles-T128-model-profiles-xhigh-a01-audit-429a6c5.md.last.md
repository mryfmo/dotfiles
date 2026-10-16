[P2] high conformance home/dot_agents/agent-config.yaml:44 — `deep.claude` becomes `xhigh`, but `review.claude` remains `high` at line 41. This contradicts the referenced design’s INV-7 requirement that Claude review and deep use identical model and effort; generated review launch arguments retain the mismatch.

[P2] high orchestration .orchestration/validation/dotfiles-T128-model-profiles-xhigh-a01-pr-feedback.json:116 — The README regression is marked `not-applicable` solely because a follow-up task owns it. That defers an acknowledged defect introduced by this head; `home/dot_config/claude/rules/pr-integration.md:4` explicitly prohibits deferral as a disposition. Fix the documentation or substantiate why the finding does not apply.

The task declares no numbered invariants. For its referenced design:
INV-7: violated home/dot_agents/agent-config.yaml:44

Orchestration findings: 1

📝 まとめ: Audited [PR #370](https://github.com/mryfmo/dotfiles/pull/370) at `429a6c55`; two findings remain. The premise holds, all six generated outputs match, and final-head CI passed.

Not checked: live model launches or local Bats; no files were modified.
Verdict: incorrect