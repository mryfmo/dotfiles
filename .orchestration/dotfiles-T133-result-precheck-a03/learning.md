---
task_id: dotfiles-T133-result-precheck-a03
round: revise-1
---

# Learning

Task-local triage; nothing promoted.

- Three secret-scan bypasses in a row came from one design choice, not three bugs: a02 built its own scan input (a concatenated stream, then a NUL-to-newline view, then a NUL-stripped view) instead of feeding the repository's detector the unchanged file it already knows how to decode. Each patch fixed one input shape and left the next one open: blob boundary, UTF-16, JSON escapes. The redesign calls the detector's own `read_scannable_text`, `json_strings` and `SECRET_PATTERN` on one blob at a time, so its decoding rules apply as they do in CI. This applies to any check that must agree with an existing validator: call it, never re-derive its input.
- A masker and a detector answer different questions. Counting the masker's rewrites as secrets made home-path examples in public source look like credentials. Keep detection (a match of `SECRET_PATTERN`) apart from normalisation (the home-path rewrite of evidence), and scope each rule as the validator scopes it.
- Running a tool on a file outside the repository root needs its path rules kept. `read_scannable_text` judges `.orchestration/` by the path relative to `ROOT`, so the blob sits at its original relative path under a temporary root, and `ROOT` points there for that one call.
- A redesign under a tight line cap still has to keep its tests whole. The test module reached its cap (520) only after the four push tests shared one helper and the repeated subprocess calls became methods. Consolidate the fixtures first, then add the cases.
- When replaying red runs, never prepend a system directory to PATH for one tool. `/usr/bin` first turned `python3` into 3.9 and made the old code fail for an unrelated reason. Call the one tool by its absolute path instead.
- A red proof is only as exact as its selector. `unittest -k` matches substrings, so a neighbouring test's failure passed for the requested test's. Run the exact dotted id and require one executed test on each side.
- A regression meant to prove one fix must fail first on that fix. The first draft of the baseline test failed earlier, on the comma-list parsing, so its red proved the wrong item. Order the assertions so the reviewed behaviour fails first, and use `.get()` for new fields, so the old code fails by assertion, not by `KeyError`.
- A revise round on a PR at its line caps costs consolidation. Fold the unnamed tests into the named ones that cover the same cases, and share the repeated assertion pair, before adding the new tests.
