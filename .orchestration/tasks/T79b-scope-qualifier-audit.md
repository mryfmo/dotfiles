# T79b: kept-core 限定子脱落の是正と全数再監査 (PR #137 review)

task_id: T79b
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-conformance
worker: codex-deep-dot
plan: PLAN-pi-pivot.md (Phase 6; PR #137 review finding)
depends: T79 (accepted)

[memory: decision — Two-tier slimming must preserve every scoping qualifier in kept-core clauses: the regime activation condition is repository-scoped ("a resident Codex worker exists for this repository"), and the defect class "tightening dropped a qualifier" is closed by re-auditing every kept-tightened clause against its pre-edit wording, not by patching the single reported instance.]

## Finding (chatgpt-codex-connector, P1, orchestrator-triaged REAL)

The slim rule activates the regime when "the agmsg bus and a resident
Codex worker are available" — the pre-edit wording scoped the worker to
"this repository". With a worker resident only for another repo, the
slim rule would activate the regime and then forbid direct mutation
while delegation is impossible. The skill retains the correct scoped
condition, but it loads only after activation.

## Fix (exact, root-cause = defect class, not the instance)

1. home/dot_config/claude/rules/agmsg-orchestration.md: restore the
   repository scoping in the activation bullet ("... or when the agmsg
   bus and a resident Codex worker for this repository are available").
   Keep the wording minimal; re-measure with the T77 estimator (core
   stays <=360 tok).
2. RE-AUDIT every T79 mapping row marked "kept core" or "kept core in
   tightened form" (and the T80 kept rows whose wording was shortened):
   diff each kept clause's post-edit wording against the pre-edit
   clause; list every dropped qualifier (scope, ordering, exclusivity,
   condition). Fix any additional drops the same way. Record the audit
   table (clause -> qualifier status) in the validation artifact.
3. Gates: make format / validate-agent-assets / unit-test.

## Allowed files

home/dot_config/claude/rules/agmsg-orchestration.md,
home/dot_config/codex/AGENTS.md (only if the audit finds a dropped
qualifier there), artifact paths (T79b set).

## Forbidden actions

git commit; git push; chezmoi apply; bats; re-growing moved detail into
the rule; touching the skill.

## Completion / RESULT contract

Five artifacts; memory add; effects=none; cost line.
Reply `AGMSG-RESULT v1 task_id=T79b`. max_turns=12.
