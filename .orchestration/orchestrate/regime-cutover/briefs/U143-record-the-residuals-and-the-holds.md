# U143 the accepted residuals and the held skill pack are rows of the store, not sentences of a document

GOAL
The orchestrator README states six residuals of the seat sandbox and the audit route as prose (`scripts/orchestrator/README.md:171` the same-user host processes that read seat-writable files, accepted by the operator on 2026-10-26 with three conditions; `:173` the srt TMPDIR `/tmp/claude` writable to every seat, the `~/.claude.json` the bridge child writes, and a resumed or forked seat (`hcom r`, `hcom f`) running uncontained; `:319` the auditor's own process outside the permission profile it binds, accepted with G18; `:320` `codex sandbox` and `codex exec` resolving the profile alike, re-measured at each codex bump). The store's `decisions.tsv` carries the operator's G17 row (2026-10-25T19:44:44Z) and the G18 row, but no row per residual, so a reader of the store alone cannot list what the program accepts and under which condition. The hold on the mukul975 Anthropic-Cybersecurity-Skills pack (not installed, pinned, vendored or referenced; `make doctor` and the kit check grep for it) has no row either. After this unit the store holds one row of phase `residuals` per README residual, each naming the README line as evidence and its acceptance as the result, and one row holding the skill pack with its three reopening conditions and its reopening route. Records only: no file outside the store changes, no scenario moves.

SCOPE
No branch. May write: `.orchestration/orchestrate/regime-cutover/decisions.tsv` (append only), `.orchestration/orchestrate/regime-cutover/units.tsv` (this unit's row). The records sync carries the rows to main as unit U20. No other file.

CONTEXT
A decisions row is six tab-separated cells: `ts`, `phase`, `decision`, `why`, `evidence`, `result`; `rounds-check.py --all` parses every row and a row of phase `residuals` counts for no unit. The six residuals and their evidence lines are the README's own words, read on 2026-11-03 at main `154c7245`: (1) `README.md:171` Boundary paragraph, G17; (2) `:173` `/tmp/claude`; (3) `:173` `~/.claude.json`; (4) `:173` `hcom r` and `hcom f`; (5) `:319` the auditor's own process; (6) `:320` `codex sandbox` and `codex exec`. The hold's three reopening conditions: a second maintainer or an organisation; signed tags or release checksums; a content review of a chosen subset. The reopening route: a `git-commit` asset with `pin`, `sha256` and `reason`, a curated subset, validator-clean frontmatter (the six admitted fields) and an audience line, never a branch head.

CHANGE
1. Append six rows of phase `residuals`, one per README residual, decision cell starting `residual:`, evidence naming the README line, result `accepted` with the condition or `re-measured at each codex bump`.
2. Append one row of phase `holds`, decision cell starting `hold:`, naming the pack, the three conditions and the reopening route.
3. `python3 -I scripts/orchestrator/rounds-check.py --all .orchestration/orchestrate/regime-cutover` exits 0 with 0 refused.
4. The records sync carries the rows.

ACCEPTANCE
1. `grep -c $'\tresiduals\t' .orchestration/orchestrate/regime-cutover/decisions.tsv` prints 6 or more. 2. `grep -c 'Cybersecurity-Skills' .orchestration/orchestrate/regime-cutover/decisions.tsv` prints 1 or more. 3. `awk -F'\t' 'NR>1 && NF!=6' .orchestration/orchestrate/regime-cutover/decisions.tsv` prints nothing. 4. `rounds-check.py --all` exits 0, 0 refused. 5. No file outside `.orchestration/orchestrate/regime-cutover/` changes (`git status --porcelain -- . ':!.orchestration'` empty).

VERIFY
The commands of ACCEPTANCE from the coordinator's checkout, their result lines in the units.tsv note; the records sync pull request audited and merged as every sync is.

CLOSURE
allowlist: the decisions rows are the closed list of what the program accepts; a residual not in the list is not accepted.

TRUST
TRUST: the unit trusts the orchestrator README's threat tables and the operator's own G17 and G18 rows as the source of each residual and its acceptance; it reads no sandbox setting, probe or path itself and changes none.

TIMEBOX
20 minutes.

FORBIDDEN
No edit to the README or any file outside the store; no scenario or check change; no mention of any private design directory in the rows.

REPORT
The seven rows' timestamps, the rounds-check summary line, the sync pull request number.

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md`; the store's rows `G17-decided` (2026-10-25T19:44:44Z) and G18 (2026-10-26); `scripts/orchestrator/README.md:171, 173, 319, 320`.
