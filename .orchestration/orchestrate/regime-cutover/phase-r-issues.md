# Phase R open issues (coordinator inventory, 2026-10-26)

One writer: the coordinator. Each row names who can act and why. "Agent" means the coordinator or its workers. "Operator" means a step the agent cannot take, with the rule or tool limit that stops it. Facts were measured on 2026-10-26 unless a row says otherwise.

## A. Units (agent)

| id | problem | state |
| --- | --- | --- |
| U95 #567 | Seat launch took 112 s on a checkout with 283 worktrees; git-state checks had type and enumeration gaps. Nested worktrees refuse (operator decision U95-nested-refuse-decided). | landed as 294a024d; deployed on macOS, where the dry run now refuses in 8 s naming the nested worktree |
| U96 #568 | `public-bootstrap` failed intermittently with `chezmoi: unexpected EOF`. | landed as 5c3e8b74 |
| U97 #569 | Lint tool versions differed between hosts and CI; `make format` checked another file set. | landed as 20d345d0; macOS now runs ShellCheck 0.11.0 and shfmt 3.14.1 from the pins |
| U98 #570 | `HTTPServer.server_bind` reverse DNS lookup (about 35 s on macos-15). | landed as 3aea4608 |
| U99 #571 | No bats test or installer download had a time bound. | landed as 88cd19a2 |
| U100 #572 | Git 2.55 background maintenance raced test cleanup and reddened main. | landed as 04a15081 |
| U71b #559 | Audit lever pr-audit.sh (gate G18). | landed as d677de9e; deployed on macOS; audits now run through it (standing order 28, ship.sh) |
| U102 #575 | The real-install bats test stalled on the trickling Azure apt mirror; the step timeout fired before the per-test bound. | landed as 950dd803 |
| U101 #574 | records-sync copied 99 foreign files from a stale checkout and pushed through a rewriting user config. | landed as 590db689 (13 rounds; the copy set is the store against origin/main, built in a config-less scratch repository; the checkout listing runs no fsmonitor hook) |

## B. Program bookkeeping (agent)

| id | problem | next action |
| --- | --- | --- |
| B1 | units.tsv row U71b said `planned feat/audit-lever`; the real branch is feat/audit-lever-g18, PR #559, in flight. | Corrected in place. |
| B2 | gates.md G12 to G16 had no status although their units landed. | Annotated with the landing evidence; G16 points at section C. |
| B3 | Records sync (store redacted; bare host word and home paths included). | Sync 11 landed as 5bd0fb07 after a hand correction (decisions.tsv deviation-records-sync-11). The next sync waits for U101's fixed lever. |
| B4 | macOS deploy. | Done at d677de9e (U71b): `make update` rc 0, `make doctor` tools=passed, runtime=passed with the C6 and C7 warnings; ShellCheck 0.11.0 and shfmt 3.14.1 from the pins; the seat dry run refuses in 8 s naming the nested worktree. |
| B5 | Phase R done predicate (phase-r-plan.md). | Verify clause by clause at close, with evidence rows. |
| B6 | The audit model sometimes answers `Selected model is at capacity` and leaves no verdict. | Audits now run through the installed pr-audit.sh (ship.sh); a missing verdict exits 3 and is rerun. |

## C. Operator only

| id | problem | why the agent cannot | operator step | default if no answer |
| --- | --- | --- | --- | --- |
| C1 | Bot threads need an answer before merge (AGENTS.md merge rule). | Resolved without the operator on 2026-10-26: main's ruleset does not require thread resolution, and the agent answers with `gh pr comment` (`Refutes|Fixes bot finding <id>`, standing order 32); land.sh checks those comments. | none | n/a |
| C2 | CI reruns of a flaky job. | Tool policy blocks `gh run rerun`. | none needed: the agent gets a new run by merging origin/main into the branch. | n/a |
| C3 | <ubuntu-host> runs main at 81c74922: no srt and no ripgrep, so every seat launch there refuses after U85 (f1374ba7). | Standing orders 27 and 30: host changes go through the operator; ssh is read-only. | `make update` in ~/.local/share/chezmoi after the last unit lands (handouts/phase-r-operator.md). | Seats cannot start on <ubuntu-host>. |
| C4 | Nested worktrees inside the checkouts make every seat launch refuse after U95: 10 on macOS (.claude/worktrees, 8 under .gc-quarantine), 5 on <ubuntu-host> (G16 row 12). | No agent writes under ~/Workspace; standing order 30. | `git worktree remove` each (commands in the handout). | Seats refuse with a message naming the worktree. |
| C5 | G16 host cleanups not yet run. macOS rows 1, 2, 3, 7, 13 and <ubuntu-host> rows 5, 6, 8, 12 still show their pre-cleanup state; <ubuntu-host> rows 4 and 11 are done. | Standing order 30. | docs/operator-handout-g16.md, rerunning each dry-run first. | Leftovers stay; nothing breaks. |
| C6 | `make doctor` on macOS warns that the GitHub login is in the OS keyring, which the Claude sandbox cannot reach. | `make gh-auth` is an interactive login. | Run `make gh-auth`. | gh fails inside the Claude sandbox on macOS. |
| C7 | `make doctor` on macOS warns that `ai-coe-daily-ops@ai-coe` is enabled with no pin. It comes from a local directory marketplace under ~/Workspace (work content). | Pinning it in the public manifest would publish a work identifier; pinning it in the private source is a policy choice. | Choose: disable it, keep it with the warning, or ask for a private-source pin unit. | Keep it; the warning stays. |
| C8 | U88: seats use the operator's GitHub identity. | Creating a GitHub machine account needs a human. | Create the account and a fine-grained PAT (design in units.tsv U88). | U88 stays planned; G17 conditions still hold. |
| C9 | F027: whether SIWC model discovery returns a list. The probe parser is fixed (U79), but the live re-probe was never run. | The probe (`.orchestration/validation/025-pilot-s0-siwc-probe.py`) signs in through a browser OAuth consent on auth.openai.com with the operator's ChatGPT account and registers an agent; only the operator can consent. | Run the probe once, consent in the browser, and paste its model count; the agent then registers fetchDynamicModels if the list is non-empty. | Static model rows stay (works today). |
| C10 | The agent's read-only ssh to <ubuntu-host> now stops at a Tailscale SSH check (`# Tailscale SSH requires an additional check`, a login.tailscale.com link), so the agent can no longer measure that host. | The check is a browser login. | Approve the Tailscale SSH check once, or tell the coordinator to rely on your reports for that host. | The Ubuntu rows in this file stay as measured on 2026-10-26. |
