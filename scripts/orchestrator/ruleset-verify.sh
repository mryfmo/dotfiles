#!/usr/bin/env bash
# @file ruleset-verify.sh
# @brief Verify the live ruleset and optionally timestamp D1 and D2 on equality.
# @option --expected <file> Read the expected JSON from a file.
# @option --progress <file> Timestamp D1 and D2 in an existing checkout ledger after equality.
# @example bash scripts/orchestrator/ruleset-verify.sh
set -euo pipefail
# shellcheck source=scripts/orchestrator/ruleset-request.sh
source "$(dirname "${BASH_SOURCE[0]}")/ruleset-request.sh"
compare_ruleset verify "$@"
