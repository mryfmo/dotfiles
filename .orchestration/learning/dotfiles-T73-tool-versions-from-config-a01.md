# Learning triage: dotfiles-T73-tool-versions-from-config-a01

Candidates only; nothing is promoted.

1. **Unversioned mise calls resolve from the config.** `mise -C <dir> install --locked <tool>` and `mise -C <dir> where <tool>` without `@version` use the version that `<dir>`'s config declares. CI can therefore pin through the copied config alone.
2. **A pin hides in more places than the task names.** Search the whole literal across the repo before declaring "one declaration". Here the fingerprint sat in four test fixtures besides the named constant.
3. **Raw-string fixtures take `.replace` placeholders.** For shell code inside raw strings, `@PLACEHOLDER@` plus `.replace(...)` (the existing `@AWS_CLI_VERSION@` pattern) avoids escaping the braces that an f-string would need.
