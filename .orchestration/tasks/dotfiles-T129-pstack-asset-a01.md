---
format: 2
task_id: dotfiles-T129-pstack-asset-a01
kind: code
security: false
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
allowed_files:
  - home/dot_agents/agent-config.yaml
  - scripts/update-agent-assets.sh
  - scripts/check-agent-runtime.py
  - .github/workflows/agent-assets.yml
  - tests/unit/test_pstack_asset.py
  - tests/unit/test_check_agent_runtime.py
  - .orchestration/dotfiles-T129-pstack-asset-a01/**
after: [dotfiles-T129-assets-omp-hcom-a01]
threat_table:
  - control: "the PR edits home/dot_agents/agent-config.yaml in one place (assets.pstack with the fields item 1 lists; no other section)"
    disposition: "residual: the assets section, not a seat's execution boundary; the diff review and the audit compare against this row"
  - control: "the PR edits scripts/update-agent-assets.sh in three places (the rendered constants PSTACK_PIN_COMMIT and PSTACK_TREE_SHA256 with the PSTACK_UPSTREAM_URL and PSTACK_SKILLS definitions beside them; pstack_tree_hash and pstack_verify_tree; update_pstack added to main's list)"
    disposition: "closed: tests/unit/test_pstack_asset.py::test_update_pstack_fetches_the_pin_links_only_the_listed_skills_and_writes_the_receipt"
  - control: "the PR edits scripts/check-agent-runtime.py in one place (the receipt reader takes the receipt path and is called for the terminal-browser receipt and for ~/.local/state/pstack/skills.links)"
    disposition: "closed: tests/unit/test_check_agent_runtime.py::test_pstack_receipt_links_are_managed_shared_skills"
  - control: "the PR edits .github/workflows/agent-assets.yml in one place (a step that sparse-clones the pinned upstream read-only into RUNNER_TEMP and runs pstack_verify_tree from the sourced updater)"
    disposition: "residual: the step runs the repository's own script on the tree of a public repository at the exact commit the rendered constant names; the tree is data (hashed and read for front matter, never executed); no new action, secret or permission; a pin-bump PR whose tree, skill set or front matter changed fails this step, which is the step's purpose"
  - control: "the PR adds tests/unit/test_pstack_asset.py (the two tests of item 5: the sourced functions on a fixture tree, and update_pstack against a local repository as the upstream with HOME in a temporary directory)"
    disposition: "residual: the fixture and the local repository are written by the test with real git; the audit reads each case against items 2 to 4"
  - control: the PR edits tests/unit/test_check_agent_runtime.py only for the new case
    disposition: "residual: one new test beside the existing ones, which stay byte-identical"
  - control: "the upstream tree as an input (cursor/plugins at the pinned commit, path pstack/, MIT licence in pstack/LICENSE)"
    disposition: "residual: fetched read-only at an exact commit, its tree hash compared with the manifest's before anything is linked, only the listed skills linked, nothing from the tree executed; the clone keeps pstack/LICENSE beside the skills, and nothing is copied into the repository, so no notice is due here (the rewritten skills of the H PRs carry their own LICENSE, UPSTREAM and notices)"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T129-pstack-asset-a01/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T129-pstack-asset-a01/ (report.md, validation.md, sandbox.md, learning.md)
    disposition: "residual: prose and pasted command output; the sandbox record lists every permission-gated command; the audit reads them"
  - control: "task metadata (the front matter of the task copy: kind, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: in-process effects
    disposition: "residual: the tests run the sourced updater's functions in bash subprocesses (the main guard runs nothing on source) with HOME in a temporary directory, a local repository as PSTACK_UPSTREAM_URL and real git, and import only the standard library; nothing is imported into another process"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: .github/workflows/agent-assets.yml is in allowed_files for the one step above and nothing else; update-agent-assets.sh runs git (clone, sparse-checkout, fetch, checkout at the pin), find, sort, shasum or sha256sum (agmsg_sha256), ln and rm as it runs its tools today; check-agent-runtime.py runs under its interpreter as today; a PR checkout as cwd chooses nothing new"
  - control: new or renamed scripts
    disposition: "residual: no new or renamed script (three functions in the existing updater, one new test module); any other new or renamed script is an undeclared change the audit fails"
  - control: orchestrator effect merge
    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
premises:
  - claim: the manifest on origin/main has no pstack asset
    command: git show origin/main:home/dot_agents/agent-config.yaml | /usr/bin/grep -c "pstack" || true
    output: |-
      0
  - claim: the generator renders a Claude symlink template for every file under home/dot_agents/skills (one rglob line), so no pstack file may live there
    command: git show origin/main:scripts/generate-agent-configs.py | /usr/bin/grep -c "skills_root.rglob"
    output: |-
      1
  - claim: the validator requires verify sha256 for a git-commit asset (one line), so the pin is checked by a tree hash in the manifest
    command: 'git show origin/main:scripts/validate-agent-assets.py | /usr/bin/grep -cF ''"git-commit": {"sha256"}'' '
    output: |-
      1
  - claim: the updater on origin/main runs main only when executed (one guard line), so the tests and the workflow step can source its functions
    command: 'git show origin/main:scripts/update-agent-assets.sh | /usr/bin/grep -cF ''if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then'' '
    output: |-
      1
  - claim: check-agent-runtime.py on origin/main reads one skills receipt, the terminal-browser one (one line), so pstack links would be WARNs without item 3
    command: git show origin/main:scripts/check-agent-runtime.py | /usr/bin/grep -c "skills.links"
    output: |-
      1
---

# AGMSG-TASK dotfiles-T129-pstack-asset-a01 — pstack as a tracked asset: pinned upstream, the as-is skills linked where omp's .agents provider reads, a tree hash the bump PR must move (plan 023 PR G)

Written 2026-10-17 by the orchestrator seat as plan 023's PR G on the operator's request. Facts read today (plan 023 and `gh api` at 10:1xZ): upstream `cursor/plugins`, path `pstack/`, author Lauren Tan (@poteto), `pstack/LICENSE` MIT (Copyright (c) 2026 Lauren Tan), the repository root declares no licence, `pstack/plugin.json` version 0.15.25, `pstack/skills/` holds 54 skill directories and every name listed in item 2 is present at `main` = `101b274dd991f694e1f7024be2157e5f3adf07de`. The monorepo has no per-plugin tag, so the pin is a commit sha of `main` with the plugin.json version it holds. Round 2 of this text applies the Codex half's round 1: the manifest's `pin` plus a tree `sha256` is the lock (the validator's git-commit field set, premise 3), so there is no lock file and nothing under `home/dot_agents/skills` (premise 2); only the as-is skills are linked here and every rewritten skill, vendored copy and notice belongs to the H PRs (decision D-G-scope, default A); CI checks the real upstream tree at the pin; the links are recorded in a receipt the runtime check reads (premise 5); omp's provider switch is PR B's.

## Goal

`make update` fetches pstack at the manifest's pinned commit, refuses a tree whose hash differs from the manifest's, and links the listed skills into `~/.agents/skills/<name>`; the agent-assets workflow fails a pin-bump PR whose tree hash, skill set or front matter changed.

## Files

1. `home/dot_agents/agent-config.yaml`: `assets.pstack` with `source: git-commit`, `upstream: cursor/plugins`, `pin: <the sha of main the worker reads at task start (101b274dd991f694e1f7024be2157e5f3adf07de at 10:1xZ today), with the plugin.json version it holds in the note>`, `verify: sha256`, `sha256: <the tree hash of pstack/ at the pin: the sha256 of the LC_ALL=C-sorted lines "<sha256>  <path relative to pstack/>" of every file under pstack/, as pstack_tree_hash prints it>`, `reason: the monorepo publishes no per-plugin tag, release, checksum or signature; the commit and the tree hash are the only check`, `note: pstack/plugin.json version 0.15.25 at the pin; pstack/LICENSE MIT (Lauren Tan); the repository root declares no licence, so only pstack/ is taken; the skill allowlist is PSTACK_SKILLS in scripts/update-agent-assets.sh`, `install_path: ~/.local/share/pstack/repo` (the sparse clone), `installer: scripts/update-agent-assets.sh#update_pstack`, `render: {file: scripts/update-agent-assets.sh, constants: {PSTACK_PIN_COMMIT: pin, PSTACK_TREE_SHA256: sha256}}` (as understand-anything renders into the updater). `uv run --with pyyaml scripts/validate-agent-assets.py` passes (pasted).
2. `scripts/update-agent-assets.sh`: beside the rendered constants, `PSTACK_UPSTREAM_URL="https://github.com/cursor/plugins"` (non-readonly, the test's seam, as installer-pins.sh's assignments are) and the array `PSTACK_SKILLS=(principle-attack-the-premise principle-boundary-discipline principle-build-the-lever principle-encode-lessons-in-structure principle-exhaust-the-design-space principle-experience-first principle-explain-the-number principle-fix-root-causes principle-foundational-thinking principle-guard-the-context-window principle-laziness-protocol principle-make-operations-idempotent principle-migrate-callers-then-delete-legacy-apis principle-minimize-reader-load principle-model-the-domain principle-never-block-on-the-human principle-outcome-oriented-execution principle-prove-it-works principle-redesign-from-first-principles principle-separate-before-serializing-shared-state principle-sequence-verifiable-units principle-subtract-before-you-add principle-test-behavior-not-implementation principle-type-system-discipline correct sharpen in-your-own-words blast-radius why tdd technical-writing unslop no-comments)`; `pstack_tree_hash <tree>` prints the hash of item 1 (relative paths, so the value does not depend on where the tree sits); `pstack_verify_tree <tree>`: exit 1 printing both values when the tree hash differs from `PSTACK_TREE_SHA256`, then for each name in `PSTACK_SKILLS` exit 1 naming the skill and the field when `<tree>/skills/<name>/SKILL.md` is absent or its front matter (the lines between the first two `---` lines) lacks a non-empty `name:` or `description:`; `update_pstack`: skip with the script's usual message when git is absent; clone `PSTACK_UPSTREAM_URL` into `~/.local/share/pstack/repo` with `--filter=blob:none --no-checkout` when absent, `git sparse-checkout set pstack`, fetch when the pin is unknown, `git checkout --detach <PSTACK_PIN_COMMIT>`; `pstack_verify_tree repo/pstack` (a failure stops here, nothing linked); `ln -sfn` each listed skill directory to `~/.agents/skills/<name>`, write every link path to `~/.local/state/pstack/skills.links`, and remove a link the previous receipt listed that is no longer in `PSTACK_SKILLS`; `manifest_record` as the other installers call it; idempotent on a second run. `update_pstack` joins `main`'s list after `update_hcom`.
3. `scripts/check-agent-runtime.py`: `terminal_browser_receipt_paths` becomes `receipt_link_paths(receipt)` taking the receipt path; its two callers pass the terminal-browser receipt and `~/.local/state/pstack/skills.links` and union the sets, so the pstack links are managed shared skills, not `WARN: unmanaged skill dir` lines.
4. `.github/workflows/agent-assets.yml`: one step after "Validate agent assets", "Check pstack at the pin": `pin=$(bash -c 'source scripts/update-agent-assets.sh; printf %s "$PSTACK_PIN_COMMIT"')`, `git clone --filter=blob:none --no-checkout https://github.com/cursor/plugins "$RUNNER_TEMP/pstack"`, `git -C "$RUNNER_TEMP/pstack" sparse-checkout set pstack`, `git -C "$RUNNER_TEMP/pstack" checkout --detach "$pin"`, then `bash -c 'source scripts/update-agent-assets.sh; pstack_verify_tree "$RUNNER_TEMP/pstack/pstack"'`.
5. Tests: `tests/unit/test_pstack_asset.py` (new): `test_pstack_verify_tree_refuses_a_drifted_hash_a_missing_skill_and_a_bad_front_matter` (a fixture tree with two listed skills; a bash subprocess sources the updater, sets `PSTACK_SKILLS` to the two names and `PSTACK_TREE_SHA256` to `pstack_tree_hash` of the fixture: exit 0; a changed file, a removed listed skill directory and an empty `description:` each exit 1 naming the cause), `test_update_pstack_fetches_the_pin_links_only_the_listed_skills_and_writes_the_receipt` (a local repository committed with real git holding `pstack/skills/<two listed>/SKILL.md`, one unlisted skill and `pstack/LICENSE`; `PSTACK_UPSTREAM_URL` that repository, `PSTACK_PIN_COMMIT` its head, `PSTACK_TREE_SHA256` its tree hash, HOME a temporary directory: `update_pstack` creates the two links and not the third, the receipt lists both, a second run changes nothing, a renamed listed skill between two runs removes the stale link; with another `PSTACK_TREE_SHA256` nothing is linked and the exit is non-zero). `tests/unit/test_check_agent_runtime.py`: `test_pstack_receipt_links_are_managed_shared_skills` (a pstack receipt naming a link under the shared skills root: no WARN for it; without the receipt the WARN appears, as today).

## Out of scope

The rewritten skills and everything redistributed (H1 to H9: `vendor/<name>/` with LICENSE and UPSTREAM, `THIRD-PARTY-NOTICES.md`; nothing is copied into the repository here, so no notice is due: D-G-scope); omp's provider configuration that makes omp read `~/.agents/skills` (`enabledProviders`, PR B); until B merges omp does not list these skills, and this PR's live check is `ls -l ~/.agents/skills/sharpen` showing the link; any change to a skill's content (never: the links point into upstream's tree); the hcom and herdr assets.

## Check

`uv run python -m unittest tests/unit/test_pstack_asset.py tests/unit/test_check_agent_runtime.py -v` green and `uv run --with pyyaml scripts/validate-agent-assets.py` (exit 0) pasted in the validation file, with `shellcheck scripts/update-agent-assets.sh`, the live run on the worker's machine (`bash -c 'source scripts/update-agent-assets.sh; update_pstack'` then `ls -l ~/.agents/skills/sharpen` and `wc -l ~/.local/state/pstack/skills.links`, pasted), the agent-assets workflow green on the PR, and `git diff --numstat origin/main...HEAD`: at most 200 changed lines (added plus deleted) outside `tests/` and outside `.orchestration/` (plan 021 step 7.2) and 1000 added lines under `tests/` (INV-2).

## Completion

One PR from a fresh branch off `origin/main` after dotfiles-T129-assets-omp-hcom-a01 merges (the two tasks share the manifest and the updater). The PR is ready for the orchestrator's integration when the ruleset's required checks are green, the Bot's review of the final head is in (at PR open, and once more on `@codex review` after a P0/P1 fix round: plan 020 step 2), every Bot thread is replied to and resolved by the orchestrator with its disposition, the validation file carries the Check's outputs, and the RESULT names every P0/P1 thread with `fixed:<sha>` and every P2 thread with the disposition the worker proposes; the orchestrator's audit of the final head is dispositioned finding by finding before the gate, and a P0/P1 it leaves is the operator's decision. The Bot's P0 and P1 get at most one fix round, worker-side before the RESULT, each named `fixed:<sha>` in the RESULT; a P0 or P1 that survives the round is listed as `open:<thread id>` with `bot_rounds=2` (the Bot's review at PR open and its re-review after the fix round), stops the PR and goes to the operator as a decision; a P2 of the Bot's first review on this PR's own change whose fix stays within `allowed_files` and is small (one flag or a few lines plus one test) is fixed in a revise round the orchestrator sends with a `check=` while INV-6's counts allow it (C-50; every fix round, before or after the first RESULT, counts toward INV-6's cap of two, C-61); the third finding of one class on this PR stops the rounds until the orchestrator's `re-plan:` line (C-59); a later review's P2 and every P3 are advisory (C-61), as is any other P2, owned by `dotfiles-T129-pstack-asset-followup-a01`, which the orchestrator writes when the first advisory P2 appears, before the PR's dispositions (C-51), and recorded under `## Owned by dotfiles-T129-pstack-asset-followup-a01` in this task's acceptance record. The orchestrator integrates (local review once per head, sweep, audit, gate) and merges with `gh pr merge --squash --match-head-commit <audited head>`. The RESULT names head, base, branch, files, every Bot thread with its disposition, the test names, the caps, `task_copy=<sha256 of .orchestration/dotfiles-T129-pstack-asset-a01/task.md>` and the evidence paths.

## Change (round 2, 2026-10-17T10:19:55Z)

The Codex half's round 1 (five P1, two P2): the git-commit asset carries verify, sha256 (a tree hash), reason and installer with a render into the updater (item 1, premise 3); the lock file and `scripts/pstack-lock.py` are gone, nothing lives under `home/dot_agents/skills` (premise 2); the rewritten skills, `vendor/pstack/**` and `THIRD-PARTY-NOTICES.md` leave for the H PRs and the contradiction with "never change a skill's content" is gone (D-G-scope); omp's provider switch is named as PR B's with this PR's live check (Out of scope); CI checks the real upstream tree at the pin (item 4) and the drifted-hash case is the first test (item 5); the fetch mechanism is written out (item 2, premise 4); the links are recorded in a receipt the runtime check reads (item 3, premise 5); this task follows PR A (shared files).

## Checks (pasted by the orchestrator before each send)

```
dotfiles-T129-pstack-asset-a01.md: OK
premise 1: OK
premise 2: OK
premise 3: OK
premise 4: OK
premise 5: OK
masked 0 match(es) in .orchestration/tasks/dotfiles-T129-pstack-asset-a01.md
```
