---
task: dotfiles-T129-anthropic-auth-route-check-a01
head: c1ba96fe43ffa5eda0eb95dda5a5a9febedaa40e
pr: 389
base: 99a4a80f5a5b32a70cf7eb4f4d0db5a02d113841
started: 2026-10-18T05:08:46Z
finished: 2026-10-18T05:12:22Z
findings: 3
engine: codex review --base main (profile review, read-only)
---

- [P1] Inspect multiline values before accepting an empty assignment — scripts/validate-agent-assets.py:1632-1632
- [P2] Require a complete identifier when matching the key name — scripts/validate-agent-assets.py:1614-1614
- [P2] Separate value terminators from the reference being checked — scripts/validate-agent-assets.py:1615-1616

```text
The new check misses multiline literal assignments and rejects valid references and unrelated identifiers. These cases were reproduced using in-memory fixtures; the full test suite was not run in the read-only sandbox.

Full review comments:

- [P1] Inspect multiline values before accepting an empty assignment — scripts/validate-agent-assets.py:1632-1632
  For valid JSON with `"ANTHROPIC_API_KEY":` on one line and `"literal-value"` on the next, the validator accepts the key line as an empty assignment and never associates the following value with it. The existing secret scanner also accepts this example, so ordinary formatting bypasses R2. Inspect complete assignments and add a multiline regression test to close the validator's threat-table control ([AGENTS.md:78](AGENTS.md#L78)).

- [P2] Separate value terminators from the reference being checked — scripts/validate-agent-assets.py:1615-1616
  A normal JSON field such as `"ANTHROPIC_API_KEY": "${DEPLOYED_KEY}",` fails R2 because the comma prevents the exemption from reaching the end-of-line anchor. Compact JSON ending in `}` and shell references followed by a command or semicolon fail similarly. These are environment references, not literal credentials, but they now fail the required agent-assets check. Recognize the surrounding syntax's value terminators before classifying the value.

- [P2] Require a complete identifier when matching the key name — scripts/validate-agent-assets.py:1614-1614
  The unanchored search has no left identifier boundary, so `HAS_ANTHROPIC_API_KEY=0` matches the suffix and fails R2. This assignment initializes a different variable and does not configure the Anthropic credential, yet adding it to an applied script makes validation fail. Require an identifier boundary before the key name and cover prefixed identifiers with a negative test.
The new check misses multiline literal assignments and rejects valid references and unrelated identifiers. These cases were reproduced using in-memory fixtures; the full test suite was not run in the read-only sandbox.

Full review comments:

- [P1] Inspect multiline values before accepting an empty assignment — scripts/validate-agent-assets.py:1632-1632
  For valid JSON with `"ANTHROPIC_API_KEY":` on one line and `"literal-value"` on the next, the validator accepts the key line as an empty assignment and never associates the following value with it. The existing secret scanner also accepts this example, so ordinary formatting bypasses R2. Inspect complete assignments and add a multiline regression test to close the validator's threat-table control ([AGENTS.md:78](AGENTS.md#L78)).

- [P2] Separate value terminators from the reference being checked — scripts/validate-agent-assets.py:1615-1616
  A normal JSON field such as `"ANTHROPIC_API_KEY": "${DEPLOYED_KEY}",` fails R2 because the comma prevents the exemption from reaching the end-of-line anchor. Compact JSON ending in `}` and shell references followed by a command or semicolon fail similarly. These are environment references, not literal credentials, but they now fail the required agent-assets check. Recognize the surrounding syntax's value terminators before classifying the value.

- [P2] Require a complete identifier when matching the key name — scripts/validate-agent-assets.py:1614-1614
  The unanchored search has no left identifier boundary, so `HAS_ANTHROPIC_API_KEY=0` matches the suffix and fails R2. This assignment initializes a different variable and does not configure the Anthropic credential, yet adding it to an applied script makes validation fail. Require an identifier boundary before the key name and cover prefixed identifiers with a negative test.
```
