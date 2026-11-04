# U151 e2e is mandatory for a web or mobile project and installed nowhere else: the four install conditions recorded, the project question answered by its default, no install

GOAL
The e2e research decision of 2026-11-02 makes the tester-army e2e tool mandatory for a project with a web or mobile surface and forbids it everywhere else: this repository has no browser or device surface, so nothing here changes for an install. The plan's unit M-16 asks the operator one question, which project installs e2e, with the default `none until a web or mobile project asks`. This unit is records only. It states the four conditions every such install must meet with the value each takes, applies the default, and lands one `decisions.tsv` row that records the absence of a project so the unit's state is in the store. No project is named, nothing is installed anywhere, and the install tasks of M-16 wait on a later row that names a project.

SCOPE
No branch. Writes: `decisions.tsv` (one row, by the coordinator) and `units.tsv` (this unit's row) in the program store, carried to `main` by the next records sync; the coordinator keeps the task notes outside the store. Nothing else: no file of the kit, no file of any project, no seat.

CONTEXT
Measured 2026-11-03 (UTC) on `main` at c92078d0 by the coordinator, from the design set of the e2e decision: the decision document's fifth concrete item, the decision's requirement scenarios, the research behind it, and the plan rows of M-16. The four conditions, each with the exact value it takes, in plain words:

1. The telemetry variable. The variable named E2E_TELEMETRY_DISABLED is set to the value 1 in the worker seat's environment before the first run. Why: the tool sends telemetry by default to a PostHog endpoint in the European Union and records whether its caller is a coding agent; the research behind the decision names the same variable as the opt-out, with DO_NOT_TRACK set to 1 as the alternative the plan does not use.
2. The pinned version. The install names one exact release of the tool and the publisher's checksum for it, never a floating tag and never a run through `npx` at latest. Why: the tool is before its 1.0 release and its own status line says its API and settings can change between minor releases; the newest release the decision's research measured is 0.22.0 of 2026-10-30, which carried a breaking change to screenshot behaviour. The value to pin is resolved from the npm registry on the day a project is named (task 03), so the number 0.22.0 is the newest release the design set measured, not the pin.
3. The Playwright download hosts. Exactly three host names enter the worker seat's srt network allowance, the key named network.allowedDomains: playwright.azureedge.net, cdn.playwright.dev and playwright.download.prss.microsoft.com. Why: the seat's network reaches a fixed set of hosts, which would block the browser download the tool needs on first use and, by design, keeps blocking the telemetry endpoint.
4. The worker seat. The tests run on a worker seat of the project, never on the operator's host and never in the coordinator's session; the skill is listed for the audience omp-worker alone through the project's skills.audience entry, and the plan's seat is started as a worker named e2e-1. Why: the tool runs test files, its settings file and custom engines with the full authority of the account that runs it, so the account must be a contained worker.

The default applies. No web or mobile project has asked, so no project is named and no install happens anywhere. Two facts of this checkout stand behind the row: the decision document names the telemetry variable (one match, the plan's verify command for task 01), and the store holds no M-16 row yet (zero matches for the verify command of task 02, so the row this unit lands is the first). One plan defect is recorded for the coordinator: the check of task 10, as the plan writes it, exits 1 in this checkout before any install, because the word playwright already occurs in the gh-comment-attach-files skill and in a retired Codex server name; the narrower form the design checker's own narrower form uses (tester-army or the e2e-dev scope) exits 0. Task 10 needs the narrower pattern before it can pass.

CHANGE
1. One `decisions.tsv` row by the coordinator (phase `M-16`, decision starting `M-16 e2e install: no project named;`): the default applied, the four conditions with their values as the evidence, the task 10 defect, and the result naming the superseding row that reopens the install tasks when a project asks. The exact row text is in the coordinator's notes.
2. The `units.tsv` row for U151 (`track` records, state `done` once the row is written, pr `-`, head `-`, brief this file).
3. The waiting tasks, each unblocked by the condition the notes file names: 03 (a superseding M-16 row names the project), 04 (03's pin and checksum), 05, 06 and 07 (04's asset entry in the project), 08 (05, 06 and 07 all done), 09 (08 done and the project's seat login present on the host), 11 (the seat of 09 running), 12 (11 read 1 inside the seat), 13 (12's run outcome). Tasks 95 and 96 wait with them in substance: the two scenarios describe an install that has not happened, so a flip today would make the holds-today run claim what is false.

ACCEPTANCE
1. `grep -c 'E2E_TELEMETRY_DISABLED' <the e2e decision document, outside the store>` prints 1 or more (the plan's verify command for task 01; measured 1). 2. `grep -c 'M-16' .orchestration/orchestrate/regime-cutover/decisions.tsv` prints 1 or more once the coordinator appends the row (the plan's verify command for task 02; measured 0 before the append). 3. `awk -F'\t' 'NR>1 && NF!=6' .orchestration/orchestrate/regime-cutover/decisions.tsv` prints nothing after the append. 4. `~/.local/bin/common/brief-check.py .orchestration/orchestrate/regime-cutover/briefs/U151-e2e-install-waits-for-a-surface-project.md` exits 0 and prints nothing. 5. The coordinator's notes hold one row per M-16 task (16 rows), kept outside the store. 6. The next records sync carries the row and the brief to `main` and is audited and merged through the levers.

VERIFY
The commands of ACCEPTANCE 1 to 5 run by the coordinator in the checkout, their output pasted into the unit's note in `units.tsv`.

TIMEBOX
20 minutes.

FORBIDDEN
No install of e2e, Playwright or any npm package anywhere; no change to any file of the kit (the manifest, the installers, the Makefile, the mise settings, the workflows, the skills) or of any project; no seat started; no network call; no row or brief naming a private design directory or any word of `redact-words.txt`; no flip of the two scenario tags.

REPORT
The `units.tsv` note: the row timestamp, the four values (the variable and its value, the newest measured release and that the pin is resolved by task 03, the three hosts, the seat audience and name), the task 10 defect with the narrower pattern, and the list of waiting tasks with the condition that unblocks each.

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md`; `handoff/README.md` conventions in the same store; `.orchestration/orchestrate/regime-cutover/briefs/U146-gate-job-pattern-compared.md` as the model of a records-only unit.
