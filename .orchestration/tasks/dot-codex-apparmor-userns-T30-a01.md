# AGMSG-TASK dot-codex-apparmor-userns-T30-a01

## Objective

Operator decision (2026-09-27): restore sandboxed Codex execution on Ubuntu
hosts by shipping an AppArmor unprivileged-user-namespace allowance via
dotfiles (managed install step + doctor check), instead of relaxing the
global `kernel.apparmor_restrict_unprivileged_userns` sysctl.

Host facts (verified 2026-09-27, reproduce before designing):

- `kernel.apparmor_restrict_unprivileged_userns = 1`,
  `kernel.unprivileged_userns_clone = 1`, max_user_namespaces ample.
- Bare `bwrap --ro-bind / / true` fails: `bwrap: setting up uid map:
Permission denied` — AppArmor is the gate, nothing else.
- Consequence: every sandboxed codex run fails
  (`codex --profile audit review --commit <sha>` →
  `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`, review
  blocked with an explicit non-verdict). Audit and security lanes are down.
- codex is installed via mise (`npm:@openai/codex`), reached through the mise
  shim; bwrap is the process that actually needs userns.

[memory:decision] T30: sandboxed codex execution is restored with a
dotfiles-managed AppArmor userns profile (narrowest working scope, preferring
the bwrap/codex executable path over any global sysctl change), installed by
a managed step and verified by doctor (operator 2026-09-27).

## Repo / branch

- Work ONLY in `~/Workspace/dotfiles/.claude/worktrees/worker-c`.
- `git fetch origin`, then
  `git switch -c feat/codex-apparmor-userns origin/main`.
  (Verify the dispatched task_rev sha256 against this file on your base, else
  stop and PONG.)
- If the worktree has uncommitted files, stop and report via AGMSG-PONG.

## Changes

### 1. Investigate (read-only, paste evidence)

- Current AppArmor state: `aa-status` (or
  `cat /sys/kernel/security/apparmor/profiles | grep -i 'bwrap\|unpriv'`),
  existing `/etc/apparmor.d/*bwrap*` / `*userns*` profiles, Ubuntu's stock
  `unprivileged_userns` profile semantics on this release.
- Resolve the real codex binary path behind the mise shim and how it invokes
  bwrap (which executable creates the namespace).
- Decide the NARROWEST profile that works, in this preference order:
  (a) a profile attached to the codex-shipped/bwrap executable path granting
  `userns,`; (b) a profile for `/usr/bin/bwrap` granting `userns,`;
  (c) anything wider requires an explicit orchestrator sign-off via PONG
  before implementation. Never propose the global sysctl.
  State in the report why the chosen level is the narrowest that works.

### 2. Ship the profile via dotfiles

- Add the AppArmor profile source under the repo's platform config area
  (follow existing Linux-only install-script conventions; shdoc English
  comments) and a managed install step that copies it to
  `/etc/apparmor.d/` and loads it (`apparmor_parser -r`) — sudo-gated,
  idempotent, Linux-only, no-op when AppArmor or the restriction is absent.
  Follow the existing install/ script + asset-manifest recording pattern
  (manifest step so `remove-agent-asset` can reverse it); declare the
  `/etc/apparmor.d` write as `effects=` in the RESULT.
- Do NOT activate it on this host from the task (no sudo in the worktree
  task); activation is orchestrator/operator-side at deploy.

### 3. Doctor check

- `make doctor` gains a Linux-only check: when
  `apparmor_restrict_unprivileged_userns=1`, verify the shipped profile is
  loaded and a probe `bwrap --ro-bind / / true` succeeds; report a clear
  warn/error otherwise (warn_optional if codex is not installed).

### 4. Remove the OpenSandbox vocabulary (operator decision 2026-09-27)

OpenSandbox (the Alibaba container control plane) was evaluated and rejected
for this fleet: the agent CLIs cannot delegate their built-in sandboxes, and
containerizing agents is structurally incompatible with the herdr-pane +
worktree + agmsg regime. It was never installed; only vocabulary remains.

- `home/dot_agents/skills/agmsg-orchestration/SKILL.md`: exactly two lines
  reference it (the `sandboxes/` layout line and Worker Playbook step 7).
  Replace the OpenSandbox mentions with neutral wording — e.g.
  `sandboxes/`: "per-task isolation records (sandbox/worktree evidence)";
  step 7: "Put the isolation status or fallback rationale in
  `expected_sandbox_file`." Keep the record contract itself unchanged (every
  task still writes a sandbox record).
- Do not rewrite historical `.orchestration/` records that mention
  OpenSandbox; history stays as written.

### 5. AGENTS.md — Code Review Rules section (operator-provided, verbatim)

Append the following section to `AGENTS.md` (after the `## Audit` section),
EXACTLY as written — operator-provided text, do not edit or reflow it:

```markdown
## Code Review Rules

### Dotfiles safety

- Do not silently change shell startup behavior, PATH order, authentication helpers, agent hooks, or permission policy defaults without calling out the user-visible impact.
- For security-sensitive files, check whether secrets, tokens, auth caches, local-only paths, or overly broad permissions could be exposed.
- Leave formatting-only feedback to CI unless it affects behavior.
```

### 6. Tests

- Unit tests for the new check and install-step logic per the existing
  fake/fixture patterns, with a mutation baseline (paste the FAILED run
  against unmodified scripts).
- No local bats (repo policy); do not run the sudo install step in tests.

## Allowed files

- the new AppArmor profile source file (name it per repo conventions; report
  the exact path)
- the new/extended install script under `install/` (+ its chezmoi wrapper if
  the pattern requires one)
- `home/dot_agents/agent-config.yaml` ONLY if the manifest step-recording
  pattern requires an entry (report why)
- `scripts/check-agent-runtime.py` or the doctor-owning script (report which
  file owns the check)
- `README.md` (one short paragraph: why the profile exists, how to remove)
- `home/dot_agents/skills/agmsg-orchestration/SKILL.md` (deliverable 4 only)
- `AGENTS.md` (deliverable 5 only, operator-provided verbatim text)
- matching unit test files under `tests/unit/`
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dot-codex-apparmor-userns-T30-a01.md` (main checkout)

## Forbidden actions

- Running anything with sudo; changing sysctls; activating the profile on
  this host; touching model_profiles, herdr-agents, permgate, hooks configs,
  dependencies, or `reviews/ADH_Integrated_Plan/`.
- Merging; force push; local bats; `make apply`/`chezmoi apply`; writes
  outside the worktree except the listed `.orchestration` paths.

## Validation commands (paste verbatim output)

```
make validate-agent-assets
make unit-test
git -C ~/Workspace/dotfiles/.claude/worktrees/worker-c diff origin/main --stat
gh pr checks <pr-number>
```

## Completion

1. PR to `main`, English title/description ending with
   `🤖 Generated with [Claude Code](https://claude.com/claude-code)`.
   Watch CI to green.
2. Artifacts at the exact expected paths; validation with verbatim outputs
   (including the mutation baseline) and the PR number/head SHA; `effects=`
   declared with its reverse mapping.
3. CompactionDB from the main checkout:
   `python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "T30: dotfiles ships an AppArmor userns profile restoring sandboxed codex under apparmor_restrict_unprivileged_userns=1 (narrowest executable-scoped grant, managed install step + doctor probe); global sysctl relaxation rejected; OpenSandbox rejected for this fleet (CLIs cannot delegate built-in sandboxes; containerization incompatible with the herdr/worktree/agmsg regime) and its vocabulary removed from the orchestration skill (operator 2026-09-27)"`
   — paste command and output.
4. `AGMSG-RESULT v1` with all artifact paths; `cost:` line in the report.
