# Report: dotfiles-T74-bootstrap-dead-code-a01

- **Worker and branch:** `claude-standard-dot-a005` in worker-c, branch `chore/bootstrap-dead-code` from `origin/main` 138e6a72.
- **task_rev:** `66b87608…`, matched.
- **PR:** #247, https://github.com/mryfmo/dotfiles/pull/247.
- **Commits:**
  - `2487b05a`: the deletions.
  - `c0ea3e7f`: platform guard kept.
- **Final head:** `c0ea3e7f`.
  - **CI:** green; 16 pass, including CodeRabbit and the `build` jobs that the Makefile path triggers, and there is no `nix` context any more.
  - **Branch:** up to date with `main` 138e6a72.
  - **Codex:** `bot: none` on `c0ea3e7f` within 15 minutes; two P2s on `2487b05a`.
  - **`mergeable_state`:** `blocked`, only by those two P2 threads (4175951414 `fixed:c0ea3e7f`; 4175951412 `not-applicable`).

## Done (each re-verified; no unexpected reference found)

1. **`install/macos/arm64/run.sh`:** deleted. `prepare_arm64_system.sh` stays.
2. **`make init`:** now `chezmoi init --apply --verbose` only. In `tests/install/common/lifecycle.bats`, "Makefile skips private init when chezmoi-private is unavailable" is replaced by "Makefile init runs only the public chezmoi init". The new test asserts `make -n init` prints exactly that line; it does locally. The `update` target's private handling and its test (`:208`) are untouched.
3. **`setup.sh`:** `get_system_from_chezmoi`, `restart_shell_system`, `restart_shell` and the commented call in `main` are deleted. `main`'s two live calls stay. `bash -n`, shellcheck and shfmt are clean.
4. **Empty chezmoiexternal templates:** `macos.yaml.tmpl` and `ubuntu.yaml.tmpl` (0 bytes) are deleted. `home/.chezmoiexternal.yaml.tmpl` drops their includes. The workflow's fixture cleanup lines (`test.yaml` `rm -f …/.chezmoiexternal.yaml.tmpl`, `rm -rf …/chezmoiexternal.d`) are kept. **Deviation, see below:** the OS `fail` branch is kept.
5. **Nix:**
   - `flake.nix`, `flake.lock` and `nix/**` (3 files) are deleted, along with the workflow's `should_nix` output, its filter block and the `nix` job.
   - `test_nix_inputs_lock_and_ci_use_2605` is deleted. `json` is still used elsewhere in `test_supply_chain_policy.py`, so the import stays.
   - No other workflow, `renovate.json` or script references nix, flakes or cachix.
   - Totals: 700 unit tests OK, and `make validate-agent-assets` in the worktree exits 0.

## Deviation: the platform guard is kept (commit `c0ea3e7f`, Codex P2 4175951414)

- **What the task said:** item 4 said "the OS `fail` branch goes with the empty includes".
- **Why I kept it:** Codex pointed out that the branch is a live guard, not dead code. Without it, on a non-Debian Linux or non-macOS host, `chezmoi apply` would render the common externals and download Spacemacs and the font archives before anything stops it. Other templates do fail on some unsupported setups (sheldon `plugins.toml.tmpl` for client systems; the Ubuntu run_once scripts for non-Ubuntu ids), but none of them clearly runs before the externals are fetched.
- **The change:** the guard stays, rewritten as a single `if not (or darwin (and linux debian))` → `fail`, now ahead of the common include. The two empty includes are still gone. The rendered output on this supported host is identical to `origin/main`, and the guard's `fail` fires when the OS test is forced false (validation file).
- **Easy to drop:** it is a separate commit. If you want the guard gone as the task text says, drop `c0ea3e7f`.

## Codex threads

| Thread | Head | Proposed disposition |
|---|---|---|
| 4175951414 P2 "Retain the external template's platform guard" | 2487b05a | `fixed:c0ea3e7f` |
| 4175951412 P2 "Update Nix documentation after deleting the flake" | 2487b05a | `not-applicable`: `docs/plans/nix-first-architecture.md` and `docs/plans/nix-migration.md` are prose owned by T78/T83, and this task forbids editing them. The stale sentences are listed below for those tasks. |

## Stale prose for T78/T83 (not edited)

- `docs/plans/nix-first-architecture.md:16, 58, 64, 70, 76`: the flake outputs, the `home-manager switch --flake .#mryfmo-linux/darwin`, `darwin-rebuild switch --flake .#mryfmo-mac` and `nix flake check` commands.
- `docs/plans/nix-migration.md:23-26, 33-34, 37, 110`: add `flake.nix` and the `nix/**` modules, `nix flake show/check`, the "CI evaluates every declared output", and the flake.lock regression procedure.
- `plans/004-harden-and-lock-the-supply-chain.md:44, 64-65, 92, 109, 371, 386-393`: Nix flake locks, the flake selecting 25.05, the Nix lock/check row, the flake files and Nix CI job, the flake.lock regeneration, and the `should_nix` gate with its adversarial check.
- `docs/verification/acceptance/005.md:12`: "the expected Nix skip". This is a historical record, so it is probably fine to leave.

## CompactionDB

```
cd ~/Workspace/dotfiles && python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'dotfiles-T74 (operator 2026-10-03): the unused bootstrap paths are deleted: `install/macos/arm64/run.sh`, the `make init` private-init branch, setup.sh'"'"'s disabled `restart_shell` family, the empty macOS/Ubuntu chezmoiexternal templates, and the whole nix flake with its CI job and test; bootstrap is `./setup.sh` + chezmoi only.'
9c4baa38-0730-4e71-b6a7-fcc6b06be80c
```

[memory:decision] dotfiles-T74 (operator 2026-10-03): the unused bootstrap paths are deleted: `install/macos/arm64/run.sh`, the `make init` private-init branch, setup.sh's disabled `restart_shell` family, the empty macOS/Ubuntu chezmoiexternal templates, and the whole nix flake with its CI job and test; bootstrap is `./setup.sh` + chezmoi only.

## Artifacts

- validation: `.orchestration/validation/dotfiles-T74-bootstrap-dead-code-a01.md`
- sandbox: `.orchestration/sandboxes/dotfiles-T74-bootstrap-dead-code-a01.md`
- learning: `.orchestration/learning/dotfiles-T74-bootstrap-dead-code-a01.md`
- autoskill: `.orchestration/autoskill/runs/dotfiles-T74-bootstrap-dead-code-a01.md`

cost: n/a (no subagents, no model-driven runs; the runtime does not expose session totals).

## Addendum 1 and PONG decision 1 (task_rev `ee21597b…`)

- **Addendum greps** (pasted in the validation file):
  - The first two agree with the addendum.
  - The third matched only `home/dot_codex/rules/default.rules:172` (the T63 forbidden-rule example) and not README:640.
  - I sent a blocked PONG at 03:19:48Z.
- **Decision 1:**
  - Proceed as pushed (`2487b05a`). The grep-3 wording was the orchestrator's error.
  - The platform-guard deviation (`c0ea3e7f`) is accepted. It is described above.
  - The nix-docs P2 4175951412 is `not-applicable`; the orchestrator replies on that thread.
