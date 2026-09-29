# Validation: dot-herdr-agents-seat-labels-T35-a01 (revision 1)

### task_rev
```
$ git show origin/main:.orchestration/tasks/dot-herdr-agents-seat-labels-T35-a01.md | sha256sum   # at b790ee0
2e8aa0d2595db53feae437a91c73f359d2b970795a9aecfa982f7441993f3cd1  -
```

### Diagnosis (read-only): upstream 1.5.0 sources, herdr --help, live list output
```
# Diagnosis (read-only): installed agmsg 1.5.0 sources, herdr --help, and herdr list output
$ cat ~/.agents/skills/agmsg/VERSION
1.5.0
$ grep -rn -i "workspace rename\|herdr workspace" ~/.agents/skills/agmsg/scripts   # upstream never renames a workspace
[matches: 0]
$ sed -n 1240,1260p ~/.agents/skills/agmsg/scripts/drivers/terminals/herdr/ops.sh   # the two renames self-naming performs
  printf 'a%s\n' "${hex:0:24}"
}

# control op: name the pane (scope Naming). Two copies:
#   VISIBLE:    herdr pane rename <id> <team>:<agent>   (free text, ':' is fine)
#   RESOLVABLE: herdr agent rename <id> <key>           where <key> is the
#               collision-resistant SHA-256 derivation above — an INTERNAL key,
#               never shown; peek/poke go by the recorded pane id, so the user never
#               meets it. Idempotent. The visible rename is the required one; a
#               failed agent rename (a live-name collision, or no SHA-256 tool to
#               derive the key) is non-fatal — the pane id in the record still
#               resolves.
# <mode> is `key` or absent. Absent means both names; `key` means the resolvable
# one only, and the caller has already decided that (the registry reads the env
# var, so the policy lives in one place and this only carries it out).
#
# Which of the two is which matters: `pane rename` is the label a person reads,
# `agent rename` is the name herdr itself addresses the agent by, in its own
# namespace — NOT what this repo's `peek`/`poke` resolve through, which is the
# placement record's pane id. So under `key` that name is still established and
# only the decoration is skipped —
$ grep -n "pane rename\|agent rename" ~/.agents/skills/agmsg/scripts/drivers/terminals/herdr/ops.sh | sed -n 1,20p
540:  _herdr_cli "$qualified" pane rename "$pane" "$label" >/dev/null 2>&1 || true
1369:  _err="$(_herdr_cli "$id" agent rename "$(_herdr_bare_of "$id")" "$key" 2>&1 >/dev/null)" || _rc=$?
1382:    _herdr_cli "$id" pane rename "$(_herdr_bare_of "$id")" "$label" >/dev/null 2>&1 || true
$ grep -n "AGMSG_SELF_NAME\|name its own pane\|when it ACTS" ~/.agents/skills/agmsg/scripts/lib/self-name.sh | head
2:# self-name.sh — a seat names its own pane when it ACTS, if it is not named.
33:#     name. The old seat, if it acts again from elsewhere, finds its mark
57:#   agmsg_self_name_on_action <team> <agent> [<project>] [<type>]
59:[ -n "${_AGMSG_SELF_NAME_SH:-}" ] && return 0
60:_AGMSG_SELF_NAME_SH=1
62:_agmsg_self_name_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
63:: "${SKILL_DIR:=$(cd "$_agmsg_self_name_dir/../.." && pwd)}"
95:_agmsg_self_name_env_corroborated() {   # <terminal> <id> <team> <agent>
$ grep -n "agmsg_self_name_on_action" ~/.agents/skills/agmsg/scripts/send.sh ~/.agents/skills/agmsg/scripts/inbox.sh
/home/moriya/.agents/skills/agmsg/scripts/send.sh:77:agmsg_self_name_on_action "$TEAM" "$FROM"
/home/moriya/.agents/skills/agmsg/scripts/inbox.sh:23:agmsg_self_name_on_action "$TEAM" "$AGENT"
$ herdr workspace --help | sed -n 1,14p
Manage workspaces over the socket API

Usage: herdr workspace [COMMAND]

Commands:
  list             List workspaces
  create           Create a workspace
  get              Show a workspace
  focus            Focus a workspace
  rename           Rename a workspace
  report-metadata  Report display-only workspace metadata
  close            Close a workspace

Are you an AI? Use these resources ONLY IF your task specifically asks you to:
$ herdr workspace list | jq -c ".result.workspaces[] | {workspace_id,label,keys:keys}"
{"workspace_id":"wJ","label":"dotfiles","keys":["active_tab_id","agent_status","focused","label","number","pane_count","tab_count","workspace_id"]}
$ herdr pane list --workspace wJ | jq -c ".result.panes[] | {pane_id,tab_id,label,agent,cwd}"
{"pane_id":"wJ:p1","tab_id":"wJ:t1","label":"dotfiles:claude-remediation-dot","agent":"claude","cwd":"/home/moriya/Workspace/dotfiles"}
{"pane_id":"wJ:p2","tab_id":"wJ:t1","label":"dotfiles:claude-standard-dot-a005","agent":"claude","cwd":"/home/moriya/Workspace/dotfiles"}
{"pane_id":"wJ:p5","tab_id":"wJ:t4","label":"audit","agent":null,"cwd":"/home/moriya/Workspace/dotfiles"}
$ herdr agent list | jq -c ".result.agents[] | {name,pane_id,agent}"
{"name":"a449a05f399333edd28a0dac1","pane_id":"wJ:p1","agent":"claude"}
{"name":"a46054f860901eb4904f5a133","pane_id":"wJ:p2","agent":"claude"}
```

### Branch diff against origin/main and commits
```
$ git diff origin/main --stat; git log --oneline origin/main..HEAD
 README.md                                          |  21 +++
 .../dot_agents/skills/agmsg-orchestration/SKILL.md |   1 +
 home/dot_local/bin/common/executable_herdr-agents  | 121 ++++++++++++++--
 tests/unit/test_herdr_agents.py                    | 160 +++++++++++++++++++++
 4 files changed, 288 insertions(+), 15 deletions(-)
903c9fa fix(herdr-agents): map only the pair's own worker seat; attach finds the worker by label
549b257 fix(herdr-agents): recognize the pair under upstream agmsg self-naming
```

### Mutation baseline: the 6 tests against unmodified origin/main
```
herdr-agents == origin/main b790ee0 (pre-change)
$ python3 -m unittest tests.unit.test_herdr_agents -k self_named -k seat_label
FFFFFF
======================================================================
FAIL: test_attach_from_the_self_named_worker_pane_exits_quietly (tests.unit.test_herdr_agents.HerdrAgentsTest.test_attach_from_the_self_named_worker_pane_exits_quietly)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_herdr_agents.py", line 2951, in test_attach_from_the_self_named_worker_pane_exits_quietly
    self.assertFalse(any(c.startswith(("pane rename", "pane split", "agent start")) for c in self.calls()), self.calls())
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: True is not false : ['identities /tmp/herdr-agents-test-eor_u4bx/project claude-code', 'pane list --workspace w-old', 'agent get claude-worker-w-old', 'agent get claude-worker-w-old', 'pane rename w-old:p2 claude-orchestrator']

======================================================================
FAIL: test_attach_leaves_a_self_named_pair_alone (tests.unit.test_herdr_agents.HerdrAgentsTest.test_attach_leaves_a_self_named_pair_alone)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_herdr_agents.py", line 2943, in test_attach_leaves_a_self_named_pair_alone
    self.assertFalse(any(c.startswith(("pane rename", "pane swap", "pane split", "agent start")) for c in calls), calls)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: True is not false : ['identities /tmp/herdr-agents-test-e128lk2v/project claude-code', 'pane list --workspace w-old', 'agent get claude-worker-w-old', 'agent get claude-worker-w-old', 'pane rename w-old:p1 claude-orchestrator']

======================================================================
FAIL: test_audit_finds_the_self_named_pair_workspace (tests.unit.test_herdr_agents.HerdrAgentsTest.test_audit_finds_the_self_named_pair_workspace)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_herdr_agents.py", line 2932, in test_audit_finds_the_self_named_pair_workspace
    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 2 != 0 : herdr-agents: no managed Herdr workspace for /tmp/herdr-agents-test-0vnvdbjj/project; run herdr-agents /tmp/herdr-agents-test-0vnvdbjj/project (full mode) to create one, or run codex --profile audit review headless.


======================================================================
FAIL: test_full_mode_heals_nothing_in_a_healthy_self_named_pair (tests.unit.test_herdr_agents.HerdrAgentsTest.test_full_mode_heals_nothing_in_a_healthy_self_named_pair)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_herdr_agents.py", line 2975, in test_full_mode_heals_nothing_in_a_healthy_self_named_pair
    self.assertFalse(any(c.startswith(("workspace create", "pane split", "agent start", "pane rename", "agent prompt")) for c in calls), calls)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: True is not false : ['identities /tmp/herdr-agents-test-zsjenw64/project claude-code', 'workspace list', 'pane list --workspace w-old', 'workspace create --cwd /tmp/herdr-agents-test-zsjenw64/project --label project agents --env CLICOLOR_FORCE=1 --env FORCE_COLOR=1 --env HERDR_AGENTS_LAYOUT=managed --focus', 'pane rename w-test:p1 claude-orchestrator', 'pane process-info --pane w-test:p1', 'pane read w-test:p1 --source recent-unwrapped --lines 50', 'agent start claude-orchestrator-w-test --kind claude --pane w-test:p1 --timeout 30000 --', 'pane split w-test:p1 --direction right --cwd /tmp/herdr-agents-test-zsjenw64/project --env CLICOLOR_FORCE=1 --env FORCE_COLOR=1 --env AGMSG_CC_MONITOR_KEEP_ALIVE=1 --env AGMSG_RESOLVE_PROJECT=0 --no-focus', 'pane process-info --pane w-test:p3', 'pane read w-test:p3 --source recent-unwrapped --lines 50', 'agent start claude-worker-w-test --kind claude --pane w-test:p3 --timeout 30000 -- --model opus --effort high', 'pane wait-output w-test:p3 --match trust this folder --timeout 3000', 'pane rename w-test:p3 claude-worker', 'delivery set both claude-code /tmp/herdr-agents-test-zsjenw64/project', 'doctor --project /tmp/herdr-agents-test-zsjenw64/project --type claude-code', 'identities /tmp/herdr-agents-test-zsjenw64/project claude-code']

======================================================================
FAIL: test_restart_worker_finds_the_worker_by_its_seat_label (tests.unit.test_herdr_agents.HerdrAgentsTest.test_restart_worker_finds_the_worker_by_its_seat_label)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_herdr_agents.py", line 2958, in test_restart_worker_finds_the_worker_by_its_seat_label
    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 2 != 0 : herdr-agents: no managed Herdr workspace for /tmp/herdr-agents-test-sd25jc7c/project; run herdr-agents /tmp/herdr-agents-test-sd25jc7c/project (full mode) to create one.


======================================================================
FAIL: test_two_self_named_pair_workspaces_still_refuse (tests.unit.test_herdr_agents.HerdrAgentsTest.test_two_self_named_pair_workspaces_still_refuse)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_herdr_agents.py", line 2984, in test_two_self_named_pair_workspaces_still_refuse
    self.assertIn("multiple managed Herdr workspaces", result.stderr)
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'multiple managed Herdr workspaces' not found in 'herdr-agents: no managed Herdr workspace for /tmp/herdr-agents-test-adijcpyc/project; run herdr-agents /tmp/herdr-agents-test-adijcpyc/project (full mode) to create one, or run codex --profile audit review headless.\n'

----------------------------------------------------------------------
Ran 6 tests in 0.598s

FAILED (failures=6)
```

### Mutation baseline, review fixes: new tests against the reviewed head 549b257
```
herdr-agents content == HEAD 549b257 (reviewed head; checked with: git show HEAD:<file> | cmp - <file> before the run; only the file mode differed, 100755 at HEAD vs the restored 100644)
$ python3 -m unittest tests.unit.test_herdr_agents -k another_team_members -k attach_completes_bootstrap -k mixed_legacy -k worker_worktree_registration -k self_named -k seat_label
FF.......F
======================================================================
FAIL: test_another_team_members_pane_is_not_a_second_worker (tests.unit.test_herdr_agents.HerdrAgentsTest.test_another_team_members_pane_is_not_a_second_worker)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_herdr_agents.py", line 2988, in test_another_team_members_pane_is_not_a_second_worker
    self.assertIn("refusing restart", result.stderr)
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'refusing restart' not found in 'herdr-agents: no claude worker pane in Herdr workspace w-old; run herdr-agents /tmp/herdr-agents-test-er5pwe4d/project (full mode) to heal it.\n'

======================================================================
FAIL: test_attach_completes_bootstrap_on_a_self_named_pair (tests.unit.test_herdr_agents.HerdrAgentsTest.test_attach_completes_bootstrap_on_a_self_named_pair)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_herdr_agents.py", line 2996, in test_attach_completes_bootstrap_on_a_self_named_pair
    self.assertNotIn("refusing repair", result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'refusing repair' unexpectedly found in 'Herdr attach panes are ambiguous or include unmanaged panes; refusing repair.\n'

======================================================================
FAIL: test_worker_seat_label_comes_from_the_worker_worktree_registration (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_seat_label_comes_from_the_worker_worktree_registration)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_herdr_agents.py", line 3033, in test_worker_seat_label_comes_from_the_worker_worktree_registration
    self.assertIn(f"identities {worktree} claude-code", self.calls())
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'identities /tmp/herdr-agents-test-su4hdka1/project/.claude/worktrees/worker-c claude-code' not found in ['identities /tmp/herdr-agents-test-su4hdka1/project claude-code', 'team dotfiles --json', 'identities /tmp/herdr-agents-test-su4hdka1/project claude-code', 'pane list --workspace w-old', 'agent get claude-worker-w-old']

----------------------------------------------------------------------
Ran 10 tests in 1.631s

FAILED (failures=3)
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
Ran 543 tests in 91.236s

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
$ git ls-files -s home/dot_local/bin/common/executable_herdr-agents
```

### CI on 549b257
```
$ gh pr checks 207
CodeRabbit	pass	0		Review skipped: manual review required for this OSS repository
changes	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/36521155085/job/109254093010	
private-bootstrap (macos-14, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/36521155045/job/109254093104	
private-bootstrap (ubuntu-latest, client)	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/36521155045/job/109254092992	
private-bootstrap (ubuntu-latest, server)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/36521155045/job/109254093105	
public-bootstrap (macos-14, client)	pass	8m22s	https://github.com/mryfmo/dotfiles/actions/runs/36521155045/job/109254093093	
public-bootstrap (ubuntu-latest, client)	pass	9m30s	https://github.com/mryfmo/dotfiles/actions/runs/36521155045/job/109254093064	
public-bootstrap (ubuntu-latest, server)	pass	8m40s	https://github.com/mryfmo/dotfiles/actions/runs/36521155045/job/109254092843	
test (macos-14, client)	pass	3m28s	https://github.com/mryfmo/dotfiles/actions/runs/36521155085/job/109254139319	
validate	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/36521155067/job/109254093041	
nix	skipping	0	https://github.com/mryfmo/dotfiles/actions/runs/36521155085/job/109254140442	
test (ubuntu-latest, client)	pass	5m31s	https://github.com/mryfmo/dotfiles/actions/runs/36521155085/job/109254139287	
test (ubuntu-latest, server)	pass	3m1s	https://github.com/mryfmo/dotfiles/actions/runs/36521155085/job/109254139359	
exit=0
$ gh pr view 207 --json headRefOid -q .headRefOid
549b2576f54ad8f1bb9fd297fa221e83da381ae6
```

### CompactionDB
```
$ python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "T35: herdr-agents recognizes the managed pair by agmsg seat evidence (registered identities behind <team>:<name> pane labels, managed layout env, legacy labels as fallback) instead of fixed labels, so upstream agmsg 1.5.0 self-naming no longer hides the workspace from --audit, --attach, --restart-worker and heal (operator 2026-09-29). Diagnosis: no upstream script renames workspaces and herdr exposes no workspace env; self-naming renames panes to <team>:<name> and herdr agents to hash keys."
ad0dbc1a-d2f7-4b0e-9649-df4dc8b8a8a3
```

### Independent review (subagent, separate context) on 549b257, condensed findings and verdict

```
P2 high  executable_herdr-agents:421-424,439  every team member mapped to <kind>-worker (spec: only the worker-worktree seat or legacy label); a second member pane -> labeled_worker_pane_id empty -> heal splits a duplicate worker, restart refuses.
P2 high  :1187 (refusal :1192-1195)  orchestrator --attach finds the worker only via live_worker_pane_id (agent renamed upstream) -> "ambiguous ... refusing repair" every SessionStart, bootstrap_agmsg skipped.
P3 high  README.md:515-516  worker's own attach self-check claim false for a worktree-seated worker (seats read at the worktree).
P3 med   :421-424  member .type ignored (claude-code member relabeled codex-worker under worker_kind=codex).
P3 med   :1165  team.sh --json (~1.8 s live) on every attach.
P3 high  file mode 100644 -> 100755 unmentioned.
P3 high  tests  no third-member pane, no completed attach, no mixed labels, no HOME-guard test.
Refuted: jq index semantics, regex, ${1%%:*}, pipefail paths, audit ordering, workspace detection vs foreign panes.
Verdict: incorrect
```

Disposition: every finding is resolved in 903c9fa, with one resolved crit record each in `.orchestration/validation/dot-herdr-agents-seat-labels-T35-a01-crit.json` (receipt `…-review-receipt.md`).

### CI on the final head 903c9fa
```
$ gh pr checks 207
CodeRabbit	pass	0		Review skipped: manual review required for this OSS repository
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/36522717302/job/109258911035	
private-bootstrap (macos-14, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/36522717326/job/109258910303	
nix	skipping	0	https://github.com/mryfmo/dotfiles/actions/runs/36522717302/job/109259077268	
private-bootstrap (ubuntu-latest, client)	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/36522717326/job/109258909982	
private-bootstrap (ubuntu-latest, server)	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/36522717326/job/109258910024	
public-bootstrap (macos-14, client)	pass	8m49s	https://github.com/mryfmo/dotfiles/actions/runs/36522717326/job/109258910074	
public-bootstrap (ubuntu-latest, client)	pass	8m50s	https://github.com/mryfmo/dotfiles/actions/runs/36522717326/job/109258910066	
public-bootstrap (ubuntu-latest, server)	pass	6m53s	https://github.com/mryfmo/dotfiles/actions/runs/36522717326/job/109258910071	
test (macos-14, client)	pass	3m34s	https://github.com/mryfmo/dotfiles/actions/runs/36522717302/job/109259076195	
test (ubuntu-latest, client)	pass	6m2s	https://github.com/mryfmo/dotfiles/actions/runs/36522717302/job/109259076248	
test (ubuntu-latest, server)	pass	2m45s	https://github.com/mryfmo/dotfiles/actions/runs/36522717302/job/109259076179	
validate	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/36522717399/job/109258909828	
exit=0
$ gh pr view 207 --json headRefOid -q .headRefOid
903c9fad9901198acf585465c9b684a820c00994
```

---

## Revision 2 (fix 72a0a14)

### Mutation baseline: the new tests against 903c9fa
```
herdr-agents content == HEAD 903c9fa (903c9fa, checked with cmp)
$ python3 -m unittest tests.unit.test_herdr_agents -k solo_codex -k survive_seat_label
FFF
======================================================================
FAIL: test_explicit_worker_kind_and_profile_survive_seat_label_loading (tests.unit.test_herdr_agents.HerdrAgentsTest.test_explicit_worker_kind_and_profile_survive_seat_label_loading)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_herdr_agents.py", line 3080, in test_explicit_worker_kind_and_profile_survive_seat_label_loading
    self.assertTrue(
    ~~~~~~~~~~~~~~~^
        any(c.startswith("agent start codex-worker-") and c.endswith("--sandbox workspace-write --profile express") for c in calls),
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        calls,
        ^^^^^^
    )
    ^
AssertionError: False is not true : ['identities /tmp/herdr-agents-test-chn0_gdg/project claude-code', 'identities /tmp/herdr-agents-test-chn0_gdg/project codex', 'workspace list', 'workspace create --cwd /tmp/herdr-agents-test-chn0_gdg/project --label project agents --env CLICOLOR_FORCE=1 --env FORCE_COLOR=1 --env HERDR_AGENTS_LAYOUT=managed --focus', 'pane list --workspace w-test', 'pane rename w-test:p1 claude-orchestrator', 'pane process-info --pane w-test:p1', 'pane read w-test:p1 --source recent-unwrapped --lines 50', 'agent start claude-orchestrator-w-test --kind claude --pane w-test:p1 --timeout 30000 --', 'pane split w-test:p1 --direction right --cwd /tmp/herdr-agents-test-chn0_gdg/project --env CLICOLOR_FORCE=1 --env FORCE_COLOR=1 --env AGMSG_RESOLVE_PROJECT=0 --no-focus', 'pane process-info --pane w-test:p3', 'pane read w-test:p3 --source recent-unwrapped --lines 50', 'agent start codex-worker-w-test --kind codex --pane w-test:p3 --timeout 30000 -- --sandbox workspace-write --profile standard', 'pane list --workspace w-test', 'pane rename w-test:p3 codex-worker', 'delivery set both claude-code /tmp/herdr-agents-test-chn0_gdg/project', 'doctor --project /tmp/herdr-agents-test-chn0_gdg/project --type claude-code', 'identities /tmp/herdr-agents-test-chn0_gdg/project claude-code']

======================================================================
FAIL: test_full_mode_does_not_duplicate_a_solo_codex_worker_seat (tests.unit.test_herdr_agents.HerdrAgentsTest.test_full_mode_does_not_duplicate_a_solo_codex_worker_seat)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_herdr_agents.py", line 3068, in test_full_mode_does_not_duplicate_a_solo_codex_worker_seat
    self.assertFalse(any(c.startswith(("pane split", "agent start")) for c in self.calls()), self.calls())
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: True is not false : ['identities /tmp/herdr-agents-test-eottkxb5/project claude-code', 'identities /tmp/herdr-agents-test-eottkxb5/project codex', 'workspace list', 'pane list --workspace w-old', 'pane list --workspace w-old', 'agent get codex-worker-w-old', 'pane split w-old:p1 --direction right --cwd /tmp/herdr-agents-test-eottkxb5/project --env CLICOLOR_FORCE=1 --env FORCE_COLOR=1 --env AGMSG_RESOLVE_PROJECT=0 --no-focus', 'pane process-info --pane w-old:p3', 'pane read w-old:p3 --source recent-unwrapped --lines 50', 'agent start codex-worker-w-old --kind codex --pane w-old:p3 --timeout 30000 -- --sandbox workspace-write --profile standard', 'pane list --workspace w-old', 'pane rename w-old:p3 codex-worker', 'pane list --workspace w-old', 'pane list --workspace w-old', 'delivery set turn codex /tmp/herdr-agents-test-eottkxb5/project', 'delivery set both claude-code /tmp/herdr-agents-test-eottkxb5/project', 'doctor --project /tmp/herdr-agents-test-eottkxb5/project --type codex', 'identities /tmp/herdr-agents-test-eottkxb5/project codex', 'doctor --project /tmp/herdr-agents-test-eottkxb5/project --type claude-code', 'identities /tmp/herdr-agents-test-eottkxb5/project claude-code', 'workspace focus w-old']

======================================================================
FAIL: test_restart_worker_finds_a_solo_codex_worker_seat (tests.unit.test_herdr_agents.HerdrAgentsTest.test_restart_worker_finds_a_solo_codex_worker_seat)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_herdr_agents.py", line 3057, in test_restart_worker_finds_a_solo_codex_worker_seat
    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 2 != 0 : herdr-agents: no codex worker pane in Herdr workspace w-old; run herdr-agents /tmp/herdr-agents-test-fxac9dlq/project (full mode) to heal it.


----------------------------------------------------------------------
Ran 3 tests in 0.855s

FAILED (failures=3)
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
Ran 546 tests in 92.382s

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

### CI on 72a0a14
```
$ gh pr checks 207
CodeRabbit	pass	0		Review skipped: manual review required for this OSS repository
changes	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/36524704283/job/109265064206	
private-bootstrap (macos-14, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/36524704268/job/109265064175	
private-bootstrap (ubuntu-latest, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/36524704268/job/109265064383	
private-bootstrap (ubuntu-latest, server)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/36524704268/job/109265064369	
public-bootstrap (macos-14, client)	pass	8m45s	https://github.com/mryfmo/dotfiles/actions/runs/36524704268/job/109265064406	
public-bootstrap (ubuntu-latest, client)	pass	8m32s	https://github.com/mryfmo/dotfiles/actions/runs/36524704268/job/109265064487	
validate	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/36524704296/job/109265064424	
nix	skipping	0	https://github.com/mryfmo/dotfiles/actions/runs/36524704283/job/109265093307	
public-bootstrap (ubuntu-latest, server)	pass	5m15s	https://github.com/mryfmo/dotfiles/actions/runs/36524704268/job/109265064357	
test (macos-14, client)	pass	3m1s	https://github.com/mryfmo/dotfiles/actions/runs/36524704283/job/109265091767	
test (ubuntu-latest, client)	pass	6m37s	https://github.com/mryfmo/dotfiles/actions/runs/36524704283/job/109265091747	
test (ubuntu-latest, server)	pass	3m24s	https://github.com/mryfmo/dotfiles/actions/runs/36524704283/job/109265091789	
exit=0
$ gh pr view 207 --json headRefOid -q .headRefOid
72a0a14d7459c53ccaff72b27d0c1d6e88ceb7d4
```
