# AGMSG-TASK dot-version-currency-T29-a01

## Objective

Operator directive (2026-09-27): repo-side portion of the version-currency
remediation decided after the 2026-09-27 research pass (decision record:
`.agents/worklog/claude/dotfiles-golden-sunbeam.md`, orchestrator plan). Four
deliverables: (1) adopt Renovate and remove Dependabot; (2) follow the ccusage
upstream org move (ryoppippi → ccusage org) in repository references —
WITHOUT bumping the ccusage version (that is `make upgrade` lane, operator
side); (3) bump the Understand-Anything installer pin to upstream main
`6df3065` via the sanctioned `--set-asset` path; (4) codify the
AGENTS.md-canonical decision in AGENTS.md.

Research facts to rely on (verified 2026-09-27, do not re-research):

- Dependabot supports only fixed ecosystems (no custom manifests, no mise);
  the current `.github/dependabot.yml` covers github-actions weekly only.
- Renovate has a first-class `mise` manager, but its default file match does
  NOT include this repo's chezmoi source path `home/dot_mise/config.toml` —
  it needs a `managerFilePatterns` override. Renovate CANNOT recompute this
  repo's `trusted_hash`/`sha256.<arch>` asset fields, so `agent-config.yaml`
  pin bumps must be notification-only, never auto-merged.
- Understand-Anything upstream main HEAD is `6df3065` (2026-09-12); our
  installer pin `797ce7969312411be2e125c39628854166f055d7` is 81 commits
  behind; interim commits are fixes, no breaking changes. The asset's
  `source: git-commit` pin is the commit hash itself (no paired sha256).
- Claude Code ≥ 2.1.277 reads AGENTS.md natively; official guidance says a
  CLAUDE.md containing `@AGENTS.md` may stay and never causes a double read.

[memory:decision] T29: Renovate replaces Dependabot (github-actions manager;
mise manager pointed at home/dot_mise/config.toml; agent-config.yaml pins
notification-only because Renovate cannot recompute sha256 fields); ccusage
references follow the upstream org move; UA installer pinned to 6df3065;
AGENTS.md documents itself as canonical with CLAUDE.md as the Claude-only
shim (operator 2026-09-27).

## Repo / branch

- Work ONLY in `/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c`.
- `git fetch origin`, then `git switch -c feat/version-currency origin/main`.
  (Verify the dispatched task_rev sha256 against this file on your base, else
  stop and PONG.)
- If the worktree has uncommitted files, stop and report via AGMSG-PONG.

## Changes

### 1. Renovate adoption

- New `renovate.json` (repo root, schema-referenced):
  - `github-actions` manager enabled (replaces Dependabot 1:1).
  - `mise` manager with `managerFilePatterns` matching
    `home/dot_mise/config.toml`.
  - `customManagers` regex entries for `pin:` fields in
    `home/dot_agents/agent-config.yaml` with the `github-releases` datasource
    for the GitHub-release assets (mise, sheldon, starship, tode,
    terminal-browser, crit, zed) — configured NOTIFICATION-ONLY: use
    `dependencyDashboard: true` plus `dependencyDashboardApproval: true` (or
    draft PRs) for exactly these custom-manager packages, with a comment in
    the JSON stating why (sha256/trusted_hash pairing lives in
    `upgrade-tools.sh --set-asset`; a bare pin bump would break `verify:`).
  - Weekly schedule; group minor/patch updates; label `dependencies`.
  - Validate with `npx --yes renovate-config-validator renovate.json` and
    paste the verbatim output (one-off npx run; do not add a dependency).
- Delete `.github/dependabot.yml` (Renovate's github-actions manager covers
  it; running both is redundant).
- If any validator/test/docs reference dependabot.yml, update them (report
  which).

### 2. ccusage upstream org move (references only)

- Find every repository reference to the old upstream
  (`ryoppippi/ccusage`, or ccusage GitHub URLs under the old org) with a
  repo-wide grep; update each to the `ccusage` org equivalent. Paste the
  grep output before and after in the validation file.
- Do NOT change the ccusage version pin anywhere (mise config/lock, workflow,
  tests, check script stay at 20.0.23) — the version bump is `make upgrade`
  lane and out of scope.
- If zero references exist, state that with the grep evidence and skip.

### 3. Understand-Anything installer pin

- `uv run --with pyyaml scripts/generate-agent-configs.py --set-asset understand-anything-installer.pin=6df3065<full-40-hex>` —
  resolve the full 40-char commit sha from
  `https://github.com/Egonex-AI/Understand-Anything` main (verify it is
  reachable and on main; paste the resolution command output). Then
  regenerate and `--check`; expected diff limited to the manifest and its
  rendered pin constants (report exact files).

### 4. AGENTS.md canonicality note

- Add a short section (≤6 lines) near the top of AGENTS.md: AGENTS.md is the
  canonical agent instruction file for every runtime; `CLAUDE.md` is a
  Claude-only shim that must contain nothing but the `@AGENTS.md` import and
  the compactiondb-managed block; new repository rules go here, never into
  CLAUDE.md.

### 5. Tests

- Only where code changed. `--set-asset` and renovate.json need no new unit
  tests; run the existing suites. If step 1 or 2 touched any script under
  `scripts/`, cover the change with the existing test pattern and a mutation
  baseline.
- No local bats (repo policy).

## Allowed files

- `renovate.json` (new)
- `.github/dependabot.yml` (delete)
- `AGENTS.md`
- `home/dot_agents/agent-config.yaml` (via --set-asset only)
- generated pin render targets owned by --set-asset (report exact paths, e.g.
  `scripts/lib/installer-pins.sh`)
- files containing old-org ccusage references found in step 2 (list each in
  the report; keep the set minimal)
- any validator/docs references to dependabot.yml (report each)
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dot-version-currency-T29-a01.md` (main checkout)

## Forbidden actions

- Any version bump other than the UA installer pin (no mise/uv/node/ccusage
  version changes — `make upgrade` lane).
- Changing model_profiles, worker/interactive/audit settings, herdr-agents,
  permgate, hooks configs, dependencies (npx one-off validator excepted), or
  `reviews/ADH_Integrated_Plan/`.
- Editing CLAUDE.md.
- Merging; force push; local bats; `make apply`/`chezmoi apply`; writes
  outside the worktree except the listed `.orchestration` paths.

## Validation commands (paste verbatim output)

```
npx --yes renovate-config-validator renovate.json
uv run --with pyyaml scripts/generate-agent-configs.py --check
make validate-agent-assets
make unit-test
git -C /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c diff origin/main --stat
gh pr checks <pr-number>
```

## Completion

1. PR to `main`, English title/description ending with
   `🤖 Generated with [Claude Code](https://claude.com/claude-code)`.
   Watch CI to green.
2. Artifacts at the exact expected paths, validation with verbatim outputs
   and the PR number/head SHA.
3. CompactionDB from the main checkout:
   `python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "T29: Renovate replaces Dependabot (mise manager at home/dot_mise/config.toml; manifest pins notification-only), ccusage references follow the org move, UA installer pinned to 6df3065, AGENTS.md codified as canonical with CLAUDE.md as Claude-only shim (operator 2026-09-27)"`
   — paste command and output.
4. `AGMSG-RESULT v1` with all artifact paths; `cost:` line in the report.
