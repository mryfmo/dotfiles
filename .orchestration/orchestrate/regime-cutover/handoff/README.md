# Regime-cutover handoff

This directory is the snapshot of the `regime-cutover` program as the coordinator measured it on 2026-10-28 (JST), written for the next coding agent. The coordinator owns these files and commits them. A later agent that learns something new appends a dated section to the file it extends and does not rewrite the earlier text. Read the files in the order of the table below, from the program status to the open items.

## Files

| File                                                             | Diátaxis mode | Question it answers                                                                                                                                                                                                                                           |
| ---------------------------------------------------------------- | ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [01-program-status.md](01-program-status.md)                     | reference     | Where does the program stand after the 2026-10-28 pickup, phase by phase and unit by unit?                                                                                                                                                                    |
| [02-audit-treadmill-analysis.md](02-audit-treadmill-analysis.md) | explanation   | Why did the audit round set the program's pace, and what did the units with ten or more rounds have in common?                                                                                                                                                |
| [03-remediation-spec.md](03-remediation-spec.md)                 | how-to        | What does the adopting coordinator copy into a brief to remove the cause of the long audit runs?                                                                                                                                                              |
| [04-open-items.md](04-open-items.md)                             | reference     | Which items stay open, who owns each, what blocks it, and what happens if nobody acts?                                                                                                                                                                        |
| [05-remediation-plan.md](05-remediation-plan.md)                 | explanation   | Which mechanism do the vendor sources support for each root cause, what did the program decide, and in which order do the units run?                                                                                                                          |
| [06-audit-loop-decision.md](06-audit-loop-decision.md)           | explanation   | Why the audit loop took ten to twenty-four rounds per unit, what the literature, the vendors and the documentation support, and the five changes decided on 2026-10-30 with their gates.                                                                      |
| [research/](research/)                                           | reference     | The problem statement and the two research files (git and shell, CI reliability) that hold every citation the plan rests on.                                                                                                                                  |
| [evaluations/](evaluations/)                                     | reference     | The measured evaluations the remediation plan asked for before a decision: U115 (workflow lockfile and the Dependabot triage, plan P-35) and U116 (mise.lock, plan P-36), each a dated file whose commands, outputs and draft decisions row are pasted whole. |

## Conventions

- Unit ids are `U<n>`. A fix unit of `U<n>` carries a letter suffix, as in `U6b`, `U6c` and `U71b`.
- The store is `.orchestration/orchestrate/regime-cutover/`. Paths in this set that start with a bare file name, such as `units.tsv` or `briefs/`, are relative to the store. Other paths are relative to the repository root.
- The store files and what each holds:

| File                                | Content                                                                                                                                                                                          |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [units.tsv](../units.tsv)           | `id track state branch pr head_sha brief note`, one row per unit.                                                                                                                                |
| [ledger.tsv](../ledger.tsv)         | `ts unit pr head_sha verdict verifier evidence`, one row per audit round. `head_sha` is the full 40-hex sha of the head the row judged. `pr-merge.sh` matches that full sha and nothing shorter. |
| [decisions.tsv](../decisions.tsv)   | `ts phase decision why evidence result`, one row per choice that changed the plan.                                                                                                               |
| [gates.md](../gates.md)             | The gates `G<n>` the operator decides. This set cites G4, G8, G9, G10, G11, G17 and G18.                                                                                                         |
| [preferences.md](../preferences.md) | The standing orders. A standing order is cited by its number, as in "standing order 21".                                                                                                         |
| `verdicts/U<n>-<sha8>.md`           | One audit verdict per round, named by the unit and the first eight hex digits of the head it judged. [verdicts/U101-efafe11f.md](../verdicts/U101-efafe11f.md) is the last U101 verdict.         |
| `briefs/U<n>-<slug>.md`             | One brief per unit, in the section grammar below.                                                                                                                                                |

- A brief has the sections GOAL, SCOPE, CHANGE or CONTEXT, ACCEPTANCE, VERIFY, TIMEBOX, FORBIDDEN, REPORT and STANDING, in that order. [briefs/U46-dead-uninstall-functions-removed.md](../briefs/U46-dead-uninstall-functions-removed.md) is the model.
- The levers a coordinator runs, with their exact invocations:
  - `~/.local/bin/common/pr-audit.sh <pr>` runs a fresh Codex audit of the PR head. It refuses a PR body without a `## Contract` section. It prints the verdict file path and one of `Verdict: correct`, `Verdict: incorrect` or `Verdict: blocked`.
  - `~/.local/bin/common/pr-threads-check.sh <pr> --head <40-hex>` requires a reply on every review thread. The first line of the reply is `fixed: <40-hex sha>`, `refuted: <text with URL or file:line>`, `residual: unit=U<n> gate=<clause>` or `residual: operator=<ts>`.
  - `~/.local/bin/common/pr-thread-reply.sh <pr> <comment-id> --body-file <file>` posts that reply. The body file lives under `$TMPDIR` or under the store.
  - `~/.local/bin/common/pr-merge.sh <pr> --records .orchestration/orchestrate/<program>` merges only with a `correct` ledger row for the full current head sha and green CI.
  - `~/.local/bin/common/records-sync.sh --program regime-cutover --unit U20` copies the store against origin/main into a `records/sync-<n>` branch and opens the PR. Run it from the main checkout.
  - `gh pr comment <pr> --body-file <file>` posts the `Fixes bot finding <id>` and `Refutes bot finding <id>` comments that standing order 32 requires.

## How to verify this document set

Every Mermaid block in these files parses, and prettier accepts every file. Both checks were run on 2026-10-28 before this set was reported.

The Mermaid check runs outside the repository with bun, mermaid 11 and jsdom. The checker `check-md.mjs` reads every fenced `mermaid` block of the files named on its command line, calls `mermaid.parse(text, { suppressErrors: false })` on each, and prints `<file>:<block n> ok` or the parse error.

```sh
cd "$TMPDIR/mmd-check"
bun run check-md.mjs \
	~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/handoff/README.md \
	~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/handoff/01-program-status.md \
	~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/handoff/02-audit-treadmill-analysis.md \
	~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/handoff/03-remediation-spec.md \
	~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/handoff/04-open-items.md
```

If `$TMPDIR/mmd-check` is gone, recreate it with `bun add jsdom mermaid@11` in an empty directory and this `check-md.mjs`:

````js
import { readFileSync } from "node:fs";
import { JSDOM } from "jsdom";
const dom = new JSDOM("<!doctype html><html><body></body></html>");
globalThis.window = dom.window;
globalThis.document = dom.window.document;
globalThis.DOMParser = dom.window.DOMParser;
globalThis.navigator = dom.window.navigator;
const mermaid = (await import("mermaid")).default;
mermaid.initialize({ startOnLoad: false });
const fence = /^```mermaid[^\n]*\n([\s\S]*?)^```/gm;
let failures = 0;
for (const file of process.argv.slice(2)) {
  const text = readFileSync(file, "utf8");
  let n = 0;
  for (const match of text.matchAll(fence)) {
    n += 1;
    try {
      await mermaid.parse(match[1], { suppressErrors: false });
      console.log(`${file}:${n} ok`);
    } catch (error) {
      failures += 1;
      console.log(
        `${file}:${n} ${String(error.message ?? error).split("\n")[0]}`,
      );
    }
  }
  if (n === 0) console.log(`${file}: no mermaid block`);
}
process.exit(failures === 0 ? 0 : 1);
````

The prettier check runs from the repository root. `.prettierignore` lists `.orchestration/`, so the explicit ignore path is required for prettier to read these files at all. CI's own call, `scripts/ci/run-on-lint-files.sh markdown prettier --check`, does not read them.

```sh
cd ~/Workspace/dotfiles
prettier --check --ignore-path /dev/null .orchestration/orchestrate/regime-cutover/handoff/*.md
```

## Added 2026-10-30: research/04-llm-review-loop-literature.md

[research/04-llm-review-loop-literature.md](research/04-llm-review-loop-literature.md) (reference) holds the literature behind the audit-round loop of [02-audit-treadmill-analysis.md](02-audit-treadmill-analysis.md): fifteen 2024 to 2026 sources on LLM-judge inconsistency, the convergence of review and repair loops, agentic judges with execution, specification-bounded review, and the fragility of command denylists over shell, each with its venue, URL, quoted figures and one line on what it implies for the loop. It passes the prettier check above and has no Mermaid block.

## Added 2026-10-30: research/05-review-tools-and-loop-practice.md

[research/05-review-tools-and-loop-practice.md](research/05-review-tools-and-loop-practice.md) (reference) closes the two items [05-remediation-plan.md](05-remediation-plan.md) section 5 left "Not verified": published data on fresh-context LLM review rounds, and Copilot code review as a reviewer. It reads twelve AI code review tools (CodeRabbit, Cursor Bugbot, GitHub Copilot, Graphite Agent, Greptile, Qodo, Sourcery, Ellipsis, OpenAI Codex, Anthropic Code Review, Google Gemini Code Assist with Google's and Meta's in-house programs) and thirty-odd 2025 to 2026 practitioner posts on agent PR loops against five questions: noise bounds (severity tiers, thresholds, what blocks, path and rule scopes, published precision), incremental review and finding memory, convergence (round caps, stop conditions, escalation, a recurring class as a design problem), sandboxing for reviewers that execute tests, and a contract or threat model in the PR body. One comparison table, the patterns with quotes, the round counts practitioners report against the ledger's own, and proposals V3-1 to V3-4 in the brief grammar for plan D6, D7, G-20, G-21 and P-41. Every URL was read on 2026-10-30. It passes the prettier check above and has no Mermaid block.

## Added 2026-10-30: the audit-loop decision and three more research files

[06-audit-loop-decision.md](06-audit-loop-decision.md) (explanation) decides the redesign of the review loop from the store's measurements and the research below: one blocking threshold (P0 and P1), a round cap of three with a two-strike class rule and a defined response, incremental audits that read earlier dispositions as data with `carried` rows for unchanged diffs, closure named at brief time with the threat boundary copied into the Contract, and a cheaper, parallel audit after three measurements. Gates G-20, G-21 and G-24 carry the defaults applied under the operator's 2026-10-30 order.

- [research/06-codex-and-actions-security.md](research/06-codex-and-actions-security.md) (reference): the Codex CLI documentation (`codex exec` sandbox modes and writable roots, structured output, `-c`, reasoning effort, AGENTS.md discovery, ChatGPT-login usage windows and the one-`auth.json`-per-stream rule, the GitHub review product's P0/P1 posting) and GitHub's Actions security documentation (the job as one trust domain, `GITHUB_ENV` and `GITHUB_PATH`, the `run:` shell defaults), with proposals A-1 to A-7.
- [research/07-oss-lints-and-shell-safety.md](research/07-oss-lints-and-shell-safety.md) (reference): the OSS linters for GitHub Actions (zizmor, actionlint, poutine, octoscan, ghalint, Scorecard, harden-runner) against the U109 rule, the ShellCheck masked-return facts against the U112 lint, the Bash manual's rebinding channels and what an allowlist buys, and the stopping rules of OSS agents that gate with an LLM judge.
- [research/05-review-tools-and-loop-practice.md](research/05-review-tools-and-loop-practice.md) is registered in the section above.
