---
task_id: dotfiles-T128-s1-replan-gate-a01
status: final
---

Both S1 checks now use the same version-independent definition: a word is a maximal ASCII letter run [A-Za-z]+, with exact case-sensitive comparison against specification/design/implementation/verification. Every other character, including Unicode letters, digits and underscores, separates words. jq scan and Python re.findall each contain that regex once; header comments name their twin. This explicitly implements operator decision D-S1-382-A and the authorized C-59 re-plan, replacing the previous Unicode-table-dependent grammar.

Branch fix/s1-replan-gate, PR https://github.com/mryfmo/dotfiles/pull/382. Revision previous_head4460d525612b8869f852d2a1d23160c54c272ae4; current GitHub base58303c37a2ac7854ba7f8d4032b5ee2b9c28776e. Original dispatch basef7847616970d6bd83739a75a65ad8f7c35e91462 and prior implementation/evidence heads are historical. Against current GitHub base: scripts/regime-counters.sh13 additions+6 deletions and scripts/require-crit-review.py11 additions =30 source changed lines<=200; test additions61+72+2 fixture=135<=1000. No new script, dependency, workflow, config, reader API or interpreter change.

Round3 changes only those two regexes/header comments, one test method per existing module and task evidence. The shared fixture and every existing test method, including the six original S1 tests, are unchanged from4460d525 (AST comparison and byte comparisons recorded). The original task's S1 behavior remains: counters print re-plan present/missing for non-advisory classes at three rows, gate refuses a missing re-plan, exact class prefix is required, and S6 still sees every class including advisory-p2.

Finding dispositions proposed for orchestrator integration:
- 4301061412, local:4460d52:1 and audit:4460d52:1: fixed by this revision's publishing commit, identified in RESULT-round3. The old advisory owner proposal/no-source-fix statements are historical and superseded by the explicit re-plan authorization. No worker reply or thread resolution.
- audit:4460d52:2/3/4: orchestrator-owned process findings addressed/dispositioned in the main acceptance record; no worker edit to those records. revise.yaml preserves the old evidence-only directive as historical and adds the exact current previous_head, two failing-test selectors and re-plan reference.

Required regressions:
- tests.unit.test_regime_counters.RegimeCountersTest.test_s1_replan_words_are_ascii_letter_runs: U+1C89 adjacent to design with all four words prints present; verification missing prints missing.
- tests.unit.test_require_crit_review.ReviewGuardTest.test_s1_replan_words_are_ascii_letter_runs: the same two texts are accepted/refused respectively. Both positive subcases failed before the regex change; both tests now pass inside the full suite.

The six original S1 test methods are test_s1_reports_replan_present_for_the_class, test_s1_reports_replan_missing_without_a_complete_matching_line, test_s1_excludes_advisory_p2_at_three_rows (counter module), test_s1_class_at_three_without_a_replan_line_is_refused, test_s1_class_at_three_with_all_replan_words_is_accepted and test_s1_class_at_three_with_a_missing_replan_word_is_refused (guard module).

All128 tests in the two requested modules pass in84.935s. ShellCheck, shfmt, Ruff format, shared-fixture Prettier and source/test whitespace pass. Process-only signing override permits temporary fixture commits; no persistent Git config change. Tests use synthetic histories and stub GitHub responses, never the live store or merge operations. No local Bats. The changed grammar intentionally treats non-ASCII characters and digits/underscore as separators; that behavior is the operator's specification, not an accidental compatibility claim.

Crit reports no review file or daemon. The explicit AGENTS.md fallback is a fresh independent read-only security-profile review (manifest gpt-6-astra/high) of the incremental scripts/tests. Its complete transcript, resolved JSON record and receipt are committed with current evidence; parent reads both transcript and JSON before the worker gate. Historical records are retained as checkpoint approvals and do not certify the new revision. This worker gate is process evidence; integration sweep/audit/acceptance/dispositions/merge stay with the orchestrator.

This final record binds to the source SHA-256 below and the publishing commit containing it. All13 checks of previous_head4460d525 are historical; the exact new publishing head, final-head CI watcher result and Bot re-review are named after push in RESULT-round3 and raw round3-ascii logs. Future external observations and the self-referential publishing hash are not embedded by another head-changing commit. Canonical task/report/validation/sandbox/learning/autoskill, updated final supplement pointers, revise.yaml, reviewJSON and receipt are committed before RESULT. Worklogs/raw duplicate outputs are not committed.

Source SHA-256:
- scripts/regime-counters.sh: 3d6aa8bbebe8b365a525527001270984cade93c08cca4d72a6b8a594f2995ad3
- scripts/require-crit-review.py: eac3d98c77207ba5665d60ec2d4bfe25957d75a1a1c446affd1a1a19e078d356
- tests/unit/test_regime_counters.py: 91f937c23fe48284464121cc1b41b08a1725586c3ee51c8355ca35f4e0d29b27
- tests/unit/test_require_crit_review.py: 12b46cc3f55beadd5f29dc8c6e56a90ab6e9743da5fa4b1d29af5823c70c8117
- tests/fixtures/gate-evidence/acceptance-s6-present.md: 165bc935eaf40dd3752142ffb38957649795a91ec7035fd4f6bcad3c59cb806d

Task copy SHA256:072564c75c137fffd42d54a6d7bcf86dcd7917e49cc3fa2ae6bf8a0b0ce8072e (byte-identical). No permission escalation, live process probes, browser/daemon, Crit web/server, Plan Mode, graph update, AutoSkill or memory promotion. Stale graph queried, targeted rg used; no hook fired. Earlier branch375/379/383 work remains preserved. PR379's independent observers may finish while this branch is active; its RESULT names its preserved02fdf061 commit and committed evidence, never the current382 tree.

cost: n/a
