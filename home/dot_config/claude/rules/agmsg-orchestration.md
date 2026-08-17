## agmsg orchestration

- Activate this regime when the operator requests agmsg/Codex collaboration or when the agmsg bus and a resident Codex worker are available; agmsg is then required unless the operator opts out for the current task. Invoke the `agmsg-orchestration` skill immediately for the full protocol. Only after an opt-out may the orchestrator mutate the repository directly.
- Delegate all repository mutations to resident Codex workers. agmsg/herdr control-plane work and evidence-sync bookkeeping are exempt; otherwise the orchestrator is limited to lightweight reads, judgment, tasking, and acceptance.
- Review every RESULT adversarially across correctness, regressions, security, and omissions; try to refute it and independently re-derive findings rather than trusting spot checks.
- Acceptance, adversarial RESULT review, and review-profile work remain Claude-side; never delegate them, and keep `make require-crit-review` as the final integration step, until the worker model surpasses the orchestrator tier.
- At regime/session boundaries, write pending acceptances, verify a consolidated decision for every accepted task, and mechanically commit all `.orchestration` evidence with zero untracked tail. Commit `make upgrade` mise config/lock changes as a separate chore in the same session; never leave that pair dirty across sessions.
