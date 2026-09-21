# dot-ubuntu-fix-T1-a01 validation

review_surface: crit-data
reviewer: codex
review_source: .agents/worklog/codex/review/dot-ubuntu-fix-T1-a01-crit-comments.json
review_outcome: approved
review_notes: Resolved CI-revision approval `r_0398ab` covers the one-line non-login-shell fix, related-pattern audit, and direct empty-output validation.

## Shell, shdoc-compatible scripts, and chezmoi templates

Command:

```text
bash -n <changed scripts> && mise x shellcheck -- shellcheck -x <changed scripts> && mise x shfmt -- shfmt -i 4 -sr -d <changed scripts> && chezmoi execute-template <changed templates> | bash -n/shellcheck/shfmt
```

Verbatim output:

```text
shell and template validation: OK
```

## Direct behavior validation

Command exercised unauthenticated gh behavior, a missing Japanese locale, idempotent GitHub known_hosts installation, and non-TTY age decryption.

Verbatim output:

```text
Warning: GitHub CLI is not authenticated. Run setup-gh, then rerun chezmoi apply to install extensions.
Generating ja_JP.UTF-8 ...
sudo --preserve-env=http_proxy,https_proxy,no_proxy apt-get install -y locales
sudo locale-gen ja_JP.UTF-8
sudo update-locale LANG=en_US.UTF-8
       1 /var/folders/r2/_gkywj713g54lbxkc_hv7j400000gn/T/tmp.OofiwV1Jbl/.ssh/known_hosts
behavior validation: OK
```

## Python supply-chain policy tests

Command:

```text
uv run python -m unittest tests.unit.test_supply_chain_policy
```

Verbatim output:

```text
.................
----------------------------------------------------------------------
Ran 17 tests in 0.240s

OK
```

## Git diff whitespace check

Command:

```text
git diff --check && printf 'git diff --check: OK\n'
```

Verbatim output:

```text
git diff --check: OK
```

## F2 before: existing reproduced VM state

Command:

```text
limactl shell adh-test -- sudo -i -u dotftest bash -lc 'set +e; /home/dotftest/.local/bin/mise --version; /home/dotftest/.local/bin/mise which uv; /home/dotftest/.local/bin/mise which yazi; /home/dotftest/.local/bin/mise exec -- uv --version; /home/dotftest/.local/bin/mise exec -- yazi --version; exit 0'
```

Verbatim output:

```text
2026.7.5 linux-arm64 (2026-07-09)
mise WARN  mise version 2026.9.12 available
mise WARN  To update, run mise self-update
mise ERROR uv is not a mise bin. Perhaps you need to install it first.
mise ERROR Version: 2026.7.5 linux-arm64 (2026-07-09)
mise ERROR Run with --verbose or MISE_VERBOSE=1 for more information
mise ERROR yazi is not a mise bin. Perhaps you need to install it first.
mise ERROR Version: 2026.7.5 linux-arm64 (2026-07-09)
mise ERROR Run with --verbose or MISE_VERBOSE=1 for more information
mise ERROR "uv" couldn't exec process: No such file or directory
mise ERROR Version: 2026.7.5 linux-arm64 (2026-07-09)
mise ERROR Run with --verbose or MISE_VERBOSE=1 for more information
mise ERROR "yazi" couldn't exec process: No such file or directory
mise ERROR Version: 2026.7.5 linux-arm64 (2026-07-09)
mise ERROR Run with --verbose or MISE_VERBOSE=1 for more information
```

## F2 after: changed installer in a credential-free scratch user

The command created `dotf2test`, installed the exact worktree `install/common/mise.sh`, used a two-tool config plus the repository lock, ran the checks below, and then removed the scratch user.

Verbatim output:

```text
mise WARN  No untrusted config files found.
mise by @jdx – installing 2 tools
mise ✓ yazi@26.8.15  1.1s  yazi-aarch64-unknown-linux-gnu.zip
mise ✓ uv@0.12.5     1.3s  uv-aarch64-unknown-linux-gnu.tar.gz
mise ████████████████ 2/2 · installed 2 tools in 1.3s
2026.9.12 linux-arm64 (2026-09-20)
/home/dotf2test/.local/share/mise/installs/uv/0.12.5/.mise-bins/uv
/home/dotf2test/.local/share/mise/installs/yazi/26.8.15/.mise-bins/yazi
uv 0.12.5 (aarch64-unknown-linux-gnu)
Yazi
    Version: 26.8.15 (1f3588d 2026-08-15)
    Debug  : false
    Triple : aarch64-unknown-linux-gnu (linux-aarch64)
    Rustc  : 1.97.1 (8bab26f4 2026-07-14)
```

Scratch-user cleanup output:

```text
userdel: dotf2test mail spool (/var/mail/dotf2test) not found
```

## Deliberately not run

```text
bats: not run locally (repository policy); bats files were updated for CI.
```

## CompactionDB project memories

Commands:

```text
python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'dot-ubuntu-fix-T1-a01: Pin mise v2026.9.12; fresh Ubuntu arm64 installs resolve the unchanged locked uv/yazi GNU artifacts through .mise-bins.'
python3 .claude/hooks/contextdb_cli.py memory add --kind failure --scope project --content 'dot-ubuntu-fix-T1-a01: HOME override under sudo -i did not isolate mise global config; use a credential-free scratch user with a minimal config for backend validation.'
```

Verbatim output:

```text
7b773deb-b084-420e-81d2-40e4ba7134d9
6cc64147-8c39-4f86-9d52-2a735213aa25
```

## Crit review gate

Command:

```text
AGENT_REVIEWED=1 REVIEW_EVIDENCE=.orchestration/validation/dot-ubuntu-fix-T1-a01.md make require-crit-review
```

Verbatim output:

```text
Review requirement satisfied by AGENT_REVIEWED=1 with REVIEW_EVIDENCE.
```

## Bats login-shell revision: direct non-TTY behavior

Command rendered the decrypt template, invoked it through `bash -c`, captured combined output, required it to be empty, and required no key file.

Verbatim output:

```text
decrypt non-login empty-output validation: OK
```

## Bats login-shell revision: task pattern audit and diff

Commands audited for any remaining `bash -lc` plus empty-output assertion, printed the two relevant non-login invocations, and ran `git diff --check`.

Verbatim output:

```text
76:    run env CI=false HOME="${home_dir}" bash -c "
29:    run env CALLS_PATH="${calls_path}" bash -c '
task login-shell pattern audit: OK
revision git diff --check: OK
```

## Bats login-shell revision: CompactionDB failure memory

Command:

```text
python3 .claude/hooks/contextdb_cli.py memory add --kind failure --scope project --content 'dot-ubuntu-fix-T1-a01 CI revise: bats tests that assert empty output must use bash -c, not bash -lc, because runner login profiles may emit unrelated output.'
```

Verbatim output:

```text
8c177c0d-b525-4924-8eda-f7122015172c
```

## Bats login-shell revision: review gate

Command:

```text
AGENT_REVIEWED=1 REVIEW_EVIDENCE=.orchestration/validation/dot-ubuntu-fix-T1-a01.md make require-crit-review
```

Verbatim output:

```text
Review requirement satisfied by AGENT_REVIEWED=1 with REVIEW_EVIDENCE.
```

## Docker keyring revision: static validation

Command:

```text
bash -n install/ubuntu/client/docker.sh && mise x shellcheck -- shellcheck -x install/ubuntu/client/docker.sh && mise x shfmt -- shfmt -i 4 -sr -d install/ubuntu/client/docker.sh && printf 'docker static validation: OK\n'
```

Verbatim output:

```text
docker static validation: OK
```

## Docker keyring revision: two-run behavior

Command mocked curl, dpkg, lsb_release, and sudo, then called `setup_repository` twice and inspected the GPG calls.

Verbatim output:

```text
2
gpg --batch --yes --dearmor -o /etc/apt/keyrings/docker.gpg
gpg --batch --yes --dearmor -o /etc/apt/keyrings/docker.gpg
docker rerun behavior: OK
```

## Docker keyring revision: CompactionDB decision

Command:

```text
python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'dot-ubuntu-fix-T1-a01 revise: Docker apt keyring replacement must invoke gpg with --batch --yes so reruns never prompt on /dev/tty when docker.gpg already exists.'
```

Verbatim output:

```text
096e1f34-f289-46ca-8c60-e5dea660a1ad
```

## Docker keyring revision: final diff and review gate

Commands:

```text
git diff --check && printf 'revision git diff --check: OK\n'
AGENT_REVIEWED=1 REVIEW_EVIDENCE=.orchestration/validation/dot-ubuntu-fix-T1-a01.md make require-crit-review
```

Verbatim output:

```text
revision git diff --check: OK
Review requirement satisfied by AGENT_REVIEWED=1 with REVIEW_EVIDENCE.
```
