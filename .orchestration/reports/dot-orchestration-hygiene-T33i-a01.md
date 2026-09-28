# T33i report — dot-orchestration-hygiene-T33i-a01 (revision 3)

- worker: `claude-standard-dot-a005`; orchestrator: `claude-remediation-dot`
- worktree: `/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c` (clean before the switch)
- branch: `fix/orchestration-hygiene-T33i` from `origin/main` = `013b3d6`
- task_rev: sha256 `3fac6e1c5efd6dcae0e5ef6bd7c4843a0afd159ae5ba61ae3eef1722beaba16e`, checked
- cleanup: deleted the merged local branch `fix/permgate-codex-stdin` (was `6bc5918`), as the task allows
- PR: https://github.com/mryfmo/dotfiles/pull/204, head `19941426f261f79ca66fd9556bac457f57688f8f` (rev3; rev2 head `bb190d5`, rev1 head `18c7164`)
- status: ready_for_review. CI is green on rev3 head 1994142 (and earlier on bb190d5 and 18c7164): all checks pass except nix, which was skipped. Verbatim `gh pr checks 204` output is in the validation file.

## Revision 3 (AGMSG-ACCEPTANCE status=revise, 2026-09-28T22:37:04Z)

The visible-lane audit of `bb190d5` found a confirmed P2. If a tracked
validator was deleted from the working tree, the `-f` test was false, so the
step took the "repository has no validator" exception and unmasked evidence
could pass. The fix is `1994142` on the same branch and PR #204.

1. **The exception now comes from git.** Masking is skipped silently only
   when all three of these hold:
   - `git ls-files --error-unmatch -- scripts/validate-agent-assets.py` fails,
     which is the ruled condition;
   - `git cat-file -e HEAD:scripts/validate-agent-assets.py` fails;
   - nothing is at that path, not even a dangling symlink.

   In every other case the full guard applies. The masker is refused (WARN,
   then `Audit verdict: unmasked`, exit 1) when:
   - the tracked validator is missing from the tree;
   - the validator is untracked;
   - it differs from `HEAD`;
   - DIR is at the audited commit.
2. **Deviations from the literal next_action, both stricter.**
   - The skip also requires `HEAD` to lack the path. `git rm` drops the file
     from the index *and* the tree, so an `ls-files` check alone would take
     the skip again while `HEAD` still has the validator. This matches the
     ruling's own gloss: "path-not-tracked-at-HEAD".
   - The skip also requires the path to be absent on disk. Without that, an
     untracked copy would make `ls-files` fail and be skipped, which
     contradicts the ruling's "untracked copy -> unmasked".
3. **Tests.** New `test_audit_refuses_a_tracked_masker_missing_from_the_tree`
   has two subtests, `deleted` (the file is unlinked) and `removed-from-index`
   (`git rm`). Both expect exit 1, `unmasked`, and the refusal WARN.
   - The WARN wording changed, so the rev2 audited-commit test now asserts the
     stable prefix `refusing to run the masker`.
   - The existing skip, untracked, modified and audited-commit cases are kept.
4. **Mutation baseline** against unmodified `bb190d5` (checked as no diff
   from HEAD): 2 failures out of 7, namely both new subtests. After the fix:
   26/26 audit tests, `make unit-test` 522 OK, `make validate-agent-assets`
   ok, and `shellcheck -x` and `shfmt` clean.
5. **Docs.** The shdoc `@description` and the README `--audit` sentence now
   state the git-based skip rule.
6. **Still open from rev2.** An audit of the commit DIR has checked out still
   ends as `unmasked`. That case still needs your decision.

7. **CompactionDB (rev3).** `[memory:decision]` recorded with:
   `python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "T33i rev3: herdr-agents --audit decides the mask exception from git: masking is skipped only when git tracks no scripts/validate-agent-assets.py (ls-files fails and HEAD lacks it) and nothing is on disk; a tracked validator missing from the tree, an untracked copy, a changed validator, or DIR at the audited commit ends the audit as unmasked with exit 1 (operator ruling 2026-09-28)."`
   The output is in the validation file.

## Revision 2 (AGMSG-ACCEPTANCE status=revise, 2026-09-28T22:09:48Z)

The visible-lane audit of `18c7164` gave `Verdict: incorrect`. The P2 was
accepted; the P1 was partly refuted but leaves a real residual. The fix is
commit `bb190d5` on the same branch and PR #204.

1. **A failed mask now fails the audit (P2).** A failed `--mask-secrets`
   call now prints `Audit verdict: unmasked` and exits 1 **before** the
   verdict gate, so the gate never reports `correct` with unmasked
   evidence. Before this change it only warned.
2. **Trust guard (P1 residual).** When `DIR/scripts/validate-agent-assets.py`
   exists, the masker is refused (a `WARN: herdr-agents: refusing to run the
   masker in DIR: it is the audited commit or has uncommitted changes;
   evidence stays unmasked.` line on stderr, then `Audit verdict:
   unmasked`, exit 1) when any of these hold:
   - `git -C DIR rev-parse HEAD` equals the audited commit's full sha
     (`git rev-parse --verify <sha>^{commit}`);
   - the validator is **untracked** (`git ls-files --error-unmatch`). I
     added this because `git diff --quiet HEAD` cannot see an untracked
     file;
   - the validator has **uncommitted changes, staged or unstaged**
     (`git diff --quiet HEAD -- scripts/validate-agent-assets.py`).

   A validator that is present while `python3` is missing also fails closed
   as `unmasked`. With no validator in DIR (another repository), the step
   is still skipped silently.
3. **Documentation.** The assumption is now stated in the shdoc
   `@description` (audit mode) and in the README `--audit` sentence: DIR is
   the orchestrator's own checkout, and the audited commit is only fetched.
4. **Tests.** The fake repo validator now lives in a git-committed DIR (a
   test-local `git init` with global and system config isolated). New
   cases:
   - `test_audit_fails_as_unmasked_when_masking_fails`: the masker exits 1,
     so the result is exit 1 with `unmasked` and no `correct`.
   - `test_audit_refuses_the_masker_from_the_audited_commit`: running
     `--audit <DIR HEAD>` gives exit 1, `unmasked`, the WARN, and **no**
     masker call.
   - `test_audit_refuses_an_uncommitted_or_untracked_masker`, with subtests
     `modified` and `untracked`: exit 1, `unmasked`, and no masker call.

   The existing mask tests are unchanged and pass on the committed fixture.
5. **Mutation baseline** against unmodified `18c7164` (checked as no diff
   from HEAD before the run): **4 failures** across 6 mask tests, namely all
   new guard and propagation cases. The 2 pre-existing mask tests pass on
   both versions. After the fix, 25/25 audit tests pass,
   `make unit-test` gives 521 OK, `make validate-agent-assets` is ok, and
   `shellcheck -x` and `shfmt` are clean.
6. **Consequence to be aware of, not changed.** A post-merge audit of the
   commit that DIR currently has checked out will now always end as
   `Audit verdict: unmasked` (exit 1). An example is auditing the merge
   commit at main's HEAD, as the T32b live audit of `6b9babc` did. This is
   exactly the ruling's "HEAD equals the audited commit" guard. The
   workaround is to run such audits from a checkout whose HEAD is not the
   audited commit, or to accept `unmasked` and mask manually. Please decide
   whether that case needs a different rule, for example comparing against
   the validator blob rather than the whole commit.

7. **CompactionDB (rev2).** `[memory:decision]` recorded with:
   `python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "T33i rev2: herdr-agents --audit fails closed (Audit verdict: unmasked, exit 1) when masking fails, when python3 is missing, or when the masker is untrusted (DIR HEAD equals the audited commit, or scripts/validate-agent-assets.py is untracked or differs from HEAD); DIR is assumed to be the orchestrator checkout (operator ruling 2026-09-28)."`
   The output is in the validation file.

## 1. Audit-evidence secret masking (mechanical) (revision 1)

- **`scripts/validate-agent-assets.py`.**
  - New `mask_secret_matches(text)` and `mask_secrets(paths)`, and a
    `--mask-secrets <file>...` entry point checked before `main()`.
  - **Single source of truth.** The allowed placeholders become one
    `ALLOWED_SECRET_PLACEHOLDERS` constant, with a shared
    `strip_allowed_secret_placeholders()` that the committed-secret scan now
    uses as well. `SECRET_PATTERN` and the scan's coverage are unchanged:
    the same files and the same pattern.
  - **Line-level mirror of the scan.** A line is masked only when its
    placeholder-stripped form still matches, and every other line is kept
    byte for byte. A final whole-text pass covers a match that spans lines,
    so masked output always passes the scan. My first version tested only
    the match text, and the allowed-placeholder test caught it, because the
    regex match starts at the "TOKEN, colon, quoted value" part, which is inside the placeholder name.
  - **Output.** It prints `masked <n> match(es) in <file>` per file and
    exits 0. It exits 2 on any missing file, naming it on stderr, without
    touching the others.
  - **Real data.** On a scratch copy of `04746ca:.orchestration/validation/dot-ua-graph-refresh-T33c-a01-audit.md`,
    the file that turned main red, it gives `masked 2 match(es)`. The rescan
    then finds 0 remaining matches and 2 redaction markers. Verbatim in the
    validation file.
- **`home/dot_local/bin/common/executable_herdr-agents` `--audit`.**
  - **When.** The step runs right after the `Audit exit:` / `Audit
    evidence:` / `Audit last message:` lines and **before** the exit-status
    check, so a failed audit's evidence is masked too. It is therefore also
    before the verdict gate, which reads the masked last-message file.
    Masking never touches a `Verdict:` line, which cannot match the pattern.
  - **What.** When `DIR/scripts/validate-agent-assets.py` exists and
    `python3` is available, it runs
    `python3 DIR/scripts/validate-agent-assets.py --mask-secrets <files>`
    and prints its output. `<files>` is whichever of the transcript and
    `<evidence>.last.md` exist. Deviation: I pass only existing files,
    because the spec's missing-file exit 2 would otherwise fire on every
    transcript-fallback run. The step is skipped silently otherwise (another
    repository). A mask failure prints a review reminder on stderr and never
    changes the audit result.
  - **Bug caught in review.** My first edit called `has_command`, which does
    not exist in herdr-agents; it would have skipped masking silently. I
    switched to `command -v python3`, which the script already uses.
- **Tests.**
  - `MaskSecretsModeTest` (3 tests):
    - counts and in-place redaction, with `Verdict:` and other lines kept
      and a clean rescan;
    - allowed placeholders left untouched;
    - a missing file gives exit 2 and changes nothing.
  - `test_herdr_agents.py` (3 tests), using a fake DIR validator that logs
    and masks:
    - the mask call runs on both files and prints before `Audit verdict:`;
    - it runs even with a nonzero audit exit, passing only existing files;
    - it is skipped silently without the validator.
  - **Fixtures.** Secret-shaped strings are built at runtime
    (`"tok" + "en"`). My first draft had literal fixtures, and
    `make validate-agent-assets` then failed on the test file itself. I
    caught this before committing, following exactly the rule being
    codified.
  - **Mutation baseline** against the unmodified scripts: 5 of 6 fail. The
    skip case passes on both versions, as a regression guard. Verbatim in
    the validation file.

## 2 and 3. Rule text (quoted)

- `home/dot_config/claude/rules/agmsg-orchestration.md`, a new bullet after
  the boundary bullet, and `home/dot_agents/skills/agmsg-orchestration/SKILL.md`
  "Review and integration invariants", a new bullet after the boundary
  bullet with identical text:
  > Before every `.orchestration` boundary commit, run `make validate-agent-assets` and branch on its real exit status, never through a pipe; fix a failure before pushing, because committed audit evidence can trip the secret scan.
- SKILL "Orchestrator Playbook" step 3, appended:
  > Ground `allowed_files` by grepping the repository for every touch point the task names (tests that pin call sequences, mirrors, fixtures) before dispatch. Verify every CLI constraint the task asserts by running the real command in a safe form, not by reading `--help`. Presume an auditor finding that contradicts your own review is right until you refute it with evidence.

## 4. README

- In the Understand-Anything paragraph:
  > Plugin 2.9.7 has two known coverage gaps: `merge-batch-graphs.py` drops `tested_by` edges from `.bats` tests and from non-`file:` production nodes, and `extract-structure.mjs` misses shell functions with a subshell body. A full rebuild therefore under-reports test coverage until upstream fixes land.
- In the `--audit` paragraph, one sentence (my addition, for accuracy about
  the new visible behaviour):
  > Before the gate, the transcript and last-message file are masked in place with `scripts/validate-agent-assets.py --mask-secrets`, so committed evidence never trips the repository's secret scan.

## Artifact self-check

Following rule 2, I ran `--mask-secrets` on this task's own `.orchestration`
artifacts before sending the RESULT, and then ran the scan over them. The
output is in the validation file. The baseline test output could otherwise
carry rendered fixture strings into the committed validation file.

## CompactionDB

[memory:decision] T33i: audit evidence is secret-masked by `validate-agent-assets.py
--mask-secrets` inside `herdr-agents --audit` before the verdict gate; the orchestrator
validates agent assets (real exit status) before every boundary commit; task authoring
grounds allowed_files by grep, verifies CLI constraints by execution, and presumes auditor
findings right until refuted; the README records the Understand-Anything 2.9.7 coverage
gaps (operator 2026-09-28).

Id `84c2f5f2-399c-4166-a3c7-fb70aaa628aa`; the output is in the validation
file.

## Effects

None outside the repository. Live E2E (a real `--audit` run showing the mask
step) is orchestrator-side.

cost: n/a (the Claude Code runtime does not expose session token/cost figures to the worker)
