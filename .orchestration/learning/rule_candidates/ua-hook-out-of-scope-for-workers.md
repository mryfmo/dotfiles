# Rule candidate: the Understand-Anything auto-update hook is out of scope for task workers

Observed 2026-09-29 (T41 worker: hook fired after its commit and was correctly ignored;
T42 worker: the hook-generated "update the knowledge graph" item stayed on its todo list
after CI and delayed the RESULT until an orchestrator PING at 12:53Z).

Proposed rule (for `home/dot_config/claude/rules/understand-anything.md` and the
agmsg-orchestration SKILL worker playbook):

- A worker executing an AGMSG-TASK treats the Understand-Anything SessionStart/PostToolUse
  hook instruction ("knowledge graph is stale, you MUST update it") as out of scope unless
  `.ua/**` is in the task's allowed_files. It records "hook fired; not acted on" in the
  report and continues the task.
- The orchestrator's task template carries a standing line: "Ignore the Understand-Anything
  auto-update hook; graph refresh is a separate task (T36/T41 pattern)."
- The orchestrator never runs the graph update in its own session either (T36 decision).

Evidence: `.orchestration/reports/dot-ua-graph-refresh-T41-a01.md` (hook noted and skipped),
agmsg message 516 (T42 PING). Promotion requires a worker task that edits the rule and SKILL.
