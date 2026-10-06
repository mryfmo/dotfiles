# AGMSG-TASK dotfiles-T110-gh-auth-file-storage-a01

Drafted 2026-10-06 07:00Z by the orchestrator seat. Defect found while answering "did everything complete": T108's `scripts/gh-auth.sh` logs in with gh's default storage, which on a Linux host with a running Secret Service is the keyring. Verified from inside the Claude Bash sandbox on spark-9e8d (`gh auth status`): the file-stored account works, the keyring-stored account reports `Failed to log in … (default)`, because the sandbox denies unix sockets and so the D-Bus keyring. Today every seat works only because the active account's token still sits in gh's plain-text `hosts.yml` from an earlier login; a fresh machine set up with `make gh-auth` would leave the Claude worker seats (and the orchestrator's sandboxed Bash) without `gh`. The operator's decision A (design report §12, §16) is file storage. Kind: shell script, doctor, README, tests; Claude seat allowed. Dispatched to `claude-standard-dot-a005` (worker-c, wT:p2).

## Objective

1. `scripts/gh-auth.sh`: `gh auth login --hostname github.com --git-protocol https --insecure-storage`, then `chmod 600` on `$(gh's config dir)/hosts.yml` (`${GH_CONFIG_DIR:-${XDG_CONFIG_HOME:-$HOME/.config}/gh}`), failing the step with a message if the chmod fails (the T103 `secure_hosts_file` form). Header comment: file storage is deliberate because the Claude sandbox cannot reach the OS keyring; the file is user-owned 0600.
2. Doctor (`scripts/check-agent-runtime.py` GitHub login finding): when the active login's storage is the keyring (the `gh auth status` text names `(keyring)` for it, or its `hosts.yml` has no `oauth_token` for that user), WARN `GitHub login is stored in the OS keyring, which the Claude sandbox cannot reach; run make gh-auth to store it in gh's file` ; when `hosts.yml` exists with a token, check mode 0600 (WARN with the `make gh-auth` hint otherwise). Keep the existing one-login check.
3. README GitHub section: one sentence restoring the reason (the Claude Linux sandbox cannot reach the host keyring, so the login lives in gh's 0600 file; a lost machine costs one revocation).
4. Tests: `tests/unit/test_gh_auth.py` (login call carries `--insecure-storage`; chmod to 0600; failing chmod fails the step), doctor tests for the keyring-only and the wrong-mode cases; `make unit-test`, validator rc=0, shellcheck, prettier.

Forbidden: anything else; `make update`; thread resolution; printing any credential.

[memory:decision] dotfiles-T110 (orchestrator 2026-10-06): `make gh-auth` stores the login in gh's 0600 file (`--insecure-storage`) because the Claude sandbox cannot reach the OS keyring; the doctor warns when the active login is keyring-only.

## Repo / branch

worker-c; `git fetch origin`; `git switch -c fix/gh-auth-file-storage --no-track origin/main` (main at 46002810 or later); verify task_rev.

## Allowed files

`scripts/gh-auth.sh`, `scripts/check-agent-runtime.py`, `README.md` (one sentence), `tests/unit/test_gh_auth.py`, `tests/unit/test_check_agent_runtime.py`. Artifacts at the standard seven `dotfiles-T110-gh-auth-file-storage-a01` paths in the main checkout (Claude seat), masked.

## Validation commands (paste verbatim output, whole)

```
bash -n scripts/gh-auth.sh; echo "rc=$?"
shellcheck scripts/gh-auth.sh; echo "rc=$?"
uv run --no-project python -m unittest tests.unit.test_gh_auth tests.unit.test_check_agent_runtime 2>&1 | tail -3
make unit-test 2>&1 | tail -3
uv run --no-project --with pyyaml scripts/validate-agent-assets.py; echo "rc=$?"
mise x node npm:prettier -- prettier --check README.md 2>&1 | tail -2
gh pr checks <pr>
```

## Completion

PR to `main` (English, attribution footer), CI green, Bot wait per the SKILL, artifacts, the CompactionDB `memory add` of the decision line, `AGMSG-RESULT v1 task_id=dotfiles-T110` via `agmsg-dispatch dotfiles claude-standard-dot-a005 claude-remediation-dot wT:p1 "<single line>"`. max_turns=12.

## Revise round 1 (orchestrator, 2026-10-06 09:08Z) — audit of 80cc3e3d: `incorrect` (2 P2, 1 P3; one P2 is the orchestrator's)

1. **Doctor coverage (P2, `check-agent-runtime.py:627`).** The storage and mode checks run only when exactly one account exists and it authenticates, so two accounts (today's state on spark) suppress the keyring warning and a 0644 token file goes unchecked, and an authentication error skips the mode check. Check the active login's storage (tokenSource) and the file's mode independently of the one-login count and of the auth state, and keep the one-login warning as a separate finding; tests for "two accounts, active one in the keyring", "two accounts, 0644 file", and "auth error, 0644 file".
2. **Bot-wait evidence (P3, validation `:83`).** The 15-minute wait shows a label and empty results; paste the actual polling command and its elapsed-time output (or the loop's final iteration) for the final head.
3. (Orchestrator's, no action for you.) The sweep JSON was taken before the orchestrator resolved the Bot thread; it is re-swept after your push.

Then push, CI, Bot wait on the final head, `AGMSG-RESULT v1 … round=1`. No `make update`.

## Revise round 2 (orchestrator, 2026-10-06 09:40Z) — audit of 449fa66d: `incorrect` (1 P2, 1 P3)

1. **Mode check must not depend on `tokenSource` (P2, `check-agent-runtime.py:642`).** gh may report a keyring source for an account whose `hosts.yml` still holds a token (an inactive account with both), so a 0644 token file gets no `stat`. Check the configured file directly: `${GH_CONFIG_DIR:-${XDG_CONFIG_HOME:-$HOME/.config}/gh}/hosts.yml`, when it exists, must be a user-owned regular file with mode 0600, independent of what gh reports; keep the tokenSource-based keyring warning. Regression test: active account keyring-sourced, inactive account file-sourced, file at 0644 → the mode WARN appears.
2. **Evidence (P3, validation `:139`, report `:7`, `:45`).** Replace the elided live-verification command with the exact command and output, and paste the `sha256sum` and `crit status --json` outputs the report claims (or drop the claims).

Then push, CI, Bot wait on the final head, `AGMSG-RESULT v1 … round=2`. No `make update`.

## Revise round 3 (orchestrator, 2026-10-06 10:12Z) — audit of 1d4d2e44: `incorrect` (1 P2)

1. **File check must run even when `gh auth status` fails (P2, `check-agent-runtime.py:628`).** A timeout, a missing `gh` or invalid JSON returns before the configured `hosts.yml` is checked. Restructure so the function collects the status-derived warnings (gh missing/failed, count, keyring) and then always runs the file check (`lstat` of the configured `hosts.yml`: regular file, owned by the user, mode 0600, with the `make gh-auth` hint), returning the combined list. Regression test: `gh` missing or timing out plus a 0644 file → both warnings. **Boundary:** with this the finding is independent of gh in every path; no further decomposition is requested.

Then push, CI, Bot wait on the final head, `AGMSG-RESULT v1 … round=3`. No `make update`.

### PONG decision 1 (orchestrator, 2026-10-06 10:45Z) — audit of a431fd46: one artifact correction, no push

No code finding. The sandbox record claims a Ruff run that the validation file does not show. Either append the exact Ruff command and its verbatim output to the validation file or remove the claim from the sandbox record; re-mask; answer `AGMSG-PONG v1 task_id=dotfiles-T110 status=corrected …`. No push; the head stays a431fd46.
