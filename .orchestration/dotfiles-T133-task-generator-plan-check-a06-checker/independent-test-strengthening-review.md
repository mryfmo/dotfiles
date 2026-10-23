# Independent test-strengthening review

The reviewed production bytes remain unchanged. The test-only strengthening is correct, and no new finding was identified. This approval is bound to the source and test hashes below; all previous reports, records and the 13-selector proof are preserved.

| File | SHA-256 |
| --- | --- |
| `scripts/orchestrator/task-consistency-check.py` | `42183ecc521ae501e705d23a36d3cdb3394298c33eb00b45205a7911092b2d9e` |
| `tests/unit/test_task_consistency_c11_c15.py` | `55c31abd30f195965013a26b21ded96b6fefd758a6675d10d7836700a6358080` |
| `tests/unit/test_task_checkers.py` | `20eff6f4cf0cbdb55da3f1265edaec6a3479f238a08a7ef36abfe03a8968e99f` |
| a06 `task.md` | `b9e04cb9b2fdb9d4fea9f8f93eec3a88de55b72d5114797103c98e9784b572af` |

The additional case enumerates only the NFC filename while its matching NFD row and literal scope resolve to a different target. It requires C12 and expressly excludes a collision diagnostic. Changing the modeled targets from `.txt` to `.py` makes their resolved classification applied, so this exercises coverage identity independently of collision refusal. The previous collision and valid controls remain.

Independently verified that these are the only test changes: removing the three new lines and changing the one modeled target suffix back to `.txt` reconstructs SHA-256 `3d7b31c8782b65e73972e72c18d39f2ed5cf24e52c24eb7c8243fdf6bea0f56a`, the exact test file used by the prior 13-selector proof.

Exact read-only comparison command, exit 0:

```sh
"$HOME/.local/share/mise/installs/python/3.15.0/bin/python3.15" -I - <<'PY'
import hashlib
from pathlib import Path
text = Path('tests/unit/test_task_consistency_c11_c15.py').read_text()
block = '''            if destinations is targets:
                one = prefix.replace(repr([Path(nfc).name, Path(nfd).name]), repr([Path(nfc).name]))
                self.assertNotIn("path collision:", self.finding("C12", prefix=one))
'''
assert text.count(block) == 1
prior = text.replace(block, '').replace('tests/fixtures/target-{i}.py', 'tests/fixtures/target-{i}.txt', 1)
actual = hashlib.sha256(prior.encode()).hexdigest()
print(actual)
assert actual == '3d7b31c8782b65e73972e72c18d39f2ed5cf24e52c24eb7c8243fdf6bea0f56a'
PY
```

The printed digest matched the assertion. No worktree file was edited by this comparison.

Ran `TaskConsistencyC11C15Test.test_canonical_path_pipeline_rejects_normalised_collisions` independently on both runtimes. `independent-test-strengthening-commands.json` contains exact expanded argv, environment, working directory, executable hashes, before/after source/test/task bindings and exits. The driver exited 0 after confirming unchanged hashes and successful test processes.

| Runtime | Actual exit | Observed result | Complete output |
| --- | --- | --- | --- |
| Python 3.15.0 | 0 | 1 test, OK, one native subtest skipped | `independent-test-strengthening-3.15.0.log` |
| Python 3.12.15 | 0 | 1 test, OK, one native subtest skipped | `independent-test-strengthening-3.12.15.log` |

Both processes executed the new assertion and the existing modeled controls before the native collision subtest skipped. The skip reason is the observed NFC/NFD samefile alias on this filesystem. This is not a zero-test result or a skipped modeled identity check; it supplies no native normalization-sensitive filesystem coverage.

The production review and 13-selector runs remain recorded in `independent-final-verification.md`, its JSON, command record and per-runtime logs. The three earlier findings remain resolved on unchanged production bytes.

Measured numstat against `60a6fb2b`: checker 416 additions + 27 deletions = 443; legacy tests 35 + 22 = 57; new tests 655 + 0 = 655; combined tests 712. These fit the amended 450/720 caps.

The parent's complete-module, historical-red and mutation claims are not independently rerun here. No source/test edits, network, browser, Bats, gate, commit or integration action. Existing parent-execution and same-UID residual risks remain. This is local process evidence, not reviewer authentication or integration authority.

Verdict: correct
