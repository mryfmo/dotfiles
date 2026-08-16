# T61a: CI fixes for PR #128 — chezmoi-rendered sourcing + shellcheck

task_id: T61a
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-conformance
worker: codex-deep-dot
plan: PLAN-harness-composability-integration.md (Phase 7; CI failures on PR #128)

[memory: failure — update-agent-assets.sh is ALSO executed as a chezmoi-rendered /tmp script via run_once_after_06-install-agent-assets.sh.tmpl ({{ include }}); a BASH_SOURCE-relative `source lib/...` therefore fails in bootstrap. Any file split of a chezmoi-included script must be inlined by the template or guarded.]

## CI evidence (orchestrator-extracted)

1. public-bootstrap (both OS):
   `/tmp/....sh: line 14: /tmp/lib/asset-manifest.sh: No such file or directory`
   -> chezmoi renders home/.chezmoiscripts/common/run_once_after_06-install-agent-assets.sh.tmpl
   (content: `{{ include "../scripts/update-agent-assets.sh" }}`) into /tmp;
   the T57 `source "${AGENT_ASSET_SCRIPT_DIR}/lib/asset-manifest.sh"` cannot
   resolve there.
2. test (ShellCheck):
   - scripts/lib/asset-manifest.sh:98 SC2016 (single-quoted jq filter —
     intentional jq variables)
   - scripts/update-agent-assets.sh:13 SC2155 (declare-and-assign)
   - scripts/update-agent-assets.sh:14 SC1091 (source not followed)

## Fix (exact)

1. Wrapper template: change
   home/.chezmoiscripts/common/run_once_after_06-install-agent-assets.sh.tmpl
   to include the lib BEFORE the main script:
   ```
   {{ include "../scripts/lib/asset-manifest.sh" }}
   {{ include "../scripts/update-agent-assets.sh" }}
   ```
2. update-agent-assets.sh: make the source guarded and shellcheck-clean:
   - split declare/assign (SC2155);
   - only source when the manifest function is not already defined
     (`if ! declare -F manifest_record >/dev/null 2>&1; then source ...; fi`)
     so the inlined bootstrap rendering skips the source;
   - add `# shellcheck source=scripts/lib/asset-manifest.sh` (SC1091).
     Verify asset-manifest.sh tolerates being INLINED before the main
     script under `set -Eeuo pipefail` (no top-level side effects beyond
     function definitions and readonly constants; adjust if needed —
     double-inclusion must also be harmless).
3. asset-manifest.sh: add a targeted
   `# shellcheck disable=SC2016` with a one-line justification comment on
   the jq filter (do not rewrite the filter).
4. Tests: add one unit test simulating the chezmoi rendering — concatenate
   lib + main into one temp file (in that order), `bash -n` it, and
   execute a harmless function path (e.g. manifest_record into a fake
   HOME) to prove the inlined form works; keep all existing tests green.
5. Run shellcheck locally on both files with the CI's default settings
   and paste clean output.

## Allowed files

- home/.chezmoiscripts/common/run_once_after_06-install-agent-assets.sh.tmpl
- scripts/update-agent-assets.sh (guard + shellcheck lines only)
- scripts/lib/asset-manifest.sh (shellcheck directive only; plus minimal
  inline-safety adjustment if step 2 verification requires it)
- tests/unit/ (matching module)
- Your artifact paths (T61a five artifacts)

## Forbidden actions

git commit; git push; chezmoi apply; bats; dependency changes; behavior
changes beyond the sourcing guard; weakening any T57 semantics.

## Validation

1. shellcheck clean on both scripts (paste).
2. `make format`; `bash -n`; `make unit-test` all green (totals + new).
3. `make validate-agent-assets` green.
4. Concatenated-rendering test transcript.
5. `git status --porcelain` / `git diff --stat` -> only Allowed files.

## Completion / RESULT contract

Five artifacts (T61a set); memory add with the failure fact
(--kind failure); effects=none expected.
Reply `AGMSG-RESULT v1 task_id=T61a status=ready_for_review`. max_turns=15.
