#!/usr/bin/env bash
# shellcheck disable=SC2034 # Variables are consumed by the scripts that source this file.

# @file scripts/lib/installer-pins.sh
# @brief Pinned upstream installer versions and script checksums.
# @description
#   Holds the reviewed version and installer-script SHA256 for upstream tools
#   installed through sha256-verified curl installers. The file is rewritten
#   wholesale by scripts/upgrade-tools.sh (bump_terminal_tool_pins) and
#   consumed by scripts/update-agent-assets.sh. Review and commit the diff
#   like a mise config/lock bump. Assignments stay non-readonly so the file
#   can be sourced again after a rewrite within the same process.

TERMINAL_CODE_PIN_VERSION="v0.3.4"
TERMINAL_CODE_INSTALLER_SHA256="026192e9f377af44f48c1c1e9f008c081369013d96901e5bff898f210272813c"
TERMINAL_BROWSER_PIN_VERSION="v0.7.4"
TERMINAL_BROWSER_INSTALLER_SHA256="bed6a3317d8894132241440999f9439da272543caae1732f6e128cfc826f0119"
