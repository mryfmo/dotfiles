# U226b round 2: `--set-asset` can move `ref_commit`, so a harness bump updates the build's commit through the documented command

GOAL
Codex review thread 4488929392 on PR 674 (P2, frequency 4, severity 3, weight 12) is right: `SETTABLE_ASSET_FIELD` (`scripts/generate-agent-configs.py:294`) accepts only `pin`, `sha256` and `sha256.<arch>`, optionally under `fallback.`, so the documented pin workflow (`README.md:1275-1276`, `generate-agent-configs.py --set-asset NAME.FIELD=VALUE`) cannot move the new `ref_commit`, and the next harness tag bump would leave `DSH_COMMIT` at the old commit. This round admits `ref_commit` to the settable fields with a 40-lowercase-hex value rule and tests it. Nothing else changes.

SCOPE
The same branch `fix/dsh-build-commit-input` in your tree, on top of 9a0170e6 (your HEAD). May write: `scripts/generate-agent-configs.py` (`SETTABLE_ASSET_FIELD`, `set_asset_field` and the message it prints), `tests/unit/test_generate_agent_configs.py`, and the body file `/tmp/claude/U226/U226-pr-body.md`. Nothing else.

CONTEXT
`set_asset_field` (`:297-322`) rejects a path outside `SETTABLE_ASSET_FIELD` with the message `--set-asset may change only pin, sha256, or sha256.<arch>, optionally under fallback.` and a value outside `PLAIN_PIN_VALUE`; `main()` (`:2830-2856`) applies each assignment, re-parses, checks the value read back as the same string, and renders the asset constants. The existing tests (`test_generate_agent_configs.py:482-620`) cover the rewrite, the fallback path, unknown targets, the refused fields (asserting the message text at `:594`) and the end-to-end update. `ref_commit` is already a known field of the validator (`validate-agent-assets.py:1344`).

CHANGE
1. `SETTABLE_ASSET_FIELD` admits `ref_commit` (not under `fallback.`); `set_asset_field` requires a `ref_commit` value to match `^[0-9a-f]{40}$` and fails with a message naming the field and the rule otherwise; the refusal message for other fields names `ref_commit` among the allowed ones.
2. Tests: (a) `set_asset_field(text, "deepseek-harness", "ref_commit", <40 hex>)` rewrites that scalar alone (extend the manifest fixture with a `ref_commit` line); (b) a 39-character, an uppercase and a non-hex value are refused with the message naming `ref_commit`; (c) `fallback.ref_commit` is refused; (d) the end-to-end `--set-asset deepseek-harness.ref_commit=<40 hex>` run renders the `DSH_COMMIT` constant (reuse the pattern of `test_set_asset_updates_the_manifest_and_renders_its_pins`); (e) update the asserted message text at `:594` to the new wording.
3. The body: a `## Round 2` section (the thread id, the admitted field and its rule), one threat row for the pin-update path, and the ACCEPTANCE lines under Verification.

ACCEPTANCE
1. `uv run python -m unittest tests.unit.test_generate_agent_configs -v 2>&1 | grep -E 'ref_commit|^Ran|^OK|FAILED'` shows the new tests OK and the module OK apart from the seat's pre-existing `test_audit_profile_renders_read_only_sandbox_override` denial (name it if it fails).
2. `uv run --with pyyaml scripts/generate-agent-configs.py --set-asset deepseek-harness.ref_commit=b830ec950faba0a46dda564be3e2d854afed94f1` prints `asset pins updated: deepseek-harness.ref_commit` and `git status --porcelain` is empty afterwards (the same value).
3. `make render-check` exit 0.
4. `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed` exit 0.
5. `git diff --stat 9a0170e6` names the generator and its test module alone.

VERIFY
The ACCEPTANCE commands in your tree with their result lines pasted into the body.

CLOSURE
allowlist

TRUST
TRUST: the round trusts the generator's existing rewrite of a named scalar and the validator's `ref_commit` field as reviewed mechanisms; it widens one field rule, adds tests, reads no network, and changes no other file.

TIMEBOX
25 minutes.

FORBIDDEN
No change to the validator, the updater, the manifest value or any other generator function; no amend of the round-1 commit; no local bats; no network read; no push; no `gh` call; no mention of any private design directory; none of the words in `.orchestration/orchestrate/regime-cutover/redact-words.txt` and no absolute home directory in tracked files or the PR body (write `~/...`).

WORKER RULES (standing orders 27, 29, 31, 34; read `preferences.md` lines 23 to 45 in the store)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in your tree. Never `git stash`. Before you report, `git -C ~/Workspace/dotfiles status --porcelain=v1 --untracked-files=all -- . ':!.orchestration/orchestrate' | shasum` must print the value the TASK line carries.
- Progress line in `/tmp/claude/U226/U226-progress.txt`.
- Commit unsigned: `git -c commit.gpgsign=false commit`. The message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Comments explain a non-obvious why only.

REPORT
Status, head sha (40 hex), `git diff --stat 9a0170e6`, the ACCEPTANCE result lines, deviations. Under 10 lines, ending with `head=<40 hex>`.

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` (standing orders 27, 29, 32, 34, 35); PR 674 review comment 4488929392; `briefs/U226-dsh-build-commit-input-pinned.md`.
