# Acceptance: dotfiles-T117-upgrade-outside-canonical-clone-a01

- **Decision:** ACCEPTED. PR #308 squash-merged to `main` as `f1e46ea6` (2026-10-09 07:0xZ) with `gh pr merge 308 --squash --match-head-commit bdd01aa98e698c59cac86d3a883030e93689516e`; gate passed at that head in the orchestrator-review worktree with the PR-feedback, audit (`correct`) and crit evidence (`BASE=origin/main AUDIT_EVIDENCE=… AGENT_REVIEWED=1 REVIEW_EVIDENCE=… PR_FEEDBACK_EVIDENCE=… make require-crit-review` rc=0; evidence copies removed). PR #308 `feat/upgrade-outside-canonical-clone`, final head `bdd01aa9` (the `gh pr update-branch` merge of main `15672ea5` over the round-1 diff head `c6cd343f`; branch commits 6000cfb4, b2b7be60, 8e7a1866, c6cd343f). Earlier: blocked PONG 04:56Z (the existing canonical-checkout test needs the override) → Amendment 1; blocked PONG 05:16Z (the Makefile test pinned the removed `agmsg-bootstrap` line) → Amendment 2; RESULT 05:53Z head 8e7a1866; REVISE round 1 (two Bot guard findings accepted, README line 392) → RESULT 06:19Z head c6cd343f; update-branch by the orchestrator → bdd01aa9.
- **Worker:** `claude-standard-dot-a001`, seated for this task with the new launcher's bare `herdr-agents --add-worker` (default worktree worker-c, w4:p7).
- **Exemption declared:** acceptance and final integration; evidence-sync bookkeeping; Bot thread replies and resolution; `--add-worker` / `--remove-worker` (control plane); and, under the operator's directive of 2026-10-09 that repairing the canonical clone is not the operator's job, the one-time repair of `~/.local/share/chezmoi` (restore of the conflicted `mise.lock` from `origin/main`, drop of the single `autostash` entry, pull to `b37937ca`, `make update` rc=0) before this task was dispatched.
- **Origin:** operator directive 2026-10-09 (chat): fix the cause of the canonical clone conflicts, grounded in current official documentation, so the operator never repairs the clone again. Research recorded in the task file: `mise upgrade --bump` edits the config and the lock (mise.jdx.dev/cli/upgrade); the lock's checksum choice is backend-dependent (mise.jdx.dev/dev-tools/mise-lock); git's `rebase.autoStash` is "use with care" (git-scm.com/docs/git-config); `chezmoi update` itself runs `git pull --autostash --rebase` (chezmoi.io/reference/commands/update). Cause: `make upgrade` ran in the canonical clone and dirtied it; the autostash path then conflicted when the carried diff differed.

## What is under acceptance (PR #308, head bdd01aa9)

- `scripts/upgrade-tools.sh` `require_pins_checkout`, first in `main()`: with `chezmoi` installed, exit 2 when its source path cannot be resolved or is not a git checkout, and when that checkout is this one (the canonical clone); without `chezmoi`, skip; then for this repository fetch `origin main` (exit 2 on failure) and exit 2 unless tracked files are clean and `HEAD` equals `origin/main`; `CHEZMOI_ALLOW_UPGRADE_IN_SOURCE=1` skips every check. Each refusal names its fix.
- `Makefile`: `upgrade` no longer runs `agmsg-bootstrap`.
- README lifecycle: `herdr-agents --add-worker .claude/worktrees/pins ~/Workspace/dotfiles`, `make -C ~/Workspace/dotfiles/.claude/worktrees/pins upgrade`, the worker commits the changed files, then `make -C "$(git -C "$(chezmoi source-path)" rev-parse --show-toplevel)" update` on the host; the mise-version delay until the pins PR merges is stated; the agent-setup block no longer tells the operator to run `make upgrade` in the canonical clone; no documented one-liner starts with a bare `git pull`.
- SKILL boundary bullet: the pins worktree procedure with a path-scoped pre-dispatch diff as the acceptance comparison; the T114 extraction and post-merge restore paragraphs are gone. Rule Delegation bullet: the canonical clone is `pull and apply only`. `check-regime-boundary.sh` differs line names the pins worktree.
- Tests: guard cases in `test_runtime_health.py` (canonical refused; override; dirty or behind refused; clean at `origin/main` proceeds; fetch fails; source fails; source not git) on a local bare origin; `test_herdr_agents.py` Makefile test (update includes, upgrade excludes `agmsg-bootstrap`) and the two differs-line strings. CI 13 of 13 on c6cd343f; the full local suite fails the same 193 ids as `origin/main` in the sandbox.
- Accepted deviations: step 4 derives the clone from `chezmoi source-path` (Bot 4226889624); the `upgrade_fixture` fake chezmoi source is `git init`-ed because the new rule refuses a non-git source.
- Supersedes: the T114 decision memory `febb8cb9` (extraction and restore procedure) and the T114 SKILL pins clause; both described a procedure for a dirty canonical clone that can no longer arise.

## Audit / sweep / gate

| scope | verdict |
|---|---|
| task-level, bdd01aa9 (final head) | correct (no findings: eight files within the amended scope, artifacts present, guard behaviour, override, callers, tests and documentation match the amended requirements, evidence matches CI and the six resolved Bot threads, the merge commit adds no code) |

- Sweep (final at bdd01aa9): `.orchestration/validation/dotfiles-T117-upgrade-outside-canonical-clone-a01-pr-feedback.json`; Codex Bot threads 4226831987 and 4226889624 `fixed:8e7a1866`, 4226831998 `fixed:b2b7be60`, 4226889615 and 4226889631 `fixed:c6cd343f`, 4226832007 `not-applicable` (a resume mode that accepts an existing diff is the state the guard forbids; rerun re-derives every pin; discard step documented); all six replied to and resolved by the orchestrator. Crit evidence `…-crit.json` (1 orchestrator review record) / `…-review-receipt.md`; worker-side `…-worker-crit.json` / `…-worker-review-receipt.md` (`review_outcome: addressed`).
- Bot wait: reviews of 6000cfb4 and b2b7be60 (six threads); none on 8e7a1866 or c6cd343f within the wait.

## Parallelism

- Single task; the worker was seated on demand for it and is removed at this acceptance.

## CompactionDB

- Worker records `ac3bdd3e…` and `f02c683a…` (see the report). Orchestrator consolidation `00d73620-9966-4e9c-bb1f-660b08834a8a` (supersedes `febb8cb9`).

cost: n/a
