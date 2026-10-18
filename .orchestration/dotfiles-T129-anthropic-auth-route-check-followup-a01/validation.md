# T129 UTF-8 revise validation

Original owner validation is preserved in handoff-a010/tree/validation.md. This worker reran the complete module after the UTF8 fix. Task copy unchanged SHA25652db410226c5361d3a8400ffe429acf7def38bb9973006a20126ee97324eee1d; previous_headdea816110ed58813c0812beee53a1b99588bce3f. Logs:handoff-a010/raw.

- RED named regression:3 malformed-UTF8 structured subcases fail before production edit.
- GREEN named regression:1 test passes,3 formats plus unchanged shell/chezmoi text.
- Full uv run --no-project --with pyyaml python -m unittest tests.unit.test_validate_agent_assets -v:106 tests,3.636s,OK.
- ruff format --check:2 files formatted. Same original-path stdin Ruff:baseline8/current8/new[]. First evidence-directory baseline was ignored by config; failed comparison retained but not used as regression proof.
- Root make validate-agent-assets:exit2 on preserved unrelated T128 commit-c50.log home-path evidence; no unrelated artifact edited.
- Initialized clean Git archive snapshot dea816 plus exact two-file overlay:make validate-agent-assets exit0, agent asset validation ok. This snapshot binds exact source/test bytes; final PR CI also validates the updated narrative evidence.
- Crit data/session absent,daemonfalse. Independent JSON saved/read and native gate passed; handoff-a010/worker-review-receipt-revise.md.
- git diff --check passed. No local Bats; no pre-commit config exists.

## RED output

       Building pyyaml==6.0.3
          Built pyyaml==6.0.3
    Installed 1 package in 1ms
    test_anthropic_auth_route_check_refuses_malformed_utf8_in_a_structured_source (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_auth_route_check_refuses_malformed_utf8_in_a_structured_source) ...
      test_anthropic_auth_route_check_refuses_malformed_utf8_in_a_structured_source (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_auth_route_check_refuses_malformed_utf8_in_a_structured_source) (rel='home/dot_config/fixture.json') ... FAIL
      test_anthropic_auth_route_check_refuses_malformed_utf8_in_a_structured_source (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_auth_route_check_refuses_malformed_utf8_in_a_structured_source) (rel='home/dot_config/fixture.toml') ... FAIL
      test_anthropic_auth_route_check_refuses_malformed_utf8_in_a_structured_source (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_auth_route_check_refuses_malformed_utf8_in_a_structured_source) (rel='home/dot_config/fixture.yaml') ... FAIL

    ======================================================================
    FAIL: test_anthropic_auth_route_check_refuses_malformed_utf8_in_a_structured_source (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_auth_route_check_refuses_malformed_utf8_in_a_structured_source) (rel='home/dot_config/fixture.json')
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "~/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_validate_agent_assets.py", line 1592, in test_anthropic_auth_route_check_refuses_malformed_utf8_in_a_structured_source
        self.assertTrue(refused)
        ~~~~~~~~~~~~~~~^^^^^^^^^
    AssertionError: False is not true

    ======================================================================
    FAIL: test_anthropic_auth_route_check_refuses_malformed_utf8_in_a_structured_source (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_auth_route_check_refuses_malformed_utf8_in_a_structured_source) (rel='home/dot_config/fixture.toml')
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "~/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_validate_agent_assets.py", line 1592, in test_anthropic_auth_route_check_refuses_malformed_utf8_in_a_structured_source
        self.assertTrue(refused)
        ~~~~~~~~~~~~~~~^^^^^^^^^
    AssertionError: False is not true

    ======================================================================
    FAIL: test_anthropic_auth_route_check_refuses_malformed_utf8_in_a_structured_source (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_auth_route_check_refuses_malformed_utf8_in_a_structured_source) (rel='home/dot_config/fixture.yaml')
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "~/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_validate_agent_assets.py", line 1592, in test_anthropic_auth_route_check_refuses_malformed_utf8_in_a_structured_source
        self.assertTrue(refused)
        ~~~~~~~~~~~~~~~^^^^^^^^^
    AssertionError: False is not true

    ----------------------------------------------------------------------
    Ran 1 test in 0.158s

    FAILED (failures=3)

## GREEN and full module summary

    test_anthropic_auth_route_check_refuses_malformed_utf8_in_a_structured_source (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_anthropic_auth_route_check_refuses_malformed_utf8_in_a_structured_source) ... ok

    ----------------------------------------------------------------------
    Ran 1 test in 0.148s

    OK


    ----------------------------------------------------------------------
    Ran 106 tests in 3.636s

    OK

CI/automatic-only review window starts on new main-target draft/ready PR. No manual review comment. Original396 had only CodeRabbit(skipped)/GitGuardian and no Actions; those checks do not validate the final main-target PR.
