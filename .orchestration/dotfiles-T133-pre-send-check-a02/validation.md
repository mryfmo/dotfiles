# Validation: dotfiles-T133-pre-send-check-a02

Verbatim outputs. Home paths are written `~` and the sandbox temporary directory `$TMPDIR`.

## 1. Red: the final test source against 11584e19's script (swapped in, then restored)

The old script's leak of the fixture token is the red being proven. The token, a literal in that test source, is written `<fixture-token>` here; the final test makes it at run time.

```text
$ git show 11584e19:scripts/orchestrator/pre-send.sh > scripts/orchestrator/pre-send.sh; shasum -a 256 scripts/orchestrator/pre-send.sh tests/unit/test_pre_send.py
b675f8bdd81fe03feecf3e2ae7c9aec144817cbb1154f859098fd7a4a5e3aeb7  scripts/orchestrator/pre-send.sh
a5497feb08413df1bd6867c025c1e4f5c5d715bc9ea41b7ea2b41e4705c3472c  tests/unit/test_pre_send.py
$ <the task env -i module command> -v
test_all_refusals_are_reported (__main__.PreSendTest.test_all_refusals_are_reported) ... FAIL
test_checker_diagnostics_never_echo_secret_fragments (__main__.PreSendTest.test_checker_diagnostics_never_echo_secret_fragments) ... FAIL
test_checker_exit_and_line_numbers_only (__main__.PreSendTest.test_checker_exit_and_line_numbers_only) ... FAIL
test_complete_fences_before_shell_selection (__main__.PreSendTest.test_complete_fences_before_shell_selection) ... FAIL
test_consistency_refusal (__main__.PreSendTest.test_consistency_refusal) ... FAIL
test_fence_backtick (__main__.PreSendTest.test_fence_backtick) ... FAIL
test_fence_indented_closer (__main__.PreSendTest.test_fence_indented_closer) ... FAIL
test_fence_indented_opener (__main__.PreSendTest.test_fence_indented_opener) ... FAIL
test_fence_longer_closer (__main__.PreSendTest.test_fence_longer_closer) ... FAIL
test_fence_longer_opener (__main__.PreSendTest.test_fence_longer_opener) ... FAIL
test_fence_open_at_the_end (__main__.PreSendTest.test_fence_open_at_the_end) ... FAIL
test_fence_tilde (__main__.PreSendTest.test_fence_tilde) ... FAIL
test_fenced_bash_syntax (__main__.PreSendTest.test_fenced_bash_syntax) ... FAIL
test_input_refusal (__main__.PreSendTest.test_input_refusal) ... 
  test_input_refusal (__main__.PreSendTest.test_input_refusal) (args=()) ... FAIL
  test_input_refusal (__main__.PreSendTest.test_input_refusal) (args=(PosixPath('$TMPDIR/tmpm9z_rkbj/dotfiles-T999-fixture-a01.md'), PosixPath('$TMPDIR/tmpm9z_rkbj/dotfiles-T999-fixture-a01.md'))) ... FAIL
  test_input_refusal (__main__.PreSendTest.test_input_refusal) (args=(PosixPath('$TMPDIR/tmpm9z_rkbj/absent.md'),)) ... FAIL
  test_input_refusal (__main__.PreSendTest.test_input_refusal) (args=(PosixPath('$TMPDIR/tmpm9z_rkbj'),)) ... FAIL
test_literal_home_refusal (__main__.PreSendTest.test_literal_home_refusal) ... FAIL
test_output_is_labels_and_numbers_only (__main__.PreSendTest.test_output_is_labels_and_numbers_only) ... FAIL
test_owner_section_and_rows (__main__.PreSendTest.test_owner_section_and_rows) ... 
  test_owner_section_and_rows (__main__.PreSendTest.test_owner_section_and_rows) (text=None, items=2) ... FAIL
  test_owner_section_and_rows (__main__.PreSendTest.test_owner_section_and_rows) (text='# r\n\n## Other\n- x\n', items=2) ... FAIL
  test_owner_section_and_rows (__main__.PreSendTest.test_owner_section_and_rows) (text='## Owned by dotfiles-T999-fixture-a01\n\n## Next\n', items=1) ... FAIL
  test_owner_section_and_rows (__main__.PreSendTest.test_owner_section_and_rows) (text='## Owned by dotfiles-T999-fixture-a01\n\n## Next\n- outside\nlocal:abc1234:2\tfix\n', items=1) ... FAIL
test_passes_and_prints_final_sha256 (__main__.PreSendTest.test_passes_and_prints_final_sha256) ... ok
test_secret_pattern_matches_validator (__main__.PreSendTest.test_secret_pattern_matches_validator) ... FAIL
test_secret_spanning_two_lines (__main__.PreSendTest.test_secret_spanning_two_lines) ... FAIL
test_self_cap (__main__.PreSendTest.test_self_cap) ... 
  test_self_cap (__main__.PreSendTest.test_self_cap) (spelling='at or under **{} lines**') ... FAIL
  test_self_cap (__main__.PreSendTest.test_self_cap) (spelling='at or under {} lines') ... FAIL
test_task_id_yaml_comment (__main__.PreSendTest.test_task_id_yaml_comment) ... FAIL

======================================================================
FAIL: test_all_refusals_are_reported (__main__.PreSendTest.test_all_refusals_are_reported)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 183, in test_all_refusals_are_reported
    result = self.run_send(path)
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 66, in run_send
    self.assertTrue(all(GRAMMAR.fullmatch(x) for x in result.stdout.splitlines()), result.stdout)
    ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: False is not true : consistency: refused (exit 1: dotfiles-T999-other-a01.md: FAIL C1 task_id dotfiles-T999-fixture-a01 != file dotfiles-T999-other-a01)
secret-pattern: refused (1 match(es) on line(s) 14)
literal-home: refused (line(s) 15)
bash-syntax: refused (block(s) 1)
self-cap: refused (22 lines over the cap of 3)
owner-section: refused (record .orchestration/acceptance/x.md missing)
sha256: c18ec47364d51a2acbdc22a1178d0b572505ecd9c967ef58dbf4258bc562154c


======================================================================
FAIL: test_checker_diagnostics_never_echo_secret_fragments (__main__.PreSendTest.test_checker_diagnostics_never_echo_secret_fragments)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 168, in test_checker_diagnostics_never_echo_secret_fragments
    result = self.run_send(self.task(front=f"bad: [ <redacted:secret-pattern>\n"))
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 66, in run_send
    self.assertTrue(all(GRAMMAR.fullmatch(x) for x in result.stdout.splitlines()), result.stdout)
    ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: False is not true : consistency: refused (exit 1: Traceback (most recent call last): File "$TMPDIR/tmp72pxul28/repo/scripts/orchestrator/task-consistency-check.py", line 150, in <module> sys.exit(main()) ~~~~^^ File "$TMPDIR/tmp72pxul28/repo/scripts/orchestrator/task-consistency-check.py", line 143, in main fails = check(p, args.root) File "$TMPDIR/tmp72pxul28/repo/scripts/orchestrator/task-consistency-check.py", line 48, in check fm = front(text := p.read_text()) File "$TMPDIR/tmp72pxul28/repo/scripts/orchestrator/task-consistency-check.py", line 40, in front return yaml.safe_load(text.split("\n---\n", 1)[0].lstrip("-\n")) ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ File "~/.cache/uv/archive-v0/31F2mEsBsyaNJEyC/lib/python3.15/site-packages/yaml/__init__.py", line 125, in safe_load return load(stream, SafeLoader) File "~/.cache/uv/archive-v0/31F2mEsBsyaNJEyC/lib/python3.15/site-packages/yaml/__init__.py", line 81, in load return loader.get_single_data() ~~~~~~~~~~~~~~~~~~~~~~^^ File "~/.cache/uv/archive-v0/31F2mEsBsyaNJEyC/lib/python3.15/site-packages/yaml/constructor.py", line 49, in get_single_data node = self.get_single_node() File "~/.cache/uv/archive-v0/31F2mEsBsyaNJEyC/lib/python3.15/site-packages/yaml/composer.py", line 36, in get_single_node document = self.compose_document() File "~/.cache/uv/archive-v0/31F2mEsBsyaNJEyC/lib/python3.15/site-packages/yaml/composer.py", line 55, in compose_document node = self.compose_node(None, None) File "~/.cache/uv/archive-v0/31F2mEsBsyaNJEyC/lib/python3.15/site-packages/yaml/composer.py", line 84, in compose_node node = self.compose_mapping_node(anchor) File "~/.cache/uv/archive-v0/31F2mEsBsyaNJEyC/lib/python3.15/site-packages/yaml/composer.py", line 133, in compose_mapping_node item_value = self.compose_node(node, item_key) File "~/.cache/uv/archive-v0/31F2mEsBsyaNJEyC/lib/python3.15/site-packages/yaml/composer.py", line 82, in compose_node node = self.compose_sequence_node(anchor) File "~/.cache/uv/archive-v0/31F2mEsBsyaNJEyC/lib/python3.15/site-packages/yaml/composer.py", line 110, in compose_sequence_node while not self.check_event(SequenceEndEvent): ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^ File "~/.cache/uv/archive-v0/31F2mEsBsyaNJEyC/lib/python3.15/site-packages/yaml/parser.py", line 98, in check_event self.current_event = self.state() ~~~~~~~~~~^^ File "~/.cache/uv/archive-v0/31F2mEsBsyaNJEyC/lib/python3.15/site-packages/yaml/parser.py", line 483, in parse_flow_sequence_entry raise ParserError("while parsing a flow sequence", self.marks[-1], "expected ',' or ']', but got %r" % token.id, token.start_mark) yaml.parser.ParserError: while parsing a flow sequence in "<unicode string>", line 5, column 6: bad: [ [redacted],' or ']', but got ':' in "<unicode string>", line 6, column 14: allowed_files: ^)
secret-pattern: refused (1 match(es) on line(s) 6)
sha256: 721dae3338c51c85bfb0e0e3cd091996c3e375404720765f1ab0e789a7acbc08


======================================================================
FAIL: test_checker_exit_and_line_numbers_only (__main__.PreSendTest.test_checker_exit_and_line_numbers_only)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 164, in test_checker_exit_and_line_numbers_only
    self.refused(self.run_send(self.task(front="bad: [ unclosed\n")), "consistency", "6,7")
                 ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 66, in run_send
    self.assertTrue(all(GRAMMAR.fullmatch(x) for x in result.stdout.splitlines()), result.stdout)
    ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: False is not true : consistency: refused (exit 1: Traceback (most recent call last): File "$TMPDIR/tmpij_nwngy/repo/scripts/orchestrator/task-consistency-check.py", line 150, in <module> sys.exit(main()) ~~~~^^ File "$TMPDIR/tmpij_nwngy/repo/scripts/orchestrator/task-consistency-check.py", line 143, in main fails = check(p, args.root) File "$TMPDIR/tmpij_nwngy/repo/scripts/orchestrator/task-consistency-check.py", line 48, in check fm = front(text := p.read_text()) File "$TMPDIR/tmpij_nwngy/repo/scripts/orchestrator/task-consistency-check.py", line 40, in front return yaml.safe_load(text.split("\n---\n", 1)[0].lstrip("-\n")) ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ File "~/.cache/uv/archive-v0/31F2mEsBsyaNJEyC/lib/python3.15/site-packages/yaml/__init__.py", line 125, in safe_load return load(stream, SafeLoader) File "~/.cache/uv/archive-v0/31F2mEsBsyaNJEyC/lib/python3.15/site-packages/yaml/__init__.py", line 81, in load return loader.get_single_data() ~~~~~~~~~~~~~~~~~~~~~~^^ File "~/.cache/uv/archive-v0/31F2mEsBsyaNJEyC/lib/python3.15/site-packages/yaml/constructor.py", line 49, in get_single_data node = self.get_single_node() File "~/.cache/uv/archive-v0/31F2mEsBsyaNJEyC/lib/python3.15/site-packages/yaml/composer.py", line 36, in get_single_node document = self.compose_document() File "~/.cache/uv/archive-v0/31F2mEsBsyaNJEyC/lib/python3.15/site-packages/yaml/composer.py", line 55, in compose_document node = self.compose_node(None, None) File "~/.cache/uv/archive-v0/31F2mEsBsyaNJEyC/lib/python3.15/site-packages/yaml/composer.py", line 84, in compose_node node = self.compose_mapping_node(anchor) File "~/.cache/uv/archive-v0/31F2mEsBsyaNJEyC/lib/python3.15/site-packages/yaml/composer.py", line 133, in compose_mapping_node item_value = self.compose_node(node, item_key) File "~/.cache/uv/archive-v0/31F2mEsBsyaNJEyC/lib/python3.15/site-packages/yaml/composer.py", line 82, in compose_node node = self.compose_sequence_node(anchor) File "~/.cache/uv/archive-v0/31F2mEsBsyaNJEyC/lib/python3.15/site-packages/yaml/composer.py", line 110, in compose_sequence_node while not self.check_event(SequenceEndEvent): ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^ File "~/.cache/uv/archive-v0/31F2mEsBsyaNJEyC/lib/python3.15/site-packages/yaml/parser.py", line 98, in check_event self.current_event = self.state() ~~~~~~~~~~^^ File "~/.cache/uv/archive-v0/31F2mEsBsyaNJEyC/lib/python3.15/site-packages/yaml/parser.py", line 483, in parse_flow_sequence_entry raise ParserError("while parsing a flow sequence", self.marks[-1], "expected ',' or ']', but got %r" % token.id, token.start_mark) yaml.parser.ParserError: while parsing a flow sequence in "<unicode string>", line 5, column 6: bad: [ unclosed ^ expected ',' or ']', but got ':' in "<unicode string>", line 6, column 14: allowed_files: ^)
sha256: 0bcb76296a4e1dc2ca50acafc559c14d440b6e1761cb61853fd99b7b232eb92b


======================================================================
FAIL: test_complete_fences_before_shell_selection (__main__.PreSendTest.test_complete_fences_before_shell_selection)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 128, in test_complete_fences_before_shell_selection
    self.passed(self.task("\n````markdown\n```bash\nif then\n```\n````\n"))
    ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 75, in passed
    result = self.run_send(path)
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 66, in run_send
    self.assertTrue(all(GRAMMAR.fullmatch(x) for x in result.stdout.splitlines()), result.stdout)
    ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: False is not true : bash-syntax: refused (block(s) 1)
sha256: 0daae7e1d2bb4af30266bd9da7c2712ce7594ee89e41d3a01094b593214da51e


======================================================================
FAIL: test_consistency_refusal (__main__.PreSendTest.test_consistency_refusal)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 80, in test_consistency_refusal
    self.refused(self.run_send(self.task(name="dotfiles-T999-other-a01")), "consistency")
                 ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 66, in run_send
    self.assertTrue(all(GRAMMAR.fullmatch(x) for x in result.stdout.splitlines()), result.stdout)
    ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: False is not true : consistency: refused (exit 1: dotfiles-T999-other-a01.md: FAIL C1 task_id dotfiles-T999-fixture-a01 != file dotfiles-T999-other-a01)
sha256: 7b4c3f32cc3b736ebb4e47dd0cc50601c0d554cfef51c76cc3a948fd71708f3c


======================================================================
FAIL: test_fence_backtick (__main__.PreSendTest.test_fence_backtick)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 211, in <lambda>
    setattr(PreSendTest, f"test_fence_{_name}", lambda self, form=_form: self.fence(*form))
                                                                         ~~~~~~~~~~^^^^^^^
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 124, in fence
    self.refused(self.run_send(self.task(body)), "bash-syntax", "18")
                 ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 66, in run_send
    self.assertTrue(all(GRAMMAR.fullmatch(x) for x in result.stdout.splitlines()), result.stdout)
    ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: False is not true : bash-syntax: refused (block(s) 2)
sha256: 2dd918d9780226906a785b5d7bde6d0d18703dabb8aabdf9bd4ed8b55c202552


======================================================================
FAIL: test_fence_indented_closer (__main__.PreSendTest.test_fence_indented_closer)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 211, in <lambda>
    setattr(PreSendTest, f"test_fence_{_name}", lambda self, form=_form: self.fence(*form))
                                                                         ~~~~~~~~~~^^^^^^^
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 124, in fence
    self.refused(self.run_send(self.task(body)), "bash-syntax", "18")
                 ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 66, in run_send
    self.assertTrue(all(GRAMMAR.fullmatch(x) for x in result.stdout.splitlines()), result.stdout)
    ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: False is not true : bash-syntax: refused (block(s) 2)
sha256: 0d525b74841f9bd19dec4faae911d2041b3d77eeb4dcc13d6ce382fc02683233


======================================================================
FAIL: test_fence_indented_opener (__main__.PreSendTest.test_fence_indented_opener)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 211, in <lambda>
    setattr(PreSendTest, f"test_fence_{_name}", lambda self, form=_form: self.fence(*form))
                                                                         ~~~~~~~~~~^^^^^^^
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 124, in fence
    self.refused(self.run_send(self.task(body)), "bash-syntax", "18")
                 ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 66, in run_send
    self.assertTrue(all(GRAMMAR.fullmatch(x) for x in result.stdout.splitlines()), result.stdout)
    ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: False is not true : bash-syntax: refused (block(s) 2)
sha256: 7df9d84b9da35cb56c4b83f1bf81f4c9dda9b5ede7bc77179a8053859731b8fa


======================================================================
FAIL: test_fence_longer_closer (__main__.PreSendTest.test_fence_longer_closer)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 211, in <lambda>
    setattr(PreSendTest, f"test_fence_{_name}", lambda self, form=_form: self.fence(*form))
                                                                         ~~~~~~~~~~^^^^^^^
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 124, in fence
    self.refused(self.run_send(self.task(body)), "bash-syntax", "18")
                 ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 66, in run_send
    self.assertTrue(all(GRAMMAR.fullmatch(x) for x in result.stdout.splitlines()), result.stdout)
    ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: False is not true : bash-syntax: refused (block(s) 2)
sha256: 69fc88f43286e290537587d5cee06ddd59ee5c482ef84ed64348549ad9f1dcad


======================================================================
FAIL: test_fence_longer_opener (__main__.PreSendTest.test_fence_longer_opener)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 211, in <lambda>
    setattr(PreSendTest, f"test_fence_{_name}", lambda self, form=_form: self.fence(*form))
                                                                         ~~~~~~~~~~^^^^^^^
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 124, in fence
    self.refused(self.run_send(self.task(body)), "bash-syntax", "18")
                 ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 66, in run_send
    self.assertTrue(all(GRAMMAR.fullmatch(x) for x in result.stdout.splitlines()), result.stdout)
    ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: False is not true : bash-syntax: refused (block(s) 2)
sha256: 3f12370ff31f633d12d925fb45e0fe4b7116480b8f1dd43b8fbce545640a1310


======================================================================
FAIL: test_fence_open_at_the_end (__main__.PreSendTest.test_fence_open_at_the_end)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 211, in <lambda>
    setattr(PreSendTest, f"test_fence_{_name}", lambda self, form=_form: self.fence(*form))
                                                                         ~~~~~~~~~~^^^^^^^
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 124, in fence
    self.refused(self.run_send(self.task(body)), "bash-syntax", "18")
                 ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 66, in run_send
    self.assertTrue(all(GRAMMAR.fullmatch(x) for x in result.stdout.splitlines()), result.stdout)
    ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: False is not true : bash-syntax: refused (block(s) 2)
sha256: 5775957d73eb5ea169affcf8e3afb2337b21e1f641dfa1563fe63a4b9469a229


======================================================================
FAIL: test_fence_tilde (__main__.PreSendTest.test_fence_tilde)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 211, in <lambda>
    setattr(PreSendTest, f"test_fence_{_name}", lambda self, form=_form: self.fence(*form))
                                                                         ~~~~~~~~~~^^^^^^^
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 124, in fence
    self.refused(self.run_send(self.task(body)), "bash-syntax", "18")
                 ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 66, in run_send
    self.assertTrue(all(GRAMMAR.fullmatch(x) for x in result.stdout.splitlines()), result.stdout)
    ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: False is not true : bash-syntax: refused (block(s) 2)
sha256: 954c9a29b39f378fd1b4b07df3e3c61ef4ddf7226ccb4da2de5f4d54dd2a146d


======================================================================
FAIL: test_fenced_bash_syntax (__main__.PreSendTest.test_fenced_bash_syntax)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 117, in test_fenced_bash_syntax
    self.refused(self.run_send(path), "bash-syntax", "18,22")  # each failing block's opener
                 ~~~~~~~~~~~~~^^^^^^
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 66, in run_send
    self.assertTrue(all(GRAMMAR.fullmatch(x) for x in result.stdout.splitlines()), result.stdout)
    ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: False is not true : bash-syntax: refused (block(s) 2,3)
sha256: 123fd0ba22399a52508aa802125fff13259d6838aa4026e0b698b0580e4db71a


======================================================================
FAIL: test_input_refusal (__main__.PreSendTest.test_input_refusal) (args=())
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 197, in test_input_refusal
    result = self.run_send(*args)
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 66, in run_send
    self.assertTrue(all(GRAMMAR.fullmatch(x) for x in result.stdout.splitlines()), result.stdout)
    ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: False is not true : input: refused (usage: pre-send.sh <task.md>)


======================================================================
FAIL: test_input_refusal (__main__.PreSendTest.test_input_refusal) (args=(PosixPath('$TMPDIR/tmpm9z_rkbj/dotfiles-T999-fixture-a01.md'), PosixPath('$TMPDIR/tmpm9z_rkbj/dotfiles-T999-fixture-a01.md')))
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 197, in test_input_refusal
    result = self.run_send(*args)
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 66, in run_send
    self.assertTrue(all(GRAMMAR.fullmatch(x) for x in result.stdout.splitlines()), result.stdout)
    ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: False is not true : input: refused (usage: pre-send.sh <task.md>)


======================================================================
FAIL: test_input_refusal (__main__.PreSendTest.test_input_refusal) (args=(PosixPath('$TMPDIR/tmpm9z_rkbj/absent.md'),))
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 197, in test_input_refusal
    result = self.run_send(*args)
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 66, in run_send
    self.assertTrue(all(GRAMMAR.fullmatch(x) for x in result.stdout.splitlines()), result.stdout)
    ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: False is not true : input: refused (not a readable file: $TMPDIR/tmpm9z_rkbj/absent.md)


======================================================================
FAIL: test_input_refusal (__main__.PreSendTest.test_input_refusal) (args=(PosixPath('$TMPDIR/tmpm9z_rkbj'),))
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 197, in test_input_refusal
    result = self.run_send(*args)
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 66, in run_send
    self.assertTrue(all(GRAMMAR.fullmatch(x) for x in result.stdout.splitlines()), result.stdout)
    ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: False is not true : input: refused (not a readable file: $TMPDIR/tmpm9z_rkbj)


======================================================================
FAIL: test_literal_home_refusal (__main__.PreSendTest.test_literal_home_refusal)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 96, in test_literal_home_refusal
    self.refused(self.run_send(self.task(body)), "literal-home", "14,16,17,18")
                 ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 66, in run_send
    self.assertTrue(all(GRAMMAR.fullmatch(x) for x in result.stdout.splitlines()), result.stdout)
    ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: False is not true : literal-home: refused (line(s) 14,16,17,18)
sha256: 36091c133247deadac1bb741ee32ea607aefbf8fd41feb62604c08c30079bbc2


======================================================================
FAIL: test_output_is_labels_and_numbers_only (__main__.PreSendTest.test_output_is_labels_and_numbers_only)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 174, in test_output_is_labels_and_numbers_only
    result = self.run_send(self.task(body, name="dotfiles-T999-other-a01", front=f"bad: [ {TOKEN}\n"))
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 66, in run_send
    self.assertTrue(all(GRAMMAR.fullmatch(x) for x in result.stdout.splitlines()), result.stdout)
    ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: False is not true : consistency: refused (exit 1: Traceback (most recent call last): File "$TMPDIR/tmp564ix_cf/repo/scripts/orchestrator/task-consistency-check.py", line 150, in <module> sys.exit(main()) ~~~~^^ File "$TMPDIR/tmp564ix_cf/repo/scripts/orchestrator/task-consistency-check.py", line 143, in main fails = check(p, args.root) File "$TMPDIR/tmp564ix_cf/repo/scripts/orchestrator/task-consistency-check.py", line 48, in check fm = front(text := p.read_text()) File "$TMPDIR/tmp564ix_cf/repo/scripts/orchestrator/task-consistency-check.py", line 40, in front return yaml.safe_load(text.split("\n---\n", 1)[0].lstrip("-\n")) ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ File "~/.cache/uv/archive-v0/31F2mEsBsyaNJEyC/lib/python3.15/site-packages/yaml/__init__.py", line 125, in safe_load return load(stream, SafeLoader) File "~/.cache/uv/archive-v0/31F2mEsBsyaNJEyC/lib/python3.15/site-packages/yaml/__init__.py", line 81, in load return loader.get_single_data() ~~~~~~~~~~~~~~~~~~~~~~^^ File "~/.cache/uv/archive-v0/31F2mEsBsyaNJEyC/lib/python3.15/site-packages/yaml/constructor.py", line 49, in get_single_data node = self.get_single_node() File "~/.cache/uv/archive-v0/31F2mEsBsyaNJEyC/lib/python3.15/site-packages/yaml/composer.py", line 36, in get_single_node document = self.compose_document() File "~/.cache/uv/archive-v0/31F2mEsBsyaNJEyC/lib/python3.15/site-packages/yaml/composer.py", line 55, in compose_document node = self.compose_node(None, None) File "~/.cache/uv/archive-v0/31F2mEsBsyaNJEyC/lib/python3.15/site-packages/yaml/composer.py", line 84, in compose_node node = self.compose_mapping_node(anchor) File "~/.cache/uv/archive-v0/31F2mEsBsyaNJEyC/lib/python3.15/site-packages/yaml/composer.py", line 133, in compose_mapping_node item_value = self.compose_node(node, item_key) File "~/.cache/uv/archive-v0/31F2mEsBsyaNJEyC/lib/python3.15/site-packages/yaml/composer.py", line 82, in compose_node node = self.compose_sequence_node(anchor) File "~/.cache/uv/archive-v0/31F2mEsBsyaNJEyC/lib/python3.15/site-packages/yaml/composer.py", line 110, in compose_sequence_node while not self.check_event(SequenceEndEvent): ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^ File "~/.cache/uv/archive-v0/31F2mEsBsyaNJEyC/lib/python3.15/site-packages/yaml/parser.py", line 98, in check_event self.current_event = self.state() ~~~~~~~~~~^^ File "~/.cache/uv/archive-v0/31F2mEsBsyaNJEyC/lib/python3.15/site-packages/yaml/parser.py", line 483, in parse_flow_sequence_entry raise ParserError("while parsing a flow sequence", self.marks[-1], "expected ',' or ']', but got %r" % token.id, token.start_mark) yaml.parser.ParserError: while parsing a flow sequence in "<unicode string>", line 5, column 6: bad: [ <fixture-token> ^ expected ',' or ']', but got ':' in "<unicode string>", line 6, column 14: allowed_files: ^)
secret-pattern: refused (1 match(es) on line(s) 15)
literal-home: refused (line(s) 16)
bash-syntax: refused (block(s) 1)
self-cap: refused (21 lines over the cap of 3)
sha256: fbd9f17e7237b0d200f734e77decc77745a1ac501dd5bff596f83d50467ae889


======================================================================
FAIL: test_owner_section_and_rows (__main__.PreSendTest.test_owner_section_and_rows) (text=None, items=2)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 152, in test_owner_section_and_rows
    self.refused(self.run_send(path), "owner-section", str(12 + 2 * items))
                 ~~~~~~~~~~~~~^^^^^^
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 66, in run_send
    self.assertTrue(all(GRAMMAR.fullmatch(x) for x in result.stdout.splitlines()), result.stdout)
    ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: False is not true : owner-section: refused (record .orchestration/acceptance/r.md missing)
sha256: bb49e04f6a7dbb46e823c5fe275a96a086dcf63d52c7d420cbaa85dc89e802f9


======================================================================
FAIL: test_owner_section_and_rows (__main__.PreSendTest.test_owner_section_and_rows) (text='# r\n\n## Other\n- x\n', items=2)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 152, in test_owner_section_and_rows
    self.refused(self.run_send(path), "owner-section", str(12 + 2 * items))
                 ~~~~~~~~~~~~~^^^^^^
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 66, in run_send
    self.assertTrue(all(GRAMMAR.fullmatch(x) for x in result.stdout.splitlines()), result.stdout)
    ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: False is not true : owner-section: refused (no '## Owned by dotfiles-T999-fixture-a01' section in .orchestration/acceptance/r.md)
sha256: bb49e04f6a7dbb46e823c5fe275a96a086dcf63d52c7d420cbaa85dc89e802f9


======================================================================
FAIL: test_owner_section_and_rows (__main__.PreSendTest.test_owner_section_and_rows) (text='## Owned by dotfiles-T999-fixture-a01\n\n## Next\n', items=1)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 152, in test_owner_section_and_rows
    self.refused(self.run_send(path), "owner-section", str(12 + 2 * items))
                 ~~~~~~~~~~~~~^^^^^^
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 66, in run_send
    self.assertTrue(all(GRAMMAR.fullmatch(x) for x in result.stdout.splitlines()), result.stdout)
    ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: False is not true : owner-section: refused (no row under '## Owned by dotfiles-T999-fixture-a01' in .orchestration/acceptance/r.md, and no other Item)
sha256: 6ee6fcf8f1e434189d2cd77db151f67dce9887659d6ce070540efaac5c5f0724


======================================================================
FAIL: test_owner_section_and_rows (__main__.PreSendTest.test_owner_section_and_rows) (text='## Owned by dotfiles-T999-fixture-a01\n\n## Next\n- outside\nlocal:abc1234:2\tfix\n', items=1)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 152, in test_owner_section_and_rows
    self.refused(self.run_send(path), "owner-section", str(12 + 2 * items))
                 ~~~~~~~~~~~~~^^^^^^
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 66, in run_send
    self.assertTrue(all(GRAMMAR.fullmatch(x) for x in result.stdout.splitlines()), result.stdout)
    ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: False is not true : owner-section: refused (no row under '## Owned by dotfiles-T999-fixture-a01' in .orchestration/acceptance/r.md, and no other Item)
sha256: 6ee6fcf8f1e434189d2cd77db151f67dce9887659d6ce070540efaac5c5f0724


======================================================================
FAIL: test_secret_pattern_matches_validator (__main__.PreSendTest.test_secret_pattern_matches_validator)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 86, in test_secret_pattern_matches_validator
    self.refused(self.run_send(path), "secret-pattern", "14,20")
                 ~~~~~~~~~~~~~^^^^^^
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 66, in run_send
    self.assertTrue(all(GRAMMAR.fullmatch(x) for x in result.stdout.splitlines()), result.stdout)
    ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: False is not true : secret-pattern: refused (2 match(es) on line(s) 14,20)
sha256: 9975ddedc92131be4b71635287dec33c022441da4b607a527a779dfa4a68fa66


======================================================================
FAIL: test_secret_spanning_two_lines (__main__.PreSendTest.test_secret_spanning_two_lines)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 91, in test_secret_spanning_two_lines
    self.refused(self.run_send(path), "secret-pattern", "14,15")
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 70, in refused
    self.assertEqual(1, result.returncode, result.stdout)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 1 != 0 : sha256: 016e38e11c0ed8937ad89bd34280a3e4d81de8eb0a6da5c06148f4c86d123d31


======================================================================
FAIL: test_self_cap (__main__.PreSendTest.test_self_cap) (spelling='at or under **{} lines**')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 107, in test_self_cap
    self.refused(self.run_send(path), "self-cap", "14")  # the declaration's line
                 ~~~~~~~~~~~~~^^^^^^
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 66, in run_send
    self.assertTrue(all(GRAMMAR.fullmatch(x) for x in result.stdout.splitlines()), result.stdout)
    ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: False is not true : self-cap: refused (14 lines over the cap of 13)
sha256: 31804ad2eec62c2bb9250e66b7f0152b544be117830ceddaa9b0a85502409a7a


======================================================================
FAIL: test_self_cap (__main__.PreSendTest.test_self_cap) (spelling='at or under {} lines')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 107, in test_self_cap
    self.refused(self.run_send(path), "self-cap", "14")  # the declaration's line
                 ~~~~~~~~~~~~~^^^^^^
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 66, in run_send
    self.assertTrue(all(GRAMMAR.fullmatch(x) for x in result.stdout.splitlines()), result.stdout)
    ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: False is not true : self-cap: refused (14 lines over the cap of 13)
sha256: b8cb7424825d5687a04954a1523a8ea8a66da9b6840e3aa4b59528218d8a7398


======================================================================
FAIL: test_task_id_yaml_comment (__main__.PreSendTest.test_task_id_yaml_comment)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 160, in test_task_id_yaml_comment
    self.refused(self.run_send(path), "owner-section", "14")
                 ~~~~~~~~~~~~~^^^^^^
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_pre_send.py", line 66, in run_send
    self.assertTrue(all(GRAMMAR.fullmatch(x) for x in result.stdout.splitlines()), result.stdout)
    ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: False is not true : owner-section: refused (record .orchestration/acceptance/none.md missing)
sha256: 44a79eb2a05a624831591a1b2fef007fca345eb3927b48be9412bd4e9e174a44


----------------------------------------------------------------------
Ran 22 tests in 7.897s

FAILED (failures=28)
exit 1
```

## 2. Green at de7f70ec: the module, the shell checks, ruff, the preflight on the a02 text, the crit gate, the caps

```text
$ git rev-parse HEAD
de7f70ec60b6356a7861a5d43433050f4dc62562
$ <the task env -i module command> -v
test_all_refusals_are_reported (__main__.PreSendTest.test_all_refusals_are_reported) ... ok
test_checker_diagnostics_never_echo_secret_fragments (__main__.PreSendTest.test_checker_diagnostics_never_echo_secret_fragments) ... ok
test_checker_exit_and_line_numbers_only (__main__.PreSendTest.test_checker_exit_and_line_numbers_only) ... ok
test_complete_fences_before_shell_selection (__main__.PreSendTest.test_complete_fences_before_shell_selection) ... ok
test_consistency_refusal (__main__.PreSendTest.test_consistency_refusal) ... ok
test_fence_backtick (__main__.PreSendTest.test_fence_backtick) ... ok
test_fence_indented_closer (__main__.PreSendTest.test_fence_indented_closer) ... ok
test_fence_indented_opener (__main__.PreSendTest.test_fence_indented_opener) ... ok
test_fence_longer_closer (__main__.PreSendTest.test_fence_longer_closer) ... ok
test_fence_longer_opener (__main__.PreSendTest.test_fence_longer_opener) ... ok
test_fence_open_at_the_end (__main__.PreSendTest.test_fence_open_at_the_end) ... ok
test_fence_tilde (__main__.PreSendTest.test_fence_tilde) ... ok
test_fenced_bash_syntax (__main__.PreSendTest.test_fenced_bash_syntax) ... ok
test_input_refusal (__main__.PreSendTest.test_input_refusal) ... ok
test_literal_home_refusal (__main__.PreSendTest.test_literal_home_refusal) ... ok
test_output_is_labels_and_numbers_only (__main__.PreSendTest.test_output_is_labels_and_numbers_only) ... ok
test_owner_section_and_rows (__main__.PreSendTest.test_owner_section_and_rows) ... ok
test_passes_and_prints_final_sha256 (__main__.PreSendTest.test_passes_and_prints_final_sha256) ... ok
test_secret_pattern_matches_validator (__main__.PreSendTest.test_secret_pattern_matches_validator) ... ok
test_secret_spanning_two_lines (__main__.PreSendTest.test_secret_spanning_two_lines) ... ok
test_self_cap (__main__.PreSendTest.test_self_cap) ... ok
test_task_id_yaml_comment (__main__.PreSendTest.test_task_id_yaml_comment) ... ok

----------------------------------------------------------------------
Ran 22 tests in 7.173s

OK
exit 0
$ bash -n scripts/orchestrator/pre-send.sh
exit 0
$ shellcheck -x scripts/orchestrator/pre-send.sh
exit 0
$ shfmt -i 4 -sr -d scripts/orchestrator/pre-send.sh
exit 0
$ ruff check --config ruff.toml tests/unit/test_pre_send.py
All checks passed!
exit 0
$ ruff format --config ruff.toml --check tests/unit/test_pre_send.py
1 file already formatted
exit 0
$ scripts/orchestrator/pre-send.sh ~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-pre-send-check-a02.md
sha256: 438089b8b9eb46db347e724913c1d4070d575df5091e3ea4a7e1d4b46412bf95
exit 0
$ make require-crit-review
Review not required: no meaningful review trigger found.
exit 0
$ git diff --numstat 60a6fb2b324d0381c4a6e539b37c650105154a7e...HEAD -- scripts tests
89	0	scripts/orchestrator/pre-send.sh
18	0	tests/unit/test_mise_config.py
215	0	tests/unit/test_pre_send.py
6	5	tests/unit/test_regime_ci.py
1	0	tests/unit/test_supply_chain_policy.py
outside tests/ and .orchestration/: 92 of 90; under tests/: 245 of 220
```

## 3. The caps' two measures

```text
$ git diff --numstat 60a6fb2b324d0381c4a6e539b37c650105154a7e...HEAD | grep -v .orchestration/
2	1	home/dot_mise/config.toml
89	0	scripts/orchestrator/pre-send.sh
18	0	tests/unit/test_mise_config.py
215	0	tests/unit/test_pre_send.py
6	5	tests/unit/test_regime_ci.py
1	0	tests/unit/test_supply_chain_policy.py
$ git log --oneline --merges 60a6fb2b..HEAD
d0679105 Merge branch 'main' into tools/pre-send-check-a01
9ce253f1 Merge branch 'main' into tools/pre-send-check-a01
9ff87ee1 Merge branch 'main' into tools/pre-send-check-a01
$ git diff --numstat origin/main...HEAD | grep -v .orchestration/   # the PR's own change
89	0	scripts/orchestrator/pre-send.sh
215	0	tests/unit/test_pre_send.py
```
