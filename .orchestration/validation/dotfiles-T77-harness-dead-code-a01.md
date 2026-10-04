# dotfiles-T77-harness-dead-code-a01 — validation

PR #260 (https://github.com/mryfmo/dotfiles/pull/260), branch `chore/harness-dead-code`, final head `977bdf1f757fec64ebc732dead4f55a69ad745a3`, base `origin/main` f6320f37.

## Task file verification

```text
$ sha256sum /home/moriya/Workspace/dotfiles/.orchestration/tasks/dotfiles-T77-harness-dead-code-a01.md
038f0fdaf2fbdbdcbc0b11a87b36c905e266b9f583e64519d587f7fce9e7e4d7  /home/moriya/Workspace/dotfiles/.orchestration/tasks/dotfiles-T77-harness-dead-code-a01.md
dispatched task_rev e4595b65… (initial) and 038f0fda… (PONG decision); the sha256 above matches the latest
```

## Validation commands on the final head (verbatim)

The task grep is run with `/usr/bin/grep` (this shell's `grep` is a ugrep wrapper) and `--exclude-dir=__pycache__`, so stale bytecode does not add "binary file matches" lines. The `git ls-files` hits are historical `.orchestration` records whose names contain `herdr-session`, not code. The remaining content hits are:

- `enforce-uv.sh` `"decision": "approve"`: item 5, excluded and routed to T77b.
- `test_chezmoiremove_agmsg.py:72-73`: the retired-target pins this PR adds.

The unit-test count fell from 791 to 773, the 18 removed tests: 7 in `test_runtime_health.py` (1 private-runs, 4 `agent-fanout`, 2 CCR) and 11 in `test_herdr_agents.py`.

```text
$ git rev-parse HEAD; echo "rc=$?"
977bdf1f757fec64ebc732dead4f55a69ad745a3
rc=0
$ git log --format="%H %s" origin/main..HEAD
977bdf1f757fec64ebc732dead4f55a69ad745a3 chore(chezmoi): retire the deployed herdr-session and agent-fanout executables
6f8b568313beeb7b98170c3c6dd0559dd54ff738 chore(harness): delete herdr-session, agent-fanout, the CCR gate notice, the Codex profile alias and the CompactionDB archive
$ git diff origin/main --stat; echo "rc=$?"
 README.md                                          |  22 +-
 archive/CompactionDB-2.0.0.zip                     | Bin 96789 -> 0 bytes
 home/.chezmoiremove                                |   2 +
 home/dot_agents/agent-config.yaml                  |   2 +-
 home/dot_agents/model-profiles.env                 |   2 +-
 home/dot_local/bin/common/executable_agent-fanout  | 231 -------------
 home/dot_local/bin/common/executable_herdr-agents  |  16 +-
 home/dot_local/bin/common/executable_herdr-session |  31 --
 home/dot_zshrc                                     |  14 -
 scripts/generate-agent-configs.py                  |   2 +-
 scripts/require-crit-review.py                     |   1 -
 scripts/upgrade-tools.sh                           |  28 --
 scripts/validate-agent-assets.py                   |  14 +-
 tests/unit/test_chezmoiremove_agmsg.py             |   2 +
 tests/unit/test_herdr_agents.py                    | 374 ---------------------
 tests/unit/test_require_crit_review.py             |   1 -
 tests/unit/test_runtime_health.py                  | 242 +------------
 17 files changed, 26 insertions(+), 958 deletions(-)
rc=0
$ git ls-files | /usr/bin/grep -E 'herdr-session|agent-fanout|archive/' ; echo "rc=$?"
.orchestration/autoskill/runs/T33-herdr-session-design-restore.md
.orchestration/learning/T33-herdr-session-design-restore.md
.orchestration/reports/T33-herdr-session-design-restore.md
.orchestration/sandboxes/T33-herdr-session-design-restore.md
.orchestration/tasks/T33-herdr-session-design-restore.md
.orchestration/tasks/T5-herdr-session-bootstrap.md
.orchestration/validation/T33-herdr-session-design-restore.md
rc=0
$ /usr/bin/grep -rn --exclude-dir=__pycache__ "agent-fanout\|herdr-session\|HERDR_AGENTS_CODEX_PROFILE\|CCR gate\|\"decision\": *\"approve\"" home scripts tests README.md ; echo "rc=$?"
home/.chezmoiremove:9:.local/bin/common/herdr-session
home/.chezmoiremove:10:.local/bin/common/agent-fanout
home/dot_claude/hooks/executable_enforce-uv.sh:218:        echo '{"decision": "approve"}'
home/dot_claude/hooks/executable_enforce-uv.sh:278:    echo '{"decision": "approve"}'
tests/unit/test_chezmoiremove_agmsg.py:72:        ".local/bin/common/herdr-session",
tests/unit/test_chezmoiremove_agmsg.py:73:        ".local/bin/common/agent-fanout",
rc=0
$ make render-check; echo "rc=$?"
uv run --with pyyaml scripts/generate-agent-configs.py --check
generated agent configs are up to date
rc=0
$ bash -n scripts/upgrade-tools.sh && bash -n home/dot_local/bin/common/executable_herdr-agents && zsh -n home/dot_zshrc; echo "rc=$?"
rc=0
$ shellcheck scripts/upgrade-tools.sh home/dot_local/bin/common/executable_herdr-agents; echo "rc=$?"
rc=0
$ shfmt --indent 4 --space-redirects --diff scripts/upgrade-tools.sh home/dot_local/bin/common/executable_herdr-agents; echo "rc=$?"
rc=0
$ git ls-files -z "*.py" | xargs -0 mise x ruff -- ruff format --config ruff.toml --check; echo "rc=$?"
41 files already formatted
rc=0
$ mise x node npm:prettier -- prettier --check README.md; echo "rc=$?"
Checking formatting...
All matched files use Prettier code style!
rc=0
$ make validate-agent-assets 2>&1 | grep -v "^WARN: regime-boundary" | tail -3; echo "rc=$?"   (exit status captured without a pipe)
uv run --with pyyaml scripts/validate-agent-assets.py
agent asset validation ok
rc=0
$ make unit-test 2>&1 | tail -4; echo "rc=$?"   (exit status captured without a pipe)
----------------------------------------------------------------------
Ran 773 tests in 176.709s

OK (skipped=1)
rc=0
```

## `gh pr checks 260` and state (final head 977bdf1f)

```text
$ gh pr checks 260 --watch --interval 30; gh pr checks 260
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37215436669/job/111474870079	
private-bootstrap (macos-14, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37215436696/job/111474870359	
private-bootstrap (ubuntu-24.04, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37215436696/job/111474870196	
private-bootstrap (ubuntu-24.04, server)	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/37215436696/job/111474870340	
public-bootstrap (macos-14, client)	pass	8m19s	https://github.com/mryfmo/dotfiles/actions/runs/37215436696/job/111474870352	
public-bootstrap (ubuntu-24.04, client)	pass	8m59s	https://github.com/mryfmo/dotfiles/actions/runs/37215436696/job/111474870338	
public-bootstrap (ubuntu-24.04, server)	pass	7m22s	https://github.com/mryfmo/dotfiles/actions/runs/37215436696/job/111474870341	
test (macos-14, client)	pass	5m56s	https://github.com/mryfmo/dotfiles/actions/runs/37215436669/job/111474904023	
test (ubuntu-24.04, client)	pass	7m42s	https://github.com/mryfmo/dotfiles/actions/runs/37215436669/job/111474904011	
test (ubuntu-24.04, server)	pass	4m39s	https://github.com/mryfmo/dotfiles/actions/runs/37215436669/job/111474904021	
test (ubuntu-26.04, client)	pass	7m25s	https://github.com/mryfmo/dotfiles/actions/runs/37215436669/job/111474904037	
validate	pass	21s	https://github.com/mryfmo/dotfiles/actions/runs/37215436672/job/111474870153	
$ gh api repos/mryfmo/dotfiles/pulls/260 --jq '.head.sha, .mergeable_state'; git ls-remote origin refs/heads/main
977bdf1f757fec64ebc732dead4f55a69ad745a3
blocked
f6320f37d3835b37204584e00eb67d0bb41bf577	refs/heads/main
```

## Bot wait (final head 977bdf1f pushed 2026-10-04T16:04:50Z; window ended 16:19:55Z)

The Bot reviewed 6f8b5683 (first push) at 16:07:20Z with one P2 finding. It posted no review of 977bdf1f within the 15 minutes.

```text
window 2026-10-04T16:14:13Z .. 2026-10-04T16:19:55Z; final head 977bdf1f757fec64ebc732dead4f55a69ad745a3
$ gh api --paginate repos/mryfmo/dotfiles/pulls/260/reviews --jq '.[]|select(.user.type=="Bot")|[.commit_id,.submitted_at]|@tsv'
6f8b568313beeb7b98170c3c6dd0559dd54ff738	2026-10-04T16:07:20Z
$ gh api --paginate repos/mryfmo/dotfiles/pulls/260/comments --jq '.[]|select(.in_reply_to_id == null and .user.type=="Bot")|[.id,.commit_id,.path]|@tsv'
4178373800	6f8b568313beeb7b98170c3c6dd0559dd54ff738	home/dot_local/bin/common/executable_agent-fanout
review of final head: no (bot: none)
$ gh api --paginate repos/mryfmo/dotfiles/pulls/260/comments --jq '.[]|select(.in_reply_to_id == null and .user.type=="Bot" and (.original_commit_id=="977bdf1f757fec64ebc732dead4f55a69ad745a3" or .original_commit_id=="6f8b568313beeb7b98170c3c6dd0559dd54ff738"))|[.id,.original_commit_id[:8],.path,.line]|@tsv'
4178373800	6f8b5683	home/dot_local/bin/common/executable_agent-fanout	1
$ gh api repos/mryfmo/dotfiles/pulls/comments/4178373800 --jq .body
**<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  Remove retired executables from existing homes**

On machines that previously applied these dotfiles, removing the source file alone does not remove `~/.local/bin/common/agent-fanout` (nor `herdr-session`), and this change adds neither path to `home/.chezmoiremove`. Those old commands therefore remain runnable after `chezmoi apply`, leaving the supposedly retired harness behavior deployed; add both retired target paths to the removal manifest.

Useful? React with 👍 / 👎.
```

## CompactionDB (main checkout, unsandboxed; enforce-uv clause dropped per the Dispatch routing note)

```text
$ cd /home/moriya/Workspace/dotfiles && python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'dotfiles-T77 (operator 2026-10-03): the `herdr()` zsh wrapper and `herdr-session`, `agent-fanout`, the CCR adoption-gate notice, the `HERDR_AGENTS_CODEX_PROFILE` alias and `archive/CompactionDB-2.0.0.zip` are deleted.'
fd9cacff-99b2-4c8c-8e64-dd7bc8693229
```
