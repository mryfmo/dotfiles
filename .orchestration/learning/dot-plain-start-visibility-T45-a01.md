# Learning: dot-plain-start-visibility-T45-a01

1. **Tests that fake `HOME` must also clear `XDG_CONFIG_HOME`** (and the other XDG base
   variables the code honours). GitHub runners export it, so a path derived as
   `${XDG_CONFIG_HOME:-$HOME/.config}` escapes the fake home on CI only. Status: validated
   (the CI failure on 89e95e4 was reproduced locally with `XDG_CONFIG_HOME` exported).
2. **When separating fixes from a merge resolution, save copies and restore only the hunk.**
   Do not `git checkout HEAD -- <file>` on files the merge auto-merged: that drops the other
   side's changes. Status: observation (recovered from saved copies in this task).
3. **Docs written before a related fix landed** (here, T45's `actas-claim.sh` bring-up step
   before T49's composite-id rule) need a consistency pass at merge time. Status: observation.

No rule or skill was promoted.

## Resume round 2 triage

1. **Derive only paths the sandbox allowlists.** Honouring XDG for a socket the sandbox pins by literal path lets an existence check pass and the real call fail. Status: observation (Codex review of 9eb3e43).
2. **Short paths for AF_UNIX tests on macOS:** symlink a short `/tmp` name to the fake home instead of moving the fixtures. Status: validated (CI).
