Audited [PR #359](https://github.com/mryfmo/dotfiles/pull/359) at `73f51ab2`.

[P2] high implementation `home/dot_claude/hooks/executable_project-map-reload.sh:24` — Another repository’s map satisfies the suffix-only selector, suppressing creation of this event’s map and reloading the unrelated tab. Reproduced with the exact jq filter. Match the normalized event path and test two distinct map paths.

[P2] high orchestration `.orchestration/validation/dotfiles-T128-project-map-pane-open-a01-pr-feedback.json:116` — The disposition acknowledges that defect but marks it `not-applicable` because a follow-up owns it. This is deferred work, which the standing integration rule explicitly rejects as a disposition; ownership does not refute or fix the finding.

[P2] high orchestration `.orchestration/tasks/dotfiles-T128-project-map-pane-open-a01.md:78` — The task cites INV-2 but declares no front-matter invariants, and the referenced design’s `implementing_tasks` omits this task. The invariant-ID and exact-sentence binding required by design line 56 is therefore absent.

INV-2: violated `.orchestration/tasks/dotfiles-T128-project-map-pane-open-a01.md:78` — Invariant binding is missing; numerical caps pass: four source/test files, 10 non-test additions, 14 non-test changed lines, 104 test additions.

Orchestration findings: 2

Both premises hold against the pinned base and installed CLI. Task-copy SHA matches; saved CI records match the final head and report success. ShellCheck and Bash syntax checks passed. Nothing was modified.

Not checked: live pane behavior or unit-test reruns; GitHub was unreachable, and direct hook execution encountered the read-only sandbox’s temporary-file restriction.
Verdict: incorrect