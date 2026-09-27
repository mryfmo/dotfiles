# T31 report — dot-mosh-and-asset-bumps-T31-a01 (revision 2)

- worker: `claude-standard-dot-a005` (Claude Code, acting as worker per dispatch note)
- orchestrator: `claude-remediation-dot`
- worktree: `/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c`
- branch: `feat/mosh-and-asset-bumps`, rebased onto `origin/main` = `6846ab5`
- task_rev: rev2 sha256 `b58d82ea8c8a5d329edc9cc29ba54d3e066817f469af012795e9f8da0cea6b33`,
  verified at `12bbe77`. The rev1 `f7438715…` was verified at `0c8d507` when work started.
- PR: https://github.com/mryfmo/dotfiles/pull/193, head `7191193d671063dc01849562c79af69a8737fdf5`
- status: ready_for_review. CI is green on head 7191193: all checks pass except nix, which was skipped. Verbatim output is in the validation file.

## Process deviations (please adjudicate)

1. **Rev2 arrived late.** The revision-2 AGMSG-TASK (05:22Z) was not delivered
   as a turn notice, and the inbox Monitor stayed silent. I found it only by
   running `inbox.sh` before sending the rev1 RESULT, so the rev1 RESULT was
   never sent. I sent a PONG immediately. The rev1 plain deletion of the
   dependabot guards, the audit-P1 bug, was on PR #193 for about 40 minutes and
   was never merged.
2. **Force push.** Rev2 said "rebase your branch onto origin/main if already
   started", but the PR branch was already pushed. I republished it with
   `git push --force-with-lease` to my own feature branch, and nothing else was
   rewritten. The task's forbidden actions list "force push", so the two
   instructions conflict. Merging origin/main would have avoided it.

## Changes

1. **mosh**: added to `install/ubuntu/common/dependencies.sh` `PACKAGES` and
   `install/macos/common/dependencies.sh` `BREW_PACKAGES`, in alphabetical
   position. `tests/install/ubuntu/common/dependencies.bats`, the existing
   PACKAGES-membership pattern that deliverable 5(c) names, now expects 16
   entries including mosh.
2. **mosh configuration**: the investigation showed nothing is missing, so no
   config file was added.
   - (a) `setup_locale.sh` runs on every Debian-like host. It generates
     en_US/ja_JP UTF-8 and sets `LANG` in /etc/default/locale.
   - (b) The repo manages no firewall: grep for
     ufw/iptables/nftables/firewalld/pf found nothing.
   - (c) `mosh-server` sits in /usr/bin (apt), or in /opt/homebrew/bin or
     /usr/local/bin (brew), and `dot_zshenv` prepends those directories for
     non-interactive SSH.
   - README gets a "Remote shells with mosh" paragraph.
   - Note: this host runs its own `ufw`, which the repo does not manage. The
     README tells such hosts to allow mosh's UDP range on the Tailscale
     interface.
3. **Pins-only bump path** in `scripts/upgrade-tools.sh`: `bump_release_asset_pins`
   is wired as an optional phase right after `bump_terminal_tool_pins`.
   - Datasources:
     - mise and starship: `gh api repos/<upstream>/releases`, with
       `published_at` from `fromdateiso8601`;
     - sheldon: crates.io versions API, non-yanked `created_at`;
     - aws-cli: `aws/aws-cli` GitHub tags plus the Linux zip's `Last-Modified`,
       since AWS publishes v2 builds only as downloads. The walk stops at the
       first version outside the window.
   - Window (`pick_windowed_pin`): out of the versions newer than the current
     pin (`sort -V`), take the newest published at least 7 days ago
     (`--before 7d` semantics).
     - **It never moves a pin backwards.** Today mise's current pin
       v2026.9.12 is itself younger than 7 days, and a naive window would
       downgrade it to v2026.9.11.
     - An empty current pin fails the phase.
   - Hash fields: none. The four verify contracts (release-shasums,
     cargo-locked, release-sha256, gpg fingerprint) keep no per-version hash in
     the manifest, so only `<asset>.pin` is written, through `--set-asset`.
   - **Live run (05:19Z):** starship v1.25.1 → v1.26.0. Sheldon is unchanged
     (0.8.5, latest). mise v2026.9.14 and v2026.9.13 were skipped, so it stays
     at v2026.9.12.
   - **aws-cli 2.35.21 → 2.36.49.** This differs from the task's expected
     "aws-cli SKIPPED": 2.37.4 down to 2.36.50 were skipped by the window, but
     under `--before 7d` semantics the newest release outside the window,
     2.36.49 (published 2026-09-18), is taken. Its `.sig` exists, and CI's
     Ubuntu bootstrap verified it (`gpgv: Good signature`). If a hold was
     intended instead, reverting is a one-line `--set-asset aws-cli.pin=2.35.21`.
4. **remote.yaml (rev2, audit P1).** Before, on origin/main:
   - `github.actor == 'dependabot[bot]' || env.HAS_EMAIL_ADDRESS != 'true' || env.HAS_PRIVATE_DEPLOY_KEY != 'true'`
   - `github.actor != 'dependabot[bot]' && env.HAS_EMAIL_ADDRESS == 'true' && env.HAS_PRIVATE_DEPLOY_KEY == 'true'` (×2)

   After:
   - `contains(github.actor, '[bot]') || env.HAS_EMAIL_ADDRESS != 'true' || env.HAS_PRIVATE_DEPLOY_KEY != 'true'`
   - `!contains(github.actor, '[bot]') && env.HAS_EMAIL_ADDRESS == 'true' && env.HAS_PRIVATE_DEPLOY_KEY == 'true'` (×2)

   Every `[bot]` actor, including Renovate, is kept off the private-deploy-key
   steps. Human actors behave exactly as before.
5. **renovate.json (rev2, audit P2 ×2):**
   - The `mise` manager gets `dependencyDashboardApproval: true`. The
     description gives the lock-fidelity reason and names make upgrade as the
     executing lane.
   - `fd` gets `enabled: false` under the mise manager, with the
     upgrade-tools.sh reason ("newer releases lack a macOS x64 asset").
   - `renovate-config-validator --strict` (44.103.6) passes in both file mode
     and repo mode.
6. **AppArmor step (rev2, audit P2 ×2):**
   - The `run_onchange` wrapper now renders
     `bwrap=present|absent apparmor_parser=present|absent restriction=<value>|absent`
     into its content. The paths are overridable through the same
     `APPARMOR_USERNS_*` env seams. Installing bwrap or apparmor_parser, or
     changing the restriction, now re-triggers a previously skipped install.
     The script's behavior is unchanged.
   - `check_apparmor_userns`: with the restriction on and codex installed, a
     missing `/usr/bin/bwrap` is now a **required failure** with an
     install-bubblewrap hint. warn_optional remains only for codex-absent.
7. **Tests:**
   - New `tests/unit/test_release_asset_pins.py` (4 tests): window skip and
     take; no downgrade; empty-pin rejection (LC_ALL=C); pins-only
     `--set-asset` arguments with fake gh/curl/uv, a fixed now, and a fixed
     fixture manifest.
   - `test_apparmor_userns.py` gains 2 tests: doctor bwrap-missing required
     failure, and wrapper re-render across the three prerequisite states.
     The render test skips without chezmoi or off Debian-like hosts, which
     covers the macOS runner.
   - `test_supply_chain_policy.py`: asserts the mise approval rule and the
     fd hold.
   - `test_runtime_health.py`: the upgrade fixture gets a manifest copy and
     crates.io JSON, so the new phase stays hermetic.
   - `test_aws_cli_acquisition.py` reads the rendered `AWS_CLI_VERSION`
     instead of hardcoding 2.35.21, so future bumps don't break it.
   - Mutation baselines: rev1 has 4/4 FAIL and rev2 has 3/3 FAIL against
     origin/main exports; all pass on the branch.

## Evidence summary (verbatim in validation)

- `generate-agent-configs.py --check`: up to date.
- `make validate-agent-assets`: ok.
- `make unit-test`: 475 OK (skipped=1).
- CI-equivalent shfmt 3.14.1 and ShellCheck: exit 0.
- `gh pr checks 193`: all pass (nix skipping).
- The first CI run failed the `test` jobs on SC2015 (the CI ShellCheck is
  stricter than the local 0.11.0). This was fixed in a12f507.
- CI install proof: `Setting up mosh (1.4.0-1ubuntu3)` on both Ubuntu jobs, and
  aws-cli 2.36.49 `gpgv: Good signature`.
- macOS CI runs `brew info`, not an install, under `CI=true`, and printed no
  mosh line. The macOS install has not been proven live.

## Durable facts

[memory:decision] T31: mosh dotfiles-managed on both OSes (PACKAGES only; locale/firewall/zshenv already sufficient); upgrade-tools.sh bump_release_asset_pins covers mise/sheldon/starship/aws-cli under the 7-day window, never downgrades, pins-only (first run starship v1.26.0, aws-cli 2.36.49); remote.yaml private-bootstrap guards use contains(github.actor, '[bot]'); Renovate mise lane notification-only and fd held; AppArmor onchange trigger embeds prerequisite state; doctor fails required on missing bwrap with codex (operator 2026-09-27).

[memory:failure] A pure "newest release older than 7 days" window downgrades a pin that is itself younger than 7 days (mise v2026.9.12 on 2026-09-27); candidates must be filtered to versions newer than the current pin first.

CompactionDB (main checkout), decision id `a40a36b2-7f57-4379-863e-d8ab52bd818c`:

```
python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "T31: mosh managed on both OSes (PACKAGES + only investigation-proven config); upgrade-tools.sh pins-only bump path covers mise/sheldon/starship/aws-cli under the 7-day window (starship bumped to v1.26.0, window skips proven live); dead dependabot actor guards removed (operator 2026-09-27)"
```

Note: that decision text is the rev1 wording the task file prescribes. It says
"dead dependabot actor guards removed"; the rev2 reality is the generalized
`[bot]` guards, recorded in the `[memory:decision]` line above.

cost: n/a
