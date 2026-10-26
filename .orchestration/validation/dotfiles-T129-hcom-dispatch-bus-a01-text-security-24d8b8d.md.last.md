[P1] high .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a01.md:102 `BUS_HISTORY` selects an executable from inherited environment state without trusted-path validation; together with the PATH-resolved commands retained by row 48, an injected override or mise shim can execute code and fabricate the history used for dispatch decisions—the sanitized Checks commands do not constrain this runtime path.

[P1] high .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a01.md:22 Read-only access and a schema guard do not authenticate history: attacker-selected `HCOM_DIR` can point to a schema-compatible fabricated store, supplying false senders, receipts and counts; no store-identity control or corresponding hostile-store test is specified.

[P1] high .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a01.md:36 Acceptance-time byte comparison does not bind execution-time input: a same-user writer can replace the task pathname after hashing and restore it before acceptance; the design requires neither protected snapshot consumption nor consumer-side verification of the consumed bytes.

[P1] high .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a01.md:103 The new counters write retains record handling that accepts independently supplied writable paths without canonical containment or stable file identity; symlinked parents, case aliases and replacement between validation and write can redirect acceptance evidence.

[P1] high .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a01.md:52 `--match-head-commit` binds only the commit, not the executable, repository or host: inherited `GIT_*`, repository configuration and host configuration can redirect plain `gh` operations, while the text supplies no enforced execution prerequisite for Linux’s unsandboxed gh path; argv-stub tests cannot establish that boundary.

[P2] high .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a01.md:100 The required TSV history is incompatible with the unchanged marker-format parsers required by items 3 and 5: `bus-read.sh` reports `open: none`, and dispatch cannot identify and record the sent row; the five-field contract also omits the required read marker.

[P2] high .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a01.md:103 The new refusals and revise count select `verdict=revise`, but the cited acceptance records and existing protocol use `status=revise`, so ordinary revision directives bypass the required previous-head, test-selector and counters checks.

Not checked: implementation, live Linux execution or adversarial races; same-user isolation remains a declared residual, and these controls do not establish it.
Verdict: incorrect