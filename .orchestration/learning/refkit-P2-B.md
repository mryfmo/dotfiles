# refkit-P2-B learning triage

[memory:decision] Validated reusable fact: Python's `re` module's `.` matches newlines
under `re.DOTALL`/`re.S` — and this codebase's `selftest()` runner always passes
`flags=re.M | re.S`. Several new mutation patterns written as `(^# .*)$` (intending
"rest of this one line") silently matched from the first `# ` heading all the way to
the _last_ line-end in the file, corrupting the fixture in a way that produced a
different, misleading error rather than a clean failure. Always use `[^\n]*` instead of
bare `.*`/`.+` in any pattern run under this project's selftest runner, unless the
intent genuinely is to span newlines (use `[\s\S]*?` explicitly for that, as the
existing patterns already do).

[memory:decision] Validated reusable fact: this session's Edit/Write-tool auto-formatter
(see refkit-P2-A's learning record) reformats _every_ file it touches, including scratch
files under the session's own scratchpad directory — not just repo files. A scratch
`.py` patch script written via the Write tool, then `cp`'d into a repo file, carries
whatever quote-style the formatter left it in. Concretely: `portability_test.py` ended
up entirely double-quoted (formatter output) even though the patch-script source was
written single-quoted, because the _scratch file itself_ was reformatted before the
`cp`. When writing a _whole new file_ this way, treat the copied-in style as final and
match it in all subsequent fix-up patches to that file, rather than assuming the
original scratch-file text you wrote is what actually landed.

Disposition: both recorded in CompactionDB (see `.orchestration/reports/refkit-P2-B.md`).
