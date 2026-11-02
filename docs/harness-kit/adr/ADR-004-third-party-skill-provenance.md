# ADR-004: Third-party skill provenance

Status: accepted
Date: 2026-11-02

## Context

The repository already pins every third-party asset. `assets:` in the manifest holds one declaration per component with its upstream, release or pin, verification and installer; a component whose publisher offers no verification keeps a `pin` with its sha256 and a `reason` (`home/dot_agents/agent-config.yaml:1074-1085`). The pstack skill tree is pinned to a `cursor/plugins` commit with the sha256 of that commit's archive (`agent-config.yaml:1261-1266`, `docs/omp-skills.md`, "The pin"). Claude plugins are pinned by version, or by content digest where upstream has no version (`agent-config.yaml:1364-1385`). The validator requires a complete declaration per asset (`scripts/validate-agent-assets.py:1270`), admits only the six Agent Skills frontmatter fields (`:469`) and scans every tracked file for committed secrets (`:250`, `:2481`).

Two candidates test that posture. anthropics/knowledge-work-plugins is Anthropic's own repository, Apache-2.0, with the engineering and operations plugins listed as "Anthropic verified" in the claude.com directory; the vendored plugins move with `main`, there is no tag or lockfile, and a content change at the same `version` is possible (research/anthropics-knowledge-work-plugins.md, "Security and trust boundary", "Maturity and risk"). The skills are prompt text only, 32 to 158 lines each, with `argument-hint` in every engineering skill and connector placeholders that must be rewritten ("The skills-first policy").

mukul975/Anthropic-Cybersecurity-Skills is a single-maintainer personal repository of 818 generated skills whose name begins with "Anthropic" and whose disclaimer appeared fourteen days after creation; the v1.0.0 release notes still point at a non-existent `anthropics/cybersecurity-skills` repository (research/mukul975-anthropic-cybersecurity-skills.md, sections 1 and 3). Every distribution channel resolves to `main` HEAD, no tag is signed, no release carries assets or checksums, CI pushes to `main` under the maintainer's identity, and there has been no push since 2026-08-31 while 42 pull requests stay open (sections 2, 4 and 5). The provenance review assessed metadata, packaging, provenance and governance only; skill content was not assessed (section 1, Scope).

## Decision

Adopt a third-party skill only with a verified publisher, a commit pin with a sha256 or a vendored copy that records its upstream commit, a curated subset, validator-clean frontmatter and a review cadence. The knowledge-work-plugins engineering and operations skills are adopted as a skills-first port. The cybersecurity skills pack is held.

Concrete rules:

1. Publisher: the upstream organisation or person is identified from primary sources, and a name that borrows another organisation's is a flag, not a credential.
2. Pin: a skill tree installed by an installer carries an `assets:` entry with `pin` (a commit or a tag) and `sha256`, as pstack does. A skill copied into `home/dot_agents/skills` records the upstream path and commit in `metadata` of its frontmatter and keeps the upstream licence notice.
3. Subset: only the skills the operator names are adopted. For knowledge-work-plugins the candidate subset is the skills with no counterpart here: `incident-response`, `deploy-checklist`, `architecture`, `tech-debt`, `testing-strategy`, `runbook`, `change-request`, `risk-assessment`, `status-report` (research/anthropics-knowledge-work-plugins.md, "Integration options", option 1); the operator confirms the list.
4. Frontmatter: a copy holds only the six admitted fields; `argument-hint`, `~~connector` placeholders, `$ARGUMENTS` and `@$1` are removed or rewritten; each copy gets a `skills.audience` entry.
5. Cadence: a unit test diffs each copy against the recorded upstream text, so drift is visible, and the subset is re-read at each reviewed bump of the recorded commit.
6. Held: the cybersecurity skills pack is not installed, pinned, vendored or referenced until it has a second maintainer or an organisation, signed tags or release checksums, and a content review of the chosen subset.

Forbidden: `npx skills add <repo>` or a marketplace add that resolves to a branch head; a copied skill without a recorded upstream commit; a skill with a field outside the admitted six.

## Alternatives considered

- Pin the engineering plugin as a Claude plugin instead of copying skills. Rejected in ADR-001: it brings eight Claude-only MCP servers and reaches neither Codex nor omp.
- Install the cybersecurity pack from a pinned commit as a curated subset. Rejected for now: a pin fixes the bytes but not the provenance flags (single maintainer, no integrity controls, bulk-generated origin, nine weeks idle), and the content of any subset was not reviewed (research/mukul975-anthropic-cybersecurity-skills.md, section 5).
- Track upstream automatically with a nightly bump, as upstream itself does for its marketplace entries. Rejected: a skill is prompt text that reaches every agent, so a change is reviewed by a person at a recorded commit.
- Admit `argument-hint` to the validator's field list. Held as an operator question: Claude Code honours it, the Agent Skills specification does not define it, and keeping the specification means editing every copied skill (research/anthropics-knowledge-work-plugins.md, "Open questions").

## Consequences

Positive:

- Every third-party skill in the kit has a named publisher, a recorded commit and a visible diff against upstream.
- The engineering and operations skills with no counterpart here reach all three agents.
- The rule set is the one the repository already applies to binaries and plugin trees, extended to prompt text.

Negative:

- One to two days of reading and editing for the port, and a review at every bump (research/anthropics-knowledge-work-plugins.md, "Integration options", option 1).
- The cybersecurity pack's 818 skills stay out, so a security engagement gets no vendor skill pack from the kit for now.
- The subset question and the `argument-hint` question need the operator's answer before the port unit starts.

Units created:

- The knowledge-work skills port with its drift test (rollout phase 2).
- A decisions row holding the cybersecurity pack with the three reopening conditions (phase 1).

## Verification

`bdd/third-party-skills.feature`, run by `check.py --holds-today` for the scenarios that hold today:

- `@R-15`: every third-party asset declares its pin and verification; a vendored skill tree is pinned by commit and archive digest (both hold today).
- `@R-16`: the validator admits only the Agent Skills frontmatter fields (holds today).
- `@R-17`: the cybersecurity skills pack is not installed or referenced; the committed-secret scan covers every tracked file (both hold today).
- `@R-18`: a ported skill records its upstream and works without Claude Code command substitutions (target).
- `@R-19`: drift from the recorded upstream commit is visible (target).
