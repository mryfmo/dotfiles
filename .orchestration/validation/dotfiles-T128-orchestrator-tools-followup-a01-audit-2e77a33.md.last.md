[P1] high implementation scripts/orchestrator/boundary.sh:54 — Deleted filenames are passed as Git pathspecs. A literal filename such as `.orchestration/a*.md` can therefore remove other matching records from the boundary commit; `--` does not disable globbing. Use literal pathspecs. [Git documentation](https://git-scm.com/docs/git-rm#Documentation/git-rm.txt-ltpathspecgt82308203)

[P1] high implementation scripts/orchestrator/fill_sweep.py:63 — Collision detection precedes `discussion_r` normalization. An in-memory replay with review fragment `discussion_r123`, an unrelated failing status fragment `123`, and one `123` TSV row exited successfully and marked both items fixed. Detect collisions using the actual lookup keys.

[P2] high orchestration .orchestration/acceptance/dotfiles-T128-orchestrator-tools-followup-a01.md:38 — The acceptance message claims the two proposed dispositions were decided in this record, but neither decision appears. In particular, owned finding `audit:7b574d3:7` remains unsupported: the worker’s inaccessible-memory explanation does not verify or correct the original identifiers.

[P2] high orchestration .orchestration/validation/dotfiles-T128-orchestrator-tools-followup-a01-pr-feedback.json:177 — The disposition’s evidence command selects `.url == "None"`, whereas the status has JSON `null`. Replaying that command returned nothing, so the recorded evidence does not substantiate this disposition.

INV-1: holds .orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-a01.md:90 — For the task’s stated tier/hash requirements: scope matches and the committed task copy matches the dispatched SHA.
INV-2: holds .orchestration/validation/dotfiles-T128-orchestrator-tools-followup-a01.md:300 — Verified 5 code/test files, 75 production additions, and 126 test additions.

Orchestration findings: 2

Not rerun: filesystem-writing tests or live GitHub verification (`gh` could not connect); saved [PR 361](https://github.com/mryfmo/dotfiles/pull/361) feedback matches the final head and records successful checks. Nothing modified; deletion and false-disposition risks remain.
Verdict: incorrect