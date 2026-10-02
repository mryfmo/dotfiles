# AGMSG-TASK dot-macos-brew-untrusted-taps-T57-a01

Drafted 2026-10-02 by the orchestrator seat; operator-approved (queued after T56; dispatch comes after T56 acceptance). Worker: `claude-standard-dot-a005` in `/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c`. Do not start before the AGMSG-TASK dispatch for T57 arrives.

## Objective

Every PR carries one `warning` annotation from the `Snippet install` workflow, job `public-bootstrap (macos-14, client)` (example: run 37018721870, job 110875969684):

```
The following taps are not trusted:
  aws/tap
  azure/bicep
  hashicorp/tap
Homebrew is currently ignoring formulae, casks and commands from these taps because ...
```

Root cause: the GitHub `macos-14` runner image ships these taps pre-tapped and untrusted; Homebrew 7 warns on every `brew install` while an untrusted tap is present. The repository's macOS bootstrap (`setup.sh` → `chezmoi apply` → `install/macos/common/*.sh`, Homebrew installs from homebrew/core only) never handles image-provided taps. `.github/workflows/test.yaml:121-129` works around it inline with `brew trust aws/tap azure/bicep`, which is duplicated logic and already incomplete (`hashicorp/tap` is new in the image). So far each PR has dispositioned this warning as `not-applicable`; that stops with this task.

Fix once, in one place:

1. In `install/macos/common/brew.sh` (the `run_once_before_03-install-brew` installer, which runs before every other macOS brew step) add one function that, when running on a CI runner (`CI=true`), enumerates the installed taps that Homebrew reports as untrusted and either untaps them (the dotfiles use none of them) or trusts them, whichever Homebrew's official documentation names as the supported handling. Verify the exact commands against `brew help trust`, `brew help untap`, `brew tap-info --help` on the macOS runner and against https://docs.brew.sh (paste the command help you relied on). Do not hard-code the three tap names: the image list changes; derive it from Homebrew's own listing. Outside CI the function is a no-op (a developer's own taps are theirs).
2. Replace the inline `brew trust aws/tap azure/bicep` in `test.yaml` with a call to that function (`bash -c 'source install/macos/common/brew.sh; <function>'`), so the handling exists exactly once.
3. Add one bats case to `tests/install/macos/common/brew.bats` that proves the function is a no-op outside CI and, under `CI=true` with a fake `brew` that reports untrusted taps, issues the documented command for each untrusted tap (bats run in CI only, per AGENTS.md).
4. One sentence in `README.md`'s macOS setup section stating that CI runner taps are handled by the brew installer.

[memory:decision] T57 (operator 2026-10-02): recurring CI/bot findings are fixed at the root once, never dispositioned `not-applicable` repeatedly; image-provided Homebrew taps are handled in `install/macos/common/brew.sh` under `CI=true` only, derived from Homebrew's own tap listing.

## Repo / branch

- Work ONLY in the worker-c worktree. `git fetch origin`; `git switch -c fix/macos-brew-untrusted-taps origin/main`. Verify the dispatched task_rev sha256 against this file; else stop and PONG blocked. If the worktree has uncommitted files, stop and PONG.

## Allowed files

- `install/macos/common/brew.sh`
- `.github/workflows/test.yaml` (the `Install tools` macOS branch only)
- `tests/install/macos/common/brew.bats`
- `README.md` (one sentence in the macOS setup section)
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dot-macos-brew-untrusted-taps-T57-a01.md` (main checkout)

## Forbidden actions

- Changing which packages are installed; touching `setup.sh`, `dependencies.sh`, `misc.sh`, pins, rules, skills, the launcher; merging; force push; local bats; `make apply`; pushing `main`.

## Validation commands (paste verbatim output)

```
git diff origin/main --stat
shellcheck install/macos/common/brew.sh
shfmt -d install/macos/common/brew.sh
make validate-agent-assets
gh pr checks <pr-number>
python3 scripts/pr-feedback.py <pr-number> --json "$TMPDIR/t57-feedback.json" && python3 -c "import json,sys;d=json.load(open(sys.argv[1]));print('untrusted-tap warnings:',sum(1 for i in d['items'] if i.get('level')=='warning' and 'taps are not trusted' in (i.get('body') or '')))" "$TMPDIR/t57-feedback.json"
```

The last command must print `untrusted-tap warnings: 0` on the PR's final head; that is the acceptance criterion for this task.

## Completion

1. PR to `main`, English title/description ending with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. CI green and the warning count above 0.
2. Artifacts at the exact expected paths; validation with verbatim outputs, PR number and head SHA, and the Homebrew help text you relied on.
3. CompactionDB `memory add --kind decision --scope project` with the `[memory:decision]` text; paste command and output.
4. `AGMSG-RESULT v1` via `agmsg-dispatch dotfiles claude-standard-dot-a005 claude-remediation-dot wT:p1 "<single line>"` (outside the sandbox). `cost:` line. max_turns=25.

## Revise round 1 (orchestrator, 2026-10-03, after audit of f314ab2a)

Codex audit (`.orchestration/validation/dot-macos-brew-untrusted-taps-T57-a01-audit.md`, Verdict: incorrect) found one P2, which the orchestrator reproduced against Homebrew 7.0.7 source (`Library/Homebrew/cmd/list.rb` lines 104-120 at tag 7.0.7):

- `brew list --formula --full-name` with no named arguments does NOT load formulae. It walks `Formula.racks` and reads each rack's keg receipt (`Keg.from_rack(rack)&.tab&.tap`), printing `<tap>/<name>` for every installed formula including those from untrusted taps. `Cask::Caskroom.casks` does the same for casks. So the claim in `brew.sh` ("Homebrew cannot list installed formulae from an untrusted tap, so item-level trust is not derivable") and the same rationale in the report and PR description are false. `Formula.installed` hides them; `brew list --full-name` does not.

Required in round 1 (one new commit on the same branch and PR #228, no force push):

1. Correct the comment in `install/macos/common/brew.sh` and the rationale in the report and the PR description. Nothing in the committed text may claim that item-level trust is not derivable.
2. Decide item-level versus whole-tap trust by evidence, not by assertion. Implement item-level trust first: derive the installed items from `brew list --formula --full-name` and `brew list --cask --full-name`, keep only those whose tap is in the `brew untrust --tap` listing, and run `brew trust --formula <tap/name>` / `brew trust --cask <tap/name>` for them. Then check in the CI job (`Snippet install` / `public-bootstrap (macos-14, client)`) whether the "taps are not trusted" warning is gone after item-level trust alone. If it is, keep item-level trust (least privilege). If the warning persists because it is tap-scoped, fall back to whole-tap trust and state that evidence (the job URL and the log lines) in the comment and the report. Either way the committed comment states what was measured, not what was assumed.
3. Update the bats case to the chosen call sequence (CI unset/empty/false/1/yes still no-op).
4. Re-run the acceptance count on the final head (`untrusted-tap warnings: 0`) and paste the job log lines that show the function acted (`Trusted …` lines), as before.

Scope unchanged (same four files). Send `AGMSG-RESULT v1 … round=revise-1` via agmsg-dispatch outside the sandbox.
