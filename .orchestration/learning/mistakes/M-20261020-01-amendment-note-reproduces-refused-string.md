---
id: M-20261020-01
date: 2026-10-20
classes: [text-defect]
severity: P2
---

# An amendment note reproduced the string the amendment removed

**What happened.** CI `validate` refused PR #437 head 4045295b: `scripts/validate-agent-assets.py` SECRET_PATTERN (its clause `token\s*[:=]\s*["'][^"']+["']`, case-insensitive) matched the double-quoted token self-assignment in Commands (e)/(f)/(f') of the task copy. Amendment 1 (dispatch 2680, 03:31Z) renamed the variable and verified the Commands block against the pattern, but its own note at line 199 quoted the refused assignment verbatim; head 32f400c3 failed `validate` the same way (run 39364986999, job 118439659322, 03:37:02Z). Worker a013 found the same line independently (PONG 2685, 03:38:42Z) and asked for a new author source.

**What the rules say.** C-100: before a dispatch the orchestrator runs the text's own prerequisites. C-99: a change is applied to every consumer sentence. The task text is a file CI validates, so the validator's scan over the whole file is a prerequisite of every send.

**Why the rules did not fire.** The check was run on the edited part (the Commands block), not on the whole file, and no single pre-send command existed that applies CI's checks to the text as a whole; each check was recalled and run by hand.

**Mechanism.** `.agents/worklog/orchestrator-glue/pre-send.sh <task-file>` runs, in one call, the consistency checker, the validator's own SECRET_PATTERN over every line, a literal-home-path grep, the text's self cap and `bash -n` over every fenced bash block, and prints the sha256 the dispatch line carries; every dispatch and amendment runs it on the final bytes and pastes its output in the record (C-100). Its tracked home is `scripts/orchestrator/dispatch.sh`, owned by the loop-limits lineage (`dotfiles-T133-loop-limits-a01` lists it): the follow-up text of that lineage folds the pre-send checks into `dispatch.sh --next` so the orchestrator cannot send unchecked bytes.
