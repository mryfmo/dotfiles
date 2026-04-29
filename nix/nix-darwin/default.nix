{
  config,
  lib,
  pkgs,
  username,
  ...
}:

{
  nixpkgs.config.allowUnfree = true;

  users.users.${username}.home = "/Users/${username}";

  # User-level packages are owned by the integrated Home Manager module.
  # Keep systemPackages empty in the initial scaffold to avoid duplicating the
  # same tools in both the system and user profiles.
  environment.systemPackages = [ ];

  nix = {
    settings = {
      experimental-features = [
        "nix-command"
        "flakes"
      ];
    };
  };

  programs.zsh.enable = true;

  homebrew = {
    enable = true;
    # This only lets nix-darwin manage Homebrew formulae/casks/taps.
    # It does not install Homebrew itself; install Homebrew before activation.
    onActivation = {
      autoUpdate = false;
      cleanup = "none";
      upgrade = false;
    };
  };

  system = {
    primaryUser = username;

    # Do not change casually. This gates nix-darwin defaults and migrations.
    stateVersion = 5;
  };
}
