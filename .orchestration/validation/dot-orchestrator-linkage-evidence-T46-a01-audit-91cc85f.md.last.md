[P2] high home/dot_local/bin/common/executable_herdr-agents:834 The unconditional fallback suppresses upstream’s refusal when both ID-keyed and legacy placement records exist, then selects the potentially stale legacy pane for dispatch. Restrict legacy fallback to an unavailable library/helper; propagate resolver failures. The added test covers only successful resolution.

Confirmed with an in-memory simulation using the installed upstream resolver. Shell syntax passes. Full tests were not run in the read-only sandbox; GitHub CI was unreachable, and local validation evidence covers only the parent commit.

📝 まとめ: Audited only `91cc85f`; found one placement-resolution defect requiring correction.

Verdict: incorrect