# Report: dotfiles-T108-one-login-per-machine-a01

- **PR:** #293, branch `feat/one-login-per-machine` on base `origin/main` `e0027811`.
- **Final head:** `f0a5407aadb54d00e47f2e4c9a27a180f18481f1` (revise round 1). Before that, `b66f42971e072f15c4d59bdfde3744674def6285`, built in seven commits:
  - `e7f5d1d3` herdr-agents;
  - `90961987` gate;
  - `9c550ab4` login, doctor, check-tools, manifest and renderer;
  - `14559a0e` execpolicy;
  - `668b201f` SKILL and rule;
  - `a8ebd8de` README;
  - `b66f4297` review and CI fixes.
- **task_rev:** dispatch `sha256:a7a0e451…0c177`, PONG decision 1 `sha256:14437890…6b126`.
- **Kind:** Claude seat. Claude's permission, sandbox and hook blocks and permgate are untouched.
- **First step:** the T107 branch and its uncommitted edits were discarded, as the cancellation instructed.

## What changed (decision A: every seat on a machine acts as its one GitHub account)

1. **herdr-agents.** Six pieces are removed:
   - `worker_github_config_dir`;
   - `notice_missing_worker_github_credential` and its three call sites;
   - `worker_github_shell_env`;
   - `codex_worker_github_config` (the `shell_environment_policy` override in both the pair launch and the spawn options);
   - `spawn_worker_with_github`, whose herdr adapter injected `GH_CONFIG_DIR` and empty tokens. `spawn.sh` is now called directly, with the same arguments and environment prefix.
   - the worker pane's `pane run` that unset tokens and exported the store.

   The shell-prompt wait before a worker starts stays; its refusal now reads "refusing to start the worker". Worker panes inherit the user's gh configuration like any shell.
2. **Gate.** `require-crit-review.py` loses `github_identity_errors`: the worker hosts.yml probe, the effective-rules approval and bypass checks, author ≠ merger, the current-head approval, and their notices. PR feedback, audit and crit evidence checks are unchanged. Unused imports (`shlex`, `datetime`) are removed.
3. **Manifest and renderer.** The `owner_`, `work_` and `worker_gh_config_dir` keys and their `*_GH_CONFIG_DIR` rendering are removed; `model-profiles.env` is re-rendered and `make render-check` is clean. The generator's now-unused `os` and `shlex` imports are removed.
4. **Login step.** `scripts/gh-auth-stores.sh` is renamed `scripts/gh-auth.sh` (git mv) and reduced to a single login:
   - mise shims go on PATH; a missing gh exits 1 with the hint;
   - token variables are cleared;
   - a working `gh auth status` means skip;
   - with no terminal, exit 1 with the `make gh-auth` hint;
   - otherwise `gh auth login --hostname github.com --git-protocol https` runs, with default storage and no `--insecure-storage`;
   - there is no `setup-git`.

   `make gh-auth` and `setup.sh` (`authenticate_github`) call it.
5. **Doctor and check-tools.**
   - `check-agent-runtime.py`'s three-store findings become `gh_login_findings`. Exactly one account in gh's status, and it working, gives `found: GitHub login <login> (every seat on this machine acts as it)`. Otherwise it warns with the `make gh-auth` / `gh auth logout --user` hint. Token variables are stripped from gh's environment, and the hosts.yml mode check is gone, because default storage may be the keyring.
   - `check-tools.sh` loses `check_github_identities` and its section.
6. **Codex execpolicy.** Next to the existing `gh pr merge` rule, `home/dot_codex/rules/default.rules` forbids `gh api -X PUT`, `gh api --method PUT` and `gh api graphql`, with the justification "Merging and auto-merge are the orchestrator's acceptance step; report the PR instead." It has `match`/`not_match` examples, and `gh api repos/o/r/pulls/1/reviews` and `-X GET` stay allowed.
   - **Verified with Codex itself:** `codex execpolicy check --rules … -- <command>` returns `forbidden` for the four forms, and no match for the reads.
   - **Not caught by a prefix rule:** a flag after the path, `-XPUT`, and `--method=PUT`. Both the rules comment and the README say so.
7. **SKILL and rule (PONG decision 1).**
   - Orchestrator Playbook step 10.1 loses the role-setup approval step, and step 10.4 the approval-from-another-login bullet.
   - Step 10.5 becomes `gh pr merge <pr> --squash`.
   - The REST `PUT …/merge` mentions go from the `main` bullet and the Stop checklist.
   - Worker Playbook step 4 keeps the Claude seat's three gated commands without the T90/T90b condition.
   - The rule's `main` bullet names `gh pr merge --squash`.
   - The docs test's pinned token follows.
8. **README.** The GitHub section now covers:
   - **The integrity ruleset:** one ruleset with its payload (no bypass actors, zero approvals, and why approvals cannot work under one account), and the steps to apply it, including deleting an earlier merge-control ruleset.
   - **Who merges:** the gate. Codex seats' native denial is described with its exact coverage, and the Claude seats' denial is stated as pending.
   - **The residual risk.**
   - **The single login step:** `setup.sh` / `make gh-auth`, default storage, no credentials in any repository, `make update` never prompts, no `setup-git`, and the doctor line.
   - **The Claude seat's gated `gh`/`git push`/`git fetch` on Linux.**

   Removed: the merge-control payload and activation, the T90 account separation, the three-store table, the encrypted hosts.yml sentence, the operator-verification table, the REST merge procedure, and the gate role-check text.
9. **Tests.**
   - **Removed:**
     - herdr-agents: the 4 notice tests and the 2 injection tests;
     - the gate: 6 role-gate tests and their fixture;
     - the 2 store-renderer tests;
     - the old store script tests;
     - the runtime-health role test.
   - **Inverted** (the removed names are banned from `tests/`, so these assert other traces):
     - no `pane run` carries `GH_TOKEN` and no `agent start` carries `shell_environment_policy.set.`;
     - no `tab create` has `--env GH_`, and the boot environment keeps an inherited `GH_TOKEN`;
     - the gate source has no `bypass_actors`, `required_approving_review_count` or `rulesets/`, and a populated default store triggers no `gh api` call;
     - the rendered env has no `_CONFIG_DIR=`;
     - check-tools has no role check.
   - **New:**
     - single-login script tests: skip, no terminal, pty login with default storage, missing gh, an incomplete login, the CI skip, and a fresh PATH with a mise shim;
     - doctor login tests;
     - execpolicy prefix and example tests.
   - **Updated:** the reworded refusal, the docs token, and the tool-check warning count (2 → 1).

## Review and validation

- **Independent review:** a subagent reviewed `a8ebd8de` (`-worker-crit.json` and the receipt, `review_outcome: addressed`). It found the code correct and in scope, plus 1 P2 and 7 P3.
  - **The P2:** the docs overclaimed merge denial for Claude worker seats. Fixed in `b66f4297`.
  - **The P3s:** four fixed (execpolicy coverage wording, gate-authority wording, squash-only placement, the login-failure test) and three not-applicable. The reasons are in the records.
- **CI on `a8ebd8de`:** the four `test` jobs failed in my new `test_a_missing_gh_is_reported`. CI runners have a real `gh` in `/usr/bin`, so `PATH=/usr/bin:/bin` did not make gh missing. The test now uses a PATH holding only bash (`b66f4297`).
- **Validation on `b66f4297`:**
  - `make unit-test`: 911 tests, OK (skipped=1).
  - `bash -n` and shellcheck, `make render-check`, the validator (rc=0), ruff format and prettier all pass.
  - **The task's grep:** rc=0 only because of two untracked, gitignored `__pycache__` `.pyc` files from before the rename; with `-I`, rc=1, no match. Both are pasted.
- **CI on `b66f4297`:** all 16 checks pass, and `mergeable_state` is `clean`. The watch itself ended on a network reset while three checks were pending; the state read right after is pasted.
- **Bot:** the wait on `b66f4297` found no Bot item. The first head's wait ended on the 04:17:26Z quota notice. The Codex security review of `a8ebd8d` completed with no findings. There are no Bot reviews or threads on any head.

## For the orchestrator

- **Claude worker seats have no native merge denial yet.** `worker_kind` is `claude`, and the ruleset no longer requires an approval. So until the planned Codex-seat task adds `Bash(gh pr merge:*)`, `Bash(gh api -X PUT:*)`, `Bash(gh api --method PUT:*)` and `Bash(gh api graphql:*)` to the worker worktree's `settings.local.json`, the permission prompt is the only local stop for a Claude worker's merge.
- **The README cites design report §14–§16,** which is only in the main checkout. The next boundary PR should carry it.
- **Codex seat and the keyring:** with default storage, a Codex seat on Linux may not reach the keyring inside its sandbox. Check this live before a Codex worker seat relies on `gh`.
- **Leftover config:** the T107 branch deletion could not update `.git/config` from the sandbox, so `branch.fix/gh-stores-per-machine.*` entries may remain. The remote branch is untouched.

[memory:decision] dotfiles-T108 (operator 2026-10-06, decision A): every seat on a machine acts as that machine's single GitHub account; the T90/T102/T103 role separation is removed; `main` is protected by actor-independent rulesets, native denial of merge commands in worker seats, and the integration gate.

CompactionDB: recorded as `8b5d314b-2b89-4602-a318-66dad566ba8a`, which supersedes `2a0f73e2`; the command and readback are in the validation file.

- **Not run:** `make update`, `make apply`, `make gh-auth`, `gh auth login`.

## Revise round 1 (task_rev `sha256:2b4e8650…c0bee32a`)

The audit of `b66f4297` returned `incorrect`: 1 P2 and 1 P3. Both are fixed.

1. **Head binding of the merge (P2): fixed in `f0a5407a`.**
   - **Problem:** the REST merge carried `sha=<head>`. Its replacement, `gh pr merge <pr> --squash`, would have merged a newer CI-green head on the audited head's evidence.
   - **Fix:** SKILL step 10.5, the agmsg-orchestration rule's `main` bullet and the README now merge with `gh pr merge <pr> --squash --match-head-commit <audited head sha>`, so GitHub refuses the merge if the head moved after the audit. `gh pr merge --help` (gh 2.101.0) lists the flag; the output is in the validation file.
   - **Test:** the docs test pins `--match-head-commit <audited head sha>` in the rule and the SKILL.
2. **Sandbox record (P3): fixed in the main checkout.**
   - The authenticated `gh` and `git push` calls used this machine's real login through gh, the normal path.
   - No command read, listed or printed a credential value.
   - Only the doctor, script and gate tests ran against fake HOMEs and a fake `gh`.

- **Re-run on `f0a5407a`:**
  - `make unit-test`: 911 tests, OK (skipped=1).
  - `bash -n`, shellcheck, `make render-check`, the validator (rc=0) and prettier all pass.
  - The task's grep with `-I` finds no match.
  - CI and the Bot wait are in the validation file.
- **Not run:** `make update`.

cost: n/a
