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

- Work ONLY in `/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-sec`;
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
