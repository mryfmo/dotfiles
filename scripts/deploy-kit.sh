#!/usr/bin/env bash

# @file scripts/deploy-kit.sh
# @brief Apply the kit's own chezmoi targets by name, refuse a locally edited one, then refresh the agent assets.
# @description
#   The coordinator's deploy of a merged unit (regime-cutover U276). `make update` is the operator's whole-home
#   step: `chezmoi apply` over every managed target, the tool upgrades and the herdr reload. This script applies
#   only the managed targets under the kit's own roots, the one table below, and leaves every other target to
#   `make update`:
#
#     root            | reason   | source
#     ~/.local/bin    | levers   | home/dot_local/bin (the orchestrator levers, the seat launcher)
#     ~/.agents       | assets   | home/dot_agents (skills, rules, omp profiles and policies, regime files)
#     ~/.dsh          | profiles | home/dot_dsh (the DSH profiles and plugins)
#
#   The operator's targets, never touched here: `~/.codex`, `~/.claude`, the shell rc files, `~/.config`,
#   `~/.omp/agent`, `~/Library/LaunchAgents`, `~/.local/share`, `~/.ssh`, `~/.gnupg`, and the run_ scripts of the
#   source, which a named apply does not run.
#
#   Steps, every chezmoi read status-checked so a failed read refuses before anything is applied:
#   1. `chezmoi managed --path-style absolute`, filtered to the roots: the kit targets. None found is a refusal.
#   2. `chezmoi status --path-style absolute`, filtered the same way. A row whose second column is not blank is
#      pending: `chezmoi apply` would change that target. (One status read is the per-target oracle: it compares
#      every target against the source as `chezmoi verify` does, and a verify call per target is one chezmoi start
#      each; verify runs once below, over the applied names.)
#   3. A pending row whose first column is not blank is refused: the target's content is not what chezmoi last
#      wrote, so an apply would drop an edit the source does not have (`MM` in `chezmoi status`, two-sided drift).
#      The refused rows are printed and nothing is applied.
#   4. `chezmoi apply --verbose` of the pending targets by name, then `chezmoi verify` of the same names, then
#      scripts/update-agent-assets.sh. The asset refresh runs when nothing was pending too: a merged unit may
#      change only the pins that script installs.
#   5. The applied list. A second run finds nothing pending and exits 0.
# @option --dry-run Print the pending rows and the refusals; apply nothing, run no asset refresh. A refusal still
#   exits 1, so a dry run gives the verdict the real run would.
# @exitcode 0 The pending targets were applied (or none was pending) and the asset refresh passed.
# @exitcode 1 A chezmoi read failed, no kit target is managed, a pending target is not what chezmoi last wrote,
#   the apply, the verify or the asset refresh failed.
# @exitcode 2 Usage.
# @example
#   ./scripts/deploy-kit.sh --dry-run

set -Eeuo pipefail

readonly KIT_ROOTS=("${HOME}/.local/bin" "${HOME}/.agents" "${HOME}/.dsh")

dry_run=false
for argument in "$@"; do
    case ${argument} in
    --dry-run) dry_run=true ;;
    *)
        printf 'usage: %s [--dry-run]\n' "$0" >&2
        exit 2
        ;;
    esac
done

# dirname is captured on its own line so its status is read.
script_dir="$(dirname -- "${BASH_SOURCE[0]}")" || {
    printf 'deploy-kit: dirname failed on %s; the asset refresh script is unknown, nothing applied.\n' "${BASH_SOURCE[0]}" >&2
    exit 1
}
readonly ASSETS_SCRIPT="${script_dir}/update-agent-assets.sh"

#
# @description Whether a chezmoi target lies under one of the kit roots.
# @arg $1 path The target, as `chezmoi managed --path-style absolute` prints it.
# @exitcode 0 Under a kit root.
# @exitcode 1 Not under one: the operator's.
#
function under_kit_root() {
    local target=$1 root
    for root in "${KIT_ROOTS[@]}"; do
        case ${target} in # lint-comparisons: allow both sides are chezmoi's absolute target spellings (its destination directory joined with the managed path), the boundary table, not filesystem identities
        "${root}"/*) return 0 ;;
        esac
    done
    return 1
}

if ! managed_listing="$(chezmoi managed --path-style absolute)"; then
    printf 'deploy-kit: chezmoi managed failed; the kit targets are unknown, nothing applied.\n' >&2
    exit 1
fi
kit_targets=()
while IFS= read -r target; do
    [[ -n ${target} ]] || continue
    if under_kit_root "${target}"; then
        kit_targets+=("${target}")
    fi
done <<< "${managed_listing}"
printf 'deploy-kit: kit roots: %s\n' "${KIT_ROOTS[*]}"
printf 'deploy-kit: managed kit targets: %d\n' "${#kit_targets[@]}"
if ((${#kit_targets[@]} == 0)); then
    printf 'deploy-kit: chezmoi manages no target under the kit roots; the source or the root table is wrong, nothing applied.\n' >&2
    exit 1
fi

if ! status_listing="$(chezmoi status --path-style absolute)"; then
    printf 'deploy-kit: chezmoi status failed; the drift of the kit targets is unknown, nothing applied.\n' >&2
    exit 1
fi
pending=()
pending_rows=()
refused_rows=()
# Each row is `XY <target>`: X the change since chezmoi last wrote the target, Y the change an apply would make.
while IFS= read -r row; do
    [[ -n ${row} ]] || continue
    target=${row:3}
    under_kit_root "${target}" || continue
    [[ ${row:1:1} != ' ' ]] || continue
    if [[ ${row:0:1} != ' ' ]]; then
        refused_rows+=("${row}")
    else
        pending+=("${target}")
        pending_rows+=("${row}")
    fi
done <<< "${status_listing}"

printf 'deploy-kit: pending: %d\n' "${#pending[@]}"
for row in ${pending_rows[@]+"${pending_rows[@]}"}; do
    printf '  %s\n' "${row}"
done
if ((${#refused_rows[@]} > 0)); then
    printf 'deploy-kit: refused: %d kit targets are not what chezmoi last wrote (status first column); an apply would drop a local edit the source does not have, nothing applied:\n' "${#refused_rows[@]}" >&2
    for row in "${refused_rows[@]}"; do
        printf '  %s\n' "${row}" >&2
    done
    exit 1
fi
if [[ ${dry_run} == true ]]; then
    printf 'deploy-kit: dry run; nothing applied, %s not run.\n' "${ASSETS_SCRIPT}"
    exit 0
fi

if ((${#pending[@]} > 0)); then
    # stdin closed: a target changed between the status read and here would make chezmoi prompt; it fails instead.
    if ! chezmoi apply --verbose "${pending[@]}" < /dev/null; then
        printf 'deploy-kit: chezmoi apply failed; %s not run.\n' "${ASSETS_SCRIPT}" >&2
        exit 1
    fi
    if ! chezmoi verify "${pending[@]}"; then
        printf 'deploy-kit: chezmoi verify finds an applied target still differing from the source; %s not run.\n' "${ASSETS_SCRIPT}" >&2
        exit 1
    fi
fi
if ! "${ASSETS_SCRIPT}"; then
    printf 'deploy-kit: %s failed.\n' "${ASSETS_SCRIPT}" >&2
    exit 1
fi
printf 'deploy-kit: applied: %d\n' "${#pending[@]}"
for target in ${pending[@]+"${pending[@]}"}; do
    printf '  %s\n' "${target}"
done
