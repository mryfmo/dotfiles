# AGMSG-TASK dotfiles-T70-make-update-unattended-a01

Drafted 2026-10-04 by the orchestrator seat from the approved correction plan (Phase 3, dotfiles-T70). Pulled forward because it is independent of every in-flight task (T64 herdr-agents/README/SKILL, T65 stop-gate, T62 withdrawn) and its files are disjoint from them. Worker: the identity named in the dispatch, in its own worktree.

## Objective

Principle 8: the lifecycle converges unattended. `make update` must never prompt and must not fail because Herdr is absent; `make upgrade` must keep mise at the pinned version.

1. `Makefile` `update` target (lines ~72-75, 79-82, 101 only): when `herdr status server --json` fails, parses oddly or reports an unknown status, print `Herdr server unreachable; skipping config reload.` to stderr and continue (exit 0 path), instead of `exit 1`. Keep the existing `protocol_mismatch` handling and the `not_running`/absent skips. Update `tests/install/common/lifecycle.bats` (around lines 168, 174) which pin the old failures.
2. `install/ubuntu/common/apparmor_userns.sh` `install_profile`: guard every `sudo` with `-n` and a non-fatal fallback: `sudo -n true 2>/dev/null || { echo "apparmor bwrap-userns profile pending: run 'sudo -v && make update'" >&2; return 0; }`, then `sudo -n install …` and `sudo -n apparmor_parser …` (expect 3 `sudo -n` occurrences). `scripts/check-tools.sh`: one `warn_optional` when the userns restriction is 1, `bwrap` is present and `/etc/apparmor.d/bwrap-userns` is absent, naming the same `sudo -v && make update` remedy. Any test that pins the old apparmor script text.
3. `scripts/upgrade-tools.sh` (~170-181): `mise self-update --yes` → `mise self-update --yes "$(asset_manifest_pin mise "${repo_root}")"` (the helper exists around line 592; verify its output is the `v`-prefixed or bare form `mise self-update` accepts, and strip accordingly). Update `tests/unit/test_runtime_health.py` upgrade tests that pin the old command.
4. Definitions to write as a comment block at the top of the `update` target (short): **operator phase** (interactive, once per machine) = `./setup.sh` (chezmoi init prompts, age passphrase, sudo keepalive, macOS CLT `read`, Ubuntu `chsh`, SSH/gh/codex logins, `run_once_*`) plus `sudo -v` right before `make update` when the pulled diff touches `install/**` or `.chezmoiscripts/**`; **unattended `make update`** = no prompt ever. README wording is T83's.

[memory:decision] dotfiles-T70 (operator 2026-10-03): `make update` converges unattended: Herdr unreachable is a skipped reload, apparmor profile installation uses `sudo -n` with a doctor warning instead of a password prompt, and `make upgrade` keeps mise at the manifest pin; interactive steps belong to the operator phase (`./setup.sh`, `sudo -v` before `make update` when installers changed).

## Repo / branch

- Work ONLY in your own worktree. `git fetch origin`; `git switch -c fix/make-update-unattended origin/main`. Verify the dispatched task_rev; else stop and PONG blocked.
- Strict status checks: if `main` moves, `gh pr update-branch <pr>` and wait for CI again before RESULT.

## Allowed files

- `Makefile` (the `update` target lines named above and the comment block), `tests/install/common/lifecycle.bats`
- `install/ubuntu/common/apparmor_userns.sh`, `scripts/check-tools.sh`, and bats/unit tests that pin their text (name them)
- `scripts/upgrade-tools.sh` (the mise self-update line), `tests/unit/test_runtime_health.py` (upgrade tests)
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dotfiles-T70-make-update-unattended-a01.md` (main checkout)

## Forbidden actions

- Pin values; new make targets; `README.md`; `home/**`; `herdr-agents`; running `make update`/`make upgrade`/`make apply` on this machine (operator lifecycle; the live check below is the operator's); local bats; merging; force push; pushing `main`.

## Validation commands (paste verbatim output)

```
git diff origin/main --stat
grep -c 'sudo -n' install/ubuntu/common/apparmor_userns.sh            # expect 3
grep -n 'mise self-update' scripts/upgrade-tools.sh                      # pinned form only
grep -n 'Herdr server unreachable' Makefile
bash -n install/ubuntu/common/apparmor_userns.sh scripts/check-tools.sh scripts/upgrade-tools.sh; shellcheck -x install/ubuntu/common/apparmor_userns.sh scripts/check-tools.sh
mise x shfmt -- shfmt -i 4 -sr -d install/ubuntu/common/apparmor_userns.sh scripts/check-tools.sh scripts/upgrade-tools.sh
make -n update 2>&1 | head -40      # dry run shows the new branch; no execution
make unit-test
make validate-agent-assets
gh pr checks <pr-number>             # lifecycle.bats runs in CI
gh api repos/mryfmo/dotfiles/pulls/<pr-number> --jq '.mergeable_state'
```

Live acceptance (operator, after merge and `make update`): `sudo -K; script -q /dev/null make update` exits 0 with no "password" line; `herdr server stop; make update` exits 0.

## Completion

1. PR to `main`, English title/description ending with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. CI green on the final head, branch up to date.
2. After the final push: `gh pr checks <pr> --watch`; wait (≤15 min) for the Codex Bot review of that head; fix P0/P1 inline findings and repeat; do not resolve threads.
3. Artifacts at the exact expected paths; validation with verbatim outputs, PR number, head SHA.
4. CompactionDB `memory add --kind decision --scope project` with the `[memory:decision]` text from the main checkout; paste command and output.
5. `AGMSG-RESULT v1` via `agmsg-dispatch dotfiles <your identity> claude-remediation-dot wT:p1 "<single line>"` (outside the sandbox). `cost:` line. max_turns=30.

## PONG decision 1 (2026-10-03T23:07Z, two questions)

1. **Remedy text.** Correct observation: `run_onchange_after_07` runs the script through chezmoi, which records the run on exit 0, so after an unattended `sudo -n` skip a later `sudo -v && make update` does not rerun it (identical content). Use the standalone form everywhere the remedy is printed: `sudo -v && bash install/ubuntu/common/apparmor_userns.sh`. No `home/**` change, no rerun marker.
2. **check-tools.sh.** Do not add a duplicate `warn_optional`. The existing REQUIRED failure for "profile missing while the bwrap probe fails" is the right severity (the Claude sandbox cannot run without the profile, so `make doctor` failing is the true state); only replace its stale remedy text ("chezmoi apply installs it") with the standalone command from item 1. Keep `test_apparmor_userns` pins at req=1 opt=0, updating only the text they assert. The plan's "one warn_optional" line is superseded by this decision.

## Revise round 1 (2026-10-03T23:34Z RESULT on 229a2ec1): README passages are in scope

The two Codex P2s are correct about README drift (`README.md:177-180` says an ambiguous Herdr status fails `make update`; `README.md:295-300` says `chezmoi apply` installs the AppArmor profile and `make doctor` confirms it). A Bot finding is fixed at its root in the PR that caused it, not deferred, so `README.md` is added to the allowed files for exactly those two passages: describe the warning-and-skip behaviour for an unreachable Herdr, and the pending-profile state with the manual remedy `sudo -v && bash install/ubuntu/common/apparmor_userns.sh`. Keep the paragraphs short; `prettier --check README.md` must pass. One commit; push; wait for the Codex review of the new head; new RESULT; do not resolve threads.
