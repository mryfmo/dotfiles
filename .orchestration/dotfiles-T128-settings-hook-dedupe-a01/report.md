# T15 amendment 2: preserve user command chains

PR: https://github.com/mryfmo/dotfiles/pull/369
Branch: fix/managed-post-tool-use-dedupe
Previous head: 5bcab1f98c60ff6043422794b1c1a72483edb1ac
Base: 8b25f9ca6d6bc25c21b30f2a67cb462a6dd4a95e
Task-copy SHA256: 79d2af63e1c0079a9215d0a063bee9ec6f3bf9d67ce542df15c34cd9805f17fd

[memory:decision] Recognize only the exact managed invocation: one shlex token, or an interpreter (python3/python/bash/sh) followed by one token, whose basename is managed. Any further argument or chain keeps the whole user hook. The code change from the previous head is one predicate line, bool(parts) to len(parts) == 1 after optional interpreter stripping. Existing dict/string/shlex and empty-command guards remain; SessionStart and shared merge functions are unchanged. This preserves user chained commands on the next apply instead of silently removing them.

BotP1 comment4290538244 at home/dot_claude/modify_private_settings.json:85 (https://github.com/mryfmo/dotfiles/pull/369#discussion_r4290538244) is addressed by this source revision; its fixed commit SHA is recorded by RESULT after commit. The required new chained case failed on5bcab1f9, then all20 tests pass. The single new test method test_managed_post_tool_use_replaces_stale_format_only_entry covers stale/duplicate/mixed/absent/wrapper/chain/interpreter and invalid commands, including managed scripts with arguments and interpreter plus chain. The original19 methods are unchanged. No setting command is executed by recognition; tests use temporary source/settings files.

Committed validation.md contains the current red/green, renderer, task hash, caps and format proof. Full PR caps are14 added source lines (under200 changed) and57 test additions (under1000); only two non-evidence files. Native test format passes. Source formatter differences are byte-identical to the previous head and limited to pre-existing unrelated formatting. make render-check passes with the known harmless mise tool-version warning. Current-head CI/Bot are collected after publication and named separately by RESULT, not inferred from the previous head's green CI or earlier Bot no-findings.

All core report/validation/sandbox/learning remain committed with the revision; the prior stale-validation P3 was fixed5bcab1f9. Original wrapper loss was fixedbf6beb53, and the chain regression now pins the stricter amended contract. INV-6 release/accounting remains orchestrator/operator-owned; no worker waiver. Main-checkout CompactionDB consolidation and final-head sweep/audit/gate remain orchestrator-owned. Thread replies/resolution stay with orchestrator.

Limits: matching uses exact token shape and managed basenames as specified, not a shell parser or filesystem identity check; custom same-basename single-token commands remain indistinguishable. No installed apply/restart, local bats, template/manifest/hook-executable or dependency/sandbox-policy edit, graph update or merge.

cost: n/a
