# AGMSG-TASK dotfiles-T74-bootstrap-dead-code-a01

Drafted 2026-10-04 by the orchestrator seat from the approved correction plan (Phase 4, dotfiles-T74). No dependency. Queued for the next free worker; its files are disjoint from every in-flight task (T65 `scripts/agent-stop-gate.sh`, T68 `scripts/require-crit-review.py`, T88 SKILL/rule, T91 `scripts/validate-agent-assets.py`).

## Objective

Principle 9: delete bootstrap code that nothing runs. Every item below was traced by the orchestrator on `main` 138e6a72; re-verify each `grep` before deleting and report any reference you find instead of deleting around it.

1. **`install/macos/arm64/run.sh`:** delete. It only echoes its own path; nothing includes it (`grep -rn 'arm64/run' home install setup.sh Makefile .github tests` → only itself). `install/macos/arm64/prepare_arm64_system.sh` stays (included by `home/.chezmoiscripts/macos/run_once_before_01-prepare-system.sh.tmpl`).
2. **`Makefile` `init` (lines 34-41):** reduce to `chezmoi init --apply --verbose`; the `chezmoi-private init … || echo Warning` branch and its else-echo go. `tests/install/common/lifecycle.bats:235-240` ("Makefile skips private init when chezmoi-private is unavailable") is replaced by one test that `make -n init` prints exactly the chezmoi line and nothing about private. The `update` target's private handling (lifecycle.bats:208) is untouched.
3. **`setup.sh`:** delete `get_system_from_chezmoi` (369-373), `restart_shell_system` (375-391), `restart_shell` (393-401) and the commented call at 408 (`# restart_shell # Disabled …`). `grep -n 'restart_shell\|get_system_from_chezmoi' setup.sh` → nothing afterwards. Keep `main`'s two live calls.
4. **Empty chezmoiexternal templates:** delete `home/.chezmoitemplates/chezmoiexternal.d/macos.yaml.tmpl` and `ubuntu.yaml.tmpl` (both 0 bytes) and reduce `home/.chezmoiexternal.yaml.tmpl` to the `common.yaml.tmpl` include alone (the OS `fail` branch goes with the empty includes). `.github/workflows/test.yaml:336-337` still removes the fixture's `.chezmoiexternal.yaml.tmpl` and `chezmoiexternal.d/`; keep both lines, they stay valid.
5. **Nix:** delete `flake.nix`, `flake.lock`, `nix/**`. In `.github/workflows/test.yaml` delete the `should_nix` output (line 21), its filter block (80-84) and the `nix` job (415-437). In `tests/unit/test_supply_chain_policy.py` delete `test_nix_inputs_lock_and_ci_use_2605` (460-473) and any now-unused import. `docs/plans/nix-first-architecture.md`, `docs/plans/nix-migration.md` and `plans/004-harden-and-lock-the-supply-chain.md` mention nix: do not edit them (T78/T83 own prose); list the stale sentences in the report.

Forbidden: `Dockerfile` and the docker target (T72); any pin value; README and the plan documents above; `install/macos/arm64/prepare_arm64_system.sh`; `home/**` beyond the two template deletions and the one include change.

[memory:decision] dotfiles-T74 (operator 2026-10-03): the unused bootstrap paths are deleted: `install/macos/arm64/run.sh`, the `make init` private-init branch, setup.sh's disabled `restart_shell` family, the empty macOS/Ubuntu chezmoiexternal templates, and the whole nix flake with its CI job and test; bootstrap is `./setup.sh` + chezmoi only.

## Repo / branch

- Work ONLY in your own worktree. `git fetch origin`; `git switch -c chore/bootstrap-dead-code origin/main` (138e6a72 or later). Verify the dispatched task_rev; else stop and PONG blocked.
- Strict status checks: if `main` moves, `gh pr update-branch <pr>` and wait for CI again before RESULT.

## Allowed files

- `install/macos/arm64/run.sh` (delete), `Makefile`, `tests/install/common/lifecycle.bats`, `setup.sh`, `home/.chezmoiexternal.yaml.tmpl`, `home/.chezmoitemplates/chezmoiexternal.d/macos.yaml.tmpl` (delete), `home/.chezmoitemplates/chezmoiexternal.d/ubuntu.yaml.tmpl` (delete), `flake.nix` (delete), `flake.lock` (delete), `nix/**` (delete), `.github/workflows/test.yaml`, `tests/unit/test_supply_chain_policy.py`
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dotfiles-T74-bootstrap-dead-code-a01.md` (main checkout)

## Validation commands (paste verbatim output)

```
git diff origin/main --stat
git ls-files | grep -E '^(flake\.|nix/|install/macos/arm64/run\.sh|home/\.chezmoitemplates/chezmoiexternal\.d/(macos|ubuntu))' ; echo "rc=$?"
grep -rn "restart_shell\|chezmoi-private init\|should_nix\|get_system_from_chezmoi" setup.sh Makefile .github ; echo "rc=$?"
grep -rn 'arm64/run' home install setup.sh Makefile .github tests ; echo "rc=$?"
bash -n setup.sh
chezmoi execute-template --init --promptString email=ci@example.invalid --promptChoice system=client < home/.chezmoiexternal.yaml.tmpl | head -5
make unit-test
make validate-agent-assets
mise x node npm:prettier -- prettier --check .github/workflows/test.yaml
gh pr checks <pr-number>
gh api repos/mryfmo/dotfiles/pulls/<pr-number> --jq '.mergeable_state'
```

(The `chezmoi execute-template` flags are a starting point: use whatever renders the template with your local chezmoi config; paste what you ran.) `bats` runs in CI only.

## Completion

1. PR to `main`, English title/description ending with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. CI green on the final head (the `nix` job no longer exists, so the status-check list in the ruleset is unaffected: it was never a required context), branch up to date.
2. After the final push: `gh pr checks <pr> --watch`; wait (≤15 min) for the Codex Bot on that head by listing `gh api repos/mryfmo/dotfiles/pulls/<pr>/reviews --jq '.[]|select(.user.type=="Bot")|[.commit_id,.submitted_at]|@tsv'`; fix P0/P1 inline findings and repeat; close your crit server if Plan Mode opened one; do not resolve threads. The RESULT names every unresolved thread with `fixed:<sha>` or a proposed `not-applicable:<reason>`.
3. Artifacts at the exact expected paths; validation with verbatim outputs, PR number, head SHA.
4. CompactionDB `memory add --kind decision --scope project` with the `[memory:decision]` text from the main checkout; paste command and output.
5. `AGMSG-RESULT v1` via `agmsg-dispatch dotfiles <your identity> claude-remediation-dot wT:p1 "<single line>"` (outside the sandbox). `cost:` line. max_turns=30.

## Dispatch

- 2026-10-04 03:20Z to `claude-standard-dot-a005` (worker-c, wT:p2) right after its T91 RESULT. T91 acceptance is pending: keep `fix/secret-scan-sk-boundary` (PR #245) in worker-c untouched and branch from `origin/main` (138e6a72 or later).

### Addendum 1 (orchestrator, 2026-10-04 03:40Z) — why item 2 is dead, and what to verify

`make init`'s private branch duplicates the chezmoi-managed bootstrap: `chezmoi init --apply` runs `home/.chezmoiscripts/common/run_once_after_01-setup-chezmoi-private.sh.tmpl`, which includes `install/common/chezmoi_private.sh` and initializes `mryfmo/dotfiles-private` when the `.chezmoi.yaml.tmpl` prompt `usePrivate` is true. `setup.sh` never calls `chezmoi-private`, and nothing in the repository calls `make init` (README:640 only lists it among guarded targets). Before deleting, confirm all three facts with `grep -rn chezmoi_private home/.chezmoiscripts`, `grep -n chezmoi-private setup.sh ; echo rc=$?` and `grep -rn 'make init' . --exclude-dir=.git --exclude-dir=.orchestration --exclude-dir=.agents --exclude-dir=.ua` (expect only README:640), paste them, and PONG blocked if any of them disagrees. The replacement lifecycle test asserts `make -n init` prints exactly the one `chezmoi init --apply --verbose` line.

### PONG decision 1 (orchestrator, 2026-10-04 04:00Z)

Proceed with the deletion as pushed (2487b05a). The addendum's third grep was the orchestrator's wording error: README:640 lists the target as "init" inside "`make setup`, `init`, `update`", so `grep 'make init'` cannot match it, and `home/dot_codex/rules/default.rules:172` is the T63 forbidden-rule example that stops agents from running `make init`, not a caller. The substance the addendum asked for holds: the private layer is initialized by the run_once script, `setup.sh` never calls `chezmoi-private`, and nothing calls `make init`. Keeping a platform guard in the chezmoiexternal template (c0ea3e7f) is accepted as a deviation from item 4; describe it in the report. The nix-docs P2 is `not-applicable` as proposed (T78/T83 own that prose); the orchestrator replies on the thread.
