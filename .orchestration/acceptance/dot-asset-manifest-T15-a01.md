# AGMSG-ACCEPTANCE dot-asset-manifest-T15-a01 (in progress)

PR #181 (e26d9e0, 794d473, 1a2dc78), head 1a2dc78, CI 15 pass / nix skipping.

## GitHub feedback sweep (orchestrator, before merge)
- Issue comments: coderabbitai[bot] 10:33:37Z "fewer than 10 stars → manual trigger". Orchestrator posted `@coderabbitai full review` at 10:45:09Z; waiting for the review (poll bounded to 15 min). Dispositions of its comments will be appended here.
- Reviews / inline comments (human): none at 10:46Z.
- Check-run annotations (non-notice): `public-bootstrap (macos-14, client)` failure ×2 `crit: no bottle available!` and warning ×3 untrusted taps. Pre-existing on main (also on #178/#180), not introduced by this PR. Disposition: not-applicable-to-this-diff; root-cause task dot-macos-crit-pinned-install-T17-a01 (pinned darwin release, remove `|| true`).
- Notices: ubuntu-latest → Ubuntu 26 migration on every ubuntu job. Disposition: task dot-runner-label-pin-T18-a01.

## Independent re-derivation (orchestrator)
- `git diff 7879aea origin/feat/asset-manifest -- scripts/lib/installer-pins.sh`: only two header comment lines added.
- `git diff ... -- install`: no non-comment line changes in installers.
- `home/.chezmoitemplates`: no diff (rendered Codex/Claude templates unchanged).
- Adversarial review in a separate context: pending.

## Process observation
The nested worktree `.claude/worktrees/env-converge-T10` disappeared from `git worktree list` for the second time right after an orchestrator `gh pr merge --squash --delete-branch` of the branch it had checked out (#178 → recreated for T13; #180 → recreated for T15). Procedure change from now: merge without `--delete-branch` while the worker worktree holds the branch; delete the remote branch only after the worker has switched. Root cause to confirm (Phase 5).

## Round 1 — status: revise (10:55Z)
- Independent adversarial review (separate context): S1 `make upgrade` (`bump_terminal_tool_pins`) still writes `installer-pins.sh` directly, so a regenerate silently reverts a bump (reproduced in scratch); S2 `assets.aws-cli` provenance wrong (awscli.amazonaws.com + gpgv, not github-release); N1 install_path/installer not validated; N2 agmsg/gh-poi pins unsourced; N3 YAML float pin hazard; N4 sweep misses scripts/*.sh and lowercase; N5 `enforced: false` unused. Byte identity, idempotence, 425 tests, shellcheck/shfmt, scope, security all verified OK.
- CodeRabbit full review (triggered 10:45:09Z, finished 10:52:16Z, review id 5316800496, profile CHILL): 1 actionable — validator keys rendered constants by name only (L549-569); a duplicate `*_VERSION` in another installer would pass and never be re-rendered. Disposition: fix in the same revision (forwarded 10:56Z). Plan note: 1 included review per hour; re-trigger only after 11:52Z on the final head.
- Crit records: r_ (review), 4 line comments on upgrade-tools.sh:431, agent-config.yaml:401/510, validate-agent-assets.py:550. allowed_files widened for S1: `scripts/upgrade-tools.sh` + its tests.

## Round 2 — delta review of 836a740 + 367023e (11:10Z): closed at the root, hardening requested
- Independent delta review: S1 (installer-pins.sh now only rendered; `--set-asset` validates grammar, refuses unknown NAME/FIELD, re-parses and read-back-compares before any write; bump/unbump byte-exact), S2, N1–N5 and the CodeRabbit (file,constant) keying (negative test present) all closed. `--check` up to date, validator ok, 429 tests OK, shellcheck/shfmt clean. Worker RESULT (11:10:54Z, head 367023e, CI 15 pass) carries a full disposition table and replied on the CodeRabbit thread (discussion_r4103925053).
- Requested before acceptance (one-liners on the new write path): read-back `isinstance(value, str)`; YAMLError → `fail()` in `--set-asset` mode; restrict `--set-asset` to `pin` / `sha256` / `sha256.<arch>`; three negative tests. Deferred to L.3: non-atomic two-file write, prose in `install_path`/`installer` fields, `render.file` existence check.
- CodeRabbit final review: to be triggered once on the final head after the hardening commit (plan window ≥ 11:52Z).

## Round 3 — CodeRabbit final full review on f4db46b (triggered 11:52:42Z in the hourly window, posted 12:03:52Z, review id 5317380626)
- 1 actionable (inline 4104294574, validate-agent-assets.py L548-551): `LITERAL_VERSION_ASSIGNMENT` matches only double-quoted literals; unquoted/single-quoted handwritten versions escape the sweep. Valid. Disposition: fixed at the root in round 3 (regex widened with assignment boundary, `$`-references still excluded, two negative tests); worker replies on the thread; the thread acknowledgement on the new head closes the item (no extra trigger under the 1-review/hour plan).
- Also found: CodeRabbit incremental review 5316940017 (11:10:49Z) was only the acknowledgement of the (file,constant) fix and resolved the thread; no new item.
- Merge proceeds after the round-3 RESULT and CI green, without `--delete-branch`.

## Final — status: accepted (12:30Z), merged as 6026837 (squash, branch kept)
- Round 3 (cf7019c): regex accepts double/single/unquoted literals with an assignment boundary and still excludes `$`/backtick references; two negative tests + three non-literal negatives. Verified in the orchestrator review worktree (validator tests OK), CI 15 pass. CodeRabbit re-analysed and resolved thread 4104294574 at 12:14:37Z; both CodeRabbit threads resolved.
- GitHub feedback sweep on the final head: only pre-existing macOS `crit: no bottle` failure/warning annotations (→ T17) and the runner notice (→ T18). No human reviews.
- Crit: review-scope record resolved with the final disposition; evidence `.agents/worklog/claude/crit/pr-181-review.json`; receipt `.agents/worklog/claude/crit/pr-181-receipt.md`; guard run in the review worktree with the receipt.
- Worker CompactionDB decision recorded in its report; orchestrator consolidation added at acceptance.
- Process notes: orchestrator verification moved to `.claude/worktrees/orchestrator-review`; Crit session addressing from outside the author worktree is not possible without an active daemon (`--session` requires a live session) — follow-up in Phase 5 (Crit evidence tooling by review path).

cost: n/a
