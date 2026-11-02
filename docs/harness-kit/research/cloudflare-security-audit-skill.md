# cloudflare/security-audit-skill

Research note for the TechnoPro harness agent kit. Written 2026-11-02 (JST) from primary sources: the GitHub REST API, a full clone of the repository at `main` HEAD `c1c8a8c1471069fb0e188eeaff69b8e8db6564a8` (2026-09-14), the Cloudflare blog post the README cites, the skills.sh registry page, and this dotfiles repository at local HEAD `8227cc52`. Every external claim carries its URL or file; every repository claim names the file. Lines marked **measured** are command output on this host (macOS, Darwin 27.2.0); lines marked **doc** quote the project's own text; lines marked **inferred** are the researcher's reading, not a measured fact. The two bundled Node test files were **not executed** on this host (downloaded code; test counts below are taken from an upstream issue).

Method note. `$TMPDIR/hk-research/` held no shared method file when this note was written, and none was found in the repository, the prompt archive or the session history. The six sibling notes written the same day report the same and converge on: verdict first, vitals, what it is, how it runs, provenance and governance, fit against this repository, risks, open questions, sources. This note follows that order.

## Verdict

- `security-audit-skill` is a **single agent skill** (one `SKILL.md` plus fourteen Markdown companions, one JSON schema and two zero-dependency Node validators), not a harness, framework or service. It is the "~450-line skill" Cloudflare says seeded its fleet-wide Vulnerability Discovery Harness, published the same day as the blog post that describes it (2026-06-18); the harness itself is not in the repository, the blog says it will "hopefully … follow shortly", and no such repository exists in the `cloudflare` organization at observation (doc, blog; measured, repository search).
- It is **prompt orchestration for a coding agent with sub-agents**: a parent agent runs six phases (reconnaissance, coverage-led hunting waves, adversarial candidate validation, structured `findings.json`, independent re-verification, target-neutral report) and delegates each hunter, critic and verifier to a fresh sub-agent. Only the two validators are code that runs (measured, tree).
- It is **agent-neutral by vocabulary** (`Parent`, `Task tool`, `research` and `general` agent roles) and installed through `npx skills add` into `skills/security-audit/`; there is no `plugin.json`, no `.claude-plugin/`, no `.codex-plugin/`, no release, no tag (measured).
- **Maintenance has stopped**: last push 2026-09-14, zero merged PRs since 2026-09-10, 71 open PRs and 39 open issues with no maintainer comment on any thread (measured, GitHub search API). The repository has 56,580 stars and 73.9K skills.sh installs, so the gap between adoption and stewardship is wide.
- **Fit for this repository**: usable as a read-mostly skill under the existing Claude Code and Codex sandboxes, which already supply most of what its "Universal execution safety" section demands (no network, read-only target, denied credentials). It would enter through the pinned-asset mechanism in `agent-config.yaml` (commit + sha256, audience list), not through `npx skills add`. The parts that need an "OS-enforced sandbox with an empty allowlisted environment and scratch-only writes" map onto the Codex `audit` permission profile; the "promotion procedure" (descriptor-based copy from scratch to artifacts) has no implementation anywhere and is instructions to the model. The one reported real-world harm (an agent wiping a real user profile while trying to satisfy "scratch-local HOME", issue #128) is exactly the failure the repository's `failIfUnavailable: true` sandbox and `allowUnsandboxedCommands: false` settings are designed to prevent, but only for Claude Code Bash; it is not prevented for an unsandboxed Codex or omp seat.

## Vitals

| Item                              | Value                                                                                                                                                                             | Evidence                                              |
| --------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| Repository                        | https://github.com/cloudflare/security-audit-skill, id 1273427276, public, not a fork, not archived                                                                               | repos API                                             |
| Owner                             | GitHub organization `cloudflare`. Repository-level rulesets `repository_delete` and `repository_transfer` come from the `cloudflare` Enterprise (measured, `rules/branches/main`) | repos API                                             |
| Description                       | "A coding-agent skill for multi-phase security audits with independently verified, machine-readable findings"                                                                     | repos API                                             |
| Created / last push / last update | 2026-06-18T14:08:44Z / 2026-09-14T19:29:02Z / 2026-11-02T05:50:50Z                                                                                                                | repos API                                             |
| Default branch                    | `main`; only branch on the remote                                                                                                                                                 | measured, `git branch -r`                             |
| Stars / forks / watchers          | 56,580 / 3,689 / 208                                                                                                                                                              | repos API                                             |
| Open issues counter               | 110 = 39 issues + 71 pull requests                                                                                                                                                | repos API; search API                                 |
| Language / size                   | JavaScript 117,195 B (the two validators and two test files); 143 KB repo size                                                                                                    | languages API                                         |
| Topics                            | none                                                                                                                                                                              | repos API                                             |
| Features                          | issues on; projects, wiki, discussions, downloads, pages off                                                                                                                      | repos API                                             |
| License                           | MIT, `LICENSE` 1,078 B, "Copyright (c) 2026 Cloudflare, Inc."                                                                                                                     | measured                                              |
| Community health                  | 87%: README, LICENSE, Code of Conduct (Contributor Covenant) and CONTRIBUTING inherited from `cloudflare/.github`; no issue template, no PR template                              | community/profile API                                 |
| Releases / tags                   | none                                                                                                                                                                              | releases API, tags API, `git tag`                     |
| Commits                           | 14 on `main`, 5 merge commits, 6 author identities, 4 GitHub accounts                                                                                                             | measured, `git log`                                   |
| Registry                          | skills.sh lists 1 skill, 73.9K total installs                                                                                                                                     | https://www.skills.sh/cloudflare/security-audit-skill |
| Contact                           | security-ai-research@cloudflare.com                                                                                                                                               | README                                                |

## 1. What it is

### Tree (measured, `main` HEAD)

```
LICENSE  README.md
skills/security-audit/
  SKILL.md (192 lines)             RECONNAISSANCE.md (156)     HUNTING.md (251)
  ATTACK-CLASSES.md (130)          VALIDATION-AND-REPORTING.md (186)
  AI-AND-LLM.md (83)               CLIENT-SIDE.md (83)         CLOUD-AND-DEPLOYMENT.md (86)
  DATA-ISOLATION-AND-LIFECYCLE.md (84)   DESKTOP-MOBILE-AND-LOCAL-IPC.md (89)
  MEMORY-SAFETY-AND-BINARY.md (101)      PROTOCOLS-RPC-AND-MESSAGING.md (81)
  RESOURCE-EXHAUSTION-AND-AVAILABILITY.md (78)  SUPPLY-CHAIN-AND-RELEASE.md (73)
  WEB-PROTOCOL-AND-AUTH.md (105)
  report-schema.json (461 lines)
  validate-findings.cjs (773)  validate-findings.test.cjs (652)
  validate-coverage-ledger.cjs (872)  validate-coverage-ledger.test.cjs (740)
```

No `.github/`, no `.gitignore`, no `package.json`, no lockfile, no CI (measured, `git ls-tree`). The only prose outside the skill directory is the README.

### Frontmatter and trigger

`SKILL.md` has two frontmatter keys, `name: security-audit` and a `description` that names the trigger: "Security guidance and vulnerability review for codebases, APIs, services, CLI tools, libraries, and daemons. Use for security questions, focused reviews, vulnerability research, security audits, or pen tests. Run the complete workflow only for explicit codebase audit or pen-test requests, full/comprehensive/end-to-end reviews, or requested report artifacts." (doc, `SKILL.md:1-4`). No `allowed-tools`, `license`, `version` or `metadata` keys.

### Two operating modes (doc, `SKILL.md` "Operating modes")

- **Guidance mode** is the default: "Loading it does not authorize the complete audit workflow or file creation." Security questions and focused reviews use only the relevant parts and write no artifacts.
- **Full audit mode** runs all six phases and writes files, only when the user explicitly asks for an audit, pen test, full review, or report artifacts. Ambiguity triggers one clarifying question. This split was the last change on `main` (commit `c1c8a8c`, "Clarify guidance and full audit modes", 2026-09-14; measured).

### The six phases (doc, README and `SKILL.md` "Full audit workflow")

1. Reconnaissance: map architecture, trust boundaries, input surfaces, prior evidence; write `architecture.md` and a deterministic `coverage-ledger.json`.
2. Coverage-led hunting: assign isolated hunters from ledger units; coverage critics find gaps between waves.
3. Candidate validation: every unique candidate goes to a fresh verifier "that did not hunt it" and tries to disprove it.
4. Structured output: `confirmed`, `needs_validation`, `rejected` records in `findings.json`, validated against `report-schema.json` with `validate-findings.cjs`; the ledger validated with `validate-coverage-ledger.cjs`.
5. Independent record verification: fresh agents re-verify final source claims; a material replacement gets yet another verifier.
6. Target-neutral report: `REPORT.md`, `FINDINGS-DETAIL.md`, `NEEDS-VALIDATION.md` derived from the records, "with no live-probe instructions".

Two terminal states only: all Phase 6 artifacts written and both validators pass, or `run_status: "incomplete"` with an exact reason (doc, `SKILL.md`).

### Agent model (doc, `SKILL.md` "Platform terminology"; `HUNTING.md`; `VALIDATION-AND-REPORTING.md`)

- **Parent** coordinates and is the only writer of the shared run files (`run-metadata.json`, `architecture.md`, `coverage-ledger.json`, `findings.json`, the three reports).
- **Task tool** is "the platform's delegation or sub-agent mechanism".
- **`research` agent**: focused source exploration; **`general` agent**: broad investigation and bounded local execution. Hunters and verifiers are `general`.
- Every hunter prompt must contain, in order: role preamble, `architecture.md` verbatim, assigned coverage IDs, the selected attack-class blocks copied verbatim, explicit exclusions, the core hunting method block, the validation rules, carried prior exclusions, and the scratch/artifact paths plus the relevant `report-schema.json` branches copied verbatim (doc, `HUNTING.md` "Required hunter prompt"). Prompts are therefore large: each hunter receives the whole architecture summary plus several hundred lines of method text (inferred from the list).
- Each hunter or verifier gets `<output-dir>/agents/<agent-id>/{scratch,artifacts}/`; it may write only to `scratch/`. Agent IDs match `^[a-z0-9][a-z0-9_-]{0,63}$` and may not be a Windows device name (doc, `SKILL.md` "Write isolation").

### Run profiles, scope and budget (doc, `SKILL.md` "Full audit planning")

- Profiles `quick`, `standard` (default), `deep`; scoped runs audit named paths, one subsystem, one companion domain, or a diff between two refs, and must present themselves as partial coverage.
- A **cost budget** is a maximum number of agent invocations across all phases, recorded in `run-metadata.json`. The text reserves critics and verifiers before hunting, and defines `incomplete_reason` values (`budget_cannot_fund_reconnaissance_and_reserves`, `critic_budget_exhausted`, `validation_budget_exhausted`).
- Prior runs under the same output root are read additively; a prior `confirmed` record is carried only when the relevant source is unchanged, and still goes through current verification (doc, "Coverage and prior runs").

### Evidence bar (doc, `SKILL.md` "Core principles"; README "Design principles")

- A candidate must name a lower-trust principal, accepted input, intended control, crossed boundary, affected principal or resource, and a concrete observed result. Missing best practices, guessed deployment behaviour and self-impact are not findings.
- Only `confirmed` records get severity; anchors from `critical` (unauthenticated code execution, full data-store access, arbitrary account takeover) to `informational`. `needs_validation` has "an exact unresolved fact and no severity".
- "Defense-in-depth gaps are not vulnerabilities." "The agent that checks a finding is never the agent that found it." "The audit describes fixes; it does not modify target source."
- Ten listed anti-patterns, including "Writing the report before independent verification or letting prose and JSON disagree."

### Attack-class companions

`ATTACK-CLASSES.md` holds the "core, wildcard, and obvious-things" prompts; eleven companion files add domain classes (memory safety and binary, AI and LLM, HTTP protocol and auth, client side, supply chain and release, cloud and deployment, RPC and messaging, resource exhaustion, data isolation and lifecycle, desktop/mobile/local IPC) (doc, README "Files"). The parent selects companions during reconnaissance and copies the chosen blocks into hunter prompts. Issue #119 notes that the companions are reachable only through other reference files, not from `SKILL.md`, against Anthropic's one-level-deep guidance (doc, issue #119; confirmed by reading `SKILL.md`, which links only `RECONNAISSANCE.md`, `HUNTING.md`, `ATTACK-CLASSES.md` and `VALIDATION-AND-REPORTING.md`, measured).

### The validators (measured, file heads and `grep`)

- `validate-findings.cjs`: "a dependency-free interpreter for the JSON Schema keywords used by report-schema.json, plus finding-specific checks". Supports a fixed keyword set (`type`, `enum`, `const`, `pattern`, `properties`, `required`, `oneOf`, `items`, `minItems`, `uniqueItems`, `minimum`, `minLength`, `additionalProperties`, and a custom `visibleContent`), ranks severities, and applies limits (`arrayItems: 1000`, 256-byte diagnostic clipping). Usage: `node validate-findings.cjs <path-to-findings.json>`.
- `validate-coverage-ledger.cjs`: validates `coverage-ledger.json` and "canonical coverage IDs" with hard limits (5 MiB input, 10,000 units, 1,000 collection items, 1,000 object fields, depth 64, 500,000 preflight values).
- `report-schema.json`: top-level `type: array` whose `items` is a `oneOf` over the three verdict objects (`confirmed`, `needs_validation`, `rejected`), each with a `const` verdict, a `fingerprint` matching `^[A-Za-z0-9][A-Za-z0-9._:/@+-]*$` "that does not change between validation states", and `visibleContent: true` on the prose fields the report may show (measured, first 30 lines). The validator interprets this file directly rather than through a JSON Schema library.
- Both read input through a `readFileWithinLimit()` that requires `fs.constants.O_NOFOLLOW` and `O_NONBLOCK` (`validate-findings.cjs:605-606`). Those constants are undefined on Windows, so **both CLIs reject every input on win32**. This is deliberate: the ledger validator carries the comment "Node exposes no race-safe fallback on these platforms, so reject all inputs" (`validate-coverage-ledger.cjs:725`, measured). Issue #117 reproduces it and gives the only test counts available (findings tests 34 with 7 failing, ledger tests 31 passing with 7 skipped on Windows). Open PRs #99 and #113 propose fallbacks; unmerged.
- Requires only Node.js; `require("fs")`, `require("path")`, `require("util")` and the `node:` forms, nothing from npm (measured).

## 2. How it runs

### Installation (doc, README "Installation")

```bash
npx skills add https://github.com/cloudflare/security-audit-skill --skill security-audit
npx skills add https://github.com/cloudflare/security-audit-skill --skill security-audit --global
```

The Skills CLI reads the Git tree at `main` HEAD; there is no tag, release, checksum or signature to pin to (measured). Issue #64 reports that uploading the GitHub ZIP into the claude.ai Skills UI fails because `SKILL.md` is nested under `skills/security-audit/` rather than at the ZIP root (doc). PR #120 (reopened from #110) adds a `plugin.json` so the repository loads as an Agent Plugin for Claude Code, Codex and omp; it is open and unreviewed (doc, PRs #110, #120).

### Runtime requirements (doc, README "Requirements")

- "A coding agent with a model that supports tool use and parallel sub-agents."
- Node.js for the validators.
- "An OS-enforced sandbox for target-controlled builds, tests, processes, browsers, emulators, fuzzers, and fixtures. It must disable external networking, use a sanitized allowlisted environment, enforce resource limits, and allow writes only to assigned scratch paths. Without these controls, the workflow keeps the lead as `needs_validation` instead of executing target code."

The skill supplies **no sandbox, no wrapper script and no promotion code**. The nine-step "artifact promotion procedure" (retained directory descriptors, no-follow component walks, `fstat` link-count checks, exclusive creates) is text the parent model is told to carry out with "trusted parent-side code" that does not exist in the repository (doc, `SKILL.md` "Write isolation"; measured, no such script in the tree). An agent platform either has these controls or the run degrades to source-only `needs_validation` records.

### Output location and write surface (doc, `SKILL.md` "Full audit setup")

Default output is `~/security-audit-skill/<repo-name>/run-<N>` outside the target. Writing inside the target is allowed only when the user selects a directory and the parent verifies it is version-control-ignored. `/tmp` and the host home are explicitly forbidden as writable fallbacks for agents. Issue #94 and PR #95 point out that `<repo-name>` is target-controlled (directory name or Git remote) and drives both the output path and prior-run reuse (doc).

### Cost and duration

The README's only figure: "In our test runs, a single run found roughly half of the vulnerabilities that repeated runs found in total" (doc). The blog reports 3 to 4 hours for a full run on a ~30k-line repository in the later harness, and "the worst run took just over 14 hours" (doc, blog). Issue #77 reports a 2.5-hour run under Codex that ended with the output hidden behind a sign-up prompt from a third-party tool (doc). The skill's own budget mechanism is a cap on agent invocations, not tokens or wall-clock (doc, `SKILL.md` "Cost budget").

### Network and credentials

The skill text forbids contacting deployed endpoints, provider APIs, registries, identity systems and brokers, forbids installing dependencies, and tells hunters to record only allowlisted environment variable names and non-secret values (doc, `HUNTING.md` core method). The validators contain no URL, no `fetch`, no `child_process`, no `process.env` read and no token-like literal (measured, `grep` over both `.cjs` files; the only hit is a tokenizer helper named `isTokenDelimiter`). They are offline programs that read one file and exit.

## 3. Provenance and governance

### Origin

- Root commit `4de1ac8`, 2026-06-18T17:20:36+01:00, author "Dan Jones <literally-dan@users.noreply.github.com>", "Initial commit": `SKILL.md` (101 lines), `HUNTING.md` (108), `RECONNAISSANCE.md` (46), `ATTACK-CLASSES.md` (107), `VALIDATION-AND-REPORTING.md` (107), `report-schema.json`, `validate-findings.cjs`, README, MIT LICENSE, all at the repository root (measured, `git log --stat`). The five Markdown files total 469 lines, matching the blog's "~450-line `security-audit` skill" (doc, blog; measured).
- The Cloudflare blog post "Build your own vulnerability harness" (author Grant Bourzikas, Cloudflare CISO; URL in Sources) describes the skill as the seed of the Vulnerability Discovery Harness and Vulnerability Validation System, says it has "been slightly cleaned up before release", and links the repository. The post's skill-to-harness table maps the skill's phases one-to-one onto the harness stages Recon, Hunt, Validate, Report, mechanical validation, independent validation (doc, blog).
- The blog was published 2026-06-18T17:59Z (`article:published_time`, measured); the repository was created at 14:08Z and the root commit is timestamped 16:20Z UTC the same day. The blog's description of the original skill differs from today's tree in two places: it describes a 7-phase run ending in "submitted to the ingest API" (an internal Cloudflare step, absent here) and "Three parallel research agents do recon"; the current `RECONNAISSANCE.md` says "Launch several `research` agents in parallel" and `SKILL.md` reserves "the four baseline reconnaissance calls" (doc). The post was on the Hacker News front page on 2026-09-17 (213 points, 38 comments, Algolia API), three days after the last push.

### History shape (measured, `git log origin/main`)

| Date               | Commit                                | Change                                                                                                                                                                                                                                                                       |
| ------------------ | ------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2026-06-18         | `4de1ac8`                             | Initial commit, flat layout                                                                                                                                                                                                                                                  |
| 2026-06-24 / 06-29 | `75be8dd`, merge `f75f9a0`            | PR #2 (lambda0xyz): move files under `skills/security-audit/` for `npx skills add` compatibility                                                                                                                                                                             |
| 2026-07-02 / 07-03 | `71e1549`, merge `fc70ead`            | PR #4 (CooperSheroy): validate trace step ordering                                                                                                                                                                                                                           |
| 2026-07-04         | `f5c2df0`, `78d28fa`, merge `642fbad` | PR #3 (kennysarnoski-jarvis): `MEMORY-SAFETY-AND-BINARY.md`, then maintainer moves it into the skill directory                                                                                                                                                               |
| 2026-07-06         | `b6b3f15`, `c1239b9`, merge `8bac420` | PR #6 (maintainer): AI/LLM, web-protocol/auth, client-side companions; "one coherent house style"                                                                                                                                                                            |
| 2026-09-10         | `158eb44`, merge `d24bc26`            | PR #12 (maintainer): "Rework the audit workflow, findings contract, and validators end to end", +4,792 / -701 lines, adds six companions, the coverage ledger, both test files; `validate-findings.cjs` grows from 194 to 773 lines and `report-schema.json` from 210 to 461 |
| 2026-09-14         | `c1c8a8c`                             | "Clarify guidance and full audit modes", pushed directly to `main` (no PR)                                                                                                                                                                                                   |

Fourteen commits in 13 weeks, then nothing for 7 weeks before observation. The September rework is 85% of all lines ever added (inferred from the stat).

### Authorship and signing (measured)

- `git shortlog -sne`: `literally-dan <9935415+…>` 6, `Dan Jones <9935415+…>` 4, `Dan Jones <literally-dan@users.noreply…>` 1 (same account, three identities), `CooperSheroy` 1, `kennysarnoski` 1, `lambda0xyz` 1. The maintainer authored 11 of 14 commits.
- `git log --format=%G?`: the five GitHub-web merge commits are `E` (signed by GitHub, key not available locally); all nine non-merge commits are `N`, unsigned, including the latest direct push.
- GitHub account `literally-dan`: created 2014-11-24, no name, company, bio or blog, 1 public repository, 129 followers (users API). Public membership of the `cloudflare` org: not listed (HTTP 404 on `orgs/cloudflare/public_members/literally-dan`; private membership cannot be checked). The link to Cloudflare rests on the repository living in the organization, the Cloudflare copyright line, and the blog post; the account itself discloses nothing (**inferred**).

### Releases and distribution

No release, no tag, no `CHANGELOG`, no version field anywhere in the tree (measured). Consumers of `npx skills add` and skills.sh get `main` HEAD. The pinned-asset model this dotfiles repository uses (commit plus archive sha256) is the only way to get a stable artifact (inferred).

### Governance and throughput (measured, search API, 2026-11-02)

| Queue                                       | Count                                        |
| ------------------------------------------- | -------------------------------------------- |
| PRs merged (all time)                       | 5 (#2, #3, #4, #6, #12), last on 2026-09-10  |
| PRs closed unmerged                         | 4                                            |
| PRs open                                    | 71, oldest from September, newest 2026-11-01 |
| Issues open / closed                        | 39 / 7                                       |
| Threads with a comment from `literally-dan` | 0                                            |

- Issue #114 (2026-10-27, "65 open PRs, 0 merged in 42 days") documents that the queue is self-conflicting: PRs #63 and #97 make incompatible changes to the validator CLI entry point, and "77 PR pairs conflict". The only replies are from other contributors (doc).
- Issue #128 (2026-11-01) reports that on Windows, with no sandbox available, an agent following the "scratch-local `HOME`" instruction deleted `~/.claude`, `~/.agents/skills`, `~/.ssh`, `~/.npmrc` and gutted the system Python; the reporter attributes it to the skill naming an isolation requirement without a mechanism or an explicit "the real HOME is not yours to clean" invariant, and proposes a fail-closed isolation check (doc). PR #129 implements it; unreviewed.
- Issues #94 (target-controlled repo name drives output path and prior-run reuse), #107 (asymmetric parser limits between the two validators), #117 (Windows), #119 (nested references), #80/#79/#78 (ledger state-machine gaps) are substantive design reports, all unanswered (doc).
- Several open issues are spam or off-topic (#122, #115, #98, #72, #71, #52). The seven closed issues include #61, opened and closed within 29 seconds by its own author (measured, `closed_by`). No issue or PR shows a close, label, comment or review from the maintainer after 2026-09-14 (measured, search API `commenter:literally-dan` returns zero threads).
- Policy documents are inherited from `cloudflare/.github`: Contributor Covenant Code of Conduct, CONTRIBUTING (both HTTP 200 at the org `.github` repo, measured). No repository-level `SECURITY.md`; the org file exists. No CODEOWNERS, no `MAINTAINERS`, no branch-protection data (HTTP 401), no CI to gate PRs (measured).
- The README invites "comparing notes" at a Cloudflare mailbox rather than through issues, and the blog says the harness will "hopefully … follow shortly"; read together with zero maintainer activity since 2026-09-14 and no harness repository in the organization, the repository looks like a one-time publication alongside the blog, not a maintained project (**inferred**).

## 4. Fit against this repository

### What this repository already has that the skill asks for

The skill's "Universal execution safety" (doc, `SKILL.md`) asks for no external network, an allowlisted environment, a read-only target and toolchain, scratch-only writes, and resource limits. Against `home/dot_agents/agent-config.yaml` (repository, read 2026-11-02):

| Skill requirement                                    | Claude Code seat                                                                                                           | Codex, audit profile                                                                            | omp seat                                |
| ---------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- | --------------------------------------- |
| No external network                                  | Bash sandbox `network.allowedDomains` is a short GitHub list; `failIfUnavailable: true`, `allowUnsandboxedCommands: false` | `sandbox_workspace_write.network_access: false`; `audit` profile is `read-only` with no network | srt per `anthropics-sandbox-runtime.md` |
| Read-only target                                     | not by default: the working directory is writable (`workspace-write` equivalent)                                           | `audit` profile `sandbox_mode: read-only`                                                       | per seat policy                         |
| Scratch-only writes                                  | `filesystem.allowWrite` is cache and state directories only; TMPDIR writable                                               | `writable_roots: []`                                                                            | per seat policy                         |
| Empty allowlisted environment                        | `sandbox.credentials` denies named files and env vars, but the environment is otherwise inherited                          | `shell_environment_policy.inherit: core`                                                        | srt                                     |
| Resource limits (CPU, memory, processes, wall-clock) | none in the manifest                                                                                                       | none                                                                                            | none                                    |
| Credentials denied                                   | `~/.ssh`, gh hosts, agent login stores, chezmoi age key denied                                                             | audit profile filesystem allowlist                                                              | srt denies                              |

So the network, credential and write-root controls exist on every seat; **resource limits and an empty environment do not**, and the skill text would push hunters to `needs_validation` for any check that needs execution unless the parent judges the controls "all available" (inferred from the skill's fail-closed wording). The Codex `audit` profile (read-only, no network, allowlisted filesystem, scratch HOME, "nothing is readable unless an entry opens it", `agent-config.yaml` comments around line 689) is the closest match to the skill's sandbox description.

### Sub-agents

The skill needs a parent that can launch parallel sub-agents and receive one JSON object back from each (doc, `HUNTING.md`). Claude Code's Task tool and this repository's hcom seats (orchestrator and worker roles in `agent-config.yaml` `omp.roles`) both provide that; Codex `codex exec` under the `audit` profile is a single process and would run the skill only in guidance mode or as one hunter at a time (inferred). The skill's `research` and `general` roles are abstract; the text says "Use equivalent platform capabilities while preserving role, write-isolation, prompt, and independence boundaries" (doc, `SKILL.md`), so the parent picks whatever sub-agent type the platform offers. This repository defines no agent named `research` or `general` (measured, `home/dot_claude/agents/`).

### How it would be installed here

`agent-config.yaml` keeps shared skills in `~/.agents/skills`, declares every skill's audience under `skills.audience`, and brings third-party trees in as pinned `assets` entries: `source: git-commit` with `pin: <40-hex commit>` and `sha256:` of the archive (the Homebrew entry at `agent-config.yaml:1149-1153`), with a `reason` string when upstream "publishes no per-plugin tag, release, checksum or signature" (the pstack entry, `agent-config.yaml:1275-1287`). The manifest's own rule is "pins here only, through generate-agent-configs.py --set-asset" (`agent-config.yaml:1083`). This repository would therefore not run `npx skills add`; it would add a `git-commit` asset pinned to `c1c8a8c…` with the tree's sha256, install `skills/security-audit/` under a managed root, and name the audience (`claude`, `codex`, `omp-*`) explicitly.

The frontmatter would pass this repository's validator: `scripts/validate-agent-assets.py` accepts exactly `name`, `description`, `license`, `compatibility`, `metadata` and `allowed-tools` (`SKILL_FIELDS`, line 469), and the skill uses only the first two (measured). Whether the validator objects to `.cjs` and `.json` files inside a skill directory was not dry-run (**unverified**).

### Where the two designs already agree

- **Adversarial, independent verification** of every finding by an agent that did not produce it, and a mechanical validator before the report: the same shape as this repository's per-head verdict rows and the `pr-audit.sh` / `codex-audit` chain (repository, `agent-config.yaml` `claude.levers`; inferred parallel).
- **Fail closed**: both the skill ("If every control cannot be enforced, do not execute target code") and this repository (`failIfUnavailable: true`, `allowUnsandboxedCommands: false`) refuse rather than degrade. The difference is that the repository enforces it in configuration and the skill only states it in prose; issue #128 is what happens when the prose meets a host without the configuration.
- **Target content is untrusted**: the skill treats every scratch entry as target-controlled after execution; PR #108 ("Treat target content as untrusted data in every agent prompt") shows this is incomplete in the hunter prompts (doc).

### What it would add

- A concrete, long-tested hunting methodology and ten attack-class companions that are agent-neutral and MIT-licensed; the budget, profile and ledger vocabulary; a findings schema with three verdict branches and a validator for it.
- Nothing executable beyond the two Node validators; nothing that touches hcom, herdr, permgate or the chezmoi apply.

### What it would not do

- It is not a CI check (a full run is hours and dozens of agent calls; the blog says Cloudflare runs the harness as "a periodic backlog sweep and not a per-PR check").
- It does not audit shell, YAML or chezmoi templates any better than any other prompt; the companions are weighted toward web, native, cloud and IPC targets.

## 5. Risks and caveats

1. **Unmaintained since 2026-09-14** with 71 open PRs, 39 open issues and no maintainer response. Any fix this repository needs (Windows validators, nested references, repo-name sanitisation) would be a local patch to a pinned copy.
2. **No pinning surface upstream**: no tag, release, checksum or signature; `npx skills add` and skills.sh deliver `main` HEAD. Pin by commit and content hash.
3. **Prose-only isolation**: the sandbox, empty environment and promotion procedure are instructions to a model. Issue #128 documents a real user-profile wipe when an agent improvised them. Run it only on a seat whose sandbox is enforced by configuration, and never on a bare Windows or unsandboxed host.
4. **Validators are POSIX-only** (`O_NOFOLLOW`, `O_NONBLOCK`), so Phase 4 cannot complete on Windows; irrelevant for this repository's macOS and Ubuntu hosts, relevant for WSL only if Node runs on the Windows side.
5. **Target-controlled output path**: `<repo-name>` from the directory or remote feeds the output directory and prior-run lookup (issue #94). A malicious target name can escape or poison the run root. Pass an explicit output directory.
6. **Prompt size and cost**: every hunter prompt embeds `architecture.md`, several companion blocks and the schema verbatim; hunter count scales with ledger units. A `standard` run on a mid-size target is tens of sub-agent invocations and hours (doc, blog; inferred).
7. **Large single-author rewrite**: 85% of the content landed in one 4,792-line commit on 2026-09-10 with no external review visible, two months after the public launch. The later issues (#79, #80, #107) read as review of that commit after the fact.
8. **Companion reachability**: topic files are not linked from `SKILL.md`, so an agent that reads only one level deep never sees them (issue #119).
9. **Dual-use text**: the companions are attack methodology, bounded by "defensive, source-first" constraints throughout. The constraints are prompt text; the repository's own command policy and sandbox remain the control.

## 6. Open questions and unverified items

- Who `literally-dan` is inside Cloudflare, and whether a team or one person owns the repository: **unverified** (no org membership visible, no profile data).
- Whether the harness itself will be published ("hopefully … follow shortly" in the blog): **unverified**; a GitHub repository search for `org:cloudflare harness vulnerability` returns nothing (measured, 2026-11-02).
- Branch protection on `main`: **blocked** (HTTP 401). The direct push of `c1c8a8c` suggests no required review, or a bypass for the maintainer.
- Whether `validate-agent-assets.py` accepts `.cjs` and `.json` files inside a skill directory: **unverified**, needs a dry run. The frontmatter itself passes (see section 4).
- Test suite results on this host: **not run** (downloaded code policy). Upstream counts on Windows from issue #117 are the only numbers available.
- Whether PR #120 (`plugin.json`, state open, `mergeable_state: clean`, zero comments) will land: **unverified**; it is the one change that would let Codex and omp load the repository as an Agent Plugin without a local copy.

## 7. Sources

- Repository: https://github.com/cloudflare/security-audit-skill, clone at `$TMPDIR/hk-research/_src/cf-sas` (HEAD `c1c8a8c1471069fb0e188eeaff69b8e8db6564a8`, fetched 2026-11-02): `README.md`, `LICENSE`, `skills/security-audit/SKILL.md`, `HUNTING.md:1-83`, `VALIDATION-AND-REPORTING.md:1-63`, heads and `grep` of `validate-findings.cjs` and `validate-coverage-ledger.cjs`, `git log --stat`, `git shortlog -sne`, `git log --format=%G?`, `git tag`, `git branch -r`, `git ls-tree`
- GitHub REST API: `repos/cloudflare/security-audit-skill` (repo, releases, tags, contributors, community/profile, languages, rules/branches/main, branches/main/protection → 401), `users/literally-dan`, `orgs/cloudflare/public_members/literally-dan` → 404, `search/issues` (is:pr, is:pr is:merged, is:pr is:open, is:pr is:closed is:unmerged, is:issue is:open, is:issue is:closed, commenter:literally-dan), `issues/{64,77,110,112,114,117,119,128}` and comments on #110 and #114
- Cloudflare blog, "Build your own vulnerability harness", Grant Bourzikas: https://blog.cloudflare.com/build-your-own-vulnerability-harness
- skills.sh registry: https://www.skills.sh/cloudflare/security-audit-skill
- `cloudflare/.github`: https://raw.githubusercontent.com/cloudflare/.github/master/SECURITY.md and `CONTRIBUTING.md` (HTTP 200)
- This repository (`~/Workspace/dotfiles`, HEAD `8227cc52`), read-only: `home/dot_agents/agent-config.yaml` (`skills.audience`, `omp.skills_directories`, `codex.sandbox_workspace_write`, `codex` audit profile comments, `claude.sandbox`, `assets` entries for pstack and Homebrew, the `--set-asset` rule), `scripts/validate-agent-assets.py` (`SKILL_FIELDS`), `home/dot_agents/skills/` and `home/dot_claude/agents/` listings
- Hacker News Algolia API: https://hn.algolia.com/api/v1/search?query=security-audit-skill%20cloudflare&tags=story
- Sibling notes in `$TMPDIR/hk-research/` for structure: `anthropics-sandbox-runtime.md`, `graphify-labs-graphify.md`, `mukul975-anthropic-cybersecurity-skills.md`, `tester-army-e2e.md`
