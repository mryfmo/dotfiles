---
task_id: dotfiles-T129-anthropic-auth-route-check-followup-a01
seat: claude-standard-dot-a007
---

# Validation: dotfiles-T129-anthropic-auth-route-check-followup-a01

Every command ran from the worktree `.claude/worktrees/worker-c` on the branch `tools/anthropic-auth-route-structured` (from PR #389's head 862ab31c; the code commit 7ee711cc), inside the sandbox, before the evidence commit; `MAIN` names the main checkout and `T` the task id. The output is verbatim, with the home directory replaced by `~` and the main checkout by `$MAIN`; each block ends with the exit status of the command shown. Section 8 follows the rebase onto origin/main after #389 merges.

## 1. Task file and task copy (amendment 2)

```console
$ shasum -a 256 "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md"; cmp "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md" && echo byte-identical
52db410226c5361d3a8400ffe429acf7def38bb9973006a20126ee97324eee1d  $MAIN/.orchestration/tasks/dotfiles-T129-anthropic-auth-route-check-followup-a01.md
52db410226c5361d3a8400ffe429acf7def38bb9973006a20126ee97324eee1d  .orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a01/task.md
byte-identical
(exit 0)
$ UV_OFFLINE=1 uv run --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py --root "$PWD" "$MAIN/.orchestration/tasks/$T.md"
dotfiles-T129-anthropic-auth-route-check-followup-a01.md: OK
(exit 0)
```

## 2. The format of each structured source, and the check on this tree

Amendment 1: the format is decided after stripping chezmoi's attribute prefixes; the eight `modify_` sources are text. The check runs on this worktree's tracked tree and refuses nothing.

```python
import importlib.util, collections
spec = importlib.util.spec_from_file_location("v", "scripts/validate-agent-assets.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
names = open(__import__("sys").argv[1]).read().split()
print(collections.Counter(str(m.applied_file_format(n)) for n in names))
print([n for n in names if m.applied_file_format(n) is None])
m.validate_anthropic_auth_route()
print("real tree: no refusal")
```

```console
$ git ls-files -- home install | grep -E "\.(json|toml|ya?ml)$" > structured.txt; wc -l < structured.txt
      35
(exit 0)
$ uv run --offline --no-project --with pyyaml python -I classify.py structured.txt   # the format of each structured source, and the check on this tree; the script is pasted above
Counter({'toml': 13, 'yaml': 8, 'None': 8, 'json': 6})
['home/dot_claude/modify_private_settings.json', 'home/dot_codex/modify_private_audit.config.toml', 'home/dot_codex/modify_private_config.toml', 'home/dot_codex/modify_private_deep.config.toml', 'home/dot_codex/modify_private_express.config.toml', 'home/dot_codex/modify_private_review.config.toml', 'home/dot_codex/modify_private_security.config.toml', 'home/dot_codex/modify_private_standard.config.toml']
real tree: no refusal
(exit 0)
```

## 3. The diff against 862ab31c

```console
$ git diff 862ab31c11edc0ba0c8830a19946d8b04dd01955 -- scripts tests
diff --git a/scripts/validate-agent-assets.py b/scripts/validate-agent-assets.py
index 6fbdfdd3..ca159ab5 100644
--- a/scripts/validate-agent-assets.py
+++ b/scripts/validate-agent-assets.py
@@ -1572,39 +1572,149 @@ def validate_no_obvious_secrets() -> None:
             )
 
 
-# R2: an assignment (`=`, `:` or Bash's `+=`, the name bare or in matching quotes as a JSON, YAML or TOML key) whose
-# whole value, up to the end of the line or a `#` comment after whitespace, is not one `$NAME`/`${NAME}` reference,
-# one `{{ }}` template or empty, each optionally quoted. Anything else is a literal Bash could assign: `$'...'`,
-# `$"..."`, `$(...)`, `${NAME:-...}`, or a reference with more after it.
+# R2 on text (shell, templates, chezmoi scripts): an assignment (`=`, `:` or Bash's `+=`, the name bare or in matching
+# quotes) whose whole value, up to the end of the line or a `#` comment after whitespace, is not one `$NAME`/`${NAME}`
+# reference (bare or double-quoted: Bash expands nothing inside single quotes), one `{{ }}` template (optionally
+# quoted) or empty. Anything else is a literal Bash could assign: `$'...'`, `$"..."`, `$(...)`, `${NAME:-...}`, or a
+# reference with more after it.
 ANTHROPIC_API_KEY_LITERAL = re.compile(
     r"""(?P<k>["']?)ANTHROPIC_API_KEY(?P=k)\s*(?:\+?=|:)(?!\s*(?:"""
-    r"""(?P<q>["']?)\$(?:[A-Za-z_][A-Za-z0-9_]*|\{[A-Za-z_][A-Za-z0-9_]*\})(?P=q)"""
+    r"""(?P<q>"?)\$(?:[A-Za-z_][A-Za-z0-9_]*|\{[A-Za-z_][A-Za-z0-9_]*\})(?P=q)"""
     r"""|(?P<t>["']?)\{\{(?:(?!\}\}).)*\}\}(?P=t)|""|'')?\s*(?:(?<=\s)#.*)?$)"""
 )
+# R2 on parsed data, where the value is already unquoted: one reference, one template, or empty.
+ANTHROPIC_API_KEY_DATA = re.compile(r"\$(?:[A-Za-z_][A-Za-z0-9_]*|\{[A-Za-z_][A-Za-z0-9_]*\})|\{\{(?:(?!\}\}).)*\}\}|")
+CHEZMOI_FILE_ATTRIBUTES = frozenset(
+    {
+        *("after", "before", "create", "dot", "empty", "encrypted", "executable", "literal"),
+        *("modify", "once", "onchange", "private", "readonly", "remove", "run", "symlink"),
+    }
+)
+# A chezmoi source with one of these holds a script, a link target or ciphertext, not the target's data.
+CHEZMOI_NOT_DATA = frozenset({"encrypted", "modify", "run", "symlink"})
+PARSED_SUFFIXES = {".json": "json", ".toml": "toml", ".yaml": "yaml", ".yml": "yaml"}
+
+
+class JsonPairs(list):
+    """A JSON object as its (key, value) pairs, so a duplicate key cannot hide behind the last one."""
+
+
+def applied_file_format(name: str) -> str | None:
+    """`json`, `toml` or `yaml` for an applied file the check parses; None for text, as its chezmoi name decides."""
+    base = name.rsplit("/", 1)[-1]
+    while "_" in base and (attribute := base.split("_", 1)[0]) in CHEZMOI_FILE_ATTRIBUTES:
+        if attribute in CHEZMOI_NOT_DATA:
+            return None
+        base = base.split("_", 1)[1]
+        if attribute == "literal":
+            break
+    return PARSED_SUFFIXES.get(Path(base).suffix)
+
+
+def parsed_entry(node: Any) -> tuple[str, Any]:
+    """A JSON or TOML value, or a YAML node, as ("map", pairs), ("seq", items), ("str", text), ("null"|"other", None)."""
+    if yaml is not None and isinstance(node, yaml.Node):
+        if isinstance(node, yaml.MappingNode):
+            return "map", [(key.value if isinstance(key, yaml.ScalarNode) else "", value) for key, value in node.value]
+        if isinstance(node, yaml.SequenceNode):
+            return "seq", node.value
+        tag = node.tag.rsplit(":", 1)[-1]
+        return ("str", node.value) if tag == "str" else ("null" if tag == "null" else "other", None)
+    if isinstance(node, JsonPairs):
+        return "map", list(node)
+    if isinstance(node, dict):
+        return "map", list(node.items())
+    if isinstance(node, list):
+        return "seq", node
+    if isinstance(node, str):
+        return "str", node
+    return ("null" if node is None else "other"), None
+
+
+def anthropic_text_findings(text: str, where: str) -> list[tuple[str, str, str]]:
+    """R1 and the text form of R2 on one decoded key or string (a string may hold an env line or embedded shell)."""
+    found = []
+    if "ANTHROPIC_OAUTH_TOKEN" in text:
+        found.append(("R1", where, "names ANTHROPIC_OAUTH_TOKEN; Anthropic is reached by API key only"))
+    if any(ANTHROPIC_API_KEY_LITERAL.search(line) for line in text.splitlines()):
+        found.append(("R2", where, "a string assigns ANTHROPIC_API_KEY a literal; reference the environment"))
+    return found
+
+
+def anthropic_parsed_findings(rel: str, fmt: str, text: str) -> list[tuple[str, str, str]]:
+    """(rule, key path, reason) for each refusal in a parsed applied file; a file that does not parse is refused."""
+    if fmt == "yaml" and yaml is None:
+        fail("PyYAML is required")
+    errors = (ValueError, RecursionError) + ((yaml.YAMLError,) if yaml is not None else ())
+    try:
+        if fmt == "json":
+            roots = [json.loads(text, object_pairs_hook=JsonPairs)]
+        elif fmt == "toml":
+            roots = [tomllib.loads(text)]
+        else:
+            roots = list(yaml.compose_all(text, Loader=yaml.SafeLoader))
+    except errors as error:
+        # The type only: a parser's message can quote the file, and the file may hold a key.
+        fail(f"{rel}: cannot be parsed as {fmt} ({type(error).__name__}); the Anthropic auth route check refuses it")
+    found, seen, stack = [], set(), [(root, "") for root in roots]
+    while stack:
+        node, where = stack.pop()
+        kind, payload = parsed_entry(node)
+        if kind in ("map", "seq"):
+            # Each container once: a YAML alias shares its node, so anchors cannot multiply the walk.
+            if id(node) in seen:
+                continue
+            seen.add(id(node))
+        if kind == "map":
+            for key, child in payload:
+                here = f"{where}.{key}" if where else str(key)
+                found += anthropic_text_findings(str(key), here)
+                child_kind, child_text = parsed_entry(child)
+                # Only null or an allowed string passes: a number, a boolean, a mapping or a list is no reference.
+                allowed = child_kind == "null" or (
+                    child_kind == "str" and ANTHROPIC_API_KEY_DATA.fullmatch(child_text) is not None
+                )
+                if str(key).endswith("ANTHROPIC_API_KEY") and not allowed:
+                    found.append(("R2", here, "assigns ANTHROPIC_API_KEY a literal; reference the environment"))
+                stack.append((child, here))
+        elif kind == "seq":
+            stack.extend((child, f"{where}[{index}]") for index, child in enumerate(payload))
+        elif kind == "str":
+            found += anthropic_text_findings(payload, where)
+    return found
 
 
 def validate_anthropic_auth_route() -> None:
-    """Plan 023 PR D: the applied files reach Anthropic through ANTHROPIC_API_KEY from the environment only."""
+    """Plan 023 PR D: the applied files reach Anthropic through ANTHROPIC_API_KEY from the environment only.
+
+    JSON, TOML and YAML are read through their parsers, so a key name is decoded and a value is data; every other file
+    (shell, templates, chezmoi scripts) is read line by line.
+    """
     listed = subprocess.run(
         ["git", "-C", str(ROOT), "ls-files", "-z", "--", "home", "install"], capture_output=True, check=False
     )
     if listed.returncode != 0:
         fail(f"git ls-files failed, so the Anthropic auth route check cannot run: {os.fsdecode(listed.stderr).strip()}")
     for name in filter(None, listed.stdout.split(b"\0")):
-        path = ROOT / os.fsdecode(name)
+        rel = os.fsdecode(name)
+        path = ROOT / rel
         # A tracked symlink is not followed: on a PR checkout it could point at a device and hang the run.
         if path.is_symlink() or not path.is_file():
             continue
-        for number, line in enumerate(path.read_bytes().decode("utf-8", errors="replace").splitlines(), 1):
+        text = path.read_bytes().decode("utf-8", errors="replace")
+        parsed = applied_file_format(rel)
+        for number, line in enumerate(text.splitlines(), 1):
             # The file, the line number and the rule only: the line itself may hold a real key, and CI logs are public.
             if "ANTHROPIC_OAUTH_TOKEN" in line:
-                fail(
-                    f"{os.fsdecode(name)}:{number}: R1: names ANTHROPIC_OAUTH_TOKEN; Anthropic is reached by API key only"
-                )
-            if ANTHROPIC_API_KEY_LITERAL.search(line):
-                fail(
-                    f"{os.fsdecode(name)}:{number}: R2: assigns ANTHROPIC_API_KEY a literal; reference the environment"
-                )
+                fail(f"{rel}:{number}: R1: names ANTHROPIC_OAUTH_TOKEN; Anthropic is reached by API key only")
+            # A parsed file reads R2 from its data below, where quotes, escapes and delimiters are syntax.
+            if parsed is None and ANTHROPIC_API_KEY_LITERAL.search(line):
+                fail(f"{rel}:{number}: R2: assigns ANTHROPIC_API_KEY a literal; reference the environment")
+        if parsed is not None:
+            # The key path names where, escaped: a key is PR text, and a newline in it could forge a CI log line
+            # or a workflow command. A value is never printed.
+            for rule, where, reason in anthropic_parsed_findings(rel, parsed, text):
+                fail(f"{rel}: {rule}: {where.encode('unicode_escape').decode('ascii')}: {reason}")
 
 
 def validate_compactiondb_project_copy() -> None:
diff --git a/tests/unit/test_validate_agent_assets.py b/tests/unit/test_validate_agent_assets.py
index a9bee6e7..c95a8e07 100644
--- a/tests/unit/test_validate_agent_assets.py
+++ b/tests/unit/test_validate_agent_assets.py
@@ -1419,23 +1419,31 @@ class ValidateAgentAssetsTest(unittest.TestCase):
         with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
             self.module.validate_no_obvious_secrets()
 
-    def anthropic_route_fixture(self):
-        """One tracked file under home/, install/ and scripts/, and check(rel, line) -> (refused, stderr)."""
-        files = ("home/dot_config/fixture.sh", "install/fixture.sh", "scripts/fixture.sh")
+    def anthropic_route_fixture(self, *extra: str):
+        """One tracked file under home/, install/ and scripts/ (and each extra), and check(rel, line) -> (refused, stderr).
+
+        check writes `# fixture` and the line, or with verbatim=True the text as given (JSON has no comments); between
+        checks every file holds an empty document, so each check sees one fixture.
+        """
+        files = ("home/dot_config/fixture.sh", "install/fixture.sh", "scripts/fixture.sh", *extra)
+
+        def empty(rel: str) -> str:
+            return "{}\n" if rel.endswith(".json") else ""
+
         for rel in files:
-            self.write_text_file(rel, "")
+            self.write_text_file(rel, empty(rel))
         subprocess.run(["git", "init", "-q", str(self.temp_dir)], check=True)
         subprocess.run(["git", "-C", str(self.temp_dir), "add", *files], check=True)
 
-        def check(rel: str, line: str) -> tuple[bool, str]:
-            self.write_text_file(rel, f"# fixture\n{line}\n")
+        def check(rel: str, line: str, verbatim: bool = False) -> tuple[bool, str]:
+            self.write_text_file(rel, line if verbatim else f"# fixture\n{line}\n")
             stderr, refused = io.StringIO(), False
             with contextlib.redirect_stderr(stderr):
                 try:
                     self.module.validate_anthropic_auth_route()
                 except SystemExit:
                     refused = True
-            self.write_text_file(rel, "")
+            self.write_text_file(rel, empty(rel))
             return refused, stderr.getvalue()
 
         return files, check
@@ -1508,7 +1516,6 @@ class ValidateAgentAssetsTest(unittest.TestCase):
             f"{key}=$DEPLOYED_KEY",
             f"{key}=${{DEPLOYED_KEY}}",
             f'{key}="$DEPLOYED_KEY"',
-            f"{key}='${{DEPLOYED_KEY}}'",
             f'{key}: "{{{{ .anthropic }}}}"',
             f"{key}=$DEPLOYED_KEY  # from the environment",
         ):
@@ -1545,12 +1552,118 @@ class ValidateAgentAssetsTest(unittest.TestCase):
         for line in (
             f'"{key}": "${{{key}}}"',
             f'"{key}": "{{{{ .anthropic }}}}"',
-            f"'{key}' = '${{{key}}}'",
             f"{key}+=${key}",
         ):
             with self.subTest(line=line):
                 self.assertEqual((False, ""), check(home, line))
 
+    def assert_parsed_refusals(self, check, cases, line_grammar_misses: bool) -> None:
+        """Each (rel, text, rule, where) is refused naming the key path, never the literal value."""
+        for rel, text, rule, where in cases:
+            with self.subTest(rel=rel, text=text):
+                if line_grammar_misses:
+                    lines = text.splitlines()
+                    self.assertFalse(any(self.module.ANTHROPIC_API_KEY_LITERAL.search(line) for line in lines))
+                    self.assertFalse(any("ANTHROPIC_OAUTH_" + "TOKEN" in line for line in lines))
+                refused, stderr = check(rel, text, verbatim=True)
+                self.assertTrue(refused)
+                self.assertIn(f"ERROR: {rel}: {rule}: {where}:", stderr)
+                self.assertNotIn("literal-value", stderr)
+
+    def test_anthropic_auth_route_reads_json_and_toml_through_their_parsers(self) -> None:
+        # The re-plan of 4302758230 (escaped-name): a parsed format's key names are decoded and its values are data, so
+        # escapes, key quoting and line breaks no longer hide an assignment the line grammar cannot see.
+        key, oauth = "ANTHROPIC_API_" + "KEY", "ANTHROPIC_OAUTH_" + "TOKEN"
+        escaped_key, escaped_oauth = "ANTHROPIC_API_\\u004b" + "EY", "ANTHROPIC_OAUTH_\\u0054" + "OKEN"
+        json_rel, toml_rel = "home/dot_config/fixture.json", "home/dot_config/fixture.toml"
+        script_rel = "home/dot_config/modify_private_fixture.json"
+        _, check = self.anthropic_route_fixture(json_rel, toml_rel, script_rel)
+        refused_by_the_parse_only = (
+            (toml_rel, f'"{escaped_key}" = "literal-value"\n', "R2", key),
+            (json_rel, f'{{"{escaped_key}": "literal-value"}}\n', "R2", key),
+            (json_rel, f'{{"env": {{"{key}":\n"literal-value"}}}}\n', "R2", f"env.{key}"),
+            (json_rel, f'{{"env": ["{escaped_key}=literal-value"]}}\n', "R2", "env[0]"),
+            (toml_rel, f'"{escaped_oauth}" = "x"\n', "R1", oauth),
+        )
+        self.assert_parsed_refusals(check, refused_by_the_parse_only, line_grammar_misses=True)
+        self.assert_parsed_refusals(
+            check,
+            (
+                (json_rel, f'{{"{escaped_key}": "literal-value", "{key}": "${{{key}}}"}}\n', "R2", key),  # a duplicate
+                (json_rel, f'{{"{key}": 12}}\n', "R2", key),
+                # A key with a newline is printed escaped, so it cannot start a log line of its own.
+                (json_rel, f'{{"a\\n::error::x": {{"{key}": "literal-value"}}}}\n', "R2", f"a\\n::error::x.{key}"),
+            ),
+            line_grammar_misses=False,
+        )
+        for rel, text in (
+            (toml_rel, f'{key} = "${{{key}}}"\n'),
+            (toml_rel, f'[env]\n{key} = "{{{{ .anthropic }}}}"\n'),
+            (json_rel, f'{{"{key}": "", "apiKeyEnv": "{key}"}}\n'),
+            (script_rel, f"#!/bin/sh\n{key}=${key}\n"),  # a chezmoi modify_ source is a script, read as text
+        ):
+            with self.subTest(rel=rel, text=text):
+                self.assertEqual((False, ""), check(rel, text, verbatim=True))
+        refused, stderr = check(script_rel, f"#!/bin/sh\n{key}=literal-value\n", verbatim=True)
+        self.assertTrue(refused)
+        self.assertIn(f"ERROR: {script_rel}:2: R2:", stderr)
+        refused, stderr = check(json_rel, "{\n", verbatim=True)  # a parse failure is a refusal, never a skip
+        self.assertTrue(refused)
+        self.assertIn(f"ERROR: {json_rel}: cannot be parsed as json", stderr)
+
+    @unittest.skipUnless(importlib.util.find_spec("yaml"), "PyYAML is not installed")
+    def test_anthropic_auth_route_reads_yaml_through_its_parser(self) -> None:
+        # The re-plan of 4302758230 for YAML: the node graph keeps duplicate keys and decodes quoted escapes.
+        key, escaped_key = "ANTHROPIC_API_" + "KEY", "ANTHROPIC_API_\\u004b" + "EY"
+        yaml_rel = "home/dot_config/fixture.yaml"
+        _, check = self.anthropic_route_fixture(yaml_rel)
+        self.assert_parsed_refusals(
+            check,
+            (
+                (yaml_rel, f'"{escaped_key}": literal-value\n', "R2", key),
+                (yaml_rel, f"env:\n  {key}:\n    literal-value\n", "R2", f"env.{key}"),
+                (yaml_rel, f"{key}:\n  literal-value\n", "R2", key),
+            ),
+            line_grammar_misses=True,
+        )
+        self.assert_parsed_refusals(
+            check,
+            ((yaml_rel, f'"{escaped_key}": literal-value\n{key}: ${key}\n', "R2", key),),
+            line_grammar_misses=False,
+        )
+        for text in (f"{key}: ${key}\n", f"{key}:\n", f'{key}: "{{{{ .anthropic }}}}"\n', "a: &a [x]\nb: [*a, *a]\n"):
+            with self.subTest(text=text):
+                self.assertEqual((False, ""), check(yaml_rel, text, verbatim=True))
+        refused, stderr = check(yaml_rel, "a: [\n", verbatim=True)
+        self.assertTrue(refused)
+        self.assertIn(f"ERROR: {yaml_rel}: cannot be parsed as yaml", stderr)
+
+    def test_anthropic_auth_route_refuses_a_single_quoted_reference_in_text(self) -> None:
+        # Row 4302758234: Bash expands nothing inside single quotes, so '$NAME' assigns the text $NAME; in text a
+        # reference passes bare or double-quoted only. A TOML literal string is data, so the parser reads it.
+        key = "ANTHROPIC_API_" + "KEY"
+        toml_rel = "home/dot_config/fixture.toml"
+        (home, *_), check = self.anthropic_route_fixture(toml_rel)
+        for line in (f"{key}='$DEPLOYED_KEY'", f"{key}='${{DEPLOYED_KEY}}'", f"'{key}' = '${{{key}}}'"):
+            with self.subTest(line=line):
+                refused, stderr = check(home, line)
+                self.assertTrue(refused)
+                self.assertIn(f"ERROR: {home}:2: R2:", stderr)
+        for line in (f'{key}="$DEPLOYED_KEY"', f"{key}=$DEPLOYED_KEY", f"{key}='{{{{ .anthropic }}}}'"):
+            with self.subTest(line=line):
+                self.assertEqual((False, ""), check(home, line))
+        self.assertEqual((False, ""), check(toml_rel, f"'{key}' = '${{{key}}}'\n", verbatim=True))
+
+    def test_anthropic_auth_route_reads_a_json_reference_before_a_delimiter(self) -> None:
+        # Row 4302758239: in JSON a comma or a brace after the value is syntax; the parser reads the value alone, where
+        # the line grammar refused the line.
+        key = "ANTHROPIC_API_" + "KEY"
+        json_rel = "home/dot_config/fixture.json"
+        _, check = self.anthropic_route_fixture(json_rel)
+        text = f'{{"{key}": "${{{key}}}", "x": 1}}\n'
+        self.assertIsNotNone(self.module.ANTHROPIC_API_KEY_LITERAL.search(text))
+        self.assertEqual((False, ""), check(json_rel, text, verbatim=True))
+
     def write_manifest(self, hook_command: str) -> None:
         path = self.temp_dir / "home/dot_agents/agent-config.yaml"
         path.parent.mkdir(parents=True, exist_ok=True)
(exit 0)
$ git diff --numstat 862ab31c11edc0ba0c8830a19946d8b04dd01955 -- scripts tests
125	15	scripts/validate-agent-assets.py
122	9	tests/unit/test_validate_agent_assets.py
(exit 0)
```

## 4. The new tests on 862ab31c's validator, and one mutant per property

Each variant is written over `scripts/validate-agent-assets.py`, the eight route tests run with PyYAML (so the YAML test runs), and the branch file is written back and compared byte for byte. On 862ab31c's validator the four new tests fail 19 subtests; each mutant fails at least one.

```python
"""The follow-up's route tests against 862ab31c's validator and one mutant per property of the parser-based check.

Each variant is written over scripts/validate-agent-assets.py, the tests run (with PyYAML, so the YAML test runs), and
the branch file is written back and compared byte for byte. Mutants are literal string replacements asserted to match
once.
"""

import re
import subprocess
from pathlib import Path

script = Path("scripts/validate-agent-assets.py")
fixed = script.read_text()
before = subprocess.run(
    ["git", "show", "862ab31c11edc0ba0c8830a19946d8b04dd01955:" + str(script)],
    capture_output=True,
    text=True,
    check=True,
).stdout
prefix = "tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_auth_route_"
tests = [
    prefix + name
    for name in (
        "reads_json_and_toml_through_their_parsers",
        "reads_yaml_through_its_parser",
        "refuses_a_single_quoted_reference_in_text",
        "reads_a_json_reference_before_a_delimiter",
        "refuses_an_oauth_token_in_applied_files_and_a_literal_api_key_assignment",
        "r2_accepts_only_a_whole_value_reference_template_or_empty",
        "reads_a_comment_after_an_empty_value_as_empty",
        "r2_reaches_a_quoted_key_and_a_compound_assignment",
    )
]


def mutate(old, new):
    assert fixed.count(old) == 1, old
    return fixed.replace(old, new)


variants = [
    ("862ab31c's validator (the line grammar for every file)", before),
    (
        "mutant: JSON duplicates collapse (no pairs hook)",
        mutate("json.loads(text, object_pairs_hook=JsonPairs)", "json.loads(text)"),
    ),
    (
        "mutant: the line grammar's R2 also runs on parsed files",
        mutate(
            "if parsed is None and ANTHROPIC_API_KEY_LITERAL",
            "if ANTHROPIC_API_KEY_LITERAL",
        ),
    ),
    (
        "mutant: a parse failure is skipped",
        mutate(
            "    except errors as error:\n",
            "    except errors as error:\n        return []\n",
        ),
    ),
    (
        "mutant: a single-quoted reference passes in text",
        mutate('(?P<q>"?)', """(?P<q>["']?)"""),
    ),
    (
        "mutant: a chezmoi modify_ source is parsed",
        mutate(
            'frozenset({"encrypted", "modify", "run", "symlink"})',
            'frozenset({"encrypted", "run", "symlink"})',
        ),
    ),
    (
        "mutant: decoded strings are not read",
        mutate(
            "            found += anthropic_text_findings(payload, where)\n",
            "            pass\n",
        ),
    ),
    (
        "mutant: a decoded key is not compared",
        mutate(
            'if str(key).endswith("ANTHROPIC_API_KEY") and not allowed:', "if False:"
        ),
    ),
    (
        "mutant: the key path is printed unescaped",
        mutate("{where.encode('unicode_escape').decode('ascii')}", "{where}"),
    ),
]
try:
    for name, body in variants:
        script.write_text(body)
        result = subprocess.run(
            [
                "uv",
                "run",
                "--offline",
                "--with",
                "pyyaml",
                "python",
                "-m",
                "unittest",
                *tests,
            ],
            capture_output=True,
            text=True,
        )
        failing = sorted(
            {
                m.group(1) + " " + (m.group(2) or "")
                for m in re.finditer(
                    r"^(?:FAIL|ERROR): (test_\w+) .*?(\((?:rel|line|text)=.*\))?$",
                    result.stderr,
                    re.M,
                )
            }
        )
        tail = [x for x in result.stderr.splitlines() if x.startswith(("OK", "FAILED"))]
        print(f"{name}: rc={result.returncode} {' | '.join(tail)}")
        for f in failing:
            print(f"    failing: {f[:200]}")
finally:
    script.write_text(fixed)
print("restored byte-identical:", script.read_text() == fixed)
```

```console
$ uv run --offline --no-project python -I t129f_mutants.py   # from the worktree root; the script is pasted above
862ab31c's validator (the line grammar for every file): rc=1 FAILED (failures=19)
    failing: test_anthropic_auth_route_reads_a_json_reference_before_a_delimiter 
    failing: test_anthropic_auth_route_reads_json_and_toml_through_their_parsers 
    failing: test_anthropic_auth_route_reads_json_and_toml_through_their_parsers (rel='home/dot_config/fixture.json', text='{"ANTHROPIC_API_KEY": "", "apiKeyEnv": "ANTHROPIC_API_KEY"}\n')
    failing: test_anthropic_auth_route_reads_json_and_toml_through_their_parsers (rel='home/dot_config/fixture.json', text='{"ANTHROPIC_API_KEY": 12}\n')
    failing: test_anthropic_auth_route_reads_json_and_toml_through_their_parsers (rel='home/dot_config/fixture.json', text='{"ANTHROPIC_API_\\u004bEY": "literal-value", "ANTHROPIC_API_KEY": "${ANTHROPIC_API_KEY}"}
    failing: test_anthropic_auth_route_reads_json_and_toml_through_their_parsers (rel='home/dot_config/fixture.json', text='{"ANTHROPIC_API_\\u004bEY": "literal-value"}\n')
    failing: test_anthropic_auth_route_reads_json_and_toml_through_their_parsers (rel='home/dot_config/fixture.json', text='{"a\\n::error::x": {"ANTHROPIC_API_KEY": "literal-value"}}\n')
    failing: test_anthropic_auth_route_reads_json_and_toml_through_their_parsers (rel='home/dot_config/fixture.json', text='{"env": ["ANTHROPIC_API_\\u004bEY=literal-value"]}\n')
    failing: test_anthropic_auth_route_reads_json_and_toml_through_their_parsers (rel='home/dot_config/fixture.json', text='{"env": {"ANTHROPIC_API_KEY":\n"literal-value"}}\n')
    failing: test_anthropic_auth_route_reads_json_and_toml_through_their_parsers (rel='home/dot_config/fixture.toml', text='"ANTHROPIC_API_\\u004bEY" = "literal-value"\n')
    failing: test_anthropic_auth_route_reads_json_and_toml_through_their_parsers (rel='home/dot_config/fixture.toml', text='"ANTHROPIC_OAUTH_\\u0054OKEN" = "x"\n')
    failing: test_anthropic_auth_route_reads_yaml_through_its_parser 
    failing: test_anthropic_auth_route_reads_yaml_through_its_parser (rel='home/dot_config/fixture.yaml', text='"ANTHROPIC_API_\\u004bEY": literal-value\n')
    failing: test_anthropic_auth_route_reads_yaml_through_its_parser (rel='home/dot_config/fixture.yaml', text='"ANTHROPIC_API_\\u004bEY": literal-value\nANTHROPIC_API_KEY: $ANTHROPIC_API_KEY\n')
    failing: test_anthropic_auth_route_reads_yaml_through_its_parser (rel='home/dot_config/fixture.yaml', text='ANTHROPIC_API_KEY:\n  literal-value\n')
    failing: test_anthropic_auth_route_reads_yaml_through_its_parser (rel='home/dot_config/fixture.yaml', text='env:\n  ANTHROPIC_API_KEY:\n    literal-value\n')
    failing: test_anthropic_auth_route_refuses_a_single_quoted_reference_in_text (line="'ANTHROPIC_API_KEY' = '${ANTHROPIC_API_KEY}'")
    failing: test_anthropic_auth_route_refuses_a_single_quoted_reference_in_text (line="ANTHROPIC_<redacted:secret-pattern>")
    failing: test_anthropic_auth_route_refuses_a_single_quoted_reference_in_text (line="ANTHROPIC_<redacted:secret-pattern>")
mutant: JSON duplicates collapse (no pairs hook): rc=1 FAILED (failures=1)
    failing: test_anthropic_auth_route_reads_json_and_toml_through_their_parsers (rel='home/dot_config/fixture.json', text='{"ANTHROPIC_API_\\u004bEY": "literal-value", "ANTHROPIC_API_KEY": "${ANTHROPIC_API_KEY}"}
mutant: the line grammar's R2 also runs on parsed files: rc=1 FAILED (failures=6)
    failing: test_anthropic_auth_route_reads_a_json_reference_before_a_delimiter 
    failing: test_anthropic_auth_route_reads_json_and_toml_through_their_parsers (rel='home/dot_config/fixture.json', text='{"ANTHROPIC_API_KEY": "", "apiKeyEnv": "ANTHROPIC_API_KEY"}\n')
    failing: test_anthropic_auth_route_reads_json_and_toml_through_their_parsers (rel='home/dot_config/fixture.json', text='{"ANTHROPIC_API_KEY": 12}\n')
    failing: test_anthropic_auth_route_reads_json_and_toml_through_their_parsers (rel='home/dot_config/fixture.json', text='{"ANTHROPIC_API_\\u004bEY": "literal-value", "ANTHROPIC_API_KEY": "${ANTHROPIC_API_KEY}"}
    failing: test_anthropic_auth_route_reads_json_and_toml_through_their_parsers (rel='home/dot_config/fixture.json', text='{"a\\n::error::x": {"ANTHROPIC_API_KEY": "literal-value"}}\n')
    failing: test_anthropic_auth_route_refuses_a_single_quoted_reference_in_text 
mutant: a parse failure is skipped: rc=1 FAILED (failures=2)
    failing: test_anthropic_auth_route_reads_json_and_toml_through_their_parsers 
    failing: test_anthropic_auth_route_reads_yaml_through_its_parser 
mutant: a single-quoted reference passes in text: rc=1 FAILED (failures=3)
    failing: test_anthropic_auth_route_refuses_a_single_quoted_reference_in_text (line="'ANTHROPIC_API_KEY' = '${ANTHROPIC_API_KEY}'")
    failing: test_anthropic_auth_route_refuses_a_single_quoted_reference_in_text (line="ANTHROPIC_<redacted:secret-pattern>")
    failing: test_anthropic_auth_route_refuses_a_single_quoted_reference_in_text (line="ANTHROPIC_<redacted:secret-pattern>")
mutant: a chezmoi modify_ source is parsed: rc=1 FAILED (failures=2)
    failing: test_anthropic_auth_route_reads_json_and_toml_through_their_parsers 
    failing: test_anthropic_auth_route_reads_json_and_toml_through_their_parsers (rel='home/dot_config/modify_private_fixture.json', text='#!/bin/sh\nANTHROPIC_API_KEY=$ANTHROPIC_API_KEY\n')
mutant: decoded strings are not read: rc=1 FAILED (failures=1)
    failing: test_anthropic_auth_route_reads_json_and_toml_through_their_parsers (rel='home/dot_config/fixture.json', text='{"env": ["ANTHROPIC_API_\\u004bEY=literal-value"]}\n')
mutant: a decoded key is not compared: rc=1 FAILED (failures=10)
    failing: test_anthropic_auth_route_reads_json_and_toml_through_their_parsers (rel='home/dot_config/fixture.json', text='{"ANTHROPIC_API_KEY": 12}\n')
    failing: test_anthropic_auth_route_reads_json_and_toml_through_their_parsers (rel='home/dot_config/fixture.json', text='{"ANTHROPIC_API_\\u004bEY": "literal-value", "ANTHROPIC_API_KEY": "${ANTHROPIC_API_KEY}"}
    failing: test_anthropic_auth_route_reads_json_and_toml_through_their_parsers (rel='home/dot_config/fixture.json', text='{"ANTHROPIC_API_\\u004bEY": "literal-value"}\n')
    failing: test_anthropic_auth_route_reads_json_and_toml_through_their_parsers (rel='home/dot_config/fixture.json', text='{"a\\n::error::x": {"ANTHROPIC_API_KEY": "literal-value"}}\n')
    failing: test_anthropic_auth_route_reads_json_and_toml_through_their_parsers (rel='home/dot_config/fixture.json', text='{"env": {"ANTHROPIC_API_KEY":\n"literal-value"}}\n')
    failing: test_anthropic_auth_route_reads_json_and_toml_through_their_parsers (rel='home/dot_config/fixture.toml', text='"ANTHROPIC_API_\\u004bEY" = "literal-value"\n')
    failing: test_anthropic_auth_route_reads_yaml_through_its_parser (rel='home/dot_config/fixture.yaml', text='"ANTHROPIC_API_\\u004bEY": literal-value\n')
    failing: test_anthropic_auth_route_reads_yaml_through_its_parser (rel='home/dot_config/fixture.yaml', text='"ANTHROPIC_API_\\u004bEY": literal-value\nANTHROPIC_API_KEY: $ANTHROPIC_API_KEY\n')
    failing: test_anthropic_auth_route_reads_yaml_through_its_parser (rel='home/dot_config/fixture.yaml', text='ANTHROPIC_API_KEY:\n  literal-value\n')
    failing: test_anthropic_auth_route_reads_yaml_through_its_parser (rel='home/dot_config/fixture.yaml', text='env:\n  ANTHROPIC_API_KEY:\n    literal-value\n')
mutant: the key path is printed unescaped: rc=1 FAILED (failures=1)
    failing: test_anthropic_auth_route_reads_json_and_toml_through_their_parsers (rel='home/dot_config/fixture.json', text='{"a\\n::error::x": {"ANTHROPIC_API_KEY": "literal-value"}}\n')
restored byte-identical: True
(exit 0)
```

## 5. The Check: the module without PyYAML (as CI runs it) and with it

```console
$ uv run python -m unittest tests/unit/test_validate_agent_assets.py -v   # as CI runs it, without PyYAML
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
test_anthropic_auth_route_r2_accepts_only_a_whole_value_reference_template_or_empty (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_auth_route_r2_accepts_only_a_whole_value_reference_template_or_empty) ... ok
test_anthropic_auth_route_r2_reaches_a_quoted_key_and_a_compound_assignment (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_auth_route_r2_reaches_a_quoted_key_and_a_compound_assignment) ... ok
test_anthropic_auth_route_reads_a_comment_after_an_empty_value_as_empty (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_auth_route_reads_a_comment_after_an_empty_value_as_empty) ... ok
test_anthropic_auth_route_reads_a_json_reference_before_a_delimiter (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_auth_route_reads_a_json_reference_before_a_delimiter) ... ok
test_anthropic_auth_route_reads_json_and_toml_through_their_parsers (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_auth_route_reads_json_and_toml_through_their_parsers) ... ok
test_anthropic_auth_route_reads_yaml_through_its_parser (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_auth_route_reads_yaml_through_its_parser) ... skipped 'PyYAML is not installed'
test_anthropic_auth_route_refuses_a_single_quoted_reference_in_text (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_auth_route_refuses_a_single_quoted_reference_in_text) ... ok
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
test_repo_claude_settings_reject_machine_specific_interpreter (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_repo_claude_settings_reject_machine_specific_interpreter) ... ERROR: /tmp/claude-501/validate-agent-assets-test-hcpvl0nu/.claude/settings.json hook SessionEnd must not hard-code a machine-specific home path: ~/.local/share/mise/installs/python/3.14.7/bin/python3.14
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
Ran 105 tests in 3.113s

OK (skipped=1)
(exit 0)
```

```console
$ uv run --offline --with pyyaml python -m unittest tests/unit/test_validate_agent_assets.py -v   # with PyYAML, so the YAML test runs
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
test_anthropic_auth_route_r2_accepts_only_a_whole_value_reference_template_or_empty (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_auth_route_r2_accepts_only_a_whole_value_reference_template_or_empty) ... ok
test_anthropic_auth_route_r2_reaches_a_quoted_key_and_a_compound_assignment (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_auth_route_r2_reaches_a_quoted_key_and_a_compound_assignment) ... ok
test_anthropic_auth_route_reads_a_comment_after_an_empty_value_as_empty (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_auth_route_reads_a_comment_after_an_empty_value_as_empty) ... ok
test_anthropic_auth_route_reads_a_json_reference_before_a_delimiter (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_auth_route_reads_a_json_reference_before_a_delimiter) ... ok
test_anthropic_auth_route_reads_json_and_toml_through_their_parsers (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_auth_route_reads_json_and_toml_through_their_parsers) ... ok
test_anthropic_auth_route_reads_yaml_through_its_parser (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_auth_route_reads_yaml_through_its_parser) ... ok
test_anthropic_auth_route_refuses_a_single_quoted_reference_in_text (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_auth_route_refuses_a_single_quoted_reference_in_text) ... ok
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
test_repo_claude_settings_reject_machine_specific_interpreter (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_repo_claude_settings_reject_machine_specific_interpreter) ... ERROR: /tmp/claude-501/validate-agent-assets-test-j1a0za0t/.claude/settings.json hook SessionEnd must not hard-code a machine-specific home path: ~/.local/share/mise/installs/python/3.14.7/bin/python3.14
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
Ran 105 tests in 3.507s

OK
(exit 0)
```

## 6. Ruff

The same eight findings as on 862ab31c's copies of the two files, all in lines this PR does not touch; formatting passes.

```console
$ ruff check --config ruff.toml --output-format concise scripts/validate-agent-assets.py tests/unit/test_validate_agent_assets.py
scripts/validate-agent-assets.py:1:1: EXE001 Shebang is present but file is not executable
scripts/validate-agent-assets.py:4:1: I001 [*] Import block is un-sorted or un-formatted
scripts/validate-agent-assets.py:133:9: SIM102 Use a single `if` statement instead of nested `if` statements
scripts/validate-agent-assets.py:867:12: C401 Unnecessary generator (rewrite as a set comprehension)
scripts/validate-agent-assets.py:924:18: UP022 Prefer `capture_output` over sending `stdout` and `stderr` to `PIPE`
tests/unit/test_validate_agent_assets.py:1:1: EXE001 Shebang is present but file is not executable
tests/unit/test_validate_agent_assets.py:252:13: FLY002 Consider f-string instead of string join
tests/unit/test_validate_agent_assets.py:1814:41: UP037 [*] Remove quotes from type annotation
Found 8 errors.
[*] 2 fixable with `--fix` (3 unsafe fixes available with `--fix --unsafe-fixes`).
(exit 1)
$ ruff format --config ruff.toml --check scripts/validate-agent-assets.py tests/unit/test_validate_agent_assets.py
2 files already formatted
(exit 0)
```

## 7. The repository validator

```console
$ make validate-agent-assets > "$TMPDIR/t129f/09-validate.txt" 2>&1; echo "make rc=$?"   # 189 s, at 7ee711cc
make rc=0
$ grep -v "^WARN: regime-boundary:" "$TMPDIR/t129f/09-validate.txt"
uv run --offline --with pyyaml scripts/validate-agent-assets.py
agent asset validation ok
(exit 0)
$ grep -c "^WARN: regime-boundary:" "$TMPDIR/t129f/09-validate.txt"   # the Stop-checklist report, warnings that never fail the run
1172
(exit 0)
```
