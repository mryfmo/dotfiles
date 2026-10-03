# Learning triage: dot-main-push-guard-revert-T60-a01

Candidates only; nothing is promoted.

1. **Retiring a generated file means recognising it by its exact content.**
   - Lesson: to remove a file an earlier tool version generated, match its exact content (for example a `git hash-object` blob id derived from the old generator), not a marker line. Users may have extended the file while keeping the marker.
   - Also resolve the path the way the generator did (`--git-path hooks`) and stay within the bounds it wrote to (the common git dir).
2. **A "no matches" grep can conflict with the removal code itself.**
   - Lesson: code that removes a retired artifact must name the artifact (here the log file name and the test fixture body). Task files should allow that residual explicitly, or scope the grep to exclude the removal function and its tests.
3. **The Codex bot reviews every push, and the ruleset requires resolved threads.**
   - Lesson: each push can add threads. Thread resolution under `required_review_thread_resolution` is the orchestrator's sweep step.
   - Workers should list each thread with its fix commit and stop iterating once the remaining threads are policy questions.
4. **Boundary branch reuse.** With `delete_branch_on_merge` off and squash merges, a reused branch name goes stale. Recurring PR branches need a fresh name, or a fresh base from `origin/main`, each time.
