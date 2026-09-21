# dot-mkt-mode-T1-a01 validation

review_surface: crit-data
reviewer: codex
review_source: .agents/worklog/codex/review/dot-mkt-mode-T1-a01-crit.json
review_outcome: approved

## Test-first RED

Command:

```text
uv run python tests/unit/test_runtime_health.py RuntimeHealthTest.test_codex_crit_normalizes_managed_marketplace_mode
```

Verbatim output before implementation (exit 1):

```text
F
======================================================================
FAIL: test_codex_crit_normalizes_managed_marketplace_mode (__main__.RuntimeHealthTest.test_codex_crit_normalizes_managed_marketplace_mode)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/mryfmo/Workspace/dotfiles/.claude/worktrees/marketplace-mode/tests/unit/test_runtime_health.py", line 309, in test_codex_crit_normalizes_managed_marketplace_mode
    self.assertEqual(0o644, stat.S_IMODE(marketplace.stat().st_mode))
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 420 != 436

----------------------------------------------------------------------
Ran 1 test in 0.019s

FAILED (failures=1)
```

## Focused GREEN

Command:

```text
uv run python tests/unit/test_runtime_health.py RuntimeHealthTest.test_codex_crit_normalizes_managed_marketplace_mode
```

Verbatim output (exit 0):

```text
.
----------------------------------------------------------------------
Ran 1 test in 0.027s

OK
```

## VM harness corrections

The first credential-free scratch run proved that direct `--source` use needs initialized chezmoi data. It still removed the scratch user:

```text
chezmoi_2.70.4_linux_arm64.tar.gz: OK
=== cycle 1: chezmoi apply ===
chezmoi: warning: config file template has changed, run chezmoi init to regenerate config file
chezmoi: template: .chezmoiignore:6:11: executing ".chezmoiignore" at <.system>: map has no entry for key "system"
userdel: dotmktcheck mail spool (/var/mail/dotmktcheck) not found
scratch-user-removed=yes
```

After adding native `chezmoi init`, Lima exposed its host-mount mode translation: the host 0644 source appeared as 0664 inside the VM. The scratch user was again removed:

```text
chezmoi_2.70.4_linux_arm64.tar.gz: OK
=== cycle 1: chezmoi apply ===
chezmoi: .agents/plugins/marketplace.json: stat /home/dotmktcheck/.agents/plugins: no such file or directory
diff --git a/.agents/plugins/marketplace.json b/.agents/plugins/marketplace.json
new file mode 100664
userdel: dotmktcheck mail spool (/var/mail/dotmktcheck) not found
scratch-user-removed=yes
```

After copying the source into the VM-local scratch filesystem, an intermediate run proved why the writers need their real umasks: first apply under 002 records 0664, so a later normalized 0644 file correctly triggers the opposite mode prompt.

```text
mode=644 path=/home/dotmktcheck/.agents/plugins/marketplace.json
=== cycle 1: content diff ===
content-diff=clean
=== cycle 2: chezmoi apply (drift gate) ===
chezmoi: .agents/plugins/marketplace.json: could not open a new TTY: open /dev/tty: no such device or address
.agents/plugins/marketplace.json has changed since chezmoi last wrote it?
userdel: dotmktcheck mail spool (/var/mail/dotmktcheck) not found
scratch-user-removed=yes
```

The final harness used umask 022 for the chezmoi writer and explicit Ubuntu umask 002 for the Crit writer, matching the operator's old-mode-0644/new-mode-0664 reproduction.

## F2 final adh-test two-cycle proof

Command:

```text
limactl shell adh-test -- bash .orchestration/validation/dot-mkt-mode-T1-a01.md <repo> dotmktcheck
```

The command used the temporary validation path as a shell harness before this evidence replaced it. It downloaded checksum-verified chezmoi 2.70.4, copied the mounted source into the VM-local scratch filesystem, initialized client data, used real pinned Crit, and used `/bin/true` only for the updater's Codex-exists guard. Verbatim output (exit 0):

```text
chezmoi_2.70.4_linux_arm64.tar.gz: OK
=== cycle 1: chezmoi apply ===
diff --git a/.agents/plugins/marketplace.json b/.agents/plugins/marketplace.json
new file mode 100644
index 0000000000000000000000000000000000000000..ea291c482cd03513b1b840fe1a2e82ef61018e5b
--- /dev/null
+++ b/.agents/plugins/marketplace.json
@@ -0,0 +1,32 @@
+{
+  "interface": {
+    "displayName": "mryfmo Personal Plugins"
+  },
+  "name": "mryfmo-personal-plugins",
+  "plugins": [
+    {
+      "category": "Productivity",
+      "name": "mryfmo-dev-workflows",
+      "policy": {
+        "authentication": "ON_INSTALL",
+        "installation": "AVAILABLE"
+      },
+      "source": {
+        "path": "./plugins/mryfmo-dev-workflows",
+        "source": "local"
+      }
+    },
+    {
+      "category": "Developer Tools",
+      "name": "crit",
+      "policy": {
+        "authentication": "ON_INSTALL",
+        "installation": "INSTALLED_BY_DEFAULT"
+      },
+      "source": {
+        "path": "./.codex/plugins/crit",
+        "source": "local"
+      }
+    }
+  ]
+}
=== cycle 1: agent-assets update_codex_crit (umask 002) ===

==> Crit CLI

==> Codex Crit plugin
  Installed: /home/dotmktcheck/.agents/plugins/marketplace.json
  Installed: .agents/skills/crit/SKILL.md
  Installed: .agents/skills/crit-cli/SKILL.md
  Installed: .agents/skills/crit-story/SKILL.md
  Installed: /home/dotmktcheck/.codex/plugins/crit/.codex-plugin/plugin.json
  Installed: /home/dotmktcheck/.codex/plugins/crit/skills/crit/SKILL.md
  Installed: /home/dotmktcheck/.codex/plugins/crit/skills/crit-cli/SKILL.md
  Installed: /home/dotmktcheck/.codex/plugins/crit/skills/crit-story/SKILL.md
  Installed: /home/dotmktcheck/.codex/plugins/crit/hooks/hooks.json
  Installed: /home/dotmktcheck/.codex/plugins/cache/mryfmo-personal-plugins/crit/local
  Installed: /home/dotmktcheck/.codex/config.toml
  Use $crit in Codex to start a review loop
  The crit-cli skill is available to Codex agents when needed
  Use $crit-story in Codex to author a story and continue the review loop
  The Crit plugin is registered in the local Codex plugin marketplace
  The plugin-packaged crit skill is available to Codex as $crit:crit
  The plugin-packaged crit-cli skill is available to Codex agents when needed
  The plugin-packaged crit-story skill is available to Codex as $crit-story
  The Crit plugin includes a Codex Stop hook for proposed-plan review
  The Crit Codex plugin is enabled as crit@mryfmo-personal-plugins

mode=644 path=/home/dotmktcheck/.agents/plugins/marketplace.json
=== cycle 1: content diff ===
content-diff=clean
=== cycle 2: chezmoi apply (drift gate) ===
=== cycle 2: agent-assets update_codex_crit (umask 002) ===

==> Codex Crit plugin
  Installed: /home/dotmktcheck/.agents/plugins/marketplace.json
  Installed: .agents/skills/crit/SKILL.md
  Installed: .agents/skills/crit-cli/SKILL.md
  Installed: .agents/skills/crit-story/SKILL.md
  Installed: /home/dotmktcheck/.codex/plugins/crit/.codex-plugin/plugin.json
  Installed: /home/dotmktcheck/.codex/plugins/crit/skills/crit/SKILL.md
  Installed: /home/dotmktcheck/.codex/plugins/crit/skills/crit-cli/SKILL.md
  Installed: /home/dotmktcheck/.codex/plugins/crit/skills/crit-story/SKILL.md
  Installed: /home/dotmktcheck/.codex/plugins/crit/hooks/hooks.json
  Installed: /home/dotmktcheck/.codex/plugins/cache/mryfmo-personal-plugins/crit/local
  Skipped:   /home/dotmktcheck/.codex/config.toml (Codex plugin already enabled)
  Use $crit in Codex to start a review loop
  The crit-cli skill is available to Codex agents when needed
  Use $crit-story in Codex to author a story and continue the review loop
  The Crit plugin is registered in the local Codex plugin marketplace
  The plugin-packaged crit skill is available to Codex as $crit:crit
  The plugin-packaged crit-cli skill is available to Codex agents when needed
  The plugin-packaged crit-story skill is available to Codex as $crit-story
  The Crit plugin includes a Codex Stop hook for proposed-plan review
  The Crit Codex plugin is enabled as crit@mryfmo-personal-plugins

mode=644 path=/home/dotmktcheck/.agents/plugins/marketplace.json
=== cycle 2: content diff ===
content-diff=clean
=== final chezmoi status ===
final-status=clean
userdel: dotmktcheck mail spool (/var/mail/dotmktcheck) not found
scratch-user-removed=yes
```

The empty span after `=== cycle 2: chezmoi apply (drift gate) ===` is the required no-drift proof. Both real Crit runs produced content identical to the managed source.

## Static checks

Commands, each exit 0 with empty stdout/stderr:

```text
bash -n scripts/update-agent-assets.sh
mise exec shellcheck -- shellcheck -x -e SC1091 scripts/update-agent-assets.sh
mise exec shfmt -- shfmt --indent 4 --space-redirects --diff scripts/update-agent-assets.sh
git diff --check
```

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

## Full Python unit suite

Confirmation command:

```text
set -o pipefail; make unit-test 2>&1 | tail -5
```

Verbatim output:

```text

----------------------------------------------------------------------
Ran 363 tests in 43.314s

OK
```

## CompactionDB decision

Command:

```text
python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'dot-mkt-mode-T1-a01: After crit install codex-plugin rewrites the chezmoi-managed marketplace.json, update_codex_crit must normalize that file to mode 0644; real Crit leaves its content identical to the source, and two consecutive cycles remain drift-free when chezmoi runs with umask 022 and Crit with umask 002.'
```

Verbatim output:

```text
91c32f19-a3a5-495d-9dac-7a3d3bd83658
```

## Crit-data review gate

Initial `make require-crit-review` output (exit 2):

```text
Native agent review required before completion.
- agent lifecycle path changed: scripts/update-agent-assets.sh
```

Finding-free approval `r_b70307` was resolved and saved in the declared JSON evidence path. Final command:

```text
AGENT_REVIEWED=1 REVIEW_EVIDENCE=.agents/worklog/codex/review/dot-mkt-mode-T1-a01-receipt.md make require-crit-review
```

Verbatim output:

```text
Review requirement satisfied by AGENT_REVIEWED=1 with REVIEW_EVIDENCE.
```

## Final scratch cleanup check

Command:

```text
limactl shell adh-test -- bash -lc 'if id -u dotmktcheck > /dev/null 2>&1; then echo scratch-user-present; exit 1; else echo scratch-user-absent; fi'
```

Verbatim output:

```text
scratch-user-absent
```

## Deliberately not run

```text
bats: NOT RUN locally (task and repository policy)
git commit: NOT RUN
git push: NOT RUN
codex login: NOT RUN
```
