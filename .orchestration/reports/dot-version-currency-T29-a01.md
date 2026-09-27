# T29 report — dot-version-currency-T29-a01

- worker: `claude-standard-dot-a005` (Claude Code, acting as worker per dispatch note)
- orchestrator: `claude-remediation-dot`
- worktree: `/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c`
- branch: `feat/version-currency` (base `origin/main` = `5b15d1e`)
- task_rev: sha256 `7e1a66e44eabdd6734fe2c2e80ab45b6024da400a653211bc3f14a19d839429b`, verified
  against the task file at `5b15d1e` (see validation file)
- PR: https://github.com/mryfmo/dotfiles/pull/191, head `c57c3cf`
- status: ready_for_review; CI green on head c57c3cf (all checks pass except nix, which was skipped; verbatim output in the validation file)

## Changes

1. **Renovate** — new `renovate.json`; `.github/dependabot.yml` deleted.
   - `extends: config:recommended`.
   - `enabledManagers: [github-actions, mise, custom.regex]`, so Renovate does
     not open PRs for other ecosystems (nix, pip, etc.).
   - Weekly schedule `* 0-3 * * 1`, label `dependencies`,
     `dependencyDashboard: true`.
   - `github-actions` is the 1:1 Dependabot replacement.
   - `mise.managerFilePatterns: ["/(^|/)home/dot_mise/config\\.toml$/"]`.
   - Two regex custom managers on `home/dot_agents/agent-config.yaml`:
     - `source: github-release` → `github-releases`, with `depName` taken from
       `upstream`: mise, starship, crit, zed.
     - `source: crates` → `crate`: sheldon.
     - Checked against the real manifest: they extract exactly these 5 deps.
   - packageRules:
     - Minor/patch updates are grouped for github-actions and mise only.
     - A notification-only rule applies `dependencyDashboardApproval: true` to
       `custom.regex` updates on agent-config.yaml.
     - JSON has no comments, so the rule's `description` field carries the
       "why": the sha256/trusted_hash pairing is recomputed only by
       `upgrade-tools.sh --set-asset`.
     - No `automerge` anywhere.
   - `tests/unit/test_supply_chain_policy.py`:
     `test_dependabot_owns_github_action_updates` is replaced by
     `test_renovate_owns_dependency_update_notifications`. It asserts no
     dependabot file exists, the exact enabled managers, that the mise pattern
     matches `home/dot_mise/config.toml`, that exactly one custom.regex rule
     requires dashboard approval, and that no automerge is set. Baseline: it
     FAILS against an origin/main export and passes on the branch.
   - The formatter hook reformatted the whole test file. I reverted that and
     reapplied only the test change, so the diff is 27 lines.
2. **ccusage org move**: zero references to the old org
   (`ryoppippi|github.com/.../ccusage`) exist on origin/main outside
   `.orchestration`/`.ua`, so nothing changed. Grep evidence before and after
   is in the validation file. The ccusage version (20.0.23) is untouched.
3. **Understand-Anything installer**: `--set-asset` pin
   `6df3065f1d8ddc2ce3615314d1d493f36d6b1c80` (main HEAD, 2026-09-12, 81 ahead
   of 797ce79, 0 behind) **and** `sha256=cb84ca53…bc464`. Rendered files:
   `home/dot_agents/agent-config.yaml`, `scripts/update-agent-assets.sh`.
4. **AGENTS.md**: a new `## Canonical Instructions` section (3 bullets) at the
   top. CLAUDE.md is not edited; it already matches the shim rule.

## Deviations from the task text (please adjudicate)

- **The UA sha256 was bumped too.** The task's research note says the
  git-commit pin has "no paired sha256". That is wrong for this asset:
  - `assets.understand-anything-installer` has `verify: sha256` plus a
    `sha256` field.
  - It renders `CODEX_UNDERSTAND_ANYTHING_INSTALLER_SHA256`, which
    `update_codex_understand_anything` compares against `shasum` of
    `install.sh` at the pinned commit. On a mismatch it prints "installer
    checksum mismatch" and skips the install.
  - The rendered file's own comment says to change the commit and sha256
    together.
  - Recomputing the old hash reproduced the recorded
    `54f0350d…`, which confirms the method.
  - The install.sh diff between the two commits is one line: the kimi
    skills path `~/.kimi/skills` → `~/.kimi-code/skills`.
  - This is not a version bump beyond the UA pin; it is the pin's integrity
    pair.
- **tode and terminal-browser have no Renovate manager.** The task listed
  them under `github-releases`, but they are `source: installer-script`.
  Their installers download from `tode-releases.zenbu-labs.workers.dev` and
  `terminal-browser.sh/install/dl/…`, not GitHub releases, so a
  github-releases lookup has no repo to query. `make upgrade`
  (`fetch_installer_pin`) remains their update path.
- **sheldon uses the `crate` datasource instead of `github-releases`.** This
  matches its manifest `source: crates`. Updates stay notification-only either
  way.

## Not changed

- `.github/workflows/remote.yaml` has three `github.actor == 'dependabot[bot]'`
  guards. They reference the Dependabot actor, not `dependabot.yml`. Once
  Dependabot is gone they are dead but harmless, and the file is outside
  allowed_files, so they are left for the orchestrator.
- `plans/003`/`plans/004` mention Dependabot as historical plan text; not changed.

## Risk to check before merging mise PRs

The Renovate `mise` manager updates `home/dot_mise/config.toml`. I did not
verify whether it regenerates `home/dot_mise/mise.lock`. The repo verifies
mise tools with `verify: mise-lock`, so a Renovate mise PR may need a lock
refresh before merge. Nothing auto-merges.

## Evidence summary (verbatim in validation file)

- `renovate-config-validator --strict`: validated successfully with Renovate
  44.103.6, in both file mode and repo mode.
  - The first npx run hit a stale cached 37.440.7 that rejects
    `managerFilePatterns`.
  - npm's 7-day release-age guard refused 44.115.10; I did not override it.
- `generate-agent-configs.py --check`: up to date.
- `make validate-agent-assets`: ok.
- `make unit-test`: 462 tests OK (skipped=1).
- `gh pr checks 191`: all pass except nix (skipped).
- Diff: 6 files on the branch.
  - `origin/main` has since advanced to 00c77f5 (the T30 task file), so the
    two-dot stat also lists that file.
  - The merge-base stat is in the validation file.
- No local bats (repo policy).

## Durable facts

[memory:decision] T29: Renovate replaces Dependabot (github-actions; mise manager at home/dot_mise/config.toml; agent-config.yaml pins notification-only via dependencyDashboardApproval), ccusage had no old-org references, UA installer pinned to 6df3065 with its install.sh sha256, AGENTS.md codified as canonical with CLAUDE.md as the Claude-only shim (operator 2026-09-27).

[memory:failure] The UA installer git-commit pin is paired with the sha256 of install.sh at that commit; bumping only the pin makes update-agent-assets skip the Codex UA install on checksum mismatch.

CompactionDB (main checkout), decision id `be406d1a-d948-4866-b447-245036f85e0d`:

```
python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "T29: Renovate replaces Dependabot (mise manager at home/dot_mise/config.toml; manifest pins notification-only), ccusage references follow the org move, UA installer pinned to 6df3065, AGENTS.md codified as canonical with CLAUDE.md as Claude-only shim (operator 2026-09-27)"
```

cost: n/a
