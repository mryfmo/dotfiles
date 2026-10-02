# AGMSG-TASK dot-ccstatusline-ubuntu26-hang-T59-a01

Drafted 2026-10-03 by the orchestrator seat; operator-approved ("A で進めろ、T59 を起票しろ"). Worker: `claude-standard-dot-a005` in `/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c`.

## Objective

T58 (#229) added the non-required canary cell `test (ubuntu-26.04, client)`. It is red on every run: in the step "Smoke-test statusline tools without network", `scripts/check-statusline-tools.py` (5 s timeout per command) raises `subprocess.TimeoutExpired` on `/home/runner/.local/share/mise/installs/npm-ccstatusline/2.2.30/bin/ccstatusline --version` under `sudo unshare --net` with `HTTP_PROXY=http://127.0.0.1:1` (run 37064146970, job 111027711303, image ubuntu-26.04 / ubuntu26/20260927.149, Python 3.14). The same command passes on ubuntu-24.04 and macos-14. Until the canary is green, every PR's feedback sweep carries a `failure` item that would have to be dispositioned repeatedly, which the operator has forbidden.

Find the root cause and fix it at the root, so that the canary passes without weakening the check:

1. Reproduce on the canary cell with diagnostics only (a PR whose first commit adds temporary diagnostics to the canary run is acceptable, but the final head must not contain them): capture what `ccstatusline --version` does for those 5 s on 26.04 without network. Candidates to test, each with evidence from the job log: node startup (`node --version` under the same `unshare --net`), the mise shim/launcher of the npm package, a first-run update/telemetry check inside ccstatusline that waits on DNS or a proxy connect (`HTTPS_PROXY` points at a closed port, so a connect fails fast, but a DNS lookup or a long retry would not), an IPv6/localhost resolution difference on the 26.04 image, Python 3.14 `subprocess` behaviour with the 5 s timeout. Use `strace -f -tt` or `NODE_DEBUG=net,dns`/`timeout 30` as diagnostics in the temporary commit.
2. Fix the cause where it lives: if ccstatusline itself phones home on `--version`, disable it through its documented environment or config (ccstatusline docs/README, pinned version 2.2.30) in the smoke invocation and, if that setting matters for users too, in `home/dot_ccstatusline/settings.json` or the rendered Claude statusLine command; if the cause is the node/mise launch path on 26.04, fix the invocation in `test.yaml` or the installer; if the cause is the 5 s budget being too tight for a cold start on that image while the behaviour is otherwise correct, state the measured cold-start time and justify any budget change in `scripts/check-statusline-tools.py` (with the matching unit test). Do not simply raise the timeout without a measured reason, and do not drop the no-network smoke.
3. If the root cause is a defect in ccstatusline that a newer release fixes, do not bump the pin here: report the upstream fix (version, changelog link) and stop; pins travel through the operator's `make upgrade` and a pin task (T37/T53 precedent).
4. Final head: canary `test (ubuntu-26.04, client)` green, all required checks green, no diagnostics left, `make unit-test` OK.

[memory:decision] T59 (operator 2026-10-03): the Ubuntu 26.04 canary stays non-required but must be green; a canary failure is fixed at its root (here `ccstatusline --version` hanging without network on the 26.04 image), never dispositioned repeatedly.

## Repo / branch

- Work ONLY in the worker-c worktree. `git fetch origin`; `git switch -c fix/ccstatusline-ubuntu26-hang origin/main` (750cc4a9 or later). Verify the dispatched task_rev sha256 against this file; else stop and PONG blocked. If the worktree has uncommitted files, stop and PONG.

## Allowed files

- `.github/workflows/test.yaml` (the statusline smoke step and, temporarily, diagnostics on the canary cell only)
- `scripts/check-statusline-tools.py`, `tests/unit/test_statusline_tools.py`
- `home/dot_ccstatusline/settings.json`, `home/dot_agents/agent-config.yaml` (only the Claude `statusLine` command/env if the fix is an environment variable for ccstatusline), and its rendered outputs via `make render-check` if touched
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dot-ccstatusline-ubuntu26-hang-T59-a01.md` (main checkout)

## Forbidden actions

- Changing any pin (mise, agent-config assets); removing or weakening the no-network smoke; marking the canary as always-passing; merging; force push; local bats; `make apply`; pushing `main`.

## Validation commands (paste verbatim output)

```
git diff origin/main --stat
make unit-test
make render-check            # if agent-config.yaml or settings were touched
make validate-agent-assets
gh pr checks <pr-number>     # test (ubuntu-26.04, client) must be pass on the final head
gh run view --job <canary-job-id> --log | grep -iE 'ccstatusline|statusline|timed out'   # the passing canary's smoke lines
```

Also paste the diagnostic job log excerpt that shows the root cause (the evidence behind the fix), with the run/job ids.

## Completion

1. PR to `main`, English title/description ending with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. CI green including the canary.
2. Artifacts at the exact expected paths; validation with verbatim outputs, PR number and head SHA, root-cause evidence.
3. CompactionDB `memory add --kind decision --scope project` with the `[memory:decision]` text; paste command and output.
4. `AGMSG-RESULT v1` via `agmsg-dispatch dotfiles claude-standard-dot-a005 claude-remediation-dot wT:p1 "<single line>"` (outside the sandbox). `cost:` line. max_turns=30.

## PONG decision 1 (2026-10-02T22:34Z, status=blocked: second canary failure)

Verified by the orchestrator from job 111054323730 (`FileExistsError: [Errno 17] File exists: '/bin/grub-ntldr-img' -> .../no-tar-bin/grub-ntldr-img`): `test_agmsg_refuses_to_install_without_tar` iterates `/usr/bin` then `/bin` (the same directory under usrmerge); the 26.04 image ships a dangling `/usr/bin/grub-ntldr-img` symlink, so the first pass creates a dangling link in `no-tar-bin`, `Path.exists()` follows it and answers False on the second pass, and `symlink_to` raises.

- Decision: `tests/unit/test_runtime_health.py` is added to the allowed files, limited to that guard. Fix the condition once (`not (path.exists() or path.is_symlink())`, or `os.path.lexists`); do not catch `FileExistsError`, skip entries, or dedupe the directory list, and keep the test's purpose (a PATH without `tar`) unchanged. Same objective: the canary passes at its root on the final head.
- The cold-start-only finding for `ccstatusline --version` is noted; the fix must still name what the cold start waits on (which path, which timeout) with log evidence, not only the observation that a warm call passes.
