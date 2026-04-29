{ pkgs }:

let
  optionalPackage = name: if builtins.hasAttr name pkgs then [ pkgs.${name} ] else [ ];
in
with pkgs;
[
  age
  chezmoi
  cmake
  eza
  fd
  gh
  git
  gnupg
  jq
  nodejs
  python311
  rustup
  ripgrep
  shellcheck
  shfmt
  starship
  tmux
  uv
  vim
  yazi
  yq
  zsh
]
++ optionalPackage "awscli2"
