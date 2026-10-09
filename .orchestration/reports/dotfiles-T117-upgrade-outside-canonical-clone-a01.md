# Report: dotfiles-T117-upgrade-outside-canonical-clone-a01

Worker `claude-standard-dot-a001` (Claude Code), worktree `.claude/worktrees/worker-c`, branch `feat/upgrade-outside-canonical-clone` from `origin/main` b37937ca. PR #308, final head `c6cd343f8eeae6f25dd9cccd30445b2a522d0605` (revise round 1); all 13 checks pass (validation §R1.6). Round 0 ended at `8e7a1866`.

## Status: ready_for_review

## Commits

- `6000cfb4` feat(upgrade): run make upgrade in a pins worktree, never in the canonical clone
- `b2b7be60` fix(upgrade): follow the removed agmsg-bootstrap line and tighten pins prose (Amendment 2, worker-review P3 fixes)
- `8e7a1866` docs(upgrade): seat the pins worker for the working clone and derive the update path (Codex Bot 4226831987, 4226889624)
- `c6cd343f` fix(upgrade): refuse a failed fetch and an unresolvable chezmoi source (revise round 1; Codex Bot 4226889615, 4226889631)

## Revise round 1 (c6cd343f)

- **Fetch failure (Bot 4226889615).** In `require_pins_checkout`, a failed `git fetch --quiet origin main` now exits 2 with the round's message verbatim (`make upgrade refused: git fetch origin main failed in <repo_root>, so origin/main cannot be verified fresh; restore network or credentials and rerun (CHEZMOI_ALLOW_UPGRADE_IN_SOURCE=1 skips the guard)`) instead of warning.
- **Unresolvable source (Bot 4226889631).** The canonical check now runs only when `chezmoi` is on PATH (`has_command chezmoi`); absence still skips it. With `chezmoi` installed, a failing `chezmoi source-path`, or a source path whose `git rev-parse --show-toplevel` fails, exits 2 with the round's second message verbatim. A resolvable source keeps the canonical comparison as before. The order is still canonical checks, then the fetch, so a canonical-clone run refuses without network.
- **Guard test.** `test_upgrade_refuses_the_canonical_clone_and_a_dirty_or_stale_checkout` now pushes each scratch repo to a local bare origin, so the guard's fetch succeeds offline. It has seven cases:
  - `canonical` → exit 2, canonical message;
  - `source-fails` (a fake `chezmoi` that exits 1, prepended to PATH) → exit 2, unresolved message;
  - `source-not-git` (source path is a plain directory) → exit 2, unresolved message;
  - `fetch-fails` (origin URL is a missing path) → exit 2, fetch message;
  - `dirty` → exit 2, stale message;
  - `moved` → exit 2, stale message;
  - `clean` → exit 0, `Upgrade summary:`.
- **Fixture change, reported.** `upgrade_fixture`'s fake `chezmoi` printed `<temp>/other-source/home`, a path that did not exist. Under the new rule that refuses every default-fixture upgrade test, so the fixture now creates that directory and runs `git init -q` on `<temp>/other-source`. This change is in `tests/unit/test_runtime_health.py` and serves the guard's coverage only; without it the guard's own rule would refuse every default-fixture test.
- **README.** The guard paragraph states both new refusals ("It refuses as well when that fetch fails, or when an installed `chezmoi` cannot resolve its source checkout, since neither check can then be trusted"), and the override now "skips every check". In the agent setup block (former line 392), `# Then upgrade installed tools using the applied mise and agent settings.` / `make upgrade` is replaced by `# Tool upgrades run in the pins worktree, never here; see "Lifecycle" above.`, with no command line. The literal `make upgrade` and `make upgrade SYSTEM=1` lines in the lifecycle block remain for `lifecycle.bats`.
- **Validation.** On `c6cd343f`, validation §R1 (the full local suite fails the same 193 ids as origin/main, none new, §R1.7):
  - shellcheck rc 0;
  - the 14-case scratch guard check, with a local bare origin, an unreachable origin, a failing chezmoi, a non-git source, chezmoi absent and the override;
  - the upgrade tests (only the two sandbox baseline failures);
  - the boundary and Makefile tests OK;
  - the validator rc 0, the render check rc 0, and prettier, shfmt and ruff clean;
  - CI 13 of 13.
- The PR base update (`gh pr update-branch 308` onto `15672ea5`) is the orchestrator's, as the round says.

## What changed (round 0)

**`scripts/upgrade-tools.sh`**
- New `require_pins_checkout`, called in `main()` right after `parse_args`, so `--help` and the unknown-option exit still work everywhere and no phase runs before it. It is not called on `source`, so `tests/unit/test_release_asset_pins.py`, which sources the script, is unaffected.
- `CHEZMOI_ALLOW_UPGRADE_IN_SOURCE=1` (T113 shape, `${…:-0}` = `1`) returns 0 before either check.
- Canonical clone: `chezmoi source-path` → `git -C <that> rev-parse --show-toplevel` → physical path equal to `repo_root`'s physical path (the comparison `apply_upgraded_mise_config` already makes) → the task's first message verbatim on stderr, exit 2. When chezmoi is absent or the source path is not a git checkout, nothing is refused (round 0; since round 1 only absence skips the check, see above).
- Stale or dirty checkout: only when `git -C <repo_root> rev-parse --show-toplevel` is `repo_root` itself (physical path), so a scratch directory under an unrelated repository never inherits that repository's state. It runs `git fetch --quiet origin main`, which warned and continued on failure at round 0 (since round 1 a failed fetch exits 2, see above), then refuses with the task's second message verbatim and exit 2 in three cases: tracked changes (`git status --porcelain --untracked-files=no` non-empty; untracked files are ignored), an unborn `HEAD`, or `HEAD` ≠ `refs/remotes/origin/main` (`rev-parse -q --verify` on the exact remote-tracking ref, so a missing ref never compares equal to a missing `HEAD`, and a local branch named `origin/main` cannot stand in for it).
- The file header's shdoc description names the refusal.

**`Makefile`**: the `upgrade` target's `$(MAKE) agmsg-bootstrap` line is removed; nothing else changed.

**`README.md`**
- Lifecycle block: after `make doctor`, the procedure in the task's order. (1) `herdr-agents --add-worker .claude/worktrees/pins ~/Workspace/dotfiles`, with the working clone passed as `DIR` because the block has already `cd`'d into the canonical clone and `herdr-agents` resolves the worktree under `DIR` (Bot 4226831987); (2) `make -C ~/Workspace/dotfiles/.claude/worktrees/pins upgrade`, with the literal `make upgrade` and `make upgrade SYSTEM=1` lines kept, labelled as run from inside the pins worktree; (3) the orchestrator dispatches the pins task, and the worker commits the files `make upgrade` changed with the matching `tests/**` version assertions; (4) `make -C "$(git -C "$(chezmoi source-path)" rev-parse --show-toplevel)" update` after the merge (Bot 4226889624; see Decisions). The `cd "$(git -C "$(chezmoi source-path)" rev-parse --show-toplevel)"` line that `lifecycle.bats` greps stays.
- A new paragraph after the `SYSTEM=` paragraph states the user-visible change, and says how to re-run after a partly failed upgrade: `git -C ~/Workspace/dotfiles/.claude/worktrees/pins reset --hard origin/main`, after which the run bumps the pins again. `make upgrade` in the canonical clone exits 2; a dirty or not-at-`origin/main` checkout is refused; there is an override. New mise-managed versions reach `~/.config/mise` only after the pins PR merges and `make update` runs, though the upgrade run installs the tools. Homebrew, uv tool and gh extension upgrades still land immediately. The mise probe in validation §3 confirms this.
- Pins paragraph (former line 1242): the operator runs `make upgrade` in the pins worktree. The worker seated there commits it as the PR. The acceptance comparison is defined once, in the SKILL. `make check-regime-boundary` reports a canonical clone left different from `origin/main` as a sign that something ran where it must not.

**`home/dot_agents/skills/agmsg-orchestration/SKILL.md`** (boundary bullet only)
- The whole pins clause T114 wrote is replaced: patch extraction with `git diff --full-index HEAD`, the staged-bytes handling, the added-file `--no-index` append, the sha256 record and the blob-header identity proof. So is the post-merge restore paragraph: the added-file removal, `restore -SW` and the autostash drop. The new clause: the operator runs `make upgrade` in the pins worktree seated with `herdr-agents --add-worker .claude/worktrees/pins`, and the script refuses the canonical clone and a stale or dirty pins worktree. Before dispatch the orchestrator takes `git -C <pins worktree> diff`. The worker commits every file it changed, not only the mise config/lock pair, as one class-pure PR that also syncs the `tests/**` expected-version assertions (T37 #209, T53 #224) and passes `make require-crit-review`. Acceptance compares the PR diff of those files with that pre-dispatch diff, and both come from the same checkout (Bot 4226831998, worker review t117-w3). After the merge the canonical clone is updated as usual with `make update` (README "Lifecycle"); it is never dirty, so its autostash has nothing to re-apply.
- `make check-regime-boundary` "keeps reporting" a dirty canonical clone, "now as a sign that something ran where it must not" (it replaces "never leave that diff dirty across sessions"). The closing sentence now reads "The canonical clone is pull and apply only and untouched by any seat: no edits, no `make upgrade`, no apply from a dirty tree…".

**`home/dot_config/claude/rules/agmsg-orchestration.md`**: Delegation bullet `pull, apply and make upgrade only` → `pull and apply only`.

**`scripts/check-regime-boundary.sh`**: the differs line now reads `…; run make upgrade only in the pins worktree (herdr-agents --add-worker .claude/worktrees/pins); restore a merged pins diff with git -C ${canon} restore -SW --source=${ref} -- <files> and drop its autostash`. The section comment says the clone stays pull/apply only, so a diff, stash or unmerged entry means something ran where it must not. The other three lines are unchanged.

**Tests**
- `tests/unit/test_herdr_agents.py`: the two differs-line assertions follow the new wording. Amendment 2: `test_make_update_and_upgrade_include_agmsg_bootstrap` pinned the removed Makefile line and failed all four CI test jobs on 6000cfb4 (validation §6b). It is renamed `test_make_update_includes_and_upgrade_excludes_agmsg_bootstrap` and now asserts that `make -n update` prints `make agmsg-bootstrap` and `make -n upgrade` does not. Nothing else in that module changed.
- `tests/unit/test_runtime_health.py` (Amendment 1): `test_upgrade_applies_mise_only_from_successful_canonical_checkout` sets `CHEZMOI_ALLOW_UPGRADE_IN_SOURCE=1` for its `canonical=True` subtests, the only remaining path to the canonical branch of `apply_upgraded_mise_config` (unchanged). The new `test_upgrade_refuses_the_canonical_clone_and_a_dirty_or_stale_checkout` uses `upgrade_fixture` (fake `chezmoi` and tools on PATH) with a committed `tracked` file and `refs/remotes/origin/main` set by `update-ref` (no `origin` remote, so the guard's fetch fails offline). It covers canonical → exit 2 with the first message and no `==>` phase heading; tracked edit → exit 2 with the second message; `HEAD` one commit past `origin/main` (subtest `moved`) → exit 2 with the second message; and clean at `origin/main` → exit 0, no refusal, the fetch warning, `Upgrade summary:`. Untracked-only is covered implicitly, since the fixture's `bin/`, `scripts/` and `home/` stay untracked in every case.

## Decisions and deviations

- **Task-file contradiction, bare pull.** Line 13 gives the operator one-liner as `git -C ~/.local/share/chezmoi pull && make -C ~/.local/share/chezmoi update`, while line 19 says the bare `git -C ~/.local/share/chezmoi pull` "disappears from every documented one-liner" because `make update` already fetches and fast-forwards only a clean `main`. I followed line 19, the procedure section, which gives the reason. No document adds a bare pull.
- **Step 4 path, deviation from the literal.** Lines 13 and 19 write the post-merge update as `make -C ~/.local/share/chezmoi update`. The Codex Bot (4226889624) pointed out that the same README block says `sourceDir` may be configured elsewhere and derives the root from `chezmoi source-path` for that reason. So step 4 uses `make -C "$(git -C "$(chezmoi source-path)" rev-parse --show-toplevel)" update`, and the SKILL names `make update` without a path, so the path lives once, in the README. On a default machine this resolves to the same `~/.local/share/chezmoi`.
- **Guard placement.** Both guards are one function, called after `parse_args`. The canonical check runs before the fetch, so a canonical-clone run refuses without touching the network.
- **No new test file.** Amendment 1 moved the guard cases into `test_runtime_health.py`, so `tests/unit/test_upgrade_tools_guard.py` was not created.
- **`git -C <pins worktree> diff` and added files.** The SKILL names plain `git diff`, as the task does. A file that `make upgrade` newly adds would be untracked and absent from it. No current upgrade phase creates a tracked file (they rewrite the mise config and lock, the manifest and rendered pins), so I did not add an untracked-file clause; the README and SKILL now say "the files make upgrade changed", without "tracked".

## Out of scope, reported, not edited

- **`README.md` line 392**, fixed in revise round 1 (c6cd343f); the round-0 note follows. Agent setup block, outside the allowed line ranges at round 0: `# Then upgrade installed tools using the applied mise and agent settings.` / `make upgrade` follows a `make update` in the canonical clone, so as written it is now refused with exit 2 and the instructions. A one-line follow-up should point it at the lifecycle procedure.
- **Sandbox-only baseline failures**, identical on `origin/main` in this sandbox (validation §4 and §6): `tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_bumps_terminal_and_crit_pins_from_fetched_artifacts` and `tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_github_extensions_are_warning_only`. In both, the terminal-pin phase warns in the sandbox. The seven canonical-clone boundary tests in `test_herdr_agents.py` fail in the sandbox on both trees (signing key read-denied) and pass with `GIT_CONFIG_GLOBAL=/dev/null` (validation §5). The full local suite on the final head fails exactly the same 193 test ids as `origin/main` b37937ca in this sandbox, none only on the final head (validation §6a); CI runs it green on all four test jobs (§8).
- `home/dot_codex/rules/default.rules:190`, `tests/unit/test_aws_cli_acquisition.py:13` and `executable_herdr-agents:692` are unchanged, as the task grounded.

## User-visible change (also in the PR body)

- `make upgrade` in `~/.local/share/chezmoi` now exits 2 with instructions, and so does any checkout whose tracked tree is dirty or whose `HEAD` is not the fetched `origin/main`. Override: `CHEZMOI_ALLOW_UPGRADE_IN_SOURCE=1`.
- New mise-managed tool versions reach `~/.config/mise` only after the pins PR merges and `make update` runs; Homebrew, uv tool and gh extension upgrades still land immediately.
- `make upgrade` no longer runs `agmsg-bootstrap`.

## Review

- **Worker-side independent agent review.** A separate read-only subagent reviewed 6000cfb4 and returned one P1 (the Makefile test, fixed through Amendment 2 in b2b7be60) and five P3s: four fixed in b2b7be60, and README line 392 reported as out of scope. Evidence: `.orchestration/validation/dotfiles-T117-upgrade-outside-canonical-clone-a01-worker-crit.json` and `-worker-review-receipt.md` (`review_outcome: addressed`, head 8e7a1866). Crit data was unavailable.
- **Bot.** The Codex Bot reviewed 6000cfb4 and b2b7be60 (three P2 threads each). The round-0 head 8e7a1866 drew no review within 15 minutes: `bot: none` (validation §10). The round-1 head c6cd343f drew none either: `bot: none`, no comments (validation §R1.8). CodeRabbit auto review is disabled. The Codex security review of 6000cfb4 completed with no findings.
- **Threads.** Six unresolved, all P2. The worker resolves none.
  - `4226831987` (README step 1 seats the worker under the canonical clone): `fixed:8e7a1866`. The working clone is passed as `DIR`.
  - `4226831998` (scope the acceptance comparison to upgrade-produced paths): `fixed:b2b7be60`. The SKILL compares the PR diff of those files.
  - `4226832007` (allow a failed upgrade to be resumed): `not-applicable`, accepted by the orchestrator in revise round 1. Task line 12 requires the refusal unless the tracked tree is clean, and a resume mode that accepts local edits is the state that guard exists to forbid. Every phase re-derives its pins from upstream, so discard and re-run loses nothing but time, and b2b7be60 documents it in the README.
  - `4226889615` (refuse when the fetch fails): `fixed:c6cd343f` (revise round 1). Round 0 had proposed `not-applicable`.
  - `4226889624` (hard-coded `~/.local/share/chezmoi` in step 4): `fixed:8e7a1866`. The path is derived from `chezmoi source-path` (see Decisions).
  - `4226889631` (fail closed when the source cannot be resolved): `fixed:c6cd343f` (revise round 1). An installed chezmoi that cannot resolve its source is refused; absence still skips the canonical check.

## CompactionDB

Run from the main checkout through the permission gate (validation §7):

```
cd ~/Workspace/dotfiles && uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content '<the task file [memory:decision] line, verbatim>'
uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind failure --scope project --content '<the task file [memory:failure] line, verbatim>'
```

[memory:decision] dotfiles-T117 (worker 2026-10-09): `scripts/upgrade-tools.sh` `require_pins_checkout` refuses the canonical chezmoi clone and any checkout whose tracked tree is dirty or whose HEAD is not the fetched `origin/main`, both with exit 2 before any phase; `CHEZMOI_ALLOW_UPGRADE_IN_SOURCE=1` skips both, and is the only path left to the canonical `chezmoi apply` of the mise config.

## Hooks

- The Understand-Anything stale-graph hook did not fire in this task.

cost: n/a
