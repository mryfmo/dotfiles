# Learning: dotfiles-T95-sandbox-placeholder-files-on-disk-a01

- **A gitignore pattern without a trailing slash matches directories too.** To ignore only a file form, pair `/<path>` with `!/<path>/`. The negation re-includes only a directory, so its contents stay visible. Codex caught this on the first head.
- **Test ignore rules in a fresh repository.** The main checkout's `.git/info/exclude` is shared by every worktree and already held the stopgap entries, so `git check-ignore` in the real repository would pass with or without the tracked change.
- **The placeholder files have two forms.** Inside the sandbox they are mounts (`/dev/null`, read-only), which the gate's mount check skips. On the host they are plain 0-byte, 0444 files that appear in some checkouts and not others. A sandboxed command of this worker session did not create them in either place.
