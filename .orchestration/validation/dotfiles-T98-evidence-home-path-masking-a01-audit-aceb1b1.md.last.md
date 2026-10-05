- [P2] high specification `scripts/validate-agent-assets.py:1315` — The scan ignores the running user’s `$HOME`. With `HOME=/srv/operator`, evidence containing `/srv/operator/.ssh/id_ed25519` passes validation, although the masker detects it; the required boundary enforcement is incomplete.
- [P2] high implementation `scripts/validate-agent-assets.py:1290` — Repository-entry exclusions also exempt valid account names: `/home/dot_config/.ssh/id_ed25519` passes both masking and validation unchanged. The final Bot finding remains reproducible despite its “not applicable” disposition.
- [P2] high implementation `scripts/validate-agent-assets.py:1298` — Restricting root-home matches to hidden children leaves ordinary home paths exposed. A non-root run accepts and preserves `~/Library/Keychains/login.keychain-db`; protecting Codex agent identifiers does not justify excluding these filesystem paths.
- [P2] high evidence-reality `.orchestration/reports/dotfiles-T98-evidence-home-path-masking-a01.md:95` — “I fixed every finding” contradicts the supplied feedback: final-head finding `4181459798` was resolved without a fix. Update the report to distinguish eight fixed findings from this remaining limitation.
- [P3] high evidence-reality `.orchestration/validation/dotfiles-T98-evidence-home-path-masking-a01.md:5387` — The earlier validation capture was overwritten and replaced with a narrated count, contrary to the required verbatim evidence and line 8’s completeness claim.

Verified: all changed files are allowed, all expected artifacts exist, and all 749 evidence rewrites match the transformation. Credential detection is unchanged. The supplied [PR #276](https://github.com/mryfmo/dotfiles/pull/276) snapshot records 12 successful CI checks and resolved threads. Two existing pure masking tests passed; live GitHub access was unavailable.

📝 まとめ: Read-only audit completed; masking gaps and evidence corrections remain.

Verdict: incorrect