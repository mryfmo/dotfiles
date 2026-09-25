# dot-ubuntu-parity-T8-a01 — learning triage

## Reusable rule candidate

Confirms the general shape already noted in T5's and T7's learning
records: an install/apply-style script that stages a temporary path under
a directory it doesn't otherwise guarantee exists (here
`${HOME}/.local/share`) must create that parent directory before its
first use, not "eventually" later in the same function. This is the third
occurrence in this branch's work of a "works on any real, already-
provisioned machine, fails on a genuinely fresh one" bug (T5: systemd
timer script-ordering; T7/T8: zed.sh mkdir-after-mv). Worth a standing
review habit: any new install script that creates files under
`~/.local/{bin,share}/**` should have its directory-creation step audited
for correct ordering relative to first use, especially before this kind of
work targets a fresh-bootstrap CI job again.

Not promoting to `skills/candidates/` — still a project-specific pattern,
not a reusable Claude/Codex workflow.

## Process note

This is a clean example of the loop this whole regime is built around:
T4 shipped code only checked with `bash -n`; T7 (asked to actually run the
new tests) found and fixed the tests, and in doing so surfaced a real bug
in the script itself that was out of T7's scope; T8 closed that follow-up
immediately, with the orchestrator filing it as its own bounded task rather
than letting it linger. Worth keeping this pattern — a worker discovering
an out-of-scope bug should report it precisely (as T7 did) rather than
either fixing it out-of-scope or silently ignoring it, and the orchestrator
should file the follow-up promptly, as happened here.
