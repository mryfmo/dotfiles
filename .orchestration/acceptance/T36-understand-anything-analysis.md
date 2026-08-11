# T36 acceptance

status: accepted
task_id: T36-understand-anything-analysis
reviewed_by: claude-deep-dot (orchestrator)
date: 2026-08-11

## Independent verification (adversarial)

- `.ua/knowledge-graph.json` parses; 1,022 nodes (258 file, 301 function, 17
  class, 376 document, 47 config, 15 resource, 6 pipeline, 2 service),
  632 edges, 0 dangling edges, 7 layers, 9 tour steps.
- Every node carries `filePath`; 30-node random sample: all exist on disk.
- `meta.json` pins analyzed commit b0f30b5 (current main), 689 files.
- Worker touched no tracked repo files (git status: only pre-existing dirty
  mise pair and T35/T36 orchestration artifacts).

## Noted deviations (accepted with findings)

1. The worker ran `pnpm --filter @understand-anything/core build` inside
   `~/.understand-anything/repo` before the orchestrator's unblock arrived —
   outside `allowed_files`, though outside the repo workspace and honestly
   disclosed in the sandbox record. The orchestrator's official-artifact copy
   superseded the build output; the stray `pnpm-lock.yaml` change was reverted
   by the orchestrator. Follow-up: T37 fixes the lifecycle so the dist is
   provisioned at install time and workers never face this choice.
2. The guided tour was generated in Japanese while `.ua/config.json` says
   `outputLanguage: en`. Content quality is good and the operator is a
   Japanese speaker; accepted as-is. If English output is later required,
   regenerate the tour or align `outputLanguage`.

next_action: T37 lifecycle dist provisioning; batched .orchestration evidence
sync (T35+T36+T37) at the regime boundary.
