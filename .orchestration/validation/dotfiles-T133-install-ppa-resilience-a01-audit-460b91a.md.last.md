[P2] high implementation install/ubuntu/client/ghostty.sh:78 An already-configured PPA is queried by the dependency-phase `apt-get update` before `ppa_step` runs. If that refresh returns 100 for a PPA-only outage, `set -e` aborts without the retry message. A read-only fake reproduced exit 100, violating the promised outage handling on subsequent applies.

[P2] high implementation home/.chezmoiscripts/ubuntu/run_once_50-client-install-misc.sh.tmpl:9 Removing Ghostty also removes the refresh preceding `misc.sh`, which directly installs packages. Existing machines rerun this changed `run_once_` script while earlier unchanged installers remain skipped; stale indexes can therefore cause package-download failures before the new `run_after_` refresh executes. The fake comparison passed at the base and exited 100 at this head. [Chezmoi execution order](https://www.chezmoi.io/reference/application-order/) confirms the ordering.

[P2] high orchestration .orchestration/acceptance/dotfiles-T133-install-ppa-resilience-a01.md:109 The record exempts round 4 from the revision count by calling it a worker-side P0/P1 fix. INV-6 explicitly counts RESULTs minus one, without that exemption: four reported RESULTs mean three revisions. Integration requires the prescribed reset or waiver; relabeling the round does not release the threshold.

The task declares no `invariants` mapping. Its acceptance record invokes the following regime invariant:

INV-6: violated .orchestration/acceptance/dotfiles-T133-install-ppa-resilience-a01.md:109

Orchestration findings: 1

Verified [PR 454](https://github.com/mryfmo/dotfiles/pull/454) at `460b91a5`: final-head Ghostty tests passed, task-copy hashes match, and changes meet the 67/110 and 159/160 caps. The separate `regime` failure matches the recorded task-copy mismatch.

📝 まとめ: Read-only audit completed with two implementation findings and one orchestration finding; no files changed.
Not run: local Bats or live apt; the outage and stale-index risks remain.
Verdict: incorrect