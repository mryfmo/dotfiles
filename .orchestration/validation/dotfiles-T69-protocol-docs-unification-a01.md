# dotfiles-T69-protocol-docs-unification-a01 — validation

PR: https://github.com/mryfmo/dotfiles/pull/253 — branch `docs/protocol-unification` from origin/main febd0cb7. Final head `d31dc32d0a5a0fceceab81d5f8f0d2d9a28e4437`. Outputs are verbatim.

### task file verification

```text
$ sha256sum .orchestration/tasks/dotfiles-T69-protocol-docs-unification-a01.md
40b66d86d0896e85e2e4f3f756aa09cf573d2f23cab13032a1ea00a02bc47ff9  /home/moriya/Workspace/dotfiles/.orchestration/tasks/dotfiles-T69-protocol-docs-unification-a01.md
```

### commits

```text
$ git log --format="%H %s" febd0cb7..HEAD
d31dc32d0a5a0fceceab81d5f8f0d2d9a28e4437 docs(orchestration): continue after an incorrect audit verdict and filter the Bot wait to Bot comments
0d9cb61afd9953fb452657c3b06449b525773dad Merge branch 'main' into docs/protocol-unification
c6b348ba5d271717292962c2b47c6c87b133fd2a feat(claude): enable auto mode with publish denies (#254)
3c6a3cb2b15c8b5ba44d8d1a7f0eeed47fdf700d docs(orchestration): ungated boundary PRs, masked headless audits, AUDIT_DISPOSITIONS in the README example
82611f39f9ad5e33bb14b31951f3f56e0a958872 Merge branch 'main' into docs/protocol-unification
4e83dd8dc0b43b0cbe9911d5c4789873e1ebe274 docs(orchestration): make the audit and Bot-wait steps executable as written
6de9516757077c85126f3ec9074a947a243c3ae0 fix(git): ignore the Claude Code sandbox placeholder files at the repository root (#252)
acb1b93c5f834fb34b5d44770054e6e3150ed8c6 docs(orchestration): unify the audit, integration and Bot-wait protocol after T64/T67/T68
```

## On the first commit acb1b93c (origin/main febd0cb7)

### `git diff origin/main --stat`

```text
 AGENTS.md                                          |  4 +--
 Makefile                                           |  6 +++--
 README.md                                          | 10 +++++---
 .../dot_agents/skills/agmsg-orchestration/SKILL.md | 26 ++++++++++++++++---
 home/dot_agents/skills/gh-first-workflow/SKILL.md  |  2 +-
 .../dot_config/claude/rules/agmsg-orchestration.md |  4 +--
 home/dot_config/claude/rules/model-selection.md    |  2 +-
 home/dot_config/claude/rules/pr-integration.md     |  1 +
 home/dot_config/codex/AGENTS.md                    |  3 ++-
 home/dot_local/bin/common/executable_herdr-agents  |  2 +-
 tests/unit/test_agmsg_orchestration_docs.py        | 29 ++++++++++++++++++++++
 tests/unit/test_herdr_agents.py                    |  5 ++--
 12 files changed, 75 insertions(+), 19 deletions(-)
exit status: 0
```

### `grep -rn "review --commit" AGENTS.md README.md home/dot_config home/dot_agents home/dot_local/bin/common/executable_herdr-agents Makefile ; echo "rc=$?"`

```text
README.md:786:`codex review --commit` is not used: it accepts no prompt with `--commit` and
rc=0
```

### `grep -rln "AUDIT_EVIDENCE" AGENTS.md README.md Makefile home/dot_agents/skills home/dot_config`

```text
AGENTS.md
Makefile
README.md
home/dot_config/codex/AGENTS.md
home/dot_config/claude/rules/agmsg-orchestration.md
home/dot_agents/skills/gh-first-workflow/SKILL.md
home/dot_agents/skills/agmsg-orchestration/SKILL.md
home/dot_config/claude/rules/pr-integration.md
exit status: 0
```

### `uv run python -m unittest tests.unit.test_agmsg_orchestration_docs tests.unit.test_herdr_agents 2>&1 | tail -3`

```text
Ran 235 tests in 130.558s

OK (skipped=1)
```

### `mise x node npm:prettier -- prettier --check README.md AGENTS.md home/dot_config/claude/rules/*.md home/dot_agents/skills/agmsg-orchestration/SKILL.md`

```text
Checking formatting...
All matched files use Prettier code style!
exit status: 0
```

## Item 4 VERIFY: REST field names

```text
$ gh api repos/mryfmo/dotfiles/pulls/243/reviews --jq '.[]|select(.user.type=="Bot")|[.commit_id,.submitted_at,.user.login,.user.type]|@tsv' | head -3
e50150df15039af16cda2c41b607cc3e65fafeca	2026-10-04T01:14:51Z	chatgpt-codex-connector[bot]	Bot
3222564734bc43a28d8341c29b269028732d239c	2026-10-04T03:16:40Z	chatgpt-codex-connector[bot]	Bot
c5706e2e53fef7e0e9c90f2873b4835193f03a52	2026-10-04T03:38:45Z	chatgpt-codex-connector[bot]	Bot
$ gh api repos/mryfmo/dotfiles/pulls/243/comments --jq '.[0] | {id, in_reply_to_id, commit_id, original_commit_id, user_type: .user.type}'
{"commit_id":"e50150df15039af16cda2c41b607cc3e65fafeca","id":4175647852,"in_reply_to_id":null,"original_commit_id":"e50150df15039af16cda2c41b607cc3e65fafeca","user_type":"Bot"}
```

GitHub REST docs (WebFetch, apiVersion 2022-11-28): `GET /repos/{owner}/{repo}/pulls/{pull_number}/reviews` documents `commit_id` ("required, string or null"), `submitted_at` ("string, format: date-time"), `user.type` ("required, string"), `state`, default `per_page` 30 (max 100), chronological order; `GET /repos/{owner}/{repo}/pulls/{pull_number}/comments` documents `in_reply_to_id` (integer, the comment it replies to), `commit_id`, `original_commit_id`, default `per_page` 30 (max 100).

## Final head d31dc32d (after review fixes 4e83dd8d, 3c6a3cb2, d31dc32d and update-branch merges of main 6de95167 and c6b348ba)

### `git diff origin/main --stat` (origin/main = c6b348ba)

```text
 AGENTS.md                                          |  4 +--
 Makefile                                           |  6 +++--
 README.md                                          | 12 ++++++---
 .../dot_agents/skills/agmsg-orchestration/SKILL.md | 28 ++++++++++++++++++---
 home/dot_agents/skills/gh-first-workflow/SKILL.md  |  2 +-
 .../dot_config/claude/rules/agmsg-orchestration.md |  4 +--
 home/dot_config/claude/rules/model-selection.md    |  2 +-
 home/dot_config/claude/rules/pr-integration.md     |  1 +
 home/dot_config/codex/AGENTS.md                    |  3 ++-
 home/dot_local/bin/common/executable_herdr-agents  |  2 +-
 tests/unit/test_agmsg_orchestration_docs.py        | 29 ++++++++++++++++++++++
 tests/unit/test_herdr_agents.py                    |  5 ++--
 12 files changed, 79 insertions(+), 19 deletions(-)
```

### `grep -rn "review --commit" AGENTS.md README.md home/dot_config home/dot_agents home/dot_local/bin/common/executable_herdr-agents Makefile ; echo "rc=$?"`

```text
README.md:786:`codex review --commit` is not used: it accepts no prompt with `--commit` and
rc=0
```

### `grep -rln "AUDIT_EVIDENCE" AGENTS.md README.md Makefile home/dot_agents/skills home/dot_config`

```text
home/dot_agents/skills/agmsg-orchestration/SKILL.md
Makefile
home/dot_agents/skills/gh-first-workflow/SKILL.md
home/dot_config/codex/AGENTS.md
home/dot_config/claude/rules/agmsg-orchestration.md
AGENTS.md
README.md
home/dot_config/claude/rules/pr-integration.md
```

### `uv run python -m unittest tests.unit.test_agmsg_orchestration_docs tests.unit.test_herdr_agents 2>&1 | tail -3`

```text
Ran 235 tests in 132.855s

OK
```

### `mise x node npm:prettier -- prettier --check README.md AGENTS.md home/dot_config/claude/rules/*.md home/dot_agents/skills/agmsg-orchestration/SKILL.md`

```text
Checking formatting...
All matched files use Prettier code style!
exit status: 0
```

### `make unit-test` on d31dc32d (tail)

```text
Ran 777 tests in 174.556s

OK
unit-test rc=0
```

### `make validate-agent-assets` on d31dc32d (tail; regime-boundary WARN lines about other tasks omitted)

```text
uv run --with pyyaml scripts/validate-agent-assets.py
agent asset validation ok
validate-agent-assets rc=0
```

### `gh pr checks 253` and `mergeable_state`

```text
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37198640082/job/111425572949	
private-bootstrap (macos-14, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37198640131/job/111425573053	
private-bootstrap (ubuntu-24.04, client)	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/37198640131/job/111425573191	
private-bootstrap (ubuntu-24.04, server)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37198640131/job/111425573142	
public-bootstrap (macos-14, client)	pass	8m7s	https://github.com/mryfmo/dotfiles/actions/runs/37198640131/job/111425573172	
public-bootstrap (ubuntu-24.04, client)	pass	6m50s	https://github.com/mryfmo/dotfiles/actions/runs/37198640131/job/111425573149	
public-bootstrap (ubuntu-24.04, server)	pass	7m24s	https://github.com/mryfmo/dotfiles/actions/runs/37198640131/job/111425573205	
test (macos-14, client)	pass	6m4s	https://github.com/mryfmo/dotfiles/actions/runs/37198640082/job/111425600715	
test (ubuntu-24.04, client)	pass	7m18s	https://github.com/mryfmo/dotfiles/actions/runs/37198640082/job/111425600653	
test (ubuntu-24.04, server)	pass	4m15s	https://github.com/mryfmo/dotfiles/actions/runs/37198640082/job/111425600658	
test (ubuntu-26.04, client)	pass	6m45s	https://github.com/mryfmo/dotfiles/actions/runs/37198640082/job/111425600651	
validate	pass	15s	https://github.com/mryfmo/dotfiles/actions/runs/37198640171/job/111425573145	
exit status: 0
d31dc32d0a5a0fceceab81d5f8f0d2d9a28e4437
blocked
c6b348ba5d271717292962c2b47c6c87b133fd2a	refs/heads/main
```

## Bot waits (Worker Playbook step 15, script `/tmp/claude-1000/botwait.py <pr> <head> <deadline>`)

```text
window 2026-10-04T10:34:40Z .. 2026-10-04T10:34:41Z; final head acb1b93c5f834fb34b5d44770054e6e3150ed8c6
$ gh api --paginate repos/mryfmo/dotfiles/pulls/253/reviews --jq '.[]|select(.user.type=="Bot")|[.commit_id,.submitted_at]|@tsv'
acb1b93c5f834fb34b5d44770054e6e3150ed8c6	2026-10-04T10:32:18Z
$ gh api --paginate repos/mryfmo/dotfiles/pulls/253/comments --jq '.[]|select(.in_reply_to_id == null)|[.id,.commit_id,.path]|@tsv'
4177126680	acb1b93c5f834fb34b5d44770054e6e3150ed8c6	home/dot_agents/skills/agmsg-orchestration/SKILL.md
4177126683	acb1b93c5f834fb34b5d44770054e6e3150ed8c6	home/dot_agents/skills/agmsg-orchestration/SKILL.md
4177126686	acb1b93c5f834fb34b5d44770054e6e3150ed8c6	home/dot_agents/skills/agmsg-orchestration/SKILL.md
4177126689	acb1b93c5f834fb34b5d44770054e6e3150ed8c6	home/dot_agents/skills/agmsg-orchestration/SKILL.md
review of final head: yes
```

```text
window 2026-10-04T10:52:36Z .. 2026-10-04T10:52:37Z; final head 82611f39f9ad5e33bb14b31951f3f56e0a958872
$ gh api --paginate repos/mryfmo/dotfiles/pulls/253/reviews --jq '.[]|select(.user.type=="Bot")|[.commit_id,.submitted_at]|@tsv'
acb1b93c5f834fb34b5d44770054e6e3150ed8c6	2026-10-04T10:32:18Z
82611f39f9ad5e33bb14b31951f3f56e0a958872	2026-10-04T10:44:50Z
$ gh api --paginate repos/mryfmo/dotfiles/pulls/253/comments --jq '.[]|select(.in_reply_to_id == null)|[.id,.commit_id,.path]|@tsv'
4177126680	82611f39f9ad5e33bb14b31951f3f56e0a958872	home/dot_agents/skills/agmsg-orchestration/SKILL.md
4177126683	82611f39f9ad5e33bb14b31951f3f56e0a958872	home/dot_agents/skills/agmsg-orchestration/SKILL.md
4177126686	acb1b93c5f834fb34b5d44770054e6e3150ed8c6	home/dot_agents/skills/agmsg-orchestration/SKILL.md
4177126689	acb1b93c5f834fb34b5d44770054e6e3150ed8c6	home/dot_agents/skills/agmsg-orchestration/SKILL.md
4177157846	82611f39f9ad5e33bb14b31951f3f56e0a958872	home/dot_config/claude/rules/pr-integration.md
4177157848	82611f39f9ad5e33bb14b31951f3f56e0a958872	home/dot_agents/skills/agmsg-orchestration/SKILL.md
4177157852	82611f39f9ad5e33bb14b31951f3f56e0a958872	README.md
review of final head: yes
```

```text
window 2026-10-04T11:20:57Z .. 2026-10-04T11:20:58Z; final head 0d9cb61afd9953fb452657c3b06449b525773dad
$ gh api --paginate repos/mryfmo/dotfiles/pulls/253/reviews --jq '.[]|select(.user.type=="Bot")|[.commit_id,.submitted_at]|@tsv'
acb1b93c5f834fb34b5d44770054e6e3150ed8c6	2026-10-04T10:32:18Z
82611f39f9ad5e33bb14b31951f3f56e0a958872	2026-10-04T10:44:50Z
0d9cb61afd9953fb452657c3b06449b525773dad	2026-10-04T11:18:51Z
$ gh api --paginate repos/mryfmo/dotfiles/pulls/253/comments --jq '.[]|select(.in_reply_to_id == null)|[.id,.commit_id,.path]|@tsv'
4177126680	0d9cb61afd9953fb452657c3b06449b525773dad	home/dot_agents/skills/agmsg-orchestration/SKILL.md
4177126683	0d9cb61afd9953fb452657c3b06449b525773dad	home/dot_agents/skills/agmsg-orchestration/SKILL.md
4177126686	acb1b93c5f834fb34b5d44770054e6e3150ed8c6	home/dot_agents/skills/agmsg-orchestration/SKILL.md
4177126689	acb1b93c5f834fb34b5d44770054e6e3150ed8c6	home/dot_agents/skills/agmsg-orchestration/SKILL.md
4177157846	82611f39f9ad5e33bb14b31951f3f56e0a958872	home/dot_config/claude/rules/pr-integration.md
4177157848	82611f39f9ad5e33bb14b31951f3f56e0a958872	home/dot_agents/skills/agmsg-orchestration/SKILL.md
4177157852	0d9cb61afd9953fb452657c3b06449b525773dad	README.md
4177247697	0d9cb61afd9953fb452657c3b06449b525773dad	home/dot_agents/skills/agmsg-orchestration/SKILL.md
4177247706	0d9cb61afd9953fb452657c3b06449b525773dad	home/dot_agents/skills/agmsg-orchestration/SKILL.md
4177247710	0d9cb61afd9953fb452657c3b06449b525773dad	home/dot_agents/skills/agmsg-orchestration/SKILL.md
review of final head: yes
```

```text
window 2026-10-04T11:33:21Z .. 2026-10-04T11:39:34Z; final head d31dc32d0a5a0fceceab81d5f8f0d2d9a28e4437
$ gh api --paginate repos/mryfmo/dotfiles/pulls/253/reviews --jq '.[]|select(.user.type=="Bot")|[.commit_id,.submitted_at]|@tsv'
acb1b93c5f834fb34b5d44770054e6e3150ed8c6	2026-10-04T10:32:18Z
82611f39f9ad5e33bb14b31951f3f56e0a958872	2026-10-04T10:44:50Z
0d9cb61afd9953fb452657c3b06449b525773dad	2026-10-04T11:18:51Z
$ gh api --paginate repos/mryfmo/dotfiles/pulls/253/comments --jq '.[]|select(.in_reply_to_id == null and .user.type=="Bot")|[.id,.commit_id,.path]|@tsv'
4177126680	0d9cb61afd9953fb452657c3b06449b525773dad	home/dot_agents/skills/agmsg-orchestration/SKILL.md
4177126683	0d9cb61afd9953fb452657c3b06449b525773dad	home/dot_agents/skills/agmsg-orchestration/SKILL.md
4177126686	acb1b93c5f834fb34b5d44770054e6e3150ed8c6	home/dot_agents/skills/agmsg-orchestration/SKILL.md
4177126689	acb1b93c5f834fb34b5d44770054e6e3150ed8c6	home/dot_agents/skills/agmsg-orchestration/SKILL.md
4177157846	82611f39f9ad5e33bb14b31951f3f56e0a958872	home/dot_config/claude/rules/pr-integration.md
4177157848	82611f39f9ad5e33bb14b31951f3f56e0a958872	home/dot_agents/skills/agmsg-orchestration/SKILL.md
4177157852	d31dc32d0a5a0fceceab81d5f8f0d2d9a28e4437	README.md
4177247697	0d9cb61afd9953fb452657c3b06449b525773dad	home/dot_agents/skills/agmsg-orchestration/SKILL.md
4177247706	0d9cb61afd9953fb452657c3b06449b525773dad	home/dot_agents/skills/agmsg-orchestration/SKILL.md
4177247710	0d9cb61afd9953fb452657c3b06449b525773dad	home/dot_agents/skills/agmsg-orchestration/SKILL.md
review of final head: no (bot: none)
```

(The first three listings used the comments query without the Bot filter; it was added to the procedure and the script by d31dc32d, and the fourth listing uses it.)

### CompactionDB (main checkout, run unsandboxed)

```text
$ cd /home/moriya/Workspace/dotfiles && python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "dotfiles-T69 (operator 2026-10-03): the written protocol names one audit per task on the final head via \`herdr-agents --audit <sha> --task <id>\` (headless \`codex … exec --sandbox read-only\` otherwise), the acceptance order sweep → audit → acceptance record → gate with \`AUDIT_EVIDENCE\` → merge → ACCEPTANCE, the worker's Bot-wait by listing reviews of the final head, and the boundary PR as a sweep-free, audit-free exception; \`codex --profile audit review --commit\` is no longer written anywhere."
784fed94-42f9-4daf-8f1c-5f1f2fa53214
```
