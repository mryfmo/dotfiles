# DeepSeek harness (dsh) under srt

The DeepSeek harness control host runs under Anthropic's sandbox-runtime as the
`dsh` role of `scripts/orchestrator/hcom-seat` (installed as
`~/.local/bin/common/hcom-seat`; regime-cutover U272, after the four audits of
the standalone launcher of PR 687 withdrew it). From a checkout of this
repository, `hcom-seat dsh [--profile <name>] [--home <DSH_HOME>] -- <dsh args>`
renders the worker seat's srt settings with the role's own rows and nothing
else: the write roots are `DSH_HOME` (the `--home` option, else the
environment's `DSH_HOME`, else `~/.dsh`), a per-launch state slot
`<seats-root>/.state/dsh-<utc stamp>-<pid>` holding the scratch cwd and the
bridge child's `CLAUDE_CONFIG_DIR`, the role's own omp profile
`~/.omp/profiles/dsh` (where the login child `omp auth-gateway stdio` lives,
selected by `OMP_PROFILE`) and `~/.omp/run`; the read grants are the role's own
as well (the scratch cwd and its state slot, `DSH_HOME`, `~/.omp/profiles/dsh`,
`~/.agents/skills` and the lever's pinned tool directory; U272c). srt reads
everything an explicit deny does not name, so a grant the role lacks denies
nothing: the role's containment is a deny list it owns (U272d). After the
worker's read denies (credentials, the operator's Claude Code state,
`~/.omp/agent`, the chezmoi sources, `~/Workspace`, `~/.local/state/hcom`,
every seats root, the main checkout), the dsh settings deny for read and for
write the physical paths of the checkout's git directory and git common
directory, the `.git` entry of every linked worktree git lists, the hcom store
`HCOM_DIR` and every existing `~/.local/state/hcom-*` sibling store (the
lever's own `hcom-seat` directory excepted), the records directory
`<checkout>/.orchestration` and every other seat's directory under the seats
root. Every row of the settings' final `allowRead` and `allowWrite` lists is
judged against every row of their final `denyRead` and `denyWrite` lists
(every path compared physically and by identity), and a grant that is,
contains or lies inside a deny is refused by name before any directory is
made, the only exemptions being the own slot and cwd against the seats-root
and project-file rows they overlap by construction and the own profile
against the profiles deny, each by a tag the rendering attaches and only
while the grant lies where it is rendered (U272f); the per-launch slots are
removed with their modes reset, a slot that remains failing the launch with
exit 2 on a normal exit and under a signal alike (U272e, U272f).
Git directories elsewhere on the host are not computed by the lever and are
not denied. The domain list, no unix socket and no local binding are the
worker's. The lever's
existing containment does the rest: every tool it runs outside the sandbox
is pinned by its physical argv and refused when it, or a directory above it,
has the identity of any seat write root, `DSH_HOME` included from the first
statement, so a `node` or `python3` planted under `DSH_HOME` never runs; the
shim
`<seats-root>/.sandbox/dsh-<stamp>-<pid>/bin/dsh` proves the sandbox with the
four-word canary (a write into the sandbox directory, reads of the settings
file and `~/.ssh`, a write under the operator's `~/.claude/debug` must all fail
inside) and only then execs `srt --settings <file> -- /usr/bin/env PATH=<seat
path> <DSH_HOME>/bin/dsh [--profile <name>] <args>`; the lever runs that shim
in the foreground under `/usr/bin/env -i` with `HOME`, `USER`, `LANG`, `TERM`,
`PATH`, `DSH_HOME`, `OMP_PROFILE` and a caller's `CLAUDE_CODE_OAUTH_TOKEN`
alone, waits, removes the per-launch slots and returns dsh's status; a hangup,
interrupt or termination runs the same removal before the lever ends by that
signal. Before the launch the lever places the kit's rendered overlay
`~/.agents/omp/profiles/dsh.yml` (the bridge route as `modelRoles.default`,
the bridge extension, the seat providers off) as the profile's own
`~/.omp/profiles/dsh/agent/config.yml`, the file the gateway child reads for
its providers, with the extension entry at its canonical allow-list path; the
write is one run of the pinned helper `profile-config-place.py` beside the
lever, every step on one held descriptor of `agent/` (`dir_fd`, `O_NOFOLLOW`:
the compare, an exclusive create at a random name, the write, the rename, a
read-back), so an equal file is left alone, a different one replaced, and a
linked `agent/` or `config.yml`, a directory at `config.yml`, an entry at the
temporary's name or a failed step refuses with exit 2 naming the step (U310,
U310d; `tests/unit/test_profile_config_place.py`). The dsh
runtime is never executed outside srt. Two launches at once share no settings
file. The role's rows and the hazard-by-hazard account of the four verdicts
are in `scripts/orchestrator/README.md` ("The dsh role") and the tests in
`tests/unit/test_hcom_seat_dsh.py`.
