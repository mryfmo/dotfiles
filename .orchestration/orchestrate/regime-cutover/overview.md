# Overview (append-only PR and issue DB)

## Existing PRs and branches the program builds on (gh, 2026-10-23T01:09Z)

- #406 draft `tools/omp-config-render` head 2e978db7 "feat(agents): render omp's default model role from the manifest (T129 omp-config-render a01)": files `home/.chezmoitemplates/omp-config-managed.yml`, `home/dot_omp/agent/modify_config.yml`, `scripts/generate-agent-configs.py`, `home/dot_agents/agent-config.yaml`, `home/dot_agents/README.md`, `home/dot_agents/model-profiles.env`, tests. Picked up by U4.
- #407 draft `tools/hcom-dispatch-bus-a01` head dfa9001b: records only (a01 findings). The a02 worktree branch `tools/hcom-dispatch-bus-a02` (d961efa3) is records only. U5 starts a fresh branch `feat/hcom-dispatch-bus` and reads both reports.
- Open PRs of the former regime (19, per the project map 2026-10-23 08:31 JST) are not touched by this program; close-or-carry is a coordinator decision at the end (gates).

## Program PRs

| unit | PR | branch | head | state | verdict |
| --- | --- | --- | --- | --- | --- |
| U3 | #458 | feat/openai-siwc-extension | 0f9cfdf5 → main 8846f34b | landed 2026-10-23T03:48:01Z | unit-test-verified (round 2) |
| U4 | #406 | tools/omp-config-render | d661a9f4 → main 34e216e9 | landed 2026-10-23T03:48:01Z | unit-test-verified |
| U5 | #460 | feat/hcom-dispatch-bus | 940d05b7 → main a39ce5d6 | landed 2026-10-23T02:00:14Z | unit-test-verified |
| U6 | #459 | feat/omp-seat-policy | f201d2fe → main 6f154b60 | landed 2026-10-23T02:49:41Z | unit-test-verified |
| U8 | #463 | feat/omp-run | d4dd2b16 → main | landed 2026-10-23T03:55:09Z | unit-test-verified |
| U2 | #461 | feat/pi-claude-bridge-asset | c4d18653 → main a729702e | landed 2026-10-23T04:23Z | live-verified (operator install + PONG) |
| U13 | #462 | feat/regime-ci-program-marker | 62f0f15d → main 3953e9cf | landed 2026-10-23T03:06:51Z | unit-test-verified |
| U7 | (pending) | feat/hcom-seat | | in-flight | |
| U10 | #465 | feat/omp-pstack-skills | 50a11a7c → main | landed 2026-10-23T04:36:23Z | unit-test-verified |
| records | #464 | records/program-store-1 | 54644817 → main 0f0fe4c6 | landed 2026-10-23T04:03Z | n/a (records only) |
| records 2 | #467 | records/program-store-2 | b8742836 | auto-merge armed (the store itself, missed by #464) | n/a (records only) |
| U14 | #468 | feat/omp-role-overlays | 99ddf5cc → main | landed 2026-10-23T05:35:30Z | unit-test-verified |
| U7 | #466 | feat/hcom-seat | ccc40eae → main c67d4d0b | landed 2026-10-23T05:58:55Z | unit-test-verified |
| U9 | #469 | feat/orchestrator-seat | af35fd50 → main | landed 2026-10-23T05:57:12Z | unit-test-verified |
| U7c | #470 | fix/hcom-seat-go | d7ea7262 → main 8e55aedd | landed 2026-10-23T06:40:24Z | unit-test-verified; live: hcom-seat started the seats at X7 relaunch and final X |
| U6b | #471 | fix/audit-seat-reply-route | f95738b4 → main 844b047e | landed 2026-10-23T07:3xZ | unit-test-verified; live: audit VERDICT row 47 |
| U9b | #472 | fix/stop-gate-audit-verdict | 12b27b3d (U9c) → main a3526828 | landed 2026-10-23T08:40:55Z | unit-test-verified; gate rule not yet live-measured |
| U10b | #473 | feat/pstack-skills-asset | 81a48c2a → main f0bbb5d6 | landed 2026-10-23T10:50:09Z | unit-test-verified; live: 82 skills, poteto-mode hidden in both profiles |
| U9d | #475 | fix/audit-worktree-positioning | a4d1045f → main 4f004231 | landed 2026-10-23T12:30Z | unit-test-verified; live: the positioning step moved the audit tree before rows 122 |
| U14b | #476 | fix/omp-overlays-no-wizard | ac7a4e0f → main 28b2855c | landed 2026-10-23T12:1xZ | unit-test-verified; live: 0 wizard lines in the three relaunched panes |
| U6c | #477 | fix/audit-policy-name | 3809e407 (U6d) → main 994c3616 | landed 2026-10-23T13:57Z | unit-test-verified; live: audit VERDICT row 122 through hcom-reply |
