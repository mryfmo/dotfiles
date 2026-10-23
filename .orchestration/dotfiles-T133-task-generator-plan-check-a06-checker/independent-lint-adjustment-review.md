# Independent lint-adjustment review

Reviewed source SHA-256: `1779440ff4274ccdcf19dc68193a73ca78dea904528bb2647419ece1e8d201b7`.
Test SHA-256: `7ba89c81cca29144d5702c056f45547cee8ce83d2ed7c4572f9fc8819de7ed61`.
Legacy test SHA-256: `20eff6f4cf0cbdb55da3f1265edaec6a3479f238a08a7ef36abfe03a8968e99f`.
The prior repair verification approves only its explicitly bound `98c0904f` source; it does not approve this adjustment.

**P2, high confidence — `scripts/orchestrator/task-consistency-check.py:476`.**
Passing an enumerated filesystem name through `normalise_name` discards applied-prefix classification for valid POSIX filenames containing a backslash. The metadata grammar deliberately rejects backslashes, but the wildcard enumerator must still recognize actual files under `scripts/` as applied. With an extensionless `scripts/evil\name` file, `scripts/**` scope, and a concrete row only for the ordinary `scripts/tool.py`, this source exits 0 / OK. Restoring only the prior prefix-classification expression in the temporary checker copy produces exit 1 / C12 unsafe or unnamed. The fix must preserve filesystem-name classification without weakening the task operand grammar.

Reported promptly to the parent before any repair. No worktree source/test changes were made. Only the disposable fixture's copied checker was altered for the one-expression comparison. The record remains unresolved and requires owner disposition.

Exact command, run from the assigned worktree:

```sh
PATH=/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/a012-a05-runtime-ze2fbz0e/parent-bin:/usr/bin:/bin UV_CACHE_DIR="$PWD/.uv-cache" TRUSTED_PYTHON="$HOME/.local/share/mise/installs/python/3.15.0/bin/python3.15" "$HOME/.local/share/mise/installs/python/3.15.0/bin/python3.15" -I - <<'PY'
import sys
from pathlib import Path
sys.path.insert(0,str(Path.cwd()/'tests/unit'))
from test_task_consistency_c11_c15 import TaskConsistencyC11C15Test, RESIDUAL
TaskConsistencyC11C15Test.setUpClass()
c=TaskConsistencyC11C15Test();c.setUp()
try:
    c.put('scripts/evil\\name','applied script\n')
    c.task(allowed=['scripts/**'],extra=[dict(control='scripts/tool.py',disposition=RESIDUAL)])
    rc,out=c.check();print('current',rc,out)
    c.script.write_text(c.script.read_text().replace('(normalise_name(resolved) or "").startswith(APPLIED_DIRS)', 'resolved.startswith(APPLIED_DIRS)'))
    rc,out=c.check();print('previous classification clause only',rc,out)
finally:
    c.doCleanups()
PY
```

Outer command exit: 0. Actual checker exits: current 0; previous classification clause only 1. The latter is a counterfactual one-expression control, not a complete historical-source run.

```text
current 0 t-a01.md: OK
api-input-sha256 5a84b79716842f146f7533d890cc7308cad7b21abdc29c1852c6b3bb8ad66672
canonical-main aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
api-input-sha256 eac1a220d55f355b06773fad79f256881d14d7842d318ed7b9e33ec7156a18db

previous classification clause only 1 t-a01.md: FAIL
  C12 the scope scripts/** matches unsafe or unnamed scripts/evil\name
api-input-sha256 5a84b79716842f146f7533d890cc7308cad7b21abdc29c1852c6b3bb8ad66672
canonical-main aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
api-input-sha256 eac1a220d55f355b06773fad79f256881d14d7842d318ed7b9e33ec7156a18db
```

The fixture cache bootstrap also exited 0 using the previously validated Python 3.15.0 and uv 0.13.1 bindings. No assertion/import/provisioning error accounts for either result.

Not rerun on these bytes: Python 3.12, complete modules, mutation suite, lint or CI. No network, browser, Bats, gate, commit or integration action. Existing parent-execution and same-UID risks remain.

Verdict: incorrect
