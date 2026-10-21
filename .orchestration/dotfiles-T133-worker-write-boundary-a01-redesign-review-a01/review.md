---
task_id: dotfiles-T133-worker-write-boundary-a01-redesign-review-a01
seat: claude-standard-dot-a009
kind: review
design_sha256: ae1088a7fdef88152f6829c18440f9a4616b07dd4bde6381ed0f120d1b06be50
verdict: accept
---

# Review: the redesign dotfiles-T133-worker-write-boundary-a02 (INV-6 reset anchor of a01)

Read-only, from this worktree inside the sandbox. The subject is the main checkout's `.orchestration/tasks/dotfiles-T133-worker-write-boundary-a02.md`; the record is `.orchestration/acceptance/dotfiles-T133-worker-write-boundary-a01.md`. The task copy of this review is the dispatched file, sha256 `557ca6e3…`.

## Hash

```console
$ shasum -a 256 ~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-a02.md
ae1088a7fdef88152f6829c18440f9a4616b07dd4bde6381ed0f120d1b06be50  ~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-a02.md
```

It equals the expected `ae1088a7…`. Observation, not a finding: `origin/main` `f7f38067` carries a different version of the file (`git show origin/main:… | shasum -a 256` → `6d36b24e…`). This review judges the expected hash, as the task directs.

## Items

1. **The hash: ok.** As above.
2. **`reset_of`, the findings, and no widening: ok.**
   - **`reset_of`:** the front matter has `reset_of: [dotfiles-T133-worker-write-boundary-a01]` (a02:7). `format`, `kind: code`, `security: true` and `after: []` are as in a01.
   - **The findings that forced the reset** (the record's lines from 12:38:02Z to 12:51:39Z):
     - **`security:ea3c4fb:1` (tracked-hook-startup-validation).** a02:549 names it. Its Goal item 1 adds one whole-inventory screening before worker start, covering every documented executable configuration source (S01–S23). That includes the tracked `.claude/settings.json` hooks, `apiKeyHelper`, `statusLine.command` and MCP commands, in the tracked, legacy, user and managed scopes (a02:181, :408, :494, :722). Legacy `--legacy` handling may not retain an executable field (a02:722). The test `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_executable_settings_entrypoints_are_checked_before_launch` must be red on `ea3c4fb8` and green at the final head (a02:828, :912, :992).
     - **The superseded-head P1 `security:a286915` (the SKILL step 4 contradiction).** a02:549 settles it explicitly instead of treating its absence from the final-head report as closure. Step 4 states one sandbox-only sentence, with no worker exception in steps 2, 5 and 11. The three exemptions (evidence-sync writes and masking, CompactionDB consolidation, agmsg-dispatch) stay orchestrator-only (a02:860–870). Its test is `tests/unit/test_agmsg_orchestration_docs.py::AgmsgOrchestrationSkillTest::test_worker_playbook_has_no_sandbox_exceptions` (a02:870, :1004), with threat rows a02:57 and :69.
   - **The carried decisions and rows:**
     - The D-024-26 narrowing is kept. The executable-binding family stays out, and the a01 implementation continues from `ea3c4fb8` on PR #431 (a02:197, :451, :1052).
     - The agmsg-hardening owner rows (`text-security:08e6ac7:2`, `text-security:5cbbc03:2`) are carried, with the same count of mentions as a01 (3).
   - **No widening of permissions or trust boundaries:**
     - `allowed_files` is the same 22-entry list as a01, apart from the task's own evidence directory.
     - The managed `sandbox.excludedCommands` list is exactly a01's three entries: `agmsg-dispatch *`, `herdr-agents *` and `<absolute-home>/.agents/skills/agmsg/scripts/actas-claim.sh *` (a01:392–398 = a02:685–691).
     - The managed `allowUnixSockets` herdr socket is unchanged (a01:400 = a02:693).
     - The worker user policy keeps `failIfUnavailable: true`, `allowUnsandboxedCommands: false`, no excluded commands, no Herdr socket, and restricted writes (a02:353, :377, :386–387).
     - Among a02's added lines, the permission terms only narrow. Administrative scope does not exempt executable fields (a02:181). Managed MCP definitions get no exemption (rows a02:55, :78). The former Linux gh exemption stays removed (a02:609). Refusal is no invitation to bypass the sandbox (a02:545).
3. **Read only: ok.** This review changed no tracked file and dispatched nothing. Its only output is this uncommitted file in this worktree, with no commit, PR or push.

## Verdict

`verdict: accept`.

Scope of this judgment: whether the redesign's front matter, its coverage of the reset findings, and its permission surface meet items 1 to 3. It is not a re-run of the C-80 security review of the a02 text, which the record and the text's Checks block list separately.
