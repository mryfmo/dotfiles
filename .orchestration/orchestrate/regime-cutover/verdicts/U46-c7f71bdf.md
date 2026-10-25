No findings. The six removed helpers have no callers; surviving installer functions, `main` functions, and test behavior are unchanged. The used macOS Ghostty uninstaller remains intact.

Reproduced:

- `git status --short` and `git rev-parse HEAD`: clean tree at `c7f71bdf81f14717223f986f11714c25864407e8`.
- `git grep -n -w` at base and head: confirmed the caller inventory.
- Python assertions using `git show` and Bash `declare -f`: all surviving functions match; other executable text is unchanged.
- `bash -n` on all six installers: passed.
- `git diff --check`: passed.
- `make shellcheck` with ShellCheck 0.11.0: exit 0, with nonfatal sandbox cache warnings.

📝 まとめ: U46 の指定差分を読み取り専用で監査し、指摘はありませんでした。
Not checked: Bats (repository policy), GitHub CI/PR metadata, or the original RESULT (offline scope).
Verdict: correct