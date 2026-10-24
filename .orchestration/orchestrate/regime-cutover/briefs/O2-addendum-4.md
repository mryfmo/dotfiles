# O2 addendum 4 (coordinator, 2026-10-24T05:5xZ): the orchestrator seat owns the backlog; the old regime is retired first

The operator's direction: stop developing under the old regime; cut over to the hcom regime decisively and keep improving the environment while developing. From this addendum on, the orchestrator seat owns the whole program loop, steps 1 to 7, for every unit in `units.tsv`, including writing the briefs of units that have none. The coordinator session (the Claude Code pane) only relays the operator's words into the store or the bus and reports; it sends no TASK of its own except an addendum like this one.

Order (two lanes; a lane takes the next unit whose inputs landed; disjoint SCOPE as always):
1. In flight: U30 (worker-2-nova), U31 (worker-mugo). Unchanged.
2. Next: U32 (`briefs/U32-rules-cutover.md`, written by the coordinator): the retired rules leave every session. Then U26 (agmsg tooling removal) and U27 (agmsg docs, skills, deployed skill with the archived db): write their briefs from the `units.tsv` notes and the inventory in decisions row D-024-142, in the shape of the O1/O2 briefs (GOAL, SCOPE, CONTEXT with measured facts, ACCEPTANCE, VERIFY, TIMEBOX, FORBIDDEN, REPORT, STANDING). U26 deletes; it does not refine agmsg code (no more units like U25d).
3. Then U28 (levers for the remaining GitHub writes, with the records-sync lever) after U31 lands; then `records-sync.sh` once for U20 and the records PR.
4. U21 (openai-codex route drop) when its gate opens (not before 2026-10-24T06:17Z, the 24 h SIWC refresh evidence; read the auth record's mtime and paste it in the decisions row). U22, U23, U24 after, briefs written by you. U19 (G8: the clean-up table) when U28's `pr-close.sh --from-table` and U16's `worktree-gc.sh --apply` are deployed.
5. `make -C ~/.local/share/chezmoi update` after each merge that changes `home/` (step 7), as before.

Standing changes:
- preferences.md line 21 (fail closed on every producer) and the U30 addendum 2 first-pass gate apply to every TASK from now, including the ones you write.
- A unit that fails its audit three times is HELD and re-planned, never patched a fourth time (O2 addendum 2 item 2).
- Report to the thread with one PONG per landed unit (`AGMSG-PONG v1 task_id=O2 status=progress note=<unit> landed <sha>`) and one at the end of each lane; the coordinator reads them for the operator.
