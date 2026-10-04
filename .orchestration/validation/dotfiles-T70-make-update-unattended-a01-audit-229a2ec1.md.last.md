- [P2] high confidence Makefile:87 README.md:179 still says ambiguous Herdr status fails the update; this commit instead warns and succeeds, making the documented failure contract inaccurate.
- [P2] high confidence install/ubuntu/common/apparmor_userns.sh:62 README.md:297 still promises profile installation. The new successful skip is recorded by chezmoi, so unchanged applies never retry; document the pending state and standalone recovery command.

Syntax checks pass. [Commit CI](https://github.com/mryfmo/dotfiles/actions/runs/37161591011) confirms passing Python and Bats tests. No additional implementation or security findings.

📝 まとめ: Audited only `229a2ec1`; two documentation regressions remain.

Verdict: incorrect