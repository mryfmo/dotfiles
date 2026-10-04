- [P2] High confidence `home/dot_local/bin/common/executable_setup-python-env:1` — Deleting the six source files without `.chezmoiremove` entries leaves their installed targets behind after updates, including the runnable `setup-python-env`. Retire all six target paths and add an upgrade regression check. [Chezmoi maintainer explanation](https://github.com/twpayne/chezmoi/discussions/1446).

Shell syntax, Sheldon TOML, and `dev` behavior checks passed. No additional security or rule-compliance findings. Live CI was inaccessible; supplied [PR #244](https://github.com/mryfmo/dotfiles/pull/244) evidence concerns later merge head `fa5f5a3f`.

📝 まとめ: Audited only `ef5742f9`; one deployment cleanup defect remains.

Verdict: incorrect