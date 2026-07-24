# Plan 004 Supply-chain Inventory

## Executable bootstrap sources

| Caller | Immutable selector | Integrity source | Platforms | Test/validation |
|---|---|---|---|---|
| `setup.sh`, `install/macos/common/brew.sh` | Homebrew/install `c7952e40b7957268f61643152f4db725379b292e` | independently computed SHA-256 `99287f…6d9d` | macOS x64/arm64 | mismatch before Bash execution |
| `setup.sh` | chezmoi 2.70.4 release archives | upstream `chezmoi_2.70.4_checksums.txt` | Linux/macOS x64/arm64 | corrupt/missing checksum and public bootstrap |
| `install/common/mise.sh` | mise v2026.5.9 archives | upstream `SHASUMS256.txt` | Linux/macOS x64/arm64 | cross-artifact mismatch and real pinned binary dry-run |
| `install/common/sheldon.sh` | crates.io exact `=0.8.5` | crates.io registry checksum `43a2d8…b4d`, packaged Cargo.lock | Linux/macOS x64/arm64 source build | Cargo checksum failure leaves destination untouched |
| `install/ubuntu/server/starship.sh` | Starship v1.25.1 archives | per-artifact upstream `.sha256` | Linux x64/arm64 | mismatch preserves Starship and sibling |

All verified binary installers stage in the destination directory and rename only after successful verification/build. The executable remote-content scan has no unverified pipe-to-shell path.

## External Actions

| Action | Readable ref | Pinned SHA |
|---|---|---|
| actions/checkout | v7 | `9c091bb21b7c1c1d1991bb908d89e4e9dddfe3e0` |
| astral-sh/setup-uv | v7 | `37802adc94f370d6bfd71619e3f0bf239e1f3b78` |
| jdx/mise-action | v4 | `e6a8b3978addb5a52f2b4cd9d91eafa7f0ab959d` |
| webfactory/ssh-agent | v0.10.0 | `e83874834305fe9a4a2997156cb26c5de65a8555` |
| benchmark-action/github-action-benchmark | v1 branch | `52576c92bccf6ac60c8223ec7eb2565637cae9ba` |
| codecov/codecov-action | v7 | `fb8b3582c8e4def4969c97caa2f19720cb33a72f` |
| cachix/install-nix-action | v31 | `a49548c11d9846ad46ecc0115273879b045f001c` |
| actions/upload-artifact | v4 | `ea165f8d65b6e75b540449e92b4886f43607fa02` |

## Non-executable archives and Git inputs

- Nerd Fonts v3.4.0 RobotoMono/Hack and LINE Seed archives have fixed URLs and native chezmoi `checksum.sha256` fields; hashes were re-downloaded and verified.
- All ten Sheldon GitHub plugins use Sheldon 0.8.5's supported `rev` field with a full commit SHA; actual lock output confirmed each checkout.
- mise requests are exact, `mise.lock` is committed under its native applied name, strict mode is enabled, and platform URL/checksum coverage is tested where the backend supports it.
