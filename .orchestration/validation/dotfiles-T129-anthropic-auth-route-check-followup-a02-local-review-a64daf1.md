---
task: dotfiles-T129-anthropic-auth-route-check-followup-a02
head: a64daf175c24a7f3e00d6f558cd255ea9ba5b356
pr: 412
base: 3e41e36abc949acd7e6b4859c1a22df9e665c8d4
started: 2026-10-18T20:09:41Z
finished: 2026-10-18T20:15:37Z
findings: 4
engine: codex review --base main (profile review, read-only)
---

- [P1] Reject ANSI-C-escaped authentication variable names — scripts/validate-agent-assets.py:1760-1762
- [P2] Isolate Markdown examples from prose quote state — scripts/validate-agent-assets.py:1882-1886
- [P2] Preserve non-shell separators when checking whole values — scripts/validate-agent-assets.py:1889-1893
- [P2] Redact assignment payloads from diagnostic key paths — scripts/validate-agent-assets.py:1895-1897

```text
Targeted reproductions show authentication-check bypasses and credential text appearing in diagnostics. The current-tree check passes, but the full filesystem-writing unit suite was not run in the read-only sandbox.

Full review comments:

- [P1] Reject ANSI-C-escaped authentication variable names — scripts/validate-agent-assets.py:1760-1762
  Bash accepts `export $'ANTHROPIC_API_\x4bEY'=literal-value` and exports `ANTHROPIC_API_KEY`, but this check accepts it. The escape leaves a non-identifier in `name`, so this guard skips refusal, while the literal-name regex cannot recognize the encoded spelling. The equivalent escaped OAuth name also passes. Decode these names or reject unsupported name expansions so the applied-input mitigation actually holds ([AGENTS.md:78](AGENTS.md#L78)).

- [P2] Redact assignment payloads from diagnostic key paths — scripts/validate-agent-assets.py:1895-1897
  For `{"ANTHROPIC_API_KEY=literal-value": "unused"}`, the diagnostic prints `literal-value` because the entire mapping key becomes `where`. TOML-escaped credential text can likewise pass the preceding raw secret scan, be decoded here, and then appear in CI output. Escaping the path prevents forged log lines but does not redact credentials. Sanitize assignment-bearing keys before printing them to preserve the claimed diagnostic mitigation ([AGENTS.md:78](AGENTS.md#L78)).

- [P2] Isolate Markdown examples from prose quote state — scripts/validate-agent-assets.py:1882-1886
  A managed Markdown file beginning with `Don't store credentials.` accepts a later fenced example containing `NAME=ANTHROPIC_API_KEY; export "$NAME"=literal-value`; replacing `Don't` with `Never` makes it fail. Removing fences leaves the prose apostrophe in the shell parser's quote state, hiding the assignment operator. Parse fenced examples independently rather than letting prose disable the applied-input check ([AGENTS.md:78](AGENTS.md#L78)).

- [P2] Preserve non-shell separators when checking whole values — scripts/validate-agent-assets.py:1889-1893
  An actual U+2028 or vertical-tab character between `$DEPLOYED_KEY` and `literal-value` makes an API-key assignment pass: `splitlines()` separates the suffix from the allowed reference. Bash instead retains both in the same assignment word, so a literal suffix bypasses the whole-value allowlist. Split shell text on LF only, both here and in `anthropic_text_findings`, to maintain the applied-input mitigation ([AGENTS.md:78](AGENTS.md#L78)).
Targeted reproductions show authentication-check bypasses and credential text appearing in diagnostics. The current-tree check passes, but the full filesystem-writing unit suite was not run in the read-only sandbox.

Full review comments:

- [P1] Reject ANSI-C-escaped authentication variable names — scripts/validate-agent-assets.py:1760-1762
  Bash accepts `export $'ANTHROPIC_API_\x4bEY'=literal-value` and exports `ANTHROPIC_API_KEY`, but this check accepts it. The escape leaves a non-identifier in `name`, so this guard skips refusal, while the literal-name regex cannot recognize the encoded spelling. The equivalent escaped OAuth name also passes. Decode these names or reject unsupported name expansions so the applied-input mitigation actually holds ([AGENTS.md:78](AGENTS.md#L78)).

- [P2] Redact assignment payloads from diagnostic key paths — scripts/validate-agent-assets.py:1895-1897
  For `{"ANTHROPIC_API_KEY=literal-value": "unused"}`, the diagnostic prints `literal-value` because the entire mapping key becomes `where`. TOML-escaped credential text can likewise pass the preceding raw secret scan, be decoded here, and then appear in CI output. Escaping the path prevents forged log lines but does not redact credentials. Sanitize assignment-bearing keys before printing them to preserve the claimed diagnostic mitigation ([AGENTS.md:78](AGENTS.md#L78)).

- [P2] Isolate Markdown examples from prose quote state — scripts/validate-agent-assets.py:1882-1886
  A managed Markdown file beginning with `Don't store credentials.` accepts a later fenced example containing `NAME=ANTHROPIC_API_KEY; export "$NAME"=literal-value`; replacing `Don't` with `Never` makes it fail. Removing fences leaves the prose apostrophe in the shell parser's quote state, hiding the assignment operator. Parse fenced examples independently rather than letting prose disable the applied-input check ([AGENTS.md:78](AGENTS.md#L78)).

- [P2] Preserve non-shell separators when checking whole values — scripts/validate-agent-assets.py:1889-1893
  An actual U+2028 or vertical-tab character between `$DEPLOYED_KEY` and `literal-value` makes an API-key assignment pass: `splitlines()` separates the suffix from the allowed reference. Bash instead retains both in the same assignment word, so a literal suffix bypasses the whole-value allowlist. Split shell text on LF only, both here and in `anthropic_text_findings`, to maintain the applied-input mitigation ([AGENTS.md:78](AGENTS.md#L78)).
```
