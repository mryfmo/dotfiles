- P2, high confidence — `.orchestration/tasks/dotfiles-T128-orchestrator-tools-a01.md:20`: C7 requires one threat row per `allowed_files` entry, but this row combines `scripts/regime-counters.sh` and `tests/unit/test_regime_counters.py`; split them into separate rows.

Task-file verdict: dotfiles-T128-orchestrator-tools-a01: revise