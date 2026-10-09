#!/usr/bin/env bash
# shellcheck disable=SC2034 # Variables are consumed by the scripts that source this file.

# @file scripts/lib/installer-pins.sh
# @brief Pins for the vendor installer scripts that publish no verification.
# @description
#   tode and terminal-browser install through a vendor `curl | bash` script
#   whose publisher signs nothing and ships no checksum; the script embeds the
#   sha256 of the payload it downloads, so the committed script hash is the
#   only integrity check for both. Every other release asset resolves its
#   newest cooled-down release (scripts/lib/github-release.sh) instead.
#   Consumed by scripts/update-agent-assets.sh. Assignments stay non-readonly
#   so tests can override them after sourcing. The values render from assets:
#   in home/dot_agents/agent-config.yaml through scripts/generate-agent-configs.py.

TERMINAL_CODE_PIN_VERSION="v0.4.2"
TERMINAL_CODE_INSTALLER_SHA256="de7c1540305d516ded9734f7dca4ed2d7d308fcc9cdb27a52717c4d26054e933"
TERMINAL_BROWSER_PIN_VERSION="v0.13.4"
TERMINAL_BROWSER_INSTALLER_SHA256="11b3f157debcf9bb8e5d8c6a5efc16fb9385ccb97478ae8bdb0fb0ea9e1f23bc"
