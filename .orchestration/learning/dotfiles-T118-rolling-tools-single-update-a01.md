# Learning triage: dotfiles-T118-rolling-tools-single-update-a01

These are candidates only; nothing is promoted.

1. [memory:failure] A Claude seat on macOS cannot run any mise network command inside the Seatbelt sandbox.
   - mise 2026.9.17 verifies TLS through the Security framework and fails with `OSStatus -26276`, even with the host in `allowed_domains`.
   - curl reaches the same host, and `SSL_CERT_FILE` does not help.
   - mise network probes need a Codex seat, the operator, or the orchestrator outside the sandbox.
   - Candidate for the SKILL's Worker Playbook step 4 list of known boundaries.
2. [memory:failure] `mise x …` in a worktree writes trust state under `~/.local/state/mise/trusted-configs`, which the sandbox denies.
   - `MISE_TRUSTED_CONFIG_PATHS=<main checkout>` marks the main checkout and every worktree under it as trusted, with no write.
   - Candidate for the task template's notes on validation commands, since prettier and ruff checks run through `mise x`.
3. [memory:failure] `mise settings ls --all` omits a setting that is unset and has no default (`self_update.minimum_release_age` on 2026.9.17).
   - Its absence from the listing is not evidence that the key does not exist.
   - Probe with `mise settings set <key> <value>`, using an unknown key as the control.
   - I reported the key as missing, and the independent review caught it.
   - Candidate for the validation guidance.
4. [memory:failure] Edits made by a script (`uv run python` replacements) bypass the PostToolUse formatter hook, so CI's `ruff format --check` failed twice (f999cc68, 4ab9634e).
   - Before every push, run `mise x ruff -- sh -c 'git ls-files -z "*.py" | xargs -0 ruff format --config ruff.toml --check'`, plus the same prettier check over `*.md`.
   - Candidate for the Worker Playbook's push step.
5. A task that deletes a shared artifact (here `mise.lock`, and functions in `upgrade-tools.sh`) should grep the forbidden wave-2 files for that artifact before dispatch.
   - Two T119 tests depended on what T118 removed (Amendment 1).
   - The same holds for helpers that read the deleted value: `scripts/check-statusline-tools.py` read the exact version from `config.toml` (Amendment 4).
   - Candidate for Orchestrator Playbook step 3 ("ground allowed_files"): include the forbidden files, and every reader of a changed value, in the grep.
6. With a `"latest"` request, mise answers `mise which <bin>` through the `installs/<tool>/latest` symlink, while `mise where <tool>` names the version directory.
   - Path-prefix checks must compare physical paths (`pwd -P`).
   - This applies to any CI or test check that compares a mise bin path with its install root.
7. Homebrew 7 asks for confirmation before `brew upgrade` by default ("Ask mode is the default"). Unattended callers need `HOMEBREW_NO_ASK=1` (or `--no-ask`).
8. `MISE_CEILING_PATHS` at the checkout root keeps parent `mise.toml` files out of `mise ls --current`.
   - Neither no ceiling nor a `$HOME` ceiling does that (`mise config ls` evidence, validation §5).
   - The task text offered both of those; the Codex Bot caught it.
9. In mise 2026.9.17 on macOS, moving `XDG_CONFIG_HOME` did not move mise's global config directory. The `MISE_CONFIG_DIR` pin stays only as a guard. This does not generalise and is not a rule candidate.

10. [memory:failure] Offline, `mise install --yes <tool>` on a `"latest"` request exits 1 even when the tool is installed, because it re-resolves `latest` remotely.
    - A bare `mise install --yes` exits 0 when every declared tool is installed, and 1 when one is missing.
    - `mise upgrade --yes <tool>` exits 0 offline.
    - `mise ls --current --missing` does not list a missing `latest` tool offline, so it is no gate.
    - Applies to any lifecycle step that must converge offline with `latest` requests (revise round 1, validation §12).

11. [memory:failure] make parses the Makefile before a recipe runs, so a recipe that pulls its own repository runs the pre-pull recipe.
    - The fix is structural: pull in one step, then `$(MAKE) <rest>` in a second make that reads the fetched Makefile.
    - The first run after the change still uses the old recipe, so it needs a one-time `git pull && make update`.
    - Applies to every lifecycle Makefile that updates its own checkout (revise round 2, validation §14).

12. [memory:failure] Codex execpolicy `prefix_rule` matches whole tokens, so forbidding `make update` does not cover a new target named `make update-tree`.
    - Every new host-mutating Makefile target needs its own entry in `home/dot_codex/rules/default.rules`, plus a required prefix in `tests/unit/test_codex_execpolicy.py`.
    - Verify with `codex execpolicy check --rules home/dot_codex/rules/default.rules make <target>` (revise round 3).

13. [memory:failure] A RESULT must reconcile every top-level Bot comment on the PR, not only those on the heads whose Bot wait ran.
    - Two P2 threads on b621af77 went unnamed: its Bot wait was skipped while a Codex seat worked on the same branch, and the final recheck listed them without matching them to dispositions.
    - Before sending, diff the thread ids in the recheck listing against the `threads=` field of the RESULT.
    - Candidate for Worker Playbook step 15 (revise round 4).

14. [memory:failure] `mise install --force <tool>` removes the existing install before fetching the replacement, so a failed forced reinstall leaves the tool missing.
    - Follow every forced reinstall with a required bare `mise install --yes`, which restores the missing resolved version, or fails.
    - Applies to any repair path that uses `--force` (revise round 5).
    - Better (Bot round on d0dd981d): avoid `--force` altogether. Move the install aside, install the exact version, and restore the backup on failure, so a repair that cannot download never destroys a working tool.

15. [memory:failure] Two things kept failing here: detecting a state change by comparing two points inside one process, and keeping one policy in two places.
    - The installer moved node before this script ran, and it ran under npm's 7-day gate before the script's override.
    - Record the state persistently (a marker under `$XDG_STATE_HOME`) and keep each policy in one file (`~/.npmrc` equal to mise's cooldown) (revise round 6).

16. [memory:failure] A move-aside rebuild still loses the tool when the script is interrupted between the move and the restore.
    - Set INT/TERM/EXIT traps that restore the backup right after the move, and clear them as soon as the install returns.
    - On the next run, restore a leftover backup (a SIGKILL runs no trap) instead of deleting it.
    - Test the interruption by having the fake tool signal its parent (`kill -TERM "$PPID"`): a tool that only kills itself exercises the ordinary failure branch (revise round 7).

17. [memory:failure] In a Claude Code Bash tool session, `grep` is a shell-snapshot function that runs the bundled ugrep 7.8.4 with `-G`, not `/usr/bin/grep`. ugrep reads `${...}` in a basic regex as an anchor and an interval, so such alternatives silently match nothing, and the pasted evidence then omits lines; BSD grep matches them.
    - Use `grep -nF -e <literal> -e <literal>` for code literals, or call `/usr/bin/grep` explicitly (revise round 7).

18. [memory:failure] A `cut -c1-N` at the end of an evidence script truncates commands and output silently. Paste evidence uncut and mask paths with `sed` only (revise round 7).

19. [memory:failure] A recovery step must not depend on looking up the thing it recovers.
    - After a SIGKILL the install is gone, so `mise where` fails, and a restore placed after that lookup never runs.
    - Find leftovers from a location you can compute without the tool (mise's installs directory), and restore them before any command that needs the tool (revise round 8).
    - Test the exact state the failure leaves (the directory absent), not only a convenient neighbour (a partial directory).

20. [memory:failure] Removing one `cut -c1-N` from one evidence script does not clean evidence pasted earlier through other widths.
    - List every `cut -c1-N` width the session used, and check the published file for lines of exactly those lengths before claiming the evidence is complete (revise round 8).

21. [memory:failure] A leftover scan that restores backups turns any backup surviving a successful operation into a future revert.
    - Rename the backup out of the scanned pattern before deleting it, so a failed delete leaves nothing the scan would act on. Do not just propagate the delete failure: a partly deleted backup would still be restored.
    - mise lists every directory under `installs/<tool>/` as an installed version, but ignores dot-prefixed names, so leftovers there should be dot-named (Bot round on f79d7b4e).

22. [memory:failure] `rm -rf old && mv new old` is not a replace: when `rm -rf` cannot delete everything, `mv` moves the directory *inside* the survivor.
    - Check that the target path is gone before the move, and report both paths when it is not (revise round 9).
    - Evidence scripts must print every command whose output they paste, including filters (`| grep -E …`) and second commands.

Rule candidates written: none (`learning/rule_candidates/` untouched).
