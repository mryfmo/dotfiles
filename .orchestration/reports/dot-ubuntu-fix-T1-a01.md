# dot-ubuntu-fix-T1-a01 report

status: ready_for_review
cost: n/a

## Result

- F1: Removed interactive `gh auth login` from bootstrap. Unauthenticated applies warn, return success, and skip extension installation.
- F2: [memory:decision] Pinned mise v2026.9.12. In a credential-free Ubuntu arm64 scratch user, the unchanged lock installed uv/yazi GNU artifacts and resolved both through `.mise-bins`; uv and yazi executed successfully.
- F3: Removed unused `busybox` from Ubuntu dependencies and updated package tests.
- F4: Preserved an existing `LANG`, generated both English and Japanese locales for Ubuntu client/server, installed Japanese language/font/IME packages on clients, and documented Mozc input-source setup.
- F5: Skipped age passphrase decryption when stdin is not a TTY while preserving the interactive path.
- F6: Added GitHub's published Ed25519 host key idempotently to the user's `known_hosts`; the pinned fingerprint is documented in the script.
- F7: Documented age and GitHub authentication follow-up behavior in Setup.

## Revision: Docker keyring rerun

- [memory:decision] Added `gpg --batch --yes` to Docker's apt-key dearmor pipeline so an existing `/etc/apt/keyrings/docker.gpg` is replaced without `/dev/tty` interaction.
- Added a focused bats case that calls `setup_repository` twice and requires both GPG invocations to carry the non-interactive overwrite flags.
- Direct two-run mock, bash syntax, mise-managed shellcheck, and mise-managed shfmt all pass. Local bats remains unrun by policy.

## Tests and validation

- Updated bats coverage but did not run bats locally, as required by repository policy.
- Passed bash syntax, mise-managed shellcheck/shfmt, rendered chezmoi template checks, direct behavior checks, `tests.unit.test_supply_chain_policy`, and `git diff --check`.
- Captured F2 before/after command output in the validation artifact.
- The broader local Python unit discovery also exited successfully; existing expected-error and ResourceWarning output was unrelated to this task.
- Completed finding-free Crit data self-reviews with resolved records `r_1f790a` and revision-specific `r_13a66b`; the agent review gate passed.

## Files

- Product/docs: `README.md`, `install/**`, `home/.chezmoiscripts/**`, `home/dot_config/sheldon/plugin_sources/common.toml`.
- Tests: `tests/install/**`, `tests/unit/test_supply_chain_policy.py`.
- No `home/dot_mise/mise.lock` change was necessary.

## CompactionDB

- `python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'dot-ubuntu-fix-T1-a01: Pin mise v2026.9.12; fresh Ubuntu arm64 installs resolve the unchanged locked uv/yazi GNU artifacts through .mise-bins.'` → `7b773deb-b084-420e-81d2-40e4ba7134d9`
- `python3 .claude/hooks/contextdb_cli.py memory add --kind failure --scope project --content 'dot-ubuntu-fix-T1-a01: HOME override under sudo -i did not isolate mise global config; use a credential-free scratch user with a minimal config for backend validation.'` → `6cc64147-8c39-4f86-9d52-2a735213aa25`
- `python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'dot-ubuntu-fix-T1-a01 revise: Docker apt keyring replacement must invoke gpg with --batch --yes so reruns never prompt on /dev/tty when docker.gpg already exists.'` → `096e1f34-f289-46ca-8c60-e5dea660a1ad`

## Constraints honored

- No commit or push.
- No local bats execution.
- VM work used only `limactl shell adh-test`; no credentials were copied.
- Temporary VM scratch user and temporary validation directories were removed.
