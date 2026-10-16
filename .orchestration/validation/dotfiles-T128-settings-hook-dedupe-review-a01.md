# Review receipt: dotfiles-T128-settings-hook-dedupe-review-a01 (round 7: amendment 5 of the dispatched task)

- previous_receipt: round 6 at this path, sha256 `4cde3074b80b714d004d29255baaad8ccc8eec04c41e2723dbcb94bff07bbe33` (verdict confirm on `d539949ca5122bd6c9930fd58c6484e7e6d14406f8361bf997d8e6bdba3cf512`, amendment 4)
- reviewer: claude-review-dot-a001 (review seat half; the Codex half confirmed first)
- brief: `.orchestration/tasks/dotfiles-T128-settings-hook-dedupe-review-a01.md` sha256 `bc0757d63f9bd4978c7de2d8bfc44e35c0303901de132d57f665ddd4cb20acc5` (diff against round 6's `601dbd70…`: one amendment-5 paragraph appended; the stop condition and the output are round 2's)
- reviewed file: `.orchestration/tasks/dotfiles-T128-settings-hook-dedupe-a01.md` sha256 `f317d68de16722f12d972deb2e1b46433df0c8b0eadabe78c8a8393ca8bb574d` (copied from the main checkout and hashed before reading; diff against the round-6 copy `d539949c…`: items 1 and 2 at lines 66 and 67 and the new section "Amendment 5" at lines 100 to 103, nothing else; the pre-amendment copy `.orchestration/validation/dotfiles-T128-settings-hook-dedupe-a01-pre-amend5.md` hashes to `d539949c…`)
- sources: the acceptance record (lines 116 and 117: the worker's peer review of amendment 4's implementation before its commit, `~/bin/audit-edit.sh;/usr/bin/python3 ~/.claude/hooks/format-edited-files.py` as two `shlex` parts, the first with an interpreter's basename, the second the managed path, so the interpreter clause deleted the user's command; the Codex half's confirm on `f317d68d`); `home/.chezmoitemplates/claude-settings-managed.json` lines 99 to 113 on origin/main (the PostToolUse commands are bare tilde paths, no interpreter form); the round-6 receipt; origin/main at this round `3b60d6da`

## Checks (stop condition 1 to 4, on the amendment)

1. The amendment removes the interpreter clause: a managed hook is exactly one `shlex` part equal to one of the two renderings of the managed path for this home, and any command of two or more parts is unmanaged whatever its parts, which keeps the peer finding's command and every earlier shape (wrapper, arguments, chain, shared basename, glued token, another prefix) by one rule; the template has never rendered an interpreter form, so nothing managed is lost by dropping it; the constant, the helper, the dict entry, the unchanged merge functions and the failure modes are round 6's. Nothing else changed.
2. The test name is unchanged and verbatim; case ten asserts the kept command for the two-part form whose first part ends in an interpreter's basename, the case that fails under amendment 4's rule (which was never committed, so no head is named for it); cases one to nine are round 6's.
3. and 4. Unchanged from round 6 and re-run on the amended file: 13 controls with the seven generic rows byte-identical to the template after id substitution (compared by script); `task-consistency-check.py` `dotfiles-T128-settings-hook-dedupe-a01.md: OK` with origin/main's copy (`0f84a229`) and the older one (`ba27c4da`); `validate-agent-assets.py --mask-secrets` on a second copy: `masked 0 match(es)`, `cmp` equal; the three premises replayed with `bash -c` from the main checkout after `git fetch` (origin/main now `3b60d6da`): `0`, `1`, `19`, equal.

## Findings

None.

Task-file verdict: dotfiles-T128-settings-hook-dedupe-a01: confirm
