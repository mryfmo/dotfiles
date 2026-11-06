# Needs validation: dotfiles at b2467ae6ac7ad375d124165cbb461b11d12c2cc8

No `needs_validation` record exists in this run, and the carried run-9 holds none.

The source settles the U283 change:
- **The destination proof.** Its refusals, and every call site before a delete or sync.
- **Exit rules.** The single-step and full-run rules under `set -Eeuo pipefail`, and the counted rsync, record and prune failures.
- **Sandbox reach.** No sandbox write root covers an asserted destination (`home/dot_agents/agent-config.yaml:943-952`).

A bounded local check would confirm the remaining check-to-use window. It was not run, by task rule. In the required sandbox it would be: in a scratch HOME, swap `~/.agents/compactiondb` for a link between the assert and the rsync of a stubbed run.

The carried unvalidated candidate, `records-sync/redaction/account-identity-residue-in-published-row` (`REPORT.md` section 5a), is not a `needs_validation` record. Its decisive facts are source-visible; what it lacks is an independent verifier. One fact stays owner-observed: whether the origin repository is public.
