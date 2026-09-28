# AGMSG-TASK dot-audit-verdict-gate-T33b-a01 (revision 2)

Revision 2 (2026-09-28, pre-merge visible-lane Codex audit of 05f689b: P1 + P2, both confirmed by the orchestrator):

- **P1 — drop the positional PROMPT.** The pinned Codex CLI 0.157.1 rejects it: `codex review --commit <sha> 'x'` → `error: the argument '--commit <SHA>' cannot be used with '[PROMPT]'`, exit 2 (orchestrator reproduced on the real CLI; revision 1's task text was wrong to assert otherwise). Remove `audit_prompt` and the `%q` PROMPT from the inner command, the README PROMPT example and "headless parity" sentence, `AUDIT_PROMPT` and the prompt test. The verdict instruction channel is the AGENTS.md Audit section alone (already tightened to the exact `Verdict:` line in this PR; codex review reads the project AGENTS.md). Keep the gate: a missing verdict exits 1 as `missing`, which is the orchestrator's signal to judge manually.
- **P2 — parse only the auditor's final response.** The evidence file is the codex CLI transcript: blocks introduced by a line that is exactly `user`, `thinking`, `exec`, or `codex`; the final assistant message is the text after the LAST line matching `^codex$` (to EOF or a following `tokens used` line). Tool output (`exec` blocks) contains repository text — the T32 live evidence carries 16 lines of `AUDIT-EXIT` from a diff, and the audit of THIS PR carries 12 lines with `Review blocked` from its own README/tests — so matching the whole file yields false `blocked` (this PR's merge commit would fail its own live E2E) and false `correct` (a fixture line in an exec block). Extract the last `codex` block first, then apply the whole-line `Verdict:` match (last one wins) and a LINE-START `^Review blocked` match inside that block only. No `codex` block at all → `missing`.
- Tests (mutation baseline against the unmodified 05f689b script for the new/changed cases): evidence fixtures must use the transcript format; add (f) `exec` block containing `Verdict: correct` as a printed fixture, `codex` block without a verdict → exit 1 `missing`; (g) `exec` block containing a commit message line with `Review blocked` plus a `codex` block ending `Verdict: correct` → exit 0 `correct`; (h) `codex` block starting `Review blocked: …` → `blocked`; (i) no `codex` block → `missing`; keep (a)–(d) in transcript form; delete (e).

Items below are the revision-1 text, superseded where the notes above say so.

## Objective

Two evidence-integrity defects found while operating the audit lane:

1. `codex review` exits 0 when it does not assess the code (observed: "Review
   blocked: `0000000` does not resolve to a commit in this repository" → the
   launcher printed `Audit exit: 0`). A non-assessment must not read as a
   passing audit.
2. Audits ended without the explicit overall verdict that AGENTS.md "Audit"
   requires (`correct` or `incorrect`); three of five live audits omitted it.

Fix in `herdr-agents --audit`:

- Pass custom review instructions as the `codex review` positional PROMPT
  (kept in one shell variable, `%q`-quoted into the inner command like the
  paths): "Follow the AGENTS.md Audit section. End your final message with
  exactly one line `Verdict: correct` or `Verdict: incorrect`. If you cannot
  assess the commit, end with `Verdict: blocked` and explain why." Keep
  `--commit <sha>` as is.
- After the exit marker, gate on the evidence file: if the audit exit is 0
  but the file lacks a final `Verdict: correct|incorrect` line, or contains
  `Verdict: blocked` or `Review blocked`, print
  `Audit verdict: <blocked|missing>` on stdout and exit 1 (distinct from a
  nonzero codex exit, which stays as today). Print `Audit verdict: correct`
  or `Audit verdict: incorrect` otherwise; `incorrect` also exits 1 (findings
  are input to the orchestrator; the nonzero exit is the signal).
- Headless fallback parity: document in the README paragraph that headless
  invocations should pass the same PROMPT (quote it once in the README).

Fix in `AGENTS.md` "Audit": change the verdict bullet to require the exact
final line format `Verdict: correct` / `Verdict: incorrect` / `Verdict:
blocked` (blocked only when the changeset could not be assessed).

[memory:decision] T33b: herdr-agents --audit passes explicit verdict
instructions to codex review and gates on the evidence file — a missing or
`blocked` verdict, or a "Review blocked" non-assessment, exits 1 even when
codex exits 0; AGENTS.md Audit requires the exact `Verdict: correct|incorrect|blocked`
final line (operator 2026-09-28).

## Repo / branch

- Work ONLY in `/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c`.
- `git fetch origin`; `git switch -c fix/audit-verdict-gate origin/main`.
  Verify the dispatched task_rev sha256 against this file on your base, else
  stop and PONG. If the worktree has uncommitted files, stop and PONG.

## Changes

- `home/dot_local/bin/common/executable_herdr-agents` (audit mode only; keep
  the whole-command quoting, nonce marker, cd prefix, unwrapped snapshots).
- `AGENTS.md` Audit bullet as above.
- `README.md` `--audit` paragraph: verdict gate + headless PROMPT parity.
- `tests/unit/test_herdr_agents.py`: the fake pane run writes nothing, so tests
  pre-create the evidence file. Cases with a mutation baseline against the
  unmodified origin/main script: (a) evidence ending `Verdict: correct` → exit
  0 and `Audit verdict: correct`; (b) evidence with `Review blocked` → exit 1
  and `Audit verdict: blocked` although the marker says 0; (c) evidence without
  any verdict line → exit 1, `Audit verdict: missing`; (d) `Verdict:
  incorrect` → exit 1, `Audit verdict: incorrect`; (e) the decoded inner
  command contains the PROMPT as one word after `--commit <sha>` (reuse the
  T32b decoding helpers).

## Allowed files

- `home/dot_local/bin/common/executable_herdr-agents`
- `AGENTS.md`
- `README.md`
- `tests/unit/test_herdr_agents.py`
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dot-audit-verdict-gate-T33b-a01.md` (main checkout)

## Forbidden actions

- Running a real audit or any codex invocation; creating real herdr tabs or
  panes; touching model_profiles, permgate, hooks configs, dependencies,
  validator/generator scripts, rules/SKILL text, `reviews/ADH_Integrated_Plan/`.
- Merging; force push; local bats; `make apply`/`chezmoi apply`; writes
  outside the worktree except the listed `.orchestration` paths.

## Validation commands (paste verbatim output)

```
make validate-agent-assets
make unit-test
shellcheck home/dot_local/bin/common/executable_herdr-agents
shfmt --indent 4 --space-redirects --diff home/dot_local/bin/common/executable_herdr-agents
git -C /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c diff origin/main --stat
gh pr checks <pr-number>
```

## Completion

1. PR to `main`, English title/description ending with
   `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. CI green.
2. Artifacts at the exact expected paths; validation with verbatim outputs
   (including the mutation baseline) and the PR number/head SHA.
3. CompactionDB from the main checkout: `memory add --kind decision --scope project` with the `[memory:decision]` text above — paste command and output.
4. `inbox.sh dotfiles claude-standard-dot-a005` at each milestone.
5. `AGMSG-RESULT v1` with all artifact paths; `cost:` line in the report.
   Live E2E (a real `--audit` run through the verdict gate) is
   orchestrator-side at acceptance.
