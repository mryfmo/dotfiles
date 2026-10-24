# O2 Orchestrator-seat run: U25 completion, U17, U18, U25d, U30, U28 — brief for the orchestrator seat

GOAL
Run the full `hcom-orchestration` loop (steps 1 to 7) for the next units, in two worker lanes, from this brief: you add the `units.tsv` rows, send the TASK lines, check the RESULTs, task the audit seat, write the verdict rows, merge with `--match-head-commit`, deploy with `make update`, and report. O1 proved steps 3 to 7; O2 adds steps 1 and 2 and the two-lane schedule.

STEP 0 (before any TASK): finish U25's live effect in the workspace
D-024-145: `make agmsg-retire` acted on the chezmoi clone only. Run `herdr-agents --retire-agmsg ~/Workspace/dotfiles` from your seat (your policy has no deny for it; it edits `~/Workspace/dotfiles/.claude/settings.local.json` and leaves the team), then `~/.agents/skills/agmsg/scripts/team.sh dotfiles-conformance` and `grep -c agmsg ~/Workspace/dotfiles/.claude/settings.local.json`; paste both into a `decisions.tsv` row and set the U25 note accordingly. Expected: `0 member(s)` or "Team not found", and no `agmsg/scripts/` hook left (the `inbox.sh` allow line may remain; report it).

LANES (disjoint SCOPE; TASK lines name the brief by absolute path under `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/briefs/`)
- Lane A, `worker-mugo`: U17 (`F2-claude-secret-paths-sandbox.md`, read its ADDENDUM: the Linux doctor check moves into CI), then U18 (`F3-claude-update-policy.md`) after U17 lands (same files). Both are Claude-boundary changes: an omp worker seat authors them, never a Claude Code seat.
- Lane B, `worker-2-nova`: U25d (`U25d-agmsg-retire-registered-projects.md`), then U30 (`U30-seat-text-hygiene.md`), then U28 (`U28-role-levers-github-writes.md`, with its ADDENDUM) only after U17 has landed, because U28 and U17 both edit `scripts/validate-agent-assets.py`.
- Branch names are in each brief. PR bodies carry `Program-Unit: regime-cutover/U<n>` with the parent id for a fix round (regime-ci accepts `U[0-9]+` only).

VERIFY AND MERGE (skill steps 3 to 6)
- U17, U18, U25d, U28: audit seat `audit-tomo` under `U<n>-audit` after positioning its worktree (step 4). U30 is docs-only: your own verdict with a spot-check (the pinned sentences in the test) is enough.
- Bot findings (step 5) as in O1: fix in a new head through a `U<n>b` TASK, or a worker `gh pr comment` refutation; the worker's policy denies `gh pr edit`, so a body correction is a top-level comment until U28 lands its lever.
- Merge order within a lane is the lane order; across lanes, whichever is ready. After each merge: MERGED line, `units.tsv` landed with the merge sha, main CI check.
- Step 7: `make -C ~/.local/share/chezmoi update` after U17 lands and again after the last unit of each lane lands (U18, U28); paste the tail into a `decisions.tsv` row each time. U17 changes `permissions.deny` and the sandbox blocks of the Claude settings; U18 the login environment; U25d the retire path; U28 the omp policies.
- When U28 is deployed, run `scripts/orchestrator/records-sync.sh` once (U20) and merge the records PR after CI green with a `records-only` verdict row.

TIMEBOX
6 hours from the first TASK. A unit blocked for more than 60 minutes gets a HOLD line with the reason and the other lane continues; on expiry, write the partial state into the rows and send `AGMSG-PONG v1 task_id=O2 status=partial note=<where you stopped>`.

FORBIDDEN
No edits outside the store (step 0's retire and step 7's `make update` are the two exceptions); no seat launch unless a worker seat has stopped (then `scripts/orchestrator/hcom-seat worker --name <name>` is allowed and recorded); no `git push`; no merge of #481; no merge without a verdict row for the exact head; no `--admin`.

REPORT
`AGMSG-PONG v1 task_id=O2 status=done note=<unit:merge sha,…>,update=<n> runs,records=<pr>` on the thread, then end your turn. Standing orders: `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` (line 20).
