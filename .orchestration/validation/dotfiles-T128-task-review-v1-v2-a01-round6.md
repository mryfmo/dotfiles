---
reviewed_at: 2026-10-10T22:28:36Z
reviewer: claude-review-dot-a001
profile: review
session: 2089b04f-f9c7-498b-86c5-76f2140048d5
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@25b36e1c6e41aed8014af28911dbe9744bacc77a37ad6c1e445b35a03c5030be
task: dotfiles-T128-task-review-v1-v2-a01
round: 6
previous: .orchestration/validation/dotfiles-T128-task-review-v1-v2-a01-round5.md
files:
  - dotfiles-T128-v1-task-schema-a01@472267ac53ba2deb7e87552283e68eb5c1295b11ce05dc82f18031364e435d0a
  - dotfiles-T128-v1b-pr-caps-a01@1b30a793a420000af3059060e9571d6107a2b9b0c9a8392e1d72bff73172e71d
  - dotfiles-T128-v1c-regime-ci-check-a01@98e1e6e9a0ce2634a31fdae94bc83c7a7d06c6b9fd49a61a071f5cb138ed91cd
  - dotfiles-T128-v2-audit-schema-and-runner-a01@7e1786adc0d9fe3b6d3dc2f1eb026ca3653d90f7443b75f9860affdf44928c2a
verdicts:
  dotfiles-T128-v1-task-schema-a01: "revise: R6-1 first-segment regex admits scripts*"
  dotfiles-T128-v1b-pr-caps-a01: ready
  dotfiles-T128-v1c-regime-ci-check-a01: ready
  dotfiles-T128-v2-audit-schema-and-runner-a01: "revise: R6-2 fallback refuses a head that changes .claude/skills/**"
---

# Task-file review round 6: the four files after design v6

PyYAML check: each file's invariant equals design v6 byte for byte; all four pointers name the round-6 receipt; the hashes match the TASK. The design itself is at revise this round for INV-7 (two reviews); none of these four tasks implements INV-7, so their sentences will not move when INV-7 does, but their pointers will, as before.

## V1: revise

- Applied: legacy exemption only under .orchestration/tasks/ with --no-grandfather (item 3); wildcard entries classified by literal prefix with scripts/* and home/** deriving design (item 2); tests for the branch copy, --no-grandfather, ['*'], ['**'], ['*/x'] and the two wildcard derivations (item 4).
- R6-1: the schema pattern for allowed_files entries, ^[A-Za-z0-9_.-][^/]*(/.*)?$ (item 1), requires only a literal first character; scripts* or s?ripts/x pass it, while INV-1 says the first segment is literal and INV-12 names "a wildcard first segment" as a gaming path. Use ^[A-Za-z0-9_.-]+(/.*)?$ and add scripts* to the schema-error tests.

## V1b: ready

Item 2 compares ids as a set and sentences byte for byte against the design read from main; item 3 adds the one-character-difference fixture.

## V1c: ready

Step (a) runs the validator with --no-grandfather on branch copies; the rest is unchanged since round 5.

## V2: revise

- Applied: codex exec -C <main> --add-dir <worktree> --output-schema <main>/schemas/audit.json; the claude fallback from the main checkout with --add-dir <worktree> and the schema from main; validation against main's schema (item 2).
- R6-2: the headless page says bare mode loads skills from an --add-dir directory's .claude/skills/ folder, so a head that adds or edits .claude/skills/** reaches the fallback's context. Before the fallback, run git -C <worktree> diff --quiet origin/main -- .claude/skills; when it fails, exit 2 (blocked) with that reason instead of running claude, and add the sentence as a premise. The codex path is unaffected.

The two items are one line each; the pointer update for the INV-7 fix can ride in the same edit.
