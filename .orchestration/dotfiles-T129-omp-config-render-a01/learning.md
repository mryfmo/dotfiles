---
task_id: dotfiles-T129-omp-config-render-a01
round: 1
status: parked-draft-pr
---

# Learning

Task-local triage; nothing promoted.

- omp 18.11.3 keeps per-role reasoning inside the role value as a `:<level>` suffix (`splitThinkingSuffix` in pi-tui's `model-selector.ts`), not in a separate key; `defaultThinkingLevel` is global. A later stage that renders reasoning appends the suffix to the `modelRoles` value. Applies to PR B a02 onward and PR C's launcher.
- omp has no alias table for model ids: `anthropic/haiku` resolves only by fuzzy match within the provider, among four bundled haiku ids. A manifest `claude.model` alias does not carry over to omp exactly. Applies to any `omp.model` derived from a Claude alias (today only `express`).
- omp rewrites `config.yml` itself under `config.yml.lock` and keeps unknown keys on its own writes, so a chezmoi modify script that edits one key is the safe management form, and the apply belongs with omp closed.
- The apply interpreter on this Mac (`/usr/bin/env python3`, mise's Python) has no PyYAML, so the modify script takes its pass-through path here until PyYAML is available to that interpreter. Applies to the operator's apply after merge.
- The generator tests run under `make unit-test` without PyYAML, so a test of the tracked manifest works on its text, and a test of a PyYAML script runs it as a `uv run --no-project --with pyyaml` subprocess.
