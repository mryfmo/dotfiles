# Codex token usage and ChatGPT-OAuth monthly projection (2026-10-05)

Source: `~/.codex/sessions/**/*.jsonl` (347 sessions with `token_count`, 2026-09-27 .. 2026-10-05, 8.3 days; the last `total_token_usage` of each session), the `rate_limits` field of those events (plan `team` with 5-hour windows until 2026-09-30, plan `pro` with 10080-minute weekly windows since), and GitHub (`chatgpt-codex-connector[bot]` reviews and quota comments on mryfmo/dotfiles). Roles by cwd: `codex exec` from the main checkout = auditor; `.claude/worktrees/*` = Codex worker seat; other cwds = other projects.

| role (period total) | sessions | total tokens | uncached input | cached input | output | per 30 days |
|---|---:|---:|---:|---:|---:|---:|
| dotfiles worker seats (worker-e, worker-sec; gpt-6-astra via `security` profile, one gpt-5.6-terra) | 5 | 275.5M | 4.4M | 270.3M | 0.68M | ≈ 996M |
| dotfiles auditor exec (gpt-6.1-sol before T96, gpt-6-astra after) | 241 | 149.3M | 18.2M | 129.7M | 1.45M | ≈ 540M |
| other projects (tpro-platform etc.) | 101 | 96.6M | 9.2M | 86.9M | 0.55M | ≈ 349M |
| all Codex on this account | 347 | 521.4M | 31.8M | 486.9M | 2.68M | ≈ 1.88B |

Cached input is 93% of all tokens; uncached input ≈ 6%, output ≈ 0.5%.

Weekly window (Pro): the window 2026-10-02 21:13Z → 2026-10-09 21:13Z stood at 56% used on 2026-10-05 10:33Z after 2.55 days. Shares of that 56% by role are in the companion table below. On the `team` plan (to 2026-09-30) the 5-hour windows peaked at 95–97% three times (09-29, 09-30).

GitHub Codex Bot: 178 reviews in the last 30 days (12 active days; peak 78 on 2026-10-04, 20 on 2026-10-05); "Codex usage limits have been reached for code reviews" was posted 7 times on 2026-10-05 from 07:39Z, with the weekly CLI window at 55–56%; the account shows `credits.balance 62500`.

Observation for the operator: the Codex worker identity `codex-security-dot-a007` runs the `security` profile (gpt-6-astra high), not the `standard` worker profile (gpt-6.1-sol high) of the constellation; its single T81b session (2026-10-04 11:44Z → 10-05 07:25Z) consumed 223.7M tokens, 44% of the period's total.

## Cost at metered (Enterprise / API) rates

Rates (standard tier, developers.openai.com/api/docs/pricing and learn.chatgpt.com/docs/pricing, read 2026-10-05; USD per 1M tokens, input / cached input / output): gpt-6.1-sol 2.00 / 0.10 / 10.00; gpt-6-astra 10.00 / 1.00 / 50.00; gpt-5.6-terra 2.00 / 0.20 / 12.00. Codex credits rate card: Astra 250 / 25 / 1,250, Sol 50 / 2.5 / 250 credits per 1M; one credit is $0.04, so credit billing equals the API list price. Output tokens include reasoning tokens.

| role | sessions | USD for the 8.3-day period | USD per 30 days | USD per 1M tokens |
|---|---:|---:|---:|---:|
| dotfiles worker seats (gpt-6-astra, one gpt-5.6-terra) | 5 | 336.67 | ≈ 1,217 | 1.22 |
| dotfiles auditor exec (241 audits) | 241 | 197.39 | ≈ 713 | 1.32 |
| other projects | 101 | 204.64 | ≈ 740 | 2.12 |
| all Codex on this account | 347 | 738.69 | ≈ 2,670 | 1.42 |

- dotfiles roles: $534 for the period → ≈ $1,930 per 30 days; without the single T81b worker session ($278.64, 224M tokens on gpt-6-astra): $255 → ≈ $923 per 30 days.
- gpt-6-astra is 95% of the cost ($698 of $739). Per audit: mean $0.82 (astra era $1.19, gpt-6.1-sol era $0.35).
- Had the worker seats run the `standard` profile (gpt-6.1-sol) as the constellation specifies, the worker cost would have been $42.66 instead of $336.67 (≈ 7.9×).
- GitHub Codex Bot reviews count toward the same usage; their tokens are not visible locally. Proxy at the astra-era audit cost: 180 reviews/month × $1.19 ≈ $215 (≈ $63 if reviews run on a Sol-class model).
- Seats: ChatGPT Enterprise is negotiated (reported ≈ $45–75/user/month, 150-seat minimum, annual); ChatGPT Business is $20/user/month annual ($25 monthly) with Codex-only pay-as-you-go seats. Today's flat Pro plan (≈ $100–200/month) is replaced at metered rates by ≈ $1,900–2,700/month of token spend plus seats at the current pace, or ≈ $900–1,700/month with the worker on gpt-6.1-sol.
