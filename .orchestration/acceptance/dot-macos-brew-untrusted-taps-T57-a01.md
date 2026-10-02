# Acceptance: dot-macos-brew-untrusted-taps-T57-a01

status: accepted
pr: #228 (squash-merged to main as 3c4c2cec; branch fix/macos-brew-untrusted-taps left in place because the worker worktree holds it)
reviewed_head: f568eab6a1032a9d134d89cb43f3b0200f2016fc (revise round 1; commits f314ab2a, 50c833b3, f568eab6)
worker: claude-standard-dot-a005 (worker-c)

## Review

- Root cause: the macos-14 runner image ships aws/tap, azure/bicep and hashicorp/tap tapped but untrusted; Homebrew 7 warns on every brew install. The warning came from Snippet install / public-bootstrap (macos-14, client) and had been dispositioned not-applicable on every PR.
- Round 0 (f314ab2a): whole-tap trust derived from brew untrust --tap. Codex audit Verdict: incorrect, one P2: the rationale "item-level trust is not derivable" was false (brew list --formula --full-name reads keg receipts, cmd/list.rb 104-120 at 7.0.7). Orchestrator reproduced from source; revise sent (message 698).
- Round 1 (f568eab6): item-level trust for installed formulae/casks of the listed taps, whole-tap trust only for a listed tap with nothing installed. Decided by two CI measurements the orchestrator re-derived from the job logs: 50c833b3 (item-level only, job 110914945531) cleared azure/bicep and hashicorp/tap but still warned for aws/tap; f568eab6 (job 110919109271) printed Trusted formula x2 and Trusted tap: aws/tap with no warning. Comment and PR rationale corrected; no "not derivable" text remains. bats case updated to the exact call sequence; CI green (13 checks, nix skipped). Codex audit on f568eab6: Verdict: correct, no findings.
- Codex code review (Bot) posted one P2 on the intermediate commit 50c833b3 (aws/tap omitted): fixed:f568eab6; its broader claim is contradicted by measurement 1. The orchestrator replied on the thread and resolved it on GitHub (first use of thread resolution as part of acceptance).

## Audit dispositions

- audit.md (f314ab2a) P2 false rationale: fixed:f568eab6 (comment, report and PR body corrected; design re-decided by measurement)
- audit-rev1.md (f568eab6): no findings

## PR feedback dispositions (head f568eab6, 18 items)

- 12 annotation:notice (runner migration/capacity): not-applicable, root-cause task T58 follows
- 1 Codex review container + 1 Codex inline P2: not-applicable (container) / fixed:f568eab6 (inline)
- 1 orchestrator reply review + 1 reply comment: not-applicable (disposition reply, thread resolved)
- 1 CodeRabbit comment + 1 status: not-applicable (review disabled by operator decision)
- 0 warning items; the untrusted-tap warning is gone on the final head (acceptance criterion met)

## Gate

BASE=origin/main PR_FEEDBACK_EVIDENCE=... AGENT_REVIEWED=1 REVIEW_EVIDENCE=... make require-crit-review -> exit 0 at f568eab6 in .claude/worktrees/orchestrator-review (two earlier runs failed on evidence shape: the gate re-collects feedback and rejected a fixed: disposition carrying trailing prose; dispositions must be exactly fixed:<sha> or not-applicable:<reason>).

## Recorded option (not required)

A listed tap with nothing installed could be untapped instead of whole-tap trusted (Homebrew lists untap first). On an ephemeral CI runner the difference is negligible; the measured implementation stands.

## Learning candidates (worker, not promoted)

Homebrew 7 hides untrusted-tap formulae from Formula.installed but not from brew list --full-name; verify CLI behaviour against the released tag; README PostToolUse formatter reflows unrelated lines; bare shfmt -d uses tabs (use the repository form); zero warnings does not prove a function ran (require the log excerpt).

cost: n/a (worker: no subagents reported; orchestrator session totals not exposed)
