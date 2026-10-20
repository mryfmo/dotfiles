**P1 · High confidence · `home/dot_agents/skills/agmsg-orchestration/SKILL.md:200` — Worker escape authorization remains:** the new sandbox-only sentence is immediately contradicted by explicit exceptions permitting unsandboxed main-checkout writes, CompactionDB updates, and `agmsg-dispatch`.

Step 11 (`:207`) additionally instructs Claude workers to run dispatch outside the sandbox on the first attempt; steps 2 and 5 retain related escape instructions. Because shared exclusions remain available—and excluded commands [run unsandboxed](https://code.claude.com/docs/en/sandboxing#run-commands-outside-the-sandbox-with-excludedcommands)—these are actionable permissions, not merely stale descriptions. This invalidates the procedural controls claimed by `task.md:56` and `task.md:124`. The updated documentation test even requires the contradictory exception text at `tests/unit/test_agmsg_orchestration_docs.py:273`.

Remove the obsolete worker exceptions and update their tests. Protected main-checkout writes should remain orchestrator operations; blocked worker commands should produce the prescribed blocked result.

Reviewed the pinned [PR #431](https://github.com/mryfmo/dotfiles/pull/431) diff and threat table across the requested security categories. No other concrete findings beyond the explicitly documented residual risks. Read-only syntax and policy-consistency checks passed; no files were changed.

Not checked: full tests, live enforcement, deployment, or CI (`gh` API access failed). Shared credentials, agmsg sourcing, path races, and deferred executable binding remain risks.
Verdict: incorrect