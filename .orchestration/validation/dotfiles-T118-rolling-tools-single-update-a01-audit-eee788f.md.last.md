- [P2] high implementation `scripts/upgrade-tools.sh:286` — The rebuild moves the working installation away without an interruption cleanup trap. A read-only SIGTERM simulation exited with `-15` without restoring it, leaving the tool unavailable. Restore the backup on interruption and test that path.

- [P2] high specification-conformance `install/common/mise.sh:107` — The changed `run_once` installer still resolves per-tool `latest` requests before reaching the warning-only upgrade phase. A registry outage therefore fails `chezmoi apply` even when these tools are installed, contradicting the required offline/transient-failure convergence. Validation §12 already demonstrates this lookup failure; use installation that skips satisfied requests here too.

- [P3] high evidence-reality `.orchestration/validation/dotfiles-T118-rolling-tools-single-update-a01.md:846` — The claimed verbatim grep output omits three matches: rerunning it at the final head returns lines 276, 286, 287, 292 and 360, while the artifact records only 276 and 360. The command at line 159 is also truncated. Replace these with complete commands and output.

The supplied [PR #310](https://github.com/mryfmo/dotfiles/pull/310) snapshot matches the final head: 15 successful check runs, one successful CodeRabbit skipped-review status, and all 13 Bot threads resolved. Required local artifacts exist; no additional scope violation was found under the amendments.

📝 まとめ: Audited `eee788f0`; two runtime defects and one evidence correction remain.
Not rerun: full suites or bats; live GitHub verification was unavailable. No files changed.
Verdict: incorrect