---
task: dotfiles-T129-anthropic-auth-route-check-followup-a02
head: b1399953c5cb7a9a3e200480e144fe37cd1f2b39
pr: 412
base: de3b73cc4f8874a30be6adc47a0f07575869d0df
started: 2026-10-18T12:53:49Z
finished: 2026-10-18T12:59:25Z
findings: 2
engine: codex review --base main (profile review, read-only)
---

- [P1] Preserve single-quote semantics when handling backslashes — scripts/validate-agent-assets.py:1781-1785
- [P2] Recognize shell word boundaries after allowed references — scripts/validate-agent-assets.py:1612-1614

```text
The new validator accepts a reproducible literal-key assignment bypass and rejects legitimate environment-reference assignments followed by shell syntax. Both behaviors were reproduced without modifying repository files.

Full review comments:

- [P1] Preserve single-quote semantics when handling backslashes — scripts/validate-agent-assets.py:1781-1785
  With `NAME=ANTHROPIC_API_KEY`, the valid shell fragment `printf '%s' '\'; export "$NAME"=literal-value` passes the validator, while Bash assigns the literal key. Backslashes are literal inside single quotes, but this branch skips the closing quote, hiding the subsequent dynamic assignment from detection. Make escape handling quote-aware here and in `expansion_end`, and add regression coverage to close the trust-boundary control (`AGENTS.md:78`).

- [P2] Recognize shell word boundaries after allowed references — scripts/validate-agent-assets.py:1612-1614
  For valid shell commands such as `ANTHROPIC_API_KEY=$DEPLOYED_KEY client` or `export ANTHROPIC_<redacted:secret-pattern>; exec client`, the end-of-line requirement incorrectly reports a literal credential. Both assignments contain only an allowed environment reference; the following command or separator is not part of the value. Recognize assignment-word boundaries and add fixtures for these forms so legitimate environment-only authentication passes CI.
The new validator accepts a reproducible literal-key assignment bypass and rejects legitimate environment-reference assignments followed by shell syntax. Both behaviors were reproduced without modifying repository files.

Full review comments:

- [P1] Preserve single-quote semantics when handling backslashes — scripts/validate-agent-assets.py:1781-1785
  With `NAME=ANTHROPIC_API_KEY`, the valid shell fragment `printf '%s' '\'; export "$NAME"=literal-value` passes the validator, while Bash assigns the literal key. Backslashes are literal inside single quotes, but this branch skips the closing quote, hiding the subsequent dynamic assignment from detection. Make escape handling quote-aware here and in `expansion_end`, and add regression coverage to close the trust-boundary control (`AGENTS.md:78`).

- [P2] Recognize shell word boundaries after allowed references — scripts/validate-agent-assets.py:1612-1614
  For valid shell commands such as `ANTHROPIC_API_KEY=$DEPLOYED_KEY client` or `export ANTHROPIC_<redacted:secret-pattern>; exec client`, the end-of-line requirement incorrectly reports a literal credential. Both assignments contain only an allowed environment reference; the following command or separator is not part of the value. Recognize assignment-word boundaries and add fixtures for these forms so legitimate environment-only authentication passes CI.
```
