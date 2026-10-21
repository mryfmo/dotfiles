---
{
  "audit_findings": [],
  "dispatch": [],
  "format": 1,
  "head": null,
  "ledger": [
    {
      "class": "contract-restatement",
      "id": "audit:c32513e:401"
    },
    {
      "class": "happy-path-closing-test",
      "id": "audit:c32513e:402"
    },
    {
      "class": "contract-restatement",
      "id": "audit:c32513e:403"
    },
    {
      "class": "unsupported-claim",
      "id": "audit:c32513e:404"
    },
    {
      "class": "validation-setup",
      "id": "audit:c32513e:405"
    },
    {
      "class": "owner-mismatch",
      "id": "audit:eaf8c47:401"
    },
    {
      "class": "contract-restatement",
      "id": "audit:eaf8c47:402"
    },
    {
      "class": "validation-setup",
      "id": "audit:eaf8c47:403"
    },
    {
      "class": "validation-setup",
      "id": "audit:d44acec:401"
    }
  ],
  "pr": null,
  "replans": {
    "contract-restatement": {
      "design": "the brief template forbids restating the contract and asks for the measured seat state instead of a claim (the Linux exclusions, `failIfUnavailable: false`)",
      "implementation": "amendments 1 and 2 of this text (residual rows owned by `dotfiles-T133-regime-ci-token-followup-a01`, the measured sandbox sentence) and the C-112 pre-send check for texts that impose caller obligations",
      "specification": "a task text for a tool that runs git or gh names design 5.14 items 2, 7, 9 and 10 by reference and states only the tool's own controls; every environment or executable row it cannot close itself is `residual` with the owner named (the shared contract tests of #436, the binding of #431, or the lineage's follow-up)",
      "verification": "C-80 round 4 (`…-2c8c05a.md.last.md`) reports no contract-class finding, and the task-level audit of the final head confirms the rows."
    },
    "validation-setup": {
      "design": "the orchestrator measures the host facts before the brief (`mise` at `$HOME/.local/bin/mise`, uv under `installs/uv/<version>/uv-<target>/`) and the text carries the resolve command (`UV_DIR=$(dirname \"$(env -i PATH=/usr/bin:/bin HOME=\"$HOME\" \"$HOME/.local/bin/mise\" which uv)\")`) rather than a path",
      "implementation": "amendments 2 and 3 of this text; the brief template gains a \"host facts\" paragraph measured by the orchestrator",
      "specification": "every validation command in a text runs as written on the worker's host: executables are resolved by a stated command whose output the worker pastes, with no assumed `bin` subdirectory, pin file or shim",
      "verification": "C-80 round 4 correct; the worker's report.md pastes the resolved path and the green test run under that PATH."
    }
  },
  "searches": [],
  "task": "dotfiles-T133-regime-ci-token-a01"
}
---

# Acceptance record: dotfiles-T133-regime-ci-token-a01

Lineage: the regime workflow passes `GH_TOKEN: ${{ github.token }}` and regime-ci.py forwards it into the checker's minimal environment, so the a06 checker's new `gh api` requests (PR #440, head 2cb58482/21f52c79) get a verdict in CI. Caller-side dependency found by the local review of #440 (local:21f52c7:1); #440 waits for this lineage. Security: true (a CI workflow).

- 2026-10-20T13:27Z-13:36Z: text written whole by the review profile from the orchestrator's brief (`regime-ci-token-a01-prompt.md`); installed, 95 lines, self cap 110; pre-send OK (checker OK, secret-pattern 0, no literal home path, id free), sha256 c32513e5cbf65661a7a5d2f385dd814f6735d9ddaa1495b03da47db2f9c71335. C-80 round 1 started 13:37Z.

## Owned by dotfiles-T133-regime-ci-token-followup-a01

(no advisory rows yet; written 2026-10-20T14:17Z before the regime-ci-token PR's first advisory disposition, C-51; the owner text carries the lineage's residual rows as items)
- 2026-10-20T13:36Z-14:26Z: C-80 round 1 incorrect (1 P1 sandbox claim + 4 P2), round 2 incorrect (3 P2: the owner named a merged lineage, `failIfUnavailable`, the uv path facts), round 3 incorrect (1 P2: the pin-file and `bin` assumptions), round 4 `Verdict: correct` (`…-text-security-2c8c05a.md.last.md`); owner text `dotfiles-T133-regime-ci-token-followup-a01` written with the residual rows (CHECKER_RUN executable selection, GIT_DIR) as its item 2. Checks pasted; final sha256 61a9942b4e74bc53129a733761bb192eec875fddbd91be458243c530f448405b; dispatched to a009 at 2026-10-20T14:27Z through send-task.sh. Rows: text-security:c32513e:1-5, text-security:eaf8c47:1-3, text-security:d44acec:1.

text-security:c32513e:1	contract-restatement
text-security:c32513e:2	happy-path-closing-test
text-security:c32513e:3	contract-restatement
text-security:c32513e:4	unsupported-claim
text-security:c32513e:5	validation-setup
text-security:eaf8c47:1	owner-mismatch
text-security:eaf8c47:2	contract-restatement
text-security:eaf8c47:3	validation-setup
text-security:d44acec:1	validation-setup
re-plan: contract-restatement (rows text-security:c32513e:1, text-security:c32513e:3, text-security:eaf8c47:2; the class the D-024-37 hold was declared for) — specification: a task text for a tool that runs git or gh names design 5.14 items 2, 7, 9 and 10 by reference and states only the tool's own controls; every environment or executable row it cannot close itself is `residual` with the owner named (the shared contract tests of #436, the binding of #431, or the lineage's follow-up); design: the brief template forbids restating the contract and asks for the measured seat state instead of a claim (the Linux exclusions, `failIfUnavailable: false`); implementation: amendments 1 and 2 of this text (residual rows owned by `dotfiles-T133-regime-ci-token-followup-a01`, the measured sandbox sentence) and the C-112 pre-send check for texts that impose caller obligations; verification: C-80 round 4 (`…-2c8c05a.md.last.md`) reports no contract-class finding, and the task-level audit of the final head confirms the rows.
re-plan: validation-setup (rows text-security:c32513e:5, text-security:eaf8c47:3, text-security:d44acec:1) — specification: every validation command in a text runs as written on the worker's host: executables are resolved by a stated command whose output the worker pastes, with no assumed `bin` subdirectory, pin file or shim; design: the orchestrator measures the host facts before the brief (`mise` at `$HOME/.local/bin/mise`, uv under `installs/uv/<version>/uv-<target>/`) and the text carries the resolve command (`UV_DIR=$(dirname "$(env -i PATH=/usr/bin:/bin HOME="$HOME" "$HOME/.local/bin/mise" which uv)")`) rather than a path; implementation: amendments 2 and 3 of this text; the brief template gains a "host facts" paragraph measured by the orchestrator; verification: C-80 round 4 correct; the worker's report.md pastes the resolved path and the green test run under that PATH.
- 2026-10-20T14:28:56Z/14:36:21Z: a009 PONG `status=question` x2 (premise gap, nothing edited): regime-ci.py at f7f38067 passes no `env=` to the checker, so there is no minimal environment to extend and GH_TOKEN reaches the child once the workflow sets it; introducing an allowlist would be an unstated behaviour change and strips the sandbox proxy variables (measured: the Check's `env -i` command fails 21/16 on unmodified f7f38067 by DNS errors; 16/16 with HTTPS_PROXY/HTTP_PROXY/NO_PROXY passed through). Answer (2026-10-20T14:43Z, PING 2878): option (b) keep the inherited environment, change regime.yml only, tests for presence-iff and no token in argv/output, proxies pass through; amendment 1 carries the words (C-119). Row `worker:f7f3806:1 premise-gap` (the orchestrator's brief inferred the environment from a test name).

worker:f7f3806:1	premise-gap

