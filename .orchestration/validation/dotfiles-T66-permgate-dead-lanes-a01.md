# dotfiles-T66-permgate-dead-lanes-a01 — validation

PR: https://github.com/mryfmo/dotfiles/pull/240 — branch `chore/permgate-dead-lanes` — task commit `8ae3fdc9eb88030a3238d25def30ac8a00ab36a6`; final head `4ab48bce085dc834220b891858a4693587db8ac2` (`gh pr update-branch` merge of main 3a0816e6). Outputs are verbatim.

## On the task commit 8ae3fdc9 (base origin/main 523fda06)

### `git diff origin/main --stat`

```text
 README.md                                       |  23 +-
 home/dot_agents/permgate-policy.yaml            |  76 +--
 home/dot_config/claude/rules/model-selection.md |   4 +-
 home/dot_config/codex/AGENTS.md                 |   2 +-
 home/dot_local/bin/common/executable_permgate   | 548 +---------------
 scripts/validate-agent-assets.py                |  22 +-
 tests/install/common/lifecycle.bats             |   4 -
 tests/unit/test_permgate.py                     | 793 +-----------------------
 8 files changed, 50 insertions(+), 1422 deletions(-)
exit status: 0
```

### `wc -l home/dot_local/bin/common/executable_permgate`

```text
252 home/dot_local/bin/common/executable_permgate
exit status: 0
```

### `grep -n '"cli"\|classif\|bench\|shadow' home/dot_local/bin/common/executable_permgate; echo "exit=$?"`

```text
exit=1
```

### `uv run python -m unittest tests.unit.test_permgate 2>&1 | tail -3`

```text
Ran 17 tests in 1.175s

OK
```

### task literal: gh pr view 1, live ~/.agents policy (schema 2, pre-apply)

```text
[exit=0]
{"agent":"claude","decision":"ask","input_hash":"996772ccae343e2d87deb80b76da85bdc4a599b4920b086a6c090c4871ccd924","input_summary":"Bash:gh","latency_ms":0,"layer":"config-error","tool":"Bash","ts":"2026-10-04T00:39:09.901928+00:00"}
```

### gh pr view 1 with PERMGATE_POLICY_PATH=home/dot_agents/permgate-policy.yaml (allow JSON)

```text
{"hookSpecificOutput":{"hookEventName":"PermissionRequest","decision":{"behavior":"allow"}}}
[exit=0]
```

### ls with PERMGATE_POLICY_PATH=home/dot_agents/permgate-policy.yaml (stdout must be empty)

```text
[exit=0 stdout must be empty]
```

### `mise x node npm:prettier -- prettier --check README.md home/dot_config/claude/rules/model-selection.md home/dot_config/codex/AGENTS.md`

```text
Checking formatting...
All matched files use Prettier code style!
exit status: 0
```

### `ruff format --config ruff.toml --check tests/unit/test_permgate.py scripts/validate-agent-assets.py`

```text
2 files already formatted
exit status: 0
```

### `make unit-test` on 8ae3fdc9 (tail)

```text
----------------------------------------------------------------------
Ran 688 tests in 156.316s

OK (skipped=1)
unit-test rc=0
```

### `make validate-agent-assets` on 8ae3fdc9 (tail, regime-boundary WARN lines about other tasks omitted)

```text
uv run --with pyyaml scripts/validate-agent-assets.py
agent asset validation ok
validate-agent-assets rc=0
```

### `git push` / `gh pr create`

```text
To github.com:mryfmo/dotfiles.git
 * [new branch]        HEAD -> chore/permgate-dead-lanes
https://github.com/mryfmo/dotfiles/pull/240
```

## On the final head 4ab48bce (after `gh pr update-branch 240`: main moved to 3a0816e6, #239)

### `gh pr update-branch 240`

```text
✓ PR branch updated
```

### `git diff origin/main --stat` (origin/main = 3a0816e6)

```text
 README.md                                       |  23 +-
 home/dot_agents/permgate-policy.yaml            |  76 +--
 home/dot_config/claude/rules/model-selection.md |   4 +-
 home/dot_config/codex/AGENTS.md                 |   2 +-
 home/dot_local/bin/common/executable_permgate   | 548 +---------------
 scripts/validate-agent-assets.py                |  22 +-
 tests/install/common/lifecycle.bats             |   4 -
 tests/unit/test_permgate.py                     | 793 +-----------------------
 8 files changed, 50 insertions(+), 1422 deletions(-)
```

### `make unit-test` on 4ab48bce (tail)

```text
----------------------------------------------------------------------
Ran 695 tests in 159.056s

OK (skipped=1)
unit-test rc=0
```

### `make validate-agent-assets` on 4ab48bce (tail)

```text
uv run --with pyyaml scripts/validate-agent-assets.py
agent asset validation ok
validate-agent-assets rc=0
```

### prettier on 4ab48bce

```text
Checking formatting...
All matched files use Prettier code style!
prettier rc=0
```

### `gh pr checks 240`

```text
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37165952528/job/111328743589	
build (client)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37165952549/job/111328743747	
build (server)	pass	3s	https://github.com/mryfmo/dotfiles/actions/runs/37165952549/job/111328743826	
changes	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37165952572/job/111328743866	
private-bootstrap (macos-14, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37165952537/job/111328743876	
private-bootstrap (ubuntu-24.04, client)	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/37165952537/job/111328743835	
private-bootstrap (ubuntu-24.04, server)	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/37165952537/job/111328743930	
public-bootstrap (macos-14, client)	pass	9m38s	https://github.com/mryfmo/dotfiles/actions/runs/37165952537/job/111328743796	
public-bootstrap (ubuntu-24.04, client)	pass	8m54s	https://github.com/mryfmo/dotfiles/actions/runs/37165952537/job/111328743836	
public-bootstrap (ubuntu-24.04, server)	pass	7m25s	https://github.com/mryfmo/dotfiles/actions/runs/37165952537/job/111328743900	
nix	skipping	0	https://github.com/mryfmo/dotfiles/actions/runs/37165952572/job/111328773113	
test (macos-14, client)	pass	5m10s	https://github.com/mryfmo/dotfiles/actions/runs/37165952572/job/111328772137	
test (ubuntu-24.04, client)	pass	6m48s	https://github.com/mryfmo/dotfiles/actions/runs/37165952572/job/111328772109	
test (ubuntu-24.04, server)	pass	3m58s	https://github.com/mryfmo/dotfiles/actions/runs/37165952572/job/111328772132	
test (ubuntu-26.04, client)	pass	7m7s	https://github.com/mryfmo/dotfiles/actions/runs/37165952572/job/111328772219	
validate	pass	14s	https://github.com/mryfmo/dotfiles/actions/runs/37165952533/job/111328743651	
exit status: 0
```

### `gh api repos/mryfmo/dotfiles/pulls/240 --jq .head.sha,.mergeable_state`; `git ls-remote origin refs/heads/main`

```text
4ab48bce085dc834220b891858a4693587db8ac2
clean
3a0816e6d333e16d56923f38ba27042e44ef9482	refs/heads/main
```

### Codex Bot (reviews count / inline comments count / PR reactions)

```text
0
0
chatgpt-codex-connector[bot]	+1	2026-10-04T00:48:33Z
```

### CompactionDB (main checkout, run unsandboxed)

```text
$ cd ~/Workspace/dotfiles && python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "dotfiles-T66 (operator 2026-10-03): permgate keeps only its deterministic deny/allow lanes and the native-prompt fallthrough; the shadow LLM classifier lane, the cli workspace lane and the benchmark are deleted as dead code (0 denies in 425 decisions, 0 callers)."
151d0f98-0bd5-4d65-a43d-ebebcd3004ed
```

### Crit server close (`pgrep -af "[c]rit _serve"` unsandboxed, before and after `kill 4129281`)

```text
4129281 ~/.local/bin/crit _serve --plan-dir ~/.crit/plans/plan-agmsg-actas-claude-standard-dot-a006-2026-10-04 ...
4150161 ~/.local/bin/crit _serve --plan-dir ~/.crit/plans/plan-agmsg-actas-claude-standard-dot-a007-2026-10-04 ...
--- after kill 4129281 ---
4150161 ~/.local/bin/crit _serve --plan-dir ~/.crit/plans/plan-agmsg-actas-claude-standard-dot-a007-2026-10-04 --name plan-agmsg-actas-claude-standard-dot-a007-2026-10-04 ~/.crit/plans/plan-agmsg-actas-claude-standard-dot-a007-2026-10-04/current.md
```

## Revise round 1 (task_rev b7fa55fe…) — fix commit `a93fcb94793627c525a01263f2255d86d79004ba` on top of f26975ab

### `git log --oneline -4`

```text
a93fcb94 fix(permgate): reject non-object policies and drop the stale classifier-model sentence
f26975ab Merge branch 'main' into chore/permgate-dead-lanes
40d9eb6c chore(ci): read statusline tool versions and the awscli fingerprint from their pins (#241)
4ab48bce Merge branch 'main' into chore/permgate-dead-lanes
```

### `git show --stat a93fcb94`

```text
a93fcb94793627c525a01263f2255d86d79004ba fix(permgate): reject non-object policies and drop the stale classifier-model sentence

 home/dot_config/codex/AGENTS.md               |  2 +-
 home/dot_local/bin/common/executable_permgate |  2 +-
 scripts/validate-agent-assets.py              | 14 +++++++++++---
 tests/unit/test_permgate.py                   | 12 +++++++-----
 tests/unit/test_validate_agent_assets.py      | 22 ++++++++++++++++++++++
 5 files changed, 42 insertions(+), 10 deletions(-)
```

### `uv run python -m unittest tests.unit.test_permgate tests.unit.test_validate_agent_assets 2>&1 | tail -3`

```text
Ran 77 tests in 1.439s

OK
```

### named validator test `test_permgate_policy_requires_a_schema_3_object` (-v)

```text

----------------------------------------------------------------------
Ran 1 test in 0.011s

OK
```

### `grep -n 分類器 home/dot_config/codex/AGENTS.md` (only the deterministic-only line may remain)

```text
55:- permgate は deterministic-only です。PermissionRequest は policy の deny/allow パターンだけで判定し、それ以外と失敗時は Codex native の確認へ fail-closed します。分類器モデルは使いません。
```

### `make unit-test` on a93fcb94 (tail)

```text
Ran 696 tests in 158.001s

OK (skipped=1)
unit-test rc=0
```

### `make validate-agent-assets` on a93fcb94 (tail)

```text
agent asset validation ok
validate-agent-assets rc=0
```

### `git push origin HEAD:refs/heads/chore/permgate-dead-lanes`

```text
   f26975ab..a93fcb94  HEAD -> chore/permgate-dead-lanes
```

### `gh pr checks 240` (head a93fcb94)

```text
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/37168274438/job/111335733242	
build (client)	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/37168274437/job/111335733435	
build (server)	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/37168274437/job/111335733312	
changes	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37168274475/job/111335733383	
private-bootstrap (macos-14, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37168274477/job/111335733516	
private-bootstrap (ubuntu-24.04, client)	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/37168274477/job/111335733533	
private-bootstrap (ubuntu-24.04, server)	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/37168274477/job/111335733345	
public-bootstrap (macos-14, client)	pass	9m32s	https://github.com/mryfmo/dotfiles/actions/runs/37168274477/job/111335733590	
public-bootstrap (ubuntu-24.04, client)	pass	9m8s	https://github.com/mryfmo/dotfiles/actions/runs/37168274477/job/111335733463	
public-bootstrap (ubuntu-24.04, server)	pass	7m1s	https://github.com/mryfmo/dotfiles/actions/runs/37168274477/job/111335733500	
test (macos-14, client)	pass	5m53s	https://github.com/mryfmo/dotfiles/actions/runs/37168274475/job/111335757491	
validate	pass	17s	https://github.com/mryfmo/dotfiles/actions/runs/37168274448/job/111335733386	
nix	skipping	0	https://github.com/mryfmo/dotfiles/actions/runs/37168274475/job/111335758133	
test (ubuntu-24.04, client)	pass	6m55s	https://github.com/mryfmo/dotfiles/actions/runs/37168274475/job/111335757440	
test (ubuntu-24.04, server)	pass	3m48s	https://github.com/mryfmo/dotfiles/actions/runs/37168274475/job/111335757422	
test (ubuntu-26.04, client)	pass	7m38s	https://github.com/mryfmo/dotfiles/actions/runs/37168274475/job/111335757454	
exit status: 0
```

### Codex Bot on a93fcb94

No review or reaction between the 01:30Z push and 01:50:01Z (wait loop output `reviews_on_head=0 bot_reactions=0`); recorded as `bot: none` for that head. main then moved to 57885db1 (#242).

### `gh pr update-branch 240` → 55933ff8; Codex review of 55933ff8 raised P2 4175753764 (executable_permgate:75, null pattern entry → uncaught AttributeError)

## Revise round 1, follow-up fix commit `a31dcf868d06103564d9ff643dc928e20f8c62b2` (Codex P2 4175753764)

### `git show --stat a31dcf86`

```text
a31dcf868d06103564d9ff643dc928e20f8c62b2 fix(permgate): fail closed on malformed pattern entries

 home/dot_local/bin/common/executable_permgate |  2 +-
 scripts/validate-agent-assets.py              |  7 +++++++
 tests/unit/test_permgate.py                   |  7 ++++++-
 tests/unit/test_validate_agent_assets.py      | 10 ++++++++++
 4 files changed, 24 insertions(+), 2 deletions(-)
```

### `uv run python -m unittest tests.unit.test_permgate tests.unit.test_validate_agent_assets 2>&1 | tail -3`

```text
Ran 77 tests in 1.378s

OK
```

### null-entry smoke (`allow_patterns: [null]`), exit code and log layer

```text
(rerun: the first capture passed a malformed payload because of a `%%s` escape and logged `input-error`; this is the correct run)
[exit=0 stdout must be empty]
{"agent":"claude","decision":"ask","input_hash":"996772ccae343e2d87deb80b76da85bdc4a599b4920b086a6c090c4871ccd924","input_summary":"Bash:gh","latency_ms":0,"layer":"config-error","tool":"Bash","ts":"2026-10-04T02:19:42.292824+00:00"}
```

### `make unit-test` on a31dcf86 (tail)

```text
Ran 700 tests in 159.858s

OK (skipped=1)
unit-test rc=0
```

### `make validate-agent-assets` on a31dcf86 (tail)

```text
agent asset validation ok
validate-agent-assets rc=0
```

### `git push`

```text
   55933ff8..a31dcf86  HEAD -> chore/permgate-dead-lanes
```

### `gh pr checks 240` (final head a31dcf86)

```text
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37169981112/job/111340764251	
build (client)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37169981129/job/111340764302	
build (server)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/37169981129/job/111340764127	
changes	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37169981120/job/111340764062	
private-bootstrap (macos-14, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37169981107/job/111340764287	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37169981107/job/111340764283	
private-bootstrap (ubuntu-24.04, server)	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/37169981107/job/111340764232	
public-bootstrap (macos-14, client)	pass	13m14s	https://github.com/mryfmo/dotfiles/actions/runs/37169981107/job/111340764292	
public-bootstrap (ubuntu-24.04, client)	pass	6m52s	https://github.com/mryfmo/dotfiles/actions/runs/37169981107/job/111340764249	
public-bootstrap (ubuntu-24.04, server)	pass	6m52s	https://github.com/mryfmo/dotfiles/actions/runs/37169981107/job/111340764121	
nix	skipping	0	https://github.com/mryfmo/dotfiles/actions/runs/37169981120/job/111340792049	
test (macos-14, client)	pass	5m26s	https://github.com/mryfmo/dotfiles/actions/runs/37169981120/job/111340791451	
test (ubuntu-24.04, client)	pass	7m2s	https://github.com/mryfmo/dotfiles/actions/runs/37169981120/job/111340791469	
test (ubuntu-24.04, server)	pass	4m22s	https://github.com/mryfmo/dotfiles/actions/runs/37169981120/job/111340791474	
test (ubuntu-26.04, client)	pass	6m45s	https://github.com/mryfmo/dotfiles/actions/runs/37169981120/job/111340791408	
validate	pass	13s	https://github.com/mryfmo/dotfiles/actions/runs/37169981118/job/111340764067	
exit status: 0 (re-derived after the fact: `gh pr checks 240` on the same head a31dcf86 exited 0; the original capture printed a literal format string)
```

### final state: head, mergeable_state, origin/main, Codex reviews, inline comments, reactions

```text
a31dcf868d06103564d9ff643dc928e20f8c62b2
blocked
57885db1d080325d78c444c386c58fc25646d22e	refs/heads/main
COMMENTED	f26975ab	2026-10-04T01:14:20Z
COMMENTED	55933ff8	2026-10-04T01:55:22Z
4175645727	f26975ab	home/dot_config/codex/AGENTS.md	2026-10-04T01:14:20Z
4175645733	f26975ab	scripts/validate-agent-assets.py	2026-10-04T01:14:21Z
4175753764	55933ff8	home/dot_local/bin/common/executable_permgate	2026-10-04T01:55:22Z
chatgpt-codex-connector[bot]	+1	2026-10-04T02:07:23Z
```
