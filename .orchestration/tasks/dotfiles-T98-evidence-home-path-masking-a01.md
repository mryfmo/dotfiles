# AGMSG-TASK dotfiles-T98-evidence-home-path-masking-a01

Drafted 2026-10-05 by the orchestrator seat (dispatched 04:30Z to `claude-standard-dot-a005`, worker-c) from the Codex Bot finding on the boundary PR #273 (local `/home/<user>` paths and agent-skill/plugin locations in committed audit transcripts and worker artifacts). Independent of other tasks except `scripts/validate-agent-assets.py` (the masker); dispatch when no other task holds that file.

## Objective

Committed evidence carries no workstation-specific home paths.

1. **Masker:** `scripts/validate-agent-assets.py --mask-secrets` also normalises the running user's home directory (`$HOME` and `/home/<user>` or `/Users/<user>` forms) to `~` in the files it masks, and the repository secret scan treats a literal home path in `.orchestration/**` as a finding (so a future boundary commit cannot reintroduce them). Tests for both.
2. **`herdr-agents --audit`:** the audit transcript masking step already calls the masker; confirm the home-path normalisation applies to `<task>-audit-<sha7>.md` and its `.last.md` (test with a fake transcript).
3. **One-time re-mask:** run the masker over every tracked `.orchestration/**` file and commit the result in this PR (the diff is mechanical; paste `git diff --stat`). The gate's byte-exact comparison of PR-feedback item bodies is unaffected (bodies hold GitHub text, not local paths), but if any `-pr-feedback.json` changes, say so.
4. SKILL Stop checklist and the boundary procedure name the masker as the step before every boundary commit (one sentence each; T83, merged as 61806f56, did not place it). Use the runnable form `uv run --no-project --with pyyaml scripts/validate-agent-assets.py --mask-secrets <files>`.
5. **Validator scope:** repository-wide `rglob` scans in `scripts/validate-agent-assets.py` (for example `validate_no_removed_claude_skill`) skip the gitignored CompactionDB ledger `.claude/contextdb/state/**` (and any other gitignored local state they currently read), so a worktree whose session ledger quotes a removed token no longer fails `make validate-agent-assets` locally while CI passes (T83 incident, report section 4). Test with a fixture ledger file.

Forbidden: changing what counts as a secret for credentials; touching worker worktrees; any product file other than the masker, the launcher's masking call site and the docs sentences.

[memory:decision] dotfiles-T98 (orchestrator 2026-10-05): committed `.orchestration` evidence has home paths normalised to `~` by the repository masker, which the boundary procedure runs before every boundary commit and the secret scan enforces.

## Repo / branch

- Work ONLY in your own worktree. `git fetch origin`; `git switch -c chore/evidence-home-path-masking --no-track origin/main`. Verify the dispatched task_rev; else stop and PONG blocked.

## Allowed files

- `scripts/validate-agent-assets.py`, `tests/unit/test_validate_agent_assets.py`, `home/dot_local/bin/common/executable_herdr-agents` (the masking call site only, if a change is needed), `tests/unit/test_herdr_agents.py`, `.orchestration/**` (the mechanical re-mask), `home/dot_agents/skills/agmsg-orchestration/SKILL.md` and `home/dot_config/claude/rules/agmsg-orchestration.md` (one sentence each)
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dotfiles-T98-evidence-home-path-masking-a01.md` (main checkout)

## Validation commands (paste verbatim output)

```
git diff origin/main --stat | tail -3
uv run --no-project --with pyyaml scripts/validate-agent-assets.py; echo "rc=$?"
grep -rl "/home/[a-z]*/" .orchestration | wc -l
uv run --no-project python -m unittest tests.unit.test_validate_agent_assets tests.unit.test_herdr_agents 2>&1 | tail -3
make unit-test 2>&1 | tail -3
gh pr checks <pr-number>
gh api repos/mryfmo/dotfiles/pulls/<pr-number> --jq '.mergeable_state'
```

## Completion

1. PR to `main`, English title/description ending with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. CI green on the final head, branch up to date.
2. After the final push: Bot wait per the SKILL (diff head only, timestamped); fix P0/P1 inline findings; do not resolve threads.
3. Artifacts at the exact expected paths; validation with verbatim outputs, PR number, head SHA.
4. CompactionDB `uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project` with the `[memory:decision]` text (Claude seat) or say the orchestrator records it (Codex seat).
5. `AGMSG-RESULT v1 task_id=dotfiles-T98` via `agmsg-dispatch dotfiles <your identity> claude-remediation-dot wT:p1 "<single line>"`. `cost:` line. max_turns=30.

## Revise round 1 (orchestrator, 2026-10-05 07:22Z) — audit of head aceb1b14: `incorrect` (5 findings; 4 to fix here, 1 dispositioned by the orchestrator)

1. **Scan ignores the running user's `$HOME` (P2, `validate-agent-assets.py:1315`).** Add the running user's multi-segment `$HOME` (any form, for example `/srv/operator`) to the `.orchestration` scan as a machine-dependent backstop in addition to the machine-independent forms (a one-segment `$HOME` keeps the boundary as in the masker). Document in the docstring that this part flags only on the workstation whose home it is, which is where the evidence is written and masked; CI keeps the machine-independent forms. Test with `HOME=/srv/operator` and `/srv/operator/.ssh/id_ed25519`.
2. **macOS root homes restricted to hidden children (P2, `:1298`).** `~` and `~` match any child (`~/Library/Keychains/login.keychain-db` → `~/Library/Keychains/login.keychain-db`); keep the bare-or-`.<dir>` restriction only for plain `~`, whose non-dotted children are Codex sub-agent identifiers in transcripts (the `ponytail:` comment stays, narrowed to `~`). Tests for both forms and for `/proc/1/root~/Library/x`.
3. Re-run the masker over every tracked `.orchestration` file after 1–2; if anything changes, commit the mechanical re-mask separately and paste the masker output verbatim.
4. **Report (P2 evidence-reality, report line 95):** "I fixed every finding" must distinguish the eight fixed Bot findings from thread 4181459798 (accounts named like a top-level `home/` entry), which the orchestrator dispositioned `not-applicable` as a design limit: the exclusion keeps quoted repository paths such as `${REPO_ROOT}/home/dot_config/…` (T75 audit transcript) intact, and no host here has such an account. State it as a limit, not a fix.
5. **Validation (P3 evidence-reality, validation line 5387):** the earlier capture replaced by a narrated count must be restored as verbatim command output (re-run the command if the original output is gone; never summarise).

Then push, `gh pr checks --watch`, Bot wait on the new diff head, `AGMSG-RESULT v1 … round=1`. Same allowed files. Audit finding 2 (`/home/dot_config/.ssh/…` passes) is not in your scope: the orchestrator keeps the design-limit disposition and records it.

### PONG decision 1 (orchestrator, 2026-10-05 07:53Z) — cap the pattern after head 3363ed7a

Accepted, your own proposal from report section 3: the home-path scan is a backstop to the masking step, not a proof. Finish the Bot round on 3363ed7a (its threads are fixed there, as the commit says), run its wait, and then stop widening: a further Bot finding that only names another home-directory form (another mount root, another account-name alphabet, another namespace layout) is **not fixed**; list it in the RESULT as `proposed not-applicable: pattern capped (PONG decision 1), form absent from tracked evidence`, with the grep over `.orchestration` that shows the form absent. Fix a further finding only when it shows a form that is present in the tracked evidence, or a correctness bug (a false rewrite of a non-home path). Keep the two evidence corrections (items 4–5) as instructed. Then `AGMSG-RESULT v1 … round=1`.

## Revise round 2 (orchestrator, 2026-10-05 08:24Z) — audit of head 6ce4e3b3: `incorrect` (3 findings)

1. **Masker/scan asymmetry (P2, `validate-agent-assets.py:1452`).** `mask_secrets` decodes JSON strings only for a `.json` suffix, while the scan decodes every file whose whole text parses as JSON. A non-`.json` evidence file containing `{"path":"\/home\/alice"}` is therefore flagged by the scan and the prescribed `--mask-secrets` command repairs nothing (0 replacements, exit 0). Fix: decide JSON handling in the masker by parse success, exactly as the scan does (`json_strings(text)`), independent of the suffix; keep the pr-feedback layout rewrite for parsed documents (they are JSON whatever the suffix). Test: a `.md` file whose content is that JSON is masked to `~` and then passes the scan; a `.md` with ordinary prose containing a literal `~` path is still masked line-wise. This is also the finding the Codex Bot placed in the body of review 5411302667 (not as an inline thread); disposition it in the report as `fixed:<sha>` and name the review id.
2. **Sandbox record (P3).** `.orchestration/sandboxes/…:13` says "No scratch worktrees", but round 1 created and removed one (`git worktree add --detach`, validation line ~8720). Update the sandbox record to cover the revision rounds (scratch worktree created and removed with `git worktree remove`, no prune).
3. Re-run the masker over tracked `.orchestration` files; if anything changes, commit the mechanical re-mask separately with verbatim output (none expected).

Then push, `gh pr checks --watch`, the Bot wait on the new diff head (if the quota notice "Codex usage limits have been reached" is posted again, record it and end the wait), `AGMSG-RESULT v1 … round=2`. PONG decision 1 (cap the pattern) stands. Same allowed files.

### PONG decision 2 (orchestrator, 2026-10-05 08:44Z) — audit of aa556845: two evidence corrections, no push

The audit of aa556845 found no implementation defect within the accepted limits; two artifact lines need correcting (both files live in the main checkout and are not part of the PR, so the head does not move and no RESULT round follows):

1. `.orchestration/reports/…-a01.md` line ~144 ("unresolved threads block merging"): the orchestrator resolved all 12 threads after your round-2 RESULT; state the final status as `mergeable_state=clean`, all threads resolved by the orchestrator, head aa556845.
2. `.orchestration/learning/…-a01.md` line 4: masking guarantees a passing scan only on the machine whose `$HOME` wrote and masked the evidence; CI keeps the machine-independent forms, so a path glued to a word that only the writing machine's `$HOME` would catch (the auditor's example `F∕home∕runner/.ssh/id` masked under another `$HOME`) can pass locally and fail on a runner whose `$HOME` it is. State that as the documented limitation (your round-1 residual-risk note), not a guarantee.

Edit only those two files, re-run the masker over your five artifacts, and answer with `AGMSG-PONG v1 task_id=dotfiles-T98 status=corrected …` (no new RESULT, no push).
