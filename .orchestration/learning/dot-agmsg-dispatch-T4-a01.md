# Learning triage
Validated: herdr pane list uses result.panes[].agent_status; inbox.sh needs team and identity; shared storage helper respects alternate stores. Turn-end delivery alone cannot wake idle workers (task-established cause). Skill change is task-authorized guidance, not a new skill promotion. Same-route max(id) correlation assumes one serialized sender. Durable memory recorded in report/validation.

## PR173 revision
Retry state must be refreshed: a busy worker can become idle while receipt is pending. One absolute deadline avoids multiplying the timeout. Validate destination before insertion and preserve sent-message identity on delivery failure so callers do not blindly resend. Preserve pane-less workers as an explicit alternative.
