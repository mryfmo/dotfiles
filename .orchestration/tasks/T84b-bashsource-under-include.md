# T84b: chezmoi include 下の BASH_SOURCE 相対解決の是正

task_id: T84b
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-conformance
worker: codex-deep-dot
plan: T84 follow-up (defect exposed by the first chezmoi-context run of the lifecycle script)
depends: T84 (accepted)

[memory: decision — Lifecycle scripts inlined via chezmoi {{ include }} cannot use BASH_SOURCE-relative repo paths; the wrapper template exports the chezmoi source dir and the script prefers it, falling back to BASH_SOURCE resolution only for direct execution, with a regression test running the script from a foreign cwd.]

## Defect (observed live)

`chezmoi apply` runs run_once_after_06-install-agent-assets.sh.tmpl,
which inlines scripts/update-agent-assets.sh; BASH_SOURCE then points
into chezmoi's temp dir, so line 648's
`$(dirname BASH_SOURCE)/../vendor/compactiondb/` resolved to
/var/folders/... and the update_compactiondb step failed (rsync lstat +
awk CHANGELOG errors, manifest step not recorded). Works only when
invoked from the repo via make update.

## Fix (exact; class = every BASH_SOURCE-relative repo path)

1. In home/.chezmoiscripts/common/run_once_after_06-install-agent-assets.sh.tmpl:
   before the include line, set and export
   `DOTFILES_SOURCE_DIR={{ .chezmoi.sourceDir | quote }}` (wrapper stays
   an intentionally thin include per AGENTS.md — one env line + include).
2. In scripts/update-agent-assets.sh: introduce one shared resolver
   (shdoc-documented) that returns the repo source root:
   `${DOTFILES_SOURCE_DIR}` when set and valid (contains
   vendor/compactiondb), else the existing BASH_SOURCE derivation, else
   fail with a clear error. Replace the line-648 derivation with it.
   Audit line 13 `AGENT_ASSET_SCRIPT_DIR` and every other repo-relative
   use in the script: route each through the resolver or justify in the
   report why it is include-safe.
3. Manifest hygiene: verify the failed `update_compactiondb` step
   records correctly on the next run (no stale/partial entry left; the
   deployed asset is already current at 2.0.0+dotfiles.5, so this is
   bookkeeping only).
4. Tests: unit/regression that runs the script (or its resolver) with
   cwd and BASH_SOURCE outside the repo and DOTFILES_SOURCE_DIR set,
   asserting the vendor path resolves into the repo; and the
   direct-execution path still resolves.
5. Gates: make format / shellcheck / shfmt / unit-test /
   validate-agent-assets.

## Allowed files

home/.chezmoiscripts/common/run_once_after_06-install-agent-assets.sh.tmpl,
scripts/update-agent-assets.sh, tests/unit, artifact paths (T84b set).

## Forbidden actions

git commit; git push; chezmoi apply; bats; dependency changes; changing
other lifecycle steps.

## Completion / RESULT contract

Five artifacts; memory add; effects=none; cost line.
Reply `AGMSG-RESULT v1 task_id=T84b`. max_turns=15.
