# Acceptance: dotfiles-T94-upgrade-pins-a01

- **Decision:** ACCEPTED. PR #250 squash-merged to `main` as `0ea5948b` (head `6f5c776cf04615b0a2162fd64ca6ab675be2b82a`, one commit on main f32f33a0). Merged without `--delete-branch`; worker-c holds `chore/upgrade-pins-2026-10-04`.
- **Worker:** `claude-standard-dot-a005` (worker-c). task_rev matched. Dispatched right after its T71 RESULT; disjoint from T71/T88/T92.
- **Exemption declared:** acceptance and final integration. The orchestrator captured the operator's `make upgrade` diff from the canonical clone (`~/.local/share/chezmoi`, dirty since c6de5156) as `.orchestration/tasks/dotfiles-T94-pending-pins.patch` (evidence-sync bookkeeping) and fast-forwarded that clone to f32f33a0 with the diff preserved; it mutated no repository code.
- **Plan reference:** regime rule (pending pin diff travels as one class-pure PR), outside the numbered phases.

## What was accepted (6 files, +18/−18)

- mise `v2026.9.13` → `v2026.9.14`; aws-cli `2.37.3` → `2.37.4`; crit `v0.21.0` → `v0.21.1` with four platform sha256 values; claude-code `2.1.287` → `2.1.288`; pnpm `12.6.0` → `12.7.0` (manifest, mise config/lock, rendered `install/common/mise.sh`, `install/ubuntu/common/aws_cli.sh`, `scripts/lib/installer-pins.sh`).
- `git apply --3way` applied all six files with no hand edit; render-check exit 0; no test pinned an old value; crit checksums match upstream.

## Orchestrator re-derivation

- The PR diff equals the saved patch line for line (36 changed lines compared programmatically).
- CI: 16 checks pass on 6f5c776c; Codex Bot thumbs-up, no thread; mergeable CLEAN (sweep JSON).

## Audit / Bot / sweep / gate

| scope | verdict |
|---|---|
| task-level, final head 6f5c776c | incorrect (1, evidence only) |

audit-finding: 1 validation file replaces the CI/Bot/mergeability commands with prose and truncates the unit-test output → not-applicable:evidence-only finding with no implementation defect; the orchestrator re-derived CI (16 checks pass), the Codex thumbs-up and the clean mergeable state from the live sweep JSON and compared the diff with the saved patch line for line; the worker pastes the raw outputs into the validation file as an artifact correction that does not move the head

- Sweep (head 6f5c776c): 6 items, 0 failure/warning, all dispositioned. Gate at 6f5c776c with `AUDIT_EVIDENCE` and `AUDIT_DISPOSITIONS=<this record>`: exit 0, evidence copies removed.

## Follow-ups

- Canonical clone: after the merge, discard its now-redundant working-tree pin diff (`git checkout -- <6 files>`), pull, and run `make update` so `~/.config/mise` and the installers match main.
- Recurring evidence-only audit findings (T68, T88, T91, T92, T94): the worker task template's "paste verbatim output" needs a mechanical check; candidate for T69/T83 (SKILL) and a validator rule.

## CompactionDB

- Worker decision `ae1d260b-0507-4e32-ab4a-260d5a92ded1`; cited.
