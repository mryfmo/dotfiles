---
reviewed_at: 2026-10-12T11:45:39Z
reviewer: claude-review-dot-a001
profile: review
session: 2089b04f-f9c7-498b-86c5-76f2140048d5
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@7f007ec41c9b0dedded66c964ba8e858d1d604e40b10a0ab278966f7eb2a2ae6
task: dotfiles-T128-task-review-phase1-a01
round: 1
files:
  - dotfiles-T128-gate-evidence-a01@cba77a8d6dbcfe8a191f97e75ec273be60f7d2f64c4d301f6b64f5815a97dd65
  - dotfiles-T128-playbook-rules-a01@15ae4da24f6bd2cad2899eca90d799e277cef09cca3dba749d8ba66194312ff2
  - dotfiles-T128-aws-cli-macos-a01@6000f0267e37033801bf3dfc4ceceb7f8c15bd75af11356bf917da62c2d38093
verdicts:
  dotfiles-T128-gate-evidence-a01: revise
  dotfiles-T128-playbook-rules-a01: revise
  dotfiles-T128-aws-cli-macos-a01: revise
---

# Task-file review: plan 007 Phase 1 (T702, T703) and Phase 5 (T715), one round

Read against the design in the working tree (v18 at 7f007ec4, with the round-20 INV-6 clause pending as v19), plan 007, the SKILL and AGENTS.md on main (36a20d0a), and the scripts and tests each file names. Premises re-run from this seat: every grep and sed, brew uses and brew deps, and the three HEAD requests plus the install.sh grep against awscli.amazonaws.com (the sandbox allowed that host). Shape of every threat table checked by hand: no closed selector but T715's one, in the tests/<file>::<name> form; no out-of-scope row; every residual over 20 characters; one row per allowed_files entry, per non-path control and per orchestrator effect in all three. Common note: all three point design_review.receipt at round 18, which is the design file's current pointer today; once v19 lands with a new pointer the three files repoint before dispatch, as the checker's C6 will say.

## dotfiles-T128-gate-evidence-a01 (T702)

- P1 0.95 .orchestration/tasks/dotfiles-T128-gate-evidence-a01.md:16 — a design-tier task mapped to [INV-6] carries no invariants: block; INV-2 requires the task.md invariants to equal the design's entry as ids and byte for byte as sentences, so the file must carry INV-6's sentence, and v19's sentence with the round-20 clause, which means the file is finalized after v19 lands.
- P2 0.85 .orchestration/tasks/dotfiles-T128-gate-evidence-a01.md:64 — item 2 makes ACCEPTANCE_EVIDENCE a required input whenever BASE is set; the documented gate command lives in SKILL step 10.4 (line 170 on main; owner T703, whose item 7 says the Playbook does not change), the Makefile recipe passes an explicit variable list (line 211) and its comment (206) names the inputs, README lines 427 and 1101 repeat them, and the module's existing PR-mode cases that set BASE without the new variable would fail; either the input is optional in this PR (the S6 check runs when it is given; the Playbook makes it mandatory by rule) or T703 gains the step 10.4 sentence and T702's allowed_files gain the Makefile, and item 3 says the existing PR-mode tests gain the variable.
- Premises 1 to 3 hold as pasted (sed 26,27; the two ledger rows at 26 and 33; the a07 rows at 16 to 18). Items 1 and 2 agree with INV-6's round-20 clause (evidence= on not-applicable; a class at three without a search: line and both commands); item 2's ledger grammar matches the real records. Touch points inside allowed_files: PR_FEEDBACK_DISPOSITION is used at lines 407 and 698 of the script and nowhere else; AUDIT_DISPOSITIONS is read at 677 and tested at 1000 to 1108 of the declared module.

Task-file verdict: dotfiles-T128-gate-evidence-a01: revise

## dotfiles-T128-playbook-rules-a01 (T703)

- P2 0.9 .orchestration/tasks/dotfiles-T128-playbook-rules-a01.md:64 — item 5 replaces the task-file-review bullet's clause, but tests/unit/test_agmsg_orchestration_docs.py line 278 asserts the old token "one invariant check (a -contract-a01 id maps to its implementing entry)" and item 6 adds tests for new sentences only; the task says that line 278's token becomes the new clause's token, or the module fails on the first run.
- P2 0.8 .orchestration/tasks/dotfiles-T128-playbook-rules-a01.md:66 — item 7 says the Playbook does not change beyond step 6, yet T702 as written needs step 10.4's gate command to name ACCEPTANCE_EVIDENCE (the T702 finding above); one of the two files moves: T703 gains that one sentence, or T702 makes the input optional.
- Premises 1 to 3 hold as pasted (lines 69, 71, 72, 162; AGENTS.md 78; the PINNED_SECTIONS loop and the fixture message at 240 to 252). Items 1 to 4 state sentences whose owner is the SKILL or AGENTS.md, as plan 007 cites them; item 3 names the search command as it runs; item 4's row unit matches the round-20 note (non-path controls carried by the declared test module's row). The step-6 fixture is sliceable (start "\n6. ", end "\n7. " inside the Orchestrator Playbook slice, the step-7 entry's form); the invariants and code-review-orchestration fixtures change with items 2 to 5 and are in allowed_files. The regime rule file carries no contract clause.

Task-file verdict: dotfiles-T128-playbook-rules-a01: revise

## dotfiles-T128-aws-cli-macos-a01 (T715)

- P2 0.85 .orchestration/tasks/dotfiles-T128-aws-cli-macos-a01.md:45 — premise 2's pasted grep output is not the command's output: grep -n prints ascending line numbers and the live run prints 23, 304, 309, 310, 324, 325 and 463, while the paste reads 23, 463, 309, 310 (reordered, two XDG lines and one dropped); the claim holds (team id 94KV3E626L, the pkgutil check at 463, the XDG defaults at 309 and 310) and the HEAD codes are 404, 200, 200 as pasted, but the output is re-pasted as the command prints it (plan 007's run-not-recall rule).
- P3 0.7 .orchestration/tasks/dotfiles-T128-aws-cli-macos-a01.md:69 — the macOS branch runs gpgv at every apply; it exists on a brewed macOS only through the gpg formula, which BREW_PACKAGES lists (dependencies.sh line 21) and run_once_before_50 installs before any run_after; one premise or one sentence in item 1 says so, since the task removes a formula from the same list.
- Premises 1 and 3 hold as pasted (brew uses: awscli; brew deps: the aws-c-* family, python@3.14 and the rest; aws_cli.sh line 31; BREW_PACKAGES lines 16 to 18). Touch points: the Ubuntu wrapper is the only includer of aws_cli.sh (home/.chezmoiscripts/ubuntu/run_after_04-install-aws-cli.sh.tmpl); the manifest and tests/unit/test_validate_agent_assets.py name the file as the fingerprint's render target, which a macOS branch leaves intact; tests/unit/test_supply_chain_policy.py lines 302 to 305 only assert the existing wrappers exist; the new macOS wrapper name has no clash under home/.chezmoiscripts/macos/. Tier: none of the five paths is on the design's tier list (workflows, gate scripts, permgate, settings templates, hooks), so review tier by INV-1; INV-2's caps are far off. The closed row's selector names a test item 4 defines by that exact name.

Task-file verdict: dotfiles-T128-aws-cli-macos-a01: revise
