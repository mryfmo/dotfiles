#!/usr/bin/env python3
"""Re-inject the orchestrator checklist on SessionStart/UserPromptSubmit.

Prose alone does not survive long sessions and context compaction, so the
checklist the agmsg-orchestration rules already state gets echoed back into
context via `hookSpecificOutput.additionalContext`. Orchestrator role only
(HERDR_AGENTS_ROLE=orchestrator); workers get nothing from this hook.
See: https://docs.claude.com/en/docs/claude-code/hooks
"""

from __future__ import annotations

import json
import os
import sys

CHECKLIST = """Orchestrator checklist:
- Liveness: AGMSG-PING/PONG only, never infer state from herdr agent/pane commands.
- Flow: task file -> agmsg-dispatch -> AGMSG-RESULT -> adversarial review in orchestrator-review.
- Then: GitHub feedback sweep -> Crit -> receipt -> make require-crit-review guard.
- Merge without --delete-branch while a worker worktree still holds the branch.
- Records: pending acceptances, CompactionDB decision, .orchestration sync commit.
- One consolidated revise per review round. Never idle-wait."""


def main() -> int:
    raw = sys.stdin.read()
    if os.environ.get("HERDR_AGENTS_ROLE") != "orchestrator":
        return 0
    try:
        payload = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        payload = {}
    event_name = payload.get("hook_event_name", "SessionStart")
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": event_name,
                    "additionalContext": CHECKLIST,
                }
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
