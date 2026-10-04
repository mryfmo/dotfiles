# Acceptance: dotfiles-T74-bootstrap-dead-code-a01

- **Decision:** ACCEPTED (no revise round; one PONG decision). PR #247 squash-merged to `main` as `8922f13b` (final head `c0ea3e7f1b150f43e6841642038cc62b290653c6`; substantive commits 2487b05a, c0ea3e7f; base `138e6a72`, no update-branch merge). Merged without `--delete-branch`; worker-c holds `chore/bootstrap-dead-code`.
- **Worker:** `claude-standard-dot-a005` (worker-c). task_rev `66b87608…` → `35ec2cb2…` (addendum 1) → `ee21597b…` (PONG decision 1); all matched. Parallel wave with T88/T68 (a006) and T65 (a007); dispatched the moment a005's T91 RESULT arrived.
- **Exemption declared:** acceptance and final integration; the orchestrator mutated no repository code.
- **Plan reference:** Phase 4, dotfiles-T74 (principle 9: bootstrap dead code).

## What was accepted (14 files, +4/−391)

- Deleted: `install/macos/arm64/run.sh` (echoed its own path, no includer); the `make init` private-init branch; setup.sh's disabled `restart_shell` family and its commented call; the two empty OS chezmoiexternal templates; `flake.nix`, `flake.lock`, `nix/**`, the CI `should_nix` filter and `nix` job, and the supply-chain nix test.
- Kept (deviation, c0ea3e7f): the chezmoiexternal platform guard, rewritten as one `if not (or darwin (and linux debian))` → `fail` ahead of the common include. Codex P2 4175951414 showed it is a live guard (unsupported hosts would otherwise download the externals); the rendered output on supported hosts is byte-identical.
- Lifecycle test now asserts `make -n init` prints exactly `chezmoi init --apply --verbose`.

## Orchestrator re-derivation

- The private layer is initialized by `home/.chezmoiscripts/common/run_once_after_01-setup-chezmoi-private.sh.tmpl` (includes `install/common/chezmoi_private.sh`, gated by the `usePrivate` prompt); `setup.sh` never calls `chezmoi-private`; nothing calls `make init` (README:640 lists it as a guarded target; `home/dot_codex/rules/default.rules:172` is the T63 forbidden example). The addendum's third grep was worded so it could not match README:640; the worker's blocked PONG was correct and decision 1 resolved it.
- Go template `or`/`and` short-circuit, so the `.chezmoi.osRelease.idLike` lookup is not evaluated on darwin; the auditor's nine rendering cases confirm supported output unchanged and unsupported platforms failing before the include.
- The ruleset's seven required status contexts never included `nix`; CI on c0ea3e7f shows 16 passing checks with the build jobs the Makefile path triggers.

## Audit / Bot / sweep / gate

| commit | verdict |
|---|---|
| 2487b05a | incorrect: 2 findings |
| c0ea3e7f | correct |

- audit-finding: 2487b05a `home/.chezmoiexternal.yaml.tmpl:1` platform guard removed → fixed:c0ea3e7f (audited correct)
- audit-finding: 2487b05a `flake.nix:1` nix plan documents left stale → not-applicable:`docs/plans/nix-first-architecture.md`, `docs/plans/nix-migration.md` and `plans/004-harden-and-lock-the-supply-chain.md` are plan prose this task was forbidden to edit; the stale lines are enumerated in the T74 report and rewritten by T78/T83
- Codex Bot: two P2s on 2487b05a (same two points), one fixed in c0ea3e7f and one not-applicable as above, both replied and resolved by the orchestrator; no review on c0ea3e7f within the wait. Sweep (head c0ea3e7f): 13 items, 0 failure/warning, all dispositioned. Gate at c0ea3e7f exit 0 with evidence copies, copies removed.

## Follow-ups

- T78/T83: the stale nix sentences listed in the report (`docs/plans/nix-first-architecture.md:16,58,64,70,76`; `docs/plans/nix-migration.md:23-26,33-34,37,110`; `plans/004…:44,64-65,92,109,371,386-393`).
- Operator: after `make update` on each host, `chezmoi apply` renders the externals unchanged; nothing to remove from `$HOME`.

## CompactionDB

- Worker decision `9c4baa38-0730-4e71-b6a7-fcc6b06be80c`; cited. Amendment recorded at acceptance: the chezmoiexternal platform guard is kept.
