# T68c: PR #134 review security fixes — trusted-runtime invocation, identifier grammar, shdoc

task_id: T68c
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-conformance
worker: codex-deep-dot
plan: PLAN-pi-worker-integration.md (Phase 7; PR #134 bot review, three P1s)
depends: T66e (in flight; T68c dispatches after its RESULT)

[memory: failure — PR #134 review found three real security/compliance defects: (1) contextdb.ts (and the T48 codex notify receiver — same class) executed PROJECT-LOCAL .claude/hooks/contextdb_cli.py, letting a malicious repository run arbitrary code as the user despite trust=never; capture must invoke the TRUSTED installed runtime with the project root as data. (2) agmsg_send passed model-supplied team/to into send.sh whose SQL interpolates identifiers — quote-injection into the bus DB; identifiers must be grammar-validated at the tool boundary AND send.sh must stop interpolating. (3) modified shell comments in whoami.sh/check-inbox.sh violated the shdoc policy.]

## Fixes (exact)

1. Trusted-runtime invocation (both harness receivers):
   - home/dot_pi/agent/extensions/contextdb.ts: keep the project
     OPT-IN check (existence of <cwd>/.claude/contextdb/) as DATA, but
     execute the TRUSTED installed CLI
     `<home>/.agents/compactiondb/.claude/hooks/contextdb_cli.py`
     (verify existence; absent -> silent no-op) with cwd=project so
     project_paths resolves the project DB. Never execute any file from
     the project tree.
   - home/dot_local/bin/common/executable_contextdb-codex-notify: SAME
     class, same fix (this predates the pi plan — T48 shipped it;
     include the correction here with its own regression tests).
   - Verify with the vendored source (read-only) that the installed CLI
     against a project cwd writes to the PROJECT's spool/DB (cite lines);
     if it does not, STOP and ask.
2. Identifier grammar:
   - agmsg.ts: validate team and to against the repository identifier
     grammar (`^[a-z0-9][a-z0-9_-]{0,63}$` — confirm against existing
     join.sh/name validation and cite; reject otherwise with a tool
     error). body remains free text but is passed as ONE argv element
     (already argv-array).
   - home/dot_agents/skills/agmsg/scripts/executable_send.sh: stop SQL
     string interpolation for identifiers AND body — use sqlite3
     parameter binding (.param set / ? placeholders via a here-doc) or
     equivalent safe quoting for ALL VALUES; add regression tests (a
     body/identifier containing a single quote round-trips intact and
     injects nothing; use a scratch AGMSG_STORAGE_PATH db for the test).
     Existing callers' behavior otherwise unchanged.
3. shdoc compliance: convert the modified comments in
   executable_whoami.sh and executable_check-inbox.sh (and any other
   comment touched by T68) to shdoc-compatible English annotations per
   AGENTS.md.
4. Update extension SHA-256 constants; tests for every path above.

## Allowed files

- home/dot_pi/agent/extensions/{contextdb.ts, agmsg.ts}
- home/dot_local/bin/common/executable_contextdb-codex-notify
- home/dot_agents/skills/agmsg/scripts/{executable_send.sh,
  executable_whoami.sh, executable_check-inbox.sh}
- scripts/validate-agent-assets.py (hash constants)
- tests/unit/ (matching modules)
- Your artifact paths (T68c five artifacts)

## Forbidden actions

git commit; git push; chezmoi apply; bats; dependency changes; real pi
execution; vendor changes; behavior changes beyond the three fixes.

## Validation

make format / bash -n / shellcheck -x / unit-test /
validate-agent-assets green (+ts check); quote-injection round-trip
transcript; full diffs pasted; scope check.

## Completion / RESULT contract

Five artifacts; memory add (kind=failure); effects=none. Orchestrator
pushes with T66e to PR #134, replies to all four bot comments, reruns CI.
Reply `AGMSG-RESULT v1 task_id=T68c`. max_turns=25.
