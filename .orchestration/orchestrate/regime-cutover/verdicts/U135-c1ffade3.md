## Findings

- P1 (high) [f1 s6] scripts/orchestrator/checkout-guard.sh:460: U129-4405a071 P1 :415 persists when checkout/.git points to storage/.git: the inferred checkout is storage, so linked commits and update-ref miss the actual store and succeed despite the closed threat row.
- P3 (high) [f1 s1] scripts/orchestrator/checkout-guard.sh:337: Any nonempty ref: suffix is accepted, including a tab or refs/heads/a..b; malformed symbolic values therefore exit 0 instead of receiving the promised value refusal.

## Reproduced

- Git inspection confirmed the requested head, six changed files, a clean tree, and no diff whitespace errors; Homebrew Git replaced the broken macOS launcher.
- ShellCheck, shfmt, and bash -n passed for the changed guard scripts.
- Initial unittest execution failed because the sandbox blocks the system Perl library used by shasum.
- All 54 checkout-guard, regime-init, lever-self-check, and scratch-git tests passed with scratch TMPDIR propagated and a Python SHA-256 shim.
- Four head tests replayed against base dc4491ed reproduced eight assertion failures across three selectors; the staged-mktemp selector passed, matching the reported red proof.
- With checkout/.git symlinked to storage/.git, installation succeeded and a linked-worktree commit succeeded and moved its branch.
- The same layout refused a main-checkout commit with the worker route, but linked-worktree update-ref succeeded and moved its branch off origin.
- Direct prepared-hook inputs containing ref: followed by a tab or refs/heads/a..b returned 0; git check-ref-format rejected both targets.
- Source and installed guard bytes matched, and their SHA-256 matched both changed hash records.
- Masked-dirname and git-invocation checks were blocked by sandbox-denied shell temporary files; an embedded-code replay encountered the same limitation in the version helper.
- Final git status remained clean and diff --check passed.

## Notes

Both findings concern synthetic edge cases without prior real repository occurrence; weights 6 and 1 are filed below the blocking threshold. CI was unavailable offline. The full generator check was not run because PyYAML was unavailable.

Blocking: 0
Filed: 2
Verdict: correct
