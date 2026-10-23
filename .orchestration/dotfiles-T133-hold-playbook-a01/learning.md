---
task_id: dotfiles-T133-hold-playbook-a01
seat: claude-standard-dot-a011
---

# Learning: dotfiles-T133-hold-playbook-a01

1. Whether a glob covers a scope is a question about two patterns, not about files. Expanding the files that exist, or matching one pattern string as a filename against the other, both report coverage that the regime would refuse for a later file. Mechanism: decide containment on the patterns' tokens under the same matcher the regime enforces (`regime-ci.py`'s `allowed()`), and keep one test per trap. Each trap is a broader glob whose every existing match is allowed, and §5 turns it red with the two wrong comparisons.
2. A Check command quoted without flags can disagree with the repository's formatter configuration. Bare `shfmt -d` follows `.editorconfig`, which here sets `indent_size = 4` without `indent_style`, and it then wants tabs in every script. Mechanism: run the command verbatim, reproduce its result on unchanged files at the base, run the repository's own invocation (`make format`'s flags), and report the mismatch rather than reformatting against the house style.
3. A test-first commit whose script does not exist yet is red only by an error in setUp, which says nothing about the tests' strength. Mechanism: a mutation table at the code head. Each test is paired with a plausible wrong implementation that turns it red, so every requirement row names the defect its test catches.
