# U3b openai-siwc: fix round + completion — brief

GOAL
Take PR #458 (`feat/openai-siwc-extension`, head 5b17ae6a) from design + skeleton to an extension that loads in omp 18.11.3, registers provider `openai-siwc`, and is ready for the operator's first `/login openai-siwc` (gate G2), with the verifier's findings fixed. No real OpenAI call and no login in this unit.

SCOPE
Exclusive worktree on the existing branch `feat/openai-siwc-extension` (fetch from origin; you are its only writer now). May write: `home/dot_agents/omp/extensions/openai-siwc/**`, `docs/openai-siwc.md`. Nothing else.

CONTEXT (read first)
- `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/briefs/U3-openai-siwc-design.md` (the original brief) and the worker's report: 17 pass / 1 skip; strip list with citations; open questions with defaults (send `ext_agent_host_id` on later sign-ins; accept a refresh response without `scope`; account claim optional; `gpt-6-astra` omitted; per-profile registration; usage-error wire shape not wired).
- `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/verdicts/U3-5b17ae6a.md` (verifier-failed): F1 P2 the `previous_response_id` throw in `src/requests.ts:51-55` is not a guard because omp's runner catches a `before_provider_request` throw (`src/extensibility/extensions/runner.ts:1590-1591`, `:1627-1632`, `:2121-2131`) and sends the unrewritten payload → refuse at load in `src/index.ts` when `PI_OPENAI_STATEFUL` is truthy and reword `docs/openai-siwc.md:112`; F2 P2 commit trailer must be `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>` (your new commits carry it; do not rewrite history); F3 P2 the `regime` CI check is being fixed by U13, add the line `Program-Unit: regime-cutover/U3` to the PR body; F4 P3 `tests/oauth.test.ts:128-136` skip probe too broad → skip only on `EPERM`/`EACCES` bind errors; F5 P3 `src/oauth.ts:96` pass the `signal` through `refreshToken(credentials, signal)` per `pi-ai/src/registry/oauth/types.ts:115`; F6 P3 no tsconfig → add a minimal `tsconfig.json` with `paths` to the installed omp packages (`~/.local/lib/node_modules/@oh-my-pi/pi-coding-agent/node_modules/@oh-my-pi/*`) and run `bunx tsc --noEmit` only if `tsc` is already installed (`which tsc`); otherwise a `shortcut:` comment in README; F7 P3 cite `openai-responses.ts:1779-1782`.
- Facts: `~/Workspace/dotfiles/.orchestration/validation/025-v13-facts-20261023.md` §3b (registerProvider, OAuthCredentials, callback flow), §4 (SIWC), `~/Workspace/dotfiles/.orchestration/validation/025-pilot-facts.md` (#S0 measured registration/token/inference; #G1..#G1-3 how the session path proves an extension loads: `omp -e <dir> --no-session --model <provider>/<id> -p …` prints `Failed to load extension …` on failure and a login/`No API key` message when the provider is registered but unauthenticated).
- Load dry-run form (U1 report §1-§2; copy the package to `$TMPDIR/u3b-pkg` first so the worktree guard does not interfere): `HOME=$TMPDIR/u3b-home perl -e 'alarm 120; exec @ARGV' omp --no-extensions -e $TMPDIR/u3b-pkg --no-session --model openai-siwc/gpt-6.1-sol --max-time 60 -p "hi"`; expected: no `Failed to load extension`, and a provider-side auth message (`/login openai-siwc` or `No API key`) instead of `No models matching`. Paste it. Also `omp --no-extensions -e $TMPDIR/u3b-pkg --no-session --max-time 30 -p "" 2>&1 | head` is not an instrument; use the session path.

ACCEPTANCE
1. F1-F7 fixed as above (F2 via new commits; F3 via the PR body line). Paste `bun test` (expect ≥ 18 pass, the loopback test either runs or skips only on EPERM/EACCES).
2. The load dry-run above shows the extension loaded and the provider registered (paste stderr/stdout and the matching `~/.omp/logs` line under the scratch HOME).
3. Model ids come from the manifest convention `openai-siwc/<id>` with `gpt-6.1-sol` (measured #S0) and `gpt-6-astra` (【仮定】, flagged in docs); `fetchDynamicModels` stays optional and off by default.
4. Error mapping: `subscription_sharing_usage_limit_exceeded` and `subscription_sharing_usage_unavailable` surface as non-retryable provider errors (test with a fake 429/403 body in the fake Responses server; omp's generic retry must not loop five times, cite the omp retry hook you use).
5. README: operator steps for G2 (`/login openai-siwc` in each of the three profiles, what the browser shows, where the registration record and tokens live, how to verify with one `-p` turn), each with a `source` column.
6. PR #458 updated (push), still draft is fine, body carries `Program-Unit: regime-cutover/U3`, English per STANDING 14; `gh pr checks 458` pasted (the `regime` check may stay red until U13 lands and the branch is updated; say so).

VERIFY
`bun test`; the load dry-run; `git diff --stat origin/main...HEAD`. Network: `api.github.com`, `github.com`, and `raw.githubusercontent.com` only.

TIMEBOX
75 minutes.

FORBIDDEN
No real OpenAI/ChatGPT calls, no login, no edits outside SCOPE, no history rewrite, no merge, no rebase.

REPORT
≤ 200 words: head sha, PR link, test summary, the load dry-run lines, F1-F7 status, deviations, what G2 needs from the operator.

STANDING
Read and obey `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` before any command.
