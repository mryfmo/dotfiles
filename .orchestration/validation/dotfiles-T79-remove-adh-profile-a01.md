# dotfiles-T79-remove-adh-profile-a01 — validation

PR #267 (https://github.com/mryfmo/dotfiles/pull/267), branch `chore/remove-adh-profile`.

- Diff head: `c86eb99a42edef32d7d30ad063f1824709de8607`, on `origin/main` 36ffe6ca.
- Final head: `123bf10476c85911e55eabc7f1795fa597f13195`, the `gh pr update-branch` merge of main 8ba3c8bc (#266).

## Task file verification

```text
$ sha256sum ~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T79-remove-adh-profile-a01.md
def2ae58e778a8416769efb1f16fa7b7e1e7d63bac9011bfcc6e39a37a66dbc7  ~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T79-remove-adh-profile-a01.md
dispatched task_rev def2ae58…; matches
```

## Validation commands on the diff head c86eb99a (verbatim)

The two remaining grep hits are intended:

- the `.chezmoiremove` retirement entry;
- the new test that rejects an extra `adh` profile.

`README.md` names no `adh` profile, so there is nothing to list for T83.

```text
$ git rev-parse HEAD; echo "rc=$?"
c86eb99a42edef32d7d30ad063f1824709de8607
rc=0
$ git diff origin/main --stat; echo "rc=$?"
 home/.chezmoiremove                           |   1 +
 home/dot_agents/agent-config.yaml             |   8 --
 home/dot_agents/model-profiles.env            |   2 -
 home/dot_codex/modify_private_adh.config.toml | 161 --------------------------
 scripts/check-agent-runtime.py                |  24 +---
 scripts/generate-agent-configs.py             |  17 ---
 scripts/validate-agent-assets.py              |  21 +---
 tests/unit/test_validate_agent_assets.py      |   9 ++
 8 files changed, 13 insertions(+), 230 deletions(-)
rc=0
$ /usr/bin/grep -rn --exclude-dir=__pycache__ "adh\b\|ADH" home scripts tests | /usr/bin/grep -v worktrees; echo "rc=$?"
home/.chezmoiremove:2:.codex/adh.config.toml
tests/unit/test_validate_agent_assets.py:714:        manifest["model_profiles"]["adh"] = manifest["model_profiles"]["deep"]
rc=0
$ /usr/bin/grep -n -i "\badh\b\|MODEL_PROFILE_ADH" README.md; echo "rc=$?"   (README mentions for T83: none)
rc=1
$ git diff origin/main --stat -- home/dot_codex home/.chezmoitemplates home/dot_agents/model-profiles.env; echo "rc=$?"   (only the adh source and the two env lines change)
 home/dot_agents/model-profiles.env            |   2 -
 home/dot_codex/modify_private_adh.config.toml | 161 --------------------------
 2 files changed, 163 deletions(-)
rc=0
$ make render-check; echo "rc=$?"
uv run --with pyyaml scripts/generate-agent-configs.py --check
generated agent configs are up to date
rc=0
$ make validate-agent-assets 2>&1 | grep -v "^WARN: regime-boundary" | tail -3; echo "rc=$?"   (exit status captured without a pipe)
uv run --with pyyaml scripts/validate-agent-assets.py
agent asset validation ok
rc=0
$ make unit-test 2>&1 | tail -3; echo "rc=$?"   (exit status captured without a pipe)
Ran 788 tests in 196.773s

OK (skipped=1)
rc=0
$ git ls-files -z "*.py" | xargs -0 mise x ruff -- ruff format --config ruff.toml --check; echo "rc=$?"
41 files already formatted
rc=0
$ uv run python -m unittest tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_the_retired_adh_profile -v 2>&1 | tail -4; echo "rc=$?"
----------------------------------------------------------------------
Ran 1 test in 0.003s

OK
rc=0
```

## Re-run on the final head 123bf104 (after the update-branch merge of main 8ba3c8bc)

```text
$ git rev-parse HEAD; git log --format="%h %s" -3
123bf10476c85911e55eabc7f1795fa597f13195
123bf104 Merge branch 'main' into chore/remove-adh-profile
8ba3c8bc fix(hooks): use the current PreToolUse denial contract in the uv hook (#266)
c86eb99a chore(agents): delete the adh model profile
$ make render-check; echo "rc=$?"
uv run --with pyyaml scripts/generate-agent-configs.py --check
generated agent configs are up to date
rc=0
$ make validate-agent-assets 2>&1 | grep -v "^WARN: regime-boundary" | tail -2; echo "rc=$?"   (exit status captured without a pipe)
uv run --with pyyaml scripts/validate-agent-assets.py
agent asset validation ok
rc=0
$ make unit-test 2>&1 | tail -3; echo "rc=$?"   (exit status captured without a pipe)
Ran 790 tests in 197.497s

OK
rc=0
```

## `gh pr checks 267` and state (final head 123bf104)

```text
$ gh pr checks 267 --watch --interval 30; gh pr checks 267
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37229477356/job/111515923499	
private-bootstrap (macos-14, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37229477355/job/111515923320	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37229477355/job/111515923187	
private-bootstrap (ubuntu-24.04, server)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37229477355/job/111515923317	
public-bootstrap (macos-14, client)	pass	8m4s	https://github.com/mryfmo/dotfiles/actions/runs/37229477355/job/111515923332	
public-bootstrap (ubuntu-24.04, client)	pass	8m54s	https://github.com/mryfmo/dotfiles/actions/runs/37229477355/job/111515923366	
public-bootstrap (ubuntu-24.04, server)	pass	6m24s	https://github.com/mryfmo/dotfiles/actions/runs/37229477355/job/111515923331	
test (macos-14, client)	pass	7m1s	https://github.com/mryfmo/dotfiles/actions/runs/37229477356/job/111515949128	
test (ubuntu-24.04, client)	pass	8m3s	https://github.com/mryfmo/dotfiles/actions/runs/37229477356/job/111515949161	
test (ubuntu-24.04, server)	pass	5m7s	https://github.com/mryfmo/dotfiles/actions/runs/37229477356/job/111515949237	
test (ubuntu-26.04, client)	pass	8m19s	https://github.com/mryfmo/dotfiles/actions/runs/37229477356/job/111515949188	
validate	pass	19s	https://github.com/mryfmo/dotfiles/actions/runs/37229477412/job/111515923579	
$ gh api repos/mryfmo/dotfiles/pulls/267 --jq '.head.sha, .mergeable_state'; git ls-remote origin refs/heads/main
123bf10476c85911e55eabc7f1795fa597f13195
clean
8ba3c8bc2f95093646b0779f749d799492179fe1	refs/heads/main
```

## Bot wait (diff head c86eb99a pushed 2026-10-04T19:35:32Z; window ended 19:50:32Z, listing at 19:54Z)

There is no Codex Bot review and no inline comment on either head. The connector left only a +1 reaction on the PR, which is not a review. The CodeRabbit issue comment is its "Review skipped" notice (auto reviews are disabled).

```text
window 2026-10-04T19:54:46Z .. 2026-10-04T19:54:47Z; final head c86eb99a42edef32d7d30ad063f1824709de8607
$ gh api --paginate repos/mryfmo/dotfiles/pulls/267/reviews --jq '.[]|select(.user.type=="Bot")|[.commit_id,.submitted_at]|@tsv'
(no output)
$ gh api --paginate repos/mryfmo/dotfiles/pulls/267/comments --jq '.[]|select(.in_reply_to_id == null and .user.type=="Bot")|[.id,.commit_id,.path]|@tsv'
(no output)
review of final head: no (bot: none)
$ gh api --paginate repos/mryfmo/dotfiles/pulls/267/comments --jq '.[]|select(.in_reply_to_id == null and .user.type=="Bot" and (.original_commit_id=="c86eb99a42edef32d7d30ad063f1824709de8607" or .original_commit_id=="123bf10476c85911e55eabc7f1795fa597f13195"))|[.id,.original_commit_id[:8],.path,.line]|@tsv'
$ gh api --paginate repos/mryfmo/dotfiles/issues/267/comments --jq '.[]|select(.user.type=="Bot")|[.user.login,.created_at]|@tsv'
coderabbitai[bot]	2026-10-04T19:35:40Z
$ gh api repos/mryfmo/dotfiles/issues/267/reactions --jq '.[]|[.user.login,.content,.created_at]|@tsv'
chatgpt-codex-connector[bot]	+1	2026-10-04T19:37:42Z
```

## CompactionDB (main checkout, unsandboxed)

```text
$ cd ~/Workspace/dotfiles && python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'dotfiles-T79 (operator 2026-10-03): the `adh` model profile is deleted from the manifest, the generator, the validator, the runtime check and the Codex profile sources; `.codex/adh.config.toml` is retired through `.chezmoiremove`.'
bc88afea-5083-42ca-9cee-6b78d3e7ad98
```
