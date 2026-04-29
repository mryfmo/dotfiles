# Nix-first architecture plan

This document describes the intended direction for an optional Nix layer in this dotfiles repository. It is a plan, not the default bootstrap path.

## Current authority model

- `setup.sh` and chezmoi remain the default and authoritative bootstrap path.
- Public dotfiles under `home/` remain managed by chezmoi.
- Private dotfiles and secrets remain outside this repository in the private chezmoi source.
- The new Nix files are opt-in and should not change existing machines unless a user explicitly runs Home Manager or nix-darwin commands.

## Initial Nix scope

The initial scaffold provides:

- A flake with Home Manager standalone outputs:
  - `mryfmo-linux`
  - `mryfmo-darwin`
- A nix-darwin output:
  - `mryfmo-mac`
- A shared conservative package list based mostly on the existing mise, apt, and Homebrew bootstrap intent.
- A development shell with Nix-related tooling.
- A formatter output for `nix fmt`.

The initial Home Manager module intentionally manages only packages and Home Manager metadata. It must not define `home.file` or `xdg.configFile` for paths already represented in `home/`, because those files are currently owned by chezmoi.

## Package ownership

Near-term package ownership can be split as follows:

- Chezmoi remains responsible for configuration files, scripts, and templates.
- Nix may install a conservative base toolset such as Git, GnuPG, Vim, Zsh, tmux, CMake, jq, yq, fd, eza, uv, ShellCheck, shfmt, Starship, chezmoi, age, GitHub CLI, Rust via rustup, Node.js, Python 3.11, ripgrep, yazi, and AWS CLI when available.
- Existing mise usage may continue for project-local language versions and tools that are not yet migrated. If both Nix and mise provide Rust, Node.js, or Python, mise remains the project-specific version selector while Nix provides only the baseline interactive toolchain. Go is intentionally not part of the default Nix package set.

## Future target

A fuller Nix-first design may eventually move these areas into Nix after explicit migration decisions:

- Language toolchains and developer CLIs currently installed by mise.
- macOS package declarations currently installed manually or through Homebrew.
- Linux packages currently installed through apt scripts.
- Machine roles such as client, server, or work-specific hosts.

Configuration files should move from chezmoi to Home Manager only after collision risks are resolved and rollback behavior is documented.

## Activation examples

Home Manager standalone on Linux:

```shell
nix run github:nix-community/home-manager/release-25.05 -- switch --flake .#mryfmo-linux
```

Home Manager standalone on Apple Silicon macOS:

```shell
nix run github:nix-community/home-manager/release-25.05 -- switch --flake .#mryfmo-darwin
```

nix-darwin on Apple Silicon macOS:

```shell
sudo darwin-rebuild switch --flake .#mryfmo-mac
```

The nix-darwin configuration enables Homebrew management, but `homebrew.enable` does not install Homebrew itself. Install Homebrew before activating nix-darwin if Homebrew management is needed.

## Non-goals for the initial scaffold

- Do not replace `setup.sh`.
- Do not migrate existing files under `home/` into Home Manager.
- Do not add private secrets, host-specific credentials, SSH keys, GnuPG secret keyrings, or VPN profiles.
- Do not remove chezmoi as the default source of truth.
