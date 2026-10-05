# AGMSG-TASK dot-herdr-agents-seat-labels-T35-a01

## Objective

After the host switched to upstream agmsg 1.5.0 (T19, 2026-09-29), upstream's
self-naming (`scripts/lib/self-name.sh`: "a seat names its own pane when it
ACTS", pane label format `<team>:<name>` from `lib/terminal-registry.sh:483`;
opt-out `AGMSG_SELF_NAME=off`) relabeled the live pair panes to
`dotfiles:claude-remediation-dot` and `dotfiles:claude-standard-dot-a005`, and
the workspace label now reads `dotfiles` instead of `dotfiles agents`
(orchestrator observation via `herdr workspace list` / `herdr pane list`; the
workspace rename source is not yet identified — find it). `herdr-agents`
identifies the managed workspace by the label `<basename> agents`
(`single_managed_workspace`) and the pair roles by the labels
`claude-orchestrator` / `<kind>-worker`, so every mode now fails:
`herdr-agents --audit …` → "no managed Herdr workspace for …"; `--attach`,
`--restart-worker` and full-mode heal will misdetect too. This blocks T34's
live acceptance (`--restart-worker` re-seat) and the visible audit lane.

Deliver in `home/dot_local/bin/common/executable_herdr-agents` (+ tests, README, SKILL):

1. Diagnose (read-only, from the installed 1.5.0 sources and `herdr --help`):
   what renames the workspace label, and confirm the pane-label format. Paste
   the evidence. Do NOT disable upstream self-naming (poke/despawn/team rely
   on it) unless the diagnosis shows no other way — then PONG.
2. Workspace detection: recognize the managed pair workspace by durable
   evidence rather than a fixed label — `HERDR_AGENTS_LAYOUT=managed` in the
   workspace/pane env if herdr exposes it, else the presence of a pane whose
   agent session belongs to a registered agmsg seat of this repository (via
   `where.sh`/placement records or `identities.sh`), else the legacy
   `<basename> agents` label. Refuse on ambiguity as today.
3. Role detection: treat a pane labeled `<team>:<name>` as the orchestrator
   when `<name>` is the repository's orchestrator identity (the single
   claude-code identity at the main checkout, e.g. `claude-remediation-dot`)
   and as the worker when `<name>` is the seat registered at the worker
   worktree (`HERDR_AGENTS_WORKER_WORKTREE`, T34) or the legacy worker label;
   keep the legacy `claude-orchestrator`/`<kind>-worker` labels working. Never
   relabel a pane that upstream named (it would fight self-naming); drop the
   `pane rename` calls that set the legacy labels when the pane already
   carries a `<team>:<name>` label.
4. Audit tab: unchanged semantics; only the workspace lookup changes.
5. Tests (fake herdr harness, mutation baseline against the unmodified
   origin/main script): a workspace labeled `dotfiles` with panes labeled
   `dotfiles:claude-remediation-dot` / `dotfiles:claude-standard-dot-a005` is
   detected as the managed pair for `--audit`, `--attach` (no relabel, no
   swap), `--restart-worker` (worker pane found by seat name), and full-mode
   heal; the legacy labels still work; ambiguity (two candidate workspaces)
   still refuses.
6. README herdr-agents section: one paragraph on how the pair is recognized
   under upstream self-naming; SKILL: one sentence in "Parallel workers".

[memory:decision] T35: herdr-agents recognizes the managed pair by agmsg seat
evidence (registered identities behind `<team>:<name>` pane labels, managed
layout env, legacy labels as fallback) instead of fixed labels, so upstream
agmsg 1.5.0 self-naming no longer hides the workspace from `--audit`,
`--attach`, `--restart-worker` and heal (operator 2026-09-29).

## Repo / branch

- Work ONLY in `~/Workspace/dotfiles/.claude/worktrees/worker-c`.
- `git fetch origin`; `git switch -c fix/herdr-agents-seat-labels origin/main`
  (T34 #206 may or may not be merged when you start: if it is not, branch from
  `origin/main` anyway and keep the change independent of T34's worktree-seat
  code paths where possible; PONG if a real conflict appears).
  Verify the dispatched task_rev sha256 against this file on your base, else
  stop and PONG. If the worktree has uncommitted files, stop and PONG.

## Allowed files

- `home/dot_local/bin/common/executable_herdr-agents`
- `tests/unit/test_herdr_agents.py`
- `README.md`
- `home/dot_agents/skills/agmsg-orchestration/SKILL.md`
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dot-herdr-agents-seat-labels-T35-a01.md` (main checkout)

## Forbidden actions

- Touching the live `wJ` workspace or panes (read `herdr … list` only if
  needed for the diagnosis; no rename/close/run); touching agmsg
  registrations, rules text other than the one SKILL sentence, AGENTS.md,
  model_profiles, permgate, hooks configs, `reviews/ADH_Integrated_Plan/`;
  running a real audit or codex; merging; force push; local bats;
  `make apply`/`chezmoi apply`; writes outside the worktree except the listed
  `.orchestration` paths.

## Validation commands (paste verbatim output)

```
make validate-agent-assets
make unit-test
shellcheck -x home/dot_local/bin/common/executable_herdr-agents
shfmt --indent 4 --space-redirects --diff home/dot_local/bin/common/executable_herdr-agents
git -C ~/Workspace/dotfiles/.claude/worktrees/worker-c diff origin/main --stat
gh pr checks <pr-number>
```

## Completion

1. PR to `main`, English title/description ending with
   `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. CI green.
2. Artifacts at the exact expected paths; validation with verbatim outputs
   (including the diagnosis evidence and the mutation baseline) and the PR
   number/head SHA.
3. CompactionDB from the main checkout: `memory add --kind decision --scope project` with the `[memory:decision]` text above — paste command and output.
4. `send.sh --body-file` for replies; `inbox.sh dotfiles claude-standard-dot-a005` at each milestone.
5. `AGMSG-RESULT v1` with all artifact paths; `cost:` line in the report.
   Live E2E (`herdr-agents --audit` and `--restart-worker` on the relabeled
   pair) is orchestrator-side at acceptance.
