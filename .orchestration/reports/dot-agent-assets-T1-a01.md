# dot-agent-assets-T1-a01 report

status: ready_for_review
cost: n/a

## Result

- Updated the terminal-browser pin to `v0.11.1` and SHA-256 `accb57252d6e7dde513db2a473c008d71897cf72feaaecd58c5042821d1d63f9`.
- Independently downloaded `https://terminal-browser.sh/install` without executing it and reproduced the pinned digest.
- Kept the existing Codex Superpowers installed-plugin detection path, while skipping `codex plugin add` with the required message when `openai-curated` is not a configured Git marketplace.
- Added a focused Python unit test whose mock emits the observed raw error if the forbidden add path is called.

[memory:decision] terminal-browser installer is pinned at v0.11.1 with SHA-256 accb57252d6e7dde513db2a473c008d71897cf72feaaecd58c5042821d1d63f9; Codex Superpowers plugin installation is skipped unless openai-curated is a configured Git marketplace, while already-installed detection remains active.

## Files changed

- `scripts/lib/installer-pins.sh`
- `scripts/update-agent-assets.sh`
- `tests/unit/test_runtime_health.py`
- Required task evidence and Codex worklog files.

## Validation

See `.orchestration/validation/dot-agent-assets-T1-a01.md`. Required script checks, focused mock trace, runtime-health tests, supply-chain tests, installer digest calculation, and diff check passed. Local bats, installer execution, VM use, git commit, and push were not performed.

## CompactionDB

Command:

```text
python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'terminal-browser installer is pinned at v0.11.1 with SHA-256 accb57252d6e7dde513db2a473c008d71897cf72feaaecd58c5042821d1d63f9; Codex Superpowers plugin installation is skipped unless openai-curated is a configured Git marketplace, while already-installed detection remains active.'
```

Decision ID: `efab8207-2839-456f-96de-2207b9eb8d52`
