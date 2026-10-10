#!/usr/bin/env bash
# shellcheck disable=SC2034 # Variables are consumed by the scripts that source this file.

# @file scripts/lib/installer-pins.sh
# @brief Pins for the assets whose publisher offers no verification independent of the release.
# @description
#   tode and terminal-browser install through a vendor `curl | bash` script
#   whose publisher signs nothing and ships no checksum; the script embeds the
#   sha256 of the payload it downloads, so the committed script hash is the
#   only integrity check for both. Crit's releases are mutable and carry only a
#   checksums.txt from the same release, so the reviewed sha256 per platform is
#   the check. An asset with an attestation, a pinned-key signature or an
#   immutable registry resolves its newest cooled-down release instead.
#   Consumed by scripts/update-agent-assets.sh. Assignments stay non-readonly
#   so tests can override them after sourcing. The values render from assets:
#   in home/dot_agents/agent-config.yaml through scripts/generate-agent-configs.py.

TERMINAL_CODE_PIN_VERSION="v0.4.2"
TERMINAL_CODE_INSTALLER_SHA256="de7c1540305d516ded9734f7dca4ed2d7d308fcc9cdb27a52717c4d26054e933"
TERMINAL_BROWSER_PIN_VERSION="v0.13.4"
TERMINAL_BROWSER_INSTALLER_SHA256="11b3f157debcf9bb8e5d8c6a5efc16fb9385ccb97478ae8bdb0fb0ea9e1f23bc"
CRIT_PIN_VERSION="v0.22.0"
CRIT_LINUX_AMD64_SHA256="fecd40eea356020cd605dfca6a4be6ab3c9635134ca5e28ee99e6286ab62c31d"
CRIT_LINUX_ARM64_SHA256="92311ddf4862179c655087d4703e7f2e3f4b4aacb0549c22e5dae999c0fb2b6e"
CRIT_DARWIN_AMD64_SHA256="1f88b739234931a583097522bad29aa30566fa3ecb3227d753bb5ec01d4c369b"
CRIT_DARWIN_ARM64_SHA256="60153a194b85ba85ad72225694a2ccd7f348bc08bece756f7b56a0444a33e93d"
