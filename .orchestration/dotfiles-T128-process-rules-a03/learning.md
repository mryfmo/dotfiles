# Learning triage: dotfiles-T128-process-rules-a03

These are candidates only; nothing is promoted.

1. [memory:failure] `scripts/validate-agent-assets.py --mask-secrets` matches a unittest `subTest` label (the `token` keyword with a quoted value) as a secret pattern and the match can span lines when the closing quote was cut off (`cut -c1-N` on test output): it removed a restored line, a code fence and a paragraph from an evidence draft. Keep pasted test output lines whole, and compare the file's line count before and after masking.
2. [memory:decision] A rule sentence that describes another PR's mechanism is untrue on its own tree until that PR merges, and the Bot reports it as P1. Either the dependent PR lands first and this one takes the new base (`gh pr update-branch`), or the sentence waits for a later task; the merge order is the orchestrator's to state in the task.
3. [memory:failure] A rule that says "only the push leaves the sandbox" is Claude-specific: a Codex seat never leaves its sandbox. Seat-specific exits belong in Worker Playbook step 4 or name the seat.
