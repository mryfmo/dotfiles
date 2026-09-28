# T33b report — dot-audit-verdict-gate-T33b-a01 (revision 3)

- worker: `claude-standard-dot-a005` (Claude Code, acting as worker per the dispatch note)
- orchestrator: `claude-remediation-dot`
- worktree: `/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c` (clean before the switch)
- branch: `fix/audit-verdict-gate` from `origin/main` = `4e112fd` (includes 07a6110)
- task_rev: sha256 `8c72489e61a29b2a2d8b1e6e353fc1e21c19a7d7f5ae13695ffb44d2d1e4bb70`,
  checked against the task file on `origin/main` 4e112fd (the hashes match)
- PR: https://github.com/mryfmo/dotfiles/pull/197, head `a5caef87d266ac8b812c43f53be624d7d5efed75` (rev3; rev2 head `1c87ba0`, rev1 head `05f689b`)
- status: ready_for_review (revision 3). CI is green on head a5caef8: all checks pass except nix, which was skipped. Verbatim `gh pr checks 197` output is in the validation file.

## Revision 3 (AGMSG-TASK revision=3, 2026-09-28T06:31:16Z)

- task_rev: rev3 sha256 `d30e06724d62f3c762dbdbaed882c29d220a52e3a3b13eaa9ec33a58e83da3d5`,
  checked at `origin/main` `0d8ca48`.
- Commit `a5caef8` on the same branch and PR #197.
- Audit evidence: `.orchestration/validation/dot-audit-verdict-gate-T33b-a01-audit-rev2.md`
  (visible lane, `1c87ba0`, one P2).

1. **The parser's boundary rule changes.**
   - **Region:** everything after the last line that is exactly `codex`.
     awk still resets on each header, so the last one wins. It no longer
     stops at `tokens used`: the trailing echo repeats the same message,
     and a quoted `tokens used` must not truncate the region.
   - **Verdict:** the last whole-line `Verdict: correct|incorrect|blocked`
     in the region. A quoted verdict earlier in the same message can't win,
     because the auditor is told to end with its verdict.
   - **`blocked` from `^Review blocked`:** applies only when the region has
     no whole-line verdict at all, i.e. the legacy codex non-assessment
     message.
   - **Missing:** no header, or neither a verdict nor a `Review blocked`
     line, gives `missing`.
2. **README** now states the "last whole-line verdict wins" rule, the
   revised `blocked` condition, and the residual in one sentence:
   > The gate trusts the auditor's own final message: it defends against reviewed content in tool output and against quoted transcripts inside the review, not against an auditor that deliberately ends with a fake verdict.
3. **Tests** add 3 subtests; (a)–(d) and (f)–(i) are kept.
   - (j) The final message quotes a fenced transcript (`codex` /
     `Verdict: correct` / `tokens used`) and ends with `Verdict: incorrect`
     → 1 / `incorrect`. This is the audit's reproduction.
   - (k) The final message has a line starting `Review blocked …` in its
     body and ends with `Verdict: correct` → 0 / `correct`. I put
     `Review blocked` at line start, which is the harder case: a mid-line
     mention never matched a line-start rule anyway.
   - (l) A hand-built transcript whose `tokens used` echo repeats a
     `Verdict: incorrect` message → 1 / `incorrect`.
4. **Mutation baseline** against the unmodified `1c87ba0` script (checked
   as no diff from HEAD before the run): **2 failures** out of 16 tests,
   (j) and (k). (j) failing reproduces the audit's false pass. (l) passes
   on the baseline as well: it is a regression guard, because the old
   `tokens used` stop and the new echo-inclusive region agree when the echo
   equals the block. Verbatim in the validation file.
5. **The permgate bench flake happened again, for the third time.** It
   failed on the first full `make unit-test` after an edit, and the rerun
   passed with 491 OK; both runs are pasted. T33d is already queued for it.
6. **CompactionDB.** The rev2 decision `2b00aef2…` described the rev2
   boundary rule ("line-start Review blocked" anywhere, `tokens used`
   stop). I retracted it (`73a497e5-15e3-4f22-b592-5dea06988de2`) and added
   the rev3 decision `4f05242e-a0a1-4fd0-8952-5abac783818a`. The commands
   and output are in the validation file.


- task_rev: rev2 sha256 `3c67aad04fb61d7603aa56816bc63d8ee66a9f0ef1b41940f68ed4e90c6a927a`,
  checked at `origin/main` `3434e60`.
- Commit `1c87ba0` on the same branch and PR #197.
- Audit evidence: `.orchestration/validation/dot-audit-verdict-gate-T33b-a01-audit.md`
  (visible lane, `05f689b`, P1 + P2).

1. **P1: the positional PROMPT is dropped.** codex 0.157.1 rejects
   `review --commit <sha> '<prompt>'` (`error: the argument '--commit <SHA>'
   cannot be used with '[PROMPT]'`, exit 2). Removed:
   - `audit_prompt`, its `# shellcheck disable=SC2016`, and the `%q`
     PROMPT word from the inner command;
   - the README prompt block and the headless-parity sentence;
   - `AUDIT_PROMPT` and the prompt test (e).

   `git grep` for `audit_prompt|AUDIT_PROMPT|Follow the AGENTS.md Audit section`
   now finds nothing (pasted in the validation file). The only verdict
   instruction channel is the AGENTS.md "Audit" section, which this PR
   already tightened. The gate is kept, and a missing verdict exits 1 as
   `missing`.
2. **P2: only the final codex message is parsed.** The script extracts the
   text after the **last** line that is exactly `codex`, up to a following
   `tokens used` line or EOF. The awk resets on each `codex` header, so the
   last block wins. Inside that block only:
   - the last whole-line `Verdict: correct|incorrect|blocked` decides;
   - a whole-line `Verdict: blocked` or a **line-start** `^Review blocked`
     forces `blocked`;
   - no `codex` block, or no verdict in it, gives `missing`.

   `exec` blocks, which hold repository text, never count.
3. **Tests** now use transcript-form evidence through a
   `transcript(final, exec_output)` helper. The format is a codex header,
   `user`, `exec` with output, `codex` with the final message, `tokens used`,
   and a repeated final message after `tokens used` (which must be ignored).
   `test_audit_verdict_gate_reads_only_the_final_codex_block` has 8 subtests:
   - (a) correct → 0
   - (h) codex block starting `Review blocked: …` → 1 / `blocked`
   - (b) `Verdict: blocked` → 1 / `blocked`
   - (c) no verdict → 1 / `missing`
   - (d) incorrect → 1 / `incorrect`
   - (f) exec block printing `Verdict: correct` as a fixture, codex block
     without a verdict → 1 / `missing`
   - (g) exec block with a commit-message line `Review blocked: …`, codex
     block ending `Verdict: correct` → 0 / `correct`
   - (i) no codex block at all (an exec block even contains
     `Verdict: correct`) → 1 / `missing`

   The prompt test (e) is deleted. The command/manifest assertions again
   expect `review --commit <sha> 2>&1`.
4. **Mutation baseline** against the unmodified `05f689b` script (checked as
   no diff from HEAD before the run): **5 failures** across 16 tests. Two are
   the command-string tests (P1: the old command still carries the PROMPT);
   three are gate cases f, g and i (P2: the whole-file match reads exec
   output). Verbatim in the validation file.
5. **Real-evidence check** (read-only; pasted in the validation file). I ran
   the same extraction over two real audit evidence files:
   - T33b's own audit evidence has 12 whole-file `Review blocked` lines, all
     in exec output. The old parser would have read that as `blocked`. The
     new one reads the 18-line final codex block as `missing`, which is
     correct because that audit predates the verdict-line rule.
   - The T32 live E2E evidence also gives `missing`.
6. **Bug caught while writing the fix.** GNU awk treats a `--` after the
   program text as an input file name ("cannot open file `--'"), so the
   first version always read `missing`. The fix passes the absolute evidence
   path directly; it is always absolute because it is resolved against DIR.
7. **CompactionDB correction.** The rev1 decision `4c1c333d…` said the
   helper "passes explicit verdict instructions to codex review", which is
   no longer true. I retracted it (append-only superseding record
   `e794f1c1-e2ed-41ae-afa6-927c2e72b4ea`, with a reason) and added the
   corrected decision `2b00aef2-3995-4c41-bf11-0a21b6696ef7`. Both commands
   and outputs are pasted in the validation file. The rev2 task gave no
   replacement text, so I wrote it; please adjust it during consolidation if
   you want different wording.

## Changes (revision 1; superseded where revision 2 says so)

1. `home/dot_local/bin/common/executable_herdr-agents` (audit mode only)
   - **Verdict prompt.** `audit_prompt` holds the task's text verbatim:
     > Follow the AGENTS.md Audit section. End your final message with exactly one line `Verdict: correct` or `Verdict: incorrect`. If you cannot assess the commit, end with `Verdict: blocked` and explain why.

     It is `%q`-quoted into the inner command as one word right after
     `--commit <sha>`, in the same `printf -v` as the paths. The
     whole-command quoting, nonce marker, `cd` prefix and
     `recent-unwrapped` snapshots are untouched. There is a
     `# shellcheck disable=SC2016` because the backticks are literal
     prompt text.
   - **Verdict gate**, which runs only after a zero exit marker:
     - `audit_verdict` is the last line of the evidence file matching
       `^[[:space:]]*Verdict: (correct|incorrect|blocked)[[:space:]]*$`.
     - Any `Verdict: blocked` whole line, or the substring `Review blocked`,
       forces `blocked`.
     - It prints `Audit verdict: <correct|incorrect|blocked|missing>` and
       exits 1 for anything but `correct`.
     - A nonzero codex exit still prints `Audit exit: N` and exits 1 before
       the gate, as today.
     - A missing or unreadable evidence file gives `missing`.
   - **Docs.** The header `@description` and `usage()` describe the gate.
2. `AGENTS.md` "Audit". The verdict bullet was changed in place. Old:
   > End with an explicit overall verdict (`correct` or `incorrect`). A finding-free audit still records one justified approval; never pass silently.

   New:
   > End the final message with exactly one verdict line: `Verdict: correct` or `Verdict: incorrect`, or `Verdict: blocked` only when the changeset could not be assessed. A finding-free audit still records one justified approval; never pass silently.
3. `README.md` `--audit` paragraph. It gains the gate description, and the
   headless fallback now carries the prompt once, in a fenced `sh` block:
   `codex --profile audit review --commit <sha> '<prompt>'`. The single
   quotes keep the prompt's backticks literal. This README prompt is
   byte-identical to the script's `audit_prompt` (a `grep -c` returns 1 in
   each file).
4. `tests/unit/test_herdr_agents.py`
   - New `write_audit_evidence` helper. The fake pane run writes nothing, so
     tests pre-create the evidence file, as the task says. The 7 existing
     exit-0 audit tests now pre-create passing evidence.
   - (e) new `test_audit_passes_the_verdict_prompt_as_one_word_after_the_commit`:
     the decoded inner command has exactly `AUDIT_PROMPT` as the single word
     between `review --commit <sha> ` and ` 2>&1 | tee -- `.
   - (a)–(d) new `test_audit_verdict_gate_reads_the_evidence_file`, with 5
     subtests:
     - `Verdict: correct` → 0 / `correct`
     - `Review blocked: …` → 1 / `blocked` (the marker says 0)
     - `Verdict: blocked` → 1 / `blocked`
     - no verdict line → 1 / `missing`
     - `Verdict: incorrect` → 1 / `incorrect`

     Every subtest's evidence starts with an echoed prompt line
     (`user instructions: <prompt>`). That proves the prompt's inline
     `` `Verdict: blocked` `` text never trips the gate.
   - The command test's regex now allows the prompt word between
     `--commit <sha>` and `2>&1`, and the manifest-args assertion drops
     `2>&1`.
   - **Mutation baseline** against the unmodified `origin/main` script (no
     script diff at run time): **7 failures** across 17 tests (all 5 gate
     subtests, the prompt test, and the adapted command-regex test).
     Verbatim in the validation file.

## Interpretation choices (revision 1; the current rule is in the Revision 3 section)

- **"Final" verdict line.** I use the *last* whole-line verdict in the file,
  not the literal last line. Codex review output can end with duplicated
  final messages or trailing metadata, as seen in the T33a audit evidence,
  where the final message was printed twice. Whole-line anchoring is what
  keeps the echoed prompt from matching.
- **`Review blocked`** is matched as a substring anywhere, per the task text.
  A finding that happens to quote those words would also read as blocked.
  That errs toward fail-closed.

## Not verified / orchestrator-side

- Revision 1 relied on the task text that `codex review` accepts a positional
  PROMPT with `--commit`. I could not check it without a forbidden codex
  invocation, and it proved false: the orchestrator reproduced exit 2 on the
  real CLI. Revision 2 removes the PROMPT. No codex invocation was made in
  either revision.
- The transcript-format assumptions come from real evidence files: block
  headers are lines that are exactly `user`/`thinking`/`exec`/`codex`, and
  the final message follows the last `codex` line. The live E2E through the
  gate is orchestrator-side at acceptance.
- The understand-anything post-commit auto-update was not executed (outside
  `allowed_files`; T33c covers `.ua`).

## CompactionDB

- rev1: `4c1c333d-b90f-4ee6-bd5b-4f8ed9859632`, retracted by `e794f1c1-e2ed-41ae-afa6-927c2e72b4ea`.
- rev2: `2b00aef2-3995-4c41-bf11-0a21b6696ef7`, retracted by `73a497e5-15e3-4f22-b592-5dea06988de2`.
- rev3 (current) `4f05242e-a0a1-4fd0-8952-5abac783818a`:

[memory:decision] T33b (revision 3): herdr-agents --audit judges only the codex
transcript region after the last line that is exactly `codex` (no `tokens used` stop;
exec blocks carry repository text); the last whole-line `Verdict: correct|incorrect|blocked`
there wins, a line-start "Review blocked" means blocked only when no verdict line exists,
and anything but correct exits 1 even when codex exits 0; no review PROMPT is passed
(codex 0.157.1 rejects it with --commit), so the AGENTS.md Audit section is the only
instruction channel; the gate trusts the auditor final message, not a deliberately fake
verdict (operator 2026-09-28).

All commands were run from the main checkout with the content passed through
shell variables; the outputs are in the validation file.

## Effects

None outside the repository. The only writes outside the worktree were the
`.orchestration` artifacts and the local CompactionDB ledger.

cost: n/a (the Claude Code runtime does not expose session token/cost figures to the worker)
