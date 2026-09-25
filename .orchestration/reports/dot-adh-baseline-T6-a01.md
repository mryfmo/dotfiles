# dot-adh-baseline-T6-a01
status: ready_for_review
cost: n/a

## Completed
Created task-specified worktree /Users/mryfmo/Workspace/dotfiles/.claude/worktrees/adh-baseline, branch docs/adh-integrated-plan-baseline, from origin/main. Copied reviews with rsync -a --exclude .DS_Store.
197 checksum entries OK; zero non-OK lines. All 196 PACKAGE_MANIFEST.json listed files exist.
198 total files; 5072 KiB allocated size. Exact byte total is in validation.
Requested secret-pattern scan via rg --hidden --no-ignore: empty output, exit 1 (no matches).
rsync checksum dry-run against canonical source is empty: copied tree byte-identical excluding .DS_Store. No .DS_Store found in copy. Baseline files were never edited.

## Explicit stop condition
Task step 5 says to stop if any repository tool scans reviews.
scripts/validate-agent-assets.py:1039 (removed-skill scan) and :1080 (obvious-secret scan) traverse ROOT.rglob("*"), excluding only .git/site/__pycache__ plus a few named fixtures. Both include this baseline.
CI shfmt/shellcheck instead select only install/scripts/setup files; reviews is outside those selectors. Makefile format scans "." broadly, but no shell files were found in this baseline.

Stopped before unit suite, asset validator execution and git add. No test failure is claimed; this is a scope-policy blocker, not a demonstrated validation failure. git diff --check is empty but baseline remains untracked/not staged.

## Narrowest next action
Prefer explicit permission to run existing read-only validators unchanged, retaining secret scanning. If semantic removed-skill policy conflicts with frozen evidence, narrow any exclusion to reviews/ADH_Integrated_Plan/** in that specific semantic scan only, not all reviews or the security scan. Do not edit baseline or .gitignore. No exclusion implemented.

[memory:failure] Immutable baseline import pauses on task-defined scanner-scope gate.
Memory command (canonical repo): `python3 .claude/hooks/contextdb_cli.py memory add --kind failure --scope project --content 'dot-adh-baseline-T6-a01: byte-identical copy validates 197 SHA256 entries and 196 manifest files, secret-pattern scan empty. Task requires stopping if any repo validator scans reviews; validate-agent-assets.py recursively scans all files in removed-skill and obvious-secret checks, including this immutable baseline. No stage or baseline edits; request orchestrator decision before continuing, preserve secret scanning.'`
Memory ID: 23fa8495-ff06-46c4-b1a1-bec496c0864b.

## Authorized continuation — final result
status: ready_for_review
cost: n/a

Explicit approval received to run read-only scans unchanged. make unit-test passed: 409 tests. Asset validator passed. No exclusions or baseline edits were needed.
Ran git add reviews in .claude/worktrees/adh-baseline; exactly 198 files are staged, all under reviews/. No .DS_Store or other paths staged. git diff --cached --check passed, unstaged tracked diff is empty, and checksum rsync comparison to canonical source remains empty. Total content size: 4,756,933 bytes (5072 KiB allocated).
Required Crit gate passed using .agents/worklog/codex/t6-review.md with parsed resolved evidence in t6-crit.json. Review approves byte-preserving import scope, not ADH plan semantics.
No commit, push, PR, local Bats, .gitignore changes or source modifications. Orchestrator can commit the staged baseline.
[memory:decision] Preserve immutable baseline and existing security scans; read-only validators need no exclusion for this import.
Memory command (canonical repository): `python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'dot-adh-baseline-T6-a01: orchestrator explicitly permits existing read-only validator scans of reviews. Unchanged unit suite (409 tests) and asset validator pass with ADH baseline present. Stage only the 198 byte-identical baseline files, excluding .DS_Store; preserve checksum-protected content and security scans without exclusions.'`
Memory ID: 5d5509a2-05b6-4749-8f59-5360d69bc619.
