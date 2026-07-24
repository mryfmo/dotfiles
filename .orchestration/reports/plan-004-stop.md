# Plan 004 STOP / Resolution Record

## Historical STOP

- Dependency: Sheldon 0.8.5 GitHub release binaries.
- Reason: mutable release with no independently published checksum/signature or attestation.
- The original worker correctly stopped and did not substitute GitHub release digest metadata.

## Resolution

- Status: **RESOLVED by operator-approved plan revision**.
- Approved source: crates.io package `sheldon 0.8.5`.
- crates.io registry SHA-256: `43a2d8fc0be4474cfe2d603992c7e9765c9a0f87465aabcfc0603c1de4290b4d`.
- Downloaded crate bytes matched the registry checksum and contained `sheldon-0.8.5/Cargo.lock`.
- Installer uses `cargo install --registry crates-io --version =0.8.5 --locked` with vendored native dependencies and atomically replaces only the Sheldon binary.

The STOP is preserved as historical evidence; it is not an outstanding blocker. The remaining blocker is the missing Nix-generated `flake.lock`, unrelated to Sheldon.
