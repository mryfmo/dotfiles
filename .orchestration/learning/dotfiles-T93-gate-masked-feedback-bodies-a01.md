# Learning: dotfiles-T93-gate-masked-feedback-bodies-a01

- **Check equivalence across representations, not just per call.** "Use the same masker on both sides" is not enough when one side was masked as a JSON file and the other is the decoded body. The file masker works on JSON lines, which are whole bodies with escaped quotes and newlines. Checking the real `--mask-secrets` output against the gate key found a fail-closed mismatch (placeholders) that unit tests with hand-written masked bodies missed.
- **Fix the producer, not an emulation of it.** Three successive gate-side emulations of file-level masking each leaked a new case: placeholders, escaped quotes, and an assignment prefix that broke the JSON. Making `--mask-secrets` mask decoded JSON string values made both sides equal by construction. The gate then accepts only verbatim or exactly-masked bodies, which never widens acceptance.
- **In zsh, brace a variable before a colon.** `$ref:scripts` is a history modifier. Write `${ref}:path` in any `git show` loop.
- **A zero needs a positive control.** `grep -P '\x00'` found nothing, including in a control file that holds a NUL. Only the Python scan with a detected control counts as "no NUL present".
- **Test code is scanned too.** A variable named like a credential, assigned a key-shaped literal, trips the token-assignment pattern. Name such variables neutrally, as in `key_shaped`.

## Revise round 1

- **A scan and its masker must read the same structure.** The JSON-aware scan reads duplicate members, so the masker must see them too, which an `object_pairs_hook` provides. Otherwise the masking workflow cannot clear what the scan rejects.
- **Never `echo` a command label that contains `\0` or `\x00` in zsh.** It writes real NUL bytes, and the evidence then fails the new `.orchestration` NUL check.
- **A fail-closed limit can still be rejected as "later".** The auditor treats a proposed `not-applicable` for a fixable limit as deferral; fixing it cost one function.

## Revise round 2

- **A format-specific decode must not run ahead of a security check.** UTF-16 text legitimately contains NUL bytes, so the NUL rejection has to come first for paths where only UTF-8 is valid.
- **A masker that merges colliding outputs loses data silently.** A collision must fail and leave the input unchanged.
- **A NUL-free UTF-16 fixture needs code units with no zero byte.** A newline encodes as `0a 00`.
