# O2 addendum 5 (coordinator, 2026-10-24T06:0xZ): availability to other projects is the rate-limiting goal

The operator's direction: make the environment usable by the other projects that develop in parallel on this host, and let that be the pace-setter; everything else follows. The unit that makes that true is U33 (`briefs/U33-regime-kit-other-repositories.md`, written by the coordinator); U31 (in flight) is its prerequisite. The old-regime removals (U32, U26, U27) stay in the plan but behind it.

Order from now:
- Lane A (worker-mugo): U31 (in flight) → U33 → the U33 pilot in a second repository (its ACCEPTANCE 6; you run the live half) → the one-time move of the dotfiles seats to the per-repository root (U33 ACCEPTANCE 2) after `make update`.
- Lane B (worker-2-nova): U30 (in flight) → U28 (levers for the remaining GitHub writes and `records-sync.sh`; other projects' orchestrators need them too) → U32 → U26 → U27.
- U21 at its gate (not before 06:17Z); U22, U23, U24, U19 (G8) afterwards as before.

Report `AGMSG-PONG v1 task_id=O2 status=progress note=<unit> landed <sha>` per landed unit, and when U33's pilot RESULT arrives, `note=kit pilot passed <rows>`; that row is the operator's "available" signal.
