# Plan 004 Takeover Report

- Verdict: **REVISE**
- Worktree: `/private/tmp/dotfiles-plan-004`
- Branch: `orchestrator/plan-004`
- Exact base: `69e2338489e22d5279ca3fdf6917f0cbe5950400`
- Exact head: `208aeb3cce50b3a4925768c3c90ee043a7b40f75`
- Commit: `208aeb3 feat(supply-chain): pin and verify external inputs`
- Push/PR/merge: not performed

## Takeover findings fixed

- Replaced non-atomic direct binary writes with verified same-directory staging and rename.
- Changed Sheldon `--version 0.8.5` semver range to exact `=0.8.5`, forced crates.io, packaged `Cargo.lock`, and vendored native dependencies.
- Replaced unsupported Sheldon `commit` keys (reported unused by Sheldon 0.8.5) with supported full-SHA `rev` keys.
- Corrected the applied mise lock name from `config.lock` to `mise.lock`, enabled lockfiles explicitly, and made maintenance upgrades temporarily leave strict mode so config and lock can advance together.
- Replaced mutable asdf eza resolution with locked crates.io source, corrected yq's ARM64 macOS artifact via the GitHub backend, and downgraded fd to the newest release with all four supported artifacts.
- Added exact workflow permission parsing, immutable Action pins, native Dependabot ownership, offline external rendering/checksum tests, and a Nix-generated lock artifact route.

## A001-A033

| Task | Status | Evidence / limitation |
|---|---|---|
| A001 | COMPLETE | Inventory updated; all executable download callers classified. |
| A002 | COMPLETE | Corrupt/missing checksum and no-execution assertions added. |
| A003 | IMPLEMENTED | chezmoi 2.70.4 archive and upstream checksum manifest; CI Bats pending. |
| A004 | IMPLEMENTED | mise v2026.5.9 archive and upstream manifest; pinned binary accepts the strict lock. |
| A005 | IMPLEMENTED | Exact crates.io 0.8.5, registry checksum verified, packaged `Cargo.lock` present, `--locked`; CI source-build Bats pending. |
| A006 | IMPLEMENTED | Starship v1.25.1 artifacts/checksums and atomic replacement; CI Bats pending. |
| A007 | COMPLETE | Homebrew commit/hash independently rechecked. |
| A008 | COMPLETE | Remote-execution scan has no unverified pipe-to-shell path. |
| A009 | PARTIAL | Syntax/ShellCheck/unit gates pass; public Bats matrix requires push. |
| A010 | COMPLETE | Six Action repositories plus Nix/upload actions enumerated. |
| A011 | COMPLETE | checkout v7 SHA verified with `gh`. |
| A012 | COMPLETE | setup-uv v7 annotated tag peeled and verified. |
| A013 | COMPLETE | mise-action v4 SHA verified. |
| A014 | COMPLETE | ssh-agent v0.10.0 SHA verified. |
| A015 | COMPLETE | benchmark v1 branch SHA verified. |
| A016 | COMPLETE | Codecov v7 annotated tag peeled and verified. |
| A017 | COMPLETE | Exact six-workflow permissions and job-override rejection tested adversarially. |
| A018 | COMPLETE | Native weekly Dependabot `github-actions` config added. |
| A019 | PARTIAL | YAML/scans/unit tests pass; hosted workflow execution pending. |
| A020 | COMPLETE | Exact-version and reviewed-upgrade policy documented. |
| A021 | COMPLETE | `mise.lock` generated twice identically for four platforms; strict dry-run passes with current and bootstrap mise. |
| A022 | COMPLETE | Every Sheldon Git source uses supported full-SHA `rev`; two isolated native locks are identical. |
| A023 | PARTIAL | Strict locked dry-run passes; hosted clean bootstrap pending. |
| A024 | COMPLETE | Default render succeeds with network proxies disabled. |
| A025 | COMPLETE | Latest-release calls removed; fixed URLs and native checksum schema used. |
| A026 | COMPLETE | No live discovery retained in normal rendering. |
| A027 | COMPLETE | Real chezmoi wrong-checksum fixture preserves the destination. |
| A028 | PARTIAL | Offline/checksum unit oracles pass; hosted public bootstrap pending. |
| A029 | COMPLETE | Official 26.05 branches exist for nixpkgs, Home Manager, and nix-darwin. |
| A030 | INCOMPLETE | Inputs changed together, but `flake.lock` is absent because local Nix/Docker is unavailable. No lock content was invented. |
| A031 | PENDING | Requires the GitHub Linux/macOS Nix matrix. |
| A032 | IMPLEMENTED | Existing test workflow has change gating, pinned Nix install, two-OS evaluation, generated-lock artifacts, and fails until the Nix-generated lock is committed. |
| A033 | COMPLETE | 26.05 and no-activation evaluation commands documented; Nix remains opt-in. |

## Required next action

After push and draft-PR creation are authorized, push this branch and open a draft PR so the PR version of `test.yaml` runs. Download both `flake-lock-ubuntu-latest` and `flake-lock-macos-14`, require byte-identical content, place that Nix-generated file at `flake.lock`, review its owners/revisions, commit it, and rerun CI including the Bats/public bootstrap and Nix matrices. Until then A030/A031 and CI-dependent closure tasks remain open.
