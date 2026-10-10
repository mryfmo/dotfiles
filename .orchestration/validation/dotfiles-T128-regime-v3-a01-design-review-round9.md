---
reviewed_at: 2026-10-10T22:46:42Z
reviewer: claude-review-dot-a001
profile: review
session: 2089b04f-f9c7-498b-86c5-76f2140048d5
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@015e32530307a3fe65b8f9a328a85ce99a8beda72602f790c6822d17ad34cb30
design_hash_kind: whole-file sha256 (the canonical hash tool is V1's deliverable)
task: dotfiles-T128-design-review-a01
round: 9
previous: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round8.md
premises:
  1: holds (uv run --no-project --with jsonschema --with pyyaml prints 4.26.0 6.0.3; no --with jsonschema in Makefile or workflows)
  2: holds (troubleshooting and events pages fetched this session)
  3: holds for the CLI part (codex exec --help lists --output-schema; --full-auto and -a rejected); the server-side strict flag rests on codex-factsheet.md:17's source read, not re-read here
  4: holds (headless page fetched; the four quoted statements are on it)
  5: holds (best-practices page, verbatim)
  6: holds (stat of the four T119 audit files; history 21:26Z to 08:32Z)
  7: holds (Codex hooks page and Claude hooks Stop section fetched)
  8: holds (the named transcript: 5168 usage entries, fields as stated)
  9: holds (20 rows by default; the whole history with a limit)
  10: holds (events page: "only trigger a workflow run if the workflow file exists on the default branch")
  11: holds (headless page: bare mode "loads skills from its .claude/skills/ folder" for an --add-dir directory)
  12: holds (auto-mode-config page: "Content-scoped ask rules ... are evaluated before the classifier and always force a permission prompt, even in auto mode"); see the caveat under INV-1 below
---

# Design review: dotfiles-T128-regime-v3-a01, round 9 (six invariants after the second Codex review)

Round 8's items (INV-1 waiver owner and routing, INV-5 once-per-head versus re-audit, the waiver record outside the sandbox write roots) are acknowledged for v10 and are not repeated here except where v9 touches them.

## The six changed invariants and V5c

INV-2: accepted. 15 files outside .orchestration/, 500 added lines outside tests/, .orchestration/ and the data list, and a separate 1000 under tests/ bound both halves of the review load; V1b carries tests_added.

INV-3: accepted. The exact selector run on the head (pass) and on previous_head (fail or absent) in a required revise-check job is the deterministic fact the Codex P2 asked for; the main-pinned existence-and-diff check and the host gate's history check stay. Note for V3c: the selector form tests/<file>::<name> is pytest's, while make unit-test runs unittest discover (Makefile:185) and pytest is not installed there; name the runner the revise-check job uses (uv run --no-project --with pytest -m pytest <selector>) or switch the selector to unittest's dotted form, so the worker does not have to ask.

INV-4: accepted. Every premise dispositioned by each reviewer and the auditor, with the schema requiring the complete map, replaces sampling with a record; this receipt's front matter is the first such map.

INV-5: rejected: the Round-9 section says v9 puts the .claude/** refusal inside the invariant, but the sentence at line 50 carries no refusal clause; the refusal exists only in premise 11 and in V2's task text (line 53), which is the Codex P1 at line 49 restated. Right: add to INV-5 "the fallback runs only when git diff --quiet origin/main <head> -- .claude holds; otherwise the runner exits 2 blocked and the head is audited by codex alone". Round 8's once-per-head wording fix still applies to the same sentence.

INV-10: accepted. The draft PR's server-side created_at and the after list against acceptance records make both timings computable; V1 adds the after key to the schema.

INV-12: rejected: as written, main-tests blocks every intentional behavior change of a tested script. A PR that changes a rule a main test pins fails main's old test by design, so the only way through is a prior tests PR whose new tests fail on main, which the unit-test job refuses. Right: main-tests runs main's test modules against the PR's scripts for the modules the PR's task.md allowed_files do not list (regression protection outside the task's scope; a PR cannot lower that bar), while modules the task lists run in the PR's version under unit-test with their diff bounded by INV-2's tests cap and read by the design-tier audit. State that split; INV-1's workflow-edit refusal keeps the job itself out of the PR's hands, as section 9 says.

V5c: the wave exists (line 182) with its implementing_tasks entry; the Order line (line 185) omits it; place it after V5b.

## INV-1 caveat from the auto-mode page (for v10)

The page that confirms premise 12 also says an ask rule matches only a command written the way the rule expects ("A push Claude writes another way ... doesn't match the rule"), so Bash(scripts/regime-waive.sh *) is bypassed by bash scripts/regime-waive.sh, ./scripts/regime-waive.sh, a make target or a copy of the script. The ask rule is therefore not the friction; the record location is. Round 8's anchor becomes the mechanism: regime-waive.sh writes under a directory outside every seat's sandbox write roots, the gate and check-regime-boundary.sh accept waivers from that directory only, and the ask rule is the intended path to it rather than the guard. A PreToolUse hook that forces ask on any command text containing regime-waive (the page's own recommendation for full-text checkpoints) closes the rewording path at the prompt layer if the design wants both.

## Unchanged

INV-1, INV-6, INV-7, INV-8, INV-9, INV-11: accepted as of round 8, with round 8's INV-1 items pending in v10.

## Process note

This is the ninth Claude round and the second Codex round on one design, with per-finding revisions interleaved from two reviewers; INV-6 would have reset a task at two revise rounds. v10 should collect every open item (round 8: INV-1 owner, routing and record location; INV-5 once-per-head; round 9: INV-5 refusal clause, INV-12 scope split, V5c order, the selector runner; the Codex round 9 items) and go to both reviewers once, as a single confirmation, rather than one revision per finding.

Design verdict: revise
