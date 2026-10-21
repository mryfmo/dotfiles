---
id: M-20261019-02
artifact: "dotfiles-T133-permission-guard-gate-a03 amendment 1 (2026-10-19T00:0xZ) set the test-line cap at 780 while the branch's tests already held 779 lines; revise 1 (00:40Z) then demanded three security regressions under that cap, and a010's cap question of 00:42:51Z became the second question PONG (INV-6 S2): the task stopped and went back to design (a04)"
classes: [text-defect, cap-without-room]
found_at: "2026-10-19T00:42:51Z (a010's PONG status=question; scripts/regime-counters.sh printed S2: questions 2 >= 2 at 00:45Z)"
detector: "the worker's question and the live counter, not a check at amendment or revise time"
count_at_detection: "one task stopped at S2; the P1-14 merge estimate moved from ~11:30 to ~11:40 JST against the 12:00 JST deadline"
corrections: [C-79]
status: open
recorded_at: "2026-10-19T00:5xZ"
---

# M-20261019-02

- **Evidence:** amendment 1 in `.orchestration/acceptance/dotfiles-T133-permission-guard-gate-a03.md` (cap 780); a010's revise-1 plan ("779/780 used; three required regressions need room"); the counter line `S2: questions 2 >= 2 source=live` pasted in the same record; the a010 PONGs of 00:42:51Z and 00:49:43Z.
- **Detection and why not earlier:** the orchestrator wrote the cap from the a03 text's number plus a margin it did not measure; neither the amendment nor the revise pasted `wc -l` of the branch's test files, so the one-line headroom was never seen until the worker counted.
- **Root cause:** a cap for a continuing branch is written without measuring the branch's current count; the task-consistency check (C1–C10) validates the text's shape, not the cap against the files it governs.
- **Should have been:** before writing or amending a cap for a branch that already exists, run `git show <head>:<path> | wc -l` for every file under the cap and set the cap at the measured total plus the regressions the round names (here 779 + 3 tests ≈ 120 lines → 900), pasting the counts into the amendment or revise.
- **Corrections:** C-79 (new): every cap in an amendment or revise for an existing branch is preceded by the pasted `wc -l` of the governed files at the branch head and leaves room for the round's named tests; the a04 reset carries caps 900/650 measured this way; `task-consistency-check.py` gains a C16 (P1-12 owner) that compares a cap against the named branch head when the task names one.
