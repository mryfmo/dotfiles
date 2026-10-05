# Validation: dot-ua-graph-refresh-T55-a01

- PR: #226 https://github.com/mryfmo/dotfiles/pull/226
- PR head SHA: 98bdf43ff966f4b73dd25832d1f77c1196dc0bdb (branch chore/ua-graph-refresh-T55, base origin/main 940a3a2b07adfd14140a0acff96784ef53a0a509)
- Node/edge counts: before 885 nodes / 1325 edges (origin/main graph at 72b89015); after 984 nodes / 1774 edges
- meta gitCommitHash = 940a3a2b (source HEAD the build ran on); branch HEAD 98bdf43f = that commit + one .ua-only commit (see report "gitCommitHash vs branch HEAD")

## Task validation commands (verbatim)

```
$ jq -r .gitCommitHash .ua/meta.json
940a3a2b07adfd14140a0acff96784ef53a0a509
$ git rev-parse HEAD
98bdf43ff966f4b73dd25832d1f77c1196dc0bdb
$ git diff --name-only $(jq -r .gitCommitHash .ua/meta.json)..HEAD | head
.ua/fingerprints.json
.ua/knowledge-graph.json
.ua/meta.json
$ git show origin/main:.ua/knowledge-graph.json > "$TMPDIR/kg-old.json"
(exit 0)
$ ua-symbol-coverage "$TMPDIR/kg-old.json" .ua/knowledge-graph.json --old-ref 72b890157078c583f45d71a61ee6eba0df86afb5 --repo-ref "$(git rev-parse HEAD)"
| file | old | new | def-like lines | status | note |
|---|---|---|---|---|---|
| .chezmoiroot | 0 | 0 | - | ok |  |
| .claude/contextdb/config.json | 0 | 0 | - | ok |  |
| .claude/contextdb/contextdb/__init__.py | 0 | 0 | 0 | ok |  |
| .claude/contextdb/contextdb/cli.py | 4 | 9 | 9 | ok |  |
| .claude/contextdb/contextdb/config.py | 3 | 6 | 6 | ok |  |
| .claude/contextdb/contextdb/hook.py | 2 | 2 | 2 | ok |  |
| .claude/contextdb/contextdb/memory.py | 3 | 4 | 5 | ok |  |
| .claude/contextdb/contextdb/normalize.py | 5 | 6 | 6 | ok |  |
| .claude/contextdb/contextdb/paths.py | 4 | 5 | 5 | ok |  |
| .claude/contextdb/contextdb/probe.py | 1 | 1 | 1 | ok |  |
| .claude/contextdb/contextdb/recall.py | 5 | 8 | 8 | ok |  |
| .claude/contextdb/contextdb/recover_hook.py | 3 | 3 | 3 | ok |  |
| .claude/contextdb/contextdb/recovery.py | 4 | 4 | 4 | ok |  |
| .claude/contextdb/contextdb/redaction.py | 6 | 8 | 10 | ok |  |
| .claude/contextdb/contextdb/semantic.py | 4 | 4 | 4 | ok |  |
| .claude/contextdb/contextdb/spool.py | 6 | 9 | 12 | ok |  |
| .claude/contextdb/contextdb/storage.py | 25 | 25 | 34 | ok |  |
| .claude/contextdb/contextdb/util.py | 19 | 20 | 20 | ok |  |
| .claude/contextdb/health/.gitkeep | 0 | 0 | - | ok |  |
| .claude/contextdb/spool/incoming/.gitkeep | 0 | 0 | - | ok |  |
| .claude/contextdb/spool/quarantine/.gitkeep | 0 | 0 | - | ok |  |
| .claude/contextdb/state/.gitkeep | 0 | 0 | - | ok |  |
| .claude/hooks/contextdb_cli.py | 0 | 0 | 0 | ok |  |
| .claude/hooks/contextdb_hook.py | 0 | 0 | 0 | ok |  |
| .claude/hooks/contextdb_recover.py | 0 | 0 | 0 | ok |  |
| .claude/hooks/query_log.py | 0 | 0 | 0 | ok |  |
| .claude/settings.json | 0 | 0 | - | ok |  |
| .coderabbit.yaml | 0 | 0 | - | ok |  |
| .github/copilot-instructions.md | 0 | 0 | - | ok |  |
| .github/funding.yaml | 0 | 0 | - | ok |  |
| .github/workflows/agent-assets.yml | 0 | 0 | - | ok |  |
| .github/workflows/docs.yml | 0 | 0 | - | ok |  |
| .github/workflows/macos.yaml | 0 | 0 | - | ok |  |
| .github/workflows/remote.yaml | 0 | 0 | - | ok |  |
| .github/workflows/test.yaml | 0 | 0 | - | ok |  |
| .github/workflows/ubuntu.yaml | 0 | 0 | - | ok |  |
| .simplecov | 0 | 0 | - | ok |  |
| .ua/config.json | 0 | 0 | - | ok |  |
| .ua/fingerprints.json | 0 | 0 | - | ok |  |
| .ua/knowledge-graph.json | 0 | 0 | - | ok |  |
| .ua/meta.json | 0 | 0 | - | ok |  |
| AGENTS.md | 0 | 0 | - | ok |  |
| CLAUDE.md | 0 | 0 | - | ok |  |
| Dockerfile | 0 | 0 | - | ok |  |
| Makefile | 0 | 0 | - | ok |  |
| README.md | 0 | 0 | - | ok |  |
| codecov.yml | 0 | 0 | - | ok |  |
| docs/assets/stylesheets/extra.css | 0 | 0 | - | ok |  |
| docs/plans/nix-first-architecture.md | 0 | 0 | - | ok |  |
| docs/plans/nix-migration.md | 0 | 0 | - | ok |  |
| docs/verification/acceptance/005.md | 0 | 0 | - | ok |  |
| flake.nix | 0 | 0 | - | ok |  |
| home/.chezmoi.yaml.tmpl | 0 | 0 | - | ok |  |
| home/.chezmoiexternal.yaml.tmpl | 0 | 0 | - | ok |  |
| home/.chezmoiignore | 0 | 0 | - | ok |  |
| home/.chezmoiremove | 0 | 0 | - | ok |  |
| home/.chezmoiscripts/common/run_once_after_01-setup-chezmoi-private.sh.tmpl | 0 | 0 | - | ok |  |
| home/.chezmoiscripts/common/run_once_after_02-install-mise.sh.tmpl | 0 | 0 | 0 | ok |  |
| home/.chezmoiscripts/common/run_once_after_03-install-sheldon.sh.tmpl | 0 | 0 | 0 | ok |  |
| home/.chezmoiscripts/common/run_once_after_06-install-agent-assets.sh.tmpl | 0 | 0 | 0 | ok |  |
| home/.chezmoiscripts/common/run_once_after_99-install-gh-extensions.sh.tmpl | 0 | 0 | 0 | ok |  |
| home/.chezmoiscripts/common/run_once_before_01-decrypt-private-key.sh.tmpl | 1 | 1 | 3 | ok |  |
| home/.chezmoiscripts/macos/run_once_04-install-ghostty.sh.tmpl | 0 | 0 | - | ok |  |
| home/.chezmoiscripts/macos/run_once_10-install-docker.sh.tmpl | 0 | 0 | - | ok |  |
| home/.chezmoiscripts/macos/run_once_99-install-defaults.sh.tmpl | 0 | 0 | - | ok |  |
| home/.chezmoiscripts/macos/run_once_after_50-install-misc.sh.tmpl | 0 | 0 | - | ok |  |
| home/.chezmoiscripts/macos/run_once_before_01-prepare-system.sh.tmpl | 0 | 0 | - | ok |  |
| home/.chezmoiscripts/macos/run_once_before_02-install-command-line-tool.sh.tmpl | 0 | 0 | - | ok |  |
| home/.chezmoiscripts/macos/run_once_before_03-install-brew.sh.tmpl | 0 | 0 | - | ok |  |
| home/.chezmoiscripts/macos/run_once_before_50-install-dependencies.sh.tmpl | 0 | 0 | - | ok |  |
| home/.chezmoiscripts/ubuntu/run_once_00-setup-ssh.sh.tmpl | 0 | 0 | - | ok |  |
| home/.chezmoiscripts/ubuntu/run_once_10-install-docker.sh.tmpl | 0 | 0 | - | ok |  |
| home/.chezmoiscripts/ubuntu/run_once_10-install-starship.sh.tmpl | 0 | 0 | - | ok |  |
| home/.chezmoiscripts/ubuntu/run_once_50-client-install-misc.sh.tmpl | 0 | 0 | 0 | ok |  |
| home/.chezmoiscripts/ubuntu/run_once_50-server-docker-ssh.sh.tmpl | 0 | 0 | - | ok |  |
| home/.chezmoiscripts/ubuntu/run_once_50-server-install-mics.sh.tmpl | 0 | 0 | - | ok |  |
| home/.chezmoiscripts/ubuntu/run_once_50-server-setup-timezone.sh.tmpl | 0 | 0 | - | ok |  |
| home/.chezmoiscripts/ubuntu/run_once_50-setup-locale.sh.tmpl | 0 | 0 | - | ok |  |
| home/.chezmoiscripts/ubuntu/run_once_51-client-default-shell.sh.tmpl | 0 | 0 | 0 | ok |  |
| home/.chezmoiscripts/ubuntu/run_once_52-client-install-zed.sh.tmpl | 0 | 0 | 0 | ok |  |
| home/.chezmoiscripts/ubuntu/run_once_53-client-install-tailscale.sh.tmpl | 0 | 0 | - | ok |  |
| home/.chezmoiscripts/ubuntu/run_once_99-client-gnome-defaults.sh.tmpl | 0 | 0 | - | ok |  |
| home/.chezmoiscripts/ubuntu/run_once_after_04-install-aws-cli.sh.tmpl | 0 | 0 | - | ok |  |
| home/.chezmoiscripts/ubuntu/run_once_before_50-common-dependencies.sh.tmpl | 0 | 0 | - | ok |  |
| home/.chezmoiscripts/ubuntu/run_onchange_after_07-apparmor-bwrap-userns.sh.tmpl | 0 | 0 | - | ok |  |
| home/.chezmoiscripts/ubuntu/run_onchange_after_60-enable-usage-snapshot-timer.sh.tmpl | 0 | 0 | 0 | ok |  |
| home/.chezmoitemplates/chezmoiexternal.d/common.yaml.tmpl | 0 | 0 | - | ok |  |
| home/.chezmoitemplates/chezmoiexternal.d/macos.yaml.tmpl | 0 | 0 | - | ok |  |
| home/.chezmoitemplates/chezmoiexternal.d/ubuntu.yaml.tmpl | 0 | 0 | - | ok |  |
| home/.chezmoitemplates/chezmoiignore.d/common | 0 | 0 | - | ok |  |
| home/.chezmoitemplates/chezmoiignore.d/macos | 0 | 0 | - | ok |  |
| home/.chezmoitemplates/chezmoiignore.d/ubuntu/client | 0 | 0 | - | ok |  |
| home/.chezmoitemplates/chezmoiignore.d/ubuntu/common | 0 | 0 | - | ok |  |
| home/.chezmoitemplates/chezmoiignore.d/ubuntu/server | 0 | 0 | - | ok |  |
| home/.chezmoitemplates/claude-settings-managed.json | 0 | 0 | - | ok |  |
| home/.chezmoitemplates/codex-config-managed.toml | 0 | 0 | - | ok |  |
| home/.key.txt.age | 0 | 0 | - | ok |  |
| home/Library/LaunchAgents/com.mryfmo.dotfiles.usage-snapshot.plist.tmpl | 0 | 0 | - | ok |  |
| home/dot_agents/README.md | 0 | 0 | - | ok |  |
| home/dot_agents/agent-config.yaml | 0 | 0 | - | ok |  |
| home/dot_agents/model-profiles.env | 0 | 0 | - | ok |  |
| home/dot_agents/permgate-policy.yaml | 0 | 0 | - | ok |  |
| home/dot_agents/plugins/create_marketplace.json | 0 | 0 | - | ok |  |
| home/dot_agents/plugins/mryfmo-dev-workflows/.codex-plugin/plugin.json | 0 | 0 | - | ok |  |
| home/dot_agents/skills/agmsg-orchestration/SKILL.md | 0 | 0 | - | ok |  |
| home/dot_agents/skills/convert-to-transformers/SKILL.md | 0 | 0 | - | ok |  |
| home/dot_agents/skills/convert-to-transformers/references/common-pitfalls.md | 0 | 0 | - | ok |  |
| home/dot_agents/skills/convert-to-transformers/references/learnings.md | 0 | 0 | - | ok |  |
| home/dot_agents/skills/gh-comment-attach-files/SKILL.md | 0 | 0 | - | ok |  |
| home/dot_agents/skills/gh-comment-attach-files/agents/openai.yaml | 0 | 0 | - | ok |  |
| home/dot_agents/skills/gh-comment-attach-files/scripts/attach_comment_files.py | 24 | 24 | 24 | ok |  |
| home/dot_agents/skills/gh-first-workflow/SKILL.md | 0 | 0 | - | ok |  |
| home/dot_agents/skills/gh-first-workflow/agents/openai.yaml | 0 | 0 | - | ok |  |
| home/dot_agents/skills/gh-first-workflow/references/gh-git-rules.md | 0 | 0 | - | ok |  |
| home/dot_agents/skills/humanizer-ja/SKILL.md | 0 | 0 | - | ok |  |
| home/dot_agents/skills/humanizer-ja/agents/openai.yaml | 0 | 0 | - | ok |  |
| home/dot_agents/skills/humanizer-ja/references/ai-patterns-ja.md | 0 | 0 | - | ok |  |
| home/dot_agents/skills/python-uv-workflow/SKILL.md | 0 | 0 | - | ok |  |
| home/dot_agents/skills/python-uv-workflow/agents/openai.yaml | 0 | 0 | - | ok |  |
| home/dot_agents/skills/python-uv-workflow/references/python-uv-rules.md | 0 | 0 | - | ok |  |
| home/dot_agents/skills/shdoc-shell-docs/SKILL.md | 0 | 0 | - | ok |  |
| home/dot_agents/skills/shdoc-shell-docs/agents/openai.yaml | 0 | 0 | - | ok |  |
| home/dot_agents/skills/shdoc-shell-docs/references/shdoc-rules.md | 0 | 0 | - | ok |  |
| home/dot_bash/client/bashrc | 0 | 0 | 0 | ok |  |
| home/dot_bash/server/bashrc | 0 | 0 | 0 | ok |  |
| home/dot_ccstatusline/settings.json | 0 | 0 | - | ok |  |
| home/dot_claude/agents/express-explorer.md | 0 | 0 | - | ok |  |
| home/dot_claude/commands/commit.md | 0 | 0 | - | ok |  |
| home/dot_claude/hooks/executable_enforce-uv.sh | 8 | 8 | 8 | ok |  |
| home/dot_claude/hooks/executable_format-edited-files.py | 2 | 2 | 3 | ok |  |
| home/dot_claude/modify_private_settings.json | 7 | 7 | 12 | ok |  |
| home/dot_claude/private_mcp.json.tmpl | 0 | 0 | - | ok |  |
| home/dot_claude/rules/symlink_agmsg-orchestration.md.tmpl | 0 | 0 | - | ok |  |
| home/dot_claude/rules/symlink_ask-user-question.md.tmpl | 0 | 0 | - | ok |  |
| home/dot_claude/rules/symlink_compactiondb.md.tmpl | 0 | 0 | - | ok |  |
| home/dot_claude/rules/symlink_crit-review.md.tmpl | 0 | 0 | - | ok |  |
| home/dot_claude/rules/symlink_gpu.md.tmpl | 0 | 0 | - | ok |  |
| home/dot_claude/rules/symlink_latex.md.tmpl | 0 | 0 | - | ok |  |
| home/dot_claude/rules/symlink_model-selection.md.tmpl | 0 | 0 | - | ok |  |
| home/dot_claude/rules/symlink_ponytail.md.tmpl | 0 | 0 | - | ok |  |
| home/dot_claude/rules/symlink_pr-integration.md.tmpl | 0 | 0 | - | ok |  |
| home/dot_claude/rules/symlink_python.md.tmpl | 0 | 0 | 0 | ok |  |
| home/dot_claude/rules/symlink_understand-anything.md.tmpl | 0 | 0 | - | ok |  |
| home/dot_claude/skills/agmsg-orchestration/symlink_SKILL.md.tmpl | 0 | 0 | - | ok |  |
| home/dot_claude/skills/convert-to-transformers/references/symlink_common-pitfalls.md.tmpl | 0 | 0 | - | ok |  |
| home/dot_claude/skills/convert-to-transformers/references/symlink_learnings.md.tmpl | 0 | 0 | - | ok |  |
| home/dot_claude/skills/convert-to-transformers/symlink_SKILL.md.tmpl | 0 | 0 | - | ok |  |
| home/dot_claude/skills/gh-comment-attach-files/agents/symlink_openai.yaml.tmpl | 0 | 0 | - | ok |  |
| home/dot_claude/skills/gh-comment-attach-files/scripts/symlink_attach_comment_files.py.tmpl | 0 | 0 | - | ok |  |
| home/dot_claude/skills/gh-comment-attach-files/symlink_SKILL.md.tmpl | 0 | 0 | - | ok |  |
| home/dot_claude/skills/gh-first-workflow/agents/symlink_openai.yaml.tmpl | 0 | 0 | - | ok |  |
| home/dot_claude/skills/gh-first-workflow/references/symlink_gh-git-rules.md.tmpl | 0 | 0 | - | ok |  |
| home/dot_claude/skills/gh-first-workflow/symlink_SKILL.md.tmpl | 0 | 0 | - | ok |  |
| home/dot_claude/skills/humanizer-ja/agents/symlink_openai.yaml.tmpl | 0 | 0 | - | ok |  |
| home/dot_claude/skills/humanizer-ja/references/symlink_ai-patterns-ja.md.tmpl | 0 | 0 | - | ok |  |
| home/dot_claude/skills/humanizer-ja/symlink_SKILL.md.tmpl | 0 | 0 | - | ok |  |
| home/dot_claude/skills/python-uv-workflow/agents/symlink_openai.yaml.tmpl | 0 | 0 | 0 | ok |  |
| home/dot_claude/skills/python-uv-workflow/references/symlink_python-uv-rules.md.tmpl | 0 | 0 | 0 | ok |  |
| home/dot_claude/skills/python-uv-workflow/symlink_SKILL.md.tmpl | 0 | 0 | 0 | ok |  |
| home/dot_claude/skills/shdoc-shell-docs/agents/symlink_openai.yaml.tmpl | 0 | 0 | - | ok |  |
| home/dot_claude/skills/shdoc-shell-docs/references/symlink_shdoc-rules.md.tmpl | 0 | 0 | - | ok |  |
| home/dot_claude/skills/shdoc-shell-docs/symlink_SKILL.md.tmpl | 0 | 0 | - | ok |  |
| home/dot_codex/modify_private_adh.config.toml | 0 | 0 | 7 | ok |  |
| home/dot_codex/modify_private_audit.config.toml | 0 | 0 | 7 | ok |  |
| home/dot_codex/modify_private_config.toml | 0 | 0 | 10 | ok |  |
| home/dot_codex/modify_private_deep.config.toml | 0 | 0 | 7 | ok |  |
| home/dot_codex/modify_private_express.config.toml | 0 | 0 | 6 | ok |  |
| home/dot_codex/modify_private_review.config.toml | 0 | 0 | 6 | ok |  |
| home/dot_codex/modify_private_security.config.toml | 0 | 0 | 7 | ok |  |
| home/dot_codex/modify_private_standard.config.toml | 0 | 0 | 7 | ok |  |
| home/dot_codex/symlink_AGENTS.md.tmpl | 0 | 0 | - | ok |  |
| home/dot_config/alias/client.sh | 0 | 0 | 0 | ok |  |
| home/dot_config/alias/common.sh | 0 | 0 | 0 | ok |  |
| home/dot_config/alias/server.sh | 0 | 0 | 0 | ok |  |
| home/dot_config/ccstatusline/symlink_settings.json.tmpl | 0 | 0 | - | ok |  |
| home/dot_config/claude/rules/agmsg-orchestration.md | 0 | 0 | - | ok |  |
| home/dot_config/claude/rules/ask-user-question.md | 0 | 0 | - | ok |  |
| home/dot_config/claude/rules/compactiondb.md | 0 | 0 | - | ok |  |
| home/dot_config/claude/rules/crit-review.md | 0 | 0 | - | ok |  |
| home/dot_config/claude/rules/gpu.md | 0 | 0 | - | ok |  |
| home/dot_config/claude/rules/latex.md | 0 | 0 | - | ok |  |
| home/dot_config/claude/rules/model-selection.md | 0 | 0 | - | ok |  |
| home/dot_config/claude/rules/ponytail.md | 0 | 0 | - | ok |  |
| home/dot_config/claude/rules/pr-integration.md | 0 | 0 | - | ok |  |
| home/dot_config/claude/rules/python.md | 0 | 0 | - | ok |  |
| home/dot_config/claude/rules/understand-anything.md | 0 | 0 | - | ok |  |
| home/dot_config/codex/AGENTS.md | 0 | 0 | - | ok |  |
| home/dot_config/ghostty/config | 0 | 0 | - | ok |  |
| home/dot_config/git/config.tmpl | 0 | 0 | - | ok |  |
| home/dot_config/git/ignore | 0 | 0 | - | ok |  |
| home/dot_config/gwq/config.toml | 0 | 0 | - | ok |  |
| home/dot_config/herdr/config.toml | 0 | 0 | - | ok |  |
| home/dot_config/herdr/plugins/config/herdr-file-viewer/config.toml | 0 | 0 | - | ok |  |
| home/dot_config/mise/config.toml.tmpl | 0 | 0 | - | ok |  |
| home/dot_config/mise/mise.lock.tmpl | 0 | 0 | - | ok |  |
| home/dot_config/powerlevel10k/p10k.zsh | 2 | 2 | 5 | ok |  |
| home/dot_config/sheldon/plugin_sources/client/common.toml | 0 | 0 | - | ok |  |
| home/dot_config/sheldon/plugin_sources/client/macos.toml | 0 | 0 | - | ok |  |
| home/dot_config/sheldon/plugin_sources/client/ubuntu.toml | 0 | 0 | - | ok |  |
| home/dot_config/sheldon/plugin_sources/common.toml | 0 | 0 | - | ok |  |
| home/dot_config/sheldon/plugin_sources/server.toml | 0 | 0 | - | ok |  |
| home/dot_config/sheldon/plugins.toml.tmpl | 0 | 0 | - | ok |  |
| home/dot_config/starship.toml | 0 | 0 | - | ok |  |
| home/dot_config/systemd/user/usage-snapshot.service.tmpl | 0 | 0 | - | ok |  |
| home/dot_config/systemd/user/usage-snapshot.timer.tmpl | 0 | 0 | - | ok |  |
| home/dot_config/tango.yml | 0 | 0 | - | ok |  |
| home/dot_config/uv/uv.toml | 0 | 0 | - | ok |  |
| home/dot_config/yazi/yazi.toml | 0 | 0 | - | ok |  |
| home/dot_config/zed/keymap.json | 0 | 0 | - | ok |  |
| home/dot_config/zed/settings.json | 0 | 0 | - | ok |  |
| home/dot_config/zsh/plugins/chezmoi-notify/chezmoi-notify.plugin.zsh | 1 | 1 | 1 | ok |  |
| home/dot_local/bin/common/executable_agent-fanout | 2 | 2 | 2 | ok |  |
| home/dot_local/bin/common/executable_agent-session-staleness | 8 | 8 | 13 | ok |  |
| home/dot_local/bin/common/executable_agmsg-dispatch | 1 | 1 | 4 | ok |  |
| home/dot_local/bin/common/executable_cdgwq | 0 | 0 | 1 | ok |  |
| home/dot_local/bin/common/executable_cdw | 1 | 1 | 1 | ok |  |
| home/dot_local/bin/common/executable_chezmoi-cd | 0 | 0 | 1 | ok |  |
| home/dot_local/bin/common/executable_compactiondb-install | 0 | 0 | 0 | ok |  |
| home/dot_local/bin/common/executable_contextdb-codex-notify | 0 | 0 | 0 | ok |  |
| home/dot_local/bin/common/executable_dev | 1 | 1 | 2 | ok |  |
| home/dot_local/bin/common/executable_fgc | 0 | 0 | 1 | ok |  |
| home/dot_local/bin/common/executable_git-delete-merged-branches | 1 | 1 | 3 | ok |  |
| home/dot_local/bin/common/executable_herdr-agents | 34 | 44 | 62 | ok |  |
| home/dot_local/bin/common/executable_herdr-session | 0 | 0 | 1 | ok |  |
| home/dot_local/bin/common/executable_permgate | 16 | 16 | 25 | ok |  |
| home/dot_local/bin/common/executable_provision-machine-key | 2 | 2 | 4 | ok |  |
| home/dot_local/bin/common/executable_remove-agent-asset | 11 | 11 | 21 | ok |  |
| home/dot_local/bin/common/executable_setup-gh | 2 | 2 | 5 | ok |  |
| home/dot_local/bin/common/executable_setup-gpg | 1 | 1 | 3 | ok |  |
| home/dot_local/bin/common/executable_setup-python-env | 0 | 0 | 3 | ok |  |
| home/dot_local/bin/common/executable_ua-symbol-coverage | 0 | 6 | 11 | ok |  |
| home/dot_local/bin/common/executable_uv-format | 0 | 0 | 1 | ok |  |
| home/dot_local/bin/server/cache.sh | 0 | 0 | 0 | ok |  |
| home/dot_local/bin/server/cuda.sh | 0 | 0 | 0 | ok |  |
| home/dot_local/bin/server/history.sh | 1 | 1 | 2 | ok |  |
| home/dot_local/bin/server/ssh_agent.sh | 1 | 1 | 1 | ok |  |
| home/dot_local/share/aws-cli-keys/aws-cli-public-key.asc | 0 | 0 | - | ok |  |
| home/dot_mise/config.toml | 0 | 0 | - | ok |  |
| home/dot_npmrc | 0 | 0 | - | ok |  |
| home/dot_profile | 0 | 0 | - | ok |  |
| home/dot_vimrc | 0 | 0 | - | ok |  |
| home/dot_zprofile | 0 | 0 | 0 | ok |  |
| home/dot_zshenv | 0 | 0 | 0 | ok |  |
| home/dot_zshrc | 0 | 2 | 2 | ok |  |
| home/private_dot_gnupg/gpg-agent.conf.tmpl | 0 | 0 | - | ok |  |
| home/private_dot_ssh/private_config | 0 | 0 | - | ok |  |
| home/symlink_dot_bashrc.tmpl | 0 | 0 | - | ok |  |
| install/common/chezmoi_private.sh | 1 | 1 | 3 | ok |  |
| install/common/gh_extensions.sh | 1 | 1 | 3 | ok |  |
| install/common/mise.sh | 4 | 4 | 8 | ok |  |
| install/common/sheldon.sh | 1 | 1 | 3 | ok |  |
| install/macos/arm64/prepare_arm64_system.sh | 0 | 0 | 2 | ok |  |
| install/macos/arm64/run.sh | 0 | 0 | 1 | ok |  |
| install/macos/common/brew.sh | 1 | 1 | 4 | ok |  |
| install/macos/common/command_line_tool.sh | 1 | 1 | 2 | ok |  |
| install/macos/common/defaults.sh | 7 | 7 | 16 | ok |  |
| install/macos/common/dependencies.sh | 1 | 1 | 3 | ok |  |
| install/macos/common/docker.sh | 0 | 0 | 3 | ok |  |
| install/macos/common/ghostty.sh | 0 | 0 | 4 | ok |  |
| install/macos/common/misc.sh | 2 | 2 | 5 | ok |  |
| install/ubuntu/client/default_shell.sh | 1 | 1 | 1 | ok |  |
| install/ubuntu/client/docker.sh | 3 | 3 | 6 | ok |  |
| install/ubuntu/client/ghostty.sh | 0 | 0 | 5 | ok |  |
| install/ubuntu/client/gnome_settings.sh | 1 | 1 | 9 | ok |  |
| install/ubuntu/client/misc.sh | 0 | 0 | 4 | ok |  |
| install/ubuntu/client/tailscale.sh | 2 | 2 | 4 | ok |  |
| install/ubuntu/client/zed.sh | 3 | 3 | 5 | ok |  |
| install/ubuntu/common/apparmor/bwrap-userns | 0 | 0 | - | ok |  |
| install/ubuntu/common/apparmor_userns.sh | 4 | 4 | 4 | ok |  |
| install/ubuntu/common/aws_cli.sh | 3 | 3 | 5 | ok |  |
| install/ubuntu/common/dependencies.sh | 3 | 3 | 4 | ok |  |
| install/ubuntu/common/setup_locale.sh | 1 | 1 | 1 | ok |  |
| install/ubuntu/common/ssh.sh | 0 | 0 | 4 | ok |  |
| install/ubuntu/server/misc.sh | 0 | 0 | 4 | ok |  |
| install/ubuntu/server/setup_timezone.sh | 0 | 0 | 1 | ok |  |
| install/ubuntu/server/ssh_server.sh | 2 | 2 | 5 | ok |  |
| install/ubuntu/server/starship.sh | 2 | 2 | 4 | ok |  |
| mise.toml | 0 | 0 | - | ok |  |
| mkdocs.yml | 0 | 0 | - | ok |  |
| nix/home-manager/default.nix | 0 | 0 | - | ok |  |
| nix/nix-darwin/default.nix | 0 | 0 | - | ok |  |
| nix/shared/packages.nix | 0 | 0 | - | ok |  |
| plans/001-contain-starship-cleanup.md | 0 | 0 | - | ok |  |
| plans/002-make-review-evidence-non-vacuous.md | 0 | 0 | - | ok |  |
| plans/003-make-bootstrap-safe-and-publicly-testable.md | 0 | 0 | - | ok |  |
| plans/004-harden-and-lock-the-supply-chain.md | 0 | 0 | - | ok |  |
| plans/005-make-runtime-health-and-verification-truthful.md | 0 | 0 | - | ok |  |
| plans/README.md | 0 | 0 | - | ok |  |
| renovate.json | 0 | 0 | - | ok |  |
| scripts/check-agent-runtime.py | 17 | 19 | 39 | ok |  |
| scripts/check-regime-boundary.sh | 0 | 1 | 1 | ok |  |
| scripts/check-statusline-tools.py | 2 | 2 | 3 | ok |  |
| scripts/check-tools.sh | 8 | 14 | 14 | ok |  |
| scripts/generate-agent-configs.py | 19 | 19 | 37 | ok |  |
| scripts/generate-docs.sh | 24 | 34 | 34 | ok |  |
| scripts/lib/asset-manifest.sh | 2 | 5 | 5 | ok |  |
| scripts/lib/installer-pins.sh | 0 | 0 | 0 | ok |  |
| scripts/pr-feedback.py | 5 | 5 | 11 | ok |  |
| scripts/refresh-mkdocs-toc.py | 0 | 0 | 1 | ok |  |
| scripts/require-crit-review.py | 11 | 13 | 24 | ok |  |
| scripts/run_bashcov_unit_test.rb | 3 | 3 | 3 | ok |  |
| scripts/run_benchmark.sh | 4 | 8 | 8 | ok |  |
| scripts/run_unit_test.sh | 2 | 4 | 4 | ok |  |
| scripts/update-agent-assets.sh | 30 | 41 | 41 | ok |  |
| scripts/upgrade-tools.sh | 22 | 35 | 35 | ok |  |
| scripts/usage-report.py | 10 | 10 | 16 | ok |  |
| scripts/usage-snapshot.sh | 0 | 0 | 0 | ok |  |
| scripts/validate-agent-assets.py | 33 | 34 | 44 | ok |  |
| setup.sh | 12 | 12 | 25 | ok |  |
| tests/files/common.bats | 0 | 0 | 0 | ok |  |
| tests/files/helpers.bash | 1 | 1 | 5 | ok |  |
| tests/files/macos.bats | 0 | 0 | 1 | ok |  |
| tests/files/ubuntu.bats | 0 | 0 | 2 | ok |  |
| tests/install/common/check_tools.bats | 0 | 0 | 1 | ok |  |
| tests/install/common/chezmoi_private.bats | 0 | 0 | 2 | ok |  |
| tests/install/common/decrypt_private_key.bats | 1 | 1 | 6 | ok |  |
| tests/install/common/gh_extensions.bats | 0 | 0 | 6 | ok |  |
| tests/install/common/lifecycle.bats | 1 | 1 | 1 | ok |  |
| tests/install/common/mise.bats | 0 | 0 | 8 | ok |  |
| tests/install/common/private_layer.bats | 0 | 0 | 9 | ok |  |
| tests/install/common/provision_machine_key.bats | 0 | 0 | 3 | ok |  |
| tests/install/common/setup.bats | 2 | 2 | 10 | ok |  |
| tests/install/macos/common/brew.bats | 0 | 0 | 1 | ok |  |
| tests/install/macos/common/defaults.bats | 0 | 0 | 1 | ok |  |
| tests/install/macos/common/docker.bats | 0 | 0 | 3 | ok |  |
| tests/install/macos/common/ghostty.bats | 0 | 0 | 2 | ok |  |
| tests/install/macos/common/misc.bats | 0 | 0 | 4 | ok |  |
| tests/install/ubuntu/client/default_shell.bats | 0 | 0 | 7 | ok |  |
| tests/install/ubuntu/client/docker.bats | 0 | 0 | 6 | ok |  |
| tests/install/ubuntu/client/ghostty.bats | 0 | 0 | 2 | ok |  |
| tests/install/ubuntu/client/gnome_settings.bats | 0 | 0 | 4 | ok |  |
| tests/install/ubuntu/client/misc.bats | 0 | 0 | 2 | ok |  |
| tests/install/ubuntu/client/tailscale.bats | 0 | 0 | 6 | ok |  |
| tests/install/ubuntu/client/zed.bats | 0 | 0 | 7 | ok |  |
| tests/install/ubuntu/common/dependencies.bats | 0 | 0 | 4 | ok |  |
| tests/install/ubuntu/common/dependencies_unit.bats | 0 | 0 | 12 | ok |  |
| tests/install/ubuntu/common/setup_locale.bats | 0 | 0 | 2 | ok |  |
| tests/install/ubuntu/common/ssh.bats | 0 | 0 | 3 | ok |  |
| tests/install/ubuntu/server/setup_timezone.bats | 0 | 0 | 1 | ok |  |
| tests/install/ubuntu/server/sheldon.bats | 0 | 0 | 2 | ok |  |
| tests/install/ubuntu/server/starship.bats | 0 | 0 | 3 | ok |  |
| tests/unit/test_agent_session_staleness.py | 3 | 3 | 19 | ok |  |
| tests/unit/test_agmsg_dispatch.py | 1 | 1 | 16 | ok |  |
| tests/unit/test_agmsg_orchestration_docs.py | 1 | 1 | 3 | ok |  |
| tests/unit/test_apparmor_userns.py | 2 | 2 | 19 | ok |  |
| tests/unit/test_asset_manifest.py | 1 | 1 | 17 | ok |  |
| tests/unit/test_aws_cli_acquisition.py | 1 | 1 | 13 | ok |  |
| tests/unit/test_check_agent_runtime.py | 1 | 1 | 54 | ok |  |
| tests/unit/test_chezmoiremove_agmsg.py | 1 | 1 | 2 | ok |  |
| tests/unit/test_claude_settings_merge.py | 1 | 1 | 22 | ok |  |
| tests/unit/test_codex_config_merge.py | 1 | 1 | 15 | ok |  |
| tests/unit/test_contextdb_codex_notify.py | 1 | 1 | 8 | ok |  |
| tests/unit/test_files_fixture.py | 1 | 1 | 4 | ok |  |
| tests/unit/test_generate_agent_configs.py | 3 | 3 | 60 | ok |  |
| tests/unit/test_herdr_agents.py | 1 | 1 | 285 | ok |  |
| tests/unit/test_permgate.py | 2 | 2 | 53 | ok |  |
| tests/unit/test_pr_feedback.py | 5 | 5 | 23 | ok |  |
| tests/unit/test_release_asset_pins.py | 2 | 2 | 10 | ok |  |
| tests/unit/test_remove_agent_asset.py | 1 | 1 | 23 | ok |  |
| tests/unit/test_require_crit_review.py | 2 | 2 | 72 | ok |  |
| tests/unit/test_runtime_health.py | 1 | 1 | 58 | ok |  |
| tests/unit/test_statusline_tools.py | 1 | 1 | 7 | ok |  |
| tests/unit/test_supply_chain_policy.py | 1 | 1 | 19 | ok |  |
| tests/unit/test_ua_symbol_coverage.py | 0 | 3 | 27 | ok |  |
| tests/unit/test_update_agent_assets_ua_core.py | 1 | 1 | 23 | ok |  |
| tests/unit/test_usage_review.py | 3 | 3 | 11 | ok |  |
| tests/unit/test_validate_agent_assets.py | 3 | 3 | 83 | ok |  |
| tests/unit/test_workflow_security.py | 4 | 4 | 12 | ok |  |
files: 368, regressions: 0
(exit 0)
$ python3 -c "...len(nodes), len(edges)" (new)
984 nodes 1774 edges
$ (same, previous graph from origin/main)
885 nodes 1325 edges
$ git diff origin/main --stat | tail -3
 .ua/knowledge-graph.json | 31894 ++++++++++++++++++++++++++-------------------
 .ua/meta.json            |     6 +-
 3 files changed, 18891 insertions(+), 13518 deletions(-)
$ git diff --exit-code origin/main -- .ua/config.json
(exit 0)
```

## gh pr checks 226 (verbatim, unsandboxed)

```
$ gh pr checks 226
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37014424164/job/110861682282	
private-bootstrap (macos-14, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37014424514/job/110861683730	
private-bootstrap (ubuntu-latest, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37014424514/job/110861683387	
private-bootstrap (ubuntu-latest, server)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37014424514/job/110861683614	
public-bootstrap (macos-14, client)	pass	9m0s	https://github.com/mryfmo/dotfiles/actions/runs/37014424514/job/110861683693	
validate	pass	15s	https://github.com/mryfmo/dotfiles/actions/runs/37014424605/job/110861683482	
nix	skipping	0	https://github.com/mryfmo/dotfiles/actions/runs/37014424164/job/110861758454	
public-bootstrap (ubuntu-latest, client)	pass	9m17s	https://github.com/mryfmo/dotfiles/actions/runs/37014424514/job/110861683684	
public-bootstrap (ubuntu-latest, server)	pass	7m17s	https://github.com/mryfmo/dotfiles/actions/runs/37014424514/job/110861683764	
test (macos-14, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37014424164/job/110861756154	
test (ubuntu-latest, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37014424164/job/110861756075	
test (ubuntu-latest, server)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37014424164/job/110861756024	
(exit 0)
$ gh pr view 226 --json headRefOid,state,mergeable -q ...
98bdf43ff966f4b73dd25832d1f77c1196dc0bdb OPEN MERGEABLE
```

## Extra checks

```
$ python3 (graph filePaths ⊆ git ls-files)
graph filePaths 368 outside git ls-files: []
$ python3 (layers / tour shape)
9 layers ['Bootstrap and Installation', 'Shell and Desktop Runtime', 'Agent Runtime', 'Context Persistence', 'Managed Configuration', 'Maintenance Tooling', 'CI and Infrastructure', 'Behavioral Tests', 'Documentation and Workflow Guidance']
15 tour steps
$ git ls-remote origin refs/heads/chore/ua-graph-refresh-T55
98bdf43ff966f4b73dd25832d1f77c1196dc0bdb	refs/heads/chore/ua-graph-refresh-T55
$ git status --porcelain --untracked-files=no
(exit 0, empty = clean)
$ git log --oneline -1
98bdf43f chore(ua): rebuild the Understand-Anything graph in full at 940a3a2b
```

## Merge report (merge-batch-graphs.py, summary lines verbatim)

```
Found 38 batch files (31 logical batches, 4 multi-part):

Input: 984 nodes, 1870 edges

Fixed (96 corrections):
    96 × tested_by edges dropped (orphan endpoint or test↔test / prod↔prod pair)

Tested-by linker:
     0 × tested_by edges produced (path-convention supplement, production → test)
    40 × production nodes tagged "tested"

Output: 984 nodes, 1774 edges

Imports edge recovery:
  Recovered 0 `imports` edges from importMap (368 entries scanned)

Written to ~/Workspace/dotfiles/.claude/worktrees/worker-c/.ua/intermediate/assembled-graph.json (924 KB)
```

## CompactionDB (main checkout, unsandboxed)

```
$ cd ~/Workspace/dotfiles && python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "T55 (operator 2026-10-02): the .ua/ graph is rebuilt in full as the semantic index before the whole-repository review of tools, libraries and content; the orchestrator never runs the graph build in its own session."
958a79ca-0099-4276-9294-b834ee886185
(exit 0)
```

## PR identity (verbatim, unsandboxed)

```
$ gh pr view 226 --json number,url,headRefOid,state -q '"#\(.number) \(.url) \(.headRefOid) \(.state)"'
#226 https://github.com/mryfmo/dotfiles/pull/226 98bdf43ff966f4b73dd25832d1f77c1196dc0bdb OPEN
```

## Inline validator review.json (verbatim, from the Phase 7 trash copy)

```
$ python3 -c 'print issues, warnings, stats from review.json'
issues []
warnings 45
  Node 'file:home/dot_local/bin/server/cuda.sh' has no edges (orphan)
  Node 'file:.claude/contextdb/contextdb/__init__.py' has no edges (orphan)
  Node 'file:.claude/contextdb/health/.gitkeep' has no edges (orphan)
  Node 'file:.claude/contextdb/spool/incoming/.gitkeep' has no edges (orphan)
  Node 'file:.claude/contextdb/spool/quarantine/.gitkeep' has no edges (orphan)
  Node 'file:.claude/contextdb/state/.gitkeep' has no edges (orphan)
  Node 'document:.github/copilot-instructions.md' has no edges (orphan)
  Node 'config:.github/funding.yaml' has no edges (orphan)
  Node 'document:docs/verification/acceptance/005.md' has no edges (orphan)
  Node 'file:home/dot_config/ghostty/config' has no edges (orphan)
  Node 'file:home/dot_config/git/config.tmpl' has no edges (orphan)
  Node 'file:home/dot_config/git/ignore' has no edges (orphan)
  Node 'config:home/dot_config/gwq/config.toml' has no edges (orphan)
  Node 'config:home/dot_config/tango.yml' has no edges (orphan)
  Node 'config:home/dot_config/uv/uv.toml' has no edges (orphan)
  Node 'config:home/dot_config/yazi/yazi.toml' has no edges (orphan)
  Node 'file:home/dot_local/bin/common/executable_fgc' has no edges (orphan)
  Node 'file:home/dot_local/bin/common/executable_setup-python-env' has no edges (orphan)
  Node 'file:home/dot_local/share/aws-cli-keys/aws-cli-public-key.asc' has no edges (orphan)
  Node 'file:home/dot_vimrc' has no edges (orphan)
  Node 'file:home/dot_zprofile' has no edges (orphan)
  Node 'file:home/dot_zshenv' has no edges (orphan)
  Node 'file:home/private_dot_gnupg/gpg-agent.conf.tmpl' has no edges (orphan)
  Node 'file:home/private_dot_ssh/private_config' has no edges (orphan)
  Node 'file:install/macos/arm64/run.sh' has no edges (orphan)
  Node 'file:tests/install/common/chezmoi_private.bats' has no edges (orphan)
  Node 'file:tests/install/common/gh_extensions.bats' has no edges (orphan)
  Node 'file:tests/install/common/private_layer.bats' has no edges (orphan)
  Node 'file:tests/install/common/provision_machine_key.bats' has no edges (orphan)
  Node 'file:tests/install/macos/common/brew.bats' has no edges (orphan)
  Node 'file:tests/install/macos/common/defaults.bats' has no edges (orphan)
  Node 'file:tests/install/macos/common/docker.bats' has no edges (orphan)
  Node 'file:tests/install/macos/common/ghostty.bats' has no edges (orphan)
  Node 'file:tests/install/macos/common/misc.bats' has no edges (orphan)
  Node 'file:tests/install/ubuntu/client/default_shell.bats' has no edges (orphan)
  Node 'file:tests/install/ubuntu/client/docker.bats' has no edges (orphan)
  Node 'file:tests/install/ubuntu/client/ghostty.bats' has no edges (orphan)
  Node 'file:tests/install/ubuntu/client/gnome_settings.bats' has no edges (orphan)
  Node 'file:tests/install/ubuntu/client/misc.bats' has no edges (orphan)
  Node 'file:tests/install/ubuntu/client/tailscale.bats' has no edges (orphan)
  Node 'file:tests/install/ubuntu/common/dependencies.bats' has no edges (orphan)
  Node 'file:tests/install/ubuntu/common/setup_locale.bats' has no edges (orphan)
  Node 'file:tests/install/ubuntu/common/ssh.bats' has no edges (orphan)
  Node 'file:tests/install/ubuntu/server/setup_timezone.bats' has no edges (orphan)
  Node 'file:tests/install/ubuntu/server/sheldon.bats' has no edges (orphan)
stats {"totalNodes": 984, "totalEdges": 1774, "totalLayers": 9, "tourSteps": 15, "nodeTypes": {"file": 270, "function": 577, "class": 38, "service": 2, "pipeline": 7, "config": 49, "document": 41}, "edgeTypes": {"contains": 645, "exports": 136, "imports": 43, "calls": 464, "depends_on": 155, "related": 140, "triggers": 27, "tested_by": 51, "documents": 74, "configures": 39}}
```

# Revise round 1 (task_rev sha256:6540ebdd…, after audit of 98bdf43)

- Head: 8694200f9fa0a36d3dec8f8a95a0a9f7c7186c52 (one new commit on 98bdf43f, no force push)
- Counts: 984 nodes / 1985 edges (round 0: 984 / 1774; previous graph 885 / 1325)

## Round-1 commands (verbatim)

```
$ sha256sum ~/Workspace/dotfiles/.orchestration/tasks/dot-ua-graph-refresh-T55-a01.md
6540ebdd0584630f3b97d43ebaafd45f255401611c94c179cc146bd872254f36  ~/Workspace/dotfiles/.orchestration/tasks/dot-ua-graph-refresh-T55-a01.md
$ git log --oneline -3
8694200f fix(ua): restore lost calls edges and numeric lineRanges in the T55 graph
98bdf43f chore(ua): rebuild the Understand-Anything graph in full at 940a3a2b
940a3a2b chore(orchestration): T53 and T54 accepted and merged (#224 → 00ce4f6, #225 → ae22603); regime boundary
$ git ls-remote origin refs/heads/chore/ua-graph-refresh-T55
8694200f9fa0a36d3dec8f8a95a0a9f7c7186c52	refs/heads/chore/ua-graph-refresh-T55
$ jq -r .gitCommitHash .ua/meta.json
940a3a2b07adfd14140a0acff96784ef53a0a509
$ git rev-parse HEAD
8694200f9fa0a36d3dec8f8a95a0a9f7c7186c52
$ git diff --name-only $(jq -r .gitCommitHash .ua/meta.json)..HEAD | head
.ua/fingerprints.json
.ua/knowledge-graph.json
.ua/meta.json
$ git diff --name-only 98bdf43f..HEAD
.ua/fingerprints.json
.ua/knowledge-graph.json
.ua/meta.json
$ git diff --exit-code origin/main -- .ua/config.json
(exit 0)
$ git diff origin/main --stat | tail -3
 .ua/knowledge-graph.json | 33184 +++++++++++++++++++++++++++------------------
 .ua/meta.json            |     6 +-
 3 files changed, 20290 insertions(+), 13413 deletions(-)
$ python3 -c "...len(nodes), len(edges)"
984 nodes 1985 edges

$ python3 /tmp/claude-1000/edge-table.py "$TMPDIR/kg-old.json" .ua/knowledge-graph.json   # old = origin/main graph (72b89015), new = HEAD graph; same pair as ua-symbol-coverage
| edge type | old total | new total | files decreased |
|---|---|---|---|
| calls | 220 | 629 | 0 |
| configures | 35 | 46 | 0 |
| contains | 546 | 645 | 0 |
| depends_on | 141 | 180 | 0 |
| documents | 46 | 78 | 0 |
| exports | 131 | 137 | 2 |
| imports | 43 | 43 | 0 |
| related | 99 | 149 | 0 |
| tested_by | 39 | 51 | 0 |
| triggers | 25 | 27 | 0 |

no file lost outgoing calls edges
all-type per-file decreases:
| exports | .claude/contextdb/contextdb/paths.py | 4 | 3 |
| exports | .claude/contextdb/contextdb/recover_hook.py | 3 | 2 |
nodes whose lineRange is not a two-integer range: 0 []

$ cat /tmp/claude-1000/edge-table.py
import json,collections,sys
old=json.load(open(sys.argv[1])); new=json.load(open(sys.argv[2]))
def per(g,et):
    m={n['id']:n.get('filePath') for n in g['nodes']}; c=collections.Counter()
    for e in g['edges']:
        if e['type']==et: c[m.get(e['source'])]+=1
    return c
types=sorted({e['type'] for e in old['edges']}|{e['type'] for e in new['edges']})
print('| edge type | old total | new total | files decreased |'); print('|---|---|---|---|')
dec_all=[]
for et in types:
    o,n=per(old,et),per(new,et); dec=[(f,o[f],n.get(f,0)) for f in sorted(o) if n.get(f,0)<o[f]]
    dec_all+=[(et,)+d for d in dec]
    print(f'| {et} | {sum(o.values())} | {sum(n.values())} | {len(dec)} |')
print()
o,n=per(old,'calls'),per(new,'calls')
d=[(f,o[f],n.get(f,0)) for f in sorted(o) if n.get(f,0)<o[f]]
print('per-file outgoing calls decreases:' if d else 'no file lost outgoing calls edges')
for f,a,b in d: print(f'| {f} | {a} | {b} |')
print('all-type per-file decreases:' if dec_all else 'no file lost outgoing edges of any type')
for x in dec_all: print('|',' | '.join(map(str,x)),'|')
bad=[n['id'] for n in new['nodes'] if 'lineRange' in n and not (isinstance(n['lineRange'],list) and len(n['lineRange'])==2 and all(type(v) is int for v in n['lineRange']))]
print('nodes whose lineRange is not a two-integer range:',len(bad),bad)

$ node /tmp/claude-1000/ua-validate.mjs .ua/knowledge-graph.json   # plugin validateGraph from packages/core/dist/schema.js (the dashboard App.tsx load path)
{
 "file": ".ua/knowledge-graph.json",
 "success": true,
 "fatal": null,
 "inputNodes": 984,
 "inputEdges": 1985,
 "validNodes": 984,
 "validEdges": 1985,
 "layers": 9,
 "tour": 15,
 "issueCount": 0,
 "issues": []
}
$ node /tmp/claude-1000/ua-validate.mjs .ua/knowledge-graph.json  (same, on the round-0 graph at 98bdf43f, for comparison: summary fields only)
{'success': True, 'validNodes': 982, 'validEdges': 1754, 'inputNodes': 984, 'inputEdges': 1774, 'issueCount': 22}
$ cat /tmp/claude-1000/ua-validate.mjs
import { readFileSync } from "node:fs";
import { validateGraph } from "~/.claude/plugins/cache/understand-anything/understand-anything/2.9.7/packages/core/dist/schema.js";
const p = process.argv[2];
const g = JSON.parse(readFileSync(p, "utf8"));
const r = validateGraph(g);
const out = r.data ?? {};
console.log(JSON.stringify({ file: p, success: r.success, fatal: r.fatal ?? null,
  inputNodes: g.nodes.length, inputEdges: g.edges.length,
  validNodes: out.nodes?.length ?? null, validEdges: out.edges?.length ?? null,
  layers: out.layers?.length ?? null, tour: out.tour?.length ?? null,
  issueCount: (r.issues ?? []).length,
  issues: (r.issues ?? []).map(i => ({ level: i.level, category: i.category, path: i.path, message: i.message })) }, null, 1));

$ node .ua/tmp/ua-inline-validate.cjs .ua/knowledge-graph.json .ua/tmp/review-r1.json; python3 (issues, warning count)
issues [] warnings 44
stats {"totalNodes": 984, "totalEdges": 1985, "totalLayers": 9, "tourSteps": 15, "nodeTypes": {"file": 270, "function": 577, "class": 38, "service": 2, "pipeline": 7, "config": 49, "document": 41}, "edgeTypes": {"contains": 645, "exports": 137, "imports": 43, "calls": 629, "depends_on": 180, "related": 149, "triggers": 27, "tested_by": 51, "documents": 78, "configures": 46}}

$ git show origin/main:.ua/knowledge-graph.json > "$TMPDIR/kg-old.json"
$ ua-symbol-coverage "$TMPDIR/kg-old.json" .ua/knowledge-graph.json --old-ref 72b890157078c583f45d71a61ee6eba0df86afb5 --repo-ref "$(jq -r .gitCommitHash .ua/meta.json)"
| file | old | new | def-like lines | status | note |
|---|---|---|---|---|---|
| .chezmoiroot | 0 | 0 | - | ok |  |
| .claude/contextdb/config.json | 0 | 0 | - | ok |  |
| .claude/contextdb/contextdb/__init__.py | 0 | 0 | 0 | ok |  |
| .claude/contextdb/contextdb/cli.py | 4 | 9 | 9 | ok |  |
| .claude/contextdb/contextdb/config.py | 3 | 6 | 6 | ok |  |
| .claude/contextdb/contextdb/hook.py | 2 | 2 | 2 | ok |  |
| .claude/contextdb/contextdb/memory.py | 3 | 4 | 5 | ok |  |
| .claude/contextdb/contextdb/normalize.py | 5 | 6 | 6 | ok |  |
| .claude/contextdb/contextdb/paths.py | 4 | 5 | 5 | ok |  |
| .claude/contextdb/contextdb/probe.py | 1 | 1 | 1 | ok |  |
| .claude/contextdb/contextdb/recall.py | 5 | 8 | 8 | ok |  |
| .claude/contextdb/contextdb/recover_hook.py | 3 | 3 | 3 | ok |  |
| .claude/contextdb/contextdb/recovery.py | 4 | 4 | 4 | ok |  |
| .claude/contextdb/contextdb/redaction.py | 6 | 8 | 10 | ok |  |
| .claude/contextdb/contextdb/semantic.py | 4 | 4 | 4 | ok |  |
| .claude/contextdb/contextdb/spool.py | 6 | 9 | 12 | ok |  |
| .claude/contextdb/contextdb/storage.py | 25 | 25 | 34 | ok |  |
| .claude/contextdb/contextdb/util.py | 19 | 20 | 20 | ok |  |
| .claude/contextdb/health/.gitkeep | 0 | 0 | - | ok |  |
| .claude/contextdb/spool/incoming/.gitkeep | 0 | 0 | - | ok |  |
| .claude/contextdb/spool/quarantine/.gitkeep | 0 | 0 | - | ok |  |
| .claude/contextdb/state/.gitkeep | 0 | 0 | - | ok |  |
| .claude/hooks/contextdb_cli.py | 0 | 0 | 0 | ok |  |
| .claude/hooks/contextdb_hook.py | 0 | 0 | 0 | ok |  |
| .claude/hooks/contextdb_recover.py | 0 | 0 | 0 | ok |  |
| .claude/hooks/query_log.py | 0 | 0 | 0 | ok |  |
| .claude/settings.json | 0 | 0 | - | ok |  |
| .coderabbit.yaml | 0 | 0 | - | ok |  |
| .github/copilot-instructions.md | 0 | 0 | - | ok |  |
| .github/funding.yaml | 0 | 0 | - | ok |  |
| .github/workflows/agent-assets.yml | 0 | 0 | - | ok |  |
| .github/workflows/docs.yml | 0 | 0 | - | ok |  |
| .github/workflows/macos.yaml | 0 | 0 | - | ok |  |
| .github/workflows/remote.yaml | 0 | 0 | - | ok |  |
| .github/workflows/test.yaml | 0 | 0 | - | ok |  |
| .github/workflows/ubuntu.yaml | 0 | 0 | - | ok |  |
| .simplecov | 0 | 0 | - | ok |  |
| .ua/config.json | 0 | 0 | - | ok |  |
| .ua/fingerprints.json | 0 | 0 | - | ok |  |
| .ua/knowledge-graph.json | 0 | 0 | - | ok |  |
| .ua/meta.json | 0 | 0 | - | ok |  |
| AGENTS.md | 0 | 0 | - | ok |  |
| CLAUDE.md | 0 | 0 | - | ok |  |
| Dockerfile | 0 | 0 | - | ok |  |
| Makefile | 0 | 0 | - | ok |  |
| README.md | 0 | 0 | - | ok |  |
| codecov.yml | 0 | 0 | - | ok |  |
| docs/assets/stylesheets/extra.css | 0 | 0 | - | ok |  |
| docs/plans/nix-first-architecture.md | 0 | 0 | - | ok |  |
| docs/plans/nix-migration.md | 0 | 0 | - | ok |  |
| docs/verification/acceptance/005.md | 0 | 0 | - | ok |  |
| flake.nix | 0 | 0 | - | ok |  |
| home/.chezmoi.yaml.tmpl | 0 | 0 | - | ok |  |
| home/.chezmoiexternal.yaml.tmpl | 0 | 0 | - | ok |  |
| home/.chezmoiignore | 0 | 0 | - | ok |  |
| home/.chezmoiremove | 0 | 0 | - | ok |  |
| home/.chezmoiscripts/common/run_once_after_01-setup-chezmoi-private.sh.tmpl | 0 | 0 | - | ok |  |
| home/.chezmoiscripts/common/run_once_after_02-install-mise.sh.tmpl | 0 | 0 | 0 | ok |  |
| home/.chezmoiscripts/common/run_once_after_03-install-sheldon.sh.tmpl | 0 | 0 | 0 | ok |  |
| home/.chezmoiscripts/common/run_once_after_06-install-agent-assets.sh.tmpl | 0 | 0 | 0 | ok |  |
| home/.chezmoiscripts/common/run_once_after_99-install-gh-extensions.sh.tmpl | 0 | 0 | 0 | ok |  |
| home/.chezmoiscripts/common/run_once_before_01-decrypt-private-key.sh.tmpl | 1 | 1 | 3 | ok |  |
| home/.chezmoiscripts/macos/run_once_04-install-ghostty.sh.tmpl | 0 | 0 | - | ok |  |
| home/.chezmoiscripts/macos/run_once_10-install-docker.sh.tmpl | 0 | 0 | - | ok |  |
| home/.chezmoiscripts/macos/run_once_99-install-defaults.sh.tmpl | 0 | 0 | - | ok |  |
| home/.chezmoiscripts/macos/run_once_after_50-install-misc.sh.tmpl | 0 | 0 | - | ok |  |
| home/.chezmoiscripts/macos/run_once_before_01-prepare-system.sh.tmpl | 0 | 0 | - | ok |  |
| home/.chezmoiscripts/macos/run_once_before_02-install-command-line-tool.sh.tmpl | 0 | 0 | - | ok |  |
| home/.chezmoiscripts/macos/run_once_before_03-install-brew.sh.tmpl | 0 | 0 | - | ok |  |
| home/.chezmoiscripts/macos/run_once_before_50-install-dependencies.sh.tmpl | 0 | 0 | - | ok |  |
| home/.chezmoiscripts/ubuntu/run_once_00-setup-ssh.sh.tmpl | 0 | 0 | - | ok |  |
| home/.chezmoiscripts/ubuntu/run_once_10-install-docker.sh.tmpl | 0 | 0 | - | ok |  |
| home/.chezmoiscripts/ubuntu/run_once_10-install-starship.sh.tmpl | 0 | 0 | - | ok |  |
| home/.chezmoiscripts/ubuntu/run_once_50-client-install-misc.sh.tmpl | 0 | 0 | 0 | ok |  |
| home/.chezmoiscripts/ubuntu/run_once_50-server-docker-ssh.sh.tmpl | 0 | 0 | - | ok |  |
| home/.chezmoiscripts/ubuntu/run_once_50-server-install-mics.sh.tmpl | 0 | 0 | - | ok |  |
| home/.chezmoiscripts/ubuntu/run_once_50-server-setup-timezone.sh.tmpl | 0 | 0 | - | ok |  |
| home/.chezmoiscripts/ubuntu/run_once_50-setup-locale.sh.tmpl | 0 | 0 | - | ok |  |
| home/.chezmoiscripts/ubuntu/run_once_51-client-default-shell.sh.tmpl | 0 | 0 | 0 | ok |  |
| home/.chezmoiscripts/ubuntu/run_once_52-client-install-zed.sh.tmpl | 0 | 0 | 0 | ok |  |
| home/.chezmoiscripts/ubuntu/run_once_53-client-install-tailscale.sh.tmpl | 0 | 0 | - | ok |  |
| home/.chezmoiscripts/ubuntu/run_once_99-client-gnome-defaults.sh.tmpl | 0 | 0 | - | ok |  |
| home/.chezmoiscripts/ubuntu/run_once_after_04-install-aws-cli.sh.tmpl | 0 | 0 | - | ok |  |
| home/.chezmoiscripts/ubuntu/run_once_before_50-common-dependencies.sh.tmpl | 0 | 0 | - | ok |  |
| home/.chezmoiscripts/ubuntu/run_onchange_after_07-apparmor-bwrap-userns.sh.tmpl | 0 | 0 | - | ok |  |
| home/.chezmoiscripts/ubuntu/run_onchange_after_60-enable-usage-snapshot-timer.sh.tmpl | 0 | 0 | 0 | ok |  |
| home/.chezmoitemplates/chezmoiexternal.d/common.yaml.tmpl | 0 | 0 | - | ok |  |
| home/.chezmoitemplates/chezmoiexternal.d/macos.yaml.tmpl | 0 | 0 | - | ok |  |
| home/.chezmoitemplates/chezmoiexternal.d/ubuntu.yaml.tmpl | 0 | 0 | - | ok |  |
| home/.chezmoitemplates/chezmoiignore.d/common | 0 | 0 | - | ok |  |
| home/.chezmoitemplates/chezmoiignore.d/macos | 0 | 0 | - | ok |  |
| home/.chezmoitemplates/chezmoiignore.d/ubuntu/client | 0 | 0 | - | ok |  |
| home/.chezmoitemplates/chezmoiignore.d/ubuntu/common | 0 | 0 | - | ok |  |
| home/.chezmoitemplates/chezmoiignore.d/ubuntu/server | 0 | 0 | - | ok |  |
| home/.chezmoitemplates/claude-settings-managed.json | 0 | 0 | - | ok |  |
| home/.chezmoitemplates/codex-config-managed.toml | 0 | 0 | - | ok |  |
| home/.key.txt.age | 0 | 0 | - | ok |  |
| home/Library/LaunchAgents/com.mryfmo.dotfiles.usage-snapshot.plist.tmpl | 0 | 0 | - | ok |  |
| home/dot_agents/README.md | 0 | 0 | - | ok |  |
| home/dot_agents/agent-config.yaml | 0 | 0 | - | ok |  |
| home/dot_agents/model-profiles.env | 0 | 0 | - | ok |  |
| home/dot_agents/permgate-policy.yaml | 0 | 0 | - | ok |  |
| home/dot_agents/plugins/create_marketplace.json | 0 | 0 | - | ok |  |
| home/dot_agents/plugins/mryfmo-dev-workflows/.codex-plugin/plugin.json | 0 | 0 | - | ok |  |
| home/dot_agents/skills/agmsg-orchestration/SKILL.md | 0 | 0 | - | ok |  |
| home/dot_agents/skills/convert-to-transformers/SKILL.md | 0 | 0 | - | ok |  |
| home/dot_agents/skills/convert-to-transformers/references/common-pitfalls.md | 0 | 0 | - | ok |  |
| home/dot_agents/skills/convert-to-transformers/references/learnings.md | 0 | 0 | - | ok |  |
| home/dot_agents/skills/gh-comment-attach-files/SKILL.md | 0 | 0 | - | ok |  |
| home/dot_agents/skills/gh-comment-attach-files/agents/openai.yaml | 0 | 0 | - | ok |  |
| home/dot_agents/skills/gh-comment-attach-files/scripts/attach_comment_files.py | 24 | 24 | 24 | ok |  |
| home/dot_agents/skills/gh-first-workflow/SKILL.md | 0 | 0 | - | ok |  |
| home/dot_agents/skills/gh-first-workflow/agents/openai.yaml | 0 | 0 | - | ok |  |
| home/dot_agents/skills/gh-first-workflow/references/gh-git-rules.md | 0 | 0 | - | ok |  |
| home/dot_agents/skills/humanizer-ja/SKILL.md | 0 | 0 | - | ok |  |
| home/dot_agents/skills/humanizer-ja/agents/openai.yaml | 0 | 0 | - | ok |  |
| home/dot_agents/skills/humanizer-ja/references/ai-patterns-ja.md | 0 | 0 | - | ok |  |
| home/dot_agents/skills/python-uv-workflow/SKILL.md | 0 | 0 | - | ok |  |
| home/dot_agents/skills/python-uv-workflow/agents/openai.yaml | 0 | 0 | - | ok |  |
| home/dot_agents/skills/python-uv-workflow/references/python-uv-rules.md | 0 | 0 | - | ok |  |
| home/dot_agents/skills/shdoc-shell-docs/SKILL.md | 0 | 0 | - | ok |  |
| home/dot_agents/skills/shdoc-shell-docs/agents/openai.yaml | 0 | 0 | - | ok |  |
| home/dot_agents/skills/shdoc-shell-docs/references/shdoc-rules.md | 0 | 0 | - | ok |  |
| home/dot_bash/client/bashrc | 0 | 0 | 0 | ok |  |
| home/dot_bash/server/bashrc | 0 | 0 | 0 | ok |  |
| home/dot_ccstatusline/settings.json | 0 | 0 | - | ok |  |
| home/dot_claude/agents/express-explorer.md | 0 | 0 | - | ok |  |
| home/dot_claude/commands/commit.md | 0 | 0 | - | ok |  |
| home/dot_claude/hooks/executable_enforce-uv.sh | 8 | 8 | 8 | ok |  |
| home/dot_claude/hooks/executable_format-edited-files.py | 2 | 2 | 3 | ok |  |
| home/dot_claude/modify_private_settings.json | 7 | 7 | 12 | ok |  |
| home/dot_claude/private_mcp.json.tmpl | 0 | 0 | - | ok |  |
| home/dot_claude/rules/symlink_agmsg-orchestration.md.tmpl | 0 | 0 | - | ok |  |
| home/dot_claude/rules/symlink_ask-user-question.md.tmpl | 0 | 0 | - | ok |  |
| home/dot_claude/rules/symlink_compactiondb.md.tmpl | 0 | 0 | - | ok |  |
| home/dot_claude/rules/symlink_crit-review.md.tmpl | 0 | 0 | - | ok |  |
| home/dot_claude/rules/symlink_gpu.md.tmpl | 0 | 0 | - | ok |  |
| home/dot_claude/rules/symlink_latex.md.tmpl | 0 | 0 | - | ok |  |
| home/dot_claude/rules/symlink_model-selection.md.tmpl | 0 | 0 | - | ok |  |
| home/dot_claude/rules/symlink_ponytail.md.tmpl | 0 | 0 | - | ok |  |
| home/dot_claude/rules/symlink_pr-integration.md.tmpl | 0 | 0 | - | ok |  |
| home/dot_claude/rules/symlink_python.md.tmpl | 0 | 0 | 0 | ok |  |
| home/dot_claude/rules/symlink_understand-anything.md.tmpl | 0 | 0 | - | ok |  |
| home/dot_claude/skills/agmsg-orchestration/symlink_SKILL.md.tmpl | 0 | 0 | - | ok |  |
| home/dot_claude/skills/convert-to-transformers/references/symlink_common-pitfalls.md.tmpl | 0 | 0 | - | ok |  |
| home/dot_claude/skills/convert-to-transformers/references/symlink_learnings.md.tmpl | 0 | 0 | - | ok |  |
| home/dot_claude/skills/convert-to-transformers/symlink_SKILL.md.tmpl | 0 | 0 | - | ok |  |
| home/dot_claude/skills/gh-comment-attach-files/agents/symlink_openai.yaml.tmpl | 0 | 0 | - | ok |  |
| home/dot_claude/skills/gh-comment-attach-files/scripts/symlink_attach_comment_files.py.tmpl | 0 | 0 | - | ok |  |
| home/dot_claude/skills/gh-comment-attach-files/symlink_SKILL.md.tmpl | 0 | 0 | - | ok |  |
| home/dot_claude/skills/gh-first-workflow/agents/symlink_openai.yaml.tmpl | 0 | 0 | - | ok |  |
| home/dot_claude/skills/gh-first-workflow/references/symlink_gh-git-rules.md.tmpl | 0 | 0 | - | ok |  |
| home/dot_claude/skills/gh-first-workflow/symlink_SKILL.md.tmpl | 0 | 0 | - | ok |  |
| home/dot_claude/skills/humanizer-ja/agents/symlink_openai.yaml.tmpl | 0 | 0 | - | ok |  |
| home/dot_claude/skills/humanizer-ja/references/symlink_ai-patterns-ja.md.tmpl | 0 | 0 | - | ok |  |
| home/dot_claude/skills/humanizer-ja/symlink_SKILL.md.tmpl | 0 | 0 | - | ok |  |
| home/dot_claude/skills/python-uv-workflow/agents/symlink_openai.yaml.tmpl | 0 | 0 | 0 | ok |  |
| home/dot_claude/skills/python-uv-workflow/references/symlink_python-uv-rules.md.tmpl | 0 | 0 | 0 | ok |  |
| home/dot_claude/skills/python-uv-workflow/symlink_SKILL.md.tmpl | 0 | 0 | 0 | ok |  |
| home/dot_claude/skills/shdoc-shell-docs/agents/symlink_openai.yaml.tmpl | 0 | 0 | - | ok |  |
| home/dot_claude/skills/shdoc-shell-docs/references/symlink_shdoc-rules.md.tmpl | 0 | 0 | - | ok |  |
| home/dot_claude/skills/shdoc-shell-docs/symlink_SKILL.md.tmpl | 0 | 0 | - | ok |  |
| home/dot_codex/modify_private_adh.config.toml | 0 | 0 | 7 | ok |  |
| home/dot_codex/modify_private_audit.config.toml | 0 | 0 | 7 | ok |  |
| home/dot_codex/modify_private_config.toml | 0 | 0 | 10 | ok |  |
| home/dot_codex/modify_private_deep.config.toml | 0 | 0 | 7 | ok |  |
| home/dot_codex/modify_private_express.config.toml | 0 | 0 | 6 | ok |  |
| home/dot_codex/modify_private_review.config.toml | 0 | 0 | 6 | ok |  |
| home/dot_codex/modify_private_security.config.toml | 0 | 0 | 7 | ok |  |
| home/dot_codex/modify_private_standard.config.toml | 0 | 0 | 7 | ok |  |
| home/dot_codex/symlink_AGENTS.md.tmpl | 0 | 0 | - | ok |  |
| home/dot_config/alias/client.sh | 0 | 0 | 0 | ok |  |
| home/dot_config/alias/common.sh | 0 | 0 | 0 | ok |  |
| home/dot_config/alias/server.sh | 0 | 0 | 0 | ok |  |
| home/dot_config/ccstatusline/symlink_settings.json.tmpl | 0 | 0 | - | ok |  |
| home/dot_config/claude/rules/agmsg-orchestration.md | 0 | 0 | - | ok |  |
| home/dot_config/claude/rules/ask-user-question.md | 0 | 0 | - | ok |  |
| home/dot_config/claude/rules/compactiondb.md | 0 | 0 | - | ok |  |
| home/dot_config/claude/rules/crit-review.md | 0 | 0 | - | ok |  |
| home/dot_config/claude/rules/gpu.md | 0 | 0 | - | ok |  |
| home/dot_config/claude/rules/latex.md | 0 | 0 | - | ok |  |
| home/dot_config/claude/rules/model-selection.md | 0 | 0 | - | ok |  |
| home/dot_config/claude/rules/ponytail.md | 0 | 0 | - | ok |  |
| home/dot_config/claude/rules/pr-integration.md | 0 | 0 | - | ok |  |
| home/dot_config/claude/rules/python.md | 0 | 0 | - | ok |  |
| home/dot_config/claude/rules/understand-anything.md | 0 | 0 | - | ok |  |
| home/dot_config/codex/AGENTS.md | 0 | 0 | - | ok |  |
| home/dot_config/ghostty/config | 0 | 0 | - | ok |  |
| home/dot_config/git/config.tmpl | 0 | 0 | - | ok |  |
| home/dot_config/git/ignore | 0 | 0 | - | ok |  |
| home/dot_config/gwq/config.toml | 0 | 0 | - | ok |  |
| home/dot_config/herdr/config.toml | 0 | 0 | - | ok |  |
| home/dot_config/herdr/plugins/config/herdr-file-viewer/config.toml | 0 | 0 | - | ok |  |
| home/dot_config/mise/config.toml.tmpl | 0 | 0 | - | ok |  |
| home/dot_config/mise/mise.lock.tmpl | 0 | 0 | - | ok |  |
| home/dot_config/powerlevel10k/p10k.zsh | 2 | 2 | 5 | ok |  |
| home/dot_config/sheldon/plugin_sources/client/common.toml | 0 | 0 | - | ok |  |
| home/dot_config/sheldon/plugin_sources/client/macos.toml | 0 | 0 | - | ok |  |
| home/dot_config/sheldon/plugin_sources/client/ubuntu.toml | 0 | 0 | - | ok |  |
| home/dot_config/sheldon/plugin_sources/common.toml | 0 | 0 | - | ok |  |
| home/dot_config/sheldon/plugin_sources/server.toml | 0 | 0 | - | ok |  |
| home/dot_config/sheldon/plugins.toml.tmpl | 0 | 0 | - | ok |  |
| home/dot_config/starship.toml | 0 | 0 | - | ok |  |
| home/dot_config/systemd/user/usage-snapshot.service.tmpl | 0 | 0 | - | ok |  |
| home/dot_config/systemd/user/usage-snapshot.timer.tmpl | 0 | 0 | - | ok |  |
| home/dot_config/tango.yml | 0 | 0 | - | ok |  |
| home/dot_config/uv/uv.toml | 0 | 0 | - | ok |  |
| home/dot_config/yazi/yazi.toml | 0 | 0 | - | ok |  |
| home/dot_config/zed/keymap.json | 0 | 0 | - | ok |  |
| home/dot_config/zed/settings.json | 0 | 0 | - | ok |  |
| home/dot_config/zsh/plugins/chezmoi-notify/chezmoi-notify.plugin.zsh | 1 | 1 | 1 | ok |  |
| home/dot_local/bin/common/executable_agent-fanout | 2 | 2 | 2 | ok |  |
| home/dot_local/bin/common/executable_agent-session-staleness | 8 | 8 | 13 | ok |  |
| home/dot_local/bin/common/executable_agmsg-dispatch | 1 | 1 | 4 | ok |  |
| home/dot_local/bin/common/executable_cdgwq | 0 | 0 | 1 | ok |  |
| home/dot_local/bin/common/executable_cdw | 1 | 1 | 1 | ok |  |
| home/dot_local/bin/common/executable_chezmoi-cd | 0 | 0 | 1 | ok |  |
| home/dot_local/bin/common/executable_compactiondb-install | 0 | 0 | 0 | ok |  |
| home/dot_local/bin/common/executable_contextdb-codex-notify | 0 | 0 | 0 | ok |  |
| home/dot_local/bin/common/executable_dev | 1 | 1 | 2 | ok |  |
| home/dot_local/bin/common/executable_fgc | 0 | 0 | 1 | ok |  |
| home/dot_local/bin/common/executable_git-delete-merged-branches | 1 | 1 | 3 | ok |  |
| home/dot_local/bin/common/executable_herdr-agents | 34 | 44 | 62 | ok |  |
| home/dot_local/bin/common/executable_herdr-session | 0 | 0 | 1 | ok |  |
| home/dot_local/bin/common/executable_permgate | 16 | 16 | 25 | ok |  |
| home/dot_local/bin/common/executable_provision-machine-key | 2 | 2 | 4 | ok |  |
| home/dot_local/bin/common/executable_remove-agent-asset | 11 | 11 | 21 | ok |  |
| home/dot_local/bin/common/executable_setup-gh | 2 | 2 | 5 | ok |  |
| home/dot_local/bin/common/executable_setup-gpg | 1 | 1 | 3 | ok |  |
| home/dot_local/bin/common/executable_setup-python-env | 0 | 0 | 3 | ok |  |
| home/dot_local/bin/common/executable_ua-symbol-coverage | 0 | 6 | 11 | ok |  |
| home/dot_local/bin/common/executable_uv-format | 0 | 0 | 1 | ok |  |
| home/dot_local/bin/server/cache.sh | 0 | 0 | 0 | ok |  |
| home/dot_local/bin/server/cuda.sh | 0 | 0 | 0 | ok |  |
| home/dot_local/bin/server/history.sh | 1 | 1 | 2 | ok |  |
| home/dot_local/bin/server/ssh_agent.sh | 1 | 1 | 1 | ok |  |
| home/dot_local/share/aws-cli-keys/aws-cli-public-key.asc | 0 | 0 | - | ok |  |
| home/dot_mise/config.toml | 0 | 0 | - | ok |  |
| home/dot_npmrc | 0 | 0 | - | ok |  |
| home/dot_profile | 0 | 0 | - | ok |  |
| home/dot_vimrc | 0 | 0 | - | ok |  |
| home/dot_zprofile | 0 | 0 | 0 | ok |  |
| home/dot_zshenv | 0 | 0 | 0 | ok |  |
| home/dot_zshrc | 0 | 2 | 2 | ok |  |
| home/private_dot_gnupg/gpg-agent.conf.tmpl | 0 | 0 | - | ok |  |
| home/private_dot_ssh/private_config | 0 | 0 | - | ok |  |
| home/symlink_dot_bashrc.tmpl | 0 | 0 | - | ok |  |
| install/common/chezmoi_private.sh | 1 | 1 | 3 | ok |  |
| install/common/gh_extensions.sh | 1 | 1 | 3 | ok |  |
| install/common/mise.sh | 4 | 4 | 8 | ok |  |
| install/common/sheldon.sh | 1 | 1 | 3 | ok |  |
| install/macos/arm64/prepare_arm64_system.sh | 0 | 0 | 2 | ok |  |
| install/macos/arm64/run.sh | 0 | 0 | 1 | ok |  |
| install/macos/common/brew.sh | 1 | 1 | 4 | ok |  |
| install/macos/common/command_line_tool.sh | 1 | 1 | 2 | ok |  |
| install/macos/common/defaults.sh | 7 | 7 | 16 | ok |  |
| install/macos/common/dependencies.sh | 1 | 1 | 3 | ok |  |
| install/macos/common/docker.sh | 0 | 0 | 3 | ok |  |
| install/macos/common/ghostty.sh | 0 | 0 | 4 | ok |  |
| install/macos/common/misc.sh | 2 | 2 | 5 | ok |  |
| install/ubuntu/client/default_shell.sh | 1 | 1 | 1 | ok |  |
| install/ubuntu/client/docker.sh | 3 | 3 | 6 | ok |  |
| install/ubuntu/client/ghostty.sh | 0 | 0 | 5 | ok |  |
| install/ubuntu/client/gnome_settings.sh | 1 | 1 | 9 | ok |  |
| install/ubuntu/client/misc.sh | 0 | 0 | 4 | ok |  |
| install/ubuntu/client/tailscale.sh | 2 | 2 | 4 | ok |  |
| install/ubuntu/client/zed.sh | 3 | 3 | 5 | ok |  |
| install/ubuntu/common/apparmor/bwrap-userns | 0 | 0 | - | ok |  |
| install/ubuntu/common/apparmor_userns.sh | 4 | 4 | 4 | ok |  |
| install/ubuntu/common/aws_cli.sh | 3 | 3 | 5 | ok |  |
| install/ubuntu/common/dependencies.sh | 3 | 3 | 4 | ok |  |
| install/ubuntu/common/setup_locale.sh | 1 | 1 | 1 | ok |  |
| install/ubuntu/common/ssh.sh | 0 | 0 | 4 | ok |  |
| install/ubuntu/server/misc.sh | 0 | 0 | 4 | ok |  |
| install/ubuntu/server/setup_timezone.sh | 0 | 0 | 1 | ok |  |
| install/ubuntu/server/ssh_server.sh | 2 | 2 | 5 | ok |  |
| install/ubuntu/server/starship.sh | 2 | 2 | 4 | ok |  |
| mise.toml | 0 | 0 | - | ok |  |
| mkdocs.yml | 0 | 0 | - | ok |  |
| nix/home-manager/default.nix | 0 | 0 | - | ok |  |
| nix/nix-darwin/default.nix | 0 | 0 | - | ok |  |
| nix/shared/packages.nix | 0 | 0 | - | ok |  |
| plans/001-contain-starship-cleanup.md | 0 | 0 | - | ok |  |
| plans/002-make-review-evidence-non-vacuous.md | 0 | 0 | - | ok |  |
| plans/003-make-bootstrap-safe-and-publicly-testable.md | 0 | 0 | - | ok |  |
| plans/004-harden-and-lock-the-supply-chain.md | 0 | 0 | - | ok |  |
| plans/005-make-runtime-health-and-verification-truthful.md | 0 | 0 | - | ok |  |
| plans/README.md | 0 | 0 | - | ok |  |
| renovate.json | 0 | 0 | - | ok |  |
| scripts/check-agent-runtime.py | 17 | 19 | 39 | ok |  |
| scripts/check-regime-boundary.sh | 0 | 1 | 1 | ok |  |
| scripts/check-statusline-tools.py | 2 | 2 | 3 | ok |  |
| scripts/check-tools.sh | 8 | 14 | 14 | ok |  |
| scripts/generate-agent-configs.py | 19 | 19 | 37 | ok |  |
| scripts/generate-docs.sh | 24 | 34 | 34 | ok |  |
| scripts/lib/asset-manifest.sh | 2 | 5 | 5 | ok |  |
| scripts/lib/installer-pins.sh | 0 | 0 | 0 | ok |  |
| scripts/pr-feedback.py | 5 | 5 | 11 | ok |  |
| scripts/refresh-mkdocs-toc.py | 0 | 0 | 1 | ok |  |
| scripts/require-crit-review.py | 11 | 13 | 24 | ok |  |
| scripts/run_bashcov_unit_test.rb | 3 | 3 | 3 | ok |  |
| scripts/run_benchmark.sh | 4 | 8 | 8 | ok |  |
| scripts/run_unit_test.sh | 2 | 4 | 4 | ok |  |
| scripts/update-agent-assets.sh | 30 | 41 | 41 | ok |  |
| scripts/upgrade-tools.sh | 22 | 35 | 35 | ok |  |
| scripts/usage-report.py | 10 | 10 | 16 | ok |  |
| scripts/usage-snapshot.sh | 0 | 0 | 0 | ok |  |
| scripts/validate-agent-assets.py | 33 | 34 | 44 | ok |  |
| setup.sh | 12 | 12 | 25 | ok |  |
| tests/files/common.bats | 0 | 0 | 0 | ok |  |
| tests/files/helpers.bash | 1 | 1 | 5 | ok |  |
| tests/files/macos.bats | 0 | 0 | 1 | ok |  |
| tests/files/ubuntu.bats | 0 | 0 | 2 | ok |  |
| tests/install/common/check_tools.bats | 0 | 0 | 1 | ok |  |
| tests/install/common/chezmoi_private.bats | 0 | 0 | 2 | ok |  |
| tests/install/common/decrypt_private_key.bats | 1 | 1 | 6 | ok |  |
| tests/install/common/gh_extensions.bats | 0 | 0 | 6 | ok |  |
| tests/install/common/lifecycle.bats | 1 | 1 | 1 | ok |  |
| tests/install/common/mise.bats | 0 | 0 | 8 | ok |  |
| tests/install/common/private_layer.bats | 0 | 0 | 9 | ok |  |
| tests/install/common/provision_machine_key.bats | 0 | 0 | 3 | ok |  |
| tests/install/common/setup.bats | 2 | 2 | 10 | ok |  |
| tests/install/macos/common/brew.bats | 0 | 0 | 1 | ok |  |
| tests/install/macos/common/defaults.bats | 0 | 0 | 1 | ok |  |
| tests/install/macos/common/docker.bats | 0 | 0 | 3 | ok |  |
| tests/install/macos/common/ghostty.bats | 0 | 0 | 2 | ok |  |
| tests/install/macos/common/misc.bats | 0 | 0 | 4 | ok |  |
| tests/install/ubuntu/client/default_shell.bats | 0 | 0 | 7 | ok |  |
| tests/install/ubuntu/client/docker.bats | 0 | 0 | 6 | ok |  |
| tests/install/ubuntu/client/ghostty.bats | 0 | 0 | 2 | ok |  |
| tests/install/ubuntu/client/gnome_settings.bats | 0 | 0 | 4 | ok |  |
| tests/install/ubuntu/client/misc.bats | 0 | 0 | 2 | ok |  |
| tests/install/ubuntu/client/tailscale.bats | 0 | 0 | 6 | ok |  |
| tests/install/ubuntu/client/zed.bats | 0 | 0 | 7 | ok |  |
| tests/install/ubuntu/common/dependencies.bats | 0 | 0 | 4 | ok |  |
| tests/install/ubuntu/common/dependencies_unit.bats | 0 | 0 | 12 | ok |  |
| tests/install/ubuntu/common/setup_locale.bats | 0 | 0 | 2 | ok |  |
| tests/install/ubuntu/common/ssh.bats | 0 | 0 | 3 | ok |  |
| tests/install/ubuntu/server/setup_timezone.bats | 0 | 0 | 1 | ok |  |
| tests/install/ubuntu/server/sheldon.bats | 0 | 0 | 2 | ok |  |
| tests/install/ubuntu/server/starship.bats | 0 | 0 | 3 | ok |  |
| tests/unit/test_agent_session_staleness.py | 3 | 3 | 19 | ok |  |
| tests/unit/test_agmsg_dispatch.py | 1 | 1 | 16 | ok |  |
| tests/unit/test_agmsg_orchestration_docs.py | 1 | 1 | 3 | ok |  |
| tests/unit/test_apparmor_userns.py | 2 | 2 | 19 | ok |  |
| tests/unit/test_asset_manifest.py | 1 | 1 | 17 | ok |  |
| tests/unit/test_aws_cli_acquisition.py | 1 | 1 | 13 | ok |  |
| tests/unit/test_check_agent_runtime.py | 1 | 1 | 54 | ok |  |
| tests/unit/test_chezmoiremove_agmsg.py | 1 | 1 | 2 | ok |  |
| tests/unit/test_claude_settings_merge.py | 1 | 1 | 22 | ok |  |
| tests/unit/test_codex_config_merge.py | 1 | 1 | 15 | ok |  |
| tests/unit/test_contextdb_codex_notify.py | 1 | 1 | 8 | ok |  |
| tests/unit/test_files_fixture.py | 1 | 1 | 4 | ok |  |
| tests/unit/test_generate_agent_configs.py | 3 | 3 | 60 | ok |  |
| tests/unit/test_herdr_agents.py | 1 | 1 | 285 | ok |  |
| tests/unit/test_permgate.py | 2 | 2 | 53 | ok |  |
| tests/unit/test_pr_feedback.py | 5 | 5 | 23 | ok |  |
| tests/unit/test_release_asset_pins.py | 2 | 2 | 10 | ok |  |
| tests/unit/test_remove_agent_asset.py | 1 | 1 | 23 | ok |  |
| tests/unit/test_require_crit_review.py | 2 | 2 | 72 | ok |  |
| tests/unit/test_runtime_health.py | 1 | 1 | 58 | ok |  |
| tests/unit/test_statusline_tools.py | 1 | 1 | 7 | ok |  |
| tests/unit/test_supply_chain_policy.py | 1 | 1 | 19 | ok |  |
| tests/unit/test_ua_symbol_coverage.py | 0 | 3 | 27 | ok |  |
| tests/unit/test_update_agent_assets_ua_core.py | 1 | 1 | 23 | ok |  |
| tests/unit/test_usage_review.py | 3 | 3 | 11 | ok |  |
| tests/unit/test_validate_agent_assets.py | 3 | 3 | 83 | ok |  |
| tests/unit/test_workflow_security.py | 4 | 4 | 12 | ok |  |
files: 368, regressions: 0
(exit 0)

$ merge-batch-graphs.py (round 1, summary lines)
Found 42 batch files (31 logical batches, 6 multi-part):

Input: 984 nodes, 2081 edges

Fixed (96 corrections):
    96 × tested_by edges dropped (orphan endpoint or test↔test / prod↔prod pair)

Tested-by linker:
     0 × tested_by edges produced (path-convention supplement, production → test)
    40 × production nodes tagged "tested"

Output: 984 nodes, 1985 edges

Imports edge recovery:
  Recovered 0 `imports` edges from importMap (368 entries scanned)

Written to ~/Workspace/dotfiles/.claude/worktrees/worker-c/.ua/intermediate/assembled-graph.json (979 KB)

$ git diff 98bdf43f HEAD -- .ua/fingerprints.json | grep "^[-+]" (only generatedAt and the three .ua self-entries)
-  "generatedAt": "2026-10-02T13:34:06.405Z",
+  "generatedAt": "2026-10-02T14:12:51.032Z",
-      "contentHash": "3b6204d3c3a9382aae91c90d63561e588c6daa08d02d126753fe425a06bf473f",
+      "contentHash": "3c82c180d0a8b8bdc45a84f34a6e5e235c2ef0316d0e999167a924a8d59e2990",
-      "totalLines": 10698,
+      "totalLines": 11035,
-      "contentHash": "1a5236ee9a2fd76432c7c0945144ce4aec68c374abe6bdb259d38f690d7f6193",
+      "contentHash": "7a74ed8ea46bbf18066b5e524ac8eef56003bd69debbe8c9e031dddaaf62f50b",
-      "totalLines": 29219,
+      "totalLines": 30723,
-      "contentHash": "575f8afe67b9b34f434c8a944796fe5a05fe9795fa8bb6c7dada96046e444134",
+      "contentHash": "b36cec2294297482b45219cc1e637535fa1bfa5009e7e5c5027c71f4d3404d4b",
```

## Private-helper exports check (verbatim)

```
$ git grep -n "_load_or_create_project_id\|_record_recovery_injected" -- ':!.ua' ':!.orchestration'
.claude/contextdb/contextdb/paths.py:52:def _load_or_create_project_id(path: Path) -> str:
.claude/contextdb/contextdb/paths.py:107:    return replace(result, project_id=_load_or_create_project_id(project_id_path))
.claude/contextdb/contextdb/recover_hook.py:15:def _record_recovery_injected(paths: ProjectPaths, config: dict[str, Any], session_id: str, context: str) -> None:
.claude/contextdb/contextdb/recover_hook.py:54:    _record_recovery_injected(paths, config, session_id, context)
vendor/compactiondb/.claude/contextdb/contextdb/paths.py:52:def _load_or_create_project_id(path: Path) -> str:
vendor/compactiondb/.claude/contextdb/contextdb/paths.py:107:    return replace(result, project_id=_load_or_create_project_id(project_id_path))
vendor/compactiondb/.claude/contextdb/contextdb/recover_hook.py:15:def _record_recovery_injected(paths: ProjectPaths, config: dict[str, Any], session_id: str, context: str) -> None:
vendor/compactiondb/.claude/contextdb/contextdb/recover_hook.py:54:    _record_recovery_injected(paths, config, session_id, context)
$ git grep -n "__all__" .claude/contextdb/contextdb/paths.py .claude/contextdb/contextdb/recover_hook.py
(exit 1, 1 = no __all__)
$ python3 (incoming edges of both helpers in the new graph)
_load_or_create_project_id [('calls', 'project_paths'), ('contains', '.claude/contextdb/contextdb/paths.py')]
_record_recovery_injected [('calls', 'recovery_output'), ('contains', '.claude/contextdb/contextdb/recover_hook.py')]
```

## gh pr checks 226 on 8694200f (verbatim, unsandboxed)

```
$ gh pr checks 226
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37018721514/job/110875968724	
private-bootstrap (macos-14, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37018721870/job/110875969768	
private-bootstrap (ubuntu-latest, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37018721870/job/110875969676	
nix	skipping	0	https://github.com/mryfmo/dotfiles/actions/runs/37018721514/job/110876024067	
private-bootstrap (ubuntu-latest, server)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37018721870/job/110875969741	
public-bootstrap (macos-14, client)	pass	8m30s	https://github.com/mryfmo/dotfiles/actions/runs/37018721870/job/110875969684	
public-bootstrap (ubuntu-latest, client)	pass	8m21s	https://github.com/mryfmo/dotfiles/actions/runs/37018721870/job/110875969753	
public-bootstrap (ubuntu-latest, server)	pass	7m20s	https://github.com/mryfmo/dotfiles/actions/runs/37018721870/job/110875969988	
test (macos-14, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37018721514/job/110876022169	
test (ubuntu-latest, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37018721514/job/110876022437	
test (ubuntu-latest, server)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37018721514/job/110876022465	
validate	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37018722066/job/110875970099	
(exit 0)
$ gh pr view 226 --json number,url,headRefOid,state -q '"#\(.number) \(.url) \(.headRefOid) \(.state)"'
#226 https://github.com/mryfmo/dotfiles/pull/226 8694200f9fa0a36d3dec8f8a95a0a9f7c7186c52 OPEN
```
