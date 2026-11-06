#!/usr/bin/env bash

# @file scripts/deploy-kit.sh
# @brief Apply the kit's own chezmoi targets by name, refuse a locally edited one, then run the kit's asset steps.
# @description
#   The coordinator's deploy of a merged unit (regime-cutover U276, round 2 U276b). `make update` is the operator's
#   whole-home step: `chezmoi apply` over every managed target, the tool upgrades, the whole asset updater and the
#   herdr reload. This script applies only the managed targets under the kit's own roots and runs only the asset
#   steps whose writes stay under those roots; the two tables below are the boundary, and everything else is left
#   to `make update`:
#
#     root            | reason   | source
#     ~/.local/bin    | levers   | home/dot_local/bin (the orchestrator levers, the seat launcher)
#     ~/.agents       | assets   | home/dot_agents (skills, rules, omp profiles and policies, regime files)
#     ~/.dsh          | profiles | home/dot_dsh (the DSH profiles and plugins)
#
#   Each root is read physically before anything else (`cd -P`, `pwd -P`): a root that is missing, is a symbolic
#   link, or whose physical path is not the physical HOME joined with its name (a link on its path) refuses the run
#   with the path, since an apply through a link writes outside the boundary.
#
#     kit asset function (scripts/update-agent-assets.sh)  | writes
#     retire_shared_pstack_copies                          | ~/.agents/skills/<name> (copies identical to ~/.agents/pstack/skills)
#     retire_marketplace_dev_workflows                     | ~/.agents/plugins/marketplace.json
#     retire_agmsg_shim                                    | ~/.agents/bin/agy-tui, ~/.agents/bin
#     update_security_audit_skill                          | ~/.agents/skills/security-audit, ~/.agents/.installed-manifest.json
#     update_deepseek_harness                              | ~/.dsh/dsh, ~/.dsh/bin/dsh, ~/.dsh/profiles/thak/node_modules, ~/.agents/.installed-manifest.json
#     update_compactiondb                                  | ~/.agents/compactiondb, ~/.agents/.installed-manifest.json
#     manifest_prune_retired                               | ~/.agents/.installed-manifest.json
#
#   The updater's other steps write under `~/.claude`, `~/.codex` (`refresh_codex_hook_trust` force-applies the
#   Codex configs), `~/.local/lib`, `~/.local/share`, `~/.local/state`, the npm and uv tool trees, the mise installs
#   and herdr's hooks: the operator's. This script calls the updater once per function above, by name, and never
#   its `main`.
#
#   The operator's targets, never touched here: `~/.codex`, `~/.claude`, the shell rc files, `~/.config`,
#   `~/.omp/agent`, `~/Library/LaunchAgents`, `~/.local/share`, `~/.ssh`, `~/.gnupg`, and the run_ scripts of the
#   source, which a named apply does not run.
#
#   Steps, every producer status-checked so a failed read refuses before anything is applied (a failed read is
#   never an empty read; the message names the producer):
#   1. The physical root check above.
#   2. `chezmoi managed --path-style absolute --refresh-externals=never -- <roots>`, filtered to the roots by the
#      table: the kit targets. None found is a refusal.
#   3. `chezmoi status --path-style absolute --refresh-externals=never -- <roots>`, filtered the same way. A row whose
#      second column is not blank is pending: `chezmoi apply` would change that target. (One status read is the
#      per-target oracle: it compares every target against the source as `chezmoi verify` does, and a verify call
#      per target is one chezmoi start each; verify runs once below, over the applied names.) The listings are
#      split in the shell, not through a here-string: bash backs a here-string with a temporary file, and a
#      redirection that fails there reads as an empty listing.
#   4. A pending row whose first column is not blank is refused: the target's content is not what chezmoi last
#      wrote, so an apply would drop an edit the source does not have (`MM` in `chezmoi status`, two-sided drift).
#      The refused rows are printed and nothing is applied.
#   5. `chezmoi apply --verbose` of the pending targets by name, then `chezmoi verify` of the same names.
#   6. `scripts/update-agent-assets.sh <function>` for each row of the asset table, in order; the first failure
#      stops the run. The asset steps run when nothing was pending too: a merged unit may change only the pins
#      they install.
#   7. The applied list. A second run finds nothing pending and exits 0.
#   `--refresh-externals=never`: chezmoi reads its whole source state, every external included, on each of these
#   commands, whatever targets are named; `never` serves a cached external whatever its age (the archives are
#   checksum-pinned, so age changes nothing), and only an external with no cache entry at all is fetched, by
#   chezmoi, as `make update`'s prefetch would.
# @option --dry-run Print the pending rows and the refusals; apply nothing, run no asset step. A refusal still
#   exits 1, so a dry run gives the verdict the real run would.
# @exitcode 0 The pending targets were applied (or none was pending) and every asset step passed.
# @exitcode 1 A root is missing or a link, a producer failed, no kit target is managed, a pending target is not what
#   chezmoi last wrote, the apply, the verify or an asset step failed.
# @exitcode 2 Usage.
# @example
#   ./scripts/deploy-kit.sh --dry-run

set -Eeuo pipefail

readonly KIT_ROOTS=("${HOME}/.local/bin" "${HOME}/.agents" "${HOME}/.dsh")
# The asset table above, in the order the updater's main runs them.
readonly KIT_ASSET_FUNCTIONS=(
    retire_shared_pstack_copies
    retire_marketplace_dev_workflows
    retire_agmsg_shim
    update_security_audit_skill
    update_deepseek_harness
    update_compactiondb
    manifest_prune_retired
)

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
    printf 'deploy-kit: dirname failed on %s; the asset updater script is unknown, nothing applied.\n' "${BASH_SOURCE[0]}" >&2
    exit 1
}
readonly ASSETS_SCRIPT="${script_dir}/update-agent-assets.sh" # run below once per kit function, never bare (its main is the operator's)

#
# @description Whether a chezmoi target lies under one of the kit roots.
# @arg $1 path The target, as `chezmoi managed --path-style absolute` prints it.
# @exitcode 0 Under a kit root.
# @exitcode 1 Not under one: the operator's.
#
function under_kit_root() {
    local target=$1 root
    for root in "${KIT_ROOTS[@]}"; do
        case ${target} in # lint-comparisons: allow both sides are chezmoi's absolute target spellings (its destination directory joined with the managed path), the boundary table, not filesystem identities; the roots were read physically above
        "${root}"/*) return 0 ;;
        esac
    done
    return 1
}

#
# @description Split a producer's captured output into ROWS, one line each, with string operations alone. A
#   `while read` over a here-string needs a temporary file, and a failure to make it read as an empty listing.
# @arg $1 string The output, as a command substitution returns it (no trailing newline).
# @set ROWS array The lines, empty ones included.
#
function split_lines() {
    local text=$1
    ROWS=()
    while [[ -n ${text} ]]; do
        ROWS+=("${text%%$'\n'*}")
        [[ ${text} == *$'\n'* ]] || break
        text=${text#*$'\n'}
    done
}

home_physical="$(cd -P -- "${HOME}" && pwd -P)" || {
    printf 'deploy-kit: the physical path of HOME %s could not be read; the kit roots are unknown, nothing applied.\n' "${HOME}" >&2
    exit 1
}
for root in "${KIT_ROOTS[@]}"; do
    if [[ -L ${root} ]]; then
        printf 'deploy-kit: the kit root %s is a symbolic link; an apply through it would write outside the kit roots, nothing applied.\n' "${root}" >&2
        exit 1
    fi
    if [[ ! -d ${root} ]]; then
        printf 'deploy-kit: the kit root %s is missing; the kit has not been bootstrapped here (make update creates it), nothing applied.\n' "${root}" >&2
        exit 1
    fi
    root_physical="$(cd -P -- "${root}" && pwd -P)" || {
        printf 'deploy-kit: the physical path of the kit root %s could not be read, nothing applied.\n' "${root}" >&2
        exit 1
    }
    if [[ ${root_physical} != "${home_physical}/${root#"${HOME}/"}" ]]; then # lint-comparisons: allow both sides are pwd -P physical paths
        printf 'deploy-kit: the kit root %s resolves to %s, not %s; a link on its path would let an apply write outside the kit roots, nothing applied.\n' "${root}" "${root_physical}" "${home_physical}/${root#"${HOME}/"}" >&2
        exit 1
    fi
done

if ! managed_listing="$(chezmoi managed --path-style absolute --refresh-externals=never -- "${KIT_ROOTS[@]}")"; then
    printf 'deploy-kit: chezmoi managed failed; the kit targets are unknown, nothing applied.\n' >&2
    exit 1
fi
split_lines "${managed_listing}"
kit_targets=()
for target in ${ROWS[@]+"${ROWS[@]}"}; do
    [[ -n ${target} ]] || continue
    if under_kit_root "${target}"; then
        kit_targets+=("${target}")
    fi
done
printf 'deploy-kit: kit roots: %s\n' "${KIT_ROOTS[*]}"
printf 'deploy-kit: managed kit targets: %d\n' "${#kit_targets[@]}"
if ((${#kit_targets[@]} == 0)); then
    printf 'deploy-kit: chezmoi manages no target under the kit roots; the source or the root table is wrong, nothing applied.\n' >&2
    exit 1
fi

if ! status_listing="$(chezmoi status --path-style absolute --refresh-externals=never -- "${KIT_ROOTS[@]}")"; then
    printf 'deploy-kit: chezmoi status failed; the drift of the kit targets is unknown, nothing applied.\n' >&2
    exit 1
fi
split_lines "${status_listing}"
pending=()
pending_rows=()
refused_rows=()
# Each row is `XY <target>`: X the change since chezmoi last wrote the target, Y the change an apply would make.
for row in ${ROWS[@]+"${ROWS[@]}"}; do
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
done

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
    printf 'deploy-kit: dry run; nothing applied, the kit asset steps of %s not run.\n' "${ASSETS_SCRIPT}"
    exit 0
fi

if ((${#pending[@]} > 0)); then
    # stdin closed: a target changed between the status read and here would make chezmoi prompt; it fails instead.
    if ! chezmoi apply --verbose --refresh-externals=never "${pending[@]}" < /dev/null; then
        printf 'deploy-kit: chezmoi apply failed; the kit asset steps not run.\n' >&2
        exit 1
    fi
    if ! chezmoi verify --refresh-externals=never "${pending[@]}"; then
        printf 'deploy-kit: chezmoi verify finds an applied target still differing from the source; the kit asset steps not run.\n' >&2
        exit 1
    fi
fi
for kit_function in "${KIT_ASSET_FUNCTIONS[@]}"; do
    printf 'deploy-kit: %s %s\n' "${ASSETS_SCRIPT}" "${kit_function}"
    if ! "${ASSETS_SCRIPT}" "${kit_function}"; then
        printf 'deploy-kit: %s %s failed; the later kit asset steps not run.\n' "${ASSETS_SCRIPT}" "${kit_function}" >&2
        exit 1
    fi
done
printf 'deploy-kit: applied: %d\n' "${#pending[@]}"
for target in ${pending[@]+"${pending[@]}"}; do
    printf '  %s\n' "${target}"
done
