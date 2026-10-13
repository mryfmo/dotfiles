P2 high `.orchestration/tasks/dotfiles-T128-orchestrator-tools-a02.md:101` — `codex-review.sh` accepts any `<profile>`, contradicting line 37’s “profile pinned to review” control and design INV-7’s mandatory review profile; no test rejects another profile.

P2 high `.orchestration/tasks/dotfiles-T128-orchestrator-tools-a02.md:101` — the specified command only reads the prompt and has no reviewed-file argument or hash-injection step, so it cannot provide line 37’s claimed control that the script computes the reviewed file’s hash and renders it into the prompt.

Task-file verdict: dotfiles-T128-orchestrator-tools-a02: revise