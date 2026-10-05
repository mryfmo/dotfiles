# T30 report — dot-codex-apparmor-userns-T30-a01

- worker: `claude-standard-dot-a005` (Claude Code, acting as worker per dispatch note)
- orchestrator: `claude-remediation-dot`
- worktree: `~/Workspace/dotfiles/.claude/worktrees/worker-c`
- branch: `feat/codex-apparmor-userns` (base `origin/main` = `c326c73`)
- task_rev: sha256 `469797747c33379e7d296ac9f0e9810ffcc9b6254ebf852b76c4699cc601c682`,
  verified against the task file at `c326c73`
- PR: https://github.com/mryfmo/dotfiles/pull/192, head `74b517b4331a7283b165610ceb89895dff14845c`
- status: ready_for_review. CI is green on head 74b517b: every check passes except nix, which was skipped. Verbatim output is in the validation file.
- scope ruling: level (b) and option A were approved by orchestrator PING
  (2026-09-27T04:53:46Z). remove-agent-asset is not extended.
- effects: `apparmor-bwrap-userns-profile` (see Effects)

## Investigation findings (verbatim in validation)

- Ubuntu 24.04.5, kernel 7.0.0-1019-nvidia (aarch64), AppArmor 4.0.1.
  - `apparmor_restrict_unprivileged_userns=1`, `unprivileged_userns_clone=1`,
    `max_user_namespaces=512927`.
  - `bwrap --ro-bind / / true` fails with `setting up uid map: Permission
    denied`, which confirms AppArmor is the gate.
- As a non-root user, `aa-status` and `/sys/kernel/security/apparmor/profiles`
  are unreadable.
- `/etc/apparmor.d` has the stock `unprivileged_userns` stacking profile, but
  no bwrap profile. Ubuntu 24.04 ships per-app profiles of the form
  `profile <name> <exe> flags=(unconfined) { userns, }`, for example chrome,
  lxc-usernsexec, and bazel's linux-sandbox.
- codex path: the mise shim resolves to `.../npm-openai-codex/0.157.1/bin/codex`,
  then `codex.js` (node), then the vendored musl `codex`, then
  `~/.codex/tmp/arg0/.../codex-linux-sandbox`, which **execs `/usr/bin/bwrap`
  by absolute path**. strace shows it twice: a `--help` capability probe, then
  the sandbox with `--unshare-user ...`.
  - A PATH-first logging shim was never invoked.
  - The vendored `codex-resources/bwrap` ("bubblewrap built for Codex") was not
    executed while `/usr/bin/bwrap` was present.
- **Why (b) is the narrowest level that works:**
  - The executable that creates the namespace is `/usr/bin/bwrap`, so a
    level-(a) profile on codex's own binaries would never attach.
  - Attaching to the vendored bwrap path would also be *weaker*. That path is
    user-writable and version-specific, so any file dropped there would
    inherit the grant.
  - `/usr/bin/bwrap` is root-owned, and the grant is scoped to that one
    executable, not the global sysctl.
  - Known ceiling: any caller of `/usr/bin/bwrap` gets a userns. This is the
    same trade-off as Ubuntu's stock per-app profiles. The profile header
    documents it, and names the upstream stacked `bwrap-userns-restrict` style
    as the upgrade path.

## Changes

1. `install/ubuntu/common/apparmor/bwrap-userns`: the profile source (new).
   - `abi <abi/4.0>`, `include <tunables/global>`,
     `profile bwrap-userns /usr/bin/bwrap flags=(unconfined) { userns, include if exists <local/bwrap-userns> }`.
   - It parses with `apparmor_parser -Q -K`. A broken negative control fails,
     so the check is real.
2. `install/ubuntu/common/apparmor_userns.sh` (new, shdoc English) and
   `home/.chezmoiscripts/ubuntu/run_onchange_after_07-apparmor-bwrap-userns.sh.tmpl`
   (new wrapper, Linux/debian-gated like its siblings).
   - The script runs `sudo install -m 0644 <source> /etc/apparmor.d/bwrap-userns`,
     then `sudo apparmor_parser -r` on it. Both steps are idempotent.
   - It is a no-op, with a one-line reason, when the restriction sysctl is not
     `1` or is absent, or when `apparmor_parser` or `/usr/bin/bwrap` is
     missing. The sysctl is never touched.
   - Profile source lookup order: the `APPARMOR_USERNS_PROFILE_SOURCE` seam,
     then `$CHEZMOI_SOURCE_DIR/../install/...` under chezmoi, then the
     script's own directory.
   - The wrapper embeds the profile's sha256, so a profile edit re-triggers
     the `run_onchange` step. The wrapper render was verified.
   - No `agent-config.yaml` entry was added: install/ scripts do not use the
     asset manifest, and option A was approved.
3. Doctor: `scripts/check-tools.sh` owns the check (`make doctor` runs it
   first). A new `check_apparmor_userns` function lives in a new "AppArmor"
   section.
   - It reports "not applicable" when the restriction is not `1`.
   - It gives `warn_optional` when codex is missing, and when bwrap is missing.
   - It runs the unprivileged probe `bwrap --ro-bind / / true`, and reports
     `found` when the probe succeeds.
   - When the probe fails it records a required failure. The hint depends on
     the profile file: missing means "chezmoi apply installs it"; present
     means "sudo apparmor_parser -r ...".
   - It does not check that the profile is loaded: the list of loaded
     profiles is root-only, so the effective probe is used instead.
   - On this host it currently reports the required failure truthfully,
     because the profile is not deployed.
4. `home/dot_agents/skills/agmsg-orchestration/SKILL.md`: the only two
   OpenSandbox lines now read "per-task isolation records (sandbox/worktree
   evidence)" and "Put the isolation status or fallback rationale in
   `expected_sandbox_file`." The record contract is unchanged, and historical
   records are untouched.
5. `AGENTS.md`: the operator-provided `## Code Review Rules` section is
   appended after `## Audit`. A `diff` against the task-file block is empty,
   so it is byte-identical.
6. `README.md`: one paragraph on why the profile exists, where it lives, the
   doctor probe, and the two removal commands.
7. Tests:
   - New `tests/unit/test_apparmor_userns.py` with 7 tests:
     - installer no-op for restriction-off, no-parser, and no-bwrap;
     - exact sudo install and reload calls, for both the repo checkout and the
       `CHEZMOI_SOURCE_DIR` source path;
     - installer fails and stops after the first failed sudo;
     - doctor reports not-applicable, warns optionally without codex, passes
       when the probe passes, and fails when the probe fails (profile missing
       and profile present-but-ineffective).
   - The mutation baseline has all 7 FAIL or ERROR against an origin/main
     export. I tightened one test that initially passed vacuously there.
   - `tests/unit/test_runtime_health.py`: `doctor_environment` now pins
     `APPARMOR_USERNS_SYSCTL` to a non-existent file. Without this, the
     existing doctor test read this host's real sysctl (=1) and gained an
     optional warning.

## Effects

`effects=apparmor-bwrap-userns-profile`

- The effect: at deploy time on a restricted Ubuntu host, `chezmoi apply` runs
  the step, which writes `/etc/apparmor.d/bwrap-userns` with sudo and loads it
  into the kernel with `apparmor_parser -r`.
- Reverse mapping (documented removal procedure, README):
  `sudo apparmor_parser -R /etc/apparmor.d/bwrap-userns && sudo rm /etc/apparmor.d/bwrap-userns`.
  The script's shdoc header also carries it.
- There is no asset-manifest step and no `remove-agent-asset` path (option A
  approved).
- It was **not activated on this host by this task**: no sudo was run and no
  sysctl was changed. In CI the step ran on both Ubuntu bootstrap jobs and
  skipped with `/usr/bin/bwrap is not installed`. The restriction and parser
  gates passed there, but the sudo path itself has only been exercised by unit
  tests. The first live install happens at operator deploy.

## After deploy (orchestrator/operator side)

1. `chezmoi apply` (prompts for sudo once).
2. `make doctor` should show `found:   bwrap user namespaces allowed`.
3. Re-run `codex --profile audit review --commit <sha>` and confirm the
   loopback/RTM_NEWADDR error is gone.

## Notes

- `test_permgate...test_bench_runs_five_layer_two_fixtures` failed once in the
  first full run (`successful_classifications` 0 != 5). It then passed 3/3 in
  isolation and in a full rerun (469 OK). It is timing-flaky and unrelated;
  learning suggests a de-flake task.
- `origin/main` advanced after I branched: 4642941 (mise pins) and 0c8d507
  (T31 task). The merge-base stat, which shows the branch's 9 files only, is in
  the validation file.
- The Understand-Anything post-commit graph-update hook was not run, because
  `.ua/` is outside allowed_files.

## Durable facts

[memory:decision] T30: dotfiles ships the `bwrap-userns` AppArmor profile (`/usr/bin/bwrap` flags=(unconfined) userns) via install/ubuntu/common/apparmor_userns.sh (run_onchange, sudo, no-op unless restricted) with a make doctor bwrap probe; global sysctl relaxation rejected; removal is documented (apparmor_parser -R + rm), no remove-agent-asset extension; OpenSandbox vocabulary removed (operator 2026-09-27).

[memory:failure] codex-cli 0.157.1 execs /usr/bin/bwrap by absolute path (not PATH, not its bundled codex-resources/bwrap); under apparmor_restrict_unprivileged_userns=1 every sandboxed codex run fails until /usr/bin/bwrap has a userns-granting profile.

CompactionDB (main checkout), decision id `891736ee-64fb-41ff-b9be-37616b2ffd8e`:

```
python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "T30: dotfiles ships an AppArmor userns profile restoring sandboxed codex under apparmor_restrict_unprivileged_userns=1 (narrowest executable-scoped grant, managed install step + doctor probe); global sysctl relaxation rejected; OpenSandbox rejected for this fleet (CLIs cannot delegate built-in sandboxes; containerization incompatible with the herdr/worktree/agmsg regime) and its vocabulary removed from the orchestration skill (operator 2026-09-27)"
```

cost: n/a
