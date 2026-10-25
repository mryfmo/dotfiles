# U22b The hcom 0.7.31 pin, measured live before it stays — brief (U22 part 2 follow-up)

GOAL
U22 measured facts 1 to 13 of the hcom contract identical under 0.7.30 and 0.7.31 and held the pin because facts 14 and 15 (a seat's live `listening`/`active` status; the multi-event `(latest)` stop history `regime-start` parses) need a logged-in omp seat under 0.7.31. This unit bumps the pin on a branch with the measured digests, and the orchestrator deploys it to this host and measures the two live facts on one relaunched worker seat; the PR merges only if both hold, else a second commit reverts the pin and the facts that failed are recorded.

SCOPE
One branch `chore/hcom-0-7-31` from `origin/main` (the U22 merge or later). May write: the hcom pin's single source and its receipt or lockfile (the files U22's fact table names), `docs/` lines naming the version, `docs/omp-skills.md:39` (the one-line `enabledProviders` correction U22 left: the setting that silences the agent-plugins provider is `disabledProviders`), and the tests that pin the version string. Nothing else.

CHANGE
1. The bump with the four PyPI digests from U22's PR body (verify them again against PyPI, paste the `curl -sI`/`pip download --no-deps` checksums or the registry JSON `digests.sha256`), the receipt updated the way U15/U42 did for other tools; `make render-check` and `make validate-agent-assets` pasted.
2. The docs line.
3. The RESULT names the two live facts as "orchestrator measures after deployment"; you measure nothing live.

ACCEPTANCE
1. CI green on the head; the pinned digests match PyPI (paste).
2. After the orchestrator's `make update` on this host and one worker relaunch under 0.7.31: fact 14 (`hcom list` shows the relaunched seat `listening`, then `active` during a turn, then `listening`) and fact 15 (`hcom list --stopped <base>` of a seat killed with `hcom kill` shows `killed by:cli` as `(latest)` with the earlier stop events kept) hold, measured by the orchestrator and pasted into the ledger row; if either fails the orchestrator asks for the revert commit and records the facts.
3. PR body `Program-Unit: regime-cutover/U22`, the threat table (a tool every seat runs changes version; the 13 measured facts and the 2 live ones named), the footer; pre-RESULT five-point self-check; orchestrator verdict after the live measurement.

TIMEBOX
30 minutes for the branch; the live measurement is the orchestrator's at a quiet moment.

FORBIDDEN
No `hcom update` on the host; no live seat changes; no omp subagent; no merge, rebase, force-push, PR close.

REPORT
Per STANDING 12 plus the RESULT line (standing order 23).

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` (lines 20 to 24).

ADDENDUM (orchestrator-sari, 2026-10-24T16:2xZ): the pin reaches this host only through `main` (`make update` applies the clone at `main`), so GOAL's "merges only if both hold" cannot be literal. The pilot's order is: orchestrator verdict on the static part (digests equal PyPI's, receipt and installer URLs consistent, CI green), merge at a quiet moment, `make update` (hcom 0.7.31 installed), one idle worker seat relaunched under it, facts 14 and 15 measured by the orchestrator and pasted into the ledger row; if either fails, a revert PR (`U22c`) restores 0.7.30 the same day and the facts are recorded. Thirteen of fifteen facts already hold, which makes the revert path the cheaper risk.
