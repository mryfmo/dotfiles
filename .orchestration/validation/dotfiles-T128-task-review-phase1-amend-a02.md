---
reviewed_at: 2026-10-12T13:27:50Z
reviewer: claude-review-dot-a001
profile: review
session: 2089b04f-f9c7-498b-86c5-76f2140048d5
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@9c9d42cb00c52457e8e7df37bf5276d42978d3466768286cd30b326fb8fdc0e2
task: dotfiles-T128-task-review-phase1-amend-a02
round: 2
previous_file: dotfiles-T128-playbook-rules-a02@6e8a06cfdd8a6e26 (round 1, confirmed)
files:
  - dotfiles-T128-playbook-rules-a02@07b78f643bc5a488614bca59d195d45da93defb7d7c0acf5fc8a4820e00f4f33
verdicts:
  dotfiles-T128-playbook-rules-a02: confirm
---

# Amendment confirmation, round 2: dotfiles-T128-playbook-rules-a02 amendment 1 (the trigger sentence on INV-10's clock, no override)

The Codex half asked for INV-10's own clock and no override; the orchestrator applied it once. Item 1's last sentence now reads "Thirty minutes after a TASK, an amendment or a revise enters the bus history with no bus event from its seat since (the clock and the figure of INV-10's first-push rule) trigger a bus read, then a PING; a longer silent wait is never the answer." The start is the message's history timestamp, which INV-10 uses for the first push and which history.sh prints, and the end is the seat's next bus event, so the trigger is computable from the bus alone. The rule sentence carries no override; the only remaining expected_minutes is the introduction's description of the withdrawn first draft. The introduction's amendment sentence matches the new wording. Against main (7cbe5405) the diff is the heading note, the introduction paragraph and item 1's last sentence (three lines changed); the front matter, items 2 to 8, premises, Validation and Completion are unchanged. The checker prints OK (C1 to C7). The round-2 TASK line carried a mistyped amended_task_sha256; the orchestrator's PING of 13:27:03Z gave the true whole-file sha256, which this seat computed independently and which is the hash in this header. Round 1's note for T712 (A7's parked 45-minute no-push rule beside this 30-minute rule) stands.

No findings.

Amendment verdict: dotfiles-T128-playbook-rules-a02: confirm
