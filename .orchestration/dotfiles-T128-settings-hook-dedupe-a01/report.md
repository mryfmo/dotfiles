# T15 amendments4/5: exact bare managed invocation

PR: https://github.com/mryfmo/dotfiles/pull/369
Branch: fix/managed-post-tool-use-dedupe
Published previous head: e5d0141bfe63f3bcb558631731785d6f92a92080
PR base before publication: 8b25f9ca6d6bc25c21b30f2a67cb462a6dd4a95e
Branch merge base for caps: 8b25f9ca6d6bc25c21b30f2a67cb462a6dd4a95e
Task-copy SHA256: f317d68de16722f12d972deb2e1b46433df0c8b0eadabe78c8a8393ca8bb574d

Operator D-P1-369-2-A authorizes the extra round. Amendment4 remained uncommitted after peer P1; amendment5 corrects its interpreter contract within that same round. No extra published head or Bot round was consumed by amendment4.

[memory:decision] managed_post_tool_use_paths() enumerates only tilde and current-home absolute forms for each managed script, reusing home_dir() (CHEZMOI_HOME_DIR else Path.home()). Predicate requires exactly one shlex token with whole-string membership. Removes arbitrary-prefix regex/re import and interpreter stripping. Every two-or-more-token invocation stays unmanaged, including interpreter forms and compound-first-token chains; the managed template never rendered interpreter forms. Current-home bare/tilde entries deduplicate. Shared merge functions, SessionStart and input guards remain unchanged.

BotP14290805581 project-local path loss and precommit peer interpreter-chain P1 are addressed in this source; RESULT names the commit SHA after publication. Project/interpreter/foreign-home cases failed on published e5d0141b before helper correction. The peer compound-interpreter case failed on uncommitted amendment4; four interpreter expectations plus that case then failed before the amendment5 clause removal. All20 tests now pass. Original19 methods unchanged; the single new method retains duplicate/stale/mixed/wrapper/argument/chain/foreign-path cases and current-home absolute migration. Interpreter subcases now explicitly assert preservation. Full PR20 source lines under200 and81 test additions under1000. Native test format, source-format baseline comparison and render-check pass; known harmless mise warning remains. Root validation whitespace is normalized after the earlier diagnostic, checked before commit.

Four updated nonempty root report/validation/sandbox/learning files are committed with the new task bytes. This is implementation proof, not advance evidence of a future commit's CI/Bot; those are reported after publication. Prior same-basename/compact-chain P1s fixede5d0141b, spaced-chain P1 fixed72d0e66d, wrapper fixedbf6beb53 and stale validation fixed5bcab1f9. No old-head Bot no-findings claim applies to this source. Thread replies/resolution, INV6 release and final sweep/audit/gate/acceptance remain orchestrator/operator-owned. Main-checkout CompactionDB consolidation stays with orchestrator.

Behavior boundary: only bare managed-path spellings are replaced. Interpreter-prefixed commands, aliases, alternative path spellings and other-home paths are preserved as unmanaged. No filesystem/symlink canonicalization. No installed apply/restart, local bats, dependency/sandbox-policy edit, graph update, template/manifest/hook-executable edit or merge. T13 was accepted/merged by orchestrator separately.

cost: n/a
