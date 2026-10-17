[P1] high .orchestration/tasks/dotfiles-T129-pstack-asset-a01.md:77 The asset declaration omits `verify`, `sha256`, `reason` and `installer`, which origin/main requires for git-commit assets, so implementing it literally fails validation.

[P1] high .orchestration/tasks/dotfiles-T129-pstack-asset-a01.md:13 Adding this lock makes the existing generator require `home/dot_claude/skills/symlink_pstack.lock.json.tmpl`, which allowed_files excludes, preventing generated-config validation from passing.

[P1] high .orchestration/tasks/dotfiles-T129-pstack-asset-a01.md:77 Item 1 requires rewriting eight skills while line 84 prohibits changing any skill’s content, leaving contradictory scope across PR G and plan 023’s later H adaptations.

[P1] high .orchestration/tasks/dotfiles-T129-pstack-asset-a01.md:78 Plan 023 records foreign user skill providers as opt-in, but this task enables no provider and waits only for asset PR A, so installation can succeed without omp discovering the skills.

[P1] high .orchestration/tasks/dotfiles-T129-pstack-asset-a01.md:80 Both specified tests use fixtures without requiring CI to check the actual pinned upstream tree against the committed manifest and lock, allowing removed upstream skills or stale committed content through the promised bump-PR gate.

[P2] high .orchestration/tasks/dotfiles-T129-pstack-asset-a01.md:80 The lock test specifies only missing-skill, bad-front-matter and pin-drift mutations, omitting the content-only hash-drift case required by stop condition 2.

[P2] high .orchestration/tasks/dotfiles-T129-pstack-asset-a01.md:78 The claimed existing checkout flow is absent: Homebrew downloads a commit-pinned installer and verifies its SHA-256, while update-agent-assets.sh provides no generic sparse/shallow git-commit checkout mechanism.

📝 まとめ: Hash matched; C1–C10/C7b passed; mask found 0 matches; premises replayed as `0` and `absent`; fixed generic rows and Completion matched. Implementation and CI were not run, and evidence files were not written under the read-only constraint.
Task-file verdict: dotfiles-T129-pstack-asset-a01: revise