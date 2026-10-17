---
task_id: dotfiles-T129-assets-omp-hcom-followup-a02
seat: claude-standard-dot-a007
---

# Validation: dotfiles-T129-assets-omp-hcom-followup-a02

Every command ran from the worktree `.claude/worktrees/worker-c` on the branch `tools/assets-hcom-followup-a02` (stacked on PR #398's head 2b91aef9), inside the sandbox; `MAIN` names the main checkout and `T` the task id. The output is verbatim, with the home directory replaced by `~`; each block ends with the exit status of the command shown. The updater tests run with the a01 task's evidence-run `mktemp` shim first on PATH (macOS `mktemp` without a template fails in this sandbox); the shim is not in the repository:

```sh
#!/bin/sh
# Evidence-run shim, not in the repository: macOS mktemp without a template ignores TMPDIR, and the Claude sandbox
# denies its default directory; give the two template-less forms a TMPDIR template.
if [ "$#" -eq 0 ]; then exec /usr/bin/mktemp "${TMPDIR:-/tmp}/tmp.XXXXXXXX"; fi
if [ "$#" -eq 1 ] && [ "$1" = "-d" ]; then exec /usr/bin/mktemp -d "${TMPDIR:-/tmp}/tmp.XXXXXXXX"; fi
exec /usr/bin/mktemp "$@"
```

## 1. Task file, task copy and the owned rows

```console
$ shasum -a 256 "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md"; cmp "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md" && echo byte-identical
adef9ddfc4d3458c85340a73aca9954f2ad8210982bc868171dbd68a2d65ee76  $MAIN/.orchestration/tasks/dotfiles-T129-assets-omp-hcom-followup-a02.md
adef9ddfc4d3458c85340a73aca9954f2ad8210982bc868171dbd68a2d65ee76  .orchestration/dotfiles-T129-assets-omp-hcom-followup-a02/task.md
byte-identical
(exit 0)
$ UV_OFFLINE=1 uv run --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py --root "$PWD" "$MAIN/.orchestration/tasks/$T.md"
dotfiles-T129-assets-omp-hcom-followup-a02.md: OK
(exit 0)
$ git rev-parse HEAD   # PR #398 head, the stacked base
2b91aef95161bf1e38755a2b233094b30dca80c1
(exit 0)
$ grep -E "^(4303212235|4303338055|local:fbbc6d9:1)" the owner sections   # the three rows as recorded
38:4303212235	uninstall-leaves-tool-env
50:4303338055	install-receipt-repair
108:- re-own: local:fbbc6d9:1 and local:fbbc6d9:2 -> dotfiles-T129-assets-omp-hcom-followup-a01 (the assets lineage; fixed in PR #398 by 457984c9 and 1537863d);
(exit 0)
```

## 2. The diff against 2b91aef9

```console
$ git diff 2b91aef95161bf1e38755a2b233094b30dca80c1 -- scripts tests home
diff --git a/home/dot_local/bin/common/executable_remove-agent-asset b/home/dot_local/bin/common/executable_remove-agent-asset
index 92df2d7d..8120e158 100755
--- a/home/dot_local/bin/common/executable_remove-agent-asset
+++ b/home/dot_local/bin/common/executable_remove-agent-asset
@@ -95,7 +95,8 @@ function path_is_in_safe_root() {
         "${HOME}/.claude/plugins/cache" \
         "${CODEX_ASSET_ROOT}/plugins/cache" \
         "${CODEX_ASSET_ROOT}/.tmp/plugins/plugins" \
-        "${HOME}/.local/share/mise/installs"; do
+        "${HOME}/.local/share/mise/installs" \
+        "${HOME}/.local/share/agent-assets"; do
         root="$(normalize_root_path "${root}")" || return 1
         if [ "${candidate}" != "${root}" ] && path_has_prefix "${candidate}" "${root}"; then
             return 0
@@ -432,6 +433,25 @@ function load_entry() {
     done < <(printf '%s\n' "${ENTRY}" | jq -r '.commands[]')
 }
 
+#
+# @description Remove hcom: uv uninstalls its tool environment, receipt and entry point, then the retained wheel goes.
+#
+function remove_hcom() {
+    local path
+    local -a wheels=()
+    for path in "${RECORDED_PATHS[@]}"; do
+        # uv owns the entry point it created; the updater owns the wheel it kept for uv's receipt.
+        [ "${path}" = "${HOME}/.local/bin/hcom" ] || wheels+=("${path}")
+    done
+    has_command uv || {
+        fail "uv is not installed, so hcom's uv tool environment cannot be uninstalled; nothing was removed"
+        return 1
+    }
+    [ "${#wheels[@]}" -eq 0 ] || preflight_deletion_paths "${wheels[@]}"
+    run_operation uv tool uninstall hcom
+    [ "${#wheels[@]}" -eq 0 ] || remove_recorded_paths "${wheels[@]}"
+}
+
 #
 # @description Parse arguments and perform the selected inverse operation.
 # @arg $@ string Command-line arguments.
@@ -463,7 +483,11 @@ function main() {
             fail "manifest step has no removal paths: ${STEP}"
             return 1
         }
-        remove_recorded_paths "${RECORDED_PATHS[@]}"
+        if [ "${STEP}" = "update_hcom" ]; then
+            remove_hcom
+        else
+            remove_recorded_paths "${RECORDED_PATHS[@]}"
+        fi
         ;;
     brew)
         remove_brew
diff --git a/scripts/update-agent-assets.sh b/scripts/update-agent-assets.sh
index 31cdc4c6..047b5bfe 100755
--- a/scripts/update-agent-assets.sh
+++ b/scripts/update-agent-assets.sh
@@ -919,7 +919,7 @@ function update_terminal_browser() {
 # @exitcode 1 The download checksum or installed version differs from its pin.
 #
 function update_omp() (
-    local installed download_dir tarball actual
+    local installed download_dir tarball actual entry aside=""
     has_command npm || {
         printf 'Skipping omp: npm command not found.\n'
         return 0
@@ -940,11 +940,25 @@ function update_omp() (
         printf 'omp checksum mismatch: expected %s, got %s.\n' "${OMP_TARBALL_SHA256}" "${actual}" >&2
         return 1
     fi
+    # npm refuses to replace a bin entry it does not own (EEXIST): a standalone executable or a link anywhere but
+    # this package, a dangling one included, moves aside, and comes back if the install does not end at the pin.
+    entry="${HOME}/.local/bin/omp"
+    if { [ -e "${entry}" ] || [ -L "${entry}" ]; } &&
+        [[ "$(readlink "${entry}" 2> /dev/null)" != *lib/node_modules/@oh-my-pi/pi-coding-agent/* ]]; then
+        aside="${download_dir}/omp.previous"
+        mv "${entry}" "${aside}" || return
+        printf 'omp: moved the existing non-npm %s aside for the npm install.\n' "${entry}"
+    fi
     # Allow this reviewed pin before the default three-day cooldown expires.
-    npm_config_min_release_age=0 npm install -g --prefix "${HOME}/.local" "${tarball}" || return
-    installed="$("${HOME}/.local/bin/omp" --version 2> /dev/null | awk 'NR == 1 { print $NF }')" || installed=none
-    installed="${installed#omp/}"
+    if npm_config_min_release_age=0 npm install -g --prefix "${HOME}/.local" "${tarball}"; then
+        installed="$("${entry}" --version 2> /dev/null | awk 'NR == 1 { print $NF }')" || installed=none
+        installed="${installed#omp/}"
+    else
+        installed=failed
+    fi
     if [ "${installed}" != "${OMP_PIN_VERSION}" ]; then
+        [ -z "${aside}" ] || { rm -f "${entry}" && mv "${aside}" "${entry}"; }
+        [ "${installed}" = failed ] && return 1
         printf 'omp version mismatch: expected %s, got %s.\n' "${OMP_PIN_VERSION}" "${installed}" >&2
         return 1
     fi
@@ -992,7 +1006,11 @@ function update_hcom() (
     fi
     mkdir -p "${wheel_dir}" && mv -f "${wheel}" "${wheel_dir}/" || return
     wheel="${wheel_dir}/${url##*/}"
-    uv tool install --force "${wheel}" || return
+    # A failed install drops the kept wheel, so the next run retries instead of skipping on it (the Bot's 4303338055).
+    uv tool install --force "${wheel}" || {
+        rm -f "${wheel}"
+        return 1
+    }
     installed="$("${HOME}/.local/bin/hcom" --version 2> /dev/null | awk 'NR == 1 { print $NF }')" || installed=none
     if [ "${installed}" != "${HCOM_PIN_VERSION}" ]; then
         printf 'hcom version mismatch: expected %s, got %s.\n' "${HCOM_PIN_VERSION}" "${installed}" >&2
diff --git a/tests/unit/test_remove_agent_asset.py b/tests/unit/test_remove_agent_asset.py
index 2fc154e3..77631933 100644
--- a/tests/unit/test_remove_agent_asset.py
+++ b/tests/unit/test_remove_agent_asset.py
@@ -343,6 +343,38 @@ class RemoveAgentAssetTest(unittest.TestCase):
         )
         self.assertEqual({}, self.manifest()["steps"])
 
+    def test_hcom_removal_uninstalls_the_uv_tool_before_the_kept_wheel(self) -> None:
+        # The Bot's 4303212235: uv owns hcom's tool environment, receipt and entry point, so the removal runs
+        # `uv tool uninstall hcom`, then deletes the wheel the updater kept for uv's receipt; without uv it removes nothing.
+        log = self.temp_dir / "uv.log"
+        hcom = self.home / ".local/bin/hcom"
+        wheel = self.home / ".local/share/agent-assets/hcom/hcom-0.7.30-py3-none-any.whl"
+        for path in (hcom, wheel):
+            path.parent.mkdir(parents=True, exist_ok=True)
+            path.write_text("fixture\n")
+        step = self.step("installer", [hcom, wheel], ["uv tool install --force <verified-hcom-wheel>"])
+
+        self.write_manifest({"update_hcom": step})
+        result = self.run_remover("update_hcom", "--yes")
+        self.assertEqual(1, result.returncode)
+        self.assertIn("uv is not installed", result.stderr)
+        self.assertTrue(wheel.exists())
+        self.assertIn("update_hcom", self.manifest()["steps"])
+
+        self.executable("uv", 'printf "uv %s\\n" "$*" >> "$TEST_LOG"\nrm -f "$HOME/.local/bin/hcom"\n')
+        dry = self.run_remover("update_hcom", env={"TEST_LOG": str(log)})
+        self.assertEqual(0, dry.returncode, dry.stderr)
+        self.assertIn("DRY-RUN: uv tool uninstall hcom", dry.stdout)
+        self.assertFalse(log.exists())
+        self.assertTrue(wheel.exists())
+
+        result = self.run_remover("update_hcom", "--yes", env={"TEST_LOG": str(log)})
+        self.assertEqual(0, result.returncode, result.stderr)
+        self.assertEqual("uv tool uninstall hcom\n", log.read_text())
+        self.assertFalse(wheel.exists())
+        self.assertFalse(hcom.exists())
+        self.assertEqual({}, self.manifest()["steps"])
+
     def executable(self, name: str, body: str) -> None:
         path = self.bin_dir / name
         path.write_text("#!/usr/bin/env bash\n" + textwrap.dedent(body))
diff --git a/tests/unit/test_update_agent_assets.py b/tests/unit/test_update_agent_assets.py
index 29fc43d2..321d325a 100644
--- a/tests/unit/test_update_agent_assets.py
+++ b/tests/unit/test_update_agent_assets.py
@@ -34,7 +34,22 @@ else:
     entry["sha256"] = hashlib.sha256(artifact.read_bytes()).hexdigest()
     tool = "omp" if name == "npm" else "hcom"
     target = Path(os.environ["HOME"]) / ".local/bin" / tool
-    target.write_text("#!/usr/bin/env bash\nprintf '%s\\n' " + shlex.quote(tool + ("/" if tool == "omp" else " ") + os.environ["FIXTURE_VERSION"]) + "\n")
+    script = "#!/usr/bin/env bash\nprintf '%s\\n' " + shlex.quote(tool + ("/" if tool == "omp" else " ") + os.environ["FIXTURE_VERSION"]) + "\n"
+    if name == "npm":
+        # As npm does: it links its bin entry into the package and refuses an entry it does not own (EEXIST).
+        with open(os.environ["CALLS"], "a") as log:
+            log.write(json.dumps(entry) + "\n")
+        link = "../lib/node_modules/@oh-my-pi/pi-coding-agent/omp.js"
+        if (target.exists() or target.is_symlink()) and not (target.is_symlink() and os.readlink(target) == link):
+            sys.exit("npm error code EEXIST: " + str(target))
+        package = target.parent.parent / "lib/node_modules/@oh-my-pi/pi-coding-agent"
+        package.mkdir(parents=True, exist_ok=True)
+        (package / "omp.js").write_text(script)
+        (package / "omp.js").chmod(0o755)
+        target.unlink(missing_ok=True)
+        target.symlink_to(link)
+        sys.exit(0)
+    target.write_text(script)
     target.chmod(0o755)
 with open(os.environ["CALLS"], "a") as log:
     log.write(json.dumps(entry) + "\n")
@@ -263,6 +278,100 @@ class UpdateAgentAssetsTest(unittest.TestCase):
             self.assertIn("hcom 0.7.30 is already installed", skipped.stdout)
             self.assertEqual("", log.read_text())
 
+    def test_update_hcom_drops_the_kept_wheel_when_the_install_fails(self):
+        # The Bot's 4303338055: when `uv tool install` fails after the wheel moved into place, the wheel goes, so the
+        # next run retries instead of skipping on it.
+        with tempfile.TemporaryDirectory() as directory:
+            home = Path(directory)
+            hcom = home / ".local/bin/hcom"
+            hcom.parent.mkdir(parents=True)
+            hcom.write_text("#!/bin/sh\nprintf 'hcom 0.7.30\\n'\n")
+            hcom.chmod(0o755)
+            payload = "reproduced wheel bytes; no real package\n"
+            log = home / "calls"
+            wheel = home / ".local/share/agent-assets/hcom/hcom-0.7.30-py3-none-any.whl"
+            stubs = (
+                "HCOM_PIN_VERSION=0.7.30; HCOM_LINUX_AMD64_URL=https://fixture.invalid/hcom-0.7.30-py3-none-any.whl; "
+                f"HCOM_LINUX_AMD64_SHA256={hashlib.sha256(payload.encode()).hexdigest()}; "
+                "has_command() { return 0; }; manifest_record() { :; }; "
+                'uname() { if [ "$1" = -s ]; then echo Linux; else echo x86_64; fi; }; '
+                'curl() { printf %s "$PAYLOAD" > "${@: -1}"; echo curl >> "$CALLS"; }; '
+                'uv() { echo "uv $*" >> "$CALLS"; return "$UV_RC"; }; '
+            )
+
+            def update(uv_rc):
+                return subprocess.run(
+                    ["bash", "-c", 'source "$1"; ' + stubs + "update_hcom", "bash", str(UPDATER)],
+                    env=os.environ | {"HOME": directory, "PAYLOAD": payload, "CALLS": str(log), "UV_RC": uv_rc},
+                    capture_output=True,
+                    text=True,
+                    timeout=30,
+                    check=False,
+                )
+
+            failed = update("1")
+            self.assertNotEqual(0, failed.returncode)
+            self.assertFalse(wheel.exists())
+            log.write_text("")
+            retried = update("0")
+            self.assertEqual(0, retried.returncode, retried.stdout + retried.stderr)
+            self.assertEqual(["curl", f"uv tool install --force {wheel}"], log.read_text().splitlines())
+            self.assertTrue(wheel.exists())
+
+    def test_update_omp_moves_a_non_npm_entry_aside_and_restores_it_on_failure(self):
+        # local:fbbc6d9:1: npm refuses a bin entry it does not own, so a standalone omp, an external link or a dangling
+        # one moves aside for the install, and comes back when the install does not end at the pin.
+        script = 'source "$1"; OMP_PIN_VERSION=18.11.3; OMP_TARBALL_SHA256="$2"; manifest_record() { :; }; update_omp'
+
+        def update(home, digest, version):
+            return subprocess.run(
+                ["bash", "-c", script, "bash", str(UPDATER), digest],
+                env=os.environ
+                | {
+                    "HOME": str(home),
+                    "PATH": f"{home / '.local/bin'}{os.pathsep}{os.environ['PATH']}",
+                    "CALLS": str(home / "calls"),
+                    "PAYLOAD": str(home / "payload"),
+                    "FIXTURE_VERSION": version,
+                },
+                capture_output=True,
+                text=True,
+                timeout=30,
+                check=False,
+            )
+
+        for kind in ("file", "link", "dangling"):
+            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as directory:
+                home = Path(directory)
+                binary = home / ".local/bin"
+                binary.mkdir(parents=True)
+                for name in ("curl", "npm"):
+                    (binary / name).write_text(STUB.replace("@PYTHON@", sys.executable))
+                    (binary / name).chmod(0o755)
+                entry, outside = binary / "omp", home / "elsewhere/omp"
+                if kind == "file":
+                    entry.write_text("#!/bin/sh\necho omp/1.0.0\n")
+                    entry.chmod(0o755)
+                else:
+                    if kind == "link":
+                        outside.parent.mkdir()
+                        outside.write_text("#!/bin/sh\necho omp/1.0.0\n")
+                        outside.chmod(0o755)
+                    entry.symlink_to(outside)
+                before = os.readlink(entry) if entry.is_symlink() else entry.read_text()
+                (home / "payload").write_bytes(b"reproduced artifact bytes; no real package\n")
+                digest = hashlib.sha256((home / "payload").read_bytes()).hexdigest()
+
+                drifted = update(home, digest, "0.0.1")
+                self.assertNotEqual(0, drifted.returncode)
+                self.assertIn("version mismatch", drifted.stderr)
+                self.assertEqual(before, os.readlink(entry) if entry.is_symlink() else entry.read_text())
+                installed = update(home, digest, "18.11.3")
+                self.assertEqual(0, installed.returncode, installed.stdout + installed.stderr)
+                self.assertIn("moved the existing non-npm", installed.stdout)
+                self.assertEqual("../lib/node_modules/@oh-my-pi/pi-coding-agent/omp.js", os.readlink(entry))
+                self.assertEqual(kind == "link", outside.exists())  # the external target itself is left alone
+
     def test_updates_use_managed_binaries_when_path_is_shadowed(self):
         for tool in ("omp", "hcom"):
             for shadow_version in ("pin", "0.0.0"):
(exit 0)
```

## 3. The row tests against 2b91aef9's two scripts

```console
$ PATH="$TMPDIR/t129h/shim:$PATH" uv run python -m unittest <the four row tests> -v   # this branch's tests against 2b91aef9's two scripts
test_hcom_removal_uninstalls_the_uv_tool_before_the_kept_wheel ... FAIL
test_update_hcom_drops_the_kept_wheel_when_the_install_fails ... FAIL
test_update_omp_moves_a_non_npm_entry_aside_and_restores_it_on_failure ... 
  test_update_omp_moves_a_non_npm_entry_aside_and_restores_it_on_failure (kind='file') ... FAIL
  test_update_omp_moves_a_non_npm_entry_aside_and_restores_it_on_failure (kind='link') ... FAIL
  test_update_omp_moves_a_non_npm_entry_aside_and_restores_it_on_failure (kind='dangling') ... FAIL
test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin ... FAIL
FAIL: test_hcom_removal_uninstalls_the_uv_tool_before_the_kept_wheel
AssertionError: 'uv is not installed' not found in 'ERROR: refusing path outside allowed asset roots: /private/tmp/claude-501/remove-agent-asset-test-hj6c_l91/home/.local/bin/hcom\n'
FAIL: test_update_hcom_drops_the_kept_wheel_when_the_install_fails
AssertionError: True is not false
FAIL: test_update_omp_moves_a_non_npm_entry_aside_and_restores_it_on_failure (kind='file')
AssertionError: 'version mismatch' not found in 'npm error code EEXIST: /tmp/claude-501/tmp36ae4efz/.local/bin/omp\n'
FAIL: test_update_omp_moves_a_non_npm_entry_aside_and_restores_it_on_failure (kind='link')
AssertionError: 'version mismatch' not found in 'npm error code EEXIST: /tmp/claude-501/tmpf8yip67p/.local/bin/omp\n'
FAIL: test_update_omp_moves_a_non_npm_entry_aside_and_restores_it_on_failure (kind='dangling')
AssertionError: 'version mismatch' not found in 'npm error code EEXIST: /tmp/claude-501/tmpyyjwi0r0/.local/bin/omp\n'
FAIL: test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin
AssertionError: 0 != 1 : 
Ran 4 tests in 1.290s
FAILED (failures=6)
(exit 1)
```

## 4. One mutant per part of the three fixes

```python
"""The a02 rows: one mutant per part of each fix, each run against the row tests."""
import subprocess
from pathlib import Path
RA, UA = Path("home/dot_local/bin/common/executable_remove-agent-asset"), Path("scripts/update-agent-assets.sh")
fixed = {RA: RA.read_text(), UA: UA.read_text()}
P1, P2 = "tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.", "tests.unit.test_remove_agent_asset.RemoveAgentAssetTest."
tests = [P2 + "test_hcom_removal_uninstalls_the_uv_tool_before_the_kept_wheel", P1 + "test_update_hcom_drops_the_kept_wheel_when_the_install_fails",
         P1 + "test_update_omp_moves_a_non_npm_entry_aside_and_restores_it_on_failure"]
def mutate(path, old, new):
    assert fixed[path].count(old) == 1, old
    return path, fixed[path].replace(old, new)
variants = [
    ("remove: no uv tool uninstall", *mutate(RA, "    run_operation uv tool uninstall hcom\n", "")),
    ("remove: the agent-assets root not safe", *mutate(RA, ' \\\n        "${HOME}/.local/share/agent-assets"; do', "; do")),
    ("remove: no uv check", *mutate(RA, "    has_command uv || {", "    true || {")),
    ("hcom: the wheel stays after a failed install", *mutate(UA, '        rm -f "${wheel}"\n        return 1\n    }', "        return 1\n    }")),
    ("omp: no restore", *mutate(UA, '        [ -z "${aside}" ] || { rm -f "${entry}" && mv "${aside}" "${entry}"; }\n', "")),
    ("omp: a dangling link is not an entry", *mutate(UA, 'if { [ -e "${entry}" ] || [ -L "${entry}" ]; } &&', 'if [ -e "${entry}" ] &&')),
]
try:
    for name, path, body in variants:
        path.write_text(body)
        r = subprocess.run(["uv", "run", "python", "-m", "unittest", *tests], capture_output=True, text=True)
        tail = [x for x in r.stderr.splitlines() if x.startswith(("OK", "FAILED"))]
        print(f"{name}: rc={r.returncode} {' | '.join(tail)}")
        path.write_text(fixed[path])
finally:
    for path, text in fixed.items():
        path.write_text(text)
print("restored byte-identical:", all(p.read_text() == t for p, t in fixed.items()))
```

```console
$ PATH="$TMPDIR/t129h/shim:$PATH" uv run --offline --no-project python -I mutants.py   # from the worktree root; the script is pasted in the record
remove: no uv tool uninstall: rc=1 FAILED (failures=1)
remove: the agent-assets root not safe: rc=1 FAILED (failures=1)
remove: no uv check: rc=1 FAILED (failures=1)
hcom: the wheel stays after a failed install: rc=1 FAILED (failures=1)
omp: no restore: rc=1 FAILED (failures=3)
omp: a dangling link is not an entry: rc=1 FAILED (failures=1)
restored byte-identical: True
(exit 0)
```

## 5. The Check: both modules

```console
$ PATH="$TMPDIR/t129h/shim:$PATH" uv run python -m unittest tests/unit/test_remove_agent_asset.py tests/unit/test_update_agent_assets.py -v
test_all_paths_are_preflighted_before_any_deletion (tests.unit.test_remove_agent_asset.RemoveAgentAssetTest.test_all_paths_are_preflighted_before_any_deletion) ... ok
test_brew_refuses_ambiguous_formula (tests.unit.test_remove_agent_asset.RemoveAgentAssetTest.test_brew_refuses_ambiguous_formula) ... ok
test_brew_uses_uninstall_for_unambiguous_formula (tests.unit.test_remove_agent_asset.RemoveAgentAssetTest.test_brew_uses_uninstall_for_unambiguous_formula) ... ok
test_crit_plugin_falls_back_to_data_path_but_not_config (tests.unit.test_remove_agent_asset.RemoveAgentAssetTest.test_crit_plugin_falls_back_to_data_path_but_not_config) ... ok
test_default_and_explicit_dry_run_print_without_mutating (tests.unit.test_remove_agent_asset.RemoveAgentAssetTest.test_default_and_explicit_dry_run_print_without_mutating) ... ok
test_hcom_removal_uninstalls_the_uv_tool_before_the_kept_wheel (tests.unit.test_remove_agent_asset.RemoveAgentAssetTest.test_hcom_removal_uninstalls_the_uv_tool_before_the_kept_wheel) ... ok
test_integration_uses_verified_herdr_uninstall (tests.unit.test_remove_agent_asset.RemoveAgentAssetTest.test_integration_uses_verified_herdr_uninstall) ... ok
test_invalid_manifest_is_rejected (tests.unit.test_remove_agent_asset.RemoveAgentAssetTest.test_invalid_manifest_is_rejected) ... ok
test_parameterized_step_removal_preserves_sibling_identity (tests.unit.test_remove_agent_asset.RemoveAgentAssetTest.test_parameterized_step_removal_preserves_sibling_identity) ... ok
test_plugin_uses_verified_claude_uninstall (tests.unit.test_remove_agent_asset.RemoveAgentAssetTest.test_plugin_uses_verified_claude_uninstall) ... ok
test_plugin_uses_verified_codex_remove (tests.unit.test_remove_agent_asset.RemoveAgentAssetTest.test_plugin_uses_verified_codex_remove) ... ok
test_recorded_symlink_is_removed_without_following_target (tests.unit.test_remove_agent_asset.RemoveAgentAssetTest.test_recorded_symlink_is_removed_without_following_target) ... ok
test_tampered_manifest_outside_safe_roots_is_refused (tests.unit.test_remove_agent_asset.RemoveAgentAssetTest.test_tampered_manifest_outside_safe_roots_is_refused) ... ok
test_unknown_step_lists_known_steps_without_guessing (tests.unit.test_remove_agent_asset.RemoveAgentAssetTest.test_unknown_step_lists_known_steps_without_guessing) ... ok
test_yes_removes_only_recorded_path_and_preserves_other_steps (tests.unit.test_remove_agent_asset.RemoveAgentAssetTest.test_yes_removes_only_recorded_path_and_preserves_other_steps) ... ok
test_omp_version_check_accepts_the_branded_omp_slash_version_form (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_omp_version_check_accepts_the_branded_omp_slash_version_form) ... ok
test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin) ... ok
test_update_hcom_drops_the_kept_wheel_when_the_install_fails (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_hcom_drops_the_kept_wheel_when_the_install_fails) ... ok
test_update_hcom_keeps_the_wheel_uv_records_as_its_source (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_hcom_keeps_the_wheel_uv_records_as_its_source) ... ok
test_update_hcom_reinstalls_a_pinned_install_without_its_retained_wheel (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_hcom_reinstalls_a_pinned_install_without_its_retained_wheel) ... ok
test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin) ... ok
test_update_omp_moves_a_non_npm_entry_aside_and_restores_it_on_failure (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_omp_moves_a_non_npm_entry_aside_and_restores_it_on_failure) ... ok
test_updates_use_managed_binaries_when_path_is_shadowed (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_updates_use_managed_binaries_when_path_is_shadowed) ... ok

----------------------------------------------------------------------
Ran 23 tests in 16.952s

OK
(exit 0)
```

## 6. ShellCheck (with -x), shfmt, Ruff and the caps

```console
$ shellcheck -x scripts/update-agent-assets.sh home/dot_local/bin/common/executable_remove-agent-asset
(exit 0)
$ shfmt -i 4 -sr -d scripts/update-agent-assets.sh home/dot_local/bin/common/executable_remove-agent-asset
(exit 0)
$ ruff format --config ruff.toml --check tests/unit/test_update_agent_assets.py tests/unit/test_remove_agent_asset.py
2 files already formatted
(exit 0)
$ ruff check --config ruff.toml --output-format concise tests/unit/test_update_agent_assets.py tests/unit/test_remove_agent_asset.py   # the two test_remove_agent_asset.py findings are on 2b91aef9 too
tests/unit/test_remove_agent_asset.py:1:1: EXE001 Shebang is present but file is not executable
tests/unit/test_remove_agent_asset.py:4:1: I001 [*] Import block is un-sorted or un-formatted
Found 2 errors.
[*] 1 fixable with `--fix`.
(exit 1)
$ git diff --numstat 2b91aef95161bf1e38755a2b233094b30dca80c1
26	2	home/dot_local/bin/common/executable_remove-agent-asset
23	5	scripts/update-agent-assets.sh
32	0	tests/unit/test_remove_agent_asset.py
110	1	tests/unit/test_update_agent_assets.py
(exit 0)
```

## 7. The repository validator

```console
$ make validate-agent-assets > "$TMPDIR/a02/06-validate.txt" 2>&1; echo "make rc=$?"   # 334 s
make rc=0
$ grep -v "^WARN: regime-boundary:" "$TMPDIR/a02/06-validate.txt"
uv run --offline --with pyyaml scripts/validate-agent-assets.py
agent asset validation ok
(exit 0)
```
