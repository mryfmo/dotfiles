# dotfiles-T68-gate-audit-evidence-a01 — validation

PR: https://github.com/mryfmo/dotfiles/pull/246 — branch `feat/gate-audit-evidence`. Final head `3ba270d66778dab382e9cb055f55199e6d6c328d`, the `gh pr update-branch` merge of main 8922f13b. Outputs are verbatim.

Commits:
- `46f14681` fix(review-gate): read the audit verdict exactly where herdr-agents does
- `8922f13b` chore(bootstrap): delete bootstrap code that nothing runs (#247)
- `22efc32c` fix(review-gate): bind the audit to the task named by the PR feedback evidence
- `83074eea` fix(review-gate): tie audit dispositions to numbered findings, count bulleted findings, exempt .orchestration-only PRs
- `abf9933f` feat(review-gate): require the task-level audit of HEAD for PR integration

## Task commit abf9933f (origin/main 138e6a72)

### `git diff origin/main --stat` (origin/main = 138e6a72)

```text
 home/dot_config/claude/rules/pr-integration.md |   1 +
 scripts/require-crit-review.py                 | 107 ++++++++++++++++++-
 tests/unit/test_require_crit_review.py         | 138 +++++++++++++++++++++++++
 3 files changed, 245 insertions(+), 1 deletion(-)
exit status: 0
```

### `uv run python -m unittest tests.unit.test_require_crit_review 2>&1 | tail -3`

```text
Ran 66 tests in 9.438s

OK
```

### new audit tests (-v)

```text
test_audit_must_name_head_and_live_under_validation (tests.unit.test_require_crit_review.ReviewGuardTest.test_audit_must_name_head_and_live_under_validation) ... ok
test_audit_verdict_prefers_the_last_message_file (tests.unit.test_require_crit_review.ReviewGuardTest.test_audit_verdict_prefers_the_last_message_file) ... ok
test_base_accepts_a_correct_audit_of_head (tests.unit.test_require_crit_review.ReviewGuardTest.test_base_accepts_a_correct_audit_of_head) ... ok
test_base_requires_audit_evidence_for_a_reviewed_change (tests.unit.test_require_crit_review.ReviewGuardTest.test_base_requires_audit_evidence_for_a_reviewed_change) ... ok
test_blocked_or_missing_audit_verdict_fails (tests.unit.test_require_crit_review.ReviewGuardTest.test_blocked_or_missing_audit_verdict_fails) ... ok
test_incorrect_audit_needs_not_applicable_dispositions (tests.unit.test_require_crit_review.ReviewGuardTest.test_incorrect_audit_needs_not_applicable_dispositions) ... ok
test_incorrect_audit_without_findings_fails (tests.unit.test_require_crit_review.ReviewGuardTest.test_incorrect_audit_without_findings_fails) ... ok
test_orchestration_only_pr_needs_no_audit (tests.unit.test_require_crit_review.ReviewGuardTest.test_orchestration_only_pr_needs_no_audit) ... ok
```

### `make unit-test` (tail)

```text
Ran 709 tests in 161.241s

OK (skipped=1)
unit-test rc=0
```

### `make validate-agent-assets` (tail)

```text
agent asset validation ok
validate-agent-assets rc=0
```

### `mise x node npm:prettier -- prettier --check home/dot_config/claude/rules/pr-integration.md`

```text
Checking formatting...
All matched files use Prettier code style!
exit status: 0
```

### `ruff format --config ruff.toml --check scripts/require-crit-review.py tests/unit/test_require_crit_review.py`

```text
2 files already formatted
exit status: 0
```

### GNU make passes AUDIT_* to recipes (env and command-line forms; probe makefile on stdin)

```text
recipe sees AUDIT_EVIDENCE=probe-value
recipe sees AUDIT_DISPOSITIONS=cli-value
```

### `git push` / `gh pr create`

```text
 * [new branch]        HEAD -> feat/gate-audit-evidence
https://github.com/mryfmo/dotfiles/pull/246
```

## Review rounds

### Codex inline comments (all heads)

```text
4175944623 chatgpt-codex-connector[bot] abf9933f scripts/require-crit-review.py:641 **<sub><sub>![P1 Badge](https://img.shields.io/badge/P1-orange?style=flat)</sub></sub>  Require distinct dispositions for audit findings**
4175944624 chatgpt-codex-connector[bot] abf9933f home/dot_config/claude/rules/pr-integration.md:7 **<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  Document the audit requirement for Codex users**
4175944626 chatgpt-codex-connector[bot] abf9933f scripts/require-crit-review.py:29 **<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  Accept the established bullet-form audit findings**
4175944628 chatgpt-codex-connector[bot] abf9933f scripts/require-crit-review.py:712 **<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  Preserve the .orchestration-only audit exemption**
4175981346 chatgpt-codex-connector[bot] 83074eea scripts/require-crit-review.py:724 **<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  Update the remaining PR-integration instructions**
4175981351 chatgpt-codex-connector[bot] 83074eea scripts/require-crit-review.py:610 **<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  Bind audit evidence to the feedback task**
4176028652 chatgpt-codex-connector[bot] 22efc32c home/dot_config/claude/rules/pr-integration.md:7 **<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  Show the required audit arguments**
4176028656 chatgpt-codex-connector[bot] 22efc32c scripts/require-crit-review.py:597 **<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  Validate the companion last-message path**
4176028658 chatgpt-codex-connector[bot] 22efc32c scripts/require-crit-review.py:600 **<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  Parse fallback transcripts by their final Codex block**
```

### Codex reviews and reactions

```text
chatgpt-codex-connector[bot]	COMMENTED	abf9933f	2026-10-04T03:10:18Z
chatgpt-codex-connector[bot]	COMMENTED	83074eea	2026-10-04T03:26:43Z
chatgpt-codex-connector[bot]	COMMENTED	22efc32c	2026-10-04T03:46:58Z
chatgpt-codex-connector[bot]	+1	2026-10-04T03:58:27Z
```

## Final head 3ba270d6

### `git diff origin/main --stat` (origin/main = 8922f13b)

```text
 home/dot_config/claude/rules/pr-integration.md |   1 +
 home/dot_config/codex/AGENTS.md                |   2 +-
 scripts/require-crit-review.py                 | 150 +++++++++++++++++-
 tests/unit/test_require_crit_review.py         | 202 +++++++++++++++++++++++++
 4 files changed, 353 insertions(+), 2 deletions(-)
```

### `uv run python -m unittest tests.unit.test_require_crit_review 2>&1 | tail -3` (run from `git archive 3ba270d6 scripts tests` in a temp dir)

```text
Ran 69 tests in 9.832s

OK
```

### `make unit-test` on 46f14681 (tail)

```text
Ran 712 tests in 165.100s

OK (skipped=1)
unit-test rc=0
```

### `make validate-agent-assets` on 46f14681 (tail)

```text
agent asset validation ok
validate-agent-assets rc=0
```

### `gh pr checks 246` (final head 3ba270d6)

```text
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37175483512/job/111357102899	
private-bootstrap (macos-14, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37175483466/job/111357102883	
private-bootstrap (ubuntu-24.04, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37175483466/job/111357102851	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37175483466/job/111357102915	
public-bootstrap (macos-14, client)	pass	8m20s	https://github.com/mryfmo/dotfiles/actions/runs/37175483466/job/111357102896	
public-bootstrap (ubuntu-24.04, client)	pass	9m16s	https://github.com/mryfmo/dotfiles/actions/runs/37175483466/job/111357102936	
public-bootstrap (ubuntu-24.04, server)	pass	7m15s	https://github.com/mryfmo/dotfiles/actions/runs/37175483466/job/111357102875	
test (macos-14, client)	pass	5m59s	https://github.com/mryfmo/dotfiles/actions/runs/37175483512/job/111357129191	
test (ubuntu-24.04, client)	pass	7m7s	https://github.com/mryfmo/dotfiles/actions/runs/37175483512/job/111357129237	
test (ubuntu-24.04, server)	pass	4m14s	https://github.com/mryfmo/dotfiles/actions/runs/37175483512/job/111357129259	
test (ubuntu-26.04, client)	pass	7m11s	https://github.com/mryfmo/dotfiles/actions/runs/37175483512/job/111357129228	
validate	pass	15s	https://github.com/mryfmo/dotfiles/actions/runs/37175483516/job/111357103289	
exit status: 0
```

### `gh api repos/mryfmo/dotfiles/pulls/246 --jq .head.sha,.mergeable_state`; `git ls-remote origin refs/heads/main`

```text
3ba270d66778dab382e9cb055f55199e6d6c328d
blocked
8922f13bc370b2a2144184a4a03518015002e2aa	refs/heads/main
```

### CompactionDB (main checkout, run unsandboxed)

```text
$ cd /home/moriya/Workspace/dotfiles && python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "dotfiles-T68 (operator 2026-10-03): \`make require-crit-review\` with BASE requires \`AUDIT_EVIDENCE=<.orchestration/validation/<id>-audit-<sha7>.md>\` whose sha matches HEAD and whose last \`Verdict:\` is \`correct\`, or \`incorrect\` with every finding dispositioned \`not-applicable\` in the acceptance record (\`AUDIT_DISPOSITIONS\`); \`.orchestration\`-only PRs are exempt."
5a73b2dc-d0e5-42aa-b935-87078b55547a
$ python3 .claude/hooks/contextdb_cli.py memory search dotfiles-T68
5a73b2dc-d0e5-42aa-b935-87078b55547a [project/decision] dotfiles-T68 (operator 2026-10-03): `make require-crit-review` with BASE requires `AUDIT_EVIDENCE=<.orchestration/validation/<id>-audit-<sha7>.md>` whose sha matches HEAD and whose last `Verdict:` is `correct`, or `incorrect` with every finding dispositioned `not-applicable` in the acceptance record (`AUDIT_DISPOSITIONS`); `.orchestration`-only PRs are exempt.
```

## Revise round 1 (task_rev 9e175902…): task-level audit of 3ba270d6 was incorrect

### Fix commit

```text
5168613a5ea297cbe7a101cedb055986bd64c5b2 fix(review-gate): take the audit verdict only from the audit's own last message
 home/dot_config/claude/rules/pr-integration.md |  2 +-
 home/dot_config/codex/AGENTS.md                |  2 +-
 scripts/require-crit-review.py                 | 65 +++++++++++-------------
 tests/unit/test_require_crit_review.py         | 70 ++++++++++++--------------
 4 files changed, 63 insertions(+), 76 deletions(-)
```

### `uv run python -m unittest tests.unit.test_require_crit_review 2>&1 | tail -3` (from `git archive 5168613a scripts tests`)

```text
Ran 68 tests in 10.195s

OK
```

### `final_codex_block` removed (`grep -c`)

```text
0
```

### `make unit-test` on 5168613a (tail)

```text
Ran 710 tests in 164.776s

OK (skipped=1)
unit-test rc=0
```

### `make validate-agent-assets` on 5168613a (tail)

```text
agent asset validation ok
validate-agent-assets rc=0
```

### `git push`

```text
   3ba270d6..5168613a  HEAD -> feat/gate-audit-evidence
```

### `gh pr checks 246` (final head 5168613a)

```text
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37178959492/job/111367409759	
private-bootstrap (macos-14, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37178959497/job/111367409711	
private-bootstrap (ubuntu-24.04, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37178959497/job/111367409655	
private-bootstrap (ubuntu-24.04, server)	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/37178959497/job/111367409604	
public-bootstrap (macos-14, client)	pass	8m8s	https://github.com/mryfmo/dotfiles/actions/runs/37178959497/job/111367409719	
public-bootstrap (ubuntu-24.04, client)	pass	9m22s	https://github.com/mryfmo/dotfiles/actions/runs/37178959497/job/111367409878	
public-bootstrap (ubuntu-24.04, server)	pass	5m45s	https://github.com/mryfmo/dotfiles/actions/runs/37178959497/job/111367409726	
test (macos-14, client)	pass	5m27s	https://github.com/mryfmo/dotfiles/actions/runs/37178959492/job/111367432811	
test (ubuntu-24.04, client)	pass	7m15s	https://github.com/mryfmo/dotfiles/actions/runs/37178959492/job/111367432831	
test (ubuntu-24.04, server)	pass	3m52s	https://github.com/mryfmo/dotfiles/actions/runs/37178959492/job/111367432840	
test (ubuntu-26.04, client)	pass	7m40s	https://github.com/mryfmo/dotfiles/actions/runs/37178959492/job/111367432799	
validate	pass	16s	https://github.com/mryfmo/dotfiles/actions/runs/37178959529/job/111367409649	
exit status: 0
```

### final state (paginated listings): head, mergeable_state, origin/main, reviews, inline comments, reactions

```text
5168613a5ea297cbe7a101cedb055986bd64c5b2
blocked
8922f13bc370b2a2144184a4a03518015002e2aa	refs/heads/main
chatgpt-codex-connector[bot]	COMMENTED	abf9933f	2026-10-04T03:10:18Z
chatgpt-codex-connector[bot]	COMMENTED	83074eea	2026-10-04T03:26:43Z
chatgpt-codex-connector[bot]	COMMENTED	22efc32c	2026-10-04T03:46:58Z
moriya-fumio-thd	COMMENTED	3ba270d6	2026-10-04T04:23:25Z
moriya-fumio-thd	COMMENTED	3ba270d6	2026-10-04T04:23:27Z
moriya-fumio-thd	COMMENTED	3ba270d6	2026-10-04T04:23:29Z
moriya-fumio-thd	COMMENTED	3ba270d6	2026-10-04T04:23:32Z
moriya-fumio-thd	COMMENTED	3ba270d6	2026-10-04T04:23:34Z
moriya-fumio-thd	COMMENTED	3ba270d6	2026-10-04T04:23:36Z
moriya-fumio-thd	COMMENTED	3ba270d6	2026-10-04T04:23:38Z
moriya-fumio-thd	COMMENTED	3ba270d6	2026-10-04T04:23:40Z
moriya-fumio-thd	COMMENTED	3ba270d6	2026-10-04T04:23:43Z
chatgpt-codex-connector[bot]	COMMENTED	5168613a	2026-10-04T05:11:53Z
4175944623 chatgpt-codex-connector[bot] abf9933f scripts/require-crit-review.py:641 **<sub><sub>![P1 Badge](https://img.shields.io/badge/P1-orange?style=flat)</sub></sub>  Require distinct dispositions for audit findings**
4175944624 chatgpt-codex-connector[bot] abf9933f home/dot_config/claude/rules/pr-integration.md:7 **<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  Document the audit requirement for Codex users**
4175944626 chatgpt-codex-connector[bot] abf9933f scripts/require-crit-review.py:29 **<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  Accept the established bullet-form audit findings**
4175944628 chatgpt-codex-connector[bot] abf9933f scripts/require-crit-review.py:712 **<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  Preserve the .orchestration-only audit exemption**
4175981346 chatgpt-codex-connector[bot] 83074eea scripts/require-crit-review.py:724 **<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  Update the remaining PR-integration instructions**
4175981351 chatgpt-codex-connector[bot] 83074eea scripts/require-crit-review.py:587 **<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  Bind audit evidence to the feedback task**
4176028652 chatgpt-codex-connector[bot] 22efc32c home/dot_config/claude/rules/pr-integration.md:7 **<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  Show the required audit arguments**
4176028656 chatgpt-codex-connector[bot] 22efc32c scripts/require-crit-review.py:597 **<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  Validate the companion last-message path**
4176028658 chatgpt-codex-connector[bot] 22efc32c scripts/require-crit-review.py:618 **<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  Parse fallback transcripts by their final Codex bloc
4176134375 moriya-fumio-thd abf9933f scripts/require-crit-review.py:641 Disposition (orchestrator acceptance): fixed in 83074eea (verified in the PR head diff).
4176134424 moriya-fumio-thd abf9933f home/dot_config/claude/rules/pr-integration.md:7 Disposition (orchestrator acceptance): fixed in 83074eea (verified in the PR head diff).
4176134457 moriya-fumio-thd abf9933f scripts/require-crit-review.py:29 Disposition (orchestrator acceptance): fixed in 83074eea (verified in the PR head diff).
4176134517 moriya-fumio-thd abf9933f scripts/require-crit-review.py:712 Disposition (orchestrator acceptance): fixed in 83074eea (verified in the PR head diff).
4176134582 moriya-fumio-thd 83074eea scripts/require-crit-review.py:587 Disposition (orchestrator acceptance): fixed in 22efc32c (the audit file's <task> must equal the feedback JSON's <task>).
4176134667 moriya-fumio-thd 22efc32c home/dot_config/claude/rules/pr-integration.md:7 Disposition (orchestrator acceptance): fixed in 46f14681 (verified in the PR head diff).
4176134723 moriya-fumio-thd 22efc32c scripts/require-crit-review.py:597 Disposition (orchestrator acceptance): fixed in 46f14681 (verified in the PR head diff).
4176134778 moriya-fumio-thd 22efc32c scripts/require-crit-review.py:618 Disposition (orchestrator acceptance): fixed in 46f14681 (verified in the PR head diff).
4176134896 moriya-fumio-thd 83074eea scripts/require-crit-review.py:724 Disposition (orchestrator acceptance): not-applicable for this PR. T68 is the gate code plus its own rule bullet and its Codex mirror; root 
4176238899 chatgpt-codex-connector[bot] 5168613a scripts/require-crit-review.py:604 **<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  Restore the audit runner's transcript fallback**
```

## Task file revision verification (revise round 2, evidence correction; head stays 5168613a)

### `sha256sum` of the current task file (run for this round)

```text
$ sha256sum /home/moriya/Workspace/dotfiles/.orchestration/tasks/dotfiles-T68-gate-audit-evidence-a01.md
de14890fe72e1f272420bb4ec68845440b46d83bc91bbf213cc52693217dd2a1  /home/moriya/Workspace/dotfiles/.orchestration/tasks/dotfiles-T68-gate-audit-evidence-a01.md
```

This matches the round-2 dispatch `task_rev=sha256:de14890fe72e1f272420bb4ec68845440b46d83bc91bbf213cc52693217dd2a1`.

### Earlier revisions, cited verbatim from this worker's session log (the file has since changed, so they cannot be re-run)

```text
# dispatch (2026-10-04T02:50:29Z), task_rev 3959867c…
$ sha256sum /home/moriya/Workspace/dotfiles/.orchestration/tasks/dotfiles-T68-gate-audit-evidence-a01.md
3959867cdc71c645d78c30576f02abd172cc3e2562d39910a7d2435d068d9c7a  /home/moriya/Workspace/dotfiles/.orchestration/tasks/dotfiles-T68-gate-audit-evidence-a01.md
# PONG decision 1 (2026-10-04T03:16:24Z), task_rev fcbe596a…
$ sha256sum /home/moriya/Workspace/dotfiles/.orchestration/tasks/dotfiles-T68-gate-audit-evidence-a01.md
fcbe596a2cc8c909efb419a81ea42751b2ee2d278414a11937e6cfed6df3c745  /home/moriya/Workspace/dotfiles/.orchestration/tasks/dotfiles-T68-gate-audit-evidence-a01.md
# revise round 1 (2026-10-04T04:56:31Z), task_rev 9e175902…
$ sha256sum /home/moriya/Workspace/dotfiles/.orchestration/tasks/dotfiles-T68-gate-audit-evidence-a01.md
9e17590276236f01de9ee18e68c9fa284c17bb6f5585bf5f8869eeafcb4b8cc3  /home/moriya/Workspace/dotfiles/.orchestration/tasks/dotfiles-T68-gate-audit-evidence-a01.md
```

PONG decision 2 (2026-10-04T03:41:07Z, `task_rev=sha256:7d99160137bdaf60600e8fc83733219c6d8567b586b62079742bc2381fe08692`) was **not** verified with `sha256sum`. Its decision (4175981351 `fixed:22efc32c`; 4175981346 not-applicable to T69) was taken from the dispatch message alone. The report's earlier claim that this revision was verified is corrected there.
