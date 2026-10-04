[P2] high implementation scripts/agent-stop-gate.sh:135 — `$4 == $5` rejects genuine self-binds when `/home` is a separate filesystem: field 4 is `/moriya/.../.zshrc`, while field 5 is `/home/moriya/.../.zshrc`. The extracted final predicate reproduced `reported`, so sandbox placeholders still block stops on that layout. Compare both paths in the same coordinate system. [Kernel documentation](https://docs.kernel.org/filesystems/proc.html#proc-pid-mountinfo-information-about-mounts)

The diff stays within allowed files, and all expected artifacts exist. Supplied final-head feedback confirms 12 successful CI checks and seven resolved Bot findings. Syntax, ShellCheck, and formatting checks pass.

📝 まとめ: Completed the read-only audit of [PR #248](https://github.com/mryfmo/dotfiles/pull/248); the self-bind comparison needs correction and separate-`/home` regression coverage.

Verdict: incorrect