# dot-herdr-sheldon-T1-a01 report

status: ready_for_review

cost: n/a

## Result

- [memory:decision] `make update` now captures Herdr reload output and treats only a failure containing `protocol_mismatch` as recoverable. It emits one restart/manual-reload instruction and continues to `agmsg-bootstrap`; all other reload failures remain fatal.
- [memory:decision] The Ubuntu client Sheldon plugin is now inline and defers a readability-guarded source of `${HOME}/.local/bin/client/ubuntu.sh`. Machines without private dotfiles no longer require the removed public client directory, while private-managed machines retain the source behavior.
- `client/common.toml` remains unchanged: both path/fpath entries use the zsh `(N-/)` qualifier and disappear when the directory is absent.
- README and Bats coverage were updated. Bats was not run locally by policy; the exact fixture function was exercised directly for both reload branches.

## Files changed

- `Makefile`
- `README.md`
- `home/dot_config/sheldon/plugin_sources/client/ubuntu.toml`
- `tests/install/common/lifecycle.bats`
- `tests/install/common/setup.bats`

## CompactionDB

Command:

`python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'dot-herdr-sheldon-T1-a01: make update captures Herdr reload output and tolerates only protocol_mismatch with restart guidance; the Ubuntu Sheldon client plugin uses a guarded inline zsh-defer source so private ~/.local/bin/client/ubuntu.sh remains optional.'`

Decision ID: `83254df8-b144-4fbc-916b-496b89836263`

## Side effects

No persistent side effects outside the repository. The VM scratch user `dot-herdr-sheldon-a01` was removed during validation.
