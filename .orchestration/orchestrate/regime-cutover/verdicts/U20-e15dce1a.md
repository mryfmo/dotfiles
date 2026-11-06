## Findings

- P1 (high) [f1 s10] .orchestration/orchestrate/regime-cutover/preferences.md:42: Both assume-unchanged and skip-worktree hide local edits from every stated cleanliness check; checkout-index -f then overwrites those edits and postflight reports clean.
- P1 (high) [f1 s10] .orchestration/orchestrate/regime-cutover/preferences.md:42: On the case-insensitive filesystem, an incoming .ORCHESTRATION store alias passes the outside-path checks and overwrites the live ledger; postflight still lists store paths alone.
- P1 (high) [f1 s10] .orchestration/orchestrate/regime-cutover/preferences.md:42: checkout-index executes repository smudge filters without isolation; a reproduced filter overwrote the live ledger while every stated preflight and postflight condition passed.
- P1 (high) [f1 s10] .orchestration/orchestrate/regime-cutover/preferences.md:42: The ancestry check trusts info/grafts; a graft made diverged main pass, after which update-ref removed its local-only commit from branch history and the procedure deleted its file.
- P1 (high) [f1 s10] .orchestration/orchestrate/regime-cutover/preferences.md:42: The status check interprets filenames as pathspecs: an incoming literal filename :(literal)README concealed its existing ignored file, which checkout-index subsequently overwrote.
- P1 (high) [f1 s10] .orchestration/orchestrate/regime-cutover/preferences.md:42: Checking only the incoming leaf misses an ignored regular-file ancestor; adding docs/file passed all checks and checkout-index -f deleted the ignored docs file to create its directory.
- P2 (high) [f10 s4] .orchestration/orchestrate/regime-cutover/verdicts/U190-6f66ffdc.md:3: Four added verdicts contain inner location tokens rejected by the current reader, making filed-findings.py exit 2 without an issue list; the documented U207 repair remains outside this head.
- P2 (high) [f10 s3] .orchestration/orchestrate/regime-cutover/preferences.md:42: The new standing order controls live checkout writes and orchestrator behavior, but this PR body omits the required Threat table and its path, control and orchestrator-effect rows.
- P2 (high) [f1 s5] .orchestration/orchestrate/regime-cutover/preferences.md:42: Advancing main before checkout-index leaves old working files after an interruption; rerunning rejects those files as dirty and computes an empty touched set, with no recovery procedure supplied.
- P2 (high) [f1 s4] .orchestration/orchestrate/regime-cutover/preferences.md:42: A readme-to-README rename passes preflight on the case-insensitive filesystem, but the listed addition then deletion removes the newly checked-out file and leaves main's tracked README missing.
- P2 (high) [f1 s3] .orchestration/orchestrate/regime-cutover/preferences.md:42: The new ancestry, index, status and touched-list safety decisions carry no failure-injection tests, contrary to the standing audit rule.

## Reproduced

- Git inspection confirmed the requested head, a clean tree and exactly 70 changed regular 100644 files confined to the contracted store; system Git failed, so subsequent checks used Homebrew Git.
- git diff --check passed; final HEAD and clean status remained unchanged.
- validate-agent-assets.py --scan-identifiers scanned all 70 changed files with zero findings; private redact words were unavailable.
- In-memory masking checks found zero additional matches; UTF-8, NUL, terminal-newline, TSV-width and JSON parsing checks passed.
- rounds-check.py --all with the named base and head checked 172 units and refused none.
- brief-check.py passed for all 17 added briefs.
- Record comparison confirmed 40 append-only ledger additions and 18 append-only decisions additions; changed unit IDs and decision timestamps match the PR summary.
- All 11 added sweep sets have matching summary counts, fingerprints, head SHAs and advisory ledger rows naming the pinned skill.
- audit-carry.findings_of parsed nine added verdicts and rejected four; filed-findings.py exits 2 on the head, whereas the base's 352 verdict files produce 134 filed findings successfully.
- Scratch procedure probes reproduced silent local-edit loss with both assume-unchanged and skip-worktree.
- Scratch case-alias and smudge-filter probes each overwrote live store bytes while satisfying the stated checks.
- A scratch graft probe made diverged ancestry pass and removed the local-only commit and file from main.
- Scratch pathspec and ignored-parent probes each passed preflight and silently deleted local ignored data.
- An interruption probe left HEAD advanced and working files old; rerunning rejected the dirty files and found no touched paths.
- Case-only rename probes passed in one direction and deleted the tracked file for readme-to-README.
- Initial helper probes encountered setup errors in path handling, sweep keys, case-only staging and directory creation; corrected probes completed.

## Notes

Historical truth was excluded as contracted; operational controls and record readability were assessed. Source-store equality, private redact words, build/push isolation and live CI were not independently verified. No network access or repository edits were performed.

Blocking: 6
Filed: 3
Verdict: incorrect
