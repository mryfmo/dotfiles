# mukul975/Anthropic-Cybersecurity-Skills — metadata, packaging, provenance, governance

- Target: https://github.com/mukul975/Anthropic-Cybersecurity-Skills
- Observed: 2026-11-02 (UTC). HEAD of `main` = `54a798831d2266a3ca61ce68a7acb80b81160d57` (2026-08-31T04:32:42Z).
- Scope: metadata, packaging, provenance and governance only. Skill content quality, script correctness and framework-mapping accuracy are out of scope and were not assessed.
- Evidence basis: GitHub REST API (repo, user, releases, tags, contributors, commits, community profile, issue search), raw files on `main`, a blobless `git clone --filter=blob:none` of the repository (245 commits, all tags), the maintainer's homepage, and the skills.sh registry page. Items marked **unverified** could not be confirmed from a primary source; items marked **blocked** hit GitHub API rate limiting (HTTP 403) or required authentication (HTTP 401).
- Method note: no shared method document was present in `hk-research/` or discoverable in the workspace or session history, so this report follows the four requested headings with a facts table, evidence pointers and flags per section.

## 1. Metadata

| Field                                  | Value                                                                                                                                                                                                                                                                                        | Evidence                        |
| -------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------- |
| Repository                             | `mukul975/Anthropic-Cybersecurity-Skills`, id `1166506614`, public, not a fork, not archived, not a template                                                                                                                                                                                 | repos API                       |
| Created / last push / last update      | 2026-02-25T09:47:50Z / 2026-08-31T04:32:44Z / 2026-11-02T04:10:50Z                                                                                                                                                                                                                           | repos API                       |
| Default branch                         | `main`                                                                                                                                                                                                                                                                                       | repos API                       |
| Owner                                  | `mukul975` (user account, not an organization). Display name "Mahipal"; BibTeX in README gives "Jangra, Mahipal". Location "Berlin", blog `Mahipal.engineer`, X handle `Mukul_jangra`. Account created 2018-08-31. 33 public repos, 1,415 followers.                                         | users API                       |
| Description                            | "817 structured cybersecurity skills for AI agents · Mapped to 6 frameworks … agentskills.io standard · Works with Claude Code, GitHub Copilot, Codex CLI, Cursor, Gemini CLI & 20+ platforms · 29 security domains · Apache 2.0"                                                            | repos API                       |
| Homepage                               | `https://mahipal.engineer/Anthropic-Cybersecurity-Skills/` (self-hosted; `has_pages` is false). Page content is stale: headline "754 Cybersecurity Skills", "26 Security Domains", "5 Security Frameworks".                                                                                  | repos API; homepage fetch       |
| Stars / forks / watchers (subscribers) | 35,414 / 4,317 / 267                                                                                                                                                                                                                                                                         | repos API                       |
| Open issues counter                    | 68 (= 26 issues + 42 pull requests)                                                                                                                                                                                                                                                          | repos API; search API           |
| Size / languages                       | 12,737 KB. Python 9,438,852 B, PowerShell 36,674 B, YARA 478 B                                                                                                                                                                                                                               | repos API; languages API        |
| Topics (20)                            | ai-agents, claude-code, cloud-security, cybersecurity, devsecops, ethical-hacking, incident-response, infosec, llm, malware-analysis, mcp, mitre-attack, nist-csf, osint, penetration-testing, red-team, security, security-automation, threat-hunting, threat-intelligence                  | repos API                       |
| Features enabled                       | issues, projects, wiki, discussions, pull requests (creation policy "all"). Downloads off, Pages off. `web_commit_signoff_required` false.                                                                                                                                                   | repos API                       |
| License (GitHub detection)             | Apache-2.0 (`LICENSE`, 11,255 B). Appendix notice reads "Copyright 2026 mukul975".                                                                                                                                                                                                           | repos API; `LICENSE`            |
| Community health                       | 100%. Detected: README, LICENSE, CODE_OF_CONDUCT (Contributor Covenant), CONTRIBUTING. Not detected: issue template (API null, though six template files exist under `.github/ISSUE_TEMPLATE/`), pull request template (absent).                                                             | community/profile API; git tree |
| Citation metadata                      | `CITATION.cff` (cff 1.2.0, type software): title "Anthropic-Cybersecurity-Skills", author "Mahipal" alias `mukul975` with personal email, license Apache-2.0, **version "1.1.0", date-released 2026-03-21** (stale; latest release is v1.3.0 on 2026-06-22).                                 | `CITATION.cff`                  |
| Root tree                              | `.claude-plugin/`, `.github/`, `.gitignore`, `AGENTS.md`, `ATTACK_COVERAGE.md`, `CITATION.cff`, `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, `LICENSE`, `README.fr.md`, `README.md`, `SCOPE.md`, `SECURITY.md`, `SUPPORT.md`, `assets/`, `docs/`, `index.json`, `mappings/`, `skills/`, `tools/` | contents API                    |

### Skill-count drift across surfaces

| Surface                                                                                        | Count stated                                                                                              |
| ---------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| GitHub description, `CITATION.cff`, `SCOPE.md`, `AGENTS.md`, `.github/copilot-instructions.md` | 817                                                                                                       |
| README badges and headline, `plugin.json`, `marketplace.json`, `index.json` `total_skills`     | 818                                                                                                       |
| README body (framework-coverage paragraph, domain-table footer)                                | 817                                                                                                       |
| Homepage                                                                                       | 754                                                                                                       |
| skills.sh registry                                                                             | 834                                                                                                       |
| Git tree on `main`                                                                             | 818 directories under `skills/`, each with `SKILL.md`; 817 carry a per-skill `LICENSE`; 4,484 files total |

The README and manifests are rewritten by CI on each skills change (see §2), while the GitHub description, CITATION and copilot instructions are hand-maintained and have lagged.

### Naming and affiliation

- The repository name begins with "Anthropic". The README carries a boxed notice: "Community Project — This is an independent, community-created project. Not affiliated with Anthropic PBC." The footer repeats it.
- That disclaimer first appeared in commit `4ed6f49` (2026-03-11, "chore: fix license, add disclaimer, quick start, GitHub topics, issue templates"), fourteen days after the repository was created. The initial README (2026-02-25) had no disclaimer.
- The v1.0.0 release notes (published 2026-03-11, still live) give the clone URL, issue tracker and "Repository" link as `https://github.com/anthropics/cybersecurity-skills`. That URL returns HTTP 404 today. The notes were never corrected.
- `tools/README.md`, `.github/copilot-instructions.md` and the homepage all use the "Anthropic Cybersecurity Skills" name without the disclaimer in their titles; the homepage shows the disclaimer as a banner link.

## 2. Packaging and distribution

### Artifact shape

- Content-only repository. Each skill is a flat directory `skills/<kebab-name>/` containing `SKILL.md` (YAML frontmatter + Markdown), `references/`, `scripts/` (commonly `agent.py`), optional `assets/`, and a per-skill `LICENSE`. `SCOPE.md` states 817/817 have `SKILL.md`, `references/`, `scripts/`; the tree on `main` confirms 818 `SKILL.md` and 817 per-skill `LICENSE` files.
- Per-skill `LICENSE` files resolve to three distinct blobs: 814 copies identical to the root Apache-2.0 file, 2 copies of Apache-2.0 with "Copyright 2025 mukul975", 1 copy of Apache-2.0 with "Copyright 2026 dakshverma23". All Apache-2.0.
- `SKILL.md` frontmatter across all 818 skills (fetched from the clone): `license:` is `Apache-2.0` in 818/818; `version:` is `"1.0"` in 633 and `"1.0.0"` in 185 (two formats; the README example shows `"1.2"`); framework blocks present: `mitre_attack` 806, `nist_csf` 805, `d3fend_techniques` 139, `nist_ai_rmf` 97, `mitre_f3` 94, `atlas_techniques` 93 (README states 805/804/139/97/94/93, one behind on ATT&CK and CSF).
- `index.json` (447,124 B) is a generated catalogue: top-level keys `version`, `generated_at`, `repository`, `domain`, `total_skills`, `skills`; each entry has `name`, `description`, `domain`, `path`. Current values: `version` **"1.1.0"** (never bumped by any workflow), `generated_at` 2026-08-24T10:40:36Z, `total_skills` 818.
- `mappings/attack-navigator-layer.json` is checked into the tree. Its README says "Navigator layer v4.5 format, Enterprise ATT&CK v14", while the main README says all mappings were revalidated against ATT&CK v19.1. The README also says the layer is "included in the v1.0.0 release assets"; no release has any asset (see below).
- No `package.json`, `pyproject.toml`, `requirements.txt` or lockfile at HEAD. A `package.json` was added and removed on 2026-02-25 (commits `18393eb`, `f0b3f50`). The only tooling dependency is PyYAML, installed ad hoc by `pip install pyyaml` in CI and in the documented local commands.

### Distribution channels

| Channel                              | Mechanism                                                                                                                                              | Notes                                                                                                                                                                                                                                                                                                               |
| ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Git clone                            | `git clone https://github.com/mukul975/Anthropic-Cybersecurity-Skills.git`                                                                             | Primary. README Quick start "Option 2".                                                                                                                                                                                                                                                                             |
| skills.sh CLI                        | `npx skills add mukul975/Anthropic-Cybersecurity-Skills`                                                                                               | README "Option 1 (recommended)". The CLI reads the GitHub repository directly; nothing is published to npm by this project. skills.sh lists 834 skills and 109.3K total installs as of 2026-11-02.                                                                                                                  |
| Claude Code plugin marketplace       | `.claude-plugin/marketplace.json` + `.claude-plugin/plugin.json`; homepage documents `/plugin marketplace add mukul975/Anthropic-Cybersecurity-Skills` | marketplace: name `anthropic-cybersecurity-skills`, owner `mukul975` (with personal email), one plugin `cybersecurity-skills`, `source: "./"`, version 1.3.0, license Apache-2.0, category security, 9 keywords. plugin.json: name `cybersecurity-skills`, version 1.3.0, description "818 cybersecurity skills …". |
| Third-party indexes listed in README | VoltAgent/awesome-agent-skills, ottosulin/awesome-ai-security, RoggeOhta/awesome-codex-cli, SkillsLLM, Openflows, NeverSight/skills_feed               | Not verified here.                                                                                                                                                                                                                                                                                                  |
| Homepage badges                      | Trendshift repository badges, Star History rank badge                                                                                                  | Promotional, not distribution.                                                                                                                                                                                                                                                                                      |

No PyPI, npm, Homebrew, container image or GitHub Packages artifact exists for this project. Every channel resolves to the Git tree at `main` HEAD (or a user-chosen ref).

### Releases and versioning

| Tag    | Date       | Tag type                              | Assets | Skills at tag |
| ------ | ---------- | ------------------------------------- | ------ | ------------- |
| v1.0.0 | 2026-03-11 | lightweight (points at `dfea41c`)     | 0      | 734           |
| v1.1.0 | 2026-03-21 | annotated (tagger mukul975, unsigned) | 0      | 753           |
| v1.2.0 | 2026-04-06 | lightweight (`c0ab6cf`)               | 0      | 754           |
| v1.3.0 | 2026-06-22 | lightweight (`101ca0b`)               | 0      | 817           |

- Four releases in four months, none since 2026-06-22. Main has moved one skill (817 → 818) and 30+ commits past v1.3.0 without a release.
- No release carries assets, checksums, SBOM, signature or SLSA/attestation. No tag is cryptographically signed.
- Version bump automation: `sync-marketplace-version.yml` fires on `release: published` and rewrites `marketplace.json` and `plugin.json` to the tag version, committing to `main` as `mukul975 <mukuljangra5@gmail.com>` with `GITHUB_TOKEN`. The v1.3.0 notes say this fixed `plugin.json` being "stuck at 1.0.0".
- Count sync automation: `update-index.yml` fires on push to `main` touching `skills/**`, regenerates `index.json`, and regex-rewrites the skill count into README badges/phrases and both plugin manifests, committing as the maintainer identity. It does not bump `index.json`'s `version` field.
- Semantic versioning is nominal: minor bumps for content additions; no changelog file (release bodies serve as changelogs).

### Integrity and supply-chain posture

- Consumers receive whatever is at `main` HEAD with no pinning guidance, hash manifest or signature. Open issue #162 (2026-10-22, "Intake accepts submissions with unfilled placeholders — no content verification") proposes per-file content-hash manifests and an advisory scan at intake; unanswered as of observation.
- GitHub Actions use `actions/checkout@v4` by tag, not by commit SHA. Three of four workflows have `contents: write` and push to `main` directly.
- `.gitignore` excludes `.claude/`, `teams/`, `launch/`, `extract_attack.py`, `AUDIT_REPORT.md`, model-weight extensions and `node_modules/`.
- No Dependabot or Renovate configuration; nothing to update beyond PyYAML and Actions versions.

## 3. Provenance

### Origin

- Root commit `22a7ab1462aa0ed29a08f73e8faa2cba2dd9ba5c`, 2026-02-25T10:47:44+01:00, author `mukul975 <mukul975@users.noreply.github.com>`, message "Initial commit - 611 cybersecurity skills across all subdomains". It adds 1,765 files across 611 skill directories plus `.gitignore` and `README.md`. The initial README states "License: MIT" and a nested layout `skills/cybersecurity/{skill-name}/`.
- The same morning (10:51–11:22 local) 14 further commits add `marketplace.json` ("index of 607 cybersecurity skills"), `index.json`, `.claude-plugin/`, issue templates, CI workflows, a README overhaul, "GitHub launch playbook files - legal, community, mappings, launch content", "launch outreach docs: awesome lists, conferences, metrics tracker", "launch content: HN post, Reddit posts, Twitter thread, LinkedIn, Dev.to article", then "Remove unnecessary files", then the Code of Conduct. `launch/` was later gitignored and `launch/twitter-thread.md` untracked (2026-03-11).
- 2026-03-10/11 (21:02–01:48 local): one commit adds "folder anatomy (scripts/agent.py + references/api-reference.md) for 648 cybersecurity skills", another completes it "for all 649 skills + update LICENSE to Mahipal", another fixes frontmatter so "all 649 skills now pass CI validation". Then roughly 85 skills land in batches of 4–10 per commit at intervals of one to three minutes (00:37–01:21), interleaved with CI "auto-update index.json" commits. Commit `7944892` "correct license from Apache-2.0 to MIT for batch 2 skills" is followed 50 minutes later by `4ed6f49` "fix license, add disclaimer …". v1.0.0 was tagged at 01:48.
- The cadence (hundreds of multi-file skills per hour) indicates machine generation of the catalogue. The project's own documents acknowledge generated-content debt: `CONTRIBUTING.md` says "Roughly 980 pre-existing failures are grandfathered in `tools/lint-baseline.json`", and `tools/README.md` says a parser bug "shipped 604 of 817 descriptions broken in `index.json`".

### History shape

| Month (2026) | Commits |
| ------------ | ------- |
| Feb          | 15      |
| Mar          | 111     |
| Apr          | 26      |
| May          | 5       |
| Jun          | 45      |
| Jul          | 8       |
| Aug          | 35      |
| Sep–Nov 2    | 0       |

- 245 commits total, 19 merge commits. Last commit 2026-08-31 ("chore: update contributor wall", CI-authored). No push in the nine weeks before observation while issues and PRs continued to arrive (latest issue #166 on 2026-10-29, latest PR #165 on 2026-10-26).
- Skill count over time: 611 (2026-02-25) → 649 (2026-03-11) → 734 (v1.0.0) → 753 (v1.1.0) → 754 (v1.2.0) → 817 (v1.3.0) → 818 (HEAD).

### Authorship

GitHub contributors API (linked accounts): mukul975 189, valorisa 18, juliosuas 13, Daytona39264 3, kevglynn 2, andrewibrah 2, and 1 each for Bortlesboat, DevRedious, ioxoi, OctoBored, shanujans, farhan6667, dakshverma23, nyxst4ck, and `claude[bot]`. The README contributor wall lists 14 humans (bots excluded by `tools/update-contributors.py`).

`git shortlog` shows 23 author identities. The maintainer appears under four: `mukul975 <mukul975@users.noreply.github.com>` (82), `mukul975 <mukuljangra5@gmail.com>` (52, includes all CI bot commits, which are configured to use this identity), `Mahipal <42860185+mukul975@users.noreply.github.com>` (38), `Mahipal <mukuljangra5@gmail.com>` (17). Combined: 189 of 245 commits (77%).

Identities not linked to a GitHub account:

- `MAGI <magi@MAGIs-Mac-mini.local>`: 8 commits, 2026-03-17 to 03-22, UTC-6, all on the AWS Detective skill and ATT&CK mappings "per CodeRabbit review" (fixes #1, #6). Same timezone and subject matter as `juliosuas`; attribution to a person is **unverified**.
- `Rida <ridaqp@LAPTOP-1AL9622A.localdomain>`: 1 commit, 2026-07-08.
- `Homan Ansari`, `Andrew Barnes`, `Syed Farhan Ahmed`, `Kevin Glynn`, `Julio César Suástegui`, `Shanujan Suresh`: personal emails that GitHub has linked to the accounts above.

AI-authored commit on `main`: `fbc47b7` (2026-04-21) by `claude[bot]`, "fix: replace word-split tags with domain-specific cybersecurity tags", trailer `Co-Authored-By: Claude Code <noreply@anthropic.com>`. Several closed PRs (e.g. #147) carry the "Generated with Claude Code" footer. `CONTRIBUTING.md` requires AI-assisted PRs to disclose it and to have a human run the commands.

Frontmatter `author:` field across 818 `SKILL.md` files: `mahipal` 770, `mukul975` 30 (maintainer total 800, 98%), `andrewibrah` 7, `team-cybersecurity` 7, `juliosuas` 2, `devredious` 1, `dakshverma23` 1. Only seven distinct values, versus 14 linked GitHub contributors. A GitHub user `Team-Cybersecurity` (id 83020170) exists with no public repositories and no commits in this repository; its relationship to the maintainer is **unverified**, although `CONTRIBUTING.md` requires `author` to name an account able to answer review questions.

### Commit and tag signing

- `git log --format=%G?`: 203 commits `N` (unsigned), 42 `E` (signature present but cannot be checked without the public key; these include GitHub-web-flow merges and some maintainer commits). GitHub's API reports HEAD `54a7988` as `verified: false, reason: unsigned`.
- Tags: v1.1.0 annotated and unsigned; v1.0.0, v1.2.0, v1.3.0 lightweight.
- Bot commits from the three write-enabled workflows are authored as the maintainer's personal name and email, so CI output and human commits are not distinguishable by author metadata.

### External signals

- skills.sh: 109.3K installs, 834 skills listed (the registry count exceeds the tree; cause not determined).
- Maintainer's site has a "Black Hat USA 2026 Arsenal Lab — Anthropic Cybersecurity Skills Recap" page and the homepage shows a "Featured Black Hat USA 2026 · Arsenal Lab" link to the Black Hat presenter list. The blackhat.com listing itself was not fetched; **unverified**.
- Growth: Star History tweet embedded on the homepage shows 16.1k stars on 2026-06-18; homepage star button showed 27.4k when the Black Hat recap was indexed; API shows 35,414 today.
- README "Featured in" and "What people are saying" sections cite X posts and a Medium article; not verified.

## 4. Governance

### People and decision rights

- Single maintainer. `SUPPORT.md`: "This project is maintained by one person alongside other work." `CONTRIBUTING.md`: "I review every pull request myself." `SCOPE.md`: "Scope decisions are mine to make, but they should be arguable in the open."
- No organization, no `CODEOWNERS`, no `MAINTAINERS` file, no listed co-maintainers or successor plan. Bus factor is 1.
- Enforcement contact for the Code of Conduct, marketplace owner email, CI committer email, and CITATION author email are all the maintainer's personal Gmail address.
- Funding: `.github/FUNDING.yml` → GitHub Sponsors `mukul975` and a PayPal.me link.

### Policy documents on `main`

| Document                          | Size     | Key provisions                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| --------------------------------- | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `CONTRIBUTING.md`                 | 13,922 B | One skill per PR; required frontmatter template; five local validators; description must contain a `Use when`, `Keywords:` and `Do not use for … use <slug>` clause; new skills that overlap existing ones are redirected to extend the existing one; 14-day stale-close after review request; mandatory disclosure of self-links, vendor affiliation and AI assistance ("a human must have run the commands"); 34 canonical subdomains; contributions licensed Apache-2.0. States that most of the policy "is new" and applies prospectively. |
| `SCOPE.md`                        | 8,848 B  | Repository is a catalogue only. Out of scope: runtimes/engines/MCP servers, applications built on the catalogue, a second toolchain, process/roadmap documents, editor configs, product-shaped skills, bulk imports. Offensive and dual-use content is explicitly in scope "subject to the authorised-use notice in README.md". Acknowledges a months-long review backlog.                                                                                                                                                                     |
| `SECURITY.md`                     | 1,644 B  | Report via GitHub private security advisory; acknowledgment within 48 h, triage within 1 week, fix "typically within 2 weeks"; in scope: harmful commands/scripts, instructions leading to unauthorised access, leaked sensitive data, compromised external references; credit in changelog.                                                                                                                                                                                                                                                   |
| `SUPPORT.md`                      | 2,589 B  | No SLA; "some pull requests have waited months"; Discussions for questions, Issues for defects.                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| `CODE_OF_CONDUCT.md`              | 5,477 B  | Contributor Covenant 2.1; enforcement via maintainer's personal email.                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| `AGENTS.md`                       | 2,472 B  | Instructions for AI agents editing the repo: PyYAML-only frontmatter parsing, run the five validators, `index.json` is generated.                                                                                                                                                                                                                                                                                                                                                                                                              |
| `.github/copilot-instructions.md` | —        | Maintainer-owned agent instructions; states "MITRE ATT&CK v14", contradicting README's v19.1.                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `.github/ISSUE_TEMPLATE/`         | 6 files  | `bug-report.yml`, `new-skill-request.yml`, `skill-improvement.yml`, legacy `new-skill.md`, `improve-skill.md`; `config.yml` disables blank issues and links to advisories and Discussions.                                                                                                                                                                                                                                                                                                                                                     |
| README authorised-use notice      | —        | "Authorized & lawful use only … Only use them against systems you own or have explicit written permission to test … You are solely responsible for how you use these skills."                                                                                                                                                                                                                                                                                                                                                                  |

Absent: pull request template, `CODEOWNERS`, `GOVERNANCE.md`, `CHANGELOG.md`, Dependabot config, DCO or CLA, trademark statement.

### Review and merge process

- CI (`validate-skills.yml`) runs on push and PR touching `skills/**`, `tools/**` or itself: guard against regex frontmatter parsers; `validate-skill.py --all`; `validate-agentskills.py --strict`; `generate-index.py --check` (PRs only, since 2026-08-24 to avoid racing the index workflow); `lint-descriptions.py --all --stats` against a grandfathered baseline; `detect-collisions.py --max-unreviewed 55` (ratchet "sitting exactly at its ceiling"); duplicate-name check; stats summary. Documentation-only PRs trigger no checks.
- Branch protection on `main`: **blocked** (HTTP 401). Workflows push to `main` with the default `GITHUB_TOKEN`, which implies either no required reviews or a bypass for Actions; not confirmed.
- Human review is one person. Merges observed as squash/merge commits by the maintainer; 19 merge commits in history.

### Throughput (as of 2026-11-02)

| Queue                               | Count        |
| ----------------------------------- | ------------ |
| Issues open / closed                | 26 / 19      |
| PRs open / merged / closed unmerged | 42 / 23 / 35 |

- 23 merged PRs over eight months; the most recent merge is #129 on 2026-08-24. 35 PRs were closed without merge, including #147 (2026-09-25, a Claude-Code-generated subdomain normalisation sweep closed five minutes after opening). That closure is the last observed repository action; everything filed since (PRs #164, #165; issues #162, #166) shows no response.
- Open issue #166 (2026-10-29) is an unfilled template ("[IMPROVE] skill-name-here"), the failure mode issue #162 complains about.
- Issue #119 (2026-08-01, "Security: Urgent vulnerabilities found on mrkt.land") was redacted and closed within four minutes; spam.
- Published security advisories: **blocked** (HTTP 403); none are referenced in release notes or README.

### Commercial and promotional entanglement

- README places, above the fold, a "GARS-2026 Survey" badge and section ("I'm running a global academic study … Supervised by SRH Berlin … You get 50 Casky Tokens for early access to casky.ai") and a "Playground — Casky.ai" badge and section linking to a waitlist with `utm_campaign=cohort_launch`.
- `CONTRIBUTING.md` bans undisclosed self-links and says "Where the README links to something of mine, it should be labelled as mine." The survey section is written in the first person; the Casky.ai playground section does not state the maintainer's relationship to Casky.ai. The relationship is **unverified** here but the omission is inconsistent with the stated policy.
- The maintainer's personal site describes commercial-adjacent activity (conference briefings, tooling); the repository is presented as the maintainer's flagship project.

## 5. Flags

1. **Single-maintainer, nine weeks without a push, 42 PRs open.** All review, merge, release, security-response and CoC enforcement authority sits with one personal account. The 48-hour acknowledgment promise in `SECURITY.md` is not backed by any second responder.
2. **No integrity controls on distribution.** All channels (git, `npx skills add`, Claude plugin marketplace) deliver `main` HEAD; no signed tags, no release assets, no checksums or attestations; CI pushes to `main` under the maintainer's identity with `GITHUB_TOKEN`; Actions pinned by tag only. Issue #162 asking for hash manifests is unanswered.
3. **Naming.** "Anthropic" in the repository name with a disclaimer added two weeks after creation; v1.0.0 release notes still point at a non-existent `anthropics/cybersecurity-skills` repository.
4. **Metadata drift.** Skill counts range from 754 (homepage) to 834 (skills.sh); `CITATION.cff` pinned at 1.1.0; `index.json` `version` stuck at 1.1.0; copilot instructions and Navigator layer say ATT&CK v14 while README says v19.1; README claims release assets that do not exist.
5. **Bulk-generated origin.** 611 skills in the root commit, ~85 more in 45 minutes on launch night, and self-reported technical debt (980 grandfathered lint failures, 604 broken descriptions at one point). Governance documents written later (SCOPE, revised CONTRIBUTING) explicitly apply only prospectively.
6. **License churn at launch.** README said MIT on day one; per-skill licenses flipped Apache → MIT → Apache within an hour on 2026-03-11. Current state is uniformly Apache-2.0 (root file plus 817 per-skill copies, three blob variants).
7. **Promotional content in README** (survey with token incentive, Casky.ai waitlist) without the affiliation label the project's own contribution policy requires.
8. **Unlinked committer identities** (`MAGI@…local`, `Rida@LAPTOP…localdomain`) and one AI-bot-authored commit on `main`; author metadata cannot distinguish CI, human and AI commits.

## 6. Source index

- `https://api.github.com/repos/mukul975/Anthropic-Cybersecurity-Skills` (repo, languages, tags, releases, contributors, commits, community/profile, contents/)
- `https://api.github.com/users/mukul975`
- `https://api.github.com/search/issues?q=repo:mukul975/Anthropic-Cybersecurity-Skills+…` (is:pr is:merged / is:open / is:closed is:unmerged; is:issue is:open / is:closed)
- `https://api.github.com/repos/mukul975/Anthropic-Cybersecurity-Skills/issues?state=all&per_page=100` (partial; issues #162, #164, #165, #166 bodies)
- Raw files on `main`: `README.md`, `CONTRIBUTING.md`, `SCOPE.md`, `SECURITY.md`, `SUPPORT.md`, `AGENTS.md`, `CITATION.cff`, `LICENSE`, `.gitignore`, `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `.github/workflows/*.yml`
- Blobless clone at `$TMPDIR/hk-research/_src/acs/repo` (HEAD `54a7988`): `git rev-list --count`, `git shortlog -sne`, `git log --format=%G?`, `git for-each-ref refs/tags`, `git cat-file -p v1.1.0`, `git diff-tree --root 22a7ab1`, `git ls-tree` of `skills/`, `.github/`, `tools/`, `docs/`, `mappings/`, `assets/`, `git show` of `index.json`, `tools/README.md`, `mappings/README.md`, `.github/FUNDING.yml`, `.github/ISSUE_TEMPLATE/config.yml`, `.github/copilot-instructions.md`, `CODE_OF_CONDUCT.md`, per-skill `LICENSE` blobs, root-commit `README.md`, and all 818 `skills/*/SKILL.md` files (frontmatter tallied by regex on `license`, `author`, `version` and framework keys)
- `https://github.com/team-cybersecurity` (profile exists, no public repositories)
- `https://www.skills.sh/mukul975/anthropic-cybersecurity-skills`
- `https://www.mahipal.engineer/Anthropic-Cybersecurity-Skills/` and search hit `https://www.mahipal.engineer/blackhat-usa-2026`
- `https://github.com/anthropics/cybersecurity-skills` (HTTP 404)
- Blocked: `branches/main/protection` (401); `security-advisories`, `pulls`, `contents/.github`, `contents/tools`, `contents/docs`, `contents/mappings`, `git/trees/…` (403 rate limit; tree data taken from the clone instead)
