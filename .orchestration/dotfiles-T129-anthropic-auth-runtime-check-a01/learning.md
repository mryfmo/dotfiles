---
task_id: dotfiles-T129-anthropic-auth-runtime-check-a01
round: 1
status: pushed-pr-not-opened
---

# Learning

Task-local triage; nothing promoted.

- A bats `skip` ends the whole `@test`, so in one multi-run case every run that does not need the skipped tool goes before the guard. Here run (e) (an empty store file) needs no `sqlite3` and runs first, so a runner without `sqlite3` still checks the fail-closed path. Applies to any bats case that mixes tool-dependent and tool-free runs.
- In a Claude seat's sandbox, the `test_agmsg_*` installer tests of `tests/unit/test_runtime_health.py` fail on `mktemp` in the system temp directory, which the sandbox denies. Baseline them on a detached `origin/main` worktree before reading them as a regression. Applies to Claude workers running that module locally.
- WebFetch quotes at most 125 characters at a time, so a long statement (a `CREATE TABLE`) comes back as a summary or in pieces. Ask for the parts separately, or rely on a quote already taken by the orchestrator.
- omp's Anthropic provider id is not defined under `packages/ai/src/`: `Provider` and `authProviders()` come from `@oh-my-pi/pi-catalog`. A lookup confined to `packages/ai/src/` finds only uses of `"anthropic"` (in `auth-storage.ts` and `registry/oauth/anthropic.ts`), not the definition or any `storeCredentialsAs` remap.
