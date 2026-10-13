[P2] high — .orchestration/tasks/dotfiles-T128-orchestrator-tools-a02.md:55 — The environment-inputs row omits dependencies required by the specified implementations: `design-keydiff.py` imports PyYAML, while `replay.sh` invokes `env` and `bash`; therefore stop-condition item 4/C7b does not pass.

Task-file verdict: dotfiles-T128-orchestrator-tools-a02: revise