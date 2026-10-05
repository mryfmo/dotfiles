# T41 validation (dot-ua-graph-refresh-T41-a01)

Section 1 was re-run verbatim from worker-c at PR #212 head c3afc7a. Section 3 is verbatim text captured during the run (JSON re-flowed onto one line).

## 1. Task validation commands

```
$ jq -r .gitCommitHash .ua/meta.json
72b890157078c583f45d71a61ee6eba0df86afb5
exit=0

$ git rev-parse HEAD
c3afc7a664c8e55147f3569c98e76b480fccff59
exit=0

$ git diff --name-only $(jq -r .gitCommitHash .ua/meta.json)..HEAD | head
.ua/fingerprints.json
.ua/knowledge-graph.json
.ua/meta.json
exit=0

$ git -C ~/Workspace/dotfiles/.claude/worktrees/worker-c diff origin/main --stat | tail -3
 .ua/knowledge-graph.json                           | 13863 +++++++++----------
 .ua/meta.json                                      |     6 +-
 4 files changed, 7338 insertions(+), 7243 deletions(-)
exit=0
# NOTE: origin/main advanced to f26d4ec (T42 task file, .orchestration-only) after the branch was cut at 72b8901; the 4th file is that .orchestration path, and the PR's own diff vs its merge-base is exactly the 3 .ua files (see `git show --stat HEAD` below).

$ gh pr checks 212
test (macos-14, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/36561482290/job/109383190365	
test (ubuntu-latest, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/36561482290/job/109383190378	
test (ubuntu-latest, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/36561482290/job/109383190283	
nix	skipping	0	https://github.com/mryfmo/dotfiles/actions/runs/36561482290/job/109383192635	
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/36561482290/job/109383140154	
private-bootstrap (macos-14, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/36561482299/job/109383140264	
private-bootstrap (ubuntu-latest, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/36561482299/job/109383140466	
private-bootstrap (ubuntu-latest, server)	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/36561482299/job/109383140398	
public-bootstrap (macos-14, client)	pass	6m8s	https://github.com/mryfmo/dotfiles/actions/runs/36561482299/job/109383140418	
public-bootstrap (ubuntu-latest, client)	pass	8m42s	https://github.com/mryfmo/dotfiles/actions/runs/36561482299/job/109383140385	
public-bootstrap (ubuntu-latest, server)	pass	7m29s	https://github.com/mryfmo/dotfiles/actions/runs/36561482299/job/109383140422	
validate	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/36561482317/job/109383154041	
exit=0

$ gh pr view 212 --json number,headRefOid,mergeable,state,url
{
  "headRefOid": "c3afc7a664c8e55147f3569c98e76b480fccff59",
  "mergeable": "MERGEABLE",
  "number": 212,
  "state": "OPEN",
  "url": "https://github.com/mryfmo/dotfiles/pull/212"
}
exit=0

```

## 2. Graph checks against the committed graph

```
$ sha256sum ~/Workspace/dotfiles/.orchestration/tasks/dot-ua-graph-refresh-T41-a01.md; git show 72b8901:.orchestration/tasks/dot-ua-graph-refresh-T41-a01.md | sha256sum
05dc8ca7250cd5aa2696f5d6ed2c9d60bdfd4b57be8420489c022b80db4aceb2  ~/Workspace/dotfiles/.orchestration/tasks/dot-ua-graph-refresh-T41-a01.md
05dc8ca7250cd5aa2696f5d6ed2c9d60bdfd4b57be8420489c022b80db4aceb2  -
exit=0

$ node /tmp/claude-1000/-home-moriya-Workspace-dotfiles--claude-worktrees-worker-c/89763728-b428-46b1-9b19-2d786c97de12/scratchpad/ua-core-validate.mjs $HOME/.understand-anything-plugin/packages/core/dist/index.js .ua/knowledge-graph.json
{"success":true,"fatal":null,"nodesIn":844,"nodesOut":844,"edgesIn":1198,"edgesOut":1198,"issueCount":0,"droppedIssues":0,"issueLevels":{}}
exit=0

$ jq '[.nodes[] | select(.lineRange != null and ((.lineRange|type) != "array"))] | length' .ua/knowledge-graph.json
0
exit=0

$ jq -c '{nodes:(.nodes|length),edges:(.edges|length),layers:(.layers|length),tour:(.tour|length)}' .ua/knowledge-graph.json
{"nodes":844,"edges":1198,"layers":9,"tour":15}
exit=0

$ git show 72b8901:.ua/knowledge-graph.json | jq -c '{nodes:(.nodes|length),edges:(.edges|length),layers:(.layers|length),tour:(.tour|length)}'
{"nodes":853,"edges":1219,"layers":9,"tour":15}
exit=0

$ grep -cE '(ghp_[A-Za-z0-9]{20,}|github_pat_|sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|AGE-SECRET-KEY-|-----BEGIN [A-Z ]*PRIVATE KEY|xox[baprs]-)' .ua/knowledge-graph.json
0
exit=1

# NOTE: grep -c exits 1 on zero matches; 0 is the passing result.

$ while IFS='=' read -r k v; do v=${v%\"}; v=${v#\"}; [ ${#v} -ge 12 ] || continue; grep -qF -- "$v" .ua/knowledge-graph.json && echo "hit: $k=$v"; done < <(grep -E '^[A-Z_]+=' home/dot_agents/model-profiles.env); echo scan-done
hit: MODEL_PROFILE_AUDIT_CODEX_ARGS=--profile audit
scan-done
exit=0

# NOTE: the one hit is the non-secret CLI argument '--profile audit' (in the modify_private_audit.config.toml summary); model-profiles.env is tracked in this public repo.

$ git show --stat HEAD | tail -5

 .ua/fingerprints.json    |   639 ++-
 .ua/knowledge-graph.json | 13863 ++++++++++++++++++++++-----------------------
 .ua/meta.json            |     6 +-
 3 files changed, 7338 insertions(+), 7170 deletions(-)
exit=0

$ grep -nE '^\.ua/' .gitignore
17:.ua/intermediate/
18:.ua/tmp/
19:.ua/diff-overlay.json
exit=0

```

## 3. Incremental attempt (captured during the run, verbatim text)

```
$ node ~/.understand-anything-plugin/skills/understand/prepare-incremental.mjs "$PWD" 7b69b1e76bb7cd8896007b7f78b70bc5b8620659
scan-project: filesScanned=361 filteredByIgnore=1671 complexity=large
extract-import-map: filesScanned=361 filesWithImports=13 totalEdges=43
Incremental plan: ARCHITECTURE_UPDATE; analyze=30; delete=0; cosmetic=2; ignored=51; generated=3
exit=0
{"action":"ARCHITECTURE_UPDATE","reason":"30 files have structural changes — architecture re-analysis needed","rerunArchitecture":true,"rerunTour":true,"analyze":30}

$ python3 <skill>/merge-batch-graphs.py "$PWD"   (stderr tail; exit=1)
    unknown: "function:install/ubuntu/common/aws_cli.sh:install_aws_cli" ("install_aws_cli") — Old symbol cannot be mapped uniquely, or source parsing is unavailable/failed
  "install/ubuntu/common/dependencies.sh": nodes 4 -> 4; symbols 3 -> 3
    unknown: "function:install/ubuntu/common/dependencies.sh:run_apt_get" ("run_apt_get") — Old symbol cannot be mapped uniquely, or source parsing is unavailable/failed
    unknown: "function:install/ubuntu/common/dependencies.sh:install_apt_packages" ("install_apt_packages") — Old symbol cannot be mapped uniquely, or source parsing is unavailable/failed
    unknown: "function:install/ubuntu/common/dependencies.sh:uninstall_apt_packages" ("uninstall_apt_packages") — Old symbol cannot be mapped uniquely, or source parsing is unavailable/failed
  "scripts/check-tools.sh": nodes 8 -> 9; symbols 7 -> 8
    unknown: "function:scripts/check-tools.sh:check_command" ("check_command") — Old symbol cannot be mapped uniquely, or source parsing is unavailable/failed
    unknown: "function:scripts/check-tools.sh:private_layer_enabled" ("private_layer_enabled") — Old symbol cannot be mapped uniquely, or source parsing is unavailable/failed
    unknown: "function:scripts/check-tools.sh:check_private_chezmoi" ("check_private_chezmoi") — Old symbol cannot be mapped uniquely, or source parsing is unavailable/failed
    unknown: "function:scripts/check-tools.sh:check_crit_cli" ("check_crit_cli") — Old symbol cannot be mapped uniquely, or source parsing is unavailable/failed
    unknown: "function:scripts/check-tools.sh:check_apparmor_userns" ("check_apparmor_userns") — Old symbol cannot be mapped uniquely, or source parsing is unavailable/failed
    unknown: "function:scripts/check-tools.sh:check_agmsg" ("check_agmsg") — Old symbol cannot be mapped uniquely, or source parsing is unavailable/failed
    unknown: "function:scripts/check-tools.sh:main" ("main") — Old symbol cannot be mapped uniquely, or source parsing is unavailable/failed
  "scripts/generate-agent-configs.py": nodes 19 -> 20; symbols 18 -> 19
  "scripts/lib/installer-pins.sh": nodes 1 -> 1; symbols 0 -> 0
  "scripts/pr-feedback.py": nodes 0 -> 6; symbols 0 -> 5
  "scripts/require-crit-review.py": nodes 9 -> 12; symbols 8 -> 11
  "scripts/validate-agent-assets.py": nodes 33 -> 34; symbols 32 -> 33
  "tests/install/ubuntu/common/dependencies.bats": nodes 1 -> 1; symbols 0 -> 0
  "tests/unit/test_pr_feedback.py": nodes 0 -> 6; symbols 0 -> 5
  "tests/unit/test_require_crit_review.py": nodes 3 -> 3; symbols 2 -> 2
  "tests/unit/test_runtime_health.py": nodes 2 -> 2; symbols 1 -> 1
  "tests/unit/test_validate_agent_assets.py": nodes 4 -> 4; symbols 3 -> 3
Symbol validation blocked publication; baseline not advanced

$ candidate counts (.ua/intermediate/assembled-graph.json of the blocked run)
{"nodes":874,"edges":1318}

$ jq -c ".unresolvedFiles, [.files[]|select(.missing|length>0)|{filePath, missing:(.missing|length), statuses:([.missing[].status]|unique)}]" incremental-symbol-report.json
["install/ubuntu/common/aws_cli.sh","install/ubuntu/common/dependencies.sh","scripts/check-tools.sh"]
[{"filePath":"install/ubuntu/common/aws_cli.sh","missing":3,"statuses":["unknown"]},{"filePath":"install/ubuntu/common/dependencies.sh","missing":3,"statuses":["unknown"]},{"filePath":"scripts/check-tools.sh","missing":7,"statuses":["unknown"]}]

$ per-ID presence of every flagged symbol in the candidate (correct re-run)
     13 present
```

## 4. Full rebuild (captured during the run, verbatim text)

```
$ node <skill>/compute-batches.mjs "$PWD"
Loaded 365 files (216 code).
Info: compute-batches: merged 247 small batches (256 files) into 11 misc batches — singletons and orphans consolidated
Wrote 31 batches (sizes: max=25, min=1) to .../.ua/intermediate/batches.json

$ python3 <skill>/merge-batch-graphs.py "$PWD"   (stderr from Input:, exit=0)
Input: 841 nodes, 1240 edges

Fixed (44 corrections):
    44 × tested_by edges dropped (orphan endpoint or test↔test / prod↔prod pair)

Tested-by linker:
     0 × tested_by edges produced (path-convention supplement, production → test)
    33 × production nodes tagged "tested"

Could not fix (3 issues — needs agent review):
  - Edge function:install/ubuntu/common/apparmor_userns.sh:main → function:install/ubuntu/common/apparmor_userns.sh:skip_reason (calls): dropped, missing target 'function:install/ubuntu/common/apparmor_userns.sh:skip_reason'
  - Edge function:install/ubuntu/common/apparmor_userns.sh:main → function:install/ubuntu/common/apparmor_userns.sh:install_profile (calls): dropped, missing target 'function:install/ubuntu/common/apparmor_userns.sh:install_profile'
  - Edge function:install/ubuntu/common/apparmor_userns.sh:install_profile → function:install/ubuntu/common/apparmor_userns.sh:profile_source (calls): dropped, missing source 'function:install/ubuntu/common/apparmor_userns.sh:install_profile', target 'function:install/ubuntu/common/apparmor_userns.sh:profile_source'

Output: 841 nodes, 1192 edges

Imports edge recovery:
  Recovered 0 `imports` edges from importMap (365 entries scanned)

Written to ~/Workspace/dotfiles/.claude/worktrees/worker-c/.ua/intermediate/assembled-graph.json (729 KB)

$ node .ua/tmp/ua-inline-validate.cjs assembled-graph.json review.json
inline exit=0
{"issues":0,"sample":[],"warnings":52,"stats":{"totalNodes":844,"totalEdges":1198,"totalLayers":9,"tourSteps":15,"nodeTypes":{"file":267,"function":442,"class":36,"service":2,"pipeline":7,"config":49,"document":41},"edgeTypes":{"contains":479,"exports":107,"imports":43,"calls":184,"depends_on":141,"triggers":25,"related":99,"documents":46,"configures":35,"tested_by":39}}}

$ node ua-core-validate.mjs <core> assembled-graph.json   # pre-save
{"success":true,"fatal":null,"nodesIn":844,"nodesOut":844,"edgesIn":1198,"edgesOut":1198,"issueCount":0,"droppedIssues":0,"issueLevels":{}}
core exit=0

$ node <skill>/build-fingerprints.mjs fingerprint-input.json
[json-parser] Failed to parse JSON: Unexpected token '#', "#!/usr/bin"... is not valid JSON
Fingerprints baseline: 365 files
fingerprints exit=0

$ git log --oneline -2
c3afc7a chore(ua): full knowledge-graph rebuild at 72b8901 (T41)
72b8901 chore(orchestration): T41 task - incremental knowledge graph refresh after T37-T39

$ gh pr create ...
https://github.com/mryfmo/dotfiles/pull/212

$ python3 .claude/hooks/contextdb_cli.py memory add --kind decision ...   (full command in the report)
6704a725-799b-4c4b-ad51-d8adec806abc
$ python3 .claude/hooks/contextdb_cli.py memory add --kind failure ...    (full command in the report)
16001714-ab6e-4386-ab29-1915fe73fdf7
```

## 5. Revision 2 — verbatim re-runs at head 7ee3658

```
$ jq -r .gitCommitHash .ua/meta.json
72b890157078c583f45d71a61ee6eba0df86afb5
exit=0

$ git rev-parse HEAD
7ee365860d15146dc3e79f03a2704a0f333d364e
exit=0

$ git diff --name-only $(jq -r .gitCommitHash .ua/meta.json)..HEAD | head
.ua/fingerprints.json
.ua/knowledge-graph.json
.ua/meta.json
exit=0

$ git -C ~/Workspace/dotfiles/.claude/worktrees/worker-c diff origin/main --stat | tail -3
 .ua/knowledge-graph.json                           | 19043 ++++++++++---------
 .ua/meta.json                                      |     6 +-
 4 files changed, 10715 insertions(+), 9046 deletions(-)
exit=0

$ git show --stat HEAD | tail -4

 .ua/fingerprints.json    |   12 +-
 .ua/knowledge-graph.json | 9702 +++++++++++++++++++++++++++-------------------
 2 files changed, 5644 insertions(+), 4070 deletions(-)
exit=0

$ node /tmp/claude-1000/-home-moriya-Workspace-dotfiles--claude-worktrees-worker-c/89763728-b428-46b1-9b19-2d786c97de12/scratchpad/ua-core-validate.mjs $HOME/.understand-anything-plugin/packages/core/dist/index.js .ua/knowledge-graph.json
{"success":true,"fatal":null,"nodesIn":885,"nodesOut":885,"edgesIn":1325,"edgesOut":1325,"issueCount":0,"droppedIssues":0,"issueLevels":{}}
exit=0

$ jq '[.nodes[] | select(.lineRange != null and ((.lineRange|type) != "array"))] | length' .ua/knowledge-graph.json
0
exit=0

$ jq -c '{nodes:(.nodes|length),edges:(.edges|length),layers:(.layers|length),tour:(.tour|length)}' .ua/knowledge-graph.json
{"nodes":885,"edges":1325,"layers":9,"tour":15}
exit=0

$ git show 72b8901:.ua/knowledge-graph.json > /tmp/claude-1000/-home-moriya-Workspace-dotfiles--claude-worktrees-worker-c/89763728-b428-46b1-9b19-2d786c97de12/scratchpad/t41r2/old-graph.json && python3 /tmp/claude-1000/-home-moriya-Workspace-dotfiles--claude-worktrees-worker-c/89763728-b428-46b1-9b19-2d786c97de12/scratchpad/t41r2/compare.py /tmp/claude-1000/-home-moriya-Workspace-dotfiles--claude-worktrees-worker-c/89763728-b428-46b1-9b19-2d786c97de12/scratchpad/t41r2/old-graph.json .ua/knowledge-graph.json /tmp/claude-1000/-home-moriya-Workspace-dotfiles--claude-worktrees-worker-c/89763728-b428-46b1-9b19-2d786c97de12/scratchpad/t41r2/compare-committed.json
files in both: 360 decreased: 0 symbols lost: 0
exit=0

$ git show c3afc7a:.ua/knowledge-graph.json > /tmp/claude-1000/-home-moriya-Workspace-dotfiles--claude-worktrees-worker-c/89763728-b428-46b1-9b19-2d786c97de12/scratchpad/t41r2/rev1-graph.json && python3 /tmp/claude-1000/-home-moriya-Workspace-dotfiles--claude-worktrees-worker-c/89763728-b428-46b1-9b19-2d786c97de12/scratchpad/t41r2/compare.py /tmp/claude-1000/-home-moriya-Workspace-dotfiles--claude-worktrees-worker-c/89763728-b428-46b1-9b19-2d786c97de12/scratchpad/t41r2/old-graph.json /tmp/claude-1000/-home-moriya-Workspace-dotfiles--claude-worktrees-worker-c/89763728-b428-46b1-9b19-2d786c97de12/scratchpad/t41r2/rev1-graph.json /tmp/claude-1000/-home-moriya-Workspace-dotfiles--claude-worktrees-worker-c/89763728-b428-46b1-9b19-2d786c97de12/scratchpad/t41r2/compare-rev1.json
files in both: 360 decreased: 8 symbols lost: 35
.claude/contextdb/contextdb/storage.py: old=19 new=1 defs 7b69b1e=34 72b8901=34 missingIds=18
home/dot_agents/skills/gh-comment-attach-files/scripts/attach_comment_files.py: old=24 new=14 defs 7b69b1e=24 72b8901=24 missingIds=10
home/dot_local/bin/common/executable_agent-fanout: old=2 new=1 defs 7b69b1e=2 72b8901=2 missingIds=1
home/dot_local/bin/server/history.sh: old=1 new=0 defs 7b69b1e=2 72b8901=2 missingIds=1
install/ubuntu/client/docker.sh: old=3 new=2 defs 7b69b1e=6 72b8901=6 missingIds=1
install/ubuntu/client/tailscale.sh: old=2 new=1 defs 7b69b1e=4 72b8901=4 missingIds=1
install/ubuntu/client/zed.sh: old=3 new=2 defs 7b69b1e=5 72b8901=5 missingIds=1
scripts/run_bashcov_unit_test.rb: old=3 new=1 defs 7b69b1e=3 72b8901=3 missingIds=2
exit=0

$ gh pr checks 212
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/36563582920/job/109390018818	
private-bootstrap (macos-14, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/36563582881/job/109390020685	
test (macos-14, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/36563582920/job/109390062677	
test (ubuntu-latest, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/36563582920/job/109390062628	
nix	skipping	0	https://github.com/mryfmo/dotfiles/actions/runs/36563582920/job/109390064517	
private-bootstrap (ubuntu-latest, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/36563582881/job/109390020445	
private-bootstrap (ubuntu-latest, server)	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/36563582881/job/109390020428	
public-bootstrap (macos-14, client)	pass	12m23s	https://github.com/mryfmo/dotfiles/actions/runs/36563582881/job/109390020381	
public-bootstrap (ubuntu-latest, client)	pass	9m29s	https://github.com/mryfmo/dotfiles/actions/runs/36563582881/job/109390020310	
public-bootstrap (ubuntu-latest, server)	pass	7m6s	https://github.com/mryfmo/dotfiles/actions/runs/36563582881/job/109390020057	
test (ubuntu-latest, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/36563582920/job/109390062578	
validate	pass	13s	https://github.com/mryfmo/dotfiles/actions/runs/36563582852/job/109390018780	
exit=0

$ gh pr view 212 --json number,headRefOid,mergeable,state,url
{
  "headRefOid": "7ee365860d15146dc3e79f03a2704a0f333d364e",
  "mergeable": "MERGEABLE",
  "number": 212,
  "state": "OPEN",
  "url": "https://github.com/mryfmo/dotfiles/pull/212"
}
exit=0

```

### Comparison script (scratchpad t41r2/compare.py, verbatim)

```python
import json, re, subprocess, sys
old = json.load(open(sys.argv[1])); new = json.load(open(sys.argv[2])); out = sys.argv[3]
SYM = {"function", "class", "method"}
def per_file(g):
    files, syms = set(), {}
    for n in g["nodes"]:
        fp = n.get("filePath")
        if not fp: continue
        if n["type"] in SYM: syms.setdefault(fp, set()).add(n["id"])
        else: files.add(fp)
    return files | set(syms), syms
of, os_ = per_file(old); nf, ns = per_file(new)
PY = re.compile(r"^\s*(async\s+def|def|class)\s+\w+")
RB = re.compile(r"^\s*(def|class|module)\s+\S+")
SH = re.compile(r"^\s*(function\s+[\w:.-]+|[\w:.-]+\s*\(\)\s*[{(]?)\s*$|^\s*(function\s+[\w:.-]+|[\w:.-]+\s*\(\))\s*[{(]")
def lang(path, text):
    first = text.split("\n", 1)[0]
    if path.endswith(".py") or "python" in first: return PY
    if path.endswith(".rb") or "ruby" in first: return RB
    if path.endswith((".sh", ".bash", ".zsh", ".bats")) or "bash" in first or "/sh" in first or "zsh" in first or path.endswith(".tmpl"): return SH
    return None
def defs(rev, path):
    r = subprocess.run(["git", "show", f"{rev}:{path}"], capture_output=True, text=True, errors="replace")
    if r.returncode: return None
    rx = lang(path, r.stdout)
    return sum(1 for l in r.stdout.splitlines() if rx and rx.search(l)) if rx else "-"
rows = []
for fp in sorted(of & nf):
    o, n = len(os_.get(fp, ())), len(ns.get(fp, ()))
    rows.append({"file": fp, "old": o, "new": n, "defs_7b69b1e": defs("7b69b1e", fp), "defs_72b8901": defs("72b8901", fp),
                 "missing_ids": sorted(os_.get(fp, set()) - ns.get(fp, set()))})
json.dump(rows, open(out, "w"), indent=1)
dec = [r for r in rows if r["new"] < r["old"]]
print("files in both:", len(rows), "decreased:", len(dec), "symbols lost:", sum(r["old"]-r["new"] for r in dec))
for r in dec: print(f'{r["file"]}: old={r["old"]} new={r["new"]} defs 7b69b1e={r["defs_7b69b1e"]} 72b8901={r["defs_72b8901"]} missingIds={len(r["missing_ids"])}')
```

"def-like lines" = lines matching the per-language definition regex in the script (Python `def`/`class`, Ruby `def`/`class`/`module`, shell `function name` / `name()` including subshell bodies), counted with `git show <rev>:<file>`; `-` = no definition grammar for that file type.

### Per-file symbol nodes for EVERY file present in both graphs (360 files)

| file | old symbol nodes (graph at 72b8901, meta 7b69b1e) | rev1 symbol nodes (c3afc7a) | rev2 symbol nodes (7ee3658) | def-like lines 7b69b1e | def-like lines 72b8901 | rev2 >= old |
|---|---|---|---|---|---|---|
| `.chezmoiroot` | 0 | 0 | 0 | - | - | yes |
| `.claude/contextdb/config.json` | 0 | 0 | 0 | - | - | yes |
| `.claude/contextdb/contextdb/__init__.py` | 0 | 0 | 0 | 0 | 0 | yes |
| `.claude/contextdb/contextdb/cli.py` | 4 | 4 | 4 | 9 | 9 | yes |
| `.claude/contextdb/contextdb/config.py` | 3 | 3 | 3 | 6 | 6 | yes |
| `.claude/contextdb/contextdb/hook.py` | 2 | 2 | 2 | 2 | 2 | yes |
| `.claude/contextdb/contextdb/memory.py` | 3 | 3 | 3 | 5 | 5 | yes |
| `.claude/contextdb/contextdb/normalize.py` | 5 | 5 | 5 | 6 | 6 | yes |
| `.claude/contextdb/contextdb/paths.py` | 4 | 4 | 4 | 5 | 5 | yes |
| `.claude/contextdb/contextdb/probe.py` | 1 | 1 | 1 | 1 | 1 | yes |
| `.claude/contextdb/contextdb/recall.py` | 5 | 5 | 5 | 8 | 8 | yes |
| `.claude/contextdb/contextdb/recover_hook.py` | 3 | 3 | 3 | 3 | 3 | yes |
| `.claude/contextdb/contextdb/recovery.py` | 4 | 4 | 4 | 4 | 4 | yes |
| `.claude/contextdb/contextdb/redaction.py` | 6 | 6 | 6 | 10 | 10 | yes |
| `.claude/contextdb/contextdb/semantic.py` | 4 | 4 | 4 | 4 | 4 | yes |
| `.claude/contextdb/contextdb/spool.py` | 6 | 6 | 6 | 12 | 12 | yes |
| `.claude/contextdb/contextdb/storage.py` | 19 | 1 | 25 | 34 | 34 | yes |
| `.claude/contextdb/contextdb/util.py` | 19 | 19 | 19 | 20 | 20 | yes |
| `.claude/contextdb/health/.gitkeep` | 0 | 0 | 0 | - | - | yes |
| `.claude/contextdb/spool/incoming/.gitkeep` | 0 | 0 | 0 | - | - | yes |
| `.claude/contextdb/spool/quarantine/.gitkeep` | 0 | 0 | 0 | - | - | yes |
| `.claude/contextdb/state/.gitkeep` | 0 | 0 | 0 | - | - | yes |
| `.claude/hooks/contextdb_cli.py` | 0 | 0 | 0 | 0 | 0 | yes |
| `.claude/hooks/contextdb_hook.py` | 0 | 0 | 0 | 0 | 0 | yes |
| `.claude/hooks/contextdb_recover.py` | 0 | 0 | 0 | 0 | 0 | yes |
| `.claude/hooks/query_log.py` | 0 | 0 | 0 | 0 | 0 | yes |
| `.claude/settings.json` | 0 | 0 | 0 | - | - | yes |
| `.github/copilot-instructions.md` | 0 | 0 | 0 | - | - | yes |
| `.github/funding.yaml` | 0 | 0 | 0 | - | - | yes |
| `.github/workflows/agent-assets.yml` | 0 | 0 | 0 | - | - | yes |
| `.github/workflows/docs.yml` | 0 | 0 | 0 | - | - | yes |
| `.github/workflows/macos.yaml` | 0 | 0 | 0 | - | - | yes |
| `.github/workflows/remote.yaml` | 0 | 0 | 0 | - | - | yes |
| `.github/workflows/test.yaml` | 0 | 0 | 0 | - | - | yes |
| `.github/workflows/ubuntu.yaml` | 0 | 0 | 0 | - | - | yes |
| `.simplecov` | 0 | 0 | 0 | - | - | yes |
| `.ua/config.json` | 0 | 0 | 0 | - | - | yes |
| `.ua/fingerprints.json` | 0 | 0 | 0 | - | - | yes |
| `.ua/knowledge-graph.json` | 0 | 0 | 0 | - | - | yes |
| `.ua/meta.json` | 0 | 0 | 0 | - | - | yes |
| `AGENTS.md` | 0 | 0 | 0 | - | - | yes |
| `CLAUDE.md` | 0 | 0 | 0 | - | - | yes |
| `Dockerfile` | 0 | 0 | 0 | - | - | yes |
| `Makefile` | 0 | 0 | 0 | - | - | yes |
| `README.md` | 0 | 0 | 0 | - | - | yes |
| `codecov.yml` | 0 | 0 | 0 | - | - | yes |
| `docs/assets/stylesheets/extra.css` | 0 | 0 | 0 | - | - | yes |
| `docs/plans/nix-first-architecture.md` | 0 | 0 | 0 | - | - | yes |
| `docs/plans/nix-migration.md` | 0 | 0 | 0 | - | - | yes |
| `docs/verification/acceptance/005.md` | 0 | 0 | 0 | - | - | yes |
| `flake.nix` | 0 | 0 | 0 | - | - | yes |
| `home/.chezmoi.yaml.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/.chezmoiexternal.yaml.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/.chezmoiignore` | 0 | 0 | 0 | - | - | yes |
| `home/.chezmoiremove` | 0 | 0 | 0 | - | - | yes |
| `home/.chezmoiscripts/common/run_once_after_01-setup-chezmoi-private.sh.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/.chezmoiscripts/common/run_once_after_02-install-mise.sh.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/.chezmoiscripts/common/run_once_after_03-install-sheldon.sh.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/.chezmoiscripts/common/run_once_after_06-install-agent-assets.sh.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/.chezmoiscripts/common/run_once_after_99-install-gh-extensions.sh.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/.chezmoiscripts/common/run_once_before_01-decrypt-private-key.sh.tmpl` | 1 | 1 | 1 | 3 | 3 | yes |
| `home/.chezmoiscripts/macos/run_once_04-install-ghostty.sh.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/.chezmoiscripts/macos/run_once_10-install-docker.sh.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/.chezmoiscripts/macos/run_once_99-install-defaults.sh.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/.chezmoiscripts/macos/run_once_after_50-install-misc.sh.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/.chezmoiscripts/macos/run_once_before_01-prepare-system.sh.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/.chezmoiscripts/macos/run_once_before_02-install-command-line-tool.sh.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/.chezmoiscripts/macos/run_once_before_03-install-brew.sh.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/.chezmoiscripts/macos/run_once_before_50-install-dependencies.sh.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/.chezmoiscripts/ubuntu/run_once_00-setup-ssh.sh.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/.chezmoiscripts/ubuntu/run_once_10-install-docker.sh.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/.chezmoiscripts/ubuntu/run_once_10-install-starship.sh.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/.chezmoiscripts/ubuntu/run_once_50-client-install-misc.sh.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/.chezmoiscripts/ubuntu/run_once_50-server-docker-ssh.sh.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/.chezmoiscripts/ubuntu/run_once_50-server-install-mics.sh.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/.chezmoiscripts/ubuntu/run_once_50-server-setup-timezone.sh.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/.chezmoiscripts/ubuntu/run_once_50-setup-locale.sh.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/.chezmoiscripts/ubuntu/run_once_51-client-default-shell.sh.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/.chezmoiscripts/ubuntu/run_once_52-client-install-zed.sh.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/.chezmoiscripts/ubuntu/run_once_53-client-install-tailscale.sh.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/.chezmoiscripts/ubuntu/run_once_99-client-gnome-defaults.sh.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/.chezmoiscripts/ubuntu/run_once_after_04-install-aws-cli.sh.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/.chezmoiscripts/ubuntu/run_once_before_50-common-dependencies.sh.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/.chezmoiscripts/ubuntu/run_onchange_after_07-apparmor-bwrap-userns.sh.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/.chezmoiscripts/ubuntu/run_onchange_after_60-enable-usage-snapshot-timer.sh.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/.chezmoitemplates/chezmoiexternal.d/common.yaml.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/.chezmoitemplates/chezmoiexternal.d/macos.yaml.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/.chezmoitemplates/chezmoiexternal.d/ubuntu.yaml.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/.chezmoitemplates/chezmoiignore.d/common` | 0 | 0 | 0 | - | - | yes |
| `home/.chezmoitemplates/chezmoiignore.d/macos` | 0 | 0 | 0 | - | - | yes |
| `home/.chezmoitemplates/chezmoiignore.d/ubuntu/client` | 0 | 0 | 0 | - | - | yes |
| `home/.chezmoitemplates/chezmoiignore.d/ubuntu/common` | 0 | 0 | 0 | - | - | yes |
| `home/.chezmoitemplates/chezmoiignore.d/ubuntu/server` | 0 | 0 | 0 | - | - | yes |
| `home/.chezmoitemplates/claude-settings-managed.json` | 0 | 0 | 0 | - | - | yes |
| `home/.chezmoitemplates/codex-config-managed.toml` | 0 | 0 | 0 | - | - | yes |
| `home/.key.txt.age` | 0 | 0 | 0 | - | - | yes |
| `home/Library/LaunchAgents/com.mryfmo.dotfiles.usage-snapshot.plist.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/dot_agents/README.md` | 0 | 0 | 0 | - | - | yes |
| `home/dot_agents/agent-config.yaml` | 0 | 0 | 0 | - | - | yes |
| `home/dot_agents/model-profiles.env` | 0 | 0 | 0 | - | - | yes |
| `home/dot_agents/permgate-policy.yaml` | 0 | 0 | 0 | - | - | yes |
| `home/dot_agents/plugins/create_marketplace.json` | 0 | 0 | 0 | - | - | yes |
| `home/dot_agents/plugins/mryfmo-dev-workflows/.codex-plugin/plugin.json` | 0 | 0 | 0 | - | - | yes |
| `home/dot_agents/skills/agmsg-orchestration/SKILL.md` | 0 | 0 | 0 | - | - | yes |
| `home/dot_agents/skills/convert-to-transformers/SKILL.md` | 0 | 0 | 0 | - | - | yes |
| `home/dot_agents/skills/convert-to-transformers/references/common-pitfalls.md` | 0 | 0 | 0 | - | - | yes |
| `home/dot_agents/skills/convert-to-transformers/references/learnings.md` | 0 | 0 | 0 | - | - | yes |
| `home/dot_agents/skills/gh-comment-attach-files/SKILL.md` | 0 | 0 | 0 | - | - | yes |
| `home/dot_agents/skills/gh-comment-attach-files/agents/openai.yaml` | 0 | 0 | 0 | - | - | yes |
| `home/dot_agents/skills/gh-comment-attach-files/scripts/attach_comment_files.py` | 24 | 14 | 24 | 24 | 24 | yes |
| `home/dot_agents/skills/gh-first-workflow/SKILL.md` | 0 | 0 | 0 | - | - | yes |
| `home/dot_agents/skills/gh-first-workflow/agents/openai.yaml` | 0 | 0 | 0 | - | - | yes |
| `home/dot_agents/skills/gh-first-workflow/references/gh-git-rules.md` | 0 | 0 | 0 | - | - | yes |
| `home/dot_agents/skills/humanizer-ja/SKILL.md` | 0 | 0 | 0 | - | - | yes |
| `home/dot_agents/skills/humanizer-ja/agents/openai.yaml` | 0 | 0 | 0 | - | - | yes |
| `home/dot_agents/skills/humanizer-ja/references/ai-patterns-ja.md` | 0 | 0 | 0 | - | - | yes |
| `home/dot_agents/skills/python-uv-workflow/SKILL.md` | 0 | 0 | 0 | - | - | yes |
| `home/dot_agents/skills/python-uv-workflow/agents/openai.yaml` | 0 | 0 | 0 | - | - | yes |
| `home/dot_agents/skills/python-uv-workflow/references/python-uv-rules.md` | 0 | 0 | 0 | - | - | yes |
| `home/dot_agents/skills/shdoc-shell-docs/SKILL.md` | 0 | 0 | 0 | - | - | yes |
| `home/dot_agents/skills/shdoc-shell-docs/agents/openai.yaml` | 0 | 0 | 0 | - | - | yes |
| `home/dot_agents/skills/shdoc-shell-docs/references/shdoc-rules.md` | 0 | 0 | 0 | - | - | yes |
| `home/dot_bash/client/bashrc` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/dot_bash/server/bashrc` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/dot_ccstatusline/settings.json` | 0 | 0 | 0 | - | - | yes |
| `home/dot_claude/agents/express-explorer.md` | 0 | 0 | 0 | - | - | yes |
| `home/dot_claude/commands/commit.md` | 0 | 0 | 0 | - | - | yes |
| `home/dot_claude/hooks/executable_enforce-uv.sh` | 8 | 8 | 8 | 8 | 8 | yes |
| `home/dot_claude/hooks/executable_format-edited-files.py` | 2 | 2 | 2 | 3 | 3 | yes |
| `home/dot_claude/modify_private_settings.json` | 5 | 7 | 7 | 12 | 12 | yes |
| `home/dot_claude/private_mcp.json.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/dot_claude/rules/symlink_agmsg-orchestration.md.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/dot_claude/rules/symlink_ask-user-question.md.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/dot_claude/rules/symlink_compactiondb.md.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/dot_claude/rules/symlink_crit-review.md.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/dot_claude/rules/symlink_gpu.md.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/dot_claude/rules/symlink_latex.md.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/dot_claude/rules/symlink_model-selection.md.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/dot_claude/rules/symlink_ponytail.md.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/dot_claude/rules/symlink_python.md.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/dot_claude/rules/symlink_understand-anything.md.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/dot_claude/skills/agmsg-orchestration/symlink_SKILL.md.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/dot_claude/skills/convert-to-transformers/references/symlink_common-pitfalls.md.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/dot_claude/skills/convert-to-transformers/references/symlink_learnings.md.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/dot_claude/skills/convert-to-transformers/symlink_SKILL.md.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/dot_claude/skills/gh-comment-attach-files/agents/symlink_openai.yaml.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/dot_claude/skills/gh-comment-attach-files/scripts/symlink_attach_comment_files.py.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/dot_claude/skills/gh-comment-attach-files/symlink_SKILL.md.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/dot_claude/skills/gh-first-workflow/agents/symlink_openai.yaml.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/dot_claude/skills/gh-first-workflow/references/symlink_gh-git-rules.md.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/dot_claude/skills/gh-first-workflow/symlink_SKILL.md.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/dot_claude/skills/humanizer-ja/agents/symlink_openai.yaml.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/dot_claude/skills/humanizer-ja/references/symlink_ai-patterns-ja.md.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/dot_claude/skills/humanizer-ja/symlink_SKILL.md.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/dot_claude/skills/python-uv-workflow/agents/symlink_openai.yaml.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/dot_claude/skills/python-uv-workflow/references/symlink_python-uv-rules.md.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/dot_claude/skills/python-uv-workflow/symlink_SKILL.md.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/dot_claude/skills/shdoc-shell-docs/agents/symlink_openai.yaml.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/dot_claude/skills/shdoc-shell-docs/references/symlink_shdoc-rules.md.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/dot_claude/skills/shdoc-shell-docs/symlink_SKILL.md.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/dot_codex/modify_private_adh.config.toml` | 0 | 0 | 0 | 7 | 7 | yes |
| `home/dot_codex/modify_private_audit.config.toml` | 0 | 0 | 0 | 7 | 7 | yes |
| `home/dot_codex/modify_private_config.toml` | 0 | 0 | 0 | 10 | 10 | yes |
| `home/dot_codex/modify_private_deep.config.toml` | 0 | 0 | 0 | 7 | 7 | yes |
| `home/dot_codex/modify_private_express.config.toml` | 0 | 0 | 0 | 6 | 6 | yes |
| `home/dot_codex/modify_private_review.config.toml` | 0 | 0 | 0 | 6 | 6 | yes |
| `home/dot_codex/modify_private_security.config.toml` | 0 | 0 | 0 | 7 | 7 | yes |
| `home/dot_codex/modify_private_standard.config.toml` | 0 | 0 | 0 | 7 | 7 | yes |
| `home/dot_codex/symlink_AGENTS.md.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/dot_config/alias/client.sh` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/dot_config/alias/common.sh` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/dot_config/alias/server.sh` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/dot_config/ccstatusline/symlink_settings.json.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/dot_config/claude/rules/agmsg-orchestration.md` | 0 | 0 | 0 | - | - | yes |
| `home/dot_config/claude/rules/ask-user-question.md` | 0 | 0 | 0 | - | - | yes |
| `home/dot_config/claude/rules/compactiondb.md` | 0 | 0 | 0 | - | - | yes |
| `home/dot_config/claude/rules/crit-review.md` | 0 | 0 | 0 | - | - | yes |
| `home/dot_config/claude/rules/gpu.md` | 0 | 0 | 0 | - | - | yes |
| `home/dot_config/claude/rules/latex.md` | 0 | 0 | 0 | - | - | yes |
| `home/dot_config/claude/rules/model-selection.md` | 0 | 0 | 0 | - | - | yes |
| `home/dot_config/claude/rules/ponytail.md` | 0 | 0 | 0 | - | - | yes |
| `home/dot_config/claude/rules/python.md` | 0 | 0 | 0 | - | - | yes |
| `home/dot_config/claude/rules/understand-anything.md` | 0 | 0 | 0 | - | - | yes |
| `home/dot_config/codex/AGENTS.md` | 0 | 0 | 0 | - | - | yes |
| `home/dot_config/ghostty/config` | 0 | 0 | 0 | - | - | yes |
| `home/dot_config/git/config.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/dot_config/git/ignore` | 0 | 0 | 0 | - | - | yes |
| `home/dot_config/gwq/config.toml` | 0 | 0 | 0 | - | - | yes |
| `home/dot_config/herdr/config.toml` | 0 | 0 | 0 | - | - | yes |
| `home/dot_config/herdr/plugins/config/herdr-file-viewer/config.toml` | 0 | 0 | 0 | - | - | yes |
| `home/dot_config/mise/config.toml.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/dot_config/mise/mise.lock.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/dot_config/powerlevel10k/p10k.zsh` | 2 | 2 | 2 | 5 | 5 | yes |
| `home/dot_config/sheldon/plugin_sources/client/common.toml` | 0 | 0 | 0 | - | - | yes |
| `home/dot_config/sheldon/plugin_sources/client/macos.toml` | 0 | 0 | 0 | - | - | yes |
| `home/dot_config/sheldon/plugin_sources/client/ubuntu.toml` | 0 | 0 | 0 | - | - | yes |
| `home/dot_config/sheldon/plugin_sources/common.toml` | 0 | 0 | 0 | - | - | yes |
| `home/dot_config/sheldon/plugin_sources/server.toml` | 0 | 0 | 0 | - | - | yes |
| `home/dot_config/sheldon/plugins.toml.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/dot_config/starship.toml` | 0 | 0 | 0 | - | - | yes |
| `home/dot_config/systemd/user/usage-snapshot.service.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/dot_config/systemd/user/usage-snapshot.timer.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/dot_config/tango.yml` | 0 | 0 | 0 | - | - | yes |
| `home/dot_config/uv/uv.toml` | 0 | 0 | 0 | - | - | yes |
| `home/dot_config/yazi/yazi.toml` | 0 | 0 | 0 | - | - | yes |
| `home/dot_config/zed/keymap.json` | 0 | 0 | 0 | - | - | yes |
| `home/dot_config/zed/settings.json` | 0 | 0 | 0 | - | - | yes |
| `home/dot_config/zsh/plugins/chezmoi-notify/chezmoi-notify.plugin.zsh` | 1 | 1 | 1 | 1 | 1 | yes |
| `home/dot_local/bin/common/executable_agent-fanout` | 2 | 1 | 2 | 2 | 2 | yes |
| `home/dot_local/bin/common/executable_agent-session-staleness` | 8 | 8 | 8 | 13 | 13 | yes |
| `home/dot_local/bin/common/executable_agmsg-dispatch` | 1 | 1 | 1 | 4 | 4 | yes |
| `home/dot_local/bin/common/executable_cdgwq` | 0 | 0 | 0 | 1 | 1 | yes |
| `home/dot_local/bin/common/executable_cdw` | 1 | 1 | 1 | 1 | 1 | yes |
| `home/dot_local/bin/common/executable_chezmoi-cd` | 0 | 0 | 0 | 1 | 1 | yes |
| `home/dot_local/bin/common/executable_compactiondb-install` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/dot_local/bin/common/executable_contextdb-codex-notify` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/dot_local/bin/common/executable_dev` | 1 | 1 | 1 | 2 | 2 | yes |
| `home/dot_local/bin/common/executable_fgc` | 0 | 0 | 0 | 1 | 1 | yes |
| `home/dot_local/bin/common/executable_git-delete-merged-branches` | 1 | 1 | 1 | 3 | 3 | yes |
| `home/dot_local/bin/common/executable_herdr-agents` | 34 | 34 | 34 | 52 | 52 | yes |
| `home/dot_local/bin/common/executable_herdr-session` | 0 | 0 | 0 | 1 | 1 | yes |
| `home/dot_local/bin/common/executable_permgate` | 16 | 16 | 16 | - | - | yes |
| `home/dot_local/bin/common/executable_provision-machine-key` | 2 | 2 | 2 | 4 | 4 | yes |
| `home/dot_local/bin/common/executable_remove-agent-asset` | 11 | 11 | 11 | 21 | 21 | yes |
| `home/dot_local/bin/common/executable_setup-gh` | 2 | 2 | 2 | 5 | 5 | yes |
| `home/dot_local/bin/common/executable_setup-gpg` | 1 | 1 | 1 | 3 | 3 | yes |
| `home/dot_local/bin/common/executable_setup-python-env` | 0 | 0 | 0 | 3 | 3 | yes |
| `home/dot_local/bin/common/executable_uv-format` | 0 | 0 | 0 | 1 | 1 | yes |
| `home/dot_local/bin/server/cache.sh` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/dot_local/bin/server/cuda.sh` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/dot_local/bin/server/history.sh` | 1 | 0 | 1 | 2 | 2 | yes |
| `home/dot_local/bin/server/ssh_agent.sh` | 1 | 1 | 1 | 1 | 1 | yes |
| `home/dot_local/share/aws-cli-keys/aws-cli-public-key.asc` | 0 | 0 | 0 | - | - | yes |
| `home/dot_mise/config.toml` | 0 | 0 | 0 | - | - | yes |
| `home/dot_npmrc` | 0 | 0 | 0 | - | - | yes |
| `home/dot_profile` | 0 | 0 | 0 | - | - | yes |
| `home/dot_vimrc` | 0 | 0 | 0 | - | - | yes |
| `home/dot_zprofile` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/dot_zshenv` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/dot_zshrc` | 0 | 0 | 0 | 2 | 2 | yes |
| `home/private_dot_gnupg/gpg-agent.conf.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `home/private_dot_ssh/private_config` | 0 | 0 | 0 | - | - | yes |
| `home/symlink_dot_bashrc.tmpl` | 0 | 0 | 0 | 0 | 0 | yes |
| `install/common/chezmoi_private.sh` | 1 | 1 | 1 | 3 | 3 | yes |
| `install/common/gh_extensions.sh` | 1 | 1 | 1 | 3 | 3 | yes |
| `install/common/mise.sh` | 4 | 4 | 4 | 8 | 8 | yes |
| `install/common/sheldon.sh` | 1 | 1 | 1 | 3 | 3 | yes |
| `install/macos/arm64/prepare_arm64_system.sh` | 0 | 0 | 0 | 2 | 2 | yes |
| `install/macos/arm64/run.sh` | 0 | 0 | 0 | 1 | 1 | yes |
| `install/macos/common/brew.sh` | 1 | 1 | 1 | 4 | 4 | yes |
| `install/macos/common/command_line_tool.sh` | 1 | 1 | 1 | 2 | 2 | yes |
| `install/macos/common/defaults.sh` | 7 | 7 | 7 | 16 | 16 | yes |
| `install/macos/common/dependencies.sh` | 1 | 1 | 1 | 3 | 3 | yes |
| `install/macos/common/docker.sh` | 0 | 0 | 0 | 3 | 3 | yes |
| `install/macos/common/ghostty.sh` | 0 | 0 | 0 | 4 | 4 | yes |
| `install/macos/common/misc.sh` | 2 | 2 | 2 | 5 | 5 | yes |
| `install/ubuntu/client/default_shell.sh` | 1 | 1 | 1 | 1 | 1 | yes |
| `install/ubuntu/client/docker.sh` | 3 | 2 | 3 | 6 | 6 | yes |
| `install/ubuntu/client/ghostty.sh` | 0 | 0 | 0 | 5 | 5 | yes |
| `install/ubuntu/client/gnome_settings.sh` | 1 | 1 | 1 | 9 | 9 | yes |
| `install/ubuntu/client/misc.sh` | 0 | 0 | 0 | 4 | 4 | yes |
| `install/ubuntu/client/tailscale.sh` | 2 | 1 | 2 | 4 | 4 | yes |
| `install/ubuntu/client/zed.sh` | 3 | 2 | 3 | 5 | 5 | yes |
| `install/ubuntu/common/apparmor/bwrap-userns` | 0 | 0 | 0 | - | - | yes |
| `install/ubuntu/common/apparmor_userns.sh` | 1 | 4 | 4 | 4 | 4 | yes |
| `install/ubuntu/common/aws_cli.sh` | 3 | 3 | 3 | 5 | 5 | yes |
| `install/ubuntu/common/dependencies.sh` | 3 | 3 | 3 | 4 | 4 | yes |
| `install/ubuntu/common/setup_locale.sh` | 1 | 1 | 1 | 1 | 1 | yes |
| `install/ubuntu/common/ssh.sh` | 0 | 0 | 0 | 4 | 4 | yes |
| `install/ubuntu/server/misc.sh` | 0 | 0 | 0 | 4 | 4 | yes |
| `install/ubuntu/server/setup_timezone.sh` | 0 | 0 | 0 | 1 | 1 | yes |
| `install/ubuntu/server/ssh_server.sh` | 2 | 2 | 2 | 5 | 5 | yes |
| `install/ubuntu/server/starship.sh` | 2 | 2 | 2 | 4 | 4 | yes |
| `mise.toml` | 0 | 0 | 0 | - | - | yes |
| `mkdocs.yml` | 0 | 0 | 0 | - | - | yes |
| `nix/home-manager/default.nix` | 0 | 0 | 0 | - | - | yes |
| `nix/nix-darwin/default.nix` | 0 | 0 | 0 | - | - | yes |
| `nix/shared/packages.nix` | 0 | 0 | 0 | - | - | yes |
| `plans/001-contain-starship-cleanup.md` | 0 | 0 | 0 | - | - | yes |
| `plans/002-make-review-evidence-non-vacuous.md` | 0 | 0 | 0 | - | - | yes |
| `plans/003-make-bootstrap-safe-and-publicly-testable.md` | 0 | 0 | 0 | - | - | yes |
| `plans/004-harden-and-lock-the-supply-chain.md` | 0 | 0 | 0 | - | - | yes |
| `plans/005-make-runtime-health-and-verification-truthful.md` | 0 | 0 | 0 | - | - | yes |
| `plans/README.md` | 0 | 0 | 0 | - | - | yes |
| `renovate.json` | 0 | 0 | 0 | - | - | yes |
| `scripts/check-agent-runtime.py` | 17 | 17 | 17 | 37 | 37 | yes |
| `scripts/check-statusline-tools.py` | 2 | 2 | 2 | 3 | 3 | yes |
| `scripts/check-tools.sh` | 7 | 8 | 8 | 13 | 14 | yes |
| `scripts/generate-agent-configs.py` | 18 | 19 | 19 | 42 | 43 | yes |
| `scripts/generate-docs.sh` | 24 | 24 | 24 | 34 | 34 | yes |
| `scripts/lib/asset-manifest.sh` | 2 | 2 | 2 | 5 | 5 | yes |
| `scripts/lib/installer-pins.sh` | 0 | 0 | 0 | 0 | 0 | yes |
| `scripts/refresh-mkdocs-toc.py` | 0 | 0 | 0 | 1 | 1 | yes |
| `scripts/require-crit-review.py` | 8 | 11 | 11 | 15 | 21 | yes |
| `scripts/run_bashcov_unit_test.rb` | 3 | 1 | 3 | 3 | 3 | yes |
| `scripts/run_benchmark.sh` | 4 | 4 | 4 | 8 | 8 | yes |
| `scripts/run_unit_test.sh` | 2 | 2 | 2 | 4 | 4 | yes |
| `scripts/update-agent-assets.sh` | 30 | 30 | 30 | 41 | 41 | yes |
| `scripts/upgrade-tools.sh` | 22 | 22 | 22 | 35 | 35 | yes |
| `scripts/usage-report.py` | 10 | 10 | 10 | 16 | 16 | yes |
| `scripts/usage-snapshot.sh` | 0 | 0 | 0 | 0 | 0 | yes |
| `scripts/validate-agent-assets.py` | 32 | 33 | 33 | 41 | 42 | yes |
| `setup.sh` | 12 | 12 | 12 | 25 | 25 | yes |
| `tests/files/common.bats` | 0 | 0 | 0 | 0 | 0 | yes |
| `tests/files/helpers.bash` | 1 | 1 | 1 | 5 | 5 | yes |
| `tests/files/macos.bats` | 0 | 0 | 0 | 1 | 1 | yes |
| `tests/files/ubuntu.bats` | 0 | 0 | 0 | 2 | 2 | yes |
| `tests/install/common/check_tools.bats` | 0 | 0 | 0 | 1 | 1 | yes |
| `tests/install/common/chezmoi_private.bats` | 0 | 0 | 0 | 2 | 2 | yes |
| `tests/install/common/decrypt_private_key.bats` | 1 | 1 | 1 | 6 | 6 | yes |
| `tests/install/common/gh_extensions.bats` | 0 | 0 | 0 | 6 | 6 | yes |
| `tests/install/common/lifecycle.bats` | 1 | 1 | 1 | 1 | 1 | yes |
| `tests/install/common/mise.bats` | 0 | 0 | 0 | 8 | 8 | yes |
| `tests/install/common/private_layer.bats` | 0 | 0 | 0 | 9 | 9 | yes |
| `tests/install/common/provision_machine_key.bats` | 0 | 0 | 0 | 3 | 3 | yes |
| `tests/install/common/setup.bats` | 2 | 2 | 2 | 10 | 10 | yes |
| `tests/install/macos/common/brew.bats` | 0 | 0 | 0 | 1 | 1 | yes |
| `tests/install/macos/common/defaults.bats` | 0 | 0 | 0 | 1 | 1 | yes |
| `tests/install/macos/common/docker.bats` | 0 | 0 | 0 | 3 | 3 | yes |
| `tests/install/macos/common/ghostty.bats` | 0 | 0 | 0 | 2 | 2 | yes |
| `tests/install/macos/common/misc.bats` | 0 | 0 | 0 | 4 | 4 | yes |
| `tests/install/ubuntu/client/default_shell.bats` | 0 | 0 | 0 | 7 | 7 | yes |
| `tests/install/ubuntu/client/docker.bats` | 0 | 0 | 0 | 6 | 6 | yes |
| `tests/install/ubuntu/client/ghostty.bats` | 0 | 0 | 0 | 2 | 2 | yes |
| `tests/install/ubuntu/client/gnome_settings.bats` | 0 | 0 | 0 | 4 | 4 | yes |
| `tests/install/ubuntu/client/misc.bats` | 0 | 0 | 0 | 2 | 2 | yes |
| `tests/install/ubuntu/client/tailscale.bats` | 0 | 0 | 0 | 6 | 6 | yes |
| `tests/install/ubuntu/client/zed.bats` | 0 | 0 | 0 | 7 | 7 | yes |
| `tests/install/ubuntu/common/dependencies.bats` | 0 | 0 | 0 | 4 | 4 | yes |
| `tests/install/ubuntu/common/dependencies_unit.bats` | 0 | 0 | 0 | 12 | 12 | yes |
| `tests/install/ubuntu/common/setup_locale.bats` | 0 | 0 | 0 | 2 | 2 | yes |
| `tests/install/ubuntu/common/ssh.bats` | 0 | 0 | 0 | 3 | 3 | yes |
| `tests/install/ubuntu/server/setup_timezone.bats` | 0 | 0 | 0 | 1 | 1 | yes |
| `tests/install/ubuntu/server/sheldon.bats` | 0 | 0 | 0 | 2 | 2 | yes |
| `tests/install/ubuntu/server/starship.bats` | 0 | 0 | 0 | 3 | 3 | yes |
| `tests/unit/test_agent_session_staleness.py` | 3 | 3 | 3 | 19 | 19 | yes |
| `tests/unit/test_agmsg_dispatch.py` | 1 | 1 | 1 | 16 | 16 | yes |
| `tests/unit/test_agmsg_orchestration_docs.py` | 1 | 1 | 1 | 3 | 3 | yes |
| `tests/unit/test_apparmor_userns.py` | 2 | 2 | 2 | 19 | 19 | yes |
| `tests/unit/test_asset_manifest.py` | 1 | 1 | 1 | 17 | 17 | yes |
| `tests/unit/test_aws_cli_acquisition.py` | 1 | 1 | 1 | 13 | 13 | yes |
| `tests/unit/test_check_agent_runtime.py` | 1 | 1 | 1 | 51 | 51 | yes |
| `tests/unit/test_chezmoiremove_agmsg.py` | 1 | 1 | 1 | 2 | 2 | yes |
| `tests/unit/test_claude_settings_merge.py` | 1 | 1 | 1 | 22 | 22 | yes |
| `tests/unit/test_codex_config_merge.py` | 1 | 1 | 1 | 15 | 15 | yes |
| `tests/unit/test_contextdb_codex_notify.py` | 1 | 1 | 1 | 8 | 8 | yes |
| `tests/unit/test_files_fixture.py` | 1 | 1 | 1 | 4 | 4 | yes |
| `tests/unit/test_generate_agent_configs.py` | 3 | 3 | 3 | 57 | 57 | yes |
| `tests/unit/test_herdr_agents.py` | 1 | 1 | 1 | 207 | 207 | yes |
| `tests/unit/test_permgate.py` | 2 | 2 | 2 | 53 | 53 | yes |
| `tests/unit/test_release_asset_pins.py` | 2 | 2 | 2 | 10 | 10 | yes |
| `tests/unit/test_remove_agent_asset.py` | 1 | 1 | 1 | 23 | 23 | yes |
| `tests/unit/test_require_crit_review.py` | 2 | 2 | 2 | 34 | 54 | yes |
| `tests/unit/test_runtime_health.py` | 1 | 1 | 1 | 57 | 58 | yes |
| `tests/unit/test_statusline_tools.py` | 1 | 1 | 1 | 7 | 7 | yes |
| `tests/unit/test_supply_chain_policy.py` | 1 | 1 | 1 | 19 | 19 | yes |
| `tests/unit/test_update_agent_assets_ua_core.py` | 1 | 1 | 1 | 23 | 23 | yes |
| `tests/unit/test_usage_review.py` | 3 | 3 | 3 | 11 | 11 | yes |
| `tests/unit/test_validate_agent_assets.py` | 3 | 3 | 3 | 75 | 81 | yes |
| `tests/unit/test_workflow_security.py` | 4 | 4 | 4 | 12 | 12 | yes |

Result: 0 rows with rev2 < old; no file whose def-like line count decreased between 7b69b1e and 72b8901, so no decrease needs a source-change explanation. Symbol totals over these 360 files: old 492, rev1 468, rev2 509.
