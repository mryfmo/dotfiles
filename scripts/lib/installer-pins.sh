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
CRIT_PIN_VERSION="v0.20.3"
CRIT_LINUX_AMD64_SHA256="d3a348770e828f9f1710501735504107d1eccb195f29cacdffed92f75b6abba1"
CRIT_LINUX_ARM64_SHA256="5a779fa202a1c7e8a1a6c5b05b4afa3a098b77c0c25103b0daf1d899f6d766ff"
ZED_PIN_VERSION="v1.21.0"
ZED_LINUX_AMD64_SHA256="b79a992e960ed4067cb2b50d66789ed8618eeb1780ed6a0f8f1e71dd80f74200"
ZED_LINUX_ARM64_SHA256="69eff51b22203be7a4d0fd9df0864a8abd4d5183e8fb9aafa2af57f3cd42b9a3"
