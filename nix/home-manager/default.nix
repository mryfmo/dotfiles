{
  config,
  lib,
  pkgs,
  username,
  ...
}:

let
  isDarwin = pkgs.stdenv.isDarwin;
in
{
  home = {
    inherit username;
    homeDirectory = if isDarwin then "/Users/${username}" else "/home/${username}";

    # Do not change casually. This gates Home Manager defaults and migrations.
    stateVersion = "25.05";

    packages = import ../shared/packages.nix { inherit pkgs; };
  };

  programs.home-manager.enable = true;

  # This initial opt-in module intentionally avoids home.file and xdg.configFile.
  # Existing dotfiles under home/ remain owned by chezmoi to prevent collisions.
  news.display = "silent";
}
