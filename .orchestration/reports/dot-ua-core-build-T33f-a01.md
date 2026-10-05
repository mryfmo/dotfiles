# T33f report — dot-ua-core-build-T33f-a01 (revision 2)

- worker: `claude-standard-dot-a005`; orchestrator: `claude-remediation-dot`
- worktree: `~/Workspace/dotfiles/.claude/worktrees/worker-c` (clean before the switch)
- branch: `fix/ua-core-build` from `origin/main` = `7b42472`
- task_rev: sha256 `97c01daa9f1be4a3b566fa6a563b2607524839ff6c0d750405e6ef546688a0af`, checked
- PR: https://github.com/mryfmo/dotfiles/pull/201, head `657bfe4fef083b0cf4c22bb7bdc34b915eb29ffe` (rev2; rev1 head `3d63f0a`)
- status: ready_for_review (revision 2). CI is green on head 657bfe4: all checks pass except nix, which was skipped. Verbatim `gh pr checks 201` output is in the validation file.

## Revision 2 (AGMSG-ACCEPTANCE status=revise, 2026-09-28T11:01:31Z)

The visible-lane audit of `3d63f0a` gave `Verdict: incorrect`, with one
high-confidence P2 confirmed by the orchestrator. `build_understand_anything_core`
skipped whenever `dist/index.js` existed, so the doctor's "core build is
stale; run make update" warning could not be repaired by `make update`.

- **Fix, commit `657bfe4`, same branch and PR #201.** The guard now
  rebuilds when `packages/core/dist/index.js` is missing **or** older than
  any **file** under `packages/core/src` or the root `pnpm-lock.yaml`:
  ```
  find src pnpm-lock.yaml -type f -newer dist/index.js -print -quit
  ```
  It skips otherwise.
- **Why `-type f`.** Directory entries do not count, matching the doctor's
  files-only scan. Without it the `src` directory entry itself matched,
  which the fresh-dist test caught. `-newer` means strictly newer, and the
  `|| true` keeps a missing lockfile from aborting under `set -e`.
- **Doctor.** `understand_anything_core_warnings` now uses the same rule,
  so the root `pnpm-lock.yaml` counts as an input too. The stale message is
  `… is older than <src> or <pnpm-lock.yaml>; run make update`. The two
  docstrings cross-reference each other.
- **Tests.**
  - (i) `test_rebuilds_a_release_dist_older_than_its_sources`: subtests
    `newer=src` and `newer=lockfile`. The stale dist gets rebuilt
    (install, then build) and the fresh `built` dist is copied into the
    clone.
  - (ii) the existing fresh-dist skip test now sets explicit mtimes, with
    dist newer than both src and the lockfile, and asserts no pnpm call.
  - (iii) `test_doctor_stale_warning_is_cleared_by_the_update_build`
    covers the repair path end to end: the doctor reports 1 stale WARN for
    the clone, the update build runs (no release artifact, so it builds in
    the clone), and the doctor then reports `[]`.
  - The doctor also gains
    `test_ua_core_warns_when_dist_is_older_than_the_root_lockfile`, and
    the stale-src test now expects the updated message. `find` was added to
    the test PATH's symlinked tools.
- **README.** The sentence now states the shared rule and that
  `make update` repairs what the doctor reports.
- **Mutation baseline** against the unmodified `3d63f0a` scripts (checked
  as no diff from HEAD before the run): **5 failures** across 14 tests.
  They are the two rebuild subtests, the doctor-repair path, and the two
  doctor stale-message checks (src and lockfile). After the change, 50/50
  pass in the two files; `make unit-test` gives 508 OK;
  `make validate-agent-assets` is ok; `shellcheck -x` and `shfmt` are clean.
  Plain `shellcheck` still shows only the pre-existing SC1091 infos. All
  verbatim in the validation file.

## Changes (revision 1)

1. **`scripts/update-agent-assets.sh`.** A new
   `build_understand_anything_core <tree>` (shdoc in English). It:
   - returns silently when `<tree>/packages/core` is absent;
   - returns early when `packages/core/dist/index.js` already exists, which
     is upstream's idempotence guard;
   - resolves pnpm in this order: `pnpm` on PATH (after `main`
     prepends `~/.local/share/mise/shims`, this is the shim for the pinned
     `npm:pnpm`), then `mise exec npm:pnpm -- pnpm`, which uses the manifest
     pin; otherwise it prints `WARN: Understand-Anything core not built:
     pnpm not found; run: cd <tree> && pnpm install --frozen-lockfile &&
     pnpm --filter @understand-anything/core build` and returns 0;
   - runs upstream's exact command in a subshell, `cd <tree> &&
     { pnpm install --frozen-lockfile 2>/dev/null || pnpm install; } &&
     pnpm --filter @understand-anything/core build`. On failure it prints
     `WARN: Understand-Anything core build failed in <tree>; run: …` and
     returns 0, so `make update` is never failed by it.

   `provision_codex_understand_anything_runtime` calls it on the
   **release artifact** before the existing copy loop, which then copies
   `dist` and `node_modules` into the Codex clone as before. When no
   matching release artifact exists, including when python3 is missing and
   nothing can be resolved, it builds directly in the **Codex clone** after
   the existing message. That message is kept verbatim, because
   lifecycle.bats and the validator grep for it.
2. **pnpm pin.** `home/dot_mise/config.toml` gets `"npm:pnpm" = "12.4.1"`
   with a one-line reason, following the existing `npm:` tool pattern.
   `home/dot_mise/mise.lock` gets `[[tools."npm:pnpm"]] version/backend`,
   in alphabetical position, the same shape as the other `npm:` entries,
   which carry no per-platform checksums.
   - **Window check** (read-only `gh api repos/pnpm/pnpm/releases`,
     verbatim in the validation file): now is 2026-09-28T10:39Z, so the
     cutoff is 2026-09-21T10:39Z. v12.4.1 was published 2026-09-10T17:00Z,
     18 days ago, which is **outside the window**, so no PONG was needed.
   - I chose 12.4.1 because the plugin declares no `packageManager`, its
     lockfile is `lockfileVersion: '9.0'` (pnpm ≥ 9), and 12.4.1 is the
     version the orchestrator used successfully.
   - For reference, the newest release outside the window is v12.5.1
     (09-18). v12.6.0, v12.7.0 and v12.8.0 are inside it. Bumping later is
     `make upgrade`'s job; I did not do it here.
3. **`scripts/check-agent-runtime.py`.** New
   `understand_anything_core_warnings(home)`, wired into `check()` before
   the chezmoi drift warnings. It is quiet when there is no Codex clone
   (`~/.understand-anything/repo/understand-anything-plugin/packages/core`).
   Otherwise it reports:
   - `WARN: Understand-Anything core not built: <dist/index.js> is missing;
     run make update` when `dist/index.js` is absent;
   - `WARN: Understand-Anything core build is stale: <dist/index.js> is
     older than <src>; run make update` when the newest file under `src` is
     newer than `dist/index.js`.

   Both are `WARN:` lines, so doctor's exit code is unchanged.
4. **`README.md`.** One sentence in the Understand-Anything paragraph about
   the core build in `make update` and the doctor warning.
5. **Tests.**
   - New `tests/unit/test_update_agent_assets_ua_core.py`. It uses a fake
     HOME with a clone and a release artifact at the same version, and a
     restricted PATH containing only symlinked python3, bash, cat, cp,
     dirname, mkdir and rm plus fake `pnpm`/`mise` that log `cwd|argv` and
     create `dist` on build. The script is sourced (it has a `BASH_SOURCE`
     guard) and the function called directly. Cases:
     - (a) the build runs in the release artifact and is copied into the
       clone;
     - the frozen-install fallback;
     - (b) the build is skipped when `dist` exists;
     - the build runs in the clone when there is no release artifact;
     - the `mise exec npm:pnpm` fallback;
     - (c) a WARN when no pnpm is resolvable;
     - a WARN when the build fails.
   - `tests/unit/test_check_agent_runtime.py` gets (d): a missing dist
     WARNs (and `is_warning` is true), a stale dist WARNs, a fresh dist or
     no clone is quiet, and `check()` includes the new warnings.
   - **Mutation baseline** against the unmodified scripts (checked as no
     diff against origin/main at run time): **10 of 11** new tests fail or
     error. The dist-present skip case passes on both versions, as a
     regression guard for the existing copy behaviour. Verbatim in the
     validation file.

## Validation notes

- `make validate-agent-assets` is ok, `make unit-test` gives 505 OK, and
  `shfmt` is clean.
- Plain `shellcheck scripts/update-agent-assets.sh` exits 1, but only on
  SC1091 *info* notes about the sourced `lib/asset-manifest.sh` and
  `lib/installer-pins.sh`. Those are pre-existing and identical on
  `origin/main`, where the same run shows the same three SC1091 lines. The
  CI-style `shellcheck -x` exits 0. Both outputs are pasted.
- No real `update-agent-assets.sh`, `make update`, `mise install`, `pnpm`
  or network install was run. Everything was exercised through fake CLIs.
  The only network access was the read-only `gh api` release listing.
  Live verification (`make update` on this host after merge) is
  orchestrator-side.

## CompactionDB

[memory:decision] T33f: `update-agent-assets.sh` builds Understand-Anything `packages/core`
idempotently after provisioning the Codex-side clone using a mise-pinned pnpm, and
`make doctor` warns when `dist` is missing or stale, so `.ua/` incremental updates never
depend on a manual build (operator 2026-09-28).

Id `fff493a7-0f62-4b37-99d1-c965e1c9c05a`; the output is in the validation
file.

## Effects

None executed. The shipped script, once run by `make update`, will write
`packages/core/dist` and `node_modules` into the Claude plugin cache
release artifact and the Codex clone. That is upstream-sanctioned in-place
build output, removable with `rm -rf <tree>/packages/core/dist
<tree>/packages/core/node_modules <tree>/node_modules`. The next
`update_codex_understand_anything` re-provisions it anyway.

cost: n/a (the Claude Code runtime does not expose session token/cost figures to the worker)
