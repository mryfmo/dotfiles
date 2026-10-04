# Acceptance: dotfiles-T92-stop-gate-sandbox-placeholders-a01

- **Decision:** ACCEPTED after two revise rounds. PR #248 squash-merged to `main` as `f2b5c115`; final head `3371cc818276df49ceeae78c17f3f16d7661375e` (substantive commits cbbd26cd, 776cbfec, 5d4928fb, 68d8e142, bbd3d3fb, adca1e6b, 153a647d, 8535b3f3, a8a87bd9; update-branch merges onto 0ea5948b and 65915b93). Merged without `--delete-branch`; worker-e holds `fix/stop-gate-sandbox-placeholders`.
- **Worker:** `claude-standard-dot-a007` (worker-e). task_rev chain matched. Urgent follow-up to T65, dispatched the moment the live gate blocked the orchestrator's Stop.
- **Exemption declared:** acceptance and final integration; the orchestrator mutated no repository code.
- **Plan reference:** T65 follow-up (the gate must not block on Claude Code sandbox placeholders), outside the numbered phases.

## What was accepted (`scripts/agent-stop-gate.sh`, `tests/unit/test_agent_stop_gate.py`)

- The orchestrator seat's dirty-tree loop skips an untracked entry only when it is a Claude Code sandbox placeholder: an empty regular file that is a read-only self-bind, or a character device that is a read-only bind of `/dev/null`. Mounts are read once from `/proc/self/mountinfo` (fields 3-6, two-pass awk): a mount's root is joined onto the mount point of its source filesystem's root mount, so a self-bind must join to exactly its own mount point and a `/dev/null` mask to exactly `/dev/null`; exact text matching in mountinfo's escaping follows no symlink; read-only comes from the mount options, not `-w`. The skipped count is printed only when the gate blocks for another reason. The test override is argv `--mountinfo`, which the Stop hook never passes. No `/proc` (macOS) means no placeholders, which is correct for that sandbox.
- Verified live by the orchestrator inside its own sandbox at every round head: 19 placeholders ignored, a pending RESULT still reported; main's gate reported the same 19 as uncommitted changes.

## Decisions taken during the rounds

- Codex P1/P2s (nine threads): one `mountpoint` process per path and symlink following (776cbfec), every untracked mount treated as a placeholder (5d4928fb), `-w` under root (68d8e142), env override and char-device masks (bbd3d3fb), self-bind via mountinfo root (adca1e6b, the earlier not-applicable withdrawn), separate `/home` filesystem and exact /dev/null provenance (8535b3f3, a8a87bd9). All fixed in-PR, replied and resolved.
- Audit rounds: bbd3d3fb (bind of another file skipped → root field), 153a647d (`$4 == $5` fails on a separate `/home` → join onto the source filesystem's root mount), 3371cc81 (below).

## Audit / Bot / sweep / gate

| scope | verdict |
|---|---|
| task-level, final head 3371cc81 | incorrect (4) → dispositions below |
| task-level, 153a647d | incorrect (1) → fixed in 8535b3f3/a8a87bd9 |
| task-level, bbd3d3fb | incorrect (3) → fixed in adca1e6b and the artifacts |

audit-finding: 1 a filesystem whose root mount has a root other than `/` (btrfs subvolume, chroot) makes a genuine self-bind unrecognised → not-applicable:no regime host uses a subvolume or chroot layout for the checkout, and the failure is fail-closed (the placeholder is reported and the stop blocks visibly, never a bypass); documented here as a known ceiling for the day such a host appears
audit-finding: 2 a hidden read-only self-bind stays eligible when an unrelated read-write mount is stacked over the same path → not-applicable:stacking a foreign rw mount over the orchestrator checkout's own paths is not a mistake the gate guards against and does not occur on the regime hosts; selecting the visible mount is a refinement for a host that stacks mounts, recorded as a ceiling
audit-finding: 3 the validation file shows an invalid jq Bot selector and invalid shell for the reviewThreads query → not-applicable:evidence-only finding with no code defect; the worker replaces both with the executable commands and their output as an artifact correction that does not move the head; the orchestrator's own sweep JSON and GraphQL thread listing at 3371cc81 are the gate's evidence
audit-finding: 4 the report's bootstrap-failure diagnosis (network clone, fail-fast cancellation) has no pasted check output → not-applicable:evidence-only finding about a transient first-run CI failure that passed on rerun; the worker pastes the check output as an artifact correction; the final head's 12 checks pass per the sweep JSON

- Sweep (head 3371cc81): 70 items, 0 failure/warning, all dispositioned. Gate at 3371cc81 with `AUDIT_EVIDENCE` and `AUDIT_DISPOSITIONS=<this record>`: exit 0, evidence copies removed. The orchestrator checkout fast-forwarded to f2b5c115, so the live Stop hook now ignores the placeholders.

## Follow-ups

- Known ceilings (findings 1-2) belong in the script header as a `ponytail:` note when the gate is next touched (T69/T83 or a later fix).
- Lesson for the SKILL (T69): probe hooks from inside the sandbox; a `dangerouslyDisableSandbox` probe hides what the hook sees.

## CompactionDB

- Worker decision `74bc8922…` (per RESULT); cited.
