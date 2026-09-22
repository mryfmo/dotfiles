#!/usr/bin/env bash

# @file install/ubuntu/client/gnome_settings.sh
# @brief Apply the preferred GNOME defaults for this dotfiles setup on Ubuntu client machines.
# @description
#   Ports every install/macos/common/defaults.sh preference that has a real
#   GNOME gsettings equivalent. Skips entirely on headless/CI hosts (no
#   gsettings, or no display/session bus), and guards every individual key
#   with a schema/writability check so a missing schema (e.g. the
#   dash-to-dock extension not installed) never fails the script.

set -Eeuo pipefail

if [ "${DOTFILES_DEBUG:-}" ]; then
    set -x
fi

#
# @description Report whether this host can apply GNOME settings right now.
#
function gnome_session_available() {
    command -v gsettings > /dev/null 2>&1 || return 1
    [ -n "${DISPLAY:-}" ] || [ -n "${DBUS_SESSION_BUS_ADDRESS:-}" ] || return 1
}

#
# @description Set a gsettings key, skipping silently if its schema/key isn't writable.
# @arg $1 schema GSettings schema id.
# @arg $2 key Key name within the schema.
# @arg $@ value The value(s) to pass to `gsettings set`.
#
function gset() {
    local schema="$1" key="$2"
    shift 2
    gsettings writable "${schema}" "${key}" > /dev/null 2>&1 || return 0
    gsettings set "${schema}" "${key}" "$@"
}

#
# @description Port defaults_keyboard: repeat rate/delay and the Caps Lock -> Ctrl remap.
#
function gnome_keyboard() {
    # macOS KeyRepeat=2 and InitialKeyRepeat=25 are in 15ms units.
    gset org.gnome.desktop.peripherals.keyboard repeat-interval 30
    gset org.gnome.desktop.peripherals.keyboard delay 375
    gset org.gnome.desktop.input-sources xkb-options "['ctrl:nocaps']"
}

#
# @description Port defaults_trackpad: tap-to-click and three-finger drag.
#
function gnome_trackpad() {
    gset org.gnome.desktop.peripherals.touchpad tap-to-click true
    gset org.gnome.desktop.peripherals.touchpad three-finger-drag true
}

#
# @description Port defaults_ui: show the battery percentage in the top bar.
#
function gnome_ui() {
    gset org.gnome.desktop.interface show-battery-percentage true
}

#
# @description Port defaults_dock: keep the dock visible and match the macOS icon size.
# @description
#   Requires the dash-to-dock shell extension; no-ops (via gset's schema
#   check) when it isn't installed.
#
function gnome_dock() {
    gset org.gnome.shell.extensions.dash-to-dock dock-fixed true
    gset org.gnome.shell.extensions.dash-to-dock dash-max-icon-size 30
}

#
# @description Port defaults_input_sources: US + Mozc Japanese IME, matching input source order.
#
function gnome_input_sources() {
    gset org.gnome.desktop.input-sources sources "[('xkb','us'),('ibus','mozc-jp')]"
}

#
# @description Port defaults_screencapture: save screenshots under ~/Pictures.
#
function gnome_screencapture() {
    gset org.gnome.gnome-screenshot auto-save-directory "file://${HOME}/Pictures"
}

#
# @description Apply all GNOME defaults managed by this script.
#
function main() {
    gnome_session_available || return 0

    gnome_ui
    gnome_keyboard
    gnome_trackpad
    gnome_dock
    gnome_input_sources
    gnome_screencapture
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main
fi

# 対応不能一覧 (no GNOME equivalent, or the macOS default has no meaningful
# port and is left out rather than guessed at):
#   - defaults_ui: "NSStatusItem Visible Bluetooth" — GNOME Quick Settings
#     shows Bluetooth automatically based on hardware; not a gsettings toggle.
#   - defaults_dock: Mission Control mru-spaces, and the specific
#     persistent-apps pins (Chrome.app / System Preferences.app) — these are
#     macOS application-bundle paths with no Linux equivalent to port.
#   - defaults_input_sources: "Automatically switch to a document's input
#     source" (AppleGlobalTextInputProperties) is a macOS Cocoa text-input
#     behavior with no GNOME analogue; the Command+` "previous input source"
#     symbolic hotkey has no faithful GNOME equivalent (differs from GNOME's
#     own input-source-switching convention) and is intentionally left as a
#     symbolic-hotkey-class item, per the same rationale as other symbolic
#     hotkeys.
#   - defaults_finder: NewWindowTarget/NewWindowTargetPath,
#     AppleShowAllExtensions, FXEnableExtensionChangeWarning, ShowStatusBar,
#     ShowPathbar, FXPreferredGroupBy, FXArrangeGroupViewBy,
#     DSDontWriteNetworkStores/DSDontWriteUSBStores, WarnOnEmptyTrash,
#     FXRemoveOldTrashItems — Finder-specific behaviors and the .DS_Store
#     mechanism have no corresponding Nautilus/GNOME Files gsettings keys.
#   - defaults_screencapture: the screenshot filename prefix ("Screen Shot")
#     and disabling the floating thumbnail preview have no reliable GNOME
#     Shell screenshot gsettings key.
#   - defaults_assistant: Siri and dictation auto-enable are Apple-only
#     features with nothing to disable on GNOME.
#   - defaults_ghostty: already a no-op on macOS (Ghostty config is managed
#     by chezmoi directly); nothing to port.
#   - kill_affected_applications / open_killed_applications / open_rectangle:
#     macOS-only plumbing to make `defaults write` changes take effect by
#     restarting cfprefsd-backed apps. gsettings changes apply live, so this
#     mechanism has no GNOME equivalent and needs no port.
