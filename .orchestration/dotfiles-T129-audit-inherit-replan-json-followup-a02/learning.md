# Learning triage: dotfiles-T129-audit-inherit-replan-json-followup-a02

These are candidates only; nothing is promoted.

1. [memory:decision] Two implementations of one schema drift unless the second is derived from the first's predicates, not from its prose.
   - The counters' jq read "four non-empty parts". The gate's Python reads "exactly these four keys, each `str.strip()` non-empty, every entry of the object, class slug `[a-z0-9-]+`".
   - Copy each predicate across, then write one fixture per predicate in the copy: the extra key, the other class, the slug, and the whitespace the two languages disagree on.
2. [memory:failure] jq's `\s` and Python's `str.strip()` disagree on U+001C to U+001F. Those are whitespace to Python and text to jq.
   - A jq check that has to agree with a Python `strip()` uses an explicit class of the 29 characters `str.isspace()` names.
3. [memory:failure] A guard that only checks a receipt file exists inherits whatever the receipt says.
   - A copied audit has to pass the gate's own acceptance rule (the verdict line and its findings) before it is reused. Otherwise a blocked result is perpetuated, and the "already audited" precondition blocks the retry.
4. [memory:failure] jq's (Oniguruma's) `$` also matches before a final newline, so `test("^[a-z0-9-]+$")` accepts `"abc\n"`, while Python's `re.fullmatch` rejects it.
   - A jq check that has to agree with a Python `fullmatch` ends its pattern with `\z` (`\\z` in a jq string literal). The fixture is the key with a trailing newline.
   - Likewise `// {}` replaces `false` as well as `null`. Where only an absent value means empty, write `if . == null then {} else . end`.
5. [memory:failure] An environment failure was explained by its first visible message (`--base 'main' does not resolve`), not by its cause (a fixture commit that signing made fail).
   - Before an environment row goes into a report, run the failing fixture's first command by hand and quote its own error. Then rerun the module with that cause removed, as validation §6b does.
