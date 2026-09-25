# dot-docs-align-T1-a01 validation

## Agent asset validator

Initial sandboxed attempt:

```text
error: Request failed after 3 retries in 5.9s
  Caused by: Failed to fetch: `https://pypi.org/simple/pyyaml/`
  Caused by: error sending request for url (https://pypi.org/simple/pyyaml/)
  Caused by: client error (Connect)
  Caused by: dns error
  Caused by: failed to lookup address information: nodename nor servname provided, or not known
```

Final command:

```text
env UV_CACHE_DIR=/tmp/dot-docs-align-uv-cache uv run --with pyyaml python scripts/validate-agent-assets.py
```

Final output:

```text
agent asset validation ok
```

## Shell checks

Commands:

```text
shellcheck -x scripts/update-agent-assets.sh
mise x shfmt@3.14.1 -- shfmt -i 4 -sr -d scripts/update-agent-assets.sh
```

Output:

```text
mise WARN  tool purgatory cleanup failed: Operation not permitted (os error 1)
```

Both commands exited 0. The warning is from mise's post-run cache cleanup; shfmt emitted no diff.

## Python unit suite

Command:

```text
env UV_CACHE_DIR=/tmp/dot-docs-align-uv-cache make unit-test
```

Output tail:

```text
----------------------------------------------------------------------
Ran 368 tests in 45.426s

OK
```

## Herdr implementation assertions quoted from tests

`tests/unit/test_herdr_agents.py:458-463`:

```text
f"pane split w-attach:p1 --direction right --cwd {self.workdir.resolve()} --env CLICOLOR_FORCE=1 --env FORCE_COLOR=1 --no-focus"
self.assertIn("--kind codex --pane w-attach:p3", codex_start)
self.assertNotIn("--cwd", codex_start)
```

`tests/unit/test_herdr_agents.py:1022-1026`:

```text
f"pane split w-test:p1 --direction right --cwd {self.workdir.resolve()} --env CLICOLOR_FORCE=1 --env FORCE_COLOR=1 --no-focus"
"agent start codex-worker-w-test --kind codex --pane w-test:p3 --timeout 30000 -- --sandbox workspace-write --profile standard"
```

These assertions match the revised README separation of pane cwd assignment from agent start.

## Docker build progression

Command for all attempts:

```text
limactl shell adh-test -- sudo -n env DOCKER_BUILDKIT=0 docker build --no-cache --rm -t dotfiles-docs-align:a01 .
```

First red result:

```text
Step 8/13 : RUN groupadd --gid $USER_GID $USERNAME     && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME -G sudo -s /bin/bash     && echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
 ---> Running in c6e186875aa3
groupadd: GID '1000' already exists
The command '/bin/sh -c groupadd --gid $USER_GID $USERNAME     && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME -G sudo -s /bin/bash     && echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers' returned a non-zero code: 4
```

Second red result after account reuse:

```text
Step 12/13 : RUN mkdir -p ~/.local/share/fonts
 ---> Running in ca773c25ed17
mkdir: cannot create directory '/home/mryfmo/.local/share/fonts': Permission denied
The command '/bin/sh -c mkdir -p ~/.local/share/fonts' returned a non-zero code: 1
```

Final green tail after precreating and chowning the workdir:

```text
Step 11/13 : RUN sudo sh -c "$(curl -fsLS get.chezmoi.io)" -- -b /usr/local/bin
 ---> Running in b97052fc18d9
info found chezmoi version 2.72.2 for latest/linux/arm64
info installed /usr/local/bin/chezmoi
 ---> Removed intermediate container b97052fc18d9
 ---> 3cb2adb1ee11
Step 12/13 : RUN mkdir -p ~/.local/share/fonts
 ---> Running in be796975f1fd
 ---> Removed intermediate container be796975f1fd
 ---> fc50f637e013
Step 13/13 : RUN mkdir -p /tmp
 ---> Running in ea071bee9561
 ---> Removed intermediate container ea071bee9561
 ---> 25c732175381
Successfully built 25c732175381
Successfully tagged dotfiles-docs-align:a01
```

## Docker cleanup

The task tag, unused layers, and the two exact stopped containers/images left by failed builds were removed. Final output:

```text
ca773c25ed17
c6e186875aa3
Deleted: sha256:f9392d03675793966116a2cc1dfad6c87de2ce108d62600e6cb836729c44b47a
Deleted: sha256:fcb3e775b448773b92d7c85d6dad12dfa768adda8d65092f29708dbffb05a3cd
remaining_images=0
remaining_containers=0
```

## Stale-text and diff checks

Commands:

```text
git diff --check
rg -n -- "--split right|agent start <agent-name> --cwd|ubuntu:22\\.04|^[[:space:]]*bats \\\\$|^9\\. For implementation" README.md Dockerfile home/dot_agents/README.md
```

Output: empty (exit 0; `rg` was allowed to return no matches).

## CompactionDB

Command:

```text
python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'dot-docs-align-T1-a01: lifecycle and Herdr documentation now mirrors the actual gh-extension/CompactionDB/agmsg and pane-split/agent-start flows; the Dockerfile uses Ubuntu 24.04, removes apt Bats, reuses the base image default UID/GID 1000 by renaming that account, and precreates a user-owned workdir.'
```

Output:

```text
b0c22d42-c6a6-40d0-a705-7ed1927cdc7b
```

## Review gate

Command:

```text
AGENT_REVIEWED=1 REVIEW_EVIDENCE=.agents/worklog/codex/review/dot-docs-align-T1-a01-receipt.md make require-crit-review
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
