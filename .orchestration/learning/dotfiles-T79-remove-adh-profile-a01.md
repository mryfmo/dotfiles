# dotfiles-T79-remove-adh-profile-a01 — learning triage

1. **Do not echo regex command lines through zsh `echo` into evidence.** zsh's `echo` interprets `\b` as a backspace, so a recorded `grep "adh\b"` line showed up as `adh` followed by a control character. Use `printf '%s\n' '<command>'` or a quoted heredoc for command lines that hold backslashes. This was repaired here before pasting.
2. **Keep a pinned error-message phrase when tightening a validator.** Changing "must define the six base profiles and only the optional adh profile" to "exactly the six" broke a test that pins the "must define the six base profiles" substring. "… and no others" keeps the phrase and the meaning.
3. **A deletion of an allowed value deserves one negative test.** The old predicate `required <= set(p) and not (set(p) - required - {"adh"})` silently accepted `adh`. One test with an extra `adh` profile pins the new behaviour.
