#!/usr/bin/env bash
# @file seat-settings-render.sh
# @brief The one srt settings writer of the seat levers: the rows every seat's settings share and the JSON text they are written in, sourced by hcom-seat and acp-broker.
# @description
#   Regime-cutover U344 (M-24 part 2). Sourced by `hcom-seat` (every role's settings) and by `acp-broker` (the
#   worker's settings, per connection) from the directory they run from (`LEVER_DIR`), never run on its own. It
#   checks its own sha256 against its `claude.levers.sha256.seat-settings-render.sh` pin first, like regime-env, so a
#   rewritten helper stops the caller. It holds what the two renderings shared by copy until this unit (the U343
#   header: "This copy of the dsh row's shape is interim: U344 extracts one writer for both levers"): the path rule
#   every settings row obeys (clean_path, clean_row), the fixed rows of the deny table (the credential stores denied
#   for read, the project files denied for write under a seat's own directory, the rows denied for write under the
#   shared Claude Code directory), the domain list, and the
#   JSON writer (seat_settings_rows_json for a list, seat_settings_json for the file's text). It judges nothing (each
#   lever's `settings_judge` stays its own) and writes no file (the caller writes the text it is handed, as before);
#   each lever passes its rows, its `allowLocalBinding` value, its `allowUnixSockets` list and its Linux tool
#   fragment. `acp-broker` reads the deny table back from the Router's settings `hcom-seat` rendered, so the rows
#   below are spelled once and rendered once. tests/unit/test_acp_broker.py
#   `test_one_settings_writer_renders_the_worker_and_the_dsh_row_byte_for_byte` holds the two levers' files
#   byte-identical but the role's own rows.
# @description Refuse to run unless this file's sha256 equals its pin in the manifest beside it (regime-cutover U31):
#   `~/.agents/agent-config.yaml` for the installed copy under ~/.local/bin/common, which a sandboxed session cannot
#   write, else the checkout's home/dot_agents/agent-config.yaml. Every read is checked; a failure exits 2 naming the
#   file. The pin is the `claude.levers.sha256.<name>` line, which `scripts/generate-agent-configs.py` refreshes.
# @set LEVER_MANIFEST The manifest the pin came from.
# @set LEVER_DIR The physical directory of this file, where the levers that source it sit.
lever_self_check() {
    local src dir self name pin digest home
    # The directory is split from the path in the shell, so no external producer (dirname) can fail unseen.
    src=${BASH_SOURCE[0]}
    case ${src} in
    */*) dir=${src%/*} ;;
    *) dir=. ;;
    esac
    [[ -n ${dir} ]] || dir=/
    dir=$(cd "${dir}" && pwd -P) || {
        echo "${src##*/}: refused: cannot resolve the script directory of ${src}" >&2
        exit 2
    }
    self=${dir}/${BASH_SOURCE[0]##*/}
    # shellcheck disable=SC2034 # read by the levers that source this helper from this directory
    LEVER_DIR=${dir}
    name=${self##*/}
    home=$(cd "${HOME}" 2> /dev/null && pwd -P) || home=''
    if [[ -n ${home} && ${dir} == "${home}/.local/bin/common" ]]; then # lint-comparisons: allow both sides are pwd -P forms
        LEVER_MANIFEST=${HOME}/.agents/agent-config.yaml
    else
        LEVER_MANIFEST=${dir}/../../home/dot_agents/agent-config.yaml
    fi
    [[ -r ${LEVER_MANIFEST} ]] || {
        echo "${name}: refused: manifest unreadable: ${LEVER_MANIFEST}" >&2
        exit 2
    }
    pin=$(sed -n -E "s/^      ${name//./\\.}: ([0-9a-f]{64})\$/\\1/p" "${LEVER_MANIFEST}") || {
        echo "${name}: refused: cannot read ${LEVER_MANIFEST}" >&2
        exit 2
    }
    [[ ${pin} =~ ^[0-9a-f]{64}$ ]] || {
        echo "${name}: refused: no single sha256 pin for ${name} in ${LEVER_MANIFEST}" >&2
        exit 2
    }
    if command -v sha256sum > /dev/null; then
        digest=$(sha256sum < "${self}") || digest=''
    else
        digest=$(shasum -a 256 < "${self}") || digest=''
    fi
    digest=${digest%% *}
    [[ ${digest} =~ ^[0-9a-f]{64}$ ]] || {
        echo "${name}: refused: cannot hash ${self}" >&2
        exit 2
    }
    [[ ${digest} == "${pin}" ]] || {
        echo "${name}: refused: sha256 ${digest} of ${self} differs from the pin in ${LEVER_MANIFEST}" >&2
        exit 2
    }
}
lever_self_check

# @description Succeed when `$1` is a clean absolute path that srt cannot read as a pattern: `/` followed by
#   components of `[A-Za-z0-9._@+-]` only (no glob metacharacter `*?[]{}`, no whitespace, no quote or backslash), none
#   of them empty, `.` or `..`, and no trailing `/`. srt 0.0.81 turns a settings path into a Seatbelt regex or a glob,
#   so `/private/tmp/hcom*` would grant its siblings; a clean path names exactly itself (regime-cutover U85).
# @arg $1 string The path.
# @exitcode 1 The path is not clean.
clean_path() {
    [[ $1 =~ ^(/[A-Za-z0-9._@+-]+)+$ ]] || return 1
    [[ /$1/ != */./* && /$1/ != */../* ]] # lint-comparisons: allow a component test on one path, no path compare
}

# @description Succeed when `$1` is a row the settings may carry: a clean path, or (for `denyWrite`, `$2` = 1) one of
#   the macOS worktree patterns `hcom-seat` renders, a clean prefix and the fixed `worktrees/*/<file>` suffix, the
#   one place a settings entry is not a clean path (srt reads `*` as `[^/]*`).
# @arg $1 string The row.
# @arg $2 int 1 when the pattern form is allowed.
# @exitcode 1 The row is neither.
clean_row() {
    clean_path "$1" && return 0
    (($2)) || return 1
    [[ $1 =~ ^(/[A-Za-z0-9._@+-]+)+/worktrees/\*/(config\.worktree|info|commondir|gitdir)$ ]] || return 1
    [[ /${1%/worktrees/*}/ != */./* && /${1%/worktrees/*}/ != */../* ]] # lint-comparisons: allow a component test on one pattern's clean prefix, no path compare
}

# The fixed rows of the deny table, relative to the root each is rendered under (hcom-seat seat_settings_render
# renders them for every role; acp-broker reads them back from the Router's settings, re-rooting the project-file rows
# under the task cwd, so each list is spelled here once). The credential stores every seat is denied for read, under
# HOME. The project files a seat is denied for write under its own directory (a cwd that holds `.omp` is refused
# outright: omp merges it before `disabledProviders` applies; the hook shims under `.claude/hooks` import their code
# from `.claude/contextdb`, run by sessions outside the seat). The rows denied for write under the shared Claude Code
# directory, what another seat's child or the operator's login command would load (regime-cutover U318, U190).
# shellcheck disable=SC2034 # read by the levers that source this helper
SEAT_SETTINGS_CREDENTIAL_DENIES=(.ssh .gnupg .aws .netrc .docker .kube .config/gcloud .codex .omp/agent)
# shellcheck disable=SC2034 # read by the levers that source this helper
SEAT_SETTINGS_PROJECT_FILES=(.claude/settings.json .claude/settings.local.json .claude/hooks .claude/contextdb .omp .codex .envrc .mcp.json)
# shellcheck disable=SC2034 # read by the levers that source this helper
SEAT_SETTINGS_CLAUDE_ROWS=(settings.json settings.local.json rules hooks plugins skills commands agents)
# The outbound hosts every seat may reach (`network.allowedDomains`): GitHub and its API, upload, codeload and content
# hosts; PyPI; the Anthropic and Claude hosts; the OpenAI hosts of the openai-siwc route.
SEAT_SETTINGS_DOMAINS='"github.com","api.github.com","uploads.github.com","codeload.github.com","objects.githubusercontent.com"'
SEAT_SETTINGS_DOMAINS+=',"raw.githubusercontent.com","release-assets.githubusercontent.com","pypi.org","files.pythonhosted.org"'
SEAT_SETTINGS_DOMAINS+=',"api.anthropic.com","claude.ai","platform.claude.com","console.anthropic.com"'
SEAT_SETTINGS_DOMAINS+=',"chatgpt.com","auth.openai.com","api.openai.com"'

# @description Print a JSON array of the rows `$@` in their order, each held to clean_row first, so no JSON escaping is
#   needed and no settings tool runs; a row that is not clean fails the function with nothing printed, and the caller
#   refuses naming the list (standing order 21: the caller reads this status).
# @arg $1 int 1 when the macOS worktree pattern form is allowed (a `denyWrite` list).
# @arg $@ string The rows after it.
# @stdout The array, `[]` for no rows.
# @exitcode 1 A row is not one the settings may carry.
seat_settings_rows_json() {
    local patterns=$1 row out='' sep=''
    shift
    for row in "$@"; do
        clean_row "${row}" "${patterns}" || return 1
        out+=${sep}\"${row}\"
        sep=,
    done
    printf '[%s]' "${out}"
}

# @description Set `settings_json` to the one-line text of a seat's srt settings file from its rendered lists: the
#   network block (the domain list above, no denied domain, the `allowUnixSockets` list `$2`, the trustd Mach
#   lookup every sandboxed process needs, the `allowLocalBinding` value `$1`), the filesystem block in the order
#   `denyRead`, `allowRead`, `allowWrite`, `denyWrite`, `allowPty` true and, on Linux, the tool fragment `$7` naming
#   the checked bwrap, socat and rg. The key order and the compact form are what the levers wrote before this helper
#   (hcom-seat seat_sandbox_write, acp-broker), so every earlier head's settings re-render byte for byte.
# @arg $1 string `true` or `false`, the role's `allowLocalBinding`.
# @arg $2 string The `allowUnixSockets` JSON array (seat_settings_rows_json; `[]` for every role but the router).
# @arg $3 string The `denyRead` JSON array.
# @arg $4 string The `allowRead` JSON array.
# @arg $5 string The `allowWrite` JSON array.
# @arg $6 string The `denyWrite` JSON array.
# @arg $7 string The Linux tool fragment (`,"bwrapPath":…`), empty on macOS.
# @set settings_json The text, without a trailing newline.
# @exitcode 1 `$1` is neither `true` nor `false`.
seat_settings_json() {
    [[ $1 == true || $1 == false ]] || return 1
    settings_json="{\"network\":{\"allowedDomains\":[${SEAT_SETTINGS_DOMAINS}],\"deniedDomains\":[],\"allowUnixSockets\":$2"
    settings_json+=",\"allowMachLookup\":[\"com.apple.trustd.agent\"],\"allowLocalBinding\":$1}"
    settings_json+=",\"filesystem\":{\"denyRead\":$3,\"allowRead\":$4"
    settings_json+=",\"allowWrite\":$5,\"denyWrite\":$6},\"allowPty\":true$7}"
}
