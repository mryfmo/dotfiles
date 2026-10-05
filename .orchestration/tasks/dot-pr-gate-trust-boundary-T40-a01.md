# AGMSG-TASK dot-pr-gate-trust-boundary-T40-a01

revision: 2 (2026-09-30: README and Codex AGENTS.md removed from scope so the task is file-disjoint from the concurrent T44; the doc sentence goes into the PR description for a later doc sync).

Lane: security (Codex worker on the `security` profile, identity
`codex-security-dot`; orchestrator-side acceptance). Origin: three review
findings deferred from T38 (PR #210, merged as d2f19ec); all three are
trust-boundary defects in the PR integration gate.

## Objective

Close the three deferred findings in `scripts/require-crit-review.py` and
`scripts/pr-feedback.py`, each with a unit test that fails before the fix.

1. **(2) P2 BASE is not bound to the PR's base.** `collected_feedback_errors`
   accepts any `--base`; `BASE=HEAD` (or any commit on the PR branch) empties
   the base diff and lets the PR's own collector run. Fix: the collector
   records the PR's GitHub base (`base_ref` name and `base_sha` =
   `baseRefOid`) in the document next to `head_sha`; the guard then requires
   `git rev-parse <base>` to equal the collected `base_sha`, or to be an
   ancestor of it that is not an ancestor of HEAD's first-parent chain (allow
   `origin/main` slightly ahead of the PR's recorded base only when
   `git merge-base <base> HEAD` equals the PR's merge-base with `base_sha`).
   Reject with a clear message otherwise. Keep the bootstrap fallback to
   HEAD's collector ONLY when `git show <base>:scripts/pr-feedback.py` fails
   AND `<base>` is bound as above; a fallback with an unbound base is an
   error.
2. **(3) P3 `is_ignored` excludes any path named by `PR_FEEDBACK_EVIDENCE`.**
   Only a file under `.orchestration/validation/` whose name ends with
   `-pr-feedback.json` may be excluded from diff sizing; anything else named
   by the variable is an error ("evidence must live under
   .orchestration/validation/ and end with -pr-feedback.json"), not a silent
   exclusion.
3. **(4) P3 `gh api -F` coercion.** In `gh_graphql`, pass string variables
   with `-f` (raw) and only genuine integers (PR number, page sizes) with
   `-F`; never let `owner`, `repo`, or a cursor go through `-F` (all-digit
   names become numbers, `@file` values read files). Add a test that an
   all-digit owner and an `@`-prefixed cursor arrive as strings.

Also: update `home/dot_config/claude/rules/pr-integration.md` only where the new
rejection conditions need a sentence. Do NOT edit README.md or
`home/dot_config/codex/AGENTS.md` (owned by the concurrent T44/T43 lane);
put the one-sentence README/mirror wording in the PR description under
"Doc follow-up" instead.

[memory:decision] T40: the PR integration gate binds `--base` to the PR's
recorded GitHub base, excludes from diff sizing only a
`.orchestration/validation/*-pr-feedback.json` evidence file, and passes
GraphQL string variables raw (`-f`), closing the three findings deferred from
T38 (operator 2026-09-29).

## Repo / branch

- Work ONLY in `~/Workspace/dotfiles/.claude/worktrees/worker-sec`;
  ignore the Understand-Anything auto-update hook during this task; branch `fix/pr-gate-trust-boundary` from `origin/main`.
  Verify the dispatched task_rev sha256 against this file; else stop and
  PONG blocked.

## Allowed files

- `scripts/require-crit-review.py`, `scripts/pr-feedback.py`
- `tests/unit/test_require_crit_review.py`, `tests/unit/test_pr_feedback.py`
- `home/dot_config/claude/rules/pr-integration.md`
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dot-pr-gate-trust-boundary-T40-a01.md`

## Forbidden actions

- Editing `README.md` or `home/dot_config/codex/AGENTS.md` (concurrent lane); weakening any existing check (head-match, fixed-range, reason length, multiset coverage, fail-closed base); touching `.github/workflows/**`, `Makefile`, hooks, settings, permgate, `.ua/**`, `.orchestration/tasks/**`; posting PR comments; merging; force push; local bats; `make update`/`upgrade`.

## Validation commands (paste verbatim output)

```
git merge-base --is-ancestor origin/main HEAD && echo base-ok
git diff --stat origin/main
make unit-test
make validate-agent-assets  # if uv cannot write ~/.cache/uv inside a sandbox, prefix UV_CACHE_DIR=$TMPDIR/uv-cache
python3 scripts/pr-feedback.py <pr> --json .orchestration/validation/dot-pr-gate-trust-boundary-T40-a01-pr-feedback.json && python3 -c 'import json;d=json.load(open(".orchestration/validation/dot-pr-gate-trust-boundary-T40-a01-pr-feedback.json"));print(d["head_sha"],d.get("base_ref"),d.get("base_sha"))'
PR_FEEDBACK_EVIDENCE=.orchestration/validation/dot-pr-gate-trust-boundary-T40-a01-pr-feedback.json AGENT_REVIEWED=1 REVIEW_EVIDENCE=<receipt> python3 scripts/require-crit-review.py --base origin/main ; echo "guard exit $?"
PR_FEEDBACK_EVIDENCE=.orchestration/validation/dot-pr-gate-trust-boundary-T40-a01-pr-feedback.json AGENT_REVIEWED=1 REVIEW_EVIDENCE=<receipt> python3 scripts/require-crit-review.py --base HEAD ; echo "guard exit $? (must be non-zero)"
gh pr checks <pr-number>
```

## Completion

1. PR to `main` titled `fix(gate): bind --base to the PR base, scope the evidence exclusion, pass GraphQL strings raw`, English description ending with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. CI green.
2. Artifacts at the exact expected paths with verbatim outputs, PR number and head SHA.
3. CompactionDB from the main checkout: `memory add --kind decision --scope project` with the `[memory:decision]` text above — paste command and output.
4. `AGMSG-RESULT v1` with all artifact paths; `cost:` line in the report.

## Orchestrator amendment r3 (2026-10-02; resume after the Codex pause)

The pause on Codex usage (2026-09-29) is lifted; the seat in
`.claude/worktrees/worker-sec` is re-created with `herdr-agents --add-worker`
(same identity `codex-security-dot-a006`, same worktree). Resume point, as
verified by the orchestrator from the worktree (read-only):

- Branch `fix/pr-gate-trust-boundary`, checked out at f45cf73 with zero
  commits ahead of it; nothing was pushed, no PR exists.
- Uncommitted WIP in exactly the five allowed files (212 insertions, 15
  deletions): `feedback_path_error` (item 2) and `pr_base_errors` (item 1)
  are drafted in `scripts/require-crit-review.py`, with tests started in
  `tests/unit/test_require_crit_review.py` and `tests/unit/test_pr_feedback.py`,
  a four-line change in `scripts/pr-feedback.py`, and one sentence in
  `home/dot_config/claude/rules/pr-integration.md`. Keep this WIP; do not
  reset the worktree.
- `origin/main` has moved past f45cf73 (T43–T49) but
  `git log f45cf73..origin/main -- <the five files>` is empty, so a rebase is
  trivial: `git fetch origin && git rebase origin/main` (name the resulting
  base sha in the report), then continue items 1–3 as specified above.
- Shared `.git` writes (refs, config) from the Codex workspace-write sandbox
  can fail and leave an empty `.git/config.lock` (the r2 failure). If a git
  metadata write is denied, do not escalate: PONG `status=blocked` with the
  exact command, and the orchestrator clears the lock.
  **Ruling after PONG 651 (operator decision 2026-10-02):** the worktree's
  git metadata (`.git/worktrees/worker-sec/*`, `.git/objects`, `.git/refs`)
  lives outside the Codex writable root, so every `git add/commit/rebase/push`
  needs an escalation; the operator answers those prompts in the wQ pane.
  Request the escalation each time (or once per session if offered), never
  self-approve, never retry sandboxed; record each escalation in the sandbox
  file. The structural fix (writable roots for worktree git dirs) is T50.
- The Understand-Anything auto-update hook stays ignored for this task.
- The revision-2 scope stands: `README.md` and `home/dot_config/codex/AGENTS.md`
  remain out of scope; the doc sentence goes into the PR description.

Validation and completion are unchanged; include the verbatim rebase output
and `git log --oneline origin/main..HEAD` in the validation file.
