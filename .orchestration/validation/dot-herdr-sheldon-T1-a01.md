# dot-herdr-sheldon-T1-a01 validation

## TOML parse

Command:

```text
python3 - <<'PY'
import tomllib
from pathlib import Path
for name in ('common.toml', 'ubuntu.toml'):
    path = Path('home/dot_config/sheldon/plugin_sources/client') / name
    tomllib.loads(path.read_text())
    print(f'parsed {path}')
PY
```

Output:

```text
parsed home/dot_config/sheldon/plugin_sources/client/common.toml
parsed home/dot_config/sheldon/plugin_sources/client/ubuntu.toml
```

## Herdr reload fixture trace

The existing `run_update_fixture` function was loaded directly without invoking Bats, which is forbidden locally.

Output:

```text
protocol_mismatch status=0
Notice: local source not pulled (current branch is feature/test, not main); run 'git -C /private/var/folders/r2/_gkywj713g54lbxkc_hv7j400000gn/T/tmp.uwZpyK0AYm/update-1 pull' to fetch remote updates.
chezmoi apply --verbose
mise install --locked node
mise install --locked npm:ccstatusline npm:ccusage
./scripts/update-agent-assets.sh
protocol_mismatch: client protocol 20 is older than server protocol 22
Herdr was updated; restart the server with 'herdr server stop' or recreate the Ghostty session, then run 'herdr server reload-config' manually.
/Library/Developer/CommandLineTools/usr/bin/make agmsg-bootstrap
Herdr agents source helper not found; skipping agmsg bootstrap.
ordinary_failure status=2
Notice: local source not pulled (current branch is feature/test, not main); run 'git -C /private/var/folders/r2/_gkywj713g54lbxkc_hv7j400000gn/T/tmp.uwZpyK0AYm/update-2 pull' to fetch remote updates.
chezmoi apply --verbose
mise install --locked node
mise install --locked npm:ccstatusline npm:ccusage
./scripts/update-agent-assets.sh
reload failed
make: *** [update] Error 1
```

## Sheldon lock/source

Command used a temporary config copied from `client/ubuntu.toml`, then ran Sheldon 0.8.5 `lock` and `source`.

Output:

```text
LOADED /var/folders/r2/_gkywj713g54lbxkc_hv7j400000gn/T/tmp.QtL1UgOAxh/plugins.toml
LOCKED /var/folders/r2/_gkywj713g54lbxkc_hv7j400000gn/T/tmp.QtL1UgOAxh/data/plugins.lock
function _ubuntu_command() {
    # Private dotfiles may provide this file on client machines.
    [ -r "${HOME}/.local/bin/client/ubuntu.sh" ] && source "${HOME}/.local/bin/client/ubuntu.sh"
}
zsh-defer _ubuntu_command
```

## adh-test VM scratch-user trace

Command class: `limactl shell adh-test -- sudo -n bash -s`. No login shell was used. Sheldon was not installed in the VM, so the lock-equivalent check parsed the plugin and proved it has no `local` lookup, then executed its emitted inline zsh with an immediate test `zsh-defer` shim.

Output:

```text
sheldon_lock_equivalent=parsed; ubuntu-command=inline; local_lookup=absent
client_path_null_glob_count=2
missing_private_source=skipped
present_private_source=sourced
userdel: dot-herdr-sheldon-a01 mail spool (/var/mail/dot-herdr-sheldon-a01) not found
scratch_user_removed=dot-herdr-sheldon-a01
```

## Python unit suite

Command:

```text
env UV_CACHE_DIR=/tmp/dot-herdr-sheldon-uv-cache make unit-test
```

Output tail:

```text
----------------------------------------------------------------------
Ran 368 tests in 42.720s

OK
```

## Shell formatting/lint applicability

No `.sh` file changed. Repository CI limits shfmt to tracked `install/**/*.sh` and `scripts/**/*.sh`, and shellcheck to `setup.sh`, `install/*.sh`, `install/**/*.sh`, and `scripts/*.sh`. The changed Makefile fragment is covered by the lifecycle fixture; changed `.bats` tests will run in CI and were not run locally per task policy.

## Diff check

Command: `git diff --check`

Output: empty (exit 0).

## CompactionDB

Command:

```text
python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'dot-herdr-sheldon-T1-a01: make update captures Herdr reload output and tolerates only protocol_mismatch with restart guidance; the Ubuntu Sheldon client plugin uses a guarded inline zsh-defer source so private ~/.local/bin/client/ubuntu.sh remains optional.'
```

Output:

```text
83254df8-b144-4fbc-916b-496b89836263
```

## Review gate

Initial receipt validation output:

```text
AGENT_REVIEWED=1 requires review evidence before completion.
- REVIEW_EVIDENCE agent reviewer requires `review_outcome: approved` or `review_outcome: addressed`
make: *** [require-crit-review] Error 1
```

The receipt field was corrected to the exact accepted value. Final command:

```text
AGENT_REVIEWED=1 REVIEW_EVIDENCE=.agents/worklog/codex/review/dot-herdr-sheldon-T1-a01-receipt.md make require-crit-review
```

Output:

```text
Review requirement satisfied by AGENT_REVIEWED=1 with REVIEW_EVIDENCE.
```

## Final artifact checks

Output:

```text
diff_check=ok
crit_json=ok
required_artifacts=present
```
