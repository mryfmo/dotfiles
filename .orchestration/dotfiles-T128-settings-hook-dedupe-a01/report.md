# T15 amendment3: match managed hook paths

PR: https://github.com/mryfmo/dotfiles/pull/369
Branch: fix/managed-post-tool-use-dedupe
Previous head: 72d0e66dcf27bfdb1161f4f4f52b35ef3857b928
Base: 8b25f9ca6d6bc25c21b30f2a67cb462a6dd4a95e
Task-copy SHA256: ae03671345c8cd0faf9a46ae2a7f972987799f56d11f5912f477986e03d23200

Operator decision D-P1-369-A authorizes one more fix round per ACCEPTANCE03:56:19Z for BotP14290664196 and the worker's compact-chain P1. This revision follows that new dispatched contract; it does not waive the stop rule independently.

[memory:decision] Recognize the specified managed hook path, not any matching basename: after optional interpreter stripping require one token fullmatching MANAGED_POST_TOOL_USE_HOOK. The compiled regex is exactly the task's plain-character path ending in /.claude/hooks/ plus an escaped managed basename, declared beside the basename tuple; re is standard library. An unrelated /opt/team/format-edited-files.py and a compact user-command;managed-path token stay unmanaged and preserved. A stale absolute managed path under the temporary home still migrates. Existing dict/string/shlex guards, SessionStart and shared merge functions remain unchanged. No hook command is executed by classification.

BotP1comment4290664196 (https://github.com/mryfmo/dotfiles/pull/369#discussion_r4290664196) and worker compact-chain P1 are addressed by this revision; RESULT names the fix SHA after commit. The regression fails on72d0e66d for both shapes and the interpreter same-basename case, then all20 tests pass. The same single new method now includes cases6-8, plus prior wrapper/chain/argument/interpreter guards; original19 methods unchanged. Full PR caps18 source lines under200 and73 test additions under1000; only two non-evidence files. Native test format passes; source formatting differences match previous baseline after removing shifted line-number headers. render-check passes with the known harmless mise warning.

Four current root report/validation/sandbox/learning records stay committed with source. Previous wrapper loss fixedbf6beb53, stale validation fixed5bcab1f9, spaced chain loss fixed72d0e66d; no claim of current-head CI/Bot before publication. Current commit/head and final CI/Bot are recorded separately after push. New task copy is byte-identical to dispatched hash; source scope stays allowed. Main-checkout CompactionDB consolidation and final sweep/audit/gate/acceptance/INV6 release remain orchestrator/operator-owned. Thread replies/resolution remain orchestrator-owned.

Limits: recognition is the specified lexical path suffix and plain-character class, not filesystem identity or canonicalization; paths outside the pattern remain unmanaged. No template/manifest/hook-executable change, installed apply/restart, local bats, graph update, new dependency, sandbox-policy change or merge.

cost: n/a
