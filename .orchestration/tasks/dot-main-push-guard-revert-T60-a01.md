# AGMSG-TASK dot-main-push-guard-revert-T60-a01

Drafted 2026-10-03 by the orchestrator seat; operator-approved ("G1 を適用した、T60 を起票しろ"). Worker: `claude-standard-dot-a005` in `~/Workspace/dotfiles/.claude/worktrees/worker-c`.

## Objective

GitHub is now the boundary for `main`. On 2026-10-03 the operator applied the ruleset "main integration gate" to `mryfmo/dotfiles` (`gh api repos/mryfmo/dotfiles/rules/branches/main` lists `deletion`, `non_fast_forward`, `pull_request` with `required_review_thread_resolution: true`, and `required_status_checks` with the seven contexts from README, strict policy on; repository merge settings are now squash-only with auto-merge enabled, `delete_branch_on_merge` stays false). The repository-local pre-push guard that T54 (#225, ae22603) added duplicates that boundary with a client-side hook an agent can satisfy or bypass itself (`ORCH_PUSH_MAIN`, `--no-verify`). Operator decision (target-state §6 #4): the ruleset is authoritative, the guard is reverted.

Remove the guard and the `ORCH_PUSH_MAIN` convention completely, and make the documented push path match the ruleset:

1. `home/dot_local/bin/common/executable_herdr-agents`: delete `main_push_guard`, `install_main_push_guard`, the `--main-push-guard` mode dispatch (around line 1884), the call from `--bootstrap-agmsg` (around line 1706), and every header/usage/shdoc mention (lines 27–28, 45, 86, 107–111). In the `agmsg-orchestration:` directive printed by `--attach` (line 609) replace the sentence "Never push a repository change to main yourself: the pre-push guard passes only ORCH_PUSH_MAIN=boundary (...) and ORCH_PUSH_MAIN=acceptance." with one sentence stating that `main` accepts only pull requests (GitHub ruleset), so every change, the `.orchestration` boundary commit included, travels as a PR merged with `gh pr merge --squash`.
   - `--bootstrap-agmsg` must remove a stub it wrote earlier: a `<git-common-dir>/hooks/pre-push` whose second line is exactly `# herdr-agents main-push guard: written by herdr-agents --bootstrap-agmsg; the checks live in herdr-agents --main-push-guard.` is deleted (and `<git-common-dir>/orch-push-main.log` with it); any other pre-push hook is left alone, as T54 already promised. Both machines currently carry that stub (DGX: `~/Workspace/dotfiles/.git/hooks/pre-push` and `~/.local/share/chezmoi/.git/hooks/pre-push`), and with the guard mode gone the stub's fallback branch would refuse every push to `main`, so the removal is what makes `make update` converge.
2. `tests/unit/test_herdr_agents.py`: delete the guard tests (`test_bootstrap_installs_a_main_push_guard_that_needs_an_override`, `test_main_push_guard_allows_boundary_commits_and_refuses_rewinds_and_deletes`, `test_main_push_guard_checks_a_merge_by_its_tree_diff`, `test_main_push_guard_fails_closed_when_the_changes_cannot_be_listed`, `test_bootstrap_keeps_an_edited_main_push_guard_stub`, `test_main_push_guard_stub_without_a_launcher_refuses_only_main`, `test_main_push_guard_stub_with_an_old_launcher_refuses_only_main`, `test_bootstrap_skips_the_guard_while_the_launcher_predates_it`, `test_bootstrap_leaves_a_foreign_pre_push_hook_alone`, `test_bootstrap_installs_no_guard_without_an_orchestrator_identity`) and their helpers (the `ORCH_PUSH_MAIN` env plumbing around lines 1339–1341, the old-launcher fixture around 1358, the hook path helper around 1391); update the directive assertions (lines 737 and 2091–2092) to the new sentence; add exactly two tests: bootstrap removes its own stub (and the log) and bootstrap leaves a foreign pre-push hook alone. `test_codex_worker_is_not_subject_to_the_identity_guard` and `test_audit_tab_keeps_the_full_mode_duplicate_workspace_guard` are unrelated and stay.
3. `home/dot_config/claude/rules/agmsg-orchestration.md` (line 13) and `home/dot_agents/skills/agmsg-orchestration/SKILL.md` (lines 60 and 62): rewrite the push bullets. Invariant: the orchestrator never pushes to `main`; `main` is protected by the GitHub ruleset (pull request required, review threads resolved, the seven required checks, strict up-to-date policy, no deletion or rewind); the `.orchestration` boundary commit goes on a branch (`orchestration/boundary-<YYYY-MM-DD>`), is opened as a PR and merged with `gh pr merge --squash --auto` (the `changes` job skips the test matrix for `.orchestration`-only diffs, the required checks report `skipped`, which the ruleset accepts); an acceptance merge happens only on GitHub with `gh pr merge --squash` (local merge + push is no longer a path). Remove every `ORCH_PUSH_MAIN` mention from the Stop checklist. Keep the rule and SKILL wording byte-identical where `tests/unit/test_agmsg_orchestration_docs.py` requires shared invariants, and replace the `"ORCH_PUSH_MAIN=boundary"` token there (line 23) with a token of the new invariant that both files contain (for example `gh pr merge --squash`).
4. `README.md`: replace the paragraph at line 999 (pre-push guard, `ORCH_PUSH_MAIN`, "GitHub branch protection is the server-side boundary") with the statement that the ruleset is the boundary; update the ruleset section (around lines 905–945): it is applied as of 2026-10-03, the payload shown is the applied form (add `{"type": "deletion"}` and `{"type": "non_fast_forward"}` before the `pull_request` rule, in that order), changes to the ruleset are made with `gh api -X PUT repos/mryfmo/dotfiles/rulesets/<id>` and never by disabling enforcement, and the repository merge settings are squash-only with auto-merge enabled.
5. Do not touch the other T54 content (the regime-activation directive itself, the `make upgrade` pin-path rule, the mise floor) or `.ua/`.

[memory:decision] T60 (operator 2026-10-03): the GitHub ruleset "main integration gate" is the sole boundary for `main`; the T54 client-side pre-push guard and the `ORCH_PUSH_MAIN` convention are removed, and the `.orchestration` boundary commit travels as a squash-merged PR like every other change.

## Repo / branch

- Work ONLY in the worker-c worktree. `git fetch origin`; `git switch -c chore/revert-main-push-guard origin/main` (0a812d30 or later). Verify the dispatched task_rev sha256 against this file; else stop and PONG blocked. The local pre-push stub guards only `main`, so pushing the feature branch is unaffected.
- The ruleset's strict policy applies to your PR: if `main` moves while the PR is open, run `gh pr update-branch <pr>` (or `gh api -X PUT repos/mryfmo/dotfiles/pulls/<pr>/update-branch`) and wait for CI again before RESULT.

## Allowed files

- `home/dot_local/bin/common/executable_herdr-agents`
- `tests/unit/test_herdr_agents.py`, `tests/unit/test_agmsg_orchestration_docs.py`
- `home/dot_config/claude/rules/agmsg-orchestration.md`, `home/dot_agents/skills/agmsg-orchestration/SKILL.md`
- `README.md` (only the two regions named above)
- any unit test that asserts the exact README ruleset payload or the old directive sentence, if one exists (name it in the report)
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dot-main-push-guard-revert-T60-a01.md` (main checkout)

## Forbidden actions

- Changing pins; touching `.ua/`, `Makefile`, hooks under `home/dot_claude/hooks`, or `scripts/`; adding any replacement client-side push check; running `make update`/`make apply` (operator lifecycle); local bats; merging; force push; pushing `main`.

## Validation commands (paste verbatim output)

```
git diff origin/main --stat
grep -rn 'ORCH_PUSH_MAIN\|main-push-guard\|main_push_guard\|orch-push-main' home scripts tests Makefile README.md AGENTS.md docs; echo "exit=$?"   # expect no matches, exit=1
make unit-test
make validate-agent-assets
mise x shfmt@<pin> -- shfmt -i 4 -sr -d home/dot_local/bin/common/executable_herdr-agents   # or the repository's shfmt form; expect no diff
gh pr checks <pr-number>     # all seven required contexts pass on the final head; nothing pending
gh api repos/mryfmo/dotfiles/pulls/<pr-number> --jq '.mergeable_state'   # expect "clean" (strict policy satisfied)
```

## Completion

1. PR to `main`, English title/description ending with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. CI green on the final head and the branch up to date with `main`.
2. Artifacts at the exact expected paths; validation with verbatim outputs, PR number and head SHA; report lists every removed function/test and the two added tests.
3. CompactionDB `memory add --kind decision --scope project` with the `[memory:decision]` text from the main checkout; paste command and output.
4. `AGMSG-RESULT v1` via `agmsg-dispatch dotfiles claude-standard-dot-a005 claude-remediation-dot wT:p1 "<single line>"` (outside the sandbox). `cost:` line. max_turns=35.

## Revise round 1 (2026-10-03, after RESULT on 8259cf5c)

Audits: 8259cf5c `correct` (no findings); 560df81b `incorrect` with three findings all fixed later in the PR (marker-only match → 4445917b, hooks path → 4445917b, date-only branch → 8259cf5c); 4445917b `incorrect` with two findings, one fixed in 8259cf5c (external `core.hooksPath`) and **one still live on the final head**:

- `remove_retired_pre_push_stub` compares with `git hash-object -- "${hook}"`, which applies the clean filters that `.gitattributes` selects for that path (git-hash-object: without `--no-filters` the file name is used for attribute lookup). A customized hook can therefore hash equal to the retired stub after filtering and be deleted; the auditor reproduced it with deletion intercepted. Fix: `git hash-object --no-filters -- "${hook}"` so the comparison is on raw bytes. Add one subtest to `test_bootstrap_leaves_a_foreign_pre_push_hook_alone` that fails without `--no-filters` (for example a `.gitattributes` in the workdir with `* text` and a copy of the stub whose bytes differ only in line endings, which must be left alone).

Keep the fix to that line and that subtest; push to the same branch; CI green; branch up to date with `main`; then a new `AGMSG-RESULT v1` with the new head. The Codex Bot may post on the push: list any new thread with its fix commit in the report, do not resolve threads.
