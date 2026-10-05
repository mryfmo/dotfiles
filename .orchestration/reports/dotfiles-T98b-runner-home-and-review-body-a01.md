# Report: dotfiles-T98b-runner-home-and-review-body-a01

- **Worker and branch:** `claude-standard-dot-a005` in worker-c, branch `fix/runner-home-and-review-body` from `origin/main` 58f7594f with `--no-track`.
- **task_rev:** `sha256:0021ef8c…7e56f5c2`, matched in the main checkout.
- **PR:** #280, https://github.com/mryfmo/dotfiles/pull/280.
- **Commit and diff head:** `70f060e7`. CI, the Bot wait and `mergeable_state` are in the validation file.
- **CI:** green; `mergeable_state` is `clean`.
- **Bot:** no review of 70f060e7. The Codex Bot posted its quota notice "Codex usage limits have been reached for code reviews" (issue comment, 09:13:55Z) right after the PR opened. My wait counted quota notices only from the moment its script started, seconds after that notice, so it missed this one and ran the full 15 minutes, ending `bot: none` (09:29:54Z–09:45:01Z). The notice is pasted in the validation file.
- **Status:** ready_for_review.

Example paths are spelt with `∕` (U+2215) where a literal path would be masked or flagged by the scan.

## What changed

1. **Runner homes as anywhere-forms** (`scripts/validate-agent-assets.py`, `compiled_home_path_pattern`):
   - The pattern gains `∕(?:home|Users)∕runner` with no leading boundary, like a multi-segment `$HOME`. Under any `$HOME`, a workstation's masker rewrites a glued runner path (`..F∕home∕runner∕.ssh∕id` becomes `..F~/.ssh/id`) exactly as a runner flags it, and the `.orchestration` scan flags it on every machine.
   - The global trailing lookahead `(?![\w.-])` keeps `∕home∕runner-up` and `∕home∕runners` out of this form. They stay ordinary account forms with the boundary: masked at a boundary, untouched when glued.
   - Every other form is unchanged, and `SECRET_PATTERN` is untouched.
   - Test `test_runner_homes_match_anywhere` (under `HOME=∕home∕alice`): `..F∕home∕runner∕.ssh∕id` becomes `..F~/.ssh/id` and `x∕Users∕runner∕y` becomes `x~/y`; the runner-up and runners forms are masked at a boundary and left alone when glued. The scan's verdict is asserted for each case.
2. **Review-body findings** (SKILL):
   - Worker Playbook step 15 gains: "Read each listed review's body too … Such a review-body finding is listed alongside the top-level inline comments and fixed or dispositioned the same way", and "Fix P0/P1 findings, inline or review-body, …".
   - Orchestrator Playbook step 10.4 gains: "A `review` sweep item whose body carries a `P0`–`P3` badge is a finding with its own `fixed:<commit>` or `not-applicable:<reason>` disposition, never a container for its inline threads."
   - Both sentences are pinned in `test_skill_carries_the_audit_gate_and_bot_wait_mechanics`.
3. **Boundary step: decided, no edit.** The boundary-commit bullet (SKILL line 70, from T98) already says: run the masker on the files the boundary commit adds or changes, then `make validate-agent-assets`. A second sentence would duplicate it, against the one-place rule. No `HOME=∕home∕runner` re-run mention exists to remove.

- **Re-mask:** running the masker over every tracked `.orchestration` file (2,502) printed `masked 0 match(es)` for each, so there is no re-mask commit (the #279 files were already masked under the runner `$HOME`).
- **Rule file:** unedited at 429 words.
- **Validation:**
  - `make unit-test`: 876 tests OK.
  - The validator and docs tests: 110 OK.
  - `make validate-agent-assets`: OK as the operator and as `HOME=∕home∕runner`.

- **Work done:** one commit, one CI round.

cost: n/a

The `[memory:decision]` line spells the runner homes with `∕`, because the masker would otherwise turn both into `~`. The CompactionDB record (5328b485) holds the literal text.

[memory:decision] dotfiles-T98b (orchestrator 2026-10-05): `∕home∕runner` and `∕Users∕runner` are machine-independent anywhere-forms of the home-path masker and scan, and Bot review-body findings are swept and dispositioned like inline threads (Worker step 15, Orchestrator step 10.4).
