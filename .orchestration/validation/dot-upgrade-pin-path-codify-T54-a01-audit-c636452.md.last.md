- [P1] High confidence `home/dot_local/bin/common/executable_herdr-agents:1649` The stub unconditionally invokes the installed launcher’s new mode, but `make upgrade` bootstraps from source before applying that launcher; the previous launcher exits 2, blocking every push, including worker branches. Reproduced with both feature and main refs.
- [P2] High confidence `home/dot_local/bin/common/executable_herdr-agents:1653` An identical stub returns early without checking its execute bit; bootstrap leaves a disabled hook non-executable, so Git silently skips the guard and permits unguarded main pushes.

Verified green [PR #225 CI](https://github.com/mryfmo/dotfiles/pull/225), including Python and bats. The report’s claim that worker pushes remain unaffected omits the launcher-version case.

📝 まとめ: Audited only `c636452`; found two regressions requiring fixes. No files changed.

Verdict: incorrect