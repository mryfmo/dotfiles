---
reviewed_at: 2026-10-10T22:06:21Z
reviewer: claude-review-dot-a001
profile: review
session: 2089b04f-f9c7-498b-86c5-76f2140048d5
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@6eedc15f74d9a150a601190e3fb839175be3799c2eadf37331f850430c930210
task: dotfiles-T128-task-review-v1-v2-a01
round: 3
previous: .orchestration/validation/dotfiles-T128-task-review-v1-v2-a01-round2.md
files:
  - dotfiles-T128-v1-task-schema-a01@70a4a7abd656df5b8c0f423062762881fdc00a7908606020c63fa8f412955f35
  - dotfiles-T128-v1c-regime-ci-check-a01@f1fa2a3ca4f65757ec1e8996b97b974963b440bf25d9f9e9d1ad79d49b7c36be
  - dotfiles-T128-v1b-pr-caps-a01@121cf591817c6faeec79d8f986d248c463f4e12729de3aaed019436a621b253c
  - dotfiles-T128-v2-audit-schema-and-runner-a01@745c85c102521cd839e551f1d145f0bf3fd9ef8d75eae01db3fb576c2502d55a
verdicts:
  dotfiles-T128-v1-task-schema-a01: ready
  dotfiles-T128-v1c-regime-ci-check-a01: "revise: V1c-1 test location for the process_tiers rule, V1c-2 one task.md per PR"
  dotfiles-T128-v1b-pr-caps-a01: ready
  dotfiles-T128-v2-audit-schema-and-runner-a01: ready
---

# Task-file review round 3: V1 (split), V1c (new), V1b and V2 (pointer change)

Mechanical check with PyYAML: each file's one invariant equals design v4's byte for byte, each key equals the design's map entry, and every receipt pointer names the round-4 receipt. Touch points re-checked for V1c: the word-budget test in tests/unit/test_agmsg_orchestration_docs.py:81-83 caps the rule file (447 of 450 words) and the always-loaded rules, not the SKILL, and none of these tasks edits a rule file; astral-sh/setup-uv is SHA-pinned in agent-assets.yml:30; no test enumerates the manifest's top-level keys; README has the "Agent review and permission assets" section (README.md:281).

## V1 (dotfiles-T128-v1-task-schema-a01): ready

Five files, validation only; the process_tiers lookup is deferred to V1c (line 46) and V1c lists scripts/validate-task.py for it. Size is under the cap by construction (schema, validator and module at most 320 lines outside tests and the data list). Notes: line 34 still says "gate script and workflow"; the design-file fixture (line 47) has no fixtures path in allowed_files, so it lives inline in the test module or as a copy the test writes to a temporary directory, which the task could say in four words.

## V1c (dotfiles-T128-v1c-regime-ci-check-a01): revise

1. Scope and sentence: the CI half of INV-1, verbatim, map [INV-1]; nothing from another wave except audit_budget_usd per tier (line 47), which is INV-9's field added early because V2 reads it; say so in one clause so V5b owns the rest of the budgets.
2. allowed_files: complete for regime-check.sh, the workflow, the manifest, the validator's lookup and the prose; render-check is named. Caps: seven files, about 200 added lines outside tests/. V1c-1: item 3 adds a rule to scripts/validate-task.py (a missing process_tiers table is a failure) and INV-12 wants a test that fails when the rule is removed, but tests/unit/test_validate_task.py is not in allowed_files and item 6 lists only regime-check cases; either name the test in tests/unit/test_regime_check.py (it already drives the validator as a subprocess) or add test_validate_task.py to allowed_files.
3. Premises: the four hold (GitHub pages, test.yaml:5, the grep at validate-agent-assets.py:719, the workflow_dispatch sentence), all re-run in rounds 1 and 2. None missing.
4. Routing: Claude seat; regime.yml, the scripts, the manifest's new top-level key and prose are no Claude-boundary source; PR 313 edited the manifest from a Claude seat.
5. Ponytail: thin workflow, decisions in one script, V1's validator reused. V1c-2 (worker question): steps (a) and (b) say "the PR's task.md"; state that a PR carries exactly one .orchestration/<id>/task.md (a second is refused), and that a PR that changes .github/workflows/** with no task.md is refused by (b), while an .orchestration/-only PR with no task.md passes.
6. Contradictions: none with the design; the dry-run sequence (line 53), the discipline (line 45) and the first-commit copy (line 57) match. INV-1's hashed sentence says "V1's acceptance record" for the ruleset action; V1c's acceptance record carries it (noted in the round-4 design receipt).

## V1b (dotfiles-T128-v1b-pr-caps-a01): ready

Receipt pointer round 4; "dispatched after V1c merges" (line 27). Note: line 32 still says "scripts/regime-check.sh (V1's)"; it is V1c's.

## V2 (dotfiles-T128-v2-audit-schema-and-runner-a01): ready

Receipt pointer round 4; the audit_budget_usd default of 5 (line 50) matches what V1c adds to the manifest.
