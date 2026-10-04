# dotfiles-T78-dead-docs-adh-a01 — report (status: ready_for_review)

- PR: #261 (https://github.com/mryfmo/dotfiles/pull/261), branch `chore/dead-docs-adh`.
- Final head: `8d536a38`, a single commit on `origin/main` 6534df0f (#258).
- CI: all 13 checks pass, and the branch is up to date with main (unchanged). `mergeable_state` is `blocked`: an unresolved Bot thread and the required review.
- Codex Bot: reviewed the final head at 17:02:26Z with one P2 finding.

## Changes

1. **`AGENTS.md`**: the "ADH (autonomous-dev-harness)" section is deleted. Nothing else in the file changed.
2. **`reviews/`**:
   - `reviews/ADH_Integrated_Plan/` is deleted (198 files; `git ls-files reviews` was entirely that directory and is now empty);
   - the `.coderabbit.yaml` `"!reviews/**"` path filter and, per PONG decision 1, the `.prettierignore` `reviews/` line are dropped.
3. **Hermes and `learn_index.md`**: the passages were located by text, since T69/T97 moved the line numbers.
   - In `agmsg-orchestration/SKILL.md`:
     - the description loses "without installing the Hermes Agents runtime";
     - the "adopts only the Hermes Skill Subset ideas …" bullet is removed;
     - the learn bullet drops the `learn_index.md` maintenance and index-format sentences, but keeps the learn-file content rule;
     - "Do not install Hermes Agents runtime for this protocol." is removed.
   - In `home/dot_config/codex/AGENTS.md`, the whole "セッション開始時の learn 確認" section (heading and three bullets) is deleted, per PONG decision 2.
   - `git ls-files | grep learn_index` is empty, and `test_agmsg_orchestration_docs.py` pinned none of these phrases.
4. **`.github/copilot-instructions.md`**: deleted.
5. **Conventional Commits**:
   - `home/dot_claude/commands/commit.md` no longer embeds the Conventional Commits 1.0.0 specification (old lines 19-119), and step 5 points to `~/.agents/skills/gh-first-workflow/references/gh-git-rules.md`, the deployed path, since the command runs in any repository;
   - `plans/README.md:18` points to the repo path of the same file.
6. **Nix plans**:
   - `docs/plans/nix-first-architecture.md` and `docs/plans/nix-migration.md` each get a dated note under the title: the flake was removed in #247, and the commands and paths below no longer apply;
   - `plans/004-*` gets a narrower note covering only its Nix commands and paths (`flake.nix`, `flake.lock`, `nix flake …`), because most of that supply-chain plan is not about Nix;
   - the bodies are unchanged.

## Codex Bot thread

- **4178539979** (P2, `.github/copilot-instructions.md`): "Retain Copilot repository instructions".
  - Proposed: `not-applicable:task item 4 deletes the file by operator decision (Copilot is not part of this harness and no tooling here reads it); the Bot's point only applies to someone using Copilot on this repository`.
  - The thread is not resolved.

## Reporting notes

- The task's "Conventional Commit" grep still lists `gh-first-workflow/SKILL.md`, the skill that owns `gh-git-rules.md`: one description line and two one-line format reminders, not a restated specification. I left it as it is.
- Out of scope: `README.md` (forbidden) was not checked for ADH or Copilot mentions beyond the task grep. The `adh` model profile and its validators belong to T79.

cost: n/a (the Claude Code runtime does not expose per-session token or cost figures to the worker)
