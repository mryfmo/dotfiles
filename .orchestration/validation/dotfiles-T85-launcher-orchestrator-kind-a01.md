# Validation: dotfiles-T85-launcher-orchestrator-kind-a01

- **task_rev:** `sha256:5c036338be03f430f70b3e047212b952966134e439677bad7ec4048b086cd37f`; `sha256sum` of the main-checkout task file matches.
- **PR:** #270. **Final head:** `20361c5d19ca70548b27f1e0269cf5d8a7e1abf1`.

## Task validation commands (verbatim)

shfmt ran through the pinned scratch mise directory with an absolute path. The last command is an extra read-only `--directive` run in the main checkout.

```
$ git diff origin/main --stat   (working tree; committed below)
 README.md                                         |   8 ++
 home/dot_local/bin/common/executable_herdr-agents | 102 ++++++++++++--
 tests/unit/test_herdr_agents.py                   | 162 ++++++++++++++++++++++
 3 files changed, 258 insertions(+), 14 deletions(-)
$ mise x shfmt -- shfmt -i 4 -sr -d home/dot_local/bin/common/executable_herdr-agents; shellcheck home/dot_local/bin/common/executable_herdr-agents   (shfmt via the pinned scratch mise dir, absolute path)
[shfmt exit 0]
[shellcheck exit 0]
$ uv run python -m unittest tests.unit.test_herdr_agents 2>&1 | tail -3
Ran 229 tests in 148.713s

OK (skipped=1)
$ make unit-test 2>&1 | tail -3
Ran 800 tests in 200.701s

OK (skipped=1)
$ make validate-agent-assets   (WARN lines omitted)
uv run --with pyyaml scripts/validate-agent-assets.py
agent asset validation ok
[exit 0]
$ HERDR_AGENTS_ORCHESTRATOR_KIND=codex bash home/dot_local/bin/common/executable_herdr-agents --attach "$PWD"; echo "rc=$?"   (worker-c is the manifest worker_worktree, so the guard lets it through; this shell is in a Herdr pane and attach takes no DIR argument, so usage and exit 2)
Usage: herdr-agents [DIR]
       herdr-agents --attach
       herdr-agents --restart-worker [DIR]
rc=2
$ (cd /home/moriya/Workspace/dotfiles && HERDR_AGENTS_ORCHESTRATOR_KIND=codex bash <this branch script> --attach "$PWD"; echo "rc=$?")   (the main checkout: refused)
herdr-agents: orchestrator_kind=codex: use codex-orchestrate
rc=2
$ bash home/dot_local/bin/common/executable_herdr-agents --directive; echo "rc=$?"   (in worker-c, a linked worktree, so no regime line)
rc=0
$ (cd /home/moriya/Workspace/dotfiles/docs && PATH=/usr/bin:/bin bash <this branch script> --directive; echo "rc=$?")   (read-only, from a subdirectory of the main checkout; no herdr on PATH)
agmsg-orchestration: this session is the orchestrator seat claude-remediation-dot for /home/moriya/Workspace/dotfiles (worker seat .claude/worktrees/worker-c). Before any other action, invoke the agmsg-orchestration skill. Delegate every repository-mutating change, make upgrade pin diffs included, to the seated worker as an AGMSG-TASK; when no worker is seated, seat one first (herdr-agents --restart-worker in the pair, herdr-agents --add-worker .claude/worktrees/worker-c otherwise): no worker is never an implicit opt-out. Before acting directly under an exemption, declare which one in one line. Never push to main yourself: main accepts only pull requests (GitHub ruleset), so every change, the .orchestration boundary commit included, travels as a PR merged with gh pr merge --squash.
rc=0
```

## The new tests against the `origin/main` launcher (verbatim)

```
$ (executable_herdr-agents from origin/main 2527be54) uv run python -m unittest -k orchestrator_kind -k directive_prints tests.unit.test_herdr_agents
FAIL: test_codex_orchestrator_kind_refuses_the_claude_pair_before_herdr (tests.unit.test_herdr_agents.HerdrAgentsTest.test_codex_orchestrator_kind_refuses_the_claude_pair_before_herdr) (mode='full mode')
FAIL: test_codex_orchestrator_kind_refuses_the_claude_pair_before_herdr (tests.unit.test_herdr_agents.HerdrAgentsTest.test_codex_orchestrator_kind_refuses_the_claude_pair_before_herdr) (mode='restart-worker')
FAIL: test_codex_orchestrator_kind_refuses_the_claude_pair_before_herdr (tests.unit.test_herdr_agents.HerdrAgentsTest.test_codex_orchestrator_kind_refuses_the_claude_pair_before_herdr) (mode='attach in a pane')
FAIL: test_codex_orchestrator_kind_refuses_the_claude_pair_before_herdr (tests.unit.test_herdr_agents.HerdrAgentsTest.test_codex_orchestrator_kind_refuses_the_claude_pair_before_herdr) (mode='attach in a plain shell')
FAIL: test_directive_prints_the_regime_line_without_herdr (tests.unit.test_herdr_agents.HerdrAgentsTest.test_directive_prints_the_regime_line_without_herdr)
FAIL: test_orchestrator_kind_comes_from_the_manifest_env_and_is_validated (tests.unit.test_herdr_agents.HerdrAgentsTest.test_orchestrator_kind_comes_from_the_manifest_env_and_is_validated)
Ran 5 tests in 0.803s
FAILED (failures=6)
```

## The review tests against the `5643ba22` launcher (verbatim)

```
$ (executable_herdr-agents from 5643ba22) uv run python -m unittest -k codex_orchestrator_identity -k worker_worktree_attach_quiet tests.unit.test_herdr_agents
FAIL: test_codex_orchestrator_kind_leaves_a_worker_worktree_attach_quiet (tests.unit.test_herdr_agents.HerdrAgentsTest.test_codex_orchestrator_kind_leaves_a_worker_worktree_attach_quiet)
AssertionError: 2 != 0 : herdr-agents: orchestrator_kind=codex: use codex-orchestrate
FAIL: test_directive_looks_up_a_codex_orchestrator_identity (tests.unit.test_herdr_agents.HerdrAgentsTest.test_directive_looks_up_a_codex_orchestrator_identity)
AssertionError: 0 != 1 : 
Ran 2 tests in 0.059s
FAILED (failures=2)
```

## The worker-seat test against the `f50e6af7` launcher (verbatim)

```
$ (executable_herdr-agents from f50e6af7) uv run python -m unittest -k refuses_attach_in_another_linked_worktree tests.unit.test_herdr_agents
FAIL: test_codex_orchestrator_kind_refuses_attach_in_another_linked_worktree (tests.unit.test_herdr_agents.HerdrAgentsTest.test_codex_orchestrator_kind_refuses_attach_in_another_linked_worktree)
AssertionError: "herdr-agents: worker_kind=claude would s[650 chars]E.\n" != 'herdr-agents: orchestrator_kind=codex: u[18 chars]te\n'
Ran 1 test in 0.062s
FAILED (failures=1)
```

## The leader-type and subdirectory tests against the `4d210709` launcher (verbatim)

```
$ (executable_herdr-agents from 4d210709) uv run python -m unittest -k add_worker_names_the_seat_from_a_codex -k directive_prints_the_regime_line tests.unit.test_herdr_agents
FAIL: test_add_worker_names_the_seat_from_a_codex_orchestrator_identity (tests.unit.test_herdr_agents.HerdrAgentsTest.test_add_worker_names_the_seat_from_a_codex_orchestrator_identity)
AssertionError: 2 != 0 : herdr-agents: need exactly one orchestrator claude-code identity at /tmp/claude-1000/herdr-agents-test-6laywsyy/project to name the worker; register the worker yourself with: AGMSG_RESOLVE_PROJECT=0 /tmp/claude-1000/herdr-agents-test-6laywsyy/home/.agents/skills/agmsg/scripts/join.sh <team> <name> claude-code /tmp/claude-1000/herdr-agents-test-6laywsyy/project/.claude/worktrees/b1
FAIL: test_directive_prints_the_regime_line_without_herdr (tests.unit.test_herdr_agents.HerdrAgentsTest.test_directive_prints_the_regime_line_without_herdr)
AssertionError: '' != 'agmsg-orchestration: this session is the [769 chars]h.\n'
Ran 2 tests in 0.168s
FAILED (failures=2)
```

## Timestamped Bot wait for the final head (verbatim)

```
2026-10-04T23:18:39Z checks-done rc=0
2026-10-04T23:18:39Z bot-wait start head=20361c5d19ca70548b27f1e0269cf5d8a7e1abf1
2026-10-04T23:18:40Z poll reviews=[20361c5d19ca70548b27f1e0269cf5d8a7e1abf1	2026-10-04T23:13:45Z] comments=[4179731976	20361c5d19ca70548b27f1e0269cf5d8a7e1abf1	home/dot_local/bin/common/executable_herdr-agents]
2026-10-04T23:18:40Z end: review found
```

## CI, branch and Codex bot on the final head (verbatim)

```
$ gh pr checks 270
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37242696760/job/111554399372	
private-bootstrap (macos-14, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37242696743/job/111554399392	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37242696743/job/111554399226	
private-bootstrap (ubuntu-24.04, server)	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/37242696743/job/111554399039	
public-bootstrap (macos-14, client)	pass	8m7s	https://github.com/mryfmo/dotfiles/actions/runs/37242696743/job/111554399264	
public-bootstrap (ubuntu-24.04, client)	pass	9m18s	https://github.com/mryfmo/dotfiles/actions/runs/37242696743/job/111554399170	
public-bootstrap (ubuntu-24.04, server)	pass	6m15s	https://github.com/mryfmo/dotfiles/actions/runs/37242696743/job/111554399254	
test (macos-14, client)	pass	6m24s	https://github.com/mryfmo/dotfiles/actions/runs/37242696760/job/111554431663	
test (ubuntu-24.04, client)	pass	7m19s	https://github.com/mryfmo/dotfiles/actions/runs/37242696760/job/111554431697	
test (ubuntu-24.04, server)	pass	4m49s	https://github.com/mryfmo/dotfiles/actions/runs/37242696760/job/111554431751	
test (ubuntu-26.04, client)	pass	7m55s	https://github.com/mryfmo/dotfiles/actions/runs/37242696760/job/111554431721	
validate	pass	22s	https://github.com/mryfmo/dotfiles/actions/runs/37242696749/job/111554399499	
[exit 0]
$ gh api repos/mryfmo/dotfiles/pulls/270 --jq '.mergeable_state'
blocked
$ gh api repos/mryfmo/dotfiles/pulls/270 --jq '.head.sha'
20361c5d19ca70548b27f1e0269cf5d8a7e1abf1
$ gh api repos/mryfmo/dotfiles/compare/main...feat/launcher-orchestrator-kind --jq '[.behind_by,.ahead_by]|@tsv'
0	4
$ gh api --paginate repos/mryfmo/dotfiles/pulls/270/reviews --jq '.[]|select(.user.type=="Bot")|[.commit_id,.submitted_at]|@tsv'
5643ba22ef152ca2c475a81af0b07dce2f6a6661	2026-10-04T22:20:21Z
f50e6af793c3389e57e273504aef50f6a215bb26	2026-10-04T22:36:34Z
4d210709b83559e00564aa1dc142cdc385151af8	2026-10-04T22:58:24Z
20361c5d19ca70548b27f1e0269cf5d8a7e1abf1	2026-10-04T23:13:45Z
$ gh api --paginate repos/mryfmo/dotfiles/pulls/270/comments --jq '.[]|select(.in_reply_to_id == null and .user.type=="Bot")|[.id,.original_commit_id,.path]|@tsv'
4179583126	5643ba22ef152ca2c475a81af0b07dce2f6a6661	home/dot_local/bin/common/executable_herdr-agents
4179583130	5643ba22ef152ca2c475a81af0b07dce2f6a6661	home/dot_local/bin/common/executable_herdr-agents
4179583135	5643ba22ef152ca2c475a81af0b07dce2f6a6661	home/dot_local/bin/common/executable_herdr-agents
4179629453	f50e6af793c3389e57e273504aef50f6a215bb26	home/dot_local/bin/common/executable_herdr-agents
4179692400	4d210709b83559e00564aa1dc142cdc385151af8	home/dot_local/bin/common/executable_herdr-agents
4179692403	4d210709b83559e00564aa1dc142cdc385151af8	home/dot_local/bin/common/executable_herdr-agents
4179692405	4d210709b83559e00564aa1dc142cdc385151af8	home/dot_local/bin/common/executable_herdr-agents
4179731976	20361c5d19ca70548b27f1e0269cf5d8a7e1abf1	home/dot_local/bin/common/executable_herdr-agents
```
