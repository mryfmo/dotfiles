---
task_id: dotfiles-T133-trusted-exec-contract-tests-a01
seat: claude-standard-dot-a011
code_head: 7d3ecd4f
---

# Validation: dotfiles-T133-trusted-exec-contract-tests-a01

Every command below ran inside the sandbox from `.claude/worktrees/worker-d` on the branch `tools/trusted-exec-contract-tests-a01`, created with `--no-track` from `origin/main` `ba318e53` and update-branched by the orchestrator to `9545e59f`.

The tested code head is `7d3ecd4f`. Its commits: the task copy (`e603ac51`), the tests written first (`755d9002`, red), the helper (`4729b83c`), the worker review's fix round (`f4eed1cc`), then revise 1's tests (`bb539aa7`, red), fix (`65c81c98`), the non-absolute home case (`eda9b5ee`) and the fixes from its worker review (`7d3ecd4f`).

The final head adds only records under `.orchestration/dotfiles-T133-trusted-exec-contract-tests-a01/`, so the RESULT carries its diff and CI.

Names used below:

- `MAIN`: the main checkout. `SCRATCH`: the seat's scratchpad.
- The commands are recorded literally: the 3.15 and 3.10 interpreters by their `~/` paths, the red test commits `755d9002` and `bb539aa7`, and the code head `7d3ecd4f` the mutants check out. Amendment 1's records round replaced the generator's `$UT`, `$PY`, `$PY310`, `$H`, `$RED`, `$RED2` and `$T` with these values; the outputs are unchanged.
- `PREV`: the audited head of revise 1, `9545e59f`.
- `$HOME_OF_THE_SEAT`: the seat's home directory, which appears only in interpreter paths and in the live passwd lookup of section 6.

Each block ends with the exit status of the command shown.

The repository's mask (`scripts/validate-agent-assets.py --mask-secrets`) rewrites every home-shaped path, fake ones included. Four fake fixture homes from the passwd test table therefore appear as `~` in the pasted test output of sections 4 and 7.

## 1. Task copy

````console
$ shasum -a 256 "$MAIN/.orchestration/tasks/dotfiles-T133-trusted-exec-contract-tests-a01.md" ".orchestration/dotfiles-T133-trusted-exec-contract-tests-a01/task.md"; cmp "$MAIN/.orchestration/tasks/dotfiles-T133-trusted-exec-contract-tests-a01.md" ".orchestration/dotfiles-T133-trusted-exec-contract-tests-a01/task.md" && echo byte-identical
dd7549118bd470af98f52096ee668165a53727981eba4cb8466550641e2dc12c  $MAIN/.orchestration/tasks/dotfiles-T133-trusted-exec-contract-tests-a01.md
dd7549118bd470af98f52096ee668165a53727981eba4cb8466550641e2dc12c  .orchestration/dotfiles-T133-trusted-exec-contract-tests-a01/task.md
byte-identical
[exit 0]
````

````console
$ uv run --offline --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py --root "$PWD" "$MAIN/.orchestration/tasks/dotfiles-T133-trusted-exec-contract-tests-a01.md"
dotfiles-T133-trusted-exec-contract-tests-a01.md: OK
[exit 0]
````

## 2. Premises, re-run at worker start, and the observed interpreters

````console
$ python3 --version; uname -s; python3 -c 'import shutil; print("dscl=" + str(shutil.which("dscl"))); print("getent=" + str(shutil.which("getent")))'; git ls-tree --name-only origin/main -- tests/unit/trusted_exec_contract.py; echo "ls-tree exit $?"; git merge-base --is-ancestor ba318e53 origin/main && echo "ba318e53 is on origin/main"; ~/.local/share/mise/installs/python/3.15.0/bin/python3.15 -c "import platform; print(platform.python_version())"; ~/.local/share/uv/python/cpython-3.10-macos-aarch64-none/bin/python3.10 -c "import platform; print(platform.python_version())"
Python 3.15.0
Darwin
dscl=/usr/bin/dscl
getent=None
ls-tree exit 0
ba318e53 is on origin/main
3.15.0
3.10.22
[exit 0]
````

The interpreter uv picks without `--python` depends on HOME: the seat's own HOME gives 3.10, a temporary HOME gives 3.15. Every suite run below therefore names its interpreter by absolute path.

````console
$ uv run --no-project --offline python -c "import platform; print(platform.python_version())"; HOME="$(/usr/bin/mktemp -d "$TMPDIR/tec-home.XXXXXX")" uv run --no-project --offline python -c "import platform; print(platform.python_version())"
3.10.22
3.15.0
[exit 0]
````

## 3. Branch and provenance

````console
$ git log --oneline origin/main..HEAD; git diff --name-status origin/main...7d3ecd4f
7d3ecd4f fix(unit): the worker-root probe reads content only from the same regular file and is checked twice; passwd subtests name their outcome (T133 trusted-exec-contract-tests a01, revise 1, worker review P3)
eda9b5ee test(unit): the passwd lookup refuses a non-absolute home from the passwd entry (T133 trusted-exec-contract-tests a01, revise 1)
65c81c98 fix(unit): the worker-root probe compares content from a fixed past mtime; passwd_home reads getpwuid and treats dscl or getent as an optional cross-check (T133 trusted-exec-contract-tests a01, revise 1)
bb539aa7 test(unit): a same-length worker-root overwrite and a passwd home from getpwuid with dscl or getent as an optional cross-check (T133 trusted-exec-contract-tests a01, revise 1, red)
9545e59f Merge branch 'main' into tools/trusted-exec-contract-tests-a01
25dd01e5 docs(orchestration): T133 trusted-exec-contract-tests a01 evidence, the worker review and the review gate
f4eed1cc test(unit): the trusted-exec probes after the worker review: whole red reasons, each hostile GIT_* name shown live, the runner argv and env observed, refusal reasons named, a worker-root probe by access time with no FIFO (T133 trusted-exec-contract-tests a01)
4729b83c test(unit): trusted_exec_contract.py, the shared probes of design 5.14 item 7 and the trusted-parent runner (T133 trusted-exec-contract-tests a01)
755d9002 test(unit): the trusted-exec contract probes, each red on a noncompliant consumer stub and green on a compliant one (T133 trusted-exec-contract-tests a01, design 5.14 item 7, red)
e603ac51 docs(orchestration): T133 trusted-exec-contract-tests a01 task copy
A	.orchestration/dotfiles-T133-trusted-exec-contract-tests-a01/autoskill.md
A	.orchestration/dotfiles-T133-trusted-exec-contract-tests-a01/dotfiles-T133-trusted-exec-contract-tests-a01-worker-crit.json
A	.orchestration/dotfiles-T133-trusted-exec-contract-tests-a01/dotfiles-T133-trusted-exec-contract-tests-a01-worker-review-receipt.md
A	.orchestration/dotfiles-T133-trusted-exec-contract-tests-a01/learning.md
A	.orchestration/dotfiles-T133-trusted-exec-contract-tests-a01/report.md
A	.orchestration/dotfiles-T133-trusted-exec-contract-tests-a01/result.txt
A	.orchestration/dotfiles-T133-trusted-exec-contract-tests-a01/sandbox.md
A	.orchestration/dotfiles-T133-trusted-exec-contract-tests-a01/task.md
A	.orchestration/dotfiles-T133-trusted-exec-contract-tests-a01/validation.md
A	tests/unit/test_trusted_exec_contract.py
A	tests/unit/trusted_exec_contract.py
[exit 0]
````

## 4. Red before each change

At the first test commit the helper did not exist. At the revise's test commit `bb539aa7` (on the audited head `9545e59f`), the two new tests run against the old helper: the same-length overwrite goes unseen, and the passwd lookup fails when dscl cannot run, accepts a disagreeing directory answer, or refuses a platform without one.

````console
$ git worktree add --detach -q "$SCRATCH/tec-red" 755d9002 && (cd "$SCRATCH/tec-red" && uv run --no-project --offline --python ~/.local/share/mise/installs/python/3.15.0/bin/python3.15 python -B -m unittest discover -s tests/unit -p test_trusted_exec_contract.py) > "$SCRATCH/tec-red.out" 2>&1; echo "unittest exit status: $?"; /usr/bin/grep -E "Error|^Ran|^FAILED" "$SCRATCH/tec-red.out"; git worktree remove --force "$SCRATCH/tec-red"
unittest exit status: 1
ImportError: Failed to import test module: test_trusted_exec_contract
ModuleNotFoundError: No module named 'trusted_exec_contract'. Did you mean: 'test_trusted_exec_contract'?
Ran 1 test in 0.000s
FAILED (errors=1)
[exit 0]
````

````console
$ git worktree add --detach -q "$SCRATCH/tec-red" bb539aa7 && (cd "$SCRATCH/tec-red" && HOME="$(/usr/bin/mktemp -d "$TMPDIR/tec-home.XXXXXX")" uv run --no-project --offline --python ~/.local/share/mise/installs/python/3.15.0/bin/python3.15 python -B -m unittest discover -s tests/unit -p test_trusted_exec_contract.py) > "$SCRATCH/tec-red.out" 2>&1; echo "unittest exit status: $?"; /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^FAILED" "$SCRATCH/tec-red.out" | sed "s/ (test_trusted_exec_contract[^)]*)//" | cut -c1-170; git worktree remove --force "$SCRATCH/tec-red"
unittest exit status: 1
ERROR: test_passwd_home_uses_getpwuid_and_treats_dscl_or_getent_as_an_optional_cross_check [darwin CalledProcessError(70, ['/usr/bin/dscl', '.', '-read', '~', 
ERROR: test_passwd_home_uses_getpwuid_and_treats_dscl_or_getent_as_an_optional_cross_check [linux OSError('no getent')]
ERROR: test_passwd_home_uses_getpwuid_and_treats_dscl_or_getent_as_an_optional_cross_check [win32 None]
FAIL: test_passwd_home_uses_getpwuid_and_treats_dscl_or_getent_as_an_optional_cross_check [darwin 'NFSHomeDirectory: ~\n']
FAIL: test_passwd_home_uses_getpwuid_and_treats_dscl_or_getent_as_an_optional_cross_check [darwin 'No such key: NFSHomeDirectory\n']
FAIL: test_passwd_home_uses_getpwuid_and_treats_dscl_or_getent_as_an_optional_cross_check [linux 'a:b\n']
FAIL: test_worker_root_probe_detects_a_same_length_overwrite [input]
FAIL: test_worker_root_probe_detects_a_same_length_overwrite [output]
Ran 10 tests in 3.442s
FAILED (failures=5, errors=3)
[exit 0]
````

## 5. The Check, with a temporary HOME and UV_CACHE_DIR, on Python 3.15 and 3.10

Fixture directories (`trusted-exec-*`) under `$TMPDIR` are counted before and after, the temporary HOME is listed after, and this repository's Git configuration is hashed before and after.

````console
$ git rev-parse HEAD; export TEC_HOME="$(/usr/bin/mktemp -d "$TMPDIR/tec-home.XXXXXX")" TEC_UVC="$(/usr/bin/mktemp -d "$TMPDIR/tec-uvcache.XXXXXX")"; echo "HOME=$TEC_HOME UV_CACHE_DIR=$TEC_UVC"; fixtures() { find "$TMPDIR" -maxdepth 1 -name "trusted-exec-*" | wc -l | tr -d " "; }; gitcfg() { git config --list --show-origin | shasum -a 256 | cut -c1-16; }; echo "fixture dirs before: $(fixtures); git config before: $(gitcfg)"; HOME="$TEC_HOME" UV_CACHE_DIR="$TEC_UVC" uv run --no-project --offline --python ~/.local/share/mise/installs/python/3.15.0/bin/python3.15 python -B -m unittest discover -s tests/unit -p test_trusted_exec_contract.py -v; rc=$?; echo "unittest exit status: ${rc}"; echo "fixture dirs after: $(fixtures); git config after: $(gitcfg)"; echo "temporary HOME after the run:"; find "$TEC_HOME" -mindepth 1 | head; echo "(end of listing)"
7d3ecd4f417ece5038d3218e006e5bfe24070c61
HOME=$TMPDIR/tec-home.ld0qAK UV_CACHE_DIR=$TMPDIR/tec-uvcache.dIYg54
fixture dirs before: 0; git config before: 3e9c9ddbc66eac10
test_each_probe_detects_condition (test_trusted_exec_contract.TrustedExecContractTest.test_each_probe_detects_condition) ... ok
test_hostile_git_probe (test_trusted_exec_contract.TrustedExecContractTest.test_hostile_git_probe) ... ok
test_passwd_home_uses_getpwuid_and_treats_dscl_or_getent_as_an_optional_cross_check (test_trusted_exec_contract.TrustedExecContractTest.test_passwd_home_uses_getpwuid_and_treats_dscl_or_getent_as_an_optional_cross_check) ... ok
test_probes_clean_up_after_an_exception (test_trusted_exec_contract.TrustedExecContractTest.test_probes_clean_up_after_an_exception) ... ok
test_sanitized_environment_probe (test_trusted_exec_contract.TrustedExecContractTest.test_sanitized_environment_probe) ... ok
test_shim_probe (test_trusted_exec_contract.TrustedExecContractTest.test_shim_probe) ... ok
test_swapped_file_probe (test_trusted_exec_contract.TrustedExecContractTest.test_swapped_file_probe) ... ok
test_trusted_parent_probe (test_trusted_exec_contract.TrustedExecContractTest.test_trusted_parent_probe) ... ok
test_worker_root_probe (test_trusted_exec_contract.TrustedExecContractTest.test_worker_root_probe) ... ok
test_worker_root_probe_detects_a_same_length_overwrite (test_trusted_exec_contract.TrustedExecContractTest.test_worker_root_probe_detects_a_same_length_overwrite) ... ok

----------------------------------------------------------------------
Ran 10 tests in 4.606s

OK
unittest exit status: 0
fixture dirs after: 0; git config after: 3e9c9ddbc66eac10
temporary HOME after the run:
(end of listing)
[exit 0]
````

````console
$ export TEC_HOME="$(/usr/bin/mktemp -d "$TMPDIR/tec-home.XXXXXX")" TEC_UVC="$(/usr/bin/mktemp -d "$TMPDIR/tec-uvcache.XXXXXX")"; HOME="$TEC_HOME" UV_CACHE_DIR="$TEC_UVC" uv run --no-project --offline --python ~/.local/share/uv/python/cpython-3.10-macos-aarch64-none/bin/python3.10 python -B -c "import sys; print(sys.version.split()[0])"; HOME="$TEC_HOME" UV_CACHE_DIR="$TEC_UVC" uv run --no-project --offline --python ~/.local/share/uv/python/cpython-3.10-macos-aarch64-none/bin/python3.10 python -B -m unittest discover -s tests/unit -p test_trusted_exec_contract.py 2>&1 | tail -3
3.10.22
Ran 10 tests in 4.665s

OK
[exit 0]
````

## 6. Each probe, red against a deliberately failing stub and green against a compliant one

The printer below runs the test module's `case_*` functions: the noncompliant stub must fail the probe assertion for the intended reason, then the compliant stub must pass. It elides the runner's inherited variable names and PATH value from the environment reasons.

````console
$ cat "$SCRATCH/tec-cases.py"; HOME="$(/usr/bin/mktemp -d "$TMPDIR/tec-home.XXXXXX")" ~/.local/share/mise/installs/python/3.15.0/bin/python3.15 -B "$SCRATCH/tec-cases.py"
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
shim_on_path (TrustedExecContractTest::test_shim_probe): red: "shim ran: git ['$TMPDIR/trusted-exec-5enton41/bin/git', 'status', 'a b', '']"; green: the compliant stub passed
hostile_git (TrustedExecContractTest::test_hostile_git_probe): red: 'environment: hostile git: attacker root $TMPDIR/trusted-exec-j1wvgh61/attacker; attacker content; attacker hook ran; local-worktree: hostile git: attacker root $TMPDIR/trusted-exec-j1wvgh61/attacker; attacker content; local-include: hostile git: attacker hook ran'; green: the compliant stub passed
worker_root (TrustedExecContractTest::test_worker_root_probe): red: 'worker root: read $TMPDIR/trusted-exec-e4kg2rng/root/.claude/worktrees/probe-seat/ledger.tsv; wrote $TMPDIR/trusted-exec-e4kg2rng/root/.claude/worktrees/probe-seat/out.txt; created $TMPDIR/trusted-exec-e4kg2rng/root/.claude/worktrees/probe-seat/new/out.txt'; green: the compliant stub passed
swapped_file (TrustedExecContractTest::test_swapped_file_probe): red: 'attacker content consumed'; green: the compliant stub passed
sanitized_environment (TrustedExecContractTest::test_sanitized_environment_probe): red: "environment: undeclared: [128 inherited names elided; 'LEAK' among them: True]"; green: the compliant stub passed
trusted_parent (TrustedExecContractTest::test_trusted_parent_probe): red: "environment: undeclared: [124 inherited names elided; 'LEAK' among them: False]; PATH is <the inherited value, elided>, not '/usr/bin:/bin'"; green: the compliant stub passed
[exit 0]
````

````console
$ HOME="$(/usr/bin/mktemp -d "$TMPDIR/tec-home.XXXXXX")" ~/.local/share/mise/installs/python/3.15.0/bin/python3.15 -B -c "import sys; sys.path.insert(0, \"tests/unit\"); import trusted_exec_contract as t
with t.swapped_file() as p: print(\"alias:\", None if p.alias is None else p.alias.name, \"reason:\", repr(p.alias_reason))"; HOME="$(/usr/bin/mktemp -d "$TMPDIR/tec-home.XXXXXX")" uv run --no-project --offline --python ~/.local/share/mise/installs/python/3.15.0/bin/python3.15 python -B -m unittest discover -s tests/unit -p test_trusted_exec_contract.py -k test_swapped_file_probe -v 2>&1 | tail -4
alias: cHECKED.TSV reason: ''
----------------------------------------------------------------------
Ran 1 test in 0.003s

OK
[exit 0]
````

Live, with no stub: `dscl` fails inside this sandbox, and `passwd_home()` still returns the passwd entry's home rather than `HOME` (a temporary one here).

````console
$ cat "$SCRATCH/tec-live-passwd.py"; HOME="$(/usr/bin/mktemp -d "$TMPDIR/tec-home.XXXXXX")" ~/.local/share/mise/installs/python/3.15.0/bin/python3.15 -I -B "$SCRATCH/tec-live-passwd.py"
"""Live: dscl on this seat, and what passwd_home() returns without any stub."""
import os, pwd, subprocess, sys

sys.path.insert(0, "tests/unit")
import trusted_exec_contract as t  # noqa: E402

name = pwd.getpwuid(os.getuid()).pw_name
try:
    t._directory_service(["/usr/bin/dscl", ".", "-read", "/Users/" + name, "NFSHomeDirectory"])
    print("dscl: ran")
except subprocess.CalledProcessError as error:
    print(f"dscl: exit {error.returncode}")
home = t.passwd_home()
print("passwd_home() == pwd.getpwuid(os.getuid()).pw_dir:", home == pwd.getpwuid(os.getuid()).pw_dir)
print("passwd_home() == $HOME:", home == os.environ.get("HOME"))
print("passwd_home():", home)
dscl: exit 70
passwd_home() == pwd.getpwuid(os.getuid()).pw_dir: True
passwd_home() == $HOME: False
passwd_home(): $HOME_OF_THE_SEAT
[exit 0]
````

## 7. Each claimed check against a wrong implementation

Each block truncates its output file, checks `7d3ecd4f` out into a scratch worktree, applies one replacement to `tests/unit/trusted_exec_contract.py` (asserted to match exactly once; the block shows `mutated:` only when it applied) and only then runs the module. The first eight are the worker review's survivors (M16 now anchored on the runner's `check=False` call, which the audit found matching twice); then a no-op per probe assertion and the revise's changes. Each must turn a test red.

````console
$ : > "$SCRATCH/tec-mut.out"; git worktree add --detach -q "$SCRATCH/tec-mut" 7d3ecd4f && ~/.local/share/mise/installs/python/3.15.0/bin/python3.15 -I -c 'import sys; p, o, n = sys.argv[1:4]; s = open(p).read(); assert s.count(o) == 1, (s.count(o), o); open(p, "w").write(s.replace(o, n)); print("mutated:", o.strip(), "->", n.strip())' "$SCRATCH/tec-mut/tests/unit/trusted_exec_contract.py" 'if content != LEGIT:' 'if False:' && { (cd "$SCRATCH/tec-mut" && HOME="$(/usr/bin/mktemp -d "$TMPDIR/tec-home.XXXXXX")" uv run --no-project --offline --python ~/.local/share/mise/installs/python/3.15.0/bin/python3.15 python -B -m unittest discover -s tests/unit -p test_trusted_exec_contract.py) > "$SCRATCH/tec-mut.out" 2>&1; echo "M33 the content check a no-op: unittest exit status: $?"; < "$SCRATCH/tec-mut.out" /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED" | sed "s/ (test_trusted_exec_contract[^)]*)//" | cut -c1-150 | sort | uniq -c; }; git worktree remove --force "$SCRATCH/tec-mut"
mutated: if content != LEGIT: -> if False:
M33 the content check a no-op: unittest exit status: 1
   1 FAIL: test_each_probe_detects_condition [hostile_git]
   1 FAIL: test_hostile_git_probe
   1 FAILED (failures=2)
   1 Ran 10 tests in 2.312s
[exit 0]
````

````console
$ : > "$SCRATCH/tec-mut.out"; git worktree add --detach -q "$SCRATCH/tec-mut" 7d3ecd4f && ~/.local/share/mise/installs/python/3.15.0/bin/python3.15 -I -c 'import sys; p, o, n = sys.argv[1:4]; s = open(p).read(); assert s.count(o) == 1, (s.count(o), o); open(p, "w").write(s.replace(o, n)); print("mutated:", o.strip(), "->", n.strip())' "$SCRATCH/tec-mut/tests/unit/trusted_exec_contract.py" 'values = (git_dir, self.attacker, self.config, self.config, self.legit, git_dir / "objects")' 'values = (git_dir, self.attacker, "/dev/null", "/dev/null", self.legit, git_dir / "objects")' && { (cd "$SCRATCH/tec-mut" && HOME="$(/usr/bin/mktemp -d "$TMPDIR/tec-home.XXXXXX")" uv run --no-project --offline --python ~/.local/share/mise/installs/python/3.15.0/bin/python3.15 python -B -m unittest discover -s tests/unit -p test_trusted_exec_contract.py) > "$SCRATCH/tec-mut.out" 2>&1; echo "M04 the hostile config inert: unittest exit status: $?"; < "$SCRATCH/tec-mut.out" /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED" | sed "s/ (test_trusted_exec_contract[^)]*)//" | cut -c1-150 | sort | uniq -c; }; git worktree remove --force "$SCRATCH/tec-mut"
mutated: values = (git_dir, self.attacker, self.config, self.config, self.legit, git_dir / "objects") -> values = (git_dir, self.attacker, "/dev/null", "/dev/null", self.legit, git_dir / "objects")
M04 the hostile config inert: unittest exit status: 1
   1 FAIL: test_each_probe_detects_condition [hostile_git]
   1 FAIL: test_hostile_git_probe
   1 FAILED (failures=2)
   1 Ran 10 tests in 1.873s
[exit 0]
````

````console
$ : > "$SCRATCH/tec-mut.out"; git worktree add --detach -q "$SCRATCH/tec-mut" 7d3ecd4f && ~/.local/share/mise/installs/python/3.15.0/bin/python3.15 -I -c 'import sys; p, o, n = sys.argv[1:4]; s = open(p).read(); assert s.count(o) == 1, (s.count(o), o); open(p, "w").write(s.replace(o, n)); print("mutated:", o.strip(), "->", n.strip())' "$SCRATCH/tec-mut/tests/unit/trusted_exec_contract.py" 'values = (git_dir, self.attacker, self.config, self.config, self.legit, git_dir / "objects")' 'values = (git_dir, self.attacker, self.config, self.config, "/nonexistent", "/nonexistent")' && { (cd "$SCRATCH/tec-mut" && HOME="$(/usr/bin/mktemp -d "$TMPDIR/tec-home.XXXXXX")" uv run --no-project --offline --python ~/.local/share/mise/installs/python/3.15.0/bin/python3.15 python -B -m unittest discover -s tests/unit -p test_trusted_exec_contract.py) > "$SCRATCH/tec-mut.out" 2>&1; echo "M05 the ceiling and alternates inert: unittest exit status: $?"; < "$SCRATCH/tec-mut.out" /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED" | sed "s/ (test_trusted_exec_contract[^)]*)//" | cut -c1-150 | sort | uniq -c; }; git worktree remove --force "$SCRATCH/tec-mut"
mutated: values = (git_dir, self.attacker, self.config, self.config, self.legit, git_dir / "objects") -> values = (git_dir, self.attacker, self.config, self.config, "/nonexistent", "/nonexistent")
M05 the ceiling and alternates inert: unittest exit status: 1
   1 FAIL: test_hostile_git_probe
   1 FAILED (failures=1)
   1 Ran 10 tests in 3.343s
[exit 0]
````

````console
$ : > "$SCRATCH/tec-mut.out"; git worktree add --detach -q "$SCRATCH/tec-mut" 7d3ecd4f && ~/.local/share/mise/installs/python/3.15.0/bin/python3.15 -I -c 'import sys; p, o, n = sys.argv[1:4]; s = open(p).read(); assert s.count(o) == 1, (s.count(o), o); open(p, "w").write(s.replace(o, n)); print("mutated:", o.strip(), "->", n.strip())' "$SCRATCH/tec-mut/tests/unit/trusted_exec_contract.py" 'argv = ["/usr/bin/env", "-i", f"PATH={SAFE_PATH}"' 'argv = ["/usr/bin/env", f"PATH={SAFE_PATH}"' && { (cd "$SCRATCH/tec-mut" && HOME="$(/usr/bin/mktemp -d "$TMPDIR/tec-home.XXXXXX")" uv run --no-project --offline --python ~/.local/share/mise/installs/python/3.15.0/bin/python3.15 python -B -m unittest discover -s tests/unit -p test_trusted_exec_contract.py) > "$SCRATCH/tec-mut.out" 2>&1; echo "M14 no env -i: unittest exit status: $?"; < "$SCRATCH/tec-mut.out" /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED" | sed "s/ (test_trusted_exec_contract[^)]*)//" | cut -c1-150 | sort | uniq -c; }; git worktree remove --force "$SCRATCH/tec-mut"
mutated: argv = ["/usr/bin/env", "-i", f"PATH={SAFE_PATH}" -> argv = ["/usr/bin/env", f"PATH={SAFE_PATH}"
M14 no env -i: unittest exit status: 1
   1 FAIL: test_each_probe_detects_condition [trusted_parent]
   1 FAIL: test_trusted_parent_probe
   1 FAILED (failures=2)
   1 Ran 10 tests in 3.414s
[exit 0]
````

````console
$ : > "$SCRATCH/tec-mut.out"; git worktree add --detach -q "$SCRATCH/tec-mut" 7d3ecd4f && ~/.local/share/mise/installs/python/3.15.0/bin/python3.15 -I -c 'import sys; p, o, n = sys.argv[1:4]; s = open(p).read(); assert s.count(o) == 1, (s.count(o), o); open(p, "w").write(s.replace(o, n)); print("mutated:", o.strip(), "->", n.strip())' "$SCRATCH/tec-mut/tests/unit/trusted_exec_contract.py" 'argv += ["/bin/bash", "--noprofile", "--norc", "-p", str(real)' 'argv += ["/bin/bash", str(real)' && { (cd "$SCRATCH/tec-mut" && HOME="$(/usr/bin/mktemp -d "$TMPDIR/tec-home.XXXXXX")" uv run --no-project --offline --python ~/.local/share/mise/installs/python/3.15.0/bin/python3.15 python -B -m unittest discover -s tests/unit -p test_trusted_exec_contract.py) > "$SCRATCH/tec-mut.out" 2>&1; echo "M15 bash with startup files and without -p: unittest exit status: $?"; < "$SCRATCH/tec-mut.out" /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED" | sed "s/ (test_trusted_exec_contract[^)]*)//" | cut -c1-150 | sort | uniq -c; }; git worktree remove --force "$SCRATCH/tec-mut"
mutated: argv += ["/bin/bash", "--noprofile", "--norc", "-p", str(real) -> argv += ["/bin/bash", str(real)
M15 bash with startup files and without -p: unittest exit status: 1
   1 FAIL: test_each_probe_detects_condition [trusted_parent]
   1 FAIL: test_trusted_parent_probe
   1 FAILED (failures=2)
   1 Ran 10 tests in 3.439s
[exit 0]
````

````console
$ : > "$SCRATCH/tec-mut.out"; git worktree add --detach -q "$SCRATCH/tec-mut" 7d3ecd4f && ~/.local/share/mise/installs/python/3.15.0/bin/python3.15 -I -c 'import sys; p, o, n = sys.argv[1:4]; s = open(p).read(); assert s.count(o) == 1, (s.count(o), o); open(p, "w").write(s.replace(o, n)); print("mutated:", o.strip(), "->", n.strip())' "$SCRATCH/tec-mut/tests/unit/trusted_exec_contract.py" 'return subprocess.run(argv, env={}, capture_output=True, text=True, check=False' 'return subprocess.run(argv, env=dict(os.environ), capture_output=True, text=True, check=False' && { (cd "$SCRATCH/tec-mut" && HOME="$(/usr/bin/mktemp -d "$TMPDIR/tec-home.XXXXXX")" uv run --no-project --offline --python ~/.local/share/mise/installs/python/3.15.0/bin/python3.15 python -B -m unittest discover -s tests/unit -p test_trusted_exec_contract.py) > "$SCRATCH/tec-mut.out" 2>&1; echo "M16 the inherited environment: unittest exit status: $?"; < "$SCRATCH/tec-mut.out" /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED" | sed "s/ (test_trusted_exec_contract[^)]*)//" | cut -c1-150 | sort | uniq -c; }; git worktree remove --force "$SCRATCH/tec-mut"
mutated: return subprocess.run(argv, env={}, capture_output=True, text=True, check=False -> return subprocess.run(argv, env=dict(os.environ), capture_output=True, text=True, check=False
M16 the inherited environment: unittest exit status: 1
   1 FAIL: test_each_probe_detects_condition [trusted_parent]
   1 FAIL: test_trusted_parent_probe
   1 FAILED (failures=2)
   1 Ran 10 tests in 3.395s
[exit 0]
````

````console
$ : > "$SCRATCH/tec-mut.out"; git worktree add --detach -q "$SCRATCH/tec-mut" 7d3ecd4f && ~/.local/share/mise/installs/python/3.15.0/bin/python3.15 -I -c 'import sys; p, o, n = sys.argv[1:4]; s = open(p).read(); assert s.count(o) == 1, (s.count(o), o); open(p, "w").write(s.replace(o, n)); print("mutated:", o.strip(), "->", n.strip())' "$SCRATCH/tec-mut/tests/unit/trusted_exec_contract.py" 'if not Path(script).is_absolute():' 'if False:' && { (cd "$SCRATCH/tec-mut" && HOME="$(/usr/bin/mktemp -d "$TMPDIR/tec-home.XXXXXX")" uv run --no-project --offline --python ~/.local/share/mise/installs/python/3.15.0/bin/python3.15 python -B -m unittest discover -s tests/unit -p test_trusted_exec_contract.py) > "$SCRATCH/tec-mut.out" 2>&1; echo "M18 no relative-path refusal: unittest exit status: $?"; < "$SCRATCH/tec-mut.out" /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED" | sed "s/ (test_trusted_exec_contract[^)]*)//" | cut -c1-150 | sort | uniq -c; }; git worktree remove --force "$SCRATCH/tec-mut"
mutated: if not Path(script).is_absolute(): -> if False:
M18 no relative-path refusal: unittest exit status: 1
   1 FAIL: test_trusted_parent_probe [relative]
   1 FAILED (failures=1)
   1 Ran 10 tests in 3.500s
[exit 0]
````

````console
$ : > "$SCRATCH/tec-mut.out"; git worktree add --detach -q "$SCRATCH/tec-mut" 7d3ecd4f && ~/.local/share/mise/installs/python/3.15.0/bin/python3.15 -I -c 'import sys; p, o, n = sys.argv[1:4]; s = open(p).read(); assert s.count(o) == 1, (s.count(o), o); open(p, "w").write(s.replace(o, n)); print("mutated:", o.strip(), "->", n.strip())' "$SCRATCH/tec-mut/tests/unit/trusted_exec_contract.py" 'return Path(__file__).resolve().parents[2]' 'return Path(subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip())' && { (cd "$SCRATCH/tec-mut" && HOME="$(/usr/bin/mktemp -d "$TMPDIR/tec-home.XXXXXX")" uv run --no-project --offline --python ~/.local/share/mise/installs/python/3.15.0/bin/python3.15 python -B -m unittest discover -s tests/unit -p test_trusted_exec_contract.py) > "$SCRATCH/tec-mut.out" 2>&1; echo "M25 the root from git and GIT_*: unittest exit status: $?"; < "$SCRATCH/tec-mut.out" /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED" | sed "s/ (test_trusted_exec_contract[^)]*)//" | cut -c1-150 | sort | uniq -c; }; git worktree remove --force "$SCRATCH/tec-mut"
mutated: return Path(__file__).resolve().parents[2] -> return Path(subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip())
M25 the root from git and GIT_*: unittest exit status: 1
   1 FAIL: test_trusted_parent_probe
   1 FAILED (failures=1)
   1 Ran 10 tests in 3.700s
[exit 0]
````

````console
$ : > "$SCRATCH/tec-mut.out"; git worktree add --detach -q "$SCRATCH/tec-mut" 7d3ecd4f && ~/.local/share/mise/installs/python/3.15.0/bin/python3.15 -I -c 'import sys; p, o, n = sys.argv[1:4]; s = open(p).read(); assert s.count(o) == 1, (s.count(o), o); open(p, "w").write(s.replace(o, n)); print("mutated:", o.strip(), "->", n.strip())' "$SCRATCH/tec-mut/tests/unit/trusted_exec_contract.py" 'found += [f"read {path}"] if path == self.input and st.st_atime_ns else []' 'found += []' && { (cd "$SCRATCH/tec-mut" && HOME="$(/usr/bin/mktemp -d "$TMPDIR/tec-home.XXXXXX")" uv run --no-project --offline --python ~/.local/share/mise/installs/python/3.15.0/bin/python3.15 python -B -m unittest discover -s tests/unit -p test_trusted_exec_contract.py) > "$SCRATCH/tec-mut.out" 2>&1; echo "worker-root read detection a no-op: unittest exit status: $?"; < "$SCRATCH/tec-mut.out" /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED" | sed "s/ (test_trusted_exec_contract[^)]*)//" | cut -c1-150 | sort | uniq -c; }; git worktree remove --force "$SCRATCH/tec-mut"
mutated: found += [f"read {path}"] if path == self.input and st.st_atime_ns else [] -> found += []
worker-root read detection a no-op: unittest exit status: 1
   1 FAIL: test_each_probe_detects_condition [worker_root]
   1 FAIL: test_worker_root_probe
   1 FAILED (failures=2)
   1 Ran 10 tests in 3.382s
[exit 0]
````

````console
$ : > "$SCRATCH/tec-mut.out"; git worktree add --detach -q "$SCRATCH/tec-mut" 7d3ecd4f && ~/.local/share/mise/installs/python/3.15.0/bin/python3.15 -I -c 'import sys; p, o, n = sys.argv[1:4]; s = open(p).read(); assert s.count(o) == 1, (s.count(o), o); open(p, "w").write(s.replace(o, n)); print("mutated:", o.strip(), "->", n.strip())' "$SCRATCH/tec-mut/tests/unit/trusted_exec_contract.py" 'if ((st.st_ino, st.st_mode), st.st_mtime_ns, content) != (identity, BASELINE_NS, LEGIT.encode()):' 'if False:' && { (cd "$SCRATCH/tec-mut" && HOME="$(/usr/bin/mktemp -d "$TMPDIR/tec-home.XXXXXX")" uv run --no-project --offline --python ~/.local/share/mise/installs/python/3.15.0/bin/python3.15 python -B -m unittest discover -s tests/unit -p test_trusted_exec_contract.py) > "$SCRATCH/tec-mut.out" 2>&1; echo "worker-root write detection a no-op: unittest exit status: $?"; < "$SCRATCH/tec-mut.out" /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED" | sed "s/ (test_trusted_exec_contract[^)]*)//" | cut -c1-150 | sort | uniq -c; }; git worktree remove --force "$SCRATCH/tec-mut"
mutated: if ((st.st_ino, st.st_mode), st.st_mtime_ns, content) != (identity, BASELINE_NS, LEGIT.encode()): -> if False:
worker-root write detection a no-op: unittest exit status: 1
   1 FAIL: test_each_probe_detects_condition [worker_root]
   1 FAIL: test_worker_root_probe
   1 FAIL: test_worker_root_probe_detects_a_same_length_overwrite [input]
   1 FAIL: test_worker_root_probe_detects_a_same_length_overwrite [output]
   1 FAILED (failures=4)
   1 Ran 10 tests in 3.439s
[exit 0]
````

````console
$ : > "$SCRATCH/tec-mut.out"; git worktree add --detach -q "$SCRATCH/tec-mut" 7d3ecd4f && ~/.local/share/mise/installs/python/3.15.0/bin/python3.15 -I -c 'import sys; p, o, n = sys.argv[1:4]; s = open(p).read(); assert s.count(o) == 1, (s.count(o), o); open(p, "w").write(s.replace(o, n)); print("mutated:", o.strip(), "->", n.strip())' "$SCRATCH/tec-mut/tests/unit/trusted_exec_contract.py" '(identity, BASELINE_NS, LEGIT.encode())' '(identity, BASELINE_NS, content)' && { (cd "$SCRATCH/tec-mut" && HOME="$(/usr/bin/mktemp -d "$TMPDIR/tec-home.XXXXXX")" uv run --no-project --offline --python ~/.local/share/mise/installs/python/3.15.0/bin/python3.15 python -B -m unittest discover -s tests/unit -p test_trusted_exec_contract.py) > "$SCRATCH/tec-mut.out" 2>&1; echo "worker-root content not compared: unittest exit status: $?"; < "$SCRATCH/tec-mut.out" /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED" | sed "s/ (test_trusted_exec_contract[^)]*)//" | cut -c1-150 | sort | uniq -c; }; git worktree remove --force "$SCRATCH/tec-mut"
mutated: (identity, BASELINE_NS, LEGIT.encode()) -> (identity, BASELINE_NS, content)
worker-root content not compared: unittest exit status: 1
   1 FAIL: test_worker_root_probe_detects_a_same_length_overwrite [input]
   1 FAIL: test_worker_root_probe_detects_a_same_length_overwrite [output]
   1 FAILED (failures=2)
   1 Ran 10 tests in 3.454s
[exit 0]
````

````console
$ : > "$SCRATCH/tec-mut.out"; git worktree add --detach -q "$SCRATCH/tec-mut" 7d3ecd4f && ~/.local/share/mise/installs/python/3.15.0/bin/python3.15 -I -c 'import sys; p, o, n = sys.argv[1:4]; s = open(p).read(); assert s.count(o) == 1, (s.count(o), o); open(p, "w").write(s.replace(o, n)); print("mutated:", o.strip(), "->", n.strip())' "$SCRATCH/tec-mut/tests/unit/trusted_exec_contract.py" 'os.utime(path, ns=(st.st_atime_ns, st.st_mtime_ns), follow_symlinks=False)' 'pass' && { (cd "$SCRATCH/tec-mut" && HOME="$(/usr/bin/mktemp -d "$TMPDIR/tec-home.XXXXXX")" uv run --no-project --offline --python ~/.local/share/mise/installs/python/3.15.0/bin/python3.15 python -B -m unittest discover -s tests/unit -p test_trusted_exec_contract.py) > "$SCRATCH/tec-mut.out" 2>&1; echo "worker-root access time not put back: unittest exit status: $?"; < "$SCRATCH/tec-mut.out" /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED" | sed "s/ (test_trusted_exec_contract[^)]*)//" | cut -c1-150 | sort | uniq -c; }; git worktree remove --force "$SCRATCH/tec-mut"
mutated: os.utime(path, ns=(st.st_atime_ns, st.st_mtime_ns), follow_symlinks=False) -> pass
worker-root access time not put back: unittest exit status: 1
   1 FAIL: test_each_probe_detects_condition [worker_root]
   1 FAIL: test_worker_root_probe
   1 FAILED (failures=2)
   1 Ran 10 tests in 3.454s
[exit 0]
````

````console
$ : > "$SCRATCH/tec-mut.out"; git worktree add --detach -q "$SCRATCH/tec-mut" 7d3ecd4f && ~/.local/share/mise/installs/python/3.15.0/bin/python3.15 -I -c 'import sys; p, o, n = sys.argv[1:4]; s = open(p).read(); assert s.count(o) == 1, (s.count(o), o); open(p, "w").write(s.replace(o, n)); print("mutated:", o.strip(), "->", n.strip())' "$SCRATCH/tec-mut/tests/unit/trusted_exec_contract.py" 'if runs := self.records():' 'if runs := []:' && { (cd "$SCRATCH/tec-mut" && HOME="$(/usr/bin/mktemp -d "$TMPDIR/tec-home.XXXXXX")" uv run --no-project --offline --python ~/.local/share/mise/installs/python/3.15.0/bin/python3.15 python -B -m unittest discover -s tests/unit -p test_trusted_exec_contract.py) > "$SCRATCH/tec-mut.out" 2>&1; echo "shim assertion a no-op: unittest exit status: $?"; < "$SCRATCH/tec-mut.out" /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED" | sed "s/ (test_trusted_exec_contract[^)]*)//" | cut -c1-150 | sort | uniq -c; }; git worktree remove --force "$SCRATCH/tec-mut"
mutated: if runs := self.records(): -> if runs := []:
shim assertion a no-op: unittest exit status: 1
   1 FAIL: test_each_probe_detects_condition [shim_on_path]
   1 FAIL: test_shim_probe
   1 FAILED (failures=2)
   1 Ran 10 tests in 2.416s
[exit 0]
````

````console
$ : > "$SCRATCH/tec-mut.out"; git worktree add --detach -q "$SCRATCH/tec-mut" 7d3ecd4f && ~/.local/share/mise/installs/python/3.15.0/bin/python3.15 -I -c 'import sys; p, o, n = sys.argv[1:4]; s = open(p).read(); assert s.count(o) == 1, (s.count(o), o); open(p, "w").write(s.replace(o, n)); print("mutated:", o.strip(), "->", n.strip())' "$SCRATCH/tec-mut/tests/unit/trusted_exec_contract.py" 'os.replace(self.base / ".swap", target)' 'os.unlink(self.base / ".swap")' && { (cd "$SCRATCH/tec-mut" && HOME="$(/usr/bin/mktemp -d "$TMPDIR/tec-home.XXXXXX")" uv run --no-project --offline --python ~/.local/share/mise/installs/python/3.15.0/bin/python3.15 python -B -m unittest discover -s tests/unit -p test_trusted_exec_contract.py) > "$SCRATCH/tec-mut.out" 2>&1; echo "swap barrier a no-op: unittest exit status: $?"; < "$SCRATCH/tec-mut.out" /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED" | sed "s/ (test_trusted_exec_contract[^)]*)//" | cut -c1-150 | sort | uniq -c; }; git worktree remove --force "$SCRATCH/tec-mut"
mutated: os.replace(self.base / ".swap", target) -> os.unlink(self.base / ".swap")
swap barrier a no-op: unittest exit status: 1
   1 FAIL: test_each_probe_detects_condition [swapped_file]
   1 FAIL: test_swapped_file_probe
   1 FAILED (failures=2)
   1 Ran 10 tests in 3.452s
[exit 0]
````

````console
$ : > "$SCRATCH/tec-mut.out"; git worktree add --detach -q "$SCRATCH/tec-mut" 7d3ecd4f && ~/.local/share/mise/installs/python/3.15.0/bin/python3.15 -I -c 'import sys; p, o, n = sys.argv[1:4]; s = open(p).read(); assert s.count(o) == 1, (s.count(o), o); open(p, "w").write(s.replace(o, n)); print("mutated:", o.strip(), "->", n.strip())' "$SCRATCH/tec-mut/tests/unit/trusted_exec_contract.py" 'if other != entry.pw_dir:' 'if False:' && { (cd "$SCRATCH/tec-mut" && HOME="$(/usr/bin/mktemp -d "$TMPDIR/tec-home.XXXXXX")" uv run --no-project --offline --python ~/.local/share/mise/installs/python/3.15.0/bin/python3.15 python -B -m unittest discover -s tests/unit -p test_trusted_exec_contract.py) > "$SCRATCH/tec-mut.out" 2>&1; echo "passwd cross-check off: unittest exit status: $?"; < "$SCRATCH/tec-mut.out" /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED" | sed "s/ (test_trusted_exec_contract[^)]*)//" | cut -c1-150 | sort | uniq -c; }; git worktree remove --force "$SCRATCH/tec-mut"
mutated: if other != entry.pw_dir: -> if False:
passwd cross-check off: unittest exit status: 1
   1 FAIL: test_passwd_home_uses_getpwuid_and_treats_dscl_or_getent_as_an_optional_cross_check [darwin 'NFSHomeDirectory: ~\n' disagree]
   1 FAIL: test_passwd_home_uses_getpwuid_and_treats_dscl_or_getent_as_an_optional_cross_check [darwin 'No such key: NFSHomeDirectory\n' disagree]
   1 FAIL: test_passwd_home_uses_getpwuid_and_treats_dscl_or_getent_as_an_optional_cross_check [linux 'a:b\n' disagree]
   1 FAILED (failures=3)
   1 Ran 10 tests in 3.494s
[exit 0]
````

````console
$ : > "$SCRATCH/tec-mut.out"; git worktree add --detach -q "$SCRATCH/tec-mut" 7d3ecd4f && ~/.local/share/mise/installs/python/3.15.0/bin/python3.15 -I -c 'import sys; p, o, n = sys.argv[1:4]; s = open(p).read(); assert s.count(o) == 1, (s.count(o), o); open(p, "w").write(s.replace(o, n)); print("mutated:", o.strip(), "->", n.strip())' "$SCRATCH/tec-mut/tests/unit/trusted_exec_contract.py" 'except (OSError, subprocess.CalledProcessError):' 'except ():' && { (cd "$SCRATCH/tec-mut" && HOME="$(/usr/bin/mktemp -d "$TMPDIR/tec-home.XXXXXX")" uv run --no-project --offline --python ~/.local/share/mise/installs/python/3.15.0/bin/python3.15 python -B -m unittest discover -s tests/unit -p test_trusted_exec_contract.py) > "$SCRATCH/tec-mut.out" 2>&1; echo "passwd fails when dscl or getent cannot run: unittest exit status: $?"; < "$SCRATCH/tec-mut.out" /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED" | sed "s/ (test_trusted_exec_contract[^)]*)//" | cut -c1-150 | sort | uniq -c; }; git worktree remove --force "$SCRATCH/tec-mut"
mutated: except (OSError, subprocess.CalledProcessError): -> except ():
passwd fails when dscl or getent cannot run: unittest exit status: 1
   1 ERROR: test_passwd_home_uses_getpwuid_and_treats_dscl_or_getent_as_an_optional_cross_check [darwin CalledProcessError(70, ['/usr/bin/dscl', '.', '-rea
   1 ERROR: test_passwd_home_uses_getpwuid_and_treats_dscl_or_getent_as_an_optional_cross_check [linux OSError('no getent') ~]
   1 FAILED (errors=2)
   1 Ran 10 tests in 3.504s
[exit 0]
````

````console
$ : > "$SCRATCH/tec-mut.out"; git worktree add --detach -q "$SCRATCH/tec-mut" 7d3ecd4f && ~/.local/share/mise/installs/python/3.15.0/bin/python3.15 -I -c 'import sys; p, o, n = sys.argv[1:4]; s = open(p).read(); assert s.count(o) == 1, (s.count(o), o); open(p, "w").write(s.replace(o, n)); print("mutated:", o.strip(), "->", n.strip())' "$SCRATCH/tec-mut/tests/unit/trusted_exec_contract.py" 'if not entry.pw_dir.startswith("/") or "\n" in entry.pw_dir:' 'if False:' && { (cd "$SCRATCH/tec-mut" && HOME="$(/usr/bin/mktemp -d "$TMPDIR/tec-home.XXXXXX")" uv run --no-project --offline --python ~/.local/share/mise/installs/python/3.15.0/bin/python3.15 python -B -m unittest discover -s tests/unit -p test_trusted_exec_contract.py) > "$SCRATCH/tec-mut.out" 2>&1; echo "passwd accepts a non-absolute home: unittest exit status: $?"; < "$SCRATCH/tec-mut.out" /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED" | sed "s/ (test_trusted_exec_contract[^)]*)//" | cut -c1-150 | sort | uniq -c; }; git worktree remove --force "$SCRATCH/tec-mut"
mutated: if not entry.pw_dir.startswith("/") or "\n" in entry.pw_dir: -> if False:
passwd accepts a non-absolute home: unittest exit status: 1
   1 FAIL: test_passwd_home_uses_getpwuid_and_treats_dscl_or_getent_as_an_optional_cross_check [win32 None no absolute]
   1 FAILED (failures=1)
   1 Ran 10 tests in 3.585s
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
$ make format > "$SCRATCH/tec-format.out" 2>&1; echo "make format exit status: $?"; base="$(git merge-base origin/main HEAD)"; sed -n "s/^diff \([^ ]*\)\.orig .*/\1/p" "$SCRATCH/tec-format.out" > "$SCRATCH/tec-flagged.txt"; echo "files the whole-tree shfmt step flags: $(wc -l < "$SCRATCH/tec-flagged.txt" | tr -d " ")"; while read -r f; do git diff --quiet "$base" HEAD -- "$f" && echo "unchanged from ${base:0:8}: $f" || echo "CHANGED by this PR: $f"; done < "$SCRATCH/tec-flagged.txt"
make format exit status: 2
files the whole-tree shfmt step flags: 12
unchanged from 118daafa: .orchestration/tasks/dotfiles-T128-chain-github-scripts-a01-input/pr-cost.sh
unchanged from 118daafa: .orchestration/tasks/dotfiles-T128-chain-github-scripts-a01-input/resolve-threads.sh
unchanged from 118daafa: .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/local-advisory.sh
unchanged from 118daafa: .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/local-review.sh
unchanged from 118daafa: .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/sandbox-scan.sh
unchanged from 118daafa: .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/boundary.sh
unchanged from 118daafa: .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/ff-main.sh
unchanged from 118daafa: .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/orch-audit.sh
unchanged from 118daafa: .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/orch-gate.sh
unchanged from 118daafa: .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/t717-prep.sh
unchanged from 118daafa: home/dot_claude/hooks/executable_project-map-reload.sh
unchanged from 118daafa: tests/install/macos/common/brew.bats
[exit 0]
````

````console
$ git diff --numstat origin/main...HEAD -- tests; git diff --numstat origin/main...HEAD -- tests/unit/trusted_exec_contract.py tests/unit/test_trusted_exec_contract.py | awk '{ printf "%s: %d added + %d deleted = %d changed lines (cap %d)\n", $3, $1, $2, $1 + $2, ($3 ~ /test_trusted/ ? 350 : 250) }'; wc -l tests/unit/trusted_exec_contract.py tests/unit/test_trusted_exec_contract.py .orchestration/dotfiles-T133-trusted-exec-contract-tests-a01/task.md
350	0	tests/unit/test_trusted_exec_contract.py
247	0	tests/unit/trusted_exec_contract.py
tests/unit/test_trusted_exec_contract.py: 350 added + 0 deleted = 350 changed lines (cap 350)
tests/unit/trusted_exec_contract.py: 247 added + 0 deleted = 247 changed lines (cap 250)
     247 tests/unit/trusted_exec_contract.py
     350 tests/unit/test_trusted_exec_contract.py
     198 .orchestration/dotfiles-T133-trusted-exec-contract-tests-a01/task.md
     795 total
[exit 0]
````

## 9. macOS CI does not run this module

The macOS CI row skips the unit suite for this pull request. `.github/workflows/test.yaml` skips macOS on a pull request whose every relevant path is Python, docs or records, and this diff is `tests/unit/*.py` plus `.orchestration/`. The unit-test run on the earlier evidence head `25dd01e5` (the same path classes) shows the macOS job's test steps skipped. The macOS evidence for this module is therefore this seat's local runs above; Linux CI is the only CI that runs it.

````console
$ sed -n "113,123p" .github/workflows/test.yaml
          relevant="$(grep -v '^\.orchestration/' <<< "${changed}" || true)"
          if ! grep -Eq '^(\.github/workflows/|\.github/flakes\.yaml$|home/|install/|scripts/|tests/|plans/|docs/|setup\.sh$|Makefile$|ruff\.toml$|\.prettierignore$)|(^|/)[^/]+\.(py|md)$' <<< "${relevant}"; then
            echo "should_test=false" >> "${GITHUB_OUTPUT}"
            echo "skip_reason=unrelated" >> "${GITHUB_OUTPUT}"
          # macOS adds nothing to a pull request whose every relevant path is Python, docs or records: a shell,
          # install, home, bats, Makefile or workflow change keeps it, and a push to main runs the full matrix.
          elif [ "${OS:-}" = macos-14 ] && [ "${EVENT_NAME}" = pull_request ] &&
            ! grep -Evq '^(scripts/.*\.py$|tests/unit/.*\.py$|docs/|plans/|\.orchestration/|[^/]+\.md$|ruff\.toml$|\.prettierignore$)' <<< "${relevant}"; then
            echo "should_test=false" >> "${GITHUB_OUTPUT}"
            echo "skip_reason=os-independent on macos-14" >> "${GITHUB_OUTPUT}"
          else
[exit 0]
````

````console
$ gh run view 39353594398 --repo mryfmo/dotfiles --json headSha,jobs --jq '"head " + .headSha[0:8], (.jobs[] | select(.name | test("macos")) | .name + ": " + .conclusion, (.steps[] | select(.number >= 4 and .number <= 17) | "  \(.number) \(.name): \(.conclusion)"))'
head 25dd01e5
test (macos-14, client): success
  4 Decide whether the diff needs the unit tests: success
  5 Skip full unit test run for unrelated changes: success
  6 Install tools: skipped
  7 Prepare statusline tool config: skipped
  8 Setup mise for statusline smoke: skipped
  9 Install statusline tools: skipped
  10 Smoke-test statusline tools without network: skipped
  11 Run `shfmt`: skipped
  12 Check Python and Markdown formatting: skipped
  13 Run `ShellCheck`: skipped
  14 Setup uv: skipped
  15 Run Python unit tests: skipped
  16 Prepare public dotfiles fixture: skipped
  17 Run unit test: skipped
[exit 0]
````

## 10. The review gate

Run with the records in place and uncommitted, before the evidence commit.

````console
$ make require-crit-review AGENT_REVIEWED=1 REVIEW_EVIDENCE=.orchestration/dotfiles-T133-trusted-exec-contract-tests-a01/dotfiles-T133-trusted-exec-contract-tests-a01-worker-review-receipt.md
Review requirement satisfied by AGENT_REVIEWED=1 with REVIEW_EVIDENCE.
[exit 0]
````
