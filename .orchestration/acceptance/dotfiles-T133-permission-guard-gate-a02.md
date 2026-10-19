---
{
  "audit_findings": [],
  "dispatch": [
    "AGMSG-TASK v1 task_id=dotfiles-T133-permission-guard-gate-a02 round=1 reset_of=dotfiles-T133-permission-guard-gate-a01 repo=~/Workspace/dotfiles/.claude/worktrees/worker-e task_file=.orchestration/tasks/dotfiles-T133-permission-guard-gate-a02.md task_sha256=8623badb987ae8c4c5f66a3ac3ab1bfefb1e347e878c31ae6317eba726f6b1d4 deadline=2026-10-19T03:00Z done_signal=AGMSG-RESULT note=a010:INV-6-reset-of-a01(three-question-PONGs);redesigned-by-the-review-profile"
  ],
  "format": 1,
  "head": null,
  "ledger": [],
  "pr": null,
  "searches": [],
  "task": "dotfiles-T133-permission-guard-gate-a02"
}
---

# Acceptance record: dotfiles-T133-permission-guard-gate-a02

Plan 024 P1-14 and D3 (d), the INV-6 reset of `dotfiles-T133-permission-guard-gate-a01` (S2: three question PONGs; counters and the redesign in the a01 record). Redesigned by a review-profile context (`.agents/worklog/orchestrator-glue/redesign/p114-a02.md`); seat a010 (worker-e, Codex) continues on its existing branch, stacked on PR #412's head d3480fc0 until #412 merges. Deadline 2026-10-19T03:00Z.

- 2026-10-18T10:15:24Z: task text installed, `task-consistency-check.py … : OK`, home-path scan 0 matches, dispatched to a010 (the line above; the full note is in the bus history).
- Checks before the send:

```
dotfiles-T133-permission-guard-gate-a02.md: OK
0 (/Users/ or login matches)
```

## S1: argv-text-mismatch (2026-10-18T10:30:50Z), class table and re-plan

a010 stopped itself (Worker Playbook step 15) after its independent review of the rebuilt hook found three findings of one class; it committed, pushed and opened nothing (source head d3480fc0 unchanged; the a02 artifacts are untracked under `.claude/worktrees/worker-e/.orchestration/dotfiles-T133-permission-guard-gate-a02/`: report.md, validation.md, sandbox.md, learning.md, autoskill.md, measure.md, independent-review.md, finding-classes.json, closure_probes.py, the worker crit JSON; 279 tests green in 46.7 s; 54 semantic probes with 0 mismatches, which do not close the new findings).

| # | where | finding (class argv-text-mismatch) |
| --- | --- | --- |
| 1 | T131 review of PR #400 at 0b874adb (2026-10-17) | the hook decided from command text, not argv (the class's defining findings) |
| 2 | live, 2026-10-18 18:29 JST | the hand-applied #400 hook prompted a009 and a008 on commands whose heredoc bodies contained the words gh pr merge / gh pr create while no gh ran |
| 3 | a010's independent review of the a02 rebuild (10:30:50Z) | P1 line 175: an `env -S` split string and a pipeline into bash not recognised; P1 line 68: a heredoc delimiter with backslash-newline marked quoted; P2 line 180: a bracket test prompts without gh |

Three rows (the third review alone holds three): S1. The artifact goes to redesign; no fourth round. One more P2 of that review (line 59: the ruleset comparison drops duplicate rule types) is carried into the redesign as an item.

re-plan: argv-text-mismatch -> specification: the a02 item 7 (written into the redesign prompt by the orchestrator) promised no decision whenever gh stands in no command position, which is unsound under indirect execution (bash -c, env -S, eval, xargs, pipes and heredocs into shells cannot be told apart from prose by any static parse), so the promise is withdrawn and the hook has three outcomes: allow only one metacharacter-free simple command whose shlex argv is exactly the gated grammar and whose anchor and evidence conditions hold; ask whenever the quote-and-backslash-stripped text contains the gated words (gh followed later by merge, create or update-branch, or the bigram pr merge, pr create or pr update-branch) outside that grammar; otherwise no decision; design: no tokenizer on the ask path, shlex only on the allow path, one regex over the normalised text for the ask path, the hook never executes command text, and prose that carries those words is written with the file-edit tool (a SKILL sentence, the orchestrator's); implementation: about forty lines replace the quote-aware tokenizer, and the remaining residual (a command name assembled from variables) is stated in the threat row with permgate and the auto-mode classifier as the next layer; verification: a table-driven test over the T131 dry inputs, the two live heredoc shapes (expected ask, the accepted cost), a010's three forms (expected ask) and the honest commands (expected allow), plus one property test asserting that no input containing a shell metacharacter is ever allowed.

- root cause and mechanism: the unsound clause came from the orchestrator's prompt, not from the worker or the review context; M-20261018-13 and C-73 (a redesign-brief standing item: a hook or guard specification enumerates its indirect-execution residuals and never derives silence from command positions).
- 10:5xZ: `AGMSG-ACCEPTANCE … status=withdrawn` sent to a010 with the re-plan summary; the a03 redesign (review profile, prompt `.agents/worklog/orchestrator-glue/p114-a03-redesign-prompt.md`) follows; a010 keeps its branch and artifacts.
- 2026-10-18T12:44:56Z: a03 (task sha256 f87c2054…) dispatched to a010; record `.orchestration/acceptance/dotfiles-T133-permission-guard-gate-a03.md`.
