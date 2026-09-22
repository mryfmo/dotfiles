# dot-ubuntu-parity-T5-a01 — worker report

status: ready_for_review

## Objective

CI run 35796642953 failed the Snippet install workflow's public-bootstrap
(ubuntu-latest, client) job:

```
Failed to enable unit: Unit file usage-snapshot.timer does not exist.
chezmoi: .chezmoiscripts/ubuntu/60-enable-usage-snapshot-timer.sh: exit status 1
```

Root cause: chezmoi runs `.chezmoiscripts` entries in target-name lexical
order, interleaved with target-state application. `.chezmoiscripts/...`
sorts before `.config/...`, so on a fresh bootstrap the
`run_onchange_60-enable-usage-snapshot-timer.sh.tmpl` script ran before
`home/dot_config/systemd/user/usage-snapshot.{service,timer}.tmpl` had been
applied to disk. Already-provisioned machines didn't reproduce this because
the unit files already existed from a prior apply.

## Work done

One commit, `026ce2e`:

`fix(usage): run timer enablement after files are applied`

- `git mv home/.chezmoiscripts/ubuntu/run_onchange_60-enable-usage-snapshot-timer.sh.tmpl home/.chezmoiscripts/ubuntu/run_onchange_after_60-enable-usage-snapshot-timer.sh.tmpl`
  — content unchanged, only the filename changes. chezmoi's `after_`
  attribute defers execution until all target state has been applied,
  matching the existing `run_once_after_04-install-aws-cli.sh.tmpl`
  convention already in this repo.

## Other new scripts checked (not affected)

Confirmed by reading each script's rendered content (pasted in validation)
that none of T4's other new `run_once_*` scripts depend on chezmoi-applied
files, so none share this ordering bug:

- `run_once_52-client-install-zed.sh.tmpl` — only includes
  `scripts/lib/installer-pins.sh` and `install/ubuntu/client/zed.sh`
  (both repo-tracked source files included at render time, not
  chezmoi-managed target files).
- `run_once_53-client-install-tailscale.sh.tmpl` — only includes
  `install/ubuntu/client/tailscale.sh`.
- `run_once_99-client-gnome-defaults.sh.tmpl` — only includes
  `install/ubuntu/client/gnome_settings.sh`.
- `run_once_50-server-setup-timezone.sh.tmpl` — only includes
  `install/ubuntu/server/setup_timezone.sh`.

None of these reference a path under `home/dot_config/**` or any other
chezmoi target file, so `run_once_` (not `run_once_after_`) is correct for
all four as-is. No further changes made.

## Test-name references

Searched for any test or template referencing the old filename
(`run_onchange_60-enable-usage-snapshot-timer` or
`60-enable-usage-snapshot`) — no matches (see validation). Nothing else
needed updating for the rename.

## Branch

Per the task's forbidden_actions note ("feat/ubuntu-parity は main へ
マージ済みのため、新ブランチ `fix/usage-timer-ordering` を main から切って
作業"), independently verified before branching that `origin/main` already
contains all of T2/T3/T4's content (same commit messages, different hashes —
confirms a rebase/re-apply rather than a fast-forward merge; see validation
for the exact verification commands and output). Created
`fix/usage-timer-ordering` from `origin/main` in this worktree per the task's
explicit instruction, since the tree was clean (no unrelated in-progress
work to protect).

## Validation

`make format`, `uv run python -m unittest discover -s tests/unit -v` (376
tests, OK, 1 pre-existing skip), and `uv run --with pyyaml
scripts/validate-agent-assets.py` all green — verbatim/tail output in
`.orchestration/validation/dot-ubuntu-parity-T5-a01.md`.

## CompactionDB

Registered a `[memory:decision]` about chezmoi's script-ordering /
`_after_` convention:

```
python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "chezmoi executes .chezmoiscripts entries in target-name lexical order interleaved with file application (.chezmoiscripts/... sorts before .config/... on a fresh bootstrap). A script that depends on files chezmoi applies (e.g. enabling a systemd unit shipped via home/dot_config/**) must use the run_onchange_after_ / run_once_after_ prefix so chezmoi defers it until all target state is applied, matching the existing run_once_after_04-install-aws-cli.sh.tmpl convention."
```

Returned ID: `ebab46ec-b613-400d-91ac-2b2a0de8ee88`

## Scope / forbidden actions

No files touched outside `allowed_files`. No push, no PR, no `chezmoi
apply`, no writes under `$HOME`, no commits to `main` (new branch
`fix/usage-timer-ordering` used instead, per the task's own instruction).

## cost

n/a (runtime does not expose token/cost figures to this session).
