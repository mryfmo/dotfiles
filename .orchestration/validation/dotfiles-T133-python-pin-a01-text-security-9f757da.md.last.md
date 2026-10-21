[P2] High confidence .orchestration/tasks/dotfiles-T133-python-pin-a01.md:136 — `unittest discover -p test_mise_config.py` also imports subpackage initializers regardless of the pattern: an untracked `tests/unit/extra_package/__init__.py` can execute while contributing zero tests, preserving `Ran 1 test` and contradicting the in-process mitigation at line 40; execute the intended file directly under `-I` instead. Confirmed with the installed interpreter’s loader using an in-memory probe. [Python documentation](https://docs.python.org/3.15/library/unittest.html#unittest.TestLoader.discover).

All required threat-row units are present. Earlier environment and bare-`gh` findings are addressed; same-UID replacement and deferred symlink/case-alias protections remain explicitly residual.

📝 まとめ: Completed the read-only design and cited-record review; one finding remains for orchestrator disposition.
Not checked: implementation, CI or deployment; no files changed. The discovery command still permits unintended imports.
Verdict: incorrect