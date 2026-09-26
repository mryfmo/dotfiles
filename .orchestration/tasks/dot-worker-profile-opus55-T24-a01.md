# AGMSG-TASK dot-worker-profile-opus55-T24-a01

## Objective

Operator directive (2026-09-27): orchestrator stays on `claude-fable-5` effort
high; herdr worker panes must run Claude Code Opus 5.5 (`claude-opus-5-5`)
effort high. Today `resolve_worker_profile()` falls back to
`MODEL_PROFILE_INTERACTIVE` (= `deep`), so workers launch on fable-5 high.
Introduce a manifest-driven worker profile and repoint the `standard` profile's
claude side at Opus 5.5.

[memory:decision] Operator decision 2026-09-27: herdr worker = Claude Code
`claude-opus-5-5` effort high via manifest `worker_profile: standard`;
`worker_kind` stays `claude`. This supersedes T19 supplement-2's
"set worker_kind: codex" instruction.

## Repo / branch

- Work ONLY in the worktree `/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c`.
- Step 0 — preserve the leftover T21 WIP first (this completes the step-0 the
  withdrawn T20 task already authorized): the worktree is on a detached HEAD
  with uncommitted modifications from task T21. Commit them AS-IS to a new
  branch `wip/orchestrator-guardrails-T21` (commit message
  `wip: preserve T21 orchestrator-guardrails work (T24 step 0)`, plus the
  standard Co-Authored-By line) and `git push -u origin
wip/orchestrator-guardrails-T21`. Do not review, fix, or extend that WIP.
  If the preservation commit or push fails, stop and report via AGMSG-PONG.
- Step 1: `git fetch origin`, then `git switch -c feat/worker-profile-opus55 origin/main`.
- Never touch the main checkout at `/home/moriya/Workspace/dotfiles` (except the
  `.orchestration` artifact paths below, which live in the main checkout).

## Changes (all line numbers against origin/main 8332803)

### 1. `home/dot_agents/agent-config.yaml`

- `standard.claude`: `{ model: sonnet, effort: high }` → `{ model: claude-opus-5-5, effort: high }` (codex side unchanged).
- `review.claude`: `{ model: sonnet, effort: medium }` → `{ model: claude-fable-5, effort: medium }` (keeps the "one capability tier above the worker at reduced effort" invariant; comment stays true).
- Directly after `worker_kind: claude`, add (do NOT insert anything between the
  `adh:` block and `interactive_profile:` — `scripts/check-agent-runtime.py:362`
  regex constraint):

  ```yaml
  # Worker pane model profile for herdr-agents. Renders into
  # ~/.agents/model-profiles.env as HERDR_AGENTS_WORKER_PROFILE; an explicit
  # HERDR_AGENTS_WORKER_PROFILE in the environment still overrides it.
  worker_profile: standard
  ```

### 2. `scripts/generate-agent-configs.py`

- Add `worker_profile(manifest)` next to `worker_kind()` (~L146): returns
  `manifest.get("worker_profile")`; when present it must name a key of
  `model_profiles(manifest)`, otherwise fail. Absent key returns None.
- `render_model_profiles_env()` (~L741): after the `HERDR_AGENTS_WORKER_KIND`
  line, emit `HERDR_AGENTS_WORKER_PROFILE="<value>"` only when the key is set.

### 3. `home/dot_local/bin/common/executable_herdr-agents`

- Rewrite `resolve_worker_profile()` (L73–89) mirroring `resolve_worker_kind()`
  (L93–104) local-shadow pattern. Precedence: explicit env
  `HERDR_AGENTS_WORKER_PROFILE` > deprecated `HERDR_AGENTS_CODEX_PROFILE` >
  env-file `HERDR_AGENTS_WORKER_PROFILE` > env-file `MODEL_PROFILE_INTERACTIVE`
  > `standard`. (Today the env-file value is dead: the explicit-env check
  > returns before the file is sourced.)
- Update the shdoc comments in English (header `@arg` block ~L14–18 and the
  function `@description` ~L69–72) to document the manifest fallback.
- Do NOT change `start_worker_agent()`.

### 4. `scripts/validate-agent-assets.py`

- In `validate_agent_manifest()` after the worker_kind checks (~L640–644):
  when `worker_profile` is present it must name a defined model profile,
  else fail with a message naming the bad value. No README-sentence or
  env-token check (generator `--check` already catches staleness).

### 5. Docs

- `README.md` ~L343–347: insert the manifest `worker_profile` step into the
  worker-profile resolution order (env var > deprecated alias > manifest value
  rendered into `~/.agents/model-profiles.env`, currently `standard` >
  `MODEL_PROFILE_INTERACTIVE` > `standard`).
- `home/dot_config/claude/rules/model-selection.md` L4: extend the
  `worker_kind` sentence to also name `worker_profile` and forbid ad-hoc
  `HERDR_AGENTS_WORKER_PROFILE` exports.

### 6. Tests (mirror the existing worker_kind cases)

- `tests/unit/test_generate_agent_configs.py`: (a) worker_profile renders the
  env line, (b) absent key renders no line, (c) unknown name fails.
- `tests/unit/test_herdr_agents.py`: (a) env-file `HERDR_AGENTS_WORKER_PROFILE`
  is used for the worker launch args, (b) an explicit environment variable
  overrides the env-file value (fixture pattern near L1206).
- `tests/unit/test_validate_agent_assets.py`: unknown `worker_profile` is
  rejected.
- Do not run bats locally (repo policy); CI covers `lifecycle.bats`.

### 7. Regenerate

```
uv run --with pyyaml scripts/generate-agent-configs.py
uv run --with pyyaml scripts/generate-agent-configs.py --check
```

Expected generated diff: ONLY `home/dot_agents/model-profiles.env`
(`MODEL_PROFILE_STANDARD_CLAUDE_ARGS="--model claude-opus-5-5 --effort high"`,
`MODEL_PROFILE_REVIEW_CLAUDE_ARGS="--model claude-fable-5 --effort medium"`,
new `HERDR_AGENTS_WORKER_PROFILE="standard"` after `HERDR_AGENTS_WORKER_KIND`).
`home/.chezmoitemplates/claude-settings-managed.json`, all codex outputs, and
`express-explorer.md` must be unchanged; if they change, stop and report.

## Allowed files

- `home/dot_agents/agent-config.yaml`
- `home/dot_agents/model-profiles.env` (generated)
- `scripts/generate-agent-configs.py`
- `home/dot_local/bin/common/executable_herdr-agents`
- `scripts/validate-agent-assets.py`
- `README.md`
- `home/dot_config/claude/rules/model-selection.md`
- `tests/unit/test_generate_agent_configs.py`
- `tests/unit/test_herdr_agents.py`
- `tests/unit/test_validate_agent_assets.py`
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dot-worker-profile-opus55-T24-a01.md` (in the main checkout)

## Forbidden actions

- Changing `worker_kind`, `interactive_profile`, any codex model/effort, the
  `express`/`deep`/`security`/`adh` profiles, or any file not listed above.
- Merging the PR; editing permgate policy, hooks configs, or anything under
  `reviews/ADH_Integrated_Plan/`.
- Force push (a plain `git push -u origin feat/worker-profile-opus55` on a
  fresh branch needs no force). Dependency changes. Running bats locally.
- `make apply` / `chezmoi apply` / any write outside the repo worktree
  (deployment is orchestrator-side after acceptance).

## Validation commands (paste verbatim output into the validation file)

```
uv run --with pyyaml scripts/generate-agent-configs.py --check
make validate-agent-assets
make unit-test
git -C /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c diff origin/main --stat
gh pr checks <pr-number>
```

## Deliverables

1. Branch `feat/worker-profile-opus55` pushed; PR to `main` with English title
   and description ending with the line
   `🤖 Generated with [Claude Code](https://claude.com/claude-code)`.
   Watch GitHub Actions; fix and re-push until all checks pass.
2. Artifacts at the exact expected paths (report, validation with verbatim
   outputs including the PR number and head SHA, sandbox, learning, autoskill).
3. CompactionDB: run
   `python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "T24: herdr worker profile = standard (claude-opus-5-5 high) via manifest worker_profile; worker_kind stays claude (operator 2026-09-27)"`
   from the main checkout and paste the command + output into the validation
   file.
4. `AGMSG-RESULT v1` with status and all artifact paths. If blocked, still
   write the report/validation explaining the blocker and send
   `status=blocked`.

## Notes

- CI conflict risk with PR #179 (`feat/claude-sandbox-manifest`) and PR #182/#183
  is expected to be zero at branch time (branch from origin/main), but do not
  rebase onto any of those branches.
- cost: include a `cost:` line in the report (observed token/cost or `cost: n/a`).
