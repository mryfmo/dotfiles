[P2] high implementation home/dot_claude/hooks/executable_project-map-reload.sh:18 The target filter accepts `close`, `new`, and `list`. A listing containing `targetId: "close"` therefore produces `agent-browser … tab close`, which closes a tab instead of selecting a CDP target. The extracted jq filter reproduces this; the installed binary’s help confirms those operation names. Validate actual CDP target IDs and test rejection of reserved operations.

[P2] high orchestration .orchestration/acceptance/dotfiles-T128-project-map-reload-hook-a01.md:40 Amendment 2 is accepted and dispatched, but the pre-audit record contains no required `scripts/regime-counters.sh` output. The standing playbook requires that evidence before every acceptance action. With two amendments recorded, the omission prevents verification of the required reset decision; record the counters and their disposition before integration.

INV-2: holds .orchestration/tasks/dotfiles-T128-project-map-reload-hook-a01.md:142 — Eight source/test files, 50 changed source lines, and 160 test additions satisfy the applicable caps; no front-matter invariant map is declared.

Orchestration findings: 1

Event JSON and file paths cannot choose executables or inject shell code or JavaScript. Listing values remain quoted arguments with a bounded numeric port, but the target argument can select another tab operation as described above. `TERMINAL_BROWSER_AGENT` intentionally controls the executable through the user’s environment.

Verified: rendered settings match byte-for-byte, absent-key rendering preserves base output, both renderer assertions pass, ShellCheck and Bash syntax pass, and the task copy matches its reported hash. Supplied feedback for [PR #353](https://github.com/mryfmo/dotfiles/pull/353) records 12 successful checks and eight dispositioned items.

Not checked: fresh CI, live reload latency, or the full hook test suite; network access and read-only temporary-file restrictions prevented those checks. The known tab-closure fallback remains the explicitly assigned advisory.

Verdict: incorrect