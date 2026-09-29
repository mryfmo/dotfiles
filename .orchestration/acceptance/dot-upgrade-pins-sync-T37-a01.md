# AGMSG-ACCEPTANCE dot-upgrade-pins-sync-T37-a01

RESULT 2026-09-29T07:41:16Z from claude-standard-dot-a005 (worker-c, turn delivery): status=ready_for_review, PR #209 head 52d9f6bad6a6234760ce68c0b8ba9fcd2bd26a04, branch chore/upgrade-pins-20260929 from origin/main 33452dc.

## Context

Operator-instructed `make upgrade` ran in the canonical clone (base 09a7777) and left the mise pair, the asset manifest and two rendered installers dirty. Committing the mise pair alone would have turned main red: the ccusage 20.0.24 pin disagreed with the expected version in `check-statusline-tools.py`, its unit test and `test.yaml` (the T25 lesson). Per the make-upgrade-is-machine-lifecycle procedure the pending pins were carried into a worker branch by `git apply --index` with blob-identity proof, together with the ccusage sync.

## Adversarial review (orchestrator)

- Scope: 8 files (+49/−49): the five carried pin files (blob-identical to the canonical clone — re-checked by the orchestrator for all five; the worker also verified that canonical origin/main equals 33452dc for each, so nothing landed since could be reverted) plus the three ccusage sync files (4 occurrences, no 20.0.23 left; ccstatusline stays 2.2.30).
- Versions: node 26.9.0→26.10.0, dotenvx 2.28.2→2.29.0, claude-code 2.1.283→2.1.284, codex 0.157.1→0.158.0, ccusage 20.0.23→20.0.24, pnpm 12.4.1→12.5.1 (the window's newest eligible, as predicted at T33f), aws-cli 2.36.49→2.36.50, crit v0.20.3→v0.21.0 with four per-arch sha256.
- Supply chain re-derived by the orchestrator from primary sources: crit v0.21.0 `checksums.txt` matches all four manifest digests; aws-cli tag 2.36.50 exists (tag object 63d7343). The worker additionally hashed the downloaded crit binaries.
- Independent re-derivation at 52d9f6b: `make validate-agent-assets` ok; 577 unit tests OK; `generate-agent-configs.py --check` up to date; PR CI 14/14 pass (nix skipped).
- Visible-lane Codex audit of 52d9f6b: `Audit verdict: correct` — "pins, lockfile entries, generated installers, and ccusage test/CI expectations are consistent; all five carried files matched the canonical clone."
- CompactionDB: T37 decision present. Refutation attempts found no issue.

## Review guard

`make require-crit-review` satisfied via AGENT_REVIEWED=1 with REVIEW_EVIDENCE=.orchestration/validation/dot-upgrade-pins-sync-T37-a01-receipt.md (resolved review-scope approval record r_d09ef8, crit session 16eb550d49a7, exported JSON at .orchestration/validation/dot-upgrade-pins-sync-T37-a01-crit.json).

**Decision: ACCEPTED.** Merge #209 --squash (no --delete-branch while worker-c holds the branch); then in the canonical clone discard the now-identical pending edits (`git checkout -- <5 files>`), `git pull --ff-only`, `chezmoi apply` (renders the mise config; the tools themselves were installed by `make upgrade`), `make doctor`.

[memory:decision] T37 accepted 2026-09-29: the 2026-09-29 `make upgrade` pins (node 26.10.0, dotenvx 2.29.0, claude-code 2.1.284, codex 0.158.0, ccusage 20.0.24, pnpm 12.5.1, aws-cli 2.36.50, crit v0.21.0) landed via a worker branch with blob-identity proof against the canonical clone, together with the ccusage expected-version sync in check-statusline-tools.py, its test and test.yaml; crit digests and the aws-cli tag were re-derived from upstream. PR #209 squash-merged.

cost: n/a (worker report gives no token figures)
