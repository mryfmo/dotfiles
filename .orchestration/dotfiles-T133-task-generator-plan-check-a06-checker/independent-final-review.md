# Independent final pipeline review

Review date: 2026-10-20. Reviewer: independent Codex subagent.
Changeset: working tree against `60a6fb2b324d0381c4a6e539b37c650105154a7e`.
Read the complete checker, both affected test modules, their diff, and the a06 task contract.
No source or test edits, network, Bats, or browser review.

## Binding

| File | SHA-256 |
| --- | --- |
| `scripts/orchestrator/task-consistency-check.py` | `5c09a95ad36f07ad28958ee9d9efcbb25cb8db64795ed8d655485047121a3cf3` |
| `tests/unit/test_task_consistency_c11_c15.py` | `2979c99ff8055071340a0888e755b6a87719e486d80ff8033af0ec15072dd862` |
| `tests/unit/test_task_checkers.py` | `20eff6f4cf0cbdb55da3f1265edaec6a3479f238a08a7ef36abfe03a8968e99f` |

## Findings

1. **P1, high confidence, `scripts/orchestrator/task-consistency-check.py:440`.**
   The new pipeline strips the trailing slash from directory scopes: `path_entry(root, "scripts/")[2]` becomes `scripts`. The final match therefore drops every descendant before checking confinement or directory aliases. A real CLI fixture with an outside-pointing `scripts/escape.py` symlink exits 0 and prints `OK` with `allowed_files: ["scripts/"]`, but exits 1 with `C12 confinement` for `scripts/**`. Preserve the scope's directory semantics when matching the pipeline key. This is the existing scope-filter/confinement finding class, so the owner must disposition it before another repair round.
2. **P2, high confidence, `scripts/orchestrator/task-consistency-check.py:387`.**
   The C10 extraction regex excludes Unicode combining marks, so decomposed names never reach its new `path_entry` confinement check. A docs sentence naming an escaping `scripts/cafe\u0301.py` before a later `once` clause passes, while the equivalent NFC spelling fails with C10. The later clause suppresses C9 but does not waive C10's confinement check. The regex predates this pipeline, but leaving that consumer outside original-path validation misses the a06 contract. The fix must retain the original extracted spelling until resolution.

Both findings remain unresolved; this review provides no approval.

## Additional inspection

- Collision detection runs before coverage and revokes the whole comparison key, including distinct enumerated names that resolve to one target. The existing modeled same-target test exercises this branch.
- Repeated enumeration of the identical `Path` through overlapping scopes does not create a collision. Row coverage additionally requires the comparison key and `samefile` identity.
- Original-path resolution remains present in C6, C11, C14 and resolved C16 applicability. C10's extraction gap is reported above.
- Retained interpreter precedence, checkout/shim refusal, child token environment forwarding, fixed canonical host/repository/SHA, C14 digest authorization and nonzero status handling remain in the inspected code. The complete focused module passed their existing controls.
- Source/test change totals observed: production 412 additions + 26 deletions = 438; tests 676 additions + 22 deletions = 698.

## Exact reproduction

Executed from the assigned worker worktree. The heredoc runs the real checker through the existing temporary-repository fixture. Only the output log below is a persistent artifact; no runtime helper was added.

```sh
PATH=/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/a012-a05-runtime-ze2fbz0e/parent-bin:/usr/bin:/bin UV_CACHE_DIR="$PWD/.uv-cache" TRUSTED_PYTHON="$HOME/.local/share/mise/installs/python/3.15.0/bin/python3.15" "$HOME/.local/share/mise/installs/python/3.15.0/bin/python3.15" -I - <<'PY' > .orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-final-review-repro.log 2>&1
import contextlib, hashlib, io, sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd() / 'tests/unit'))
from test_task_consistency_c11_c15 import TaskConsistencyC11C15Test
print('python', sys.version)
for name in ('scripts/orchestrator/task-consistency-check.py', 'tests/unit/test_task_consistency_c11_c15.py', 'tests/unit/test_task_checkers.py'):
    print('sha256', name, hashlib.sha256(Path(name).read_bytes()).hexdigest())
with contextlib.redirect_stdout(io.StringIO()):
    TaskConsistencyC11C15Test.setUpClass()
case = TaskConsistencyC11C15Test()
case.setUp()
try:
    outside = case.temp / 'outside.py'
    outside.write_text('outside\n')
    (case.repo / 'scripts/escape.py').symlink_to(outside)
    for scope in ('scripts/', 'scripts/**'):
        case.task(allowed=[scope])
        rc, out = case.check()
        print(f'SCOPE={scope!r} EXIT={rc}\n{out}')
    (case.repo / 'scripts/escape.py').unlink()
    (case.repo / 'scripts/cafe\u0301.py').symlink_to(outside)
    for name in ('scripts/caf\u00e9.py', 'scripts/cafe\u0301.py'):
        case.task(kind='docs', body=f'"{name} must support `mode=1` once the separate feature lands."')
        rc, out = case.check()
        print(f'NAME={ascii(name)} EXIT={rc}\n{out}')
finally:
    case.doCleanups()
PY
```

Outer command exit: 0. Complete stdout/stderr, native runtime version, bound hashes and all four child exits are in `independent-final-review-repro.log`. Observed child exits: trailing-slash scope 0; glob control 1; NFC C10 control 1; NFD C10 bypass 0.

## Existing module validation

The complete `test_task_consistency_c11_c15` module was run using native Python 3.15.0 with `-I`, the same explicit PATH and cache above, and the absolute validated `tests/unit` root inserted into `sys.path`. The isolated heredoc loaded the module with `unittest.defaultTestLoader.loadTestsFromName`, ran `unittest.TextTestRunner(verbosity=2)`, and exited with `not result.wasSuccessful()`.

Observed exit 0: `Ran 26 tests in 31.542s`, `OK (skipped=1)`.
Native case-insensitivity was observed as true. Native NFC/NFD distinctness was observed as false; only the native two-file collision subtest skipped. The modeled distinct-file and same-target collision controls and one-file control ran.

Not rerun here: Python 3.12, the legacy module, full unit suite, mutation suite, lint, CI or live API validation. Parent process and same-UID risks remain outside this review's controls.

Verdict: incorrect
