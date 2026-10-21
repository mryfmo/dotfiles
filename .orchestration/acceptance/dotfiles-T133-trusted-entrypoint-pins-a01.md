# Acceptance record: dotfiles-T133-trusted-entrypoint-pins-a01

The separate pins task extracted from `dotfiles-T133-trusted-entrypoint-binding-a01` lines 398-417 (re-plan v2 R2-15a, r2 finding 11): pin uv 0.13.1, python 3.15.0, node 26.12.0 in `home/dot_mise/config.toml`; pins -> resolver -> binding. Seat: codex-standard-dot-a012 (worker-g).

- 2026-10-21T02:00Z: text authored by author-loop.sh from `brief-pins-a01.md` (99 lines, 3 allowed_files); C-80 round 1 (`…-text-security-0908b8f.md`) correct.
- 2026-10-21T02:04Z: dispatched (TASK 2926, sha 0908b8f4); paste-checks.sh failed on this text (no premise block), so the Checks block stayed empty. Held at 02:09Z over the allowed-file overlap with PR #448 (M-20261021-03); worktree collision reconciled (02:40Z); resumed 03:59Z after #448 merged.
- 2026-10-21T04:12Z: PONG 2953 status=blocked: the independent pre-push review found a P1: `tests/unit/test_supply_chain_policy.py:374-387` holds a map of pinnable tools and requires every other tool to be `latest` and a reason comment above each held line; node and uv are not in the map, so the pins fail that test, and the file is outside the text's three allowed_files. The text omitted the test (orchestrator brief defect). Amendment 1 (brief v2): allowed_files + that test, held entries for node and uv, reason comments, caps 16/48.

text-security:0908b8f:0	correct
worker:e042663:1	brief-omitted-consumer-test
- 2026-10-21T04:27Z: amendment 1 authored by author-loop.sh from `brief-pins-a01-v2.md` (109 lines, 4 allowed_files incl. tests/unit/test_supply_chain_policy.py; held entries for node and uv; reason comments; caps 16/48); C-80 round 2 (`…-text-security-70feed4.md`) correct; sent to a012 as amendment 1 at 2026-10-21T04:28Z (TASK 2955; send-task.sh refused the first line for the missing previous_task_sha256 token, C-121, and accepted it with the token 0908b8f4).

text-security:70feed4:0	correct

