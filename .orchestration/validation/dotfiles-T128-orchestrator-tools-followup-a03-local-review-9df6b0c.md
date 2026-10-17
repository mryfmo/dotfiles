---
task: dotfiles-T128-orchestrator-tools-followup-a03
head: 9df6b0c7594cef7f42e9a43faa3e08d0f035e329
pr: 374
base: 1d41812678366506151579ce3e2ac96b20e8d4b5
started: 2026-10-16T22:33:11Z
finished: 2026-10-16T22:36:32Z
findings: 1
engine: codex review --base main (profile review, read-only)
---

- [P1] Isolate uv from inherited virtual environments — scripts/orchestrator/dispatch.sh:183-185

```text
The new uv invocation still permits an inherited virtual environment to execute code before validation. Syntax checks passed; runtime tests were not run in the read-only sandbox.

Review comment:

- [P1] Isolate uv from inherited virtual environments — scripts/orchestrator/dispatch.sh:183-185
  If the caller has `VIRTUAL_ENV` pointing at a PR checkout's `.venv`, changing directory does not isolate these calls: `uv run --no-project` still honors the active environment. Its interpreter and site-packages can therefore execute during the initial `import yaml` probe, before task validation; the later `-I` flags do not constrain uv's interpreter selection. Select a trusted interpreter, exclude the inherited environment, and add a regression test with `VIRTUAL_ENV` set. Otherwise the task's interpreter/environment residual control remains ineffective ([AGENTS.md:78](AGENTS.md#L78)).
The new uv invocation still permits an inherited virtual environment to execute code before validation. Syntax checks passed; runtime tests were not run in the read-only sandbox.

Review comment:

- [P1] Isolate uv from inherited virtual environments — scripts/orchestrator/dispatch.sh:183-185
  If the caller has `VIRTUAL_ENV` pointing at a PR checkout's `.venv`, changing directory does not isolate these calls: `uv run --no-project` still honors the active environment. Its interpreter and site-packages can therefore execute during the initial `import yaml` probe, before task validation; the later `-I` flags do not constrain uv's interpreter selection. Select a trusted interpreter, exclude the inherited environment, and add a regression test with `VIRTUAL_ENV` set. Otherwise the task's interpreter/environment residual control remains ineffective ([AGENTS.md:78](AGENTS.md#L78)).
```
