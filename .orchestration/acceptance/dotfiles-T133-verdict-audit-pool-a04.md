---
{
  "audit_findings": [],
  "dispatch": [],
  "format": 1,
  "head": null,
  "ledger": [],
  "pr": 410,
  "replans": {},
  "searches": [],
  "task": "dotfiles-T133-verdict-audit-pool-a04"
}
---

# Acceptance record: dotfiles-T133-verdict-audit-pool-a04

Reset of the verdict lineage's a03 (PR #410, branch tools/verdict-audit-pool-a01, from 6b7e7833) after the security review of the update-branch head found two P1 of the class env-trust-bypass (three rows: INV-6 S1) at the C-61 cap; the a03 record holds the class table and the re-plan line. Text designed by the review-profile context (`.agents/worklog/orchestrator-glue/redesign/v-a04.md`, prompt `v-a04-redesign-prompt.md`): program execution with `bash -p` and an env -i re-exec, no caller-supplied executable directory, O_NOFOLLOW writes inside the repository, `security` as an explicit boolean; `after: [dotfiles-T133-worker-write-boundary-a01]` (D-024-20); the sentences of design 5.14 items 2, 4, 5 and 9 quoted inline (C-88). Seat: a008 (Claude, worker-f), holding. Advisory owner: dotfiles-T133-verdict-audit-pool-a05 (written when the first row appears).

- 2026-10-19T07:36Z: text installed (333 lines + the quotations); `task-consistency-check.py: OK`.
- 2026-10-19T07:41Z: C-80 first review (`…-text-security-*.md`, see the validation directory): `Verdict: incorrect`: P1 a caller-set VERDICT_SANITIZED=1 skips the env -i re-exec and `bash -p` keeps GIT_* (fixed binaries consume attacker-selected git configuration and object stores); P1 the retained counter sources agmsg storage code whose drivers.partition selects a sourced file through worker-writable team configuration (no row, no compensating control); P1 equality to local origin/main and the merge-base trust the shared refs/objects Codex workers can write (the evaluated changeset can differ from the PR); P2 condition 8 names the security report by sha7; P2 `/bin/bash -p --noprofile --norc` exits 2 (long options must precede -p). Root causes: a sentinel is caller-controlled (the check must be of the environment itself); the design let the verdict read PR content from the shared object db and run agmsg shell code. Design 5.14 amended (item 2: option order and the clean-environment check instead of a sentinel; item 8: PR content read from GitHub at the 40-hex head or from a private clone; item 9: one trusted interpreter resolver). Decision: round 2 by the review-profile context (prompt `v-a04r2-redesign-prompt.md`).
text-security:v-a04-r1:1	sentinel-skippable
text-security:v-a04-r1:2	store-plugin-trust
text-security:v-a04-r1:3	shared-objectdb-trust
text-security:v-a04-r1:4	sha7-collision
text-security:v-a04-r1:5	bash-option-order
- 2026-10-19T08:3xZ: the a04 text's design citation is a literal home path (the validator's home-path scan refuses it in a committed task copy); the round-2 text is installed with the `$HOME`-relative form (C-86 amended).
- 2026-10-19T08:29Z: round-2 text (redesign `v-a04r2.md`, 368 lines) installed: the clean-environment check replaces the sentinel, `/bin/bash --noprofile --norc -p` order, counters read from the agmsg SQLite store read-only (no agmsg shell code sourced; the storage route named with its owner), PR content from GitHub at the 40-hex head, full-head evidence names, the 5.14 items 2/8/9 quotations refreshed; the design citation `$HOME`-relative; checker OK; C-80 round 2 started.
- 2026-10-19T08:33:20Z: C-80 second review (`…-text-security-*.md`, newest): `Verdict: incorrect`: P1 HOME preserved by the sanitization selects the resolver's install root (executable selection through an environment variable); P1 LD_PRELOAD/LD_AUDIT run before the first statement on Linux (bash -p does not enable the loader's secure mode); P1 the no-sourcing control fails during application: `dispatch.sh` calls `history.sh`, which sources the agmsg storage and partition drivers; P2 the retained gate (`make require-crit-review`) independently runs `uv python find`, rediscovers tools and rereads shared refs, so application needs a compliant-gate prerequisite; P1 `gh pr merge` without `--repo` lets the local configuration select another repository (a fork can hold the same head). Design 5.14 amended: item 2 (trusted parent, verify-and-refuse, passwd home) and item 9 (install root anchored to the passwd home) earlier today; item 8 now (`--repo` on every gh call; `--apply` prerequisites named, shadow-only until merged). The orchestrator's merge glue gains `--repo mryfmo/dotfiles` on its gh pr calls (08:3xZ). Decision: round 3 by the review-profile context (prompt `v-a04r3-redesign-prompt.md`).
text-security:v-a04-r2:1	home-anchored-trust
text-security:v-a04-r2:2	loader-env-before-exec
text-security:v-a04-r2:3	store-plugin-trust
text-security:v-a04-r2:4	gate-prerequisite
text-security:v-a04-r2:5	repository-binding
- 2026-10-19T09:19Z: round-3 text (`v-a04r3.md`, 384 lines) installed: trusted parent supplies the environment and the program verifies and refuses (allowed names, `$0` realpath, HOME = passwd home), install root anchored to the passwd home, `--repo mryfmo/dotfiles` on every gh call (11 occurrences) with a fake-gh argument test, `--apply` gated on the recorded merges of agmsg-hardening-a01 and dispositions-a02 (shadow-only until then), 5.14 items 2/4/5/8/9 quotations refreshed; checker OK; C-80 round 3 started.
- 2026-10-19T09:24:08Z: C-80 third review (`…-text-security-*.md`, newest): `Verdict: incorrect`: P1 the gate prerequisite named dispositions-a02, whose text still authenticates through `git show origin/main` and excludes require-crit-review.py (the claim was not owned); P1 the agmsg merge record does not authenticate the installed agmsg code dispatch executes (bind the installed version and the storage.sh sha256); P2 `gh api` has no `--repo` flag (installed gh 2.102.0) — the repository binds through the explicit `repos/mryfmo/dotfiles/…` endpoint (design 5.14 item 8 reworded). Decision: round 4 by the review-profile context (prompt `v-a04r4-redesign-prompt.md`): the gate prerequisite becomes the to-be-written `dotfiles-T133-gate-hardening-a01`; installation binding for agmsg; endpoint-bound gh api calls.
text-security:v-a04-r3:1	gate-prerequisite
text-security:v-a04-r3:2	installation-binding
text-security:v-a04-r3:3	repository-binding
- 2026-10-19T09:36Z: round-4 text (`v-a04r4.md`, 388 lines) installed: the `--apply` gate prerequisite is the to-be-written dotfiles-T133-gate-hardening-a01 (dispositions-a02 does not own it), the agmsg prerequisite binds the installed version file and the storage.sh sha256 pinned in the hardening record, `gh api` calls bind the repository through `repos/mryfmo/dotfiles/…` endpoints (9) and `gh pr`/`gh run` through `--repo`; checker OK; C-80 round 4 started.
- 2026-10-19T09:39:00Z: C-80 fourth review (newest `…-text-security-*.md`): `Verdict: incorrect`: P1 the installation pins (VERSION, storage.sh) do not cover the agmsg execution chain dispatch runs; P1 prerequisites authenticated at main40 while the tree is authenticated at a separately captured base40. Both attack the `--apply` mode that this task only gates. Re-plan (YAGNI; P1-4a is shadow until four agreements): `--apply` is removed from a04 (refused with a named message); application is a later task (`dotfiles-T133-verdict-apply-a01`, not written) with its own prerequisites; the evaluated tree binds to one head40/base40 pair captured once. Round 5 by the review-profile context (prompt `v-a04r5-redesign-prompt.md`).
text-security:v-a04-r4:1	installation-binding
text-security:v-a04-r4:2	prerequisite-tree-binding
re-plan: apply-mode-trust (rows text-security:v-a04-r2:3, v-a04-r3:2, v-a04-r4:1, v-a04-r4:2) — specification: a04 gated --apply behind prerequisites instead of not shipping it; design: shadow-only verdict (plan 024 P1-4a), application deferred to verdict-apply-a01; implementation: --apply removed from the text and the script; verification: --apply refuses with a named message; no agmsg code path exists.
- 2026-10-19T09:49Z: round-5 text (`v-a04r5.md`, 376 lines) installed: shadow-only (`--apply` refused with a named message; application deferred to verdict-apply-a01, not written; no agmsg code path, no gate call), the evaluated tree bound to one head40/base40 pair captured once; checker OK; C-80 round 5 started.
- 2026-10-19T09:52:37Z: C-80 fifth review (newest `…-text-security-*.md`): `Verdict: incorrect` on one P2: an endpoint-only rule for `gh api` excludes the feedback collector's `gh api graphql` calls (thread resolution state). Design 5.14 item 8 reworded (GraphQL binds the repository through fixed owner/name variables; node ids only from bound queries). Decision: round 6 by the review-profile context (prompt `v-a04r6-redesign-prompt.md`).
text-security:v-a04-r5:1	repository-binding
- 2026-10-19T10:00Z: round-6 text (`v-a04r6.md`, 376 lines) installed: REST `gh api` calls carry `repos/mryfmo/dotfiles/` endpoints, GraphQL calls bind the repository through fixed owner/name variables and node ids from bound queries, the fake-gh test asserts each form; checker OK; C-80 round 6 started.
- 2026-10-19T10:02:27Z: C-80 sixth review (newest `…-text-security-*.md`): `Verdict: correct`. The a04 text (shadow-only) waits for its prerequisite (`after: [dotfiles-T133-worker-write-boundary-a01]`, D-024-20); a008 holds; dispatch with pasted counters once P1-15 merges and deploys.
