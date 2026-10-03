# Report: dot-main-push-guard-revert-T60-a01

- **Worker and branch:** `claude-standard-dot-a005` in worker-c. Branch `chore/revert-main-push-guard` from `origin/main` 0a812d30.
- **PR:** #231, https://github.com/mryfmo/dotfiles/pull/231.
- **task_rev:** `5ce094ad…`, matched.
- **Commits:**
  - `560df81b`: the revert.
  - `4445917b`: Codex review round 1, P1 and P2.
  - `8259cf5c`: Codex review round 2, two P2s.
- **Final head:** `8259cf5c`.
  - **CI:** green; 13 pass and `nix` is skipped.
  - **Branch:** up to date with `main` (0a812d30).
  - **`mergeable_state`:** `blocked`, solely by the five unresolved Codex review threads (section 4).
  - **Bot review:** no thread on `8259cf5c` at RESULT time.

## 1. Validation grep: expectation not met, and why (orchestrator decision)

The task expected `grep -rn 'ORCH_PUSH_MAIN\|main-push-guard\|main_push_guard\|orch-push-main' … ; exit=1`. The final head has residual matches, and they are inherent to the required stub removal:

- **In the launcher, one match:** `rm -f -- "${hook}" "${common_dir}/orch-push-main.log"`. The task requires deleting that log together with the stub.
- **In `tests/unit/test_herdr_agents.py`:**
  - the `RETIRED_STUB` fixture, which is the exact 740-byte body the old installer wrote and therefore contains `--main-push-guard`;
  - the `orch-push-main.log` paths of the two required tests.

The launcher no longer contains the marker literal. It recognises the stub by its git blob id instead (see section 3). Splitting strings to dodge the grep would be gaming the check, so I did not do it. The exact residual lines are pasted in the validation file.

## 2. Removed and added (inventory)

- **Launcher (`home/dot_local/bin/common/executable_herdr-agents`):**
  - Functions removed: `main_push_guard` and `install_main_push_guard`.
  - The `--main-push-guard` mode dispatch is removed, along with the `@option --main-push-guard` shdoc line, the usage line, and the header and usage prose.
  - The `bootstrap_agmsg` call and description are updated.
  - The `agmsg-orchestration:` directive sentence now reads: "Never push to main yourself: main accepts only pull requests (GitHub ruleset), so every change, the .orchestration boundary commit included, travels as a PR merged with gh pr merge --squash."
  - Added `remove_retired_pre_push_stub`, called by `--bootstrap-agmsg`.
- **Tests removed (11):**
  - `test_bootstrap_installs_a_main_push_guard_that_needs_an_override`
  - `test_main_push_guard_allows_boundary_commits_and_refuses_rewinds_and_deletes`
  - `test_main_push_guard_checks_a_merge_by_its_tree_diff`
  - `test_main_push_guard_fails_closed_when_the_changes_cannot_be_listed`
  - `test_bootstrap_keeps_an_edited_main_push_guard_stub`
  - `test_main_push_guard_stub_without_a_launcher_refuses_only_main`
  - `test_main_push_guard_stub_with_an_old_launcher_refuses_only_main`
  - `test_bootstrap_skips_the_guard_while_the_launcher_predates_it`
  - `test_bootstrap_restores_the_execute_bit_of_the_stub` (not in the task's list; it only tests the removed installer)
  - `test_bootstrap_leaves_a_foreign_pre_push_hook_alone` (old version)
  - `test_bootstrap_installs_no_guard_without_an_orchestrator_identity`
- **Helpers removed (6):** `guard_env` (the `ORCH_PUSH_MAIN` plumbing), `guard_git`, `bootstrap_guard`, `write_old_launcher`, `commit_file`, `write_guard_repo`.
- **Tests added (exactly 2), with the helper `init_git_workdir(hooks_path=None)`:**
  - `test_bootstrap_removes_its_retired_pre_push_stub`: subtests for the default hooks dir and an in-repo `core.hooksPath`. Checks that both the stub and `orch-push-main.log` are removed.
  - `test_bootstrap_leaves_a_foreign_pre_push_hook_alone`: subtests for a foreign hook, an edited stub copy (left alone with a notice), and the exact stub under a `core.hooksPath` outside the common git dir (left alone).
- **Directive assertions updated:** the `assertIn` near line 737 and the full-directive `assertEqual` near line 2091.
- **Test count:** 718 → 709 (−11 + 2).
- **Docs:**
  - `test_agmsg_orchestration_docs.py`: the shared-invariant token `ORCH_PUSH_MAIN=boundary` becomes `gh pr merge --squash`.
  - Rule line 13 and SKILL line 62 now carry the same push bullet (ruleset invariant, fresh boundary branch from `origin/main` merged with `gh pr merge --squash --auto`, acceptance merges on GitHub only).
  - SKILL Stop checklist: `ORCH_PUSH_MAIN` is removed.
- **README:**
  - Ruleset section: applied on 2026-10-03; the payload is the applied form with `{"type": "deletion"}` and `{"type": "non_fast_forward"}` before `pull_request`; changes go through `gh api -X PUT …/rulesets/<id>`, never by disabling enforcement; merges are squash-only with auto-merge, and `delete_branch_on_merge` stays off.
  - The pre-push paragraph near line 999 is replaced by the ruleset boundary.
  - I checked the live ruleset 24397953 with `gh api`. It matches, and GitHub additionally fills in its own server-side defaults.
- **No unit test** asserts the README ruleset payload (grep of `tests/`).

## 3. Stub removal: how the deployed stubs are recognised

- **Exact blob match:** a hook is removed only when its content is exactly the stub every install wrote: git blob `af94a0b55e08a02423f72f3d4f713a4a804d905e`, 740 bytes, derived from `origin/main`'s installer body. I confirmed that **both deployed stubs on this machine** (`~/Workspace/dotfiles/.git/hooks/pre-push` and `~/.local/share/chezmoi/.git/hooks/pre-push`) have that blob id.
- **Hook location:** the hook is resolved with `git rev-parse --git-path hooks`, as the installer did, and only when it lies inside the common git dir.
- **Edited copies:** an edited copy that kept the stub header is left unchanged with a notice.
- **Deviation from the task's literal criterion:** the task said "second line is exactly the marker". The stricter exact-content match and the hooks-path handling come from the Codex review (P1 and both P2s). They serve the task's stated intent: remove only the stub it wrote, and leave every other hook alone, as T54 promised.

## 4. Codex review threads (for the orchestrator's sweep; I did not reply or resolve)

| Thread                                                     | Commit   | Status                                                                                                                                                                                                                                                                                                                                   |
| ---------------------------------------------------------- | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| P1 Preserve customized copies                              | 560df81b | fixed in `4445917b` (exact-blob match; edited copy kept with a notice)                                                                                                                                                                                                                                                                   |
| P2 Resolve the configured hooks directory                  | 560df81b | fixed in `4445917b` (`--git-path hooks`)                                                                                                                                                                                                                                                                                                 |
| P2 Preserve hooks outside Git's common directory           | 4445917b | fixed in `8259cf5c` (bounded to the common git dir; subtest)                                                                                                                                                                                                                                                                             |
| P2 Use a fresh branch for every boundary                   | 4445917b | fixed in `8259cf5c` (rule and SKILL: a fresh branch from `origin/main`, `-<n>` suffix for the same day)                                                                                                                                                                                                                                  |
| P2 Scope guard retirement to repositories with the ruleset | 4445917b | **not changed. Proposed `not-applicable`:** the operator decision retires the guard mode itself (target-state §6 #4), so it cannot be retained for other repositories. A leftover stub there would refuse every push to `main` through its fallback branch. Server-side protection for other repositories is a separate policy decision. |

`mergeable_state` stays `blocked` until these threads are resolved.

## 5. Operator notes after merge

- **Run `make update` in each clone that carries the stub.** `make update` and `make upgrade` run `agmsg-bootstrap`, which runs the **source-tree** launcher against `$(CURDIR)`, so one run per clone removes that clone's stub. Run it in `~/Workspace/dotfiles` and in `~/.local/share/chezmoi`, the second clone, which also carries the stub.
- **Until then, pushes to `main` from that clone are refused** by the old stub's fallback branch. That doesn't matter now, because `main` accepts only PRs.
- **The MacBook clone:** I couldn't check it from here; the same procedure applies.

## CompactionDB

```
cd /home/moriya/Workspace/dotfiles && python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'T60 (operator 2026-10-03): the GitHub ruleset "main integration gate" is the sole boundary for `main`; the T54 client-side pre-push guard and the `ORCH_PUSH_MAIN` convention are removed, and the `.orchestration` boundary commit travels as a squash-merged PR like every other change.'
b81a4935-5ec0-4c23-9e86-bd202fd610fd
```

[memory:decision] T60 (operator 2026-10-03): the GitHub ruleset "main integration gate" is the sole boundary for `main`; the T54 client-side pre-push guard and the `ORCH_PUSH_MAIN` convention are removed, and the `.orchestration` boundary commit travels as a squash-merged PR like every other change.

## Artifacts

- validation: `.orchestration/validation/dot-main-push-guard-revert-T60-a01.md`
- sandbox: `.orchestration/sandboxes/dot-main-push-guard-revert-T60-a01.md`
- learning: `.orchestration/learning/dot-main-push-guard-revert-T60-a01.md`
- autoskill: `.orchestration/autoskill/runs/dot-main-push-guard-revert-T60-a01.md`

cost: n/a (no subagents; the runtime does not expose session totals)

## Revise round 1 (task_rev `36500453…`)

- **Finding:** the audit finding on 4445917b was still live on 8259cf5c. `git hash-object -- <hook>` applies the clean filters that `.gitattributes` selects for that path, so a customized hook could hash equal to the retired stub and be deleted.
- **Fix:** commit `65f54c46` changes that one line to `git hash-object --no-filters -- "${hook}"`, which compares raw bytes.
- **New subtest** in `test_bootstrap_leaves_a_foreign_pre_push_hook_alone`: a CRLF copy of the stub under a workdir `.gitattributes` with `* text` must be left unchanged, with the edited-copy notice.
  - It **fails without `--no-filters`**: `ERROR … (hook='CRLF stub under a text .gitattributes')`, because the hook is deleted.
  - It passes with the flag. Both runs are pasted in the validation file.
  - To compare bytes, that test now writes and reads the hook with `write_bytes`/`read_bytes`. `read_text()` would translate CRLF to LF, so a text comparison could not detect the difference. No other test changed.
- **Final head:** `65f54c46`.
  - **CI:** green (13 pass, `nix` skipped).
  - **Branch:** up to date with `main` (0a812d30).
  - **`mergeable_state`:** **`clean`**. All five Codex threads are resolved by the orchestrator, and there is no new bot thread on `65f54c46`.
  - **`make unit-test`:** 709 tests, OK (2 skipped).
