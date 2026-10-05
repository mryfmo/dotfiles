# T77b learning

Deprecated PreToolUse top-level decision/reason still has a legacy mapping; deprecation is sufficient for this task's migration branch. Use hookSpecificOutput.permissionDecision=deny with reason, and silence when no decision is needed; do not grant unnecessary allow.

Multiline/quoted hook reasons must be JSON encoded, not interpolated into JSON heredocs. The existing jq dependency can read raw text and serialize it. Compare decoded messages against the old raw reason text to ensure a contract migration does not rewrite guidance.

Quote shell glob patterns passed to unittest discovery; zsh rejects unmatched unquoted globs before rg runs. No rule promotion.
