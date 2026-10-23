---
task: dotfiles-T133-result-precheck-a02
head: 9cd5514a790f6993136f5e74aaf3f3afa31b23d8
pr: 411
base: de3b73cc4f8874a30be6adc47a0f07575869d0df
started: 2026-10-18T11:03:41Z
finished: 2026-10-18T11:09:03Z
findings: 3
engine: codex review --base main (profile review, read-only)
---

- [P1] Decode or reject UTF-16 before scanning for secrets — scripts/orchestrator/result-precheck.sh:85-85
- [P1] Preserve blob boundaries in the secret-scan input — .githooks/pre-push:27-27
- [P2] Require an executed regression test for the previous-head proof — scripts/orchestrator/result-precheck.sh:250-252

```text
The secret guard has two reproducible bypasses, and selector evidence can claim a regression proof without executing the old test. Full subprocess tests were not run because the sandbox is read-only.

Full review comments:

- [P1] Preserve blob boundaries in the secret-scan input — .githooks/pre-push:27-27
  If one blob ends with a word character without a newline and the next starts with a GitHub token, concatenation produces `xghp_...`. The repository's token regex requires a non-word boundary, so the masker reports zero matches and permits the push. Scan blobs independently or insert a newline after every blob. Add this case to the claimed closed pre-push control ([AGENTS.md:78](AGENTS.md#L78)).

- [P1] Decode or reject UTF-16 before scanning for secrets — scripts/orchestrator/result-precheck.sh:85-85
  For a UTF-16LE or UTF-16BE credential file, replacing NUL bytes with newlines splits a token prefix into `g\nh\np\n_...`. The masker consequently reports zero matches and the hook permits the secret-bearing push. The repository's existing scanner supports UTF-16, but this normalization loses that protection. Decode supported encodings or fail closed, and cover this NUL-bearing case in the closed threat-table control ([AGENTS.md:78](AGENTS.md#L78)).

- [P2] Require an executed regression test for the previous-head proof — scripts/orchestrator/result-precheck.sh:250-252
  When a revision introduces the requested test, the untouched previous worktree either lacks its module or selects no tests. Any nonzero exit is nevertheless accepted as a red proof. The committed a01 evidence already records `previous_head_exit: 5`, `Ran 0 tests`, and `ok: true`. Run the new regression source against the previous production code and reject import, runner, and no-test failures instead of treating them as demonstrated regressions ([AGENTS.md:78](AGENTS.md#L78)).
The secret guard has two reproducible bypasses, and selector evidence can claim a regression proof without executing the old test. Full subprocess tests were not run because the sandbox is read-only.

Full review comments:

- [P1] Preserve blob boundaries in the secret-scan input — .githooks/pre-push:27-27
  If one blob ends with a word character without a newline and the next starts with a GitHub token, concatenation produces `xghp_...`. The repository's token regex requires a non-word boundary, so the masker reports zero matches and permits the push. Scan blobs independently or insert a newline after every blob. Add this case to the claimed closed pre-push control ([AGENTS.md:78](AGENTS.md#L78)).

- [P1] Decode or reject UTF-16 before scanning for secrets — scripts/orchestrator/result-precheck.sh:85-85
  For a UTF-16LE or UTF-16BE credential file, replacing NUL bytes with newlines splits a token prefix into `g\nh\np\n_...`. The masker consequently reports zero matches and the hook permits the secret-bearing push. The repository's existing scanner supports UTF-16, but this normalization loses that protection. Decode supported encodings or fail closed, and cover this NUL-bearing case in the closed threat-table control ([AGENTS.md:78](AGENTS.md#L78)).

- [P2] Require an executed regression test for the previous-head proof — scripts/orchestrator/result-precheck.sh:250-252
  When a revision introduces the requested test, the untouched previous worktree either lacks its module or selects no tests. Any nonzero exit is nevertheless accepted as a red proof. The committed a01 evidence already records `previous_head_exit: 5`, `Ran 0 tests`, and `ok: true`. Run the new regression source against the previous production code and reject import, runner, and no-test failures instead of treating them as demonstrated regressions ([AGENTS.md:78](AGENTS.md#L78)).
```
