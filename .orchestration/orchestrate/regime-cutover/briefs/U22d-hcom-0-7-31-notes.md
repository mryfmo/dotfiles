# U22d The hcom notes say what was measured: 0.7.31 facts recorded where the scripts cite 0.7.30 - brief (U22b follow-up, docs and comments only)

GOAL
U22 measured facts 1 to 13 of the hcom contract identical under 0.7.30 and 0.7.31; U22b bumped the pin and the orchestrator measured facts 14 and 15 live on this host (ledger rows 2026-10-24T16:25:00Z and 16:58:00Z). The lever comments and `scripts/orchestrator/README.md` still cite "hcom 0.7.30" as the measured version. This unit records the 0.7.31 measurement where the facts are cited, so a reader of the scripts learns the version the facts were last confirmed on, and adds the three 0.7.31 observations the pilot produced. No behaviour changes.

SCOPE
One branch `docs/hcom-0-7-31-notes` from `origin/main` (ea9b1b41 or later). May write: comment lines in `scripts/orchestrator/{bus-history.sh,hcom-dispatch,hcom-seat,regime-start}` and the same four under `home/dot_local/bin/common/executable_*` (identical copies; keep them byte-equal, the sha256 pins in `home/dot_agents/agent-config.yaml` `levers.sha256` must be refreshed the way U31/U33 did, through the manifest and `make render-check`), `scripts/orchestrator/README.md` (the "hcom 0.7.30 facts the scripts rest on" section and the two other version mentions), `home/dot_local/bin/common/executable_hcom-reply` line 14. Nothing else: no test change (the 0.7.30 strings in tests are fixtures), no pin change, no lever logic change.

CHANGE
1. Each "hcom 0.7.30" fact citation becomes "hcom 0.7.30 and 0.7.31 (measured 2026-10-23 and 2026-10-24)" or equivalent, one line each; the README section title becomes "hcom facts the scripts rest on (0.7.30, re-measured on 0.7.31)".
2. The README section gains three 0.7.31 observations from the pilot, each one line with its source: (a) `hcom kill <name>` and `hcom list --stopped <name>` accept the seat's base_name word (`rosa`) or its full name (`worker-2-rosa`), not its tag (`worker-2`), while alive seats list as `<tag>-<word>`; (b) the named stopped form prints a `Stopped:` key/value block, the `Resume:` hint, then `Stop history (<n> events):` with `(latest)` on the newest, which is the line `regime-start` parses; (c) `hcom list --format` with `name`, `base_name`, `tag`, `status` works as `regime-start` uses it. Source: ledger 16:58:00Z, decisions 16:58:00Z.
3. The lever sha256 pins refreshed from the changed copies; `make render-check` and `make validate-agent-assets` pasted; `tests/unit/test_lever_self_check.py` run.

ACCEPTANCE
1. `git grep -n '0\.7\.30' -- scripts/orchestrator home/dot_local/bin/common docs` shows every remaining mention as a paired "0.7.30 and 0.7.31" citation or a historical date; the four lever pairs byte-equal (`cmp`); the manifest pins equal `sha256sum` of the deployed-form copies.
2. CI green; PR body `Program-Unit: regime-cutover/U22`, the threat table (comment-only change; the lever pins change because the comment bytes change, named as such), the footer; pre-RESULT five-point self-check.

TIMEBOX
25 minutes.

FORBIDDEN
No logic change in any lever; no test edit; no pin change; no `hcom update`; no live seat changes; no omp subagent; no merge, rebase, force-push, PR close.

REPORT
Per STANDING 12 plus the RESULT line (standing order 23).

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` (lines 20 to 25).
