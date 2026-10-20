---
{
  "audit_findings": [],
  "dispatch": [
    "AGMSG-TASK v1 task_id=dotfiles-T129-anthropic-auth-route-check-followup-a02 round=1 repo=~/Workspace/dotfiles/.claude/worktrees/worker-e task_file=.orchestration/tasks/dotfiles-T129-anthropic-auth-route-check-followup-a02.md task_sha256=0183182a4c8d67e3c0eebcdb0df937b8eb800a0ebe667c237133faa2e07e1021 deadline=none done_signal=AGMSG-RESULT note=a010:the-INV-6-reset-of-anthropic-auth-route-check-followup-a01(redesigned-by-the-codex-review-context,reset_of-a01):PR-412-and-branch-tools/anthropic-auth-route-structured-continue-under-this-task;after-your-worker-cap-hookspath-a02-push;replace-the-a01-task.md-copy-with-this-text-s-copy,fold-in-your-amendment-3-WIP,the-case-pattern-name-refusal,the-real-entry-test-and-the-template-rendering,one-push-as-single-commands,no-@codex-review,no-gh-pr-edit,then-RESULT-with-pr=412-and-task_copy;read-the-task-file-first read_at=read",
    "AGMSG-ACCEPTANCE v1 task_id=dotfiles-T129-anthropic-auth-route-check-followup-a02 status=pending-integration reason=RESULT-received-and-reviewed;the-chain-and-the-audit-are-queued-behind-408,410,413,411 next_action=no-worker-action;the-orchestrator-runs-the-chain-in-turn read_at=read"
  ],
  "format": 1,
  "head": null,
  "ledger": [],
  "pr": null,
  "replans": {
    "shell-quoting-bypass": {
      "design": "one scanner function with one decoder, used by the three call sites (the export and assignment check, the Markdown examples, the whole-value allowlist)",
      "implementation": "the a03 redesign (review profile) keeps the two a9056299 fixes and fixes the four findings of a64daf1 on top; seat a010, before its stacked P1-14 a03",
      "specification": "the credential check never reasons about shell text with regexes over raw lines: one word scanner tokenises shell text under every bash quoting form (single, double, backslash, ANSI-C $'\u2026', locale $\"\u2026\"), decodes escaped names before comparing them with the two credential variable names, treats an assignment word as the whole word up to an unquoted blank or operator (LF alone ends a line), rejects statically undecodable name forms as unsupported, parses each Markdown fenced example with a fresh quote state, and never prints an assignment's payload in a diagnostic",
      "verification": "one red-then-green test per finding of both local reviews plus a table-driven bypass corpus with the honest forms"
    }
  },
  "searches": [],
  "task": "dotfiles-T129-anthropic-auth-route-check-followup-a02"
}
---

# Acceptance record: dotfiles-T129-anthropic-auth-route-check-followup-a02

The INV-6 reset of dotfiles-T129-anthropic-auth-route-check-followup-a01 (plan 023 PR D, the parser version of the Anthropic credential check): redesigned by a headless Codex review-profile context at 07:12Z from the a01 text and its three amendments, the record, the a010 handoff evidence and the PR #412 diff; PR #412 (branch tools/anthropic-auth-route-structured against main) continues under this task with fresh INV-6 counts; PR #396 stays open as the stacked record; PR #389 is superseded. Seat: a010 (worker-e, Codex), after dotfiles-T133-worker-cap-hookspath-a02.

- 2026-10-18T07:17Z record created before the first dispatch (Orchestrator Playbook step 6).

## RESULT round 1 (2026-10-18T08:43:08Z): PR #412 head d3480fc0 on main (the a02 reset of the parser version; PR #396 is the stacked record, PR #389 superseded)

- review (08:5xZ): the two first-review P1 of #412 (4305965376 escaped shell names, 4305965379 the real-entry registration test) and the P2 4305863865 (strict UTF-8) fixed; the template-classification validate failure fixed by rendering chezmoi templates for both platforms before parsing; the surviving case-pattern bypass closed; 108 tests, 109 on merged main, make validate-agent-assets exit 0 against main s template; CI 13/13 on d3480fc0; no Bot review of the final head within the window (no @codex review); caps 300/300 and 401/1000; evidence copied from worker-e. The chain (sweep, local review, audit) runs on d3480fc0 after #408, #410, #413 and #411.
4305965376	escaped-name-bypass
4305965379	test-calls-helper-only
4305863865	malformed-utf8-parses

## Owned by dotfiles-T129-anthropic-auth-route-check-followup-a03 (advisory P2 of the final head; plan 020 step 1.2; rows id<TAB>class)

local:b139995:2	advisory-p2
local-finding: b139995:2 not-applicable:advisory P2 owned by dotfiles-T129-anthropic-auth-route-check-followup-a03 (- [P2] Recognize shell word boundaries after allowed references — scripts/validate-agent-assets.py:1612-1614); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T129-anthropic-auth-route-check-followup-a03.md (7d2d12335df793c53fdfbf0097cf4067e6f75b35648c87950d31392921815b27)

## Local review of b1399953 (2026-10-18T13:0xZ) and revise 1

- The chain (started 11:2xZ after the #413 merge; owner task `dotfiles-T129-anthropic-auth-route-check-followup-a03` written first) update-branched PR #412 (head d3480fc0 → b1399953c5cb7a9a3e200480e144fe37cd1f2b39, code head unchanged), waited for the required checks (all 13 pass at 12:53Z), ran the local review (`codex review --base main`, profile review): 1 P1 and 1 P2 in `scripts/validate-agent-assets.py`, `.orchestration/validation/dotfiles-T129-anthropic-auth-route-check-followup-a02-local-review-b139995.md`: (1) P1 lines 1781-1785: a backslash inside single quotes is treated as an escape and skips the closing quote, so `NAME=ANTHROPIC_API_KEY; printf '%s' '\'; export "$NAME"=literal-value` passes while Bash assigns the literal key; (2) P2 lines 1612-1614: the end-of-line requirement reports `ANTHROPIC_API_KEY=$DEPLOYED_KEY client` and `export ANTHROPIC_<redacted:secret-pattern>; exec client` as literal credentials. The chain stopped at "a P0/P1 local finding: the one round or the operator"; the two rows it recorded under the owner section are superseded by revise 1 (fixed in this task, not advisory).
- counters before the send (`scripts/regime-counters.sh dotfiles-T129-anthropic-auth-route-check-followup-a02 --history-only`, 13:0xZ): `tasks=1 amendments=0 questions=0 results=1 withdrawn=0 revises=0` (no S2 line; this is the one fix round of a02).
- 13:0xZ: `status=revise previous_head=b1399953…` sent to a010 (wJ:p5), to run before it continues P1-14 a03 (whose branch is stacked on this PR's head and rebases onto the new head afterwards); `check=` names the two tests; push once, CI, RESULT round=revise-1.
- 2026-10-18T13:35:52Z: revise-1 RESULT from a010: PR #412 head a9056299ba965457b569de2d52aa0cbb7abb6e50 (parent b1399953, one push), files `scripts/validate-agent-assets.py`, `tests/unit/test_validate_agent_assets.py`; the two local findings of b139995 `fixed:a9056299` with `test_anthropic_check_keeps_single_quote_semantics_for_backslashes` and `test_anthropic_check_accepts_an_environment_reference_followed_by_a_command` (red 3 and 18 before the source change, green with the full 111); source 292/300, tests 423/1000; CI 13/13; `bot=none` after the 901 s window; native independent review correct; a010's P1-14 a03 is stacked and pushed as 7e4aace6 (no PR until this merges). Read at 19:58Z (the orchestrator's session was suspended from about 15:01Z (its last activity: the #416 chain's end at 15:00:51Z; its last bus line at 14:46:16Z) to 19:58Z); `status=pending-integration` sent 20:0xZ; the chain started on a9056299 at 20:00Z.
local:a64daf1:2	advisory-p2
local-finding: a64daf1:2 not-applicable:advisory P2 owned by dotfiles-T129-anthropic-auth-route-check-followup-a03 (- [P2] Isolate Markdown examples from prose quote state — scripts/validate-agent-assets.py:1882-1886); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T129-anthropic-auth-route-check-followup-a03.md (7d2d12335df793c53fdfbf0097cf4067e6f75b35648c87950d31392921815b27)
local:a64daf1:3	advisory-p2
local-finding: a64daf1:3 not-applicable:advisory P2 owned by dotfiles-T129-anthropic-auth-route-check-followup-a03 (- [P2] Preserve non-shell separators when checking whole values — scripts/validate-agent-assets.py:1889-1893); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T129-anthropic-auth-route-check-followup-a03.md (7d2d12335df793c53fdfbf0097cf4067e6f75b35648c87950d31392921815b27)
local:a64daf1:4	advisory-p2
local-finding: a64daf1:4 not-applicable:advisory P2 owned by dotfiles-T129-anthropic-auth-route-check-followup-a03 (- [P2] Redact assignment payloads from diagnostic key paths — scripts/validate-agent-assets.py:1895-1897); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T129-anthropic-auth-route-check-followup-a03.md (7d2d12335df793c53fdfbf0097cf4067e6f75b35648c87950d31392921815b27)

## Local review of a64daf1 (2026-10-18T20:0xZ to 20:15Z), S1 shell-quoting-bypass, withdrawal

- The chain on the revise-1 head (started 20:00Z after the orchestrator's suspension; update-branched a9056299 → a64daf17 over main 3e41e36a, CI green) ran the local review: 1 P1 and 3 P2 in `scripts/validate-agent-assets.py`, `.orchestration/validation/dotfiles-T129-anthropic-auth-route-check-followup-a02-local-review-a64daf1.md`: (1) P1 lines 1760-1762: `export $'ANTHROPIC_API_\x4bEY'=literal-value` passes (the ANSI-C escape leaves a non-identifier name, so the guard skips refusal while the literal-name regex cannot see the encoded spelling); (2) P2 lines 1895-1897: the diagnostic prints the payload of `{"ANTHROPIC_API_KEY=literal-value": "unused"}`; (3) P2 lines 1882-1886: a Markdown file beginning `Don't store credentials.` lets a later fenced example's assignment pass (the prose apostrophe stays in the shell parser's quote state); (4) P2 lines 1889-1893: a U+2028 or vertical tab between `$DEPLOYED_KEY` and `literal-value` passes (`splitlines()` splits where bash keeps one word). The chain stopped at "a P0/P1 local finding: the one round or the operator"; its four advisory rows under the owner section are superseded by the a03 redesign (fixed there, not advisory), and the file written earlier as the advisory owner task `dotfiles-T129-anthropic-auth-route-check-followup-a03` is replaced by the reset task of that name; the advisory owner of the a03 PR becomes `…-followup-a04`.
- counters (`scripts/regime-counters.sh dotfiles-T129-anthropic-auth-route-check-followup-a02 --pr 412`, 20:16Z): `tasks=1 amendments=0 questions=0 results=2 withdrawn=0 revises=1 first_result_head=d3480fc0 bot_p1_heads_after_result=0` (no S2 line yet; a second revise would reach it, and the operator's directive forbids a third round).

| # | where | finding (class shell-quoting-bypass) |
| --- | --- | --- |
| 1 | local review of b139995 (13:0xZ) | a backslash inside single quotes skipped the closing quote, hiding `export "$NAME"=literal`, fixed at a9056299 |
| 2 | local review of b139995 (13:0xZ) | an assignment word's end was the end of line, so an environment reference followed by a command was reported, fixed at a9056299 |
| 3 | local review of a64daf1 (20:15Z) | an ANSI-C-escaped credential name is not decoded, so the literal assignment passes |

Three rows: S1. The artifact goes to redesign; no further round.

re-plan: shell-quoting-bypass -> specification: the credential check never reasons about shell text with regexes over raw lines; one word scanner tokenises every bash quoting form, decodes escaped names before comparison, takes an assignment word up to an unquoted blank or operator with LF as the only line end, rejects undecodable name forms, parses each fenced example with a fresh quote state and never prints an assignment's payload; design: one scanner and one decoder for the three call sites; implementation: the a03 redesign keeps the two a9056299 fixes and fixes the four findings of a64daf1, on seat a010 before its stacked P1-14 a03; verification: one red-then-green test per finding of both reviews and a table-driven bypass corpus.

- 20:1xZ: `AGMSG-ACCEPTANCE … status=withdrawn` sent to a010 (wJ:p5), with the order: the a03 round first, then P1-14 a03 rebases onto the new #412 head; the P1-14 deadline 2026-10-19T03:00Z stands. The a03 redesign (review profile, prompt `.agents/worklog/orchestrator-glue/ar-a03-redesign-prompt.md`) follows. Record: `.orchestration/acceptance/dotfiles-T129-anthropic-auth-route-check-followup-a03.md` (created at dispatch).
- class table row 4 (added 21:2xZ): a010's independent pre-push review of its a03 source 577ad0f3 (21:20:40Z): the scanner's env context is cleared by an unresolved vanishing or option expansion before a dynamic assignment (`env $opts NAME=literal` passes). The re-plan stands; a04 makes the command-prefix rule explicit.
- class table rows 5 and 6 (added 22:3xZ): the local review of the a04 head 325f520 (22:33Z): subscripted assignments (`ANTHROPIC_API_KEY[0]=…`) pass; the wrapper context is lost through `builtin --`. Six rows; the re-plan's scanner approach is withdrawn for default-deny in a05.
- class table row 7 (added 22:3xZ): the security-profile review of 325f520: an unmatched glob under `nullglob` before a dynamic assignment clears the command context. Seven rows.
- 2026-10-19T21:35:54Z: orchestrator hygiene (C-98): the never-committed nested copies evidence-sync had placed under this task's directory in the main checkout (clean-main/, raw/misplaced-unit-cache-preserved/ (7,658 files, 264 MB)) moved aside to .agents/worklog/evidence-aside/dotfiles-T129-anthropic-auth-route-check-followup-a02/ (restorable with mv; README there); untracked files under .orchestration fell from 17,480 to 1,062, which shortens every post-merge fast-forward from ~10 minutes to seconds.
