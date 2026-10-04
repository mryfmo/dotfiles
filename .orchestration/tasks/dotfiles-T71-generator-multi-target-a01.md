# AGMSG-TASK dotfiles-T71-generator-multi-target-a01

Drafted 2026-10-04 by the orchestrator seat from the approved correction plan (Phase 3, dotfiles-T71). Prerequisite for T72 (bootstrap pins) and T80 (Codex command hooks). Dispatch only after T91 (PR #245, `scripts/validate-agent-assets.py`) has merged; its other files are disjoint from every in-flight task.

## Objective

Principle 3 (one pin, one place): an asset can render one value into several files, and into `declare -r` assignments, so `setup.sh` and `scripts/lib/*.sh` can join the render set in T72 without hand-written literals.

1. **`scripts/generate-agent-configs.py` `render_asset_constants` (~223-243):**
   - accept `render:` as today's single mapping `{file, constants}` **or** a list of such mappings; every target file is rewritten with its own constants, and the same `outputs[path]` accumulation keeps two assets (or two entries) that render into one file consistent;
   - the assignment regex becomes `^((?:readonly |declare -r )?NAME=)"[^"$`\\]*"$` so a `declare -r NAME="…"` line is rewritten exactly like `readonly NAME="…"`; the `exactly once` rule is per (file, constant).
2. **`scripts/validate-agent-assets.py`:**
   - `LITERAL_VERSION_ASSIGNMENT` (~497-499) also matches `declare -r ` as a prefix, so an unrendered `declare -r X_VERSION="1"` is reported like `readonly`;
   - the `rendered` set (~603-605) is built from every render entry when `render` is a list;
   - **do not** add `setup.sh` or `scripts/lib` to the scanned roots (~606): `setup.sh:34` still hard-codes `CHEZMOI_VERSION` until T72 declares the `chezmoi-bootstrap` asset, and the scan must not fail on `main` in between. T72 adds the root together with the asset.
   - validate the shape: each render entry has a string `file` and a non-empty `constants` mapping of string → string; a list entry that is not a mapping fails with the asset name in the message.
3. **Tests:** `tests/unit/test_generate_agent_configs.py` (around `test_asset_constants_render_into_their_files`, 147-180): a list render writes two files from one pin; a `declare -r` assignment is rewritten once and only once; a target without the assignment still fails with the existing "must assign … exactly once" message. `tests/unit/test_validate_agent_assets.py` (around 335 and 450): `declare -r X_VERSION="1"` in `install/` is reported unless rendered; a list render marks every (file, constant) as rendered.
4. `make render-check` must exit 0 with byte-identical outputs; the manifest is not touched (every current `render:` stays a single mapping).

Forbidden: `home/dot_agents/agent-config.yaml`; any pin value; `setup.sh`, `scripts/lib/**`, `.github/**`, `Dockerfile` (T72); new CLI flags.

[memory:decision] dotfiles-T71 (operator 2026-10-03): `generate-agent-configs.py` renders one asset pin into several target files (`render:` accepts a list) and into `declare -r` assignments; `validate-agent-assets.py` recognises `declare -r` literals; the scanned roots stay `install/` and `scripts/` until T72 adds the bootstrap asset.

## Repo / branch

- Work ONLY in your own worktree. `git fetch origin`; `git switch -c feat/generator-multi-target origin/main` (the commit that merged PR #245 or later; `grep -c '\\bsk-' scripts/validate-agent-assets.py` → 1 confirms it). Verify the dispatched task_rev; else stop and PONG blocked.
- Strict status checks: if `main` moves, `gh pr update-branch <pr>` and wait for CI again before RESULT.

## Allowed files

- `scripts/generate-agent-configs.py`, `scripts/validate-agent-assets.py`, `tests/unit/test_generate_agent_configs.py`, `tests/unit/test_validate_agent_assets.py`
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dotfiles-T71-generator-multi-target-a01.md` (main checkout)

## Validation commands (paste verbatim output)

```
git diff origin/main --stat
make render-check
uv run python -m unittest tests.unit.test_generate_agent_configs tests.unit.test_validate_agent_assets 2>&1 | tail -3
make unit-test
make validate-agent-assets
gh pr checks <pr-number>
gh api repos/mryfmo/dotfiles/pulls/<pr-number> --jq '.mergeable_state'
```

## Completion

1. PR to `main`, English title/description ending with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. CI green on the final head, branch up to date.
2. After the final push: `gh pr checks <pr> --watch`; wait (≤15 min) for the Codex Bot on that head by listing `gh api repos/mryfmo/dotfiles/pulls/<pr>/reviews --jq '.[]|select(.user.type=="Bot")|[.commit_id,.submitted_at]|@tsv'`; fix P0/P1 inline findings and repeat; close your crit server if Plan Mode opened one; do not resolve threads. The RESULT names every unresolved thread with `fixed:<sha>` or a proposed `not-applicable:<reason>`.
3. Artifacts at the exact expected paths; validation with verbatim outputs, PR number, head SHA.
4. CompactionDB `memory add --kind decision --scope project` with the `[memory:decision]` text from the main checkout; paste command and output.
5. `AGMSG-RESULT v1` via `agmsg-dispatch dotfiles <your identity> claude-remediation-dot wT:p1 "<single line>"` (outside the sandbox). `cost:` line. max_turns=30.

## Dispatch

- 2026-10-04 06:35Z to `claude-standard-dot-a005` (worker-c, wT:p2) right after its T91 acceptance (PR #245 merged as `312fef3f`). Branch from `origin/main` 312fef3f or later; keep `fix/secret-scan-sk-boundary` and `chore/bootstrap-dead-code` untouched. Disjoint from T68 (`scripts/require-crit-review.py`, a006), T88 (SKILL, a006) and T92 (`scripts/agent-stop-gate.sh`, a007).

## Revise round 1 (orchestrator, 2026-10-04 08:05Z) — task-level audit of 3ecb4876 is `incorrect`

1. **P2, symlink aliases bypass render-conflict detection.** The auditor reproduced two canonical relative paths reaching one file through a symlink, with the later write overwriting the pin. Key the conflict map on the resolved real path (`(ROOT / file).resolve()`, or `os.path.realpath`) in addition to requiring the canonical spelling; test with a fixture symlink inside the temp tree. This also turns Bot thread 4176458271 into `fixed:<sha>`; the orchestrator re-replies.
2. **P2, evidence: the symlink check in the validation file cannot match.** `git ls-files -s` prints `<mode> <sha> <stage>\t<path>`, so a `^(install|scripts|setup)` filter never matches; use `git ls-files -s install scripts setup.sh | awk '$1 == "120000"'` and paste the real output.
3. **P2, evidence: summary labels instead of verbatim output** for the final-head `make render-check` and `make validate-agent-assets` entries. Paste the commands and their complete output.

One commit for item 1 (code + test), artifact edits for items 2-3, `gh pr update-branch 249` if `main` moved, CI, Bot (paginated listing), RESULT naming every thread. Interleave with T94 as you see fit; both are yours.

## Revise round 2 (orchestrator, 2026-10-04 09:55Z) — task-level audit of c7b5fb3d is `incorrect`

1. **P2, `outputs` keyed by unresolved path.** With `alias.sh -> pins.sh`, a render list that updates VERSION and SHA256 through the alias and VERSION through the target passes validation (different constants, no conflict) but produces two independent snapshots in `render_asset_constants`, and the last write restores the old checksum. Accumulate `outputs` by the resolved target path (`(ROOT / entry["file"]).resolve()`, written back to that real path) so every entry for one file edits one snapshot; add a test with a fixture symlink and compatible mappings through alias and target that asserts both constants end up in the one file. Keep the validator's `rendered` set on the canonical spelling.

One commit; `gh pr update-branch 249` if `main` moved; CI; Bot (paginated listing); RESULT. Standing directive applies.
