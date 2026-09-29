# T36 validation (dot-ua-graph-refresh-T36-a01)

Verbatim output of every validation command. The commands in section 1 were re-run for the record from worker-c at PR head 476c6e1. Section 2 shows outputs captured during the run.

## 1. Task validation commands

```
$ jq -r .gitCommitHash .ua/meta.json
7b69b1e76bb7cd8896007b7f78b70bc5b8620659
exit=0

$ git rev-parse HEAD
476c6e1e7df73617c402f57642cf49189b9f9de2
exit=0

$ git diff --name-only $(jq -r .gitCommitHash .ua/meta.json)..HEAD | head
.ua/fingerprints.json
.ua/knowledge-graph.json
.ua/meta.json
exit=0

$ git -C /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c diff origin/main --stat | tail -3
 .ua/knowledge-graph.json | 22471 ++++++++++++++++++++++-----------------------
 .ua/meta.json            |     6 +-
 3 files changed, 11243 insertions(+), 12527 deletions(-)
exit=0

$ gh pr checks 208
CodeRabbit	pass	0		Review skipped: manual review required for this OSS repository
changes	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/36530927729/job/109284215168
private-bootstrap (macos-14, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/36530927676/job/109284215777
private-bootstrap (ubuntu-latest, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/36530927676/job/109284215686
public-bootstrap (macos-14, client)	pass	8m15s	https://github.com/mryfmo/dotfiles/actions/runs/36530927676/job/109284215706
nix	skipping	0	https://github.com/mryfmo/dotfiles/actions/runs/36530927729/job/109284256133
private-bootstrap (ubuntu-latest, server)	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/36530927676/job/109284215579
public-bootstrap (ubuntu-latest, client)	pass	10m12s	https://github.com/mryfmo/dotfiles/actions/runs/36530927676/job/109284215730
public-bootstrap (ubuntu-latest, server)	pass	7m7s	https://github.com/mryfmo/dotfiles/actions/runs/36530927676/job/109284215677
test (macos-14, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/36530927729/job/109284254955
test (ubuntu-latest, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/36530927729/job/109284255063
test (ubuntu-latest, server)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/36530927729/job/109284254998
validate	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/36530927708/job/109284215145
exit=0

$ gh pr view 208 --json number,headRefOid,mergeable,state,url
{
  "headRefOid": "476c6e1e7df73617c402f57642cf49189b9f9de2",
  "mergeable": "MERGEABLE",
  "number": 208,
  "state": "OPEN",
  "url": "https://github.com/mryfmo/dotfiles/pull/208"
}
exit=0

```

## 2. Graph checks (re-run against the committed graph)

```
$ sha256sum /home/moriya/Workspace/dotfiles/.orchestration/tasks/dot-ua-graph-refresh-T36-a01.md; git show origin/main:.orchestration/tasks/dot-ua-graph-refresh-T36-a01.md | sha256sum
c7bde73e21f49c294c4d0ae73258550ff9f3b4513ac8125ac66b69c9e0bde847  /home/moriya/Workspace/dotfiles/.orchestration/tasks/dot-ua-graph-refresh-T36-a01.md
c7bde73e21f49c294c4d0ae73258550ff9f3b4513ac8125ac66b69c9e0bde847  -
exit=0

$ node /tmp/claude-1000/-home-moriya-Workspace-dotfiles--claude-worktrees-worker-c/89763728-b428-46b1-9b19-2d786c97de12/scratchpad/ua-core-validate.mjs $HOME/.understand-anything-plugin/packages/core/dist/index.js .ua/knowledge-graph.json
{"success":true,"fatal":null,"nodesIn":853,"nodesOut":853,"edgesIn":1219,"edgesOut":1219,"issueCount":0,"droppedIssues":0,"issueLevels":{}}
exit=0

$ jq '[.nodes[] | select(.lineRange != null and ((.lineRange|type) != "array"))] | length' .ua/knowledge-graph.json
0
exit=0

$ jq -c '{nodes:(.nodes|length),edges:(.edges|length),layers:(.layers|length),tour:(.tour|length)}' .ua/knowledge-graph.json
{"nodes":853,"edges":1219,"layers":9,"tour":15}
exit=0

$ git show 935e198:.ua/knowledge-graph.json | jq -c '{nodes:(.nodes|length),edges:(.edges|length)}'
{"nodes":1399,"edges":2398}
exit=0
# NOTE: wrong ref for "before". 935e198 is the T33c meta base (the pre-T33c graph); the
# graph being replaced is the one at the PR parent 7b69b1e (re-run below).

$ git show 7b69b1e:.ua/knowledge-graph.json | jq -c '{nodes:(.nodes|length),edges:(.edges|length)}'
{"nodes":870,"edges":1333}
exit=0

$ git show 7b69b1e:.ua/meta.json | jq -c .
{"lastAnalyzedAt":"2026-09-28T07:32:56.000Z","gitCommitHash":"935e198406e5df993c84de67c695c7083f4b6b54","version":"1.0.0","analyzedFiles":424}

$ git show 7b69b1e:.ua/knowledge-graph.json | jq '.tour|length'
15

$ grep -cE '(ghp_[A-Za-z0-9]{20,}|github_pat_|sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|AGE-SECRET-KEY-|-----BEGIN [A-Z ]*PRIVATE KEY|xox[baprs]-)' .ua/knowledge-graph.json
0
exit=1
# NOTE: grep -c exits 1 when there are zero matches; 0 matches is the passing result.

$ n=0; while IFS='=' read -r k v; do v=${v%\"}; v=${v#\"}; [ ${#v} -ge 12 ] || continue; grep -qF -- "$v" .ua/knowledge-graph.json && n=$((n+1)); done < <(grep -E '^[A-Z_]+=' home/dot_agents/model-profiles.env); echo model-profiles-value-hits=$n
model-profiles-value-hits=0
exit=0

$ git show --stat HEAD | tail -5

 .ua/fingerprints.json    |  1293 +--
 .ua/knowledge-graph.json | 22471 ++++++++++++++++++++++-----------------------
 .ua/meta.json            |     6 +-
 3 files changed, 11243 insertions(+), 12527 deletions(-)
exit=0

$ grep -nE '^\.ua/' .gitignore
17:.ua/intermediate/
18:.ua/tmp/
19:.ua/diff-overlay.json
exit=0

```

## 3. Outputs captured during the run (verbatim text; the incremental-plan JSON is re-flowed onto one line)

```
$ node ~/.understand-anything-plugin/skills/understand/prepare-incremental.mjs "$PWD" 935e198406e5df993c84de67c695c7083f4b6b54
scan-project: filesScanned=356 filteredByIgnore=1621 complexity=large
extract-import-map: filesScanned=356 filesWithImports=13 totalEdges=43
Incremental plan: FULL_UPDATE; analyze=29; delete=67; cosmetic=1; ignored=150; generated=3
exit=0
{"action":"FULL_UPDATE","reason":"96 files have structural changes (>30 files) — full rebuild recommended","filesToReanalyze":29,"baseCommit":"935e198406e5df993c84de67c695c7083f4b6b54","headCommit":"21265647772c9e584a9e3cd4dce5e404623434f6"}

$ node <skill>/compute-batches.mjs "$PWD"
Loaded 360 files (213 code).
Info: compute-batches: merged 244 small batches (253 files) into 11 misc batches — singletons and orphans consolidated
Wrote 31 batches (sizes: max=25, min=1) to /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/.ua/intermediate/batches.json
exit=0

$ python3 <skill>/merge-batch-graphs.py "$PWD"   (stderr)
Found 36 batch files (31 logical batches, 4 multi-part):
  batch-1-part-1.json: 13 nodes, 65 edges
  batch-1-part-2.json: 30 nodes, 66 edges
  batch-2.json: 23 nodes, 97 edges
  batch-3.json: 37 nodes, 104 edges
  batch-4.json: 2 nodes, 1 edges
  batch-5.json: 6 nodes, 16 edges
  batch-6.json: 4 nodes, 3 edges
  batch-7.json: 21 nodes, 29 edges
  batch-8.json: 4 nodes, 18 edges
  batch-9.json: 8 nodes, 27 edges
  batch-10.json: 3 nodes, 2 edges
  batch-11.json: 10 nodes, 7 edges
  batch-12.json: 3 nodes, 2 edges
  batch-13.json: 6 nodes, 3 edges
  batch-14.json: 11 nodes, 9 edges
  batch-15.json: 19 nodes, 13 edges
  batch-16.json: 17 nodes, 16 edges
  batch-17.json: 13 nodes, 8 edges
  batch-18.json: 8 nodes, 6 edges
  batch-19.json: 6 nodes, 53 edges
  batch-20-part-1.json: 41 nodes, 39 edges
  batch-20-part-2.json: 55 nodes, 53 edges
  batch-21.json: 25 nodes, 30 edges
  batch-22.json: 26 nodes, 28 edges
  batch-23.json: 49 nodes, 60 edges
  batch-24.json: 40 nodes, 38 edges
  batch-25.json: 25 nodes, 0 edges
  batch-26.json: 30 nodes, 20 edges
  batch-27-part-1.json: 75 nodes, 114 edges
  batch-27-part-2.json: 28 nodes, 30 edges
  batch-28-part-1.json: 9 nodes, 6 edges
  batch-28-part-2.json: 56 nodes, 67 edges
  batch-28-part-3.json: 53 nodes, 64 edges
  batch-29.json: 29 nodes, 36 edges
  batch-30.json: 55 nodes, 119 edges
  batch-31.json: 13 nodes, 23 edges

Input: 853 nodes, 1272 edges

Fixed (53 corrections):
    53 × tested_by edges dropped (orphan endpoint or test↔test / prod↔prod pair)

Tested-by linker:
     0 × tested_by edges produced (path-convention supplement, production → test)
    31 × production nodes tagged "tested"

Output: 853 nodes, 1219 edges

Imports edge recovery:
  Recovered 0 `imports` edges from importMap (360 entries scanned)

Written to /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/.ua/intermediate/assembled-graph.json (745 KB)

$ node .ua/tmp/ua-inline-validate.cjs .ua/intermediate/assembled-graph.json .ua/intermediate/review.json
exit=0
{"issues":0,"issueSample":[],"warnings":92,"stats":{"totalNodes":853,"totalEdges":1219,"totalLayers":9,"tourSteps":15,"nodeTypes":{"file":264,"function":457,"class":35,"service":2,"pipeline":7,"config":48,"document":40},"edgeTypes":{"contains":493,"exports":121,"calls":267,"imports":43,"depends_on":94,"triggers":11,"related":59,"configures":24,"documents":67,"tested_by":40}}}

$ node ua-core-validate.mjs <core>/dist/index.js .ua/intermediate/assembled-graph.json   # pre-save
{"success":true,"fatal":null,"nodesIn":853,"nodesOut":853,"edgesIn":1219,"edgesOut":1219,"issueCount":0,"droppedIssues":0,"issueLevels":{}}
exit=0

$ node <skill>/build-fingerprints.mjs .ua/intermediate/fingerprint-input.json
[json-parser] Failed to parse JSON: Unexpected token '#', "#!/usr/bin"... is not valid JSON
Fingerprints baseline: 360 files
exit=0

$ git commit (.ua/knowledge-graph.json .ua/fingerprints.json .ua/meta.json)
476c6e1 chore(ua): full knowledge-graph rebuild at 7b69b1e (T36)
7b69b1e chore(orchestration): T36 task text - correct the staleness sentence (since 935e198, core now built)

$ gh pr create ...
https://github.com/mryfmo/dotfiles/pull/208

$ cd /home/moriya/Workspace/dotfiles && python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "T36: the .ua/ knowledge graph is refreshed incrementally by a worker task whenever the SessionStart hook reports it stale; the orchestrator never runs the graph update in its own session (operator 2026-09-28)."
c99ba88c-c4da-4e34-a776-f53f538d8be8
```
