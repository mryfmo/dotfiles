#!/usr/bin/env bash

# @file scripts/deploy-kit.sh
# @brief Apply the kit's own chezmoi targets by name, refuse a locally edited one, and do nothing else.
# @description
#   The coordinator's deploy of a merged unit (regime-cutover U276; round 2 U276b, round 3 U276c, round 4 U276d).
#   `make update` is the operator's whole-home step: `chezmoi apply` over every managed target, the tool upgrades,
#   the asset updater and the herdr reload. This script is the chezmoi apply of the managed targets under the kit's
#   own roots and nothing more; the table below is the boundary, and everything else, the pinned asset refreshes
#   included, is left to `make update` and the asset updater under their own contracts:
#
#     root            | reason   | source
#     ~/.local/bin    | levers   | home/dot_local/bin (the orchestrator levers, the seat launcher)
#     ~/.agents       | assets   | home/dot_agents (skills, rules, omp profiles and policies, regime files)
#     ~/.dsh          | profiles | home/dot_dsh (the DSH profiles and plugins)
#
#   Each root is read physically before anything else (`cd -P`, `pwd -P`): a root that is missing, is a symbolic
#   link, or whose physical path is not the physical HOME joined with its name (a link on its path) refuses the run
#   with the path, since an apply through a link writes outside the boundary. The roots are read again after the
#   status read, and a root whose physical path changed between the two reads refuses: a root replaced during the
#   run would otherwise be applied through.
#
#   The operator's targets, never touched here: `~/.codex`, `~/.claude`, the shell rc files, `~/.config`,
#   `~/.omp/agent`, `~/Library/LaunchAgents`, `~/.local/share`, `~/.ssh`, `~/.gnupg`, and the run_ scripts of the
#   source, which a named apply does not run.
#
#   Steps, every producer status-checked so a failed read refuses before anything is applied (a failed read is
#   never an empty read; the message names the producer):
#   1. The physical root check above.
#   2. `chezmoi managed --path-style absolute --refresh-externals=never -- <roots>`, filtered to the roots and the
#      roots themselves by the table: the managed kit set. None found is a refusal.
#   3. `chezmoi status --path-style absolute --refresh-externals=never -- <roots>`, filtered the same way, then the
#      root re-read of step 1. A row whose second column is not blank is pending: `chezmoi apply` would change that
#      target. (One status read is the per-target oracle: it compares every target against the source as `chezmoi
#      verify` does, and a verify call per target is one chezmoi start each; verify runs once below, over the
#      applied names.) The listings are split in the shell, not through a here-string: bash backs a here-string with
#      a temporary file, and a redirection that fails there reads as an empty listing.
#   4. A row on a root itself is refused unless it is a plain pending change to the directory entry (first column
#      blank, second not `D`): `MM` on a root is the signature of a root replaced between the reads (chezmoi sees a
#      link where it wrote a directory), and a source that removes a root makes the table stale.
#   5. Every pending name must be a member of the managed kit set of step 2; one that is not (a target that
#      appeared between the two reads, or a row the status read spelled otherwise) is refused by name, since the
#      apply would then act on a name the managed listing never vouched for.
#   6. A pending row whose first column is not blank is refused: the target's content is not what chezmoi last
#      wrote, so an apply would drop an edit the source does not have (`MM` in `chezmoi status`, two-sided drift).
#      The refused rows are printed and nothing is applied.
#   7. `chezmoi apply --verbose --recursive=false` of the pending targets by name. Without `--recursive=false` a
#      pending directory is applied with everything under it, a child added after the status read included, and
#      that child was never in the managed listing; with it, the directory entry alone is applied, and every pending
#      child is in the set as its own row.
#   8. The applied set verified by row kind. A `D` row (the source retired the target) is verified by its absence:
#      `chezmoi verify` on a name the source no longer manages answers `not managed`, which is the retirement
#      succeeding, not a failure. Every other row is verified by one `chezmoi verify --recursive=false` over the
#      names that `chezmoi managed`, read once more after the apply, still lists; a non-`D` name it no longer lists
#      is refused, since its verified state is unknown.
#   9. The applied list. A second run finds nothing pending and exits 0.
#   `--refresh-externals=never`: chezmoi reads its whole source state, every external included, on each of these
#   commands, whatever targets are named; `never` serves a cached external whatever its age (the archives are
#   checksum-pinned, so age changes nothing), and only an external with no cache entry at all is fetched, by
#   chezmoi, as `make update`'s prefetch would.
# @option --dry-run Print the pending rows and the refusals; apply nothing. A refusal still exits 1, so a dry run
#   gives the verdict the real run would.
# @exitcode 0 The pending targets were applied and verified (or none was pending).
# @exitcode 1 A root is missing or a link, a root changed between the reads, a producer failed, no kit target is
#   managed, a row on a root is not a plain pending change, a pending name is not in the managed kit set, a pending
#   target is not what chezmoi last wrote, the apply or the verify failed, a retired target is still present.
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

#
# @description Whether a chezmoi target is one of the kit roots itself.
# @arg $1 path The target, as `chezmoi status --path-style absolute` prints it.
# @exitcode 0 A root of the table.
# @exitcode 1 Not a root.
#
function is_kit_root() {
    local target=$1 root
    for root in "${KIT_ROOTS[@]}"; do
        [[ ${target} != "${root}" ]] || return 0 # lint-comparisons: allow both sides are chezmoi's absolute target spellings (its destination directory joined with the managed path), the boundary table, not filesystem identities; the roots were read physically above
    done
    return 1
}

#
# @description Whether a chezmoi target is one of the kit roots or lies under one.
# @arg $1 path The target, as `chezmoi managed --path-style absolute` prints it.
# @exitcode 0 A root or under one.
# @exitcode 1 Not under one: the operator's.
#
function under_kit_root() {
    local target=$1 root
    for root in "${KIT_ROOTS[@]}"; do
        case ${target} in # lint-comparisons: allow both sides are chezmoi's absolute target spellings (its destination directory joined with the managed path), the boundary table, not filesystem identities; the roots were read physically above
        "${root}" | "${root}"/*) return 0 ;;
        esac
    done
    return 1
}

#
# @description Whether a target is a member of the managed kit set (the filtered `chezmoi managed` listing). A
#   linear scan: bash 3.2, the macOS default, has no associative arrays, and the pending set is small.
# @arg $1 path The target, as `chezmoi status --path-style absolute` prints it.
# @exitcode 0 A member.
# @exitcode 1 Not listed by `chezmoi managed` under the kit roots.
#
function in_kit_set() {
    local target=$1 member
    for member in "${kit_targets[@]}"; do
        [[ ${member} != "${target}" ]] || return 0 # lint-comparisons: allow both sides are chezmoi's absolute target spellings from the same destination directory
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

#
# @description Read the managed kit set: `chezmoi managed` over the roots, filtered to the roots by the table.
# @set kit_targets array The managed targets that are a kit root or lie under one.
# @exitcode 0 Read.
# @exitcode 1 `chezmoi managed` failed; kit_targets is unchanged and the caller names the consequence.
#
function read_kit_set() {
    local listing target
    listing="$(chezmoi managed --path-style absolute --refresh-externals=never -- "${KIT_ROOTS[@]}")" || return 1
    split_lines "${listing}"
    kit_targets=()
    for target in ${ROWS[@]+"${ROWS[@]}"}; do
        [[ -n ${target} ]] || continue
        if under_kit_root "${target}"; then
            kit_targets+=("${target}")
        fi
    done
}

#
# @description Print a kit root's physical path, or refuse: a root that is missing, is a symbolic link, cannot be
#   read physically, or whose physical path is not the physical HOME joined with its name (a link on its path) lets
#   an apply write outside the boundary.
# @arg $1 path The root, as the table spells it.
# @stdout The physical path (`cd -P`, `pwd -P`).
# @exitcode 0 A real directory at its own physical place.
# @exitcode 1 Refused; the message names the root and ends with `nothing applied`.
#
function root_physical_path() {
    local root=$1 physical
    if [[ -L ${root} ]]; then
        printf 'deploy-kit: the kit root %s is a symbolic link; an apply through it would write outside the kit roots, nothing applied.\n' "${root}" >&2
        return 1
    fi
    if [[ ! -d ${root} ]]; then
        printf 'deploy-kit: the kit root %s is missing; the kit has not been bootstrapped here (make update creates it), nothing applied.\n' "${root}" >&2
        return 1
    fi
    physical="$(cd -P -- "${root}" && pwd -P)" || {
        printf 'deploy-kit: the physical path of the kit root %s could not be read (pwd -P), nothing applied.\n' "${root}" >&2
        return 1
    }
    if [[ ${physical} != "${home_physical}/${root#"${HOME}/"}" ]]; then # lint-comparisons: allow both sides are pwd -P physical paths
        printf 'deploy-kit: the kit root %s resolves to %s, not %s; a link on its path would let an apply write outside the kit roots, nothing applied.\n' "${root}" "${physical}" "${home_physical}/${root#"${HOME}/"}" >&2
        return 1
    fi
    printf '%s\n' "${physical}"
}

home_physical="$(cd -P -- "${HOME}" && pwd -P)" || {
    printf 'deploy-kit: the physical path of HOME %s could not be read (pwd -P); the kit roots are unknown, nothing applied.\n' "${HOME}" >&2
    exit 1
}
root_physicals=()
for root in "${KIT_ROOTS[@]}"; do
    root_physical="$(root_physical_path "${root}")" || exit 1
    root_physicals+=("${root_physical}")
done

read_kit_set || {
    printf 'deploy-kit: chezmoi managed failed; the kit targets are unknown, nothing applied.\n' >&2
    exit 1
}
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
for index in "${!KIT_ROOTS[@]}"; do
    root_physical="$(root_physical_path "${KIT_ROOTS[index]}")" || {
        printf 'deploy-kit: the kit root %s changed between the managed read and the status read, nothing applied.\n' "${KIT_ROOTS[index]}" >&2
        exit 1
    }
    if [[ ${root_physical} != "${root_physicals[index]}" ]]; then # lint-comparisons: allow both sides are pwd -P physical paths of the same root, read before and after the status read
        printf 'deploy-kit: the kit root %s resolved to %s before the managed read and to %s after the status read; the roots changed during the run, nothing applied.\n' "${KIT_ROOTS[index]}" "${root_physicals[index]}" "${root_physical}" >&2
        exit 1
    fi
done

split_lines "${status_listing}"
pending=()
pending_rows=()
retired=()
to_verify=()
root_rows=()
unmanaged_rows=()
refused_rows=()
# Each row is `XY <target>`: X the change since chezmoi last wrote the target, Y the change an apply would make.
for row in ${ROWS[@]+"${ROWS[@]}"}; do
    [[ -n ${row} ]] || continue
    target=${row:3}
    under_kit_root "${target}" || continue
    [[ ${row:1:1} != ' ' ]] || continue
    if is_kit_root "${target}" && [[ ${row:0:1} != ' ' || ${row:1:1} == 'D' ]]; then
        root_rows+=("${row}")
    elif ! in_kit_set "${target}"; then
        unmanaged_rows+=("${row}")
    elif [[ ${row:0:1} != ' ' ]]; then
        refused_rows+=("${row}")
    else
        pending+=("${target}")
        pending_rows+=("${row}")
        if [[ ${row:1:1} == 'D' ]]; then
            retired+=("${target}")
        else
            to_verify+=("${target}")
        fi
    fi
done

printf 'deploy-kit: pending: %d\n' "${#pending[@]}"
for row in ${pending_rows[@]+"${pending_rows[@]}"}; do
    printf '  %s\n' "${row}"
done
if ((${#root_rows[@]} > 0)); then
    printf 'deploy-kit: refused: %d kit roots are not what chezmoi last wrote or are removed by the source (status row on the root itself); the root was replaced between the reads or the root table is stale, nothing applied:\n' "${#root_rows[@]}" >&2
    for row in "${root_rows[@]}"; do
        printf '  %s\n' "${row}" >&2
    done
    exit 1
fi
if ((${#unmanaged_rows[@]} > 0)); then
    printf 'deploy-kit: refused: %d pending names are not in the managed kit set (chezmoi managed did not list them under the kit roots); the source changed between the two reads or the listings disagree, nothing applied:\n' "${#unmanaged_rows[@]}" >&2
    for row in "${unmanaged_rows[@]}"; do
        printf '  %s\n' "${row}" >&2
    done
    exit 1
fi
if ((${#refused_rows[@]} > 0)); then
    printf 'deploy-kit: refused: %d kit targets are not what chezmoi last wrote (status first column); an apply would drop a local edit the source does not have, nothing applied:\n' "${#refused_rows[@]}" >&2
    for row in "${refused_rows[@]}"; do
        printf '  %s\n' "${row}" >&2
    done
    exit 1
fi
if [[ ${dry_run} == true ]]; then
    printf 'deploy-kit: dry run; nothing applied.\n'
    exit 0
fi

if ((${#pending[@]} > 0)); then
    # stdin closed: a target changed between the status read and here would make chezmoi prompt; it fails instead.
    if ! chezmoi apply --verbose --recursive=false --refresh-externals=never "${pending[@]}" < /dev/null; then
        printf 'deploy-kit: chezmoi apply failed; the applied set is unknown, run chezmoi status over the kit roots.\n' >&2
        exit 1
    fi
    present=()
    for target in ${retired[@]+"${retired[@]}"}; do
        # -e follows a link, so a dangling link is present only to -L.
        if [[ -e ${target} || -L ${target} ]]; then
            present+=("${target}")
        fi
    done
    if ((${#present[@]} > 0)); then
        printf 'deploy-kit: %d retired targets are still present after the apply (status D rows); the retirement did not take, run chezmoi status over the kit roots:\n' "${#present[@]}" >&2
        for target in "${present[@]}"; do
            printf '  %s\n' "${target}" >&2
        done
        exit 1
    fi
fi
if ((${#to_verify[@]} > 0)); then
    read_kit_set || {
        printf 'deploy-kit: chezmoi managed failed after the apply; the applied targets are unverified, run chezmoi status over the kit roots.\n' >&2
        exit 1
    }
    unlisted=()
    for target in "${to_verify[@]}"; do
        in_kit_set "${target}" || unlisted+=("${target}")
    done
    if ((${#unlisted[@]} > 0)); then
        printf 'deploy-kit: %d applied targets are no longer in the managed kit set; the source changed during the run and their verified state is unknown, run chezmoi status over the kit roots:\n' "${#unlisted[@]}" >&2
        for target in "${unlisted[@]}"; do
            printf '  %s\n' "${target}" >&2
        done
        exit 1
    fi
    if ! chezmoi verify --recursive=false --refresh-externals=never "${to_verify[@]}"; then
        printf 'deploy-kit: chezmoi verify finds an applied target still differing from the source.\n' >&2
        exit 1
    fi
fi
printf 'deploy-kit: applied: %d\n' "${#pending[@]}"
for target in ${pending[@]+"${pending[@]}"}; do
    printf '  %s\n' "${target}"
done
