---
task_id: dotfiles-T133-trusted-exec-contract-tests-a01
seat: claude-standard-dot-a011
code_head: f4eed1cc
---

# Validation: dotfiles-T133-trusted-exec-contract-tests-a01

Every command below ran inside the sandbox from `.claude/worktrees/worker-d` on the branch `tools/trusted-exec-contract-tests-a01`, created with `--no-track` from `origin/main` `ba318e53`. The tested code head is `f4eed1cc`: the task copy (`e603ac51`), the tests written first (`755d9002`, red), the helper (`4729b83c`) and the worker review's fix round (`f4eed1cc`). The final head adds only records under `.orchestration/dotfiles-T133-trusted-exec-contract-tests-a01/`, so the RESULT carries its diff and CI. `MAIN` is the main checkout, `SCRATCH` the seat's scratchpad, `PY` the observed absolute interpreter, `RED` the test commit and `H` the tested head. The seat's own home directory appears as `$HOME_OF_THE_SEAT` (only in interpreter paths), and the run's temporary `HOME` is a `$TMPDIR` directory. Each block ends with the exit status of the command shown.

## 1. Task copy

````console
$ shasum -a 256 "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md"; cmp "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md" && echo byte-identical
dd7549118bd470af98f52096ee668165a53727981eba4cb8466550641e2dc12c  $MAIN/.orchestration/tasks/dotfiles-T133-trusted-exec-contract-tests-a01.md
dd7549118bd470af98f52096ee668165a53727981eba4cb8466550641e2dc12c  .orchestration/dotfiles-T133-trusted-exec-contract-tests-a01/task.md
byte-identical
[exit 0]
````

````console
$ uv run --offline --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py --root "$PWD" "$MAIN/.orchestration/tasks/$T.md"
dotfiles-T133-trusted-exec-contract-tests-a01.md: OK
[exit 0]
````

## 2. Premises, re-run at worker start, and the observed interpreter

````console
$ python3 --version; uname -s; python3 -c 'import shutil; print("dscl=" + str(shutil.which("dscl"))); print("getent=" + str(shutil.which("getent")))'; git ls-tree --name-only origin/main -- tests/unit/trusted_exec_contract.py; echo "ls-tree exit $?"; git rev-parse origin/main; command -v python3; /usr/bin/python3 -c "import os, sys; print(os.path.realpath(sys.argv[1]))" "$(command -v python3)"; "$PY" -c "import platform; print(platform.python_version(), platform.system(), platform.release())"
Python 3.15.0
Darwin
dscl=/usr/bin/dscl
getent=None
ls-tree exit 0
ba318e5369b14a79d6f515e87b685c9bcb30c12e
$HOME_OF_THE_SEAT/.local/share/mise/installs/python/latest/bin/python3
$HOME_OF_THE_SEAT/.local/share/mise/installs/python/3.15.0/bin/python3.15
3.15.0 Darwin 27.0.0
[exit 0]
````

## 3. Branch and provenance

````console
$ git log --oneline origin/main..HEAD; git merge-base origin/main HEAD; git diff --name-status origin/main...f4eed1cc
f4eed1cc test(unit): the trusted-exec probes after the worker review: whole red reasons, each hostile GIT_* name shown live, the runner argv and env observed, refusal reasons named, a worker-root probe by access time with no FIFO (T133 trusted-exec-contract-tests a01)
4729b83c test(unit): trusted_exec_contract.py, the shared probes of design 5.14 item 7 and the trusted-parent runner (T133 trusted-exec-contract-tests a01)
755d9002 test(unit): the trusted-exec contract probes, each red on a noncompliant consumer stub and green on a compliant one (T133 trusted-exec-contract-tests a01, design 5.14 item 7, red)
e603ac51 docs(orchestration): T133 trusted-exec-contract-tests a01 task copy
ba318e5369b14a79d6f515e87b685c9bcb30c12e
A	.orchestration/dotfiles-T133-trusted-exec-contract-tests-a01/task.md
A	tests/unit/test_trusted_exec_contract.py
A	tests/unit/trusted_exec_contract.py
[exit 0]
````

## 4. Red: the tests at the test commit, before the helper existed

````console
$ git worktree add --detach -q "$SCRATCH/tec-red" "$RED" && (cd "$SCRATCH/tec-red" && uv run --no-project --offline --python "$PY" python -B -m unittest discover -s tests/unit -p test_trusted_exec_contract.py -v) > "$SCRATCH/tec-red.out" 2>&1; rc=$?; echo "unittest exit status: ${rc}"; cat "$SCRATCH/tec-red.out"; git worktree remove --force "$SCRATCH/tec-red"
unittest exit status: 1
test_trusted_exec_contract (unittest.loader._FailedTest.test_trusted_exec_contract) ... ERROR

======================================================================
ERROR: test_trusted_exec_contract (unittest.loader._FailedTest.test_trusted_exec_contract)
----------------------------------------------------------------------
ImportError: Failed to import test module: test_trusted_exec_contract
Traceback (most recent call last):
  File "$HOME_OF_THE_SEAT/.local/share/mise/installs/python/3.15.0/lib/python3.15/unittest/loader.py", line 433, in _find_test_path
    module = self._get_module_from_name(name)
  File "$HOME_OF_THE_SEAT/.local/share/mise/installs/python/3.15.0/lib/python3.15/unittest/loader.py", line 374, in _get_module_from_name
    __import__(name)
    ~~~~~~~~~~^^^^^^
  File "$SCRATCH/tec-red/tests/unit/test_trusted_exec_contract.py", line 21, in <module>
    import trusted_exec_contract as tec
ModuleNotFoundError: No module named 'trusted_exec_contract'. Did you mean: 'test_trusted_exec_contract'?


----------------------------------------------------------------------
Ran 1 test in 0.000s

FAILED (errors=1)
[exit 0]
````

## 5. The Check, with a temporary HOME and UV_CACHE_DIR

The temporary directories are created first and named in the output. Fixture directories (`trusted-exec-*`) under `$TMPDIR` are counted before and after the run, the temporary HOME is listed after it, and this repository's Git configuration is hashed before and after it.

````console
$ git rev-parse HEAD; export TEC_HOME="$(/usr/bin/mktemp -d "$TMPDIR/tec-home.XXXXXX")" TEC_UVC="$(/usr/bin/mktemp -d "$TMPDIR/tec-uvcache.XXXXXX")"; echo "HOME=$TEC_HOME UV_CACHE_DIR=$TEC_UVC"; fixtures() { find "$TMPDIR" -maxdepth 1 -name "trusted-exec-*" | wc -l | tr -d " "; }; gitcfg() { git config --list --show-origin | shasum -a 256 | cut -c1-16; }; echo "fixture dirs before: $(fixtures); git config before: $(gitcfg)"; HOME="$TEC_HOME" UV_CACHE_DIR="$TEC_UVC" uv run --no-project --offline --python "$PY" python -B -m unittest discover -s tests/unit -p test_trusted_exec_contract.py -v; rc=$?; echo "unittest exit status: ${rc}"; echo "fixture dirs after: $(fixtures); git config after: $(gitcfg)"; echo "temporary HOME after the run:"; find "$TEC_HOME" -mindepth 1 | head; echo "(end of listing)"
f4eed1ccecbcabaa609e2ce27accc36910d8aa3c
HOME=$TMPDIR/tec-home.mdnnbj UV_CACHE_DIR=$TMPDIR/tec-uvcache.7KIXJI
fixture dirs before: 0; git config before: 3e9c9ddbc66eac10
test_each_probe_detects_condition (test_trusted_exec_contract.TrustedExecContractTest.test_each_probe_detects_condition) ... ok
test_hostile_git_probe (test_trusted_exec_contract.TrustedExecContractTest.test_hostile_git_probe) ... ok
test_passwd_home_reads_the_directory_service_of_each_platform (test_trusted_exec_contract.TrustedExecContractTest.test_passwd_home_reads_the_directory_service_of_each_platform) ... ok
test_probes_clean_up_after_an_exception (test_trusted_exec_contract.TrustedExecContractTest.test_probes_clean_up_after_an_exception) ... ok
test_sanitized_environment_probe (test_trusted_exec_contract.TrustedExecContractTest.test_sanitized_environment_probe) ... ok
test_shim_probe (test_trusted_exec_contract.TrustedExecContractTest.test_shim_probe) ... ok
test_swapped_file_probe (test_trusted_exec_contract.TrustedExecContractTest.test_swapped_file_probe) ... ok
test_trusted_parent_probe (test_trusted_exec_contract.TrustedExecContractTest.test_trusted_parent_probe) ... ok
test_worker_root_probe (test_trusted_exec_contract.TrustedExecContractTest.test_worker_root_probe) ... ok

----------------------------------------------------------------------
Ran 9 tests in 9.400s

OK
unittest exit status: 0
fixture dirs after: 0; git config after: 3e9c9ddbc66eac10
temporary HOME after the run:
(end of listing)
[exit 0]
````

The same suite under the default interpreter `uv` picks here (Python 3.10), which the repository's `make unit-test` would use:

````console
$ HOME="$(/usr/bin/mktemp -d "$TMPDIR/tec-home.XXXXXX")" uv run --no-project --offline python -B -c "import sys; print(sys.version.split()[0])"; HOME="$(/usr/bin/mktemp -d "$TMPDIR/tec-home.XXXXXX")" uv run --no-project --offline python -B -m unittest discover -s tests/unit -p test_trusted_exec_contract.py 2>&1 | tail -3
3.15.0
Ran 9 tests in 11.649s

OK
[exit 0]
````

## 6. Each probe, red against a deliberately failing stub and green against a compliant one

Each `case_*` function of the test module runs the noncompliant stub inside `assertRaisesRegex`, so it fails unless the probe assertion fails for the intended reason, then runs the compliant stub, which must pass. It returns the noncompliant stub's observed failure text. The selectors are the threat row's. The aggregate selector runs the same six cases as subtests (§5).

````console
$ cat "$SCRATCH/tec-cases.py"; HOME="$(/usr/bin/mktemp -d "$TMPDIR/tec-home.XXXXXX")" "$PY" -B "$SCRATCH/tec-cases.py"
"""Print each probe's red reason (noncompliant stub) and green result (compliant stub) from the test module's cases."""

import re
import sys

sys.path.insert(0, "tests/unit")
import test_trusted_exec_contract as m  # noqa: E402

SELECTORS = {
    "shim_on_path": "test_shim_probe",
    "hostile_git": "test_hostile_git_probe",
    "worker_root": "test_worker_root_probe",
    "swapped_file": "test_swapped_file_probe",
    "sanitized_environment": "test_sanitized_environment_probe",
    "trusted_parent": "test_trusted_parent_probe",
}


def elide(text):
    """The runner's inherited variable names stay out of the record: only their count, and whether LEAK is one."""

    def count(match):
        names = match.group(1).split(", ")
        return f"undeclared: [{len(names)} inherited names elided; 'LEAK' among them: {repr('LEAK') in names}]"

    text = re.sub(r"undeclared: \[([^\]]*)\]", count, text)
    return re.sub(r"PATH is '[^']*'", "PATH is <the inherited value, elided>", text)


for name in m.TrustedExecContractTest.CASES:
    case = m.TrustedExecContractTest("test_each_probe_detects_condition")
    try:
        reason = getattr(case, "case_" + name)()
        print(
            f"{name} (TrustedExecContractTest::{SELECTORS[name]}): red: {elide(reason)!r}; green: the compliant stub passed"
        )
    finally:
        case.doCleanups()
shim_on_path (TrustedExecContractTest::test_shim_probe): red: "shim ran: git ['$TMPDIR/trusted-exec-psvww7ko/bin/git', 'status', 'a b', '']"; green: the compliant stub passed
hostile_git (TrustedExecContractTest::test_hostile_git_probe): red: 'environment: hostile git: attacker root $TMPDIR/trusted-exec-x9x964i1/attacker; attacker content; attacker hook ran; local-worktree: hostile git: attacker root $TMPDIR/trusted-exec-x9x964i1/attacker; attacker content; local-include: hostile git: attacker hook ran'; green: the compliant stub passed
worker_root (TrustedExecContractTest::test_worker_root_probe): red: 'worker root: read $TMPDIR/trusted-exec-zeiru6pm/root/.claude/worktrees/probe-seat/ledger.tsv; wrote $TMPDIR/trusted-exec-zeiru6pm/root/.claude/worktrees/probe-seat/out.txt; created $TMPDIR/trusted-exec-zeiru6pm/root/.claude/worktrees/probe-seat/new/out.txt'; green: the compliant stub passed
swapped_file (TrustedExecContractTest::test_swapped_file_probe): red: 'attacker content consumed'; green: the compliant stub passed
sanitized_environment (TrustedExecContractTest::test_sanitized_environment_probe): red: "environment: undeclared: [124 inherited names elided; 'LEAK' among them: True]"; green: the compliant stub passed
trusted_parent (TrustedExecContractTest::test_trusted_parent_probe): red: "environment: undeclared: [120 inherited names elided; 'LEAK' among them: False]; PATH is <the inherited value, elided>, not '/usr/bin:/bin'"; green: the compliant stub passed
[exit 0]
````

The hostile-Git line shows the three attacks run separately: the environment, a local `core.worktree` and a local `include.path`. The swapped-file case-alias subcase, measured on this filesystem:

````console
$ HOME="$(/usr/bin/mktemp -d "$TMPDIR/tec-home.XXXXXX")" "$PY" -B -c "import sys; sys.path.insert(0, \"tests/unit\"); import trusted_exec_contract as t
with t.swapped_file() as p: print(\"alias:\", None if p.alias is None else p.alias.name, \"reason:\", repr(p.alias_reason))"; HOME="$(/usr/bin/mktemp -d "$TMPDIR/tec-home.XXXXXX")" "$PY" -B -m unittest discover -s tests/unit -p test_trusted_exec_contract.py -k test_swapped_file_probe -v 2>&1 | tail -4
alias: cHECKED.TSV reason: ''
----------------------------------------------------------------------
Ran 1 test in 0.003s

OK
[exit 0]
````

## 7. Each claimed check against a wrong implementation

Each block checks `f4eed1cc` out into a scratch worktree, replaces one line of `tests/unit/trusted_exec_contract.py` with a plausible wrong implementation (asserted to apply exactly once) and runs the module. The worker review's surviving mutants come first (its M33, M04, M05, M14, M15, M16, M18 and M25), then one no-op per probe assertion. Each must turn a test red.

````console
$ git worktree add --detach -q "$SCRATCH/tec-mut" "$H" && "$PY" -I -c 'import sys; p, o, n = sys.argv[1:4]; s = open(p).read(); assert s.count(o) == 1, o; open(p, "w").write(s.replace(o, n)); print("mutated:", o.strip(), "->", n.strip())' "$SCRATCH/tec-mut/tests/unit/trusted_exec_contract.py" 'if content != LEGIT:' 'if False:' && (cd "$SCRATCH/tec-mut" && HOME="$(/usr/bin/mktemp -d "$TMPDIR/tec-home.XXXXXX")" uv run --no-project --offline --python "$PY" python -B -m unittest discover -s tests/unit -p test_trusted_exec_contract.py) > "$SCRATCH/tec-mut.out" 2>&1; rc=$?; echo "M33 the content check a no-op: unittest exit status: ${rc}"; < "$SCRATCH/tec-mut.out" /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED" | sed "s/ (test_trusted_exec_contract[^)]*)//" | sort | uniq -c; git worktree remove --force "$SCRATCH/tec-mut"
mutated: if content != LEGIT: -> if False:
M33 the content check a no-op: unittest exit status: 1
   1 FAIL: test_each_probe_detects_condition [hostile_git]
   1 FAIL: test_hostile_git_probe
   1 FAILED (failures=2)
   1 Ran 9 tests in 7.680s
[exit 0]
````

````console
$ git worktree add --detach -q "$SCRATCH/tec-mut" "$H" && "$PY" -I -c 'import sys; p, o, n = sys.argv[1:4]; s = open(p).read(); assert s.count(o) == 1, o; open(p, "w").write(s.replace(o, n)); print("mutated:", o.strip(), "->", n.strip())' "$SCRATCH/tec-mut/tests/unit/trusted_exec_contract.py" 'values = (git_dir, self.attacker, self.config, self.config, self.legit, git_dir / "objects")' 'values = (git_dir, self.attacker, "/dev/null", "/dev/null", self.legit, git_dir / "objects")' && (cd "$SCRATCH/tec-mut" && HOME="$(/usr/bin/mktemp -d "$TMPDIR/tec-home.XXXXXX")" uv run --no-project --offline --python "$PY" python -B -m unittest discover -s tests/unit -p test_trusted_exec_contract.py) > "$SCRATCH/tec-mut.out" 2>&1; rc=$?; echo "M04 the hostile config inert: unittest exit status: ${rc}"; < "$SCRATCH/tec-mut.out" /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED" | sed "s/ (test_trusted_exec_contract[^)]*)//" | sort | uniq -c; git worktree remove --force "$SCRATCH/tec-mut"
mutated: values = (git_dir, self.attacker, self.config, self.config, self.legit, git_dir / "objects") -> values = (git_dir, self.attacker, "/dev/null", "/dev/null", self.legit, git_dir / "objects")
M04 the hostile config inert: unittest exit status: 1
   1 FAIL: test_each_probe_detects_condition [hostile_git]
   1 FAIL: test_hostile_git_probe
   1 FAILED (failures=2)
   1 Ran 9 tests in 5.318s
[exit 0]
````

````console
$ git worktree add --detach -q "$SCRATCH/tec-mut" "$H" && "$PY" -I -c 'import sys; p, o, n = sys.argv[1:4]; s = open(p).read(); assert s.count(o) == 1, o; open(p, "w").write(s.replace(o, n)); print("mutated:", o.strip(), "->", n.strip())' "$SCRATCH/tec-mut/tests/unit/trusted_exec_contract.py" 'values = (git_dir, self.attacker, self.config, self.config, self.legit, git_dir / "objects")' 'values = (git_dir, self.attacker, self.config, self.config, "/nonexistent", "/nonexistent")' && (cd "$SCRATCH/tec-mut" && HOME="$(/usr/bin/mktemp -d "$TMPDIR/tec-home.XXXXXX")" uv run --no-project --offline --python "$PY" python -B -m unittest discover -s tests/unit -p test_trusted_exec_contract.py) > "$SCRATCH/tec-mut.out" 2>&1; rc=$?; echo "M05 the ceiling and alternates inert: unittest exit status: ${rc}"; < "$SCRATCH/tec-mut.out" /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED" | sed "s/ (test_trusted_exec_contract[^)]*)//" | sort | uniq -c; git worktree remove --force "$SCRATCH/tec-mut"
mutated: values = (git_dir, self.attacker, self.config, self.config, self.legit, git_dir / "objects") -> values = (git_dir, self.attacker, self.config, self.config, "/nonexistent", "/nonexistent")
M05 the ceiling and alternates inert: unittest exit status: 1
   1 FAIL: test_hostile_git_probe
   1 FAILED (failures=1)
   1 Ran 9 tests in 7.142s
[exit 0]
````

````console
$ git worktree add --detach -q "$SCRATCH/tec-mut" "$H" && "$PY" -I -c 'import sys; p, o, n = sys.argv[1:4]; s = open(p).read(); assert s.count(o) == 1, o; open(p, "w").write(s.replace(o, n)); print("mutated:", o.strip(), "->", n.strip())' "$SCRATCH/tec-mut/tests/unit/trusted_exec_contract.py" 'argv = ["/usr/bin/env", "-i", f"PATH={SAFE_PATH}"' 'argv = ["/usr/bin/env", f"PATH={SAFE_PATH}"' && (cd "$SCRATCH/tec-mut" && HOME="$(/usr/bin/mktemp -d "$TMPDIR/tec-home.XXXXXX")" uv run --no-project --offline --python "$PY" python -B -m unittest discover -s tests/unit -p test_trusted_exec_contract.py) > "$SCRATCH/tec-mut.out" 2>&1; rc=$?; echo "M14 no env -i: unittest exit status: ${rc}"; < "$SCRATCH/tec-mut.out" /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED" | sed "s/ (test_trusted_exec_contract[^)]*)//" | sort | uniq -c; git worktree remove --force "$SCRATCH/tec-mut"
mutated: argv = ["/usr/bin/env", "-i", f"PATH={SAFE_PATH}" -> argv = ["/usr/bin/env", f"PATH={SAFE_PATH}"
M14 no env -i: unittest exit status: 1
   1 FAIL: test_each_probe_detects_condition [trusted_parent]
   1 FAIL: test_trusted_parent_probe
   1 FAILED (failures=2)
   1 Ran 9 tests in 6.246s
[exit 0]
````

````console
$ git worktree add --detach -q "$SCRATCH/tec-mut" "$H" && "$PY" -I -c 'import sys; p, o, n = sys.argv[1:4]; s = open(p).read(); assert s.count(o) == 1, o; open(p, "w").write(s.replace(o, n)); print("mutated:", o.strip(), "->", n.strip())' "$SCRATCH/tec-mut/tests/unit/trusted_exec_contract.py" 'argv += ["/bin/bash", "--noprofile", "--norc", "-p", str(real)' 'argv += ["/bin/bash", str(real)' && (cd "$SCRATCH/tec-mut" && HOME="$(/usr/bin/mktemp -d "$TMPDIR/tec-home.XXXXXX")" uv run --no-project --offline --python "$PY" python -B -m unittest discover -s tests/unit -p test_trusted_exec_contract.py) > "$SCRATCH/tec-mut.out" 2>&1; rc=$?; echo "M15 bash with startup files and without -p: unittest exit status: ${rc}"; < "$SCRATCH/tec-mut.out" /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED" | sed "s/ (test_trusted_exec_contract[^)]*)//" | sort | uniq -c; git worktree remove --force "$SCRATCH/tec-mut"
mutated: argv += ["/bin/bash", "--noprofile", "--norc", "-p", str(real) -> argv += ["/bin/bash", str(real)
M15 bash with startup files and without -p: unittest exit status: 1
   1 FAIL: test_each_probe_detects_condition [trusted_parent]
   1 FAIL: test_trusted_parent_probe
   1 FAILED (failures=2)
   1 Ran 9 tests in 5.788s
[exit 0]
````

````console
$ git worktree add --detach -q "$SCRATCH/tec-mut" "$H" && "$PY" -I -c 'import sys; p, o, n = sys.argv[1:4]; s = open(p).read(); assert s.count(o) == 1, o; open(p, "w").write(s.replace(o, n)); print("mutated:", o.strip(), "->", n.strip())' "$SCRATCH/tec-mut/tests/unit/trusted_exec_contract.py" 'return subprocess.run(argv, env={}, capture_output=True' 'return subprocess.run(argv, env=dict(os.environ), capture_output=True' && (cd "$SCRATCH/tec-mut" && HOME="$(/usr/bin/mktemp -d "$TMPDIR/tec-home.XXXXXX")" uv run --no-project --offline --python "$PY" python -B -m unittest discover -s tests/unit -p test_trusted_exec_contract.py) > "$SCRATCH/tec-mut.out" 2>&1; rc=$?; echo "M16 the inherited environment: unittest exit status: ${rc}"; < "$SCRATCH/tec-mut.out" /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED" | sed "s/ (test_trusted_exec_contract[^)]*)//" | sort | uniq -c; git worktree remove --force "$SCRATCH/tec-mut"
Traceback (most recent call last):
  File "<string>", line 1, in <module>
    import sys; p, o, n = sys.argv[1:4]; s = open(p).read(); assert s.count(o) == 1, o; open(p, "w").write(s.replace(o, n)); print("mutated:", o.strip(), "->", n.strip())
                                                                    ^^^^^^^^^^^^^^^
AssertionError: return subprocess.run(argv, env={}, capture_output=True
M16 the inherited environment: unittest exit status: 1
   1 FAIL: test_each_probe_detects_condition [trusted_parent]
   1 FAIL: test_trusted_parent_probe
   1 FAILED (failures=2)
   1 Ran 9 tests in 5.788s
[exit 0]
````

````console
$ git worktree add --detach -q "$SCRATCH/tec-mut" "$H" && "$PY" -I -c 'import sys; p, o, n = sys.argv[1:4]; s = open(p).read(); assert s.count(o) == 1, o; open(p, "w").write(s.replace(o, n)); print("mutated:", o.strip(), "->", n.strip())' "$SCRATCH/tec-mut/tests/unit/trusted_exec_contract.py" 'if not Path(script).is_absolute():' 'if False:' && (cd "$SCRATCH/tec-mut" && HOME="$(/usr/bin/mktemp -d "$TMPDIR/tec-home.XXXXXX")" uv run --no-project --offline --python "$PY" python -B -m unittest discover -s tests/unit -p test_trusted_exec_contract.py) > "$SCRATCH/tec-mut.out" 2>&1; rc=$?; echo "M18 no relative-path refusal: unittest exit status: ${rc}"; < "$SCRATCH/tec-mut.out" /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED" | sed "s/ (test_trusted_exec_contract[^)]*)//" | sort | uniq -c; git worktree remove --force "$SCRATCH/tec-mut"
mutated: if not Path(script).is_absolute(): -> if False:
M18 no relative-path refusal: unittest exit status: 1
   1 FAIL: test_trusted_parent_probe [relative]
   1 FAILED (failures=1)
   1 Ran 9 tests in 5.477s
[exit 0]
````

````console
$ git worktree add --detach -q "$SCRATCH/tec-mut" "$H" && "$PY" -I -c 'import sys; p, o, n = sys.argv[1:4]; s = open(p).read(); assert s.count(o) == 1, o; open(p, "w").write(s.replace(o, n)); print("mutated:", o.strip(), "->", n.strip())' "$SCRATCH/tec-mut/tests/unit/trusted_exec_contract.py" 'return Path(__file__).resolve().parents[2]' 'return Path(subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip())' && (cd "$SCRATCH/tec-mut" && HOME="$(/usr/bin/mktemp -d "$TMPDIR/tec-home.XXXXXX")" uv run --no-project --offline --python "$PY" python -B -m unittest discover -s tests/unit -p test_trusted_exec_contract.py) > "$SCRATCH/tec-mut.out" 2>&1; rc=$?; echo "M25 the root from git and GIT_*: unittest exit status: ${rc}"; < "$SCRATCH/tec-mut.out" /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED" | sed "s/ (test_trusted_exec_contract[^)]*)//" | sort | uniq -c; git worktree remove --force "$SCRATCH/tec-mut"
mutated: return Path(__file__).resolve().parents[2] -> return Path(subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip())
M25 the root from git and GIT_*: unittest exit status: 1
   1 FAIL: test_trusted_parent_probe
   1 FAILED (failures=1)
   1 Ran 9 tests in 7.371s
[exit 0]
````

````console
$ git worktree add --detach -q "$SCRATCH/tec-mut" "$H" && "$PY" -I -c 'import sys; p, o, n = sys.argv[1:4]; s = open(p).read(); assert s.count(o) == 1, o; open(p, "w").write(s.replace(o, n)); print("mutated:", o.strip(), "->", n.strip())' "$SCRATCH/tec-mut/tests/unit/trusted_exec_contract.py" 'found += [f"read {path}"] if path == self.input and st.st_atime_ns else []' 'found += []' && (cd "$SCRATCH/tec-mut" && HOME="$(/usr/bin/mktemp -d "$TMPDIR/tec-home.XXXXXX")" uv run --no-project --offline --python "$PY" python -B -m unittest discover -s tests/unit -p test_trusted_exec_contract.py) > "$SCRATCH/tec-mut.out" 2>&1; rc=$?; echo "worker-root read detection a no-op: unittest exit status: ${rc}"; < "$SCRATCH/tec-mut.out" /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED" | sed "s/ (test_trusted_exec_contract[^)]*)//" | sort | uniq -c; git worktree remove --force "$SCRATCH/tec-mut"
mutated: found += [f"read {path}"] if path == self.input and st.st_atime_ns else [] -> found += []
worker-root read detection a no-op: unittest exit status: 1
   1 FAIL: test_each_probe_detects_condition [worker_root]
   1 FAIL: test_worker_root_probe
   1 FAILED (failures=2)
   1 Ran 9 tests in 7.105s
[exit 0]
````

````console
$ git worktree add --detach -q "$SCRATCH/tec-mut" "$H" && "$PY" -I -c 'import sys; p, o, n = sys.argv[1:4]; s = open(p).read(); assert s.count(o) == 1, o; open(p, "w").write(s.replace(o, n)); print("mutated:", o.strip(), "->", n.strip())' "$SCRATCH/tec-mut/tests/unit/trusted_exec_contract.py" 'found += [f"wrote {path}"] if self._identity(st) != before else []' 'found += []' && (cd "$SCRATCH/tec-mut" && HOME="$(/usr/bin/mktemp -d "$TMPDIR/tec-home.XXXXXX")" uv run --no-project --offline --python "$PY" python -B -m unittest discover -s tests/unit -p test_trusted_exec_contract.py) > "$SCRATCH/tec-mut.out" 2>&1; rc=$?; echo "worker-root write detection a no-op: unittest exit status: ${rc}"; < "$SCRATCH/tec-mut.out" /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED" | sed "s/ (test_trusted_exec_contract[^)]*)//" | sort | uniq -c; git worktree remove --force "$SCRATCH/tec-mut"
mutated: found += [f"wrote {path}"] if self._identity(st) != before else [] -> found += []
worker-root write detection a no-op: unittest exit status: 1
   1 FAIL: test_each_probe_detects_condition [worker_root]
   1 FAIL: test_worker_root_probe
   1 FAILED (failures=2)
   1 Ran 9 tests in 6.393s
[exit 0]
````

````console
$ git worktree add --detach -q "$SCRATCH/tec-mut" "$H" && "$PY" -I -c 'import sys; p, o, n = sys.argv[1:4]; s = open(p).read(); assert s.count(o) == 1, o; open(p, "w").write(s.replace(o, n)); print("mutated:", o.strip(), "->", n.strip())' "$SCRATCH/tec-mut/tests/unit/trusted_exec_contract.py" 'if runs := self.records():' 'if runs := []:' && (cd "$SCRATCH/tec-mut" && HOME="$(/usr/bin/mktemp -d "$TMPDIR/tec-home.XXXXXX")" uv run --no-project --offline --python "$PY" python -B -m unittest discover -s tests/unit -p test_trusted_exec_contract.py) > "$SCRATCH/tec-mut.out" 2>&1; rc=$?; echo "shim assertion a no-op: unittest exit status: ${rc}"; < "$SCRATCH/tec-mut.out" /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED" | sed "s/ (test_trusted_exec_contract[^)]*)//" | sort | uniq -c; git worktree remove --force "$SCRATCH/tec-mut"
mutated: if runs := self.records(): -> if runs := []:
shim assertion a no-op: unittest exit status: 1
   1 FAIL: test_each_probe_detects_condition [shim_on_path]
   1 FAIL: test_shim_probe
   1 FAILED (failures=2)
   1 Ran 9 tests in 4.011s
[exit 0]
````

````console
$ git worktree add --detach -q "$SCRATCH/tec-mut" "$H" && "$PY" -I -c 'import sys; p, o, n = sys.argv[1:4]; s = open(p).read(); assert s.count(o) == 1, o; open(p, "w").write(s.replace(o, n)); print("mutated:", o.strip(), "->", n.strip())' "$SCRATCH/tec-mut/tests/unit/trusted_exec_contract.py" 'os.replace(self.base / ".swap", target)' 'os.unlink(self.base / ".swap")' && (cd "$SCRATCH/tec-mut" && HOME="$(/usr/bin/mktemp -d "$TMPDIR/tec-home.XXXXXX")" uv run --no-project --offline --python "$PY" python -B -m unittest discover -s tests/unit -p test_trusted_exec_contract.py) > "$SCRATCH/tec-mut.out" 2>&1; rc=$?; echo "swap barrier a no-op: unittest exit status: ${rc}"; < "$SCRATCH/tec-mut.out" /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED" | sed "s/ (test_trusted_exec_contract[^)]*)//" | sort | uniq -c; git worktree remove --force "$SCRATCH/tec-mut"
mutated: os.replace(self.base / ".swap", target) -> os.unlink(self.base / ".swap")
swap barrier a no-op: unittest exit status: 1
   1 FAIL: test_each_probe_detects_condition [swapped_file]
   1 FAIL: test_swapped_file_probe
   1 FAILED (failures=2)
   1 Ran 9 tests in 6.689s
[exit 0]
````

## 8. Lint, formatting and caps

````console
$ ruff format --config ruff.toml --check tests/unit/trusted_exec_contract.py tests/unit/test_trusted_exec_contract.py; ruff check --config ruff.toml tests/unit/trusted_exec_contract.py tests/unit/test_trusted_exec_contract.py
2 files already formatted
All checks passed!
[exit 0]
````

````console
$ make format > "$SCRATCH/tec-format.out" 2>&1; rc=$?; echo "make format exit status: ${rc}"; base="$(git merge-base origin/main HEAD)"; sed -n "s/^diff \([^ ]*\)\.orig .*/\1/p" "$SCRATCH/tec-format.out" > "$SCRATCH/tec-flagged.txt"; echo "files the whole-tree shfmt step flags: $(wc -l < "$SCRATCH/tec-flagged.txt" | tr -d " ")"; while read -r f; do git diff --quiet "$base" HEAD -- "$f" && echo "unchanged from ${base:0:8}: $f" || echo "CHANGED by this PR: $f"; done < "$SCRATCH/tec-flagged.txt"
make format exit status: 2
files the whole-tree shfmt step flags: 12
unchanged from ba318e53: .orchestration/tasks/dotfiles-T128-chain-github-scripts-a01-input/pr-cost.sh
unchanged from ba318e53: .orchestration/tasks/dotfiles-T128-chain-github-scripts-a01-input/resolve-threads.sh
unchanged from ba318e53: .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/local-advisory.sh
unchanged from ba318e53: .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/local-review.sh
unchanged from ba318e53: .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/sandbox-scan.sh
unchanged from ba318e53: .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/boundary.sh
unchanged from ba318e53: .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/ff-main.sh
unchanged from ba318e53: .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/orch-audit.sh
unchanged from ba318e53: .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/orch-gate.sh
unchanged from ba318e53: .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/t717-prep.sh
unchanged from ba318e53: home/dot_claude/hooks/executable_project-map-reload.sh
unchanged from ba318e53: tests/install/macos/common/brew.bats
[exit 0]
````

````console
$ git diff --numstat origin/main...HEAD; git diff --numstat origin/main...HEAD -- tests/unit/trusted_exec_contract.py tests/unit/test_trusted_exec_contract.py | awk '{ printf "%s: %d added + %d deleted = %d changed lines (cap %d)\n", $3, $1, $2, $1 + $2, ($3 ~ /test_trusted/ ? 350 : 250) }'; wc -l tests/unit/trusted_exec_contract.py tests/unit/test_trusted_exec_contract.py .orchestration/$T/task.md
199	0	.orchestration/dotfiles-T133-trusted-exec-contract-tests-a01/task.md
324	0	tests/unit/test_trusted_exec_contract.py
242	0	tests/unit/trusted_exec_contract.py
tests/unit/test_trusted_exec_contract.py: 324 added + 0 deleted = 324 changed lines (cap 350)
tests/unit/trusted_exec_contract.py: 242 added + 0 deleted = 242 changed lines (cap 250)
     242 tests/unit/trusted_exec_contract.py
     324 tests/unit/test_trusted_exec_contract.py
     198 .orchestration/dotfiles-T133-trusted-exec-contract-tests-a01/task.md
     764 total
[exit 0]
````

This record is part of the final head, so the RESULT carries `git diff --name-only f4eed1cc <final head>`, which lists only `.orchestration/dotfiles-T133-trusted-exec-contract-tests-a01/` paths.

## 9. The review gate

The gate reads the worker receipt and its crit-data JSON. An earlier receipt form, with a description inside `reviewer:`, failed with "AGENT_REVIEWED=1 requires an agent reviewer". The field now names only `claude`, with the description on `reviewer_detail:`.

````console
$ make require-crit-review AGENT_REVIEWED=1 REVIEW_EVIDENCE=.orchestration/dotfiles-T133-trusted-exec-contract-tests-a01/dotfiles-T133-trusted-exec-contract-tests-a01-worker-review-receipt.md
Review requirement satisfied by AGENT_REVIEWED=1 with REVIEW_EVIDENCE.
[exit 0]
````
