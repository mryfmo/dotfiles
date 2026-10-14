# Learning triage: dotfiles-T128-task-checkers-a01

These are candidates only; nothing is promoted.

1. [memory:failure] Whole-section pins make a rule sentence a two-file change. `test_regime_rule_sections_are_pinned_whole` compares each pinned SKILL section with its copy under `tests/fixtures/regime/` byte for byte. So a task that edits a sentence in a pinned section, and lists only the SKILL in `allowed_files`, cannot pass its own Check.
   - Detected by running that test right after the SKILL edit, before any push. The question PONG went out at once, and work on items 1 to 5 continued.
   - Mechanism candidate for T705: when `allowed_files` names a file with a pinned section (the `PINNED_SECTIONS` table), require the matching fixture beside it.
2. [memory:decision] A cap counted as added plus deleted lines is spent quickly, because every modified line counts twice. Measure it after the first draft, not at the end. `ruff format` wraps a long call or tuple onto several lines but leaves a long string literal alone. So name a long literal (`ROW_UNIT = "…|…"`, then `.split("|")`), use one `print(…, *lines, sep="\n  ")` in place of a print loop, and keep every message verbatim.
3. [memory:failure] A task's named case list can leave a branch untested. The mutation pass found two:
   - C2's other-directory branch, which none of the ten fixtures or six cases reaches;
   - `[P3]` counting, since the small audit had only `[P1]` and `[P2]` lines.

   Run the mutation pass before the first push. Close each survivor with the smallest addition, and declare in the report every case that goes beyond the task text.
4. [memory:decision] Kept, not changed, because the task forbids a change of meaning: C9 maps `task-consistency-check C<n>` to the probe `scripts/task-consistency-check.py`, while the script lands at `scripts/orchestrator/`. That form of a check id therefore never finds the script on `origin/main`. This is a T705 item, together with the prose form `C<n> of the task-consistency check`, which C9 treats as never present.
5. [memory:failure] Seen again (a05 recorded it): uv's index cache goes stale within a long sandboxed session. The first Check run of the session passed, and a later one failed on pypi being blocked. Run uv with `UV_OFFLINE=1` in the sandbox from the start, and say so in the validation header.
6. [memory:failure] `uv run` puts its environment's and its base interpreter's `bin` directories before the caller's PATH. A stub that a test puts first on PATH therefore loses to any binary that sits beside the interpreter. On the macOS runner that is a real `git`, so the stub only looked as if it worked locally, where the interpreter's directory holds none. Set PATH inside `uv run`, right before the program starts (`sh -c 'PATH="$STUB_BIN:$PATH" exec python -I "$@"'`), and read every CI platform's job before calling a green local run evidence.
7. [memory:decision] A ported checker that predicts a gate must count what the gate counts. The Bot's three checker P1 threads were all gaps between the scratchpad checkers and the merged gate (`swept_finding_ids()`, `AUDIT_FINDING`), plus C4's substring match. When a task freezes a port's meaning, diff the port's inputs against the gate's contract before the PR opens. One early question then covers what a fix round and an amendment had to cover after the Bot's review.
