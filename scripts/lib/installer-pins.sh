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

TERMINAL_CODE_PIN_VERSION="v0.4.2"
TERMINAL_CODE_INSTALLER_SHA256="de7c1540305d516ded9734f7dca4ed2d7d308fcc9cdb27a52717c4d26054e933"
TERMINAL_BROWSER_PIN_VERSION="v0.13.4"
TERMINAL_BROWSER_INSTALLER_SHA256="11b3f157debcf9bb8e5d8c6a5efc16fb9385ccb97478ae8bdb0fb0ea9e1f23bc"
CRIT_PIN_VERSION="v0.21.0"
CRIT_LINUX_AMD64_SHA256="cfaaaa4aa291ef208739b48d1fa0ef2a33b1101c20794491153b50024d800c66"
CRIT_LINUX_ARM64_SHA256="ca21efb1ff5e7f24b09de7fa4d0b6e5b44e06418da4cbead04d132f0e1dd7cf4"
CRIT_DARWIN_AMD64_SHA256="b3ded3bae8deb4997daaad7001eca9dce6be19e3e50d4e142a94bd3069708455"
CRIT_DARWIN_ARM64_SHA256="0eb05b29d81230cf16168bb373e8d9a18eab5c60ae868ef6a92fee73df7dd90e"
ZED_PIN_VERSION="v1.22.0"
ZED_LINUX_AMD64_SHA256="5ce3991b34a8fad0a23625f5821cda601c7150a6cc69683c097b8d1b083abc50"
ZED_LINUX_ARM64_SHA256="8b3c5d6e506056a9456ed33072081fd64db84ce47cdf34d4936442cc4f08394a"
