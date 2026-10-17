# T15 amendment5 publication

PR: https://github.com/mryfmo/dotfiles/pull/369
Branch: fix/managed-post-tool-use-dedupe
Head: c98e4ceafc451282c956d6f61546dff46f55864f
Previous published head: e5d0141bfe63f3bcb558631731785d6f92a92080
Base before publication: 8b25f9ca6d6bc25c21b30f2a67cb462a6dd4a95e
Task-copy SHA256: f317d68de16722f12d972deb2e1b46433df0c8b0eadabe78c8a8393ca8bb574d
Operator decision: D-P1-369-2-A
Status: ready_for_review. All13 current-head CI checks pass; CI watcher joined exit0. Current-head Bot code review completed without findings. Root integration remains pending.

The additional operator-authorized round replaces arbitrary-prefix regex recognition with exactly one shlex token equal to a known tilde/current-home absolute managed path. home_dir() is reused, no regex/dependency introduced. Interpreter stripping is removed; every multi-token command stays unmanaged. The managed template always emits bare paths. Shared merge helpers, SessionStart and existing input guards remain unchanged. This makes current-home bare hooks deduplicate while project-local, foreign-home, wrapper, arguments and chained user commands survive. Alternate spellings and aliases remain unmanaged, without filesystem canonicalization.

Amendment4 was never committed: independent peer found P1 on ~/bin/audit-edit.sh;/usr/bin/python3 followed by a managed path. The helper reproduced loss and the regression failed red. Hashed amendment5 corrected the interpreter contract within the same operator round; removing the clause fixes that finding. Peer rereview approved the whole goal and evidence. BotP1 4290805581 (project-local hook deletion) fixed:c98e4ceafc451282c956d6f61546dff46f55864f; precommit peer compound-interpreter P1 fixed:same. Project/interpreter/foreign-home cases failed on e5 before helper correction. Five interpreter/compound expectations failed on uncommitted amendment4 before amendment5 correction; this red is not claimed to be against a clean published head.

All20 unittest methods pass, original19 unchanged and one added method test_managed_post_tool_use_replaces_stale_format_only_entry. Test formatting/render/source-format baseline comparison/independent peer/agent review gate pass. Full PR20 source lines and81 test additions meet200/1000 caps. Four nonempty root report/validation/sandbox/learning files are committed and byte-matched in head-proof.txt; postpublication supplements here remain untracked for orchestrator sync.

Current-head Bot code_review completed 2026-10-16T04:31:14Z; full-SHA summary6203950188 says has_any_findings=false and has_unresolved_findings=false, receipt6208119708 names c98e4ceafc. Reviews and top-level inline lists on this original head are empty; their bodies and the summary/receipt were read. This is structured full-head completion evidence, not a reaction-only claim. Security summary remains on80f59cd685d63524089ca73884c409d7e9355b13, no new-head security claim. CodeRabbit pass means automatic reviews skipped.

Earlier BotP1 4290664196 same-basename and worker compact-chain P1 fixed:e5d0141bfe63f3bcb558631731785d6f92a92080; 4290538244 spaced-chain fixed:72d0e66dcf27bfdb1161f4f4f52b35ef3857b928; wrapper audit fixed:bf6beb53aeb56d0392566f924303581d8f819b80; stale committed evidence fixed:5bcab1f98c60ff6043422794b1c1a72483edb1ac. Thread IDs are unavailable in worker REST evidence; prior GraphQL denial was not retried. Root supplies final sweep/thread IDs and owns replies/resolution, acceptance, task audit, gate and merge. No remaining worker code finding; no waiver of stop/INV6/S1/S2. Current operator cycle bot_rounds=2 (e5 to c98); operator_extra_fix_rounds=2 cumulative. Amendment4 consumed no Bot round.

No installed apply/restart, local bats, graph update, dependency/policy change, merge or thread write. Main-checkout CompactionDB consolidation remains orchestrator-owned. T13 was already accepted/merged separately.

cost: n/a
