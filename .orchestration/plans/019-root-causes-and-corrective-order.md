# Plan 019: problems, root causes, outside references, and the corrective order (written on the operator's order of 2026-10-13 10:5xZ: "first organise the problems and root causes; study official documentation, current information and other OSS harnesses; then decide stage by stage what corrects what")

> Status: DRAFT for the operator's review, nothing executed (written 12:54Z). Figures marked (pasted) are command output of 2026-10-13; quotes are from the sources listed at the end, fetched 2026-10-13.

## 1. Problem inventory (what is observably wrong)

| # | Problem | Evidence (pasted) |
|---|---|---|
| P1 | A change of six code and test files took eight hours from PR to merge; two sibling PRs are open since 2026-10-12 | PR #336 created 01:55Z, merged 09:56Z; #328 since 10-12 12:07Z; #329 since 10-12 12:31Z |
| P2 | Reviews never converge: every new head, including update-branch heads of unchanged code, yields new findings | #336: 13 Bot reviews, 30 threads (P1 9, P2 21) on 30 commits; #328: 7 reviews, 16 threads; #329: 8 reviews, 20 threads; two update-branch rounds on #336 and one on #328 added findings with no code change |
| P3 | The task text, not the code, became the main reviewed artifact | a02 text: 12 seat rounds + 19 Codex rounds; a04 (tools) redesign: 5 + 5; task files of 100–150 lines with 20–25 threat rows and grammar tables; 28 task files across three lineages |
| P4 | Every finding breeds process: resets (a01 → a04 ×3), amendments, records (36 M / 34 C), plans (008–018), blocking asks (6, one waited 9 h) | index.yaml; plans directory; bus 48 TASK / 46 RESULT / 35 ACCEPTANCE today |
| P5 | The regime's enforcement ran before its tooling existed; the tooling was hand-built in a scratchpad and had bugs that cost rounds | 105 scratchpad scripts; M-20261012-26 (six instances), M-35 (a glob matched its negation); "Once plan 007 T718 lands" sentences in rule text |
| P6 | Records commits to main re-trigger CI and the Bot on every open PR | 11 boundary PRs today; ruleset `strict_required_status_checks_policy: true`; plans 015, 016, 017 were all caused by this loop |
| P7 | Merge mechanics were discovered at merge time | required thread resolution (30 threads to resolve and re-sweep on #336); dispositions grammar |
| P8 | Verification did not check what the design requires | the pair checked invariant ids, the design requires sentences byte-for-byte (INV-2 line 56); "thirty minutes" against INV-10's 20 (line 64) |
| P9 | One worker served three lineages in sequence, and a machine sleep stalled a round for 25 minutes | a003 did T703, T718 and a02; the 09:22Z sleep |
| P10 | No per-change cost metric existed; divergence was noticed after days | the first cost table is plan 018 |

## 2. Root causes (not symptoms) and what the references say

**RC1 — Non-deterministic reviewers used as a convergence oracle.** The regime treats every Codex Bot thread (P2 included) and every local or pair finding as a gate input that must be fixed or owned, and it re-runs the reviewer on every head. LLM reviews are not repeatable: "even with temperature minimized, LLM responses varied to different degrees … inherently limited consistency (test-retest reliability) … caution when using LLM-generated code reviews to make real-world decisions" (Klishevich et al., arXiv 2502.20747). Our own measurement agrees: the local Codex review reproduced 0 of 23 Bot threads and found 1 new one. Anthropic's guidance: "A reviewer prompted to find gaps will usually report some, even when the work is sound … Chasing every finding leads to over-engineering … flag only gaps that affect correctness or the stated requirements, and treat the rest as optional." Codex's own GitHub integration states "In GitHub, Codex flags only P0 and P1 issues so review comments stay focused on high-priority risks"; our rules elevated P2 to gate inputs. CodeRabbit bounds its loop by design: incremental review of new commits only and "automatically pauses incremental reviews after this many reviewed commits" (default 5). Agent harnesses cap iterations (OpenHands `MAX_ITERATIONS` default 100 per task, `MAX_BUDGET_PER_TASK`). Our loop had no cap and no notion of "advisory".

**RC2 — The unit of change and its specification are too large.** Google's guide: "100 lines is usually a reasonable size for a CL", "1000 lines is usually too large", "reviewers have discretion to reject your change outright for the sole reason of it being too large"; one self-contained change with its tests. Our PRs: #336 +2819 (26 files incl. evidence), #329 +3908, #328 +1788. Anthropic on specs: "The most useful specs are self-contained: they name the files and interfaces involved, state what is out of scope, and end with an end-to-end verification step"; "If you could describe the diff in one sentence, skip the plan." Our task texts specify behaviour sentence by sentence (grammar tables, 25 threat rows), so each review round finds a cell missing, and the text is re-reviewed more than the code.

**RC3 — Enforcement before mechanism.** Anthropic: "CLAUDE.md instructions … are advisory, hooks are deterministic"; rules that must hold go into executed checks. The regime stated rules whose mechanism was not landed ("Once T718 lands …"), enforced them by hand through scratchpad scripts, and the scripts' defects (M-26, M-35) became rounds. The design's own INV-6 says the gate is the mandatory point; the gate for most of this (T702) is still unmerged.

**RC4 — One integration path for code and records under a strict up-to-date rule.** GitHub: with "Require branches to be up to date before merging" … "More builds may be required"; the official alternative is the merge queue, which "provides the same benefits as the Require branches to be up to date before merging branch protection" without the author updating the branch (requires CI on `merge_group`; available for public repositories owned by an organization and private repositories on Enterprise Cloud — this repository is public but owned by a user account, so availability must be checked in the repository settings). Our boundary commits of records (11 today) each forced an update-branch, a 9-minute CI run and a Bot round on every open PR.

**RC5 — Resets and blocking asks as the response to findings.** INV-6 resets a task on counts (revise 2, amendments 2, questions 2, Bot P0/P1 on two heads); a reset means a new task file, two review halves, a reset record and a boundary. Anthropic's failure pattern: "Correcting over and over … After two failed corrections, `/clear` and write a better initial prompt" — the remedy is a smaller, clearer unit, not a fourth document in the lineage. Blocking asks (S7) waited up to 9 hours; Copilot's coding agent and Spec Kit both make the human loop asynchronous (comments, tasks with ids), not a stop.

**RC6 — No measurement.** No per-change ledger of rounds, threads, wall time and cost existed until plan 018, so the divergence (P1) was felt, not detected. Harnesses that bound loops do it on a counter they expose.

Problems map to causes: P1 ← all; P2 ← RC1, RC4; P3 ← RC2; P4 ← RC1, RC5; P5 ← RC3; P6 ← RC4; P7 ← RC3; P8 ← RC2, RC3; P9 ← RC2 (parallel lineages on one worker); P10 ← RC6.

## 3. Corrective order (each stage closes one cause, is verifiable, and does not depend on the later ones)

| Stage | Closes | Change (one setting or one small PR each) | Done when | Reference |
|---|---|---|---|---|
| 0 | RC6 | A per-PR cost ledger: rounds (Bot, local, pair), threads by priority, resets, wall from first push to merge; one line per PR in `.orchestration/metrics/`; filled from `gh api` by one script | the three open PRs have their lines; every later stage reports its line | OpenHands/SWE-agent expose the counters they cap on |
| 1 | RC1 | Review policy: (a) Codex Bot P2 and local-review P2 are advisory: recorded, never a round, never a reset trigger; only P0/P1 get at most one fix round per PR; (b) the Bot's review trigger set to "On PR open" (not every push), re-review only by `@codex review` after a fix; (c) the convergence rule is deterministic: required checks green + one adversarial review with no open P0/P1 + the audit; (d) INV-6's Bot count applies to P0/P1 only (already so) and nothing counts P2 | the next PR closes with ≤ 3 review rounds and no P2-driven round; the ledger shows it | Codex docs (P0/P1 scope; Review trigger); Anthropic (optional findings); Klishevich 2025; CodeRabbit pause |
| 2 | RC4 | Decouple: records go to main at most once per day (or to a `records` branch merged by one PR per day), never between a PR's final head and its merge; evaluate the merge queue for this repository (if available: `merge_group` in CI, "Require merge queue" in the ruleset, strict flag off); if not, strict stays and the boundary cadence alone removes the loop | zero update-branch-triggered reviews in the ledger for the next three PRs | GitHub docs (strict cost; merge queue) |
| 3 | RC2 | Unit of change: one mechanism per PR, ≤ 200 changed lines outside tests (Google's 100 as the target), tests in the same PR; task text ≤ one page: goal, files, out of scope, one end-to-end verification command; the threat table generated by the checker from `allowed_files` (one template row per path kind), not hand-written; text review = one round, seat and Codex in parallel, findings beyond that become items of the next PR | the next task text ≤ 60 lines; ≤ 1 text round; PR size within the cap | Google eng-practices; Anthropic specs |
| 4 | RC3 | Tool before rule: land the orchestrator tools (a02 PR-A, then PR-B after the gate) and the checkers (T704) before any further rule text; retire the scratchpad chain; a rule sentence may name only a landed mechanism (the "Once X lands" form is forbidden) | the integration of the next PR runs only `scripts/orchestrator/*`; grep finds no "Once … lands" in the SKILL | Anthropic (hooks over advisory text) |
| 5 | RC5 | Resets only on a failed deterministic check or a P0/P1 the one round could not fix; P2 counts never reset; operator decisions asynchronous with a default (decision panel), blocking only for P0 | resets per week in the ledger; ask wait time | Anthropic ("after two corrections, a better prompt"); Copilot agent's comment loop |
| 6 | RC6 again | Records proportionate: one M/C only when an outcome changed; a weekly retrospective from the ledger instead of per-event records | records per PR ≤ 1 | — |

Order rationale: 0 first because every later "done when" reads it; 1 and 2 remove the two largest multipliers and need no code; 3 and 4 change what a task is and what enforces it; 5 and 6 are the regime's own overhead and follow once 1–4 hold.

## 4. The three open PRs under stages 0–1 (no new rounds)

- #328 (T703): the P1 thread (4257278283) gets the one round it is owed (the amendment already pair-confirmed and on main); the three P2 (two Bot, one local) are recorded as advisory with their owner task; merge after CI, one audit, the gate.
- #329 (T702): the accepted head 21badcd7 merges after update-branch, CI, one audit, the gate; its P2 recorded as advisory.
- #346 (a02 PR-A): the worker finishes its RESULT; same rule.
- No boundary until all three merge (stage 2 applied immediately); no task-text review (stage 3 applied immediately).

## 5. What this plan could not verify

- Whether the Codex Bot in this repository re-reviews on every push by setting or by default: the official page lists a "Review trigger" preference without naming the options; user reports name "On PR open / On every push / Smart Trigger". Observed here: 13 reviews on 30 commits of #336 with 5 manual `@codex review` comments, so pushes did trigger reviews. The setting is the operator's to read at app.chatgpt.com/settings/code-review.
- Merge queue availability for a user-owned public repository (the docs name organization-owned public repositories).
- SWE-agent's exact limit keys (its config pages did not show them; not needed for the order).

## Sources

- OpenAI, "Codex code review in GitHub": https://learn.chatgpt.com/docs/third-party/github
- GitHub Docs, "Available rules for rulesets": https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets
- GitHub Docs, "Managing a merge queue": https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue ; GitHub Blog, merge queue GA: https://github.blog/changelog/2023-07-12-pull-request-merge-queue-is-now-generally-available/
- Google Engineering Practices, "Small CLs": https://google.github.io/eng-practices/review/developer/small-cls.html
- Anthropic, "Best practices for Claude Code": https://code.claude.com/docs/en/best-practices
- Klishevich et al., "Measuring Determinism in Large Language Models for Software Code Review" (2025): https://arxiv.org/abs/2502.20747
- CodeRabbit, "Auto review" configuration: https://docs.coderabbit.ai/configuration/auto-review
- OpenHands, environment variables (`MAX_ITERATIONS`, `MAX_BUDGET_PER_TASK`): https://docs.openhands.dev/openhands/usage/environment-variables
- GitHub Docs, Copilot coding agent, "Reviewing a pull request created by Copilot": https://docs.github.com/en/copilot/how-tos/agents/copilot-coding-agent/reviewing-a-pull-request-created-by-copilot
