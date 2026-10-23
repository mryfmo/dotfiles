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
| U10 | (pending) | feat/omp-pstack-skills | | in-flight | |
| records | #464 | records/program-store-1 | 54644817 → main 0f0fe4c6 | landed 2026-10-23T04:03Z | n/a (records only) |
