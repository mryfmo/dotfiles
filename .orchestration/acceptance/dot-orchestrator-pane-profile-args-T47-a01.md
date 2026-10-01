# Acceptance: dot-orchestrator-pane-profile-args-T47-a01

Dispatched 2026-09-30T04:05:15Z (msg 545, read 04:05:22Z, task_rev
d7a1cd71…) to `claude-standard-dot-a005` at Herdr wN:p2 (pair workspace
created by `herdr-agents` full mode; orchestrator session e7734322 at wN:p1).
RESULT 2026-09-30T22:12:49Z (msg 546): PR #217, head 7103797, one commit on
`origin/main` fa5ce03, branch `fix/orchestrator-pane-profile-args`.

## Why

The orchestrator pane came up on `claude-sonnet-5-5` although every rendered
config said `deep` = `claude-fable-5-1`: the organization default
(`~/.claude.json` `orgModelDefaultCache`, `override_user_selection: true`;
`/model` printed "Your organization's default (Sonnet 5.5) applies on
restart") overrides the `settings.json` model, and `start_claude_in_pane`
started a bare `claude`. The worker path already passed
`MODEL_PROFILE_<PROFILE>_CLAUDE_ARGS`; the observed worker sessions ran on
their `--model` (2ef3e10a 189/189 opus, bd93da57 95/95 opus) while the bare
orchestrator ran 27/27 on sonnet.

## Adversarial review (orchestrator, from git objects and origin refs)

- Diff: 2 files, +74/−9, exactly the allowed files. `start_claude_in_pane`
  resolves `MODEL_PROFILE_INTERACTIVE` and the profile key in two `$( )`
  subshells; `HERDR_AGENTS_CLAUDE_ARGS` is appended after the profile args;
  one `start_agent_in_pane` call with the `${arr[@]+"${arr[@]}"}` idiom; one
  summary line `orchestrator_profile=<p|none> args=<list|none>`.
- Deviation "subshell instead of the worker's global `source`": accepted and
  correct. Full mode starts p1 before `start_worker_agent`; a global `source`
  would overwrite `HERDR_AGENTS_WORKER_PROFILE`/`_KIND` resolved with env
  overrides at startup (pinned by
  `test_worker_profile_env_override_wins_over_generated_worker_profile`). My
  task text was wrong on this point; the worker caught it.
- Second subshell sources the env file without an `-f` guard: reachable only
  when the first subshell read a non-empty `MODEL_PROFILE_INTERACTIVE` from that
  file (it is shadowed to `""` first), so the file exists. OK.
- Missing `MODEL_PROFILE_<P>_CLAUDE_ARGS` → no args, `args=none`, no error;
  mirrors `${!key:-}` in the worker path.
- Both call sites (full :1822→, `--attach` heal :1784→) go through the function;
  no second path. `--restart-worker` never touches p1 (unchanged).
- Tests: `write_deep_interactive_profile`; profile-only and profile+override
  argv pinned in `herdr-calls.txt`, summary line pinned; the existing E2E
  override test unchanged (its HOME has no env file). Ran 612 OK (1 skipped),
  `validate-agent-assets` ok, shellcheck exit 0, all pasted with direct exit
  codes.
- Formatter churn: the worker amended away a 783-line reformat; the pushed
  commit holds only the 43 added test lines (diff stat confirms).
- Header: `@arg HERDR_AGENTS_CLAUDE_ARGS` updated; the new `@description`
  sentence sits at the end of the audit-mode paragraph (lines 22-24) — a
  cosmetic placement, left as is.
- Sandbox record: two sandboxed `validate-agent-assets` attempts failed on
  PyPI access and are described, not pasted; the unsandboxed runs are pasted
  before and after the artifacts. Disclosed, acceptable.
- Effects: none outside the worktree.
- CI: all pass on 7103797 (`gh pr checks` pasted; `gh pr view` CLEAN verified
  by the orchestrator).

## Codex audit (`…-audit-7103797.md`, gpt-6-astra, read-only, high)

**Verdict: correct.** No actionable findings; six isolated behaviour checks
passed; live CI/desktop not independently verified by the auditor (CI verified
by the orchestrator above).

## PR #217 feedback sweep (head 7103797, `…-pr-feedback.json`, 14 items)

11 runner notices, 1 Homebrew tap-trust warning (macOS runner; diff touches
only `executable_herdr-agents` and its test), CodeRabbit skip comment and
status → all `not-applicable`. No review comments.

## Worker-role check (operator question 2026-09-30)

wN:p2 session bd93da57 transcript: 95/95 turns `claude-opus-5-5` (observed).
The worker lane runs on the `standard` profile as configured.

## Live leg — deferred

Full mode cannot run from inside this pair. The fresh-session check (p1 on
`claude-fable-5-1` without a manual `/model`) is recorded at the operator's
next relaunch, T39 leg style. Residual: a bare `claude` outside
`herdr-agents` still gets the organization default.

## CompactionDB

Worker decision `5ff92e5b…` lives in the disposable worker-c DB; consolidated
into the main DB at acceptance with `memory add --kind decision --scope
project` (command run 2026-10-01, this record).

cost: ~136k context tokens (worker session counter; no per-task figure)

**Decision: ACCEPTED.** Merge PR #217 without `--delete-branch` (worker-c holds
the branch) under the acceptance exemption, after
`BASE=origin/main PR_FEEDBACK_EVIDENCE=<json> make require-crit-review`.
