#!/usr/bin/env bats

@test "[common] Makefile exposes the public lifecycle targets" {
    make -n setup
    make -n update
    make -n doctor
    make -n upgrade
    make -n require-crit-review
}

@test "[common] Makefile keeps apply as a compatibility alias" {
    make -n apply
}

@test "[common] Makefile force-applies only Hermes runtime config before normal file-only update" {
    run make -n update
    [ "$status" -eq 0 ]
    [[ "$output" == *'chezmoi apply --verbose --force --exclude=scripts ~/.hermes'* ]]
    grep -xF 'chezmoi apply --verbose --exclude=scripts' <<< "$output"
    [[ "$output" == *'apply --verbose --exclude=scripts'* ]]
    [[ "$output" != *'apply --verbose;'* ]]
}

@test "[common] Makefile treats private chezmoi as optional during update" {
    run make -n update
    [ "$status" -eq 0 ]
    # `make -n` prints the shell branch text without executing it; this asserts
    # the optional-private guard is present in the generated recipe.
    [[ "$output" == *'$HOME/.local/share/chezmoi-private'* ]]
    [[ "$output" == *'$HOME/.config/chezmoi-private/chezmoi.yaml'* ]]
    [[ "$output" == *'--source "$HOME/.local/share/chezmoi-private"'* ]]
    [[ "$output" == *'apply --verbose --exclude=scripts'* ]]
    [[ "$output" == *'Skipping private dotfiles'* ]]
    [[ "$output" != *'chezmoi-private apply'* ]]
}

@test "[common] Makefile maps SYSTEM=1 upgrade to system package upgrades" {
    run make -n upgrade SYSTEM=1
    [ "$status" -eq 0 ]
    [[ "$output" == *'./scripts/upgrade-tools.sh --system'* ]]
}

@test "[common] Makefile does not treat SYSTEM=0 as a system package upgrade request" {
    run make -n upgrade SYSTEM=0
    [ "$status" -eq 0 ]
    [[ "$output" == *'./scripts/upgrade-tools.sh '* ]]
    [[ "$output" != *'--system'* ]]
}

@test "[common] Makefile skips private init when chezmoi-private is unavailable" {
    run make -n init
    [ "$status" -eq 0 ]
    [[ "$output" == *'command -v chezmoi-private'* ]]
    [[ "$output" == *'Skipping private dotfiles init'* ]]
}

@test "[common] Makefile does not expose a separate upgrade-system target" {
    run make -n upgrade-system
    [ "$status" -ne 0 ]
}

@test "[common] setup.sh does not upgrade installed tools during bootstrap" {
    run grep -Eq 'brew upgrade|apt-get (dist-upgrade|full-upgrade|upgrade)|mise upgrade|uv tool upgrade|gh extension upgrade|cargo install .*--force|npm update -g' setup.sh
    [ "$status" -eq 1 ]
}

@test "[common] explicit tool lifecycle scripts are present" {
    [ -x scripts/upgrade-tools.sh ]
    [ -x scripts/check-tools.sh ]
}

@test "[common] doctor uses OS-aware mise listing" {
    grep -q 'run_optional_doctor mise ls --current' scripts/check-tools.sh
    ! grep -q 'run_optional_doctor mise current' scripts/check-tools.sh
}

@test "[common] upgrade lifecycle refreshes mise itself before mise-managed tools" {
    local self_update_line
    local install_line
    local upgrade_line

    grep -q 'mise self-update --yes' scripts/upgrade-tools.sh
    grep -q 'run_mise_tool_command install' scripts/upgrade-tools.sh
    grep -q 'run_mise_tool_command upgrade' scripts/upgrade-tools.sh
    self_update_line="$(grep -n 'upgrade_mise_self' scripts/upgrade-tools.sh | tail -n 1 | cut -d: -f1)"
    install_line="$(grep -n 'upgrade_mise_tools' scripts/upgrade-tools.sh | tail -n 1 | cut -d: -f1)"
    upgrade_line="$(grep -n 'run_mise_tool_command upgrade' scripts/upgrade-tools.sh | cut -d: -f1)"

    [ -n "${self_update_line}" ]
    [ -n "${install_line}" ]
    [ -n "${upgrade_line}" ]
    [ "${self_update_line}" -lt "${install_line}" ]
}

@test "[common] mise tool lifecycle isolates Git config and continues after individual tool failures" {
    grep -q 'function run_mise_with_isolated_git_config()' scripts/upgrade-tools.sh
    grep -q 'GIT_CONFIG_NOSYSTEM=1' scripts/upgrade-tools.sh
    grep -q 'GIT_CONFIG_GLOBAL=/dev/null' scripts/upgrade-tools.sh
    grep -q 'XDG_CONFIG_HOME="${isolated_xdg_config_home}"' scripts/upgrade-tools.sh
    grep -q 'mise_config_dir="${MISE_CONFIG_DIR:-${XDG_CONFIG_HOME:-${HOME%/}/.config}/mise}"' scripts/upgrade-tools.sh
    grep -q 'MISE_CONFIG_DIR="${mise_config_dir}"' scripts/upgrade-tools.sh
    grep -q 'rm -rf "${isolated_xdg_config_home}"' scripts/upgrade-tools.sh
    grep -q 'run_mise_with_isolated_git_config ls --current --no-header' scripts/upgrade-tools.sh
    grep -q 'run_mise_with_isolated_git_config "${mise_command}" --yes --before 7d "${mise_tool}"' scripts/upgrade-tools.sh
    grep -q 'warning: unable to list current mise tools for %s; continuing' scripts/upgrade-tools.sh
    grep -q 'warning: mise %s failed for %s; continuing' scripts/upgrade-tools.sh
}

@test "[common] Homebrew upgrade filters forbidden formulae without installed-dependent side effects" {
    grep -q 'DEFAULT_FORBIDDEN_HOMEBREW_FORMULAE="node node@\* python python@\* python3 pip npm pnpm yarn claude"' scripts/upgrade-tools.sh
    grep -q 'for forbidden_formula in ${DEFAULT_FORBIDDEN_HOMEBREW_FORMULAE} ${HOMEBREW_FORBIDDEN_FORMULAE:-}' scripts/upgrade-tools.sh
    grep -q 'case "${formula}" in' scripts/upgrade-tools.sh
    grep -q 'HOMEBREW_NO_INSTALLED_DEPENDENTS_CHECK=1 brew upgrade --formula "${upgrade_formulae\[@\]}"' scripts/upgrade-tools.sh
    grep -q 'HOMEBREW_NO_INSTALLED_DEPENDENTS_CHECK=1 brew upgrade --cask --skip-cask-deps "${outdated_casks\[@\]}"' scripts/upgrade-tools.sh
    grep -q 'brew list --cask codexbar' scripts/update-codex-statusline-tools.sh
    grep -q 'HOMEBREW_NO_INSTALLED_DEPENDENTS_CHECK=1 brew install --cask --skip-cask-deps codexbar' scripts/update-codex-statusline-tools.sh
    grep -q 'HOMEBREW_NO_INSTALLED_DEPENDENTS_CHECK=1 brew upgrade --cask --skip-cask-deps codexbar' scripts/update-codex-statusline-tools.sh
    grep -q 'HOMEBREW_NO_INSTALLED_DEPENDENTS_CHECK=1 brew upgrade --formula codexbar' scripts/update-codex-statusline-tools.sh
    grep -q 'HOMEBREW_NO_INSTALLED_DEPENDENTS_CHECK=1 brew upgrade --formula steipete/tap/codexbar' scripts/update-codex-statusline-tools.sh
}

@test "[common] agent CLI upgrade installs npm latest into mise packages and removes node-global shadows" {
    local latest_line
    local install_line
    local repair_line
    local codex_cleanup_line
    local claude_cleanup_line

    grep -q 'npm uninstall -g "${npm_package}"' scripts/upgrade-tools.sh
    grep -q 'npm view "$1" version' scripts/upgrade-tools.sh
    grep -q 'versioned_mise_tool="${mise_tool}@${package_version}"' scripts/upgrade-tools.sh
    grep -q 'npm_config_min_release_age=0 run_mise_with_isolated_git_config install --yes "${versioned_mise_tool}"' scripts/upgrade-tools.sh
    grep -q 'repair_mise_npm_package "${versioned_mise_tool}" "${npm_package}" "${package_version}"' scripts/upgrade-tools.sh
    grep -q 'if upgrade_mise_npm_agent_tool "npm:@openai/codex" "@openai/codex"; then' scripts/upgrade-tools.sh
    grep -q 'if upgrade_mise_npm_agent_tool "npm:@anthropic-ai/claude-code" "@anthropic-ai/claude-code"; then' scripts/upgrade-tools.sh
    latest_line="$(grep -n 'latest_npm_package_version "${npm_package}"' scripts/upgrade-tools.sh | cut -d: -f1)"
    install_line="$(grep -n 'run_mise_with_isolated_git_config install --yes "${versioned_mise_tool}"' scripts/upgrade-tools.sh | cut -d: -f1)"
    repair_line="$(grep -n 'repair_mise_npm_package "${versioned_mise_tool}" "${npm_package}" "${package_version}"' scripts/upgrade-tools.sh | cut -d: -f1)"
    codex_cleanup_line="$(grep -n 'remove_node_global_npm_package "@openai/codex"' scripts/upgrade-tools.sh | cut -d: -f1)"
    claude_cleanup_line="$(grep -n 'remove_node_global_npm_package "@anthropic-ai/claude-code"' scripts/upgrade-tools.sh | cut -d: -f1)"

    [ -n "${latest_line}" ]
    [ -n "${install_line}" ]
    [ -n "${repair_line}" ]
    [ -n "${codex_cleanup_line}" ]
    [ -n "${claude_cleanup_line}" ]
    [ "${latest_line}" -lt "${install_line}" ]
    [ "${install_line}" -lt "${repair_line}" ]
    [ "${repair_line}" -lt "${codex_cleanup_line}" ]
    [ "${repair_line}" -lt "${claude_cleanup_line}" ]
    grep -q 'remove_node_global_npm_package "@openai/codex"' scripts/upgrade-tools.sh
    grep -q 'remove_node_global_npm_package "@anthropic-ai/claude-code"' scripts/upgrade-tools.sh
}

@test "[common] agent asset lifecycle installs Crit integrations for Claude Code and Codex" {
    grep -q 'CLAUDE_CRIT_PLUGIN="crit@crit"' scripts/update-agent-assets.sh
    grep -q 'CLAUDE_CRIT_MARKETPLACE="tomasz-tomczyk/crit"' scripts/update-agent-assets.sh
    grep -q 'brew install crit' scripts/update-agent-assets.sh
    grep -q 'python3 -c' scripts/update-agent-assets.sh
    grep -q 'plugin.get("id") == plugin_id' scripts/update-agent-assets.sh
    grep -q 'if claude_crit_plugin_is_enabled; then' scripts/update-agent-assets.sh
    grep -q 'claude plugin enable "${CLAUDE_CRIT_PLUGIN}"' scripts/update-agent-assets.sh
    grep -q 'crit install codex-plugin --force' scripts/update-agent-assets.sh
    grep -q 'update_claude_crit' scripts/update-agent-assets.sh
    grep -q 'update_codex_crit' scripts/update-agent-assets.sh
    grep -q 'require-crit-review' Makefile
    grep -q 'CRIT_REVIEWED' scripts/require-crit-review.py
    grep -q 'AGENT_REVIEWED' scripts/require-crit-review.py
    grep -q 'REVIEW_EVIDENCE' scripts/require-crit-review.py
    grep -q 'review_surface' scripts/require-crit-review.py
    grep -q 'review_outcome' scripts/require-crit-review.py
    grep -q 'SELF_REVIEWER_TOKENS' scripts/require-crit-review.py
    grep -q 'CRIT_REVIEW=off' scripts/require-crit-review.py
    grep -q 'make require-crit-review' home/dot_config/codex/AGENTS.md
    grep -q 'make require-crit-review' home/dot_config/claude/rules/crit-review.md
}

@test "[common] agent asset lifecycle installs Ponytail integrations for Claude Code and Codex" {
    grep -q 'CLAUDE_PONYTAIL_PLUGIN="ponytail@ponytail"' scripts/update-agent-assets.sh
    grep -q 'CLAUDE_PONYTAIL_MARKETPLACE="DietrichGebert/ponytail"' scripts/update-agent-assets.sh
    grep -q 'CODEX_PONYTAIL_PLUGIN="ponytail@ponytail"' scripts/update-agent-assets.sh
    grep -q 'CODEX_PONYTAIL_MARKETPLACE="DietrichGebert/ponytail"' scripts/update-agent-assets.sh
    grep -q 'claude plugin enable "${CLAUDE_PONYTAIL_PLUGIN}"' scripts/update-agent-assets.sh
    grep -q 'codex plugin add "${CODEX_PONYTAIL_PLUGIN}"' scripts/update-agent-assets.sh
    grep -q 'update_claude_ponytail' scripts/update-agent-assets.sh
    grep -q 'update_codex_ponytail' scripts/update-agent-assets.sh
    grep -q 'PONYTAIL_DEFAULT_MODE' scripts/update-agent-assets.sh
    grep -q 'ponytail@ponytail' home/dot_codex/private_config.toml.tmpl
    grep -q 'Ponytail' home/dot_config/codex/AGENTS.md
    grep -q 'ponytail@ponytail' home/dot_config/claude/rules/ponytail.md
}

@test "[common] agent asset lifecycle installs ccgate for Claude Code and Codex permission gates" {
    grep -q 'aqua:tak848/ccgate' scripts/update-agent-assets.sh
    grep -q '"aqua:tak848/ccgate" = "latest"' home/dot_mise/config.toml
    grep -q 'ccgate --version' scripts/update-agent-assets.sh
    grep -q 'ccgate claude' home/dot_claude/private_settings.json
    grep -q 'ccgate codex' home/dot_codex/private_config.toml.tmpl
    grep -q 'claude-haiku-4-5' home/dot_claude/ccgate.jsonnet
    grep -q 'HookInput.model' home/dot_codex/ccgate.jsonnet
    grep -q 'HookInput.model' home/dot_config/codex/AGENTS.md
    grep -q 'provider.model' home/dot_config/claude/rules/model-selection.md
    grep -q 'metrics --details 5' home/dot_config/claude/rules/model-selection.md
}

@test "[common] Hermes home is managed as a private directory" {
    [ -d home/private_dot_hermes ]
    [ ! -e home/dot_hermes ]
    [ -f home/private_dot_hermes/private_config.yaml.tmpl ]
}

@test "[common] README documents setup update doctor and upgrade lifecycle" {
    grep -q '### Lifecycle' README.md
    grep -q 'make setup' README.md
    grep -q 'make update' README.md
    grep -q 'make doctor' README.md
    grep -q 'make upgrade' README.md
    grep -q 'make upgrade SYSTEM=1' README.md
    grep -q 'setup.sh' README.md
}

@test "[common] README documents agent permission asset lifecycle" {
    grep -q '### Agent review and permission assets' README.md
    grep -q 'ccgate is used as a permission gate, not as a model router' README.md
    grep -q '`provider.model` is the small classifier used for permission decisions' README.md
    grep -q 'HookInput.model' README.md
    grep -q 'ccgate codex metrics --details 5' README.md
    grep -q 'ccgate claude metrics --details 5' README.md
    grep -q 'scripts/update-agent-assets.sh' README.md
    grep -q 'make require-crit-review' README.md
    grep -q 'AGENT_REVIEWED=1' README.md
    grep -q 'REVIEW_EVIDENCE' README.md
    grep -q 'human or external reviewer' README.md
    grep -q 'CRIT_REVIEW=off' README.md
}

@test "[common] README documents clean sourceDir bootstrap and repository-root handoff" {
    grep -q "chezmoi's sourceDir" README.md
    grep -q 'usually ~/.local/share/chezmoi' README.md
    grep -q '`setup.sh` does not clone into the current directory' README.md
    grep -q 'Makefile lifecycle commands must run from the repository root, not from $HOME' README.md
    grep -q 'git -C "$(chezmoi source-path)" rev-parse --show-toplevel' README.md
    grep -q 'existing `~/.config/chezmoi/chezmoi.yaml` already sets `sourceDir`' README.md
}
