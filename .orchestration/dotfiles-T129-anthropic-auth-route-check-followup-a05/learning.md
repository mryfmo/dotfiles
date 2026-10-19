# Task learning report

Status: local implementation observation; final-head review and delivery pending. This durable task evidence is committed with report/validation/sandbox as specifically requested. Timestamped plan/todo/learn worklogs remain uncommitted.

The scanner lineage accumulated unrelated shell-context fixes because acceptance depended on recognizing shell structure. The fixed whole-line allowlist removes that interface: raw/decoded occurrence detection can grow without adding a new shell-command exception. Preserve the original line and LF mapping while decoding names; never run the acceptance regex against a normalized line.

The unchanged 325f520b baseline already rejects typeset -x. Record that baseline success rather than manufacturing a RED claim. The new policy also deliberately turns credential-free unresolved syntax into passing controls and raw comments into notes; baseline comparison therefore records classification changes separately from missed hard findings.

A layered percent-to-Unicode spelling exposed decoder ordering during implementation: stabilizing retained decoding transforms before final quote/punctuation removal preserves the backslash needed by the next transform. Its first failing run is development evidence, not an independent review or a final-head failure.

Keep actual checks distinguishable: unit/format/applied-auth pass; Ruff is an inherited failing check with an original-filename baseline; CI and audit are not yet run. Commit durable evidence with the implementation so reviewers can inspect it from the PR, and preserve large transient worklogs separately when they are not required delivery artifacts. No durable project memory was written from this read-only-to-main worker seat.

