# T62b: Incorporate omitted shell sources into the UA graph (PR #129 bot finding)

task_id: T62b
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-conformance
worker: codex-deep-dot

[memory: failure — The understand-anything auto-update extension filter (.py/.ts/... only) silently omits .sh files and extensionless executables, so incremental updates can stamp meta as current while new shell functionality has no fingerprint or graph node; shell sources must be supplemented explicitly in this repo's graph updates.]

## Finding (chatgpt-codex-connector on PR #129, orchestrator-triaged REAL)

Relative to the advertised cc977bf snapshot:

- home/dot_local/bin/common/executable_agent-session-staleness — no
  fingerprint, no node
- home/dot_local/bin/common/executable_remove-agent-asset — no
  fingerprint, no node
- scripts/lib/asset-manifest.sh — no fingerprint, no node
- scripts/update-agent-assets.sh — fingerprint and node line ranges still
  describe the pre-change version

Root cause: the 2.9.4 auto-update procedure's source-extension filter
excludes .sh and extensionless executables, while the full /understand
analysis DOES index shell (existing agmsg script nodes prove it).

## Fix (exact)

1. For the four files, produce proper graph incorporation consistent with
   the EXISTING shell nodes' schema (inspect a current agmsg script node
   for the exact node/edge/summary/filePath/fingerprint shape and follow
   it): add nodes + fingerprints for the three new files; refresh the
   fingerprint, summary, and line ranges for update-agent-assets.sh;
   add/refresh edges that the existing schema expresses (e.g.
   file-to-file source/exec relations) ONLY where the current graph
   already models such relations — do not invent new edge types.
2. Update .ua/fingerprints.json and .ua/meta.json coherently (meta keeps
   gitCommitHash cc977bf-or-current-HEAD — set to `git rev-parse HEAD`).
3. Run the graph's own invariant checks if the plugin provides them
   (consult the auto-update prompt's validation phase); at minimum both
   JSON files must parse and node/edge counts be reported before/after.
4. Do NOT modify the plugin cache or its procedure files.

## Allowed files

.ua/\*\* plus your artifact paths (T62b five artifacts).

## Forbidden actions

git commit; git push; chezmoi apply; bats; changes outside .ua/ and
artifacts; plugin cache modification.

## Validation

1. python3 json.load on knowledge-graph.json / fingerprints.json /
   meta.json.
2. Grep-level proof: each of the four paths present in fingerprints and
   as a graph node filePath; update-agent-assets.sh fingerprint changed
   from the pre-fix value (show old vs new).
3. Node/edge counts before vs after.
4. `git status --porcelain` -> only .ua/\*\* + artifacts.

## Completion / RESULT contract

Five artifacts (T62b set); memory add with the failure fact
(--kind failure); effects=none.
Reply `AGMSG-RESULT v1 task_id=T62b status=ready_for_review`. max_turns=20.
