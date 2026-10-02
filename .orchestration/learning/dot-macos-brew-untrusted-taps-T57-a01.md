# Learning triage: dot-macos-brew-untrusted-taps-T57-a01

Candidates only; nothing is promoted.

1. **Homebrew 7 hides untrusted-tap formulae from `brew list`.**
   - Lesson: `Formula.installed` silently skips formulae whose tap is untrusted, because `load_formula` requires trust and the error is rescued. Any script that tries to find what is installed from an untrusted tap through `brew list` / `brew info` sees nothing. Whole-tap trust is the only documented handling that works unattended when kegs exist.
   - Applies to: any future Homebrew tap-trust automation.
2. **Read the release tag, not the default branch.**
   - Lesson: verify a CLI behavior against the released tag the runner uses (here Homebrew 7.0.7, `?ref=7.0.7`), and check where the implementation reads data that might be filtered (`Formula.installed` vs keg receipts), before relying on it.
   - Origin: the advisor caught the item-level-trust flaw before the push.
3. **The README formatter hook.**
   - Lesson: an Edit-tool write to `README.md` triggers a PostToolUse formatter that reflows unrelated Markdown lines (list continuations, blank lines before lists). For a one-sentence task, insert with a script, or restore and re-insert, then check `git diff --stat`.
   - Candidate: document this in AGENTS.md or exclude README from the hook, via a separate task.
4. **The bare shfmt command does not use the repo style.**
   - Lesson: `shfmt -d <file>` with no flags uses tabs in this environment, despite `.editorconfig`, so it fails on unchanged files. Future task files should name the repository form: `shfmt -i 4 -sr -d`, or `mise x shfmt@<pin> -- shfmt -i 4 -sr -d`.
5. **Zero warnings does not prove a function ran.**
   - Lesson: a silent no-op also yields 0 warnings. Acceptance should include a log excerpt showing the function acted (`Trusted tap: …`) on the job that used to warn.

## Revise round 1 additions (candidates only)

6. **Check the exact code path the command takes, with its flags.**
   - Lesson: in round 0 I read `cmd/list.rb`'s plain `Formula.installed` branch and wrongly applied it to `brew list --full-name`, which reads keg receipts and does list untrusted-tap items. The advisor's warning sent me to source, but to the wrong branch.
   - Candidate: when a design rests on "tool X cannot do Y", verify it on the exact flag combination, ideally by running it. Here that would have needed a macOS runner, so for runner-only tools a measurement commit should come before the claim.
7. **Measurement beats source reading.** Item-level trust alone cleared the taps that had installed items. It left only the tap with nothing installed (`aws/tap`), because Homebrew's pre-install check covers wholly untrusted taps only. One measurement commit settled what three rounds of source reading had not.
8. **Bot reviews can be stale.** The Codex bot reviewed the measurement commit, and its P2 was partly overtaken by the next commit. Sweep dispositions should name the commit each item was written against.
