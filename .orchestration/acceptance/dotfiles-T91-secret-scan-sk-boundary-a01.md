# Acceptance: dotfiles-T91-secret-scan-sk-boundary-a01

- **Decision:** ACCEPTED after three revise rounds. PR #245 squash-merged to `main` as `312fef3f` (final head `1af78d7900ef3c42af182bfcfb6ac7bd3371a9b8`; substantive commits 35d102b7, 0bdf99f7, 5fa6f090, 9544155f, 185edb2b, ffddc8a7, 2e26ca08; base 57885db1, update-branch merges onto a5c30b6d, 138e6a72, 8922f13b, 06875e4e). Merged without `--delete-branch`; worker-c holds `fix/secret-scan-sk-boundary`.
- **Worker:** `claude-standard-dot-a005` (worker-c). task_rev chain (dispatch `9ac39529…`, revise 1 `765a7d18…`, revise 2, revise 3) matched. Parallel wave with T88/T68 (a006) and T65 (a007); a005 also ran T74 between rounds.
- **Exemption declared:** acceptance and final integration; the orchestrator mutated no repository code. Bookkeeping edits: two lines of the T91 task file reworded and the orchestrator's own evidence masked so `.orchestration` scans clean.
- **Plan reference:** boundary-commit blocker (secret-scan false positive on hyphenated slugs), outside the numbered phases.

## What was accepted (`scripts/validate-agent-assets.py` SECRET_PATTERN + tests)

- Key prefixes `ghp_`, `github_pat_`, `sk-` start after a non-word character or the start, or after any backslash escape of 1-9 letters or digits (`\n`, `\u000a`, `\U0000000A`, `\x0a`), expressed as zero-width lookbehinds so `--mask-secrets` keeps the escape and masked JSON stays valid.
- The `sk-` body must hold a run of 20+ hyphen-free key characters within its first 64: every real key shape still matches, hyphenated task slugs (`…-secret-scan-sk-boundary-a01-review-receipt.md`) do not, and the bounded lookahead keeps the scan linear (64 KB of `-sk-a`: 8.1 s → 0.024 s).
- Assignment-form alternatives unchanged. Seven new test groups, each failing on its parent commit.

## Decisions taken during the rounds

- Round 1: `\b` missed keys after JSON-escaped whitespace (audit of 35d102b7); fixed, then generalized to every escape spelling after the Bot enumerated `\uXXXX` and `\U`; zero-width form after the Bot showed masking broke JSON.
- Round 2: the standalone `-sk-<slug>` false positive (this task's own id) is removed by the key-body rule; the two contradictory Bot P2s (loosen / tighten) are not-applicable, the rule sits between them by design.
- Round 3: the task-level audit of ffddc8a7 found the quadratic lookahead (fixed), NUL bytes in the validation file that made `read_scannable_text()` skip it (removed; `zsh echo` had turned `\u`/`\U` in headings into NUL), masked evidence (accepted deviation, stated in the validation header), and a stale thread table (reconciled).

## Orchestrator re-derivation

- Read every pattern revision and confirmed against the final pattern: the T67 receipt slug, the T75 report, the T65 audit evidence (`…-sk-boundary-a01-audit-1845139e.md`) and the T91 slugs are clean; `sk-proj-` and bare keys, also after `\n`, are flagged. A read-only scan of 2,087 `.orchestration` files finds no match and no NUL byte (auditor and orchestrator independently).
- Pre-T91 behaviour restored where it mattered: keys after escaped whitespace were flagged before 35d102b7 and are flagged again.

## Audit / Bot / sweep / gate

| scope | verdict |
|---|---|
| task-level, final head 1af78d79 | correct |
| task-level, ffddc8a7 | incorrect (5) → all corrected in 2e26ca08 or in the artifacts |
| per-commit 35d102b7 | incorrect (1) → fixed in 0bdf99f7/9544155f |

- Codex Bot: five threads (three fixed in-PR, two not-applicable), all replied and resolved; thumbs-up on 2e26ca08 and 1af78d79. Sweep (head 1af78d79): 24 items, 0 failure/warning, all dispositioned.
- Gate at 1af78d79 exit 0. Disclosure: the gate compares item bodies byte for byte, so its input was a verbatim-body copy of the dispositioned sweep; the saved evidence masks the Bot's key-shaped example in one item (see the receipt's `gate_input_note`). Follow-up dotfiles-T93 lets the gate compare masked bodies.

## Follow-ups

- dotfiles-T93 (gate compares feedback bodies after secret masking) after T68 merges; dotfiles-T71 (generator multi-target) now unblocked.
- `read_scannable_text()` skips any file with a NUL byte; the validator should fail on NUL in `.orchestration` text instead of skipping (candidate for T93 or T77).

## CompactionDB

- Worker decision `319df352-4d15-4ebd-8e74-20113096861a` (round 0 text) cited; amended below with the key-body rule.
