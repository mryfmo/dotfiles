---
format: 2
task_id: dotfiles-T129-omp-config-render-a01
kind: code
security: true
allowed_files:
  - home/dot_agents/agent-config.yaml
  - scripts/generate-agent-configs.py
  - home/.chezmoitemplates/omp-config-managed.yml
  - home/dot_omp/agent/modify_config.yml
  - home/dot_agents/model-profiles.env
  - home/dot_agents/README.md
  - tests/unit/test_generate_agent_configs.py
  - tests/unit/test_omp_config_merge.py
  - .orchestration/dotfiles-T129-omp-config-render-a01/**
after: []
threat_table:
  - control: 'the PR edits home/dot_agents/agent-config.yaml only by adding one `omp: { model: "<provider>/<id>" }` mapping under each of the six model_profiles entries (item 0b) and nothing else'
    disposition: "residual: the values are model ids only, never a secret; a test strips the six omp lines from the working-tree manifest and asserts byte-identity with origin/main's manifest (skipped once origin/main carries them); `git diff origin/main -- home/dot_agents/agent-config.yaml` is pasted in validation.md with exactly six `+` lines and no `-` line, and the orchestrator confirms the derivation table at acceptance"
  - control: the PR edits scripts/generate-agent-configs.py only for items 1 to 3
    disposition: "residual: the generator gains one per-profile validator (omp.model under an allowlist of two providers and id characters) and one output; it reads the manifest only and never a credential; one test per refusal, and the orchestrator's diff review and the task-level audit from main compare the diff against the items"
  - control: home/.chezmoitemplates/omp-config-managed.yml (generated)
    disposition: "residual: byte-compared by make render-check; it carries provider and model ids only, and a test asserts the rendered text holds no ANTHROPIC or OAUTH token and no key-like value (PR D's CI grep covers the tree later)"
  - control: home/dot_omp/agent/modify_config.yml (a chezmoi modify script writing ~/.omp/agent/config.yml at apply)
    disposition: "residual: it replaces modelRoles.default only and keeps every other key omp wrote; when PyYAML is missing, the input is not YAML, or the input is not a mapping it prints its input unchanged with a warning on stderr (exit 0), so omp's file is never clobbered; it runs only under the operator's chezmoi apply, never in this task"
  - control: home/dot_agents/model-profiles.env (generated, sourced by launchers)
    disposition: 'residual: the new lines are MODEL_PROFILE_<NAME>_OMP_MODEL="<provider>/<id>" under the generator''s launcher-safe regex; render-check compares bytes; no launcher reads them until PR C'
  - control: home/dot_agents/README.md
    disposition: "residual: one list line naming the new generated file; prose"
  - control: tests/unit/test_generate_agent_configs.py
    disposition: "residual: fixtures only, one per item and per refusal, red before and green after; the manifest test shells out to git read-only (git show origin/main:…) as test_orchestrator_tools.py already does"
  - control: tests/unit/test_omp_config_merge.py (new)
    disposition: "residual: runs the modify script as a subprocess on temporary files and a stub yaml package on PYTHONPATH; never reads or writes ~/.omp"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T129-omp-config-render-a01/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T129-omp-config-render-a01/ (report.md, validation.md, sandbox.md, learning.md)
    disposition: "residual: prose and pasted command output; the sandbox record lists every permission-gated command; the audit reads them"
  - control: "task metadata (the front matter of the task copy: kind, security, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: "the provider route as a trust boundary (Anthropic by API key only, OpenAI by the openai-codex OAuth provider; plan 023 Decision)"
    disposition: "residual: the validator admits anthropic/ and openai-codex/ prefixes only, so no manifest value or rendered role can name an Anthropic OAuth route; the login state of the machine is PR D's check (dotfiles-T129-anthropic-auth-route-check-a01), not this task's"
  - control: in-process effects
    disposition: "residual: the generator tests run it in-process with module.ROOT redirected to a temporary directory (the file's existing pattern) and the modify script as a subprocess; nothing writes under $HOME"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow file is in allowed_files; the modify script runs under /usr/bin/env python3 as the two existing modify scripts do, with PyYAML optional and fail-closed; the generator keeps its uv --with pyyaml entry points"
  - control: new or renamed scripts
    disposition: "residual: one new modify script and one new generated template, both named in allowed_files and both in the generator's expected_outputs or the README list; any other new or renamed file is an undeclared change the audit fails"
  - control: orchestrator effect merge
    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
premises:
  - claim: "the generator renders nothing for omp today"
    command: '/usr/bin/grep -cw "omp" scripts/generate-agent-configs.py'
    output: |-
      0
  - claim: "no omp source lives under home/ yet (the chezmoi target ~/.omp/agent/config.yml is unmanaged)"
    command: '/bin/ls -d home/dot_omp home/private_dot_omp 2>&1 | /usr/bin/grep -c "No such file"'
    output: |-
      2
  - claim: "the manifest carries no omp block today; this PR adds six (item 0b), and the orchestrator re-runs this on the branch at acceptance expecting 6"
    command: '/usr/bin/grep -c "^    omp:" home/dot_agents/agent-config.yaml'
    output: |-
      0
  - claim: "PR A (#388) landed the omp asset with its install path, so the install is make update, not this task"
    command: '/usr/bin/grep -n "install_path: ~/.local/bin/omp" home/dot_agents/agent-config.yaml'
    output: |-
      532:    install_path: ~/.local/bin/omp
---

# AGMSG-TASK dotfiles-T129-omp-config-render-a01 — plan 023 PR B, stage 1: omp's model roles rendered from the manifest

Written 2026-10-18 by the orchestrator seat from plan 023 (`.orchestration/plans/023-omp-hcom-migration.md`, "## Pull requests" item B and the classification table), revised at the operator's 08:1x JST policy change: the worker seat adds the manifest's six `omp.model` keys itself (item 0b). Stage 1 of PR B: the renderer learns one `omp` block per model profile and writes omp's user config; nothing else of the B bullet (project `.omp` hooks, the omp auditor, the staged retirement of the `.claude` and `.codex` renderers) is in this task, see "Stages".

**Wave notes:** `scripts/generate-agent-configs.py` and `tests/unit/test_generate_agent_configs.py` are in `dotfiles-T130-codex-local-review-exclusion-a01`'s `allowed_files`, but PR #399 is held open and unmerged by D-399-A (`.orchestration/decisions.tsv` line 42), so the overlap is with a held branch, not a concurrent task: this task starts now from `origin/main`, and a revived #399 rebases onto the result later. `home/dot_agents/agent-config.yaml` is also in `dotfiles-T129-orchestrator-load-mechanisms-a01`'s list (its `after:` is `[dotfiles-T129-assets-omp-hcom-a01]`, already merged as #388, so it is dispatchable; it edits the manifest in one place, the Claude hooks entry, other lines than the six profile mappings). Ordering rule: YAML is code, not prose, so the two never run concurrently; if load-mechanisms a01 is dispatched when this task is, this task's `after:` gains its id and waits, otherwise this task goes first and load-mechanisms follows; whichever PR is second takes the new base with `gh pr update-branch` and re-runs CI, the sweep and the audit. The manifest's other listers (`dotfiles-T129-integration-seat-result-gate-cap-a01`, `dotfiles-T130-codex-local-review-exclusion-a01`, `dotfiles-T129-pstack-asset-a01`) are merged or held.

## Manifest keys this task adds (item 0b)

Under every one of the six `model_profiles` entries (express, standard, review, deep, security, audit), one mapping `omp: { model: "<provider>/<model id>" }` and nothing else in the file. `<provider>` is `openai-codex` for an OpenAI model and `anthropic` for an Anthropic model (plan 023 Decision; the local `~/.omp/agent/config.yml` already holds `modelRoles.default: anthropic/<model>`, which fixes the `provider/model` form). No reasoning key yet: omp's name for it is unverified (item 0 reports it).

## Goal

`uv run --with pyyaml scripts/generate-agent-configs.py` writes `home/.chezmoitemplates/omp-config-managed.yml` and six `MODEL_PROFILE_<NAME>_OMP_MODEL` lines from the manifest's `omp` blocks, refuses a block outside the provider allowlist, and `chezmoi apply` carries the managed `modelRoles.default` into `~/.omp/agent/config.yml` without touching omp's other keys. `make render-check` green on the branch.

## Work items (each with its test; one fixture per item, red before and green after)

0. Facts first, pasted into report.md before any code: `~/.local/bin/omp --version` (the symlink is dangling on the orchestrator's machine as of 2026-10-18 and `make update` installs 18.11.3; a worker without omp reports the version as `not installed` and continues, the file facts below suffice for this stage); the key names omp documents for model roles beyond `default` and for a per-role reasoning amount (`omp --help`, or the settings reference shipped with the installed version); whether omp rewrites `config.yml` itself (the local file holds `symbolPreset`, `composer`, `theme`, `setupVersion` beside `modelRoles`, and a `config.yml.lock` sits beside it); whether omp's `anthropic` provider accepts an alias such as `haiku` or needs a full model id. Nothing unverified is rendered: if only `default` is documented, only `default` is rendered, and the RESULT says so.
   0b. The defaults (the operator's rule of 08:1x JST). For each of the six profiles, `omp.model` is derived from that profile's existing ids: an OpenAI model goes through the `openai-codex` OAuth provider as `openai-codex/<the profile's codex.model>`; an Anthropic model goes through the API-key provider as `anthropic/<the profile's claude.model>`; never an Anthropic OAuth route. The worker chooses per profile the model of the seat kind that profile serves: `deep` (the orchestrator; `orchestrator_kind: claude`) and `review` (INV-7: the same model and effort as `deep` in a fresh context) are Claude seats; `audit` (the auditor: Codex `gpt-6-astra`, read-only) and `security` (the Codex security worker of `model-selection.md`) are Codex seats; `standard` follows `worker_kind` (`claude` today); `express` follows its launch args (both `MODEL_PROFILE_EXPRESS_CLAUDE_ARGS` and `_CODEX_ARGS` are rendered; the tree's only express consumers are the two Claude agents `express-explorer.md` and `project-map.md`), so the worker names which and why. The roles are README.md "Agent work runs as a three-role constellation" (line 361) and the manifest's `worker_kind` and `orchestrator_kind`. The worker pastes the derivation table (profile, claude id, codex id, chosen omp.model, reason) in report.md, flagging any alias item 0 found omp cannot resolve; the orchestrator confirms the table at acceptance. Test: a unit test asserts the working-tree manifest has exactly six `omp:` lines, one under each profile, each matching the allowlist, and that the manifest with those six lines removed is byte-identical to `git show origin/main:home/dot_agents/agent-config.yaml` (skipped when origin/main already holds six `omp:` lines).
1. Manifest reading. `PROFILE_AGENT_KEYS` gains `"omp": ("model",)`, validated by `OMP_MODEL_RE = ^(openai-codex|anthropic)/[A-Za-z0-9._-]+$` (the existing `PROFILE_VALUE_RE` refuses `/`, so the omp value gets its own check inside `model_profiles()`), failing with `model profile <name> is missing omp` or `model profile <name>.omp.model must be <provider>/<id> with provider openai-codex or anthropic`. Test: a profile without `omp`, one with `openai/gpt-x`, one with `anthropic/claude x` each fail with the named message; a well-formed one passes.
2. The user config. `render_omp_config(manifest)` returns `# <GENERATED_HEADER>\nmodelRoles:\n  default: <the interactive_profile's omp.model>\n` (string literal, no YAML library on the write side), and `expected_outputs` maps `ROOT / "home/.chezmoitemplates/omp-config-managed.yml"` to it. Test: the path is in `expected_outputs(sample_manifest())` with that exact text; changing `interactive_profile` changes the role; the text contains neither `ANTHROPIC` nor `OAUTH`.
3. The env lines. `render_model_profiles_env` adds `MODEL_PROFILE_<NAME>_OMP_MODEL="<provider>/<id>"` after each profile's `_CODEX_ARGS` line. Test: the six lines in sorted profile order. Regenerate the tracked `home/dot_agents/model-profiles.env` with the README's command (line 59), never by hand.
4. The apply side. `home/dot_omp/agent/modify_config.yml` (mode 755, `#!/usr/bin/env python3`, shdoc-style module docstring): reads the current `~/.omp/agent/config.yml` from stdin, reads the managed baseline from `source_dir() / ".chezmoitemplates/omp-config-managed.yml"` as `home/dot_codex/modify_private_config.toml` resolves its baseline (line 630), sets `modelRoles.default` to the managed value, keeps every other key and every other role, and writes YAML with `yaml.safe_dump(sort_keys=False)`. Fail closed: `import yaml` failing, input that does not parse, or a parsed value that is not a mapping, each writes the input unchanged to stdout, one warning line to stderr, exit 0; empty input yields the managed mapping only. Test file `tests/unit/test_omp_config_merge.py` (the `test_claude_settings_merge.py` pattern, subprocess with a temporary source dir): keeps unknown keys and other roles; empty input; invalid YAML passes through byte for byte; a stub `yaml` package on `PYTHONPATH` that raises `ImportError` passes through byte for byte.
5. `home/dot_agents/README.md`: add `home/.chezmoitemplates/omp-config-managed.yml` to the generated-files list (lines 20 to 27).

Skipped on purpose (say so in report.md): `models.yml` (both providers are built in per plan 023 "Facts read today"; add it only if item 0 shows one needs a custom entry, as a follow-up); a chezmoi-managed plain `config.yml` (omp writes its own keys there, so only a modify script is safe); per-profile omp directories (`~/.omp/profiles/<name>/agent` would split the auth store; PR C's launcher selects the model per seat from the env lines instead, VERIFY in C).

## Stages of PR B after this task (not in scope; the orchestrator writes them as `-a02` onward)

a02 the project `.omp` config, rules and hooks (the project-map reload hook as an omp hook, carrying the rows the plan keeps from `dotfiles-T128-project-map-pane-open-a01-followup-a02`: `local:3288959:1` and `:2` in `.orchestration/acceptance/dotfiles-T128-project-map-pane-open-a01-followup-a01.md`); a03 the headless auditor and reviewer as `omp` runs, replacing `codex --profile audit exec` in `scripts/orchestrator/orch-audit.sh` line 72 and `herdr-agents --audit`; a04 the Stop-gate behaviour as an hcom hook (after PR C's bus); a05 onward the retirement of the `.claude` and `.codex` renderers in stages (hooks, settings, directories), each with its tests and `.chezmoiremove` entries.

## Validation (outputs pasted in validation.md)

- `uv run --with pyyaml scripts/generate-agent-configs.py` then `make render-check` (never the renderer's own `--check` as the pasted check) and `make validate-agent-assets`.
- `git diff origin/main -- home/dot_agents/agent-config.yaml` (six `+` lines, no `-` line) and the derivation table of item 0b.
- `uv run python -m unittest tests/unit/test_generate_agent_configs.py tests/unit/test_omp_config_merge.py -v`, then `make unit-test` once on the final head (the generator tests need `chezmoi` on PATH).
- `make format`, then `git status --porcelain` showing only this task's files.
- Caps, from `git diff --numstat origin/main...HEAD`: at most 170 changed lines outside `tests/` and `.orchestration/`, at most 500 under `tests/`.

## Forbidden

Editing `home/dot_agents/agent-config.yaml` outside the six `omp` mappings, or any file outside `allowed_files`; running `chezmoi apply` or writing under `~/.omp` (the live apply is the operator's step after merge, with omp closed); adding `models.yml`, a reasoning key or a role name without item 0's evidence; an `omp.model` outside the two providers or not derived by item 0b's rule; touching the Claude or Codex rendered outputs' content (the routing rule: this task's diff must leave `claude-settings-managed.json` and `codex-config-managed.toml` byte-identical, which `make render-check` shows); any removal of a `.claude` or `.codex` renderer (later stages).

## Completion

One PR from a fresh branch off `origin/main` now. Under the morning merge-gate policy the worker opens its own PR with `gh pr create --base main --head <branch> --title <title> --body-file <path> --draft` (one command, no shell metacharacters) and, when the Check's outputs are in the validation file, marks it ready with `gh pr ready <number>`. The Completion clause of `.orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md` applies as written otherwise, with `dotfiles-T129-omp-config-render-followup-a01` as the owner of any advisory P2 and `task_copy=<sha256 of .orchestration/dotfiles-T129-omp-config-render-a01/task.md>` in the RESULT.

## RESULT contents

Head, base, branch, files, every Bot thread with its disposition, the test names, the caps, `task_copy=`, the evidence paths; item 0's facts (omp version or `not installed`, the documented role names, the reasoning key or `none`, whether omp rewrites `config.yml`, alias handling); item 0b's derivation table; the PyYAML state of the apply interpreter (`/usr/bin/env python3 -c 'import yaml'; echo exit=$?` on the worker's machine; the operator repeats it before apply); the follow-up list for a02 onward with anything item 0 changed.

## Checks (pasted by the orchestrator before each send)

```
(pending: pasted at dispatch)
```
