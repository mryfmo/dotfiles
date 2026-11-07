# Ubuntu host: today's `make update` and the seats' one login (operator steps, 2026-11-07)

Written by the coordinator 2026-11-07T02:55Z after PRs 709, 710, 712, 713, 714 and 716 landed on `main` (head 668ba887). Run the rows in order in your own shell on the Ubuntu host. Each row names the command you type, what you should see, and the command the coordinator runs afterwards to verify (standing order 48).

| # | command (Ubuntu, your shell) | expected | the agent verifies afterwards |
| --- | --- | --- | --- |
| 1 | `git -C ~/.local/share/chezmoi fetch --quiet origin main && git -C ~/.local/share/chezmoi log origin/main -1 --format='%h %s'` | `668ba887 fix(seat-login): the preflight check validates the directory chain, quotes the printed command and reads its producer's status (regime-cutover U318b) (#716)` or a later `main` commit | nothing; the commit is on `origin/main` (measured on the laptop 02:41Z) |
| 2 | `make -C ~/.local/share/chezmoi update` | exit 0. The AWS CLI step prints `gpgv: Good signature from "AWS CLI Team <aws-cli@amazon.com>"` for the versioned archive `awscli-exe-linux-<arch>-<version>.zip` (PR 713 replaced the unversioned archive whose signature failed this morning). If any step fails, paste the last 30 lines | `ssh <host> '~/.local/bin/aws --version; ~/.local/bin/common/hcom-seat --help 2>&1 \| head -1'` once you say the row is done |
| 3 | `~/.local/bin/common/seat-login-preflight --check` | `orchestrator claude-bridge: absent (no /home/<you>/.local/state/omp-seats/dotfiles/.state/claude)` and the same for worker; no `env token` line, no `host login only` line | nothing; this row shows the new lever is installed before the login |
| 4 | `CLAUDE_CONFIG_DIR="$HOME/.local/state/omp-seats/dotfiles/.state/claude" BROWSER=regime-open-url claude auth login` | `Opening browser to sign in…` then `Login successful.` The browser opens on the laptop through the ssh forward of your session (U37). If it does not open, copy the printed `https://claude.com/cai/oauth/authorize?...` URL into the laptop's browser, sign in, and paste the code at `Paste code here` | nothing until row 6 |
| 5 | `chmod 700 "$HOME/.local/state/omp-seats/dotfiles/.state" "$HOME/.local/state/omp-seats/dotfiles/.state/claude"` | no output | nothing; the launcher's row for this directory is 0700 (claude creates it 0755; measured on the laptop 02:49Z) |
| 6 | `~/.local/bin/common/seat-login-preflight --check` | `orchestrator claude-bridge: login present (claude.ai, /home/<you>/.local/state/omp-seats/dotfiles/.state/claude)` and the same for worker | `ssh <host> '~/.local/bin/common/seat-login-preflight --check'` and a `hcom-seat worker --name probe --dry-run` with the live store, exit 0 |

Do not paste a `~/...` path on Ubuntu (the laptop's HOME; the 02:5xZ attempt failed on it and on a leading `。`). Every path above is written with `$HOME` so the same line works on both hosts.

What this does not yet give the Ubuntu host: seats and a store (the one-time store move, units U215 to U222, is gated), so no seat launches there until those units land. The login is reused by them when they do.
