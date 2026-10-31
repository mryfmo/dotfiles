# U107 The committed-secret scan becomes a rule table with entropy, fingerprint allowlists, and every finding reported (plan P-25)

GOAL
`SECRET_PATTERN` in `scripts/validate-agent-assets.py` is one hand-written regex whose generic rule (`token`, `secret`, `password`, `api_key` followed by `=` or `:` and a quoted string) matched two test fixture variable assignments in U101 (rounds 10 and 13), and `validate_no_obvious_secrets()` stops at its first hit, so the second file stayed hidden until the first was fixed. GitHub's secret scanning separates provider patterns from a small set of high-precision generic patterns (https://docs.github.com/en/code-security/reference/secret-security/supported-secret-scanning-patterns), and gitleaks models a rule as id, regex, secret group, entropy threshold, keywords, plus allowlists by path, regex and fingerprint (https://github.com/gitleaks/gitleaks/blob/master/README.md), both read 2026-10-28. This unit restructures the in-repo scan to that model, inside the one script, because `records-sync.sh` copies the validator alone into a tools tree and runs `--mask-secrets` and `--scan-identifiers` from it (read `scripts/orchestrator/records-sync.sh` around the `tools=` block before you start). No external data file, no new dependency.

SCOPE
One branch `feat/secret-scan-rule-table` from `origin/main`. May write: `scripts/validate-agent-assets.py` (the secret rules, the allowlist, `validate_no_obvious_secrets`, `mask_secret_matches`, `identifier_reasons` and whatever they call; nothing else in that file), `tests/unit/test_validate_agent_assets.py`, and, only if an existing fixture must move, the fixture files it names. Nothing else. `tests/unit/test_pr_levers.py` is another unit's file this wave; if its two renamed fixtures (`planted`) would now be allowed by the new allowlist, say so in the report but do not edit it.

CHANGE
1. The rules become one tuple of rows in the script (`SECRET_RULES`), each row a small dataclass or named tuple: `id`, `description`, `regex` (compiled), `secret_group` (int), `entropy` (float or None, Shannon entropy over the secret group, computed in the script), `keywords` (tuple of lower-case substrings that must appear in the text for the rule to run). Provider rules keep today's bodies (`ghp_`, `github_pat_`, `sk-` with the existing bound) with entropy `None`. The generic assignment rules (`api_key`, `password`, `secret`, `token`) become one rule each with the quoted value as the secret group and an entropy threshold of 3.5 (gitleaks' documented example), so `planted = "ghp_" + "A1b2..."` is judged by the provider rule on the literal, not by the assignment shape, and a variable named `token` holding a low-entropy or concatenated string is not a finding. Keep the escape-sequence lookbehinds that `--mask-secrets` depends on, as a documented part of each provider regex.
2. An allowlist table `SECRET_ALLOWLIST` with rows of `rule_id` (or `*`), `path_regex` (repository-relative), `fingerprint` (optional: `<path>:<rule_id>:<line>`), and `reason`. Today's `compactiondb_dummy_secret_fixtures` and `ALLOWED_SECRET_PLACEHOLDERS` move into it as rows. The test fixtures that plant a fake `ghp_` token in `tests/unit/` get rows by path regex with the reason "test fixture, the planted token is split or synthetic".
3. `validate_no_obvious_secrets()` collects every finding across every file (rule id, path, line, the secret masked to its first four characters) and fails once at the end with all of them, never at the first hit. `--mask-secrets` and `--scan-identifiers` keep their exact external behaviour (same exit codes, same message shapes, same masked text) and are driven by the same rules; the tests that pin them must still pass unchanged where they do not depend on the removed assignment-shape behaviour.
4. Tests: a fixture tree with two files each holding a planted provider token asserts both are reported in one run; a low-entropy `<redacted:secret-pattern>

ACCEPTANCE
1. `uv run --no-project --with pyyaml python -m unittest tests.unit.test_validate_agent_assets` passes. 2. `uv run --no-project --with pyyaml scripts/validate-agent-assets.py` over the tree exits 0 on the head (the whole-tree scan; paste the result line). 3. The PR body Contract states: every finding is reported, a finding is suppressed only by an allowlist row with a reason, the masker's output for provider rules is unchanged, and the generic rules now require entropy above the threshold.

TIMEBOX
120 minutes.

FORBIDDEN
No external data file for the rules. No new dependency (gitleaks or other). No weakening of a provider rule. No `# noqa`-style suppression comments in scanned files; suppression is a table row.

CLOSURE
allowlist: the scan is one rule table with provider rows and entropy-gated generic rows, and a finding is suppressed only by a row of the allowlist table with a reason; no suppression lives in scanned text.

TRUST
TRUST: the unit trusts the rule table and the allowlist table as the one judgment of what a secret is; it trusts the provider patterns as published by their vendors and the gitleaks entropy threshold as measured, and it does not read file content for anything but the rules' matches.
Both sections were added 2026-10-31T03:29:18Z by the coordinator under standing order 37; the unit predates U121.

WORKER RULES (standing orders 27, 29, 31, 34; read `preferences.md` lines 23 to 36 in the store)
- Create your worktree from the main checkout and work only there: `git -C ~/Workspace/dotfiles fetch -q origin && git -C ~/Workspace/dotfiles worktree add -b feat/secret-scan-rule-table /tmp/dotfiles-wt/U107 origin/main`. Never write under `~/Workspace`, under `$HOME` config directories, or on any other host. Never `git stash`. No local Bats as evidence.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`. Never push, never open a PR, never merge. The coordinator pushes and opens the PR.
- Before you report, run on the committed head: the test modules your change touches plus `uv run --no-project --with pyyaml python -m unittest tests.unit.test_scratch_git`; ShellCheck 0.11.0 (`shellcheck`, the repository `.shellcheckrc` applies), `shfmt -i 4 -sr -d`, and `scripts/ci/masked-dirname-check.sh` on every touched shell file; `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check`; `uv run --no-project --with pyyaml python -m unittest tests.unit.test_lint_comparisons`; and `uv run --no-project --with pyyaml scripts/generate-agent-configs.py --check` (if it reports a stale output, run the generator without `--check` and commit the regenerated files; never hand-edit a generated file). CI runs the full suite.
- Shell comments are English shdoc. Python runs as `uv run --no-project`. Tests assert behaviour the user observes. Comments explain a non-obvious why only, no phase narration.
- A producer's status is read (standing order 21): a `$(...)` whose status is unchecked is a defect, a failed read is never treated as an absence, and every such decision has a failure-injection test.
- Write the PR body to `/tmp/dotfiles-wt/U107-pr-body.md` with these sections in order: `## Summary` (what and why, under 12 lines), `## Contract` (bullets: what this change guarantees, and what it leaves out), `## Threat table` (one row per touched path: what it does today, what changes, what could go wrong, how the change refuses it), `## Verification` (the commands you ran and their pasted result lines), the line `Program-Unit: regime-cutover/U107`, a blank line, then `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. No absolute home directory path anywhere (write `~/...`), no credential-shaped literal, none of the words in `.orchestration/orchestrate/regime-cutover/redact-words.txt`.
- Conventions: `~/.agents/pstack/skills/poteto-mode/SKILL.md` (Comments, Writing the reply), `~/.agents/pstack/skills/technical-writing/SKILL.md` for the PR body. Principles that apply to this unit: `~/.agents/pstack/skills/principle-model-the-domain/SKILL.md` (a table or registry over branching), `~/.agents/pstack/skills/principle-test-behavior-not-implementation/SKILL.md`, `~/.agents/pstack/skills/principle-fix-root-causes/SKILL.md`.

REPORT
Status, branch, head sha (40 hex), the files changed (`git diff --stat origin/main`), the commands you ran with their result lines, deviations from this brief, anything you could not verify, suggested follow-ups. Facts only. Under 40 lines.

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md`. The plan this unit implements is `handoff/05-remediation-plan.md` in the same store, with the research under `handoff/research/`.
