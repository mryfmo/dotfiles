# dot-builtin-git-auto-T1-a01 validation

## Static validation

Command:

```text
bash -n setup.sh; mise x shellcheck -- shellcheck -x setup.sh; mise x shfmt -- shfmt -i 4 -sr -d setup.sh; static flag assertions; git diff --check
```

Verbatim output:

```text
bash -n setup.sh: OK
shellcheck setup.sh: OK
shfmt setup.sh: OK
built-in Git flag regression: OK
git diff --check: OK
```

## Initial VM sandbox attempt

The first full E2E attempt was rejected before VM access. Verbatim output:

```text
time="2026-09-21T13:25:11+09:00" level=warning msg="failed to detect whether running under rosetta, assuming false" error="failed to read sysctl \"sysctl.proc_translated\": operation not permitted"
time="2026-09-21T13:25:11+09:00" level=error msg="Instance `adh-test` has configuration errors" error="failed to get Info from `/Users/mryfmo/.lima/adh-test/ha.sock`: Get \"http://lima-hostagent/v1/info\": dial unix /Users/mryfmo/.lima/adh-test/ha.sock: connect: operation not permitted"
Control socket connect(/Users/mryfmo/.lima/adh-test/ssh.sock): Operation not permitted
ssh: connect to host 127.0.0.1 port 63006: Operation not permitted
```

## VM diagnostic retries

The first approved attempt exposed remote-shell quoting and cleaned both users. Verbatim output:

```text
chezmoi_2.70.4_linux_arm64.tar.gz: OK
bash: -c: line 26: syntax error near unexpected token `('
userdel: dotgita01 mail spool (/var/mail/dotgita01) not found
userdel: dotgitb01 mail spool (/var/mail/dotgitb01) not found
scratch cleanup: OK
```

The second approved attempt exposed the root-only `mktemp` directory mode and cleaned both users. Verbatim output:

```text
chezmoi_2.70.4_linux_arm64.tar.gz: OK
env: '/tmp/dot-builtin-git-auto.Vpr7Rj/chezmoi': Permission denied
userdel: dotgita01 mail spool (/var/mail/dotgita01) not found
userdel: dotgitb01 mail spool (/var/mail/dotgitb01) not found
scratch cleanup: OK
```

## Git-present and Git-absent VM E2E

The command downloaded and checksum-verified the pinned chezmoi 2.70.4 Linux arm64 archive, created users `dotgita01` and `dotgitb01`, and ran this shared init command:

```text
chezmoi init https://github.com/mryfmo/dotfiles --branch main --use-builtin-git auto --no-tty --promptString "Email address=ci@example.invalid" --promptString "System (client or server)=server"
```

For `dotgita01`, `PATH` started with a logging wrapper that delegated to `/usr/bin/git`. For `dotgitb01`, `PATH` contained only an empty directory. An EXIT trap removed both users and the validated `/tmp/dot-builtin-git-auto.*` directory.

Verbatim output:

```text
chezmoi_2.70.4_linux_arm64.tar.gz: OK
Cloning into '/home/dotgita01/.local/share/chezmoi'...
git-present command: clone --recurse-submodules --branch main https://github.com/mryfmo/dotfiles.git /home/dotgita01/.local/share/chezmoi
git-present clone: OK
git-absent builtin clone: OK
userdel: dotgita01 mail spool (/var/mail/dotgita01) not found
userdel: dotgitb01 mail spool (/var/mail/dotgitb01) not found
scratch cleanup: OK
```

## VM cleanup check

Command:

```text
limactl shell adh-test -- bash -lc '<assert both users and /tmp/dot-builtin-git-auto.* are absent>'
```

Verbatim output:

```text
scratch users and temp directories absent: OK
```

## CompactionDB memory

Command:

```text
python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'dot-builtin-git-auto-T1-a01: setup.sh passes --use-builtin-git auto to both chezmoi init and update, preferring external Git when present while preserving built-in Git bootstrap when Git is absent; both paths were verified with credential-free scratch users in adh-test.'
```

Verbatim output:

```text
c40194a2-19ed-4a3a-bf76-6a90f3bbc889
```

## Deliberately not run

```text
bats: not run locally (repository policy); the changed Bats test is left for CI.
```

## Crit review receipt

review_surface: crit-data
reviewer: codex
review_source: .agents/worklog/codex/review/dot-builtin-git-auto-T1-a01-crit-comments.json
review_outcome: approved

The first gate invocation requested agent review. Verbatim output:

```text
Native agent review required before completion.
- broad diff touches 8 files
- broad diff changes 220 lines
Use the active agent's review path, not a browser by default:
- Codex: retrieve Crit comments/status data, review it inside the task, then address findings.
- Claude Code: retrieve Crit comments/status data, review it inside the task, then address findings.
- Use browser Crit review only when the user explicitly asks for Crit web UI or Crit data is unavailable.
Record a receipt with `review_surface:`, `reviewer:`, and `review_outcome:`.
For agent judgment, locate the review with `crit status --json`, then save `crit comments --all --json <review.json>` to a repo-local JSON file.
Evidence must contain at least one resolved record; for a finding-free review, add and resolve one review-scope approval record.
This local evidence is process evidence, not reviewer authentication.
Then use `review_surface: crit-data`, `reviewer: codex` or `reviewer: claude-code`, and `review_source: <json path>`.
After addressing review feedback, rerun with AGENT_REVIEWED=1 or CRIT_REVIEWED=1 plus REVIEW_EVIDENCE=<path>.
make: *** [require-crit-review] Error 1
```

Final gate command:

```text
AGENT_REVIEWED=1 REVIEW_EVIDENCE=.orchestration/validation/dot-builtin-git-auto-T1-a01.md make require-crit-review
```

Verbatim output:

```text
Review requirement satisfied by AGENT_REVIEWED=1 with REVIEW_EVIDENCE.
```

## Final artifact and scope check

Verbatim output:

```text
required task artifacts: OK
worklog status done: OK
final built-in Git references: OK
final git diff --check: OK
 M setup.sh
 M tests/install/common/setup.bats
?? .orchestration/autoskill/runs/dot-builtin-git-auto-T1-a01.md
?? .orchestration/learning/dot-builtin-git-auto-T1-a01.md
?? .orchestration/reports/dot-builtin-git-auto-T1-a01.md
?? .orchestration/sandboxes/dot-builtin-git-auto-T1-a01.md
?? .orchestration/tasks/dot-builtin-git-auto-T1-a01.md
?? .orchestration/validation/dot-builtin-git-auto-T1-a01.md
```

Post-evidence command:

```text
git diff --check && printf 'post-evidence git diff --check: OK\n'
```

Verbatim output:

```text
post-evidence git diff --check: OK
```
