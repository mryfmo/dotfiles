---
task: dotfiles-T129-anthropic-auth-route-check-followup-a04
head: 325f520bfc8b4dbb25e0744d27878cdf7eab2fd2
pr: 412
base: 3e41e36abc949acd7e6b4859c1a22df9e665c8d4
started: 2026-10-18T22:24:08Z
finished: 2026-10-18T22:31:46Z
findings: 5
engine: codex review --base main (profile review, read-only)
---

- [P1] Check subscripted assignments to the API-key variable — scripts/validate-agent-assets.py:1818-1818
- [P1] Preserve wrapper context through `builtin --` — scripts/validate-agent-assets.py:1612-1614
- [P2] Apply the R1 occurrence check before structured parsing — scripts/validate-agent-assets.py:1932-1934
- [P2] Preserve environment references in unquoted heredocs — scripts/validate-agent-assets.py:1759-1759
- [P3] Retain original line offsets when scanning Markdown chunks — scripts/validate-agent-assets.py:1928-1931

```text
Targeted read-only probes reproduced authentication-check bypasses, rejection of permitted heredoc references, and missed R1 occurrences. The existing corpus passes but does not cover these cases.

Full review comments:

- [P1] Check subscripted assignments to the API-key variable — scripts/validate-agent-assets.py:1818-1818
  In a tracked zsh file, `export ANTHROPIC_API_KEY=; ANTHROPIC_API_KEY[1]=literal-value` passes validation, although zsh updates the exported scalar to `literal-value`. This regex misses the subscript, and the later identifier check also excludes bracketed names. Recognize or reject subscripted authentication assignments; the scanner control marked `closed` remains bypassable ([AGENTS.md:78](AGENTS.md#L78)).

- [P1] Preserve wrapper context through `builtin --` — scripts/validate-agent-assets.py:1612-1614
  `NAME=ANTHROPIC_API_KEY; builtin -- export "$NAME"=literal-value` produces no findings, although Bash exports the literal value. Because `builtin` is only a prefix, `--` clears the command-start context and the following dynamic export escapes inspection. Handle `builtin` as a wrapper or refuse unresolved forms so the closed scanner control is enforced ([AGENTS.md:78](AGENTS.md#L78)).

- [P2] Preserve environment references in unquoted heredocs — scripts/validate-agent-assets.py:1759-1759
  An unquoted heredoc containing `ANTHROPIC_API_KEY=$DEPLOYED_KEY` is rejected as R2, even though the shell expands its value from the environment. Passing every heredoc body as `inactive=True` prevents reference recognition and marks the payload as literal. Distinguish expanding heredocs from quoted ones so this permitted environment-sourced configuration does not fail CI.

- [P2] Apply the R1 occurrence check before structured parsing — scripts/validate-agent-assets.py:1932-1934
  A tracked TOML or YAML file containing `# export ANTHROPIC_OAUTH_TOKEN=x` passes because parsing discards comments before inspection. R1 explicitly forbids any occurrence, including comments documenting the OAuth route, and text files still enforce that rule. Check the decoded source for R1 before parsing while retaining decoded-node inspection for escaped names.

- [P3] Retain original line offsets when scanning Markdown chunks — scripts/validate-agent-assets.py:1928-1931
  Each Markdown chunk restarts line counting, so a prohibited assignment on line 4 immediately after an opening fence is reported as `:2:`. Later examples likewise point to unrelated lines. Preserve each chunk's original LF offset and add it to reported locations without sharing quote state between examples.
Targeted read-only probes reproduced authentication-check bypasses, rejection of permitted heredoc references, and missed R1 occurrences. The existing corpus passes but does not cover these cases.

Full review comments:

- [P1] Check subscripted assignments to the API-key variable — scripts/validate-agent-assets.py:1818-1818
  In a tracked zsh file, `export ANTHROPIC_API_KEY=; ANTHROPIC_API_KEY[1]=literal-value` passes validation, although zsh updates the exported scalar to `literal-value`. This regex misses the subscript, and the later identifier check also excludes bracketed names. Recognize or reject subscripted authentication assignments; the scanner control marked `closed` remains bypassable ([AGENTS.md:78](AGENTS.md#L78)).

- [P1] Preserve wrapper context through `builtin --` — scripts/validate-agent-assets.py:1612-1614
  `NAME=ANTHROPIC_API_KEY; builtin -- export "$NAME"=literal-value` produces no findings, although Bash exports the literal value. Because `builtin` is only a prefix, `--` clears the command-start context and the following dynamic export escapes inspection. Handle `builtin` as a wrapper or refuse unresolved forms so the closed scanner control is enforced ([AGENTS.md:78](AGENTS.md#L78)).

- [P2] Preserve environment references in unquoted heredocs — scripts/validate-agent-assets.py:1759-1759
  An unquoted heredoc containing `ANTHROPIC_API_KEY=$DEPLOYED_KEY` is rejected as R2, even though the shell expands its value from the environment. Passing every heredoc body as `inactive=True` prevents reference recognition and marks the payload as literal. Distinguish expanding heredocs from quoted ones so this permitted environment-sourced configuration does not fail CI.

- [P2] Apply the R1 occurrence check before structured parsing — scripts/validate-agent-assets.py:1932-1934
  A tracked TOML or YAML file containing `# export ANTHROPIC_OAUTH_TOKEN=x` passes because parsing discards comments before inspection. R1 explicitly forbids any occurrence, including comments documenting the OAuth route, and text files still enforce that rule. Check the decoded source for R1 before parsing while retaining decoded-node inspection for escaped names.

- [P3] Retain original line offsets when scanning Markdown chunks — scripts/validate-agent-assets.py:1928-1931
  Each Markdown chunk restarts line counting, so a prohibited assignment on line 4 immediately after an opening fence is reported as `:2:`. Later examples likewise point to unrelated lines. Preserve each chunk's original LF offset and add it to reported locations without sharing quote state between examples.
```
