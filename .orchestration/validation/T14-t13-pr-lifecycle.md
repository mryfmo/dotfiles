# T14 validation evidence

## GitHub CLI prerequisite

### `gh --version`

Exit: 0

```text
gh version 2.96.0 (2026-07-02)
https://github.com/cli/cli/releases/tag/v2.96.0
```

### `gh auth status`

Exit: 1

```text
github.com
  X Failed to log in to github.com account mryfmo (default)
  - Active account: true
  - The token in default is invalid.
  - To re-authenticate, run: gh auth login -h github.com
  - To forget about this account, run: gh auth logout -h github.com -u mryfmo
```

## Local state

```text
branch=rule/agmsg-orchestration
HEAD=c4f80cf0f02d71c7414fe92230290068f4ae09da
remote=https://github.com/mryfmo/dotfiles.git
main..HEAD=c4f80cf feat(claude-rules): add agmsg orchestration rule and fix ponytail symlink
```

`git diff --stat main...HEAD`:

```text
 .../dot_claude/rules/symlink_agmsg-orchestration.md.tmpl |  1 +
 home/dot_claude/rules/symlink_ponytail.md.tmpl           |  2 +-
 home/dot_config/claude/rules/agmsg-orchestration.md      | 16 ++++++++++++++++
 3 files changed, 18 insertions(+), 1 deletion(-)
```

## Initially deferred

- `gh pr create --base main`
- `gh pr view --json url,number,headRefOid`

These were deferred during the API outage and completed after the orchestrator verified recovery; see the PR creation evidence below.

## Authorized push-only revision

### `git push -u origin rule/agmsg-orchestration`

Exit: 0

```text
remote: 
remote: Create a pull request for 'rule/agmsg-orchestration' on GitHub by visiting:        
remote:      https://github.com/mryfmo/dotfiles/pull/new/rule/agmsg-orchestration        
remote: 
To github.com:mryfmo/dotfiles.git
 * [new branch]      rule/agmsg-orchestration -> rule/agmsg-orchestration
branch 'rule/agmsg-orchestration' set up to track 'origin/rule/agmsg-orchestration'.
```

No `gh` or PR command was attempted in this revision.

## AGMSG-only status revision

New HEAD:

```text
f5ffc2af097465577c75b74c113c4e11965168f1
```

### `git show --stat HEAD`

```text
commit f5ffc2af097465577c75b74c113c4e11965168f1
Author: mryfmo <mryfmo@gmail.com>
Date:   Fri Jul 17 08:34:09 2026 +0900

    feat(claude-rules): require agmsg-only worker status checks
    
    Status and liveness flow over the message bus (PING/PONG, RESULT); worker screens are not a status channel.
    
    Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>

 home/dot_config/claude/rules/agmsg-orchestration.md | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
```

### `git push`

Exit: 0

```text
To github.com:mryfmo/dotfiles.git
   c4f80cf..f5ffc2a  rule/agmsg-orchestration -> rule/agmsg-orchestration
```

`git rev-list --left-right --count origin/rule/agmsg-orchestration...HEAD` returned `0 0` after the push. PR creation remains unattempted.

## Designed turn-delivery revision

New HEAD:

```text
c1b82ef0125d0a9e4f9d5b24f5942eab8abcc39f
```

### `git show --stat HEAD`

```text
commit c1b82ef0125d0a9e4f9d5b24f5942eab8abcc39f
Author: mryfmo <mryfmo@gmail.com>
Date:   Fri Jul 17 08:41:01 2026 +0900

    feat(claude-rules): adopt designed codex turn delivery
    
    Use agmsg project-scoped turn delivery (.codex/hooks.json) instead of manual inbox nudges; ignore the machine-local hook file.
    
    Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>

 .gitignore                                          | 3 +++
 home/dot_config/claude/rules/agmsg-orchestration.md | 2 +-
 2 files changed, 4 insertions(+), 1 deletion(-)
```

### `git push`

Exit: 0

```text
To github.com:mryfmo/dotfiles.git
   f5ffc2a..c1b82ef  rule/agmsg-orchestration -> rule/agmsg-orchestration
```

Current `git diff --stat main...HEAD`:

```text
 .gitignore                                               |  3 +++
 .../dot_claude/rules/symlink_agmsg-orchestration.md.tmpl |  1 +
 home/dot_claude/rules/symlink_ponytail.md.tmpl           |  2 +-
 home/dot_config/claude/rules/agmsg-orchestration.md      | 16 ++++++++++++++++
 4 files changed, 21 insertions(+), 1 deletion(-)
```

Remote divergence was `0 0`; PR creation remained unattempted at this revision point.

## PR creation after API recovery

### `gh pr create --base main`

Exit: 0

```text
Warning: 57 uncommitted changes
https://github.com/mryfmo/dotfiles/pull/74
```

The warning refers to the pre-existing dirty and orchestration artifact paths; the PR head is the pushed commit and no artifact was committed.

### `gh pr view 74 --json url,number,headRefOid`

Exit: 0

```json
{"headRefOid":"c1b82ef0125d0a9e4f9d5b24f5942eab8abcc39f","number":74,"url":"https://github.com/mryfmo/dotfiles/pull/74"}
```

### Read-only CI snapshot

`gh pr checks 74` reported `validate` failed and the remaining checks pending immediately after PR creation. Per task constraints, no log investigation, CI/bot response, fix, or merge was attempted; the orchestrator owns the next phase.

## Validator correction revision

### `uv run --with pyyaml scripts/validate-agent-assets.py`

Exit: 0. Full output: empty.

### `uv run python -m unittest tests.unit.test_validate_agent_assets -v`

Exit: 0

```text
test_agmsg_script_modes_accept_prefixed_entrypoints_and_lib_helpers (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_script_modes_accept_prefixed_entrypoints_and_lib_helpers) ... ok
test_agmsg_script_modes_reject_non_executable_prefixed_entrypoint (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_script_modes_reject_non_executable_prefixed_entrypoint) ... ok
test_agmsg_script_modes_reject_unprefixed_direct_entrypoint (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_script_modes_reject_unprefixed_direct_entrypoint) ... ok
test_codex_modify_script_requires_executable_source (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_modify_script_requires_executable_source) ... ok
test_codex_sandbox_workspace_write_accepts_matching_manifest (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_sandbox_workspace_write_accepts_matching_manifest) ... ok
test_codex_sandbox_workspace_write_must_match_manifest (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_sandbox_workspace_write_must_match_manifest) ... ok
test_codex_sandbox_workspace_write_requires_all_agmsg_roots (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_sandbox_workspace_write_requires_all_agmsg_roots) ... ok
test_secret_scan_allows_exact_placeholder_tokens (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_allows_exact_placeholder_tokens) ... ok
test_secret_scan_checks_docs_paths (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_checks_docs_paths) ... ok
test_secret_scan_checks_extensionless_executables (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_checks_extensionless_executables) ... ok
test_secret_scan_checks_utf16_bom_text (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_checks_utf16_bom_text) ... ok
test_secret_scan_rejects_placeholder_with_suffix (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_rejects_placeholder_with_suffix) ... ok

----------------------------------------------------------------------
Ran 12 tests in 0.075s

OK
```

New HEAD:

```text
3504e7d72aa0b54b8104c58dd05772406ef7db54
```

### `git show --stat HEAD`

```text
commit 3504e7d72aa0b54b8104c58dd05772406ef7db54
Author: mryfmo <mryfmo@gmail.com>
Date:   Fri Jul 17 08:53:08 2026 +0900

    fix(validate): expect corrected ponytail rule symlink target
    
    The validator encoded the doubled-home dead path that this branch repairs.
    
    Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>

 scripts/validate-agent-assets.py | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
```

### `git push`

Exit: 0

```text
To github.com:mryfmo/dotfiles.git
   c1b82ef..3504e7d  rule/agmsg-orchestration -> rule/agmsg-orchestration
```

### PR synchronization

`gh pr view 74 --json url,number,headRefOid`:

```json
{"headRefOid":"3504e7d72aa0b54b8104c58dd05772406ef7db54","number":74,"url":"https://github.com/mryfmo/dotfiles/pull/74"}
```

The PR description was refreshed to cover the full four-commit diff. Remote divergence is `0 0`. The rerun `validate` check passes; other checks remained pending, with no CI/bot response or merge.

## Review-finding revision

### `uv run --with pyyaml scripts/validate-agent-assets.py`

Exit: 0

```text
agent asset validation ok
```

New HEAD:

```text
d34968bb59b71a7ea08682cb4a8ec988d602fce8
```

### `git show --stat HEAD`

```text
commit d34968bb59b71a7ea08682cb4a8ec988d602fce8
Author: mryfmo <mryfmo@gmail.com>
Date:   Fri Jul 17 09:02:05 2026 +0900

    fix(claude-rules): resolve delegation contradiction and storage caveat
    
    Address CodeRabbit and Codex reviewer findings: exempt orchestrator control-plane commands from delegation; require matching AGMSG_STORAGE_PATH on orchestrator calls for isolated workers.
    
    Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>

 home/dot_config/claude/rules/agmsg-orchestration.md | 4 ++--
 1 file changed, 2 insertions(+), 2 deletions(-)
```

### `git push`

Exit: 0

```text
To github.com:mryfmo/dotfiles.git
   3504e7d..d34968b  rule/agmsg-orchestration -> rule/agmsg-orchestration
```

### PR synchronization

```json
{"headRefOid":"d34968bb59b71a7ea08682cb4a8ec988d602fce8","number":74,"url":"https://github.com/mryfmo/dotfiles/pull/74"}
```

The PR description was refreshed to cover the full five-commit diff. The new `validate` check passes; remaining checks were pending. No bot reply or merge was performed.

## Final review and merge phase

### Inline replies

All four reply commands exited 0:

```json
{"body":"Rejected: the validator expectation was itself the defect. sourceDir already ends in home/, so the suggested target resolves to a dead home/home path (all working rule symlinks use dot_config/...). Fixed the validator instead in 3504e7d; validate is green on d34968b.","html_url":"https://github.com/mryfmo/dotfiles/pull/74#discussion_r3599546807","id":3599546807,"in_reply_to_id":3599482284}
{"body":"Fixed in d34968b: delegation narrowed to repository-mutating work with agmsg/herdr control-plane commands explicitly exempted.","html_url":"https://github.com/mryfmo/dotfiles/pull/74#discussion_r3599546897","id":3599546897,"in_reply_to_id":3599482292}
{"body":"Fixed in 3504e7d exactly as suggested: validator now expects the corrected target and the Agent assets workflow passes.","html_url":"https://github.com/mryfmo/dotfiles/pull/74#discussion_r3599546965","id":3599546965,"in_reply_to_id":3599487177}
{"body":"Fixed in d34968b: the storage bullet now requires the orchestrator to prefix the same AGMSG_STORAGE_PATH on send/watch/history for isolated workers.","html_url":"https://github.com/mryfmo/dotfiles/pull/74#discussion_r3599547027","id":3599547027,"in_reply_to_id":3599487178}
```

### Thread resolution

The initial GraphQL query found comment `3599482292` already resolved and the other three unresolved. The three mutations exited 0:

```json
{"data":{"resolveReviewThread":{"thread":{"id":"PRRT_kwDOSMyAV86RnLpH","isResolved":true}}}}
{"data":{"resolveReviewThread":{"thread":{"id":"PRRT_kwDOSMyAV86RnMi4","isResolved":true}}}}
{"data":{"resolveReviewThread":{"thread":{"id":"PRRT_kwDOSMyAV86RnMi5","isResolved":true}}}}
```

The corrected final query exited 0 and confirmed all four threads resolved:

```json
{"data":{"repository":{"pullRequest":{"reviewThreads":{"nodes":[{"id":"PRRT_kwDOSMyAV86RnLpH","isResolved":true,"comments":{"nodes":[{"databaseId":3599482284}]}},{"id":"PRRT_kwDOSMyAV86RnLpP","isResolved":true,"comments":{"nodes":[{"databaseId":3599482292}]}},{"id":"PRRT_kwDOSMyAV86RnMi4","isResolved":true,"comments":{"nodes":[{"databaseId":3599487177}]}},{"id":"PRRT_kwDOSMyAV86RnMi5","isResolved":true,"comments":{"nodes":[{"databaseId":3599487178}]}}]}}}}}
```

Two preceding read-only verification attempts had an extra GraphQL closing brace and returned parse errors; they made no state change.

### Final checks

`gh pr checks 74` exited 0. CodeRabbit, changes, validate, all public/private bootstrap jobs, and all macOS/Ubuntu tests passed; the optional nix job was skipped.

### `gh pr merge 74 --squash --delete-branch`

Exit: 0

```text
From https://github.com/mryfmo/dotfiles
 * branch            main       -> FETCH_HEAD
   8e25a4f..1c2943e  main       -> origin/main
Updating 8e25a4f..1c2943e
Created autostash: e1014df
Fast-forward
 .gitignore                                               |  3 +++
 .../dot_claude/rules/symlink_agmsg-orchestration.md.tmpl |  1 +
 home/dot_claude/rules/symlink_ponytail.md.tmpl           |  2 +-
 home/dot_config/claude/rules/agmsg-orchestration.md      | 16 ++++++++++++++++
 scripts/validate-agent-assets.py                         |  2 +-
 5 files changed, 22 insertions(+), 2 deletions(-)
 create mode 100644 home/dot_claude/rules/symlink_agmsg-orchestration.md.tmpl
 create mode 100644 home/dot_config/claude/rules/agmsg-orchestration.md
Applied autostash.
```

### Merge metadata

```json
{"baseRefOid":"8e25a4fad4cf76fc61113280a86091485ec9935f","headRefOid":"d34968bb59b71a7ea08682cb4a8ec988d602fce8","mergeCommit":{"oid":"1c2943ec733983d438a6493bbcb79d9067f6380b"},"mergedAt":"2026-07-17T00:12:28Z","state":"MERGED","url":"https://github.com/mryfmo/dotfiles/pull/74"}
```

Local verification:

```text
branch=main
HEAD=1c2943ec733983d438a6493bbcb79d9067f6380b
```

Both `git branch --list rule/agmsg-orchestration` and the GitHub branches API returned no matching branch, confirming local and remote branch deletion.
