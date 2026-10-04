# Acceptance: dotfiles-T71-generator-multi-target-a01

- **Decision:** ACCEPTED after two revise rounds. PR #249 squash-merged to `main` as `65915b93`; final head `ef4324d03bb451fe9fde60e1643714ac065bdbf5` (substantive commits 1ea56252, 383ebbae, 3ecb4876, f03505f3, ef4324d0; base 312fef3f; update-branch merges 001affb1 onto f32f33a0 and c7b5fb3d onto 0ea5948b). Merged without `--delete-branch`; worker-c holds `feat/generator-multi-target`.
- **Worker:** `claude-standard-dot-a005` (worker-c). task_rev chain matched. Parallel wave with T88 (a006) and T92 (a007); the worker also ran T94 between rounds.
- **Exemption declared:** acceptance and final integration; the orchestrator mutated no repository code.
- **Plan reference:** Phase 3, dotfiles-T71 (principle 3: one pin, several render targets).
- **Routing note:** the worker edited `scripts/generate-agent-configs.py` before T88's seat-boundary routing rule merged; from T88 on, renderer edits go to a Codex worker or the operator.

## What was accepted (4 files)

- `render_asset_constants`: `render:` is one `{file, constants}` mapping or a list; `readonly` and `declare -r` assignments are rewritten; exactly-once per (file, constant); one snapshot per resolved real file so alias and target entries never lose a write (round 2).
- `validate-agent-assets.py`: `declare -r` literals recognised; render entries shape-checked; one canonical relative spelling per render target; conflicts keyed on the resolved real path (round 1); scanned roots unchanged (T72 adds `setup.sh`).
- Tests: list render, `declare -r`, conflict rejection, canonical paths, fixture-symlink conflict, alias snapshot; 758 tests; `make render-check` exit 0.

## Decisions taken during the rounds

- Codex P2s: conflicting mappings (383ebbae), canonical paths (3ecb4876), symlink aliases (first not-applicable, withdrawn after the task-level audit reproduced the overwrite; fixed in f03505f3); unquoted `declare -r` and alias-aware literal scan not-applicable (the renderer only ever rewrote double-quoted assignments and fails loudly; the rendered set stays on the canonical spelling by design; no render target is a symlink).
- Round 2 (audit of c7b5fb3d): `outputs` keyed by unresolved path lost a write through an alias → one snapshot per real file (ef4324d0).

## Orchestrator re-derivation

- Read the generator and validator diffs at each head; confirmed the conflict map and snapshot map both key on `(ROOT / file).resolve()` and that the rendered set keeps the canonical spelling; `make render-check` exit 0 on the final head (worker, verbatim); CI green; mergeable CLEAN after the last thread.
- Side incident reported by the worker during the T94 artifact correction: a repo-wide `git worktree prune` removed the admin entries of two stale worktrees (`worker-b`, `env-converge-T10`, whose directories no longer existed); live worktrees intact. Recorded; no action.

## Audit / Bot / sweep / gate

| scope | verdict |
|---|---|
| task-level, final head ef4324d0 | incorrect (1, evidence only) |
| task-level, c7b5fb3d | incorrect (1) → fixed in ef4324d0 |
| task-level, 3ecb4876 | incorrect (3) → fixed in f03505f3 and the artifacts |

audit-finding: 1 validation file claims path normalization prevents writes outside the checkout, but a canonical symlink to an external file passes and the generator follows it → not-applicable:evidence-only overclaim with no code defect; the normalization is lexical path validation and this record states so; the worker narrows the sentence in the validation file as an artifact correction that does not move the head; symlinked render targets do not exist in this repository and the T72 scan roots cover install/, scripts/ and setup.sh

- Codex Bot: six threads; three fixed in-PR, two not-applicable, one withdrawn-then-fixed; all replied and resolved. Sweep (head ef4324d0): 26 items, 0 failure/warning, all dispositioned. Gate at ef4324d0 with `AUDIT_EVIDENCE` and `AUDIT_DISPOSITIONS=<this record>`: exit 0, evidence copies removed.

## Follow-ups

- T72 adds `setup.sh` and `scripts/lib` to the scanned roots with the chezmoi-bootstrap asset; T93 (gate masked bodies, NUL scan) and T77 follow sequentially on the validator.

## CompactionDB

- Worker decision `ae8fe450-a4a4-46f5-be5e-5c72fc52220f`; cited.
