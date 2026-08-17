# T84b Report

Status: `ready_for_review`

cost: n/a

`effects=none`

T84b fixes repository-path resolution when `update-agent-assets.sh` is inlined into a temporary chezmoi lifecycle script.

## Result

- The thin wrapper exports `DOTFILES_SOURCE_DIR` before its two includes.
- The wrapper itself starts with `#!/usr/bin/env bash`, so the rendered lifecycle file remains directly executable before the export and included scripts.
- Because this repository uses `.chezmoiroot=home`, live rendering proved that `.chezmoi.sourceDir` is `<repo>/home`; the wrapper therefore uses `joinPath .chezmoi.sourceDir ".."` to export the canonical repository root. Exporting `.chezmoi.sourceDir` literally would reproduce the defect because it does not contain `vendor/compactiondb`.
- One shdoc-documented resolver validates the exported root, falls back to the direct script's `BASH_SOURCE` parent, and fails with one clear error if neither contains `vendor/compactiondb`.
- Both repository-relative consumers use the resolved root: the optional manifest-library source path and the CompactionDB vendor path.
- The only remaining `BASH_SOURCE` use outside the resolver is the existing `BASH_SOURCE[0] == $0` main guard. It performs no path resolution and is include-safe: rendered lifecycle execution runs `main`, while unit tests that source the script do not.
- A foreign-cwd/rendered-script regression records `update_compactiondb` with version `2.0.0+dotfiles.5` and the repository vendor path. Direct resolution and invalid-root failure are separately pinned.
- The two existing runtime-health fixtures now include the vendor directory required by the validated repository-root contract.

## Manifest hygiene

Read-only inspection shows the live version-1 manifest has one complete `update_compactiondb` rsync entry at `2.0.0+dotfiles.5`, targeting `~/.agents/compactiondb`; no partial entry exists. The foreign-cwd regression proves the next lifecycle run replaces/records that whole step successfully without needing an asset-content change.

## Project memory

[memory: decision — Lifecycle scripts inlined through chezmoi include use a wrapper-exported, validated repository root; with `.chezmoiroot=home`, the wrapper exports the canonical parent via `joinPath`, while direct execution falls back to `BASH_SOURCE`.]

Recorded as `e4206914-9e52-4861-a629-e8f99a6ce451` with:

```text
python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "Lifecycle scripts inlined via chezmoi include must not resolve repository paths from BASH_SOURCE. With .chezmoiroot=home, the wrapper exports the canonical repository parent using joinPath .chezmoi.sourceDir \"..\"; update-agent-assets uses that validated root and falls back to direct BASH_SOURCE resolution only outside the include path."
```

[memory: failure — A chezmoi lifecycle wrapper must retain a shebang as rendered line 1; placing an export before the included script's shebang causes exec-format failure.]

Recorded as `cfd10a4c-5f67-4c84-8f7c-8aa912d0301f` with:

```text
python3 .claude/hooks/contextdb_cli.py memory add --kind failure --scope project --content "A chezmoi lifecycle wrapper must keep an executable shebang as rendered line 1. Prepending DOTFILES_SOURCE_DIR export ahead of the wrapper includes removed the shebang and caused exec format error during apply; keep #!/usr/bin/env bash in the wrapper itself before all exports/includes and pin the rendered first line in tests."
```

## Review

Crit data review approved with resolved records `r_a15d5a` and `r_b3eeb6`. Evidence: `.agents/worklog/codex/review/T84b-crit-comments.json`; receipt: `.agents/worklog/codex/review/T84b-review-receipt.md`.
