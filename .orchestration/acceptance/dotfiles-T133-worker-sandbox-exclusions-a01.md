---
{
  "audit_findings": [],
  "dispatch": [],
  "format": 1,
  "head": null,
  "ledger": [
    {
      "class": "contract-restatement",
      "id": "audit:232c174:401"
    },
    {
      "class": "unsupported-claim",
      "id": "audit:232c174:402"
    },
    {
      "class": "allowed-files-gap",
      "id": "audit:232c174:403"
    },
    {
      "class": "happy-path-closing-test",
      "id": "audit:232c174:404"
    }
  ],
  "pr": null,
  "replans": {},
  "searches": [],
  "task": "dotfiles-T133-worker-sandbox-exclusions-a01"
}
---

# Acceptance record: dotfiles-T133-worker-sandbox-exclusions-a01

Lineage: design 5.14 item 10 (024-design-quality.md:116, "worker 席の除外コマンドは空にし…"), unassigned in Phase 1 until D-024-46: remove the `agmsg-dispatch *` exclusion of `home/dot_agents/agent-config.yaml`, regenerate the rendered Claude settings, make the validator expect the empty list. Claude-boundary change routed to a Codex seat; permgate stays the operator's step; the live seats take the change at the next `make update` (after P1-14 a05). Evidence for the premise: the T39 measurement (2026-10-01, herdr socket PermissionDenied inside the sandbox) predates the T130 `allowUnixSockets` entry; this orchestrator seat sent agmsg messages 2827 and 2830 from sandboxed Bash on 2026-10-20.

- 2026-10-20T12:21Z-12:29Z: text written whole by the review profile from the orchestrator's brief (`worker-sandbox-exclusions-a01-prompt.md`; security: true; the named test module `tests/unit/test_generate_agent_configs.py` exists); installed, 117 lines, self cap 120; pre-send OK (checker OK, secret-pattern 0, no literal home path, id free), sha256 232c1748c8dec08298acac26d26ef1db51c93102e39d47f3d64e50ad625bf0b5. C-80 round 1 started 12:29Z (security: true, within C-80's scope).
- 2026-10-20T12:29Z-12:32Z: C-80 round 1 (`…-text-security-232c174.md.last.md`) `Verdict: incorrect`, four P2: (1) line 35 the clean-environment control covers one line while generation, lint and Makefile recipes run through the mise-first PATH and git keeps `GIT_*` (contract class); (2) line 94 "Linux seats are measured in CI" is unsupported, no CI step launches a Linux Claude sandbox; (3) line 10 `tests/unit/test_claude_settings_merge.py:591` asserts the old exclusion lists, so the change breaks CI unless that file joins allowed_files with its own row; (4) line 33 the validator test cannot close the broad in-process-effects row. Amendment 1 (review profile, `worker-sandbox-exclusions-a01-r2-prompt.md`): (3) and (2) closed as facts, (4) narrowed, (1) a residual row by reference to design 5.14 items 2, 7, 9 rather than a restatement; C-80 round 2 follows.

text-security:232c174:1	contract-restatement
text-security:232c174:2	unsupported-claim
text-security:232c174:3	allowed-files-gap
text-security:232c174:4	happy-path-closing-test
- 2026-10-20T13:27Z-13:35Z: amendment 1 installed (124 lines, self cap 125; `tests/unit/test_claude_settings_merge.py` added to allowed_files; Linux runtime stated unmeasured; in-process and environment rows residual by reference); C-80 round 2 (`…-text-security-2116a65.md.last.md`) `Verdict: correct`. Checks pasted; final sha256 5643d5e9b3b23cc7558d7e4bd352d55858d7191e9522c79161465c239303819b; dispatched to a013 (Codex worker-h; Claude-boundary change) at 13:35Z with base origin/main 230b3676.
- 2026-10-20T13:31Z-13:33Z: the pasted Checks block took the text to 129 lines against its own cap of 125; pre-send refused and the TASK (2840, bytes 5643d5e9…) was dispatched anyway because the step ignored pre-send's exit code (M-20261020-08). Amendment 1 (one number: the self cap 125 -> 135; bytes 3d91e23d…) dispatched through the new `send-task.sh` gate (C-118), which refused once on its own grep defect before sending.
- 2026-10-20T13:39:59Z: a013 PONG `status=blocked`: the text's evidence item asked for a sandboxed `agmsg-dispatch` probe; from the Codex sandbox (`network_access=false`, no unix-socket allowlist) the probe returned `PermissionDenied: Operation not permitted` (exit 1, `pane-not-found-or-unavailable wJ:p1`), implementation_commits=0. Correct refusal; the requirement was impossible from a Codex seat (orchestrator brief defect). This measurement is the evidence for the Codex half of design 5.14 item 10: the Codex sandbox as configured denies the herdr socket; `network_access = true` (the design's Codex setting) is a separate task and its effect on unix sockets is unmeasured.
- 2026-10-20T14:12Z: INV-6 S2 (amendments 2, both orchestrator brief defects: the cap number and the probe requirement): lineage withdrawn (ACCEPTANCE status=withdrawn to a013); reset `dotfiles-T133-worker-sandbox-exclusions-a02` (review profile; evidence = the orchestrator's macOS measurement in the a02 record + the worker's own Codex probe result; cap 140; the checker's reset rows added) is in C-80. a013 holds for the a02 TASK.
