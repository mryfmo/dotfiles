# Learning triage: dotfiles-T129-anthropic-auth-route-check-a01

These are candidates only; nothing is promoted.

1. [memory:decision] A negative lookahead placed after optional or repeated pieces (`(["']?)`, `\s*`) is tried at every position those pieces can backtrack to, so a value the lookahead should reject slips through at the empty alternative. Put the optional pieces inside the lookahead (`[:=](?!\s*["']?(?:\$|\{\{)|…)`), and test each exempt form with a leading space and with quotes.
2. [memory:decision] The repository masker redacts any quoted `api_key`-style assignment, so a task text that shows such an example arrives as `<redacted:secret-pattern>`. The worker can infer the case from SECRET_PATTERN, and a task author can avoid it by describing the example in words or splitting the name.
3. [memory:decision] An exemption for a `$` reference must name the reference forms (`$NAME`, `${NAME}`), not the `$` alone: Bash reads `$'…'` and `$"…"` as literal data, so a bare `\$` exemption let a committed key through (the Bot's P1 on PR #389).
