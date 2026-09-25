# dot-shell-sp-T1-a01 report

status: ready_for_review
cost: n/a

## Result

- F1: Added an Ubuntu-client-only run-once installer that resolves zsh, adds it to `/etc/shells` when absent, and calls `sudo chsh` only when the account still uses another login shell. Ubuntu servers remain unchanged.
- F1: Added mock-based bats coverage for two-run idempotency, the existing-zsh no-op, and client-only template wiring. Local bats was not run by policy.
- F1: The `adh-test` scratch user changed from `/bin/bash` to `/usr/bin/zsh`; a second run printed the no-op message. The scratch user and temporary sudoers entry were removed and their absence verified.
- F2: **UNRESOLVED for unauthenticated fresh machines.** Codex 0.150.1 reported no marketplace, `plugin add superpowers@openai-curated` could not find the plugin, `marketplace upgrade openai-curated` rejected the source as non-Git, and adding `https://github.com/openai/plugins.git` was rejected because `openai-curated` is reserved.
- F2: [memory:decision] `openai-curated` is an authentication-backed reserved catalog, not a user-configurable Git marketplace. The updater now attempts the supported `codex plugin add` path directly and, when the catalog is unavailable, reports the reason plus `codex login` and the exact retry command. README documents the same manual step.

Official OpenAI documentation confirms that Codex CLI exposes curated plugins through its plugin browser and that signing in is required to browse, install, and manage supported OpenAI-curated plugins. Superpowers appears in that curated directory.

## Validation

- Passed bash syntax, ShellCheck, repository shfmt settings, and `git diff --check`.
- Passed all 362 Python unit tests and `make validate-agent-assets`.
- Passed the required Crit-data review with resolved approval `r_7de074`.
- Full verbatim evidence is in `.orchestration/validation/dot-shell-sp-T1-a01.md`.

## Manual completion for F2

```shell
codex login
codex plugin add superpowers@openai-curated
```

Start a new Codex session after installation.

## CompactionDB

Command:

```text
python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'dot-shell-sp-T1-a01: Ubuntu client bootstrap must set the login shell to zsh idempotently; Codex openai-curated is a reserved authentication-backed catalog, so unauthenticated fresh installs must attempt the official plugin add and report codex login plus retry instead of treating it as a configurable Git marketplace.'
```

Memory ID: `6e521a27-d31f-42ac-8b94-13ddc84fc5e4`

## Constraints honored

- No commit or push.
- No local bats execution.
- No Codex login and no credentials copied to the VM.
- VM work used only `limactl shell adh-test`.
- No mise config or lock changes.
- Scratch user and temporary sudoers state were removed.
- No persistent external side effects remain.
