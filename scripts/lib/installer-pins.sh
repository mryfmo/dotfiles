#!/usr/bin/env bash
# shellcheck disable=SC2034 # Variables are consumed by the scripts that source this file.

# @file scripts/lib/installer-pins.sh
# @brief Pinned upstream tool versions and artifact checksums.
# @description
#   Holds reviewed versions and SHA256 values for upstream installers and
#   release binaries. The file is rewritten
#   wholesale by scripts/upgrade-tools.sh (bump_terminal_tool_pins) and
#   consumed by scripts/update-agent-assets.sh. Review and commit the diff
#   like a mise config/lock bump. Assignments stay non-readonly so the file
#   can be sourced again after a rewrite within the same process.

TERMINAL_CODE_PIN_VERSION="v0.3.4"
TERMINAL_CODE_INSTALLER_SHA256="026192e9f377af44f48c1c1e9f008c081369013d96901e5bff898f210272813c"
TERMINAL_BROWSER_PIN_VERSION="v0.11.1"
TERMINAL_BROWSER_INSTALLER_SHA256="accb57252d6e7dde513db2a473c008d71897cf72feaaecd58c5042821d1d63f9"
CRIT_PIN_VERSION="v0.20.2"
CRIT_LINUX_AMD64_SHA256="d2907008164fada5bd5221ffd37ed125c181280cec3ed74465e526ea7d25d20a"
CRIT_LINUX_ARM64_SHA256="833dd8145e5b47c06d88af80f8b6505159693742aadefcf400f923d7bc6c3b11"
ZED_PIN_VERSION="v1.20.2"
ZED_LINUX_AMD64_SHA256="647dc85e09fcd99cd175365a89b7b70ccf96469c4844eb8ae6eb83dfa82f7600"
ZED_LINUX_ARM64_SHA256="715a5252234522bc9e8e4a8c1f9b462cf7bb2881eed23b7c8ae650b41c24aa6f"
