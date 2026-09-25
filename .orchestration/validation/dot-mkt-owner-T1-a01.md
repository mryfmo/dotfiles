# dot-mkt-owner-T1-a01 validation

review_surface: crit-data
reviewer: codex
review_source: .agents/worklog/codex/review/dot-mkt-owner-T1-a01-crit.json
review_outcome: approved

## F1 candidate-writer investigation

The credential-free `adh-test` scratch user used the repository-pinned tools:

```text
2026.9.12 linux-arm64 (2026-09-20)
codex-cli 0.150.1
2.1.251 (Claude Code)
crit v0.20.2 (2026-09-18, 10a7475)
Inline code review for AI agent workflows
```

Each case reset the target to the same mode 0644, mtime, size, and SHA-256. The first pass without preinstalled Crit config and the corrected pass with bootstrapped Crit plugin/config produced the same state result.

### Codex exec

Command:

```text
codex exec --skip-git-repo-check 'echo hi'
```

Verbatim state evidence:

```text
before mode=644 mtime=1789948800 size=695 sha256=eecdfa56cff1f661f3c9441ba701c04a983de51a1cafa4a65de5a121a574ad96
ERROR: unexpected status 401 Unauthorized: Missing bearer or basic authentication in header
command-status=1
after mode=644 mtime=1789948800 size=695 sha256=eecdfa56cff1f661f3c9441ba701c04a983de51a1cafa4a65de5a121a574ad96
content-diff=clean
```

### Claude version and print mode

Commands:

```text
claude --version
claude -p 'echo hi'
```

Verbatim output:

```text
before mode=644 mtime=1789948800 size=695 sha256=eecdfa56cff1f661f3c9441ba701c04a983de51a1cafa4a65de5a121a574ad96
2.1.251 (Claude Code)
Not logged in · Please run /login
version-status=0 print-status=1
after mode=644 mtime=1789948800 size=695 sha256=eecdfa56cff1f661f3c9441ba701c04a983de51a1cafa4a65de5a121a574ad96
content-diff=clean
```

### Crit rewrite of an existing target

Command:

```text
crit install codex-plugin --force
```

Verbatim state evidence:

```text
before mode=644 mtime=1789948800 size=695 sha256=eecdfa56cff1f661f3c9441ba701c04a983de51a1cafa4a65de5a121a574ad96
command-status=0
after mode=644 mtime=1789986570 size=695 sha256=eecdfa56cff1f661f3c9441ba701c04a983de51a1cafa4a65de5a121a574ad96
content-diff=clean
```

Crit was also run with the target absent under umask 002. It created mode 0644, not 0664:

```text
runtime-writer=crit first-create-mode=644 sha256=5d52165ed0bd32c00bc57ecf7073e94b8dd9210e7ea4eef76dabea6bee9d562c
```

Conclusion: the concrete operator-machine 0664 writer remains **UNIDENTIFIED**. The tested candidates excluded by this VM evidence are Codex exec 0.150.1, Claude 2.1.251 `--version`/`-p`, and Crit 0.20.2 existing-target rewrite plus first creation. Authenticated interactive Codex/Claude TUI sessions were not exercised and remain a residual hypothesis.

## Test-first behavior check

Before implementation, the focused test failed because the manifest still selected the managed source name:

```text
test_repository_marketplace_is_a_runtime_owned_seed (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_repository_marketplace_is_a_runtime_owned_seed) ... FAIL

======================================================================
FAIL: test_repository_marketplace_is_a_runtime_owned_seed (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_repository_marketplace_is_a_runtime_owned_seed)
----------------------------------------------------------------------
AssertionError: 'marketplace_path: home/dot_agents/plugins/create_marketplace.json' not found

----------------------------------------------------------------------
Ran 1 test in 0.008s

FAILED (failures=1)
```

After adding the rename and target-exists ignore contract:

```text
test_repository_marketplace_is_a_runtime_owned_seed (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_repository_marketplace_is_a_runtime_owned_seed) ... ok

----------------------------------------------------------------------
Ran 1 test in 0.005s

OK
```

## Design correction evidence

A simple `create_` rename did not satisfy existing-machine ownership. The first VM attempt preserved the old chezmoi entry state and prompted:

```text
legacy-before mode=664 sha256=63d78e89aeaac026e7d04f2522bda4fa46eda624ba4be42683115bd44aea7a0d
=== switch to create source and apply ===
.agents/plugins/marketplace.json has changed since chezmoi last wrote it?
chezmoi: .agents/plugins/marketplace.json: could not open a new TTY: open /dev/tty: no such device or address
scratch-user-removed=yes
```

A proposed `run_once_before` state deletion was rejected after real execution deadlocked on the parent apply's state lock:

```text
chezmoi: timeout obtaining persistent state lock, is another instance of chezmoi running?
chezmoi: .chezmoiscripts/common/02-forget-marketplace-state.sh: exit status 1
scratch-user-removed=yes
```

The final design combines `create_marketplace.json` with a target-exists conditional in `.chezmoiignore`. Chezmoi documents `create_` as ensuring that the file exists and creating it when absent; conditional ignore is what hands off all subsequent content and mode changes.

## Final adh-test acceptance run

The final harness used a VM-local copy, real chezmoi 2.72.0, real Crit 0.20.2, and literal `make update`. Unrelated installers and Herdr bootstrap were stubbed/absent in the scratch copy. No credentials were copied and no login was performed.

### Fresh-machine seed

Verbatim output:

```text
=== fresh-machine create seed ===
fresh-seed-created=yes mode=644 sha256=eecdfa56cff1f661f3c9441ba701c04a983de51a1cafa4a65de5a121a574ad96 expected-sha256=eecdfa56cff1f661f3c9441ba701c04a983de51a1cafa4a65de5a121a574ad96
```

### Existing-machine transition

The legacy target was given valid runtime-only content plus mode 0664. Switching to the new source preserved both byte-for-byte and mode-for-mode and emitted no drift prompt:

```text
=== initialize legacy managed source ===
legacy-before mode=664 sha256=63d78e89aeaac026e7d04f2522bda4fa46eda624ba4be42683115bd44aea7a0d
=== switch to create source and apply ===
legacy-after mode=664 sha256=63d78e89aeaac026e7d04f2522bda4fa46eda624ba4be42683115bd44aea7a0d
legacy-create-warning-count=0
```

### Literal make update drift gate

First update, verbatim relevant output:

```text
=== literal make update: first ===
Notice: local source not pulled (current branch is detached, not main); run 'git -C /home/dotmktgate/dotfiles pull' to fetch remote updates.
chezmoi apply --verbose
Warning: private chezmoi source/config not found. Skipping private dotfiles.
mise install --locked node
mise-stub install --locked node
mise install --locked npm:ccstatusline npm:ccusage
mise-stub install --locked npm:ccstatusline npm:ccusage
./scripts/update-agent-assets.sh

==> Codex Crit plugin
  Installed: /home/dotmktgate/.agents/plugins/marketplace.json
  Skipped:   /home/dotmktgate/.codex/config.toml (Codex plugin already enabled)

Herdr command not found; skipping config reload.
make agmsg-bootstrap
Herdr agents source helper not found; skipping agmsg bootstrap.
first-update-exit=0
```

Because no tested real operation reproduced 0664, the orchestrator-approved adaptation injected the operator-observed mode after the real Crit first-create check:

```text
runtime-writer=crit first-create-mode=644 sha256=5d52165ed0bd32c00bc57ecf7073e94b8dd9210e7ea4eef76dabea6bee9d562c
operator-observed-mode-injection=664
```

Second update and final gate, verbatim relevant output:

```text
=== literal make update: second drift gate ===
Notice: local source not pulled (current branch is detached, not main); run 'git -C /home/dotmktgate/dotfiles pull' to fetch remote updates.
chezmoi apply --verbose
Warning: private chezmoi source/config not found. Skipping private dotfiles.
mise install --locked node
mise-stub install --locked node
mise install --locked npm:ccstatusline npm:ccusage
mise-stub install --locked npm:ccstatusline npm:ccusage
./scripts/update-agent-assets.sh

==> Codex Crit plugin
  Installed: /home/dotmktgate/.agents/plugins/marketplace.json
  Skipped:   /home/dotmktgate/.codex/config.toml (Codex plugin already enabled)

Herdr command not found; skipping config reload.
make agmsg-bootstrap
Herdr agents source helper not found; skipping agmsg bootstrap.
second-update-exit=0
drift-warning-count=0
=== final chezmoi status ===
final-status=clean
scratch-user-removed=yes
```

## Repository validation

Commands:

```text
uv run --with pyyaml scripts/generate-agent-configs.py --check
uv run --with pyyaml scripts/validate-agent-assets.py
make unit-test
git diff --check
```

Verbatim concise output:

```text
generated agent configs are up to date
agent asset validation ok

----------------------------------------------------------------------
Ran 364 tests in 42.079s

OK
git-diff-check=clean
```

An exploratory repository-wide Ruff invocation was not used as a gate because both touched Python files already contain unrelated baseline formatting/lint findings. Its terminal summary was:

```text
2 files would be reformatted
Found 13 errors.
```

## Crit-data review gate

Initial gate output:

```text
Native agent review required before completion.
- tracked policy/config file changed: home/dot_agents/agent-config.yaml
- broad diff touches 9 files
- broad diff changes 258 lines
```

Finding-free approval `r_132f11` was resolved in `.agents/worklog/codex/review/dot-mkt-owner-T1-a01-crit.json`.

Final command:

```text
AGENT_REVIEWED=1 REVIEW_EVIDENCE=.agents/worklog/codex/review/dot-mkt-owner-T1-a01-receipt.md make require-crit-review
```

Verbatim output:

```text
Review requirement satisfied by AGENT_REVIEWED=1 with REVIEW_EVIDENCE.
```

## CompactionDB decision

Command:

```text
python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'dot-mkt-owner-T1-a01: Seed runtime-owned ~/.agents/plugins/marketplace.json with chezmoi create_ and conditionally ignore the target once it exists, because create_ alone still participates in mode/state handling. VM evidence proved fresh byte-identical creation, legacy runtime content/mode preservation, and a second literal make update with zero drift warnings after an injected operator-observed 0664 state. The concrete operator-machine 0664 writer remains unidentified: pinned Codex 0.150.1 exec, Claude 2.1.251 --version/-p, and Crit 0.20.2 create/rewrite did not reproduce it; authenticated interactive TUI sessions remain untested.'
```

Verbatim output:

```text
51b71540-dc8a-4e3b-8d8c-b5be91c6b6b4
```

## Deliberately not run

```text
bats: NOT RUN locally (task and repository policy)
git commit: NOT RUN
git push: NOT RUN
codex login: NOT RUN
claude login: NOT RUN
interactive authenticated Codex/Claude TUI: NOT RUN
```
