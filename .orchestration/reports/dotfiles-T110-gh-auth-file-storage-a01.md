# Report: dotfiles-T110-gh-auth-file-storage-a01

> **Needs an orchestrator/operator decision: Codex Bot P1 thread `4193168336` is not fixed.** Fixing it would reverse the task's objective, so it is not a worker decision. The Bot's security review of `04e143e2` says `--insecure-storage` puts the machine token in `~/.config/gh/hosts.yml`, which a same-UID, prompt-injected sandboxed worker can read and use against `api.github.com`; mode 0600 excludes only other UIDs. **That technical claim is accurate.** The task's premise is the other side of the same fact: a file-stored token is what lets sandboxed seats run `gh` at all, and on this host the active token was already file-stored before this PR (validation file, live probe). Proposed disposition: `not-applicable: operator decision A (design report §12, §16) chose gh's 0600 file over the keyring so sandboxed seats can use gh; the same-UID readability is the accepted trade-off`. I did not reply to, react to or resolve the thread.

- **PR:** #297, branch `fix/gh-auth-file-storage` from `origin/main` `46002810`.
- **Final head:** `80cc3e3dfc6fd0e44b50c07f22db7bc50bbe4415`, in two commits: `04e143e2` (the change) and `80cc3e3d` (doctor ordering fix from the worker review).
- **task_rev:** `sha256:353b14a2d67de2103d6a3896c9bf873c0db6af44cb15d13773fddf1ed5d27e34`, verified with `sha256sum` before starting.
- **Kind:** Claude seat. Only the five allowed files changed. Claude's permission, sandbox and hook blocks and permgate are untouched.

## What changed

1. **`scripts/gh-auth.sh`**
   - It logs in with `gh auth login --hostname github.com --git-protocol https --insecure-storage`.
   - Then `secure_hosts_file` (the T103 form) runs `chmod 600` on `${GH_CONFIG_DIR:-${XDG_CONFIG_HOME:-$HOME/.config}/gh}/hosts.yml`. If the chmod fails, the step prints `cannot set …/hosts.yml to mode 0600; make it yours, then run "make gh-auth"` and exits 1.
   - The header explains that file storage is deliberate.
   - **Deliberate addition beyond the literal objective:** the skip test is now "the active working login's `tokenSource` is a `hosts.yml`", read with `gh auth status --active --json hosts --jq …`. The old test was a bare `gh auth status` success. Without this change the doctor's new "run make gh-auth" hint for a keyring login would lead nowhere, because `make gh-auth` would skip. Behaviour now:
     - **Keyring login:** the step names the keyring as the reason. Without a terminal it exits 1. On a terminal it logs in again into the file. gh prefers the file token over the keyring, so the old keyring entry is never used again.
     - **File login:** the step only sets the file mode.
2. **`scripts/check-agent-runtime.py` (`gh_login_findings`)**
   - **Keyring check.** When gh holds one account and its `tokenSource` does not end in `hosts.yml`, the finding is `WARN: GitHub login is stored in the OS keyring, which the Claude sandbox cannot reach; run make gh-auth to store it in gh's file`. This check runs before the working count.
   - **Mode check.** When the token's `hosts.yml` mode is not 0600, the finding is `WARN: GitHub login: <path> has mode 0644, not 0600; run make gh-auth`. An unreadable file warns too.
   - **One-login check.** Its messages are byte-identical to before.
   - **Discriminator: the task text and the live output differ.** The task expected gh to name `(keyring)`. Inside the sandbox on this host, gh 2.101.0 shows a keyring login as `tokenSource: "default"` with `state: "error"`, as the validation file's live probe shows for `mryfmo`. Outside the sandbox gh names it `keyring`. So the check reads "not a `hosts.yml` path", which covers both forms, and it never opens `hosts.yml`.
   - **Ordering fix (`80cc3e3d`, worker-review P2).** In `04e143e2` the working count ran first. That turned the sandboxed keyring case into "0 working of 1 logins; … gh auth logout", which points the operator at the wrong fix.
   - **`CLICOLOR_FORCE` is stripped from gh's environment. This is beyond the literal objective, but inside the allowed file and necessary.** This host exports `CLICOLOR_FORCE=1`, which makes gh colour its `--json` output even through a pipe. Before the strip, the doctor's JSON parse failed and it reported "gh auth status failed". Validated by running the real function on this host: `gh holds 1 working of 2 logins …`, which is the true state, since this host holds two accounts.
3. **README:** in the login-step bullet, the "default storage: the OS keyring where present" sentence becomes one sentence: the step logs in only when gh holds no working login in its `hosts.yml`, and it stores the login there (`--insecure-storage`, mode 0600) because the Claude Linux sandbox cannot reach the host keyring. The "lost machine costs one revocation" clause already sits in the next bullet ("Where credentials live"), so I did not repeat it.
4. **Tests**
   - **`test_gh_auth.py`:** the login call carries `--insecure-storage` and leaves hosts.yml at 0600. A working file login is skipped, but its file is still set to 0600. A working keyring login exits 1 without a terminal and is logged in again on one. A fake failing `chmod` fails the step with the message.
   - **`test_check_agent_runtime.py`:** two keyring cases (`keyring` with state success, and `default` with state error), the 0644 mode warning, the forced-colour case, and `tokenSource` fixtures for the existing cases.

## Operator-visible impact (AGENTS.md "Dotfiles safety")

- **Next `make gh-auth` or `./setup.sh` from a terminal:** a machine whose working login is in the keyring gets one device-code login, which moves it into gh's 0600 file.
- **Headless run:** the same machine now exits 1 with the keyring reason, where it used to skip.
- **`make doctor`:** warns until the login is moved.
- **Credential location:** the token lives in a plaintext, user-owned 0600 file. This is the subject of the P1 above.

## Review and feedback

- **CI:** all checks pass on `80cc3e3d` (`gh pr checks 297` in the validation file).
- **Codex Bot:**
  - **`04e143e2`:** one review, with the P1 thread `4193168336` on `scripts/gh-auth.sh:64` (see the top of this report). The review body itself carries no P-badge.
  - **`80cc3e3d`:** `bot: none` after the 15-minute wait. The thread's comment `commit_id` moves to the new head, so the orchestrator's sweep will still see it.
- **Thread dispositions (proposed; the worker resolves none):** `4193168336`: not-applicable. The reason, which needs the orchestrator's or operator's decision, is at the top of this report.
- **Worker review:** `crit status --json` reported no review file, so an independent read-only subagent review is saved as `…-worker-crit.json`, with a receipt.
  - **P2 (doctor ordering):** fixed in `80cc3e3d`.
  - **P3 (operator impact):** addressed in the PR body and above.
  - **P3s not applicable:** the `--active` flag was verified live; the leftover keyring entry is never used.
  - **Follow-up candidate for the orchestrator:** README lines ~402-404 and ~435 still say `gh` reads its token from the keyring over D-Bus and so fails inside the sandbox. ~1225-1228 says a Claude seat runs `gh` outside the sandbox. The `make doctor` bullet does not list the two new warnings. The one-sentence limit kept all of these out of scope. With a file-stored login, `gh` and `git push` worked inside this seat's sandbox throughout this task.

## Durable facts

- [memory:decision] dotfiles-T110 (orchestrator 2026-10-06): `make gh-auth` stores the login in gh's 0600 file (`--insecure-storage`) because the Claude sandbox cannot reach the OS keyring; the doctor warns when the active login is keyring-only.
- [memory:failure] Inside the Claude sandbox, gh reports a keyring login as `tokenSource: "default"` with `state: "error"`, not `keyring`; a storage check must run before a working-login count.

CompactionDB (main checkout, through the permission gate), printed id `a2df6c5d-654c-43d1-96ea-97735606bd9b`:

```
cd ~/Workspace/dotfiles && uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "dotfiles-T110 (orchestrator 2026-10-06): make gh-auth stores the login in gh's 0600 file (--insecure-storage) because the Claude sandbox cannot reach the OS keyring; the doctor warns when the active login is keyring-only."
```

## Other

- **Understand-Anything hook:** did not fire in this task.
- **Plan mode:** not used, so no Crit server was started.
- **cost:** n/a. The runtime does not expose session token or cost figures to the worker.

## Revise round 1 (task_rev `sha256:84749bbfd1f7272803df5d3bd279fb24f63ae5df5380745108c4ed84f8bcdeb8`)

- **New final head:** `449fa66d78e0e809c604885bd1d525014d11d4df` (one commit on top of `80cc3e3d`; only `scripts/check-agent-runtime.py` and `tests/unit/test_check_agent_runtime.py` change).
- **Item 1, doctor coverage (P2): fixed in `449fa66d`.** `gh_login_findings` now reports each problem as its own warning:
  - **Count:** the one-login count warning is unchanged, and it is now one finding among several instead of an early return.
  - **Storage:** the keyring warning runs for the account gh marks `active`, whatever the count and its auth state.
  - **Mode:** every distinct `tokenSource` that is a `hosts.yml` path gets the 0600 check, whatever the count and auth state.
  - **`found:`:** appears only when there is no warning at all.
  - **New tests**, covering the three named cases with exact finding lists:
    - "two accounts, active one in the keyring" gives count + keyring;
    - "two accounts, 0644 file" gives count + mode;
    - "auth error, 0644 file" gives count + mode.
  - **Changed test:** the sandboxed keyring subtest (`default`, `error`) now expects count + keyring.
  - **Live check on this host** (two accounts, active one file-stored at 0600): only the count warning, which is correct.
- **Item 2, Bot-wait evidence (P3): fixed.** The validation file now pastes the polling log for the final head: each `gh api` command as run, its rc and output, and the iteration number with elapsed seconds, ending in the result line.
- **Item 3:** the orchestrator's (the sweep); no action taken.
- **Thread `4193168336`:** unchanged from round 0: not fixed, and the orchestrator decides.
- **cost:** n/a.

## Revise round 2 (task_rev `sha256:df34fdb9d6d6b27f0358c2ffa339fb3943ff8ad097c048c62ea9122387ae5418`)

- **New final head:** `1d4d2e447c26cf61319be44342946565fa7f3780` (one commit on top of `449fa66d`; only `scripts/check-agent-runtime.py` and `tests/unit/test_check_agent_runtime.py` change).
- **Item 1, mode check (P2): fixed in `1d4d2e44`.** `gh_login_findings` no longer takes the mode check from `tokenSource`. It `lstat`s the configured file, `${GH_CONFIG_DIR:-${XDG_CONFIG_HOME:-$HOME/.config}/gh}/hosts.yml`. A test can pass that directory in as the new `config_dir` parameter. When the file exists it must pass three checks, each with its own warning:
  - it is a regular file (a symlink warns `is not a regular file`);
  - the current uid owns it (`is not owned by you`);
  - its mode is 0600 (`has mode 0644, not 0600`).

  An unreadable file warns `cannot read the mode`. The `tokenSource`-based keyring warning is unchanged.
  - **New regression subtest:** "active account in the keyring, inactive one in the 0644 file" gives count + keyring + mode.
  - **New test:** a working login whose `tokenSource` names another path still gets the configured file's mode warning, and a symlinked `hosts.yml` gets the not-regular-file warning.
  - **Owner check:** not exercised by a test, because an unprivileged test cannot `chown` a file to another uid.
  - **Test isolation:** every doctor test now passes a temp `config_dir`, so the host's real gh configuration never reaches a test.
  - **Live check on this host:** only the count warning, because the real `~/.config/gh/hosts.yml` is a user-owned regular file at 0600.
- **Item 2, evidence (P3): fixed.**
  - **Exact command:** the round-2 validation section pastes the exact live-verification command (`uv run --no-project python -c '<the full snippet>'`) with its output, instead of the elided form.
  - **Fresh pastes:** it also pastes `sha256sum` of the task file at this round's rev and `crit status --json` on this branch.
  - **Round-0 claims:** the `sha256sum` that gave `353b14a2…` and the round-0 `crit status --json` are pasted verbatim from this session's transcript, because the task file has since changed.
- **Thread `4193168336`:** unchanged; the orchestrator decides.
- **cost:** n/a.

## Revise round 3 (task_rev `sha256:a383578567e7b6a7a4dfc771cfa86945da7b0441ae02bbd9a88b2aafaa91715c`)

- **New final head:** `a431fd469639378e58d528c16db78d3e47ae45a0` (one commit on top of `1d4d2e44`; only `scripts/check-agent-runtime.py` and `tests/unit/test_check_agent_runtime.py` change).
- **Item 1, file check when gh fails (P2): fixed in `a431fd46`.**
  - **New helper:** the `hosts.yml` check moves unchanged into `gh_hosts_file_findings(config_dir)`: an `lstat` of the configured file, which must be a regular file, user-owned and mode 0600, with the `make gh-auth` hint.
  - **Order:** `gh_login_findings` computes the file findings first and appends them on every path.
  - **When gh fails** (a missing gh, a timeout, or invalid JSON), the result is `[gh failed, *file findings]`.
  - **Otherwise** the result is `[count?, keyring?, *file findings]`, and `found:` appears only when that list is empty.
  - **Regression test:** three subtests, each expecting exactly the two warnings, failure plus mode, for a 0644 file:
    - gh missing (an absent path);
    - gh timing out (`subprocess.run` patched to raise `TimeoutExpired`);
    - invalid JSON (a fake gh printing `not-json`).
  - **Live check on this host:** the result is unchanged, only the count warning.
- **Boundary:** as the revise text states, the file finding now runs in every path independently of gh, and no further decomposition was made.
- **Thread `4193168336`:** unchanged; the orchestrator decides.
- **cost:** n/a.
