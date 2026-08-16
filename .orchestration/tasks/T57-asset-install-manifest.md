# T57: Asset install manifest (H1, part 1)

task_id: T57
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-conformance
worker: codex-deep-dot
plan: .orchestration/tasks/PLAN-harness-composability-integration.md (Phase 4)
analysis: .orchestration/analysis/harness-composability-research.md (H1)

[memory: decision — Every update-agent-assets install step records what it installed (paths, commands, source version) into the atomic ~/.agents/.installed-manifest.json; recording is additive-only and never changes install behavior.]

## Goal

Give the asset lifecycle its missing "what did we install" record — the
prerequisite for the H1 reverse mapping (T58 remove) and H5 repair (T59).

## Allowed files (edit boundary)

- scripts/update-agent-assets.sh (recording calls only; NO behavior change)
- scripts/lib/asset-manifest.sh (NEW, if shared functions are cleaner —
  update-agent-assets.sh may source it; state the layout decision)
- tests/unit/ (matching module, likely NEW test_asset_manifest)
- Your artifact paths (T57 five artifacts)

## Forbidden actions

git commit; git push; chezmoi apply; bats; dependency changes; running
`make update` or any real-HOME install step (fake-HOME function-level
testing only); altering any install step's existing commands, ordering,
or outputs.

## Manifest spec (fixed by the plan — do not reinterpret)

Path: `~/.agents/.installed-manifest.json`

```json
{
  "version": 1,
  "steps": {
    "<step-name>": {
      "installed_at": "<iso8601-utc>",
      "kind": "plugin|rsync|brew|installer|integration",
      "paths": ["<absolute path>", ...],
      "commands": ["<command line>", ...],
      "source_version": "<version|commit|sha|unknown>"
    }
  }
}
```

- Atomic write: temp file + mv, 0600 perms.
- Step names == the shell function names in update-agent-assets.sh
  (do not invent a different granularity).
- Recording failure: one stderr warning line, install proceeds unaffected.

## Work order (exact; ambiguity -> ask via agmsg)

1. Inventory every install step function in update-agent-assets.sh (the
   plan counts 11; list the actual function names in the report and use
   exactly those).
2. Implement `manifest_record <step-name> <kind> <source_version>
<path>... [-- <command>...]` (or an equivalent minimal interface —
   document it) with jq or python3 for JSON manipulation using ONLY tools
   already required by the repo (jq is already a hard dependency of
   herdr-agents; verify and state which you use).
3. Add exactly one recording call at the END of each install step with
   that step's principal created/updated paths, the commands it ran, and
   the best available version signal (plugin version, vendor CHANGELOG
   top entry for compactiondb, brew formula version, pinned commit for
   the understand-anything installer, `herdr --version` for integrations;
   `unknown` when genuinely unavailable — justify each in the report).
4. Merge semantics: re-recording a step replaces its entry wholesale
   (keyed object), preserving other steps.
5. Tests (fake HOME): schema validity after two different steps recorded;
   wholesale replacement on re-record; atomicity (no partial file after a
   simulated failure mid-write — kill between temp write and mv is
   acceptable to simulate by calling internals); recording-failure
   isolation (make the manifest dir unwritable -> step still "succeeds",
   one stderr line).
6. shfmt/bash -n; keep update-agent-assets.sh's existing shdoc style.

## Validation (record in validation artifact)

1. `make format` exit 0; `bash -n` on touched scripts.
2. `make unit-test` all green (totals + new count).
3. `make validate-agent-assets` green.
4. Fake-HOME transcript: run two real step functions against a fake HOME
   (choose the two safest, e.g. compactiondb rsync + a no-network step;
   if none are safe offline, simulate with stubbed commands and say so)
   and paste the resulting manifest JSON.
5. `git status --porcelain` / `git diff --stat` -> only Allowed files;
   diff of update-agent-assets.sh shows ONLY added recording lines +
   sourcing (prove with a filtered diff).

## Completion / RESULT contract

- Five artifacts (T57 set); T45-contract memory add executed and quoted.
- Reply `AGMSG-RESULT v1 task_id=T57 status=ready_for_review ...`.
  max_turns=25.
