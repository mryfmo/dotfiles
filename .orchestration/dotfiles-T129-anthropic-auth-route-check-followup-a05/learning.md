# Task learning report

Final local update: fresh full make on rebased 5a882074 exited0 with unchanged before/after input hashes. CI/automatic-window status is observed on the pushed head in the delivery record and RESULT. The a06-owned P2 stays open.

Status: one independent review, one consolidated correction and the authorized rebase complete; delivery is in progress and one Markdown-list P2 remains open under the orchestrator-confirmed a06 owner. This durable task evidence is committed with report/validation/sandbox as specifically requested. Timestamped plan/todo/learn worklogs remain uncommitted.

The scanner lineage accumulated unrelated shell-context fixes because acceptance depended on recognizing shell structure. The fixed whole-line allowlist removes that interface: raw/decoded occurrence detection can grow without adding a new shell-command exception. Preserve the original line and LF mapping while decoding names; never run the acceptance regex against a normalized line.

The unchanged 325f520b baseline already rejects typeset -x. Record that baseline success rather than manufacturing a RED claim. The new policy also deliberately turns credential-free unresolved syntax into passing controls and raw comments into notes; baseline comparison therefore records classification changes separately from missed hard findings.

A layered percent-to-Unicode spelling exposed decoder ordering during implementation: stabilizing retained decoding transforms before final quote/punctuation removal preserves the backslash needed by the next transform. Its first failing run is development evidence, not an independent review or a final-head failure.

The independent review additionally showed that normalization must be inspected alongside every raw/intermediate view, rather than only after decoding: a bare backslash before uppercase E is otherwise consumed as an ANSI-C control. Preserve both views. Its P1 and the quoted/fake-closing Markdown-fence P2 were addressed together, with four RED reproductions before the sole correction. Bounded verification then found list-contained fences still misclassified; record that P2 openly and honor the round limit instead of disguising another correction as verification.

Keep actual checks distinguishable: unit/format/applied-auth pass; Ruff is an inherited failing check with an original-filename baseline; CI and audit are not yet run. Commit durable evidence with the implementation so reviewers can inspect it from the PR, and preserve large transient worklogs separately when they are not required delivery artifacts. No durable project memory was written from this read-only-to-main worker seat.

The release at 03:17:43Z reverses PR order, so preserve its provenance rather than treating the earlier hold as current. The single rebase onto 212efe97 changes commit identities but leaves source/test/task hashes and all four reset patches identical; retain the original independent-review head and provide the rebased fix mapping. Full validation on the corrected pre-rebase snapshot passed; rebased unit/format/auth checks pass again. Post-push CI and automatic-window facts are written to the delivery observation and RESULT, avoiding a prediction in this pre-push artifact.

