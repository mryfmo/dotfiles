# Codex audit — dot-mosh-and-asset-bumps-T31-a01 (PRE-MERGE, commit 7191193)

Invocation: `codex --profile audit review --commit 7191193d671063dc01849562c79af69a8737fdf5` (orchestrator, 2026-09-27 — first pre-merge audit under the live lane).

Session header:

```
OpenAI Codex v0.157.1
--------
workdir: ~/Workspace/dotfiles
model: gpt-6-astra
provider: openai
approval: never
sandbox: read-only
reasoning effort: high
reasoning summaries: concise
session id: 01a0e1bb-ef17-74c1-b58b-e8f0cd8c26d1
--------
user
```

Verdict (verbatim, deduplicated):

```
No actionable regressions were identified in the named commit. Syntax checks, AppArmor template rendering, and the missing-bwrap failure check passed; full tests and CI were not run.
```
