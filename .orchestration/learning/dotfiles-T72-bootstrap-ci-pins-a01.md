# Learning: dotfiles-T72-bootstrap-ci-pins-a01

- **Never name a CI variable `MISE_*`.** mise deserializes every `MISE_*` environment variable into its settings, and `MISE_PIN` is a boolean, so a version string fails mise-action outright. The same applies to any tool that reads a prefixed environment namespace.
- **Check a test against the scan before trusting it.** The validator's `rglob` over `scripts/` already covered `scripts/lib`; the task text assumed otherwise.
- **Grep tests for the function being changed, even outside allowed_files.** `test_release_asset_pins.py` pinned the exact call sequence of the function item 2 changes.
- **A green job can still have skipped the step you changed.** Read its step list: the secret-gated `ubuntu.yaml` and `macos.yaml` steps skip on PRs, so a pass there says nothing about the new step.
