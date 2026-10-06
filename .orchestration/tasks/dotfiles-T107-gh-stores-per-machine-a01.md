# AGMSG-TASK dotfiles-T107-gh-stores-per-machine-a01

Drafted 2026-10-06 by the orchestrator seat from the operator's machine→account mapping (`.orchestration/validation/github-auth-design-2026-10-05.md` §14–§15). T103 (#288) assumed three stores (owner, work, worker); the human account is per machine, so there are two. Kind: manifest keys, renderer (model-profiles.env part), `scripts/gh-auth-stores.sh`, doctor, `setup.sh` untouched unless a variable name appears, README, tests; no permission, sandbox or hook boundary. Dispatched to `claude-standard-dot-a005` (worker-c, wT:p2).

## Objective

1. Two stores, not three. Manifest: remove `work_gh_config_dir`; rename `owner_gh_config_dir` → `operator_gh_config_dir` (default `~/.config/gh`, gh's default directory; comment: "this machine's human account, the one that merges on this machine; which account that is differs per machine"); keep `worker_gh_config_dir`. Renderer: `OPERATOR_GH_CONFIG_DIR` and `WORKER_GH_CONFIG_DIR` only; distinct-directory check for the two. Keep the renderer's rule that the operator store equals gh's default directory.
2. `scripts/gh-auth-stores.sh`, `scripts/check-agent-runtime.py` (store findings), `scripts/check-tools.sh` hint: follow the two stores and the variable names; behaviour otherwise unchanged (status → skip, else device-code login with `--insecure-storage`, 0600 or fail, no `setup-git`, `make update` never prompts).
3. README operator-phase block: two-row table (operator account of this machine; worker machine account, the same one on every machine), and delete the sentence about a chezmoi-private `encrypted_private_hosts.yml` (credentials are never stored in a repository; each machine logs in for its own token). Keep the statement that `make update` never prompts.
4. Tests follow (renderer keys, doctor fake stores, script tests, docs parity if any). `make render-check`, `make unit-test`, validator rc=0, prettier on README.

Forbidden: any other file; `make update`/`apply`; thread resolution; local bats; reading or printing any credential.

[memory:decision] dotfiles-T107 (operator 2026-10-06): GitHub credential stores are two per machine, the machine's operator account in gh's default directory and the shared worker machine account in `~/.config/gh-worker`; no "work" store, no credential copies in any repository.

## Repo / branch

worker-c; `git fetch origin`; `git switch -c fix/gh-stores-per-machine --no-track origin/main` (main at e0027811 or later); verify task_rev against the main checkout's task file, otherwise PONG blocked.

## Allowed files

`home/dot_agents/agent-config.yaml` (the store keys and their comment only), `home/dot_agents/model-profiles.env` (rendered), `scripts/generate-agent-configs.py`, `scripts/gh-auth-stores.sh`, `scripts/check-agent-runtime.py`, `scripts/check-tools.sh`, `setup.sh` (only if a store variable name appears), `README.md` (operator-phase block), `tests/**`. Artifacts at the standard seven `dotfiles-T107-gh-stores-per-machine-a01` paths in the main checkout (Claude seat, through the permission gate), masked.

## Validation commands (paste verbatim output, whole)

```
grep -rn 'WORK_GH_CONFIG_DIR\|work_gh_config_dir\|OWNER_GH_CONFIG_DIR\|owner_gh_config_dir\|encrypted_private_hosts' home scripts setup.sh README.md tests; echo "rc=$? (expect no match)"
bash -n setup.sh scripts/gh-auth-stores.sh; echo "rc=$?"
shellcheck setup.sh scripts/gh-auth-stores.sh scripts/check-tools.sh; echo "rc=$?"
make render-check
make unit-test 2>&1 | tail -3
uv run --no-project --with pyyaml scripts/validate-agent-assets.py; echo "rc=$?"
mise x node npm:prettier -- prettier --check README.md 2>&1 | tail -2
gh pr checks <pr>
```

## Completion

PR to `main` (English, attribution footer), CI green, Bot wait per the SKILL, artifacts, the CompactionDB `memory add` of the decision line in the main checkout, `AGMSG-RESULT v1 task_id=dotfiles-T107` via `agmsg-dispatch dotfiles claude-standard-dot-a005 claude-remediation-dot wT:p1 "<single line>"`. max_turns=15.

### PONG decision 1 (orchestrator, 2026-10-06 03:40Z) — HOLD

The operator corrected the model again: a GitHub account belongs to the local login (OS user), so a second credential store under the same OS user is not normal operation either. Stop work on this task now, do not push; keep your branch as is and stand by. The orchestrator will send either a revised objective or a cancellation.

### PONG decision 2 (orchestrator, 2026-10-06 04:10Z) — CANCELLED

Superseded by decision A (design report §16) and dotfiles-T108. The orchestrator closes PR #292 unmerged; discard the branch and its uncommitted edits as T108 instructs. Your CompactionDB memory 2a0f73e2 for the two-store decision is superseded by the T108 decision line.
