#!/usr/bin/env bash
# @file ruleset-verify.sh
# @brief Verify the live ruleset and timestamp D1 and D2 only when it matches.
# @option --expected <file> Read the expected JSON from a file.
# @example bash scripts/orchestrator/ruleset-verify.sh
set -euo pipefail
# shellcheck source=scripts/orchestrator/ruleset-request.sh
source "$(dirname "${BASH_SOURCE[0]}")/ruleset-request.sh"
compare_ruleset verify "$@"
