#!/usr/bin/env bash

# @file scripts/usage-snapshot.sh
# @brief Capture one daily ccusage snapshot for usage reviews.
# @description
#   Stores weekly and daily ccusage JSON in the repository worklog. Existing
#   snapshots are left unchanged, and unavailable or failing ccusage commands
#   warn without failing scheduled lifecycle runs.

set -Eeuo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
usage_dir="${repo_root}/.agents/worklog/claude/usage"
snapshot_date="$(date +%Y%m%d)"
snapshot_path="${usage_dir}/${snapshot_date}.json"

if [[ -e "${snapshot_path}" ]]; then
    printf 'Usage snapshot already exists: %s\n' "${snapshot_path}"
    exit 0
fi

if ! command -v ccusage > /dev/null 2>&1; then
    printf 'WARN: ccusage is unavailable; usage snapshot skipped.\n' >&2
    exit 0
fi

if ! weekly_json="$(ccusage weekly --json)"; then
    printf 'WARN: ccusage weekly failed; usage snapshot skipped.\n' >&2
    exit 0
fi
if ! daily_json="$(ccusage daily --json)"; then
    printf 'WARN: ccusage daily failed; usage snapshot skipped.\n' >&2
    exit 0
fi

mkdir -p "${usage_dir}"
captured_at="$(date '+%Y-%m-%dT%H:%M:%S%z')"
temporary_path="${snapshot_path}.tmp.$$"
trap 'rm -f "${temporary_path}"' EXIT
printf '{"captured_at":"%s","weekly":%s,"daily":%s}\n' \
    "${captured_at}" "${weekly_json}" "${daily_json}" > "${temporary_path}"
if ln "${temporary_path}" "${snapshot_path}" 2> /dev/null; then
    rm -f "${temporary_path}"
    trap - EXIT
elif [[ -e "${snapshot_path}" ]]; then
    printf 'Usage snapshot already exists: %s\n' "${snapshot_path}"
    exit 0
else
    printf 'WARN: unable to publish usage snapshot: %s\n' "${snapshot_path}" >&2
    exit 0
fi

printf 'Usage snapshot captured: %s\n' "${snapshot_path}"
