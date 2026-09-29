# Learning

- Candidate (not promoted): before implementing against a design in a task file — even a
  carefully-researched one — verify its central technical premise (here: "npm pack
  ships the scripts") directly against the real artifact before writing any code. The
  premise was wrong (npm ships a bootstrapper only), and catching it before writing the
  installer avoided building something that could never have worked.
- Candidate (not promoted): a human-authored task revision that arrives after work is
  already in flight (here, after 3 of 6 commits) should be treated the same way as the
  original task — re-verify its own new factual claims independently rather than
  adopting them wholesale, even when it explicitly supersedes prior work. One claim
  ("Claude seats both") looked at first glance like it might correct an earlier design
  choice, but turned out to be a deliberate policy choice layered on top of a verified,
  different upstream default — worth distinguishing "the revision corrects a fact I got
  wrong" from "the revision states a new requirement" before changing code either way.
- Candidate (not promoted): `find <path1> <path2> <path3> ...` on a mix of existing and
  not-yet-existing paths fails (nonzero exit) for the missing ones, and that failure
  propagates through `set -Eeuo pipefail` even inside a `$(... | sort)` command
  substitution assigned to a plain variable — not just the already-known `!`-negation and
  pipefail-inside-substitution gotchas from a prior task, this is a third variant of the
  same family (a failing command's exit status escaping a context where it looks like it
  shouldn't matter). Guard by checking `[ -d ... ]` before including a path in `find`,
  don't rely on `2>/dev/null` alone to make it non-fatal.
- Candidate (not promoted): splitting a subshell-bodied helper's caller into two
  functions can silently break trap scoping — a `trap ... RETURN` set inside a plain
  (non-subshell) function is not automatically cleared when that function returns; it
  persists and fires again on the _caller's_ next return, referencing now-unset locals.
  The existing codebase's own `install_pinned_crit` pattern (subshell function `(...)` +
  `trap ... EXIT`) exists specifically to avoid this — when introducing a new
  fetch-verify-install helper, look for and mirror that pattern from the start rather
  than discovering the bug by running the tests.
- **Corrected in round 2** (was wrong): the claim above that `identities.sh` does
  directory-hierarchy-aware ancestor matching was a misattribution. Re-verified directly
  against upstream v1.5.0 source: `identities.sh` (via
  `agmsg_project_sql_in_list`/`agmsg_project_path_variants`) is a pure, exact
  (spelling-normalized only) lookup with no ancestor logic at all. What the round-1 test
  actually exercised was most likely `join.sh` or another agent-driven entry point, which
  DOES apply ancestor resolution before ever calling `identities.sh` — a different script,
  a different mechanism, and a materially different conclusion (this one is a real P2
  collision risk for a worker registering from its own worktree, not a benign convenience).
  Root cause of the mistake: testing a positive-match scenario by hand-passing explicit
  paths to `identities.sh`, rather than tracing which upstream function actually implements
  the resolution and testing THAT.
- Candidate (promoted below): don't validate a claim about "how X's design decision
  compares to a design principle" (e.g. "is this consistent with G1") by testing the
  SYMPTOM you observed rather than reading the actual implementing function. The fix:
  when a task's finding names a specific script (`identities.sh`), open ITS source first
  and confirm the mechanism lives there before writing the verification test against it.
- Candidate (not promoted): an `AGMSG_AGENT_PID`/similar "test override" env var documented
  as bypassing a heuristic does not necessarily bypass every check the read side performs —
  here, `agmsg_agent_pid` (the write/detection side) accepted an arbitrary override, but
  `agmsg_read_project_marker` (the read side) still ran a real liveness+argv check the
  override alone didn't satisfy. When a test-only override exists, read both the write path
  and the read path before assuming one env var makes a scenario fully reproducible.
- Candidate (not promoted): two independent subsystems choosing the identical naming
  convention (`.claude/worktrees/<name>`) for genuinely unrelated concepts — Claude Code's
  own short-lived background-task sub-sessions vs. this repo's long-lived resident-worker
  git worktrees — can make an upstream path-based guard (here, agmsg's #367 skip in
  session-start.sh) silently apply to a scenario its author never intended. Worth a
  standing reminder to re-check upstream path-pattern guards whenever this repo's own
  directory-naming conventions happen to overlap with a well-known external tool's.
- Promoted: when independently re-verifying a task's citation (an issue number, a claimed
  upstream behavior), fetch the ACTUAL issue/source rather than trusting the citation is
  correctly numbered — this round found one citation (#133) that was real but entirely
  unrelated to the behavior it was attached to, and the actually-relevant issue (#1320)
  showed the claimed behavior had already been fixed upstream before the pin this repo
  uses. Declining to implement a stale instruction, with the verified reason recorded, is
  the correct action — not implementing it anyway "to be safe", which would have made the
  README say something false about the pinned version.
