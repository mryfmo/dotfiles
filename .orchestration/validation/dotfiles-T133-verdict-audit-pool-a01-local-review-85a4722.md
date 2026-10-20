---
task: dotfiles-T133-verdict-audit-pool-a01
head: 85a472294d0c10835bd7235e3c76d045846a6ed9
pr: 410
base: 68f8a70abdf523eba5a72305540ab71d50e3a029
started: 2026-10-18T09:21:51Z
finished: 2026-10-18T09:29:06Z
findings: 6
engine: codex review --base main (profile review, read-only)
---

- [P1] Count open P0/P1 findings instead of joining their IDs — scripts/orchestrator/verdict.sh:142-144
- [P1] Pin interpreter selection before allowing --apply — scripts/orchestrator/verdict.sh:91-93
- [P2] Bind saved dispositions to the current PR head — scripts/orchestrator/verdict.sh:149-150
- [P2] Count undispositioned feedback even when its URL is null — scripts/orchestrator/verdict.sh:151-153
- [P2] Preserve distinct feedback items that share a URL — scripts/orchestrator/verdict.sh:150-151
- [P2] Validate disposition contents rather than their prefixes — scripts/orchestrator/verdict.sh:151-152

```text
The verdict logic can accept unresolved P1 findings and missing, stale, or invalid feedback dispositions. Targeted read-only checks reproduced these bypasses; full unit tests were not run in the read-only sandbox.

Full review comments:

- [P1] Pin interpreter selection before allowing --apply — scripts/orchestrator/verdict.sh:91-93
  A PR checkout that changes `.python-version` and adds an executable outside the checked directories passes this guard. Subsequent `uv run` calls can execute that PR-controlled interpreter before the verdict is determined; `--offline`, `--no-project`, and Python's `-I` do not prevent interpreter selection. Pin the interpreter and environment as `orch-gate.sh` does. The interpreter/environment residual does not mitigate this trust boundary ([AGENTS.md:78](AGENTS.md#L78)).

- [P1] Count open P0/P1 findings instead of joining their IDs — scripts/orchestrator/verdict.sh:142-144
  The audit schema permits an empty finding ID. An unfixed P1 finding with `id: ""` produces an empty `a7`, making condition 7 pass. If that finding has records scope, condition 3 also passes even with an incorrect audit, allowing acceptance with an unresolved P1. Check the number of matching findings independently of the diagnostic IDs.

- [P2] Count undispositioned feedback even when its URL is null — scripts/orchestrator/verdict.sh:151-153
  `pr-feedback.py` permits commit statuses with a null `target_url`. If such a status lacks a disposition, this expression produces `[""]`, whose joined diagnostic is empty, so condition 4 passes. Count missing items before formatting their URLs; otherwise undispositioned statuses bypass the [per-item integration requirement](home/dot_config/claude/rules/pr-integration.md#L4).

- [P2] Preserve distinct feedback items that share a URL — scripts/orchestrator/verdict.sh:150-151
  `pr-feedback.py` assigns every annotation on a check run the same run URL. `from_entries` keeps only the last disposition for that URL, so a disposition on the last annotation also approves earlier annotations whose dispositions are empty. Match complete item identities and preserve multiplicity, as `missing_feedback()` already does, to enforce the [per-item integration requirement](home/dot_config/claude/rules/pr-integration.md#L4).

- [P2] Bind saved dispositions to the current PR head — scripts/orchestrator/verdict.sh:149-150
  After a new push, the saved feedback file from the previous head still passes condition 4 whenever the feedback URLs remain unchanged. Neither its `head_sha` nor the fresh sweep's head is compared with the head being accepted. Require both documents to match that head before reusing dispositions, consistent with the [head-specific integration rule](home/dot_config/claude/rules/pr-integration.md#L3).

- [P2] Validate disposition contents rather than their prefixes — scripts/orchestrator/verdict.sh:151-152
  For a normal nonempty URL, `not-applicable:; evidence=` passes this predicate despite containing neither a reason nor an evidence command. Likewise, any hexadecimal `fixed:` value passes without identifying an existing fix commit. Reuse the existing disposition and commit validation instead of this approximation, so condition 4 enforces the [required root-cause dispositions](home/dot_config/claude/rules/pr-integration.md#L4).
The verdict logic can accept unresolved P1 findings and missing, stale, or invalid feedback dispositions. Targeted read-only checks reproduced these bypasses; full unit tests were not run in the read-only sandbox.

Full review comments:

- [P1] Pin interpreter selection before allowing --apply — scripts/orchestrator/verdict.sh:91-93
  A PR checkout that changes `.python-version` and adds an executable outside the checked directories passes this guard. Subsequent `uv run` calls can execute that PR-controlled interpreter before the verdict is determined; `--offline`, `--no-project`, and Python's `-I` do not prevent interpreter selection. Pin the interpreter and environment as `orch-gate.sh` does. The interpreter/environment residual does not mitigate this trust boundary ([AGENTS.md:78](AGENTS.md#L78)).

- [P1] Count open P0/P1 findings instead of joining their IDs — scripts/orchestrator/verdict.sh:142-144
  The audit schema permits an empty finding ID. An unfixed P1 finding with `id: ""` produces an empty `a7`, making condition 7 pass. If that finding has records scope, condition 3 also passes even with an incorrect audit, allowing acceptance with an unresolved P1. Check the number of matching findings independently of the diagnostic IDs.

- [P2] Count undispositioned feedback even when its URL is null — scripts/orchestrator/verdict.sh:151-153
  `pr-feedback.py` permits commit statuses with a null `target_url`. If such a status lacks a disposition, this expression produces `[""]`, whose joined diagnostic is empty, so condition 4 passes. Count missing items before formatting their URLs; otherwise undispositioned statuses bypass the [per-item integration requirement](home/dot_config/claude/rules/pr-integration.md#L4).

- [P2] Preserve distinct feedback items that share a URL — scripts/orchestrator/verdict.sh:150-151
  `pr-feedback.py` assigns every annotation on a check run the same run URL. `from_entries` keeps only the last disposition for that URL, so a disposition on the last annotation also approves earlier annotations whose dispositions are empty. Match complete item identities and preserve multiplicity, as `missing_feedback()` already does, to enforce the [per-item integration requirement](home/dot_config/claude/rules/pr-integration.md#L4).

- [P2] Bind saved dispositions to the current PR head — scripts/orchestrator/verdict.sh:149-150
  After a new push, the saved feedback file from the previous head still passes condition 4 whenever the feedback URLs remain unchanged. Neither its `head_sha` nor the fresh sweep's head is compared with the head being accepted. Require both documents to match that head before reusing dispositions, consistent with the [head-specific integration rule](home/dot_config/claude/rules/pr-integration.md#L3).

- [P2] Validate disposition contents rather than their prefixes — scripts/orchestrator/verdict.sh:151-152
  For a normal nonempty URL, `not-applicable:; evidence=` passes this predicate despite containing neither a reason nor an evidence command. Likewise, any hexadecimal `fixed:` value passes without identifying an existing fix commit. Reuse the existing disposition and commit validation instead of this approximation, so condition 4 enforces the [required root-cause dispositions](home/dot_config/claude/rules/pr-integration.md#L4).
```
