#!/usr/bin/env bash
# @file ff-main.sh
# @brief Fast-forward the main checkout to origin/main after a merge, keeping every local edit.
# @description
#   Plan 007 T718, the sequence M-20261012-26's fourth instance records. In the
#   checkout this script lives in: the untracked files under `.orchestration`
#   that `origin/main` now holds, and the locally modified tracked files (`git
#   diff --name-only`), are moved aside under `$TMPDIR`; the tracked ones are
#   restored with `git checkout --`; then `git merge --ff-only origin/main`;
#   then each aside file that still differs from the fast-forwarded one is
#   copied back and listed. A refused fast-forward copies every aside file back
#   and exits 1. `rm` touches only its own directory under `$TMPDIR`. One
#   command per step under `set -e`, never an `&&` list across steps.
# @exitcode 0 Fast-forwarded; the restored files are listed.
# @exitcode 1 The fetch or the fast-forward failed; every local file is back in place.
# @example
#   scripts/orchestrator/ff-main.sh
set -euo pipefail

root="$(git -C "$(dirname -- "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
cd -- "${root}"
git fetch -q origin main
aside="$(mktemp -d "${TMPDIR:-/tmp}/ff-aside.XXXXXX")"
# A step that fails before the copy-back leaves the moved files where this line says.
trap 'echo "ff-main: stopped; the moved files are in ${aside}" >&2' ERR
modified=()
while IFS= read -r -d '' f; do
    modified+=("${f}")
done < <(git diff -z --name-only)
while IFS= read -r -d '' f; do
    if git cat-file -e "origin/main:${f}" 2> /dev/null; then
        modified+=("${f}")
    fi
done < <(git ls-files -z --others --exclude-standard -- .orchestration)
for f in ${modified[@]+"${modified[@]}"}; do
    mkdir -p "${aside}/$(dirname -- "${f}")"
    mv -- "${f}" "${aside}/${f}"
done
tracked=()
for f in ${modified[@]+"${modified[@]}"}; do
    if git ls-files --error-unmatch -- "${f}" > /dev/null 2>&1; then
        tracked+=("${f}")
    fi
done
if ((${#tracked[@]} > 0)); then
    git checkout -- "${tracked[@]}"
fi
rc=0
git merge -q --ff-only origin/main || rc=$?
for f in ${modified[@]+"${modified[@]}"}; do
    # After a refused fast-forward every moved file differs from, or is missing at, its path, so all come back.
    if ! git diff --no-index --quiet -- "${aside}/${f}" "${f}" 2> /dev/null; then
        mkdir -p "$(dirname -- "${f}")"
        cp -p -- "${aside}/${f}" "${f}"
        echo "restored: ${f}"
    fi
done
rm -r -- "${aside}"
if ((rc != 0)); then
    echo "ff-main: the fast-forward to origin/main was refused; every local file is back" >&2
    exit 1
fi
echo "ff-main: at $(git rev-parse --short HEAD)"
