# Validation: dotfiles-T128-process-rules-a03

Every block is the verbatim output of the command shown, run in `.claude/worktrees/worker-f` on `docs/regime-pattern` (PR #318). This branch copy covers the a03 commits; the main-checkout copy adds the final head (design INV-8).

## 1. Task file

```
$ shasum -a 256 ~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T128-process-rules-a03.md .orchestration/dotfiles-T128-process-rules-a03/task.md | cut -c1-64
867ea4ca7c86f6518432a12254c3befc471184140b46b66aea2c53e6cb5ec78d
867ea4ca7c86f6518432a12254c3befc471184140b46b66aea2c53e6cb5ec78d
```

Both equal TASK 472's `task_sha256=867ea4ca…`.

## 2. Checks at `f4d45983`

```
$ git log --oneline -3; UV_OFFLINE=1 uv run python -m unittest tests.unit.test_agmsg_orchestration_docs 2>&1 | tail -3; ruff format --config ruff.toml --check tests/unit/test_agmsg_orchestration_docs.py; ruff check --config ruff.toml tests/unit/test_agmsg_orchestration_docs.py; prettier --check AGENTS.md home/dot_agents/skills/agmsg-orchestration/SKILL.md 2>&1 | tail -1
f4d45983 chore(orchestration): task file for dotfiles-T128-process-rules-a03
798fa098 docs(regime): scope the push-only exit to Claude seats
97288f6f chore(orchestration): evidence for the a02 revise's fifth item and Bot fix round 1
Ran 36 tests in 0.011s

OK
1 file already formatted
All checks passed!
All matched files use Prettier code style!
$ git show --stat --format=%h 798fa098
798fa098

 home/dot_agents/skills/agmsg-orchestration/SKILL.md | 2 +-
 tests/unit/test_agmsg_orchestration_docs.py         | 2 ++
 2 files changed, 3 insertions(+), 1 deletion(-)
```

## 3. Removal proofs (`scratchpad/mutate-a03.sh` at `f4d45983`: the step 2 sentence of `798fa098` reverted to its a02 wording, then removed; output cut to three lines of at most 400 characters per rule)

```
== removed rule: codex-seat-pushes-inside (SKILL, diff lines: 2) -> test_workers_commit_inside_the_sandbox
FAIL: test_workers_commit_inside_the_sandbox (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_workers_commit_inside_the_sandbox) (<redacted:secret-pattern>)
AssertionError: 'a Codex seat pushes from inside it (step 4)' not found in " and read `task_file` before editing or running validations. Create the task branch without touching the shared `.git/config`, which is read-only for a Codex seat by design (T64 writable roots): `git switch -c <branch> --no-track origin/main`, push with `git push origin <branch>` (no `-u`), and open the PR as a draft with 
FAILED (failures=1)
== removed rule: commit-inside-the-sandbox (SKILL, diff lines: 2) -> test_workers_commit_inside_the_sandbox
FAIL: test_workers_commit_inside_the_sandbox (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_workers_commit_inside_the_sandbox) (<redacted:secret-pattern>)
AssertionError: 'Commit inside the sandbox, with `git -c commit.gpgsign=false` when the signing key is unreadable there' not found in " and read `task_file` before editing or running validations. Create the task branch without touching the shared `.git/config`, which is read-only for a Codex seat by design (T64 writable roots): `git switch -c <branch> --no-track origin/main`, push with `git push o
FAIL: test_workers_commit_inside_the_sandbox (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_workers_commit_inside_the_sandbox) (<redacted:secret-pattern>)
== restored: OK
```

## 4. CompactionDB (main checkout, outside the sandbox through the permission gate)

```
$ cd ~/Workspace/dotfiles && uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content '[memory:decision] dotfiles-T128-process-rules-a03 …'
ae486f65-e10d-44bd-8680-8261d6fa4492
```

## 5. Bot fix round 1 at `7524e001` (thread 4240646079)

```
$ git log --oneline -1; UV_OFFLINE=1 uv run python -m unittest tests.unit.test_agmsg_orchestration_docs 2>&1 | tail -3; ruff format --config ruff.toml --check tests/unit/test_agmsg_orchestration_docs.py; ruff check --config ruff.toml tests/unit/test_agmsg_orchestration_docs.py; prettier --check home/dot_agents/skills/agmsg-orchestration/SKILL.md 2>&1 | tail -1
7524e001 docs(regime): gh pr ready runs only while the PR is a draft
Ran 36 tests in 0.010s

OK
1 file already formatted
All checks passed!
All matched files use Prettier code style!
```

Removal proof (`scratchpad/mutate-a03-b1.sh`: the a02 wording of the step 15 bullet pasted back):

```
== removed rule: ready-only-while-draft (SKILL, diff lines: 2) -> test_bot_fix_rounds_are_capped_and_the_pr_is_ready_first
FAIL: test_bot_fix_rounds_are_capped_and_the_pr_is_ready_first (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_bot_fix_rounds_are_capped_and_the_pr_is_ready_first) (<redacted:secret-pattern>)
AssertionError: 'Mark the PR ready for review with `gh pr ready <n>` before the first wait, while it is still a draft' not found in ', wait for CI and the Codex Bot before sending RESULT.\n    - Mark the PR ready for review with `gh pr ready <n>` before the wait: the Codex Bot reviews non-draft PRs, and a draft only on an explicit `@codex review` comment. When no Bot review of the final head arriv
FAILED (failures=1)
== restored: OK
```

## 7. Revise round 1 (the revise commit; `previous_head=b7ae2d54`; §6 is the main-checkout copy's final head of the first RESULT)

```
$ git log --oneline -1 origin/docs/regime-pattern; UV_OFFLINE=1 uv run python -m unittest tests.unit.test_agmsg_orchestration_docs 2>&1 | tail -3; ruff format --config ruff.toml --check tests/unit/test_agmsg_orchestration_docs.py; ruff check --config ruff.toml tests/unit/test_agmsg_orchestration_docs.py; prettier --check AGENTS.md home/dot_agents/skills/agmsg-orchestration/SKILL.md 2>&1 | tail -1
b7ae2d54 Merge branch 'main' into docs/regime-pattern
Ran 39 tests in 0.007s

OK
1 file already formatted
All checks passed!
All matched files use Prettier code style!
$ git diff --stat -- home/dot_agents/skills/agmsg-orchestration/SKILL.md tests/unit/test_agmsg_orchestration_docs.py
 .../dot_agents/skills/agmsg-orchestration/SKILL.md |  4 +--
 tests/unit/test_agmsg_orchestration_docs.py        | 34 ++++++++++++++++++++++
 2 files changed, 36 insertions(+), 2 deletions(-)
```

Removal proofs (`scratchpad/mutate-a03-r1.sh`: the working tree's three files in a `git archive HEAD` copy, each sentence removed alone or its old wording pasted back; output cut to three lines of at most 400 characters per rule):

```
== removed rule: closed-test-at-acceptance (SKILL, diff lines: 2) -> test_closed_selector_existence_is_checked_at_acceptance
FAIL: test_closed_selector_existence_is_checked_at_acceptance (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_closed_selector_existence_is_checked_at_acceptance) (<redacted:secret-pattern>s validation of the PR")
AssertionError: "a `closed` selector names a test present in the PR tree at acceptance and in the schema's validation of the PR" not found in '\n\n- Review every RESULT adversarially across correctness, regressions, security, and reporting omissions: try to refute it, independently re-derive findings, and never treat sampled spot checks as full verification.\n- Acceptance review, adversarial RESUL
FAILED (failures=1)
== removed rule: closed-form-only-at-review (SKILL, diff lines: 2) -> test_closed_selector_existence_is_checked_at_acceptance
FAIL: test_closed_selector_existence_is_checked_at_acceptance (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_closed_selector_existence_is_checked_at_acceptance) (<redacted:secret-pattern>s form only, since the test does not exist before implementation.")
AssertionError: "For a `closed` row it checks the selector's form only, since the test does not exist before implementation." not found in '\n\n- Review every RESULT adversarially across correctness, regressions, security, and reporting omissions: try to refute it, independently re-derive findings, and never treat sampled spot checks as full verification.\n- Acceptance review, adversarial RESULT r
FAILED (failures=1)
== removed rule: reviews-any-bot-pasted-back (SKILL, diff lines: 2) -> test_the_bot_wait_filters_the_codex_bot
FAIL: test_the_bot_wait_filters_the_codex_bot (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_the_bot_wait_filters_the_codex_bot) (<redacted:secret-pattern>chatgpt-codex-connector[bot]" and .commit_id=="<head-sha>")')
AssertionError: '.[]|select(.user.login=="chatgpt-codex-connector[bot]" and .commit_id=="<head-sha>")' not found in ', wait for CI and the Codex Bot before sending RESULT.\n    - Mark the PR ready for review with `gh pr ready <n>` before the first wait, while it is still a draft (`gh pr ready` exits non-zero on a PR that is already ready, so a later head\'s wait skips it): the Codex Bot reviews no
FAIL: test_the_bot_wait_filters_the_codex_bot (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_the_bot_wait_filters_the_codex_bot)
== removed rule: comments-any-bot-pasted-back (SKILL, diff lines: 2) -> test_the_bot_wait_filters_the_codex_bot
FAIL: test_the_bot_wait_filters_the_codex_bot (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_the_bot_wait_filters_the_codex_bot) (<redacted:secret-pattern>chatgpt-codex-connector[bot]" and .original_commit_id=="<head-sha>")')
AssertionError: '.[]|select(.in_reply_to_id == null and .user.login=="chatgpt-codex-connector[bot]" and .original_commit_id=="<head-sha>")' not found in ', wait for CI and the Codex Bot before sending RESULT.\n    - Mark the PR ready for review with `gh pr ready <n>` before the first wait, while it is still a draft (`gh pr ready` exits non-zero on a PR that is already ready, so a later head\'s wai
FAIL: test_the_bot_wait_filters_the_codex_bot (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_the_bot_wait_filters_the_codex_bot)
== removed rule: coderabbit-clause (SKILL, diff lines: 2) -> test_the_bot_wait_filters_the_codex_bot
FAIL: test_the_bot_wait_filters_the_codex_bot (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_the_bot_wait_filters_the_codex_bot) (<redacted:secret-pattern>s review never ends the wait.")
AssertionError: "A human comment, a CodeRabbit review or an earlier head's review never ends the wait." not found in ', wait for CI and the Codex Bot before sending RESULT.\n    - Mark the PR ready for review with `gh pr ready <n>` before the first wait, while it is still a draft (`gh pr ready` exits non-zero on a PR that is already ready, so a later head\'s wait skips it): the Codex Bot reviews n
FAILED (failures=1)
== removed rule: s1-s2-decision (SKILL, diff lines: 2) -> test_shape_rules_and_the_decision_sentence_are_pinned
FAIL: test_shape_rules_and_the_decision_sentence_are_pinned (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_shape_rules_and_the_decision_sentence_are_pinned) (<redacted:secret-pattern>)
AssertionError: 'S1 (the same finding class three times) and S2 (the INV-6 counts) are decided from that output.' not found in '\n\n- Review every RESULT adversarially across correctness, regressions, security, and reporting omissions: try to refute it, independently re-derive findings, and never treat sampled spot checks as full verification.\n- Acceptance review, adversarial RESULT review, and r
FAILED (failures=1)
== removed rule: closed-selector-in-tree (SKILL, diff lines: 2) -> test_shape_rules_and_the_decision_sentence_are_pinned
FAIL: test_shape_rules_and_the_decision_sentence_are_pinned (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_shape_rules_and_the_decision_sentence_are_pinned) (<redacted:secret-pattern>)
AssertionError: 'a `closed` selector names a test present in the PR tree' not found in '\n\n- Review every RESULT adversarially across correctness, regressions, security, and reporting omissions: try to refute it, independently re-derive findings, and never treat sampled spot checks as full verification.\n- Acceptance review, adversarial RESULT review, and review-profile work remain orchestrator-s
FAILED (failures=1)
== removed rule: out-of-scope-owner (SKILL, diff lines: 2) -> test_shape_rules_and_the_decision_sentence_are_pinned
FAIL: test_shape_rules_and_the_decision_sentence_are_pinned (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_shape_rules_and_the_decision_sentence_are_pinned) (<redacted:secret-pattern>s `implementing_tasks`")
AssertionError: "an `out-of-scope` owner is a task id in the design's `implementing_tasks`" not found in '\n\n- Review every RESULT adversarially across correctness, regressions, security, and reporting omissions: try to refute it, independently re-derive findings, and never treat sampled spot checks as full verification.\n- Acceptance review, adversarial RESULT review, and review-profile work rem
FAILED (failures=1)
== removed rule: residual-minimum (SKILL, diff lines: 2) -> test_shape_rules_and_the_decision_sentence_are_pinned
FAIL: test_shape_rules_and_the_decision_sentence_are_pinned (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_shape_rules_and_the_decision_sentence_are_pinned) (<redacted:secret-pattern>)
AssertionError: 'a `residual` payload is a sentence of at least 20 characters' not found in '\n\n- Review every RESULT adversarially across correctness, regressions, security, and reporting omissions: try to refute it, independently re-derive findings, and never treat sampled spot checks as full verification.\n- Acceptance review, adversarial RESULT review, and review-profile work remain orchestra
FAILED (failures=1)
== restored: OK
```

CompactionDB (main checkout, outside the sandbox through the permission gate):

```
$ cd ~/Workspace/dotfiles && uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content '[memory:decision] dotfiles-T128-process-rules-a03 revise round 1 …'
fa0f25f1-360c-463e-90f6-df466c8299c4
```

## 8. Bot fix round 1 of the revise at `114d5b91` (threads 4243516879, 4243516880)

```
$ git log --oneline -1; UV_OFFLINE=1 uv run python -m unittest tests.unit.test_agmsg_orchestration_docs 2>&1 | tail -3; ruff format --config ruff.toml --check tests/unit/test_agmsg_orchestration_docs.py; ruff check --config ruff.toml tests/unit/test_agmsg_orchestration_docs.py; prettier --check home/dot_agents/skills/agmsg-orchestration/SKILL.md 2>&1 | tail -1
114d5b91 docs(regime): count review-body findings beside the counter script; survive the no-checks race
Ran 41 tests in 0.008s

OK
1 file already formatted
All checks passed!
All matched files use Prettier code style!
$ grep -n "reviews" scripts/regime-counters.sh | head -3; sed -n 122,125p scripts/regime-counters.sh   # what the counter fetches
    state=unknown
    pr="$(jq -r '.pr // empty' <<< "${counts}")"
    if [[ -n ${github_file} ]]; then
        github="$(cat -- "${github_file}")" && state=ok
```

Removal proofs (`scratchpad/mutate-a03-r1b.sh`, the same harness with the two new sentences):

```
== removed rule: counters-review-bodies (SKILL, diff lines: 2) -> test_counters_add_review_body_findings
FAIL: test_counters_add_review_body_findings (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_counters_add_review_body_findings)
AssertionError: "The script reads inline review comments only, so the orchestrator also counts the P0/P1-badged Bot review bodies of `…/pulls/<n>/reviews`, grouped by `commit_id`, by hand and pastes that command and its output beside the script's, until the script reads review bodies too." not found in '\n\n- Review every RESULT adversarially across correctness, regressions, security, and reportin
FAILED (failures=1)
== removed rule: watcher-no-checks-race (SKILL, diff lines: 2) -> test_the_ci_watcher_survives_the_no_checks_race
FAIL: test_the_ci_watcher_survives_the_no_checks_race (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_the_ci_watcher_survives_the_no_checks_race)
AssertionError: 'Right after a push GitHub can report no checks yet, and the watcher then exits 1 with `no checks reported`: start it once a check is listed, and restart it on that message instead of reading it as a CI failure.' not found in ', wait for CI and the Codex Bot before sending RESULT.\n    - Mark the PR ready for review with `gh pr ready <n>` before the first wait, while it is still a 
FAILED (failures=1)
== restored: OK
```
