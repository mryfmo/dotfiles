# Validation: dotfiles-T91-secret-scan-sk-boundary-a01

- **task_rev:** `sha256:9ac395294dca0960b8c84c61c5979af18e0796c6c9577210c0813e5ebf6652ce`. `sha256sum` of the task file in the main checkout matches.
- **Branch:** `fix/secret-scan-sk-boundary` from `origin/main` 57885db1.
- **PR:** #245, https://github.com/mryfmo/dotfiles/pull/245.
- **Commit:** `35d102b7` (one commit). Final head: `35d102b7fbe10525edec701b93aa1c9024df3970`.

**Masked evidence (accepted deviation, revise round 3 item 3).** Wherever this file would quote a key-shaped literal, that text is masked with the branch's own `scripts/validate-agent-assets.py --mask-secrets`, which rewrites `SECRET_PATTERN` matches to `<redacted:secret-pattern>`:
- the task's sample keys;
- a quoted `token` assignment;
- the Bot's example receipt name.

Verbatim output would put key-shaped literals back into tracked evidence that the scan must flag by design. `--mask-secrets` is the repository's own tool for evidence, and herdr-agents audits use it too. The `True`/`False` results and all other output stay verbatim.

The key-shaped sample strings in the task's snippet output below are masked in this file with the branch's own `scripts/validate-agent-assets.py --mask-secrets`. The masker rewrites `SECRET_PATTERN` matches to `<redacted:secret-pattern>`, the established mechanism for audit evidence. Pasting them literally would make this file trip the very scan this task fixes. The `True`/`False` results beside them are verbatim.

## Validation commands (verbatim; unit tests run in the Claude sandbox; the tree is the PR change, committed right after as `35d102b7`)

```
$ git log -1 --format=%H (pre-commit tree; committed below)
57885db1d080325d78c444c386c58fc25646d22e
$ git diff origin/main --stat
 scripts/validate-agent-assets.py         |  6 +++---
 tests/unit/test_validate_agent_assets.py | 20 ++++++++++++++++++++
 2 files changed, 23 insertions(+), 3 deletions(-)
$ uv run python -m unittest tests.unit.test_validate_agent_assets 2>&1 | tail -3
Ran 61 tests in 0.463s

OK
$ python3 - <<'PY' … (task snippet)
'dotfiles-T67-audit-task-level-a01-review-receipt.md' False
'x <redacted:secret-pattern>' True
'"<redacted:secret-pattern>"' True
'<redacted:secret-pattern>' True
$ make unit-test (tail -3)
Ran 728 tests in 165.678s

OK (skipped=2)
$ make validate-agent-assets; echo exit=$?   (in the worktree)
uv run --with pyyaml scripts/validate-agent-assets.py
agent asset validation ok
exit=0 (re-run with a real exit status; zsh has no PIPESTATUS)
```

## The boundary test fails against the previous pattern

```
$ (scripts/validate-agent-assets.py from origin/main) uv run python -m unittest -k SecretPatternBoundary tests.unit.test_validate_agent_assets
FAIL: test_a_key_prefix_inside_a_hyphenated_word_is_clean (…) (text='dotfiles-T67-audit-task-level-a01-review-receipt.md')
Ran 2 tests in 0.016s
FAILED (failures=1)
```

## The main checkout's current .orchestration tree: old pattern vs branch pattern (every file under .orchestration, read-only)

```
origin/main pattern: 5 file(s) flagged in the main checkout's .orchestration
   .orchestration/reports/dotfiles-T75-shell-dead-code-a01.md
   .orchestration/tasks/dotfiles-T91-secret-scan-sk-boundary-a01.md
   .orchestration/validation/dotfiles-T66-permgate-dead-lanes-a01-audit-a31dcf86.md
   .orchestration/validation/dotfiles-T67-audit-task-level-a01-review-receipt.md
   .orchestration/validation/dotfiles-T75-shell-dead-code-a01.md
branch pattern: 1 file(s) flagged in the main checkout's .orchestration
   .orchestration/tasks/dotfiles-T91-secret-scan-sk-boundary-a01.md
```

The one file the branch pattern still flags is the T91 task file itself. Its validation snippet contains literal key-shaped samples: an `sk-` key after a space, the same in quotes, and a `ghp_` key. A correct scan must flag them, and objective 1 requires that real keys after whitespace or quotes still match. So objective 3 ("`make validate-agent-assets` in the main checkout passes") cannot be met by the regex alone while that file holds the literals. It needs an orchestrator-side edit of the task file: build the samples without the literal shape (as the new test does), or mask them. Editing `.orchestration` was forbidden to me.

## CompactionDB

```
cd ~/Workspace/dotfiles && python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'dotfiles-T91 (operator 2026-10-04): the committed-secret scan anchors key prefixes (`ghp_`, `github_pat_`, `sk-`) at a word boundary so hyphenated slugs such as `…audit-task-level…` are not flagged; real keys after whitespace, quotes or at line start still are.'
319df352-4d15-4ebd-8e74-20113096861a
```

## Final head `d090ef7d` (two `gh pr update-branch` merges: `ac25ee18` with main a5c30b6d, then `d090ef7d` with main 138e6a72)

```
$ git log -1 --format=%H
d090ef7ddd7c19a47aeaced91c381a7e9775f914
$ git diff origin/main --stat
 scripts/validate-agent-assets.py         |  6 +++---
 tests/unit/test_validate_agent_assets.py | 20 ++++++++++++++++++++
 2 files changed, 23 insertions(+), 3 deletions(-)
$ uv run python -m unittest tests.unit.test_validate_agent_assets 2>&1 | tail -3
Ran 62 tests in 0.540s

OK
$ make unit-test (tail -3)
Ran 703 tests in 162.329s

OK (skipped=1)
$ make validate-agent-assets > log; echo exit=$?   (in the worktree)
uv run --with pyyaml scripts/validate-agent-assets.py
agent asset validation ok
exit=0
$ gh pr checks 245
CodeRabbit	pass
changes	pass
nix	skipping
private-bootstrap (macos-14, client)	pass
private-bootstrap (ubuntu-24.04, client)	pass
private-bootstrap (ubuntu-24.04, server)	pass
public-bootstrap (macos-14, client)	pass
public-bootstrap (ubuntu-24.04, client)	pass
public-bootstrap (ubuntu-24.04, server)	pass
test (macos-14, client)	pass
test (ubuntu-24.04, client)	pass
test (ubuntu-24.04, server)	pass
test (ubuntu-26.04, client)	pass
validate	pass
$ gh api repos/mryfmo/dotfiles/pulls/245 --jq '.mergeable_state'
clean
$ gh api repos/mryfmo/dotfiles/compare/main...fix/secret-scan-sk-boundary
behind_by=0 ahead_by=3
$ Codex: 35d102b7 +1 2026-10-04T02:33:34Z; ac25ee18 +1 2026-10-04T02:46:24Z; d090ef7d +1 2026-10-04T02:52:06Z (pushed 02:49:37Z); no review threads
```

## Revise round 1 (task_rev `sha256:765a7d1864efd8bd7e1a3046ef78f3f284706dc299fb3e8c76d00e823985e175`): commit `0bdf99f7`

```
$ git diff d090ef7d 0bdf99f7 -- scripts/validate-agent-assets.py   (pattern lines)
-        \bghp_[A-Za-z0-9_]{20,}
-        | \bgithub_pat_[A-Za-z0-9_]{20,}
-        | \bsk-[A-Za-z0-9_-]{20,}
+        (?:(?<![A-Za-z0-9_])|(?<=\\[nrt]))ghp_[A-Za-z0-9_]{20,}
+        | (?:(?<![A-Za-z0-9_])|(?<=\\[nrt]))github_pat_[A-Za-z0-9_]{20,}
+        | (?:(?<![A-Za-z0-9_])|(?<=\\[nrt]))sk-[A-Za-z0-9_-]{20,}
$ the three patterns on the task cases (keys built at runtime; JSON via json.dumps)
case                  pre-T91 57885db1          35d102b7 (\b)             branch (lookbehind)       
json \n + sk          flagged                   clean                     flagged                   
json \t + ghp         flagged                   clean                     flagged                   
json \r + github_pat  flagged                   clean                     flagged                   
space + sk            flagged                   flagged                   flagged                   
slug task-level       flagged                   clean                     clean                     
slug dead-code        clean                     clean                     clean                     
$ (scripts/validate-agent-assets.py from 35d102b7) uv run python -m unittest -k json_escaped tests.unit.test_validate_agent_assets
FAIL x9 (one per prefix x escape subtest)
Ran 1 test in 0.012s
FAILED (failures=9)
$ uv run python -m unittest tests.unit.test_validate_agent_assets 2>&1 | tail -2

OK
$ make unit-test (tail -3)
Ran 704 tests in 159.597s

OK (skipped=1)
$ make validate-agent-assets > log; echo exit=$?   (in the worktree)
exit=0
```

### Codex P2 4176019381 on `0bdf99f7` (`\uXXXX` escapes): commit `5fa6f090`, then the update-branch merge `82738d93` with main 8922f13b (T74)

```
$ git diff 0bdf99f7 5fa6f090 -- scripts/validate-agent-assets.py   (pattern lines)
-        (?:(?<![A-Za-z0-9_])|(?<=\\[nrt]))ghp_[A-Za-z0-9_]{20,}
-        | (?:(?<![A-Za-z0-9_])|(?<=\\[nrt]))github_pat_[A-Za-z0-9_]{20,}
-        | (?:(?<![A-Za-z0-9_])|(?<=\\[nrt]))sk-[A-Za-z0-9_-]{20,}
+        (?:(?<![A-Za-z0-9_])|(?<=\\[bfnrt])|(?<=\\u[0-9A-Fa-f]{4}))ghp_[A-Za-z0-9_]{20,}
+        | (?:(?<![A-Za-z0-9_])|(?<=\\[bfnrt])|(?<=\\u[0-9A-Fa-f]{4}))github_pat_[A-Za-z0-9_]{20,}
+        | (?:(?<![A-Za-z0-9_])|(?<=\\[bfnrt])|(?<=\\u[0-9A-Fa-f]{4}))sk-[A-Za-z0-9_-]{20,}
$ the three patterns on JSON escapes before an sk- key built at runtime
case              pre-T91 57885db1        0bdf99f7 ([nrt])        branch (bfnrt+uXXXX)    
\u000a            flagged                 clean                   flagged                 
\u000d            flagged                 clean                   flagged                 
\u0009            flagged                 clean                   flagged                 
\u0020            flagged                 clean                   flagged                 
\b                flagged                 clean                   flagged                 
\f                flagged                 clean                   flagged                 
\n                flagged                 flagged                 flagged                 
slug task-level   flagged                 clean                   clean                   
slug dead-code    clean                   clean                   clean                   
space + key       flagged                 flagged                 flagged                 
$ (scripts/validate-agent-assets.py from 0bdf99f7) uv run python -m unittest -k json_escaped tests.unit.test_validate_agent_assets
Ran 1 test in 0.012s
FAILED (failures=18)
$ uv run python -m unittest tests.unit.test_validate_agent_assets 2>&1 | tail -2  (82738d93)

OK
$ make unit-test (tail -3)   (5fa6f090)
Ran 704 tests in 162.499s

OK (skipped=1)
$ make validate-agent-assets > log; echo exit=$?   (worktree, 5fa6f090)
vaa_exit=0
```

### Codex P2 4176057502 on `82738d93` (TOML `\UXXXXXXXX`): commit `9544155f`, a general escape rule

```
$ git diff 5fa6f090 9544155f -- scripts/validate-agent-assets.py   (pattern lines)
-        (?:(?<![A-Za-z0-9_])|(?<=\\[bfnrt])|(?<=\\u[0-9A-Fa-f]{4}))ghp_[A-Za-z0-9_]{20,}
-        | (?:(?<![A-Za-z0-9_])|(?<=\\[bfnrt])|(?<=\\u[0-9A-Fa-f]{4}))github_pat_[A-Za-z0-9_]{20,}
-        | (?:(?<![A-Za-z0-9_])|(?<=\\[bfnrt])|(?<=\\u[0-9A-Fa-f]{4}))sk-[A-Za-z0-9_-]{20,}
+        (?:(?<![A-Za-z0-9_])|(?<=\\)[A-Za-z0-9]{1,9}?)ghp_[A-Za-z0-9_]{20,}
+        | (?:(?<![A-Za-z0-9_])|(?<=\\)[A-Za-z0-9]{1,9}?)github_pat_[A-Za-z0-9_]{20,}
+        | (?:(?<![A-Za-z0-9_])|(?<=\\)[A-Za-z0-9]{1,9}?)sk-[A-Za-z0-9_-]{20,}
$ patterns compared (keys built at runtime) + branch pattern on the main checkout .orchestration
case              pre-T91 57885db1          5fa6f090 (list)           branch (\ + 1-9 alnum)    
\U0000000A        flagged                   clean                     flagged                   
\x0a              flagged                   clean                     flagged                   
\0                flagged                   clean                     flagged                   
\u000a            flagged                   flagged                   flagged                   
\n                flagged                   flagged                   flagged                   
slug task-level   flagged                   clean                     clean                     
slug dead-code    clean                     clean                     clean                     
space + key       flagged                   flagged                   flagged                   
win path \task-l  flagged                   clean                     flagged                   
branch pattern on the main checkout's .orchestration: 1 file(s) flagged
   .orchestration/tasks/dotfiles-T91-secret-scan-sk-boundary-a01.md
$ (scripts/validate-agent-assets.py from 5fa6f090) uv run python -m unittest -k json_escaped tests.unit.test_validate_agent_assets
Ran 1 test in 0.011s
FAILED (failures=9)
$ uv run python -m unittest tests.unit.test_validate_agent_assets 2>&1 | tail -2
OK
$ make unit-test (tail -3)
Ran 703 tests in 160.995s

OK (skipped=1)
$ make validate-agent-assets > log; echo exit=$?   (worktree)
vaa_exit=0
```

### Codex P2 4176116962 on `9544155f` (masking corrupted the JSON escape): commit `185edb2b`

```
$ git diff 9544155f 185edb2b -- scripts/validate-agent-assets.py   (pattern lines)
-        (?:(?<![A-Za-z0-9_])|(?<=\\)[A-Za-z0-9]{1,9}?)ghp_[A-Za-z0-9_]{20,}
-        | (?:(?<![A-Za-z0-9_])|(?<=\\)[A-Za-z0-9]{1,9}?)github_pat_[A-Za-z0-9_]{20,}
-        | (?:(?<![A-Za-z0-9_])|(?<=\\)[A-Za-z0-9]{1,9}?)sk-[A-Za-z0-9_-]{20,}
+        # A key prefix starts after a non-word character or the start, or right
+        # after an escape sequence (a backslash and 1-9 letters or digits: \n,
+        # \u000a, \U0000000A, \x0a); the zero-width lookbehinds keep the escape
+        # out of the match, so --mask-secrets leaves it intact.
+        (?:(?<![A-Za-z0-9_])|(?<=\\[A-Za-z0-9])|(?<=\\[A-Za-z0-9]{2})|(?<=\\[A-Za-z0-9]{3})|(?<=\\[A-Za-z0-9]{4})|(?<=\\[A-Za-z0-9]{5})|(?<=\\[A-Za-z0-9]{6})|(?<=\\[A-Za-z0-9]{7})|(?<=\\[A-Za-z0-9]{8})|(?<=\\[A-Za-z0-9]{9}))
+        (?:ghp_[A-Za-z0-9_]{20,} | github_pat_[A-Za-z0-9_]{20,} | sk-[A-Za-z0-9_-]{20,})
$ patterns compared, the mask round trip, and the branch pattern on the main checkout .orchestration (keys built at runtime; key text shown as <24 chars>)
scan              pre-T91 57885db1        9544155f (consuming)    branch (zero-width)     
\U0000000A        flagged                 flagged                 flagged                 
\x0a              flagged                 flagged                 flagged                 
\0                flagged                 flagged                 flagged                 
\u000a            flagged                 flagged                 flagged                 
\n                flagged                 flagged                 flagged                 
slug task-level   flagged                 clean                   clean                   
slug dead-code    clean                   clean                   clean                   
space + key       flagged                 flagged                 flagged                 
mask of '{"m": "x\u000a<key>"}' -> still valid JSON?
  pre-T91 57885db1        1 match, valid JSON: {"m": "x\u000a<redacted:secret-pattern>"}
  9544155f (consuming)    1 match, INVALID JSON: {"m": "x\<redacted:secret-pattern>"}
  branch (zero-width)     1 match, valid JSON: {"m": "x\u000a<redacted:secret-pattern>"}
branch pattern on the main checkout's .orchestration: 2 file(s) flagged
   .orchestration/tasks/dotfiles-T91-secret-scan-sk-boundary-a01.md
   .orchestration/validation/dotfiles-T65-agent-stop-gate-a01-audit-1845139e.md
$ (scripts/validate-agent-assets.py from 9544155f) uv run python -m unittest -k masking_keeps tests.unit.test_validate_agent_assets
Ran 1 test in 0.012s
FAILED (failures=3)
$ uv run python -m unittest tests.unit.test_validate_agent_assets 2>&1 | tail -2
OK
$ make unit-test (tail -3)
Ran 704 tests in 160.604s

OK (skipped=1)
$ make validate-agent-assets > log; echo exit=$?   (worktree)
vaa_exit=0
$ matches in .orchestration/validation/dotfiles-T65-agent-stop-gate-a01-audit-1845139e.md (written 13:26 local), shown as first 6 chars + length and the 12 chars before
pre-T91 9 [('sk-lev…27', "'T67-audit-ta'") x3 …]
9544155f 3 [('sk-bou…30', "'secret-scan-'"), ('sk-bou…30', …), ('sk-bou…27', …)]
branch 3 [('sk-bou…30', "'secret-scan-'"), ('sk-bou…30', …), ('sk-bou…27', …)]
```

## CI, mergeable_state, branch and Codex (revise-1 final head `185edb2b`)

```
reviews=0 thumbs=1
pushed=2026-10-04T04:30:23Z polls=10
0bdf99f7b87236e6e827af11e912457809bc5ead	2026-10-04T03:43:24Z
82738d93f1129a723a9e6947b21774f1fff76c69	2026-10-04T03:58:00Z
9544155f07af07194ef36800c2b83ccdbf839d36	2026-10-04T04:15:57Z
chatgpt-codex-connector[bot] +1 2026-10-04T04:32:53Z
CodeRabbit	pass
changes	pass
private-bootstrap (macos-14, client)	pass
private-bootstrap (ubuntu-24.04, client)	pass
private-bootstrap (ubuntu-24.04, server)	pass
public-bootstrap (macos-14, client)	pass
public-bootstrap (ubuntu-24.04, client)	pass
public-bootstrap (ubuntu-24.04, server)	pass
test (macos-14, client)	pass
test (ubuntu-24.04, client)	pass
test (ubuntu-24.04, server)	pass
test (ubuntu-26.04, client)	pass
validate	pass
{
"baseRefOid": "8922f13bc370b2a2144184a4a03518015002e2aa",
"headRefOid": "185edb2b64c4ad9ee43d5f7c54b5b95933bac328",
"mergeStateStatus": "BLOCKED"
}
blocked
behind_by=0 ahead_by=8

$ unresolved review threads
4176019381 **  Recognize Unicode-escaped whitespace before key prefixes**
4176057502 **  Recognize TOML's eight-digit Unicode escapes**
4176116962 **  Keep the JSON escape intact during masking**
```

`blocked` is only these Codex P2 threads, all fixed in this round: 4176019381 `fixed:5fa6f090`, 4176057502 `fixed:9544155f`, 4176116962 `fixed:185edb2b`.

## Revise round 2 (task_rev `sha256:ca9d9fb6920eb789cad953273bc3a121867f632da36d0071b0983aa17de129ab`): commit `ffddc8a7`

```
$ git diff 185edb2b ffddc8a7 -- scripts/validate-agent-assets.py
-        (?:ghp_[A-Za-z0-9_]{20,} | github_pat_[A-Za-z0-9_]{20,} | sk-[A-Za-z0-9_-]{20,})
+        (?:ghp_[A-Za-z0-9_]{20,} | github_pat_[A-Za-z0-9_]{20,}
+           # An sk- key body holds a run of 20+ hyphen-free key characters (an
+           # sk-proj- key after proj-); a hyphenated slug such as
+           # ...-sk-boundary-a01-review-receipt never does.
+           | sk-(?=[A-Za-z0-9_-]*[A-Za-z0-9_]{20})[A-Za-z0-9_-]{20,})
$ (scripts/validate-agent-assets.py from 185edb2b) uv run python -m unittest -k hyphen_free tests.unit.test_validate_agent_assets
Ran 1 test in 0.013s
FAILED (failures=3)   (the three slug subtests; the sk- and sk-proj- keys pass on both)
$ uv run python -m unittest tests.unit.test_validate_agent_assets 2>&1 | tail -2
OK
$ make unit-test (tail -3)
Ran 705 tests in 161.787s

OK (skipped=1)
$ make validate-agent-assets > log; echo exit=$?   (worktree)
vaa_exit=0
$ read-only scan of the main checkout .orchestration with the branch pattern (matches as first 6 chars + length)
branch pattern, read-only scan of the main checkout's .orchestration: 2072 text files, 1 flagged
   .orchestration/tasks/dotfiles-T91-secret-scan-sk-boundary-a01.md ['token …11']
$ that one match, located
line 7 match '<redacted:secret-pattern>'
origin/main pattern on the same file: 7 match(es) incl. the token alternative: True
```

The expected zero is not reachable through the key-prefix change. The only remaining hit is line 7 of the T91 task file itself, the prose `key/password/secret/<redacted:secret-pattern>`, which matches the unchanged `token\s*[:=]\s*["'].+["']` alternative. The task says to keep that alternative as it is, and `origin/main` flags the line too. Rewording that one line of the task file (orchestrator-owned; for example, write the alternatives without a quoted value) makes the scan zero. No key-prefix match remains anywhere in `.orchestration`, including the T65 audit file.

(Note: the two `<redacted:secret-pattern>` spots in this round were the `token` assignment with a quoted ellipsis as its value, the very text being reported. The masker rewrote them so this file passes the scan.)

## CI, mergeable_state, branch and Codex (revise-2 final head `ffddc8a7`)

```
reviews=1 thumbs=0
pushed=2026-10-04T04:47:22Z polls=15
0bdf99f7b87236e6e827af11e912457809bc5ead	2026-10-04T03:43:24Z
82738d93f1129a723a9e6947b21774f1fff76c69	2026-10-04T03:58:00Z
9544155f07af07194ef36800c2b83ccdbf839d36	2026-10-04T04:15:57Z
ffddc8a7779029196d6be50b09594de6f0ce9a9a	2026-10-04T04:51:19Z
{
"id": 4176194976,
"line": 36,
"path": "scripts/validate-agent-assets.py"
}
{
"id": 4176194980,
"line": 31,
"path": "scripts/validate-agent-assets.py"
}
CodeRabbit	pass
changes	pass
private-bootstrap (macos-14, client)	pass
private-bootstrap (ubuntu-24.04, client)	pass
private-bootstrap (ubuntu-24.04, server)	pass
public-bootstrap (macos-14, client)	pass
public-bootstrap (ubuntu-24.04, client)	pass
public-bootstrap (ubuntu-24.04, server)	pass
test (macos-14, client)	pass
test (ubuntu-24.04, client)	pass
test (ubuntu-24.04, server)	pass
test (ubuntu-26.04, client)	pass
validate	pass
{
"baseRefOid": "8922f13bc370b2a2144184a4a03518015002e2aa",
"headRefOid": "ffddc8a7779029196d6be50b09594de6f0ce9a9a",
"mergeStateStatus": "BLOCKED"
}
blocked
behind_by=0 ahead_by=9

$ unresolved review threads
4176194976 **  Preserve scanning of hyphenated opaque `sk-` key bodies**
4176194980 **  Treat hyphen-delimited slug components as non-secret text**
```

## Revise round 3 (task_rev `sha256:c6a530e98e880a3b0ce791a76d73b78778d64d0bc9e0bd7ce4eaf09b5f045618`): commit `2e26ca08`

```
$ git diff ffddc8a7 2e26ca08 -- scripts/validate-agent-assets.py   (pattern line)
-           | sk-(?=[A-Za-z0-9_-]*[A-Za-z0-9_]{20})[A-Za-z0-9_-]{20,})
+           | sk-(?=[A-Za-z0-9_-]{0,64}[A-Za-z0-9_]{20})[A-Za-z0-9_-]{20,})
$ (scripts/validate-agent-assets.py from ffddc8a7) uv run python -m unittest -k linear_time tests.unit.test_validate_agent_assets
AssertionError: 7.876431836979464 not less than 1.0
Ran 1 test in 7.888s
FAILED (failures=1)
ffddc8a7 (unbounded): 64 KB of repeated -sk-a: search=none in 8.086s
branch ({0,64}): 64 KB of repeated -sk-a: search=none in 0.024s
sk-<24>               ffddc8a7 (unbounded): flagged  branch ({0,64}): flagged
sk-proj-<24>          ffddc8a7 (unbounded): flagged  branch ({0,64}): flagged
json \n sk-proj       ffddc8a7 (unbounded): flagged  branch ({0,64}): flagged
slug -audit           ffddc8a7 (unbounded): clean  branch ({0,64}): clean
slug -pr-feedback     ffddc8a7 (unbounded): clean  branch ({0,64}): clean
slug -review-receipt  ffddc8a7 (unbounded): clean  branch ({0,64}): clean
branch pattern via read_scannable_text over the main checkout .orchestration: 2079 scannable files, 0 flagged
T91 validation file scannable: True
$ uv run python -m unittest tests.unit.test_validate_agent_assets 2>&1 | tail -2
OK
$ make unit-test (tail -3)
Ran 706 tests in 160.713s

OK (skipped=1)
$ make validate-agent-assets > log; echo exit=$?   (worktree)
vaa_exit=0
```

**Item 2, NUL bytes.** The two NUL bytes in this file (old lines 145 and 181, both section headings) came from zsh's built-in `echo`. In the headings `(\uXXXX escapes)` and `(TOML \UXXXXXXXX)` it read `\u`/`\U` followed by non-hex text as an escape and wrote a NUL. Both headings are restored to the intended text. This file now has 0 NUL and 0 other control bytes, and `read_scannable_text()` returns its text ("T91 validation file scannable: True" above), so the secret check covers it. Later appends are written with Python, not `echo`.

## Revise-3 final head `1af78d79` (`2e26ca08` plus the update-branch merge of main 06875e4e, T65)

```
$ Codex on 2e26ca08: +1 2026-10-04T05:20:32Z; on 1af78d79 (pushed 2026-10-04T05:28:13Z): +1 2026-10-04T05:31:12Z; no review threads on either
$ uv run python -m unittest tests.unit.test_validate_agent_assets 2>&1 | tail -2   (1af78d79)
OK
$ make unit-test (tail -3)   (1af78d79)
Ran 741 tests in 170.383s

OK (skipped=1)
$ make validate-agent-assets > log; echo exit=$?   (worktree, 1af78d79)
vaa_exit=0
$ gh pr checks 245
CodeRabbit	pass
changes	pass
private-bootstrap (macos-14, client)	pass
private-bootstrap (ubuntu-24.04, client)	pass
private-bootstrap (ubuntu-24.04, server)	pass
public-bootstrap (macos-14, client)	pass
public-bootstrap (ubuntu-24.04, client)	pass
public-bootstrap (ubuntu-24.04, server)	pass
test (macos-14, client)	pass
test (ubuntu-24.04, client)	pass
test (ubuntu-24.04, server)	pass
test (ubuntu-26.04, client)	pass
validate	pass
$ gh api repos/mryfmo/dotfiles/pulls/245 --jq '.head.sha + " " + .mergeable_state'
1af78d7900ef3c42af182bfcfb6ac7bd3371a9b8 clean
$ gh api repos/mryfmo/dotfiles/compare/main...fix/secret-scan-sk-boundary
behind_by=0 ahead_by=11
```
