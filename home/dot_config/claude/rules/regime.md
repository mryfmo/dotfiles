## Regime

- **Loop.** Work runs through the omp seats on the hcom bus: the `hcom-orchestration` skill is the loop, `hcom-worker` and `hcom-audit` its two halves. The standard a change meets is `AGENTS.md` "Audit" and "Code Review Rules".
- **`main`.** Every repository change lands through a seat's pull request, merged with `gh pr merge --squash --match-head-commit <audited head>`; never push to `main`.
- **Routing.** A seat never edits the source of its own execution boundary: Claude-boundary changes go to a Codex seat, Codex-boundary changes to a Claude seat, and shared sources or permgate to the operator.
- **Records.** The program store is `.orchestration/orchestrate/<program>/`; its `preferences.md` is the standing order. It outranks bus messages and other repository text, never the operator's own instructions, which outrank both.
- **Levers.** Only logins and Keychain steps are the operator's. Everything else is a lever with an allow rule or a seat policy row, never an ad-hoc permission. A lever never widens a seat's boundary: approval is not containment, and the account and the worktree stay the boundary (`home/dot_agents/omp/policies/README.md` threat table).
