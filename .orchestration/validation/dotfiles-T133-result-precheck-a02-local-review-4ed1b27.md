---
task: dotfiles-T133-result-precheck-a02
head: 4ed1b27a666ba939db76051243143a7d7ed2aaa5
pr: 411
base: de3b73cc4f8874a30be6adc47a0f07575869d0df
started: 2026-10-18T13:35:07Z
finished: 2026-10-18T13:44:40Z
findings: 3
engine: codex review --base main (profile review, read-only)
---

- [P1] Scan blobs separately to preserve JSON secret detection — .githooks/pre-push:27-31
- [P2] Reject results that precede the latest revision request — scripts/orchestrator/dispatch.sh:174-176
- [P2] Separate home-path normalization from secret detection — scripts/orchestrator/result-precheck.sh:98-103

```text
Reviewed the original 4ed1b27a head against the supplied base because the shared worktree moved during review. Reproductions confirmed a secret-scan bypass, stale revision acceptance, and false-positive push blocking; full tests were not run in the read-only sandbox.

Full review comments:

- [P1] Scan blobs separately to preserve JSON secret detection — .githooks/pre-push:27-31
  When multiple blobs are concatenated, the scan input is usually no longer valid JSON. The masker consequently falls back to raw-text matching and misses credentials with JSON-escaped prefixes such as `\u0067hp_...`. I reproduced a detected credential becoming zero matches after appending a clean JSON blob. Scan blobs independently to preserve per-file JSON decoding, and cover this bypass in the declared closed control ([AGENTS.md:78](AGENTS.md#L78)).

- [P2] Reject results that precede the latest revision request — scripts/orchestrator/dispatch.sh:174-176
  When a `status=revise ... check=...` ACCEPTANCE follows the last ready RESULT, this slice ignores that revision. The checker accepts the old RESULT without the newly requested proof, even with `PRECHECK_REQUIRED=1`; moving the same revise row before the RESULT correctly rejects it. Require a RESULT newer than the latest revise request, and cover this ordering in the acceptance control ([AGENTS.md:78](AGENTS.md#L78)).

- [P2] Separate home-path normalization from secret detection — scripts/orchestrator/result-precheck.sh:98-103
  The masker normalizes home paths as well as credentials, so treating every rewrite as a secret rejects legitimate public source changes. For example, touching `scripts/validate-agent-assets.py` makes the pre-push scan reject its existing documentation and home-path examples: they produce 17 rewrites despite having no `SECRET_PATTERN` matches. The existing validator prohibits home paths only inside `.orchestration`, whereas this hook scans every changed blob. Preserve that scope or separate credential detection from evidence normalization.
2026-10-18T13:44:14.714987Z ERROR codex_models_manager::manager: failed to refresh available models: request timed out
Reviewed the original 4ed1b27a head against the supplied base because the shared worktree moved during review. Reproductions confirmed a secret-scan bypass, stale revision acceptance, and false-positive push blocking; full tests were not run in the read-only sandbox.

Full review comments:

- [P1] Scan blobs separately to preserve JSON secret detection — .githooks/pre-push:27-31
  When multiple blobs are concatenated, the scan input is usually no longer valid JSON. The masker consequently falls back to raw-text matching and misses credentials with JSON-escaped prefixes such as `\u0067hp_...`. I reproduced a detected credential becoming zero matches after appending a clean JSON blob. Scan blobs independently to preserve per-file JSON decoding, and cover this bypass in the declared closed control ([AGENTS.md:78](AGENTS.md#L78)).

- [P2] Reject results that precede the latest revision request — scripts/orchestrator/dispatch.sh:174-176
  When a `status=revise ... check=...` ACCEPTANCE follows the last ready RESULT, this slice ignores that revision. The checker accepts the old RESULT without the newly requested proof, even with `PRECHECK_REQUIRED=1`; moving the same revise row before the RESULT correctly rejects it. Require a RESULT newer than the latest revise request, and cover this ordering in the acceptance control ([AGENTS.md:78](AGENTS.md#L78)).

- [P2] Separate home-path normalization from secret detection — scripts/orchestrator/result-precheck.sh:98-103
  The masker normalizes home paths as well as credentials, so treating every rewrite as a secret rejects legitimate public source changes. For example, touching `scripts/validate-agent-assets.py` makes the pre-push scan reject its existing documentation and home-path examples: they produce 17 rewrites despite having no `SECRET_PATTERN` matches. The existing validator prohibits home paths only inside `.orchestration`, whereas this hook scans every changed blob. Preserve that scope or separate credential detection from evidence normalization.
```
