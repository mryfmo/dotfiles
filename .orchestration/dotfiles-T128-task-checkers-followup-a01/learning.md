# Learning triage: dotfiles-T128-task-checkers-followup-a01

These are candidates only; nothing is promoted.

1. [memory:failure] A fixed exemption can survive its own fix when no case reaches it. The first mutation pass left `(($# == 3)) ||`, the default path's exemption from the tracking check, alive: the new test edited a tracked default but never removed it from the index. One `git rm --cached` case closed it. When a fix removes a branch, the mutation pass puts that branch back first.
2. [memory:decision] An owned row whose own disposition line says "fixed in this record before the gate" is still listed under the owner heading. Reading the row's disposition line, not only the `<id><TAB><class>` row, tells whether the owner task has anything to change. The reading went to the orchestrator in an alive PONG before any code, so it could amend if it wanted a mechanism.
3. [memory:decision] Tightening a filter from a flag (`bot`) to a field (`author`) changes every hand-built fixture that set only the flag. Grep the tests for the old key before running them: here three sweeps needed the author added, and the copied real sweep under `tests/fixtures/lessons/` already had it.
