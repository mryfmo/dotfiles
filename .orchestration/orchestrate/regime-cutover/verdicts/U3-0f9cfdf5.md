# U3 verdict (round 2): PR #458 head 0f9cfdf5ff5b5e02431690f1d0b11cd86363c2a8

Verifier: fresh context, read-only, worktree `~/Workspace/dotfiles/.claude/worktrees/agent-ae2bb242b04adcb5c` at 0f9cfdf5 (detached). No edits to the PR branch. Date 2026-10-23. Previous verdict: `U3-5b17ae6a.md` (F1-F7). Written in the worktree because the harness refused the main-checkout path.

## What ran

- `git fetch origin feat/openai-siwc-extension main`; `git checkout -q 0f9cfdf5…`; `git rev-parse HEAD` = `0f9cfdf5ff5b5e02431690f1d0b11cd86363c2a8`; `git merge-base origin/main HEAD` = `d06d94fd…`; `origin/main` = `6f154b60…` (main moved by U5/U6 since the branch base). `git merge-tree --write-tree origin/main 0f9cfdf5` exit 0 (no conflict); main's new files (`home/dot_agents/omp/policies/**`, `scripts/orchestrator/**`, `tests/**`) do not overlap the PR.
- `git diff --stat 5b17ae6a..0f9cfdf5`: 10 files, 204 insertions, 91 deletions (`docs/openai-siwc.md` 65, `README.md` 27, `src/index.ts` 39, `src/oauth.ts` 29, `src/requests.ts` 7, `tests/fake-auth-server.ts` 1, `tests/index.test.ts` 25, `tests/oauth.test.ts` 14, `tests/requests.test.ts` 69, `tsconfig.json` 19 new). `git diff --stat origin/main...0f9cfdf5`: 13 files, 1242 insertions, 0 deletions. All inside the brief's SCOPE. Both diffs read in full.
- `bun test` in `home/dot_agents/omp/extensions/openai-siwc`:

```
bun test v1.4.3 (c6da4a4d3)

tests/oauth.test.ts:
SKIP loopback bind test: this sandbox refuses binding 127.0.0.1

 21 pass
 1 skip
 0 fail
 201 expect() calls
Ran 22 tests across 4 files. [156.00ms]
```

- Load dry-run, package copied to `/tmp/claude-501/u3v2-pkg`, run through a 3-line wrapper (`/tmp/claude-501/u3v2-dryrun.sh`) that exports `HOME=/tmp/claude-501/u3v2-home` and execs `perl -e 'alarm 90; exec @ARGV' omp --no-extensions -e /tmp/claude-501/u3v2-pkg --no-session --model openai-siwc/gpt-6.1-sol --max-time 60 -p hi`:

```
run A (plain), exit=1, last lines:
error: No API key found for openai-siwc.

Use /login, set an API key environment variable, or create /tmp/claude-501/u3v2-home/.omp/agent/agent.db
      at #ui (~/.local/lib/node_modules/@oh-my-pi/pi-coding-agent/dist/cli.js:28772:105)
      at async #mo (~/.local/lib/node_modules/@oh-my-pi/pi-coding-agent/dist/cli.js:28766:41882)

run B (PI_OPENAI_STATEFUL=1), exit=1, line 1:
Failed to load extension /tmp/claude-501/u3v2-pkg/src/index.ts: Failed to load extension: openai-siwc: PI_OPENAI_STATEFUL is set; SIWC needs full history in `input…

run C (--model openai-siwc/no-such-model), exit=1, line 1:
Model "openai-siwc/no-such-model" not found
```

  Run A has no `Failed to load extension` line (`/usr/bin/grep` over the 14-line log). Scratch HOME after run A: `.omp/agent/agent.db` (0600), `models.db`, `cache/`, `logs/omp.2026-10-23.9863.log`, `run/`. The omp log's last line is the fatal `No API key found for openai-siwc.` naming the registered provider; omp prints no explicit "extension loaded" line. The real `~/.omp` was not touched (the sandbox write-denies it, and HOME pointed at the scratch dir). omp's own startup tried `hyper.charm.land`, `catalog.stencil.so` and five other catalog hosts, which the sandbox denied; that is omp's built-in model discovery for other providers, not the extension (the extension registers no `fetchDynamicModels`, `tests/index.test.ts:41`).
- First attempt with the brief's `PI_CONFIG_DIR=/tmp/claude-501/u3v2-home/.omp` form failed before load:

```
EPERM: operation not permitted, mkdir '~/tmp'
      at mkdirSync (unknown:1:1)
      at open (~/.local/lib/node_modules/@oh-my-pi/pi-coding-agent/dist/cli.js:16783:130)
```

  `PI_CONFIG_DIR` is a name joined under `os.homedir()` (`pi-utils/src/dirs.ts:116` `path.join(os.homedir(), getConfigDirName())`, `:308` `process.env.PI_CONFIG_DIR || CONFIG_DIR_NAME`), so an absolute value lands under the real `$HOME` (see N1). No stray `~/tmp` or `~/private` exists now (`ls`: No such file or directory).
- Bun bind probe in this sandbox: `Bun.serve({hostname:"127.0.0.1",port:0,…})` → `code=EADDRINUSE msg=Failed to start server. Is port 0 in use?` (F4's skip condition is real).
- `which tsc` → `tsc not found` (F6's shortcut premise holds).
- Secrets: `/usr/bin/grep -E` over the added lines of `git diff 5b17ae6a..0f9cfdf5` for `sk-…`, `eyJ…`, `Bearer …`, `oaiapp_…`, `ghp_…`, `github_pat_`, `AKIA…`, `-----BEGIN`, `password`, `secret`, `console.*`, `~`: no hits (exit 1). `shortcut:` markers: `README.md:30`, `tests/requests.test.ts:180`.
- Commit trailers (`git log --format=%B -2 0f9cfdf5`): `0f9cfdf5` `style(omp): prettier format for docs/openai-siwc.md` and `53fba133` `fix(omp): openai-siwc verifier round (U3b)` both end with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`; `53fba133` also carries `Program-Unit: regime-cutover/U3`. `5b17ae6a` still carries the Opus trailer (history not rewritten, as the brief ordered).
- PR (`gh pr view 458 --json`): draft, base `main`, `headRefOid` = `0f9cfdf5…`, title `feat(omp): openai-siwc provider extension (design + skeleton)`, body English, contains the line `Program-Unit: regime-cutover/U3` and ends with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`.
- `perl -e 'alarm 60; exec @ARGV' gh pr checks 458` (exit 1, pending jobs):

```
regime	fail	14s	https://github.com/mryfmo/dotfiles/actions/runs/39891710111/job/120212767938
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/39891711672/job/120213172578
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/39891711672/job/120213172949
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/39891711672/job/120213172717
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/39891711586/job/120212771723
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/39891711586/job/120212771580
validate	pass	2m49s	https://github.com/mryfmo/dotfiles/actions/runs/39891711643/job/120212771540
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/39891711586/job/120212771661
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/39891711586/job/120212771441
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
GitGuardian Security Checks	pass	0	https://dashboard.gitguardian.com
```

  `regime` red is expected (standing order 17, U13). The seven required checks were still pending at verification time; standing order 15 makes their green the coordinator's landing gate, not this verdict's.

## F1-F7 status

| id | Status | Evidence |
| --- | --- | --- |
| F1 | Fixed | Hunk `@@ -6,25 +6,38 @@` in `src/index.ts`: `src/index.ts:38-40` `if (TRUTHY.has(process.env.PI_OPENAI_STATEFUL ?? "")) throw new Error("openai-siwc: PI_OPENAI_STATEFUL is set; …")` runs before `pi.registerProvider` at `:41`. The `TRUTHY` set (`:10`, nine values) equals omp's `parseFlag` dict exactly (`pi-utils/src/env.ts:472-482`; `:483-486` `return TRUTHY[value] === true`, no trim or case fold), so load and `$flag("PI_OPENAI_STATEFUL", …)` (`openai-responses.ts:567`) read the flag the same way. A profile `.env` is applied when `@oh-my-pi/pi-utils/env` is imported (`src/cli/flag-tables.ts:24`, `src/cli/profile-bootstrap.ts:5`), before extensions load, so the guard sees it. Dry-run B pasted above. Doc row reworded at `docs/openai-siwc.md:112` with the runner citations; `src/requests.ts:43-45` comment says the throw only reports. Test `tests/index.test.ts:16-29` (four truthy values throw, `"0"` loads). |
| F2 | Fixed for new commits | Both new commits carry the Fable trailer (pasted above). `5b17ae6a` keeps the Opus trailer; the squash body at `gh pr merge --squash` is the coordinator's step (row F2 below). |
| F3 | Program-level, unchanged | PR body carries `Program-Unit: regime-cutover/U3`; `regime` stays red until U13 lands and the branch is updated (standing order 17). |
| F4 | Fixed | Hunk `@@ -125,12 +131,16 @@` in `tests/oauth.test.ts`: `:136-146` catches only `EPERM`, `EACCES`, `EADDRINUSE` and rethrows anything else. `EADDRINUSE` on port 0 is what this sandbox's Bun 1.4.3 reports (probe pasted above), and port 0 cannot genuinely be in use. |
| F5 | Fixed | Hunk `@@ -93,15 +93,19 @@` in `src/oauth.ts`: `refreshToken(credentials, signal?)` at `:96` passes `signal` to `postToken` (`:201`), which races it with the 15 s timeout via `AbortSignal.any` (`:202`, `:208`). Matches `pi-ai/src/registry/oauth/types.ts:115` `refreshToken?(credentials, signal?)`. Test `tests/oauth.test.ts:98-102`: a pre-aborted signal rejects with the abort reason and the fake server records no refresh request (`tests/fake-auth-server.ts:63` honours `signal`). |
| F6 | Fixed | `tsconfig.json` (new, `paths` for `@oh-my-pi/pi-coding-agent` and `@oh-my-pi/*` relative to the applied copy `~/.agents/omp/extensions/openai-siwc`; four `../` reach `$HOME`). `README.md:30` `shortcut: no type check runs, because tsc is not installed …; run bunx tsc --noEmit … once …` (limit and upgrade point, order 8). `tsc not found` here too. The README's dry-run column now describes a real run (see N1 for its wording). |
| F7 | Fixed | Hunk `@@ -96,40 +96,40 @@` in `docs/openai-siwc.md`: the developer-role row (`:107`) cites `openai-responses.ts:1779-1782`. |

## Acceptance 1-6 (U3b brief)

| # | Result | Evidence |
| --- | --- | --- |
| 1 F1-F7, `bun test` ≥ 18 | Met | Table above; 21 pass / 1 skip (EADDRINUSE, the allowed sandbox code). |
| 2 load dry-run | Met | Runs A-C pasted; the scratch `~/.omp/logs` line is the fatal `No API key found for openai-siwc.` (omp logs no load line). |
| 3 model ids | Met | `src/index.ts:29-32` `gpt-6.1-sol` and `gpt-6-astra` (name says "unverified"); `docs/openai-siwc.md:157` flags the assumption (【仮定】); no `fetchDynamicModels` (`tests/index.test.ts:41`). |
| 4 error mapping | Met for 403, documented residual for 429 (N2) | `tests/requests.test.ts:165-171`: fake 403 `subscription_sharing_usage_unavailable` → 1 request, `error` event, `AIError.retriable` false. `:173-183`: fake 429 `subscription_sharing_usage_limit_exceeded` → `Flag.UsageLimit`, `isProviderRetryableError` false, 6 requests pinned under a `shortcut:`. Citations verified: `openai-http.ts:33` `DEFAULT_MAX_ATTEMPTS = 6`, `:101-107` `fetchWithRetry(… maxAttempts: init.maxAttempts ?? DEFAULT_MAX_ATTEMPTS …)`; `fetch-retry.ts:375-382` retries any retryable status unless `shouldRetryResponse` refuses or the retry hint exceeds `maxDelayMs` (`:320` 60 000 ms); `retryable.ts:20-22`, `:44-49`; `rate-limit.ts:337` `usage.?limit`; `openai-responses.ts:903-905` `shouldRetryResponse` built from `lastSubmittedRequestWasFullReplay`; `types.ts:716-723` `fetch?: FetchImpl`. Independently: `/usr/bin/grep -n maxAttempts openai-responses.ts` → no hits, and `/usr/bin/grep -n "fetch:" src/sdk.ts src/session/agent-session.ts` → no hits, so neither a provider config nor the session reaches the attempt count or the transport `fetch` on the built-in api. |
| 5 README G2 steps | Met | `README.md:11-16`: four steps per profile (`audit`, `audit-r2`, `security`) with `What you see`, `source` and `dry-run` columns; registration record and token locations cited (`pi-utils/src/dirs.ts:312-315` verified: `profiles/<profile>/agent`). |
| 6 PR | Met | Draft, head `0f9cfdf5`, `Program-Unit` line, English, footer; `gh pr checks` pasted. |

## Findings

| id | P | file:line | one line | proposed fix |
| --- | --- | --- | --- | --- |
| F2 | P3 | commit `5b17ae6a` trailer | The first commit still carries `Co-Authored-By: Claude Opus 5.5`; the two U3b commits carry Fable. History rewrite is forbidden, so this closes only at merge. | Coordinator passes a squash body ending in `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>` at `gh pr merge --squash --match-head-commit <sha>`. |
| N1 | P3 | `home/dot_agents/omp/extensions/openai-siwc/README.md:11` (step 1 `dry-run` cell), PR body "Load dry-run" paragraph | The worker's dry-run used `PI_CONFIG_DIR=<absolute $TMPDIR path>`, but omp joins that value under `os.homedir()` (`pi-utils/src/dirs.ts:116`, `:308`; my run tried `mkdir ~/tmp`, pasted above), so that run's config root sat under the real `$HOME`, not a scratch HOME as standing order 4 requires, and the cell's "Scratch config root" overstates the isolation. The `HOME=<scratch>` form works when exported inside a wrapper script (runs A-C). No stray directory remains. | Reword the cell and PR paragraph to `HOME=<scratch>` (the wrapper-script form), or state that `PI_CONFIG_DIR` is relative to `$HOME`. Wording only, no code change. |
| N2 | P3 | `home/dot_agents/omp/extensions/openai-siwc/tests/requests.test.ts:180-182`, `docs/openai-siwc.md:128` | A 429 `subscription_sharing_usage_limit_exceeded` still costs 6 transport requests before omp's usage-limit recovery sees it. Acceptable as a documented residual, not P2: every resend is refused and spends nothing; no extension hook reaches `maxAttempts` or the transport `fetch` on the built-in api (verified above); a real `retry-after` above 60 s would stop the retry at `fetch-retry.ts:380`, and the real status is unmeasured until G2 (the test forces `retry-after: 0`, the worst case). The pinned count is a deliberate tripwire for an omp release that adds a gate. The "about 15 s" default-backoff figure in the doc is the worker's; I did not measure it. | After G2 measures the wire shape: if it is a 429 without a long `retry-after`, open the custom-api shape (`docs/openai-siwc.md` Synthesis decision) or an upstream omp gate as its own unit; otherwise delete the sentence and keep the test. |

Counts: P0 0, P1 0, P2 0, P3 3.

Notes, not findings: the branch base is one squash behind `origin/main` (`d06d94fd` vs `6f154b60`), merge-tree clean, so `gh pr update-branch` is optional before landing. The required checks were pending at verification time; landing waits for their green (standing order 15). The test `expect(AIError.isProviderRetryableError(new Error(last?.error?.errorMessage)))` (`requests.test.ts:179`) classifies a message-only Error, which is weaker than the real error object, but the preceding `classifyMessage(last.error)` assertion covers the real path.

Principles applied: Prove It Works (every worker claim re-run here: `bun test`, three dry-runs, the Bun bind probe, `which tsc`, the omp source citations, the merge-tree), Fix Root Causes (F1 is judged fixed because refusing load removes the illegitimate state instead of guarding the payload), Test Behavior, Not Implementation (the 429 test's pinned count is omp's internal behaviour, kept only because it is marked as a tripwire shortcut).

Not checked: the GitHub Actions `regime` log body (host outside the allowed network; the cause is unchanged from round 1), `bunx tsc` (no `tsc`, `registry.npmjs.org` not allowed), the real `~/.omp` load (forbidden), and the default-backoff duration of the 429 storm.

Verdict: unit-test-verified
