# AGMSG-TASK dot-mosh-and-asset-bumps-T31-a01

## Objective

Operator directives (2026-09-27), two related supply/parity deliverables:

1. **mosh managed on both OSes**: install and configure mosh via dotfiles on
   Ubuntu and macOS. Today mosh is unmanaged (host has a manual apt package;
   macOS gets nothing), while `home/dot_zshenv:7` already documents that the
   file is read by the non-interactive SSH remote commands that bootstrap
   "Mosh and Herdr" — the design assumes mosh, the install does not provide
   it.
2. **Close the make-upgrade asset-bump coverage gap**: `upgrade-tools.sh`
   auto-bumps only tode/terminal-browser/crit/zed asset pins; mise, sheldon,
   starship, and aws-cli asset pins have NO automated bump path (found
   2026-09-27: starship sat at v1.25.1 with v1.26.0 published 2026-06-28).

Also fold in one accepted T29 follow-up: `.github/workflows/remote.yaml`
carries three dead `github.actor == 'dependabot[bot]'` guards (Dependabot
was removed by T29); delete them.

[memory:decision] T31: mosh is dotfiles-managed on both OSes (PACKAGES
entries + the minimal server-side config the investigation proves necessary);
upgrade-tools.sh gains a pins-only bump path for the mise/sheldon/starship/
aws-cli assets under the same 7-day supply-chain window as mise tools; dead
dependabot actor guards removed (operator 2026-09-27).

## Repo / branch

- Work ONLY in `/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c`.
- `git fetch origin`, then
  `git switch -c feat/mosh-and-asset-bumps origin/main`.
  (Verify the dispatched task_rev sha256 against this file on your base, else
  stop and PONG.)
- If the worktree has uncommitted files, stop and report via AGMSG-PONG.

## Changes

### 1. mosh install (both OSes)

- `install/ubuntu/common/dependencies.sh`: add `mosh` to `PACKAGES`
  (respect the array's ordering convention).
- `install/macos/common/dependencies.sh`: add `mosh` to its package list the
  same way.
- Follow the scripts' existing shdoc/English comment conventions; if the
  removable-packages logic classifies entries, place mosh consistently with
  comparable network tools.

### 2. mosh configuration (investigate first, then implement ONLY what is

needed — YAGNI)

- Investigate and paste evidence for each point:
  (a) UTF-8 locale: mosh-server requires a UTF-8 locale on the server; check
  what the repo/host already guarantees (locale exports in dot_zshenv or
  profile, Ubuntu locale packages). Add the minimal missing piece only if
  missing.
  (b) Firewall: check whether the repo manages any firewall (ufw/iptables
  rules, tailscale). With connectivity over Tailscale, mosh's UDP 60000-61000
  needs no public exposure; if and only if the repo manages a firewall that
  would block tailnet UDP, add the narrowest rule. Otherwise document "no
  firewall change needed" with evidence.
  (c) Non-interactive bootstrap: confirm `mosh user@host` reaches
  mosh-server through the documented dot_zshenv PATH bootstrap (static
  analysis of the PATH lines is sufficient; no live remote test required).
- `README.md`: one short paragraph — mosh is installed on both OSes, works
  over Tailscale, and the dot_zshenv non-interactive bootstrap covers it.

### 3. upgrade-tools.sh: pins-only bump path for the remaining assets

- Add a function (mirroring the existing tode/terminal-browser/crit/zed
  `--set-asset` block) that bumps the four remaining version-pinned assets —
  `mise`, `sheldon`, `starship`, `aws-cli` — each per its manifest `source:`
  / `verify:` contract (github-release tags, crates version, https download
  with sha256; compute every hash field the asset's verify contract lists,
  exactly as `generate-agent-configs.py --set-asset` accepts).
- Apply the SAME 7-day supply-chain window as the mise-tools path
  (`--before 7d` semantics: skip any release published within the last 7
  days; implement with the release's published date from the datasource).
- Wire it into the existing `make upgrade` flow next to the current
  `--set-asset` block.
- RUN the new path once in the worktree (pins-only; it writes repo files
  only, no installs): expected outcome TODAY is `starship v1.25.1 →
v1.26.0` (published 2026-06-28, outside the window) and `sheldon`
  unchanged (already latest), while `mise v2026.9.14` (2026-09-25) and
  `aws-cli 2.37.4` (2026-09-25) are SKIPPED by the window — paste the run
  output showing both the bump and the window skips (this doubles as the
  live proof of the window logic).
- `home/dot_agents/agent-config.yaml` and its rendered pin files will change
  only via that run; hand edits are forbidden (validator enforces).

### 4. Dead Dependabot guards

- `.github/workflows/remote.yaml`: remove the three
  `github.actor == 'dependabot[bot]'` conditions (T29 removed Dependabot;
  the guards are dead). Keep surrounding behavior identical for all other
  actors; state the before/after condition text in the report.

### 5. Tests

- Unit tests per the existing patterns with a mutation baseline (paste the
  FAILED run against unmodified scripts): (a) the new bump function skips a
  release younger than 7 days and takes an older one (fake datasource
  responses); (b) it writes only pin/sha256 fields via --set-asset (no other
  manifest mutation); (c) dependency-script change is covered by the existing
  install test pattern if one exists for PACKAGES membership (add the
  minimal assertion if the pattern exists; do not invent a new framework).
- No local bats (repo policy); CI's public-bootstrap jobs (ubuntu+macos)
  exercise the real installs.

## Allowed files

- `install/ubuntu/common/dependencies.sh`
- `install/macos/common/dependencies.sh`
- locale/firewall config files ONLY if the step-2 investigation proves a
  missing piece (name each with its evidence in the report)
- `scripts/upgrade-tools.sh`
- `home/dot_agents/agent-config.yaml` + rendered pin files (via the new
  pins-only run and `--set-asset` only)
- `.github/workflows/remote.yaml` (deliverable 4 only)
- `README.md`
- matching unit test files under `tests/unit/`
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dot-mosh-and-asset-bumps-T31-a01.md` (main checkout)

## Forbidden actions

- Installing anything on this host (no apt/brew runs; CI proves installs);
  sudo; version bumps other than what the new pins-only path produces under
  the 7-day window; touching model_profiles, herdr-agents, permgate, hooks
  configs, dependencies beyond the mosh package entries, or
  `reviews/ADH_Integrated_Plan/`.
- Merging; force push; local bats; `make apply`/`chezmoi apply`; writes
  outside the worktree except the listed `.orchestration` paths.

## Validation commands (paste verbatim output)

```
uv run --with pyyaml scripts/generate-agent-configs.py --check
make validate-agent-assets
make unit-test
git -C /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c diff origin/main --stat
gh pr checks <pr-number>
```

## Completion

1. PR to `main`, English title/description ending with
   `🤖 Generated with [Claude Code](https://claude.com/claude-code)`.
   Watch CI to green (public-bootstrap ubuntu+macos jobs are the mosh install
   proof).
2. Artifacts at the exact expected paths; validation with verbatim outputs
   (mutation baseline + the pins-only run showing the starship bump and the
   window skips) and the PR number/head SHA.
3. CompactionDB from the main checkout:
   `python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "T31: mosh managed on both OSes (PACKAGES + only investigation-proven config); upgrade-tools.sh pins-only bump path covers mise/sheldon/starship/aws-cli under the 7-day window (starship bumped to v1.26.0, window skips proven live); dead dependabot actor guards removed (operator 2026-09-27)"`
   — paste command and output.
4. `AGMSG-RESULT v1` with all artifact paths; `cost:` line in the report.
