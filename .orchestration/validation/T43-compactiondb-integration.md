# T43 validation

```text
$ PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -q
Ran 43 tests in 2.815s
OK

$ PYTHONDONTWRITEBYTECODE=1 python3 validate.py
status: pass
passed: 10
failed: 0
unittest_suite: 43 tests passed with ResourceWarning promoted to error
release_tree_clean: pass
claude_code_executable: 2.1.227 (optional, pass)

$ shasum -a 256 -c MANIFEST.sha256 | tail -1
./validate.py: OK

$ shasum -a 256 archive/CompactionDB-2.0.0.zip
4c803330322ab9e786717c6439f27cc30d0bcb517857de8da56529e572e8b8d9  archive/CompactionDB-2.0.0.zip
```

Regression coverage includes both explicit marker forms, leading known-kind bracket content, underscore environment assignments, Stripe/Slack/GCP credentials, additional sensitive paths, expired raw-event pruning, error-log trimming, and quarantine cleanup at SessionEnd.

Final validator revision:

```text
$ uv run --with pyyaml scripts/validate-agent-assets.py
agent asset validation ok

$ PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile scripts/validate-agent-assets.py
exit 0

$ git show --stat --oneline f560c89
f560c89 chore(validate): exempt compactiondb dummy secret fixtures
scripts/validate-agent-assets.py | 9 +++++++++
```

The exemption contains exactly these intentional dummy-secret fixtures: `vendor/compactiondb/validate.py`, `vendor/compactiondb/tests/test_migration.py`, `vendor/compactiondb/tests/test_redaction.py`, and `vendor/compactiondb/.claude/contextdb/contextdb/redaction.py`.
