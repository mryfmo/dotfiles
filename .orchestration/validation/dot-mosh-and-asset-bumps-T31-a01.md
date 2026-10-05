# T31 validation — dot-mosh-and-asset-bumps-T31-a01 (revision 2)

All blocks are verbatim command output (test runners may leave ANSI codes).

## task_rev verification (revision 2)
```
$ git show 12bbe77:.orchestration/tasks/dot-mosh-and-asset-bumps-T31-a01.md | sha256sum
b58d82ea8c8a5d329edc9cc29ba54d3e066817f469af012795e9f8da0cea6b33  -
$ git merge-base --is-ancestor 12bbe77 HEAD && echo base-contains-rev2-task-commit
base-contains-rev2-task-commit
$ git log --oneline origin/main..HEAD
7191193 fix: fold first Codex audit findings into T31 (bot guards, Renovate, AppArmor)
a12f507 fix(upgrade): avoid SC2015 in pick_windowed_pin for CI shellcheck
1c8d241 feat(upgrade): manage mosh and bump release asset pins under the 7-day window
```

## 1. mosh package entries
```
$ bash -c 'source install/ubuntu/common/dependencies.sh; echo ${#PACKAGES[@]}; printf "%s " "${PACKAGES[@]}"'
16
build-essential cmake curl git gpg htop iproute2 iputils-ping mosh perl pinentry-curses sudo unzip vim wget zsh 
$ bash -c 'source install/macos/common/dependencies.sh; printf "%s " "${BREW_PACKAGES[@]}"'
awscli cmake git gawk gpg mosh pinentry-mac vim zsh 
```

## 2. mosh configuration investigation
### (a) locale
```
## (a) locale
$ git grep -n -E "LANG|LC_ALL|LC_CTYPE|locale-gen|update-locale|UTF-8" -- home/dot_zshenv home/dot_zprofile* home/dot_zshrc* home/dot_bash* install/ubuntu | cut -c1-200
install/ubuntu/common/setup_locale.sh:6:#   Generates missing English and Japanese UTF-8 locales and keeps English as
install/ubuntu/common/setup_locale.sh:16:    en_US.UTF-8
install/ubuntu/common/setup_locale.sh:17:    ja_JP.UTF-8
install/ubuntu/common/setup_locale.sh:42:    sudo locale-gen "${missing[@]}"
install/ubuntu/common/setup_locale.sh:43:    sudo update-locale LANG="${TARGETS[0]}"
$ sed -n 1,80p install/ubuntu/common/setup_locale.sh | grep -nE "LOCALE|locale|LANG"
3:# @file install/ubuntu/common/setup_locale.sh
4:# @brief Ensure the required locales exist on Ubuntu.
6:#   Generates missing English and Japanese UTF-8 locales and keeps English as
21:# @description Generate any required locales that are not already available.
27:    available="$(locale -a 2> /dev/null | tr '[:upper:]' '[:lower:]' | tr -d '-')"
36:        printf 'Required locales already exist.\n'
41:    sudo --preserve-env=http_proxy,https_proxy,no_proxy apt-get install -y locales
42:    sudo locale-gen "${missing[@]}"
43:    sudo update-locale LANG="${TARGETS[0]}"
$ cat home/.chezmoiscripts/ubuntu/run_once_50-setup-locale.sh.tmpl
{{ if eq .chezmoi.os "linux" -}}
{{   if eq .chezmoi.osRelease.idLike "debian" -}}
{{     include "../install/ubuntu/common/setup_locale.sh" -}}
{{   end -}}
{{ end -}}
$ locale; cat /etc/default/locale
LANG=ja_JP.UTF-8
LANGUAGE=ja:en
LC_CTYPE="ja_JP.UTF-8"
LC_NUMERIC=ja_JP.UTF-8
LC_TIME=ja_JP.UTF-8
LC_COLLATE="ja_JP.UTF-8"
LC_MONETARY=ja_JP.UTF-8
LC_MESSAGES="ja_JP.UTF-8"
LC_PAPER=ja_JP.UTF-8
LC_NAME=ja_JP.UTF-8
LC_ADDRESS=ja_JP.UTF-8
LC_TELEPHONE=ja_JP.UTF-8
LC_MEASUREMENT=ja_JP.UTF-8
LC_IDENTIFICATION=ja_JP.UTF-8
LC_ALL=
LANG=en_US.UTF-8
LC_NUMERIC=ja_JP.UTF-8
LC_TIME=ja_JP.UTF-8
LC_MONETARY=ja_JP.UTF-8
LC_PAPER=ja_JP.UTF-8
LC_NAME=ja_JP.UTF-8
LC_ADDRESS=ja_JP.UTF-8
LC_TELEPHONE=ja_JP.UTF-8
LC_MEASUREMENT=ja_JP.UTF-8
LC_IDENTIFICATION=ja_JP.UTF-8
```
Conclusion: nothing is missing. `setup_locale.sh` runs on every Debian-like host (the wrapper has no client/server gate), generates en_US.UTF-8 and ja_JP.UTF-8, and sets `LANG` in /etc/default/locale.

### (b) firewall
```
$ git grep -n -i -E 'ufw|iptables|nftables|firewalld|pf\.conf|socketfilterfw' origin/main -- install home scripts Makefile setup.sh
exit=1
$ sed -n 49,55p install/macos/common/dependencies.sh
$ systemctl is-active ufw; command -v ufw   # host state, not repo-managed
active
/usr/sbin/ufw
```
Conclusion: the repo manages no firewall (grep exit 1 = no matches), so no firewall change is needed. The host ufw is operator-managed; the README tells such hosts to allow mosh UDP on the Tailscale interface.

### (c) non-interactive bootstrap
```
## (c) non-interactive bootstrap
$ sed -n 1,40p home/dot_zshenv
#!/usr/bin/env zsh

# @file home/dot_zshenv
# @brief Configure the minimal environment required by every zsh instance.
# @description
#   This file is also read by non-interactive SSH remote commands used to
#   bootstrap Mosh and Herdr. Keep it silent and lightweight. Claude Code's
#   built-in updater stays disabled so mise remains authoritative.
export DISABLE_AUTOUPDATER=1

typeset -gU path PATH
path=(
    "${HOME}/.local/share/mise/shims"
    "${HOME}/.local/bin"
    "${HOME}/.local/bin/common"
    /opt/homebrew/bin(N-/)
    /opt/homebrew/sbin(N-/)
    /usr/local/bin(N-/)
    /usr/local/sbin(N-/)
    "${path[@]}"
)
export PATH

readonly ZSHENV_PRIVATE="${HOME}/.zshenv_private"

if [[ -r "${ZSHENV_PRIVATE}" ]]; then
    source "${ZSHENV_PRIVATE}"
fi
```
Conclusion: apt installs `mosh-server` to /usr/bin (default PATH). Homebrew installs it to /opt/homebrew/bin or /usr/local/bin, and both are prepended by ~/.zshenv, which zsh reads for the non-interactive `ssh host -- mosh-server new` command.

## macOS CI install behavior
```
$ sed -n 49,55p install/macos/common/dependencies.sh

    if [[ ${#missing_packages[@]} -gt 0 ]]; then
        if [[ "${CI:-}" == "true" ]]; then
            brew info "${missing_packages[@]}"
        else
            brew install --force "${missing_packages[@]}"
        fi
    fi
```

## 3. Pins-only live run
```
$ date -u; bash -c 'source scripts/upgrade-tools.sh; bump_release_asset_pins'
2026年  9月 27日 日曜日 05:19:29 UTC

==> release asset pins
release window: skipping mise v2026.9.14 (published 1 day(s) ago, under 7)
release window: skipping mise v2026.9.13 (published 2 day(s) ago, under 7)
release window: skipping aws-cli 2.37.4 (published 1 day(s) ago, under 7)
release window: skipping aws-cli 2.37.3 (published 2 day(s) ago, under 7)
release window: skipping aws-cli 2.37.2 (published 2 day(s) ago, under 7)
release window: skipping aws-cli 2.37.1 (published 3 day(s) ago, under 7)
release window: skipping aws-cli 2.37.0 (published 4 day(s) ago, under 7)
release window: skipping aws-cli 2.36.50 (published 5 day(s) ago, under 7)
asset pins updated: mise.pin, sheldon.pin, starship.pin, aws-cli.pin
Pinned mise v2026.9.12, sheldon 0.8.5, starship v1.26.0, and aws-cli 2.36.49; review and commit the assets and installer diff.
exit=0
$ git diff origin/main...HEAD -- home/dot_agents/agent-config.yaml install/common/mise.sh install/common/sheldon.sh install/ubuntu/server/starship.sh install/ubuntu/common/aws_cli.sh
diff --git a/home/dot_agents/agent-config.yaml b/home/dot_agents/agent-config.yaml
index 03d8441..764f155 100644
--- a/home/dot_agents/agent-config.yaml
+++ b/home/dot_agents/agent-config.yaml
@@ -412,7 +412,7 @@ assets:
   starship:
     source: github-release
     upstream: starship/starship
-    pin: v1.25.1
+    pin: v1.26.0
     verify: release-sha256
     install_path: ~/.local/bin/starship
     installer: install/ubuntu/server/starship.sh
@@ -422,7 +422,7 @@ assets:
   aws-cli:
     source: https-download
     upstream: https://awscli.amazonaws.com
-    pin: 2.35.21
+    pin: 2.36.49
     verify: gpg
     gpg_fingerprint: FB5DB77FD5C118B80511ADA8A6310ACC4672475C
     install_path: ~/.local/share/aws-cli
diff --git a/install/ubuntu/common/aws_cli.sh b/install/ubuntu/common/aws_cli.sh
index ab469da..1fe3c76 100644
--- a/install/ubuntu/common/aws_cli.sh
+++ b/install/ubuntu/common/aws_cli.sh
@@ -10,7 +10,7 @@ if [ "${DOTFILES_DEBUG:-}" ]; then
 fi
 
 # Rendered from assets.aws-cli in home/dot_agents/agent-config.yaml; change it there.
-readonly AWS_CLI_VERSION="2.35.21"
+readonly AWS_CLI_VERSION="2.36.49"
 readonly AWS_CLI_FINGERPRINT="FB5DB77FD5C118B80511ADA8A6310ACC4672475C"
 readonly AWS_CLI_KEY_PATH="${AWS_CLI_KEY_PATH:-${HOME}/.local/share/aws-cli-keys/aws-cli-public-key.asc}"
 readonly AWS_CLI_INSTALL_DIR="${HOME}/.local/share/aws-cli"
diff --git a/install/ubuntu/server/starship.sh b/install/ubuntu/server/starship.sh
index c75e865..1bfb939 100644
--- a/install/ubuntu/server/starship.sh
+++ b/install/ubuntu/server/starship.sh
@@ -13,7 +13,7 @@ fi
 
 readonly BIN_DIR="${HOME}/.local/bin"
 # Rendered from assets.starship in home/dot_agents/agent-config.yaml; change it there.
-readonly STARSHIP_VERSION="v1.25.1"
+readonly STARSHIP_VERSION="v1.26.0"
 
 # @description Print the Starship Linux artifact name for the current architecture.
 function starship_artifact() {
```
aws-cli window boundary check:
```
$ cutoff: date -u -d "@$(( $(date +%s) - 604800 ))"
2026-09-20T05:19:45Z
$ curl -fsSI .../awscli-exe-linux-x86_64-2.36.50.zip | grep last-modified
Last-Modified: Mon, 21 Sep 2026 19:30:14 GMT
$ curl -fsSI .../awscli-exe-linux-x86_64-2.36.50.zip.sig | head -1
HTTP/1.1 200 OK
$ curl -fsSI .../awscli-exe-linux-x86_64-2.36.49.zip | grep last-modified
Last-Modified: Fri, 18 Sep 2026 20:02:23 GMT
$ curl -fsSI .../awscli-exe-linux-x86_64-2.36.49.zip.sig | head -1
HTTP/1.1 200 OK
```

## 4. remote.yaml bot guards (revision 2, audit P1)
```
# before (origin/main)
105:        if: ${{ github.actor == 'dependabot[bot]' || env.HAS_EMAIL_ADDRESS != 'true' || env.HAS_PRIVATE_DEPLOY_KEY != 'true' }}
109:        if: ${{ github.actor != 'dependabot[bot]' && env.HAS_EMAIL_ADDRESS == 'true' && env.HAS_PRIVATE_DEPLOY_KEY == 'true' }}
115:        if: ${{ github.actor != 'dependabot[bot]' && env.HAS_EMAIL_ADDRESS == 'true' && env.HAS_PRIVATE_DEPLOY_KEY == 'true' }}
$ git diff origin/main...HEAD -- .github/workflows/remote.yaml
diff --git a/.github/workflows/remote.yaml b/.github/workflows/remote.yaml
index 1a9ccb1..185dc2b 100644
--- a/.github/workflows/remote.yaml
+++ b/.github/workflows/remote.yaml
@@ -102,17 +102,17 @@ jobs:
           persist-credentials: false
 
       - name: Explain skipped private bootstrap
-        if: ${{ github.actor == 'dependabot[bot]' || env.HAS_EMAIL_ADDRESS != 'true' || env.HAS_PRIVATE_DEPLOY_KEY != 'true' }}
+        if: ${{ contains(github.actor, '[bot]') || env.HAS_EMAIL_ADDRESS != 'true' || env.HAS_PRIVATE_DEPLOY_KEY != 'true' }}
         run: echo "Private bootstrap is optional and secrets are unavailable in this context."
 
       - name: Set up the private deploy key
-        if: ${{ github.actor != 'dependabot[bot]' && env.HAS_EMAIL_ADDRESS == 'true' && env.HAS_PRIVATE_DEPLOY_KEY == 'true' }}
+        if: ${{ !contains(github.actor, '[bot]') && env.HAS_EMAIL_ADDRESS == 'true' && env.HAS_PRIVATE_DEPLOY_KEY == 'true' }}
         uses: webfactory/ssh-agent@e83874834305fe9a4a2997156cb26c5de65a8555 # v0.10.0
         with:
           ssh-private-key: ${{ secrets.PRIVATE_DOTFILES_PRIVATE_DEPLOY_KEY }}
 
       - name: Bootstrap with private restoration
-        if: ${{ github.actor != 'dependabot[bot]' && env.HAS_EMAIL_ADDRESS == 'true' && env.HAS_PRIVATE_DEPLOY_KEY == 'true' }}
+        if: ${{ !contains(github.actor, '[bot]') && env.HAS_EMAIL_ADDRESS == 'true' && env.HAS_PRIVATE_DEPLOY_KEY == 'true' }}
         env:
           GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
           EMAIL_ADDRESS: ${{ secrets.EMAIL_ADDRESS }}
```

## 4b. renovate.json hardening
```
$ git diff origin/main...HEAD -- renovate.json
diff --git a/renovate.json b/renovate.json
index 7d107fd..55e86fd 100644
--- a/renovate.json
+++ b/renovate.json
@@ -40,6 +40,17 @@
       "matchManagers": ["custom.regex"],
       "matchFileNames": ["home/dot_agents/agent-config.yaml"],
       "dependencyDashboardApproval": true
+    },
+    {
+      "description": "Notification-only until lock fidelity is proven: Renovate's mise artifact update runs mise lock without loading home/dot_mise/config.toml, so its PRs cannot reliably regenerate home/dot_mise/mise.lock. make upgrade remains the executing lane.",
+      "matchManagers": ["mise"],
+      "dependencyDashboardApproval": true
+    },
+    {
+      "description": "Hold fd, as scripts/upgrade-tools.sh does: newer releases lack a macOS x64 asset.",
+      "matchManagers": ["mise"],
+      "matchPackageNames": ["fd"],
+      "enabled": false
     }
   ]
 }
```

## 4c. AppArmor step robustness
```
$ git diff origin/main...HEAD -- home/.chezmoiscripts/ubuntu/run_onchange_after_07-apparmor-bwrap-userns.sh.tmpl scripts/check-tools.sh
diff --git a/home/.chezmoiscripts/ubuntu/run_onchange_after_07-apparmor-bwrap-userns.sh.tmpl b/home/.chezmoiscripts/ubuntu/run_onchange_after_07-apparmor-bwrap-userns.sh.tmpl
index 02ec81a..9b6b952 100644
--- a/home/.chezmoiscripts/ubuntu/run_onchange_after_07-apparmor-bwrap-userns.sh.tmpl
+++ b/home/.chezmoiscripts/ubuntu/run_onchange_after_07-apparmor-bwrap-userns.sh.tmpl
@@ -2,5 +2,8 @@
 {{   if eq .chezmoi.osRelease.idLike "debian" -}}
 {{     include "../install/ubuntu/common/apparmor_userns.sh" }}
 # Re-run when the profile changes. bwrap-userns sha256sum: {{ include "../install/ubuntu/common/apparmor/bwrap-userns" | sha256sum }}
+{{     $bwrap := env "APPARMOR_USERNS_BWRAP" | default "/usr/bin/bwrap" -}}
+{{     $sysctl := env "APPARMOR_USERNS_SYSCTL" | default "/proc/sys/kernel/apparmor_restrict_unprivileged_userns" -}}
+# Re-run when a prerequisite changes, so a skipped install is retried: bwrap={{ if stat $bwrap }}present{{ else }}absent{{ end }} apparmor_parser={{ if lookPath "apparmor_parser" }}present{{ else }}absent{{ end }} restriction={{ if stat $sysctl }}{{ include $sysctl | trim }}{{ else }}absent{{ end }}
 {{   end -}}
 {{ end -}}
diff --git a/scripts/check-tools.sh b/scripts/check-tools.sh
index 4ad2460..a4ead18 100755
--- a/scripts/check-tools.sh
+++ b/scripts/check-tools.sh
@@ -186,7 +186,8 @@ function check_apparmor_userns() {
         return 0
     fi
     if [ ! -x "${bwrap}" ]; then
-        warn_optional "${bwrap} is missing; sandboxed codex runs need it under the AppArmor userns restriction"
+        printf 'required failed: %s is missing; sandboxed codex runs need it under the AppArmor userns restriction (install the bubblewrap package)\n' "${bwrap}" >&2
+        ((required_failures += 1))
         return 0
     fi
     if "${bwrap}" --ro-bind / / true > /dev/null 2>&1; then
$ HOME=<empty> APPARMOR_USERNS_BWRAP=/usr/bin/bwrap chezmoi execute-template --source home < <wrapper> | tail -1
# Re-run when a prerequisite changes, so a skipped install is retried: bwrap=present apparmor_parser=present restriction=1
$ HOME=<empty> APPARMOR_USERNS_BWRAP=/nonexistent/bwrap chezmoi execute-template --source home < <wrapper> | tail -1
# Re-run when a prerequisite changes, so a skipped install is retried: bwrap=absent apparmor_parser=present restriction=1
```

## 5. Mutation baselines (new tests vs origin/main export), then branch
### revision 1 (release asset pin bump)
```
$ (origin/main export + new test file) python3 -m unittest -v tests.unit.test_release_asset_pins
test_bump_writes_only_the_four_pins_through_set_asset (tests.unit.test_release_asset_pins.ReleaseAssetPinsTest.test_bump_writes_only_the_four_pins_through_set_asset) ... [31mFAIL[0m
test_window_never_moves_a_pin_backwards (tests.unit.test_release_asset_pins.ReleaseAssetPinsTest.test_window_never_moves_a_pin_backwards) ... [31mFAIL[0m
test_window_rejects_an_unknown_current_pin (tests.unit.test_release_asset_pins.ReleaseAssetPinsTest.test_window_rejects_an_unknown_current_pin) ... [31mFAIL[0m
test_window_skips_a_young_release_and_takes_an_older_one (tests.unit.test_release_asset_pins.ReleaseAssetPinsTest.test_window_skips_a_young_release_and_takes_an_older_one) ... [31mFAIL[0m

======================================================================
[31mFAIL[0m[1;31m: test_bump_writes_only_the_four_pins_through_set_asset (tests.unit.test_release_asset_pins.ReleaseAssetPinsTest.test_bump_writes_only_the_four_pins_through_set_asset)[0m
----------------------------------------------------------------------
Traceback (most recent call last):
  File [35m"/tmp/claude-1000/-home-moriya-Workspace-dotfiles/3e54f9a0-f011-4421-9a8a-a9eb113df7ad/scratchpad/t31/base.l9pU/tests/unit/test_release_asset_pins.py"[0m, line [35m179[0m, in [35mtest_bump_writes_only_the_four_pins_through_set_asset[0m
    [31mself.assertEqual[0m[1;31m(0, result.returncode, result.stdout + result.stderr)[0m
    [31m~~~~~~~~~~~~~~~~[0m[1;31m^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^[0m
[1;35mAssertionError[0m: [35m0 != 127 : bash: 行 1: bump_release_asset_pins: コマンドが見つかりません
[0m

======================================================================
[31mFAIL[0m[1;31m: test_window_never_moves_a_pin_backwards (tests.unit.test_release_asset_pins.ReleaseAssetPinsTest.test_window_never_moves_a_pin_backwards)[0m
----------------------------------------------------------------------
Traceback (most recent call last):
  File [35m"/tmp/claude-1000/-home-moriya-Workspace-dotfiles/3e54f9a0-f011-4421-9a8a-a9eb113df7ad/scratchpad/t31/base.l9pU/tests/unit/test_release_asset_pins.py"[0m, line [35m80[0m, in [35mtest_window_never_moves_a_pin_backwards[0m
    [31mself.assertEqual[0m[1;31m(0, result.returncode, result.stderr)[0m
    [31m~~~~~~~~~~~~~~~~[0m[1;31m^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^[0m
[1;35mAssertionError[0m: [35m0 != 127 : _: line 1: pick_windowed_pin: command not found
[0m

======================================================================
[31mFAIL[0m[1;31m: test_window_rejects_an_unknown_current_pin (tests.unit.test_release_asset_pins.ReleaseAssetPinsTest.test_window_rejects_an_unknown_current_pin)[0m
----------------------------------------------------------------------
Traceback (most recent call last):
  File [35m"/tmp/claude-1000/-home-moriya-Workspace-dotfiles/3e54f9a0-f011-4421-9a8a-a9eb113df7ad/scratchpad/t31/base.l9pU/tests/unit/test_release_asset_pins.py"[0m, line [35m88[0m, in [35mtest_window_rejects_an_unknown_current_pin[0m
    [31mself.assertNotIn[0m[1;31m("command not found", result.stderr)[0m
    [31m~~~~~~~~~~~~~~~~[0m[1;31m^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^[0m
[1;35mAssertionError[0m: [35m'command not found' unexpectedly found in '_: line 1: pick_windowed_pin: command not found\n'[0m

======================================================================
[31mFAIL[0m[1;31m: test_window_skips_a_young_release_and_takes_an_older_one (tests.unit.test_release_asset_pins.ReleaseAssetPinsTest.test_window_skips_a_young_release_and_takes_an_older_one)[0m
----------------------------------------------------------------------
Traceback (most recent call last):
  File [35m"/tmp/claude-1000/-home-moriya-Workspace-dotfiles/3e54f9a0-f011-4421-9a8a-a9eb113df7ad/scratchpad/t31/base.l9pU/tests/unit/test_release_asset_pins.py"[0m, line [35m63[0m, in [35mtest_window_skips_a_young_release_and_takes_an_older_one[0m
    [31mself.assertEqual[0m[1;31m(0, result.returncode, result.stderr)[0m
    [31m~~~~~~~~~~~~~~~~[0m[1;31m^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^[0m
[1;35mAssertionError[0m: [35m0 != 127 : _: line 1: pick_windowed_pin: command not found
[0m

----------------------------------------------------------------------
Ran 4 tests in 0.015s

[1;31mFAILED[0m ([1;31mfailures=4[0m)
$ (branch) python3 -m unittest -v tests.unit.test_release_asset_pins
test_bump_writes_only_the_four_pins_through_set_asset (tests.unit.test_release_asset_pins.ReleaseAssetPinsTest.test_bump_writes_only_the_four_pins_through_set_asset) ... [32mok[0m
test_window_never_moves_a_pin_backwards (tests.unit.test_release_asset_pins.ReleaseAssetPinsTest.test_window_never_moves_a_pin_backwards) ... [32mok[0m
test_window_rejects_an_unknown_current_pin (tests.unit.test_release_asset_pins.ReleaseAssetPinsTest.test_window_rejects_an_unknown_current_pin) ... [32mok[0m
test_window_skips_a_young_release_and_takes_an_older_one (tests.unit.test_release_asset_pins.ReleaseAssetPinsTest.test_window_skips_a_young_release_and_takes_an_older_one) ... [32mok[0m

----------------------------------------------------------------------
Ran 4 tests in 0.150s

[32mOK[0m
```
### revision 2 (doctor bwrap-missing, wrapper re-render, Renovate mise/fd)
```
$ (origin/main export + rev2 test files) python3 -m unittest -v <rev2 tests>
test_doctor_fails_when_bwrap_is_missing_with_codex (tests.unit.test_apparmor_userns.AppArmorUsernsTest.test_doctor_fails_when_bwrap_is_missing_with_codex) ... [31mFAIL[0m
test_wrapper_re_renders_when_prerequisites_change (tests.unit.test_apparmor_userns.AppArmorUsernsTest.test_wrapper_re_renders_when_prerequisites_change) ... [31mFAIL[0m
test_renovate_owns_dependency_update_notifications (tests.unit.test_supply_chain_policy.SupplyChainPolicyTest.test_renovate_owns_dependency_update_notifications) ... [31mFAIL[0m

======================================================================
[31mFAIL[0m[1;31m: test_doctor_fails_when_bwrap_is_missing_with_codex (tests.unit.test_apparmor_userns.AppArmorUsernsTest.test_doctor_fails_when_bwrap_is_missing_with_codex)[0m
----------------------------------------------------------------------
Traceback (most recent call last):
  File [35m"/tmp/claude-1000/-home-moriya-Workspace-dotfiles/3e54f9a0-f011-4421-9a8a-a9eb113df7ad/scratchpad/t31/base2.H9BF/tests/unit/test_apparmor_userns.py"[0m, line [35m188[0m, in [35mtest_doctor_fails_when_bwrap_is_missing_with_codex[0m
    [31mself.assertIn[0m[1;31m("req=1 opt=0", result.stdout)[0m
    [31m~~~~~~~~~~~~~[0m[1;31m^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^[0m
[1;35mAssertionError[0m: [35m'req=1 opt=0' not found in 'req=0 opt=1\n'[0m

======================================================================
[31mFAIL[0m[1;31m: test_wrapper_re_renders_when_prerequisites_change (tests.unit.test_apparmor_userns.AppArmorUsernsTest.test_wrapper_re_renders_when_prerequisites_change)[0m
----------------------------------------------------------------------
Traceback (most recent call last):
  File [35m"/tmp/claude-1000/-home-moriya-Workspace-dotfiles/3e54f9a0-f011-4421-9a8a-a9eb113df7ad/scratchpad/t31/base2.H9BF/tests/unit/test_apparmor_userns.py"[0m, line [35m219[0m, in [35mtest_wrapper_re_renders_when_prerequisites_change[0m
    [31mself.assertIn[0m[1;31m("bwrap=absent", skipped)[0m
    [31m~~~~~~~~~~~~~[0m[1;31m^^^^^^^^^^^^^^^^^^^^^^^^^[0m
[1;35mAssertionError[0m: [35m'bwrap=absent' not found in '#!/usr/bin/env bash\n\n# @file install/ubuntu/common/apparmor_userns.sh\n# @brief Install the AppArmor profile that lets bwrap create user namespaces.\n# @description\n#   Copies install/ubuntu/common/apparmor/bwrap-userns to /etc/apparmor.d and\n#   loads it with apparmor_parser, so sandboxed Codex runs keep working under\n#   kernel.apparmor_restrict_unprivileged_userns=1. It is a no-op when the\n#   restriction is off or absent, or when apparmor_parser or /usr/bin/bwrap is\n#   missing. The global sysctl is never changed.\n#   Remove with: sudo apparmor_parser -R /etc/apparmor.d/bwrap-userns &&\n#   sudo rm /etc/apparmor.d/bwrap-userns\n\nset -Eeuo pipefail\n\nif [ "${DOTFILES_DEBUG:-}" ]; then\n    set -x\nfi\n\nreadonly RESTRICT_SYSCTL="${APPARMOR_USERNS_SYSCTL:-/proc/sys/kernel/apparmor_restrict_unprivileged_userns}"\nreadonly BWRAP_PATH="${APPARMOR_USERNS_BWRAP:-/usr/bin/bwrap}"\nreadonly PROFILE_TARGET="${APPARMOR_USERNS_PROFILE_TARGET:-/etc/apparmor.d/bwrap-userns}"\n\n#\n# @description Print the profile source path from the chezmoi source tree or this script\'s directory.\n# @stdout Absolute or relative path to the bwrap-userns profile source.\n#\nfunction profile_source() {\n    if [ -n "${APPARMOR_USERNS_PROFILE_SOURCE:-}" ]; then\n        printf \'%s\\n\' "${APPARMOR_USERNS_PROFILE_SOURCE}"\n    elif [ -n "${CHEZMOI_SOURCE_DIR:-}" ]; then\n        printf \'%s\\n\' "${CHEZMOI_SOURCE_DIR}/../install/ubuntu/common/apparmor/bwrap-userns"\n    else\n        printf \'%s\\n\' "$(dirname "${BASH_SOURCE[0]}")/apparmor/bwrap-userns"\n    fi\n}\n\n#\n# @description Print why the profile is not needed, or nothing when it is.\n# @stdout One skip reason line, or nothing.\n#\nfunction skip_reason() {\n    if [ "$(cat "${RESTRICT_SYSCTL}" 2> /dev/null)" != "1" ]; then\n        printf \'AppArmor unprivileged userns restriction is not enabled\\n\'\n    elif ! command -v apparmor_parser > /dev/null 2>&1; then\n        printf \'apparmor_parser is not installed\\n\'\n    elif [ ! -x "${BWRAP_PATH}" ]; then\n        printf \'%s is not installed\\n\' "${BWRAP_PATH}"\n    fi\n}\n\n#\n# @description Copy the profile into place and (re)load it; both steps are idempotent.\n#\nfunction install_profile() {\n    local source\n    source="$(profile_source)"\n    sudo install -m 0644 "${source}" "${PROFILE_TARGET}"\n    sudo apparmor_parser -r "${PROFILE_TARGET}"\n}\n\n#\n# @description Install the bwrap user-namespace profile when the host needs it.\n#\nfunction main() {\n    local reason\n    reason="$(skip_reason)"\n    if [ -n "${reason}" ]; then\n        printf \'Skipping bwrap AppArmor userns profile: %s.\\n\' "${reason}"\n        return 0\n    fi\n    install_profile\n    printf \'Loaded AppArmor profile bwrap-userns from %s.\\n\' "${PROFILE_TARGET}"\n}\n\nif [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then\n    main\nfi\n\n# Re-run when the profile changes. bwrap-userns sha256sum: 40fa331c27d032df5ea7c0abc130c80cc2b44af139d55b8883f89c4cf9148c3a\n'[0m

======================================================================
[31mFAIL[0m[1;31m: test_renovate_owns_dependency_update_notifications (tests.unit.test_supply_chain_policy.SupplyChainPolicyTest.test_renovate_owns_dependency_update_notifications)[0m
----------------------------------------------------------------------
Traceback (most recent call last):
  File [35m"/tmp/claude-1000/-home-moriya-Workspace-dotfiles/3e54f9a0-f011-4421-9a8a-a9eb113df7ad/scratchpad/t31/base2.H9BF/tests/unit/test_supply_chain_policy.py"[0m, line [35m491[0m, in [35mtest_renovate_owns_dependency_update_notifications[0m
    [31mself.assertTrue[0m[1;31m([0m
    [31m~~~~~~~~~~~~~~~[0m[1;31m^[0m
        [1;31many([0m
        [1;31m^^^^[0m
    ...<3 lines>...
        [1;31m)[0m
        [1;31m^[0m
    [1;31m)[0m
    [1;31m^[0m
[1;35mAssertionError[0m: [35mFalse is not true[0m

----------------------------------------------------------------------
Ran 3 tests in 0.039s

[1;31mFAILED[0m ([1;31mfailures=3[0m)
$ (branch) python3 -m unittest -v <rev2 tests>
test_doctor_fails_when_bwrap_is_missing_with_codex (tests.unit.test_apparmor_userns.AppArmorUsernsTest.test_doctor_fails_when_bwrap_is_missing_with_codex) ... [32mok[0m
test_wrapper_re_renders_when_prerequisites_change (tests.unit.test_apparmor_userns.AppArmorUsernsTest.test_wrapper_re_renders_when_prerequisites_change) ... [32mok[0m
test_renovate_owns_dependency_update_notifications (tests.unit.test_supply_chain_policy.SupplyChainPolicyTest.test_renovate_owns_dependency_update_notifications) ... [32mok[0m

----------------------------------------------------------------------
Ran 3 tests in 0.044s

[32mOK[0m
```

## Required validation commands (+ Renovate validator and CI-equivalent lint)
```
$ npx --yes --package renovate@44 -- renovate-config-validator --strict renovate.json
[32m INFO[39m: Validating renovate.json as global config
[32m INFO[39m: Config validated successfully against 1 file(s)
$ uv run --with pyyaml scripts/generate-agent-configs.py --check
generated agent configs are up to date
exit=0
$ make validate-agent-assets
uv run --with pyyaml scripts/validate-agent-assets.py
agent asset validation ok
exit=0
$ git ls-files -- install/**/*.sh scripts/**/*.sh | xargs mise x shfmt@3.14.1 -- shfmt -i 4 -sr -d
exit=0
$ git ls-files -z 'setup.sh' 'install/*.sh' 'install/**/*.sh' 'scripts/*.sh' | xargs -0 shellcheck -x
exit=0
$ npx --yes --package renovate@44 -- renovate-config-validator --strict   # repo-config mode
[32m INFO[39m: Validating renovate.json
[32m INFO[39m: Config validated successfully against 1 file(s)
```
```
$ make unit-test
uv run python -m unittest discover -s tests/unit -v
test_check_uses_same_modified_for_codex_profiles (test_check_agent_runtime.CheckAgentRuntimeTest.test_check_uses_same_modified_for_codex_profiles) ... <frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf4528357a4d0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf4528357a5c0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf4528357a3e0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf4528357a200>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf4528357a7a0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf4528357a6b0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf4528357a980>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf4528357a890>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf4528357aa70>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf4528357ab60>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf4528357ac50>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf4528357ad40>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf4528357ae30>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf4528357af20>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf45283948310>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf4528357b100>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf4528357b2e0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf4528357b3d0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf4528357b1f0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf4528357b4c0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf4528357b5b0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf4528357b6a0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf4528357b790>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf4528357b880>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf4528357b970>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf4528357ba60>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf4528357bb50>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf4528357bc40>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf4528357bd30>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf4528357b010>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf4528357bf10>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf4528357be20>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf45283400040>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf45283400130>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf45283400310>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf45283400220>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf45283400400>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf452834005e0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
ok
test_current_session_start_order_is_preserved (test_claude_settings_merge.ClaudeSettingsMergeTest.test_current_session_start_order_is_preserved)
test_managed_session_start_replacement_keeps_hook_order (test_claude_settings_merge.ClaudeSettingsMergeTest.test_managed_session_start_replacement_keeps_hook_order)
test_managed_session_start_replaces_stale_hard_coded_home_hook (test_claude_settings_merge.ClaudeSettingsMergeTest.test_managed_session_start_replaces_stale_hard_coded_home_hook)
test_model_profiles_reject_incomplete_or_unsafe_entries (test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_reject_incomplete_or_unsafe_entries) ... ERROR: model profile standard is missing codex
ERROR: model profile standard.claude.model must be a launcher-safe string
ERROR: model_profiles must define the express profile
ok
test_model_profiles_reject_unsafe_advisor (test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_reject_unsafe_advisor) ... ERROR: model profile standard.claude.advisor must be a launcher-safe string
ok
test_unknown_interactive_profile_fails (test_generate_agent_configs.GenerateAgentConfigsTest.test_unknown_interactive_profile_fails) ... ERROR: interactive_profile must name a model profile: 'missing'
ok
test_unknown_worker_kind_fails (test_generate_agent_configs.GenerateAgentConfigsTest.test_unknown_worker_kind_fails) ... ERROR: worker_kind must be one of ('codex', 'claude'): 'banana'
ok
test_unknown_worker_profile_fails (test_generate_agent_configs.GenerateAgentConfigsTest.test_unknown_worker_profile_fails) ... ERROR: worker_profile must name a model profile: 'missing'
ok
test_cli_workspace_resolves_macos_var_alias_identically (test_permgate.PermgateTest.test_cli_workspace_resolves_macos_var_alias_identically) ... skipped 'macOS /var alias only'
test_upgrade_uses_current_mise_node_after_runtime_replacement (test_runtime_health.RuntimeHealthTest.test_upgrade_uses_current_mise_node_after_runtime_replacement)
test_repo_claude_settings_reject_machine_specific_interpreter (test_validate_agent_assets.ValidateAgentAssetsTest.test_repo_claude_settings_reject_machine_specific_interpreter) ... ERROR: /tmp/validate-agent-assets-test-3rn6kpq6/.claude/settings.json hook SessionEnd must not hard-code a machine-specific home path: ~/.local/share/mise/installs/python/3.14.7/bin/python3.14
ok

----------------------------------------------------------------------
Ran 475 tests in 43.180s

OK (skipped=1)
exit=0
```
(Per-test `... ok` lines are elided. The remaining `ERROR:` lines are expected stderr from passing negative tests.)
```
$ git -C ~/Workspace/dotfiles/.claude/worktrees/worker-c diff origin/main --stat
 .github/workflows/remote.yaml                      |   6 +-
 README.md                                          |  11 ++
 ...onchange_after_07-apparmor-bwrap-userns.sh.tmpl |   3 +
 home/dot_agents/agent-config.yaml                  |   4 +-
 install/macos/common/dependencies.sh               |   1 +
 install/ubuntu/common/aws_cli.sh                   |   2 +-
 install/ubuntu/common/dependencies.sh              |   1 +
 install/ubuntu/server/starship.sh                  |   2 +-
 renovate.json                                      |  11 ++
 scripts/check-tools.sh                             |   3 +-
 scripts/upgrade-tools.sh                           | 136 ++++++++++++++
 tests/install/ubuntu/common/dependencies.bats      |   3 +-
 tests/unit/test_apparmor_userns.py                 |  52 ++++++
 tests/unit/test_aws_cli_acquisition.py             |  19 +-
 tests/unit/test_release_asset_pins.py              | 206 +++++++++++++++++++++
 tests/unit/test_runtime_health.py                  |  10 +-
 tests/unit/test_supply_chain_policy.py             |  17 ++
 17 files changed, 471 insertions(+), 16 deletions(-)
$ gh pr view 193 --json number,url,headRefOid
[1;37m{[m
  [1;34m"headRefOid"[m[1;37m:[m [32m"7191193d671063dc01849562c79af69a8737fdf5"[m[1;37m,[m
  [1;34m"number"[m[1;37m:[m 193[1;37m,[m
  [1;34m"url"[m[1;37m:[m [32m"https://github.com/mryfmo/dotfiles/pull/193"[m
[1;37m}[m
$ gh pr checks 193
CodeRabbit	pass	0		Review skipped: manual review required for this OSS repository
build	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/36302181473/job/108571756881	
build (client)	pass	3s	https://github.com/mryfmo/dotfiles/actions/runs/36302181487/job/108571756942	
build (server)	pass	3s	https://github.com/mryfmo/dotfiles/actions/runs/36302181487/job/108571757049	
changes	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/36302181476/job/108571756932	
private-bootstrap (macos-14, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/36302181481/job/108571757092	
private-bootstrap (ubuntu-latest, client)	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/36302181481/job/108571757125	
private-bootstrap (ubuntu-latest, server)	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/36302181481/job/108571757161	
public-bootstrap (macos-14, client)	pass	8m42s	https://github.com/mryfmo/dotfiles/actions/runs/36302181481/job/108571757146	
public-bootstrap (ubuntu-latest, server)	pass	7m18s	https://github.com/mryfmo/dotfiles/actions/runs/36302181481/job/108571756973	
test (macos-14, client)	pass	2m48s	https://github.com/mryfmo/dotfiles/actions/runs/36302181476/job/108571774332	
validate	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/36302181477/job/108571756962	
nix	skipping	0	https://github.com/mryfmo/dotfiles/actions/runs/36302181476/job/108571775068	
public-bootstrap (ubuntu-latest, client)	pass	7m57s	https://github.com/mryfmo/dotfiles/actions/runs/36302181481/job/108571757133	
test (ubuntu-latest, client)	pass	4m47s	https://github.com/mryfmo/dotfiles/actions/runs/36302181476/job/108571774299	
test (ubuntu-latest, server)	pass	2m7s	https://github.com/mryfmo/dotfiles/actions/runs/36302181476/job/108571774324	
exit=0
```
History note: the first CI run on 80776ab failed the three `test` jobs on ShellCheck SC2015 (a CI-vs-local ShellCheck version difference). This was fixed in a12f507, and the next run was green.

## CI install proof (revision-2 run)
```
$ gh run view --job 108571757133 --log | grep -E 'Setting up mosh|gpgv: Good signature|Skipping bwrap AppArmor'
Setting up mosh (1.4.0-1ubuntu3) ...
gpgv: Good signature from "AWS CLI Team <aws-cli@amazon.com>"
Skipping bwrap AppArmor userns profile: /usr/bin/bwrap is not installed.
$ gh run view --job 108571756973 --log | grep -E 'Setting up mosh|gpgv: Good signature|Skipping bwrap AppArmor'
Setting up mosh (1.4.0-1ubuntu3) ...
gpgv: Good signature from "AWS CLI Team <aws-cli@amazon.com>"
Skipping bwrap AppArmor userns profile: /usr/bin/bwrap is not installed.
```

## CompactionDB
```
$ python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "T31: mosh managed on both OSes (PACKAGES + only investigation-proven config); upgrade-tools.sh pins-only bump path covers mise/sheldon/starship/aws-cli under the 7-day window (starship bumped to v1.26.0, window skips proven live); dead dependabot actor guards removed (operator 2026-09-27)"
a40a36b2-7f57-4379-863e-d8ab52bd818c
```
