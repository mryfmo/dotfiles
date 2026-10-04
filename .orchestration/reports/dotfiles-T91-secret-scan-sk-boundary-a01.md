# Report: dotfiles-T91-secret-scan-sk-boundary-a01

- **Worker and branch:** `claude-standard-dot-a005` in worker-c, branch `fix/secret-scan-sk-boundary` from `origin/main` 57885db1.
- **task_rev:** `9ac39529…`, matched.
- **PR:** #245, https://github.com/mryfmo/dotfiles/pull/245.
- **Commit:** `35d102b7` (one commit).
- **Final head:** `d090ef7d`, after two `gh pr update-branch` merges: `ac25ee18` with main a5c30b6d (T66), then `d090ef7d` with main 138e6a72 (T75).
  - **CI:** green; 13 pass including CodeRabbit, and `nix` is skipped.
  - **`mergeable_state`:** `clean`.
  - **Branch:** up to date (behind_by=0).
  - **Codex:** 👍 on all three heads, with no threads.
  - **Tests:** 62 validator tests and 703 overall pass (fewer than before because main's T66 removed the permgate-lane tests).

## Change

1. **`SECRET_PATTERN`** (scripts/validate-agent-assets.py:27-29; only this literal changed):
   - The `ghp_`, `github_pat_` and `sk-` alternatives begin with `\b`. The four `key/password/secret/token` alternatives are unchanged.
   - Under `(?ix)`, `\b` sits between a non-word character (or the start) and the prefix's first letter.
   - In `task-level` the `s` follows the word character `a`, so there is no boundary and no match.
   - A key at line start, or after a space, a quote or `=`, has a boundary and still matches. That is verified by the snippet and by the new tests.
   - An `sk-` directly after a word character, for example `x_` plus `sk-…`, would no longer match. Such a token is a different identifier, not a key.
2. **`SecretPatternBoundaryTest`** in `tests/unit/test_validate_agent_assets.py`:
   - Two hyphenated slugs are clean.
   - An `sk-` sample after a space, inside quotes, at line start and after `KEY=` is flagged, and so is a `ghp_` sample after a space.
   - The samples are built at runtime (`"s" + "k-" + …`), following the file's existing rule that it never contains a literal match.
   - The slug case fails against the `origin/main` pattern.
   - Totals: 61 validator tests OK, `make unit-test` 728 OK, and `make validate-agent-assets` in the worktree exits 0.

## Objective 3, the main checkout's tree (read-only scan of every file under `.orchestration` with both patterns)

- The `origin/main` pattern flags five files: the T75 report, the T75 validation, the T67 review receipt, a T66 audit file, and the T91 task file.
- The branch pattern flags one file: **the T91 task file itself.** Its validation snippet contains literal key-shaped samples (an `sk-` key after a space, in quotes, and a `ghp_` key). A correct scan must flag those, and objective 1 requires that it does. So `make validate-agent-assets` in the main checkout will still fail on that one file until the task file's samples are rewritten without the literal shape or masked. That edit is the orchestrator's: editing `.orchestration` was forbidden to me.
- My own T91 artifacts carry no literal sample: the validation file's snippet output is masked with the branch's `--mask-secrets`, as stated in that file.

## Codex bot

👍 on `35d102b7`, `ac25ee18` and `d090ef7d`; there are no threads.

## CompactionDB

```
cd /home/moriya/Workspace/dotfiles && python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'dotfiles-T91 (operator 2026-10-04): the committed-secret scan anchors key prefixes (`ghp_`, `github_pat_`, `sk-`) at a word boundary so hyphenated slugs such as `…audit-task-level…` are not flagged; real keys after whitespace, quotes or at line start still are.'
319df352-4d15-4ebd-8e74-20113096861a
```

[memory:decision] dotfiles-T91 (operator 2026-10-04): the committed-secret scan anchors key prefixes (`ghp_`, `github_pat_`, `sk-`) at a word boundary so hyphenated slugs such as `…audit-task-level…` are not flagged; real keys after whitespace, quotes or at line start still are.

## Artifacts

- validation: `.orchestration/validation/dotfiles-T91-secret-scan-sk-boundary-a01.md`
- sandbox: `.orchestration/sandboxes/dotfiles-T91-secret-scan-sk-boundary-a01.md`
- learning: `.orchestration/learning/dotfiles-T91-secret-scan-sk-boundary-a01.md`
- autoskill: `.orchestration/autoskill/runs/dotfiles-T91-secret-scan-sk-boundary-a01.md`

cost: n/a (no subagents, no model-driven runs; the runtime does not expose session totals).

## Revise round 1 (task_rev `765a7d18…`): commit `0bdf99f7`

- **Audit P2 on `35d102b7`:** `\b` missed a key after JSON-escaped whitespace. In `json.dumps({"m": "\n" + key})` the character before the key is the `n` of `\n`, a word character. That is the shape of audit transcripts, so the scan passed and `--mask-secrets` left the key exposed.
- **Fix:** before each of `ghp_`, `github_pat_` and `sk-`, the pattern now requires `(?:(?<![A-Za-z0-9_])|(?<=\\[nrt]))`: a non-word character or the start, or an escaped `\n`, `\r` or `\t` right before the prefix.
- **Behaviour table** (validation file):
  - The JSON `\n`/`\t`/`\r` cases were flagged by the pre-T91 pattern (57885db1), missed by `35d102b7`, and are flagged again now. This restores the old behaviour rather than changing it.
  - The `task-level` slug stays clean (pre-T91 flagged it).
  - A key after a space still matches.
- **New test** `test_a_key_after_json_escaped_whitespace_is_flagged`: 3 prefixes × 3 escapes, keys built at runtime. It fails 9/9 against `35d102b7` and passes now.
- **Totals:** 704 unit tests OK, and `make validate-agent-assets` in the worktree exits 0.
- **Final head:** `0bdf99f7`, up to date with `main` 138e6a72. CI and the Bot state are in the validation file.

### Codex P2 4176019381 on `0bdf99f7`: `fixed:5fa6f090`

- **The gap:** JSON may encode whitespace as `\u000a`, `\u000d`, `\u0009` or ` ` (or as `\b` or `\f`). Those escapes end in a letter or digit, so the round-1 guard missed a key after them. The pre-T91 pattern caught it, which contradicts the round's "restore, not change" goal.
- **Fix:** the guard is now `(?:(?<![A-Za-z0-9_])|(?<=\\[bfnrt])|(?<=\\u[0-9A-Fa-f]{4}))`. It covers every JSON escape that ends in a word character. `\"`, `\/` and `\\` already end in a non-word character.
- **Behaviour table** (validation file): all six escapes are flagged as in pre-T91, both slugs stay clean, and a key after a space still matches.
- **Test:** the new subtests (6 escapes × 3 prefixes) fail 18 times against `0bdf99f7`. 704 tests OK and asset validation exits 0.
- **Commits:** this round has two fix commits (`0bdf99f7` and `5fa6f090`), because the Bot's review of the first exposed the remaining escape forms. Both serve the round's stated goal.
- **Final head:** `82738d93`, a merge of main 8922f13b (T74). CI and the Bot state are in the validation file.

### Codex P2 4176057502 on `82738d93`: `fixed:9544155f`, closed by construction

- **What the Bot found:** a third escape spelling, TOML's `\UXXXXXXXX`, that hid a key from the escape list.
- **Why I changed approach:** listing escape forms one at a time does not converge. YAML also has `\x`, `\0`, `\e`, `\N` and others.
- **New guard:** `(?:(?<![A-Za-z0-9_])|(?<=\\)[A-Za-z0-9]{1,9}?)`. The prefix starts after a non-word character or the start, or after any escape sequence: a backslash plus 1–9 letters or digits, which spans everything from `\n` to the 9-character `\U0000000A`.
- **Behaviour table** (validation file):
  - `\U0000000A`, `\x0a`, `\0`, `\u000a` and `\n` are all flagged, as they were before T91.
  - Both hyphenated slugs stay clean, because a slug has no backslash.
  - A key after a space still matches.
  - The one remaining false-positive shape is a backslash path segment directly before `…sk-` (e.g. `C:\notes\task-level-…`). Pre-T91 flagged it too.
- **Test:** the extended escape subtests (`\U`, `\x`, `\0` added) fail 9 times against `5fa6f090`. 703 tests OK and asset validation exits 0.
- **Scan:** the main checkout's `.orchestration` scan still flags only the T91 task file (its literal samples).
- **Proposal for any further Bot escape enumeration:** `not-applicable`, citing this general rule.
- **Commits:** this round now has three fix commits (`0bdf99f7`, `5fa6f090`, `9544155f`). The last one replaces the list with the general rule.

### Codex P2 4176116962 on `9544155f`: `fixed:185edb2b`

- **The problem:** the `9544155f` guard consumed the escape's letters. `--mask-secrets` then replaced, for example, `u000a` together with the key, leaving a lone backslash. Valid JSON evidence became invalid: `"x\<redacted…>"`.
- **Fix:** the guard is now nine zero-width lookbehinds, `(?<=\\[A-Za-z0-9]{n})` for n = 1–9, alongside the non-word lookbehind. The escape stays outside the match, and the mask yields `"x\u000a<redacted…>"`, which is valid JSON (the pre-T91 result).
- **Test:** `test_masking_keeps_the_escape_before_the_key` (`\n`, `\u000a`, `\U0000000A`) fails 3/3 against `9544155f`.
- **Behaviour:** detection is unchanged from `9544155f`: every escape form is flagged, the slugs stay clean, and a key after a space still matches. 704 tests OK and asset validation exits 0.

### Finding for the orchestrator (not changed; it needs a decision beyond this task's boundary scope)

- **The remaining false-positive shape:** a slug where `sk` is a standalone hyphen-separated word followed by 20 or more `[A-Za-z0-9_-]` characters. This task's own id does it: `…secret-scan-sk-boundary-a01-` plus `pr-feedback`, `audit-…` or `review-receipt`.
  - The character before `sk-` is `-`, a non-word character, so every pattern flags it: pre-T91, `\b`, and every T91 revision.
  - It is not a regression from T91, but it now blocks the boundary commit.
- **Evidence:** the main checkout's `.orchestration/validation/dotfiles-T65-agent-stop-gate-a01-audit-1845139e.md` (written 13:26 local) is flagged three times on `sk-boundary-a01-…` (validation file). The T91 task file is flagged as well.
- **Proposed fix (a key-body rule, not a boundary rule):** require a run of at least 20 key characters with no hyphen after the prefix, e.g. `sk-(?=[A-Za-z0-9_-]*[A-Za-z0-9_]{20})[A-Za-z0-9_-]{20,}`.
  - Real legacy keys (48 alphanumerics) and random base64url project keys always contain such a run.
  - Hyphenated slugs never do.
  - The same could apply to `github_pat_` and `ghp_`, whose bodies have no hyphens anyway.
- **Not implemented:** this changes what counts as a key body, beyond this round's "boundary" brief. I'm proposing it rather than adding another commit. Say the word and I'll do it as one commit with tests.

### Revise-1 final head `185edb2b`

- **CI:** green; 13 pass including CodeRabbit, and `nix` is skipped.
- **Branch:** up to date with `main` 8922f13b.
- **Codex:** 👍 at 04:32:53Z.
- **`mergeable_state`:** `blocked`, only by the unresolved Codex P2 threads, which are fixed in this round: 4176019381 `fixed:5fa6f090`, 4176057502 `fixed:9544155f`, 4176116962 `fixed:185edb2b`.
- **Fix commits in this round:** four (`0bdf99f7`, `5fa6f090`, `9544155f`, `185edb2b`), plus the `82738d93` update-branch merge.

## Revise round 2 (task_rev `ca9d9fb6…`): commit `ffddc8a7`

- **Rule:** the `sk-` body is now `sk-(?=[A-Za-z0-9_-]*[A-Za-z0-9_]{20})[A-Za-z0-9_-]{20,}`, so it needs a run of 20 or more hyphen-free key characters. The zero-width prefix guard is unchanged, so `--mask-secrets` still keeps escapes. `ghp_` and `github_pat_` are unchanged.
- **Test `test_an_sk_key_body_needs_a_hyphen_free_run`:**
  - Flagged: `sk-<24 alnum>`, `sk-proj-<24 alnum>`, and the project key inside JSON after `\n`.
  - Clean: `…-secret-scan-sk-boundary-a01-audit-1845139e.md`, `…-pr-feedback.json` and `…-review-receipt.md`. Samples are built at runtime.
  - The three slug subtests fail on the parent `185edb2b`.
  - Totals: 705 tests OK, and asset validation in the worktree exits 0.
- **Scan of the main checkout's `.orchestration`** (2072 text files): no key-prefix match remains, including the T65 audit file. One file is flagged: **the T91 task file, line 7**, where the prose that lists the four assignment alternatives (key, password, secret, token, each followed by an equals sign and a quoted value) matches the unchanged `token` assignment alternative. `origin/main` flags it as well.
  - The round's expected zero needs that one line reworded. It is the orchestrator's file, and this task says to leave those four alternatives unchanged.

### Codex on `ffddc8a7`: two P2s pulling in opposite directions, proposed not-applicable (no commit)

| Thread | Asks | Proposed disposition |
|---|---|---|
| 4176194976 "Preserve scanning of hyphenated opaque sk- key bodies" | flag `sk-proj-abcdefghij-abcdefghij-abcdefghij`, i.e. **loosen** the body rule | `not-applicable`. The round-2 decision adopted the hyphen-free-run rule. Real `sk-` keys (legacy 48 alphanumerics; `sk-proj-`/`sk-svcacct-`/`sk-admin-` followed by a long random body) always contain a run of 20 or more hyphen-free characters. The example is synthetic 10-character chunks, which is the same shape as a hyphenated slug, so loosening it reintroduces the boundary-commit false positive. |
| 4176194980 "Treat hyphen-delimited slug components as non-secret text" | clear a hyphenated name whose component after `-sk-` is 20 letters (the Bot example: a receipt name with `sk-` and a 20-letter component), i.e. **tighten** further | `not-applicable`. A 20-character random component after `sk-` is exactly what a key looks like. Clearing it would let a real key embedded in a hyphenated context through. The real repo slugs (task ids) have short components and are clean. |

The two findings contradict each other: no regex satisfies both. The adopted rule is the trade-off the orchestrator decided in round 2.

### Revise-2 final head `ffddc8a7`

- **CI:** green; 13 pass including CodeRabbit, and `nix` is skipped.
- **Branch:** up to date with `main` 8922f13b.
- **Codex:** the two P2s above.
- **`mergeable_state`:** `blocked`, only by unresolved Codex P2 threads:
  - the two new ones are proposed `not-applicable`;
  - the three earlier ones (fixed in `5fa6f090`, `9544155f`, `185edb2b`) are already resolved.

## Revise round 3 (task_rev `c6a530e9…`): commit `2e26ca08`, final thread state

1. **P2 quadratic rescanning, fixed in `2e26ca08`:** the `sk-` lookahead is bounded, `(?=[A-Za-z0-9_-]{0,64}[A-Za-z0-9_]{20})`.
   - 64 KB of repeated `-sk-a` takes 0.024 s, against 8.1 s on `ffddc8a7`. The new `test_a_long_hyphenated_run_scans_in_linear_time` bounds it at 1 s and fails (7.9 s) on the parent.
   - Key and slug detection is unchanged: `sk-`, `sk-proj-` and the JSON form are flagged, and the three slug forms are clean.
   - Totals: 706 tests OK, and asset validation in the worktree exits 0.
2. **P2 NUL bytes in the validation file, fixed in the artifact:** two section headings had been written with zsh `echo`, which turned the `\u`/`\U` text into NUL bytes. Both are restored, the file has no control bytes, and `read_scannable_text()` reads it (validation file).
3. **P2 masked evidence:** accepted deviation. It is now stated in the validation header.
4. **P3 thread state, reconciled:** all five Bot threads are resolved by the orchestrator.

| Thread | Head | Disposition |
|---|---|---|
| 4176019381 `\uXXXX` escapes | 0bdf99f7 | `fixed:5fa6f090` |
| 4176057502 TOML `\U` escapes | 82738d93 | `fixed:9544155f` |
| 4176116962 masking corrupts the JSON escape | 9544155f | `fixed:185edb2b` |
| 4176194976 hyphen-chunked `sk-proj` bodies | ffddc8a7 | `not-applicable` (round-2 rule) |
| 4176194980 hyphen-delimited slug components | ffddc8a7 | `not-applicable` (key-shaped by design) |

- **Scan of the main checkout's `.orchestration`:** through `read_scannable_text`, 2079 scannable files and **0 flagged**.
- **Final head:** `1af78d79`, which is `2e26ca08` plus the update-branch merge of main 06875e4e (T65).
  - **CI:** green; 13 pass including CodeRabbit.
  - **`mergeable_state`:** `clean`.
  - **Branch:** up to date.
  - **Codex:** 👍 on `2e26ca08` and on `1af78d79`, with no new threads.
  - **Tests:** 741 OK.
