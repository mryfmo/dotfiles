# ADR-003: Audit stack, the Codex gate stays and the security audit skill becomes a periodic sweep lens

Status: accepted
Date: 2026-11-02

## Context

The merge gate is one fresh read-only Codex run per pull request head. `pr-audit.sh` reads the rules from the main branch's `AGENTS.md`, treats the head as data, runs Codex under the pinned `audit` profile (`sandbox_mode: read-only`, no network, an allowlisted filesystem, a scratch HOME; `home/dot_agents/codex-audit/config.toml`, `home/dot_agents/agent-config.yaml` near line 689), and writes one verdict file with a findings grammar, priorities and a weight threshold (`AGENTS.md`, Audit section). `pr-merge.sh` squash-merges only a head the ledger records as `correct` with CI passed, by `--match-head-commit` (`scripts/orchestrator/README.md`). The gate has run every unit of the regime-cutover program since U71 (`.orchestration/orchestrate/regime-cutover/ledger.tsv`).

cloudflare/security-audit-skill is one Agent Skill: a `SKILL.md`, fourteen Markdown companions, a JSON findings schema and two dependency-free Node validators (research/cloudflare-security-audit-skill.md, Verdict). It is prompt orchestration for a parent agent with sub-agents: six phases from reconnaissance through coverage-led hunting waves, adversarial validation, a structured `findings.json`, independent re-verification and a target-neutral report (research, section 1). Cloudflare runs the harness it seeded "as a periodic backlog sweep and not a per-PR check", and a `standard` run is tens of sub-agent invocations and hours (research, section 4 "What it would not do", section 5 item 6). Its isolation is prose: it asks for no network, a read-only target, scratch-only writes, an empty environment and resource limits, and issue #128 records a host wipe when an agent improvised them (research, section 5 item 3). Upstream has not merged a change since 2026-09-10, has 71 open pull requests and 39 open issues without a maintainer reply, and publishes no tag, release, checksum or signature; `npx skills add` and skills.sh deliver `main` HEAD (research, Verdict and section 5 items 1 and 2). The frontmatter uses only `name` and `description`, so it passes this repository's validator (research, section 4 "How it would be installed here").

The repository's seats already enforce in configuration most of what the skill asks for in prose: network allowlists, denied credential stores, scratch-only write roots on every seat, and the Codex `audit` profile as the closest match to the skill's sandbox description. Resource limits and an empty environment exist on no seat (research, section 4, the table).

## Decision

1. `pr-audit.sh` with the Codex `audit` profile stays the one merge gate. Its verdict schema, its rounds rule and the threat-table requirement do not change for anything in this ADR.
2. cloudflare/security-audit-skill is trialled behind a flag as a periodic backlog sweep lens, never as a per-pull-request check and never as a writer of verdict rows. A sweep's findings enter the program records as advisory rows (`decisions.tsv` or a findings file under the store) and reach a unit only through a brief the coordinator writes.
3. The skill enters as a pinned `git-commit` asset at commit `c1c8a8c1471069fb0e188eeaff69b8e8db6564a8` with the archive's sha256 and a `reason` naming the absent upstream tags, through `generate-agent-configs.py --set-asset`, never through `npx skills add` (ADR-004 rules). Its `skills.audience` names only the seat that runs sweeps.
4. A sweep runs only on a seat whose sandbox is enforced by configuration: the Codex `audit` profile in guidance or single-hunter mode, or an omp seat under srt with sub-agents (ADR-002). It is given an explicit output directory under the seat's scratch root, never the target-derived `<repo-name>` path (research, section 5 item 5).
5. Reopening conditions for a wider adoption: upstream merges again or names a maintainer, a tag or release appears, or pull request #120 (`plugin.json`) lands so Codex and omp can load it as an Agent Plugin without a local copy.

Forbidden: a sweep result written as a ledger verdict; the skill installed from `main` HEAD; a sweep on a host without the configured sandbox; a Claude plugin or marketplace route for it.

## Alternatives considered

- Make the skill the audit prompt of `pr-audit.sh`. Rejected: a run is hours and dozens of sub-agent calls where the gate needs ten minutes per head; the companions weight web, native, cloud and IPC targets, and this repository's changes are shell, YAML and chezmoi templates (research, section 4 "What it would not do").
- Replace the Codex gate with the skill under Claude Code. Rejected: the gate's value is the fresh read-only run with rules from the trunk and a machine-read verdict; the skill produces a report, not a verdict, and its isolation is prose (research, section 5 item 3).
- Hold entirely. Rejected: the hunting methodology, the attack-class companions and the findings schema are MIT-licensed, agent-neutral and reusable, and the cost of a pinned asset behind a flag is small.
- Install with `npx skills add` as upstream documents. Rejected: it resolves to `main` HEAD with no pin (research, section 5 item 2), which ADR-004 forbids.

## Consequences

Positive:

- The merge gate's contract is untouched, so every unit keeps the same path to `main`.
- The kit gains a documented sweep methodology and a findings schema it can cite, at the cost of one pinned asset.
- The pin and the flag make the trial reversible: remove the asset entry and the audience line.

Negative:

- The asset is a snapshot of an unmaintained repository; every fix is a local patch, and the three reopening conditions must be checked by hand at review time.
- A sweep is expensive in agent calls and wall time, so it runs on request, not on a schedule the kit owns.
- Resource limits and an empty environment stay missing on every seat; a sweep that needs them stays in guidance mode.

Units created:

- The asset pin and audience line, with the validator dry run on `.cjs` and `.json` files inside a skill directory (research, section 6).
- One recorded sweep on this repository, its findings as advisory rows, before the flag is kept or removed.

## Verification

`bdd/audit.feature`:

- `@R-11`, `@R-12`, `@R-13`: the gate as it stands (hold today).
- `@R-14`: a sweep reports findings into the records and never writes a verdict row or changes a gate decision (target).
- `@R-15`: the skill is pinned by commit and archive digest, never installed from `main` HEAD (target, shared with ADR-004).
