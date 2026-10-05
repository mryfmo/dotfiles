# AGMSG-TASK dotfiles-T102-add-worker-credential-notice-a01

Drafted 2026-10-05 17:10Z by the orchestrator seat (dispatched to `codex-standard-dot-a006`, worker-e, `standard` profile). Lesson of 2026-10-05: the first worker seat created after the T90 deploy (`codex-standard-dot-a006`, 11:25Z) learned only from its own `gh auth status` exit 1 that `~/.config/gh-worker/hosts.yml` did not exist; `herdr-agents` said nothing while seating it, and the orchestrator dispatched a task to a seat that could not open a PR. Kind: launcher (`herdr-agents`) plus its unit tests and one README sentence; no permission or sandbox boundary source, so a Codex seat.

## Objective

1. `home/dot_local/bin/common/executable_herdr-agents`: before any seat is created in `--add-worker`, `--restart-worker` and full mode, when `$(worker_github_config_dir)/hosts.yml` does not exist, print exactly one stderr line of the form `herdr-agents: worker GitHub credential missing: <dir>/hosts.yml; the worker seat cannot run gh or push until the operator provisions it (README, operator provisioning)` and continue (exit status and every other output line unchanged; no credential content is read or printed; T90's fail-closed `GH_CONFIG_DIR` behaviour stays as is). Use the existing `worker_github_config_dir` helper; one function, shdoc comment, English.
2. `tests/unit/test_herdr_agents.py`: one test per mode that drives the seat path with a fake home where `hosts.yml` is absent and asserts the single notice line on stderr and an unchanged exit status/stdout, and one test with `hosts.yml` present (empty file is enough) asserting no notice. Reuse the existing fake-CLI fixtures of the `--add-worker` tests.
3. `README.md`, the operator provisioning paragraph (around lines 1224–1251): one sentence saying that `herdr-agents` prints that notice while seating a worker until the file exists.

Forbidden: any other file (the manifest, `scripts/`, the rules, the SKILL, `.github/`); the permission/sandbox/hook blocks; `make update`/`apply`; thread resolution; local bats; reading or printing anything from `hosts.yml`.

[memory:decision] dotfiles-T102 (orchestrator 2026-10-05): seating a worker whose `hosts.yml` is missing prints a one-line notice and continues; provisioning stays the single operator switch.

## Repo / branch

- Work ONLY in your own worktree (worker-e). `git fetch origin`; `git switch -c feat/add-worker-credential-notice --no-track origin/main` (main at aeb025e8 or later). Verify the dispatched task_rev against the main checkout's task file; otherwise stop and PONG blocked.
- Your seat has no `gh` credential (T90, provisioning pending). Disclosed deviation, same as T101: after the final local validation, push the branch over SSH, then send `AGMSG-PONG v1 task_id=dotfiles-T102 status=pushed branch=feat/add-worker-credential-notice commit=<sha>`; the orchestrator opens the PR, runs `gh pr checks`, the Bot wait and the sweep, and answers with the PR number. Do not use any other credential.

## Allowed files

- `home/dot_local/bin/common/executable_herdr-agents`, `tests/unit/test_herdr_agents.py`, `README.md` (one sentence in the provisioning paragraph; T82b edits the hook-trust section concurrently, do not touch it).
- Artifacts in your worktree at `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dotfiles-T102-add-worker-credential-notice-a01.md` plus `.orchestration/validation/dotfiles-T102-add-worker-credential-notice-a01-worker-crit.json` and `-worker-review-receipt.md`; the orchestrator copies them into the main checkout.

## Validation commands (paste verbatim output, whole, unfiltered)

```
git diff origin/main --stat | tail -5
bash -n home/dot_local/bin/common/executable_herdr-agents; echo "rc=$?"
shellcheck home/dot_local/bin/common/executable_herdr-agents; echo "rc=$?"
uv run --no-project python -m unittest tests.unit.test_herdr_agents 2>&1 | tail -3
make unit-test 2>&1 | tail -3
uv run --no-project --with pyyaml scripts/validate-agent-assets.py; echo "rc=$?"
mise x node npm:prettier -- prettier --check README.md 2>&1 | tail -2
git log -1 --format='%H %s'
```

## Completion

1. Branch pushed over SSH, PONG `status=pushed` (see above); PR title/description in English are the orchestrator's, from your report's summary paragraph (write one).
2. Artifacts at the exact expected paths; validation with verbatim outputs, commit SHA, PR number once the orchestrator sends it; `cost: n/a`.
3. CompactionDB: say in the report that the orchestrator records the decision (Codex seat).
4. After the orchestrator's PR number arrives: `AGMSG-RESULT v1 task_id=dotfiles-T102 … pr=<n> head=<sha> bot=orchestrator-side` via `agmsg-dispatch dotfiles codex-standard-dot-a006 claude-remediation-dot wT:p1 "<single line>"`. max_turns=12.

### PONG decision 1 (orchestrator, 2026-10-05 17:18Z) — PR #285 opened by the orchestrator

Your SSH push succeeded (015929c8 on `feat/add-worker-credential-notice`). The orchestrator opened PR #285 and takes over `gh pr checks`, the Bot wait and the sweep. You: set `pr: 285` in the report and validation, finish the artifacts, and send `AGMSG-RESULT v1 task_id=dotfiles-T102 … pr=285 head=015929c8 bot=orchestrator-side cost=n/a`. Do not push again unless asked.
