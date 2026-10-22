# Learning triage: dotfiles-T129-hcom-dispatch-bus-a02

These are candidates only; nothing is promoted.

1. [memory:failure] macOS's `/bin/bash` (3.2) keeps every here-document and here-string in a temporary file under `/tmp` (not TMPDIR), which the Claude sandbox refuses. Under `#!/bin/bash -p`, a heredoc yields an unset variable and a here-string yields empty input. Use pipes, process substitution, or a here-document that never runs (`true || : << 'X'`) read back by the program from its own file.
2. [memory:failure] On this host an outside scanner reads each new file once, about 2 s after creation, so an atime-based read probe needs a settle wait before the route runs. I first misread that read as `os.path.realpath()`'s; a rerun after the scanner's read showed realpath leaves the file unread (validation §13).
3. [memory:failure] `/usr/bin/shasum` is a Perl script (PERL5OPT, PERL5LIB), and `/usr/bin/python3` is an xcrun shim (DEVELOPER_DIR). An absolute path does not bind them; run them under `env -i`. Found by the independent review, not by me.
4. [memory:decision] hcom 0.7.30:
   - a message row has no tag and no read time, and the read state is the recipient's `instances.last_event_id`;
   - `--thread` is the only stored team label;
   - `hcom events` is write-free, while `sqlite3 -readonly` cannot open its idle WAL store;
   - a `--thread` reply reaches the other thread members, and an external sender is not addressable.
5. [memory:decision] Caps count `git diff --numstat` additions plus deletions, so moving a block counts it twice. Edit in place to stay under a cap.
6. [memory:decision] Give an independent reviewer the code and the binding constraints, not my conclusions. It found two P1s that my own tests missed, because the matrix never drove the record path with a hashed file.
