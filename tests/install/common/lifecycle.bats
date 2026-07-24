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

function run_update_fixture() {
    local server_status="${1-running}"
    local status_exit="${2:-0}"
    local reload_exit="${3:-0}"
    local apply_exit="${4:-0}"
    local assets_exit="${5:-0}"
    local mise_exit="${6:-0}"
    local fixture="${BATS_TEST_TMPDIR}/update-${BATS_TEST_NUMBER}"

    mkdir -p "${fixture}/bin" "${fixture}/scripts" \
        "${fixture}/home/.local/share/chezmoi-private" \
        "${fixture}/home/.config/chezmoi-private"
    touch "${fixture}/home/.config/chezmoi-private/chezmoi.yaml"
    cp Makefile "${fixture}/Makefile"
    cat > "${fixture}/bin/chezmoi" <<EOF
#!/usr/bin/env bash
printf 'chezmoi %s\n' "\$*" >> "${fixture}/calls"
exit ${apply_exit}
EOF
    cat > "${fixture}/bin/mise" <<EOF
#!/usr/bin/env bash
printf 'mise %s\n' "\$*" >> "${fixture}/calls"
exit ${mise_exit}
EOF
    cat > "${fixture}/scripts/update-agent-assets.sh" <<EOF
#!/usr/bin/env bash
printf 'assets\n' >> "${fixture}/calls"
exit ${assets_exit}
EOF
    cat > "${fixture}/bin/herdr" <<EOF
#!/usr/bin/env bash
printf 'herdr %s\n' "\$*" >> "${fixture}/calls"
if [[ \$1 == status ]]; then
    case '${server_status}' in
        missing-status) printf '{"running":true}\n' ;;
        nonstring-status) printf '{"status":true}\n' ;;
        multiple-statuses) printf '{"status":"running"}\n{"status":"not_running"}\n' ;;
        malformed-json) printf '{\n' ;;
        *) printf '{"status":"%s","running":%s}\n' '${server_status}' "\$([[ '${server_status}' == running ]] && printf true || printf false)" ;;
    esac
    exit ${status_exit}
fi
exit ${reload_exit}
EOF
    chmod +x "${fixture}/bin/chezmoi" "${fixture}/bin/mise" "${fixture}/bin/herdr" \
        "${fixture}/scripts/update-agent-assets.sh"

    run env HOME="${fixture}/home" PATH="${fixture}/bin:${PATH}" make -C "${fixture}" update
    UPDATE_FIXTURE="${fixture}"
}

@test "[common] update reloads a running Herdr server exactly once" {
    run_update_fixture running
    [ "$status" -eq 0 ]
    [ "$(grep -c '^herdr server reload-config$' "${UPDATE_FIXTURE}/calls")" -eq 1 ]
}

@test "[common] update installs statusline tools after applies and before agent assets" {
    run_update_fixture running
    [ "$status" -eq 0 ]
    run cat "${UPDATE_FIXTURE}/calls"
    [ "$output" = "chezmoi apply --verbose --exclude=scripts
chezmoi --source ${UPDATE_FIXTURE}/home/.local/share/chezmoi-private --config ${UPDATE_FIXTURE}/home/.config/chezmoi-private/chezmoi.yaml apply --verbose --exclude=scripts
mise install --locked npm:ccstatusline npm:ccusage
assets
herdr status server --json
herdr server reload-config" ]
}

@test "[common] update stops before agent assets and Herdr when statusline install fails" {
    run_update_fixture running 0 0 0 0 24
    [ "$status" -ne 0 ]
    grep -q '^mise install --locked npm:ccstatusline npm:ccusage$' "${UPDATE_FIXTURE}/calls"
    ! grep -q '^assets$' "${UPDATE_FIXTURE}/calls"
    ! grep -q '^herdr ' "${UPDATE_FIXTURE}/calls"
}

@test "[common] update skips a Herdr server that is not running" {
    run_update_fixture not_running
    [ "$status" -eq 0 ]
    [[ "$output" == *'Herdr server is not running; skipping config reload.'* ]]
    ! grep -q '^herdr server reload-config$' "${UPDATE_FIXTURE}/calls"
}

@test "[common] update skips reload when Herdr is absent" {
    local fixture="${BATS_TEST_TMPDIR}/update-${BATS_TEST_NUMBER}"
    mkdir -p "${fixture}/bin" "${fixture}/scripts" "${fixture}/home"
    cp Makefile "${fixture}/Makefile"
    printf '#!/usr/bin/env bash\nexit 0\n' > "${fixture}/bin/chezmoi"
    printf '#!/usr/bin/env bash\nexit 0\n' > "${fixture}/bin/mise"
    printf '#!/usr/bin/env bash\nexit 0\n' > "${fixture}/scripts/update-agent-assets.sh"
    chmod +x "${fixture}/bin/chezmoi" "${fixture}/bin/mise" "${fixture}/scripts/update-agent-assets.sh"

    run env HOME="${fixture}/home" PATH="${fixture}/bin:/usr/bin:/bin" make -C "${fixture}" update
    [ "$status" -eq 0 ]
    [[ "$output" == *'Herdr command not found; skipping config reload.'* ]]
}

@test "[common] update fails when Herdr status fails" {
    run_update_fixture running 42
    [ "$status" -ne 0 ]
    ! grep -q '^herdr server reload-config$' "${UPDATE_FIXTURE}/calls"
}

@test "[common] update rejects missing or unknown Herdr server status" {
    run_update_fixture unknown
    [ "$status" -ne 0 ]
    ! grep -q '^herdr server reload-config$' "${UPDATE_FIXTURE}/calls"

    run_update_fixture missing-status
    [ "$status" -ne 0 ]
    ! grep -q '^herdr server reload-config$' "${UPDATE_FIXTURE}/calls"

    for malformed in nonstring-status multiple-statuses malformed-json; do
        run_update_fixture "${malformed}"
        [ "$status" -ne 0 ]
        ! grep -q '^herdr server reload-config$' "${UPDATE_FIXTURE}/calls"
    done
}

@test "[common] update propagates Herdr reload failure" {
    run_update_fixture running 0 23
    [ "$status" -ne 0 ]
    [ "$(grep -c '^herdr server reload-config$' "${UPDATE_FIXTURE}/calls")" -eq 1 ]
}

@test "[common] update does not reload after apply or asset failure" {
    run_update_fixture running 0 0 19
    [ "$status" -ne 0 ]
    ! grep -q '^herdr ' "${UPDATE_FIXTURE}/calls"

    run_update_fixture running 0 0 0 20
    [ "$status" -ne 0 ]
    ! grep -q '^herdr ' "${UPDATE_FIXTURE}/calls"
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

@test "[common] doctor requires the OS-aware mise listing" {
    grep -q 'run_required_doctor mise ls --current' scripts/check-tools.sh
    ! grep -q 'run_required_doctor mise current' scripts/check-tools.sh
}

@test "[common] upgrade lifecycle refreshes mise itself before mise-managed tools" {
    local self_update_line
    local upgrade_line
    local tool_upgrade_line

    grep -q 'mise self-update --yes' scripts/upgrade-tools.sh
    grep -q 'run_mise_tool_command install' scripts/upgrade-tools.sh
    grep -q 'run_mise_tool_command upgrade' scripts/upgrade-tools.sh
    self_update_line="$(grep -n 'upgrade_mise_self' scripts/upgrade-tools.sh | tail -n 1 | cut -d: -f1)"
    upgrade_line="$(grep -n 'upgrade_mise_tools' scripts/upgrade-tools.sh | tail -n 1 | cut -d: -f1)"
    tool_upgrade_line="$(grep -n 'run_mise_tool_command upgrade' scripts/upgrade-tools.sh | cut -d: -f1)"

    [ -n "${self_update_line}" ]
    [ -n "${upgrade_line}" ]
    [ -n "${tool_upgrade_line}" ]
    [ "${self_update_line}" -lt "${upgrade_line}" ]
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
    grep -q 'MISE_LOCKED=0 run_mise_with_isolated_git_config upgrade --bump --yes --before 7d "${mise_tool}"' scripts/upgrade-tools.sh
    grep -q 'MISE_LOCKED=0 npm_config_min_release_age=0 run_mise_with_isolated_git_config use --global --pin --yes --minimum-release-age 0s "${versioned_mise_tool}"' scripts/upgrade-tools.sh
    grep -q 'warning: unable to list current mise tools for %s; continuing' scripts/upgrade-tools.sh
    grep -q 'warning: mise %s failed for %s; continuing' scripts/upgrade-tools.sh
}

@test "[common] Homebrew upgrade filters forbidden formulae without installed-dependent side effects" {
    grep -q 'DEFAULT_FORBIDDEN_HOMEBREW_FORMULAE="node node@\* python python@\* python3 pip npm pnpm yarn claude"' scripts/upgrade-tools.sh
    grep -q 'for forbidden_formula in ${DEFAULT_FORBIDDEN_HOMEBREW_FORMULAE} ${HOMEBREW_FORBIDDEN_FORMULAE:-}' scripts/upgrade-tools.sh
    grep -q 'case "${formula}" in' scripts/upgrade-tools.sh
    grep -q 'HOMEBREW_NO_INSTALLED_DEPENDENTS_CHECK=1 brew upgrade --formula "${upgrade_formulae\[@\]}"' scripts/upgrade-tools.sh
    grep -q 'HOMEBREW_NO_INSTALLED_DEPENDENTS_CHECK=1 brew upgrade --cask --skip-cask-deps "${outdated_casks\[@\]}"' scripts/upgrade-tools.sh
}

@test "[common] agent CLI lifecycle installs npm latest into mise packages and removes node-global shadows before asset commands" {
    local latest_line
    local upgrade_line
    local repair_line
    local cleanup_line

    grep -q 'for npm_package in "@openai/codex" "@anthropic-ai/claude-code"' scripts/update-agent-assets.sh
    grep -q 'npm uninstall -g "${npm_package}"' scripts/update-agent-assets.sh
    grep -q 'npm view "$1" version' scripts/upgrade-tools.sh
    grep -q 'versioned_mise_tool="${mise_tool}@${package_version}"' scripts/upgrade-tools.sh
    grep -q 'MISE_LOCKED=0 npm_config_min_release_age=0 run_mise_with_isolated_git_config use --global --pin --yes --minimum-release-age 0s "${versioned_mise_tool}"' scripts/upgrade-tools.sh
    grep -q 'repair_mise_npm_package "${versioned_mise_tool}" "${npm_package}" "${package_version}"' scripts/upgrade-tools.sh
    grep -q -- '--allow-scripts="${npm_package}"' scripts/upgrade-tools.sh
    grep -q 'if ! upgrade_mise_npm_agent_tool "npm:@openai/codex" "@openai/codex"; then' scripts/upgrade-tools.sh
    grep -q 'if ! upgrade_mise_npm_agent_tool "npm:@anthropic-ai/claude-code" "@anthropic-ai/claude-code"; then' scripts/upgrade-tools.sh
    latest_line="$(grep -n 'latest_npm_package_version "${npm_package}"' scripts/upgrade-tools.sh | cut -d: -f1)"
    upgrade_line="$(grep -n 'run_mise_with_isolated_git_config use --global --pin --yes --minimum-release-age 0s "${versioned_mise_tool}"' scripts/upgrade-tools.sh | cut -d: -f1)"
    repair_line="$(grep -n 'repair_mise_npm_package "${versioned_mise_tool}" "${npm_package}" "${package_version}"' scripts/upgrade-tools.sh | cut -d: -f1)"
    cleanup_line="$(grep -n '^    remove_node_global_agent_cli_shadows$' scripts/update-agent-assets.sh | cut -d: -f1)"

    [ -n "${latest_line}" ]
    [ -n "${upgrade_line}" ]
    [ -n "${repair_line}" ]
    [ -n "${cleanup_line}" ]
    [ "${latest_line}" -lt "${upgrade_line}" ]
    [ "${upgrade_line}" -lt "${repair_line}" ]
    [ "${cleanup_line}" -lt "$(grep -n '^    update_claude_superpowers$' scripts/update-agent-assets.sh | cut -d: -f1)" ]
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
    grep -q 'crit status --json' home/dot_config/codex/AGENTS.md
    grep -q 'crit status --json' home/dot_config/claude/rules/crit-review.md
    grep -q 'crit comments --all --json <review.json>' home/dot_config/codex/AGENTS.md
    grep -q 'crit comments --all --json <review.json>' home/dot_config/claude/rules/crit-review.md
    grep -q '作業手順の証跡' home/dot_config/codex/AGENTS.md
    grep -q 'レビュー実施者を認証するものではありません' home/dot_config/codex/AGENTS.md
    grep -q 'process evidence, not reviewer authentication' home/dot_config/claude/rules/crit-review.md
    ! grep -q 'crit comments --json' home/dot_config/codex/AGENTS.md
    ! grep -q 'crit comments --json' home/dot_config/claude/rules/crit-review.md
}

@test "[common] agent asset lifecycle installs Ponytail integrations for Claude Code and Codex" {
    grep -q 'CLAUDE_PONYTAIL_PLUGIN="ponytail@ponytail"' scripts/update-agent-assets.sh
    grep -q 'CLAUDE_PONYTAIL_MARKETPLACE="DietrichGebert/ponytail"' scripts/update-agent-assets.sh
    grep -q 'CODEX_PONYTAIL_PLUGIN="ponytail@ponytail"' scripts/update-agent-assets.sh
    grep -q 'CODEX_PONYTAIL_MARKETPLACE="DietrichGebert/ponytail"' scripts/update-agent-assets.sh
    grep -q 'CODEX_PONYTAIL_MARKETPLACE_SOURCE="https://github.com/DietrichGebert/ponytail.git"' scripts/update-agent-assets.sh
    grep -q 'codex_marketplace_has_source "${CODEX_PONYTAIL_MARKETPLACE_NAME}" "${CODEX_PONYTAIL_MARKETPLACE_SOURCE}"' scripts/update-agent-assets.sh
    grep -q 'codex plugin marketplace upgrade "${CODEX_PONYTAIL_MARKETPLACE_NAME}"' scripts/update-agent-assets.sh
    grep -q 'claude plugin enable "${CLAUDE_PONYTAIL_PLUGIN}"' scripts/update-agent-assets.sh
    grep -q 'codex plugin add "${CODEX_PONYTAIL_PLUGIN}"' scripts/update-agent-assets.sh
    grep -q 'update_claude_ponytail' scripts/update-agent-assets.sh
    grep -q 'update_codex_ponytail' scripts/update-agent-assets.sh
    grep -q 'PONYTAIL_DEFAULT_MODE' scripts/update-agent-assets.sh
    grep -q 'ponytail@ponytail' home/.chezmoitemplates/codex-config-managed.toml
    grep -q 'Ponytail' home/dot_config/codex/AGENTS.md
    grep -q 'ponytail@ponytail' home/dot_config/claude/rules/ponytail.md
}

@test "[common] agent asset lifecycle renders model profiles and permgate hooks" {
    grep -q 'aqua:tak848/ccgate' scripts/update-agent-assets.sh
    grep -q '"aqua:tak848/ccgate" = "0.9.5"' home/dot_mise/config.toml
    grep -q 'ccgate --version' scripts/update-agent-assets.sh
    grep -q 'permgate claude' home/.chezmoitemplates/claude-settings-managed.json
    grep -q 'permgate codex' home/.chezmoitemplates/codex-config-managed.toml
    ! grep -q 'ccgate' home/.chezmoitemplates/claude-settings-managed.json
    ! grep -q 'ccgate' home/.chezmoitemplates/codex-config-managed.toml
    grep -q '"llm_enabled": false' home/dot_agents/permgate-policy.yaml
    grep -q '"model": "claude-haiku-4-5-20251001"' home/dot_agents/permgate-policy.yaml
    grep -q '"model": "gpt-5.6-luna"' home/dot_agents/permgate-policy.yaml
    grep -q 'PERMGATE_INNER' home/dot_local/bin/common/executable_permgate
    grep -q 'PERMGATE_CODEX_COMMAND' home/dot_local/bin/common/executable_permgate
    [ ! -e home/dot_claude/ccgate.jsonnet ]
    [ ! -e home/dot_codex/ccgate.jsonnet ]
    grep -q '.codex/ccgate.jsonnet' home/.chezmoiremove
    grep -q 'model_profiles' home/dot_agents/agent-config.yaml
    grep -q 'model = ' home/dot_codex/standard.config.toml
    grep -q 'MODEL_PROFILE_INTERACTIVE' home/dot_agents/model-profiles.env
    grep -q 'model:' home/dot_claude/agents/express-explorer.md
    grep -q 'model_profiles' home/dot_config/claude/rules/model-selection.md
    grep -q 'model_profiles' home/dot_config/codex/AGENTS.md
}

@test "[common] README documents setup update doctor and upgrade lifecycle" {
    grep -q '### Lifecycle' README.md
    grep -q 'make setup' README.md
    grep -q 'make update' README.md
    grep -q 'make doctor' README.md
    grep -q 'make upgrade' README.md
    grep -q 'make upgrade SYSTEM=1' README.md
    grep -q 'setup.sh' README.md
    grep -Fq 'git -C "$(chezmoi source-path)" rev-parse --show-toplevel' README.md
}

@test "[common] README documents agent permission asset lifecycle" {
    grep -q '### Agent review and permission assets' README.md
    grep -q 'permgate' README.md
    grep -q 'model_profiles' README.md
    grep -q 'scripts/update-agent-assets.sh' README.md
    grep -q 'make require-crit-review' README.md
    grep -q 'AGENT_REVIEWED=1' README.md
    grep -q 'REVIEW_EVIDENCE' README.md
    grep -q 'crit comments --all --json <review.json>' README.md
    grep -q 'review_surface: crit-data' README.md
    grep -q 'review_source:' README.md
    grep -q 'CRIT_REVIEW=off' README.md
}

@test "[common] chezmoi source-path handoff resolves the repository root" {
    local tmpdir
    local repo_root
    local expected_root
    tmpdir="${BATS_TEST_TMPDIR}/source-path-handoff"
    repo_root="${tmpdir}/dotfiles"

    mkdir -p "${tmpdir}/bin" "${repo_root}/home"
    git init -q "${repo_root}"
    expected_root="$(cd "${repo_root}" && pwd -P)"

    cat > "${tmpdir}/bin/chezmoi" <<'CHEZMOI'
#!/usr/bin/env bash
set -euo pipefail

if [[ ${1:-} == "source-path" ]]; then
    printf '%s\n' "${CHEZMOI_SOURCE_PATH:?}"
    exit 0
fi

exit 64
CHEZMOI
    chmod +x "${tmpdir}/bin/chezmoi"

    run env PATH="${tmpdir}/bin:${PATH}" CHEZMOI_SOURCE_PATH="${repo_root}/home" bash -c '
        cd "$(git -C "$(chezmoi source-path)" rev-parse --show-toplevel 2>/dev/null)"
        pwd -P
    '

    [ "$status" -eq 0 ]
    [ "$output" = "${expected_root}" ]
}
