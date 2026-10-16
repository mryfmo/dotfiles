# Published implementation and committed validation: T15 amendment 1

PR: https://github.com/mryfmo/dotfiles/pull/369
Branch: fix/managed-post-tool-use-dedupe
Implementation/diff head validated here: bf6beb53aeb56d0392566f924303581d8f819b80
Base: 8b25f9ca6d6bc25c21b30f2a67cb462a6dd4a95e
Task-copy SHA256: 99fb3dc7f244c31f58eb9f24f0b0fd9b58c8a5eac71f91027af8a47ee3771225

Status: implementation published and validated. This evidence-only revision folds the complete implementation-head proof into tracked validation.md; no untracked supplement is needed to inspect its tests, renderer, caps, CI or Bot result. The successor evidence commit changes only task records; source and tests remain byte-identical to the implementation head above. Successor-head CI/Bot are reported by RESULT after publication, distinct from this immutable implementation snapshot.

[memory:decision] PostToolUse reuses managed-entry replacement to deduplicate stale managed hooks. Match only the command program: first shlex token or second after python3/python/bash/sh. Keep dict/string/shlex and empty/interpreter-only guards; preserve user wrappers passing managed paths as arguments. Shared merge functions and SessionStart recognition remain unchanged.

Committed validation.md contains the actual wrapper regression failure on auditedbdefcbe4, all20 tests passing after the fix, a fresh full20-test run plus the requested single-test check, make render-check passing, source/test equality tobf6beb53, and git numstat. The only non-evidence files are home/dot_claude/modify_private_settings.json (14 added source lines, under200 changed) and tests/unit/test_claude_settings_merge.py (42 additions, under1000). One new method test_managed_post_tool_use_replaces_stale_format_only_entry covers duplicate/stale/mixed/absent/wrapper/interpreter and invalid-command cases; existing19 methods unchanged.

The same tracked validation embeds all implementation-head CI checks passing on PR369, with four unit-test environments, bootstrap matrix, Agent assets and secret checks. CodeRabbit success means automatic review skipped. It also embeds Bot receipt6206111205 (https://github.com/mryfmo/dotfiles/pull/369#issuecomment-6206111205) and summary6203950188 (https://github.com/mryfmo/dotfiles/pull/369#issuecomment-6203950188): code_review explicitly binds fullbf6beb53 head and completed/no findings. This is not a reaction-only claim. The separate security review is on earlier80f59cd6, not new-head coverage.

Audit dispositions: old bdefcbe4 finding1 wrapper loss and finding3 stale publication report were fixed bybf6beb53. The bf6beb53 audit's P3 missing/stale tracked validation is addressed by this evidence-only revision; validation.md/report.md now carry the published20-test/render14/42/CI/Bot proof in the tree. INV-6 release/accounting remains the orchestrator/operator's decision per ACCEPTANCE; no worker waiver or acceptance-record edit.

Limits and boundaries: program-basename collisions and env/option invocation forms remain task limits. No settings command executed by the predicate; tests run the modifier on temporary settings. No installed apply/restart, hook executable/template/manifest changes, local bats, dependency/sandbox-policy edit, Plan Mode, Crit server, graph update or merge. Main-checkout CompactionDB consolidation and final-head sweep/audit/gate remain orchestrator-owned.

cost: n/a
