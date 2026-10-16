Audited [PR #367](https://github.com/mryfmo/dotfiles/pull/367) at `cb9ea17cd7aed296825b6641a4cb1fc18f9d8206`.

[P2] high implementation home/dot_local/bin/common/executable_herdr-agents:1950 `leave.sh` failure is suppressed, after which the placement record is archived and retirement reports success. The remaining identity then has no discoverable record, so retrying `--stale` refuses with `unknown`. A read-only mock reproduced exit 0 after failed leave. Preserve the record and return failure when required cleanup fails.

[P3] high evidence .orchestration/validation/dotfiles-T128-seat-liveness-a01.md:33 The claimed identical baseline failure set omits all 31 failing names and their comparison output; the displayed command is a prose placeholder. Preserve the actual commands and outputs so the sandbox-only failure claim can be audited.

[P3] high orchestration .orchestration/validation/dotfiles-T128-seat-liveness-a01-pr-feedback.json:139 The disposition’s evidence selector compares `.url` with `"None"`, but this item has JSON `null`. Executing that selector returns zero records. Select the status item using its source and check name.

INV-2: holds .orchestration/tasks/dotfiles-T128-seat-liveness-a01.md:87 — task-referenced caps: 162/200 implementation lines changed and 140/1000 test lines added.

Orchestration findings: 1

📝 まとめ: Read-only audit completed; nothing modified. Full tests were not rerun, live CI could not be reverified, and failed retirement can leave an unrecoverable stale seat through this command.
Verdict: incorrect