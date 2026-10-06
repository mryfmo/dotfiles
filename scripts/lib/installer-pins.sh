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
#   The values render from assets: in home/dot_agents/agent-config.yaml
#   through scripts/generate-agent-configs.py.

CHEZMOI_BOOTSTRAP_PIN_VERSION="2.73.0"
TERMINAL_CODE_PIN_VERSION="v0.4.2"
TERMINAL_CODE_INSTALLER_SHA256="de7c1540305d516ded9734f7dca4ed2d7d308fcc9cdb27a52717c4d26054e933"
TERMINAL_BROWSER_PIN_VERSION="v0.13.4"
TERMINAL_BROWSER_INSTALLER_SHA256="11b3f157debcf9bb8e5d8c6a5efc16fb9385ccb97478ae8bdb0fb0ea9e1f23bc"
CRIT_PIN_VERSION="v0.21.1"
CRIT_LINUX_AMD64_SHA256="bbc7de53ebb29377c412d1737c658752efeaf44e8bd0f124278f6e41632ad670"
CRIT_LINUX_ARM64_SHA256="875c03a0b75de7777a26294dc585f59f3e4f49fe2735f5043fb668f92e2dc258"
CRIT_DARWIN_AMD64_SHA256="08f9f1a7e2f56f5d4dc5d9d86d0e06e92c165d2b885745d6ffed5ab3eda354dc"
CRIT_DARWIN_ARM64_SHA256="40cc7014f0b6c7d604be0bfdf4c462e2366549c520b95b790b414aa221d2a9a0"
ZED_PIN_VERSION="v1.22.0"
ZED_LINUX_AMD64_SHA256="5ce3991b34a8fad0a23625f5821cda601c7150a6cc69683c097b8d1b083abc50"
ZED_LINUX_ARM64_SHA256="8b3c5d6e506056a9456ed33072081fd64db84ce47cdf34d4936442cc4f08394a"
