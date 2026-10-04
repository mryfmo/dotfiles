# AGMSG-TASK dotfiles-T91-secret-scan-sk-boundary-a01

Drafted 2026-10-04 by the orchestrator seat. Blocker for the next `.orchestration` boundary commit: `make validate-agent-assets` fails on `.orchestration/validation/dotfiles-T67-audit-task-level-a01-review-receipt.md` and on `.orchestration/reports/dotfiles-T75-shell-dead-code-a01.md` with `possible committed secret`. Root cause (reproduced with `SECRET_PATTERN` from `scripts/validate-agent-assets.py:24`): the alternative `sk-[A-Za-z0-9_-]{20,}` under `(?ix)` matches inside the hyphenated slug `…audit-task-level-a01-review-receipt…`, so any long hyphenated token containing `sk-` is flagged as an OpenAI key.

## Objective

1. `scripts/validate-agent-assets.py` `SECRET_PATTERN`: anchor the key prefixes at a word boundary (`\b` before `ghp_`, `github_pat_` and `sk-`) so a prefix inside a hyphenated word no longer matches; keep the four assignment-form alternatives (api key, password, secret, token followed by a quoted value) as they are. Confirm `\b` is right for `sk-` (preceded by a non-word char or start) and that a real `sk-...` key at line start or after a space or quote still matches.
2. Tests: in `tests/unit/test_validate_agent_assets.py` (or where `validate_no_obvious_secrets`/`SECRET_PATTERN` is tested) add cases: the slug `dotfiles-T67-audit-task-level-a01-review-receipt.md` is clean; `sk-` + 24 alphanumerics after a space, a quote and at line start is flagged; `ghp_` + 24 after a space is flagged.
3. `make validate-agent-assets` in the main checkout must pass on the current `.orchestration` tree (the orchestrator re-runs it at acceptance).

[memory:decision] dotfiles-T91 (operator 2026-10-04): the committed-secret scan anchors key prefixes (`ghp_`, `github_pat_`, `sk-`) at a word boundary so hyphenated slugs such as `…audit-task-level…` are not flagged; real keys after whitespace, quotes or at line start still are.

## Repo / branch

- Work ONLY in your own worktree (worker-c for a005). `git fetch origin`; `git switch -c fix/secret-scan-sk-boundary origin/main` (57885db1 or later). Verify the dispatched task_rev; else stop and PONG blocked.
- Strict status checks: if `main` moves, `gh pr update-branch <pr>` and wait for CI again before RESULT.

## Allowed files

- `scripts/validate-agent-assets.py` (the `SECRET_PATTERN` literal only), the validator's unit test file
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dotfiles-T91-secret-scan-sk-boundary-a01.md` (main checkout)

## Forbidden actions

- Any other validator change; masking or editing `.orchestration` evidence; `make update`/`make apply`; local bats; merging; force push; pushing `main`.

## Validation commands (paste verbatim output)

```
git diff origin/main --stat
uv run python -m unittest tests.unit.test_validate_agent_assets 2>&1 | tail -3
python3 - <<'PY'
import re,importlib.util
s=importlib.util.spec_from_file_location('va','scripts/validate-agent-assets.py'); m=importlib.util.module_from_spec(s)
try: s.loader.exec_module(m)
except SystemExit: pass
k='abcdefghijklmnopqrstuvwx'
for t in ['dotfiles-T67-audit-task-level-a01-review-receipt.md','x s'+'k-'+k,'"s'+'k-'+k+'"','gh'+'p_'+k]:  # samples built at runtime so this file never holds a key-shaped literal
    print(repr(t), bool(m.SECRET_PATTERN.search(t)))
PY
make unit-test
make validate-agent-assets        # in the worktree; the orchestrator re-runs it in the main checkout
gh pr checks <pr-number>
gh api repos/mryfmo/dotfiles/pulls/<pr-number> --jq '.mergeable_state'
```

## Completion

1. PR to `main`, English title/description ending with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. CI green on the final head, branch up to date.
2. After the final push: `gh pr checks <pr> --watch`; wait (≤15 min) for the Codex Bot review of that head; fix P0/P1 inline findings and repeat; do not resolve threads.
3. Artifacts at the exact expected paths; validation with verbatim outputs, PR number, head SHA.
4. CompactionDB `memory add --kind decision --scope project` with the `[memory:decision]` text from the main checkout; paste command and output.
5. `AGMSG-RESULT v1` via `agmsg-dispatch dotfiles <your identity> claude-remediation-dot wT:p1 "<single line>"` (outside the sandbox). `cost:` line. max_turns=20.

## Orchestrator note (2026-10-04)

- The validation snippet above originally held literal key-shaped samples, which the corrected scan rightly flags; they are now built at runtime so this task file passes `make validate-agent-assets` (the worker's objective-3 finding).

## Revise round 1 (orchestrator, 2026-10-04 04:20Z) — audit finding on 35d102b7

The task-level audit of 35d102b7 is `incorrect` with one P2: `\b` misses a genuine key that follows JSON-escaped whitespace. In `json.dumps({"m": "\n" + key})` the character before `sk-` is the word character `n` of `\n`, so the scanner accepts the content and `--mask-secrets` leaves the key exposed. That shape is exactly what the audit evidence files hold (JSON-encoded transcripts), so it must be fixed at the root, not accepted.

1. Replace `\b` before the three prefixes with `(?:(?<![A-Za-z0-9_])|(?<=\\[nrt]))` (in the raw verbose pattern: a non-word character or start before the prefix, or an escaped `\n`/`\r`/`\t` sequence immediately before it). `…task-level…` stays clean (the `a` before `sk` is a word character and not an escape), `\nsk-…`, `\tghp_…`, `\rgithub_pat_…` are flagged again, and a key after a space, a quote, `=` or at line start keeps matching.
2. Tests in `SecretPatternBoundaryTest`: for each of the three prefixes, `json.dumps({"m": "\n" + key})` is flagged; a sample built with `"\t"` is flagged; the two hyphenated slugs stay clean; samples remain built at runtime. Run the new JSON case against the `origin/main` pattern of 35d102b7's parent to confirm it also matched there (the regression must restore, not change, that behaviour).
3. One commit on `fix/secret-scan-sk-boundary`; then `gh pr update-branch 245` if `main` moved, CI, the Codex Bot on the final head (by listing its reviews), and a RESULT naming the fix commit and the final head. Do this before continuing T74's post-push wait if T74 is only waiting on CI/Bot.

## Revise round 2 (orchestrator, 2026-10-04 06:10Z) — the standalone hyphenated slug

Decision: implement the key-body rule you proposed, in one commit with tests. A `-sk-<slug>` such as this task's own id (`secret-scan-sk-boundary-a01-audit-…`) is a real false positive that blocks the boundary commit (it flags the T65 audit evidence three times), and the rule is sound: every real key has a run of at least 20 hyphen-free key characters (an OpenAI `sk-proj-…` key has one after `proj-`), a slug never does.

1. For the `sk-` alternative only: `sk-(?=[A-Za-z0-9_-]*[A-Za-z0-9_]{20})[A-Za-z0-9_-]{20,}` (keep the prefix guard and the zero-width form so `--mask-secrets` still works). `ghp_`/`github_pat_` bodies have no hyphens and stay as they are.
2. Tests: a key shaped `sk-proj-<24 alnum>` and a bare `sk-<24 alnum>` are flagged (also inside JSON after `\n`); `secret-scan-sk-boundary-a01-audit-1845139e.md`, `…-sk-boundary-a01-pr-feedback.json` and `…-review-receipt.md` are clean; the pre-round pattern flags the slug (so the test fails on its parent). Samples built at runtime.
3. Paste a read-only scan of the main checkout's `.orchestration` with the new pattern (expected: zero files); then CI, the Bot on the final head (paginated listing), RESULT with every thread's disposition.

## Revise round 3 (orchestrator, 2026-10-04 07:40Z) — task-level audit of ffddc8a7 is `incorrect`

Findings (`.orchestration/validation/dotfiles-T91-secret-scan-sk-boundary-a01-audit-ffddc8a.md.last.md`) and dispositions:

1. **P2, quadratic rescanning.** `(?=[A-Za-z0-9_-]*[A-Za-z0-9_]{20})` makes each `sk-` position scan to the end of a long hyphenated run (64 KB → 3.7 s). Bound the lookahead: `(?=[A-Za-z0-9_-]{0,64}[A-Za-z0-9_]{20})`. A real key's 20-run begins within a few characters (`sk-proj-` is 5), so detection is unchanged. Test: a 64 KB text of repeated `-sk-a` completes a `search` in well under a second (generous bound, no flakiness), and the existing key/slug cases still hold.
2. **P2, NUL bytes in the validation artifact** (lines ~145 and ~181) make `read_scannable_text()` skip the whole file, so its secret check is bypassed. Remove the NUL bytes (render them as `\0` or `^@`), say where they came from, and confirm the file is scanned (`--mask-secrets` dry run or the scan listing it).
3. **P2, masked validation evidence.** Accepted deviation, recorded by the orchestrator: verbatim output would put key-shaped literals back into tracked evidence that the scan must flag by design; `--mask-secrets` is the repository's own tool for evidence (herdr-agents audits use it). State that in the validation header; no further change.
4. **P3, report vs feedback JSON.** Reconcile the report's thread section with the final state: all five Bot threads resolved by the orchestrator with the dispositions listed there; final head named.
5. The receipt-name example quoted inside the orchestrator's `-pr-feedback.json` (a Bot thread body) matches the pattern by construction; the orchestrator masks it with the PR head's `--mask-secrets`. Not yours.

One commit for item 1; artifact edits for items 2-4; CI; Bot (paginated listing); RESULT with the fix sha and final head. The task-level audit is re-run on the new head.
