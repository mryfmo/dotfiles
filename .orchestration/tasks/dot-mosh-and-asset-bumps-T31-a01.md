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

REVISION 2 (2026-09-27, supersedes the deliverable-4 wording and adds
deliverables 6-7): the first live Codex audits (gpt-6-astra, read-only)
of the T29 and T30 merge commits produced five confirmed findings; this task
now carries their fixes. The orchestrator independently re-verified the P1
(remote.yaml:105-115: the private-deploy-key steps run for every actor except
`dependabot[bot]`, so a same-repo Renovate PR would run setup.sh with the
private deploy key in the ssh-agent).

[memory:decision] T31: mosh is dotfiles-managed on both OSes (PACKAGES
entries + the minimal server-side config the investigation proves necessary);
upgrade-tools.sh gains a pins-only bump path for the mise/sheldon/starship/
aws-cli assets under the same 7-day supply-chain window as mise tools;
remote.yaml bot guards generalized to all [bot] actors (audit P1); renovate
mise lane notification-only until lock fidelity is proven, fd excluded (audit
P2); apparmor onchange step retries after prerequisite installs and doctor
fails required when bwrap is missing with codex present (audit P2)
(operator 2026-09-27).

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

### 4. remote.yaml bot guards (REVISED — audit P1, orchestrator-confirmed)

- Do NOT simply delete the dependabot guards. `.github/workflows/remote.yaml`
  (~lines 105-115): the three `github.actor == 'dependabot[bot]'` /
  `!= 'dependabot[bot]'` conditions gate the PRIVATE-DEPLOY-KEY steps; a
  same-repo Renovate PR (actor `renovate[bot]`) currently passes them and
  would run `setup.sh` with `PRIVATE_DOTFILES_PRIVATE_DEPLOY_KEY` in the
  ssh-agent. Replace the dependabot-specific checks with generic bot-actor
  checks: `contains(github.actor, '[bot]')` (and its negation), so every bot
  — dependabot, renovate, and future ones — is excluded from the private
  bootstrap path while human PRs keep testing it. State the before/after
  condition text in the report.

### 4b. renovate.json hardening (audit P2 ×2)

- Mise lock fidelity: Renovate's mise artifact updater does not load
  `home/dot_mise/config.toml` as a discovered config (`mise lock` runs in the
  containing directory without MISE_CONFIG_DIR), so its version PRs cannot
  reliably regenerate `mise.lock`. Until a trial proves otherwise, extend the
  notification-only packageRule (`dependencyDashboardApproval: true`) to the
  `mise` manager as well, with a description stating the lock-fidelity reason
  and that `make upgrade` remains the executing lane.
- fd exclusion: `scripts/upgrade-tools.sh` deliberately skips `fd` (newer
  releases lack macOS x64 assets); the mise manager would bypass that. Add a
  packageRule disabling/holding `fd` updates with the same reason string as
  the script comment.
- Update `tests/unit/test_supply_chain_policy.py` to assert both (mise
  manager requires dashboard approval; fd is excluded).

### 4c. AppArmor step robustness (audit P2 ×2 on the T30 changeset)

- `home/.chezmoiscripts/ubuntu/run_onchange_after_07-apparmor-bwrap-userns.sh.tmpl`:
  a skipped install (e.g. bwrap absent at first apply) is permanent because
  the onchange hash only covers repository files. Include the prerequisite
  state in the rendered trigger (e.g. embed `lookPath "bwrap"`-derived state
  and the restriction sysctl value into the template comment/hash inputs) so
  installing bwrap or flipping the restriction re-triggers the step on the
  next apply. Keep the script itself unchanged in behavior.
- `scripts/check-tools.sh` `check_apparmor_userns`: when the restriction is 1
  AND codex is installed but `/usr/bin/bwrap` is missing, report a REQUIRED
  failure (currently warn_optional), with a hint to install bwrap; keep
  warn_optional only for the codex-absent case.
- Extend `tests/unit/test_apparmor_userns.py` for both (trigger re-render on
  prerequisite change can be asserted via the rendered wrapper content seam;
  doctor required-failure branch).

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
- `renovate.json` (deliverable 4b only)
- `home/.chezmoiscripts/ubuntu/run_onchange_after_07-apparmor-bwrap-userns.sh.tmpl` (deliverable 4c only)
- `scripts/check-tools.sh` (deliverable 4c only)
- `README.md`
- matching unit test files under `tests/unit/` (incl. test_supply_chain_policy.py, test_apparmor_userns.py)
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
