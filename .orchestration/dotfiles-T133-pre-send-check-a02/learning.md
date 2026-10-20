# Learning triage: dotfiles-T133-pre-send-check-a02

These are candidates only; nothing is promoted.

1. [memory:decision] Redaction failed twice (a01 rounds 1 and 2), and suppression ended the class: a preflight that prints only fixed labels and numbers has no excerpt to clip. A test holds both streams to the grammar on every run, not just in one dedicated test.
2. [memory:failure] Bash misparses a quoted heredoc inside `$( … )` when its body holds an apostrophe. Read such a helper into a variable with `read -r -d '' var << 'EOF' || true` and run it with `-c`.
3. [memory:decision] PyYAML reports two marks for an unclosed flow sequence, where it opened and where its close was due. A test expecting one line number is wrong, not the tool.
4. [memory:failure] A cap measured as `<old base>...HEAD` counts the files later main merges bring in. Measure the PR's own change against the current base as well, and paste both.
