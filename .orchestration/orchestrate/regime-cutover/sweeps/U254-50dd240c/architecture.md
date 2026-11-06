# Architecture: dotfiles at 50dd240c (scoped to unit U254)

## Product, principals and resources

A personal dotfiles repository whose `install/ubuntu/server/` scripts set up an Ubuntu server.

The chezmoi `run_once` script `home/.chezmoiscripts/ubuntu/run_once_50-server-setup-timezone.sh.tmpl` includes `install/ubuntu/server/setup_timezone.sh`. It applies only on a Debian-like Linux host whose `.system` is `server`. The step runs as the operator, with sudo, during bootstrap. The same scripts run inside CI's server bootstrap legs on GitHub-hosted runners.

**Principals.** The operator, who owns the bootstrap environment and holds sudo; root, who owns `/etc/localtime` and `/etc/timezone`; and CI, which sets `GITHUB_ACTIONS` on runners.

**Resources.** `/etc/localtime`, `/etc/timezone`, and the installed `tzdata` package. The timezone is configuration, not a security control.

## The change under hunt (b49be338..50dd240c, one commit)

`main` (`setup_timezone.sh:33-55`) now:
1. exports `TZ=Asia/Tokyo` (`:34`);
2. returns 0 with one line when `GITHUB_ACTIONS` is non-empty (`:36-39`);
3. reads `/etc/localtime` through `current_zone_file`, which runs `readlink -f` (`:23-25`, `:41-44`), treating a failure as an unknown zone;
4. returns 0 when the resolved path ends in `/Asia/Tokyo` (`:45-48`);
5. otherwise runs the three sudo commands: `ln -snf` with a now-quoted target (`:51`), `tee /etc/timezone` (`:52`), and `apt-get install -y tzdata` with `DEBIAN_FRONTEND` passed as a sudo argument (`:54`).

The bats test (`tests/install/ubuntu/server/setup_timezone.bats:12-65`) fakes `sudo` and `readlink` as shell functions and covers five cases.

## Entry surfaces and paths

1. **The `GITHUB_ACTIONS` variable.** It comes from the bootstrap's environment and selects the skip branch.
2. **The `/etc/localtime` link target.** It is resolved by `readlink -f` and judged by its tail.
3. **The sudo command lines.** They use the fixed `TZ` and literals only.
4. **The test fakes and the chezmoi wiring.**

## Trust boundaries and strongest controls

- **Bootstrap environment to step.** Only the operator, or CI, sets `GITHUB_ACTIONS`. The skip removes a privileged write and adds none.
- **`/etc/localtime` to step.** The file is root-owned, so the only principal that can craft it already has the step's authority. The write goes to a fixed path with a fixed target, and `ln -snf` replaces the link itself.
- **Values to sudo.** `TZ` is assigned a literal before every use, so the environment cannot set it. `current_zone_file`'s output reaches only an `echo`.

## Prior coverage

run-5 (`~/.local/state/omp-seats/dotfiles/.state/sweep-2/security-audit/run-5`, source 2256b56c, U240) is carried as the newest ledger. The brief names run-3, but run-5 already carries every earlier unit. U240 is absent at this head, so run-5's nine covered U240 units carry as changed-source, out-of-scope units. No prior run holds a finding.

## Companion selection

`DESKTOP-MOBILE-AND-LOCAL-IPC.md` is selected, for its `Local file ownership and TOCTOU` block on the `/etc/localtime` resolution. Every other companion is excluded with its reason in the ledger.

## Execution and independence limits of this run

No target code ran, by task rule and AGENTS.md's bats policy. The delegation tool (Task) and eval kernel are denied by policy on this seat, so every phase ran in the parent. `run-metadata.json` records the run as incomplete for that reason.

## Output directory

The brief names `run-5`, which already holds the U258 sweep. This run writes to `run-6` and leaves `run-5` untouched.
