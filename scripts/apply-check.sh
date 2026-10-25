#!/usr/bin/env bash

# @file scripts/apply-check.sh
# @brief Apply home/ as a fresh client or server into a scratch HOME, verify it, and run the credential-free doctor checks.
# @description
#   The disposable check `make apply-check` runs inside a container, for client
#   and server. It copies the parts of the working tree
#   that the apply and the checks read (.chezmoiroot, home/, scripts/) into a
#   scratch directory, applies from that copy as setup.sh's chezmoi would from a
#   clone, and points HOME at a scratch home, so the tree, the caller's HOME and
#   the caller's chezmoi config stay untouched.
#   It runs only where scripts/lib/ci-runner.sh's is_ci_runner holds: a GitHub
#   Actions runner, or the container `make apply-check` starts, which declares
#   itself one because it is as disposable and keyless as a runner. There the
#   chezmoi config renders without age encryption (home/.chezmoi.yaml.tmpl), and,
#   as setup.sh does without a tty, the encrypted_* targets leave the copy.
#   Externals are downloads and scripts are installers, so neither is applied;
#   the public-bootstrap CI job runs both. That required job also runs this
#   script, on the runner, for a diff whose home/ paths are all render-only.
#   After `chezmoi init`, `apply` and `verify` it runs the parts of `make doctor`
#   that judge the applied files and need no installed tool and no login:
#   `chezmoi doctor --no-network` and scripts/check-agent-runtime.py (its GitHub
#   login line stays a warning). The rest of `make doctor` stays out:
#   scripts/check-tools.sh and the omp asset checks require mise, uv, gh and omp,
#   which only the skipped installers put on a host, and scripts/check-sleep.sh
#   reads the host's power setting, which no apply changes. Every step's result is
#   printed, then one summary line.
# @arg $1 string `--system`
# @arg $2 string `client` or `server`
# @option --chezmoi <path> The chezmoi binary (default: `chezmoi` on PATH).
# @exitcode 0 Every step passed.
# @exitcode 1 A step failed.
# @exitcode 2 A usage error, or this is not a CI runner.

set -Eeuo pipefail

# dirname is captured on its own line: inside the cd its status would be lost.
script_dir="$(dirname -- "${BASH_SOURCE[0]}")" || {
    echo "apply-check: dirname failed on ${BASH_SOURCE[0]}; the repository root is unknown" >&2
    exit 2
}
repo_root="$(cd "${script_dir}/.." && pwd)" || exit 2
# shellcheck source=scripts/lib/ci-runner.sh
source "${script_dir}/lib/ci-runner.sh"

system=""
chezmoi_bin=chezmoi
while [ "$#" -gt 0 ]; do
    case "$1" in
    --system)
        system="${2:-}"
        shift 2 || shift
        ;;
    --chezmoi)
        chezmoi_bin="${2:-}"
        shift 2 || shift
        ;;
    *)
        echo "apply-check: unknown argument: $1 (usage: apply-check.sh --system client|server [--chezmoi PATH])" >&2
        exit 2
        ;;
    esac
done
case "${system}" in
client | server) ;;
*)
    echo "apply-check: --system must be client or server (got '${system}')" >&2
    exit 2
    ;;
esac
if ! is_ci_runner; then
    echo "apply-check: refusing to run outside a CI runner (scripts/lib/ci-runner.sh); run make apply-check, which starts a disposable container" >&2
    exit 2
fi
if ! chezmoi_path="$(command -v "${chezmoi_bin}")"; then
    echo "apply-check: chezmoi not found: ${chezmoi_bin}" >&2
    exit 2
fi
if ! chezmoi_dir="$(dirname -- "${chezmoi_path}")"; then
    echo "apply-check: dirname failed on ${chezmoi_path}" >&2
    exit 2
fi
if ! scratch="$(mktemp -d "${RUNNER_TEMP}/apply-check.XXXXXX")"; then
    echo "apply-check: cannot create a scratch directory under ${RUNNER_TEMP}" >&2
    exit 2
fi
trap 'rm -rf "${scratch}"' EXIT
# The physical path: check-agent-runtime.py resolves its own location, and on macOS /tmp and /var are symlinks, so
# a Codex project trust written for the unresolved path would read as drift.
scratch="$(cd "${scratch}" && pwd -P)" || exit 2

apply_home="${scratch}/home"
# The copy keeps the clone's layout: chezmoi reads .chezmoiroot, so the working tree is apply_tree and the source
# dir apply_tree/home, the paths the Codex config's project trust and check-agent-runtime.py derive from.
apply_tree="${scratch}/tree"
apply_source="${apply_tree}/home"
apply_config="${apply_home}/.config/chezmoi/chezmoi.yaml"
mkdir -p "${apply_tree}" "${apply_home}/.config/chezmoi"
cp -R "${repo_root}/.chezmoiroot" "${repo_root}/home" "${repo_root}/scripts" "${apply_tree}/"
rm -f "${apply_source}/.chezmoiexternal.yaml.tmpl"
rm -rf "${apply_source}/.chezmoitemplates/chezmoiexternal.d"
find "${apply_source}" -type f -name 'encrypted_*' -exec rm -f {} +
printf 'sourceDir: "%s"\ndata:\n  email: "ci@example.invalid"\n  system: "%s"\n' \
    "${apply_tree}" "${system}" > "${apply_config}"
printf 'home-sentinel\n' | tee "${scratch}/unmanaged-sentinel" > "${apply_home}/unmanaged-sentinel"

# Everything below reads only the scratch HOME: no inherited XDG or gh directory can point a check at the
# caller's own config, and REPAIR=1 can never turn check-agent-runtime.py into a writer.
unset XDG_CONFIG_HOME XDG_DATA_HOME XDG_STATE_HOME XDG_CACHE_HOME GH_CONFIG_DIR REPAIR
export HOME="${apply_home}"
# check-agent-runtime.py and chezmoi doctor call chezmoi by name.
export PATH="${chezmoi_dir}:${PATH}"
chezmoi=(
    "${chezmoi_path}" --source "${apply_tree}" --destination "${apply_home}"
    --config "${apply_config}" --no-tty
)

results=()
failed=0

#
# @description Run one step from the copied tree, print its result and record it for the summary.
# @arg $1 string The step's name in the summary.
# @arg $@ string The command.
# @exitcode 0 The step passed.
# @exitcode 1 The step failed.
#
function step() {
    local name="$1" status=0
    shift
    printf '\n==> apply-check %s: %s\n' "${system}" "${name}"
    (cd "${apply_tree}" && "$@") || status=$?
    if [ "${status}" -eq 0 ]; then
        results+=("${name}=passed")
        return 0
    fi
    printf 'apply-check %s: %s failed with exit %d\n' "${system}" "${name}" "${status}" >&2
    results+=("${name}=failed")
    failed=1
    return 1
}

# init regenerates the config from home/.chezmoi.yaml.tmpl, as setup.sh's init does. A later step means
# nothing after a failed init or apply, so those two stop the run.
if step init "${chezmoi[@]}" init &&
    step apply "${chezmoi[@]}" --refresh-externals=never apply --exclude=scripts,externals; then
    # verify exits non-zero when any managed target differs from the source after the apply.
    step verify "${chezmoi[@]}" --refresh-externals=never verify --exclude=scripts,externals || true
    # The apply left the unmanaged file alone and wrote the system's shell rc.
    step unmanaged-file cmp "${scratch}/unmanaged-sentinel" "${apply_home}/unmanaged-sentinel" || true
    if [ "${system}" = client ]; then
        step shell-rc test -e "${apply_home}/.zshrc" || true
    else
        step shell-rc test -e "${apply_home}/.bashrc" || true
    fi
    step chezmoi-doctor "${chezmoi[@]}" doctor --no-network || true
    step agent-runtime scripts/check-agent-runtime.py || true
fi

printf '\napply-check summary (%s): %s\n' "${system}" "${results[*]}"
exit "${failed}"
