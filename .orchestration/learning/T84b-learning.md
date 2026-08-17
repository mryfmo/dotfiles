# T84b Learning

## Validated learning

1. In a repository with `.chezmoiroot=home`, `.chezmoi.sourceDir` resolves to the managed `home/` root, not the Git repository root. Sibling repository assets require a template-time canonical parent such as `joinPath .chezmoi.sourceDir ".."`.
2. `BASH_SOURCE` describes the rendered temporary lifecycle file after `{{ include }}` expansion, so it is suitable only as a direct-execution fallback, never as the primary include-time repository root.
3. A source-root resolver must cover every repository-relative consumer, including early optional library sourcing, not only the failing downstream vendor lookup.
4. Minimal copied-script test repositories must include the directory used to validate repository identity; otherwise they test an impossible production shape.
5. Included content may contain a shebang, but it is no longer byte zero after a wrapper prepends environment setup. Any rendered executable wrapper must own and test its first-line shebang.

## Apply to

- All lifecycle scripts that inline repository scripts with chezmoi `include`.
- Future validators/tests that construct minimal dotfiles repository fixtures.
- Manifest bookkeeping regressions for steps whose deployed bytes are already current.

The durable decision is stored in project memory; this task-scoped learning artifact is authoritative under the allowed-file contract, so no Codex learn-index entry was added.
