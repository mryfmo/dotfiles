# T58: remove-agent-asset + doctor orphan detection (H1, part 2)

task_id: T58
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-conformance
worker: codex-deep-dot
plan: .orchestration/tasks/PLAN-harness-composability-integration.md (Phase 4)
analysis: .orchestration/analysis/harness-composability-research.md (H1)
depends: T57 (accepted)

[memory: decision — Installed agent assets are reversible: remove-agent-asset executes the manifest-recorded inverse per step (dry-run default, --yes required, prefix-guarded to manifest paths only), and doctor lists orphaned assets with removal suggestions but never deletes.]

## Goal

The reverse mapping: consume the T57 manifest to remove any installed
step, and teach doctor to surface assets that neither the source tree nor
the manifest accounts for.

## Allowed files (edit boundary)

- home/dot_local/bin/common/executable_remove-agent-asset (NEW, bash,
  shdoc English)
- scripts/check-agent-runtime.py (orphan detection addition)
- Makefile ONLY if doctor needs a variable plumbed (minimal)
- tests/unit/ (matching modules)
- Your artifact paths (T58 five artifacts)

## Forbidden actions

git commit; git push; chezmoi apply; bats; dependency changes; ANY
deletion outside manifest-recorded paths; real-HOME destructive testing
(fake HOME only); weakening the three guards below; changes to
update-agent-assets.sh or asset-manifest.sh.

## Non-negotiable guards (pin each with a test)

1. `--dry-run` is the DEFAULT; actual removal requires explicit `--yes`.
2. Every path acted on must prefix-match a path recorded in the
   manifest entry being removed (after realpath normalization; symlink
   targets outside recorded prefixes are not followed for deletion —
   remove the link, not the target).
3. Steps absent from the manifest -> error exit 1 with the list of known
   steps; never guess.

## Work order (exact; ambiguity -> ask via agmsg)

1. `remove-agent-asset <step-name> [--dry-run|--yes]`:
   - Load `~/.agents/.installed-manifest.json`; resolve the step.
   - Inverse by kind:
     - plugin: uninstall via the owning CLI — verify exact subcommands
       read-only (`claude plugin --help`, `codex plugin --help`,
       `crit --help`) and record them in the report; if a CLI lacks an
       uninstall, fall back to deleting the manifest-recorded cache/data
       paths (guarded) and say so.
     - rsync/installer: delete the manifest-recorded target paths
       (guarded, rm -rf only on recorded directories).
     - brew: `brew uninstall <formula>` (formula from commands/version
       fields; if ambiguous, error out rather than guess).
     - integration: `herdr integration uninstall <name>` if it exists
       (verify via `herdr integration --help`); else guarded path removal.
   - Dry-run prints the exact operations without executing.
   - On success with --yes: remove the step entry from the manifest via
     the T57 lib's atomic write (source scripts/lib/asset-manifest.sh if
     it exposes a suitable function; if not, implement removal locally
     with the same temp+mv pattern — do NOT modify the lib).
2. Doctor (check-agent-runtime.py): add orphan detection — directories
   directly under ~/.agents/ (and ~/.agents/skills/) that are neither
   (a) chezmoi-source-derived, (b) manifest-recorded, nor (c) in the
   existing allow-list (understand-anything symlinks, state dirs like
   .installed-manifest.json itself, compactiondb, db/run/teams runtime).
   Output: WARN lines with a suggested `remove-agent-asset <step>` when
   the orphan matches a manifest step, else "manual review" wording.
   NEVER delete.
3. Tests (fake HOME): dry-run prints and does nothing; --yes removes
   exactly recorded paths and updates the manifest; prefix-guard rejects
   a tampered manifest entry pointing outside ~/.agents//~/.claude
   plugin-cache roots (simulate an entry with /tmp path -> refused);
   unknown step exit 1; orphan detection all three classes.
4. shdoc + shfmt; bash -n.

## Validation (record in validation artifact)

1. `make format` exit 0; `bash -n` on the new script.
2. `make unit-test` all green (totals + new count).
3. `make validate-agent-assets` green.
4. Fake-HOME transcripts for all guard tests (paste).
5. `git status --porcelain` / `git diff --stat` -> only Allowed files.

## Completion / RESULT contract

- Five artifacts (T58 set); T45-contract memory add executed and quoted.
- Live one-cycle verification (install -> remove -> doctor clean) is T61
  E2E-3'.
- Reply `AGMSG-RESULT v1 task_id=T58 status=ready_for_review ...`.
  max_turns=25.
