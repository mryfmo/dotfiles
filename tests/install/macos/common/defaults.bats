#!/usr/bin/env bats

readonly SCRIPT_PATH="./install/macos/common/defaults.sh"

function setup() {
    source "${SCRIPT_PATH}"
}

@test "[macos] test for ui" {
    defaults_ui

    [ $(defaults read ~/Library/Preferences/ByHost/com.apple.controlcenter.plist BatteryShowPercentage) -eq 1 ]
}

@test "[macos] test for keyboard" {
    defaults_keyboard

    [ $(defaults read NSGlobalDomain KeyRepeat) -eq 2 ]
    [ $(defaults read NSGlobalDomain InitialKeyRepeat) -eq 25 ]
}

@test "[macos] test for trackpad" {
    defaults_trackpad

    [ $(defaults read -g com.apple.trackpad.scaling) -eq 2 ]

    [ $(defaults read NSGlobalDomain com.apple.mouse.tapBehavior) -eq 1 ]
    [ $(defaults -currentHost read NSGlobalDomain com.apple.mouse.tapBehavior) -eq 1 ]
    [ $(defaults read com.apple.AppleMultitouchTrackpad Clicking) -eq 1 ]
    [ $(defaults read com.apple.driver.AppleBluetoothMultitouch.trackpad Clicking) -eq 1 ]

    [ $(defaults read com.apple.AppleMultitouchTrackpad TrackpadThreeFingerDrag) -eq 1 ]
    [ $(defaults read com.apple.driver.AppleBluetoothMultitouch.trackpad TrackpadThreeFingerDrag) -eq 1 ]
}

@test "[macos] test for control center" {
    defaults_controlcenter

    [ $(defaults read com.apple.controlcenter "NSStatusItem Visible Bluetooth") -eq 1 ]
}

@test "[macos] test for dock" {
    defaults_dock

    [ $(defaults read com.apple.dock autohide) -eq 0 ]
    [ $(defaults read com.apple.dock tilesize) -eq 30 ]

    persistent_apps="$(defaults read com.apple.dock persistent-apps)"
    app_path_count="$(
        { grep -Eo '(/Applications/Google Chrome\.app|/System/Applications/System (Settings|Preferences)\.app/)' <<< "${persistent_apps}" || true; } |
            wc -l |
            tr -d ' '
    )"
    [ "${app_path_count}" -eq 2 ]
    grep -q '/Applications/Google Chrome.app' <<< "${persistent_apps}"
    grep -Eq '/System/Applications/System (Settings|Preferences)\.app/' <<< "${persistent_apps}"
    ! grep -q '/Applications/Visual Studio Code.app' <<< "${persistent_apps}"
    ! grep -q '/Applications/Slack.app' <<< "${persistent_apps}"
    ! grep -q '/Applications/iTerm.app' <<< "${persistent_apps}"
}

@test "[macos] dock is left unchanged when get_system_app_path fails" {
    function get_system_app_path() { return 1; }
    function defaults() { printf 'unexpected: defaults %s\n' "$*"; }

    run defaults_dock

    [ "${status}" -eq 1 ]
    [ "${output}" = "get_system_app_path failed; the Dock was not changed" ]
}
