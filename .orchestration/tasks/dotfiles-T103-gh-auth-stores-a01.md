# AGMSG-TASK dotfiles-T103-gh-auth-stores-a01

Drafted 2026-10-05 19:30Z by the orchestrator seat from the operator's direction in `.orchestration/validation/github-auth-design-2026-10-05.md` §10–§11. Kind: bootstrap script (`setup.sh`), Makefile target, doctor check, renderer (model-profiles.env part only), README; no permission, sandbox or hook boundary source, so a Claude seat is allowed. Dispatched to `claude-standard-dot-a005` (worker-c, wT:p2) on the operator's go (「是正」, 19:40Z).

## Objective

1. One GitHub credential store per account, each a `GH_CONFIG_DIR`: `~/.config/gh` (owner account, gh default), `~/.config/gh-work` (work account), `~/.config/gh-worker` (machine account, the existing T90 `worker_gh_config_dir`). Declare the three in `home/dot_agents/agent-config.yaml` next to `worker_gh_config_dir` (names and paths only, never logins or tokens) and render them into `~/.agents/model-profiles.env`.
2. `setup.sh` operator phase and a new interactive `make gh-auth`: for each store, if `GH_CONFIG_DIR=<dir> gh auth status --hostname github.com` succeeds, skip; otherwise `GH_CONFIG_DIR=<dir> gh auth login --hostname github.com --git-protocol https --insecure-storage`, `chmod 600 <dir>/hosts.yml`, `GH_CONFIG_DIR=<dir> gh auth setup-git --hostname github.com`. The device-code dialogue is gh's own; no credential value is read, echoed or logged.
3. `make update` stays unattended: no login call anywhere on its path. `make doctor` reports each store as present (file mode 0600, one user, login name) or missing, with the `make gh-auth` hint; a store that chezmoi-private already populated passes without any prompt.
4. README: replace the operator-phase block (lines ~1245–1260) with the three-store table and the `make gh-auth` step; state that a chezmoi-private `encrypted_private_hosts.yml` per store makes the step prompt for nothing; keep the sentence that `make update` never prompts.
5. Tests: `tests/unit/` coverage for the renderer keys and the doctor check with fake stores; shell syntax and shellcheck for `setup.sh` and the new script; no bats locally.

Forbidden: any `gh auth login` inside `make update`, `scripts/update-agent-assets.sh` or chezmoi scripts; reading or printing token values; editing permgate, sandbox or permission blocks; `make update`/`apply`; thread resolution.

[memory:decision] dotfiles-T103 (operator 2026-10-05): GitHub credentials are one store per account, prompted for only in the interactive operator phase (`setup.sh`, `make gh-auth`); `make update` never prompts; chezmoi-private encrypted `hosts.yml` files make the prompt a no-op.

## Repo / branch

- Work ONLY in your own worktree (worker-c). `git fetch origin`; `git switch -c feat/gh-auth-stores --no-track origin/main` (main at 2d0ef943 or later). Verify the dispatched task_rev against the main checkout's task file; otherwise stop and PONG blocked.
- Design source: `.orchestration/validation/github-auth-design-2026-10-05.md` §10–§11 (read it first; it is evidence, the objective above is the instruction).

## Allowed files

`setup.sh`, `Makefile`, a new `scripts/gh-auth-stores.sh`, `scripts/check-agent-runtime.py` (doctor), `scripts/generate-agent-configs.py`, `home/dot_agents/agent-config.yaml` (the store declarations only), `home/dot_agents/model-profiles.env` (rendered), `README.md` (operator-phase block), `tests/unit/**` for those. Artifacts at `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dotfiles-T103-gh-auth-stores-a01.md` plus `.orchestration/validation/dotfiles-T103-gh-auth-stores-a01-worker-crit.json` and `-worker-review-receipt.md`, written into the main checkout through the permission gate as a Claude seat does (SKILL Worker step 4), masked with the validator.

## Validation commands (paste verbatim output, whole)

```
bash -n setup.sh scripts/gh-auth-stores.sh; echo "rc=$?"
shellcheck setup.sh scripts/gh-auth-stores.sh; echo "rc=$?"
make render-check
make unit-test 2>&1 | tail -3
uv run --no-project --with pyyaml scripts/validate-agent-assets.py; echo "rc=$?"
grep -n 'gh auth login' Makefile scripts/update-agent-assets.sh home/.chezmoiscripts 2>/dev/null; echo "rc=$? (expect no match outside the gh-auth target)"
gh pr checks <pr>
```

## Completion

1. PR to `main`, English title/description ending with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`; CI green on the final head, branch up to date.
2. After the final push: Bot wait per the SKILL (end on a quota notice and record it); fix P0/P1 findings; do not resolve threads.
3. Artifacts at the exact expected paths; validation with verbatim outputs, PR number, head SHA; `cost: n/a`.
4. CompactionDB: record the `[memory:decision]` line above with `uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project` in the main checkout (the documented exception).
5. `AGMSG-RESULT v1 task_id=dotfiles-T103` via `agmsg-dispatch dotfiles claude-standard-dot-a005 claude-remediation-dot wT:p1 "<single line>"`. max_turns=20.

### PONG decision 1 (orchestrator, 2026-10-05 22:25Z) — drop `gh auth setup-git`; the managed helper already serves every store

Agreed with the proposal: `home/dot_config/git/config.tmpl` already installs `credential.helper = !gh auth git-credential`, that helper reads `GH_CONFIG_DIR`, so it serves all three stores, and `gh auth setup-git` would rewrite the chezmoi-managed `~/.config/git/config` and leave drift (`make update` stops at chezmoi's changed-since-last-write prompt, doctor WARN, `setup.sh` refusal). Remove the `setup-git` call from `setup.sh`, `scripts/gh-auth-stores.sh` and the README bullet; state in the README that the managed git config's helper covers every store. Objective item 2 is amended accordingly. The other review findings you listed stay in scope. `scripts/check-tools.sh` is added to the allowed files for one change: its manual-login hint points to `make gh-auth`. The drift claim is accepted on the documented behaviour of `git config --global` and chezmoi; no out-of-gate probe is wanted.

### PONG decision 2 (orchestrator, 2026-10-05 23:10Z) — file storage for every store stands; the Bot P1 is dispositioned by the orchestrator

Operator decision (design report §12): one store per account, `--insecure-storage` for all three, as objective item 2 says. Do not change the storage form. The orchestrator replies to the Bot thread on `scripts/gh-auth-stores.sh:45` with `not-applicable` (operator-accepted exposure, documented) and resolves it; you do not touch the thread. Finish the in-scope review fixes you listed, push if anything is pending, run CI and the Bot wait on the final head, then send the RESULT.

## Revise round 1 (orchestrator, 2026-10-05 23:30Z) — audit of 0a28eb74: `incorrect` (2 P2, 3 P3)

1. **Fresh bootstrap cannot find `gh` (P2, `setup.sh:374`).** `gh` is installed through mise in a child step, and the parent shell has only `~/.local/bin` on PATH, so `command -v gh` fails and the interactive login is skipped on exactly the first run it exists for. Resolve `gh` the way the bootstrap resolves other mise tools (the mise shims directory on PATH, `mise which gh`, or `mise exec -- scripts/gh-auth-stores.sh`), and make the script's own `gh` lookup follow the same path. Regression test: a fake fresh PATH without the shims where `gh` is reachable only through the fake mise still runs the login step.
2. **Duplicate-store check ignores `~` (P2, `generate-agent-configs.py:1273`).** `~/.config/gh` and its absolute form pass as two different stores. Expand `~` (against `$HOME` at render time) before `normpath` in the comparison; test the pair.
3. **Mode/ownership warning lacks the hint (P3, `check-agent-runtime.py:634`).** Every store warning ends with `run make gh-auth`, including the 0600/owner one; test it.
4. **Artifacts (P3 ×2).** The sandbox report still says `check-tools.sh` was out of scope: state the PONG-decision-1 authorization and the edit. The report's "CI green on every head" becomes the heads whose check output is pasted (first and final; add intermediate heads only if you paste them), and the ruff-check claim gets its pasted output or goes.

Then push, CI, Bot wait on the final head, `AGMSG-RESULT v1 … round=1`. No `make update`.

## Revise round 2 (orchestrator, 2026-10-06 00:00Z) — audit of a41a56bd: `incorrect` (1 P2, 1 P3)

1. **A failed `chmod 600` is swallowed (P2, `scripts/gh-auth-stores.sh:36`).** `ensure_store` runs in an `||` list, so `errexit` is off inside it; when `chmod` fails (a readable `hosts.yml` the user does not own) the function continues and returns success, and `make gh-auth` exits 0 with the file still exposed. Make both `chmod` calls explicit failures (`chmod 600 … || { message; return 1; }`) so the store counts as failed; test the case with a fake `chmod`-resistant file (or a fake `chmod` on PATH) and assert exit 1 and the message.
2. **Negative-test transcript (P3, validation `:1191`).** The round-1 regression transcript shows `FAILED (failures=4)` followed by `exit=0`; paste the wrapper command that was actually run and the test process's own exit status, separately.

Then push, CI, Bot wait on the final head, `AGMSG-RESULT v1 … round=2`. No `make update`.
