# Report: dotfiles-T113-codify-T111-lessons-a01

- **PR:** https://github.com/mryfmo/dotfiles/pull/302, branch `feat/codify-t111-lessons` from `origin/main` `7d3a45ee`, final head `f0a6f42b4489c7e02a803dec8e536ba50708ce7e`. Three commits: `2e28c274` (items 1–8), `353b149d` (worker-review fixes plus Amendment 1) and `f0a6f42b` (Codex Bot fixes).
- **Status:** ready_for_review.
- **CI:** all 15 check runs pass on `f0a6f42b` (they carry that head_sha), and on `2e28c274` and `353b149d` too.
- **Bot:** `bot: none` on the final head `f0a6f42b`: the 15-minute wait after green CI found no Bot review or inline comment (30 iterations, all `rc=0`, empty). The Codex Bot did review `2e28c274` and `353b149d` (the earlier wait found the `353b149d` review on its first iteration); its six inline findings are dispositioned below.
- **Unresolved threads:** six Codex Bot inline threads, with the proposed dispositions in "Codex Bot review" below. The worker resolves none.

## Items

1. **Guard:** new `home/.chezmoiscripts/common/run_before_00-refuse-dirty-source.sh.tmpl`. It uses inline bash, shdoc comments, `set -Eeuo pipefail` and the `DOTFILES_DEBUG` block, like the sibling decrypt script. Logic, as specified:
   - The repository is the parent of `{{ .chezmoi.sourceDir }}`.
   - It returns 0 for a non-git source, for `CI=true` and for `CHEZMOI_ALLOW_DIRTY_SOURCE=1`.
   - It applies when `git diff --quiet <ref> -- home install scripts` passes, `git ls-files --unmerged` and untracked files under those trees are both empty (the unmerged check was added in `f0a6f42b`). Otherwise it prints the specified refusal to stderr and exits 1. It never touches the network.
   - **Comparison ref:** `origin/main` whenever it resolves to a commit, else `@{upstream}`, else `HEAD`. The task gives both `upstream=@{upstream} || echo origin/main` and "when `@{upstream}` cannot be resolved, compare against HEAD"; `2e28c274` used `@{upstream}` → `origin/main` → `HEAD` to honour both literally. **Deviation in `f0a6f42b`:** the Codex Bot P1 showed that a pushed but unmerged feature branch equals its own upstream and so passed. Putting `origin/main` first follows the task's stated purpose ("changes reach the host only through a merged pull request") over its literal order; the canonical clone on `main` tracking `origin/main` behaves the same either way.
   - **Message:** when `git status --porcelain` is empty (committed-but-unmerged or stale tree), the parenthetical lists `git diff --name-only <ref>` instead, so it is never empty. After the worker review, the message also says `make update` "(which also pulls a stale tree)".
   - **Makefile:** `@git fetch --quiet origin main || true` is the first line of the `update` recipe (`make -n update` pasted).
   - **Verified:** `chezmoi execute-template` → `bash -n` and `shellcheck` give rc 0. The scratch repository with a bare origin covers 18 cases. The three the task names are there: clean → 0, modified `home/` file → 1, override → 0. The others: `CI=true` → 0; committed-but-unpushed → 1 (the T111 scenario); after push → 0; edit outside the trees → 0; untracked `install/` file → 1; the `origin/main` fallback dirty/clean → 1/0; an upstream whose ref is gone → 0; 20000 untracked files → 1 with the full message; a pushed but unmerged feature branch → 1; a conflicted path restored to `origin/main` content but not staged → 1 (`UU home/dot_a`); non-git → 0; the `HEAD` fallback clean/dirty → 0/1.
2. **README:** one sentence after the pull description in the `make update` section. It deviates from the task's wording in two ways, both kept because the original would be false:
   - The task text says "uncommitted changes". The guard also refuses committed, unpushed, unmerged and not-yet-pulled trees, so the sentence reads "differ from the last-fetched `origin/main`, through uncommitted, unmerged, unpushed or not yet pulled changes".
   - The next sentence's `It then` became `` `make update` then ``, because "It" would otherwise refer to `chezmoi apply`.
3. **Rule:** the Delegation sentence was appended verbatim. The rule is now 449/450 words (`test_agmsg_orchestration_docs` passes).
4. **SKILL, canonical-clone bullet:** the sentence was appended verbatim.
5. **SKILL, step 10:** the `git -C` and HEAD-verification sentences were appended verbatim at the end of the step's first paragraph, which keeps the numbered sub-steps intact.
6. **`scripts/check-regime-boundary.sh`:**
   - The new line is `orchestrator seat is not on main: <branch | detached at <sha>>`. It sits inside the existing seat loop and reuses its identity count, so it fires only when the main checkout holds an identity. The header comment documents it.
   - `validate-agent-assets.py` (`report_regime_boundary`) only prints these lines as `WARN:` and never fails, so CI cannot go red.
   - **Pasted:** the live `--report` from the main checkout, which is on `main`: no such line. A scratch main checkout: on main → none; detached → `detached at 7b57b58`; another branch → `feature`; no identity → no such line.
   - **No new unit test:** `tests/unit/test_herdr_agents.py` is not in `allowed_files`. A test there is a candidate for a follow-up task. The existing boundary tests pass (321 tests in the three affected modules).
7. **`project-map` agent body:** the three lines are verbatim, and `home/dot_claude/agents/project-map.md` was regenerated. The test assertions are unchanged and pass.
8. **SKILL, step 3:** the sentence was appended verbatim.
9. **Amendment 1:** the "Writes" bullet in `home/dot_agents/skills/project-map/SKILL.md`, verbatim, after the memory bullet. Regeneration changed nothing under `home/dot_claude/`.

## User-visible impact (in the PR body)

- `make update` now stops at `chezmoi apply` on a source tree with unmerged edits. The canonical clone currently carries the rejected project-map draft, so its next `make update` stops until the draft is removed or `CHEZMOI_ALLOW_DIRTY_SOURCE=1` is set.
- A clean tree that is behind its fetched upstream is also refused whenever `make update` cannot pull.
- `make update` runs `git fetch --quiet origin main` on every run; a failed fetch prints git's `fatal:` and is ignored.
- The guard covers full applies only. Targeted applies, `--exclude=scripts` and `--keep-going` get past it, which is why `make upgrade`'s targeted mise-pin apply is unaffected.

## Worker review (Worker Playbook step 5; `crit status --json` had no review file)

- **First head:** an independent read-only subagent reviewed `2e28c274`: 1 P2 and 5 P3, `changes-needed`.
- **Fixes in `353b149d`:**
  - the P2 (SIGPIPE under `pipefail` lost the refusal message);
  - the gone-upstream P3;
  - the stale-tree wording P3.
- **PR body only:** the coverage P3 and the fetch P3 are recorded there, as above.
- **Not applicable:** the gitignored-files P3. Reason in the records.
- **Second pass:** the same reviewer re-verified `353b149d` and approved it, with one non-blocking P3 (the stale hint is only true when `make update` can pull; its own Notice names the pull command).
- **Third pass:** it re-verified `f0a6f42b` over the full scenario table and approved it. It agreed that the four Codex Bot findings below are correctly left unfixed, and raised one P3 on the project-map wording for the orchestrator.
- **Evidence:** `.orchestration/validation/dotfiles-T113-codify-T111-lessons-a01-worker-crit.json` and `-worker-review-receipt.md`.

## Codex Bot review (proposed dispositions; the worker resolves no thread)

- **Review bodies:** `5437519326` (on `2e28c274`) and `5437584292` (on `353b149d`) carry no finding; each is the header only.
- **`4202957457` (P1, compare against the merged branch):** `fixed:f0a6f42b4489c7e02a803dec8e536ba50708ce7e`. Scratch case 10c (a pushed feature branch tracking its own upstream) gives rc 1.
- **`4202957461` (P1, the guard breaks `make upgrade`'s targeted apply):** `not-applicable: a targeted chezmoi apply does not run run_ scripts`. An isolated scratch chezmoi v2.73.0 ran the probe `run_before_` script 0 times for `chezmoi apply <file>` and once for a full apply (pasted). So `scripts/upgrade-tools.sh`'s `chezmoi apply ~/.config/mise/config.toml ~/.config/mise/mise.lock` never meets the guard.
- **`4202957466` (P2, unmerged index entries):** `fixed:f0a6f42b4489c7e02a803dec8e536ba50708ce7e`. The `git ls-files --unmerged` check makes scratch case 10d (a conflicted path restored to `origin/main` content) give rc 1.
- **`4203015512` (P1, deleting the guard bypasses it):** `not-applicable: the guard is a guard rail against accidental full applies from a dirty clone, not a boundary against the machine's own operator`. Deleting the tracked template is itself a local edit, which is the act the regime forbids, and it is no stronger a bypass than `CHEZMOI_ALLOW_DIRTY_SOURCE=1`. A second copy of the check in the Makefile would restate the rule (lesson C) and exceeds the task's one-line Makefile allowance.
- **`4203015529` (P2, the project-map body "only" clause excludes the other skill sections):** `not-applicable for the worker: the body is the orchestrator's verbatim item 7`. The preceding sentence, "Follow the preloaded project-map skill exactly", covers Reads, state.json and the map. Reported to the orchestrator for a wording decision.
- **`4203015540` (P2, include gitignored files):** `not-applicable: gitignored __pycache__ under home/dot_codex and scripts/ would refuse every apply` (pasted). `home/.chezmoitemplates/chezmoiignore.d/common` already excludes `**/__pycache__` and `**/*.pyc` from the target state.

## CompactionDB (main checkout, through the permission gate)

```
cd ~/Workspace/dotfiles && uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'dotfiles-T113 (orchestrator 2026-10-07): the canonical chezmoi clone is pull/apply/make-upgrade only and `chezmoi apply` refuses a dirty source tree (`CHEZMOI_ALLOW_DIRTY_SOURCE=1` overrides); checkouts are selected with `git -C`, never `cd`, and the review worktree and main HEADs are verified before audit and gate; a rule is stated once and referenced elsewhere.'
uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind failure --scope project --content 'dotfiles-T111 (orchestrator 2026-10-07): `cd <worktree> && git checkout` in sandboxed Bash ran in the main checkout and detached it at the audited head; a parallel seat at the canonical clone built and applied a second implementation outside the regime.'
```

IDs `d4378b55-e544-453e-828d-0be5f83bf579` (decision) and `40af6916-6e1d-470f-aeac-f407bad83feb` (failure), output in the validation file.

[memory:decision] dotfiles-T113 (orchestrator 2026-10-07): the canonical chezmoi clone is pull/apply/make-upgrade only and `chezmoi apply` refuses a dirty source tree; checkouts are selected with `git -C`; a rule is stated once and referenced elsewhere.
[memory:failure] dotfiles-T113 (worker 2026-10-07): `x="$(cmd | head -n 5)"` under `set -o pipefail` fails with 141 when `cmd` outlives `head`, so a guard's message is lost; append `|| true` to the assignment.

## Other

- Understand-Anything hook: did not fire. Plan Mode not used; no Crit server started.
- T112's branch `chore/pins-2026-10-07` was left untouched.
- cost: n/a
- **Main-checkout validator, for the orchestrator:** `validate-agent-assets.py` in the main checkout exits rc=1. Its only error is still `.orchestration/tasks/dotfiles-T112-pins-2026-10-07-a01.md names a home directory`, the orchestrator's T112 task file, which was already reported in the T112 RESULT. The seven T113 artifacts are masked and raise no error; the run inside worker-c passes (rc=0).
- **Follow-up candidates, not in scope:** a unit test for the new boundary line in `tests/unit/test_herdr_agents.py`, and the project-map body wording (Codex Bot `4203015529`).

## Revise round 1 (final diff head `3f7c2e131a6865487d4b3628f3ea2fadba14c4b3`)

- **Item 1 (Codex Bot `4203015529`, project-map body):** commit `3f7c2e13` sets the body of `render_claude_project_map_agent()` to the task's three lines, verbatim. The agent now follows the skill "exactly and in full; nothing in this body adds to it or narrows it." `home/dot_claude/agents/project-map.md` was regenerated, and the existing assertions hold. Proposed thread disposition: `fixed:3f7c2e131a6865487d4b3628f3ea2fadba14c4b3`.
- **Item 2 (unit test for the boundary line):** two tests in `tests/unit/test_herdr_agents.py` use the file's `boundary_repo()` and `run_boundary_check()` fixtures and a stubbed `identities.sh`:
  - `test_regime_boundary_check_flags_a_seated_main_checkout_off_main`: a seated main checkout on `main` gives no line; detached gives `orchestrator seat is not on main: detached at <sha>`; branch `feature` gives `…: feature`.
  - `test_regime_boundary_check_leaves_an_unseated_detached_checkout_alone`: no identity (a CI checkout) means no line.
  - The positive test fails against the pre-change script (`7d3a45ee`), as pasted. The file was restored from HEAD afterwards and `git diff --stat` shows it clean.
- **Item 3:** pushed. I did not merge `origin/main`; the orchestrator runs `gh pr update-branch 302` (the branch is behind `a5edf2b7`).
- **Validation:**
  - render-check, the validator, the 8 `regime_boundary` tests, the three affected unit modules (323) and `make unit-test` (923, skipped=1) pass. `ruff format --check` passes for all 44 files.
  - `ruff check`, which CI does not run, reports 32 pre-existing findings in the two touched Python files (33 on `origin/main`). None comes from this round.
- **CI:** all 15 check runs pass on `3f7c2e13` and carry that head_sha. Bot: `bot: none` (15-minute wait on `3f7c2e13` after green CI: 30 iterations, all `rc=0`, empty).
- cost: n/a

## Revise round 2 (final diff head `9311c6cb685b46585e2e1c52b40015ab0d0a66ea`)

- **Base:** local `feat/codify-t111-lessons` fast-forwarded to the orchestrator's update-branch merge `d0fa723a` (`git merge --ff-only origin/feat/codify-t111-lessons`) before the edit.
- **Item 1:** the guard header `@description` gains the task's sentence verbatim: "Git-ignored untracked files are out of scope: they never travel by pull request, are the operator's local additions, and chezmoi's own ignore rules govern whether they apply." The refusal message and the predicate are unchanged.
- **Item 2:** the README guard sentence now ends "…only through a merged pull request; git-ignored untracked files are not checked."
- **Item 3:** no predicate change. The audit's ignored-file counterexample is out of the guard's declared scope.
- **Validation:** the rendered template passes `bash -n`, shellcheck and shfmt (rc 0). Prettier, render-check and the validator pass, and so does `test_agmsg_orchestration_docs` (17 tests).
- **CI:** all 16 checks pass on `9311c6cb` (`gh pr checks 302`); every check run carries that head_sha. Bot: `bot: none` (15-minute wait on `9311c6cb` after green CI: 30 iterations, all `rc=0`, empty).
- cost: n/a
