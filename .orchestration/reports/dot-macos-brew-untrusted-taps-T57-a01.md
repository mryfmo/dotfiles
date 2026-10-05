# Report: dot-macos-brew-untrusted-taps-T57-a01

- **Worker and branch:** `claude-standard-dot-a005` in worker-c, branch `fix/macos-brew-untrusted-taps` from `origin/main` 18d192aa.
- **Commits:** `f314ab2a` (round 0); `50c833b3` (round 1 measurement: item-level trust only); `f568eab6a1032a9d134d89cb43f3b0200f2016fc` (round 1 final: whole-tap fallback for taps with nothing installed). No force push.
- **PR:** #228, https://github.com/mryfmo/dotfiles/pull/228.
- **task_rev:** `df9aa5ec…` for round 0 and `89a99b97…` for revise round 1. Both matched.
- **Status:** ready_for_review (round=revise-1).
  - **CI:** green on `f568eab6`. 13 pass, and `nix` is skipped by change detection.
  - **Acceptance count:** `untrusted-tap warnings: 0` on `f568eab6`. The sweep has no warning-level or failure-level items.

## Change (4 files)

- **`install/macos/common/brew.sh`:** a new `handle_ci_untrusted_taps`, called from `main` between `install_homebrew` and `opt_out_of_analytics`. It does nothing unless `CI` is exactly `true`. Otherwise it:
  1. reads the untrusted taps from Homebrew's own `brew untrust --tap` listing (nothing hard-coded);
  2. reads the installed items from `brew list --formula --full-name` and `brew list --cask --full-name`;
  3. trusts only the installed items whose tap is listed (`brew trust --formula …`, `brew trust --cask …`);
  4. gives whole-tap trust (`brew trust <tap>`) only to a listed tap with nothing installed.

  If `brew untrust` fails (a Homebrew without tap trust), it prints a one-line stderr notice and returns 0.
- **`.github/workflows/test.yaml`** (`Install tools`, macOS branch only): the hard-coded `brew trust aws/tap azure/bicep` is replaced with `bash -c 'source install/macos/common/brew.sh; handle_ci_untrusted_taps'`.
- **`tests/install/macos/common/brew.bats`:** a new case. It checks the function does nothing with `CI` unset, empty, `false`, `1` or `yes`. Under `CI=true` its calls are exactly: `untrust --tap`, `list --formula --full-name`, `list --cask --full-name`, `trust --formula azure/bicep/bicep hashicorp/tap/packer`, `trust --cask hashicorp/tap/vagrant`, `trust aws/tap`.
- **`README.md`:** one sentence in the macOS setup section (+2 lines).

## Item-level versus whole-tap: decided by measurement (revise round 1)

- **Round 0 was wrong.** It claimed "Homebrew cannot list installed formulae from an untrusted tap, so item-level trust is not derivable". That is false, as the auditor found. I re-derived it from `cmd/list.rb` at 7.0.7, lines 104–120. With `--full-name` and no named arguments, `brew list --formula` walks `Formula.racks` and reads each keg's install receipt (`Keg.from_rack(rack)&.tab&.tap`), so it does list items from untrusted taps. I had read the non-`--full-name` branch (`Formula.installed`, lines 200–215), which does skip them, and applied it to the wrong code path. The claim has been removed from the code comment, this report and the PR description.
- **Measurement 1: item-level trust only** (`50c833b3`, [public-bootstrap (macos-14, client)](https://github.com/mryfmo/dotfiles/actions/runs/37030239884/job/110914945531)). The log shows `Trusted formula: azure/bicep/bicep` and `Trusted formula: hashicorp/tap/packer`, and those two taps no longer warned. The annotation still warned `The following taps are not trusted: aws/tap`. `aws/tap` has nothing installed on the runner, so it has no item to trust. Homebrew's check covers only wholly untrusted taps (`Trust.wholly_untrusted_taps`), so a tap with at least one trusted item drops out of it.
- **Measurement 2: item-level plus whole-tap only for taps with nothing installed** (`f568eab6`, [public-bootstrap (macos-14, client)](https://github.com/mryfmo/dotfiles/actions/runs/37031476934/job/110919109271)). The log shows `Trusted formula: azure/bicep/bicep`, `Trusted formula: hashicorp/tap/packer` and `Trusted tap: aws/tap`, with no warning annotation. The sweep counts `untrusted-tap warnings: 0`.
- **Option left to the orchestrator:** for a tap with nothing installed, Homebrew's own message (measurement 1) lists `brew untap aws/tap` first, and untapping would grant no trust at all. I followed the task's stated fallback, whole-tap trust, and limited it to such taps. Switching that branch to `brew untap` would be a one-line change if you prefer it.

## Bot review on the measurement commit

`chatgpt-codex-connector[bot]` left an inline P2 on `50c833b3` (`install/macos/common/brew.sh:105`, https://github.com/mryfmo/dotfiles/pull/228#discussion_r4167450604): "Trust each untrusted tap, not only installed packages".

- **The `aws/tap` point is right,** and it is the same gap measurement 1 found. `f568eab6` fixes it.
- **The broader claim, that every listed tap stays untrusted to the pre-install check, is contradicted by measurement 1.** `azure/bicep` and `hashicorp/tap` cleared with item-level trust alone, so trusting every tap whole is unnecessary.
- **Proposed dispositions for the orchestrator's sweep:** `fixed:f568eab6` for the `aws/tap` case; not-applicable for the rest, citing measurement 1. I did not reply on the PR thread.

## CI evidence that the function ran

- The two bootstrap-job measurements are above.
- **`test (macos-14, client)`:** its taps are already trusted when the step starts. In PR #227's run (job 110892662913) the old inline command printed `Already trusted tap: aws/tap`, so the function lists nothing there and correctly does nothing.
- **Second call in the same job:** the existing `[macos] brew` bats case runs `bash brew.sh` with `CI=true` after `Install tools`, so the function runs again. It is idempotent: `brew trust` on already-trusted entries prints "Already trusted".

## Notes

- **Bare `shfmt -d` exits 1.** That is the task's verbatim command, but it uses shfmt's default tabs and fails on the unchanged `origin/main` file as well, as the validation shows. The repository form, `shfmt -i 4 -sr -d` with the CI-pinned 3.14.1, as in `.editorconfig`, the Makefile and test.yaml, is clean. `shellcheck` is clean.
- **README formatter incident.** A PostToolUse formatter hook rewrote unrelated README lines after my Edit-tool insert. I restored `README.md` from `origin/main` and re-inserted the sentence with a script, so the final README diff is the +2 lines only. The learning file has a candidate entry.
- **Local testing.** Bats run in CI only. A plain-bash smoke test with the same fake `brew` is pasted in the validation file as the local stand-in.
- **`make validate-agent-assets`** exits 0. It still warns about untracked T55 `.orchestration/validation` files in the main checkout; those are orchestrator bookkeeping.

## CompactionDB

```
cd ~/Workspace/dotfiles && python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'T57 (operator 2026-10-02): recurring CI/bot findings are fixed at the root once, never dispositioned `not-applicable` repeatedly; image-provided Homebrew taps are handled in `install/macos/common/brew.sh` under `CI=true` only, derived from Homebrew'"'"'s own tap listing.'
4dd72a5f-3b9e-490f-8f00-fe17c8871d98
```

[memory:decision] T57 (operator 2026-10-02): recurring CI/bot findings are fixed at the root once, never dispositioned `not-applicable` repeatedly; image-provided Homebrew taps are handled in `install/macos/common/brew.sh` under `CI=true` only, derived from Homebrew's own tap listing.

## Artifacts

- validation: `.orchestration/validation/dot-macos-brew-untrusted-taps-T57-a01.md`
- sandbox: `.orchestration/sandboxes/dot-macos-brew-untrusted-taps-T57-a01.md`
- learning: `.orchestration/learning/dot-macos-brew-untrusted-taps-T57-a01.md`
- autoskill: `.orchestration/autoskill/runs/dot-macos-brew-untrusted-taps-T57-a01.md`

cost: n/a (no subagents in either round; the runtime does not expose session totals)
