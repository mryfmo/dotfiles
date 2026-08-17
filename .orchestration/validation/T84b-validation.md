# T84b Validation

review_surface: crit-data
reviewer: codex
review_source: .agents/worklog/codex/review/T84b-crit-comments.json
review_outcome: approved
review_notes: Resolved records `r_a15d5a` and `r_b3eeb6` cover all four T84b changed files, shebang-first revision, live rendering, resolver branches, bookkeeping, and gates.

## RED / GREEN

Initial focused tests failed as intended:

- the repo-external rendered script resolved CompactionDB under its temporary parent and created no manifest;
- `resolve_dotfiles_source_dir` did not exist;
- the wrapper lacked the export.

After implementation, all 11 asset-manifest tests pass. The foreign-cwd regression sources a rendered copy outside the repository with `DOTFILES_SOURCE_DIR` set, stubs only rsync, then asserts:

- exit 0;
- manifest step `update_compactiondb` exists;
- `source_version` is `2.0.0+dotfiles.5`;
- rsync source is `<repo>/vendor/compactiondb/`.

The direct-source fallback returns the repository root with the export unset. A repo-external rendered copy with no valid export exits 1 and emits `Unable to resolve dotfiles source root`.

## Live template evidence

The initially specified literal export was rejected by live evidence:

```text
{{ .chezmoi.sourceDir | quote }}
=> "/Users/mryfmo/Workspace/dotfiles/home"
```

That path lacks `vendor/compactiondb`. The implemented expression renders correctly:

```text
#!/usr/bin/env bash
export DOTFILES_SOURCE_DIR="/Users/mryfmo/Workspace/dotfiles"
```

The complete `chezmoi execute-template` output passes `bash -n`. A regression invokes `chezmoi execute-template --source <repo>/home --file <wrapper>` and pins the two rendered lines above, preventing the live exec-format regression where `export` became line 1.

## Repository-relative audit

`rg BASH_SOURCE|AGENT_ASSET_SCRIPT_DIR|vendor/compactiondb` finds:

- `BASH_SOURCE` inside the shared direct-execution fallback;
- the resolved root feeding `AGENT_ASSET_SCRIPT_DIR/scripts`;
- the resolved root feeding `vendor/compactiondb/`;
- the existing main guard, which compares source/executable identity and does not resolve a path.

No other repository-relative consumer remains in the script.

## Manifest hygiene

Read-only `jq` inspection of `~/.agents/.installed-manifest.json` reports a complete version-1 `update_compactiondb` entry with `kind=rsync`, `source_version=2.0.0+dotfiles.5`, the one installed path, and the full rsync command. No partial/stale structure was found. No live write or apply was performed.

## Gates

```text
uv run python -m unittest tests.unit.test_asset_manifest  PASS (11 tests)
make unit-test                                           PASS (342 tests)
make format                                              PASS
make validate-agent-assets                               PASS
shellcheck -x scripts/update-agent-assets.sh             PASS
shfmt --indent 4 --space-redirects --diff <script>       PASS
bash -n source and chezmoi-rendered lifecycle script     PASS
git diff --check                                         PASS
```

The first full run exposed two intentionally minimal test repositories without `vendor/compactiondb`; adding the required vendor directory/CHANGELOG to those fixtures restored both tests without weakening resolver validation.

The orchestrator's first live apply then exposed a separate exec-format defect: adding the export as wrapper line 1 displaced the inlined script's shebang. The rendered-first-line regression failed with `export ...` versus `#!/usr/bin/env bash`, then passed after the wrapper-owned shebang was added. The complete 342-test suite and every static gate were rerun after this revision.

## Forbidden-action confirmation

- No Bats, `chezmoi apply`, other lifecycle edit, dependency mutation, Git commit, or Git push occurred.
- `effects=none`
