---
id: M-20261020-03
date: 2026-10-20
classes: [checker-exit-unchecked]
severity: P2
---

# An amendment was dispatched after its editing script had failed

**What happened.** The a07 (T128 chain-review-scripts) amendment command asserted three occurrences of `PR #402` where the text had four; the Python step raised and wrote nothing, but the shell continued, ran pre-send on the unchanged text and dispatched message 2710 (04:22:08Z) announcing an amendment that carried the unamended sha256. The project-map subagent noticed it at 13:24 JST; the text was amended and resent (`t128-a07-amend1b.txt`).

**What the rules say.** C-100: the dispatch is preceded by the text's checks on the final bytes; a dispatch line's hash must be of the bytes the note describes.

**Why the rules did not fire.** The command chained independent steps without `set -e`, and pre-send checks bytes, not intent: an unchanged text passes.

**Mechanism.** Every orchestrator command that edits and then dispatches runs under `set -e` with an explicit assertion that the sha256 changed when an amendment is announced (`[ "$sha" != "$previous" ] || exit 1`), as the resend did; the tracked home is `dispatch.sh --next` (loop-limits lineage), which should refuse an amendment note whose `previous_sha256` equals the new `task_sha256`.

**Recurrence (05:02Z).** The a03 amendment-dispatch command used `set -e`, yet the shell continued after the paste step's Python assertion failed and dispatched the unpasted (but reviewed) bytes. `set -e` is not a sufficient guard in this harness shell; the mechanism is a positive check of each step's effect (`grep -q` of the pasted marker in the file, an explicit sha comparison) with `|| exit 1`, and `dispatch.sh --next` refusing a send whose text lacks the current paste marker.

