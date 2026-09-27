# AGMSG-ACCEPTANCE dot-mosh-and-asset-bumps-T31-a01 (revision 2)

RESULT 2026-09-27T07:18:48Z from claude-standard-dot-a005 (worker-c, claude-opus-5-5 high, --advisor fable): status=ready_for_review, PR #193 head 7191193d671063dc01849562c79af69a8737fdf5, branch feat/mosh-and-asset-bumps rebased onto origin/main 6846ab5.

## Adversarial review (orchestrator, from origin refs)

- task_rev rev2 sha256 match confirmed (b58d82ea…, verified at 12bbe77); rev1 verification also recorded.
- Diff scope: 17 files (+471/−16) against the merge base, all within allowed files (starship.sh/aws_cli.sh are --set-asset render targets; dependencies.bats is the named PACKAGES-membership pattern).
- mosh: both PACKAGES lists, alphabetical; Ubuntu CI proves the real install ("Setting up mosh 1.4.0-1ubuntu3" on both jobs); macOS CI runs brew info only under CI=true — live macOS proof lands at that machine's next apply (disclosed honestly). Config investigation: locale (setup_locale.sh UTF-8), no repo-managed firewall (host ufw is unmanaged; README notes the Tailscale-interface UDP guidance), zshenv non-interactive PATH covers mosh-server — nothing added (YAGNI held).
- Pins-only bump path: `bump_release_asset_pins` with per-asset datasources (gh releases / crates.io / tags+Last-Modified for aws-cli), `pick_windowed_pin` = newest release ≥7 days old AMONG versions newer than the current pin — the no-downgrade guard is the worker's own catch (a naive window would have downgraded mise v2026.9.12 to v2026.9.11 today) and is recorded as a memory:failure. Live run: starship v1.25.1→v1.26.0; sheldon unchanged; mise correctly held; aws-cli 2.35.21→2.36.49 — the task's "aws-cli SKIPPED" expectation was the ORCHESTRATOR'S prediction error (only 2.37.4 was known; AWS ships near-daily), the worker applied the specified window semantics exactly and CI verified the 2.36.49 gpg signature. Hash fields: none exist for these four verify contracts — pins-only is correct.
- remote.yaml (audit P1): all three conditions generalized to `contains(github.actor, '[bot]')` / negation — verified in the diff; Renovate and every future bot excluded from the private-deploy-key steps, humans unchanged.
- renovate.json (audit P2 ×2): mise manager dependencyDashboardApproval with lock-fidelity description; fd `enabled: false` with the upgrade-tools reason; validator --strict passes.
- AppArmor (audit P2 ×2): onchange wrapper renders prerequisite state (bwrap/parser/restriction) so a skipped install re-triggers; doctor reports a REQUIRED failure for missing bwrap with codex present.
- Tests: +13 across 5 files; mutation baselines rev1 4/4 FAIL and rev2 3/3 FAIL against origin/main exports; 475 unit tests OK (skipped=1); CI-equivalent shfmt/ShellCheck clean; first CI red (SC2015, stricter CI shellcheck) fixed in-branch — disclosed.
- Pre-merge Codex audit (head 7191193, gpt-6-astra read-only): "No actionable regressions" — evidence at .orchestration/validation/dot-mosh-and-asset-bumps-T31-a01-audit.md. First pre-merge application of the audit lane.
- Process deviations adjudicated, both ACCEPTED:
  1. Rev2 dispatch was not delivered as a turn notice; the worker found it via inbox.sh before sending the rev1 RESULT and superseded correctly (the rev1 guard-deletion never merged). LEARNING CANDIDATE: dispatch-to-working-pane delivery latency — revision dispatches should assume pickup at the worker's next inbox check; consider a wake-on-revision follow-up.
  2. `git push --force-with-lease` on the worker's OWN feature branch to publish the rebase — T25 precedent (authorized pinned force-with-lease, recorded verbatim); the task text itself created the conflict ("rebase if already started" vs forbidden "force push"). Future task templates name the authorized path explicitly.
- CompactionDB: id a40a36b2-7f57-4379-863e-d8ab52bd818c pasted (rev1 wording as prescribed; the corrected rev2 decision is consolidated below).
- Refutation attempts found no correctness, regression, security, or omission issue.

## Review guard

make require-crit-review satisfied via AGENT_REVIEWED=1 with REVIEW_EVIDENCE=.orchestration/validation/dot-mosh-and-asset-bumps-T31-a01-receipt.md (resolved review-scope approval record r_ea4b69, crit session 871550a2379c, exported JSON at .orchestration/validation/dot-mosh-and-asset-bumps-T31-a01-crit.json).

**Decision: ACCEPTED.** Merge #193 --squash (no --delete-branch while worker-c holds the branch); deploy (canonical clone ff pull + chezmoi apply — installs mosh via apt on this host and applies the starship/aws-cli pin bumps at the next make update); T32 (audit pane visibility) dispatches after this lands.

[memory:decision] T31 accepted 2026-09-27: mosh managed on both OSes (PACKAGES only — locale/firewall/zshenv proven sufficient); bump_release_asset_pins covers mise/sheldon/starship/aws-cli pins-only under the 7-day window with a no-downgrade guard (live: starship v1.26.0, aws-cli 2.36.49); remote.yaml private-bootstrap guards generalized to all [bot] actors (audit P1); Renovate mise lane notification-only, fd held; AppArmor onchange trigger embeds prerequisite state and doctor fails required on missing bwrap with codex. PR #193 squash-merged.

cost: n/a (worker report gives no token figures)
