# T66e: Platform-identical strict path resolution in the workspace layer (CI macOS finding)

task_id: T66e
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-conformance
worker: codex-deep-dot
plan: PLAN-pi-worker-integration.md (Phase 2; PR #134 CI finding)
depends: T66d (accepted)

[memory: failure — PR #134 CI: the symlink-LOOP workspace test returned allow on macOS while ubuntu asked, because non-strict os.path.realpath resolves "as far as possible" platform-dependently; workspace path resolution must be strict (parent resolved with strict=True, final component lstat-checked, every OSError -> fall-through ask) so decisions are byte-identical across platforms.]

## CI evidence

test (macos-14): test_pi_workspace_rejects_path_escapes_root_and_symlink_escape
subtest path='loop/file.txt' -> AssertionError:
'{"decision":"allow"}' != '{"decision":"ask"}'; ubuntu jobs were
fail-fast-canceled after 374 OK. Local macOS runs passed (environment
delta), confirming the resolution is version/platform sensitive — hence
strictness, not tuning.

## Fix (exact)

1. executable_permgate workspace layer (write/edit and the read
   sensitive-path resolution alike): resolve the CANDIDATE's PARENT
   directory with os.path.realpath(parent, strict=True) inside try;
   OSError (ELOOP, ENOENT, EACCES, anything) -> fall through (ask).
   Then lstat the final component: if it exists and is a symlink ->
   fall through (ask) for write/edit (never write through a link), and
   for read resolve it strictly too (loop -> ask). Re-append the final
   name to the strictly resolved parent for the prefix comparison.
   cwd resolution likewise strict=True (existing dir; failure -> ask).
2. No behavior change for the clean cases (in-cwd plain path allow;
   plain escape fall-through) — pin with regression tests.
3. Tests: convert the loop case to assert ask deterministically on BOTH
   platforms (the strict resolver makes the outcome
   platform-independent); add: parent-ELOOP, nonexistent-parent,
   final-component-symlink (write denied path), read-through-symlink to
   a sensitive target (must deny via the resolved target), macOS
   /var vs /private/var equivalence (cwd given via the symlinked form
   still allows in-workspace writes — strict resolution of both sides).

## Allowed files

- home/dot_local/bin/common/executable_permgate
- tests/unit/ (matching module)
- Your artifact paths (T66e five artifacts)

## Forbidden actions

git commit; git push; chezmoi apply; bats; dependency changes; real pi
execution; claude/codex path changes; scope loosening.

## Validation

make format / unit-test / validate-agent-assets green; diff pasted;
scope check. State explicitly which python version guarantees
strict= support (>=3.10; the repo floor already satisfies it — verify).

## Completion / RESULT contract

Five artifacts; memory add (kind=failure); effects=none. Orchestrator
pushes to PR #134 and reruns CI.
Reply `AGMSG-RESULT v1 task_id=T66e`. max_turns=15.
