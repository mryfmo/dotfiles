# T37: Provision the Understand-Anything core dist in the Codex install path

## Objective

Fix the gap found in T36: the Codex-side vendor installer clones the raw
Understand-Anything source, but the analysis scripts require the prebuilt
`understand-anything-plugin/packages/core/dist/` (plus runtime
`node_modules`), which only ships in the Claude plugin release artifact.
Extend `update_codex_understand_anything` in `scripts/update-agent-assets.sh`
so a fresh install is immediately runnable.

## Approach (required)

After the pinned installer runs successfully, provision the runtime by copying
the official release artifact from the Claude plugin cache when available:

- Source: the highest-version directory under
  `~/.claude/plugins/cache/understand-anything/understand-anything/<version>/`
  whose `.claude-plugin/plugin.json` version matches
  `~/.understand-anything/repo/understand-anything-plugin/.claude-plugin/plugin.json`.
- Copy `packages/core/dist`, `packages/core/node_modules` (if present), and
  the top-level `node_modules` into
  `~/.understand-anything/repo/understand-anything-plugin/`, replacing any
  existing copies (`rm -rf` the destination dirs first so stale artifacts
  never mix).
- If no version-matched Claude cache exists, print a clear skip message
  (`Understand-Anything Codex runtime not provisioned: no matching Claude
plugin release artifact; run make update after installing the Claude
plugin.`) and return 0 — do NOT fall back to `pnpm install`/`pnpm build`
  (supply-chain policy: no dependency postinstall execution in the lifecycle).

Keep the existing shdoc comment style (English), `set -Eeuo pipefail`
compatibility, shellcheck/shfmt (`shfmt -i 4 -sr`) cleanliness, and the
non-fatal `|| true` posture of sibling functions.

## Also update

- `tests/install/common/lifecycle.bats`: extend the Understand-Anything test
  with grep assertions for the new provisioning lines (copy + skip message).
- `scripts/validate-agent-assets.py` `validate_understand_anything_assets()`:
  add tokens for the provisioning function/lines.
- `README.md` Understand-Anything paragraph: one sentence stating the Codex
  runtime is provisioned from the version-matched Claude release artifact.

## Scope / allowed files

- `scripts/update-agent-assets.sh`
- `scripts/validate-agent-assets.py`
- `tests/install/common/lifecycle.bats`
- `README.md`
- The five `.orchestration/**` artifact files below.

## Forbidden actions

- No git commits, branches, pushes, staging (the orchestrator handles git).
- No running `pnpm install` / `npm install` anywhere.
- No bats execution locally (CI-only policy); validate with
  `bash -n`, `shellcheck -x`, `shfmt -i 4 -sr -d`, and
  `uv run --with pyyaml scripts/validate-agent-assets.py` instead.
- No edits to `~/.understand-anything` or `~/.claude/plugins` (script code
  only; do not run the new function against the live environment).

## Validation

Record in the validation file the full output of:

- `bash -n scripts/update-agent-assets.sh`
- `shellcheck -x scripts/update-agent-assets.sh`
- `shfmt -i 4 -sr -d scripts/update-agent-assets.sh`
- `uv run --with pyyaml scripts/validate-agent-assets.py`
- A replay of each new bats grep assertion (grep commands run directly).

## Expected artifacts

- report: `.orchestration/reports/T37-understand-anything-codex-dist.md`
- validation: `.orchestration/validation/T37-understand-anything-codex-dist.md`
- sandbox: `.orchestration/sandboxes/T37-understand-anything-codex-dist.md`
- learning: `.orchestration/learning/T37-understand-anything-codex-dist.md`
- autoskill: `.orchestration/autoskill/runs/T37-understand-anything-codex-dist.md`

## Done signal

`AGMSG-RESULT v1 task_id=T37-understand-anything-codex-dist
status=ready_for_review|blocked` with all artifact paths. Max turns: 25.
