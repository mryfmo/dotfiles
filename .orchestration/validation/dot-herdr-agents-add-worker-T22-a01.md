# Validation: dot-herdr-agents-add-worker-T22-a01

## Revision 4 (T34), worker claude-standard-dot-a005

Scratch paths are shown as `$S`, the session scratchpad. Every herdr and agmsg interaction in the tests is a fake running in a temp HOME.

### task_rev
```
$ git show origin/main:.orchestration/tasks/dot-herdr-agents-add-worker-T22-a01.md | sha256sum   # at 2c1b304, then at e0b7fb9 (ruling addendum)
b81b1b63a10b23bbfa72ee550d9e36ddcf2f1dbcae228ea6ad822772f41809ea  -
c3645fc7f78ceb4c1f97c5650521287de2b78c34e96d230c407fd7e94435e31c  -
```

### Deliverable B gate: spawn carries the full profile args (installed upstream 1.5.0, read-only), and the live identities (read-only)
```
$ cat ~/.agents/skills/agmsg/VERSION
1.5.0
$ sed -n 57,72p ~/.agents/skills/agmsg/scripts/spawn.sh
#   --model <id>       launch the agent on a specific model. The id is passed
#                      through to the CLI unchecked (the CLI rejects unknown
#                      ids); the flag spelling comes from the type's manifest
#                      `model_arg=`. Refused for a type with no model_arg.
#   --fresh            force a brand-new session even when the role has a
#                      resumable prior session. Without it, a type that supports
#                      resume (manifest `resume_arg=`) is brought back into its
#                      last session's context when that transcript still exists
#                      (#339); with it, spawn always boots fresh.
#
# Spawn options: extra CLI args to always pass a given type's launched
# binary (e.g. a default permission mode or sandbox policy), configured
# per-type in a YAML file rather than hardcoded — see
# scripts/lib/spawn-options.sh. File: $AGMSG_SPAWN_OPTIONS_FILE, else
# ~/.agmsg/config/spawn_options.yaml. Optional; a missing file/section is a
# no-op.
$ sed -n 322,328p ~/.agents/skills/agmsg/scripts/spawn.sh
# Extra CLI args for this type from the spawn options file (opt-in, see
# scripts/lib/spawn-options.sh). Read line-by-line — never word-split — so a
# value containing spaces stays a single token.
SPAWN_OPT_TOKENS=()
while IFS= read -r _spawn_opt_tok; do
  SPAWN_OPT_TOKENS+=("$_spawn_opt_tok")
done < <(agmsg_spawn_options_tokens "$AGENT_TYPE")
$ sed -n 586,591p ~/.agents/skills/agmsg/scripts/spawn.sh
    fi
    agmsg_role_resume_head "$AGENT_TYPE" "$RESUME_UUID"
    [ -n "$MODEL_ID" ] && printf ' %s %q' "$MODEL_ARG" "$MODEL_ID"
    for _tok in ${SPAWN_OPT_TOKENS[@]+"${SPAWN_OPT_TOKENS[@]}"}; do
      printf ' %q' "$_tok"
    done
$ sed -n 1,24p ~/.agents/skills/agmsg/scripts/lib/spawn-options.sh
#!/usr/bin/env bash
# spawn-options.sh — per-agent-type extra CLI args injected by spawn.sh.
#
# Reads a small YAML file mapping agent type -> a flat map of CLI flag ->
# value, using the same simple dialect db/config.yaml already uses (flat
# "section:" header + 2-space-indented "key: value", no nesting, no
# quoting — see config.sh's yaml_get). Turns one type's section into a list
# of ready-to-use shell tokens spawn.sh splices into its launch command.
#
# File resolution: $AGMSG_SPAWN_OPTIONS_FILE if set, else
# ~/.agmsg/config/spawn_options.yaml — agmsg's planned install-path-
# independent config home (#201), distinct from the current skill-dir-rooted
# db/config.yaml so it survives a custom --cmd install or multiple installs.
# A missing file, missing type section, or empty file all mean "no extra
# args" — this feature is fully opt-in and backward compatible.
#
# Value semantics (per key under a type's section):
#   <key>: <value>   -> two tokens: <key> <value>
#   <key>: true      -> one token:  <key>            (boolean flag on)
#   <key>: false     -> no tokens                     (explicitly suppressed)

# Guard against double-source.
[ -n "${_AGMSG_SPAWN_OPTIONS_SH:-}" ] && return 0
_AGMSG_SPAWN_OPTIONS_SH=1
$ grep -n model_arg ~/.agents/skills/agmsg/scripts/drivers/types/{claude-code,codex}/type.conf
/home/moriya/.agents/skills/agmsg/scripts/drivers/types/claude-code/type.conf:6:model_arg=--model
/home/moriya/.agents/skills/agmsg/scripts/drivers/types/codex/type.conf:115:model_arg=-m
$ grep MODEL_PROFILE_.*_ARGS ~/.agents/model-profiles.env
MODEL_PROFILE_ADH_CLAUDE_ARGS="--model claude-fable-5-1 --effort high"
MODEL_PROFILE_ADH_CODEX_ARGS="--profile adh"
MODEL_PROFILE_AUDIT_CLAUDE_ARGS="--model claude-fable-5-1 --effort high"
MODEL_PROFILE_AUDIT_CODEX_ARGS="--profile audit"
MODEL_PROFILE_DEEP_CLAUDE_ARGS="--model claude-fable-5-1 --effort high --advisor fable"
MODEL_PROFILE_DEEP_CODEX_ARGS="--profile deep"
MODEL_PROFILE_EXPRESS_CLAUDE_ARGS="--model haiku --effort low"
MODEL_PROFILE_EXPRESS_CODEX_ARGS="--profile express"
MODEL_PROFILE_REVIEW_CLAUDE_ARGS="--model claude-fable-5 --effort medium"
MODEL_PROFILE_REVIEW_CODEX_ARGS="--profile review"
MODEL_PROFILE_SECURITY_CLAUDE_ARGS="--model claude-fable-5 --effort high"
MODEL_PROFILE_SECURITY_CODEX_ARGS="--profile security"
MODEL_PROFILE_STANDARD_CLAUDE_ARGS="--model claude-opus-5-5 --effort high --advisor fable"
MODEL_PROFILE_STANDARD_CODEX_ARGS="--profile standard"
$ herdr agent start --help | head -3
Start a supported interactive agent in an existing pane

Usage: herdr agent start <NAME> --kind <KIND> --pane <ID> [OPTIONS] [-- [AGENT_ARG]...]
$ (read-only) AGMSG_RESOLVE_PROJECT=0 identities.sh <main> claude-code; identities.sh <worker-c> claude-code
dotfiles	claude-remediation-dot
dotfiles	claude-standard-dot-a006
dotfiles	claude-standard-dot-a005
```

### Branch diff against origin/main and commits
```
$ git diff origin/main --stat; git log --oneline origin/main..HEAD
 README.md                                          |  97 ++++-
 home/dot_agents/agent-config.yaml                  |   5 +
 home/dot_agents/model-profiles.env                 |   1 +
 .../dot_agents/skills/agmsg-orchestration/SKILL.md |   5 +-
 .../dot_config/claude/rules/agmsg-orchestration.md |   2 +-
 home/dot_local/bin/common/executable_herdr-agents  | 459 ++++++++++++++++++++-
 scripts/generate-agent-configs.py                  |  16 +
 scripts/validate-agent-assets.py                   |  10 +
 tests/unit/test_generate_agent_configs.py          |  21 +
 tests/unit/test_herdr_agents.py                    | 429 +++++++++++++++++++
 tests/unit/test_validate_agent_assets.py           |  16 +
 11 files changed, 1035 insertions(+), 26 deletions(-)
e226c27 fix(herdr-agents): close the worker-seat review findings
9d5cf7c feat(herdr-agents): add and remove parallel workers through agmsg spawn/despawn
3eeaeee feat(herdr-agents): seat the pair worker in its own worktree
```

### Mutation baseline A: new seat tests against unmodified origin/main
```
herdr-agents == origin/main e0b7fb9 (pre-change)
$ python3 -m unittest tests.unit.test_herdr_agents -k worktree -k reseats -k worker_seat -k attach_from_the_worker
.FFFFFF
======================================================================
FAIL: test_attach_from_the_worker_worktree_exits_quietly (tests.unit.test_herdr_agents.HerdrAgentsTest.test_attach_from_the_worker_worktree_exits_quietly)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_herdr_agents.py", line 2030, in test_attach_from_the_worker_worktree_exits_quietly
    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 2 != 0 : herdr-agents: worker_kind=claude would share the orchestrator's claude-code agmsg identity on /tmp/herdr-agents-test-c05sqele/project/.claude/worktrees/worker-c (0 claude-code identity registered); refusing so messages do not collide silently. Registering a second identity (AGMSG_RESOLVE_PROJECT=0 /tmp/herdr-agents-test-c05sqele/home/.agents/skills/agmsg/scripts/join.sh <team> <role> claude-code /tmp/herdr-agents-test-c05sqele/project/.claude/worktrees/worker-c) lifts this guard but does not give the two sessions distinct delivery until agmsg roles land; use worker_kind=codex for separate delivery now. See the herdr-agents section of the dotfiles README.


======================================================================
FAIL: test_full_mode_splits_the_worker_pane_in_its_worktree (tests.unit.test_herdr_agents.HerdrAgentsTest.test_full_mode_splits_the_worker_pane_in_its_worktree)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_herdr_agents.py", line 1987, in test_full_mode_splits_the_worker_pane_in_its_worktree
    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 2 != 0 : herdr-agents: worker_kind=claude would share the orchestrator's claude-code agmsg identity on /tmp/herdr-agents-test-ag4k8qfd/project (1 claude-code identity registered); refusing so messages do not collide silently. Registering a second identity (AGMSG_RESOLVE_PROJECT=0 /tmp/herdr-agents-test-ag4k8qfd/home/.agents/skills/agmsg/scripts/join.sh <team> <role> claude-code /tmp/herdr-agents-test-ag4k8qfd/project) lifts this guard but does not give the two sessions distinct delivery until agmsg roles land; use worker_kind=codex for separate delivery now. See the herdr-agents section of the dotfiles README.


======================================================================
FAIL: test_restart_worker_reseats_a_main_path_worker_into_its_worktree (tests.unit.test_herdr_agents.HerdrAgentsTest.test_restart_worker_reseats_a_main_path_worker_into_its_worktree)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_herdr_agents.py", line 1948, in test_restart_worker_reseats_a_main_path_worker_into_its_worktree
    self.assertIn(f"worktree {worktree}\n", listed)
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'worktree /tmp/herdr-agents-test-p59_hxg_/project/.claude/worktrees/worker-c\n' not found in 'worktree /tmp/herdr-agents-test-p59_hxg_/project\nHEAD 37ad40b76b1025dd23882832e9d4954a18840321\nbranch refs/heads/master\n\n'

======================================================================
FAIL: test_worker_seat_refuses_a_path_that_is_not_a_worktree (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_seat_refuses_a_path_that_is_not_a_worktree)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_herdr_agents.py", line 2004, in test_worker_seat_refuses_a_path_that_is_not_a_worktree
    self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 0 != 2 : Herdr agents worker restarted in pane w-old:p2


======================================================================
FAIL: test_worker_seat_refuses_an_ambiguous_orchestrator_identity (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_seat_refuses_an_ambiguous_orchestrator_identity)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_herdr_agents.py", line 2015, in test_worker_seat_refuses_an_ambiguous_orchestrator_identity
    self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 0 != 2 : Herdr agents worker restarted in pane w-old:p2


======================================================================
FAIL: test_worker_seat_reuses_the_identity_and_hook_already_at_the_worktree (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_seat_reuses_the_identity_and_hook_already_at_the_worktree)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_herdr_agents.py", line 1979, in test_worker_seat_reuses_the_identity_and_hook_already_at_the_worktree
    self.assertIn(f"identities {worktree} claude-code resolve=0", calls)
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'identities /tmp/herdr-agents-test-73at50sk/project/.claude/worktrees/worker-c claude-code resolve=0' not found in ['identities /tmp/herdr-agents-test-73at50sk/project claude-code resolve=', 'workspace list', 'pane list --workspace w-old', 'pane list --workspace w-old', 'agent get claude-worker-w-old', 'agent prompt w-old:p2 /exit', 'pane process-info --pane w-old:p2', 'pane process-info --pane w-old:p2', 'pane read w-old:p2 --source recent-unwrapped --lines 50', 'agent start claude-worker-w-old --kind claude --pane w-old:p2 --timeout 30000 -- --model opus --effort high', 'pane wait-output w-old:p2 --match trust this folder --timeout 3000', 'pane rename w-old:p2 claude-worker']

----------------------------------------------------------------------
Ran 7 tests in 2.088s

FAILED (failures=6)
```

### Mutation baseline B: add/remove tests against the deliverable-A script (3eeaeee)
```
herdr-agents == HEAD 3eeaeee (deliverable A only)
$ python3 -m unittest tests.unit.test_herdr_agents -k add_worker -k remove_worker
FFFFFFFFFFF
======================================================================
FAIL: test_add_worker_passes_codex_profile_and_sandbox_through_spawn_options (tests.unit.test_herdr_agents.HerdrAgentsTest.test_add_worker_passes_codex_profile_and_sandbox_through_spawn_options)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_herdr_agents.py", line 2089, in test_add_worker_passes_codex_profile_and_sandbox_through_spawn_options
    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 2 != 0 : Usage: herdr-agents [DIR]
       herdr-agents --attach
       herdr-agents --restart-worker [DIR]
       herdr-agents --bootstrap-agmsg [DIR]
       herdr-agents --audit <sha> [--out PATH] [--timeout SECONDS] [DIR]

Create a Herdr workspace for DIR with equal-width Claude Code and worker
panes from left to right, and open DIR in Zed when available. Herdr, jq,
Claude Code, and the worker's own CLI (codex, or claude when
HERDR_AGENTS_WORKER_KIND=claude) are required. DIR defaults to the current
directory. HERDR_AGENTS_WORKER_KIND selects the worker pane's agent kind
(codex or claude); it defaults to worker_kind from ~/.agents/model-profiles.env,
then codex.
Full mode heals an existing managed workspace for DIR instead of creating a
second one, and exits 2 when more than one managed workspace exists.
Attach mode uses the current Herdr pane for Claude.
Restart-worker mode exits the worker agent in the existing pair's worker pane
and starts it again in the same pane with the current worker_kind and
worker_profile launch arguments; it never creates panes or workspaces.
Bootstrap mode only configures missing repo-scoped agmsg hooks.
Audit mode runs the read-only Codex audit of <sha> in the existing pair
workspace's audit tab (created once, then reused and left open), tees it to
PATH (default .orchestration/validation/audit-<sha>.md under DIR), and exits
nonzero when the audit does or when the concluding line of PATH.last.md (the
codex exec -o last message) is not `Verdict: correct` (a missing, blocked, or
incorrect verdict); it exits 2 without a managed workspace.


======================================================================
FAIL: test_add_worker_rejects_a_worktree_outside_claude_worktrees (tests.unit.test_herdr_agents.HerdrAgentsTest.test_add_worker_rejects_a_worktree_outside_claude_worktrees) (path='../elsewhere')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_herdr_agents.py", line 2117, in test_add_worker_rejects_a_worktree_outside_claude_worktrees
    self.assertIn("the worker worktree must be a path under .claude/worktrees/", result.stderr)
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'the worker worktree must be a path under .claude/worktrees/' not found in "Usage: herdr-agents [DIR]\n       herdr-agents --attach\n       herdr-agents --restart-worker [DIR]\n       herdr-agents --bootstrap-agmsg [DIR]\n       herdr-agents --audit <sha> [--out PATH] [--timeout SECONDS] [DIR]\n\nCreate a Herdr workspace for DIR with equal-width Claude Code and worker\npanes from left to right, and open DIR in Zed when available. Herdr, jq,\nClaude Code, and the worker's own CLI (codex, or claude when\nHERDR_AGENTS_WORKER_KIND=claude) are required. DIR defaults to the current\ndirectory. HERDR_AGENTS_WORKER_KIND selects the worker pane's agent kind\n(codex or claude); it defaults to worker_kind from ~/.agents/model-profiles.env,\nthen codex.\nFull mode heals an existing managed workspace for DIR instead of creating a\nsecond one, and exits 2 when more than one managed workspace exists.\nAttach mode uses the current Herdr pane for Claude.\nRestart-worker mode exits the worker agent in the existing pair's worker pane\nand starts it again in the same pane with the current worker_kind and\nworker_profile launch arguments; it never creates panes or workspaces.\nBootstrap mode only configures missing repo-scoped agmsg hooks.\nAudit mode runs the read-only Codex audit of <sha> in the existing pair\nworkspace's audit tab (created once, then reused and left open), tees it to\nPATH (default .orchestration/validation/audit-<sha>.md under DIR), and exits\nnonzero when the audit does or when the concluding line of PATH.last.md (the\ncodex exec -o last message) is not `Verdict: correct` (a missing, blocked, or\nincorrect verdict); it exits 2 without a managed workspace.\n"

======================================================================
FAIL: test_add_worker_rejects_a_worktree_outside_claude_worktrees (tests.unit.test_herdr_agents.HerdrAgentsTest.test_add_worker_rejects_a_worktree_outside_claude_worktrees) (path='.claude/worktrees/..')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_herdr_agents.py", line 2117, in test_add_worker_rejects_a_worktree_outside_claude_worktrees
    self.assertIn("the worker worktree must be a path under .claude/worktrees/", result.stderr)
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'the worker worktree must be a path under .claude/worktrees/' not found in "Usage: herdr-agents [DIR]\n       herdr-agents --attach\n       herdr-agents --restart-worker [DIR]\n       herdr-agents --bootstrap-agmsg [DIR]\n       herdr-agents --audit <sha> [--out PATH] [--timeout SECONDS] [DIR]\n\nCreate a Herdr workspace for DIR with equal-width Claude Code and worker\npanes from left to right, and open DIR in Zed when available. Herdr, jq,\nClaude Code, and the worker's own CLI (codex, or claude when\nHERDR_AGENTS_WORKER_KIND=claude) are required. DIR defaults to the current\ndirectory. HERDR_AGENTS_WORKER_KIND selects the worker pane's agent kind\n(codex or claude); it defaults to worker_kind from ~/.agents/model-profiles.env,\nthen codex.\nFull mode heals an existing managed workspace for DIR instead of creating a\nsecond one, and exits 2 when more than one managed workspace exists.\nAttach mode uses the current Herdr pane for Claude.\nRestart-worker mode exits the worker agent in the existing pair's worker pane\nand starts it again in the same pane with the current worker_kind and\nworker_profile launch arguments; it never creates panes or workspaces.\nBootstrap mode only configures missing repo-scoped agmsg hooks.\nAudit mode runs the read-only Codex audit of <sha> in the existing pair\nworkspace's audit tab (created once, then reused and left open), tees it to\nPATH (default .orchestration/validation/audit-<sha>.md under DIR), and exits\nnonzero when the audit does or when the concluding line of PATH.last.md (the\ncodex exec -o last message) is not `Verdict: correct` (a missing, blocked, or\nincorrect verdict); it exits 2 without a managed workspace.\n"

======================================================================
FAIL: test_add_worker_rejects_a_worktree_outside_claude_worktrees (tests.unit.test_herdr_agents.HerdrAgentsTest.test_add_worker_rejects_a_worktree_outside_claude_worktrees) (path='.claude/worktrees/a/b')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_herdr_agents.py", line 2117, in test_add_worker_rejects_a_worktree_outside_claude_worktrees
    self.assertIn("the worker worktree must be a path under .claude/worktrees/", result.stderr)
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'the worker worktree must be a path under .claude/worktrees/' not found in "Usage: herdr-agents [DIR]\n       herdr-agents --attach\n       herdr-agents --restart-worker [DIR]\n       herdr-agents --bootstrap-agmsg [DIR]\n       herdr-agents --audit <sha> [--out PATH] [--timeout SECONDS] [DIR]\n\nCreate a Herdr workspace for DIR with equal-width Claude Code and worker\npanes from left to right, and open DIR in Zed when available. Herdr, jq,\nClaude Code, and the worker's own CLI (codex, or claude when\nHERDR_AGENTS_WORKER_KIND=claude) are required. DIR defaults to the current\ndirectory. HERDR_AGENTS_WORKER_KIND selects the worker pane's agent kind\n(codex or claude); it defaults to worker_kind from ~/.agents/model-profiles.env,\nthen codex.\nFull mode heals an existing managed workspace for DIR instead of creating a\nsecond one, and exits 2 when more than one managed workspace exists.\nAttach mode uses the current Herdr pane for Claude.\nRestart-worker mode exits the worker agent in the existing pair's worker pane\nand starts it again in the same pane with the current worker_kind and\nworker_profile launch arguments; it never creates panes or workspaces.\nBootstrap mode only configures missing repo-scoped agmsg hooks.\nAudit mode runs the read-only Codex audit of <sha> in the existing pair\nworkspace's audit tab (created once, then reused and left open), tees it to\nPATH (default .orchestration/validation/audit-<sha>.md under DIR), and exits\nnonzero when the audit does or when the concluding line of PATH.last.md (the\ncodex exec -o last message) is not `Verdict: correct` (a missing, blocked, or\nincorrect verdict); it exits 2 without a managed workspace.\n"

======================================================================
FAIL: test_add_worker_rejects_a_worktree_outside_claude_worktrees (tests.unit.test_herdr_agents.HerdrAgentsTest.test_add_worker_rejects_a_worktree_outside_claude_worktrees) (path='/tmp/x')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_herdr_agents.py", line 2117, in test_add_worker_rejects_a_worktree_outside_claude_worktrees
    self.assertIn("the worker worktree must be a path under .claude/worktrees/", result.stderr)
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'the worker worktree must be a path under .claude/worktrees/' not found in "Usage: herdr-agents [DIR]\n       herdr-agents --attach\n       herdr-agents --restart-worker [DIR]\n       herdr-agents --bootstrap-agmsg [DIR]\n       herdr-agents --audit <sha> [--out PATH] [--timeout SECONDS] [DIR]\n\nCreate a Herdr workspace for DIR with equal-width Claude Code and worker\npanes from left to right, and open DIR in Zed when available. Herdr, jq,\nClaude Code, and the worker's own CLI (codex, or claude when\nHERDR_AGENTS_WORKER_KIND=claude) are required. DIR defaults to the current\ndirectory. HERDR_AGENTS_WORKER_KIND selects the worker pane's agent kind\n(codex or claude); it defaults to worker_kind from ~/.agents/model-profiles.env,\nthen codex.\nFull mode heals an existing managed workspace for DIR instead of creating a\nsecond one, and exits 2 when more than one managed workspace exists.\nAttach mode uses the current Herdr pane for Claude.\nRestart-worker mode exits the worker agent in the existing pair's worker pane\nand starts it again in the same pane with the current worker_kind and\nworker_profile launch arguments; it never creates panes or workspaces.\nBootstrap mode only configures missing repo-scoped agmsg hooks.\nAudit mode runs the read-only Codex audit of <sha> in the existing pair\nworkspace's audit tab (created once, then reused and left open), tees it to\nPATH (default .orchestration/validation/audit-<sha>.md under DIR), and exits\nnonzero when the audit does or when the concluding line of PATH.last.md (the\ncodex exec -o last message) is not `Verdict: correct` (a missing, blocked, or\nincorrect verdict); it exits 2 without a managed workspace.\n"

======================================================================
FAIL: test_add_worker_reuses_a_seated_workspace (tests.unit.test_herdr_agents.HerdrAgentsTest.test_add_worker_reuses_a_seated_workspace)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_herdr_agents.py", line 2104, in test_add_worker_reuses_a_seated_workspace
    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 2 != 0 : Usage: herdr-agents [DIR]
       herdr-agents --attach
       herdr-agents --restart-worker [DIR]
       herdr-agents --bootstrap-agmsg [DIR]
       herdr-agents --audit <sha> [--out PATH] [--timeout SECONDS] [DIR]

Create a Herdr workspace for DIR with equal-width Claude Code and worker
panes from left to right, and open DIR in Zed when available. Herdr, jq,
Claude Code, and the worker's own CLI (codex, or claude when
HERDR_AGENTS_WORKER_KIND=claude) are required. DIR defaults to the current
directory. HERDR_AGENTS_WORKER_KIND selects the worker pane's agent kind
(codex or claude); it defaults to worker_kind from ~/.agents/model-profiles.env,
then codex.
Full mode heals an existing managed workspace for DIR instead of creating a
second one, and exits 2 when more than one managed workspace exists.
Attach mode uses the current Herdr pane for Claude.
Restart-worker mode exits the worker agent in the existing pair's worker pane
and starts it again in the same pane with the current worker_kind and
worker_profile launch arguments; it never creates panes or workspaces.
Bootstrap mode only configures missing repo-scoped agmsg hooks.
Audit mode runs the read-only Codex audit of <sha> in the existing pair
workspace's audit tab (created once, then reused and left open), tees it to
PATH (default .orchestration/validation/audit-<sha>.md under DIR), and exits
nonzero when the audit does or when the concluding line of PATH.last.md (the
codex exec -o last message) is not `Verdict: correct` (a missing, blocked, or
incorrect verdict); it exits 2 without a managed workspace.


======================================================================
FAIL: test_add_worker_spawns_the_seat_in_its_own_workspace_with_profile_args (tests.unit.test_herdr_agents.HerdrAgentsTest.test_add_worker_spawns_the_seat_in_its_own_workspace_with_profile_args)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_herdr_agents.py", line 2067, in test_add_worker_spawns_the_seat_in_its_own_workspace_with_profile_args
    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 2 != 0 : Usage: herdr-agents [DIR]
       herdr-agents --attach
       herdr-agents --restart-worker [DIR]
       herdr-agents --bootstrap-agmsg [DIR]
       herdr-agents --audit <sha> [--out PATH] [--timeout SECONDS] [DIR]

Create a Herdr workspace for DIR with equal-width Claude Code and worker
panes from left to right, and open DIR in Zed when available. Herdr, jq,
Claude Code, and the worker's own CLI (codex, or claude when
HERDR_AGENTS_WORKER_KIND=claude) are required. DIR defaults to the current
directory. HERDR_AGENTS_WORKER_KIND selects the worker pane's agent kind
(codex or claude); it defaults to worker_kind from ~/.agents/model-profiles.env,
then codex.
Full mode heals an existing managed workspace for DIR instead of creating a
second one, and exits 2 when more than one managed workspace exists.
Attach mode uses the current Herdr pane for Claude.
Restart-worker mode exits the worker agent in the existing pair's worker pane
and starts it again in the same pane with the current worker_kind and
worker_profile launch arguments; it never creates panes or workspaces.
Bootstrap mode only configures missing repo-scoped agmsg hooks.
Audit mode runs the read-only Codex audit of <sha> in the existing pair
workspace's audit tab (created once, then reused and left open), tees it to
PATH (default .orchestration/validation/audit-<sha>.md under DIR), and exits
nonzero when the audit does or when the concluding line of PATH.last.md (the
codex exec -o last message) is not `Verdict: correct` (a missing, blocked, or
incorrect verdict); it exits 2 without a managed workspace.


======================================================================
FAIL: test_remove_worker_despawns_then_turns_delivery_off_leaves_and_closes (tests.unit.test_herdr_agents.HerdrAgentsTest.test_remove_worker_despawns_then_turns_delivery_off_leaves_and_closes)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_herdr_agents.py", line 2131, in test_remove_worker_despawns_then_turns_delivery_off_leaves_and_closes
    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 2 != 0 : Usage: herdr-agents [DIR]
       herdr-agents --attach
       herdr-agents --restart-worker [DIR]
       herdr-agents --bootstrap-agmsg [DIR]
       herdr-agents --audit <sha> [--out PATH] [--timeout SECONDS] [DIR]

Create a Herdr workspace for DIR with equal-width Claude Code and worker
panes from left to right, and open DIR in Zed when available. Herdr, jq,
Claude Code, and the worker's own CLI (codex, or claude when
HERDR_AGENTS_WORKER_KIND=claude) are required. DIR defaults to the current
directory. HERDR_AGENTS_WORKER_KIND selects the worker pane's agent kind
(codex or claude); it defaults to worker_kind from ~/.agents/model-profiles.env,
then codex.
Full mode heals an existing managed workspace for DIR instead of creating a
second one, and exits 2 when more than one managed workspace exists.
Attach mode uses the current Herdr pane for Claude.
Restart-worker mode exits the worker agent in the existing pair's worker pane
and starts it again in the same pane with the current worker_kind and
worker_profile launch arguments; it never creates panes or workspaces.
Bootstrap mode only configures missing repo-scoped agmsg hooks.
Audit mode runs the read-only Codex audit of <sha> in the existing pair
workspace's audit tab (created once, then reused and left open), tees it to
PATH (default .orchestration/validation/audit-<sha>.md under DIR), and exits
nonzero when the audit does or when the concluding line of PATH.last.md (the
codex exec -o last message) is not `Verdict: correct` (a missing, blocked, or
incorrect verdict); it exits 2 without a managed workspace.


======================================================================
FAIL: test_remove_worker_force_passes_through_to_despawn (tests.unit.test_herdr_agents.HerdrAgentsTest.test_remove_worker_force_passes_through_to_despawn)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_herdr_agents.py", line 2166, in test_remove_worker_force_passes_through_to_despawn
    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 2 != 0 : Usage: herdr-agents [DIR]
       herdr-agents --attach
       herdr-agents --restart-worker [DIR]
       herdr-agents --bootstrap-agmsg [DIR]
       herdr-agents --audit <sha> [--out PATH] [--timeout SECONDS] [DIR]

Create a Herdr workspace for DIR with equal-width Claude Code and worker
panes from left to right, and open DIR in Zed when available. Herdr, jq,
Claude Code, and the worker's own CLI (codex, or claude when
HERDR_AGENTS_WORKER_KIND=claude) are required. DIR defaults to the current
directory. HERDR_AGENTS_WORKER_KIND selects the worker pane's agent kind
(codex or claude); it defaults to worker_kind from ~/.agents/model-profiles.env,
then codex.
Full mode heals an existing managed workspace for DIR instead of creating a
second one, and exits 2 when more than one managed workspace exists.
Attach mode uses the current Herdr pane for Claude.
Restart-worker mode exits the worker agent in the existing pair's worker pane
and starts it again in the same pane with the current worker_kind and
worker_profile launch arguments; it never creates panes or workspaces.
Bootstrap mode only configures missing repo-scoped agmsg hooks.
Audit mode runs the read-only Codex audit of <sha> in the existing pair
workspace's audit tab (created once, then reused and left open), tees it to
PATH (default .orchestration/validation/audit-<sha>.md under DIR), and exits
nonzero when the audit does or when the concluding line of PATH.last.md (the
codex exec -o last message) is not `Verdict: correct` (a missing, blocked, or
incorrect verdict); it exits 2 without a managed workspace.


======================================================================
FAIL: test_remove_worker_refuses_a_dirty_worktree_without_force (tests.unit.test_herdr_agents.HerdrAgentsTest.test_remove_worker_refuses_a_dirty_worktree_without_force)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_herdr_agents.py", line 2152, in test_remove_worker_refuses_a_dirty_worktree_without_force
    self.assertIn("has uncommitted changes; commit them or pass --force", result.stderr)
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'has uncommitted changes; commit them or pass --force' not found in "Usage: herdr-agents [DIR]\n       herdr-agents --attach\n       herdr-agents --restart-worker [DIR]\n       herdr-agents --bootstrap-agmsg [DIR]\n       herdr-agents --audit <sha> [--out PATH] [--timeout SECONDS] [DIR]\n\nCreate a Herdr workspace for DIR with equal-width Claude Code and worker\npanes from left to right, and open DIR in Zed when available. Herdr, jq,\nClaude Code, and the worker's own CLI (codex, or claude when\nHERDR_AGENTS_WORKER_KIND=claude) are required. DIR defaults to the current\ndirectory. HERDR_AGENTS_WORKER_KIND selects the worker pane's agent kind\n(codex or claude); it defaults to worker_kind from ~/.agents/model-profiles.env,\nthen codex.\nFull mode heals an existing managed workspace for DIR instead of creating a\nsecond one, and exits 2 when more than one managed workspace exists.\nAttach mode uses the current Herdr pane for Claude.\nRestart-worker mode exits the worker agent in the existing pair's worker pane\nand starts it again in the same pane with the current worker_kind and\nworker_profile launch arguments; it never creates panes or workspaces.\nBootstrap mode only configures missing repo-scoped agmsg hooks.\nAudit mode runs the read-only Codex audit of <sha> in the existing pair\nworkspace's audit tab (created once, then reused and left open), tees it to\nPATH (default .orchestration/validation/audit-<sha>.md under DIR), and exits\nnonzero when the audit does or when the concluding line of PATH.last.md (the\ncodex exec -o last message) is not `Verdict: correct` (a missing, blocked, or\nincorrect verdict); it exits 2 without a managed workspace.\n"

======================================================================
FAIL: test_remove_worker_stops_when_a_graceful_despawn_fails (tests.unit.test_herdr_agents.HerdrAgentsTest.test_remove_worker_stops_when_a_graceful_despawn_fails)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_herdr_agents.py", line 2182, in test_remove_worker_stops_when_a_graceful_despawn_fails
    self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 2 != 1 : Usage: herdr-agents [DIR]
       herdr-agents --attach
       herdr-agents --restart-worker [DIR]
       herdr-agents --bootstrap-agmsg [DIR]
       herdr-agents --audit <sha> [--out PATH] [--timeout SECONDS] [DIR]

Create a Herdr workspace for DIR with equal-width Claude Code and worker
panes from left to right, and open DIR in Zed when available. Herdr, jq,
Claude Code, and the worker's own CLI (codex, or claude when
HERDR_AGENTS_WORKER_KIND=claude) are required. DIR defaults to the current
directory. HERDR_AGENTS_WORKER_KIND selects the worker pane's agent kind
(codex or claude); it defaults to worker_kind from ~/.agents/model-profiles.env,
then codex.
Full mode heals an existing managed workspace for DIR instead of creating a
second one, and exits 2 when more than one managed workspace exists.
Attach mode uses the current Herdr pane for Claude.
Restart-worker mode exits the worker agent in the existing pair's worker pane
and starts it again in the same pane with the current worker_kind and
worker_profile launch arguments; it never creates panes or workspaces.
Bootstrap mode only configures missing repo-scoped agmsg hooks.
Audit mode runs the read-only Codex audit of <sha> in the existing pair
workspace's audit tab (created once, then reused and left open), tees it to
PATH (default .orchestration/validation/audit-<sha>.md under DIR), and exits
nonzero when the audit does or when the concluding line of PATH.last.md (the
codex exec -o last message) is not `Verdict: correct` (a missing, blocked, or
incorrect verdict); it exits 2 without a managed workspace.


----------------------------------------------------------------------
Ran 8 tests in 0.166s

FAILED (failures=11)
```

### Mutation baseline, review fixes: new tests against the reviewed head (9d5cf7c)
```
herdr-agents == HEAD 9d5cf7c (reviewed head, before the review fixes)
$ python3 -m unittest tests.unit.test_herdr_agents -k heal_moves -k skipped_in -k skipped_outside -k ambiguity_leaves -k attach_repair_splits -k refuses_to_start_outside -k undefined_profile -k forces_despawn
F.EFFFFF.
======================================================================
ERROR: test_full_mode_heal_moves_a_reused_empty_pane_into_the_worktree (tests.unit.test_herdr_agents.HerdrAgentsTest.test_full_mode_heal_moves_a_reused_empty_pane_into_the_worktree)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_herdr_agents.py", line 2050, in test_full_mode_heal_moves_a_reused_empty_pane_into_the_worktree
    cd_call = calls.index(f"pane run w-old:p2 cd -- {worktree}")
ValueError: list.index(x): x not in list

======================================================================
FAIL: test_add_worker_refuses_an_undefined_profile_before_any_change (tests.unit.test_herdr_agents.HerdrAgentsTest.test_add_worker_refuses_an_undefined_profile_before_any_change)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_herdr_agents.py", line 2135, in test_add_worker_refuses_an_undefined_profile_before_any_change
    self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 0 != 2 : Herdr agents worker added: claude-missing-dot-a007 in workspace w-test (/tmp/herdr-agents-test-lc5qkjsn/project/.claude/worktrees/b3)


======================================================================
FAIL: test_remove_worker_forces_despawn_for_a_codex_seat (tests.unit.test_herdr_agents.HerdrAgentsTest.test_remove_worker_forces_despawn_for_a_codex_seat)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_herdr_agents.py", line 2154, in test_remove_worker_forces_despawn_for_a_codex_seat
    self.assertIn("despawn dotfiles claude-remediation-dot codex-standard-dot-a008 --force", calls)
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'despawn dotfiles claude-remediation-dot codex-standard-dot-a008 --force' not found in ['workspace list', 'despawn dotfiles claude-remediation-dot codex-standard-dot-a008', 'delivery set off codex /tmp/herdr-agents-test-9bu7phkr/project/.claude/worktrees/b1', 'leave dotfiles codex-standard-dot-a008']

======================================================================
FAIL: test_restart_worker_refuses_to_start_outside_the_seat_when_the_pane_hangs (tests.unit.test_herdr_agents.HerdrAgentsTest.test_restart_worker_refuses_to_start_outside_the_seat_when_the_pane_hangs)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_herdr_agents.py", line 2126, in test_restart_worker_refuses_to_start_outside_the_seat_when_the_pane_hangs
    self.assertIn(f"never reached a shell prompt; refusing to start the worker outside {worktree}", result.stderr)
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'never reached a shell prompt; refusing to start the worker outside /tmp/herdr-agents-test-0vxyliyc/project/.claude/worktrees/worker-c' not found in 'Herdr agents worker seat: /tmp/herdr-agents-test-0vxyliyc/project/.claude/worktrees/worker-c (agmsg claude-standard-dot-a005)\nHerdr pane w-old:p2 did not reach an interactive shell prompt; refusing agent start.\n'

======================================================================
FAIL: test_worker_seat_ambiguity_leaves_no_worktree_behind (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_seat_ambiguity_leaves_no_worktree_behind)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_herdr_agents.py", line 2099, in test_worker_seat_ambiguity_leaves_no_worktree_behind
    self.assertFalse(worktree.exists())
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
AssertionError: True is not false

======================================================================
FAIL: test_worker_seat_is_skipped_in_a_non_git_directory (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_seat_is_skipped_in_a_non_git_directory)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_herdr_agents.py", line 2086, in test_worker_seat_is_skipped_in_a_non_git_directory
    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 2 != 0 : herdr-agents: unable to create worker worktree /tmp/herdr-agents-test-55tav5m9/project/.claude/worktrees/worker-c from origin/main in /tmp/herdr-agents-test-55tav5m9/project.


======================================================================
FAIL: test_worker_seat_is_skipped_in_an_unregistered_repository (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_seat_is_skipped_in_an_unregistered_repository)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_herdr_agents.py", line 2060, in test_worker_seat_is_skipped_in_an_unregistered_repository
    self.assertIn("would share the orchestrator's claude-code agmsg identity", result.stderr)
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: "would share the orchestrator's claude-code agmsg identity" not found in 'herdr-agents: need exactly one orchestrator claude-code identity at /tmp/herdr-agents-test-hlmahtdz/project to name the worker; register the worker yourself with: AGMSG_RESOLVE_PROJECT=0 /tmp/herdr-agents-test-hlmahtdz/home/.agents/skills/agmsg/scripts/join.sh <team> <name> claude-code /tmp/herdr-agents-test-hlmahtdz/project/.claude/worktrees/worker-c\n'

----------------------------------------------------------------------
Ran 9 tests in 2.297s

FAILED (failures=6, errors=1)
```

### make validate-agent-assets (final tree)
```
$ make validate-agent-assets
uv run --with pyyaml scripts/validate-agent-assets.py
agent asset validation ok
exit=0
```

### make unit-test (final tree; head and tail)
```
$ make unit-test
uv run python -m unittest discover -s tests/unit -v
test_bounded_scan_finishes_under_wall_limit (test_agent_session_staleness.AgentSessionStalenessTest.test_bounded_scan_finishes_under_wall_limit) ... ok
...

----------------------------------------------------------------------
Ran 561 tests in 94.077s

OK (skipped=1)
exit=0
```

### shellcheck / shfmt / CI ShellCheck step (final tree)
```
$ shellcheck -x home/dot_local/bin/common/executable_herdr-agents
exit=0
$ shfmt --indent 4 --space-redirects --diff home/dot_local/bin/common/executable_herdr-agents
exit=0
$ git ls-files -z 'setup.sh' 'install/*.sh' 'install/**/*.sh' 'scripts/*.sh' | xargs -0 shellcheck -x
exit=0
```

### CI on 3eeaeee (deliverable A)
```
$ gh pr checks 206
CodeRabbit	pass	0		Review skipped: manual review required for this OSS repository
changes	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/36514413684/job/109233412157	
private-bootstrap (macos-14, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/36514413698/job/109233412446	
test (macos-14, client)	pass	3m58s	https://github.com/mryfmo/dotfiles/actions/runs/36514413684/job/109233440681	
nix	skipping	0	https://github.com/mryfmo/dotfiles/actions/runs/36514413684/job/109233442282	
private-bootstrap (ubuntu-latest, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/36514413698/job/109233412347	
private-bootstrap (ubuntu-latest, server)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/36514413698/job/109233412249	
public-bootstrap (macos-14, client)	pass	8m56s	https://github.com/mryfmo/dotfiles/actions/runs/36514413698/job/109233412381	
public-bootstrap (ubuntu-latest, client)	pass	9m4s	https://github.com/mryfmo/dotfiles/actions/runs/36514413698/job/109233412421	
public-bootstrap (ubuntu-latest, server)	pass	6m17s	https://github.com/mryfmo/dotfiles/actions/runs/36514413698/job/109233412355	
test (ubuntu-latest, client)	pass	5m59s	https://github.com/mryfmo/dotfiles/actions/runs/36514413684/job/109233440750	
test (ubuntu-latest, server)	pass	3m14s	https://github.com/mryfmo/dotfiles/actions/runs/36514413684/job/109233440672	
validate	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/36514413665/job/109233412059	
exit=0
$ gh pr view 206 --json headRefOid -q .headRefOid
3eeaeeef78bf7bc002171fdd6f08ca1ab02d14a7
```

### CI on 9d5cf7c (deliverable B)
```
$ gh pr checks 206
CodeRabbit	pass	0		Review skipped: manual review required for this OSS repository
changes	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/36515363361/job/109236323825	
private-bootstrap (macos-14, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/36515363303/job/109236323981	
private-bootstrap (ubuntu-latest, client)	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/36515363303/job/109236323879	
private-bootstrap (ubuntu-latest, server)	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/36515363303/job/109236324017	
public-bootstrap (macos-14, client)	pass	9m12s	https://github.com/mryfmo/dotfiles/actions/runs/36515363303/job/109236323984	
public-bootstrap (ubuntu-latest, client)	pass	9m21s	https://github.com/mryfmo/dotfiles/actions/runs/36515363303/job/109236324165	
test (macos-14, client)	pass	3m58s	https://github.com/mryfmo/dotfiles/actions/runs/36515363361/job/109236364493	
nix	skipping	0	https://github.com/mryfmo/dotfiles/actions/runs/36515363361/job/109236365830	
public-bootstrap (ubuntu-latest, server)	pass	7m10s	https://github.com/mryfmo/dotfiles/actions/runs/36515363303/job/109236324154	
test (ubuntu-latest, client)	pass	5m37s	https://github.com/mryfmo/dotfiles/actions/runs/36515363361/job/109236364536	
test (ubuntu-latest, server)	pass	3m30s	https://github.com/mryfmo/dotfiles/actions/runs/36515363361/job/109236364519	
validate	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/36515363258/job/109236323554	
exit=0
$ gh pr view 206 --json headRefOid -q .headRefOid
9d5cf7ccefaccceb047aac9bdf3c524a4b43203a
```

### CompactionDB
```
$ python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "T34/T22 r4: the herdr-agents worker pane is seated in its own worktree (manifest worker_worktree -> HERDR_AGENTS_WORKER_WORKTREE), its identity registered there with AGMSG_RESOLVE_PROJECT=0 and delivery set on that path, so task delivery reaches the worker as turn/Monitor events; parallel workers are added and removed only through herdr-agents --add-worker/--remove-worker on upstream spawn.sh/despawn.sh (operator 2026-09-29). Ruling addendum: a worktree-seated Claude worker gets turn delivery only because upstream session-start.sh skips .claude/worktrees sessions (#367); spawn carries the full profile args via a generated AGMSG_SPAWN_OPTIONS_FILE."
f568614e-a324-499c-85f9-88a134a57c90
```

### Independent review (subagent, separate context) on 9d5cf7c, condensed findings and verdict

```
P1 high  executable_herdr-agents:1577-1593  full-mode heal reuses an agentless pane (empty_pane_id) and starts the worker there without cd -> pair worker runs in the main checkout (the defect).
P2 high  :343-345 (+194,1461,1499,1644)  worker_worktree is host-global: creates <DIR>/.claude/worktrees/worker-c in any repo (before the identity check), nested worktrees from linked worktrees, and half-built workspaces in non-git DIRs.
P2 high  :1275-1290  codex seats never hold the actas lock -> graceful despawn always needs-force, and --force also disables the dirty refusal.
P2 med   :1238-1241, 293-297  unknown --profile passes the regex; claude spawn boots the default model; comment overclaims HERDR_AGENTS_CLAUDE_WORKER_ARGS.
P3 high  SKILL.md:41, README.md:484-487  "no Monitor watch" too broad (spawn seats start Monitor via actas); add-worker workspace lacks KEEP_ALIVE / RESOLVE_PROJECT env.
P3 high  README.md:400-403  still says nested-worktree seats rely on milestone inbox.sh (contradicts the retirement).
P3 med   :714  re-seat cd silently skipped when the prompt wait times out.
P3 med   :230,240-241  one name in two teams refused as ambiguous.
P3 med   :275-283  codex worktree hook written without the trust notice.
P3 high  tests  no coverage for attach repair with a seat, the heal empty-pane path, codex remove, non-git/other-repo DIRs.
Verdict: incorrect
```

Disposition: every finding is fixed in e226c27. Each has a resolved crit record in `.orchestration/validation/dot-herdr-agents-add-worker-T22-a01-crit.json` (receipt `…-review-receipt.md`); its baseline is above.

### CI on the final head e226c27
```
$ gh pr checks 206
CodeRabbit	pass	0		Review skipped: manual review required for this OSS repository
changes	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/36518197886/job/109245106702	
private-bootstrap (macos-14, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/36518197941/job/109245107572	
private-bootstrap (ubuntu-latest, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/36518197941/job/109245107459	
private-bootstrap (ubuntu-latest, server)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/36518197941/job/109245107430	
public-bootstrap (macos-14, client)	pass	8m3s	https://github.com/mryfmo/dotfiles/actions/runs/36518197941/job/109245107240	
public-bootstrap (ubuntu-latest, client)	pass	8m24s	https://github.com/mryfmo/dotfiles/actions/runs/36518197941/job/109245107537	
public-bootstrap (ubuntu-latest, server)	pass	7m15s	https://github.com/mryfmo/dotfiles/actions/runs/36518197941/job/109245107524	
test (macos-14, client)	pass	3m19s	https://github.com/mryfmo/dotfiles/actions/runs/36518197886/job/109245140754	
validate	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/36518198201/job/109245108585	
nix	skipping	0	https://github.com/mryfmo/dotfiles/actions/runs/36518197886/job/109245141741	
test (ubuntu-latest, client)	pass	6m8s	https://github.com/mryfmo/dotfiles/actions/runs/36518197886/job/109245140743	
test (ubuntu-latest, server)	pass	3m16s	https://github.com/mryfmo/dotfiles/actions/runs/36518197886/job/109245140749	
exit=0
$ gh pr view 206 --json headRefOid -q .headRefOid
e226c27a756fcdc921d831bec320db37b2dc1c3a
```

---

## Revision 4b (reply RESULT revision=5): graceful-first despawn (fix 16d095f)

### Upstream despawn.sh semantics (read-only)
```
$ sed -n 116,118p;163,175p ~/.agents/skills/agmsg/scripts/despawn.sh   # upstream: --force needs a record; graceful ok without one; needs-force with a record but no lock
if [ "$FORCE" = "1" ]; then
  KILL_RECORDED_REASON=""
  [ -f "$SPAWN_REC" ] || die "no placement record for '$TEAM/$NAME' — nothing to force (was it launched via 'spawn'? graceful despawn does not need this)"
    if [ -f "$SPAWN_REC" ]; then
      # A pane/process was placed and is likely still there. Do NOT delete the record
      # (--force reads exactly this — deleting it here is what made the advised
      # recovery impossible), and do NOT report a teardown we did not perform.
      echo "despawn: '$NAME' holds no live actas lock, but a placement record remains — graceful despawn cannot confirm a teardown (a monitor=no member such as cursor/codex never holds a lock; a watcher may have died). Retry with --force to tear it down via the record, which is kept intact." >&2
      echo "status=needs-force name=$NAME team=$TEAM note=no-live-lock-recorded"
      exit 1
    fi
    # No placement record: nothing was spawned here to tear down (a hand-joined
    # member, or one already gone). The free lock is all there is to act on.
    echo "despawn: '$NAME' holds no live actas lock and has no placement record — nothing to tear down here (if a window remains, it was not launched via spawn; close it directly)." >&2
    echo "status=ok name=$NAME team=$TEAM note=no-live-lock"
    exit 0
```

### Mutation baseline: remove-worker tests against e226c27
```
herdr-agents content == HEAD e226c27 (e226c27; checked with cmp; file mode kept at the restored 100644)
$ python3 -m unittest tests.unit.test_herdr_agents -k remove_worker
F.EFF...
======================================================================
ERROR: test_remove_worker_force_retries_a_failed_graceful_despawn (tests.unit.test_herdr_agents.HerdrAgentsTest.test_remove_worker_force_retries_a_failed_graceful_despawn)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_herdr_agents.py", line 2295, in test_remove_worker_force_retries_a_failed_graceful_despawn
    graceful = calls.index("despawn dotfiles claude-remediation-dot claude-standard-dot-a007")
ValueError: list.index(x): x not in list

======================================================================
FAIL: test_remove_worker_cleans_up_a_codex_seat_without_a_placement_record (tests.unit.test_herdr_agents.HerdrAgentsTest.test_remove_worker_cleans_up_a_codex_seat_without_a_placement_record)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_herdr_agents.py", line 2342, in test_remove_worker_cleans_up_a_codex_seat_without_a_placement_record
    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 1 != 0 : herdr-agents: despawn of codex-standard-dot-a008 did not complete; re-run with --force.


======================================================================
FAIL: test_remove_worker_force_skips_the_forced_despawn_when_graceful_succeeds (tests.unit.test_herdr_agents.HerdrAgentsTest.test_remove_worker_force_skips_the_forced_despawn_when_graceful_succeeds)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_herdr_agents.py", line 2306, in test_remove_worker_force_skips_the_forced_despawn_when_graceful_succeeds
    self.assertFalse(any(c.endswith(" --force") and c.startswith("despawn") for c in self.calls_path.read_text().splitlines()))
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: True is not false

======================================================================
FAIL: test_remove_worker_forces_despawn_when_graceful_reports_needs_force (tests.unit.test_herdr_agents.HerdrAgentsTest.test_remove_worker_forces_despawn_when_graceful_reports_needs_force)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_herdr_agents.py", line 2314, in test_remove_worker_forces_despawn_when_graceful_reports_needs_force
    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 1 != 0 : status=needs-force name=x team=dotfiles note=no-live-lock-recorded
herdr-agents: despawn of claude-standard-dot-a007 did not complete; re-run with --force.


----------------------------------------------------------------------
Ran 8 tests in 0.316s

FAILED (failures=3, errors=1)
```

### make validate-agent-assets
```
$ make validate-agent-assets
uv run --with pyyaml scripts/validate-agent-assets.py
agent asset validation ok
exit=0
```

### make unit-test (head and tail)
```
$ make unit-test
uv run python -m unittest discover -s tests/unit -v
test_bounded_scan_finishes_under_wall_limit (test_agent_session_staleness.AgentSessionStalenessTest.test_bounded_scan_finishes_under_wall_limit) ... ok
...

----------------------------------------------------------------------
Ran 564 tests in 94.002s

OK (skipped=1)
exit=0
```

### shellcheck / shfmt / CI ShellCheck step
```
$ shellcheck -x home/dot_local/bin/common/executable_herdr-agents
exit=0
$ shfmt --indent 4 --space-redirects --diff home/dot_local/bin/common/executable_herdr-agents
exit=0
$ git ls-files -z 'setup.sh' 'install/*.sh' 'install/**/*.sh' 'scripts/*.sh' | xargs -0 shellcheck -x
exit=0
```

### CI on 16d095f
```
$ gh pr checks 206
public-bootstrap (ubuntu-latest, client)	fail	6s	https://github.com/mryfmo/dotfiles/actions/runs/36523890490/job/109262524888	
nix	skipping	0	https://github.com/mryfmo/dotfiles/actions/runs/36523890516/job/109262563776	
test (macos-14, client)	pass	3m18s	https://github.com/mryfmo/dotfiles/actions/runs/36523890516/job/109262562399	
test (ubuntu-latest, server)	pass	3m8s	https://github.com/mryfmo/dotfiles/actions/runs/36523890516/job/109262562381	
public-bootstrap (macos-14, client)	fail	1m40s	https://github.com/mryfmo/dotfiles/actions/runs/36523890490/job/109262524725	
private-bootstrap (macos-14, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/36523890490/job/109262525002	
private-bootstrap (ubuntu-latest, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/36523890490/job/109262524900	
private-bootstrap (ubuntu-latest, server)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/36523890490/job/109262524956	
test (ubuntu-latest, client)	pass	5m51s	https://github.com/mryfmo/dotfiles/actions/runs/36523890516/job/109262562357	
public-bootstrap (ubuntu-latest, server)	fail	1m36s	https://github.com/mryfmo/dotfiles/actions/runs/36523890490/job/109262524989	
CodeRabbit	pass	0		Review skipped: manual review required for this OSS repository
changes	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/36523890516/job/109262524889	
validate	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/36523890544/job/109262525190	
exit=1
$ gh pr view 206 --json headRefOid -q .headRefOid
16d095f182e5f8085965ce61f1d8058933e95f75
```

### CI rerun on 16d095f (green)
```
$ gh pr checks 206   # after gh run rerun 36523890490 --failed (curl 500 in public-bootstrap)
nix	skipping	0	https://github.com/mryfmo/dotfiles/actions/runs/36523890516/job/109262563776	
CodeRabbit	pass	0		Review skipped: manual review required for this OSS repository
changes	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/36523890516/job/109262524889	
private-bootstrap (macos-14, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/36523890490/job/109265231430	
private-bootstrap (ubuntu-latest, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/36523890490/job/109265207172	
private-bootstrap (ubuntu-latest, server)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/36523890490/job/109265208055	
public-bootstrap (macos-14, client)	pass	7m48s	https://github.com/mryfmo/dotfiles/actions/runs/36523890490/job/109265206318	
public-bootstrap (ubuntu-latest, client)	pass	10m13s	https://github.com/mryfmo/dotfiles/actions/runs/36523890490/job/109265206550	
public-bootstrap (ubuntu-latest, server)	pass	7m1s	https://github.com/mryfmo/dotfiles/actions/runs/36523890490/job/109265206612	
test (macos-14, client)	pass	3m18s	https://github.com/mryfmo/dotfiles/actions/runs/36523890516/job/109262562399	
test (ubuntu-latest, client)	pass	5m51s	https://github.com/mryfmo/dotfiles/actions/runs/36523890516/job/109262562357	
test (ubuntu-latest, server)	pass	3m8s	https://github.com/mryfmo/dotfiles/actions/runs/36523890516/job/109262562381	
validate	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/36523890544/job/109262525190	
exit=0
$ gh pr view 206 --json headRefOid -q .headRefOid
16d095f182e5f8085965ce61f1d8058933e95f75
```

---

## Revision 6 (rebase onto 2e0c6f4; integration fix 9da17b9)

### Branch against origin/main, commits, file mode, SKILL bullets
```
$ git rev-parse --short origin/main; git diff origin/main --stat; git log --oneline origin/main..HEAD
2e0c6f4
 README.md                                          | 101 ++++-
 home/dot_agents/agent-config.yaml                  |   5 +
 home/dot_agents/model-profiles.env                 |   1 +
 .../dot_agents/skills/agmsg-orchestration/SKILL.md |   5 +-
 .../dot_config/claude/rules/agmsg-orchestration.md |   2 +-
 home/dot_local/bin/common/executable_herdr-agents  | 479 +++++++++++++++++++-
 scripts/generate-agent-configs.py                  |  16 +
 scripts/validate-agent-assets.py                   |  10 +
 tests/unit/test_generate_agent_configs.py          |  21 +
 tests/unit/test_herdr_agents.py                    | 481 +++++++++++++++++++++
 tests/unit/test_validate_agent_assets.py           |  16 +
 11 files changed, 1110 insertions(+), 27 deletions(-)
9da17b9 fix(herdr-agents): load seat labels after the worker's quiet attach exit
02768d9 fix(herdr-agents): despawn a removed worker graceful-first
fd0b050 fix(herdr-agents): close the worker-seat review findings
8c16ef6 feat(herdr-agents): add and remove parallel workers through agmsg spawn/despawn
019ee6d feat(herdr-agents): seat the pair worker in its own worktree
$ git ls-tree HEAD home/dot_local/bin/common/executable_herdr-agents
100644 blob ec08af2fbd157f5b8179930c62f17de41a9072e5	home/dot_local/bin/common/executable_herdr-agents
$ sed -n "/^## Parallel workers/,+3p" home/dot_agents/skills/agmsg-orchestration/SKILL.md | cut -c1-120
## Parallel workers

- Add and remove parallel workers only with `herdr-agents --add-worker <worktree> [--kind codex|claude] [--profile NAME]
- Under upstream agmsg 1.5.0 self-naming, a pair's panes carry `<team>:<name>` labels rather than `claude-orchestrator`/
```

### make validate-agent-assets
```
$ make validate-agent-assets
uv run --with pyyaml scripts/validate-agent-assets.py
agent asset validation ok
exit=0
```

### make unit-test (head and tail; the run before 9da17b9 failed only test_attach_from_the_worker_worktree_exits_quietly)
```
$ make unit-test
uv run python -m unittest discover -s tests/unit -v
test_bounded_scan_finishes_under_wall_limit (test_agent_session_staleness.AgentSessionStalenessTest.test_bounded_scan_finishes_under_wall_limit) ... ok
...

----------------------------------------------------------------------
Ran 577 tests in 97.981s

OK (skipped=1)
exit=0
```

### shellcheck / shfmt / CI ShellCheck step
```
$ shellcheck -x home/dot_local/bin/common/executable_herdr-agents
exit=0
$ shfmt --indent 4 --space-redirects --diff home/dot_local/bin/common/executable_herdr-agents
exit=0
$ git ls-files -z 'setup.sh' 'install/*.sh' 'install/**/*.sh' 'scripts/*.sh' | xargs -0 shellcheck -x
exit=0
```

### CI on the rebased head 9da17b9 (green, MERGEABLE)
```
$ gh pr checks 206
CodeRabbit	pass	0		Review skipped: manual review required for this OSS repository
changes	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/36526379482/job/109270236334	
test (ubuntu-latest, server)	pass	2m56s	https://github.com/mryfmo/dotfiles/actions/runs/36526379482/job/109270273422	
nix	skipping	0	https://github.com/mryfmo/dotfiles/actions/runs/36526379482/job/109270274371	
private-bootstrap (macos-14, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/36526379463/job/109270236270	
private-bootstrap (ubuntu-latest, client)	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/36526379463/job/109270236356	
private-bootstrap (ubuntu-latest, server)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/36526379463/job/109270236284	
public-bootstrap (macos-14, client)	pass	9m23s	https://github.com/mryfmo/dotfiles/actions/runs/36526379463/job/109270236145	
public-bootstrap (ubuntu-latest, client)	pass	9m11s	https://github.com/mryfmo/dotfiles/actions/runs/36526379463/job/109270236275	
public-bootstrap (ubuntu-latest, server)	pass	7m15s	https://github.com/mryfmo/dotfiles/actions/runs/36526379463/job/109270236320	
test (macos-14, client)	pass	3m20s	https://github.com/mryfmo/dotfiles/actions/runs/36526379482/job/109270273372	
test (ubuntu-latest, client)	pass	5m24s	https://github.com/mryfmo/dotfiles/actions/runs/36526379482/job/109270273327	
validate	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/36526379471/job/109270236152	
exit=0
$ gh pr view 206 --json headRefOid,mergeable -q "\(.headRefOid) \(.mergeable)"
9da17b9d263638937cb25bdc26893a13c06a4d60 MERGEABLE
```
