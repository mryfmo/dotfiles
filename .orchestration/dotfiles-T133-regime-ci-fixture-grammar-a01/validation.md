---
task_id: dotfiles-T133-regime-ci-fixture-grammar-a01
seat: claude-standard-dot-a009
amendment: 1
base: 60a6fb2b324d0381c4a6e539b37c650105154a7e
code_head: 15bc046ef0bc50476879e92cfaa42e5952f6878b
---

# Validation: dotfiles-T133-regime-ci-fixture-grammar-a01

- **Where:** every block ran inside the sandbox, from this worktree on `tools/regime-ci-fixture-grammar-a01`. §1 to §9 ran at the code head `15bc046e`, with §4 in a scratch worktree of the branch point `60a6fb2b`. §10 to §12 ran after the PR opened. The later commits add only this directory's records.
- **Placeholders:** each block prints its commands, their verbatim output and the block's last exit status. `MAIN` is the main checkout, `T` the task id, `$S` the session scratchpad, `$TMPDIR` the sandbox's temporary directory, and `~` the home directory. The proxy variables are passed by name, and their values are never printed.
- **Before and after:** the Check of amendment 1 passes on the unmodified module (§4) and on this head (§6), with 16 tests each time. Each block also runs it once more with the sandbox's three proxy variables passed through.
- **The proxy variables:** `env -i` strips `HTTPS_PROXY`, `HTTP_PROXY` and `NO_PROXY`. Whenever `uv run --with pyyaml` has to revalidate its index against pypi.org, the amended command then fails with a DNS error (§4h; the pre-push reviewer saw 3 failures and 1 error once). With the variables passed it does not depend on uv's cache.
- **§4h** is the round-1 history: the dispatched command's 22 errors on the unmodified module (`uv` not on `PATH`, then `git init` in the worktree, because `TMPDIR` was unset), and the DNS failure.

## 1. Task file (amendment 1, sha256 c2bfda03…) and the branch copy
```console
$ shasum -a 256 "~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-regime-ci-fixture-grammar-a01.md" ".orchestration/dotfiles-T133-regime-ci-fixture-grammar-a01/task.md"; cmp "~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-regime-ci-fixture-grammar-a01.md" ".orchestration/dotfiles-T133-regime-ci-fixture-grammar-a01/task.md" && echo byte-identical; wc -l < ".orchestration/dotfiles-T133-regime-ci-fixture-grammar-a01/task.md"
509e4c5430069deb70e35779ea1e36ff49bb7779c1a7615b1e627453242173d6  ~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-regime-ci-fixture-grammar-a01.md
c2bfda037d2012e3703f12b7eedc2e976f79f5259ec5e47798248d544a69cc2b  .orchestration/dotfiles-T133-regime-ci-fixture-grammar-a01/task.md
~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-regime-ci-fixture-grammar-a01.md .orchestration/dotfiles-T133-regime-ci-fixture-grammar-a01/task.md differ: char 5975, line 55
      66
[exit 0]
```

## 1a. The task-consistency check on the dispatched file
```console
$ uv run --offline --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py --root "$PWD" "~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-regime-ci-fixture-grammar-a01.md"
dotfiles-T133-regime-ci-fixture-grammar-a01.md: OK
[exit 0]
```

## 2. Branch, branch point and commits
```console
$ git rev-parse --abbrev-ref HEAD; git merge-base 60a6fb2b324d0381c4a6e539b37c650105154a7e HEAD; git log --format='%H %s' 60a6fb2b324d0381c4a6e539b37c650105154a7e..HEAD | cut -c1-140
tools/regime-ci-fixture-grammar-a01
60a6fb2b324d0381c4a6e539b37c650105154a7e
15bc046ef0bc50476879e92cfaa42e5952f6878b test(regime-ci): the fixture rows use the disposition grammar (T133 regime-ci fixture-grammar a01)
53c9e23f6aa421ed2a79781ba92685bfa5f5ebd0 chore(orchestration): the dotfiles-T133-regime-ci-fixture-grammar-a01 task copy (amendment 1)
[exit 0]
```

## 3. The premise at the branch point: the five bare rows
```console
$ git show 60a6fb2b324d0381c4a6e539b37c650105154a7e:tests/unit/test_regime_ci.py | /usr/bin/grep -nE 'disposition: residual'
27:    f"  - control: {name}\n    disposition: residual\n"
127:        rows = "".join(f"  - control: the PR edits {path}\n    disposition: residual\n" for path in scripts)
276:        no_row = TASK.replace("  - control: the PR edits src/tool.sh\n    disposition: residual\n", "")
372:        rows = f"  - control: the predecessor copy .orchestration/{T}/task.md\n    disposition: residual\n"
373:        rows += f"  - control: the task copy .orchestration/{later}/task.md\n    disposition: residual\n"
[exit 0]
```

## 4. Before: the Check (amendment 1), then with the sandbox proxy variables, on the unmodified module at the branch point (scratch worktree, removed)
```console
$ git worktree add --detach -q "$S/fg-base" 60a6fb2b324d0381c4a6e539b37c650105154a7e && cd "$S/fg-base" && { /usr/bin/env -i PATH="$(dirname "$(command -v uv)"):/usr/bin:/bin" HOME="$HOME" TMPDIR="$TMPDIR" LANG=C.UTF-8 "$HOME/.local/share/mise/installs/python/3.15.0/bin/python3" -I tests/unit/test_regime_ci.py 2>&1 | tail -3; echo "amended command exit=${PIPESTATUS[0]}"; /usr/bin/env -i PATH="$(dirname "$(command -v uv)"):/usr/bin:/bin" HOME="$HOME" TMPDIR="$TMPDIR" LANG=C.UTF-8 HTTPS_PROXY="$HTTPS_PROXY" HTTP_PROXY="$HTTP_PROXY" NO_PROXY="$NO_PROXY" "$HOME/.local/share/mise/installs/python/3.15.0/bin/python3" -I tests/unit/test_regime_ci.py 2>&1 | tail -3; echo "with the proxy variables exit=${PIPESTATUS[0]}"; }; rc=0; cd - > /dev/null; git worktree remove --force "$S/fg-base"; echo "removed=$?"; exit $rc
Ran 16 tests in 51.264s

OK
amended command exit=0
Ran 16 tests in 49.984s

OK
with the proxy variables exit=0
removed=0
[exit 0]
```

## 4h. History: the dispatched Check (round 1, before amendment 1) and the proxy observation, on the unmodified module
```console
$ /usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" LANG=C.UTF-8 "$HOME/.local/share/mise/installs/python/3.15.0/bin/python3" -I tests/unit/test_regime_ci.py > "$S/fixture-before-aswritten.log" 2>&1; echo "exit=$?"
exit=1
$ grep -E '^[A-Za-z.]*Error' "$S/fixture-before-aswritten.log" | sort | uniq -c; tail -2 "$S/fixture-before-aswritten.log"
  1 FileNotFoundError: [Errno 2] No such file or directory: 'uv'
 21 subprocess.CalledProcessError: Command '['git', '-c', 'commit.gpgsign=false', 'init', '-q', '-b', 'main']' returned non-zero exit status 128.

FAILED (errors=22)
$ # 04:4xZ, with uv's directory on PATH and TMPDIR set, one test run alone, while uv's index cache needed pypi.org:
$ /usr/bin/env -i PATH="/usr/bin:/bin:<uv dir>" HOME="$HOME" LANG=C.UTF-8 TMPDIR="$TMPDIR" "$HOME/.local/share/mise/installs/python/3.15.0/bin/python3" -I tests/unit/test_regime_ci.py -k test_regime_ci_reports_each_violation_once_and_passes_a_consistent_pr > "$S/fixture-one.log" 2>&1; grep -E 'AssertionError|error:|cause:' "$S/fixture-one.log"
AssertionError: Tuples differ: (0, 'regime-ci: ok 1 task(s)\n') != (2, '')
+ (2, '') : error: Request failed after 3 retries in 6.4s
  cause: Failed to fetch: https://pypi.org/simple/pyyaml/
  cause: error sending request for url (https://pypi.org/simple/pyyaml/)
  cause: client error (Connect)
  cause: dns error
  cause: failed to lookup address information: nodename nor servname provided, or not known
```

## 5. The change: one constant and the five rows
```console
$ git diff 60a6fb2b324d0381c4a6e539b37c650105154a7e...HEAD -- tests; /usr/bin/grep -nE 'disposition: residual' tests/unit/test_regime_ci.py; echo "bare rows left: grep exit=$?"
diff --git a/tests/unit/test_regime_ci.py b/tests/unit/test_regime_ci.py
index c356ff89..1f416223 100644
--- a/tests/unit/test_regime_ci.py
+++ b/tests/unit/test_regime_ci.py
@@ -23,8 +23,9 @@ UV = [
     "-I",
 ]  # as regime.yml
 T = "t1-a01"
+RESIDUAL = '"residual: the fixture row is test data for this control"'
 ROWS = "".join(
-    f"  - control: {name}\n    disposition: residual\n"
+    f"  - control: {name}\n    disposition: {RESIDUAL}\n"
     for name in (
         "the PR edits src/tool.sh",
         "the PR edits tests/unit/test_tool.py",
@@ -124,7 +125,7 @@ class RegimeCiTest(unittest.TestCase):
         # verifier and checker still decide, the checkout stays at the base, and no head program runs.
         fake = 'import pathlib\npathlib.Path("head-program-ran").write_text("x")\nprint("{line}")\n'
         scripts = {VERIFIER: fake.format(line="regime-ci: ok 1 task(s)"), CHECKER: fake.format(line="task.md: OK")}
-        rows = "".join(f"  - control: the PR edits {path}\n    disposition: residual\n" for path in scripts)
+        rows = "".join(f"  - control: the PR edits {path}\n    disposition: {RESIDUAL}\n" for path in scripts)
         policy = TASK.replace("threat_table:\n", "threat_table:\n" + rows).replace("at most 3 ", "at most 999 ")
         policy = policy.replace("  - src/tool.sh\n", "  - src/tool.sh\n" + "".join(f"  - {path}\n" for path in scripts))
         forged = policy.replace("  - src/tool.sh\n", "  - src/tool.sh\n  - stray.sh\n")
@@ -273,7 +274,7 @@ class RegimeCiTest(unittest.TestCase):
     def test_regime_ci_reports_each_violation_once_and_passes_a_consistent_pr(self):
         result = self.build()
         self.assertEqual((0, "regime-ci: ok 1 task(s)\n"), (result.returncode, result.stdout), result.stderr)
-        no_row = TASK.replace("  - control: the PR edits src/tool.sh\n    disposition: residual\n", "")
+        no_row = TASK.replace(f"  - control: the PR edits src/tool.sh\n    disposition: {RESIDUAL}\n", "")
         crash = TASK.replace("threat_table:\n", "threat_table:\n  - a row that is no mapping\n")
         worded = TASK.replace("changed lines outside", "changed lines (added plus deleted) outside")
         four = CODE | {"src/tool.sh": "a\nb\nc\nd\n"}
@@ -369,8 +370,8 @@ class RegimeCiTest(unittest.TestCase):
         # Amendment 1: a later copy whose reset_of names an earlier one is the lineage's only target; the earlier copy
         # warns, and its own .orchestration/ paths are no stray of the later one. Without reset_of, both are targets.
         later = "t1-a02"
-        rows = f"  - control: the predecessor copy .orchestration/{T}/task.md\n    disposition: residual\n"
-        rows += f"  - control: the task copy .orchestration/{later}/task.md\n    disposition: residual\n"
+        rows = f"  - control: the predecessor copy .orchestration/{T}/task.md\n    disposition: {RESIDUAL}\n"
+        rows += f"  - control: the task copy .orchestration/{later}/task.md\n    disposition: {RESIDUAL}\n"
         reset = TASK.replace(T, later).replace("allowed_files:", f"reset_of: [{T}]\nallowed_files:")
         reset = reset.replace("threat_table:\n", "threat_table:\n" + rows)
         for text, expected, kept in ((reset, 0, True), (reset, 0, False), (TASK.replace(T, later), 1, True)):
bare rows left: grep exit=1
[exit 0]
```

## 6. After: the Check (amendment 1), then with the sandbox proxy variables, on this head
```console
$ /usr/bin/env -i PATH="$(dirname "$(command -v uv)"):/usr/bin:/bin" HOME="$HOME" TMPDIR="$TMPDIR" LANG=C.UTF-8 "$HOME/.local/share/mise/installs/python/3.15.0/bin/python3" -I tests/unit/test_regime_ci.py 2>&1 | tail -3; echo "amended command exit=${PIPESTATUS[0]}"; /usr/bin/env -i PATH="$(dirname "$(command -v uv)"):/usr/bin:/bin" HOME="$HOME" TMPDIR="$TMPDIR" LANG=C.UTF-8 HTTPS_PROXY="$HTTPS_PROXY" HTTP_PROXY="$HTTP_PROXY" NO_PROXY="$NO_PROXY" "$HOME/.local/share/mise/installs/python/3.15.0/bin/python3" -I tests/unit/test_regime_ci.py 2>&1 | tail -3; echo "with the proxy variables exit=${PIPESTATUS[0]}"
Ran 16 tests in 47.044s

OK
amended command exit=0
Ran 16 tests in 49.253s

OK
with the proxy variables exit=0
[exit 0]
```

## 7. The constant's value under the a05 checker's C13 and C11 (PR #417's rules, applied to the PyYAML-parsed fixture row)
```console
$ git show origin/tools/task-generator-plan-check-a01:scripts/orchestrator/task-consistency-check.py | sed -n '390,403p'; uv run --no-project --with pyyaml python -I -c 'import re, sys, yaml; sys.path.insert(0, "."); src = open("tests/unit/test_regime_ci.py").read(); R = re.search(r"^RESIDUAL = (.*)$", src, re.M).group(1); v = eval(R); d = yaml.safe_load("threat_table:\n  - control: the PR edits src/tool.sh\n    disposition: " + v + "\n")["threat_table"][0]["disposition"]; f = next(x for x in ("closed: ", "residual: ", "out-of-scope: ") if d.startswith(x)); print(repr(d), repr(f), len(d) - len(f))'
    for r in rows:  # C13, then C11 on the form it found
        d = str(r.get("disposition") or "")
        form = next((f for f in FORMS if d.startswith(f)), None)
        if form is None:
            fails.append(f"C13 disposition is not closed:, residual: or out-of-scope: and a space: {d[:60]}")
            continue
        load = d[len(form) :]
        if form == "closed: " and not re.fullmatch(r"tests/[\w./-]+::(?:[A-Za-z_]\w*::)?[A-Za-z_]\w*", load):
            fails.append(f"C11 closed: payload is not tests/<path>::<identifier>: {load[:60]}")
        tid_ok = re.fullmatch(r"[A-Za-z0-9][\w.-]*", load) and (root / f".orchestration/tasks/{load}.md").is_file()
        if form == "out-of-scope: " and not tid_ok:
            fails.append(f"C11 out-of-scope: {load[:60]} is not a task under .orchestration/tasks/")
        if form == "residual: " and len(load) < 20:
            fails.append(f"C11 residual: payload is shorter than 20 characters: {load}")
'residual: the fixture row is test data for this control' 'residual: ' 45
[exit 0]
```

## 8. ruff format and ruff check on the module
```console
$ ruff format --config ruff.toml --check tests/unit/test_regime_ci.py; ruff check --config ruff.toml --output-format concise tests/unit/test_regime_ci.py
1 file already formatted
All checks passed!
[exit 0]
```

## 9. Caps from the branch point
```console
$ git diff --numstat 60a6fb2b324d0381c4a6e539b37c650105154a7e...HEAD; git diff --numstat 60a6fb2b324d0381c4a6e539b37c650105154a7e...HEAD | awk -F '\t' '$3 ~ /^\.orchestration\// {next} $3 ~ /^tests\// {t += $1 + $2; next} {o += $1 + $2} END {printf "outside tests/ and .orchestration/: %d of 0\nunder tests/: %d of 12\n", o, t}'
66	0	.orchestration/dotfiles-T133-regime-ci-fixture-grammar-a01/task.md
6	5	tests/unit/test_regime_ci.py
outside tests/ and .orchestration/: 0 of 0
under tests/: 11 of 12
[exit 0]
```
