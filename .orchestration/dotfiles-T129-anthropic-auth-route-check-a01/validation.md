---
task_id: dotfiles-T129-anthropic-auth-route-check-a01
seat: claude-standard-dot-a007
---

# Validation: dotfiles-T129-anthropic-auth-route-check-a01

Every command ran from the worktree `.claude/worktrees/worker-c` on the branch `tools/anthropic-auth-route-check`, inside the sandbox, before the commit; `MAIN` names the main checkout and `T` the task id. The output is verbatim, with the home directory replaced by `~` and the main checkout by `$MAIN`; each block ends with the exit status of the command shown (a pipeline's is its last command's).

## 1. Task file and task copy (amendment 1)

The task copy is the amended file (`task_sha256=6722f83d…`, amendment 1 of 2026-10-17T11:11:16Z, which answered this seat's question 1); the first dispatch was `5c00408f…`.

```console
$ shasum -a 256 "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md"; cmp "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md" && echo byte-identical
6722f83d7327378040bd35b0a7c8d72dbfd7e1d5c93c99a437a1473fab0aa07f  $MAIN/.orchestration/tasks/dotfiles-T129-anthropic-auth-route-check-a01.md
6722f83d7327378040bd35b0a7c8d72dbfd7e1d5c93c99a437a1473fab0aa07f  .orchestration/dotfiles-T129-anthropic-auth-route-check-a01/task.md
byte-identical
(exit 0)
$ UV_OFFLINE=1 uv run --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py --root "$PWD" "$MAIN/.orchestration/tasks/$T.md"
dotfiles-T129-anthropic-auth-route-check-a01.md: OK
(exit 0)
```

## 2. Branch and the premises

```console
$ git rev-parse origin/main HEAD; git log --oneline -1 origin/main
35ab0e95a7fe27c501db3478d4f37e69a514d532
35ab0e95a7fe27c501db3478d4f37e69a514d532
35ab0e95 chore(orchestration): boundary (18) records of 2026-10-17 (plan 023 filed, the T129 task texts and their dispatch, corrections C-61, the decisions and corrections inventories) (#385)
(exit 0)
$ git grep -lE "ANTHROPIC_(OAUTH_TOKEN|API_KEY)" origin/main -- home install | wc -l | tr -d " "   # premise 1
0
(exit 0)
$ a=$(git show origin/main:scripts/validate-agent-assets.py | /usr/bin/grep -c "^def validate_no_obvious_secrets"); b=$(git show origin/main:scripts/validate-agent-assets.py | /usr/bin/grep -c "ANTHROPIC" || true); echo "$a $b"   # premise 2
1 0
(exit 0)
$ git show origin/main:.github/workflows/agent-assets.yml | /usr/bin/grep -c "scripts/validate-agent-assets.py"   # premise 3
1
(exit 0)
$ git show origin/main:tests/unit/test_validate_agent_assets.py | /usr/bin/grep -c "def test_secret_scan"   # premise 4
10
(exit 0)
$ git ls-files -s -- home install | awk '$1=="120000"' | wc -l | tr -d " "   # tracked symlinks under the applied trees today
0
(exit 0)
```

## 3. R2: the regex first written in the task against the branch's

Question 1 (PONG 11:08Z): in the first regex the optional quote group and the whitespace before the negative lookahead can match empty, so the lookahead is tested at the quote or the space and four lines item 2 passes are refused. Amendment 1 states R2 as its intent and leaves the regex to the worker. The branch regex keeps the whitespace and the optional quote inside the lookahead. The two JSON-key lines are out of scope: question 2 (the name in double quotes before the colon) was not taken into the amendment, so R2 does not reach them. The repository masker shows rows 1 and 9 as `ANTHROPIC_<redacted:secret-pattern>`: a double-quoted non-empty value after the name matches SECRET_PATTERN; row 1 is the quoted literal and row 9 the quoted `${…}` reference.

```python
"""R2 as first written in the task against the branch's ANTHROPIC_API_KEY_LITERAL, on item 2's lines and five more."""

import importlib.util
import re

spec = importlib.util.spec_from_file_location(
    "validate_agent_assets", "scripts/validate-agent-assets.py"
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
branch = module.ANTHROPIC_API_KEY_LITERAL
task = re.compile(r"""ANTHROPIC_API_KEY\s*[:=]\s*(["']?)(?!\$|\{\{|\1\s*$)""")
K = "ANTHROPIC_API_" + "KEY"
cases = [  # (line, expected): True refuses, False passes, None is out of scope (the JSON key form, question 2)
    (f'{K}="literal-value"', True),
    (f"{K}: literal", True),
    (f"{K}=literal", True),
    (f"{K}=${K}", False),
    (f"apiKey: {K}", False),
    (f"env: {K}", False),
    (f"{K}=", False),
    (f'{K}=""', False),
    (f'{K}="${{{K}}}"', False),
    (f"{K}= ${K}", False),
    (f"{K}: {{{{ .anthropic }}}}", False),
    (f"export {K}=$(op read x)", False),
    (f'"{K}": "literal-value",', None),
    (f'"{K}": "${{{K}}}",', None),
]
for line, expected in cases:
    t, b = bool(task.search(line)), bool(branch.search(line))
    want = {True: "refuse", False: "pass  ", None: "n/a   "}[expected]
    marks = (
        ""
        if expected is None
        else ("" if b == expected else "BRANCH-WRONG ")
        + ("" if t == expected else "TASK-WRONG")
    )
    print(
        f"want={want} task={'refuse' if t else 'pass  '} branch={'refuse' if b else 'pass  '} {marks:<24} {line}"
    )
```

```console
$ uv run --offline --no-project python -I r2table.py   # from the worktree root; the script is pasted above
want=refuse task=refuse branch=refuse                          ANTHROPIC_<redacted:secret-pattern>
want=refuse task=refuse branch=refuse                          ANTHROPIC_API_KEY: literal
want=refuse task=refuse branch=refuse                          ANTHROPIC_API_KEY=literal
want=pass   task=pass   branch=pass                            ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY
want=pass   task=pass   branch=pass                            apiKey: ANTHROPIC_API_KEY
want=pass   task=pass   branch=pass                            env: ANTHROPIC_API_KEY
want=pass   task=pass   branch=pass                            ANTHROPIC_API_KEY=
want=pass   task=refuse branch=pass   TASK-WRONG               ANTHROPIC_API_KEY=""
want=pass   task=refuse branch=pass   TASK-WRONG               ANTHROPIC_<redacted:secret-pattern>
want=pass   task=refuse branch=pass   TASK-WRONG               ANTHROPIC_API_KEY= $ANTHROPIC_API_KEY
want=pass   task=refuse branch=pass   TASK-WRONG               ANTHROPIC_API_KEY: {{ .anthropic }}
want=pass   task=pass   branch=pass                            export ANTHROPIC_API_KEY=$(op read x)
want=n/a    task=pass   branch=pass                            "ANTHROPIC_API_KEY": "literal-value",
want=n/a    task=pass   branch=pass                            "ANTHROPIC_API_KEY": "${ANTHROPIC_API_KEY}",
(exit 0)
```

## 4. The diff

```console
$ git diff --stat
 scripts/validate-agent-assets.py         | 30 ++++++++++++++++
 tests/unit/test_validate_agent_assets.py | 59 ++++++++++++++++++++++++++++++++
 2 files changed, 89 insertions(+)
(exit 0)
$ git diff -- scripts/validate-agent-assets.py tests/unit/test_validate_agent_assets.py
diff --git a/scripts/validate-agent-assets.py b/scripts/validate-agent-assets.py
index 9547e62b..e282a3b6 100644
--- a/scripts/validate-agent-assets.py
+++ b/scripts/validate-agent-assets.py
@@ -1572,6 +1572,35 @@ def validate_no_obvious_secrets() -> None:
             )
 
 
+# R2: an assignment whose value is not a `$` reference, a `{{` template or empty. The whitespace and the optional
+# quote sit inside the lookahead, so neither can match empty in front of a reference and let it through as a literal.
+ANTHROPIC_API_KEY_LITERAL = re.compile(r"""ANTHROPIC_API_KEY\s*[:=](?!\s*["']?(?:\$|\{\{)|\s*(?:""|'')?\s*$)""")
+
+
+def validate_anthropic_auth_route() -> None:
+    """Plan 023 PR D: the applied files reach Anthropic through ANTHROPIC_API_KEY from the environment only."""
+    listed = subprocess.run(
+        ["git", "-C", str(ROOT), "ls-files", "-z", "--", "home", "install"], capture_output=True, check=False
+    )
+    if listed.returncode != 0:
+        fail(f"git ls-files failed, so the Anthropic auth route check cannot run: {os.fsdecode(listed.stderr).strip()}")
+    for name in filter(None, listed.stdout.split(b"\0")):
+        path = ROOT / os.fsdecode(name)
+        # A tracked symlink is not followed: on a PR checkout it could point at a device and hang the run.
+        if path.is_symlink() or not path.is_file():
+            continue
+        for number, line in enumerate(path.read_bytes().decode("utf-8", errors="replace").splitlines(), 1):
+            # The file, the line number and the rule only: the line itself may hold a real key, and CI logs are public.
+            if "ANTHROPIC_OAUTH_TOKEN" in line:
+                fail(
+                    f"{os.fsdecode(name)}:{number}: R1: names ANTHROPIC_OAUTH_TOKEN; Anthropic is reached by API key only"
+                )
+            if ANTHROPIC_API_KEY_LITERAL.search(line):
+                fail(
+                    f"{os.fsdecode(name)}:{number}: R2: assigns ANTHROPIC_API_KEY a literal; reference the environment"
+                )
+
+
 def validate_compactiondb_project_copy() -> None:
     """The project's CompactionDB runtime and hook scripts must be byte-identical to the vendor tree."""
     vendor = ROOT / "vendor/compactiondb/.claude"
@@ -1647,6 +1676,7 @@ def main() -> None:
     validate_git_config()
     validate_no_removed_claude_skill()
     validate_no_obvious_secrets()
+    validate_anthropic_auth_route()
     report_regime_boundary()
     print("agent asset validation ok")
 
diff --git a/tests/unit/test_validate_agent_assets.py b/tests/unit/test_validate_agent_assets.py
index d74630fe..7c11274f 100644
--- a/tests/unit/test_validate_agent_assets.py
+++ b/tests/unit/test_validate_agent_assets.py
@@ -1419,6 +1419,65 @@ class ValidateAgentAssetsTest(unittest.TestCase):
         with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
             self.module.validate_no_obvious_secrets()
 
+    def test_anthropic_auth_route_refuses_an_oauth_token_in_applied_files_and_a_literal_api_key_assignment(
+        self,
+    ) -> None:
+        # Plan 023 PR D. The names are split so this module passes the committed-secret scan it sits beside.
+        key, oauth = "ANTHROPIC_API_" + "KEY", "ANTHROPIC_OAUTH_" + "TOKEN"
+        files = ("home/dot_config/fixture.sh", "install/fixture.sh", "scripts/fixture.sh")
+        for rel in files:
+            self.write_text_file(rel, "")
+        subprocess.run(["git", "init", "-q", str(self.temp_dir)], check=True)
+        subprocess.run(["git", "-C", str(self.temp_dir), "add", *files], check=True)
+
+        def check(rel: str, line: str) -> tuple[bool, str]:
+            self.write_text_file(rel, f"# fixture\n{line}\n")
+            stderr, refused = io.StringIO(), False
+            with contextlib.redirect_stderr(stderr):
+                try:
+                    self.module.validate_anthropic_auth_route()
+                except SystemExit:
+                    refused = True
+            self.write_text_file(rel, "")
+            return refused, stderr.getvalue()
+
+        home, install, scripts = files
+        for rel, line, rule in (
+            (home, f"export {oauth}=x", "R1"),
+            (install, f"export {oauth}=x", "R1"),
+            (home, f'{key}="literal-value"', "R2"),
+            (home, f"{key}: literal", "R2"),
+            (install, f"{key}=literal", "R2"),
+        ):
+            with self.subTest(rel=rel, line=line):
+                refused, stderr = check(rel, line)
+                self.assertTrue(refused)
+                self.assertIn(f"ERROR: {rel}:2: {rule}:", stderr)
+                self.assertNotIn(line, stderr)  # the line may hold a real key; the log names only file, line and rule
+        for rel, line in (
+            (home, f"{key}=${key}"),
+            (home, f"apiKey: {key}"),
+            (home, f"env: {key}"),
+            (home, f"{key}="),
+            (home, f'{key}=""'),
+            (home, f'{key}="${{{key}}}"'),
+            (home, f"{key}= ${key}"),
+            (home, f"{key}: {{{{ .anthropic }}}}"),
+            (scripts, f"export {oauth}=x"),
+        ):
+            with self.subTest(rel=rel, line=line):
+                self.assertEqual((False, ""), check(rel, line))
+        # A tracked symlink is not followed, and a failed listing refuses instead of passing on an empty list.
+        self.write_text_file("outside.txt", f"export {oauth}=x\n")
+        (self.temp_dir / "home/dot_config/link").symlink_to("../../outside.txt")
+        subprocess.run(["git", "-C", str(self.temp_dir), "add", "home/dot_config/link"], check=True)
+        self.assertEqual((False, ""), check(scripts, ""))
+        failed = subprocess.CompletedProcess([], 128, b"", b"fatal: not a git repository")
+        with mock.patch.object(self.module.subprocess, "run", return_value=failed):
+            refused, stderr = check(scripts, "")
+        self.assertTrue(refused)
+        self.assertIn("git ls-files failed", stderr)
+
     def write_manifest(self, hook_command: str) -> None:
         path = self.temp_dir / "home/dot_agents/agent-config.yaml"
         path.parent.mkdir(parents=True, exist_ok=True)
(exit 0)
```

## 5. The new test before the change, the first regex, and one mutant per property

Each variant is written over `scripts/validate-agent-assets.py`, the new test runs, and the branch file is written back and compared byte for byte (`restored byte-identical: True`). On origin/main's validator the function does not exist, so every subtest errors. With the first regex the four lines of section 3 fail. Each mutant fails at least one subtest: R1, R2, the symlink skip, the fail-closed listing and the rule that the line never reaches the log are each tested.

```python
"""Run the new test against origin/main's validator, the task's literal R2 regex, and one mutant per property.

Each variant is written over scripts/validate-agent-assets.py, the test runs, and the fixed file is written back
and compared byte for byte. Mutants are literal string replacements asserted to match once.
"""

import re
import subprocess
from pathlib import Path

script = Path("scripts/validate-agent-assets.py")
fixed = script.read_text()
main = subprocess.run(
    ["git", "show", "origin/main:" + str(script)],
    capture_output=True,
    text=True,
    check=True,
).stdout
test = (
    "tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest."
    "test_anthropic_auth_route_refuses_an_oauth_token_in_applied_files_and_a_literal_api_key_assignment"
)
MINE = r'''re.compile(r"""ANTHROPIC_API_KEY\s*[:=](?!\s*["']?(?:\$|\{\{)|\s*(?:""|'')?\s*$)""")'''
TASK = r'''re.compile(r"""ANTHROPIC_API_KEY\s*[:=]\s*(["']?)(?!\$|\{\{|\1\s*$)""")'''


def mutate(old, new):
    assert fixed.count(old) == 1, old
    return fixed.replace(old, new)


variants = [
    ("origin/main's validator (no function yet)", main),
    ("the task's R2 regex as written", mutate(MINE, TASK)),
    ("mutant: R1 removed", mutate('if "ANTHROPIC_OAUTH_TOKEN" in line:', "if False:")),
    (
        "mutant: R2 removed",
        mutate("if ANTHROPIC_API_KEY_LITERAL.search(line):", "if False:"),
    ),
    (
        "mutant: symlinks followed",
        mutate("if path.is_symlink() or not path.is_file():", "if not path.is_file():"),
    ),
    (
        "mutant: a failed listing passes",
        mutate("if listed.returncode != 0:", "if False:"),
    ),
    (
        "mutant: the R2 message quotes the line",
        mutate(
            'a literal; reference the environment"',
            'a literal; reference the environment: {line}"',
        ),
    ),
]
try:
    for name, body in variants:
        script.write_text(body)
        result = subprocess.run(
            ["uv", "run", "python", "-m", "unittest", test],
            capture_output=True,
            text=True,
            check=False,
        )
        lines = result.stderr.splitlines()
        subtests = sorted(
            {m.group(1) for m in (re.search(r"\((rel=.*)\)$", x) for x in lines) if m}
        )
        tail = [
            x
            for x in lines
            if x.startswith(("AssertionError", "AttributeError", "OK", "FAILED"))
        ]
        print(f"{name}: rc={result.returncode} {' | '.join(tail)}")
        for subtest in subtests:
            print(f"    failing subtest: {subtest}")
finally:
    script.write_text(fixed)
print("restored byte-identical:", script.read_text() == fixed)
```

```console
$ uv run --offline --no-project python -I t129_mutants.py   # from the worktree root; the script is pasted in this section
origin/main's validator (no function yet): rc=1 AttributeError: module 'validate_agent_assets' has no attribute 'validate_anthropic_auth_route' | AttributeError: module 'validate_agent_assets' has no attribute 'validate_anthropic_auth_route' | AttributeError: module 'validate_agent_assets' has no attribute 'validate_anthropic_auth_route' | AttributeError: module 'validate_agent_assets' has no attribute 'validate_anthropic_auth_route' | AttributeError: module 'validate_agent_assets' has no attribute 'validate_anthropic_auth_route' | AttributeError: module 'validate_agent_assets' has no attribute 'validate_anthropic_auth_route' | AttributeError: module 'validate_agent_assets' has no attribute 'validate_anthropic_auth_route' | AttributeError: module 'validate_agent_assets' has no attribute 'validate_anthropic_auth_route' | AttributeError: module 'validate_agent_assets' has no attribute 'validate_anthropic_auth_route' | AttributeError: module 'validate_agent_assets' has no attribute 'validate_anthropic_auth_route' | AttributeError: module 'validate_agent_assets' has no attribute 'validate_anthropic_auth_route' | AttributeError: module 'validate_agent_assets' has no attribute 'validate_anthropic_auth_route' | AttributeError: module 'validate_agent_assets' has no attribute 'validate_anthropic_auth_route' | AttributeError: module 'validate_agent_assets' has no attribute 'validate_anthropic_auth_route' | AttributeError: module 'validate_agent_assets' has no attribute 'validate_anthropic_auth_route' | FAILED (errors=15)
    failing subtest: rel='home/dot_config/fixture.sh', line='ANTHROPIC_API_KEY: literal'
    failing subtest: rel='home/dot_config/fixture.sh', line='ANTHROPIC_API_KEY: {{ .anthropic }}'
    failing subtest: rel='home/dot_config/fixture.sh', line='ANTHROPIC_API_KEY= $ANTHROPIC_API_KEY'
    failing subtest: rel='home/dot_config/fixture.sh', line='ANTHROPIC_API_KEY=""'
    failing subtest: rel='home/dot_config/fixture.sh', line='ANTHROPIC_<redacted:secret-pattern>'
    failing subtest: rel='home/dot_config/fixture.sh', line='ANTHROPIC_<redacted:secret-pattern>'
    failing subtest: rel='home/dot_config/fixture.sh', line='ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY'
    failing subtest: rel='home/dot_config/fixture.sh', line='ANTHROPIC_<redacted:secret-pattern>home/dot_config/fixture.sh', line='apiKey: ANTHROPIC_API_KEY'
    failing subtest: rel='home/dot_config/fixture.sh', line='env: ANTHROPIC_API_KEY'
    failing subtest: rel='home/dot_config/fixture.sh', line='export ANTHROPIC_OAUTH_TOKEN=x'
    failing subtest: rel='install/fixture.sh', line='ANTHROPIC_API_KEY=literal'
    failing subtest: rel='install/fixture.sh', line='export ANTHROPIC_OAUTH_TOKEN=x'
    failing subtest: rel='scripts/fixture.sh', line='export ANTHROPIC_OAUTH_TOKEN=x'
the task's R2 regex as written: rc=1 AssertionError: Tuples differ: (False, '') != (True, 'ERROR: home/dot_config/fixture.sh:[68 chars]t\n') | AssertionError: Tuples differ: (False, '') != (True, 'ERROR: home/dot_config/fixture.sh:[68 chars]t\n') | AssertionError: Tuples differ: (False, '') != (True, 'ERROR: home/dot_config/fixture.sh:[68 chars]t\n') | AssertionError: Tuples differ: (False, '') != (True, 'ERROR: home/dot_config/fixture.sh:[68 chars]t\n') | FAILED (failures=4)
    failing subtest: rel='home/dot_config/fixture.sh', line='ANTHROPIC_API_KEY: {{ .anthropic }}'
    failing subtest: rel='home/dot_config/fixture.sh', line='ANTHROPIC_API_KEY= $ANTHROPIC_API_KEY'
    failing subtest: rel='home/dot_config/fixture.sh', line='ANTHROPIC_API_KEY=""'
    failing subtest: rel='home/dot_config/fixture.sh', line='ANTHROPIC_<redacted:secret-pattern>'
mutant: R1 removed: rc=1 AssertionError: False is not true | AssertionError: False is not true | FAILED (failures=2)
    failing subtest: rel='home/dot_config/fixture.sh', line='export ANTHROPIC_OAUTH_TOKEN=x'
    failing subtest: rel='install/fixture.sh', line='export ANTHROPIC_OAUTH_TOKEN=x'
mutant: R2 removed: rc=1 AssertionError: False is not true | AssertionError: False is not true | AssertionError: False is not true | FAILED (failures=3)
    failing subtest: rel='home/dot_config/fixture.sh', line='ANTHROPIC_API_KEY: literal'
    failing subtest: rel='home/dot_config/fixture.sh', line='ANTHROPIC_<redacted:secret-pattern>'
    failing subtest: rel='install/fixture.sh', line='ANTHROPIC_API_KEY=literal'
mutant: symlinks followed: rc=1 AssertionError: Tuples differ: (False, '') != (True, 'ERROR: home/dot_config/link:1: R1:[65 chars]y\n') | FAILED (failures=1)
mutant: a failed listing passes: rc=1 AssertionError: False is not true | FAILED (failures=1)
mutant: the R2 message quotes the line: rc=1 AssertionError: 'ANTHROPIC_<redacted:secret-pattern>' unexpectedly found in 'ERROR: home/dot_config/fixture.sh:2: R2: assigns ANTHROPIC_API_KEY a literal; reference the environment: ANTHROPIC_<redacted:secret-pattern>\n' | AssertionError: 'ANTHROPIC_API_KEY: literal' unexpectedly found in 'ERROR: home/dot_config/fixture.sh:2: R2: assigns ANTHROPIC_API_KEY a literal; reference the environment: ANTHROPIC_API_KEY: literal\n' | AssertionError: 'ANTHROPIC_API_KEY=literal' unexpectedly found in 'ERROR: install/fixture.sh:2: R2: assigns ANTHROPIC_API_KEY a literal; reference the environment: ANTHROPIC_API_KEY=literal\n' | FAILED (failures=3)
    failing subtest: rel='home/dot_config/fixture.sh', line='ANTHROPIC_API_KEY: literal'
    failing subtest: rel='home/dot_config/fixture.sh', line='ANTHROPIC_<redacted:secret-pattern>'
    failing subtest: rel='install/fixture.sh', line='ANTHROPIC_API_KEY=literal'
restored byte-identical: True
(exit 0)
```

## 6. The Check: the new test, the module and Ruff

Ruff reports the same eight findings on the branch as on origin/main's copies of the two files, all in lines this PR does not touch (UP037 moves from line 1571 to 1630 with the 59 inserted test lines); the new code adds none, and both files are formatted.

```console
$ uv run python -m unittest tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_auth_route_refuses_an_oauth_token_in_applied_files_and_a_literal_api_key_assignment -v
test_anthropic_auth_route_refuses_an_oauth_token_in_applied_files_and_a_literal_api_key_assignment (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_auth_route_refuses_an_oauth_token_in_applied_files_and_a_literal_api_key_assignment) ... ok

----------------------------------------------------------------------
Ran 1 test in 0.403s

OK
(exit 0)
```

```console
$ uv run python -m unittest tests/unit/test_validate_agent_assets.py -v
test_a_masked_key_collision_fails_and_leaves_the_file_unchanged (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_a_masked_key_collision_fails_and_leaves_the_file_unchanged) ... ok
test_keeps_carriage_returns_and_every_unmasked_byte (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_keeps_carriage_returns_and_every_unmasked_byte) ... ok
test_leaves_allowed_placeholders_the_scan_accepts (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_leaves_allowed_placeholders_the_scan_accepts) ... ok
test_masks_an_earlier_duplicate_member_so_the_scan_passes (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_masks_an_earlier_duplicate_member_so_the_scan_passes) ... ok
test_masks_every_match_in_place_and_reports_counts (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_masks_every_match_in_place_and_reports_counts) ... ok
test_masks_json_content_whatever_the_suffix (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_masks_json_content_whatever_the_suffix) ... ok
test_masks_json_string_values_and_keeps_the_document_parseable (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_masks_json_string_values_and_keeps_the_document_parseable) ... ok
test_missing_file_exits_2_without_touching_others (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_missing_file_exits_2_without_touching_others) ... ok
test_normalises_home_paths_in_text_and_json_evidence (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_normalises_home_paths_in_text_and_json_evidence) ... ok
test_a_key_after_json_escaped_whitespace_is_flagged (tests.unit.test_validate_agent_assets.SecretPatternBoundaryTest.test_a_key_after_json_escaped_whitespace_is_flagged) ... ok
test_a_key_prefix_inside_a_hyphenated_word_is_clean (tests.unit.test_validate_agent_assets.SecretPatternBoundaryTest.test_a_key_prefix_inside_a_hyphenated_word_is_clean) ... ok
test_a_long_hyphenated_run_scans_in_linear_time (tests.unit.test_validate_agent_assets.SecretPatternBoundaryTest.test_a_long_hyphenated_run_scans_in_linear_time) ... ok
test_a_real_key_prefix_is_still_flagged (tests.unit.test_validate_agent_assets.SecretPatternBoundaryTest.test_a_real_key_prefix_is_still_flagged) ... ok
test_an_sk_key_body_needs_a_hyphen_free_run (tests.unit.test_validate_agent_assets.SecretPatternBoundaryTest.test_an_sk_key_body_needs_a_hyphen_free_run) ... ok
test_masking_keeps_the_escape_before_the_key (tests.unit.test_validate_agent_assets.SecretPatternBoundaryTest.test_masking_keeps_the_escape_before_the_key) ... ok
test_a_one_segment_home_keeps_namespace_roots_intact (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_a_one_segment_home_keeps_namespace_roots_intact) ... ok
test_a_root_home_keeps_sub_agent_identifiers (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_a_root_home_keeps_sub_agent_identifiers) ... ok
test_agent_manifest_accepts_a_worker_worktree_under_claude_worktrees (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_accepts_a_worker_worktree_under_claude_worktrees) ... ok
test_agent_manifest_accepts_exact_security_profile_set (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_accepts_exact_security_profile_set) ... ok
test_agent_manifest_pins_the_audit_codex_profile (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_pins_the_audit_codex_profile) ... ok
test_agent_manifest_rejects_a_worker_worktree_outside_claude_worktrees (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_a_worker_worktree_outside_claude_worktrees) ... ok
test_agent_manifest_rejects_invalid_or_missing_orchestrator_kind (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_invalid_or_missing_orchestrator_kind) ... ok
test_agent_manifest_rejects_invalid_or_missing_worker_kind (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_invalid_or_missing_worker_kind) ... ok
test_agent_manifest_rejects_missing_audit_profile (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_missing_audit_profile) ... ok
test_agent_manifest_rejects_missing_security_profile (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_missing_security_profile) ... ok
test_agent_manifest_rejects_the_retired_adh_profile (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_the_retired_adh_profile) ... ok
test_agent_manifest_rejects_unknown_worker_profile (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_unknown_worker_profile) ... ok
test_agent_manifest_rejects_wrong_security_codex_model (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_wrong_security_codex_model) ... ok
test_agent_manifest_requires_fable_advisor_on_the_worker_profile (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_requires_fable_advisor_on_the_worker_profile) ... ok
test_agent_manifest_requires_readme_to_document_on_demand_seating (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_requires_readme_to_document_on_demand_seating) ... ok
test_agent_manifest_requires_readme_to_state_the_orchestrator_kind (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_requires_readme_to_state_the_orchestrator_kind) ... ok
test_agent_manifest_requires_readme_to_state_the_worker_kind (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_requires_readme_to_state_the_worker_kind) ... ok
test_agent_manifest_worker_kind_check_ignores_the_orchestrator_sentence (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_worker_kind_check_ignores_the_orchestrator_sentence) ... ok
test_agmsg_installer_requires_a_release_pin_and_its_tag (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_installer_requires_a_release_pin_and_its_tag) ... ok
test_agmsg_installer_requires_the_full_tag_commit (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_installer_requires_the_full_tag_commit) ... ok
test_agmsg_installer_requires_the_npm_bootstrap_integrity (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_installer_requires_the_npm_bootstrap_integrity) ... ok
test_agmsg_ownership_accepts_the_installer_layout (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_accepts_the_installer_layout) ... ok
test_agmsg_ownership_rejects_a_managed_claude_command (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_rejects_a_managed_claude_command) ... ok
test_agmsg_ownership_rejects_a_vendored_skill_copy (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_rejects_a_vendored_skill_copy) ... ok
test_agmsg_ownership_rejects_removing_installer_owned_paths (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_rejects_removing_installer_owned_paths) ... ok
test_agmsg_ownership_requires_retiring_the_symlink_farm (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_requires_retiring_the_symlink_farm) ... ok
test_anthropic_auth_route_refuses_an_oauth_token_in_applied_files_and_a_literal_api_key_assignment (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_auth_route_refuses_an_oauth_token_in_applied_files_and_a_literal_api_key_assignment) ... ok
test_assets_accept_complete_declarations_and_rendered_versions (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_accept_complete_declarations_and_rendered_versions) ... ok
test_assets_accept_rolling_releases_without_pins (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_accept_rolling_releases_without_pins) ... ok
test_assets_reject_a_malformed_render_entry (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_a_malformed_render_entry) ... ok
test_assets_reject_each_incomplete_declaration (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_each_incomplete_declaration) ... ok
test_assets_reject_invalid_rolling_and_pinned_declarations (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_invalid_rolling_and_pinned_declarations) ... ok
test_assets_reject_one_assignment_rendered_from_two_fields (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_one_assignment_rendered_from_two_fields) ... ok
test_assets_reject_one_assignment_rendered_through_a_symlink_alias (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_one_assignment_rendered_through_a_symlink_alias) ... ok
test_assets_reject_unrendered_literal_versions_anywhere_in_install_or_scripts (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_unrendered_literal_versions_anywhere_in_install_or_scripts) ... ok
test_assets_report_an_unrendered_declare_r_version (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_report_an_unrendered_declare_r_version) ... ok
test_assets_scan_setup_sh_for_unrendered_versions (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_scan_setup_sh_for_unrendered_versions) ... ok
test_claude_mcp_config_accepts_an_empty_map_and_rejects_a_non_mapping (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_mcp_config_accepts_an_empty_map_and_rejects_a_non_mapping) ... ok
test_claude_permissions_allow_must_list_non_empty_rules (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_permissions_allow_must_list_non_empty_rules) ... ok
test_claude_sandbox_accepts_manifest_symmetric_settings (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_accepts_manifest_symmetric_settings) ... ok
test_claude_sandbox_extra_allow_write_must_be_absolute_or_home_paths_without_globs (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_extra_allow_write_must_be_absolute_or_home_paths_without_globs) ... ok
test_claude_sandbox_rejects_each_broken_rule (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_rejects_each_broken_rule) ... ok
test_claude_sandbox_requires_extra_codex_writable_roots (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_requires_extra_codex_writable_roots) ... ok
test_claude_sandbox_unix_sockets_must_be_absolute_or_home_paths_without_globs (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_unix_sockets_must_be_absolute_or_home_paths_without_globs) ... ok
test_codex_command_hooks_accept_the_declared_tables (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_command_hooks_accept_the_declared_tables) ... ok
test_codex_command_hooks_reject_bad_entries_and_stray_tables (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_command_hooks_reject_bad_entries_and_stray_tables) ... ok
test_codex_modify_script_requires_executable_source (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_modify_script_requires_executable_source) ... ok
test_codex_projects_accept_working_tree_placeholder (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_projects_accept_working_tree_placeholder) ... ok
test_codex_projects_reject_hard_coded_macos_home (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_projects_reject_hard_coded_macos_home) ... ok
test_codex_projects_reject_missing_working_tree_placeholder (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_projects_reject_missing_working_tree_placeholder) ... ok
test_codex_sandbox_workspace_write_accepts_matching_manifest (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_sandbox_workspace_write_accepts_matching_manifest) ... ok
test_codex_sandbox_workspace_write_must_match_manifest (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_sandbox_workspace_write_must_match_manifest) ... ok
test_codex_sandbox_workspace_write_requires_all_agmsg_roots (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_sandbox_workspace_write_requires_all_agmsg_roots) ... ok
test_compactiondb_project_copy_must_match_the_vendor_tree (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_compactiondb_project_copy_must_match_the_vendor_tree) ... ok
test_home_paths_normalise_to_tilde_and_repository_paths_stay (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_home_paths_normalise_to_tilde_and_repository_paths_stay) ... ok
test_hook_composition_accepts_managed_source_fixture (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_accepts_managed_source_fixture) ... ok
test_hook_composition_pins_sessionstart_order (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_pins_sessionstart_order) ... ok
test_hook_composition_rejects_duplicate_command (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_rejects_duplicate_command) ... ok
test_hook_composition_rejects_sync_timeout_over_budget (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_rejects_sync_timeout_over_budget) ... ok
test_hook_composition_requires_permgate_first (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_requires_permgate_first) ... ok
test_manifest_home_paths_allow_chezmoi_home_dir (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_allow_chezmoi_home_dir) ... ok
test_manifest_home_paths_allow_flow_style_projects (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_allow_flow_style_projects) ... ok
test_manifest_home_paths_exempt_runtime_owned_projects (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_exempt_runtime_owned_projects) ... ok
test_manifest_home_paths_only_exempt_the_projects_subtree (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_only_exempt_the_projects_subtree) ... ok
test_manifest_home_paths_reject_hard_coded_home (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_reject_hard_coded_home) ... ok
test_manifest_home_paths_reject_hard_coded_linux_home (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_reject_hard_coded_linux_home) ... ok
test_manifest_home_paths_reject_non_codex_projects_mapping (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_reject_non_codex_projects_mapping) ... ok
test_permgate_policy_requires_a_schema_3_object (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_permgate_policy_requires_a_schema_3_object) ... ok
test_recursive_scans_skip_gitignored_local_state (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_recursive_scans_skip_gitignored_local_state) ... ok
test_recursive_scans_skip_nested_git_trees_only (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_recursive_scans_skip_nested_git_trees_only) ... ok
test_repo_claude_settings_accept_portable_interpreter (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_repo_claude_settings_accept_portable_interpreter) ... ok
test_repo_claude_settings_reject_machine_specific_interpreter (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_repo_claude_settings_reject_machine_specific_interpreter) ... ERROR: /tmp/claude-501/validate-agent-assets-test-quxaa6f4/.claude/settings.json hook SessionEnd must not hard-code a machine-specific home path: ~/.local/share/mise/installs/python/3.14.7/bin/python3.14
ok
test_runner_homes_match_anywhere (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_runner_homes_match_anywhere) ... ok
test_secret_scan_allows_exact_placeholder_tokens (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_allows_exact_placeholder_tokens) ... ok
test_secret_scan_checks_docs_paths (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_checks_docs_paths) ... ok
test_secret_scan_checks_extensionless_executables (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_checks_extensionless_executables) ... ok
test_secret_scan_checks_utf16_bom_text (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_checks_utf16_bom_text) ... ok
test_secret_scan_fails_a_nul_in_orchestration_text_and_skips_other_binaries (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_fails_a_nul_in_orchestration_text_and_skips_other_binaries) ... ok
test_secret_scan_flags_the_running_users_home_as_a_backstop (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_flags_the_running_users_home_as_a_backstop) ... ok
test_secret_scan_reads_json_per_key_and_string_value (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_reads_json_per_key_and_string_value) ... ok
test_secret_scan_rejects_home_paths_in_orchestration_evidence_only (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_rejects_home_paths_in_orchestration_evidence_only) ... ok
test_secret_scan_rejects_placeholder_with_suffix (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_rejects_placeholder_with_suffix) ... ok
test_secret_scan_rejects_utf16_orchestration_text_with_the_nul_offset (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_rejects_utf16_orchestration_text_with_the_nul_offset) ... ok

----------------------------------------------------------------------
Ran 98 tests in 2.422s

OK
(exit 0)
```

```console
$ ruff check --config ruff.toml --output-format concise scripts/validate-agent-assets.py tests/unit/test_validate_agent_assets.py
scripts/validate-agent-assets.py:1:1: EXE001 Shebang is present but file is not executable
scripts/validate-agent-assets.py:4:1: I001 [*] Import block is un-sorted or un-formatted
scripts/validate-agent-assets.py:133:9: SIM102 Use a single `if` statement instead of nested `if` statements
scripts/validate-agent-assets.py:867:12: C401 Unnecessary generator (rewrite as a set comprehension)
scripts/validate-agent-assets.py:924:18: UP022 Prefer `capture_output` over sending `stdout` and `stderr` to `PIPE`
tests/unit/test_validate_agent_assets.py:1:1: EXE001 Shebang is present but file is not executable
tests/unit/test_validate_agent_assets.py:252:13: FLY002 Consider f-string instead of string join
tests/unit/test_validate_agent_assets.py:1630:41: UP037 [*] Remove quotes from type annotation
Found 8 errors.
[*] 2 fixable with `--fix` (3 unsafe fixes available with `--fix --unsafe-fixes`).
(exit 1)
$ ruff check --config ruff.toml --output-format concise <origin/main copies of the two files>   # the baseline
scripts/validate-agent-assets.py:1:1: EXE001 Shebang is present but file is not executable
scripts/validate-agent-assets.py:4:1: I001 [*] Import block is un-sorted or un-formatted
scripts/validate-agent-assets.py:133:9: SIM102 Use a single `if` statement instead of nested `if` statements
scripts/validate-agent-assets.py:867:12: C401 Unnecessary generator (rewrite as a set comprehension)
scripts/validate-agent-assets.py:924:18: UP022 Prefer `capture_output` over sending `stdout` and `stderr` to `PIPE`
tests/unit/test_validate_agent_assets.py:1:1: EXE001 Shebang is present but file is not executable
tests/unit/test_validate_agent_assets.py:252:13: FLY002 Consider f-string instead of string join
tests/unit/test_validate_agent_assets.py:1571:41: UP037 [*] Remove quotes from type annotation
Found 8 errors.
[*] 2 fixable with `--fix` (3 unsafe fixes available with `--fix --unsafe-fixes`).
(exit 1)
$ ruff format --config ruff.toml --check scripts/validate-agent-assets.py tests/unit/test_validate_agent_assets.py
2 files already formatted
(exit 0)
```

## 7. The validator on the branch (premise 1: exit 0 with the rule live)

Run on the staged tree after the masker (`uv run --offline --no-project --with pyyaml scripts/validate-agent-assets.py --mask-secrets` on validation.md, report.md, sandbox.md, learning.md and autoskill.md, which masked 11, 2, 0, 0 and 0 matches; task.md is left byte-identical).

```console
$ uv run --offline --with pyyaml scripts/validate-agent-assets.py > "$TMPDIR/t129/08-validator.txt" 2>&1; echo "rc=$?"   # 167 s, on the staged tree
rc=0
$ grep -v "^WARN: regime-boundary:" "$TMPDIR/t129/08-validator.txt"
agent asset validation ok
(exit 0)
$ grep -c "^WARN: regime-boundary:" "$TMPDIR/t129/08-validator.txt"   # the Stop-checklist report, warnings that never fail the run
718
(exit 0)
$ grep -F "worktrees/worker-c" "$TMPDIR/t129/08-validator.txt"   # the lines about this worktree
WARN: regime-boundary: worker still seated at .claude/worktrees/worker-c (herdr-agents --remove-worker .claude/worktrees/worker-c)
(exit 0)
```

## 8. Caps and the files of the commit

Staged before the commit, so the numstat equals `git diff --numstat origin/main...HEAD` after it; the caps exclude `.orchestration/`, whose validation.md row grows by sections 7 and 8.

```console
$ git diff --cached --numstat origin/main   # equal to origin/main...HEAD after the commit: HEAD is origin/main
3	0	.orchestration/dotfiles-T129-anthropic-auth-route-check-a01/autoskill.md
6	0	.orchestration/dotfiles-T129-anthropic-auth-route-check-a01/learning.md
59	0	.orchestration/dotfiles-T129-anthropic-auth-route-check-a01/report.md
24	0	.orchestration/dotfiles-T129-anthropic-auth-route-check-a01/sandbox.md
98	0	.orchestration/dotfiles-T129-anthropic-auth-route-check-a01/task.md
524	0	.orchestration/dotfiles-T129-anthropic-auth-route-check-a01/validation.md
30	0	scripts/validate-agent-assets.py
59	0	tests/unit/test_validate_agent_assets.py
(exit 0)
$ git diff --cached --name-status origin/main
A	.orchestration/dotfiles-T129-anthropic-auth-route-check-a01/autoskill.md
A	.orchestration/dotfiles-T129-anthropic-auth-route-check-a01/learning.md
A	.orchestration/dotfiles-T129-anthropic-auth-route-check-a01/report.md
A	.orchestration/dotfiles-T129-anthropic-auth-route-check-a01/sandbox.md
A	.orchestration/dotfiles-T129-anthropic-auth-route-check-a01/task.md
A	.orchestration/dotfiles-T129-anthropic-auth-route-check-a01/validation.md
M	scripts/validate-agent-assets.py
M	tests/unit/test_validate_agent_assets.py
(exit 0)
```

## 9. Fix round: the Bot's P1 4302488371 on 53d9b608

The Bot's review 5557555178 of 53d9b608 (2026-10-17T11:24:20Z) raised one P1 and one P2, both on `scripts/validate-agent-assets.py:1577`. P1 4302488371: the lookahead exempted every value that starts with `$`, so `$'...'` and `$"..."`, which Bash reads as literal data, passed R2 (and SECRET_PATTERN). The one worker-side fix round narrows the exemption to the reference forms amendment 1 names, `$NAME` and `${NAME}` (`\$\{?[A-Za-z_]`); `$(...)` is no such reference and is refused too. P2 4302488376 (a comment after an empty value) is left to the orchestrator (the report proposes it as a C-50 round).

### 9.1 The three new refusal cases against 53d9b608's regex

```console
$ git diff --stat   # the three new refusal cases only; scripts/validate-agent-assets.py as at 53d9b608
 tests/unit/test_validate_agent_assets.py | 4 ++++
 1 file changed, 4 insertions(+)
(exit 0)
$ uv run python -m unittest tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_auth_route_refuses_an_oauth_token_in_applied_files_and_a_literal_api_key_assignment
FAIL: test_anthropic_auth_route_refuses_an_oauth_token_in_applied_files_and_a_literal_api_key_assignment (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_auth_route_refuses_an_oauth_token_in_applied_files_and_a_literal_api_key_assignment) (rel='home/dot_config/fixture.sh', line="ANTHROPIC_API_KEY=$'literal-value'")
AssertionError: False is not true
FAIL: test_anthropic_auth_route_refuses_an_oauth_token_in_applied_files_and_a_literal_api_key_assignment (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_auth_route_refuses_an_oauth_token_in_applied_files_and_a_literal_api_key_assignment) (rel='home/dot_config/fixture.sh', line='ANTHROPIC_API_KEY=$"literal-value"')
AssertionError: False is not true
FAIL: test_anthropic_auth_route_refuses_an_oauth_token_in_applied_files_and_a_literal_api_key_assignment (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_auth_route_refuses_an_oauth_token_in_applied_files_and_a_literal_api_key_assignment) (rel='home/dot_config/fixture.sh', line='ANTHROPIC_API_KEY=$(cat key-file)')
AssertionError: False is not true
Ran 1 test in 0.416s
FAILED (failures=3)
(exit 1)
```

### 9.2 The diff of the round

```console
$ git diff 53d9b608416aff2e99b2326fa4fa44f7274923ec -- scripts tests   # the fix round
diff --git a/scripts/validate-agent-assets.py b/scripts/validate-agent-assets.py
index e282a3b6..1adf5296 100644
--- a/scripts/validate-agent-assets.py
+++ b/scripts/validate-agent-assets.py
@@ -1572,9 +1572,12 @@ def validate_no_obvious_secrets() -> None:
             )
 
 
-# R2: an assignment whose value is not a `$` reference, a `{{` template or empty. The whitespace and the optional
-# quote sit inside the lookahead, so neither can match empty in front of a reference and let it through as a literal.
-ANTHROPIC_API_KEY_LITERAL = re.compile(r"""ANTHROPIC_API_KEY\s*[:=](?!\s*["']?(?:\$|\{\{)|\s*(?:""|'')?\s*$)""")
+# R2: an assignment whose value is not a `$NAME`/`${NAME}` reference, a `{{` template or empty; `$'...'` and `$"..."`
+# are literal data in Bash. The whitespace and the optional quote sit inside the lookahead, so neither can match empty
+# in front of a reference and let it through as a literal.
+ANTHROPIC_API_KEY_LITERAL = re.compile(
+    r"""ANTHROPIC_API_KEY\s*[:=](?!\s*["']?(?:\$\{?[A-Za-z_]|\{\{)|\s*(?:""|'')?\s*$)"""
+)
 
 
 def validate_anthropic_auth_route() -> None:
diff --git a/tests/unit/test_validate_agent_assets.py b/tests/unit/test_validate_agent_assets.py
index 7c11274f..02724484 100644
--- a/tests/unit/test_validate_agent_assets.py
+++ b/tests/unit/test_validate_agent_assets.py
@@ -1448,6 +1448,10 @@ class ValidateAgentAssetsTest(unittest.TestCase):
             (home, f'{key}="literal-value"', "R2"),
             (home, f"{key}: literal", "R2"),
             (install, f"{key}=literal", "R2"),
+            # Only $NAME and ${NAME} are references: Bash reads $'...' and $"..." as literal data (the Bot's P1).
+            (home, f"{key}=$'literal-value'", "R2"),
+            (home, f'{key}=$"literal-value"', "R2"),
+            (home, f"{key}=$(cat key-file)", "R2"),
         ):
             with self.subTest(rel=rel, line=line):
                 refused, stderr = check(rel, line)
(exit 0)
```

### 9.3 After the fix: the test, the regex table and the mutants

The table and the mutant script are the section 3 and 5 scripts with the new regex: the table gains the `$'...'` and `$"..."` rows and `$(...)` now refuses; the mutants gain `any $ exempts`, the regex before this round.

```console
$ uv run python -m unittest tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_auth_route_refuses_an_oauth_token_in_applied_files_and_a_literal_api_key_assignment -v
test_anthropic_auth_route_refuses_an_oauth_token_in_applied_files_and_a_literal_api_key_assignment (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_auth_route_refuses_an_oauth_token_in_applied_files_and_a_literal_api_key_assignment) ... ok

----------------------------------------------------------------------
Ran 1 test in 0.432s

OK
(exit 0)
```

```python
"""R2 as first written in the task against the branch's ANTHROPIC_API_KEY_LITERAL, on item 2's lines and five more."""

import importlib.util
import re

spec = importlib.util.spec_from_file_location(
    "validate_agent_assets", "scripts/validate-agent-assets.py"
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
branch = module.ANTHROPIC_API_KEY_LITERAL
task = re.compile(r"""ANTHROPIC_API_KEY\s*[:=]\s*(["']?)(?!\$|\{\{|\1\s*$)""")
K = "ANTHROPIC_API_" + "KEY"
cases = [  # (line, expected): True refuses, False passes, None is out of scope (the JSON key form, question 2)
    (f'{K}="literal-value"', True),
    (f"{K}: literal", True),
    (f"{K}=literal", True),
    (f"{K}=${K}", False),
    (f"apiKey: {K}", False),
    (f"env: {K}", False),
    (f"{K}=", False),
    (f'{K}=""', False),
    (f'{K}="${{{K}}}"', False),
    (f"{K}= ${K}", False),
    (f"{K}: {{{{ .anthropic }}}}", False),
    (f"export {K}=$(op read x)", True),  # not a $NAME or ${NAME} reference (the Bot's P1)
    (f"{K}=$'literal-value'", True),
    (f'{K}=$"literal-value"', True),
    (f'"{K}": "literal-value",', None),
    (f'"{K}": "${{{K}}}",', None),
]
for line, expected in cases:
    t, b = bool(task.search(line)), bool(branch.search(line))
    want = {True: "refuse", False: "pass  ", None: "n/a   "}[expected]
    marks = (
        ""
        if expected is None
        else ("" if b == expected else "BRANCH-WRONG ")
        + ("" if t == expected else "TASK-WRONG")
    )
    print(
        f"want={want} task={'refuse' if t else 'pass  '} branch={'refuse' if b else 'pass  '} {marks:<24} {line}"
    )
```

```console
$ uv run --offline --no-project python -I r2table.py   # from the worktree root; the script is pasted above
want=refuse task=refuse branch=refuse                          ANTHROPIC_<redacted:secret-pattern>
want=refuse task=refuse branch=refuse                          ANTHROPIC_API_KEY: literal
want=refuse task=refuse branch=refuse                          ANTHROPIC_API_KEY=literal
want=pass   task=pass   branch=pass                            ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY
want=pass   task=pass   branch=pass                            apiKey: ANTHROPIC_API_KEY
want=pass   task=pass   branch=pass                            env: ANTHROPIC_API_KEY
want=pass   task=pass   branch=pass                            ANTHROPIC_API_KEY=
want=pass   task=refuse branch=pass   TASK-WRONG               ANTHROPIC_API_KEY=""
want=pass   task=refuse branch=pass   TASK-WRONG               ANTHROPIC_<redacted:secret-pattern>
want=pass   task=refuse branch=pass   TASK-WRONG               ANTHROPIC_API_KEY= $ANTHROPIC_API_KEY
want=pass   task=refuse branch=pass   TASK-WRONG               ANTHROPIC_API_KEY: {{ .anthropic }}
want=refuse task=pass   branch=refuse TASK-WRONG               export ANTHROPIC_API_KEY=$(op read x)
want=refuse task=pass   branch=refuse TASK-WRONG               ANTHROPIC_API_KEY=$'literal-value'
want=refuse task=pass   branch=refuse TASK-WRONG               ANTHROPIC_API_KEY=$"literal-value"
want=n/a    task=pass   branch=pass                            "ANTHROPIC_API_KEY": "literal-value",
want=n/a    task=pass   branch=pass                            "ANTHROPIC_API_KEY": "${ANTHROPIC_API_KEY}",
(exit 0)
```

```python
"""Run the new test against origin/main's validator, the task's literal R2 regex, and one mutant per property.

Each variant is written over scripts/validate-agent-assets.py, the test runs, and the fixed file is written back
and compared byte for byte. Mutants are literal string replacements asserted to match once.
"""

import re
import subprocess
from pathlib import Path

script = Path("scripts/validate-agent-assets.py")
fixed = script.read_text()
main = subprocess.run(
    ["git", "show", "origin/main:" + str(script)],
    capture_output=True,
    text=True,
    check=True,
).stdout
test = (
    "tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest."
    "test_anthropic_auth_route_refuses_an_oauth_token_in_applied_files_and_a_literal_api_key_assignment"
)
MINE = r'''re.compile(
    r"""ANTHROPIC_API_KEY\s*[:=](?!\s*["']?(?:\$\{?[A-Za-z_]|\{\{)|\s*(?:""|'')?\s*$)"""
)'''
TASK = r'''re.compile(
    r"""ANTHROPIC_API_KEY\s*[:=]\s*(["']?)(?!\$|\{\{|\1\s*$)"""
)'''


def mutate(old, new):
    assert fixed.count(old) == 1, old
    return fixed.replace(old, new)


variants = [
    ("origin/main's validator (no function yet)", main),
    ("the task's R2 regex as written", mutate(MINE, TASK)),
    ("mutant: any $ exempts (the first form, the Bot's P1)", mutate(r"(?:\$\{?[A-Za-z_]|\{\{)", r"(?:\$|\{\{)")),
    ("mutant: R1 removed", mutate('if "ANTHROPIC_OAUTH_TOKEN" in line:', "if False:")),
    (
        "mutant: R2 removed",
        mutate("if ANTHROPIC_API_KEY_LITERAL.search(line):", "if False:"),
    ),
    (
        "mutant: symlinks followed",
        mutate("if path.is_symlink() or not path.is_file():", "if not path.is_file():"),
    ),
    (
        "mutant: a failed listing passes",
        mutate("if listed.returncode != 0:", "if False:"),
    ),
    (
        "mutant: the R2 message quotes the line",
        mutate(
            'a literal; reference the environment"',
            'a literal; reference the environment: {line}"',
        ),
    ),
]
try:
    for name, body in variants:
        script.write_text(body)
        result = subprocess.run(
            ["uv", "run", "python", "-m", "unittest", test],
            capture_output=True,
            text=True,
            check=False,
        )
        lines = result.stderr.splitlines()
        subtests = sorted(
            {m.group(1) for m in (re.search(r"\((rel=.*)\)$", x) for x in lines) if m}
        )
        tail = [
            x
            for x in lines
            if x.startswith(("AssertionError", "AttributeError", "OK", "FAILED"))
        ]
        print(f"{name}: rc={result.returncode} {' | '.join(tail)}")
        for subtest in subtests:
            print(f"    failing subtest: {subtest}")
finally:
    script.write_text(fixed)
print("restored byte-identical:", script.read_text() == fixed)
```

```console
$ uv run --offline --no-project python -I t129_mutants.py   # from the worktree root; the script is pasted above
origin/main's validator (no function yet): rc=1 AttributeError: module 'validate_agent_assets' has no attribute 'validate_anthropic_auth_route' | AttributeError: module 'validate_agent_assets' has no attribute 'validate_anthropic_auth_route' | AttributeError: module 'validate_agent_assets' has no attribute 'validate_anthropic_auth_route' | AttributeError: module 'validate_agent_assets' has no attribute 'validate_anthropic_auth_route' | AttributeError: module 'validate_agent_assets' has no attribute 'validate_anthropic_auth_route' | AttributeError: module 'validate_agent_assets' has no attribute 'validate_anthropic_auth_route' | AttributeError: module 'validate_agent_assets' has no attribute 'validate_anthropic_auth_route' | AttributeError: module 'validate_agent_assets' has no attribute 'validate_anthropic_auth_route' | AttributeError: module 'validate_agent_assets' has no attribute 'validate_anthropic_auth_route' | AttributeError: module 'validate_agent_assets' has no attribute 'validate_anthropic_auth_route' | AttributeError: module 'validate_agent_assets' has no attribute 'validate_anthropic_auth_route' | AttributeError: module 'validate_agent_assets' has no attribute 'validate_anthropic_auth_route' | AttributeError: module 'validate_agent_assets' has no attribute 'validate_anthropic_auth_route' | AttributeError: module 'validate_agent_assets' has no attribute 'validate_anthropic_auth_route' | AttributeError: module 'validate_agent_assets' has no attribute 'validate_anthropic_auth_route' | AttributeError: module 'validate_agent_assets' has no attribute 'validate_anthropic_auth_route' | AttributeError: module 'validate_agent_assets' has no attribute 'validate_anthropic_auth_route' | AttributeError: module 'validate_agent_assets' has no attribute 'validate_anthropic_auth_route' | FAILED (errors=18)
    failing subtest: rel='home/dot_config/fixture.sh', line="ANTHROPIC_API_KEY=$'literal-value'"
    failing subtest: rel='home/dot_config/fixture.sh', line='ANTHROPIC_API_KEY: literal'
    failing subtest: rel='home/dot_config/fixture.sh', line='ANTHROPIC_API_KEY: {{ .anthropic }}'
    failing subtest: rel='home/dot_config/fixture.sh', line='ANTHROPIC_API_KEY= $ANTHROPIC_API_KEY'
    failing subtest: rel='home/dot_config/fixture.sh', line='ANTHROPIC_API_KEY=""'
    failing subtest: rel='home/dot_config/fixture.sh', line='ANTHROPIC_<redacted:secret-pattern>'
    failing subtest: rel='home/dot_config/fixture.sh', line='ANTHROPIC_<redacted:secret-pattern>'
    failing subtest: rel='home/dot_config/fixture.sh', line='ANTHROPIC_API_KEY=$"literal-value"'
    failing subtest: rel='home/dot_config/fixture.sh', line='ANTHROPIC_API_KEY=$(cat key-file)'
    failing subtest: rel='home/dot_config/fixture.sh', line='ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY'
    failing subtest: rel='home/dot_config/fixture.sh', line='ANTHROPIC_<redacted:secret-pattern>home/dot_config/fixture.sh', line='apiKey: ANTHROPIC_API_KEY'
    failing subtest: rel='home/dot_config/fixture.sh', line='env: ANTHROPIC_API_KEY'
    failing subtest: rel='home/dot_config/fixture.sh', line='export ANTHROPIC_OAUTH_TOKEN=x'
    failing subtest: rel='install/fixture.sh', line='ANTHROPIC_API_KEY=literal'
    failing subtest: rel='install/fixture.sh', line='export ANTHROPIC_OAUTH_TOKEN=x'
    failing subtest: rel='scripts/fixture.sh', line='export ANTHROPIC_OAUTH_TOKEN=x'
the task's R2 regex as written: rc=1 AssertionError: False is not true | AssertionError: False is not true | AssertionError: False is not true | AssertionError: Tuples differ: (False, '') != (True, 'ERROR: home/dot_config/fixture.sh:[68 chars]t\n') | AssertionError: Tuples differ: (False, '') != (True, 'ERROR: home/dot_config/fixture.sh:[68 chars]t\n') | AssertionError: Tuples differ: (False, '') != (True, 'ERROR: home/dot_config/fixture.sh:[68 chars]t\n') | AssertionError: Tuples differ: (False, '') != (True, 'ERROR: home/dot_config/fixture.sh:[68 chars]t\n') | FAILED (failures=7)
    failing subtest: rel='home/dot_config/fixture.sh', line="ANTHROPIC_API_KEY=$'literal-value'"
    failing subtest: rel='home/dot_config/fixture.sh', line='ANTHROPIC_API_KEY: {{ .anthropic }}'
    failing subtest: rel='home/dot_config/fixture.sh', line='ANTHROPIC_API_KEY= $ANTHROPIC_API_KEY'
    failing subtest: rel='home/dot_config/fixture.sh', line='ANTHROPIC_API_KEY=""'
    failing subtest: rel='home/dot_config/fixture.sh', line='ANTHROPIC_<redacted:secret-pattern>'
    failing subtest: rel='home/dot_config/fixture.sh', line='ANTHROPIC_API_KEY=$"literal-value"'
    failing subtest: rel='home/dot_config/fixture.sh', line='ANTHROPIC_API_KEY=$(cat key-file)'
mutant: any $ exempts (the first form, the Bot's P1): rc=1 AssertionError: False is not true | AssertionError: False is not true | AssertionError: False is not true | FAILED (failures=3)
    failing subtest: rel='home/dot_config/fixture.sh', line="ANTHROPIC_API_KEY=$'literal-value'"
    failing subtest: rel='home/dot_config/fixture.sh', line='ANTHROPIC_API_KEY=$"literal-value"'
    failing subtest: rel='home/dot_config/fixture.sh', line='ANTHROPIC_API_KEY=$(cat key-file)'
mutant: R1 removed: rc=1 AssertionError: False is not true | AssertionError: False is not true | FAILED (failures=2)
    failing subtest: rel='home/dot_config/fixture.sh', line='export ANTHROPIC_OAUTH_TOKEN=x'
    failing subtest: rel='install/fixture.sh', line='export ANTHROPIC_OAUTH_TOKEN=x'
mutant: R2 removed: rc=1 AssertionError: False is not true | AssertionError: False is not true | AssertionError: False is not true | AssertionError: False is not true | AssertionError: False is not true | AssertionError: False is not true | FAILED (failures=6)
    failing subtest: rel='home/dot_config/fixture.sh', line="ANTHROPIC_API_KEY=$'literal-value'"
    failing subtest: rel='home/dot_config/fixture.sh', line='ANTHROPIC_API_KEY: literal'
    failing subtest: rel='home/dot_config/fixture.sh', line='ANTHROPIC_<redacted:secret-pattern>'
    failing subtest: rel='home/dot_config/fixture.sh', line='ANTHROPIC_API_KEY=$"literal-value"'
    failing subtest: rel='home/dot_config/fixture.sh', line='ANTHROPIC_API_KEY=$(cat key-file)'
    failing subtest: rel='install/fixture.sh', line='ANTHROPIC_API_KEY=literal'
mutant: symlinks followed: rc=1 AssertionError: Tuples differ: (False, '') != (True, 'ERROR: home/dot_config/link:1: R1:[65 chars]y\n') | FAILED (failures=1)
mutant: a failed listing passes: rc=1 AssertionError: False is not true | FAILED (failures=1)
mutant: the R2 message quotes the line: rc=1 AssertionError: 'ANTHROPIC_<redacted:secret-pattern>' unexpectedly found in 'ERROR: home/dot_config/fixture.sh:2: R2: assigns ANTHROPIC_API_KEY a literal; reference the environment: ANTHROPIC_<redacted:secret-pattern>\n' | AssertionError: 'ANTHROPIC_API_KEY: literal' unexpectedly found in 'ERROR: home/dot_config/fixture.sh:2: R2: assigns ANTHROPIC_API_KEY a literal; reference the environment: ANTHROPIC_API_KEY: literal\n' | AssertionError: 'ANTHROPIC_API_KEY=literal' unexpectedly found in 'ERROR: install/fixture.sh:2: R2: assigns ANTHROPIC_API_KEY a literal; reference the environment: ANTHROPIC_API_KEY=literal\n' | AssertionError: "ANTHROPIC_API_KEY=$'literal-value'" unexpectedly found in "ERROR: home/dot_config/fixture.sh:2: R2: assigns ANTHROPIC_API_KEY a literal; reference the environment: ANTHROPIC_API_KEY=$'literal-value'\n" | AssertionError: 'ANTHROPIC_API_KEY=$"literal-value"' unexpectedly found in 'ERROR: home/dot_config/fixture.sh:2: R2: assigns ANTHROPIC_API_KEY a literal; reference the environment: ANTHROPIC_API_KEY=$"literal-value"\n' | AssertionError: 'ANTHROPIC_API_KEY=$(cat key-file)' unexpectedly found in 'ERROR: home/dot_config/fixture.sh:2: R2: assigns ANTHROPIC_API_KEY a literal; reference the environment: ANTHROPIC_API_KEY=$(cat key-file)\n' | FAILED (failures=6)
    failing subtest: rel='home/dot_config/fixture.sh', line="ANTHROPIC_API_KEY=$'literal-value'"
    failing subtest: rel='home/dot_config/fixture.sh', line='ANTHROPIC_API_KEY: literal'
    failing subtest: rel='home/dot_config/fixture.sh', line='ANTHROPIC_<redacted:secret-pattern>'
    failing subtest: rel='home/dot_config/fixture.sh', line='ANTHROPIC_API_KEY=$"literal-value"'
    failing subtest: rel='home/dot_config/fixture.sh', line='ANTHROPIC_API_KEY=$(cat key-file)'
    failing subtest: rel='install/fixture.sh', line='ANTHROPIC_API_KEY=literal'
restored byte-identical: True
(exit 0)
```

### 9.4 The module, Ruff and the validator after the fix

```console
$ uv run python -m unittest tests/unit/test_validate_agent_assets.py -v
test_a_masked_key_collision_fails_and_leaves_the_file_unchanged (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_a_masked_key_collision_fails_and_leaves_the_file_unchanged) ... ok
test_keeps_carriage_returns_and_every_unmasked_byte (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_keeps_carriage_returns_and_every_unmasked_byte) ... ok
test_leaves_allowed_placeholders_the_scan_accepts (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_leaves_allowed_placeholders_the_scan_accepts) ... ok
test_masks_an_earlier_duplicate_member_so_the_scan_passes (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_masks_an_earlier_duplicate_member_so_the_scan_passes) ... ok
test_masks_every_match_in_place_and_reports_counts (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_masks_every_match_in_place_and_reports_counts) ... ok
test_masks_json_content_whatever_the_suffix (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_masks_json_content_whatever_the_suffix) ... ok
test_masks_json_string_values_and_keeps_the_document_parseable (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_masks_json_string_values_and_keeps_the_document_parseable) ... ok
test_missing_file_exits_2_without_touching_others (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_missing_file_exits_2_without_touching_others) ... ok
test_normalises_home_paths_in_text_and_json_evidence (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_normalises_home_paths_in_text_and_json_evidence) ... ok
test_a_key_after_json_escaped_whitespace_is_flagged (tests.unit.test_validate_agent_assets.SecretPatternBoundaryTest.test_a_key_after_json_escaped_whitespace_is_flagged) ... ok
test_a_key_prefix_inside_a_hyphenated_word_is_clean (tests.unit.test_validate_agent_assets.SecretPatternBoundaryTest.test_a_key_prefix_inside_a_hyphenated_word_is_clean) ... ok
test_a_long_hyphenated_run_scans_in_linear_time (tests.unit.test_validate_agent_assets.SecretPatternBoundaryTest.test_a_long_hyphenated_run_scans_in_linear_time) ... ok
test_a_real_key_prefix_is_still_flagged (tests.unit.test_validate_agent_assets.SecretPatternBoundaryTest.test_a_real_key_prefix_is_still_flagged) ... ok
test_an_sk_key_body_needs_a_hyphen_free_run (tests.unit.test_validate_agent_assets.SecretPatternBoundaryTest.test_an_sk_key_body_needs_a_hyphen_free_run) ... ok
test_masking_keeps_the_escape_before_the_key (tests.unit.test_validate_agent_assets.SecretPatternBoundaryTest.test_masking_keeps_the_escape_before_the_key) ... ok
test_a_one_segment_home_keeps_namespace_roots_intact (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_a_one_segment_home_keeps_namespace_roots_intact) ... ok
test_a_root_home_keeps_sub_agent_identifiers (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_a_root_home_keeps_sub_agent_identifiers) ... ok
test_agent_manifest_accepts_a_worker_worktree_under_claude_worktrees (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_accepts_a_worker_worktree_under_claude_worktrees) ... ok
test_agent_manifest_accepts_exact_security_profile_set (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_accepts_exact_security_profile_set) ... ok
test_agent_manifest_pins_the_audit_codex_profile (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_pins_the_audit_codex_profile) ... ok
test_agent_manifest_rejects_a_worker_worktree_outside_claude_worktrees (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_a_worker_worktree_outside_claude_worktrees) ... ok
test_agent_manifest_rejects_invalid_or_missing_orchestrator_kind (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_invalid_or_missing_orchestrator_kind) ... ok
test_agent_manifest_rejects_invalid_or_missing_worker_kind (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_invalid_or_missing_worker_kind) ... ok
test_agent_manifest_rejects_missing_audit_profile (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_missing_audit_profile) ... ok
test_agent_manifest_rejects_missing_security_profile (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_missing_security_profile) ... ok
test_agent_manifest_rejects_the_retired_adh_profile (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_the_retired_adh_profile) ... ok
test_agent_manifest_rejects_unknown_worker_profile (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_unknown_worker_profile) ... ok
test_agent_manifest_rejects_wrong_security_codex_model (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_wrong_security_codex_model) ... ok
test_agent_manifest_requires_fable_advisor_on_the_worker_profile (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_requires_fable_advisor_on_the_worker_profile) ... ok
test_agent_manifest_requires_readme_to_document_on_demand_seating (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_requires_readme_to_document_on_demand_seating) ... ok
test_agent_manifest_requires_readme_to_state_the_orchestrator_kind (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_requires_readme_to_state_the_orchestrator_kind) ... ok
test_agent_manifest_requires_readme_to_state_the_worker_kind (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_requires_readme_to_state_the_worker_kind) ... ok
test_agent_manifest_worker_kind_check_ignores_the_orchestrator_sentence (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_worker_kind_check_ignores_the_orchestrator_sentence) ... ok
test_agmsg_installer_requires_a_release_pin_and_its_tag (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_installer_requires_a_release_pin_and_its_tag) ... ok
test_agmsg_installer_requires_the_full_tag_commit (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_installer_requires_the_full_tag_commit) ... ok
test_agmsg_installer_requires_the_npm_bootstrap_integrity (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_installer_requires_the_npm_bootstrap_integrity) ... ok
test_agmsg_ownership_accepts_the_installer_layout (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_accepts_the_installer_layout) ... ok
test_agmsg_ownership_rejects_a_managed_claude_command (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_rejects_a_managed_claude_command) ... ok
test_agmsg_ownership_rejects_a_vendored_skill_copy (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_rejects_a_vendored_skill_copy) ... ok
test_agmsg_ownership_rejects_removing_installer_owned_paths (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_rejects_removing_installer_owned_paths) ... ok
test_agmsg_ownership_requires_retiring_the_symlink_farm (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_requires_retiring_the_symlink_farm) ... ok
test_anthropic_auth_route_refuses_an_oauth_token_in_applied_files_and_a_literal_api_key_assignment (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_auth_route_refuses_an_oauth_token_in_applied_files_and_a_literal_api_key_assignment) ... ok
test_assets_accept_complete_declarations_and_rendered_versions (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_accept_complete_declarations_and_rendered_versions) ... ok
test_assets_accept_rolling_releases_without_pins (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_accept_rolling_releases_without_pins) ... ok
test_assets_reject_a_malformed_render_entry (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_a_malformed_render_entry) ... ok
test_assets_reject_each_incomplete_declaration (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_each_incomplete_declaration) ... ok
test_assets_reject_invalid_rolling_and_pinned_declarations (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_invalid_rolling_and_pinned_declarations) ... ok
test_assets_reject_one_assignment_rendered_from_two_fields (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_one_assignment_rendered_from_two_fields) ... ok
test_assets_reject_one_assignment_rendered_through_a_symlink_alias (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_one_assignment_rendered_through_a_symlink_alias) ... ok
test_assets_reject_unrendered_literal_versions_anywhere_in_install_or_scripts (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_unrendered_literal_versions_anywhere_in_install_or_scripts) ... ok
test_assets_report_an_unrendered_declare_r_version (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_report_an_unrendered_declare_r_version) ... ok
test_assets_scan_setup_sh_for_unrendered_versions (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_scan_setup_sh_for_unrendered_versions) ... ok
test_claude_mcp_config_accepts_an_empty_map_and_rejects_a_non_mapping (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_mcp_config_accepts_an_empty_map_and_rejects_a_non_mapping) ... ok
test_claude_permissions_allow_must_list_non_empty_rules (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_permissions_allow_must_list_non_empty_rules) ... ok
test_claude_sandbox_accepts_manifest_symmetric_settings (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_accepts_manifest_symmetric_settings) ... ok
test_claude_sandbox_extra_allow_write_must_be_absolute_or_home_paths_without_globs (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_extra_allow_write_must_be_absolute_or_home_paths_without_globs) ... ok
test_claude_sandbox_rejects_each_broken_rule (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_rejects_each_broken_rule) ... ok
test_claude_sandbox_requires_extra_codex_writable_roots (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_requires_extra_codex_writable_roots) ... ok
test_claude_sandbox_unix_sockets_must_be_absolute_or_home_paths_without_globs (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_unix_sockets_must_be_absolute_or_home_paths_without_globs) ... ok
test_codex_command_hooks_accept_the_declared_tables (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_command_hooks_accept_the_declared_tables) ... ok
test_codex_command_hooks_reject_bad_entries_and_stray_tables (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_command_hooks_reject_bad_entries_and_stray_tables) ... ok
test_codex_modify_script_requires_executable_source (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_modify_script_requires_executable_source) ... ok
test_codex_projects_accept_working_tree_placeholder (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_projects_accept_working_tree_placeholder) ... ok
test_codex_projects_reject_hard_coded_macos_home (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_projects_reject_hard_coded_macos_home) ... ok
test_codex_projects_reject_missing_working_tree_placeholder (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_projects_reject_missing_working_tree_placeholder) ... ok
test_codex_sandbox_workspace_write_accepts_matching_manifest (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_sandbox_workspace_write_accepts_matching_manifest) ... ok
test_codex_sandbox_workspace_write_must_match_manifest (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_sandbox_workspace_write_must_match_manifest) ... ok
test_codex_sandbox_workspace_write_requires_all_agmsg_roots (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_sandbox_workspace_write_requires_all_agmsg_roots) ... ok
test_compactiondb_project_copy_must_match_the_vendor_tree (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_compactiondb_project_copy_must_match_the_vendor_tree) ... ok
test_home_paths_normalise_to_tilde_and_repository_paths_stay (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_home_paths_normalise_to_tilde_and_repository_paths_stay) ... ok
test_hook_composition_accepts_managed_source_fixture (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_accepts_managed_source_fixture) ... ok
test_hook_composition_pins_sessionstart_order (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_pins_sessionstart_order) ... ok
test_hook_composition_rejects_duplicate_command (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_rejects_duplicate_command) ... ok
test_hook_composition_rejects_sync_timeout_over_budget (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_rejects_sync_timeout_over_budget) ... ok
test_hook_composition_requires_permgate_first (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_requires_permgate_first) ... ok
test_manifest_home_paths_allow_chezmoi_home_dir (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_allow_chezmoi_home_dir) ... ok
test_manifest_home_paths_allow_flow_style_projects (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_allow_flow_style_projects) ... ok
test_manifest_home_paths_exempt_runtime_owned_projects (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_exempt_runtime_owned_projects) ... ok
test_manifest_home_paths_only_exempt_the_projects_subtree (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_only_exempt_the_projects_subtree) ... ok
test_manifest_home_paths_reject_hard_coded_home (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_reject_hard_coded_home) ... ok
test_manifest_home_paths_reject_hard_coded_linux_home (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_reject_hard_coded_linux_home) ... ok
test_manifest_home_paths_reject_non_codex_projects_mapping (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_reject_non_codex_projects_mapping) ... ok
test_permgate_policy_requires_a_schema_3_object (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_permgate_policy_requires_a_schema_3_object) ... ok
test_recursive_scans_skip_gitignored_local_state (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_recursive_scans_skip_gitignored_local_state) ... ok
test_recursive_scans_skip_nested_git_trees_only (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_recursive_scans_skip_nested_git_trees_only) ... ok
test_repo_claude_settings_accept_portable_interpreter (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_repo_claude_settings_accept_portable_interpreter) ... ok
test_repo_claude_settings_reject_machine_specific_interpreter (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_repo_claude_settings_reject_machine_specific_interpreter) ... ERROR: /tmp/claude-501/validate-agent-assets-test-36qnevnk/.claude/settings.json hook SessionEnd must not hard-code a machine-specific home path: ~/.local/share/mise/installs/python/3.14.7/bin/python3.14
ok
test_runner_homes_match_anywhere (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_runner_homes_match_anywhere) ... ok
test_secret_scan_allows_exact_placeholder_tokens (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_allows_exact_placeholder_tokens) ... ok
test_secret_scan_checks_docs_paths (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_checks_docs_paths) ... ok
test_secret_scan_checks_extensionless_executables (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_checks_extensionless_executables) ... ok
test_secret_scan_checks_utf16_bom_text (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_checks_utf16_bom_text) ... ok
test_secret_scan_fails_a_nul_in_orchestration_text_and_skips_other_binaries (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_fails_a_nul_in_orchestration_text_and_skips_other_binaries) ... ok
test_secret_scan_flags_the_running_users_home_as_a_backstop (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_flags_the_running_users_home_as_a_backstop) ... ok
test_secret_scan_reads_json_per_key_and_string_value (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_reads_json_per_key_and_string_value) ... ok
test_secret_scan_rejects_home_paths_in_orchestration_evidence_only (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_rejects_home_paths_in_orchestration_evidence_only) ... ok
test_secret_scan_rejects_placeholder_with_suffix (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_rejects_placeholder_with_suffix) ... ok
test_secret_scan_rejects_utf16_orchestration_text_with_the_nul_offset (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_rejects_utf16_orchestration_text_with_the_nul_offset) ... ok

----------------------------------------------------------------------
Ran 98 tests in 2.042s

OK
(exit 0)
```

```console
$ ruff check --config ruff.toml --output-format concise scripts/validate-agent-assets.py tests/unit/test_validate_agent_assets.py
scripts/validate-agent-assets.py:1:1: EXE001 Shebang is present but file is not executable
scripts/validate-agent-assets.py:4:1: I001 [*] Import block is un-sorted or un-formatted
scripts/validate-agent-assets.py:133:9: SIM102 Use a single `if` statement instead of nested `if` statements
scripts/validate-agent-assets.py:867:12: C401 Unnecessary generator (rewrite as a set comprehension)
scripts/validate-agent-assets.py:924:18: UP022 Prefer `capture_output` over sending `stdout` and `stderr` to `PIPE`
tests/unit/test_validate_agent_assets.py:1:1: EXE001 Shebang is present but file is not executable
tests/unit/test_validate_agent_assets.py:252:13: FLY002 Consider f-string instead of string join
tests/unit/test_validate_agent_assets.py:1634:41: UP037 [*] Remove quotes from type annotation
Found 8 errors.
[*] 2 fixable with `--fix` (3 unsafe fixes available with `--fix --unsafe-fixes`).
(exit 1)
$ ruff format --config ruff.toml --check scripts/validate-agent-assets.py tests/unit/test_validate_agent_assets.py
2 files already formatted
(exit 0)
```

```console
$ uv run --offline --with pyyaml scripts/validate-agent-assets.py > "$TMPDIR/t129/16-p1-validator.txt" 2>&1; echo "rc=$?"   # 193 s, after the fix
rc=0
$ grep -v "^WARN: regime-boundary:" "$TMPDIR/t129/16-p1-validator.txt"
agent asset validation ok
(exit 0)
$ grep -c "^WARN: regime-boundary:" "$TMPDIR/t129/16-p1-validator.txt"
757
(exit 0)
```
