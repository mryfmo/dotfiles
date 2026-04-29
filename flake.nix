{
  description = "Opt-in Nix scaffold for mryfmo/dotfiles";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-25.05";
    home-manager = {
      url = "github:nix-community/home-manager/release-25.05";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    nix-darwin = {
      url = "github:nix-darwin/nix-darwin/nix-darwin-25.05";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs =
    inputs@{
      self,
      nixpkgs,
      home-manager,
      nix-darwin,
      ...
    }:
    let
      username = "mryfmo";
      supportedSystems = [
        "aarch64-darwin"
        "x86_64-darwin"
        "aarch64-linux"
        "x86_64-linux"
      ];
      forAllSystems = nixpkgs.lib.genAttrs supportedSystems;
      mkPkgs = system:
        import nixpkgs {
          inherit system;
          config.allowUnfree = true;
        };
      mkHome = system:
        home-manager.lib.homeManagerConfiguration {
          pkgs = mkPkgs system;
          extraSpecialArgs = {
            inherit inputs username;
          };
          modules = [ ./nix/home-manager ];
        };
    in
    {
      homeConfigurations = {
        mryfmo-linux = mkHome "x86_64-linux";
        mryfmo-darwin = mkHome "aarch64-darwin";
      };

      darwinConfigurations = {
        mryfmo-mac = nix-darwin.lib.darwinSystem {
          system = "aarch64-darwin";
          specialArgs = {
            inherit inputs username;
          };
          modules = [
            home-manager.darwinModules.home-manager
            ./nix/nix-darwin
            {
              home-manager.useGlobalPkgs = true;
              home-manager.useUserPackages = true;
              home-manager.extraSpecialArgs = {
                inherit inputs username;
              };
              home-manager.users.${username} = import ./nix/home-manager;
            }
          ];
        };
      };

      devShells = forAllSystems (system:
        let
          pkgs = mkPkgs system;
        in
        {
          default = pkgs.mkShell {
            packages = [
              home-manager.packages.${system}.home-manager
              pkgs.nil
              pkgs.nixfmt-rfc-style
              pkgs.statix
            ];
          };
        });

      formatter = forAllSystems (system: (mkPkgs system).nixfmt-rfc-style);
    };
}
