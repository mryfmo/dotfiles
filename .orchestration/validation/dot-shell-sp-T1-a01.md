# dot-shell-sp-T1-a01 validation

review_surface: crit-data
reviewer: codex
review_source: .agents/worklog/codex/review/dot-shell-sp-T1-a01-crit.json
review_outcome: approved

## F2 scratch Codex installation

The first install attempt inherited a host-local working directory and therefore selected the wrong local mise config. Its actionable output was:

```text
mise ✗ npm:@openai/codex@0.154.0  2ms · failed: tool 'npm:@openai/codex@0.154.0' requires configured install dependency 'node@26.8.2', but its selected version is not installed
mise ERROR Failed to install npm:@openai/codex@0.154.0: tool 'npm:@openai/codex@0.154.0' requires configured install dependency 'node@26.8.2', but its selected version is not installed
```

The scratch user was recreated, `HOME` and the working directory were isolated, and the repository lock then installed the intended versions:

```text
userdel: dotspcheck mail spool (/var/mail/dotspcheck) not found
mise trusted ~
mise by @jdx – installing 1 tool
mise node@26.7.0 v26.7.0
mise node@26.7.0 11.19.0
mise ✓ node@26.7.0  3.0s  node-v26.7.0-linux-arm64.tar.gz
mise ████████████████ 1/1 · installed 1 tool in 3.0s
mise by @jdx – installing 1 tool
mise npm:@openai/codex@0.150.1 added 2 packages in 5s
mise npm:@openai/codex@0.150.1 Reshimming mise 26.7.0...
mise ✓ npm:@openai/codex@0.150.1  5.1s
mise ████████████████ 1/1 · installed 1 tool in 5.1s
PWD=/home/dotspcheck
HOME=/home/dotspcheck
CONFIG_CODEX="npm:@openai/codex" = "0.150.1"
MISE=2026.9.12 linux-arm64 (2026-09-20)
CODEX=codex-cli 0.150.1
```

## F2 unauthenticated catalog investigation

Command exercised marketplace list, plugin add, configured-Git upgrade, login status, and plugin list in the credential-free scratch user.

Verbatim output:

```text
=== marketplace list ===
No plugin marketplaces in scope.
status=0
=== plugin add ===
Error: plugin `superpowers` was not found in marketplace `openai-curated`
status=1
=== marketplace upgrade ===
Error: marketplace `openai-curated` is not configured as a Git marketplace
status=1
=== login status ===
Not logged in
status=1
=== plugin list json ===
{
  "installed": [],
  "available": []
}
status=0
=== marketplace list after plugin list ===
No plugin marketplaces in scope.
status=0
```

The CLI help identified `marketplace add` as accepting only local or Git sources. Testing the official OpenAI Git URL did not bypass the reserved catalog:

```text
=== add official Git marketplace ===
Error: marketplace `openai-curated` is reserved and cannot be added from this source
status=1
=== marketplace list ===
No plugin marketplaces in scope.
status=0
=== add superpowers ===
Error: plugin `superpowers` was not found in marketplace `openai-curated`
status=1
=== plugin list ===
{
  "installed": [],
  "available": []
}
status=0
=== login status ===
Not logged in
status=1
```

Targeted installed-binary strings corroborated the internal remote path without exposing credentials:

```text
/ps/plugins/list
download curated plugins archive
openai-curated-remote
remote_catalog_auth_required
https://chatgpt.com/backend-api
```

Official OpenAI documentation: `https://learn.chatgpt.com/docs/plugins` documents the Codex CLI `/plugins` browser, lists Superpowers in the curated directory, and states that signing in enables browsing, installation, and management of supported OpenAI-curated plugins.

## Test-first RED

Command:

```text
uv run python -m unittest tests.unit.test_runtime_health.RuntimeHealthTest.test_codex_superpowers_reports_login_step_when_curated_catalog_is_missing
```

Verbatim pre-implementation result:

```text
F
======================================================================
FAIL: test_codex_superpowers_reports_login_step_when_curated_catalog_is_missing (tests.unit.test_runtime_health.RuntimeHealthTest.test_codex_superpowers_reports_login_step_when_curated_catalog_is_missing)
----------------------------------------------------------------------
AssertionError: 'Codex Superpowers was not installed: the OpenAI-curated catalog is unavailable.' not found in '\n==> Codex plugins\nSkipping Codex marketplace upgrade: openai-curated is not a configured Git marketplace.\nSkipping Codex Superpowers plugin: openai-curated is not a configured Git marketplace.\n'

----------------------------------------------------------------------
Ran 1 test in 0.016s

FAILED (failures=1)
```

## F1 live `chsh` validation and cleanup

Verbatim output:

```text
/usr/bin/zsh
=== before ===
dotspcheck:x:1000:1001::/home/dotspcheck:/bin/bash
=== first run ===
Login shell changed to /usr/bin/zsh; sign in again or run `exec zsh`.
=== after first ===
dotspcheck:x:1000:1001::/home/dotspcheck:/usr/bin/zsh
=== second run ===
Login shell is already /usr/bin/zsh.
=== after second ===
dotspcheck:x:1000:1001::/home/dotspcheck:/usr/bin/zsh
=== cleanup ===
userdel: dotspcheck mail spool (/var/mail/dotspcheck) not found
scratch user removed
sudoers entry removed
```

## Final shell/static validation

Command:

```text
bash -n install/ubuntu/client/default_shell.sh scripts/update-agent-assets.sh && mise exec shellcheck -- shellcheck -x -e SC1091 install/ubuntu/client/default_shell.sh scripts/update-agent-assets.sh tests/install/ubuntu/client/default_shell.bats && mise exec shfmt -- shfmt --indent 4 --space-redirects --diff install/ubuntu/client/default_shell.sh scripts/update-agent-assets.sh tests/install/ubuntu/client/default_shell.bats && git diff --check && printf 'shell-static-and-diff: OK\n'
```

Verbatim output:

```text
shell-static-and-diff: OK
```

`SC1091` is excluded because the existing updater resolves its sourced libraries dynamically; the source annotations and `-x` remain enabled. No other ShellCheck finding was excluded.

## Full Python unit suite

Command:

```text
set -o pipefail; make unit-test 2>&1 | tail -5
```

Verbatim output:

```text

----------------------------------------------------------------------
Ran 362 tests in 42.520s

OK
```

An earlier sandboxed rerun could not initialize the shared uv cache; the approved retry above passed. The first complete run also passed 362 tests in 42.934 seconds.

## Agent asset validation

Command:

```text
make validate-agent-assets
```

Verbatim output:

```text
uv run --with pyyaml scripts/validate-agent-assets.py
agent asset validation ok
```

## CompactionDB decision

Command:

```text
python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'dot-shell-sp-T1-a01: Ubuntu client bootstrap must set the login shell to zsh idempotently; Codex openai-curated is a reserved authentication-backed catalog, so unauthenticated fresh installs must attempt the official plugin add and report codex login plus retry instead of treating it as a configurable Git marketplace.'
```

Verbatim output:

```text
6e521a27-d31f-42ac-8b94-13ddc84fc5e4
```

## Crit-data review gate

Initial command `make require-crit-review` required review because the agent lifecycle script and broad diff changed. Codex reviewed the complete diff, added finding-free approval `r_7de074`, resolved it, and saved the repo-local JSON evidence.

The first receipt attempt used an unsupported compound outcome and failed:

```text
AGENT_REVIEWED=1 requires review evidence before completion.
- REVIEW_EVIDENCE agent reviewer requires `review_outcome: approved` or `review_outcome: addressed`
make: *** [require-crit-review] Error 1
```

Final command:

```text
AGENT_REVIEWED=1 REVIEW_EVIDENCE=.agents/worklog/codex/review/dot-shell-sp-T1-a01-receipt.md make require-crit-review
```

Verbatim output:

```text
Review requirement satisfied by AGENT_REVIEWED=1 with REVIEW_EVIDENCE.
```

## Deliberately not run

```text
bats: NOT RUN locally (task and repository policy require CI)
git commit: NOT RUN
git push: NOT RUN
codex login: NOT RUN
```
