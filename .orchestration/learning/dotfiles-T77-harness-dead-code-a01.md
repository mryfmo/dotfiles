# dotfiles-T77-harness-dead-code-a01 — learning triage

1. **Do not delete Python test methods with a regex.**
   - A "next `def` or column-0 line" regex stops inside triple-quoted shell fixtures, which have column-0 lines, and leaves broken fragments behind.
   - Use `ast` instead: take each `FunctionDef`'s `lineno` (and decorators) through `end_lineno`, delete the spans in reverse order, then `py_compile` and `ruff format --check`.
2. **Deleting a chezmoi source does not delete the deployed target.**
   - A removed `executable_*` needs a `home/.chezmoiremove` entry. `tests/unit/test_chezmoiremove_agmsg.py::RETIRED` pins that list and also asserts the target has no source.
   - The Codex Bot flagged the gap independently, nine minutes after the first push.
3. **A deletion task's validation grep should exclude `__pycache__`.** Otherwise stale bytecode adds "binary file matches" noise for the deleted names.
