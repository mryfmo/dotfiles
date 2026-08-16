# T48: Codex notify → contextdb ingest receiver (P5)

task_id: T48
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-conformance
worker: codex-deep-dot
plan: .orchestration/tasks/PLAN-compactiondb-research-integration.md (Phase 3)
analysis: .orchestration/analysis/compactiondb-compaction-research.md (P5)
depends: T47 (accepted)

[memory: decision — Codex turn-level capture into CompactionDB flows through the official notify agent-turn-complete event into contextdb ingest; the receiver silently no-ops (exit 0) in non-opted-in projects and never blocks a worker turn.]

## Goal

Give Codex turn-granularity automatic capture parity: a receiver script
wired to the official Codex `notify` config forwards `agent-turn-complete`
payloads into the per-project CompactionDB via the existing `ingest`
subcommand (`ingested_from='codex'`). No vendor changes.

## Allowed files (edit boundary)

- home/dot_local/bin/common/executable_contextdb-codex-notify (NEW, bash)
- EXACTLY ONE notify-config injection point discovered in step 1 (a
  home/dot*codex/modify*\*.config.toml script and/or the generator source
  it renders from — state the finding; if the generator is
  scripts/generate-agent-configs.py or agent-config.yaml, editing those IS
  allowed but keep the change minimal and profile-scoped)
- home/dot_config/codex/AGENTS.md (usage note, <=3 lines)
- Your artifact paths (T48 five artifacts)
- NOT allowed: vendor/compactiondb/\*\* (if ingest cannot accept the
  payload, STOP and report the schema gap via agmsg)

## Forbidden actions

git commit; git push; chezmoi apply; bats; dependency changes;
vendor/compactiondb changes; touching AGMSG_STORAGE_PATH or any agmsg
delivery configuration; wiring notify into profiles other than the one(s)
identified as worker profiles in step 1.

## Work order (follow exactly; ambiguity -> ask via agmsg)

1. Discovery (report the evidence): how Codex profile configs are
   generated (agent-config.yaml -> generator -> ~/.codex/<profile>.config.toml
   and/or chezmoi modify scripts), what the official `notify` config key
   expects (array argv; the event JSON arrives as the last argv element),
   and the exact payload shape of `agent-turn-complete` (consult installed
   Codex docs/`codex --help`/config reference read-only; do not launch
   agents). Decide the single injection point for worker-facing profiles
   (standard and deep) and record why.
2. Implement `executable_contextdb-codex-notify` (bash, shdoc comments in
   English):
   - Input: the notify JSON payload argument.
   - Behavior: parse the working directory from the payload (fall back to
     $PWD if absent); if `<dir>/.claude/hooks/contextdb_cli.py` does not
     exist, exit 0 silently. Otherwise run
     `python3 <dir>/.claude/hooks/contextdb_cli.py ingest` with the
     payload on stdin (or the CLI's documented ingest input form — read
     the vendored CLI to confirm the exact invocation; do not guess),
     with a 5-second timeout.
   - Never exit non-zero: on any failure (bad JSON, timeout, ingest
     error) print ONE line to stderr and exit 0.
   - Do not read or modify any environment variables beyond PATH lookup.
3. Wire `notify = ["<absolute path>/contextdb-codex-notify"]` (or the
   template-correct equivalent) into the worker profiles decided in
   step 1, via the discovered single injection point.
4. Add <=3 lines to home/dot_config/codex/AGENTS.md: automatic turn-level
   ingest exists in opted-in projects; the T45 manual `memory add`
   contract still applies for durable decisions.
5. Static checks: `bash -n` and
   `shfmt --indent 4 --space-redirects --diff` on the new script;
   `make format` repo-wide diff clean; `make validate-agent-assets` green;
   if the generator was changed, run it (or its check mode) and show the
   rendered profile diff.
6. Local integration test (allowed; NOT bats): in a scratch directory
   under your sandbox, run `compactiondb-install <scratch>` using the
   updated vendor tree at ~/.agents/... if present or the repo vendor via
   install.py directly, then invoke the receiver with (a) a valid
   synthetic agent-turn-complete payload -> assert an events row with
   ingested_from='codex' via sqlite3; (b) the same payload in a NON-opted
   directory -> exit 0, no output, no DB; (c) broken JSON -> exit 0, one
   stderr line. Record all three transcripts.

## Validation (record in validation artifact)

1. Step 5 command outputs (all green).
2. Step 6 three-case transcript with sqlite3 evidence.
3. `git status --porcelain` / `git diff --stat` -> only Allowed files.
4. Full `git diff` of the injection point and the new script.

## Completion / RESULT contract

- Five artifacts at .orchestration/{reports/T48.md, validation/T48.txt,
  sandboxes/T48.md, learning/T48.md, autoskill/runs/T48.md}.
- Report states durable facts with `[memory:...]` markers; do not run
  `memory add` here (repo not opted in).
- Live verification with a real Codex worker turn is T51's E2E-2, not part
  of this task's acceptance.
- Reply `AGMSG-RESULT v1 task_id=T48 status=ready_for_review ...` with all
  artifact paths. max_turns=25.
