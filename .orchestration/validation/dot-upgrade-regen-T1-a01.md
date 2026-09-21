# dot-upgrade-regen-T1-a01 validation

## Initial make upgrade (exit 2)

```text
./scripts/upgrade-tools.sh 

==> Homebrew
==> Updating Homebrew...
Updated 4 taps (hashicorp/tap, tw93/tap, homebrew/core and homebrew/cask).
==> New Formulae
bend: Language that blocks AI mistakes via proof
go-arch-lint: Architecture linter for Go projects
percona-server@8.4: Drop-in MySQL replacement
ratex: Fast TeX engine written in Rust
smbclient-ng: Fast and user friendly way to interact with SMB shares
taoup: Tao of Unix Programming with Ruby-powered ANSI-colored fortunes
termaid: Render Mermaid diagrams in the terminal
workmux: Git worktrees + tmux windows for zero-friction parallel dev
xgrammar: Structured generation and reasoning engine for LLMs
==> New Casks
colamd: Markdown editor
font-google-sans
gloomberb: Finance terminal
incy: Proxy client
jlcone: Desktop client for JLCPCB quoting, ordering and order tracking
muse: AI assistant for managing tasks, projects, and long-term goals
openplc-editor: IDE for creating programs for the OpenPLC Runtime
recordly: Creator-focused screen recorder with auto-zoom, cursor effects, and more
reolink: Client for viewing and managing security cameras and NVRs
ruswitcher: Keyboard layout switcher
tapmap: Visualise network connections on an interactive world map
tencent-yingyongbao: Tencent application store
==> Outdated Formulae
awscli
crit
ffmpeg
mole
mosh
node
protobuf
terraform
uv
==> Outdated Casks
codexbar

You have 9 outdated formulae and 1 outdated cask installed.
You can upgrade them with brew upgrade
or list them with brew outdated.
Skipping forbidden Homebrew formula: node
==> Downloading bottle manifests
✔︎ Bottle Manifest crit (0.20.2)
✔︎ Bottle Manifest uv (0.12.17)
✔︎ Bottle Manifest mole (1.55.0)
✔︎ Bottle Manifest protobuf (36.2)
✔︎ Bottle Manifest ffmpeg (9.0.2)
✔︎ Bottle Manifest mosh (1.4.0_43)
✔︎ Bottle Manifest awscli (2.36.49)
Warning: `$HOMEBREW_NO_INSTALLED_DEPENDENTS_CHECK` is set: not checking for outdated
dependents or dependents with broken linkage!
==> Fetching downloads for: uv, crit, ffmpeg, mole, protobuf, mosh, hashicorp/tap/terraform and awscli
Warning: `$HOMEBREW_NO_INSTALLED_DEPENDENTS_CHECK` is set: not checking for outdated
dependents or dependents with broken linkage!
==> Would upgrade 8 requested outdated packages
uv                       0.12.15  -> 0.12.17 (18.8MB)
crit                     0.20.1   -> 0.20.2 (7.2MB)
ffmpeg                   9.0.1_1  -> 9.0.2 (21.5MB)
mole                     1.54.0   -> 1.55.0 (4MB)
protobuf                 36.1     -> 36.2 (3.8MB)
mosh                     1.4.0_42 -> 1.4.0_43 (274.9KB)
hashicorp/tap/terraform  1.16.1   -> 1.16.3
awscli                   2.36.47  -> 2.36.49 (23.4MB)
✔︎ Bottle mosh (1.4.0_43)
✔︎ Bottle protobuf (36.2)
✔︎ Bottle mole (1.55.0)
✔︎ Formula terraform (1.16.3)
✔︎ Bottle crit (0.20.2)
✔︎ Bottle ffmpeg (9.0.2)
✔︎ Bottle uv (0.12.17)
✔︎ Bottle awscli (2.36.49)
==> Upgrading uv
  0.12.15 -> 0.12.17 
==> Pouring uv--0.12.17.arm64_tahoe.bottle.tar.gz
🍺  /opt/homebrew/Cellar/uv/0.12.17: 17 files, 45.3MB
==> Upgrading crit
  0.20.1 -> 0.20.2 
==> Pouring crit--0.20.2.arm64_tahoe.bottle.tar.gz
🍺  /opt/homebrew/Cellar/crit/0.20.2: 6 files, 20.4MB
==> Upgrading ffmpeg
  9.0.1_1 -> 9.0.2 
==> Pouring ffmpeg--9.0.2.arm64_tahoe.bottle.tar.gz
🍺  /opt/homebrew/Cellar/ffmpeg/9.0.2: 290 files, 53.9MB
==> Upgrading mole
  1.54.0 -> 1.55.0 
==> Pouring mole--1.55.0.arm64_tahoe.bottle.tar.gz
🍺  /opt/homebrew/Cellar/mole/1.55.0: 64 files, 10.9MB
==> Upgrading protobuf
  36.1 -> 36.2 
==> Pouring protobuf--36.2.arm64_tahoe.bottle.tar.gz
🍺  /opt/homebrew/Cellar/protobuf/36.2: 387 files, 17.8MB
==> Upgrading mosh
  1.4.0_42 -> 1.4.0_43 
==> Pouring mosh--1.4.0_43.arm64_tahoe.bottle.tar.gz
🍺  /opt/homebrew/Cellar/mosh/1.4.0_43: 16 files, 878.1KB
==> Upgrading hashicorp/tap/terraform
  1.16.1 -> 1.16.3 
Warning: A newer Command Line Tools release is available.
Update them from Software Update in System Settings.

If that doesn't show you any updates, run:
  sudo rm -rf /Library/Developer/CommandLineTools
  sudo xcode-select --install

Alternatively, manually download them from:
  https://developer.apple.com/download/all/.
You should download the Command Line Tools for Xcode 26.6.

This is a Tier 2 configuration:
  https://docs.brew.sh/Support-Tiers#tier-2
You can report issues with Tier 2 configurations to Homebrew/* repositories!
  https://docs.brew.sh/Troubleshooting
Read the above document before opening any issues or PRs.
🍺  /opt/homebrew/Cellar/terraform/1.16.3: 8 files, 114.5MB, built in 3 seconds
==> Upgrading awscli
  2.36.47 -> 2.36.49 
==> Pouring awscli--2.36.49.arm64_tahoe.bottle.tar.gz
🍺  /opt/homebrew/Cellar/awscli/2.36.49: 14,680 files, 162.5MB
==> Cleanup
Removing: /opt/homebrew/Cellar/protobuf/36.1... (387 files, 17.8MB)
Removing: /opt/homebrew/Cellar/terraform/1.16.1... (5 files, 114.4MB)
Removing: /opt/homebrew/Cellar/crit/0.20.1... (6 files, 20.4MB)
Removing: /opt/homebrew/Cellar/mosh/1.4.0_42... (16 files, 878.1KB)
Removing: /opt/homebrew/Cellar/uv/0.12.15... (17 files, 44.5MB)
Removing: /opt/homebrew/Cellar/mole/1.54.0... (63 files, 10.9MB)
Removing: /opt/homebrew/Cellar/ffmpeg/9.0.1_1... (290 files, 53.8MB)
Removing: /Users/mryfmo/Library/Caches/Homebrew/uv--0.12.15... (18.5MB)
Removing: /Users/mryfmo/Library/Caches/Homebrew/uv_bottle_manifest--0.12.15... (18.8KB)
Removing: /Users/mryfmo/Library/Caches/Homebrew/mole--1.54.0... (4MB)
Removing: /Users/mryfmo/Library/Caches/Homebrew/mole_bottle_manifest--1.54.0... (8.8KB)
Removing: /opt/homebrew/Cellar/awscli/2.36.47... (14,680 files, 162.4MB)
Removing: /Users/mryfmo/Library/Caches/Homebrew/awscli--2.36.47... (23.4MB)
Removing: /Users/mryfmo/Library/Caches/Homebrew/awscli_bottle_manifest--2.36.47... (138.5KB)
Disable this behaviour by setting `HOMEBREW_NO_INSTALL_CLEANUP=1`.
Hide these hints with `HOMEBREW_NO_ENV_HINTS=1` (see `man brew`).
==> Caveats
zsh completions have been installed to:
  /opt/homebrew/share/zsh/site-functions
zsh completions and functions have been installed to:
  /opt/homebrew/share/zsh/site-functions
==> uv
The following uv executables are shadowed by other commands earlier in your PATH:
  uv (shadowed by /Users/mryfmo/.local/share/mise/shims/uv)
  uvx (shadowed by /Users/mryfmo/.local/share/mise/shims/uvx)
Running these by name will not invoke the version provided by Homebrew.
Disable this behaviour by setting `HOMEBREW_NO_PATH_SHADOW_CHECK=1`.
Hide these hints with `HOMEBREW_NO_ENV_HINTS=1` (see `man brew`).
==> ffmpeg
ffmpeg-full includes additional tools and libraries that are not included in the regular ffmpeg formula.
==> awscli
The "examples" directory has been installed to:
  /opt/homebrew/share/awscli/examples
==> Upgraded 8 requested outdated packages
uv                       0.12.15  -> 0.12.17
crit                     0.20.1   -> 0.20.2
ffmpeg                   9.0.1_1  -> 9.0.2
mole                     1.54.0   -> 1.55.0
protobuf                 36.1     -> 36.2
mosh                     1.4.0_42 -> 1.4.0_43
hashicorp/tap/terraform  1.16.1   -> 1.16.3
awscli                   2.36.47  -> 2.36.49
==> Would upgrade 1 requested outdated package
codexbar 0.60.4 -> 0.63.0
==> Fetching downloads for: codexbar
✔︎ Cask codexbar (0.63.0)
==> Upgrading codexbar
  0.60.4 -> 0.63.0
==> Backing up App 'CodexBar.app' to '/opt/homebrew/Caskroom/codexbar/0.60.4/CodexBar.app'
==> Removing App '/Applications/CodexBar.app'
==> Unlinking Binary '/opt/homebrew/bin/codexbar'
==> Moving App 'CodexBar.app' to '/Applications/CodexBar.app'
==> Linking Binary 'CodexBarCLI' to '/opt/homebrew/bin/codexbar'
==> Purging files for version 0.60.4 of Cask codexbar
🍺  codexbar was successfully upgraded!
==> Cleanup
Removing: /Users/mryfmo/Library/Caches/Homebrew/Cask/codexbar--0.60.4.zip... (70.5MB)
Disable this behaviour by setting `HOMEBREW_NO_INSTALL_CLEANUP=1`.
Hide these hints with `HOMEBREW_NO_ENV_HINTS=1` (see `man brew`).
==> Upgraded 1 requested outdated package
codexbar 0.60.4 -> 0.63.0

==> mise self-update
Checking target-arch... mise-v2026.9.12-macos-arm64.tar.gz
Checking current version... v2026.9.10
Looking for tag: v2026.9.12

mise release status:
  * Current exe: /Users/mryfmo/.local/bin/mise
  * New exe release: "mise-v2026.9.12-macos-arm64.tar.gz"
  * New exe download url: "https://api.github.com/repos/jdx/mise/releases/assets/576717088"

The new release will be downloaded/extracted and the existing binary will be replaced.
Downloading...
mise ERROR IoError: request or response body error
mise ERROR request or response body error
mise ERROR error reading a body from connection
mise ERROR connection reset
mise ERROR Version: 2026.9.10 macos-arm64 (2026-09-16)
mise ERROR Run with --verbose or MISE_VERBOSE=1 for more information
required failure: mise self-update

==> mise tools
mise WARN  No untrusted config files found.
mise by @jdx – installing 1 tool
mise ⇢ age@1.3.2  164ms · already installed
mise ████████████████ 1/1 · installed 0 tools · 1 already installed in 165ms
mise by @jdx – installing 1 tool
mise ⇢ aqua:micro-editor/micro@2.0.15  622ms · already installed
mise ████████████████ 1/1 · installed 0 tools · 1 already installed in 623ms
mise by @jdx – installing 1 tool
mise ⇢ bun@1.4.2  130ms · already installed
mise ████████████████ 1/1 · installed 0 tools · 1 already installed in 131ms
mise by @jdx – installing 1 tool
mise ⇢ cargo:eza@0.23.5  205ms · already installed
mise ████████████████ 1/1 · installed 0 tools · 1 already installed in 206ms
mise by @jdx – installing 1 tool
mise ⇢ cargo:pueue@4.0.4  627ms · already installed
mise ████████████████ 1/1 · installed 0 tools · 1 already installed in 628ms
mise by @jdx – installing 1 tool
mise ⇢ chezmoi@2.72.1  122ms · already installed
mise ████████████████ 1/1 · installed 0 tools · 1 already installed in 123ms
mise by @jdx – installing 1 tool
mise ⇢ cmake@4.4.3  122ms · already installed
mise ████████████████ 1/1 · installed 0 tools · 1 already installed in 123ms
mise by @jdx – installing 1 tool
mise ⇢ dotenvx@2.23.0  122ms · already installed
mise ████████████████ 1/1 · installed 0 tools · 1 already installed in 123ms
mise by @jdx – installing 1 tool
mise ⇢ fd@10.3.0  136ms · already installed
mise ████████████████ 1/1 · installed 0 tools · 1 already installed in 137ms
mise by @jdx – installing 1 tool
mise ░░░░░░░░░░░░░░░░ 0/1 · 3.0s
  github:cli/cli@2.100.0  resolving  3.0s
mise ░░░░░░░░░░░░░░░░ 0/1 · 6.0s
  github:cli/cli@2.100.0  resolving  6.0s
mise ░░░░░░░░░░░░░░░░ 0/1 · 9.0s
  github:cli/cli@2.100.0  resolving  9.0s
mise ░░░░░░░░░░░░░░░░ 0/1 · 12.0s
  github:cli/cli@2.100.0  resolving  12.0s
mise ░░░░░░░░░░░░░░░░ 0/1 · 15.0s
  github:cli/cli@2.100.0  resolving  15.0s
mise ░░░░░░░░░░░░░░░░ 0/1 · 18.0s
  github:cli/cli@2.100.0  resolving  18.0s
mise WARN  HTTP GET https://api.github.com/repos/cli/cli/releases?per_page=100 attempt 1 failed after 20.00s (transient): HTTP timed out after 20.00s for https://api.github.com/repos/cli/cli/releases?per_page=100 (change with `fetch_remote_versions_timeout` or env `MISE_FETCH_REMOTE_VERSIONS_TIMEOUT`).; retrying in 138.20165ms
mise ░░░░░░░░░░░░░░░░ 0/1 · 21.0s
  github:cli/cli@2.100.0  resolving  21.0s
mise ░░░░░░░░░░░░░░░░ 0/1 · 24.0s
  github:cli/cli@2.100.0  resolving  24.0s
mise ░░░░░░░░░░░░░░░░ 0/1 · 27.1s
  github:cli/cli@2.100.0  resolving  27.1s
mise ░░░░░░░░░░░░░░░░ 0/1 · 30.1s
  github:cli/cli@2.100.0  resolving  30.1s
mise ░░░░░░░░░░░░░░░░ 0/1 · 33.1s
  github:cli/cli@2.100.0  resolving  33.1s
mise ░░░░░░░░░░░░░░░░ 0/1 · 36.4s
  github:cli/cli@2.100.0  resolving  36.4s
mise ░░░░░░░░░░░░░░░░ 0/1 · 40.0s
  github:cli/cli@2.100.0  resolving  40.0s
mise WARN  HTTP GET https://api.github.com/repos/cli/cli/releases?per_page=100 attempt 2 failed after 20.00s (transient): HTTP timed out after 20.00s for https://api.github.com/repos/cli/cli/releases?per_page=100 (change with `fetch_remote_versions_timeout` or env `MISE_FETCH_REMOTE_VERSIONS_TIMEOUT`).; retrying in 641.771562ms
mise WARN  HTTP GET https://api.github.com/repos/cli/cli/releases?per_page=100 attempt 3 failed after 1.79s (transient): HTTP timed out after 20.00s for https://api.github.com/repos/cli/cli/releases?per_page=100 (change with `fetch_remote_versions_timeout` or env `MISE_FETCH_REMOTE_VERSIONS_TIMEOUT`).; retrying in 3.368237227s
mise ░░░░░░░░░░░░░░░░ 0/1 · 44.0s
  github:cli/cli@2.100.0  resolving  44.0s
mise ⇢ github:cli/cli@2.100.0  47.4s · already installed
mise ████████████████ 1/1 · installed 0 tools · 1 already installed in 47.4s
mise by @jdx – installing 1 tool
mise ░░░░░░░░░░░░░░░░ 0/1 · 3.0s
  github:d-kuro/gwq@0.1.1  resolving  3.0s
mise ⇢ github:d-kuro/gwq@0.1.1  3.6s · already installed
mise ████████████████ 1/1 · installed 0 tools · 1 already installed in 3.6s
mise by @jdx – installing 1 tool
mise ░░░░░░░░░░░░░░░░ 0/1 · 3.0s
  github:mikefarah/yq@4.53.6  resolving  3.0s
mise ░░░░░░░░░░░░░░░░ 0/1 · 6.0s
  github:mikefarah/yq@4.53.6  resolving  6.0s
mise ░░░░░░░░░░░░░░░░ 0/1 · 9.0s
  github:mikefarah/yq@4.53.6  resolving  9.0s
mise ░░░░░░░░░░░░░░░░ 0/1 · 12.0s
  github:mikefarah/yq@4.53.6  resolving  12.0s
mise ░░░░░░░░░░░░░░░░ 0/1 · 15.0s
  github:mikefarah/yq@4.53.6  resolving  15.0s
mise ░░░░░░░░░░░░░░░░ 0/1 · 18.0s
  github:mikefarah/yq@4.53.6  resolving  18.0s
mise WARN  HTTP GET https://api.github.com/repos/mikefarah/yq/releases?per_page=100 attempt 1 failed after 20.00s (transient): HTTP timed out after 20.00s for https://api.github.com/repos/mikefarah/yq/releases?per_page=100 (change with `fetch_remote_versions_timeout` or env `MISE_FETCH_REMOTE_VERSIONS_TIMEOUT`).; retrying in 191.56113ms
mise ░░░░░░░░░░░░░░░░ 0/1 · 21.0s
  github:mikefarah/yq@4.53.6  resolving  21.0s
mise ░░░░░░░░░░░░░░░░ 0/1 · 24.0s
  github:mikefarah/yq@4.53.6  resolving  24.0s
mise ░░░░░░░░░░░░░░░░ 0/1 · 27.1s
  github:mikefarah/yq@4.53.6  resolving  27.1s
mise ░░░░░░░░░░░░░░░░ 0/1 · 30.1s
  github:mikefarah/yq@4.53.6  resolving  30.1s
mise ░░░░░░░░░░░░░░░░ 0/1 · 33.1s
  github:mikefarah/yq@4.53.6  resolving  33.1s
mise ░░░░░░░░░░░░░░░░ 0/1 · 36.4s
  github:mikefarah/yq@4.53.6  resolving  36.4s
mise WARN  HTTP GET https://api.github.com/repos/mikefarah/yq/releases?per_page=100 attempt 2 failed after 16.50s (transient): HTTP timed out after 20.00s for https://api.github.com/repos/mikefarah/yq/releases?per_page=100 (change with `fetch_remote_versions_timeout` or env `MISE_FETCH_REMOTE_VERSIONS_TIMEOUT`).; retrying in 547.44206ms
mise ░░░░░░░░░░░░░░░░ 0/1 · 40.0s
  github:mikefarah/yq@4.53.6  resolving  40.0s
mise ⇢ github:mikefarah/yq@4.53.6  40.1s · already installed
mise ████████████████ 1/1 · installed 0 tools · 1 already installed in 40.1s
mise by @jdx – installing 1 tool
mise ⇢ github:ogulcancelik/herdr@0.9.0  893ms · already installed
mise ████████████████ 1/1 · installed 0 tools · 1 already installed in 895ms
mise by @jdx – installing 1 tool
mise ⇢ github:x-motemen/ghq@1.10.1  571ms · already installed
mise ████████████████ 1/1 · installed 0 tools · 1 already installed in 572ms
mise by @jdx – installing 1 tool
mise ⇢ http:bats@1.13.0  2ms · already installed
mise ████████████████ 1/1 · installed 0 tools · 1 already installed in 3ms
mise by @jdx – installing 1 tool
mise ⇢ http:gcloud@575.0.1  1ms · already installed
mise ████████████████ 1/1 · installed 0 tools · 1 already installed in 2ms
mise by @jdx – installing 1 tool
mise ⇢ hugo-extended@0.166.0  150ms · already installed
mise ████████████████ 1/1 · installed 0 tools · 1 already installed in 151ms
mise by @jdx – installing 1 tool
mise ⇢ jq@1.8.2  126ms · already installed
mise ████████████████ 1/1 · installed 0 tools · 1 already installed in 127ms
mise by @jdx – installing 1 tool
mise ⇢ node@26.8.2  125ms · already installed
mise ████████████████ 1/1 · installed 0 tools · 1 already installed in 126ms
mise by @jdx – installing 1 tool
mise ⇢ npm:@anthropic-ai/claude-code@2.1.275  342ms · already installed
mise ████████████████ 1/1 · installed 0 tools · 1 already installed in 344ms
mise by @jdx – installing 1 tool
mise ⇢ npm:@openai/codex@0.154.0  699ms · already installed
mise ████████████████ 1/1 · installed 0 tools · 1 already installed in 700ms
mise by @jdx – installing 1 tool
mise ⇢ npm:bash-language-server@5.6.0  297ms · already installed
mise ████████████████ 1/1 · installed 0 tools · 1 already installed in 299ms
mise by @jdx – installing 1 tool
mise ⇢ npm:ccstatusline@2.2.29  169ms · already installed
mise ████████████████ 1/1 · installed 0 tools · 1 already installed in 170ms
mise by @jdx – installing 1 tool
mise ⇢ npm:ccusage@20.0.20  185ms · already installed
mise ████████████████ 1/1 · installed 0 tools · 1 already installed in 186ms
mise by @jdx – installing 1 tool
mise ⇢ npm:fast-cli@5.2.0  237ms · already installed
mise ████████████████ 1/1 · installed 0 tools · 1 already installed in 238ms
mise by @jdx – installing 1 tool
mise ⇢ npm:pyright@1.1.414  156ms · already installed
mise ████████████████ 1/1 · installed 0 tools · 1 already installed in 157ms
mise by @jdx – installing 1 tool
mise ⇢ python@3.14.7  2.3s · already installed
mise ████████████████ 1/1 · installed 0 tools · 1 already installed in 2.3s
mise by @jdx – installing 1 tool
mise ⇢ rust@1.98.1  446ms · already installed
mise ████████████████ 1/1 · installed 0 tools · 1 already installed in 447ms
mise by @jdx – installing 1 tool
mise ⇢ shellcheck@0.11.0  118ms · already installed
mise ████████████████ 1/1 · installed 0 tools · 1 already installed in 119ms
mise by @jdx – installing 1 tool
mise ⇢ shfmt@3.14.1  116ms · already installed
mise ████████████████ 1/1 · installed 0 tools · 1 already installed in 117ms
mise by @jdx – installing 1 tool
mise ⇢ uv@0.12.13  110ms · already installed
mise ████████████████ 1/1 · installed 0 tools · 1 already installed in 111ms
mise by @jdx – installing 1 tool
mise ⇢ yazi@26.9.1  127ms · already installed
mise ████████████████ 1/1 · installed 0 tools · 1 already installed in 128ms
mise by @jdx – resolving 33 tools
mise ✓ rust                           2ms
mise ✓ node                           2ms
mise ✓ dotenvx                        2ms
mise ✓ chezmoi                        2ms
mise ✓ age                            2ms
mise ✓ bun                            2ms
mise ✓ cmake                          2ms
mise ✓ python                         2ms
mise ✓ cargo:eza                      2ms
mise ✓ hugo-extended                  2ms
mise ✓ jq                             2ms
mise ✓ yazi                           3ms
mise ✓ uv                             3ms
mise ✓ fd                             3ms
mise ✓ aqua:micro-editor/micro        3ms
mise ✓ github:mikefarah/yq            3ms
mise ✓ shellcheck                     3ms
mise ✓ shfmt                          3ms
mise ✓ npm:@anthropic-ai/claude-code  3ms
mise ✓ npm:@openai/codex              3ms
mise ✓ npm:bash-language-server       3ms
mise ✓ npm:fast-cli                   3ms
mise ✓ npm:ccusage                    3ms
mise ✓ npm:ccstatusline               3ms
mise ✓ github:shuntaka9576/blocc      4ms
mise ✓ github:x-motemen/ghq           4ms
mise ✓ npm:pyright                    4ms
mise ✓ cargo:pueue                    4ms
mise ✓ github:d-kuro/gwq              4ms
mise ✓ github:ogulcancelik/herdr      4ms
mise ✓ http:bats                      4ms
mise ✓ http:gcloud                    4ms
mise ✓ github:cli/cli                 4ms
mise ████████████████ 33/33 · resolved 33 tools in 4ms
mise by @jdx – resolving 1 tool
mise ✓ aqua:FiloSottile/age@1.3.2  1.1s
mise ████████████████ 1/1 · resolved 1 tool in 1.1s
mise All tools are up to date
mise by @jdx – resolving 33 tools
mise ✓ rust                           3ms
mise ✓ cmake                          3ms
mise ✓ python                         3ms
mise ✓ dotenvx                        3ms
mise ✓ node                           3ms
mise ✓ age                            3ms
mise ✓ bun                            3ms
mise ✓ cargo:eza                      3ms
mise ✓ chezmoi                        3ms
mise ✓ fd                             3ms
mise ✓ jq                             3ms
mise ✓ hugo-extended                  4ms
mise ✓ uv                             4ms
mise ✓ shellcheck                     4ms
mise ✓ yazi                           4ms
mise ✓ github:mikefarah/yq            4ms
mise ✓ aqua:micro-editor/micro        4ms
mise ✓ npm:bash-language-server       4ms
mise ✓ npm:@anthropic-ai/claude-code  4ms
mise ✓ npm:@openai/codex              4ms
mise ✓ shfmt                          4ms
mise ✓ npm:ccusage                    4ms
mise ✓ github:x-motemen/ghq           4ms
mise ✓ npm:fast-cli                   4ms
mise ✓ npm:ccstatusline               4ms
mise ✓ npm:pyright                    4ms
mise ✓ github:shuntaka9576/blocc      5ms
mise ✓ github:d-kuro/gwq              5ms
mise ✓ github:cli/cli                 5ms
mise ✓ cargo:pueue                    5ms
mise ✓ github:ogulcancelik/herdr      5ms
mise ✓ http:bats                      5ms
mise ✓ http:gcloud                    5ms
mise ████████████████ 33/33 · resolved 33 tools in 5ms
mise by @jdx – resolving 1 tool
mise ✓ aqua:micro-editor/micro@2.0.15  2.0s
mise ████████████████ 1/1 · resolved 1 tool in 2.0s
mise All tools are up to date
mise by @jdx – resolving 33 tools
mise ✓ node                           4ms
mise ✓ cmake                          4ms
mise ✓ bun                            4ms
mise ✓ dotenvx                        4ms
mise ✓ python                         4ms
mise ✓ age                            4ms
mise ✓ chezmoi                        4ms
mise ✓ fd                             4ms
mise ✓ rust                           4ms
mise ✓ jq                             4ms
mise ✓ cargo:eza                      4ms
mise ✓ hugo-extended                  5ms
mise ✓ uv                             5ms
mise ✓ yazi                           5ms
mise ✓ aqua:micro-editor/micro        5ms
mise ✓ shellcheck                     5ms
mise ✓ github:mikefarah/yq            5ms
mise ✓ npm:bash-language-server       5ms
mise ✓ shfmt                          5ms
mise ✓ npm:@anthropic-ai/claude-code  5ms
mise ✓ npm:@openai/codex              5ms
mise ✓ npm:fast-cli                   6ms
mise ✓ npm:ccstatusline               6ms
mise ✓ npm:pyright                    6ms
mise ✓ github:x-motemen/ghq           6ms
mise ✓ github:d-kuro/gwq              6ms
mise ✓ github:shuntaka9576/blocc      6ms
mise ✓ github:cli/cli                 6ms
mise ✓ npm:ccusage                    6ms
mise ✓ cargo:pueue                    6ms
mise ✓ github:ogulcancelik/herdr      6ms
mise ✓ http:bats                      6ms
mise ✓ http:gcloud                    6ms
mise ████████████████ 33/33 · resolved 33 tools in 6ms
mise by @jdx – resolving 1 tool
mise ✓ core:bun@1.4.2  147ms
mise ████████████████ 1/1 · resolved 1 tool in 147ms
mise All tools are up to date
mise by @jdx – resolving 33 tools
mise ✓ rust                           8ms
mise ✓ chezmoi                        8ms
mise ✓ dotenvx                        8ms
mise ✓ age                            8ms
mise ✓ python                         8ms
mise ✓ bun                            8ms
mise ✓ cmake                          8ms
mise ✓ node                           8ms
mise ✓ cargo:eza                      8ms
mise ✓ shellcheck                     8ms
mise ✓ fd                             8ms
mise ✓ hugo-extended                  8ms
mise ✓ uv                             8ms
mise ✓ jq                             8ms
mise ✓ aqua:micro-editor/micro        8ms
mise ✓ yazi                           9ms
mise ✓ github:mikefarah/yq            9ms
mise ✓ npm:bash-language-server       9ms
mise ✓ shfmt                          9ms
mise ✓ npm:@anthropic-ai/claude-code  9ms
mise ✓ npm:@openai/codex              9ms
mise ✓ npm:ccstatusline               9ms
mise ✓ npm:ccusage                    9ms
mise ✓ npm:fast-cli                   9ms
mise ✓ github:shuntaka9576/blocc      9ms
mise ✓ github:x-motemen/ghq           9ms
mise ✓ npm:pyright                    9ms
mise ✓ cargo:pueue                    11ms
mise ✓ github:d-kuro/gwq              11ms
mise ✓ github:ogulcancelik/herdr      11ms
mise ✓ github:cli/cli                 11ms
mise ✓ http:bats                      11ms
mise ✓ http:gcloud                    11ms
mise ████████████████ 33/33 · resolved 33 tools in 11ms
mise by @jdx – resolving 1 tool
mise ✓ cargo:eza@0.23.5  275ms
mise ████████████████ 1/1 · resolved 1 tool in 275ms
mise All tools are up to date
mise by @jdx – resolving 33 tools
mise ✓ rust                           3ms
mise ✓ node                           3ms
mise ✓ python                         3ms
mise ✓ cmake                          3ms
mise ✓ dotenvx                        3ms
mise ✓ bun                            3ms
mise ✓ age                            3ms
mise ✓ chezmoi                        3ms
mise ✓ cargo:eza                      3ms
mise ✓ fd                             3ms
mise ✓ jq                             3ms
mise ✓ shellcheck                     3ms
mise ✓ hugo-extended                  3ms
mise ✓ uv                             3ms
mise ✓ aqua:micro-editor/micro        3ms
mise ✓ github:mikefarah/yq            3ms
mise ✓ yazi                           4ms
mise ✓ npm:bash-language-server       4ms
mise ✓ shfmt                          4ms
mise ✓ npm:@anthropic-ai/claude-code  4ms
mise ✓ npm:@openai/codex              4ms
mise ✓ npm:fast-cli                   4ms
mise ✓ npm:ccusage                    4ms
mise ✓ npm:pyright                    4ms
mise ✓ github:shuntaka9576/blocc      4ms
mise ✓ npm:ccstatusline               4ms
mise ✓ github:x-motemen/ghq           4ms
mise ✓ github:cli/cli                 4ms
mise ✓ github:ogulcancelik/herdr      4ms
mise ✓ http:bats                      4ms
mise ✓ http:gcloud                    4ms
mise ✓ github:d-kuro/gwq              4ms
mise ✓ cargo:pueue                    5ms
mise ████████████████ 33/33 · resolved 33 tools in 5ms
mise by @jdx – resolving 1 tool
mise ✓ cargo:pueue@4.0.4  1.5s
mise ████████████████ 1/1 · resolved 1 tool in 1.5s
mise All tools are up to date
mise by @jdx – resolving 33 tools
mise ✓ rust                           3ms
mise ✓ chezmoi                        3ms
mise ✓ cmake                          3ms
mise ✓ dotenvx                        3ms
mise ✓ python                         3ms
mise ✓ node                           3ms
mise ✓ age                            3ms
mise ✓ bun                            3ms
mise ✓ cargo:eza                      3ms
mise ✓ fd                             3ms
mise ✓ uv                             3ms
mise ✓ hugo-extended                  3ms
mise ✓ yazi                           3ms
mise ✓ jq                             3ms
mise ✓ shellcheck                     4ms
mise ✓ aqua:micro-editor/micro        4ms
mise ✓ github:mikefarah/yq            4ms
mise ✓ npm:bash-language-server       4ms
mise ✓ shfmt                          4ms
mise ✓ npm:@openai/codex              4ms
mise ✓ npm:@anthropic-ai/claude-code  4ms
mise ✓ npm:fast-cli                   4ms
mise ✓ npm:ccusage                    4ms
mise ✓ github:x-motemen/ghq           4ms
mise ✓ npm:ccstatusline               4ms
mise ✓ github:shuntaka9576/blocc      4ms
mise ✓ npm:pyright                    4ms
mise ✓ github:d-kuro/gwq              4ms
mise ✓ github:cli/cli                 5ms
mise ✓ cargo:pueue                    5ms
mise ✓ github:ogulcancelik/herdr      5ms
mise ✓ http:bats                      5ms
mise ✓ http:gcloud                    5ms
mise ████████████████ 33/33 · resolved 33 tools in 5ms
mise by @jdx – resolving 1 tool
mise ✓ aqua:twpayne/chezmoi@2.72.1  2.4s
mise ████████████████ 1/1 · resolved 1 tool in 2.4s
mise by @jdx – installing 1 tool
mise ░░░░░░░░░░░░░░░░ 0/1 · 3.0s
  chezmoi@2.72.2  installing  3.0s
mise █████████████░░░ 0/1 · 6.0s
  chezmoi@2.72.2  verifying  6.0s  11/11 kB · 12 kB/s
mise WARN  HTTP GET https://github.com/twpayne/chezmoi/releases/download/v2.72.2/chezmoi_2.72.2_checksums.txt.sigstore.json attempt 1 failed after 13.1ms (transient): error sending request; retrying in 189.110173ms
mise ✓ chezmoi@2.72.2  7.0s  chezmoi_2.72.2_darwin_arm64.tar.gz
mise ████████████████ 1/1 · installed 1 tool in 7.0s
mise WARN  HTTP GET https://api.github.com/repos/shuntaka9576/blocc/releases/tags/v0.6.0 attempt 1 failed after 13.6ms (transient): error sending request; retrying in 141.05359ms
mise downloading artifact for lock-time provenance verification: chezmoi_2.72.2_linux_arm64.tar.gz
mise downloading artifact for lock-time provenance verification: chezmoi_2.72.2_darwin_amd64.tar.gz
mise downloading artifact for lock-time provenance verification: chezmoi_2.72.2_linux-glibc_amd64.tar.gz

Upgraded 1 tool:
  chezmoi 2.72.1 → 2.72.2
mise by @jdx – resolving 33 tools
mise ✓ rust                           2ms
mise ✓ cmake                          3ms
mise ✓ node                           3ms
mise ✓ python                         3ms
mise ✓ dotenvx                        3ms
mise ✓ bun                            3ms
mise ✓ chezmoi                        3ms
mise ✓ cargo:eza                      3ms
mise ✓ age                            3ms
mise ✓ shellcheck                     3ms
mise ✓ fd                             3ms
mise ✓ jq                             3ms
mise ✓ hugo-extended                  3ms
mise ✓ yazi                           3ms
mise ✓ github:mikefarah/yq            3ms
mise ✓ uv                             3ms
mise ✓ npm:bash-language-server       4ms
mise ✓ shfmt                          4ms
mise ✓ npm:@anthropic-ai/claude-code  4ms
mise ✓ aqua:micro-editor/micro        4ms
mise ✓ npm:@openai/codex              4ms
mise ✓ npm:ccstatusline               4ms
mise ✓ npm:fast-cli                   4ms
mise ✓ github:x-motemen/ghq           4ms
mise ✓ npm:ccusage                    4ms
mise ✓ github:shuntaka9576/blocc      4ms
mise ✓ npm:pyright                    4ms
mise ✓ github:d-kuro/gwq              4ms
mise ✓ cargo:pueue                    4ms
mise ✓ github:ogulcancelik/herdr      4ms
mise ✓ github:cli/cli                 4ms
mise ✓ http:bats                      4ms
mise ✓ http:gcloud                    4ms
mise ████████████████ 33/33 · resolved 33 tools in 5ms
mise by @jdx – resolving 1 tool
mise ✓ aqua:Kitware/CMake@4.4.3  1.2s
mise ████████████████ 1/1 · resolved 1 tool in 1.2s
mise All tools are up to date
mise by @jdx – resolving 33 tools
mise ✓ rust                           3ms
mise ✓ age                            3ms
mise ✓ dotenvx                        3ms
mise ✓ cmake                          3ms
mise ✓ chezmoi                        3ms
mise ✓ node                           3ms
mise ✓ python                         3ms
mise ✓ bun                            3ms
mise ✓ cargo:eza                      3ms
mise ✓ aqua:micro-editor/micro        3ms
mise ✓ uv                             3ms
mise ✓ fd                             3ms
mise ✓ jq                             3ms
mise ✓ github:mikefarah/yq            4ms
mise ✓ hugo-extended                  4ms
mise ✓ yazi                           4ms
mise ✓ shellcheck                     4ms
mise ✓ shfmt                          4ms
mise ✓ npm:bash-language-server       4ms
mise ✓ npm:@openai/codex              4ms
mise ✓ npm:fast-cli                   4ms
mise ✓ npm:ccstatusline               4ms
mise ✓ npm:@anthropic-ai/claude-code  4ms
mise ✓ npm:ccusage                    4ms
mise ✓ npm:pyright                    4ms
mise ✓ github:x-motemen/ghq           4ms
mise ✓ github:shuntaka9576/blocc      4ms
mise ✓ github:d-kuro/gwq              4ms
mise ✓ cargo:pueue                    5ms
mise ✓ github:cli/cli                 5ms
mise ✓ http:bats                      5ms
mise ✓ http:gcloud                    5ms
mise ✓ github:ogulcancelik/herdr      5ms
mise ████████████████ 33/33 · resolved 33 tools in 5ms
mise by @jdx – resolving 1 tool
mise ✓ aqua:dotenvx/dotenvx@2.23.0  1.1s
mise ████████████████ 1/1 · resolved 1 tool in 1.1s
mise WARN  newer dotenvx release 2.28.2 (released 2026-09-20, eligible 2026-09-27 09:19 JST) ignored by minimum_release_age (7d); latest eligible release is 2.24.1
mise by @jdx – installing 1 tool
mise ░░░░░░░░░░░░░░░░ 0/1 · 3.0s
  dotenvx@2.24.1  installing  3.0s
mise ░░░░░░░░░░░░░░░░ 0/1 · 6.0s
  dotenvx@2.24.1  installing  6.0s
mise ░░░░░░░░░░░░░░░░ 0/1 · 9.0s
  dotenvx@2.24.1  installing  9.0s
mise ░░░░░░░░░░░░░░░░ 0/1 · 12.0s
  dotenvx@2.24.1  installing  12.0s
mise ░░░░░░░░░░░░░░░░ 0/1 · 15.0s
  dotenvx@2.24.1  installing  15.0s
mise ░░░░░░░░░░░░░░░░ 0/1 · 18.0s
  dotenvx@2.24.1  installing  18.0s
mise WARN  HTTP GET https://api.github.com/repos/dotenvx/dotenvx/releases?per_page=100 attempt 1 failed after 20.00s (transient): HTTP timed out after 20.00s for https://api.github.com/repos/dotenvx/dotenvx/releases?per_page=100 (change with `fetch_remote_versions_timeout` or env `MISE_FETCH_REMOTE_VERSIONS_TIMEOUT`).; retrying in 169.95833ms
mise ░░░░░░░░░░░░░░░░ 0/1 · 21.0s
  dotenvx@2.24.1  installing  21.0s
mise ░░░░░░░░░░░░░░░░ 0/1 · 24.0s
  dotenvx@2.24.1  installing  24.0s
mise ░░░░░░░░░░░░░░░░ 0/1 · 27.0s
  dotenvx@2.24.1  installing  27.0s
mise ░░░░░░░░░░░░░░░░ 0/1 · 30.0s
  dotenvx@2.24.1  installing  30.0s
mise ░░░░░░░░░░░░░░░░ 0/1 · 33.1s
  dotenvx@2.24.1  installing  33.1s
mise ░░░░░░░░░░░░░░░░ 0/1 · 36.4s
  dotenvx@2.24.1  installing  36.4s
mise ░░░░░░░░░░░░░░░░ 0/1 · 40.0s
  dotenvx@2.24.1  installing  40.0s
mise WARN  HTTP GET https://api.github.com/repos/dotenvx/dotenvx/releases?per_page=100 attempt 2 failed after 20.00s (transient): HTTP timed out after 20.00s for https://api.github.com/repos/dotenvx/dotenvx/releases?per_page=100 (change with `fetch_remote_versions_timeout` or env `MISE_FETCH_REMOTE_VERSIONS_TIMEOUT`).; retrying in 698.02051ms
mise ░░░░░░░░░░░░░░░░ 0/1 · 44.0s
  dotenvx@2.24.1  installing  44.0s
mise ░░░░░░░░░░░░░░░░ 0/1 · 48.4s
  dotenvx@2.24.1  installing  48.4s
mise ░░░░░░░░░░░░░░░░ 0/1 · 53.3s
  dotenvx@2.24.1  installing  53.3s
mise WARN  HTTP GET https://api.github.com/repos/dotenvx/dotenvx/releases?per_page=100 attempt 3 failed after 13.52s (transient): HTTP timed out after 20.00s for https://api.github.com/repos/dotenvx/dotenvx/releases?per_page=100 (change with `fetch_remote_versions_timeout` or env `MISE_FETCH_REMOTE_VERSIONS_TIMEOUT`).; retrying in 2.691130544s
mise ░░░░░░░░░░░░░░░░ 0/1 · 58.6s
  dotenvx@2.24.1  installing  58.6s
mise ✓ dotenvx@2.24.1  60.3s  dotenvx-2.24.1-darwin-arm64.tar.gz
mise ████████████████ 1/1 · installed 1 tool in 60.3s

Upgraded 1 tool:
  dotenvx 2.23.0 → 2.24.1
Skipping mise upgrade for fd: newer releases lack a macOS x64 asset.
mise by @jdx – resolving 33 tools
mise ✓ rust                           2ms
mise ✓ node                           2ms
mise ✓ chezmoi                        2ms
mise ✓ cargo:eza                      2ms
mise ✓ age                            2ms
mise ✓ cmake                          2ms
mise ✓ dotenvx                        2ms
mise ✓ bun                            2ms
mise ✓ python                         2ms
mise ✓ fd                             2ms
mise ✓ jq                             2ms
mise ✓ shellcheck                     2ms
mise ✓ uv                             2ms
mise ✓ aqua:micro-editor/micro        3ms
mise ✓ yazi                           3ms
mise ✓ hugo-extended                  3ms
mise ✓ shfmt                          3ms
mise ✓ github:mikefarah/yq            3ms
mise ✓ npm:@anthropic-ai/claude-code  3ms
mise ✓ npm:bash-language-server       3ms
mise ✓ npm:@openai/codex              3ms
mise ✓ npm:fast-cli                   3ms
mise ✓ npm:ccstatusline               3ms
mise ✓ npm:ccusage                    3ms
mise ✓ npm:pyright                    3ms
mise ✓ github:shuntaka9576/blocc      3ms
mise ✓ github:x-motemen/ghq           3ms
mise ✓ github:d-kuro/gwq              3ms
mise ✓ cargo:pueue                    3ms
mise ✓ http:bats                      4ms
mise ✓ github:cli/cli                 4ms
mise ✓ http:gcloud                    4ms
mise ✓ github:ogulcancelik/herdr      4ms
mise ████████████████ 33/33 · resolved 33 tools in 4ms
mise by @jdx – resolving 1 tool
mise ✓ github:cli/cli@2.100.0  2.0s
mise ████████████████ 1/1 · resolved 1 tool in 2.0s
mise WARN  newer github:cli/cli release 2.101.0 (released 2026-09-15, eligible 2026-09-22 23:24 JST) ignored by minimum_release_age (7d); latest eligible release is 2.100.0
mise All tools are up to date
mise by @jdx – resolving 33 tools
mise ✓ rust                           3ms
mise ✓ python                         3ms
mise ✓ dotenvx                        3ms
mise ✓ cmake                          3ms
mise ✓ node                           3ms
mise ✓ age                            3ms
mise ✓ chezmoi                        3ms
mise ✓ cargo:eza                      3ms
mise ✓ bun                            3ms
mise ✓ fd                             3ms
mise ✓ hugo-extended                  3ms
mise ✓ shellcheck                     4ms
mise ✓ jq                             4ms
mise ✓ aqua:micro-editor/micro        4ms
mise ✓ github:mikefarah/yq            4ms
mise ✓ uv                             4ms
mise ✓ yazi                           4ms
mise ✓ npm:bash-language-server       4ms
mise ✓ npm:@anthropic-ai/claude-code  4ms
mise ✓ shfmt                          4ms
mise ✓ npm:@openai/codex              4ms
mise ✓ npm:ccstatusline               4ms
mise ✓ npm:fast-cli                   4ms
mise ✓ npm:pyright                    4ms
mise ✓ github:x-motemen/ghq           4ms
mise ✓ github:shuntaka9576/blocc      4ms
mise ✓ npm:ccusage                    4ms
mise ✓ github:d-kuro/gwq              5ms
mise ✓ github:ogulcancelik/herdr      5ms
mise ✓ github:cli/cli                 5ms
mise ✓ cargo:pueue                    5ms
mise ✓ http:bats                      5ms
mise ✓ http:gcloud                    5ms
mise ████████████████ 33/33 · resolved 33 tools in 5ms
mise by @jdx – resolving 1 tool
mise ✓ github:d-kuro/gwq@0.1.1  759ms
mise ████████████████ 1/1 · resolved 1 tool in 760ms
mise All tools are up to date
mise by @jdx – resolving 33 tools
mise ✓ rust                           3ms
mise ✓ age                            3ms
mise ✓ cmake                          3ms
mise ✓ bun                            3ms
mise ✓ cargo:eza                      3ms
mise ✓ python                         3ms
mise ✓ node                           3ms
mise ✓ dotenvx                        3ms
mise ✓ chezmoi                        3ms
mise ✓ fd                             3ms
mise ✓ jq                             3ms
mise ✓ shellcheck                     3ms
mise ✓ yazi                           3ms
mise ✓ hugo-extended                  3ms
mise ✓ aqua:micro-editor/micro        3ms
mise ✓ uv                             4ms
mise ✓ github:mikefarah/yq            4ms
mise ✓ npm:bash-language-server       4ms
mise ✓ shfmt                          4ms
mise ✓ npm:@openai/codex              4ms
mise ✓ npm:@anthropic-ai/claude-code  4ms
mise ✓ npm:ccusage                    4ms
mise ✓ github:shuntaka9576/blocc      4ms
mise ✓ npm:ccstatusline               4ms
mise ✓ npm:fast-cli                   4ms
mise ✓ github:x-motemen/ghq           4ms
mise ✓ npm:pyright                    4ms
mise ✓ cargo:pueue                    4ms
mise ✓ github:ogulcancelik/herdr      5ms
mise ✓ github:d-kuro/gwq              5ms
mise ✓ github:cli/cli                 5ms
mise ✓ http:gcloud                    5ms
mise ✓ http:bats                      5ms
mise ████████████████ 33/33 · resolved 33 tools in 5ms
mise by @jdx – resolving 1 tool
mise ✓ github:mikefarah/yq@4.53.6  392ms
mise ████████████████ 1/1 · resolved 1 tool in 393ms
mise All tools are up to date
mise by @jdx – resolving 33 tools
mise ✓ rust                           3ms
mise ✓ chezmoi                        3ms
mise ✓ python                         3ms
mise ✓ node                           3ms
mise ✓ cmake                          3ms
mise ✓ age                            3ms
mise ✓ dotenvx                        3ms
mise ✓ cargo:eza                      3ms
mise ✓ bun                            3ms
mise ✓ shellcheck                     4ms
mise ✓ jq                             4ms
mise ✓ yazi                           4ms
mise ✓ fd                             4ms
mise ✓ hugo-extended                  4ms
mise ✓ uv                             4ms
mise ✓ github:mikefarah/yq            4ms
mise ✓ npm:bash-language-server       4ms
mise ✓ shfmt                          4ms
mise ✓ npm:@anthropic-ai/claude-code  4ms
mise ✓ npm:@openai/codex              4ms
mise ✓ aqua:micro-editor/micro        4ms
mise ✓ npm:ccstatusline               5ms
mise ✓ npm:pyright                    5ms
mise ✓ npm:ccusage                    5ms
mise ✓ github:shuntaka9576/blocc      5ms
mise ✓ github:x-motemen/ghq           5ms
mise ✓ npm:fast-cli                   5ms
mise ✓ cargo:pueue                    5ms
mise ✓ github:d-kuro/gwq              5ms
mise ✓ github:cli/cli                 5ms
mise ✓ http:bats                      5ms
mise ✓ github:ogulcancelik/herdr      5ms
mise ✓ http:gcloud                    5ms
mise ████████████████ 33/33 · resolved 33 tools in 5ms
mise by @jdx – resolving 1 tool
mise ✓ github:ogulcancelik/herdr@0.9.0  583ms
mise ████████████████ 1/1 · resolved 1 tool in 583ms
mise WARN  newer github:ogulcancelik/herdr release 0.9.1 (released 2026-09-17, eligible 2026-09-24 03:40 JST) ignored by minimum_release_age (7d); latest eligible release is 0.9.0
mise All tools are up to date
mise by @jdx – resolving 33 tools
mise ✓ rust                           3ms
mise ✓ cmake                          3ms
mise ✓ age                            3ms
mise ✓ node                           3ms
mise ✓ python                         3ms
mise ✓ bun                            3ms
mise ✓ cargo:eza                      3ms
mise ✓ chezmoi                        3ms
mise ✓ dotenvx                        3ms
mise ✓ shellcheck                     4ms
mise ✓ jq                             4ms
mise ✓ hugo-extended                  4ms
mise ✓ uv                             4ms
mise ✓ fd                             4ms
mise ✓ aqua:micro-editor/micro        4ms
mise ✓ yazi                           4ms
mise ✓ github:mikefarah/yq            4ms
mise ✓ npm:bash-language-server       4ms
mise ✓ npm:@anthropic-ai/claude-code  4ms
mise ✓ shfmt                          4ms
mise ✓ npm:@openai/codex              4ms
mise ✓ npm:ccstatusline               5ms
mise ✓ npm:ccusage                    5ms
mise ✓ npm:fast-cli                   5ms
mise ✓ npm:pyright                    5ms
mise ✓ github:x-motemen/ghq           5ms
mise ✓ github:shuntaka9576/blocc      5ms
mise ✓ github:d-kuro/gwq              5ms
mise ✓ cargo:pueue                    5ms
mise ✓ github:cli/cli                 5ms
mise ✓ github:ogulcancelik/herdr      5ms
mise ✓ http:gcloud                    5ms
mise ✓ http:bats                      5ms
mise ████████████████ 33/33 · resolved 33 tools in 5ms
mise by @jdx – resolving 1 tool
mise ✓ github:x-motemen/ghq@1.10.1  350ms
mise ████████████████ 1/1 · resolved 1 tool in 350ms
mise All tools are up to date
Skipping mise upgrade for pinned HTTP tool: http:bats.
Skipping mise upgrade for pinned HTTP tool: http:gcloud.
mise by @jdx – resolving 33 tools
mise ✓ rust                           3ms
mise ✓ dotenvx                        3ms
mise ✓ bun                            3ms
mise ✓ python                         3ms
mise ✓ node                           3ms
mise ✓ age                            3ms
mise ✓ chezmoi                        3ms
mise ✓ cargo:eza                      3ms
mise ✓ cmake                          3ms
mise ✓ shellcheck                     3ms
mise ✓ fd                             3ms
mise ✓ jq                             3ms
mise ✓ uv                             3ms
mise ✓ hugo-extended                  3ms
mise ✓ yazi                           4ms
mise ✓ aqua:micro-editor/micro        4ms
mise ✓ github:mikefarah/yq            4ms
mise ✓ npm:bash-language-server       4ms
mise ✓ shfmt                          4ms
mise ✓ npm:@openai/codex              4ms
mise ✓ npm:@anthropic-ai/claude-code  4ms
mise ✓ npm:ccusage                    4ms
mise ✓ npm:fast-cli                   4ms
mise ✓ npm:ccstatusline               4ms
mise ✓ github:x-motemen/ghq           4ms
mise ✓ npm:pyright                    4ms
mise ✓ github:shuntaka9576/blocc      5ms
mise ✓ github:d-kuro/gwq              5ms
mise ✓ cargo:pueue                    5ms
mise ✓ github:ogulcancelik/herdr      5ms
mise ✓ github:cli/cli                 5ms
mise ✓ http:gcloud                    5ms
mise ✓ http:bats                      5ms
mise ████████████████ 33/33 · resolved 33 tools in 5ms
mise by @jdx – resolving 1 tool
mise ✓ aqua:gohugoio/hugo/hugo-extended@0.166.0  1.0s
mise ████████████████ 1/1 · resolved 1 tool in 1.0s
mise All tools are up to date
mise by @jdx – resolving 33 tools
mise ✓ rust                           3ms
mise ✓ cmake                          4ms
mise ✓ python                         4ms
mise ✓ bun                            4ms
mise ✓ dotenvx                        4ms
mise ✓ age                            4ms
mise ✓ cargo:eza                      4ms
mise ✓ chezmoi                        4ms
mise ✓ node                           4ms
mise ✓ shellcheck                     4ms
mise ✓ fd                             4ms
mise ✓ uv                             4ms
mise ✓ jq                             4ms
mise ✓ aqua:micro-editor/micro        4ms
mise ✓ yazi                           4ms
mise ✓ github:mikefarah/yq            4ms
mise ✓ hugo-extended                  4ms
mise ✓ shfmt                          5ms
mise ✓ npm:@anthropic-ai/claude-code  5ms
mise ✓ npm:@openai/codex              5ms
mise ✓ npm:bash-language-server       5ms
mise ✓ npm:fast-cli                   5ms
mise ✓ npm:pyright                    5ms
mise ✓ npm:ccstatusline               5ms
mise ✓ npm:ccusage                    5ms
mise ✓ github:x-motemen/ghq           5ms
mise ✓ cargo:pueue                    5ms
mise ✓ github:d-kuro/gwq              5ms
mise ✓ github:shuntaka9576/blocc      5ms
mise ✓ github:ogulcancelik/herdr      5ms
mise ✓ http:gcloud                    5ms
mise ✓ github:cli/cli                 5ms
mise ✓ http:bats                      5ms
mise ████████████████ 33/33 · resolved 33 tools in 6ms
mise by @jdx – resolving 1 tool
mise ✓ aqua:jqlang/jq@1.8.2  359ms
mise ████████████████ 1/1 · resolved 1 tool in 359ms
mise All tools are up to date
mise by @jdx – resolving 33 tools
mise ✓ rust                           2ms
mise ✓ cmake                          2ms
mise ✓ node                           2ms
mise ✓ age                            2ms
mise ✓ python                         2ms
mise ✓ bun                            3ms
mise ✓ chezmoi                        3ms
mise ✓ cargo:eza                      3ms
mise ✓ dotenvx                        3ms
mise ✓ fd                             3ms
mise ✓ jq                             3ms
mise ✓ yazi                           3ms
mise ✓ aqua:micro-editor/micro        3ms
mise ✓ hugo-extended                  3ms
mise ✓ github:mikefarah/yq            3ms
mise ✓ shfmt                          3ms
mise ✓ uv                             3ms
mise ✓ shellcheck                     3ms
mise ✓ npm:@anthropic-ai/claude-code  3ms
mise ✓ npm:bash-language-server       3ms
mise ✓ npm:fast-cli                   4ms
mise ✓ npm:pyright                    4ms
mise ✓ npm:ccstatusline               4ms
mise ✓ npm:ccusage                    4ms
mise ✓ npm:@openai/codex              4ms
mise ✓ github:shuntaka9576/blocc      4ms
mise ✓ github:d-kuro/gwq              4ms
mise ✓ github:cli/cli                 4ms
mise ✓ github:x-motemen/ghq           4ms
mise ✓ cargo:pueue                    4ms
mise ✓ http:bats                      4ms
mise ✓ http:gcloud                    4ms
mise ✓ github:ogulcancelik/herdr      4ms
mise ████████████████ 33/33 · resolved 33 tools in 4ms
mise by @jdx – resolving 1 tool
mise ✓ core:node@26.8.2  2ms
mise ████████████████ 1/1 · resolved 1 tool in 2ms
mise WARN  newer node release 26.9.0 (released 2026-09-16, eligible 2026-09-23 09:00 JST) ignored by minimum_release_age (7d); latest eligible release is 26.8.2
mise All tools are up to date
mise by @jdx – resolving 33 tools
mise ✓ rust                           2ms
mise ✓ dotenvx                        2ms
mise ✓ chezmoi                        2ms
mise ✓ cmake                          2ms
mise ✓ bun                            2ms
mise ✓ node                           2ms
mise ✓ age                            2ms
mise ✓ python                         3ms
mise ✓ cargo:eza                      3ms
mise ✓ uv                             3ms
mise ✓ hugo-extended                  3ms
mise ✓ jq                             3ms
mise ✓ fd                             3ms
mise ✓ github:mikefarah/yq            3ms
mise ✓ aqua:micro-editor/micro        3ms
mise ✓ yazi                           3ms
mise ✓ shellcheck                     3ms
mise ✓ shfmt                          3ms
mise ✓ npm:@anthropic-ai/claude-code  3ms
mise ✓ npm:@openai/codex              3ms
mise ✓ npm:bash-language-server       4ms
mise ✓ npm:ccusage                    4ms
mise ✓ npm:fast-cli                   4ms
mise ✓ npm:ccstatusline               4ms
mise ✓ npm:pyright                    4ms
mise ✓ github:shuntaka9576/blocc      4ms
mise ✓ github:x-motemen/ghq           4ms
mise ✓ github:cli/cli                 4ms
mise ✓ github:d-kuro/gwq              4ms
mise ✓ cargo:pueue                    4ms
mise ✓ github:ogulcancelik/herdr      4ms
mise ✓ http:bats                      4ms
mise ✓ http:gcloud                    4ms
mise ████████████████ 33/33 · resolved 33 tools in 4ms
mise by @jdx – resolving 1 tool
mise ✓ npm:@anthropic-ai/claude-code@2.1.275  197ms
mise ████████████████ 1/1 · resolved 1 tool in 197ms
mise WARN  newer npm:@anthropic-ai/claude-code release 2.1.278 (released 2026-09-19, eligible 2026-09-26 10:48 JST) ignored by minimum_release_age (7d); latest eligible release is 2.1.271
mise All tools are up to date
mise by @jdx – resolving 33 tools
mise ✓ rust                           2ms
mise ✓ dotenvx                        2ms
mise ✓ cmake                          2ms
mise ✓ chezmoi                        2ms
mise ✓ python                         2ms
mise ✓ bun                            2ms
mise ✓ node                           2ms
mise ✓ age                            2ms
mise ✓ fd                             3ms
mise ✓ jq                             3ms
mise ✓ hugo-extended                  3ms
mise ✓ yazi                           3ms
mise ✓ cargo:eza                      3ms
mise ✓ uv                             3ms
mise ✓ shellcheck                     3ms
mise ✓ aqua:micro-editor/micro        3ms
mise ✓ shfmt                          3ms
mise ✓ npm:bash-language-server       3ms
mise ✓ github:mikefarah/yq            3ms
mise ✓ npm:@anthropic-ai/claude-code  3ms
mise ✓ npm:ccstatusline               3ms
mise ✓ npm:@openai/codex              3ms
mise ✓ npm:fast-cli                   3ms
mise ✓ npm:ccusage                    4ms
mise ✓ github:shuntaka9576/blocc      4ms
mise ✓ npm:pyright                    4ms
mise ✓ cargo:pueue                    4ms
mise ✓ github:d-kuro/gwq              4ms
mise ✓ github:x-motemen/ghq           4ms
mise ✓ github:cli/cli                 4ms
mise ✓ http:gcloud                    4ms
mise ✓ http:bats                      4ms
mise ✓ github:ogulcancelik/herdr      4ms
mise ████████████████ 33/33 · resolved 33 tools in 4ms
mise by @jdx – resolving 1 tool
mise ✓ npm:@openai/codex@0.154.0  378ms
mise ████████████████ 1/1 · resolved 1 tool in 378ms
mise WARN  newer npm:@openai/codex release 0.155.1 (released 2026-09-19, eligible 2026-09-26 05:09 JST) ignored by minimum_release_age (7d); latest eligible release is 0.154.0
mise All tools are up to date
mise by @jdx – resolving 33 tools
mise ✓ rust                           3ms
mise ✓ dotenvx                        3ms
mise ✓ node                           3ms
mise ✓ bun                            3ms
mise ✓ age                            3ms
mise ✓ python                         3ms
mise ✓ chezmoi                        3ms
mise ✓ cmake                          3ms
mise ✓ cargo:eza                      3ms
mise ✓ jq                             3ms
mise ✓ yazi                           3ms
mise ✓ fd                             3ms
mise ✓ aqua:micro-editor/micro        4ms
mise ✓ hugo-extended                  4ms
mise ✓ uv                             4ms
mise ✓ shellcheck                     4ms
mise ✓ github:mikefarah/yq            4ms
mise ✓ npm:@anthropic-ai/claude-code  4ms
mise ✓ npm:bash-language-server       4ms
mise ✓ npm:@openai/codex              4ms
mise ✓ npm:pyright                    4ms
mise ✓ shfmt                          4ms
mise ✓ npm:ccstatusline               4ms
mise ✓ npm:fast-cli                   4ms
mise ✓ npm:ccusage                    4ms
mise ✓ github:shuntaka9576/blocc      5ms
mise ✓ cargo:pueue                    5ms
mise ✓ github:d-kuro/gwq              5ms
mise ✓ github:ogulcancelik/herdr      5ms
mise ✓ github:x-motemen/ghq           5ms
mise ✓ github:cli/cli                 5ms
mise ✓ http:bats                      5ms
mise ✓ http:gcloud                    5ms
mise ████████████████ 33/33 · resolved 33 tools in 5ms
mise by @jdx – resolving 1 tool
mise ✓ npm:bash-language-server@5.6.0  223ms
mise ████████████████ 1/1 · resolved 1 tool in 223ms
mise WARN  newer npm:bash-language-server release 5.8.1 (released 2026-09-20, eligible 2026-09-27 05:44 JST) ignored by minimum_release_age (7d); latest eligible release is 5.6.0
mise All tools are up to date
mise by @jdx – resolving 33 tools
mise ✓ rust                           2ms
mise ✓ dotenvx                        2ms
mise ✓ bun                            3ms
mise ✓ age                            3ms
mise ✓ cargo:eza                      3ms
mise ✓ cmake                          3ms
mise ✓ python                         3ms
mise ✓ chezmoi                        3ms
mise ✓ node                           3ms
mise ✓ fd                             3ms
mise ✓ hugo-extended                  3ms
mise ✓ uv                             3ms
mise ✓ yazi                           3ms
mise ✓ aqua:micro-editor/micro        3ms
mise ✓ shellcheck                     3ms
mise ✓ jq                             3ms
mise ✓ github:mikefarah/yq            3ms
mise ✓ shfmt                          3ms
mise ✓ npm:bash-language-server       3ms
mise ✓ npm:@anthropic-ai/claude-code  3ms
mise ✓ npm:@openai/codex              3ms
mise ✓ npm:ccusage                    4ms
mise ✓ npm:ccstatusline               4ms
mise ✓ github:x-motemen/ghq           4ms
mise ✓ npm:fast-cli                   4ms
mise ✓ github:cli/cli                 4ms
mise ✓ github:shuntaka9576/blocc      4ms
mise ✓ npm:pyright                    4ms
mise ✓ github:d-kuro/gwq              4ms
mise ✓ cargo:pueue                    4ms
mise ✓ github:ogulcancelik/herdr      4ms
mise ✓ http:bats                      4ms
mise ✓ http:gcloud                    4ms
mise ████████████████ 33/33 · resolved 33 tools in 4ms
mise by @jdx – resolving 1 tool
mise ✓ npm:ccstatusline@2.2.29  135ms
mise ████████████████ 1/1 · resolved 1 tool in 135ms
mise WARN  newer npm:ccstatusline release 2.2.30 (released 2026-09-18, eligible 2026-09-25 02:42 JST) ignored by minimum_release_age (7d); latest eligible release is 2.2.29
mise All tools are up to date
mise by @jdx – resolving 33 tools
mise ✓ rust                           2ms
mise ✓ cargo:eza                      2ms
mise ✓ node                           2ms
mise ✓ cmake                          2ms
mise ✓ dotenvx                        2ms
mise ✓ python                         2ms
mise ✓ chezmoi                        2ms
mise ✓ bun                            2ms
mise ✓ age                            2ms
mise ✓ jq                             3ms
mise ✓ fd                             3ms
mise ✓ uv                             3ms
mise ✓ aqua:micro-editor/micro        3ms
mise ✓ yazi                           3ms
mise ✓ hugo-extended                  3ms
mise ✓ shellcheck                     3ms
mise ✓ github:mikefarah/yq            3ms
mise ✓ shfmt                          3ms
mise ✓ npm:@anthropic-ai/claude-code  3ms
mise ✓ npm:bash-language-server       3ms
mise ✓ npm:@openai/codex              3ms
mise ✓ npm:pyright                    3ms
mise ✓ npm:ccstatusline               3ms
mise ✓ github:x-motemen/ghq           4ms
mise ✓ npm:fast-cli                   4ms
mise ✓ npm:ccusage                    4ms
mise ✓ github:shuntaka9576/blocc      4ms
mise ✓ github:d-kuro/gwq              4ms
mise ✓ cargo:pueue                    4ms
mise ✓ github:cli/cli                 4ms
mise ✓ github:ogulcancelik/herdr      4ms
mise ✓ http:gcloud                    4ms
mise ✓ http:bats                      4ms
mise ████████████████ 33/33 · resolved 33 tools in 4ms
mise by @jdx – resolving 1 tool
mise ✓ npm:ccusage@20.0.20  239ms
mise ████████████████ 1/1 · resolved 1 tool in 239ms
mise WARN  newer npm:ccusage release 20.0.24 (released 2026-09-21, eligible 2026-09-28 20:28 JST) ignored by minimum_release_age (7d); latest eligible release is 20.0.20
mise All tools are up to date
mise by @jdx – resolving 33 tools
mise ✓ rust                           3ms
mise ✓ age                            3ms
mise ✓ python                         3ms
mise ✓ chezmoi                        3ms
mise ✓ cmake                          3ms
mise ✓ dotenvx                        3ms
mise ✓ node                           3ms
mise ✓ bun                            3ms
mise ✓ cargo:eza                      3ms
mise ✓ shellcheck                     3ms
mise ✓ jq                             3ms
mise ✓ fd                             3ms
mise ✓ hugo-extended                  3ms
mise ✓ yazi                           4ms
mise ✓ github:mikefarah/yq            4ms
mise ✓ aqua:micro-editor/micro        4ms
mise ✓ uv                             4ms
mise ✓ shfmt                          4ms
mise ✓ npm:@anthropic-ai/claude-code  4ms
mise ✓ npm:@openai/codex              4ms
mise ✓ npm:bash-language-server       4ms
mise ✓ github:x-motemen/ghq           4ms
mise ✓ npm:ccstatusline               4ms
mise ✓ npm:ccusage                    4ms
mise ✓ npm:pyright                    4ms
mise ✓ npm:fast-cli                   4ms
mise ✓ github:shuntaka9576/blocc      4ms
mise ✓ github:d-kuro/gwq              4ms
mise ✓ github:cli/cli                 4ms
mise ✓ github:ogulcancelik/herdr      5ms
mise ✓ cargo:pueue                    5ms
mise ✓ http:gcloud                    5ms
mise ✓ http:bats                      5ms
mise ████████████████ 33/33 · resolved 33 tools in 5ms
mise by @jdx – resolving 1 tool
mise ✓ npm:fast-cli@5.2.0  234ms
mise ████████████████ 1/1 · resolved 1 tool in 234ms
mise All tools are up to date
mise by @jdx – resolving 33 tools
mise ✓ rust                           3ms
mise ✓ chezmoi                        3ms
mise ✓ node                           3ms
mise ✓ dotenvx                        3ms
mise ✓ cmake                          3ms
mise ✓ python                         3ms
mise ✓ cargo:eza                      3ms
mise ✓ bun                            3ms
mise ✓ age                            3ms
mise ✓ fd                             3ms
mise ✓ jq                             3ms
mise ✓ uv                             3ms
mise ✓ aqua:micro-editor/micro        3ms
mise ✓ yazi                           4ms
mise ✓ shellcheck                     4ms
mise ✓ github:mikefarah/yq            4ms
mise ✓ hugo-extended                  4ms
mise ✓ npm:bash-language-server       4ms
mise ✓ shfmt                          4ms
mise ✓ npm:ccusage                    4ms
mise ✓ npm:ccstatusline               4ms
mise ✓ npm:pyright                    4ms
mise ✓ github:x-motemen/ghq           4ms
mise ✓ npm:@anthropic-ai/claude-code  4ms
mise ✓ npm:@openai/codex              4ms
mise ✓ npm:fast-cli                   4ms
mise ✓ github:d-kuro/gwq              4ms
mise ✓ github:shuntaka9576/blocc      4ms
mise ✓ cargo:pueue                    5ms
mise ✓ github:ogulcancelik/herdr      5ms
mise ✓ github:cli/cli                 5ms
mise ✓ http:bats                      5ms
mise ✓ http:gcloud                    5ms
mise ████████████████ 33/33 · resolved 33 tools in 5ms
mise by @jdx – resolving 1 tool
mise ✓ npm:pyright@1.1.414  283ms
mise ████████████████ 1/1 · resolved 1 tool in 283ms
mise All tools are up to date
mise by @jdx – resolving 33 tools
mise ✓ rust                           3ms
mise ✓ node                           3ms
mise ✓ cmake                          3ms
mise ✓ dotenvx                        3ms
mise ✓ bun                            3ms
mise ✓ chezmoi                        3ms
mise ✓ age                            3ms
mise ✓ python                         3ms
mise ✓ cargo:eza                      3ms
mise ✓ fd                             3ms
mise ✓ yazi                           3ms
mise ✓ shellcheck                     3ms
mise ✓ github:mikefarah/yq            3ms
mise ✓ aqua:micro-editor/micro        3ms
mise ✓ uv                             3ms
mise ✓ jq                             3ms
mise ✓ hugo-extended                  3ms
mise ✓ npm:bash-language-server       4ms
mise ✓ npm:ccstatusline               4ms
mise ✓ npm:fast-cli                   4ms
mise ✓ shfmt                          4ms
mise ✓ npm:@openai/codex              4ms
mise ✓ npm:@anthropic-ai/claude-code  4ms
mise ✓ npm:ccusage                    4ms
mise ✓ npm:pyright                    4ms
mise ✓ github:x-motemen/ghq           4ms
mise ✓ github:d-kuro/gwq              4ms
mise ✓ github:cli/cli                 4ms
mise ✓ github:shuntaka9576/blocc      4ms
mise ✓ github:ogulcancelik/herdr      4ms
mise ✓ cargo:pueue                    4ms
mise ✓ http:bats                      4ms
mise ✓ http:gcloud                    4ms
mise ████████████████ 33/33 · resolved 33 tools in 5ms
mise by @jdx – resolving 1 tool
mise ✓ core:python@3.14.7  2ms
mise ████████████████ 1/1 · resolved 1 tool in 2ms
mise All tools are up to date
mise by @jdx – resolving 33 tools
mise ✓ rust                           2ms
mise ✓ chezmoi                        2ms
mise ✓ node                           2ms
mise ✓ dotenvx                        2ms
mise ✓ cmake                          2ms
mise ✓ age                            2ms
mise ✓ bun                            3ms
mise ✓ python                         3ms
mise ✓ cargo:eza                      3ms
mise ✓ fd                             3ms
mise ✓ jq                             3ms
mise ✓ uv                             3ms
mise ✓ yazi                           3ms
mise ✓ aqua:micro-editor/micro        3ms
mise ✓ github:mikefarah/yq            3ms
mise ✓ hugo-extended                  3ms
mise ✓ shellcheck                     3ms
mise ✓ shfmt                          3ms
mise ✓ npm:bash-language-server       3ms
mise ✓ npm:@anthropic-ai/claude-code  3ms
mise ✓ npm:@openai/codex              3ms
mise ✓ npm:fast-cli                   3ms
mise ✓ npm:ccusage                    4ms
mise ✓ github:x-motemen/ghq           4ms
mise ✓ npm:pyright                    4ms
mise ✓ github:shuntaka9576/blocc      4ms
mise ✓ github:d-kuro/gwq              4ms
mise ✓ npm:ccstatusline               4ms
mise ✓ cargo:pueue                    4ms
mise ✓ github:ogulcancelik/herdr      4ms
mise ✓ http:bats                      4ms
mise ✓ github:cli/cli                 4ms
mise ✓ http:gcloud                    4ms
mise ████████████████ 33/33 · resolved 33 tools in 4ms
mise by @jdx – resolving 1 tool
mise ✓ core:rust@1.98.1  1ms
mise ████████████████ 1/1 · resolved 1 tool in 1ms
mise All tools are up to date
mise by @jdx – resolving 33 tools
mise ✓ rust                           2ms
mise ✓ node                           2ms
mise ✓ dotenvx                        2ms
mise ✓ chezmoi                        2ms
mise ✓ age                            2ms
mise ✓ cmake                          2ms
mise ✓ python                         2ms
mise ✓ bun                            2ms
mise ✓ cargo:eza                      2ms
mise ✓ fd                             3ms
mise ✓ jq                             3ms
mise ✓ hugo-extended                  3ms
mise ✓ shellcheck                     3ms
mise ✓ uv                             3ms
mise ✓ github:mikefarah/yq            3ms
mise ✓ npm:bash-language-server       3ms
mise ✓ shfmt                          3ms
mise ✓ yazi                           3ms
mise ✓ npm:@anthropic-ai/claude-code  3ms
mise ✓ aqua:micro-editor/micro        3ms
mise ✓ npm:@openai/codex              3ms
mise ✓ github:x-motemen/ghq           3ms
mise ✓ npm:ccusage                    3ms
mise ✓ npm:fast-cli                   3ms
mise ✓ npm:ccstatusline               3ms
mise ✓ npm:pyright                    4ms
mise ✓ github:d-kuro/gwq              4ms
mise ✓ github:ogulcancelik/herdr      4ms
mise ✓ cargo:pueue                    4ms
mise ✓ github:cli/cli                 4ms
mise ✓ github:shuntaka9576/blocc      4ms
mise ✓ http:gcloud                    4ms
mise ✓ http:bats                      4ms
mise ████████████████ 33/33 · resolved 33 tools in 4ms
mise by @jdx – resolving 1 tool
mise ✓ aqua:koalaman/shellcheck@0.11.0  378ms
mise ████████████████ 1/1 · resolved 1 tool in 378ms
mise All tools are up to date
mise by @jdx – resolving 33 tools
mise ✓ rust                           3ms
mise ✓ chezmoi                        3ms
mise ✓ python                         3ms
mise ✓ bun                            3ms
mise ✓ dotenvx                        3ms
mise ✓ age                            3ms
mise ✓ cmake                          3ms
mise ✓ cargo:eza                      3ms
mise ✓ node                           3ms
mise ✓ fd                             3ms
mise ✓ shellcheck                     3ms
mise ✓ hugo-extended                  4ms
mise ✓ jq                             4ms
mise ✓ uv                             4ms
mise ✓ aqua:micro-editor/micro        4ms
mise ✓ yazi                           4ms
mise ✓ github:mikefarah/yq            4ms
mise ✓ npm:bash-language-server       4ms
mise ✓ npm:@anthropic-ai/claude-code  4ms
mise ✓ npm:@openai/codex              4ms
mise ✓ npm:fast-cli                   4ms
mise ✓ shfmt                          4ms
mise ✓ npm:ccstatusline               4ms
mise ✓ npm:pyright                    4ms
mise ✓ npm:ccusage                    4ms
mise ✓ github:x-motemen/ghq           4ms
mise ✓ github:d-kuro/gwq              5ms
mise ✓ github:shuntaka9576/blocc      5ms
mise ✓ cargo:pueue                    5ms
mise ✓ github:ogulcancelik/herdr      5ms
mise ✓ http:bats                      5ms
mise ✓ github:cli/cli                 5ms
mise ✓ http:gcloud                    5ms
mise ████████████████ 33/33 · resolved 33 tools in 5ms
mise by @jdx – resolving 1 tool
mise ✓ aqua:mvdan/sh@3.14.1  374ms
mise ████████████████ 1/1 · resolved 1 tool in 374ms
mise All tools are up to date
mise by @jdx – resolving 33 tools
mise ✓ rust                           3ms
mise ✓ dotenvx                        3ms
mise ✓ cmake                          3ms
mise ✓ bun                            3ms
mise ✓ chezmoi                        3ms
mise ✓ age                            3ms
mise ✓ node                           3ms
mise ✓ python                         3ms
mise ✓ cargo:eza                      3ms
mise ✓ shellcheck                     4ms
mise ✓ hugo-extended                  4ms
mise ✓ fd                             4ms
mise ✓ yazi                           4ms
mise ✓ jq                             4ms
mise ✓ github:mikefarah/yq            4ms
mise ✓ aqua:micro-editor/micro        4ms
mise ✓ uv                             4ms
mise ✓ npm:bash-language-server       4ms
mise ✓ shfmt                          4ms
mise ✓ npm:@openai/codex              4ms
mise ✓ npm:fast-cli                   4ms
mise ✓ npm:pyright                    4ms
mise ✓ npm:ccusage                    4ms
mise ✓ npm:ccstatusline               5ms
mise ✓ npm:@anthropic-ai/claude-code  5ms
mise ✓ github:shuntaka9576/blocc      5ms
mise ✓ github:x-motemen/ghq           5ms
mise ✓ github:d-kuro/gwq              5ms
mise ✓ github:ogulcancelik/herdr      5ms
mise ✓ cargo:pueue                    5ms
mise ✓ http:gcloud                    5ms
mise ✓ github:cli/cli                 5ms
mise ✓ http:bats                      5ms
mise ████████████████ 33/33 · resolved 33 tools in 5ms
mise by @jdx – resolving 1 tool
mise ✓ aqua:astral-sh/uv@0.12.13  354ms
mise ████████████████ 1/1 · resolved 1 tool in 354ms
mise WARN  newer uv release 0.12.17 (released 2026-09-19, eligible 2026-09-26 03:59 JST) ignored by minimum_release_age (7d); latest eligible release is 0.12.13
mise All tools are up to date
mise by @jdx – resolving 33 tools
mise ✓ rust                           3ms
mise ✓ dotenvx                        3ms
mise ✓ node                           3ms
mise ✓ cmake                          3ms
mise ✓ age                            3ms
mise ✓ chezmoi                        3ms
mise ✓ bun                            3ms
mise ✓ python                         3ms
mise ✓ cargo:eza                      3ms
mise ✓ jq                             3ms
mise ✓ fd                             3ms
mise ✓ hugo-extended                  3ms
mise ✓ github:mikefarah/yq            3ms
mise ✓ uv                             3ms
mise ✓ aqua:micro-editor/micro        4ms
mise ✓ shellcheck                     4ms
mise ✓ npm:bash-language-server       4ms
mise ✓ shfmt                          4ms
mise ✓ yazi                           4ms
mise ✓ npm:@openai/codex              4ms
mise ✓ npm:@anthropic-ai/claude-code  4ms
mise ✓ npm:ccstatusline               4ms
mise ✓ npm:ccusage                    4ms
mise ✓ npm:fast-cli                   4ms
mise ✓ github:shuntaka9576/blocc      4ms
mise ✓ github:x-motemen/ghq           4ms
mise ✓ github:d-kuro/gwq              4ms
mise ✓ cargo:pueue                    4ms
mise ✓ github:cli/cli                 4ms
mise ✓ npm:pyright                    5ms
mise ✓ github:ogulcancelik/herdr      5ms
mise ✓ http:gcloud                    5ms
mise ✓ http:bats                      5ms
mise ████████████████ 33/33 · resolved 33 tools in 5ms
mise by @jdx – resolving 1 tool
mise ✓ aqua:sxyazi/yazi@26.9.1  386ms
mise ████████████████ 1/1 · resolved 1 tool in 386ms
mise All tools are up to date

==> agent CLI tools
mise by @jdx – installing 1 tool
mise ░░░░░░░░░░░░░░░░ 0/1 · 3.0s
  npm:@openai/codex@0.155.1  installing  3.0s
mise npm:@openai/codex@0.155.1 added 2 packages in 4s
mise npm:@openai/codex@0.155.1 Reshimming mise 26.8.2...
mise ✓ npm:@openai/codex@0.155.1  4.2s
mise ████████████████ 1/1 · installed 1 tool in 4.2s
mise ~/.config/mise/config.toml tools: npm:@openai/codex@0.155.1

changed 2 packages in 2s
Reshimming mise 26.8.2...
mise by @jdx – installing 1 tool
mise npm:@anthropic-ai/claude-code@2.1.278 added 2 packages in 2s
mise npm:@anthropic-ai/claude-code@2.1.278 Reshimming mise 26.8.2...
mise ✓ npm:@anthropic-ai/claude-code@2.1.278  2.7s
mise ████████████████ 1/1 · installed 1 tool in 2.7s
mise ~/.config/mise/config.toml tools: npm:@anthropic-ai/claude-code@2.1.278

changed 2 packages in 1s
Reshimming mise 26.8.2...

==> terminal tool pins
Pinned tode v0.3.4, terminal-browser v0.11.1, and crit v0.20.2; review and commit the installer-pins diff.

==> Claude Code plugins
Updating marketplace: claude-plugins-official...✔ Successfully updated marketplace: claude-plugins-official
Checking for updates for plugin "superpowers@claude-plugins-official" at user scope…
✔ superpowers is already at the latest version (6.3.0).

==> Claude Code Crit plugin
Updating marketplace: crit...Refreshing marketplace cache (timeout: 120s)…
Cloning repository (timeout: 120s): git@github.com:tomasz-tomczyk/crit.git
Replacing the existing marketplace clone…
Clone complete, validating marketplace…
✔ Successfully updated marketplace: crit
Checking for updates for plugin "crit@crit" at user scope…
✔ crit is already at the latest version (1.8.10).
Claude Code Crit plugin is already enabled.

==> Claude Code Ponytail plugin
Updating marketplace: ponytail...Refreshing marketplace cache (timeout: 120s)…
✔ Successfully updated marketplace: ponytail
Checking for updates for plugin "ponytail@ponytail" at user scope…
✔ ponytail is already at the latest version (4.10.0).
Claude Code Ponytail plugin is already enabled.
Ponytail default mode is full. Set PONYTAIL_DEFAULT_MODE=lite|full|ultra|off to override.

==> Claude Code Understand-Anything plugin
Updating marketplace: understand-anything...Refreshing marketplace cache (timeout: 120s)…
✔ Successfully updated marketplace: understand-anything
Checking for updates for plugin "understand-anything@understand-anything" at user scope…
✔ understand-anything is already at the latest version (2.9.7).
Claude Code Understand-Anything plugin is already enabled.

==> Codex plugins
Codex Superpowers plugin installed.

==> Codex Crit plugin
  Installed: /Users/mryfmo/.agents/plugins/marketplace.json
  Installed: .agents/skills/crit/SKILL.md
  Installed: .agents/skills/crit-cli/SKILL.md
  Installed: .agents/skills/crit-story/SKILL.md
  Installed: /Users/mryfmo/.codex/plugins/crit/.codex-plugin/plugin.json
  Installed: /Users/mryfmo/.codex/plugins/crit/skills/crit/SKILL.md
  Installed: /Users/mryfmo/.codex/plugins/crit/skills/crit-cli/SKILL.md
  Installed: /Users/mryfmo/.codex/plugins/crit/skills/crit-story/SKILL.md
  Installed: /Users/mryfmo/.codex/plugins/crit/hooks/hooks.json
  Installed: /Users/mryfmo/.codex/plugins/cache/mryfmo-personal-plugins/crit/local
  Skipped:   /Users/mryfmo/.codex/config.toml (Codex plugin already enabled)
  Use $crit in Codex to start a review loop
  The crit-cli skill is available to Codex agents when needed
  Use $crit-story in Codex to author a story and continue the review loop
  The Crit plugin is registered in the local Codex plugin marketplace
  The plugin-packaged crit skill is available to Codex as $crit:crit
  The plugin-packaged crit-cli skill is available to Codex agents when needed
  The plugin-packaged crit-story skill is available to Codex as $crit-story
  The Crit plugin includes a Codex Stop hook for proposed-plan review
  The Crit Codex plugin is enabled as crit@mryfmo-personal-plugins


==> Codex Ponytail plugin
Marketplace `ponytail` is already up to date.
Codex Ponytail plugin is already installed.
Review and trust Ponytail lifecycle hooks in Codex with /hooks, then start a new thread.
Ponytail default mode is full. Set PONYTAIL_DEFAULT_MODE=lite|full|ultra|off to override.

==> Codex Understand-Anything skills
→ Updating existing checkout at /Users/mryfmo/.understand-anything/repo
Already up to date.
→ Linking skills for codex (per-skill → /Users/mryfmo/.agents/skills)
  ✓ /Users/mryfmo/.agents/skills/understand-chat → /Users/mryfmo/.understand-anything/repo/understand-anything-plugin/skills/understand-chat
  ✓ /Users/mryfmo/.agents/skills/understand-dashboard → /Users/mryfmo/.understand-anything/repo/understand-anything-plugin/skills/understand-dashboard
  ✓ /Users/mryfmo/.agents/skills/understand-diff → /Users/mryfmo/.understand-anything/repo/understand-anything-plugin/skills/understand-diff
  ✓ /Users/mryfmo/.agents/skills/understand-domain → /Users/mryfmo/.understand-anything/repo/understand-anything-plugin/skills/understand-domain
  ✓ /Users/mryfmo/.agents/skills/understand-explain → /Users/mryfmo/.understand-anything/repo/understand-anything-plugin/skills/understand-explain
  ✓ /Users/mryfmo/.agents/skills/understand-figma → /Users/mryfmo/.understand-anything/repo/understand-anything-plugin/skills/understand-figma
  ✓ /Users/mryfmo/.agents/skills/understand-knowledge → /Users/mryfmo/.understand-anything/repo/understand-anything-plugin/skills/understand-knowledge
  ✓ /Users/mryfmo/.agents/skills/understand-onboard → /Users/mryfmo/.understand-anything/repo/understand-anything-plugin/skills/understand-onboard
  ✓ /Users/mryfmo/.agents/skills/understand → /Users/mryfmo/.understand-anything/repo/understand-anything-plugin/skills/understand
→ Linking universal plugin root
  • /Users/mryfmo/.understand-anything-plugin already exists, leaving as-is

✓ Installed Understand-Anything for codex
  Restart your CLI or IDE to pick up the skills.

  Tip: Codex invokes skills with $ instead of / — type $understand, not /understand.
Invoke Understand-Anything in Codex with $understand after restarting the CLI.

==> terminal-code (tode)
tode v0.3.4 is already installed.

==> terminal-browser
terminal-browser v0.11.1 is already installed.

==> herdr integrations
installed claude integration hook to /Users/mryfmo/.claude/hooks/herdr-agent-state.sh
ensured claude settings at /Users/mryfmo/.claude/settings.json
installed codex integration hook to /Users/mryfmo/.codex/herdr-agent-state.sh
ensured codex hooks at /Users/mryfmo/.codex/hooks.json
ensured codex config at /Users/mryfmo/.codex/config.toml

==> uv tools
Nothing to upgrade

==> GitHub CLI extensions
[poi]: already up to date

==> Claude Code Router adoption gate
CCR gate G1 (#1115): open
CCR latest release: v3.1.1
CCR gates G2/G3 require manual primary-source verification before any canary.

Upgrade summary: required failures: 1; optional warnings: 0
make: *** [upgrade] Error 1
```

## Successful make upgrade retry (exit 0)

```text
./scripts/upgrade-tools.sh 

==> Homebrew
==> Updating Homebrew...
Updated 2 taps (homebrew/core and homebrew/cask).
==> New Formulae
confluence-markdown-exporter: Export Atlassian Confluence pages as Markdown files
==> New Casks
yap-app: On-device voice dictation
==> Outdated Formulae
aws-c-common
aws-c-s3
awscli
node

You have 4 outdated formulae installed.
You can upgrade them with brew upgrade
or list them with brew outdated.
Skipping forbidden Homebrew formula: node
==> Downloading bottle manifests
✔︎ Bottle Manifest aws-c-common (1.0.1)
✔︎ Bottle Manifest aws-c-s3 (1.1.3)
✔︎ Bottle Manifest awscli (2.36.50)
Warning: `$HOMEBREW_NO_INSTALLED_DEPENDENTS_CHECK` is set: not checking for outdated
dependents or dependents with broken linkage!
==> Fetching downloads for: aws-c-common, aws-c-s3 and awscli
Warning: `$HOMEBREW_NO_INSTALLED_DEPENDENTS_CHECK` is set: not checking for outdated
dependents or dependents with broken linkage!
==> Would upgrade 3 requested outdated packages
aws-c-common  1.0.0   -> 1.0.1 (249.2KB)
aws-c-s3      1.1.2   -> 1.1.3 (132.8KB)
awscli        2.36.49 -> 2.36.50 (23.4MB)
✔︎ Bottle aws-c-s3 (1.1.3)
✔︎ Bottle aws-c-common (1.0.1)
✔︎ Bottle awscli (2.36.50)
==> Upgrading aws-c-common
  1.0.0 -> 1.0.1 
==> Pouring aws-c-common--1.0.1.arm64_tahoe.bottle.tar.gz
🍺  /opt/homebrew/Cellar/aws-c-common/1.0.1: 110 files, 1MB
==> Upgrading aws-c-s3
  1.1.2 -> 1.1.3 
==> Pouring aws-c-s3--1.1.3.arm64_tahoe.bottle.tar.gz
🍺  /opt/homebrew/Cellar/aws-c-s3/1.1.3: 19 files, 436.8KB
==> Upgrading awscli
  2.36.49 -> 2.36.50 
==> Pouring awscli--2.36.50.arm64_tahoe.bottle.tar.gz
🍺  /opt/homebrew/Cellar/awscli/2.36.50: 14,681 files, 162.6MB
==> Cleanup
Removing: /opt/homebrew/Cellar/aws-c-s3/1.1.2... (19 files, 433.8KB)
Removing: /opt/homebrew/Cellar/aws-c-common/1.0.0... (109 files, 1MB)
Removing: /Users/mryfmo/Library/Caches/Homebrew/aws-c-s3--1.1.2... (131.4KB)
Removing: /Users/mryfmo/Library/Caches/Homebrew/aws-c-s3_bottle_manifest--1.1.2... (70KB)
Removing: /opt/homebrew/Cellar/awscli/2.36.49... (14,680 files, 162.5MB)
Removing: /Users/mryfmo/Library/Caches/Homebrew/awscli--2.36.49... (23.4MB)
Removing: /Users/mryfmo/Library/Caches/Homebrew/awscli_bottle_manifest--2.36.49... (138.5KB)
Disable this behaviour by setting `HOMEBREW_NO_INSTALL_CLEANUP=1`.
Hide these hints with `HOMEBREW_NO_ENV_HINTS=1` (see `man brew`).
==> Caveats
zsh completions and functions have been installed to:
  /opt/homebrew/share/zsh/site-functions
==> awscli
The "examples" directory has been installed to:
  /opt/homebrew/share/awscli/examples
==> Upgraded 3 requested outdated packages
aws-c-common  1.0.0   -> 1.0.1
aws-c-s3      1.1.2   -> 1.1.3
awscli        2.36.49 -> 2.36.50
No outdated Homebrew casks.

==> mise self-update
Checking target-arch... mise-v2026.9.12-macos-arm64.tar.gz
Checking current version... v2026.9.10
Looking for tag: v2026.9.12

mise release status:
  * Current exe: /Users/mryfmo/.local/bin/mise
  * New exe release: "mise-v2026.9.12-macos-arm64.tar.gz"
  * New exe download url: "https://api.github.com/repos/jdx/mise/releases/assets/576717088"

The new release will be downloaded/extracted and the existing binary will be replaced.
Downloading...
Verifying downloaded file...
Extracting archive... Done
Replacing binary file... Done
Updated mise to 2026.9.12
mise plugin:eza                    update git repo
mise plugin:eza                  ✓ https://github.com/mise-plugins/mise-eza.git#636e59a

==> mise tools
mise WARN  No untrusted config files found.
mise by @jdx – installing 1 tool
mise ⇢ age@1.3.2  127ms · already installed
mise ████████████████ 1/1 · installed 0 tools · 1 already installed in 128ms
mise by @jdx – installing 1 tool
mise ⇢ aqua:micro-editor/micro@2.0.15  581ms · already installed
mise ████████████████ 1/1 · installed 0 tools · 1 already installed in 582ms
mise by @jdx – installing 1 tool
mise ⇢ bun@1.4.2  118ms · already installed
mise ████████████████ 1/1 · installed 0 tools · 1 already installed in 119ms
mise by @jdx – installing 1 tool
mise ⇢ cargo:eza@0.23.5  196ms · already installed
mise ████████████████ 1/1 · installed 0 tools · 1 already installed in 197ms
mise by @jdx – installing 1 tool
mise ⇢ cargo:pueue@4.0.4  154ms · already installed
mise ████████████████ 1/1 · installed 0 tools · 1 already installed in 155ms
mise by @jdx – installing 1 tool
mise ⇢ chezmoi@2.72.2  111ms · already installed
mise ████████████████ 1/1 · installed 0 tools · 1 already installed in 112ms
mise by @jdx – installing 1 tool
mise ⇢ cmake@4.4.3  105ms · already installed
mise ████████████████ 1/1 · installed 0 tools · 1 already installed in 105ms
mise by @jdx – installing 1 tool
mise ⇢ dotenvx@2.24.1  110ms · already installed
mise ████████████████ 1/1 · installed 0 tools · 1 already installed in 110ms
mise by @jdx – installing 1 tool
mise ⇢ fd@10.3.0  116ms · already installed
mise ████████████████ 1/1 · installed 0 tools · 1 already installed in 117ms
mise by @jdx – installing 1 tool
mise ⇢ github:cli/cli@2.100.0  2.4s · already installed
mise ████████████████ 1/1 · installed 0 tools · 1 already installed in 2.4s
mise by @jdx – installing 1 tool
mise ⇢ github:d-kuro/gwq@0.1.1  470ms · already installed
mise ████████████████ 1/1 · installed 0 tools · 1 already installed in 471ms
mise by @jdx – installing 1 tool
mise ⇢ github:mikefarah/yq@4.53.6  2.7s · already installed
mise ████████████████ 1/1 · installed 0 tools · 1 already installed in 2.7s
mise by @jdx – installing 1 tool
mise ⇢ github:ogulcancelik/herdr@0.9.0  877ms · already installed
mise ████████████████ 1/1 · installed 0 tools · 1 already installed in 878ms
mise by @jdx – installing 1 tool
mise ⇢ github:x-motemen/ghq@1.10.1  683ms · already installed
mise ████████████████ 1/1 · installed 0 tools · 1 already installed in 684ms
mise by @jdx – installing 1 tool
mise ⇢ http:bats@1.13.0  1ms · already installed
mise ████████████████ 1/1 · installed 0 tools · 1 already installed in 2ms
mise by @jdx – installing 1 tool
mise ⇢ http:gcloud@575.0.1  1ms · already installed
mise ████████████████ 1/1 · installed 0 tools · 1 already installed in 2ms
mise by @jdx – installing 1 tool
mise ⇢ hugo-extended@0.166.0  119ms · already installed
mise ████████████████ 1/1 · installed 0 tools · 1 already installed in 120ms
mise by @jdx – installing 1 tool
mise ⇢ jq@1.8.2  108ms · already installed
mise ████████████████ 1/1 · installed 0 tools · 1 already installed in 109ms
mise by @jdx – installing 1 tool
mise ⇢ node@26.8.2  108ms · already installed
mise ████████████████ 1/1 · installed 0 tools · 1 already installed in 109ms
mise by @jdx – installing 1 tool
mise ⇢ npm:@anthropic-ai/claude-code@2.1.278  25ms · already installed
mise ████████████████ 1/1 · installed 0 tools · 1 already installed in 25ms
mise by @jdx – installing 1 tool
mise ⇢ npm:@openai/codex@0.155.1  54ms · already installed
mise ████████████████ 1/1 · installed 0 tools · 1 already installed in 55ms
mise by @jdx – installing 1 tool
mise ⇢ npm:bash-language-server@5.6.0  20ms · already installed
mise ████████████████ 1/1 · installed 0 tools · 1 already installed in 21ms
mise by @jdx – installing 1 tool
mise ⇢ npm:ccstatusline@2.2.29  22ms · already installed
mise ████████████████ 1/1 · installed 0 tools · 1 already installed in 23ms
mise by @jdx – installing 1 tool
mise ⇢ npm:ccusage@20.0.20  21ms · already installed
mise ████████████████ 1/1 · installed 0 tools · 1 already installed in 22ms
mise by @jdx – installing 1 tool
mise ⇢ npm:fast-cli@5.2.0  8ms · already installed
mise ████████████████ 1/1 · installed 0 tools · 1 already installed in 9ms
mise by @jdx – installing 1 tool
mise ⇢ npm:pyright@1.1.414  27ms · already installed
mise ████████████████ 1/1 · installed 0 tools · 1 already installed in 28ms
mise by @jdx – installing 1 tool
mise ⇢ python@3.14.7  697ms · already installed
mise ████████████████ 1/1 · installed 0 tools · 1 already installed in 697ms
mise by @jdx – installing 1 tool
mise ⇢ rust@1.98.1  324ms · already installed
mise ████████████████ 1/1 · installed 0 tools · 1 already installed in 325ms
mise by @jdx – installing 1 tool
mise ⇢ shellcheck@0.11.0  119ms · already installed
mise ████████████████ 1/1 · installed 0 tools · 1 already installed in 119ms
mise by @jdx – installing 1 tool
mise ⇢ shfmt@3.14.1  104ms · already installed
mise ████████████████ 1/1 · installed 0 tools · 1 already installed in 105ms
mise by @jdx – installing 1 tool
mise ⇢ uv@0.12.13  116ms · already installed
mise ████████████████ 1/1 · installed 0 tools · 1 already installed in 117ms
mise by @jdx – installing 1 tool
mise ⇢ yazi@26.9.1  116ms · already installed
mise ████████████████ 1/1 · installed 0 tools · 1 already installed in 117ms
mise by @jdx – resolving 33 tools
mise ✓ rust                           2ms
mise ✓ node                           2ms
mise ✓ dotenvx                        2ms
mise ✓ age                            2ms
mise ✓ cmake                          2ms
mise ✓ chezmoi                        2ms
mise ✓ python                         2ms
mise ✓ cargo:eza                      2ms
mise ✓ bun                            2ms
mise ✓ jq                             3ms
mise ✓ shellcheck                     3ms
mise ✓ uv                             3ms
mise ✓ yazi                           3ms
mise ✓ aqua:micro-editor/micro        3ms
mise ✓ fd                             3ms
mise ✓ hugo-extended                  3ms
mise ✓ shfmt                          3ms
mise ✓ npm:bash-language-server       3ms
mise ✓ github:mikefarah/yq            3ms
mise ✓ npm:@anthropic-ai/claude-code  3ms
mise ✓ npm:@openai/codex              3ms
mise ✓ npm:ccstatusline               3ms
mise ✓ npm:fast-cli                   3ms
mise ✓ github:x-motemen/ghq           3ms
mise ✓ npm:pyright                    4ms
mise ✓ github:shuntaka9576/blocc      4ms
mise ✓ npm:ccusage                    4ms
mise ✓ cargo:pueue                    4ms
mise ✓ github:ogulcancelik/herdr      4ms
mise ✓ http:bats                      4ms
mise ✓ github:d-kuro/gwq              4ms
mise ✓ http:gcloud                    4ms
mise ✓ github:cli/cli                 4ms
mise ████████████████ 33/33 · resolved 33 tools in 4ms
mise by @jdx – resolving 1 tool
mise ✓ aqua:FiloSottile/age@1.3.2  391ms
mise ████████████████ 1/1 · resolved 1 tool in 391ms
mise All tools are up to date
mise by @jdx – resolving 33 tools
mise ✓ rust                           3ms
mise ✓ chezmoi                        3ms
mise ✓ dotenvx                        3ms
mise ✓ bun                            3ms
mise ✓ python                         3ms
mise ✓ node                           3ms
mise ✓ cargo:eza                      3ms
mise ✓ age                            3ms
mise ✓ cmake                          3ms
mise ✓ shellcheck                     3ms
mise ✓ hugo-extended                  3ms
mise ✓ fd                             3ms
mise ✓ uv                             3ms
mise ✓ yazi                           3ms
mise ✓ jq                             3ms
mise ✓ aqua:micro-editor/micro        3ms
mise ✓ github:mikefarah/yq            4ms
mise ✓ shfmt                          4ms
mise ✓ npm:@openai/codex              4ms
mise ✓ npm:@anthropic-ai/claude-code  4ms
mise ✓ npm:bash-language-server       4ms
mise ✓ npm:ccstatusline               4ms
mise ✓ npm:pyright                    4ms
mise ✓ npm:fast-cli                   4ms
mise ✓ npm:ccusage                    4ms
mise ✓ github:shuntaka9576/blocc      4ms
mise ✓ github:x-motemen/ghq           4ms
mise ✓ github:d-kuro/gwq              4ms
mise ✓ github:cli/cli                 4ms
mise ✓ cargo:pueue                    4ms
mise ✓ http:bats                      4ms
mise ✓ github:ogulcancelik/herdr      5ms
mise ✓ http:gcloud                    5ms
mise ████████████████ 33/33 · resolved 33 tools in 5ms
mise by @jdx – resolving 1 tool
mise ✓ aqua:micro-editor/micro@2.0.15  363ms
mise ████████████████ 1/1 · resolved 1 tool in 363ms
mise All tools are up to date
mise by @jdx – resolving 33 tools
mise ✓ rust                           2ms
mise ✓ dotenvx                        2ms
mise ✓ bun                            3ms
mise ✓ node                           3ms
mise ✓ python                         3ms
mise ✓ chezmoi                        3ms
mise ✓ cmake                          3ms
mise ✓ age                            3ms
mise ✓ cargo:eza                      3ms
mise ✓ shellcheck                     3ms
mise ✓ fd                             3ms
mise ✓ hugo-extended                  3ms
mise ✓ jq                             3ms
mise ✓ uv                             3ms
mise ✓ github:mikefarah/yq            3ms
mise ✓ yazi                           3ms
mise ✓ aqua:micro-editor/micro        3ms
mise ✓ npm:bash-language-server       3ms
mise ✓ shfmt                          4ms
mise ✓ npm:fast-cli                   4ms
mise ✓ npm:@openai/codex              4ms
mise ✓ npm:ccusage                    4ms
mise ✓ npm:ccstatusline               4ms
mise ✓ npm:pyright                    4ms
mise ✓ npm:@anthropic-ai/claude-code  4ms
mise ✓ github:x-motemen/ghq           4ms
mise ✓ github:shuntaka9576/blocc      4ms
mise ✓ github:d-kuro/gwq              4ms
mise ✓ github:cli/cli                 4ms
mise ✓ github:ogulcancelik/herdr      4ms
mise ✓ http:gcloud                    4ms
mise ✓ http:bats                      4ms
mise ✓ cargo:pueue                    4ms
mise ████████████████ 33/33 · resolved 33 tools in 4ms
mise by @jdx – resolving 1 tool
mise ✓ core:bun@1.4.2  1ms
mise ████████████████ 1/1 · resolved 1 tool in 1ms
mise All tools are up to date
mise by @jdx – resolving 33 tools
mise ✓ rust                           2ms
mise ✓ dotenvx                        2ms
mise ✓ age                            2ms
mise ✓ cmake                          2ms
mise ✓ node                           2ms
mise ✓ python                         2ms
mise ✓ bun                            2ms
mise ✓ cargo:eza                      2ms
mise ✓ chezmoi                        2ms
mise ✓ fd                             3ms
mise ✓ shellcheck                     3ms
mise ✓ jq                             3ms
mise ✓ github:mikefarah/yq            3ms
mise ✓ aqua:micro-editor/micro        3ms
mise ✓ hugo-extended                  3ms
mise ✓ yazi                           3ms
mise ✓ uv                             3ms
mise ✓ npm:bash-language-server       3ms
mise ✓ shfmt                          3ms
mise ✓ npm:@anthropic-ai/claude-code  3ms
mise ✓ npm:fast-cli                   3ms
mise ✓ npm:@openai/codex              3ms
mise ✓ npm:ccstatusline               3ms
mise ✓ npm:ccusage                    3ms
mise ✓ github:x-motemen/ghq           3ms
mise ✓ github:shuntaka9576/blocc      3ms
mise ✓ npm:pyright                    3ms
mise ✓ cargo:pueue                    4ms
mise ✓ github:cli/cli                 4ms
mise ✓ github:ogulcancelik/herdr      4ms
mise ✓ github:d-kuro/gwq              4ms
mise ✓ http:bats                      4ms
mise ✓ http:gcloud                    4ms
mise ████████████████ 33/33 · resolved 33 tools in 4ms
mise by @jdx – resolving 1 tool
mise ✓ cargo:eza@0.23.5  1ms
mise ████████████████ 1/1 · resolved 1 tool in 1ms
mise All tools are up to date
mise by @jdx – resolving 33 tools
mise ✓ rust                           2ms
mise ✓ dotenvx                        2ms
mise ✓ node                           2ms
mise ✓ cmake                          2ms
mise ✓ chezmoi                        2ms
mise ✓ python                         2ms
mise ✓ age                            2ms
mise ✓ bun                            3ms
mise ✓ cargo:eza                      3ms
mise ✓ fd                             3ms
mise ✓ jq                             3ms
mise ✓ hugo-extended                  3ms
mise ✓ uv                             3ms
mise ✓ yazi                           3ms
mise ✓ aqua:micro-editor/micro        3ms
mise ✓ shellcheck                     3ms
mise ✓ github:mikefarah/yq            3ms
mise ✓ npm:@openai/codex              3ms
mise ✓ npm:bash-language-server       3ms
mise ✓ npm:@anthropic-ai/claude-code  3ms
mise ✓ shfmt                          3ms
mise ✓ npm:ccstatusline               3ms
mise ✓ npm:fast-cli                   3ms
mise ✓ npm:ccusage                    3ms
mise ✓ npm:pyright                    4ms
mise ✓ github:shuntaka9576/blocc      4ms
mise ✓ github:x-motemen/ghq           4ms
mise ✓ github:cli/cli                 4ms
mise ✓ github:d-kuro/gwq              4ms
mise ✓ cargo:pueue                    4ms
mise ✓ github:ogulcancelik/herdr      4ms
mise ✓ http:gcloud                    4ms
mise ✓ http:bats                      4ms
mise ████████████████ 33/33 · resolved 33 tools in 4ms
mise by @jdx – resolving 1 tool
mise ✓ cargo:pueue@4.0.4  1ms
mise ████████████████ 1/1 · resolved 1 tool in 1ms
mise All tools are up to date
mise by @jdx – resolving 33 tools
mise ✓ rust                           2ms
mise ✓ cmake                          2ms
mise ✓ age                            2ms
mise ✓ python                         2ms
mise ✓ dotenvx                        2ms
mise ✓ bun                            2ms
mise ✓ node                           2ms
mise ✓ chezmoi                        2ms
mise ✓ cargo:eza                      2ms
mise ✓ shellcheck                     3ms
mise ✓ fd                             3ms
mise ✓ uv                             3ms
mise ✓ github:mikefarah/yq            3ms
mise ✓ yazi                           3ms
mise ✓ jq                             3ms
mise ✓ hugo-extended                  3ms
mise ✓ aqua:micro-editor/micro        3ms
mise ✓ npm:bash-language-server       3ms
mise ✓ shfmt                          3ms
mise ✓ npm:@anthropic-ai/claude-code  3ms
mise ✓ npm:fast-cli                   3ms
mise ✓ npm:@openai/codex              3ms
mise ✓ npm:ccstatusline               4ms
mise ✓ github:shuntaka9576/blocc      4ms
mise ✓ npm:ccusage                    4ms
mise ✓ github:x-motemen/ghq           4ms
mise ✓ cargo:pueue                    4ms
mise ✓ github:ogulcancelik/herdr      4ms
mise ✓ github:cli/cli                 4ms
mise ✓ npm:pyright                    4ms
mise ✓ github:d-kuro/gwq              4ms
mise ✓ http:bats                      4ms
mise ✓ http:gcloud                    4ms
mise ████████████████ 33/33 · resolved 33 tools in 4ms
mise by @jdx – resolving 1 tool
mise ✓ aqua:twpayne/chezmoi@2.72.2  445ms
mise ████████████████ 1/1 · resolved 1 tool in 445ms
mise All tools are up to date
mise by @jdx – resolving 33 tools
mise ✓ rust                           3ms
mise ✓ age                            3ms
mise ✓ node                           3ms
mise ✓ chezmoi                        3ms
mise ✓ python                         3ms
mise ✓ bun                            3ms
mise ✓ dotenvx                        3ms
mise ✓ cmake                          3ms
mise ✓ cargo:eza                      3ms
mise ✓ jq                             3ms
mise ✓ yazi                           3ms
mise ✓ uv                             3ms
mise ✓ hugo-extended                  3ms
mise ✓ fd                             4ms
mise ✓ shellcheck                     4ms
mise ✓ aqua:micro-editor/micro        4ms
mise ✓ github:mikefarah/yq            4ms
mise ✓ npm:bash-language-server       4ms
mise ✓ npm:@openai/codex              4ms
mise ✓ shfmt                          4ms
mise ✓ npm:@anthropic-ai/claude-code  4ms
mise ✓ npm:ccusage                    4ms
mise ✓ npm:ccstatusline               4ms
mise ✓ npm:fast-cli                   4ms
mise ✓ npm:pyright                    4ms
mise ✓ github:x-motemen/ghq           4ms
mise ✓ github:shuntaka9576/blocc      4ms
mise ✓ github:d-kuro/gwq              5ms
mise ✓ github:ogulcancelik/herdr      5ms
mise ✓ github:cli/cli                 5ms
mise ✓ http:gcloud                    5ms
mise ✓ cargo:pueue                    5ms
mise ✓ http:bats                      5ms
mise ████████████████ 33/33 · resolved 33 tools in 5ms
mise by @jdx – resolving 1 tool
mise ✓ aqua:Kitware/CMake@4.4.3  352ms
mise ████████████████ 1/1 · resolved 1 tool in 352ms
mise All tools are up to date
mise by @jdx – resolving 33 tools
mise ✓ rust                           2ms
mise ✓ cmake                          3ms
mise ✓ dotenvx                        3ms
mise ✓ chezmoi                        3ms
mise ✓ node                           3ms
mise ✓ bun                            3ms
mise ✓ age                            3ms
mise ✓ python                         3ms
mise ✓ cargo:eza                      3ms
mise ✓ fd                             3ms
mise ✓ shellcheck                     3ms
mise ✓ hugo-extended                  3ms
mise ✓ uv                             3ms
mise ✓ jq                             3ms
mise ✓ github:mikefarah/yq            3ms
mise ✓ yazi                           3ms
mise ✓ aqua:micro-editor/micro        3ms
mise ✓ npm:bash-language-server       4ms
mise ✓ npm:@anthropic-ai/claude-code  4ms
mise ✓ shfmt                          4ms
mise ✓ npm:ccstatusline               4ms
mise ✓ npm:fast-cli                   4ms
mise ✓ github:x-motemen/ghq           4ms
mise ✓ npm:ccusage                    4ms
mise ✓ npm:@openai/codex              4ms
mise ✓ npm:pyright                    4ms
mise ✓ github:d-kuro/gwq              4ms
mise ✓ cargo:pueue                    4ms
mise ✓ github:shuntaka9576/blocc      4ms
mise ✓ github:ogulcancelik/herdr      4ms
mise ✓ github:cli/cli                 4ms
mise ✓ http:bats                      4ms
mise ✓ http:gcloud                    4ms
mise ████████████████ 33/33 · resolved 33 tools in 5ms
mise by @jdx – resolving 1 tool
mise ✓ aqua:dotenvx/dotenvx@2.24.1  403ms
mise ████████████████ 1/1 · resolved 1 tool in 403ms
mise WARN  newer dotenvx release 2.28.2 (released 2026-09-20, eligible 2026-09-27 09:19 JST) ignored by minimum_release_age (7d); latest eligible release is 2.24.1
mise All tools are up to date
Skipping mise upgrade for fd: newer releases lack a macOS x64 asset.
mise by @jdx – resolving 33 tools
mise ✓ rust                           3ms
mise ✓ chezmoi                        3ms
mise ✓ dotenvx                        3ms
mise ✓ node                           3ms
mise ✓ python                         3ms
mise ✓ cmake                          3ms
mise ✓ age                            3ms
mise ✓ bun                            3ms
mise ✓ cargo:eza                      3ms
mise ✓ jq                             3ms
mise ✓ yazi                           3ms
mise ✓ fd                             3ms
mise ✓ uv                             3ms
mise ✓ aqua:micro-editor/micro        3ms
mise ✓ github:mikefarah/yq            3ms
mise ✓ hugo-extended                  3ms
mise ✓ shellcheck                     4ms
mise ✓ shfmt                          4ms
mise ✓ npm:@anthropic-ai/claude-code  4ms
mise ✓ npm:bash-language-server       4ms
mise ✓ npm:@openai/codex              4ms
mise ✓ npm:ccusage                    4ms
mise ✓ npm:ccstatusline               4ms
mise ✓ npm:fast-cli                   4ms
mise ✓ npm:pyright                    4ms
mise ✓ github:shuntaka9576/blocc      4ms
mise ✓ github:x-motemen/ghq           4ms
mise ✓ github:d-kuro/gwq              4ms
mise ✓ cargo:pueue                    5ms
mise ✓ http:gcloud                    5ms
mise ✓ github:cli/cli                 5ms
mise ✓ http:bats                      5ms
mise ✓ github:ogulcancelik/herdr      5ms
mise ████████████████ 33/33 · resolved 33 tools in 5ms
mise by @jdx – resolving 1 tool
mise ✓ github:cli/cli@2.100.0  342ms
mise ████████████████ 1/1 · resolved 1 tool in 342ms
mise WARN  newer github:cli/cli release 2.101.0 (released 2026-09-15, eligible 2026-09-22 23:24 JST) ignored by minimum_release_age (7d); latest eligible release is 2.100.0
mise All tools are up to date
mise by @jdx – resolving 33 tools
mise ✓ rust                           3ms
mise ✓ bun                            3ms
mise ✓ python                         3ms
mise ✓ chezmoi                        3ms
mise ✓ dotenvx                        3ms
mise ✓ cmake                          3ms
mise ✓ age                            3ms
mise ✓ node                           3ms
mise ✓ cargo:eza                      3ms
mise ✓ jq                             3ms
mise ✓ shellcheck                     3ms
mise ✓ hugo-extended                  3ms
mise ✓ yazi                           3ms
mise ✓ fd                             4ms
mise ✓ uv                             4ms
mise ✓ aqua:micro-editor/micro        4ms
mise ✓ github:mikefarah/yq            4ms
mise ✓ shfmt                          4ms
mise ✓ npm:bash-language-server       4ms
mise ✓ npm:@openai/codex              4ms
mise ✓ npm:ccusage                    4ms
mise ✓ npm:pyright                    4ms
mise ✓ npm:ccstatusline               4ms
mise ✓ npm:fast-cli                   4ms
mise ✓ github:x-motemen/ghq           4ms
mise ✓ npm:@anthropic-ai/claude-code  4ms
mise ✓ github:d-kuro/gwq              4ms
mise ✓ github:shuntaka9576/blocc      5ms
mise ✓ http:bats                      5ms
mise ✓ github:cli/cli                 5ms
mise ✓ cargo:pueue                    5ms
mise ✓ github:ogulcancelik/herdr      5ms
mise ✓ http:gcloud                    5ms
mise ████████████████ 33/33 · resolved 33 tools in 5ms
mise by @jdx – resolving 1 tool
mise ✓ github:d-kuro/gwq@0.1.1  340ms
mise ████████████████ 1/1 · resolved 1 tool in 340ms
mise All tools are up to date
mise by @jdx – resolving 33 tools
mise ✓ rust                           3ms
mise ✓ chezmoi                        3ms
mise ✓ python                         3ms
mise ✓ cmake                          3ms
mise ✓ bun                            3ms
mise ✓ age                            3ms
mise ✓ dotenvx                        3ms
mise ✓ node                           3ms
mise ✓ cargo:eza                      3ms
mise ✓ fd                             3ms
mise ✓ jq                             3ms
mise ✓ hugo-extended                  3ms
mise ✓ uv                             3ms
mise ✓ aqua:micro-editor/micro        3ms
mise ✓ yazi                           4ms
mise ✓ shellcheck                     4ms
mise ✓ github:mikefarah/yq            4ms
mise ✓ npm:bash-language-server       4ms
mise ✓ shfmt                          4ms
mise ✓ npm:@anthropic-ai/claude-code  4ms
mise ✓ npm:ccstatusline               4ms
mise ✓ npm:fast-cli                   4ms
mise ✓ npm:ccusage                    4ms
mise ✓ npm:pyright                    4ms
mise ✓ npm:@openai/codex              5ms
mise ✓ github:shuntaka9576/blocc      5ms
mise ✓ github:x-motemen/ghq           5ms
mise ✓ cargo:pueue                    5ms
mise ✓ github:cli/cli                 5ms
mise ✓ github:d-kuro/gwq              5ms
mise ✓ github:ogulcancelik/herdr      5ms
mise ✓ http:bats                      5ms
mise ✓ http:gcloud                    5ms
mise ████████████████ 33/33 · resolved 33 tools in 5ms
mise by @jdx – resolving 1 tool
mise ✓ github:mikefarah/yq@4.53.6  353ms
mise ████████████████ 1/1 · resolved 1 tool in 353ms
mise All tools are up to date
mise by @jdx – resolving 33 tools
mise ✓ rust                           2ms
mise ✓ cmake                          2ms
mise ✓ age                            2ms
mise ✓ node                           2ms
mise ✓ chezmoi                        2ms
mise ✓ python                         2ms
mise ✓ bun                            2ms
mise ✓ cargo:eza                      2ms
mise ✓ dotenvx                        2ms
mise ✓ fd                             3ms
mise ✓ shellcheck                     3ms
mise ✓ hugo-extended                  3ms
mise ✓ uv                             3ms
mise ✓ yazi                           3ms
mise ✓ jq                             3ms
mise ✓ aqua:micro-editor/micro        3ms
mise ✓ github:mikefarah/yq            3ms
mise ✓ npm:bash-language-server       3ms
mise ✓ shfmt                          4ms
mise ✓ npm:@anthropic-ai/claude-code  4ms
mise ✓ npm:@openai/codex              4ms
mise ✓ npm:fast-cli                   4ms
mise ✓ npm:ccusage                    4ms
mise ✓ github:x-motemen/ghq           4ms
mise ✓ npm:ccstatusline               4ms
mise ✓ github:shuntaka9576/blocc      4ms
mise ✓ github:d-kuro/gwq              4ms
mise ✓ github:cli/cli                 5ms
mise ✓ npm:pyright                    5ms
mise ✓ cargo:pueue                    5ms
mise ✓ github:ogulcancelik/herdr      5ms
mise ✓ http:bats                      5ms
mise ✓ http:gcloud                    5ms
mise ████████████████ 33/33 · resolved 33 tools in 5ms
mise by @jdx – resolving 1 tool
mise ✓ github:ogulcancelik/herdr@0.9.0  601ms
mise ████████████████ 1/1 · resolved 1 tool in 602ms
mise WARN  newer github:ogulcancelik/herdr release 0.9.1 (released 2026-09-17, eligible 2026-09-24 03:40 JST) ignored by minimum_release_age (7d); latest eligible release is 0.9.0
mise All tools are up to date
mise by @jdx – resolving 33 tools
mise ✓ rust                           3ms
mise ✓ node                           3ms
mise ✓ chezmoi                        3ms
mise ✓ python                         3ms
mise ✓ age                            3ms
mise ✓ bun                            3ms
mise ✓ dotenvx                        3ms
mise ✓ cmake                          3ms
mise ✓ cargo:eza                      3ms
mise ✓ fd                             3ms
mise ✓ jq                             3ms
mise ✓ yazi                           3ms
mise ✓ github:mikefarah/yq            3ms
mise ✓ shellcheck                     3ms
mise ✓ hugo-extended                  3ms
mise ✓ aqua:micro-editor/micro        4ms
mise ✓ uv                             4ms
mise ✓ shfmt                          4ms
mise ✓ npm:bash-language-server       4ms
mise ✓ npm:@anthropic-ai/claude-code  4ms
mise ✓ npm:@openai/codex              4ms
mise ✓ npm:fast-cli                   4ms
mise ✓ npm:ccusage                    4ms
mise ✓ npm:ccstatusline               4ms
mise ✓ github:shuntaka9576/blocc      4ms
mise ✓ github:cli/cli                 4ms
mise ✓ github:ogulcancelik/herdr      4ms
mise ✓ github:x-motemen/ghq           4ms
mise ✓ npm:pyright                    4ms
mise ✓ cargo:pueue                    4ms
mise ✓ github:d-kuro/gwq              4ms
mise ✓ http:bats                      5ms
mise ✓ http:gcloud                    5ms
mise ████████████████ 33/33 · resolved 33 tools in 5ms
mise by @jdx – resolving 1 tool
mise ✓ github:x-motemen/ghq@1.10.1  355ms
mise ████████████████ 1/1 · resolved 1 tool in 355ms
mise All tools are up to date
Skipping mise upgrade for pinned HTTP tool: http:bats.
Skipping mise upgrade for pinned HTTP tool: http:gcloud.
mise by @jdx – resolving 33 tools
mise ✓ rust                           2ms
mise ✓ dotenvx                        2ms
mise ✓ bun                            3ms
mise ✓ node                           3ms
mise ✓ cmake                          3ms
mise ✓ chezmoi                        3ms
mise ✓ python                         3ms
mise ✓ age                            3ms
mise ✓ fd                             3ms
mise ✓ hugo-extended                  3ms
mise ✓ uv                             3ms
mise ✓ cargo:eza                      3ms
mise ✓ jq                             3ms
mise ✓ yazi                           3ms
mise ✓ shellcheck                     3ms
mise ✓ github:mikefarah/yq            3ms
mise ✓ aqua:micro-editor/micro        3ms
mise ✓ shfmt                          3ms
mise ✓ npm:bash-language-server       3ms
mise ✓ npm:@anthropic-ai/claude-code  4ms
mise ✓ npm:@openai/codex              4ms
mise ✓ npm:ccstatusline               4ms
mise ✓ github:x-motemen/ghq           4ms
mise ✓ npm:ccusage                    4ms
mise ✓ npm:pyright                    4ms
mise ✓ npm:fast-cli                   4ms
mise ✓ github:d-kuro/gwq              4ms
mise ✓ github:shuntaka9576/blocc      4ms
mise ✓ github:cli/cli                 4ms
mise ✓ cargo:pueue                    4ms
mise ✓ github:ogulcancelik/herdr      4ms
mise ✓ http:bats                      4ms
mise ✓ http:gcloud                    4ms
mise ████████████████ 33/33 · resolved 33 tools in 4ms
mise by @jdx – resolving 1 tool
mise ✓ aqua:gohugoio/hugo/hugo-extended@0.166.0  377ms
mise ████████████████ 1/1 · resolved 1 tool in 378ms
mise All tools are up to date
mise by @jdx – resolving 33 tools
mise ✓ rust                           2ms
mise ✓ python                         2ms
mise ✓ dotenvx                        2ms
mise ✓ cmake                          2ms
mise ✓ chezmoi                        2ms
mise ✓ node                           2ms
mise ✓ cargo:eza                      2ms
mise ✓ age                            2ms
mise ✓ bun                            2ms
mise ✓ fd                             3ms
mise ✓ hugo-extended                  3ms
mise ✓ uv                             3ms
mise ✓ yazi                           3ms
mise ✓ jq                             3ms
mise ✓ shellcheck                     3ms
mise ✓ github:mikefarah/yq            3ms
mise ✓ aqua:micro-editor/micro        3ms
mise ✓ npm:bash-language-server       3ms
mise ✓ npm:@anthropic-ai/claude-code  3ms
mise ✓ npm:@openai/codex              3ms
mise ✓ shfmt                          3ms
mise ✓ npm:ccstatusline               4ms
mise ✓ github:x-motemen/ghq           4ms
mise ✓ npm:pyright                    4ms
mise ✓ npm:ccusage                    4ms
mise ✓ github:shuntaka9576/blocc      4ms
mise ✓ npm:fast-cli                   4ms
mise ✓ github:cli/cli                 4ms
mise ✓ github:d-kuro/gwq              4ms
mise ✓ github:ogulcancelik/herdr      4ms
mise ✓ http:gcloud                    4ms
mise ✓ cargo:pueue                    4ms
mise ✓ http:bats                      4ms
mise ████████████████ 33/33 · resolved 33 tools in 4ms
mise by @jdx – resolving 1 tool
mise ✓ aqua:jqlang/jq@1.8.2  385ms
mise ████████████████ 1/1 · resolved 1 tool in 386ms
mise All tools are up to date
mise by @jdx – resolving 33 tools
mise ✓ rust                           2ms
mise ✓ cmake                          3ms
mise ✓ age                            3ms
mise ✓ chezmoi                        3ms
mise ✓ bun                            3ms
mise ✓ dotenvx                        3ms
mise ✓ python                         3ms
mise ✓ node                           3ms
mise ✓ cargo:eza                      3ms
mise ✓ fd                             3ms
mise ✓ aqua:micro-editor/micro        3ms
mise ✓ shellcheck                     3ms
mise ✓ uv                             3ms
mise ✓ yazi                           3ms
mise ✓ hugo-extended                  4ms
mise ✓ jq                             4ms
mise ✓ github:mikefarah/yq            4ms
mise ✓ npm:bash-language-server       4ms
mise ✓ npm:@anthropic-ai/claude-code  4ms
mise ✓ shfmt                          4ms
mise ✓ npm:@openai/codex              4ms
mise ✓ npm:ccstatusline               4ms
mise ✓ github:x-motemen/ghq           4ms
mise ✓ npm:fast-cli                   4ms
mise ✓ github:shuntaka9576/blocc      4ms
mise ✓ npm:pyright                    4ms
mise ✓ npm:ccusage                    5ms
mise ✓ github:d-kuro/gwq              5ms
mise ✓ cargo:pueue                    5ms
mise ✓ github:cli/cli                 5ms
mise ✓ http:bats                      5ms
mise ✓ http:gcloud                    5ms
mise ✓ github:ogulcancelik/herdr      5ms
mise ████████████████ 33/33 · resolved 33 tools in 5ms
mise by @jdx – resolving 1 tool
mise ✓ core:node@26.8.2  1ms
mise ████████████████ 1/1 · resolved 1 tool in 1ms
mise WARN  newer node release 26.9.0 (released 2026-09-16, eligible 2026-09-23 09:00 JST) ignored by minimum_release_age (7d); latest eligible release is 26.8.2
mise All tools are up to date
mise by @jdx – resolving 33 tools
mise ✓ rust                           2ms
mise ✓ node                           2ms
mise ✓ chezmoi                        2ms
mise ✓ python                         2ms
mise ✓ age                            2ms
mise ✓ bun                            2ms
mise ✓ dotenvx                        2ms
mise ✓ cmake                          2ms
mise ✓ cargo:eza                      3ms
mise ✓ fd                             3ms
mise ✓ jq                             3ms
mise ✓ shellcheck                     3ms
mise ✓ hugo-extended                  3ms
mise ✓ uv                             3ms
mise ✓ aqua:micro-editor/micro        3ms
mise ✓ yazi                           3ms
mise ✓ npm:bash-language-server       3ms
mise ✓ shfmt                          3ms
mise ✓ npm:@openai/codex              3ms
mise ✓ github:mikefarah/yq            3ms
mise ✓ npm:@anthropic-ai/claude-code  3ms
mise ✓ npm:ccstatusline               3ms
mise ✓ github:x-motemen/ghq           4ms
mise ✓ npm:ccusage                    4ms
mise ✓ npm:pyright                    4ms
mise ✓ github:shuntaka9576/blocc      4ms
mise ✓ github:cli/cli                 4ms
mise ✓ npm:fast-cli                   4ms
mise ✓ github:d-kuro/gwq              4ms
mise ✓ github:ogulcancelik/herdr      4ms
mise ✓ cargo:pueue                    4ms
mise ✓ http:bats                      4ms
mise ✓ http:gcloud                    4ms
mise ████████████████ 33/33 · resolved 33 tools in 4ms
mise by @jdx – resolving 1 tool
mise ✓ npm:@anthropic-ai/claude-code@2.1.278  158ms
mise ████████████████ 1/1 · resolved 1 tool in 158ms
mise All tools are up to date
mise by @jdx – resolving 33 tools
mise ✓ rust                           2ms
mise ✓ node                           2ms
mise ✓ python                         2ms
mise ✓ age                            2ms
mise ✓ cmake                          2ms
mise ✓ bun                            2ms
mise ✓ chezmoi                        2ms
mise ✓ dotenvx                        2ms
mise ✓ cargo:eza                      2ms
mise ✓ shellcheck                     3ms
mise ✓ jq                             3ms
mise ✓ fd                             3ms
mise ✓ yazi                           3ms
mise ✓ uv                             3ms
mise ✓ hugo-extended                  3ms
mise ✓ aqua:micro-editor/micro        3ms
mise ✓ github:mikefarah/yq            3ms
mise ✓ npm:bash-language-server       3ms
mise ✓ npm:@anthropic-ai/claude-code  3ms
mise ✓ npm:@openai/codex              3ms
mise ✓ npm:ccstatusline               3ms
mise ✓ npm:pyright                    3ms
mise ✓ shfmt                          3ms
mise ✓ npm:ccusage                    3ms
mise ✓ github:x-motemen/ghq           4ms
mise ✓ npm:fast-cli                   4ms
mise ✓ github:shuntaka9576/blocc      4ms
mise ✓ github:d-kuro/gwq              4ms
mise ✓ cargo:pueue                    4ms
mise ✓ github:cli/cli                 4ms
mise ✓ http:bats                      4ms
mise ✓ http:gcloud                    4ms
mise ✓ github:ogulcancelik/herdr      4ms
mise ████████████████ 33/33 · resolved 33 tools in 4ms
mise by @jdx – resolving 1 tool
mise ✓ npm:@openai/codex@0.155.1  359ms
mise ████████████████ 1/1 · resolved 1 tool in 360ms
mise All tools are up to date
mise by @jdx – resolving 33 tools
mise ✓ rust                           3ms
mise ✓ python                         3ms
mise ✓ dotenvx                        3ms
mise ✓ cmake                          3ms
mise ✓ node                           3ms
mise ✓ age                            3ms
mise ✓ bun                            3ms
mise ✓ chezmoi                        3ms
mise ✓ cargo:eza                      3ms
mise ✓ fd                             3ms
mise ✓ uv                             3ms
mise ✓ yazi                           3ms
mise ✓ github:mikefarah/yq            3ms
mise ✓ hugo-extended                  3ms
mise ✓ jq                             3ms
mise ✓ aqua:micro-editor/micro        3ms
mise ✓ shellcheck                     4ms
mise ✓ shfmt                          4ms
mise ✓ npm:bash-language-server       4ms
mise ✓ npm:@anthropic-ai/claude-code  4ms
mise ✓ npm:ccstatusline               4ms
mise ✓ npm:pyright                    4ms
mise ✓ npm:ccusage                    4ms
mise ✓ npm:fast-cli                   4ms
mise ✓ github:x-motemen/ghq           4ms
mise ✓ npm:@openai/codex              4ms
mise ✓ github:shuntaka9576/blocc      4ms
mise ✓ github:d-kuro/gwq              4ms
mise ✓ github:cli/cli                 4ms
mise ✓ cargo:pueue                    5ms
mise ✓ http:bats                      5ms
mise ✓ github:ogulcancelik/herdr      5ms
mise ✓ http:gcloud                    5ms
mise ████████████████ 33/33 · resolved 33 tools in 5ms
mise by @jdx – resolving 1 tool
mise ✓ npm:bash-language-server@5.6.0  219ms
mise ████████████████ 1/1 · resolved 1 tool in 219ms
mise WARN  newer npm:bash-language-server release 5.8.1 (released 2026-09-20, eligible 2026-09-27 05:44 JST) ignored by minimum_release_age (7d); latest eligible release is 5.6.0
mise All tools are up to date
mise by @jdx – resolving 33 tools
mise ✓ rust                           2ms
mise ✓ cmake                          2ms
mise ✓ python                         2ms
mise ✓ node                           2ms
mise ✓ chezmoi                        2ms
mise ✓ age                            3ms
mise ✓ dotenvx                        3ms
mise ✓ bun                            3ms
mise ✓ cargo:eza                      3ms
mise ✓ shellcheck                     3ms
mise ✓ fd                             3ms
mise ✓ jq                             3ms
mise ✓ uv                             3ms
mise ✓ yazi                           3ms
mise ✓ hugo-extended                  3ms
mise ✓ aqua:micro-editor/micro        3ms
mise ✓ github:mikefarah/yq            3ms
mise ✓ shfmt                          3ms
mise ✓ npm:bash-language-server       3ms
mise ✓ npm:@anthropic-ai/claude-code  3ms
mise ✓ npm:@openai/codex              4ms
mise ✓ npm:ccstatusline               4ms
mise ✓ npm:fast-cli                   4ms
mise ✓ npm:pyright                    4ms
mise ✓ github:x-motemen/ghq           4ms
mise ✓ github:shuntaka9576/blocc      4ms
mise ✓ npm:ccusage                    4ms
mise ✓ cargo:pueue                    4ms
mise ✓ github:d-kuro/gwq              4ms
mise ✓ github:ogulcancelik/herdr      4ms
mise ✓ github:cli/cli                 4ms
mise ✓ http:bats                      4ms
mise ✓ http:gcloud                    4ms
mise ████████████████ 33/33 · resolved 33 tools in 4ms
mise by @jdx – resolving 1 tool
mise ✓ npm:ccstatusline@2.2.29  134ms
mise ████████████████ 1/1 · resolved 1 tool in 135ms
mise WARN  newer npm:ccstatusline release 2.2.30 (released 2026-09-18, eligible 2026-09-25 02:42 JST) ignored by minimum_release_age (7d); latest eligible release is 2.2.29
mise All tools are up to date
mise by @jdx – resolving 33 tools
mise ✓ rust                           2ms
mise ✓ cmake                          2ms
mise ✓ age                            2ms
mise ✓ node                           2ms
mise ✓ dotenvx                        2ms
mise ✓ chezmoi                        2ms
mise ✓ python                         2ms
mise ✓ bun                            3ms
mise ✓ cargo:eza                      3ms
mise ✓ fd                             3ms
mise ✓ uv                             3ms
mise ✓ yazi                           3ms
mise ✓ aqua:micro-editor/micro        3ms
mise ✓ shellcheck                     3ms
mise ✓ hugo-extended                  3ms
mise ✓ jq                             3ms
mise ✓ github:mikefarah/yq            3ms
mise ✓ shfmt                          3ms
mise ✓ npm:bash-language-server       3ms
mise ✓ npm:@anthropic-ai/claude-code  3ms
mise ✓ npm:@openai/codex              3ms
mise ✓ npm:fast-cli                   4ms
mise ✓ github:x-motemen/ghq           4ms
mise ✓ github:d-kuro/gwq              4ms
mise ✓ github:cli/cli                 4ms
mise ✓ github:shuntaka9576/blocc      4ms
mise ✓ npm:pyright                    4ms
mise ✓ npm:ccstatusline               4ms
mise ✓ npm:ccusage                    4ms
mise ✓ cargo:pueue                    4ms
mise ✓ github:ogulcancelik/herdr      4ms
mise ✓ http:bats                      4ms
mise ✓ http:gcloud                    4ms
mise ████████████████ 33/33 · resolved 33 tools in 4ms
mise by @jdx – resolving 1 tool
mise ✓ npm:ccusage@20.0.20  131ms
mise ████████████████ 1/1 · resolved 1 tool in 131ms
mise WARN  newer npm:ccusage release 20.0.24 (released 2026-09-21, eligible 2026-09-28 20:28 JST) ignored by minimum_release_age (7d); latest eligible release is 20.0.20
mise All tools are up to date
mise by @jdx – resolving 33 tools
mise ✓ rust                           2ms
mise ✓ bun                            2ms
mise ✓ python                         2ms
mise ✓ age                            2ms
mise ✓ cmake                          2ms
mise ✓ dotenvx                        2ms
mise ✓ node                           2ms
mise ✓ chezmoi                        2ms
mise ✓ cargo:eza                      2ms
mise ✓ fd                             3ms
mise ✓ uv                             3ms
mise ✓ jq                             3ms
mise ✓ shellcheck                     3ms
mise ✓ yazi                           3ms
mise ✓ aqua:micro-editor/micro        3ms
mise ✓ hugo-extended                  3ms
mise ✓ npm:@anthropic-ai/claude-code  3ms
mise ✓ github:mikefarah/yq            3ms
mise ✓ shfmt                          3ms
mise ✓ npm:bash-language-server       3ms
mise ✓ npm:@openai/codex              3ms
mise ✓ npm:ccusage                    3ms
mise ✓ npm:fast-cli                   3ms
mise ✓ npm:pyright                    3ms
mise ✓ npm:ccstatusline               3ms
mise ✓ github:shuntaka9576/blocc      3ms
mise ✓ github:cli/cli                 4ms
mise ✓ github:d-kuro/gwq              4ms
mise ✓ cargo:pueue                    4ms
mise ✓ github:ogulcancelik/herdr      4ms
mise ✓ github:x-motemen/ghq           4ms
mise ✓ http:gcloud                    4ms
mise ✓ http:bats                      4ms
mise ████████████████ 33/33 · resolved 33 tools in 4ms
mise by @jdx – resolving 1 tool
mise ✓ npm:fast-cli@5.2.0  228ms
mise ████████████████ 1/1 · resolved 1 tool in 228ms
mise All tools are up to date
mise by @jdx – resolving 33 tools
mise ✓ rust                           2ms
mise ✓ age                            3ms
mise ✓ node                           3ms
mise ✓ python                         3ms
mise ✓ cmake                          3ms
mise ✓ cargo:eza                      3ms
mise ✓ dotenvx                        3ms
mise ✓ chezmoi                        3ms
mise ✓ bun                            3ms
mise ✓ shellcheck                     3ms
mise ✓ yazi                           3ms
mise ✓ hugo-extended                  3ms
mise ✓ aqua:micro-editor/micro        3ms
mise ✓ fd                             3ms
mise ✓ jq                             3ms
mise ✓ uv                             3ms
mise ✓ github:mikefarah/yq            3ms
mise ✓ npm:bash-language-server       3ms
mise ✓ shfmt                          3ms
mise ✓ npm:@anthropic-ai/claude-code  4ms
mise ✓ npm:ccusage                    4ms
mise ✓ npm:pyright                    4ms
mise ✓ npm:@openai/codex              4ms
mise ✓ npm:ccstatusline               4ms
mise ✓ github:x-motemen/ghq           4ms
mise ✓ github:d-kuro/gwq              4ms
mise ✓ github:shuntaka9576/blocc      4ms
mise ✓ npm:fast-cli                   4ms
mise ✓ github:ogulcancelik/herdr      4ms
mise ✓ cargo:pueue                    4ms
mise ✓ github:cli/cli                 4ms
mise ✓ http:gcloud                    4ms
mise ✓ http:bats                      4ms
mise ████████████████ 33/33 · resolved 33 tools in 4ms
mise by @jdx – resolving 1 tool
mise ✓ npm:pyright@1.1.414  241ms
mise ████████████████ 1/1 · resolved 1 tool in 241ms
mise All tools are up to date
mise by @jdx – resolving 33 tools
mise ✓ rust                           2ms
mise ✓ chezmoi                        2ms
mise ✓ cmake                          2ms
mise ✓ dotenvx                        2ms
mise ✓ age                            2ms
mise ✓ node                           2ms
mise ✓ bun                            2ms
mise ✓ python                         2ms
mise ✓ cargo:eza                      2ms
mise ✓ shellcheck                     3ms
mise ✓ hugo-extended                  3ms
mise ✓ yazi                           3ms
mise ✓ fd                             3ms
mise ✓ aqua:micro-editor/micro        3ms
mise ✓ jq                             3ms
mise ✓ uv                             3ms
mise ✓ github:mikefarah/yq            3ms
mise ✓ shfmt                          3ms
mise ✓ npm:bash-language-server       3ms
mise ✓ npm:@anthropic-ai/claude-code  3ms
mise ✓ npm:@openai/codex              3ms
mise ✓ npm:fast-cli                   4ms
mise ✓ github:x-motemen/ghq           4ms
mise ✓ npm:ccstatusline               4ms
mise ✓ npm:ccusage                    4ms
mise ✓ github:shuntaka9576/blocc      4ms
mise ✓ github:cli/cli                 4ms
mise ✓ github:d-kuro/gwq              4ms
mise ✓ npm:pyright                    4ms
mise ✓ cargo:pueue                    4ms
mise ✓ http:bats                      4ms
mise ✓ github:ogulcancelik/herdr      4ms
mise ✓ http:gcloud                    4ms
mise ████████████████ 33/33 · resolved 33 tools in 4ms
mise by @jdx – resolving 1 tool
mise ✓ core:python@3.14.7  2ms
mise ████████████████ 1/1 · resolved 1 tool in 2ms
mise All tools are up to date
mise by @jdx – resolving 33 tools
mise ✓ rust                           2ms
mise ✓ cmake                          2ms
mise ✓ chezmoi                        2ms
mise ✓ node                           2ms
mise ✓ dotenvx                        2ms
mise ✓ age                            2ms
mise ✓ python                         2ms
mise ✓ bun                            2ms
mise ✓ cargo:eza                      2ms
mise ✓ fd                             3ms
mise ✓ hugo-extended                  3ms
mise ✓ uv                             3ms
mise ✓ yazi                           3ms
mise ✓ jq                             3ms
mise ✓ aqua:micro-editor/micro        3ms
mise ✓ github:mikefarah/yq            3ms
mise ✓ shellcheck                     3ms
mise ✓ shfmt                          3ms
mise ✓ npm:bash-language-server       3ms
mise ✓ npm:@anthropic-ai/claude-code  3ms
mise ✓ npm:@openai/codex              3ms
mise ✓ npm:ccstatusline               3ms
mise ✓ npm:ccusage                    3ms
mise ✓ github:x-motemen/ghq           3ms
mise ✓ github:shuntaka9576/blocc      3ms
mise ✓ github:cli/cli                 4ms
mise ✓ cargo:pueue                    4ms
mise ✓ github:d-kuro/gwq              4ms
mise ✓ github:ogulcancelik/herdr      4ms
mise ✓ npm:fast-cli                   4ms
mise ✓ npm:pyright                    4ms
mise ✓ http:bats                      4ms
mise ✓ http:gcloud                    4ms
mise ████████████████ 33/33 · resolved 33 tools in 4ms
mise by @jdx – resolving 1 tool
mise ✓ core:rust@1.98.1  1ms
mise ████████████████ 1/1 · resolved 1 tool in 1ms
mise All tools are up to date
mise by @jdx – resolving 33 tools
mise ✓ rust                           2ms
mise ✓ dotenvx                        2ms
mise ✓ node                           2ms
mise ✓ age                            2ms
mise ✓ cmake                          2ms
mise ✓ python                         2ms
mise ✓ bun                            2ms
mise ✓ chezmoi                        2ms
mise ✓ cargo:eza                      2ms
mise ✓ shellcheck                     3ms
mise ✓ fd                             3ms
mise ✓ jq                             3ms
mise ✓ hugo-extended                  3ms
mise ✓ yazi                           3ms
mise ✓ uv                             3ms
mise ✓ github:mikefarah/yq            3ms
mise ✓ npm:bash-language-server       3ms
mise ✓ npm:@openai/codex              3ms
mise ✓ aqua:micro-editor/micro        3ms
mise ✓ shfmt                          3ms
mise ✓ npm:@anthropic-ai/claude-code  3ms
mise ✓ npm:pyright                    3ms
mise ✓ npm:fast-cli                   3ms
mise ✓ github:x-motemen/ghq           3ms
mise ✓ npm:ccusage                    3ms
mise ✓ npm:ccstatusline               3ms
mise ✓ github:d-kuro/gwq              4ms
mise ✓ github:shuntaka9576/blocc      4ms
mise ✓ github:cli/cli                 4ms
mise ✓ github:ogulcancelik/herdr      4ms
mise ✓ cargo:pueue                    4ms
mise ✓ http:bats                      4ms
mise ✓ http:gcloud                    4ms
mise ████████████████ 33/33 · resolved 33 tools in 4ms
mise by @jdx – resolving 1 tool
mise ✓ aqua:koalaman/shellcheck@0.11.0  367ms
mise ████████████████ 1/1 · resolved 1 tool in 367ms
mise All tools are up to date
mise by @jdx – resolving 33 tools
mise ✓ rust                           3ms
mise ✓ dotenvx                        3ms
mise ✓ age                            3ms
mise ✓ chezmoi                        3ms
mise ✓ node                           3ms
mise ✓ bun                            3ms
mise ✓ cmake                          3ms
mise ✓ python                         3ms
mise ✓ cargo:eza                      3ms
mise ✓ shellcheck                     3ms
mise ✓ fd                             3ms
mise ✓ hugo-extended                  3ms
mise ✓ jq                             4ms
mise ✓ yazi                           4ms
mise ✓ aqua:micro-editor/micro        4ms
mise ✓ uv                             4ms
mise ✓ github:mikefarah/yq            4ms
mise ✓ npm:bash-language-server       4ms
mise ✓ shfmt                          4ms
mise ✓ npm:@openai/codex              4ms
mise ✓ npm:@anthropic-ai/claude-code  4ms
mise ✓ npm:pyright                    4ms
mise ✓ npm:ccusage                    4ms
mise ✓ npm:ccstatusline               4ms
mise ✓ npm:fast-cli                   4ms
mise ✓ github:x-motemen/ghq           4ms
mise ✓ github:shuntaka9576/blocc      5ms
mise ✓ github:d-kuro/gwq              5ms
mise ✓ github:cli/cli                 5ms
mise ✓ cargo:pueue                    5ms
mise ✓ github:ogulcancelik/herdr      5ms
mise ✓ http:bats                      5ms
mise ✓ http:gcloud                    5ms
mise ████████████████ 33/33 · resolved 33 tools in 5ms
mise by @jdx – resolving 1 tool
mise ✓ aqua:mvdan/sh@3.14.1  368ms
mise ████████████████ 1/1 · resolved 1 tool in 369ms
mise All tools are up to date
mise by @jdx – resolving 33 tools
mise ✓ rust                           3ms
mise ✓ chezmoi                        3ms
mise ✓ bun                            3ms
mise ✓ python                         3ms
mise ✓ dotenvx                        3ms
mise ✓ cargo:eza                      3ms
mise ✓ age                            3ms
mise ✓ cmake                          3ms
mise ✓ node                           3ms
mise ✓ fd                             3ms
mise ✓ jq                             4ms
mise ✓ hugo-extended                  4ms
mise ✓ yazi                           4ms
mise ✓ shellcheck                     4ms
mise ✓ aqua:micro-editor/micro        4ms
mise ✓ uv                             4ms
mise ✓ github:mikefarah/yq            4ms
mise ✓ npm:bash-language-server       4ms
mise ✓ shfmt                          4ms
mise ✓ npm:@openai/codex              4ms
mise ✓ npm:fast-cli                   4ms
mise ✓ npm:ccstatusline               4ms
mise ✓ npm:@anthropic-ai/claude-code  4ms
mise ✓ npm:pyright                    4ms
mise ✓ npm:ccusage                    4ms
mise ✓ github:x-motemen/ghq           4ms
mise ✓ github:d-kuro/gwq              4ms
mise ✓ cargo:pueue                    5ms
mise ✓ github:shuntaka9576/blocc      5ms
mise ✓ github:ogulcancelik/herdr      5ms
mise ✓ http:gcloud                    5ms
mise ✓ http:bats                      5ms
mise ✓ github:cli/cli                 5ms
mise ████████████████ 33/33 · resolved 33 tools in 5ms
mise by @jdx – resolving 1 tool
mise ✓ aqua:astral-sh/uv@0.12.13  360ms
mise ████████████████ 1/1 · resolved 1 tool in 361ms
mise WARN  newer uv release 0.12.17 (released 2026-09-19, eligible 2026-09-26 03:59 JST) ignored by minimum_release_age (7d); latest eligible release is 0.12.13
mise All tools are up to date
mise by @jdx – resolving 33 tools
mise ✓ rust                           3ms
mise ✓ node                           3ms
mise ✓ age                            3ms
mise ✓ bun                            3ms
mise ✓ python                         3ms
mise ✓ chezmoi                        3ms
mise ✓ cmake                          3ms
mise ✓ dotenvx                        3ms
mise ✓ cargo:eza                      3ms
mise ✓ fd                             3ms
mise ✓ shellcheck                     3ms
mise ✓ hugo-extended                  3ms
mise ✓ yazi                           4ms
mise ✓ aqua:micro-editor/micro        4ms
mise ✓ uv                             4ms
mise ✓ jq                             4ms
mise ✓ github:mikefarah/yq            4ms
mise ✓ shfmt                          4ms
mise ✓ npm:bash-language-server       4ms
mise ✓ npm:@openai/codex              4ms
mise ✓ npm:ccusage                    4ms
mise ✓ npm:ccstatusline               4ms
mise ✓ npm:@anthropic-ai/claude-code  4ms
mise ✓ github:x-motemen/ghq           4ms
mise ✓ npm:pyright                    4ms
mise ✓ npm:fast-cli                   4ms
mise ✓ github:shuntaka9576/blocc      4ms
mise ✓ github:d-kuro/gwq              4ms
mise ✓ cargo:pueue                    5ms
mise ✓ github:ogulcancelik/herdr      5ms
mise ✓ github:cli/cli                 5ms
mise ✓ http:gcloud                    5ms
mise ✓ http:bats                      5ms
mise ████████████████ 33/33 · resolved 33 tools in 5ms
mise by @jdx – resolving 1 tool
mise ✓ aqua:sxyazi/yazi@26.9.1  1.0s
mise ████████████████ 1/1 · resolved 1 tool in 1.0s
mise All tools are up to date

==> agent CLI tools
mise by @jdx – installing 1 tool
mise ⇢ npm:@openai/codex@0.155.1  2ms · already installed
mise ████████████████ 1/1 · installed 0 tools · 1 already installed in 3ms
mise ~/.config/mise/config.toml tools: npm:@openai/codex@0.155.1

changed 2 packages in 2s
Reshimming mise 26.8.2...
mise by @jdx – installing 1 tool
mise ⇢ npm:@anthropic-ai/claude-code@2.1.278  1ms · already installed
mise ████████████████ 1/1 · installed 0 tools · 1 already installed in 2ms
mise ~/.config/mise/config.toml tools: npm:@anthropic-ai/claude-code@2.1.278

changed 2 packages in 1s
Reshimming mise 26.8.2...

==> terminal tool pins
Pinned tode v0.3.4, terminal-browser v0.11.1, and crit v0.20.2; review and commit the installer-pins diff.

==> Claude Code plugins
Updating marketplace: claude-plugins-official...✔ Successfully updated marketplace: claude-plugins-official
Checking for updates for plugin "superpowers@claude-plugins-official" at user scope…
✔ superpowers is already at the latest version (6.3.0).

==> Claude Code Crit plugin
Updating marketplace: crit...Refreshing marketplace cache (timeout: 120s)…
✔ Successfully updated marketplace: crit
Checking for updates for plugin "crit@crit" at user scope…
✔ crit is already at the latest version (1.8.10).
Claude Code Crit plugin is already enabled.

==> Claude Code Ponytail plugin
Updating marketplace: ponytail...Refreshing marketplace cache (timeout: 120s)…
✔ Successfully updated marketplace: ponytail
Checking for updates for plugin "ponytail@ponytail" at user scope…
✔ ponytail is already at the latest version (4.10.0).
Claude Code Ponytail plugin is already enabled.
Ponytail default mode is full. Set PONYTAIL_DEFAULT_MODE=lite|full|ultra|off to override.

==> Claude Code Understand-Anything plugin
Updating marketplace: understand-anything...Refreshing marketplace cache (timeout: 120s)…
✔ Successfully updated marketplace: understand-anything
Checking for updates for plugin "understand-anything@understand-anything" at user scope…
✔ understand-anything is already at the latest version (2.9.7).
Claude Code Understand-Anything plugin is already enabled.

==> Codex plugins
Codex Superpowers plugin installed.

==> Codex Crit plugin
  Installed: /Users/mryfmo/.agents/plugins/marketplace.json
  Installed: .agents/skills/crit/SKILL.md
  Installed: .agents/skills/crit-cli/SKILL.md
  Installed: .agents/skills/crit-story/SKILL.md
  Installed: /Users/mryfmo/.codex/plugins/crit/.codex-plugin/plugin.json
  Installed: /Users/mryfmo/.codex/plugins/crit/skills/crit/SKILL.md
  Installed: /Users/mryfmo/.codex/plugins/crit/skills/crit-cli/SKILL.md
  Installed: /Users/mryfmo/.codex/plugins/crit/skills/crit-story/SKILL.md
  Installed: /Users/mryfmo/.codex/plugins/crit/hooks/hooks.json
  Installed: /Users/mryfmo/.codex/plugins/cache/mryfmo-personal-plugins/crit/local
  Skipped:   /Users/mryfmo/.codex/config.toml (Codex plugin already enabled)
  Use $crit in Codex to start a review loop
  The crit-cli skill is available to Codex agents when needed
  Use $crit-story in Codex to author a story and continue the review loop
  The Crit plugin is registered in the local Codex plugin marketplace
  The plugin-packaged crit skill is available to Codex as $crit:crit
  The plugin-packaged crit-cli skill is available to Codex agents when needed
  The plugin-packaged crit-story skill is available to Codex as $crit-story
  The Crit plugin includes a Codex Stop hook for proposed-plan review
  The Crit Codex plugin is enabled as crit@mryfmo-personal-plugins


==> Codex Ponytail plugin
Marketplace `ponytail` is already up to date.
Codex Ponytail plugin is already installed.
Review and trust Ponytail lifecycle hooks in Codex with /hooks, then start a new thread.
Ponytail default mode is full. Set PONYTAIL_DEFAULT_MODE=lite|full|ultra|off to override.

==> Codex Understand-Anything skills
→ Updating existing checkout at /Users/mryfmo/.understand-anything/repo
Already up to date.
→ Linking skills for codex (per-skill → /Users/mryfmo/.agents/skills)
  ✓ /Users/mryfmo/.agents/skills/understand-chat → /Users/mryfmo/.understand-anything/repo/understand-anything-plugin/skills/understand-chat
  ✓ /Users/mryfmo/.agents/skills/understand-dashboard → /Users/mryfmo/.understand-anything/repo/understand-anything-plugin/skills/understand-dashboard
  ✓ /Users/mryfmo/.agents/skills/understand-diff → /Users/mryfmo/.understand-anything/repo/understand-anything-plugin/skills/understand-diff
  ✓ /Users/mryfmo/.agents/skills/understand-domain → /Users/mryfmo/.understand-anything/repo/understand-anything-plugin/skills/understand-domain
  ✓ /Users/mryfmo/.agents/skills/understand-explain → /Users/mryfmo/.understand-anything/repo/understand-anything-plugin/skills/understand-explain
  ✓ /Users/mryfmo/.agents/skills/understand-figma → /Users/mryfmo/.understand-anything/repo/understand-anything-plugin/skills/understand-figma
  ✓ /Users/mryfmo/.agents/skills/understand-knowledge → /Users/mryfmo/.understand-anything/repo/understand-anything-plugin/skills/understand-knowledge
  ✓ /Users/mryfmo/.agents/skills/understand-onboard → /Users/mryfmo/.understand-anything/repo/understand-anything-plugin/skills/understand-onboard
  ✓ /Users/mryfmo/.agents/skills/understand → /Users/mryfmo/.understand-anything/repo/understand-anything-plugin/skills/understand
→ Linking universal plugin root
  • /Users/mryfmo/.understand-anything-plugin already exists, leaving as-is

✓ Installed Understand-Anything for codex
  Restart your CLI or IDE to pick up the skills.

  Tip: Codex invokes skills with $ instead of / — type $understand, not /understand.
Invoke Understand-Anything in Codex with $understand after restarting the CLI.

==> terminal-code (tode)
tode v0.3.4 is already installed.

==> terminal-browser
terminal-browser v0.11.1 is already installed.

==> herdr integrations
installed claude integration hook to /Users/mryfmo/.claude/hooks/herdr-agent-state.sh
ensured claude settings at /Users/mryfmo/.claude/settings.json
installed codex integration hook to /Users/mryfmo/.codex/herdr-agent-state.sh
ensured codex hooks at /Users/mryfmo/.codex/hooks.json
ensured codex config at /Users/mryfmo/.codex/config.toml

==> uv tools
Nothing to upgrade

==> GitHub CLI extensions
[poi]: already up to date

==> Claude Code Router adoption gate
CCR gate G1 (#1115): open
CCR latest release: v3.1.1
CCR gates G2/G3 require manual primary-source verification before any canary.

Upgrade summary: required failures: 0; optional warnings: 0
/Library/Developer/CommandLineTools/usr/bin/make agmsg-bootstrap
First-time Claude Code agmsg setup may stop one same-repo watcher once; the hooks apply in the next Claude Code session.
No agmsg Claude Code identity for /Users/mryfmo/Workspace/dotfiles/.claude/worktrees/upgrade-regen; run: /Users/mryfmo/.agents/skills/agmsg/scripts/join.sh <team> <agent-name> claude-code "/Users/mryfmo/Workspace/dotfiles/.claude/worktrees/upgrade-regen"
```

## Initial unittest attempt blocked by sandbox (exit 2)

```text
error: Failed to initialize cache at `/Users/mryfmo/.cache/uv`
  Caused by: failed to open file `/Users/mryfmo/.cache/uv/sdists-v9/.git`: Operation not permitted (os error 1)
```

## Required unittest with uv cache access (exit 0)

```text
.................
----------------------------------------------------------------------
Ran 17 tests in 0.878s

OK
```

## Final repository checks

```text
$ git diff --check
exit=0

$ git diff --name-only
home/dot_mise/config.toml
home/dot_mise/mise.lock
exit=0

$ cmp /tmp/dot-upgrade-regen-installer-pins.before.sh scripts/lib/installer-pins.sh
exit=0

$ git status --short
 M home/dot_mise/config.toml
 M home/dot_mise/mise.lock
?? .orchestration/autoskill/runs/dot-upgrade-regen-T1-a01.md
?? .orchestration/learning/dot-upgrade-regen-T1-a01.md
?? .orchestration/reports/dot-upgrade-regen-T1-a01.md
?? .orchestration/sandboxes/dot-upgrade-regen-T1-a01.md
?? .orchestration/tasks/dot-upgrade-regen-T1-a01.md
exit=0

$ shasum -a 256 home/dot_mise/config.toml home/dot_mise/mise.lock scripts/lib/installer-pins.sh
dae20a74af53e3a0d1246679e5680743db773cf8da90522899c9c2713aaae8a1  home/dot_mise/config.toml
f8ec41fa766ed0e117b88ce20ac0f6f3b98037beb50db4347fa7e3e1143ed541  home/dot_mise/mise.lock
2bf6d7f6eadf6a98670ccb599133c29c255ec568b316c9b98bd2fde8b5fe1669  scripts/lib/installer-pins.sh
exit=0
```

## CompactionDB memory verification

```text
da6cdf40-7e32-4480-9b50-7d394ad7d838 [project/decision] confidence=1.00 salience=0.90 dot-upgrade-regen-T1-a01: Mac make upgrade regenerated home/dot_mise/config.toml and mise.lock for the chore change; installer-pins.sh remained unchanged. Because ~/.config/mise config and lock symlink to the normal checkout, a dedicated worktree must copy the regenerated pair from those symlink targets before review.
```

## Agent review gate

Initial gate:

```text
Native agent review required before completion.
- broad diff touches 8 files
- broad diff changes 3725 lines
Use the active agent's review path, not a browser by default:
- Codex: retrieve Crit comments/status data, review it inside the task, then address findings.
- Claude Code: retrieve Crit comments/status data, review it inside the task, then address findings.
- Use browser Crit review only when the user explicitly asks for Crit web UI or Crit data is unavailable.
Record a receipt with `review_surface:`, `reviewer:`, and `review_outcome:`.
For agent judgment, locate the review with `crit status --json`, then save `crit comments --all --json <review.json>` to a repo-local JSON file.
Evidence must contain at least one resolved record; for a finding-free review, add and resolve one review-scope approval record.
This local evidence is process evidence, not reviewer authentication.
Then use `review_surface: crit-data`, `reviewer: codex` or `reviewer: claude-code`, and `review_source: <json path>`.
After addressing review feedback, rerun with AGENT_REVIEWED=1 or CRIT_REVIEWED=1 plus REVIEW_EVIDENCE=<path>.
make: *** [require-crit-review] Error 1
```

Receipt-format correction run:

```text
AGENT_REVIEWED=1 requires review evidence before completion.
- REVIEW_EVIDENCE agent reviewer requires `review_outcome: approved` or `review_outcome: addressed`
make: *** [require-crit-review] Error 1
```

Final gate:

```text
Review requirement satisfied by AGENT_REVIEWED=1 with REVIEW_EVIDENCE.
```

Final superseding-revision completion check:

```text
git_diff_check
exit=0

changed_files
.github/workflows/test.yaml
.orchestration/learning/dot-upgrade-regen-T1-a01.md
.orchestration/reports/dot-upgrade-regen-T1-a01.md
.orchestration/validation/dot-upgrade-regen-T1-a01.md
scripts/check-statusline-tools.py
tests/install/common/mise.bats
tests/unit/test_statusline_tools.py

old_runtime_tree_occurrences
./home/dot_local/bin/common/executable_herdr-agents:70:# @description Derive and validate a herdr 0.8.2 agent registration name.

active_todos

review_gate
Review requirement satisfied by AGENT_REVIEWED=1 with REVIEW_EVIDENCE.
```

## Superseding CI consumer revision

Initial system-Python YAML attempt (exit 1):

```text
Traceback (most recent call last):
  File "<string>", line 1, in <module>
    from pathlib import Path; import yaml; files=sorted(Path(".github/workflows").glob("*.yaml")); [yaml.safe_load(path.read_text()) for path in files]; print(f"parsed {len(files)} workflow YAML files")
                              ^^^^^^^^^^^
ModuleNotFoundError: No module named 'yaml'
```

PyYAML validation after the mise-action-only revision (exit 0):

```text
parsed 6 workflow YAML files
```

Focused statusline test before exact-consumer updates (exit 1):

```text
...F.
======================================================================
FAIL: test_mise_config_and_lock_pin_exact_npm_versions (tests.unit.test_statusline_tools.StatuslineToolsTest.test_mise_config_and_lock_pin_exact_npm_versions)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/mryfmo/Workspace/dotfiles/.claude/worktrees/upgrade-regen/tests/unit/test_statusline_tools.py", line 37, in test_mise_config_and_lock_pin_exact_npm_versions
    self.assertEqual(config["tools"] | EXPECTED_TOOLS, config["tools"])
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: {'nod[568 chars]2.2.27', 'npm:ccusage': '20.0.19', 'npm:pyrigh[1422 chars]'}}}} != {'nod[568 chars]2.2.29', 'npm:ccusage': '20.0.20', 'npm:pyrigh[1422 chars]'}}}}
Diff is 2761 characters long. Set self.maxDiff to None to see it.

----------------------------------------------------------------------
Ran 5 tests in 0.037s

FAILED (failures=1)
```

Focused statusline test after exact-consumer updates (exit 0):

```text
.....
----------------------------------------------------------------------
Ran 5 tests in 0.045s

OK
```

Supply-chain policy test after revision (exit 0):

```text
.................
----------------------------------------------------------------------
Ran 17 tests in 0.375s

OK
```

Final PyYAML validation (exit 0):

```text
parsed 6 workflow YAML files
```

Old-version runtime-consumer scan and diff check:

```text
runtime_consumer_old_versions
./home/dot_local/bin/common/executable_herdr-agents:70:# @description Derive and validate a herdr 0.8.2 agent registration name.

diff_check
exit=0
```

Revision CompactionDB memory verification:

```text
0578538c-58fa-4da5-a467-a4e6aae4dd3d [project/decision] confidence=1.00 salience=0.90 dot-upgrade-regen-T1-a01 revision: CI exact-version consumers must advance with regenerated mise pins. test.yaml now uses mise-action 2026.9.12, ccstatusline 2.2.29, and ccusage 20.0.20; Python smoke expectations match; the mise.bats herdr assertion matches 0.9.0.
```

Revision agent review gate:

```text
Review requirement satisfied by AGENT_REVIEWED=1 with REVIEW_EVIDENCE.
```

## Final completion checks

```text
git_diff_check_exit=0

tracked_diff_names
home/dot_mise/config.toml
home/dot_mise/mise.lock

worktree_status
 M home/dot_mise/config.toml
 M home/dot_mise/mise.lock
?? .orchestration/autoskill/runs/dot-upgrade-regen-T1-a01.md
?? .orchestration/learning/dot-upgrade-regen-T1-a01.md
?? .orchestration/reports/dot-upgrade-regen-T1-a01.md
?? .orchestration/sandboxes/dot-upgrade-regen-T1-a01.md
?? .orchestration/tasks/dot-upgrade-regen-T1-a01.md
?? .orchestration/validation/dot-upgrade-regen-T1-a01.md

active_todos

artifacts
present .orchestration/reports/dot-upgrade-regen-T1-a01.md
present .orchestration/validation/dot-upgrade-regen-T1-a01.md
present .orchestration/sandboxes/dot-upgrade-regen-T1-a01.md
present .orchestration/learning/dot-upgrade-regen-T1-a01.md
present .orchestration/autoskill/runs/dot-upgrade-regen-T1-a01.md
Review requirement satisfied by AGENT_REVIEWED=1 with REVIEW_EVIDENCE.
```

## Node-first workflow revision

Focused test before workflow change (exit 1):

```text
F....
======================================================================
FAIL: test_ci_smokes_exact_tools_with_network_denied (tests.unit.test_statusline_tools.StatuslineToolsTest.test_ci_smokes_exact_tools_with_network_denied)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/mryfmo/Workspace/dotfiles/.claude/worktrees/upgrade-regen/tests/unit/test_statusline_tools.py", line 112, in test_ci_smokes_exact_tools_with_network_denied
    self.assertIn(token, workflow)
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
AssertionError: 'mise -C "${RUNNER_TEMP}/statusline-mise" install --locked node' not found in 'name: Unit test\n\non:\n  # Required checks must always report a final status for PRs into `main`.\n  # Do not add workflow-level path or branch filters here: GitHub can leave\n  # skipped required checks in a pending state and block merges.\n  # Keep this workflow unconditional and decide inside jobs whether the full\n  # test matrix is necessary for the current diff.\n  push:\n    branches: [main]\n  pull_request:\n    branches: [main]\npermissions:\n  contents: read\n\njobs:\n  changes:\n    runs-on: ubuntu-latest\n    outputs:\n      should_test: ${{ steps.filter.outputs.should_test }}\n      should_nix: ${{ steps.filter.outputs.should_nix }}\n      diff_range: ${{ steps.filter.outputs.diff_range }}\n\n    steps:\n      - name: Configure Git defaults\n        run: git config --global init.defaultBranch main\n\n      - name: Checkout repository\n        uses: actions/checkout@9c091bb21b7c1c1d1991bb908d89e4e9dddfe3e0 # v7\n        with:\n          fetch-depth: 0\n          persist-credentials: false\n\n      - name: Detect unit-test-relevant changes\n        id: filter\n        env:\n          EVENT_NAME: ${{ github.event_name }}\n          BASE_REF: ${{ github.base_ref }}\n          BEFORE_SHA: ${{ github.event.before }}\n          HEAD_SHA: ${{ github.sha }}\n        run: |\n          set -euo pipefail\n\n          # Keep the diff calculation here so the required workflow can always\n          # start and report a final status before we decide whether to run the\n          # heavier test steps.\n          if [ "${EVENT_NAME}" = "pull_request" ]; then\n            git fetch --no-tags --depth=1 origin "${BASE_REF}"\n            diff_range="origin/${BASE_REF}...${HEAD_SHA}"\n          elif [ -n "${BEFORE_SHA}" ] && [ "${BEFORE_SHA}" != "0000000000000000000000000000000000000000" ]; then\n            diff_range="${BEFORE_SHA}...${HEAD_SHA}"\n          else\n            diff_range="${HEAD_SHA}^...${HEAD_SHA}"\n          fi\n\n          echo "diff_range=${diff_range}" >> "${GITHUB_OUTPUT}"\n\n          # One option would be to predefine CI-relevant path groups such as\n          # `.github/workflows/`, `home/`, `install/`, and `tests/` in an env-\n          # var-like form to make the rule reusable. For this workflow, keeping\n          # the pattern inline is still easier to read because the rule is only\n          # used once and only decides whether the expensive unit-test steps\n          # should run. It does not decide whether the required workflow itself\n          # reports a status. If more workflows need the same rule later,\n          # extract a shared script instead of hiding the pattern in env.\n          if git diff --name-only "${diff_range}" | grep -Eq \'^(\\.github/workflows/|home/|install/|scripts/|tests/|setup\\.sh$|Makefile$|README\\.md$)\'; then\n            echo "should_test=true" >> "${GITHUB_OUTPUT}"\n          else\n            echo "should_test=false" >> "${GITHUB_OUTPUT}"\n          fi\n\n          if git diff --name-only "${diff_range}" | grep -Eq \'^(flake\\.(nix|lock)$|nix/)\'; then\n            echo "should_nix=true" >> "${GITHUB_OUTPUT}"\n          else\n            echo "should_nix=false" >> "${GITHUB_OUTPUT}"\n          fi\n\n  test:\n    needs: changes\n    # Run the same test suite on each target OS/system pair.\n    # We intentionally keep macOS as `client` only because this repository\n    # does not define a macOS `server` test target.\n    strategy:\n      matrix:\n        os: [ubuntu-latest, macos-14]\n        system: [client, server]\n        exclude:\n          - os: macos-14\n            system: server\n\n    runs-on: ${{ matrix.os }}\n    env:\n      # Export matrix values to shell scripts so existing test helpers can use\n      # simple `OS`/`SYSTEM` checks without depending on GitHub expression syntax.\n      OS: ${{ matrix.os }}\n      SYSTEM: ${{ matrix.system }}\n      # Keep Codecov naming deterministic per job. This makes it easy to trace\n      # upload sessions in Codecov API/UI and avoids accidental session overlap.\n      CODECOV_FLAGS: ${{ matrix.os }}-${{ matrix.system }}\n      CODECOV_NAME: codecov-dotfiles-${{ matrix.os }}-${{ matrix.system }}\n      GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}\n\n    steps:\n      - name: Configure Git defaults\n        run: git config --global init.defaultBranch main\n\n      - name: Checkout repository\n        uses: actions/checkout@9c091bb21b7c1c1d1991bb908d89e4e9dddfe3e0 # v7\n        with:\n          persist-credentials: false\n\n      - name: Skip full unit test run for unrelated changes\n        if: ${{ needs.changes.outputs.should_test != \'true\' }}\n        run: |\n          echo "No unit-test-relevant files changed."\n          echo "Compared diff range: ${{ needs.changes.outputs.diff_range }}"\n\n      - name: Install tools\n        if: ${{ needs.changes.outputs.should_test == \'true\' }}\n        run: |\n          if [ "${OS}" == "macos-14" ]; then\n            # GitHub macOS runners can include preconfigured taps that Homebrew\n            # warns about during install operations. Trust them explicitly so CI\n            # logs stay warning-clean as Homebrew tightens tap trust defaults.\n            brew trust aws/tap azure/bicep || true\n\n            # `bashcov` on macOS must use Homebrew Bash (>=5) to avoid the\n            # system Bash 3.2 parser limitations that produced empty coverage.\n            # `gawk` is available for shell tooling used by the test suite.\n            # `chezmoi` is installed so Bats can render chezmoi templates\n            # behaviorally instead of grepping template syntax.\n            brew install bash bats-core chezmoi gawk parallel shellcheck\n\n          elif [ "${OS}" == "ubuntu-latest" ]; then\n            # Ruby is required for bashcov/simplecov formatters. Install chezmoi\n            # explicitly so template tests can verify rendered behavior.\n            sudo apt-get update && sudo apt-get install -y bats curl iproute2 parallel ruby shellcheck\n            chezmoi_version=2.70.5\n            artifact="chezmoi_${chezmoi_version}_linux_amd64.tar.gz"\n            base_url="https://github.com/twpayne/chezmoi/releases/download/v${chezmoi_version}"\n            curl -fsSL "${base_url}/${artifact}" -o "${RUNNER_TEMP}/${artifact}"\n            curl -fsSL "${base_url}/chezmoi_${chezmoi_version}_checksums.txt" \\\n              | grep "  ${artifact}$" \\\n              | (cd "${RUNNER_TEMP}" && sha256sum --check --strict)\n            tar -xzf "${RUNNER_TEMP}/${artifact}" -C "${RUNNER_TEMP}" chezmoi\n            sudo install -m 0755 "${RUNNER_TEMP}/chezmoi" /usr/local/bin/chezmoi\n\n          else\n            echo "${OS} and ${SYSTEM} are not supported" >&2\n            exit 1\n          fi\n\n          files_test_chezmoi="$(command -v chezmoi)"\n          case "${files_test_chezmoi}" in\n            /*/mise/shims/*|"")\n              echo "Files test chezmoi must resolve outside mise shims: ${files_test_chezmoi:-missing}" >&2\n              exit 1\n              ;;\n            /*) ;;\n            *)\n              echo "Files test chezmoi must be an absolute path: ${files_test_chezmoi}" >&2\n              exit 1\n              ;;\n          esac\n          test -x "${files_test_chezmoi}"\n          printf \'FILES_TEST_CHEZMOI=%s\\n\' "${files_test_chezmoi}" >> "${GITHUB_ENV}"\n\n          # Install coverage tooling as user gems and expose gem bin dir on PATH\n          # before installation so RubyGems can expose executables immediately.\n          # `--no-document` keeps CI faster and deterministic.\n          gem_bin_dir="$(ruby -r rubygems -e \'puts Gem.user_dir\')/bin"\n          echo "${gem_bin_dir}" >> "${GITHUB_PATH}"\n          export PATH="${gem_bin_dir}:${PATH}"\n          gem install --user-install --no-document bashcov --version 3.3.0\n          gem install --user-install --no-document simplecov-cobertura --version 3.1.0\n\n      - name: Prepare exact statusline tool config\n        if: ${{ needs.changes.outputs.should_test == \'true\' }}\n        run: |\n          statusline_mise_dir="${RUNNER_TEMP}/statusline-mise"\n          mkdir -p "${statusline_mise_dir}"\n          cp home/dot_mise/config.toml "${statusline_mise_dir}/mise.toml"\n          cp home/dot_mise/mise.lock "${statusline_mise_dir}/mise.lock"\n\n      - name: Setup mise for statusline smoke\n        if: ${{ needs.changes.outputs.should_test == \'true\' }}\n        uses: jdx/mise-action@e6a8b3978addb5a52f2b4cd9d91eafa7f0ab959d # v4\n        with:\n          version: 2026.9.12\n          install: false\n          cache: true\n\n      - name: Install exact statusline tools\n        if: ${{ needs.changes.outputs.should_test == \'true\' }}\n        run: |\n          mise trust --yes "${RUNNER_TEMP}/statusline-mise/mise.toml"\n          mise -C "${RUNNER_TEMP}/statusline-mise" install --locked \\\n            npm:ccstatusline@2.2.29 \\\n            npm:ccusage@20.0.20\n\n      - name: Smoke-test statusline tools without network\n        if: ${{ needs.changes.outputs.should_test == \'true\' }}\n        run: |\n          set -euo pipefail\n\n          statusline_mise_dir="${RUNNER_TEMP}/statusline-mise"\n          ccstatusline_bin="$(mise -C "${statusline_mise_dir}" which ccstatusline)"\n          ccusage_bin="$(mise -C "${statusline_mise_dir}" which ccusage)"\n          ccstatusline_root="$(mise -C "${statusline_mise_dir}" where npm:ccstatusline@2.2.29)"\n          ccusage_root="$(mise -C "${statusline_mise_dir}" where npm:ccusage@20.0.20)"\n\n          case "${ccstatusline_bin}" in\n            "${ccstatusline_root}"/*) ;;\n            *) echo "ccstatusline did not resolve from mise\'s exact install" >&2; exit 1 ;;\n          esac\n          case "${ccusage_bin}" in\n            "${ccusage_root}"/*) ;;\n            *) echo "ccusage did not resolve from mise\'s exact install" >&2; exit 1 ;;\n          esac\n\n          smoke_home="${RUNNER_TEMP}/statusline-smoke-home"\n          mkdir -p "${smoke_home}"\n          smoke=(\n            /usr/bin/env\n            "HOME=${smoke_home}"\n            "PATH=${PATH}"\n            "HTTP_PROXY=http://127.0.0.1:1"\n            "HTTPS_PROXY=http://127.0.0.1:1"\n            NO_PROXY=\n            python3 scripts/check-statusline-tools.py\n            --ccstatusline "${ccstatusline_bin}"\n            --ccusage "${ccusage_bin}"\n          )\n\n          if [ "${OS}" = "ubuntu-latest" ]; then\n            sudo unshare --net -- sh -c \'test -z "$(ip route show)"\'\n            sudo unshare --net -- "${smoke[@]}"\n          elif [ "${OS}" = "macos-14" ]; then\n            sandbox_profile=\'(version 1)(allow default)(deny network*)\'\n            if /usr/bin/sandbox-exec -p "${sandbox_profile}" \\\n              python3 -c \'import socket; s = socket.socket(); s.bind(("127.0.0.1", 0))\'; then\n              echo "macOS network-denial oracle unexpectedly bound a socket" >&2\n              exit 1\n            fi\n            /usr/bin/sandbox-exec -p "${sandbox_profile}" "${smoke[@]}"\n          else\n            echo "${OS} is not supported" >&2\n            exit 1\n          fi\n\n      - name: Run `shfmt`\n        if: ${{ needs.changes.outputs.should_test == \'true\' }}\n        run: |\n          # shfmt is version-pinned via mise: brew/apt ship divergent versions\n          # (3.14 changed heredoc-in-if formatting) and unpinned runners disagree.\n          git ls-files -- \':(glob)install/**/*.sh\' \':(glob)scripts/**/*.sh\' | xargs mise x shfmt@3.14.1 -- shfmt -i 4 -sr -d\n\n      - name: Run `ShellCheck`\n        if: ${{ needs.changes.outputs.should_test == \'true\' }}\n        run: |\n          git ls-files -z \'setup.sh\' \'install/*.sh\' \'install/**/*.sh\' \'scripts/*.sh\' | xargs -0 shellcheck -x\n\n      - name: Setup uv\n        if: ${{ needs.changes.outputs.should_test == \'true\' }}\n        uses: astral-sh/setup-uv@37802adc94f370d6bfd71619e3f0bf239e1f3b78 # v7\n        with:\n          enable-cache: false\n\n      - name: Run Python unit tests\n        if: ${{ needs.changes.outputs.should_test == \'true\' }}\n        run: |\n          if [ "${OS}" == "ubuntu-latest" ]; then\n            sudo apt-get update && sudo apt-get install -y jq zsh\n          elif [ "${OS}" == "macos-14" ]; then\n            command -v jq > /dev/null 2>&1 || brew install jq\n            command -v zsh > /dev/null 2>&1 || brew install zsh\n          fi\n\n          make unit-test\n\n      - name: Prepare public dotfiles fixture\n        if: ${{ needs.changes.outputs.should_test == \'true\' }}\n        run: |\n          set -euo pipefail\n\n          files_test_home="${RUNNER_TEMP}/dotfiles-files-${OS}-${SYSTEM}"\n          files_test_source="${RUNNER_TEMP}/dotfiles-public-source-${OS}-${SYSTEM}"\n          files_test_config="${files_test_home}/.config/chezmoi/chezmoi.yaml"\n          if [ -e "${files_test_source}" ]; then\n            echo "Fixture source already exists: ${files_test_source}" >&2\n            exit 1\n          fi\n          cp -R "${GITHUB_WORKSPACE}/home" "${files_test_source}"\n          rm -f "${files_test_source}/.chezmoiexternal.yaml.tmpl"\n          rm -rf "${files_test_source}/.chezmoitemplates/chezmoiexternal.d"\n          mkdir -p "${files_test_home}" "$(dirname "${files_test_config}")"\n          printf \'sourceDir: "%s"\\ndata:\\n  email: "ci@example.invalid"\\n  system: "%s"\\n\' \\\n            "${files_test_source}" "${SYSTEM}" > "${files_test_config}"\n\n          # Remove external definitions only from the fixture copy, then apply\n          # everything else so role-specific ignores determine both boundaries.\n          # Regenerate the full config from its managed template first so\n          # subsequent `chezmoi diff` output contains only target drift.\n          CI=true HOME="${files_test_home}" "${FILES_TEST_CHEZMOI}" \\\n            --source "${files_test_source}" \\\n            --destination "${files_test_home}" \\\n            --config "${files_test_config}" \\\n            init\n          HOME="${files_test_home}" "${FILES_TEST_CHEZMOI}" \\\n            --source "${files_test_source}" \\\n            --destination "${files_test_home}" \\\n            --config "${files_test_config}" \\\n            --refresh-externals=never \\\n            apply --exclude=scripts,externals\n          {\n            printf \'FILES_TEST_HOME=%s\\n\' "${files_test_home}"\n            printf \'FILES_TEST_SOURCE=%s\\n\' "${files_test_source}"\n            printf \'FILES_TEST_CONFIG=%s\\n\' "${files_test_config}"\n          } >> "${GITHUB_ENV}"\n\n      - name: Run unit test\n        if: ${{ needs.changes.outputs.should_test == \'true\' }}\n        run: |\n          if [ "${OS}" == "macos-14" ]; then\n            # Bats uses its own tracing internals on macOS, and bashcov can\n            # misread those records as coverage trace entries. Keep macOS in\n            # the test matrix for platform validation, but collect Codecov\n            # reports from the Ubuntu jobs where bashcov parses Bats output\n            # reliably.\n            ./scripts/run_unit_test.sh\n            exit 0\n          fi\n\n          # Shared bashcov defaults:\n          # - `--skip-uncovered`: limit report to executed files.\n          # - `--root .`: normalize paths relative to repository root.\n          bashcov_args=(--skip-uncovered --root .)\n\n          # Use a unique command name per matrix job so SimpleCov keeps each\n          # session separated before Codecov merges by flag/name.\n          BASHCOV_COMMAND_NAME="unit-test-${OS}-${SYSTEM}" \\\n            ruby ./scripts/run_bashcov_unit_test.rb "${bashcov_args[@]}" -- ./scripts/run_unit_test.sh\n\n      - name: Setup for Codecov\n        if: ${{ needs.changes.outputs.should_test == \'true\' && matrix.os == \'ubuntu-latest\' && !endsWith(github.actor, \'[bot]\') }}\n        run: |\n          # codecov-action uses these tools while preparing and uploading the\n          # explicit Cobertura report in this repository setup.\n          sudo apt-get install -y jq curl\n\n      - name: Upload coverage to Codecov\n        if: ${{ needs.changes.outputs.should_test == \'true\' && matrix.os == \'ubuntu-latest\' && !endsWith(github.actor, \'[bot]\') }}\n        uses: codecov/codecov-action@fb8b3582c8e4def4969c97caa2f19720cb33a72f # v7\n        env:\n          CODECOV_TOKEN: ${{ secrets.CODECOV_TOKEN }}\n        with:\n          files: ./coverage/coverage.xml\n          # Upload only the explicit report file generated in this workflow.\n          # This prevents unexpected auto-discovery from old/temporary files.\n          disable_search: true\n          env_vars: OS,SYSTEM\n          fail_ci_if_error: false\n          flags: ${{ env.CODECOV_FLAGS }}\n          name: ${{ env.CODECOV_NAME }}\n          # Avoid language auto-discovery warnings for gcov/coverage.py in this\n          # shell-only workflow; upload the explicit Cobertura report only.\n          plugins: noop\n          # Use the PyPI-distributed CLI in CI to avoid non-actionable GPG trust\n          # warnings emitted by the standalone binary signature verifier.\n          use_pypi: true\n          verbose: false\n\n  nix:\n    needs: changes\n    if: ${{ needs.changes.outputs.should_nix == \'true\' }}\n    strategy:\n      fail-fast: false\n      matrix:\n        os: [ubuntu-latest, macos-14]\n    runs-on: ${{ matrix.os }}\n    steps:\n      - name: Checkout repository\n        uses: actions/checkout@9c091bb21b7c1c1d1991bb908d89e4e9dddfe3e0 # v7\n        with:\n          persist-credentials: false\n\n      - name: Install Nix\n        uses: cachix/install-nix-action@a49548c11d9846ad46ecc0115273879b045f001c # v31\n\n      - name: Evaluate flake outputs\n        run: |\n          nix flake check --no-build --no-update-lock-file\n          nix eval --no-update-lock-file .#homeConfigurations.mryfmo-linux.activationPackage.drvPath\n          nix eval --no-update-lock-file .#homeConfigurations.mryfmo-darwin.activationPackage.drvPath\n          nix eval --no-update-lock-file .#darwinConfigurations.mryfmo-mac.system.drvPath\n'

----------------------------------------------------------------------
Ran 5 tests in 0.042s

FAILED (failures=1)
```

Focused test after workflow change (exit 0):

```text
.....
----------------------------------------------------------------------
Ran 5 tests in 0.045s

OK
```

Supply-chain test after node-first revision (exit 0):

```text
.................
----------------------------------------------------------------------
Ran 17 tests in 0.355s

OK
```

Workflow YAML parse after node-first revision (exit 0):

```text
parsed 6 workflow YAML files
```

Focused test after formatting the ordering assertion (exit 0):

```text
.....
----------------------------------------------------------------------
Ran 5 tests in 0.033s

OK
```

Node-first completion checks:

```text
git_diff_check
exit=0

changed_files
.github/workflows/test.yaml
.orchestration/learning/dot-upgrade-regen-T1-a01.md
.orchestration/reports/dot-upgrade-regen-T1-a01.md
.orchestration/validation/dot-upgrade-regen-T1-a01.md
tests/unit/test_statusline_tools.py

active_todos

memory_verification
f2e8be05-427a-4c7d-894c-98d2ec4a4f24 [project/decision] confidence=1.00 salience=0.90 dot-upgrade-regen-T1-a01 node-first revision: mise 2026.9.12 requires configured install dependency node@26.8.2 to be installed before locked npm statusline tools in the isolated CI mise directory; test.yaml now mirrors run_mise_install ordering and the unit test asserts it.

review_gate
Review requirement satisfied by AGENT_REVIEWED=1 with REVIEW_EVIDENCE.
```
