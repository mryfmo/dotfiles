# T13 amendment 6: Bot rounds count reviews

PR: https://github.com/mryfmo/dotfiles/pull/371
Branch: fix/regime-rules-step8
Previous head: 61dbd68e6bb72b1bc0420f3e1b93b7c064fdbce3
Base: 8b25f9ca6d6bc25c21b30f2a67cb462a6dd4a95e
Task-copy SHA256: 03544af5abdfc292683383f0548109254e3928b92528dd3cb927126bb9f65c66

[memory:decision] bot_rounds counts Bot reviews. A P0/P1 surviving one fix round has two reviews (initial and re-review), so Worker Playbook15 and Message Contract now require bot_rounds=2. The one-fix-round limit, operator stop and all gate/merge controls are unchanged. Both fixed fixtures and two existing test assertions use2. The task copy's Completion clause agrees with the dispatched amended bytes; historical task Change sections retain their prior text. This fixes BotP2 comment4290644781 (https://github.com/mryfmo/dotfiles/pull/371#discussion_r4290644781); RESULT names the fix SHA after commit. Worker does not reply or resolve threads.

Actual discriminating check AgmsgRegimePatternTest.test_step_10_states_the_advisory_p2_policy failed before the prose correction and passes afterward. All53 docs tests, render-check and native test formatting pass. The initial ACCEPTANCE supplied the unchanged cadence selector; after the worker reported the mismatch, the 03:47:05Z ACCEPTANCE corrected check to the actual count test and regression_check to AgmsgOrchestrationRuleTest.test_boundary_cadence_is_stated_between_integrations. revise.yaml now matches that corrected message. Both selectors pass in the full run. No added test methods. Full PR caps47 changed source lines/67 test additions, rule447words under450; D6 and retired name zero. Current root validation contains actual outputs, not old-head CI claims.

Four nonempty root report/validation/sandbox/learning files remain committed with this revision. Prior cadence/check/evidence omissions were fixed61dbd68e; prior BotP2 checker-enforcement claim4289271574 fixed4d3d639f. The revised full PR still covers four prose files, four fixtures and one test module; this delta changes only SKILL, worker-step15/message-contract fixtures, the existing test module and task evidence. No mechanism, permission policy or installed state changes. Source text changes seat instructions after the operator applies and restarts.

This is the implementation snapshot. Its new commit SHA and final-head CI/Bot are recorded separately after publication; earlier61dbd68e has the now-fixed BotP2 and does not prove current-head approval. INV-6/D-S2-371, main-checkout CompactionDB consolidation and final sweep/audit/gate/acceptance remain orchestrator/operator-owned, with no worker waiver. No local bats, dependency, graph update, apply/restart or merge.

cost: n/a
