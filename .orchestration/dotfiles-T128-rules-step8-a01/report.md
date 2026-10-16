# T13 amendment 5 implementation snapshot

PR: https://github.com/mryfmo/dotfiles/pull/371
Branch: fix/regime-rules-step8
Previous head: 4d3d639f452e12e22c434ce62f843e0e22dc39e0
Base: 8b25f9ca6d6bc25c21b30f2a67cb462a6dd4a95e
Task-copy SHA256: 4610a9a7c064a5d93fb72b91df73c42390051a1fcb35703a6cf5aed305ef08a9

This commit aligns boundary cadence and includes the round's report, validation, sandbox and learning in the tree, replacing the prior untracked-only handoff. The Stop checklist still commits at every boundary; the boundary PR's auto-merge is queued only while no other PR is between final head and merge. The rule says records reach main only between integrations and binds the checker to the Stop checklist. No date/history enforcement claim or daily count remains in the current rule. The same-day branch suffix is unchanged. These are procedure prose changes, applied to seats on the next operator update/restart; no checker, hook or permission policy is changed.

[memory:decision] Test test_boundary_cadence_is_stated_between_integrations is in AgmsgOrchestrationRuleTest, named by the latest ACCEPTANCE supplement. It pins both operative phrases, failed on the pre-revision source and passes after the exact wording changes. All53 docs tests and render-check pass. The rule is447 words under450. Full PR caps:47 changed source lines under200 and67 test additions under1000. D6's five patterns and AUDIT_DISPOSITIONS are zero in both SKILL and AGENTS.md. One new test method is added to the prior52; the invariants fixture equals its edited section.

This amendment changes two prose files, one existing fixture and one test module, plus task evidence. The complete PR still spans the four original prose files, four fixtures and one test module. Source behavior changes from earlier rounds remain the advisory-P2/one-fix-round procedure, current-mechanism statements and platform-specific sandbox guidance; all included in this local53-test snapshot. Source diffs stay within allowed_files. The new task copy is byte-identical to the dispatched hash; the test name follows the later explicit ACCEPTANCE rename while the canonical task's historical name is preserved.

Audit of4d3d639f: the contradictory cadence and missing regression test are addressed by this amendment; missing/empty committed report, validation, sandbox and learning are addressed in this commit. INV-6/D-S2-371 is orchestrator/operator-owned; no worker waiver. Prior BotP2 comment4289271574 was fixed4d3d639f (thread PRRT_kwDOSMyAV86tAMt-), then code review completed without new findings on that old head; that old review is not current-head coverage. New commit SHA, CI/Bot findings and dispositions are reported by RESULT after publication. No merge-ready claim here.

No installed apply/restart, local bats, new dependency, graph update, mechanism edit, merge or worker thread resolution. Main-checkout CompactionDB consolidation and final integration sweep/audit/gate remain orchestrator-owned.

cost: n/a
