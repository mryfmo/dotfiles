# T33a report — dot-orchestration-rules-T33a-a01 (revision 3)

- worker: `claude-standard-dot-a005` (Claude Code, acting as worker per the dispatch note)
- orchestrator: `claude-remediation-dot`
- worktree: `~/Workspace/dotfiles/.claude/worktrees/worker-c` (clean before the switch)
- branch: `docs/orchestration-rules-T33a` from `origin/main` = `ca4af19`
- task_rev:
  - rev1 sha256 `62a1f9946980743f30032b3c3a204a937bf6a960e6a89d9ffb10e66e861b5d47` at `ca4af19`
  - rev2 sha256 `4ba24d2273a0755556f2f9c745917418f213ee2aef6d5d4fec4b218517d4d844` at `245d014`
  - both checked against `origin/main` (the hashes match)
- PR: https://github.com/mryfmo/dotfiles/pull/196
  - commits: `9a1cde2` (items 1, 2, 3, 5 and the SKILL/Claude crit wording), `8798076` (rev2: Codex AGENTS.md crit alignment)
  - head: `489c83be0e1f6cd2344acd9e6b6191f2c26b3f8d` (rev3 commit `489c83b`; rev2 head was `8798076`)
- status: ready_for_review (revision 3). CI is green on head 489c83b: all checks pass except nix, which was skipped. Verbatim `gh pr checks 196` output is in the validation file.

## Revision 3 (AGMSG-TASK revision=3, 2026-09-28T04:12:14Z)

- task_rev: rev3 sha256 `edf2b017b9f0348e7f6ed3a8069525f265177bacdc9c7233e201442d363da1be`,
  checked at `origin/main` `b1cd389`.
- Trigger: the pre-merge Codex audit of `8798076` reported a P2
  (`.orchestration/validation/dot-orchestration-rules-T33a-a01-audit.md`).
  The "Crit data unavailable → agent-side substitute evidence" fallback
  named no evidence format that `make require-crit-review` accepts.
- Item 6 is in commit `489c83b` on the same branch and PR #196. The guard is
  unchanged.

Before writing the format, I read the guard's actual rules (read-only):
- `crit_data_errors`: a non-empty list of objects; `CRIT_DATA_REQUIRED_FIELDS = ("id", "body", "scope")` must be non-empty strings; `resolved is True`; at least one `scope == "review"`, or a `line`/`file` scope with a non-empty `path`.
- `agent_review_errors`: requires `AGENT_REVIEWED=1`, `review_surface: crit-data`, `review_outcome` in {`approved`, `addressed`}, and `review_source`.
- `AGENT_REVIEWERS = {claude, claude-code, codex}`.

I then called those functions on hand-written evidence under a scratch root
(verbatim in the validation file). The results matched the format:
- A review-scope record and a path-bound line record both pass (`[]`).
- A line record without `path` is rejected, and so is an unresolved record.
- `claude-code`, `codex` and `claude` all pass as reviewers.

Added sentences:

- `AGENTS.md` "Agent Review Evidence" (new bullet, the task's text verbatim):
  > When the crit CLI or its data is unavailable, save the independent agent review in that same JSON shape (hand-written records are acceptable), mark each record `resolved: true` after addressing it, and reference it from the receipt exactly as crit-exported evidence; the guard validates shape, not provenance.
- `home/dot_config/claude/rules/crit-review.md` (appended to the `/crit`
  bullet, right after the fallback it prescribes):
  > Save that fallback evidence as a repo-local JSON list of objects, each with non-empty string `id`, `body`, and `scope` and `resolved: true`, including at least one `scope: "review"` record (or a `line`/`file` record with a non-empty `path`), and reference it from a receipt with `review_surface: crit-data`, `reviewer: claude-code` (or `claude`/`codex`), `review_source: <that JSON>`, and `review_outcome: approved` or `addressed`; hand-written records are acceptable because the guard validates shape, not provenance.
- SKILL crit bullet (appended after "never open a browser review to ask the user."):
  > When Crit data is unavailable, save the independent agent review as the same repo-local JSON list (objects with non-empty string `id`, `body`, `scope` and `resolved: true`, at least one `scope: "review"` or path-bound `line`/`file` record; hand-written records are acceptable because the guard validates shape, not provenance) and reference it from a `review_surface: crit-data` receipt with `reviewer: claude-code`, `claude`, or `codex`, `review_source: <that JSON>`, and `review_outcome: approved` or `addressed`.
- `home/dot_config/codex/AGENTS.md` (Japanese, appended to the first
  "Crit レビュー運用" bullet right after its fallback):
  > その代替証跡は、空でない文字列の `id`・`body`・`scope` と `resolved: true` を持つオブジェクトの repo 内 JSON リスト(`scope: "review"` の record、または空でない `path` を持つ `line`/`file` の record を 1 件以上含む。guard は形式だけを検証し出所は問わないため手書きの record でも可)として保存し、receipt に `review_surface: crit-data`、`reviewer: codex`、`review_source: <その JSON>`、`review_outcome: approved` または `addressed` を記載してください。

Deviation: the task gives "`reviewer: <agent>`" and "path-bound". I wrote
the concrete accepted set (`claude-code`/`claude`/`codex`) and "non-empty
`path`", because those are what the guard actually checks.

The permgate bench flake happened again. The first full `make unit-test`
after the rev3 edit failed `test_bench_runs_five_layer_two_fixtures` (0 of
5), and the rerun passed with 490 OK; both runs are in the validation file.
This is the second time it failed on the first full run after an edit.
permgate reads none of the changed files (grep over
`executable_permgate`). Its bench calls fake provider CLIs under a per-call
`timeout_seconds` of at most 8 s, so a cold-start run can time out every
call. That makes it a timing flake, not a regression, and a candidate for a
test-hardening task.

## Process (revisions 1–2)

1. Rev1 item 4 said to look for the Codex crit mirror under
   `home/dot_agents` or `home/dot_codex`. The real mirror is
   `home/dot_config/codex/AGENTS.md`: the validator's line 804 treats it as
   the canonical Codex crit document, and lifecycle.bats greps it. That path
   was outside rev1's allowed paths, and the file contradicted the Claude rule.
   I sent `AGMSG-PONG v1 status=blocked` for item 4's scope only
   (2026-09-28T03:21:38Z, per agmsg history), then continued with items 1, 2, 3, 5 and the SKILL
   crit clause (commit `9a1cde2`, PR #196), following the fail-closed
   convention this task codifies.
2. Rev2 (03:40:45Z) approved option A. I found the revision only through an
   inbox check after the push. By then `origin/main` already contained it, and
   I verified the new task_rev. I applied the Codex alignment on the same
   branch (commit `8798076`), with no rebase.

## Changed text (quoted)

### `home/dot_agents/skills/agmsg-orchestration/SKILL.md`

- Item 5 (Regime activation and progress; the bullet was changed in place).
  Old:
  > never read worker panes or screens, infer completion from pane/agent status, or use ad-hoc polling sleep loops.

  New:
  > never read worker panes or screens (including read-only probes such as `pane read`/`pane wait-output` against another agent's pane, even to learn output shapes; use `--help` and fake CLIs), infer completion from pane/agent status, or use ad-hoc polling sleep loops.
- Item 1 (Identity, delivery, and storage; new bullet):
  > Interim worker inbox discipline: a worker acting under a worktree-registered identity from a main-path pane receives no turn delivery for that identity, because no watcher or Stop hook runs on the worktree path. It runs `~/.agents/skills/agmsg/scripts/inbox.sh <team> <identity>` at each milestone (task start, push, CI green, before RESULT, after any PONG), and the orchestrator treats revision and PING dispatches as picked up at the worker's next inbox check, not as turn notices. This rule retires once the worker pane is launched inside its own worktree with its identity and delivery hooks registered there.
- Item 2 (Worker Playbook step 4; appended to the existing sentence):
  > Complete every command inside the sandbox and allowlist; never escalate an action outside that boundary for approval. Fail it instead, send `AGMSG-PONG v1 status=blocked` with the exact command and the boundary it crosses, and wait for the orchestrator to re-task. Agent-to-agent permission approval is forbidden: only the human operator answers a permission prompt.
- Item 3 (Review and integration invariants; new bullet):
  > When several RESULTs are pending at once, the auditor may pre-screen each changeset (`codex --profile audit review --commit <sha>`, in the visible audit lane when available) before the orchestrator's sequential adversarial review. Pre-screening never moves acceptance authority, and each RESULT still receives its own acceptance record.
- Item 4 (Review and integration invariants; new bullet):
  > Crit is agent-side only for Claude Code and Codex alike, as in `home/dot_config/claude/rules/crit-review.md`: record crit-data evidence (`crit status --json`, `crit comments --all --json <review.json>`) and never open a browser review to ask the user. Run `crit share` or any other publish step only when the user explicitly asks for it. Close a Crit session opened by the Plan Mode hook once its review is done, so no local Crit web server stays resident.

### `home/dot_config/claude/rules/agmsg-orchestration.md` (three new bullets)

- Item 3:
  > When several RESULTs are pending, the auditor may pre-screen each changeset before the orchestrator's sequential adversarial review; acceptance authority never moves, and each RESULT still gets its own acceptance record.
- Item 2:
  > Worker commands complete inside the sandbox and allowlist. An action outside that boundary is never escalated for approval: the worker fails it, sends `AGMSG-PONG v1 status=blocked` with the exact command and boundary, and the orchestrator re-tasks. Agent-to-agent permission approval is forbidden; only the human operator answers a permission prompt.
- Item 1:
  > Interim, until worker panes launch inside their own worktree: a worker acting under a worktree-registered identity from a main-path pane gets no turn delivery for it, so it runs `~/.agents/skills/agmsg/scripts/inbox.sh <team> <identity>` at each milestone (task start, push, CI green, before RESULT, after any PONG), and the orchestrator expects revision/PING pickup at that next check.

### `home/dot_config/claude/rules/crit-review.md` (one new bullet, shared verbatim with the SKILL)

> Run `crit share` or any other publish step only when the user explicitly asks for it. Close a Crit session opened by the Plan Mode hook once its review is done, so no local Crit web server stays resident.

I added it because the Claude rule had no share/close wording, so it could not be "identical" to the required Codex text without it. The task allows this edit "only if wording must be shared verbatim".

### `home/dot_config/codex/AGENTS.md` (rev2, crit passages only, Japanese kept)

- (a) First bullet of "Crit レビュー運用". Old:
  > ユーザが Crit web UI を明示した場合、または Crit data を取得できない場合のみ `$crit` / `crit` をブラウザ review として使ってください。

  New:
  > ユーザが Crit web UI を明示した場合のみ `$crit` / `crit` をブラウザ review として使ってください。Crit data を取得できない場合は、ブラウザ review を開かず agent-side のレビュー証跡(独立した subagent レビューと保存済みの記録)で代替し、ユーザにレビューを依頼しないでください。
- (a) The `crit --no-open` bullet. Old:
  > ユーザが明示的に Crit web UI を求めた場合、または Crit data を取得できない場合だけ `crit --no-open` または `crit` を使ってください。

  New (the rest of the bullet, the receipt flow, is unchanged):
  > ユーザが明示的に Crit web UI を求めた場合だけ `crit --no-open` または `crit` を使ってください。
- (b) The agent-only bullet, moved. Old:
  > Crit は自分(エージェント)自身のレビューにのみ使う: `crit comment` / `crit share` 等の CLI でコメントを起票・返信・解決し、JSON 証跡を `.orchestration/` または `.agents/worklog/` に保存する。

  New:
  > Crit は自分(エージェント)自身のレビューにのみ使う: `crit comment` 等の CLI でコメントを起票・返信・解決し、JSON 証跡を `.orchestration/` または `.agents/worklog/` に保存する。`crit share` などの publish は、ユーザが明示的に求めた場合だけ実行する。
- (c) New bullet:
  > Plan Mode hook が開いた Crit セッションは、レビューが終わったら閉じてください(ローカルの Crit web server を常駐させない)。
- (d) Structure. The two crit bullets misplaced under `## CompactionDB` were
  moved into `## Crit レビュー運用`. The "browser review prohibited" bullet
  is moved byte-identical. The empty `## Crit レビューの利用方針` heading
  and the stray blank line are deleted.
- All non-crit sentences are byte-identical.
- The validator-pinned tokens (`$crit`, `Crit plugin`, `CRIT_PLAN_REVIEW=off`,
  `TUI`, `http://localhost`) and the lifecycle.bats grep tokens are still
  present; the grep output is pasted in the validation file.

## Notes for acceptance

- The mandated `[memory:decision]` text says "Codex crit guidance aligned to
  the Claude no-web-UI rule". After rev2 that is accurate: `8798076` aligns
  `home/dot_config/codex/AGENTS.md`. I recorded the text verbatim before
  rev2 landed.
- **Flaky test.** The first `make unit-test` after the Codex edit failed one
  test, `test_permgate.PermgateTest.test_bench_runs_five_layer_two_fixtures`
  (`successful_classifications 0 != 5`). That test exercises the permgate
  bench with fake CLIs and does not read any file this task touches. It
  passed alone right away and in a full rerun (490 OK). All three outputs are
  pasted verbatim. It looks timing-sensitive; I did not investigate further,
  since test changes are forbidden here.
- The understand-anything post-commit auto-update was not executed. It is
  outside `allowed_files`, and graph rebuilds are orchestrator-tasked; T33c
  covers `.ua` refresh.

## CompactionDB

[memory:decision] T33a: interim worker inbox discipline (inbox.sh at each milestone for
worktree-registered identities from a main-path pane), fail-closed task convention with
PONG blocked instead of approval requests, auditor pre-screening for batched RESULTs with
orchestrator-only acceptance, Codex crit guidance aligned to the Claude no-web-UI rule,
and an explicit ban on read-only pane probes are codified in the agmsg-orchestration rule
and SKILL (operator 2026-09-28).

The command was run from the main checkout with the content passed through a
shell variable; the output is pasted in the validation file, id
`29569eaf-79a9-4d22-9fd4-7ae23029b6c7`.

## Effects

None outside the repository. The only writes outside the worktree were the
`.orchestration` artifacts and the local CompactionDB ledger.

cost: n/a (the Claude Code runtime does not expose session token/cost figures to the worker)
