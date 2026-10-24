---
task_id: dotfiles-T133-result-precheck-a02
round: 1
reset_of: dotfiles-T133-result-precheck-a01
---

# Learning

Task-local triage; nothing promoted.

- A test that accepts any diagnostic of a class can pass for the wrong reason. The first version of the malformed-record test passed against the unfixed gate because its fixture committed with `git add -A`, swept in the acceptance record the dispatch calls had written, and the old gate refused on the evidence-only ancestry rule instead; committing only the record and asserting `precheck.json:checks` or `precheck.json:selectors` made the red run real. Applies to every red-then-green proof: assert the specific diagnostic, and keep fixture commits to the files under test.
- A git hook inherits `GIT_INDEX_FILE` from git, possibly relative to the root; a hook step that changes directory pins it absolute (`git rev-parse --path-format=absolute --git-path index`).
- In a function called on the left of `||`, Bash disables errexit for the whole function body, so a failed prerequisite (a `git diff` into a file) silently leaves an empty file the next command reads as a clean scope; every such command carries its own `|| return`.
- Whole-blob scanning of pushed content flags any pre-existing match in a touched file: 13 tracked files (fixtures in tests, `scripts/validate-agent-assets.py`, vendored CompactionDB tests) already hold text the masker flags, so a push touching one is refused once the hooks are live. Applies to P1-7 (`core.hooksPath`): settle this before enabling the pre-push hook.
- Revise 1: a scan over concatenated inputs needs a separator, since the masker's word boundary is lost when one blob's last word meets the next blob's token; and a byte normalizer that maps NUL to a separator splits UTF-16 text letter by letter. Every input normalisation of a secret scan needs a case for the encodings the masker itself handles. Applies to any scanner fed a stream of files.
- Revise 1: "the previous head fails" is a proof only when it ran the new test and the test failed by assertion. The old worktree lacks a new module, so its nonzero exit was an import error, and the a01 record shows `Ran 0 tests` accepted as red. The previous head now runs this head's test source. Applies to every red-then-green record.
