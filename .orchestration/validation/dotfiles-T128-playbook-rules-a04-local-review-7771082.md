---
task: dotfiles-T128-playbook-rules-a04
head: 7771082f7db20a6ea1b53c5e95817aee6e23e177
pr: 328
base: a03c1daa394036d021c0b03b293a48603b923575
started: 2026-10-13T10:08:36Z
finished: 2026-10-13T10:09:33Z
findings: 1
engine: codex review --base main (profile review, read-only)
---

- [P2] Use an actually complete bus read — home/dot_agents/skills/agmsg-orchestration/SKILL.md:164-164

```text
The new recovery procedure claims to reconstruct state from complete bus history but caps that history at 1,000 records, which can omit active tasks in sufficiently long-lived teams.

Review comment:

- [P2] Use an actually complete bus read — home/dot_agents/skills/agmsg-orchestration/SKILL.md:164-164
  After compaction, a team with more than 1,000 messages will have older open TASK dispatches omitted by `history.sh <team> --limit 1000`, so the reconstructed open-task list can silently lose active work despite the preceding requirement for a complete read. Use an unbounded or paginated read, or explicitly continue until the team's full history has been consumed.
The new recovery procedure claims to reconstruct state from complete bus history but caps that history at 1,000 records, which can omit active tasks in sufficiently long-lived teams.

Review comment:

- [P2] Use an actually complete bus read — home/dot_agents/skills/agmsg-orchestration/SKILL.md:164-164
  After compaction, a team with more than 1,000 messages will have older open TASK dispatches omitted by `history.sh <team> --limit 1000`, so the reconstructed open-task list can silently lose active work despite the preceding requirement for a complete read. Use an unbounded or paginated read, or explicitly continue until the team's full history has been consumed.
```
