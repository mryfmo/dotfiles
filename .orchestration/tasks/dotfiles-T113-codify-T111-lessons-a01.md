# AGMSG-TASK dotfiles-T113-codify-T111-lessons-a01

Drafted 2026-10-07 by the orchestrator seat (`claude-remediation-dot`, w1A:p1). Codifies the three failures of T111 (acceptance record `.orchestration/acceptance/dotfiles-T111-project-map-subagent-a01.md`, "Notes for the operator") as repository checks and procedure text, per the regime rule that session lessons become rules, SKILL text or checks through a task. Kind: a chezmoi run_before guard, the boundary check script, rule and SKILL prose, a renderer body line; no permission, sandbox or hook block; Claude seat allowed. Dispatched to `claude-standard-dot-a005` (worker-c, w1A:p2) after T112.

## The three failures and their fixes

**A. A second implementation of project-map was built in the canonical clone `~/.local/share/chezmoi` by another seat and applied to the host with a direct `chezmoi apply`, bypassing task, PR and `make update`'s dirty-tree refusal.** Fix: refuse `chezmoi apply` from a dirty source tree, and say in the rule and SKILL that the canonical clone is pull, apply and `make upgrade` only.

1. New `home/.chezmoiscripts/common/run_before_00-refuse-dirty-source.sh.tmpl` (inline bash, shdoc comments like `run_once_before_01-decrypt-private-key.sh.tmpl`, `set -Eeuo pipefail`, the `DOTFILES_DEBUG` block). Logic: resolve the source repository as the parent of `{{ .chezmoi.sourceDir }}`; when `git -C <repo> rev-parse --is-inside-work-tree` fails, return 0 (a tarball or non-git source is not this guard's concern); when `${CI:-false}` is `true` or `${CHEZMOI_ALLOW_DIRTY_SOURCE:-0}` is `1`, return 0; otherwise compare the source tree with its last-fetched upstream, not with HEAD: `upstream="$(git -C <repo> rev-parse --abbrev-ref --symbolic-full-name '@{upstream}' 2>/dev/null || echo origin/main)"`; when `git -C <repo> diff --quiet "$upstream" -- home install scripts` succeeds and `git -C <repo> ls-files --others --exclude-standard -- home install scripts` prints nothing, return 0 (a tree whose content already equals the merged upstream, such as the canonical clone right after its `make upgrade` pins merged, applies without friction); otherwise print to stderr `chezmoi apply refused: the source tree <repo> differs from <upstream> (<first 5 lines of git status --porcelain -- home install scripts>); land the change through a pull request and run make update, or set CHEZMOI_ALLOW_DIRTY_SOURCE=1 to apply anyway` and exit 1. No network access in the guard; it reads the upstream ref as last fetched. When `@{upstream}` cannot be resolved, compare against HEAD (`git status --porcelain -- home install scripts` must be empty). Because `make update` skips its `git pull` when tracked files are dirty (Makefile:55), the upstream ref would be stale in exactly the post-merge case, so add one line at the top of the `update` recipe in `Makefile`: `@git fetch --quiet origin main || true` (before the branch/upstream checks), so the guard compares against a fresh `origin/main`. User-visible impact to state in the PR body and README sentence: `make update` on a source tree that carries unmerged edits now stops at `chezmoi apply` instead of applying them (today it only skips the pull with a Notice and applies anyway, which is how the T111 draft reached the host). Verify by rendering with `chezmoi execute-template < <file>` and running the rendered script through `bash -n` and `shellcheck -`; verify the behaviour in a scratch git repository (clean → rc 0, one modified file under home/ → rc 1, same with the override → rc 0) and paste it. CI's bootstrap jobs apply from fresh clones (clean) and the `CI=true` skip keeps them unaffected; confirm with green CI.
2. `README.md`: one sentence next to the `make update` documentation: `chezmoi apply` refuses a source tree with uncommitted changes under `home/`, `install/` or `scripts/` (override `CHEZMOI_ALLOW_DIRTY_SOURCE=1`), so changes reach the host only through a merged pull request.
3. `home/dot_config/claude/rules/agmsg-orchestration.md`, Delegation bullet: append the sentence `The canonical chezmoi clone is pull, apply and make upgrade only: no seat edits it, and nothing is applied from a dirty source tree.`
4. `home/dot_agents/skills/agmsg-orchestration/SKILL.md`, "Review and integration invariants", the bullet that names the operator's `make upgrade` in the canonical clone: append `The canonical clone is otherwise untouched by any seat: no edits, no apply from a dirty tree (the run_before guard refuses it), and one orchestrator identity per repository, seated at the working clone.`

**B. The orchestrator's `cd <worktree> && git checkout` ran in the main checkout (the worktree reflog has no entry at 09:55:05; the main checkout's has `moving from main to 2e15d4aa`), and the audit wrapper then refused its masking step.** Fix: procedure text plus a boundary violation.

5. SKILL Orchestrator Playbook step 10, after its first paragraph, add: `Select a checkout with git -C <absolute path>, never with cd, which the sandboxed Bash may not honour. After moving the review worktree to the audited head, verify git -C <review> rev-parse HEAD equals that head and git -C <main> symbolic-ref --short HEAD prints main before the audit and the gate.`
6. `scripts/check-regime-boundary.sh`: a violation `orchestrator seat is not on main: <HEAD description>` when `git -C "${main}" symbolic-ref -q --short HEAD` does not print `main`, emitted only when `${main}` is a registered orchestrator seat (an agmsg identity resolves there through the existing `identities.sh` lookup, lines 60–90), so a CI `actions/checkout` detached HEAD with no seat is never flagged. Document it in the header comment. Before coding, check how `scripts/validate-agent-assets.py` surfaces `check-regime-boundary` output (`WARN:` lines) and whether the `validate` CI job treats them as fatal; the new line must not turn CI red. Paste `bash scripts/check-regime-boundary.sh --report` from the main checkout (on `main`), from a scratch detached checkout without a seat (no violation), and the seat-detached case reproduced in a scratch repo if feasible.

**C. The write boundary was stated twice (skill and rendered agent body); a requirement added to one copy contradicted the other and cost two revise rounds.** Fix: single source, plus a pre-dispatch check.

7. `scripts/generate-agent-configs.py`, `render_claude_project_map_agent()`: the body becomes exactly
   ```
   You draw the project map and nothing else. Follow the preloaded
   project-map skill exactly; its style, write and report rules are the
   only ones you apply.
   ```
   Regenerate `home/dot_claude/agents/project-map.md`; the existing test assertions (model, effort, `  - project-map\n`) still hold.
8. SKILL Orchestrator Playbook step 3: append `Before dispatch, read the task's verbatim blocks against each other for contradictions, and state each rule once; a second artifact references the first instead of restating it.`

Forbidden: anything else; `make update`; `make upgrade`; touching `~/.local/share/chezmoi`; thread resolution; hand edits to generated files.

[memory:decision] dotfiles-T113 (orchestrator 2026-10-07): the canonical chezmoi clone is pull/apply/make-upgrade only and `chezmoi apply` refuses a dirty source tree (`CHEZMOI_ALLOW_DIRTY_SOURCE=1` overrides); checkouts are selected with `git -C`, never `cd`, and the review worktree and main HEADs are verified before audit and gate; a rule is stated once and referenced elsewhere.
[memory:failure] dotfiles-T111 (orchestrator 2026-10-07): `cd <worktree> && git checkout` in sandboxed Bash ran in the main checkout and detached it at the audited head; a parallel seat at the canonical clone built and applied a second implementation outside the regime.

## Repo / branch

worker-c; `git fetch origin`; `git switch -c feat/codify-t111-lessons --no-track origin/main`. T112 (PR #301, branch `chore/pins-2026-10-07`) is in acceptance and its files are disjoint from this task's; leave that branch untouched for its revise rounds, and when #301 merges before this PR, the orchestrator runs `gh pr update-branch` on this PR.

## Allowed files

`home/.chezmoiscripts/common/run_before_00-refuse-dirty-source.sh.tmpl` (new), `Makefile` (one fetch line in the `update` recipe), `README.md` (one sentence), `home/dot_config/claude/rules/agmsg-orchestration.md`, `home/dot_agents/skills/agmsg-orchestration/SKILL.md`, `scripts/check-regime-boundary.sh`, `scripts/generate-agent-configs.py`, `home/dot_claude/agents/project-map.md` (generator output), `tests/unit/test_generate_agent_configs.py` (only if an assertion must change). Artifacts at the standard seven `dotfiles-T113-codify-T111-lessons-a01` paths in the main checkout (Claude seat, through the permission gate), masked.

## Validation commands (paste verbatim output, whole)

```
chezmoi execute-template < home/.chezmoiscripts/common/run_before_00-refuse-dirty-source.sh.tmpl > "$TMPDIR/guard.sh"; bash -n "$TMPDIR/guard.sh"; echo "rc=$?"; shellcheck "$TMPDIR/guard.sh"; echo "rc=$?"
<scratch-repo behaviour check: clean rc, dirty rc, override rc>
bash scripts/check-regime-boundary.sh --report; echo "rc=$?"
shellcheck scripts/check-regime-boundary.sh; echo "rc=$?"
uv run --no-project --with pyyaml scripts/generate-agent-configs.py; echo "rc=$?"
make render-check; echo "rc=$?"
uv run --no-project --with pyyaml scripts/validate-agent-assets.py; echo "rc=$?"
make unit-test 2>&1 | tail -3
git ls-files -z "*.py" | xargs -0 mise x ruff -- ruff format --config ruff.toml --check; echo "rc=$?"
mise x node npm:prettier -- prettier --check README.md home/dot_config/claude/rules/agmsg-orchestration.md home/dot_agents/skills/agmsg-orchestration/SKILL.md 2>&1 | tail -2
gh pr checks <pr>
```

## Completion

PR to `main` (English title and body, attribution footer), CI green, Bot wait per the SKILL, artifacts, the CompactionDB `memory add` of the decision and failure lines, then `AGMSG-RESULT v1 task_id=dotfiles-T113` via `agmsg-dispatch dotfiles claude-standard-dot-a005 claude-remediation-dot w1A:p1 "<single line>"`. max_turns=14.

## Amendment 1 (orchestrator, 2026-10-07 04:10Z) — one more item, before your RESULT

9. `home/dot_agents/skills/project-map/SKILL.md`, "Writes" section, add a bullet after the memory bullet: `- Never launch a browser, take a screenshot, or start any process that writes elsewhere; verify the HTML by reading it.` Reason: the first live run (04:0xZ, this repository) rendered correctly but took a headless Chromium screenshot outside the sandbox, which wrote under `~/snap/chromium/common/`; the write list did not forbid it. The file is added to the allowed files. The generated `home/dot_claude/skills/project-map/symlink_SKILL.md.tmpl` does not change.

## Revise round 1 (orchestrator, 2026-10-07 05:05Z) — review of f0a6f42b: one wording fix, one test, then the base update

Accepted as delivered: the `origin/main`-first comparison (the task's purpose over its literal order), the README wording that names committed, unpushed, unmerged and not-yet-pulled trees, the unmerged-index check, and the proposed dispositions of Codex Bot threads 4202957457 (fixed), 4202957466 (fixed), 4202957461, 4203015512 and 4203015540 (not applicable, with the pasted probes). The orchestrator replies to and resolves those five threads.

1. **Project-map agent body (Codex Bot 4203015529, P2; the orchestrator's own wording).** In `render_claude_project_map_agent()` the body becomes exactly
   ```
   You draw the project map and nothing else. Follow the preloaded
   project-map skill exactly and in full; nothing in this body adds to
   it or narrows it.
   ```
   Regenerate `home/dot_claude/agents/project-map.md`; the existing test assertions still hold.
2. **Unit test for the new boundary line.** `tests/unit/test_herdr_agents.py` is added to the allowed files. Add the case the report calls a follow-up: a scratch main checkout that holds an identity and is detached (or on another branch) yields `orchestrator seat is not on main: …`, and the same checkout on `main` yields no such line. Follow the file's existing fixtures for `check-regime-boundary.sh`.
3. Push; then tell the orchestrator with the RESULT and it runs `gh pr update-branch 302` (the branch is behind `a5edf2b7`). Do not merge `origin/main` yourself. After the update-branch the orchestrator waits for CI itself; your Bot wait is on your own final diff head.

Then rerun the validation commands, push, CI, Bot wait on the final diff head, `AGMSG-RESULT v1 … round=1`. No `make update`.

## Revise round 2 (orchestrator, 2026-10-07 06:00Z) — audit of d0fa723a: `incorrect` (1 P2: the stated guarantee is wider than the predicate)

The auditor's counterexample stands: a git-ignored untracked file under `home/` (for example one matching `coverage*`) passes `--exclude-standard` and chezmoi applies it, while the README and the thread disposition claim that changes reach the host only through a merged pull request. The predicate stays as the task prescribed (ignored files are the operator's local additions, never travel by pull request, and including them would refuse every apply because of `__pycache__`); the claim is narrowed to what the predicate guarantees.

1. `home/.chezmoiscripts/common/run_before_00-refuse-dirty-source.sh.tmpl`: extend the header `@description` (or the function's `@description`) with one sentence: `Git-ignored untracked files are out of scope: they never travel by pull request, are the operator's local additions, and chezmoi's own ignore rules govern whether they apply.` Append to the refusal message's last clause nothing; the message is unchanged.
2. `README.md`: the guard sentence ends with `; git-ignored untracked files are not checked.` (so the sentence no longer claims that only merged changes reach the host).
3. No predicate change. **Boundary:** with the claim narrowed to tracked trees plus non-ignored untracked files, the finding is dispositioned as `not-applicable: out of the guard's declared scope`; no further widening of the predicate is requested in this task. A chezmoi-aware check (`chezmoi managed` against ignored untracked files) is a separate task if ever wanted.

Then rerun the validation commands (template render → `bash -n`, `shellcheck`; prettier on README), push, CI, Bot wait on the final diff head, `AGMSG-RESULT v1 … round=2`. `main` has not moved since the update-branch, so no new update-branch is expected. No `make update`.
