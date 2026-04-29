# Nix migration plan

This plan keeps Nix optional while introducing a path toward reproducible package and host management.

## Principles

1. Preserve existing behavior by default.
   - `setup.sh` remains the normal bootstrap entry point.
   - `chezmoi apply` remains authoritative for files in `home/`.
2. Keep public and private state separate.
   - Public dotfiles stay in this repository.
   - Private files and secrets stay in the private chezmoi source or on the target host.
3. Avoid file ownership collisions.
   - Do not add Home Manager `home.file` or `xdg.configFile` entries for existing chezmoi-managed paths until they are deliberately migrated.
4. Make every migration reversible.
   - Document the owner of each migrated package or config path.
   - Prefer small changes that can be rolled back independently.

## Phase 0: Opt-in scaffold

Status: initial implementation.

- Add `flake.nix`.
- Add a shared package module at `nix/shared/packages.nix`.
- Add a minimal Home Manager module at `nix/home-manager/default.nix`.
- Add a minimal nix-darwin module at `nix/nix-darwin/default.nix`.
- Add documentation describing architecture and migration rules.

Validation target:

```shell
nix fmt
nix flake show
nix flake check
```

If Nix is unavailable on a machine, skip Nix validation and rely on repository checks such as `git diff --check`. Commit `flake.lock` after the first successful `nix flake lock` or `nix flake check` on a machine with Nix installed; the scaffold intentionally does not include a hand-written lock file.

## Phase 1: Package-only adoption

Goal: use Nix to install common packages without changing dotfile ownership.

Candidate packages:

- Core: git, gnupg, vim, zsh, tmux, cmake
- CLI data tools: jq, yq
- Search and listing tools: fd, eza, ripgrep
- Development helpers: uv, shellcheck, shfmt, starship, chezmoi, age, gh
- Language runtimes: rustup, nodejs, python311
- Optional tools: yazi, awscli2 when available

Acceptance criteria:

- Home Manager standalone activation does not overwrite existing dotfiles.
- nix-darwin activation does not assume Homebrew is already installed beyond documented behavior.
- Existing chezmoi commands continue to work before and after Nix activation.

## Phase 2: Host roles and package ownership

Goal: make package sets explicit by host or role.

Possible role modules:

- `common`
- `linux-client`
- `linux-server`
- `darwin-client`
- `work`

Each role should document whether a package is owned by Nix, mise, apt, Homebrew, or another installer.

## Phase 3: Selective config migration

Goal: migrate selected dotfile paths to Home Manager only when there is a clear benefit.

Before migrating a path:

1. Identify the current chezmoi source path under `home/`.
2. Confirm whether private chezmoi overlays or templates affect the same target path.
3. Remove or disable the chezmoi source for that path in the same change that adds Home Manager ownership.
4. Document rollback steps.

Paths that should not be migrated early:

- SSH private material
- GnuPG secret keyrings
- VPN credentials
- Any host-specific or work-specific secret

## Phase 4: Optional Nix-first bootstrap

Goal: provide a Nix-first bootstrap path for users who explicitly choose it.

This should remain separate from `setup.sh` unless the repository owner decides to change the default bootstrap model. A future bootstrap may install Nix, activate Home Manager or nix-darwin, and then run chezmoi for public and private dotfiles.

## Rollback notes

Home Manager standalone rollback is generally handled with Home Manager generations. nix-darwin rollback is handled with system generations. Package-only changes should be low risk, but any future file ownership migration must include explicit rollback instructions because ownership collisions can block activation or overwrite expected state.

Useful rollback entry points:

```shell
home-manager generations
home-manager switch --rollback
sudo darwin-rebuild --rollback
```

For flake input regressions, revert the Git commit that changed `flake.nix` or `flake.lock`, then re-run the relevant Home Manager or nix-darwin switch command.
