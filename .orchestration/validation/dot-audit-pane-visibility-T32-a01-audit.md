# Codex audit — dot-audit-pane-visibility-T32-a01 (PRE-MERGE, revision 1, commit 8af8d11)

Invocation: `codex --profile audit review --commit 8af8d11` (orchestrator, headless, 2026-09-28; the visible `herdr-agents --audit` lane is what this PR adds and cannot audit itself before merge).

Session header:

```
OpenAI Codex v0.157.1
--------
workdir: /home/moriya/Workspace/dotfiles
model: gpt-6-astra
provider: openai
approval: never
sandbox: read-only
reasoning effort: high
reasoning summaries: concise
session id: 01a0e540-c8ad-7ff2-b0e5-e088197a253d
--------
```

Findings (verbatim final message):

```
The audit launcher mishandles reused panes with changed working directories and repository paths containing apostrophes. Both defects were confirmed with isolated, read-only command checks.

Full review comments:

- [P2] Reset the audit pane's working directory on every run — /home/moriya/Workspace/dotfiles/home/dot_local/bin/common/executable_herdr-agents:920-920
  When an existing audit pane has changed directories, this command runs Codex in that directory rather than the requested DIR. `--cwd` only applies when creating the tab; the caller's earlier `cd` cannot affect the persistent pane. Consequently, subsequent audits can fail to resolve the commit or run against another checkout while writing evidence under the requested repository. Explicitly set the review command's working directory on every invocation.

- [P2] Quote the complete command instead of nesting escaped paths — /home/moriya/Workspace/dotfiles/home/dot_local/bin/common/executable_herdr-agents:920-920
  If DIR contains an apostrophe, such as `/tmp/it's-a-project`, the default evidence path produces an invalid command. The earlier validation checks only `--out`, before prepending `workdir`, and `printf '%q'` emits `\'`, which cannot escape an apostrophe inside the surrounding single-quoted `bash -c` argument. This reproduces an unmatched-quote syntax error, preventing the audit and exit marker from running. Pass paths as positional arguments or shell-quote the complete Bash command.
```

Overall: 2 findings, both P2 (confirmed by the auditor with read-only reproductions); no explicit `correct`/`incorrect` verdict line was emitted. Orchestrator disposition: both ACCEPTED as real defects -> revision 2 (see acceptance record).

---

# Codex audit — revision 2 (PRE-MERGE, commit 9691870)

Invocation: `codex --profile audit review --commit 9691870` (orchestrator, headless, 2026-09-28).

Session header:

```
OpenAI Codex v0.157.1
--------
workdir: /home/moriya/Workspace/dotfiles
model: gpt-6-astra
provider: openai
approval: never
sandbox: read-only
reasoning effort: high
reasoning summaries: concise
session id: 01a0e55a-2a22-7b51-a0c9-6703fc829e6a
--------
```

Findings (verbatim final message):

```
No actionable regressions were found in commit 9691870. Syntax checks and isolated execution confirmed directory switching and correct exit markers for audit success, audit failure, and failed directory changes. Full unit tests and live Herdr integration were not run.
```

Overall: no findings; the auditor confirmed by isolated execution that the cd/pipefail/marker chain reports success, audit failure, and a failed cd correctly. Orchestrator disposition: both revision-1 P2 findings closed; no new findings.
