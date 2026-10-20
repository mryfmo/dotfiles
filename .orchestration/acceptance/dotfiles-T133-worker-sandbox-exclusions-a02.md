# Acceptance record: dotfiles-T133-worker-sandbox-exclusions-a02

Lineage: reset of dotfiles-T133-worker-sandbox-exclusions-a01 (INV-6 S2, two amendments before implementation, both orchestrator brief defects). Design 5.14 item 10's Claude half: empty the worker seats' excludedCommands (`agmsg-dispatch *` and the three Linux entries), regenerate the rendered Claude settings, make the validator expect the empty list, update the two tests that assert the old lists. Evidence carried by the orchestrator: this seat sent agmsg messages 2827 and 2830 on 2026-10-20 from sandboxed Bash (Claude sandbox, herdr socket allowlisted since T130); the Codex seat a013 measured `PermissionDenied` on the same socket from its sandbox (13:39Z), the Codex half's open point.

- 2026-10-20T14:03Z-14:11Z: text written whole by the review profile from the orchestrator's brief (`worker-sandbox-exclusions-a02-prompt.md`), installed, two checker fixes by the orchestrator (`reset_of` as a list; the predecessor-copy threat row C3 requires of a reset), 125 lines, self cap 140; pre-send OK, sha256 6f95aef556842405912d7a929d19b95ba95efaa8c2b0e61c72d1ae925e5cc7fc. C-80 round 1 started 14:11Z.

## Owned by dotfiles-T133-worker-sandbox-exclusions-followup-a01

(no advisory rows yet; written 2026-10-20T14:17Z before the worker-sandbox-exclusions PR's first advisory disposition, C-51; the owner text carries the lineage's residual rows as items)
- 2026-10-20T14:21Z: C-80 round 1 one P2 (the owner text `dotfiles-T133-worker-sandbox-exclusions-followup-a01` did not exist) -> owner text written with the Linux runtime check as its item 2; round 2 `Verdict: correct` (`…-text-security-6f95aef.md.last.md`). Dispatched to a013 (TASK 2863, read 14:22:00Z) through send-task.sh at the reviewed bytes 6f95aef5…; the author omitted the fenced block under `## Checks`, so no checks were pasted (the dispatched bytes are the reviewed bytes; the pre-send output is in this record instead: checker OK, secret-pattern 0, 125 lines of 140).
- 2026-10-20T14:29:19Z: a013 PONG `status=blocked`: the prescribed offline `uv run` regeneration exits 2 because uv writes its default cache under `~/.cache/uv`, which the Codex sandbox denies (`Operation not permitted`); correct refusal, text defect (no UV_CACHE_DIR in the prescribed commands). Amendment 1 (2026-10-20T14:43Z) prefixes every prescribed uv command with an absolute private cache under $TMPDIR; C-80 round 3 on the amended bytes, then the amendment TASK. Row `worker:f7f3806:2 cache-path`.

worker:f7f3806:2	cache-path

