- **P1 — High confidence — `scripts/orchestrator/task-consistency-check.py:355`:** C6/C15 fetch the normalized comparison key instead of the original design pathname, allowing a different canonical file to supply approval and invariants.

  `path_entry()` changes `cafe\u0301.md` into `caf\u00e9.md`; `main_entry()` also normalizes at line 176. A read-only, modeled-API reproduction passed with the NFD design’s required invariant omitted and the separate NFC design’s receipt/hash supplied. An ASCII negative control correctly produced C6/C15 findings. A nonexistent NFD design also passed when only its NFC counterpart existed.

  Preserve original path spelling for GitHub requests and use normalization only for comparisons. This leaves the threat-table claims at task lines **32, 33, 39 and 61** unproven for canonical-path identity.

No additional findings were identified in injection, token forwarding, unsafe deserialization, local traversal/symlink confinement, or C14 execution authorization. Documented parent-execution, shared-cache and same-UID residuals remain.

📝 まとめ: Reviewed [PR #440](https://github.com/mryfmo/dotfiles/pull/440) at the specified head; reproduced one approval/invariant-binding bypass. No files changed.
Not checked: full test reruns or live GitHub/CI results; `gh` failed to connect. The reproduction used mocked API responses.

Verdict: incorrect