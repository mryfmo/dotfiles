---
reviewed_at: 2026-10-10T22:41:28Z
reviewer: claude-review-dot-a001
profile: review
session: 2089b04f-f9c7-498b-86c5-76f2140048d5
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@84cec99c360383912134e6d2f5ae0963078c40c3ee0033b2e1017f030d8448d3
design_hash_kind: whole-file sha256 (the canonical hash tool is V1's deliverable)
task: dotfiles-T128-design-review-a01
round: 8
previous: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round7.md
---

# Design review: dotfiles-T128-regime-v3-a01, round 8 (eight invariants after the Codex review's reject)

Read: v8's INV-1, 3, 4, 5, 6, 9, 10, 12, section 9's one-account residual, the Codex round-7 receipt (codex-review-dot-h001, verdict reject, nine findings), the manifest's sandbox write roots (agent-config.yaml:112-116, 229-231), the managed settings' empty ask list, and permgate-policy.yaml (no waiver entry).

## The eight changed invariants

INV-1: rejected: the new mechanism has no owner. scripts/regime-waive.sh and the managed permissions.ask rule appear in INV-1 and INV-6 but in no enforcement row (line 153 is unchanged), no wave (lines 169-181) and no implementing_tasks entry; the rule lives in the manifest's claude.permissions block, a Claude-boundary source that routes to a Codex seat under P10, and the script is a gate-adjacent design-tier file. Add a wave (or fold into V3a with its routing stated) and an implementing_tasks entry. The mechanism itself is right as far as it goes; see the anchor answer below for what makes it stronger.

INV-3: accepted. The repro form is gone; a test selector plus previous_head is the one admissible fact, which answers the Codex P1 at line 47.

INV-4: accepted. Premises as evidence re-run by the reviewers and the auditor, counting as the mechanical part, is the honest statement; the Codex P1 at line 48 asked for trusted execution before dispatch, and the design now says who re-runs them. Note: name the sample size in V4's runner prompt and the audit prompt (this review has re-run at least two per file).

INV-5: rejected: one contradiction inside the sentence. "at most once per RESULT head" and "a pre-audit input edited after the audit makes the audit stale and a new audit is required" conflict for the same head. Right: "at most one valid audit per RESULT head; a stale audit is replaced by the new one, and INV-6's audit-heads count uses the latest valid audit per head". The input manifest with the pre-audit boundary in the acceptance record is the right answer to the Codex P1 at line 49, and the gate recomputing it at gate time is mechanical.

INV-6: accepted, with INV-1's anchor note applying to its release path.

INV-9: accepted. Cost as a warning metric with the raw sources' paths and sha256 recorded is honest; it answers the Codex P2 at line 53 without claiming a trusted runtime digest that does not exist.

INV-10: rejected: the committer date of the PR's first commit is set by the committer's clock and GIT_COMMITTER_DATE, so it is worker-controlled; the Codex P2 asked for an immutable GitHub timestamp. Right: the draft PR's createdAt (gh pr view --json createdAt), which GitHub assigns, since the invariant already says the first push is a draft PR. The dispatchable-task definition is now computable and accepted.

INV-12: accepted. The honest statement that the PR's own workflow runs the tests and that the design-tier audit from the trusted root is the independent oracle for a gate-script PR is the right trade: running PR code under pull_request_target is what section 9 forbids.

## The anchor question

The ask rule is the strongest friction the agent runtimes offer: permissions.ask prompts even in auto mode (auto-mode-config page), permgate has no entry for the command so the PermissionRequest hook fails closed to the native prompt, and a Codex orchestrator's on-request policy prompts the same human. A stronger anchor does exist on this machine without a second account, and it is cheap: make the waiver record live where the seats' sandboxes cannot write. The Claude allowWrite list and Codex writable_roots cover the checkout, .git, the agmsg db/teams/run/ext-tools roots and the uv cache (agent-config.yaml:112-116, 229-231); a record under $XDG_STATE_HOME/regime/waivers/ is outside them, so only an unsandboxed command writes it, and the only pre-approved unsandboxed route to it is regime-waive.sh behind the ask prompt. Any other route is dangerouslyDisableSandbox through the classifier or the prompt, a model or human decision rather than a deterministic one. The gate and check-regime-boundary.sh then read waivers only from that directory and refuse one anywhere else. This turns "a human answered a prompt" into "a path only the prompted command can reach", which is what the Codex P1s at lines 45 and 50 were asking for in substance. It still cannot tell the operator's keyboard from the orchestrator's; section 9 says so and should keep saying so.

## Codex P2 at line 88

Refuted correctly: the headless page says bare mode skips skill discovery and then states the exception, "bare mode loads skills from its .claude/skills/ folder" for a directory named with --add-dir; the fact sheet's one-line summary omitted the exception. The design's premise and V2's refusal stand.

## Unchanged

INV-2, INV-7, INV-8, INV-11: accepted. Section 9's residual is honest and gains the directory sentence above.

Design verdict: revise
