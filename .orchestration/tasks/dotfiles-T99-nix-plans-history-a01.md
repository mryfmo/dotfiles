# AGMSG-TASK dotfiles-T99-nix-plans-history-a01

Drafted 2026-10-05 06:15Z by the orchestrator seat (dispatched to `codex-security-dot-a007`, worker-e). Follow-up to T78/T83: the two Nix-era design documents stayed in `docs/plans/` because a unit test outside T83's allowed files reads them by path. This task moves them together with that test. Kind: documentation plus one test file; no boundary source.

## Objective

1. Move `docs/plans/nix-first-architecture.md` and `docs/plans/nix-migration.md` to `docs/history/` with `git mv` (new directory). Keep their T78 "superseded" notes; add one line at the top of each: "Historical document (moved 2026-10-05, dotfiles-T99); the AWS CLI ownership statements remain current and are pinned by `tests/unit/test_aws_cli_acquisition.py`." Create `docs/history/README.md` with two sentences: what the directory holds and that nothing in it is a current plan.
2. Update `tests/unit/test_aws_cli_acquisition.py` (lines 382–399 read both files by path) to the new paths; the pinned ownership statements stay unchanged and the test stays green.
3. `plans/004-harden-and-lock-the-supply-chain.md` and `plans/README.md` stay where they are (the plans index numbers them); if `plans/004` links to either moved file, fix the link. Grep the repository (`git grep -n 'docs/plans/nix'`) for any other reference (README, mkdocs or docs workflow config, skills) and update it; if a docs build exists (`mkdocs.yml`, `.github/workflows/docs.yml`), confirm it still builds or has no nav entry for the moved files, and paste the check.
4. No other content edits. If `docs/plans/` becomes empty, leave it absent (git tracks no empty directories).

Forbidden: editing `plans/**` beyond a link fix; touching `home/**`, `scripts/**`, `install/**`, or any other test; `make update`/`apply`; thread resolution; local bats.

[memory:decision] dotfiles-T99 (orchestrator 2026-10-05): the Nix-era design documents live under `docs/history/` as historical records; `tests/unit/test_aws_cli_acquisition.py` pins their AWS CLI ownership statements at the new path; `plans/004` stays indexed in `plans/README.md`.

## Repo / branch

- Work ONLY in your own worktree (worker-e). `git fetch origin`; `git switch -c docs/nix-plans-history --no-track origin/main` (main is at 794a80db or later). Verify the dispatched task_rev against the main checkout's task file; otherwise stop and PONG blocked.

## Allowed files

- `docs/plans/nix-first-architecture.md`, `docs/plans/nix-migration.md` (moves), `docs/history/**`, `tests/unit/test_aws_cli_acquisition.py`, `plans/004-harden-and-lock-the-supply-chain.md` (link fix only), `README.md` and docs config files only for a reference fix found by the grep.
- Artifacts in your worktree at `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dotfiles-T99-nix-plans-history-a01.md` plus `.orchestration/validation/dotfiles-T99-nix-plans-history-a01-worker-crit.json` and `-worker-review-receipt.md`; the orchestrator copies them into the main checkout.

## Validation commands (paste verbatim output)

```
git diff origin/main --stat | tail -5
git ls-files docs/plans docs/history
git grep -n 'docs/plans/nix' ; echo "rc=$?"
uv run --no-project python -m unittest tests.unit.test_aws_cli_acquisition 2>&1 | tail -3
make unit-test 2>&1 | tail -3
uv run --no-project --with pyyaml scripts/validate-agent-assets.py; echo "rc=$?"
mise x node npm:prettier -- --check docs/history README.md 2>&1 | tail -3
gh pr checks <pr-number>
gh api repos/mryfmo/dotfiles/pulls/<pr-number> --jq '.mergeable_state'
```

## Completion

1. PR to `main`, English title/description ending with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. CI green on the final head, branch up to date.
2. After the final push: Bot wait per the SKILL Worker Playbook step 15 (diff head only, timestamped); fix P0/P1 inline findings; do not resolve threads.
3. Artifacts at the exact expected paths; validation with verbatim outputs, PR number, head SHA.
4. CompactionDB: say in the report that the orchestrator records the decision (Codex seat).
5. `AGMSG-RESULT v1 task_id=dotfiles-T99` via `agmsg-dispatch dotfiles codex-security-dot-a007 claude-remediation-dot wT:p1 "<single line>"`. `cost:` line. max_turns=20.
