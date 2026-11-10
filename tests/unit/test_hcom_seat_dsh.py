"""Exercise the `dsh` role of scripts/orchestrator/hcom-seat (regime-cutover U272) on the scratch host of
tests/unit/test_hcom_seat.py.

The role differs from the worker by the rows of the lever's role table and nothing else, so the tests hold the role's
settings to the worker's with the named rows substituted, and the launch to what the table says: a per-launch slot,
the listed environment names, the command resolved under `DSH_HOME`, the canary refusal, the exec argv. The shim runs
under `/usr/bin/env -i`, so the fake srt here takes its instructions from a file beside it, never from the
environment, and the fake dsh records what reached it into a file the test names. Nothing real starts.
"""

import copy
import hashlib
import json
import os
import re
import shlex
import signal
import shutil
import stat
import subprocess
import sys
import tarfile
import textwrap
import time
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_hcom_seat  # noqa: E402  # the fixture, as a module attribute so its tests are not collected twice

# The unit run has no PyYAML of its own (tests/unit/test_kwp_skills_drift.py): the one YAML read-back below runs in
# the `uv run --with pyyaml` child the Makefile's probe warms, and a child that fails is a failure, never a pass.
UV_PYYAML = [
    shutil.which("uv") or "uv",
    "run",
    "--offline",
    "--no-config",
    "--no-project",
    "--with",
    "pyyaml",
    "python",
    "-I",
]
YAML_EXTENSIONS = "import json, sys, yaml\nprint(json.dumps(yaml.safe_load(sys.stdin.read())['extensions']))\n"


def yaml_extensions(text):
    """The `extensions` list PyYAML reads from `text`, through the uv child; a non-zero exit raises with its stderr."""
    run = subprocess.run([*UV_PYYAML, "-c", YAML_EXTENSIONS], input=text, capture_output=True, text=True, check=False)
    if run.returncode != 0:
        raise AssertionError(f"uv pyyaml reader exited {run.returncode}: {run.stderr}")
    return json.loads(run.stdout)


SYSTEM_PATH = test_hcom_seat.SYSTEM_PATH
SHARED_CLAUDE_DENIES = test_hcom_seat.SHARED_CLAUDE_DENIES
# Built at runtime like FAKE_OAUTH_VALUE, and named without the word the secret scan's `generic-token` rule keys on.
CALLER_OAUTH_VALUE = "caller-" + "value-u272"
# bash itself exports these into every child; the role's list is everything else.
BASH_OWN_NAMES = {"PWD", "SHLVL", "OLDPWD", "_"}
# The heads before each round's row: the omp roles' settings are held byte-identical to every one of them.
EARLIER_HEADS = (
    "52873a37745d8141eada2139ea2fa76e2773a60d",  # round one, before the read grants became a role row (U272c)
    "976fd6cdb249c76ac397ede1bbfccd931ad824c1",  # round two, before the deny row and the DSH_HOME refusal (U272d)
    "5b950a97028205f7430a7c9f36f74b91a79e88c8",  # round three, before the refusal read the rendered deny table (U272e)
    "d1ffd91939e4d069b01d0e4d467c12eff971a944",  # round four, before the judge read every rendered grant (U272f)
    "d191911256d88f4a71ebde559500353dbc4d1e19",  # round five, before the exemptions named one row by position (U272g)
    "2b2415f6cae8b5d1db8d65a560f7cfb9e48e5ab6",  # main after U306, before the profile config row (U310)
)

# The head before the router row (U321, the U318 head this branch starts from): the dsh role's settings are held
# byte-identical to it, the per-launch name aside.
DSH_EARLIER_HEADS = ("e0dd8cc221de0b19477d82c850d1f631042bef4d",)


def interpreter_own_names():
    """The names the host's python3 (the fakes' interpreter) adds to an empty environment on its own: Apple's
    /usr/bin/python3 trampoline exports SDKROOT, CPATH, LIBRARY_PATH and MANPATH; a plain interpreter adds none."""
    probe = subprocess.run(
        ["/usr/bin/env", "-i", f"PATH={SYSTEM_PATH}", "python3", "-c", "import json, os; print(json.dumps(sorted(os.environ)))"],
        capture_output=True, text=True, check=True,
    )  # fmt: skip
    return set(json.loads(probe.stdout)) - {"PATH"}


def flatten(value, path=""):
    """One `{json-pointer-like path: leaf}` map of a parsed settings file, so two renderings diff row by row."""
    if isinstance(value, dict):
        items = value.items()
    elif isinstance(value, list):
        items = enumerate(value)
    else:
        return {path: value}
    out = {}
    for key, item in items:
        out.update(flatten(item, f"{path}/{key}"))
    return out


FAKE_SRT = textwrap.dedent(
    """\
    #!/usr/bin/env python3
    import json, os, subprocess, sys
    conf = json.load(open(os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), "srt.json")))
    argv = sys.argv[1:]
    with open(os.path.join(conf["calls"], "srt"), "a") as calls:
        calls.write(json.dumps({"argv": argv, "env": sorted(os.environ), "cwd": os.getcwd()}) + "\\n")
    if argv == ["--version"]:
        print("0.0.81")
        sys.exit(0)
    command = argv[argv.index("--") + 1 :]
    if command[:2] == ["/bin/sh", "-c"]:
        answer = os.path.join(conf["calls"], "canary-answer")
        if os.path.exists(answer):
            print(open(answer).read().strip())
            sys.exit(0)
        denied = ["/nonexistent-u272/canary", "/nonexistent-u272/settings", "/nonexistent-u272/.ssh",
                  "/nonexistent-u272/.claude/debug/canary"]
        sys.exit(subprocess.run(["/bin/sh", "-c", command[2], command[3], *denied], check=False).returncode)
    os.execvp(command[0], command)
    """
)
FAKE_DSH = textwrap.dedent(
    """\
    #!/usr/bin/env python3
    import json, os, sys, time
    calls = {calls!r}
    with open(os.path.join(calls, "dsh"), "a") as record:
        record.write(json.dumps({{"argv": sys.argv[1:], "argv0": sys.argv[0], "cwd": os.getcwd(),
                                 "env": dict(os.environ),
                                 "cred_root_dir": os.path.isdir(os.path.join(os.environ.get("DSH_HOME", "/nonexistent"),
                                                                             "router-credentials"))}}) + "\\n")
    if os.path.exists(os.path.join(calls, "leave-locked")):
        os.makedirs("locked/inner")
        open("locked/inner/file", "w").close()
        os.chmod("locked/inner", 0)
        os.chmod("locked", 0)
    if "--version" in sys.argv[1:]:
        print("0.2.1-rc.5")
    deadline = time.monotonic() + 30
    while os.path.exists(os.path.join(calls, "hold")) and not os.path.exists(os.path.join(calls, "release")):
        if time.monotonic() > deadline:
            sys.exit("fake dsh: never released")
        time.sleep(0.05)
    status = os.path.join(calls, "dsh-status")
    sys.exit(int(open(status).read()) if os.path.exists(status) else 0)
    """
)
# The dsh role's rendered profile config overlay (regime-cutover U310), as the generator renders it with the fixture's
# home: the lever places it as the profile's `agent/config.yml` with the extension entry at its canonical allow-list
# path. The extension line is a parameter so a test can spell it through a link.
DSH_OVERLAY = textwrap.dedent(
    """\
    # Generated from home/dot_agents/agent-config.yaml by scripts/generate-agent-configs.py.
    modelRoles:
      default: claude-bridge/claude-opus-5-5
    skills:
      enabled: false
    extensions:
      - {extension}
    disabledProviders:
      - agent-plugins
      - openai-codex
      - native
    setupVersion: 2
    startup:
      setupWizard: false
      checkUpdate: false
    """
)


def yaml_quoted(path):
    """A single-quoted YAML scalar of `path`, the form the lever writes each extension entry in (a `'` doubled), so a
    path holding ` # `, a quote or a trailing space is read whole (U310e)."""
    return "'" + str(path).replace("'", "''") + "'"


def placed_overlay(extension):
    """The config the lever places from DSH_OVERLAY: the extension entry at `extension`, quoted."""
    return DSH_OVERLAY.format(extension=yaml_quoted(extension))


def helper_hash_hook(action):
    """A BASH_ENV text wrapping the lever's hash readers (`sha256sum`, `shasum`): the bytes hashed go through a
    temporary under `U310_HASH_TMP`, and when they are the helper's (`cmp` against `U310_HELPER_PATH`) `action` runs
    after the digest is read; the lever's and regime-env's self-checks hash other bytes and pass untouched. Keyed on
    the bytes, not on the call's position, so one hook fits 384cd256 (the helper's path hashed second) and this head
    (the lever's copy hashed right before its run, after regime-env's self-check)."""
    return (
        "hash_read() { local real tmp status=0;"
        ' tmp=$(/usr/bin/mktemp "${U310_HASH_TMP}/hash.XXXXXX") || return 7; /bin/cat > "${tmp}" || return 7;'
        ' if real=$(type -P sha256sum); then "${real}" < "${tmp}" || status=$?;'
        ' else real=$(type -P shasum) && "${real}" -a 256 < "${tmp}" || status=$?; fi;'
        f' if /usr/bin/cmp -s "${{tmp}}" "${{U310_HELPER_PATH}}"; then {action}; fi;'
        ' /bin/rm -f -- "${tmp}"; return "${status}"; }\n'
        'sha256sum() { hash_read "$@"; }\nshasum() { hash_read "$@"; }\n'
    )


class HcomSeatDshTest(test_hcom_seat.SeatFixture):
    # The lever under test; a driver may run the round-4 probes against an earlier head's lever extracted beside its
    # own regime-env and manifest (the EARLIER_HEADS form), where each probe must fail (U310d ACCEPTANCE 2).
    lever = test_hcom_seat.SEAT

    def setUp(self):
        super().setUp()
        (self.bindir / "srt").write_text(FAKE_SRT)
        (self.bindir / "srt.json").write_text(json.dumps({"calls": str(self.calls)}))
        self.dsh_home = Path(self.temp.name).resolve() / "dsh-home"
        (self.dsh_home / "bin").mkdir(parents=True)
        self.dsh = self.dsh_home / "bin/dsh"
        self.dsh.write_text(FAKE_DSH.format(calls=str(self.calls)))
        self.dsh.chmod(0o755)
        # The rendered overlay the role's profile config is placed from (U310), as chezmoi deploys it.
        (self.profiles / "dsh.yml").write_text(DSH_OVERLAY.format(extension=self.bridge))
        self.profile_config = self.home / ".omp/profiles/dsh/agent/config.yml"

    def dsh_calls(self):
        return self.calls_of("dsh")

    def launch(self, *args, **overrides):
        env = {**self.env, **{key: value for key, value in overrides.items() if value is not None}}
        for key in (key for key, value in overrides.items() if value is None):
            env.pop(key, None)
        argv = [str(self.lever), "dsh", "--seats-root", self.seats, "--home", str(self.dsh_home), *args]
        return subprocess.run(argv, cwd=self.repo, env=env, capture_output=True, text=True, check=False)

    def held_launch(self, *args, count=1, new_session=False, role="dsh", seat=None, home=None, **overrides):
        """Start `count` launches of `role` (dsh, or router, U321) by the lever `seat` (this head's by default) under the
        DSH_HOME `home` (the fixture's by default) whose dsh waits for `release`, and return them once every dsh has
        recorded itself, so the per-launch slots can be read while they exist; `new_session` makes each launcher its
        own process group, the target of a signal to the group."""
        (self.calls / "hold").touch()
        env = {**self.env, **overrides}
        argv = [
            str(seat or test_hcom_seat.SEAT),
            role,
            "--seats-root",
            self.seats,
            "--home",
            str(home or self.dsh_home),
            *args,
        ]
        before = len(self.dsh_calls())
        procs = [
            subprocess.Popen(
                argv,
                cwd=self.repo,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                start_new_session=new_session,
            )  # fmt: skip
            for _ in range(count)
        ]
        deadline = time.monotonic() + 60
        while len(self.dsh_calls()) < before + count:
            if time.monotonic() > deadline or any(proc.poll() is not None for proc in procs):
                outputs = [proc.communicate() for proc in procs]
                self.fail(f"a launch ended before its dsh recorded itself: {outputs}")
            time.sleep(0.05)
        return procs

    def release(self, procs):
        (self.calls / "release").touch()
        results = [proc.communicate() for proc in procs]
        (self.calls / "hold").unlink()
        (self.calls / "release").unlink()
        return [(proc.returncode, out, err) for proc, (out, err) in zip(procs, results)]

    def slots(self):
        """The per-launch sandbox and state slots that exist now, as (sandbox names, state names); the shared Claude
        Code directory `.state/claude` (U318) outlives every launch and is no slot."""
        sandbox = Path(self.seats, ".sandbox")
        state = Path(self.seats, ".state")
        return (
            sorted(p.name for p in sandbox.iterdir()) if sandbox.exists() else [],
            sorted(p.name for p in state.iterdir() if p.name != "claude") if state.exists() else [],
        )

    def without_launch_name(self, settings, name):
        """`settings` (a parsed settings file, or its bytes) with the per-launch seat name `name` replaced by
        `<launch>`, so two launches, of one role or of the dsh and router roles, compare."""
        if isinstance(settings, bytes):
            return settings.replace(name.encode(), b"<launch>")
        return json.loads(json.dumps(settings).replace(name, "<launch>"))

    def without_credential_rows(self, settings):
        """This head's rendered dsh settings (bytes) with exactly the U353 rows removed: the Router's credential root
        `<DSH_HOME>/router-credentials`, once in denyRead and once in denyWrite, each after another row; nothing else
        names it."""
        needle = b"," + json.dumps(f"{self.dsh_home}/router-credentials").encode()
        self.assertEqual(settings.count(needle), 2, settings)
        text = settings.replace(needle, b"")
        self.assertNotIn(b"router-credentials", text)
        return text

    def omp_credential_root(self):
        """The credential root the omp roles deny (U353b, U353d): the kit's root under the fixture's HOME, no DSH_HOME
        set; every launch makes it (U353d)."""
        return f"{self.home.resolve()}/.dsh/router-credentials"

    def without_omp_credential_rows(self, settings):
        """This head's rendered omp settings (bytes) with exactly the U353b and U353d rows removed: the Router's
        credential root under `~/.dsh`, once in denyRead (U353b) and once in denyWrite (U353d), each after another row;
        nothing else names it."""
        needle = b"," + json.dumps(self.omp_credential_root()).encode()
        self.assertEqual(settings.count(needle), 2, settings)
        text = settings.replace(needle, b"")
        self.assertNotIn(b"router-credentials", text)
        return text

    def store_root(self):
        """The program store's root regime-env derives for the fixture's checkout (U215c), which the omp roles read and
        the orchestrator writes (U219)."""
        return f"{self.home.resolve()}/.local/state/regime-store/repo"

    def without_store_root_rows(self, settings, role):
        """This head's rendered omp settings (bytes) with exactly the U219 rows removed: the store root once in
        allowRead for both roles, once in allowWrite for the orchestrator and once in denyWrite for the worker
        (U219c), each after another row; nothing else names it."""
        needle = b"," + json.dumps(self.store_root()).encode()
        self.assertEqual(settings.count(needle), 2, settings)
        text = settings.replace(needle, b"")
        self.assertNotIn(b"regime-store", text)
        return text

    def without_dsh_store_root_row(self, settings):
        """This head's rendered dsh or router settings (bytes) with exactly the U219c row removed: the store root once
        in denyWrite, after another row; nothing else names it."""
        needle = b"," + json.dumps(self.store_root()).encode()
        self.assertEqual(settings.count(needle), 1, settings)
        text = settings.replace(needle, b"")
        self.assertNotIn(b"regime-store", text)
        return text

    def earlier_lever(self, head):
        """The `hcom-seat` of the earlier `head`, unpacked with its manifest into the scratch (git archive of its
        `scripts/orchestrator` and manifest, so its self-check reads its own pin and it sources its own regime-env); a
        checkout without that commit (a shallow or squashed clone) skips the calling test."""
        probe = subprocess.run(
            ["git", "-C", str(test_hcom_seat.ROOT), "cat-file", "-e", f"{head}^{{commit}}"],
            env=self.env, capture_output=True, text=True, check=False,
        )  # fmt: skip
        if probe.returncode != 0:
            self.skipTest(f"the earlier head {head} is not in this checkout (a shallow or squashed clone)")
        old_root = Path(self.temp.name).resolve() / f"head-{head[:8]}"
        old_root.mkdir()
        archive = old_root / "tree.tar"
        subprocess.run(
            ["git", "-C", str(test_hcom_seat.ROOT), "archive", "--format=tar", "-o", str(archive), head,
             "scripts/orchestrator", "home/dot_agents/agent-config.yaml"],
            env=self.env, capture_output=True, text=True, check=True,
        )  # fmt: skip
        with tarfile.open(archive) as tar:
            tar.extractall(old_root, **({"filter": "data"} if hasattr(tarfile, "data_filter") else {}))
        old_seat = old_root / "scripts/orchestrator/hcom-seat"
        self.assertTrue(os.access(old_seat, os.X_OK), old_seat)
        return old_seat

    def test_the_dsh_settings_are_the_workers_but_the_named_rows(self):
        """The role table's rows are the only difference: the cwd and state slot for the worktree, DSH_HOME and the
        role's own omp profile for the git common directory, the hcom store and the worker profile, the role's own
        read grants, and the deny pair of the Router's credential root `<DSH_HOME>/router-credentials` (U353; the
        worker's own pair of it lies under `~/.dsh`, U353b and U353d); the rest of the read denies, the network and
        everything else are the worker's."""
        run = self.seat("worker", "--seats-root", self.seats)
        self.assertEqual(run.returncode, 0, run.stderr)
        worker = self.settings_of("worker")
        procs = self.held_launch("--", "--version")
        sandboxes, states = self.slots()
        (name,) = [entry for entry in sandboxes if entry != "worker"]
        self.assertEqual(sorted(states), sorted(["worker", name]))
        self.assertRegex(name, r"^dsh-\d{8}-\d{6}-\d+$")
        dsh = self.settings_of(name)
        ((status, out, err),) = self.release(procs)
        self.assertEqual((status, out), (0, "0.2.1-rc.5\n"), err)
        home = self.home.resolve()
        clone, cwd = str(Path(self.seats, "worker")), str(Path(self.seats, ".state", name, "cwd"))
        state_w, state_d = str(Path(self.seats, ".state/worker")), str(Path(self.seats, ".state", name))
        common, store = str((self.repo / ".git").resolve()), str(self.store.resolve())
        # allowWrite: the worker's first six rows are the clone, its state, the shared Claude Code directory (U318),
        # the common directory, the store and its profile; the dsh role's are the cwd, its state, the shared
        # directory, DSH_HOME and its profile; the rest is the same list.
        shared = str(Path(self.seats, ".state/claude"))
        write_w, write_d = worker["filesystem"]["allowWrite"], dsh["filesystem"]["allowWrite"]
        self.assertEqual(write_w[:6], [clone, state_w, shared, common, store, str(home / ".omp/profiles/worker")])
        self.assertEqual(write_d[:5], [cwd, state_d, shared, str(self.dsh_home), str(home / ".omp/profiles/dsh")])
        self.assertEqual(write_d[5:], write_w[6:])
        self.assertIn(str(home / ".omp/run"), write_d)
        self.assertNotIn(common, write_d)
        self.assertNotIn(store, write_d)
        # allowRead (U272c): the role's own grants, in the row's order; none of the worker's rows but the substituted
        # cwd, state slot and profile and the shared directory (the git directory, the store and the checkout's
        # records are the worker's alone).
        read_w, read_d = worker["filesystem"]["allowRead"], dsh["filesystem"]["allowRead"]
        self.assertEqual(read_w[:3], [clone, common, store])
        self.assertIn(shared, read_w)
        self.assertEqual(
            read_d,
            [cwd, state_d, shared, str(self.dsh_home), str(home / ".omp/profiles/dsh"), str(home / ".agents/skills"),
             str(self.tools)],
        )  # fmt: skip
        # denyWrite: the project files under the seat directory move with it; the worker's `.git` file has no dsh
        # counterpart (no worktree); the credential root (U353; the worker's own row of it under `~/.dsh`, U353d, is
        # taken out) and the deny row (U272d: the git common directory, the worker clone's `.git` entry, it being a
        # linked worktree, the hcom store, the records and the other seat's directory) follow the worker's denies; the
        # macOS worktree patterns and every other deny are the same. In denyRead the credential root's row stands
        # last, after the deny row (U343l: the router row's denyRead is a prefix of the dsh row's).
        cred = str(self.dsh_home / "router-credentials")
        row = [common, clone + "/.git", store, str(self.repo.resolve() / ".orchestration"), clone]
        deny_w = [entry for entry in worker["filesystem"]["denyWrite"]
                  if not entry.startswith(clone + "/") and entry != self.omp_credential_root()]  # fmt: skip
        deny_d = [entry for entry in dsh["filesystem"]["denyWrite"] if not entry.startswith(cwd + "/")]
        self.assertEqual([e for e in deny_d if "*" not in e], [e for e in deny_w if "*" not in e] + [cred] + row)
        self.assertEqual([e for e in deny_d if "*" in e], [e for e in deny_w if "*" in e])
        self.assertEqual(
            [entry[len(cwd) :] for entry in dsh["filesystem"]["denyWrite"] if entry.startswith(cwd + "/")],
            [entry[len(clone) :] for entry in worker["filesystem"]["denyWrite"] if entry.startswith(clone + "/") and entry != clone + "/.git"],
        )  # fmt: skip
        worker_deny_read = [e for e in worker["filesystem"]["denyRead"] if e != self.omp_credential_root()]
        self.assertEqual(dsh["filesystem"]["denyRead"], worker_deny_read + row + [cred])
        self.assertEqual(dsh["network"], worker["network"])
        self.assertEqual({k: v for k, v in dsh.items() if k not in ("filesystem", "network")},
                         {k: v for k, v in worker.items() if k not in ("filesystem", "network")})  # fmt: skip
        # The slots are per launch: both are gone once dsh exited; the worker's stay.
        self.assertEqual(self.slots(), (["worker"], ["worker"]))

    def test_the_dsh_read_grants_name_no_git_hcom_or_record_path(self):
        """PR 697 thread 4492139503 (U272c): an allowRead entry re-opens a path under the broad denyRead, so the dsh
        role's list names neither the checkout's git common directory, nor the hcom store, nor the coordinator's
        records under the checkout, by itself or by an ancestor; the checkout stays read-denied. The worker's list
        does name them, so the fixture's paths are the ones the role would have inherited."""
        procs = self.held_launch("--", "--version")
        (name,) = self.slots()[0]
        dsh = self.settings_of(name)["filesystem"]
        ((status, out, err),) = self.release(procs)
        self.assertEqual((status, out), (0, "0.2.1-rc.5\n"), err)
        run = self.seat("worker", "--seats-root", self.seats)
        self.assertEqual(run.returncode, 0, run.stderr)
        worker = self.settings_of("worker")["filesystem"]
        checkout = self.repo.resolve()
        common, store, records = checkout / ".git", self.store.resolve(), checkout / ".orchestration/orchestrate"
        for path in (common, store, records):
            with self.subTest(path=str(path)):
                self.assertIn(str(path), worker["allowRead"], "the worker's grant, the one the role used to inherit")
                self.assertFalse(
                    [entry for entry in dsh["allowRead"] if Path(entry) in (path, *path.parents)],
                    f"the dsh role re-opens {path} or an ancestor: {dsh['allowRead']}",
                )
        # The checkout is read-denied and no grant re-opens it or lies under it (the records row was the one that did).
        self.assertIn(str(checkout), dsh["denyRead"])
        for entry in dsh["allowRead"]:
            self.assertNotIn(str(checkout), (entry, *(str(p) for p in Path(entry).parents)), entry)
        self.assertEqual(self.slots(), (["worker"], ["worker"]))

    def without_shared_claude_rows(self, settings):
        """This head's rendered settings with exactly the U318 rows removed: the shared Claude Code directory, once in
        allowRead and once in allowWrite, and its eight configuration denies in denyWrite; each is present once."""
        shared = str(Path(self.seats, ".state/claude"))
        text = settings
        for row in (shared, shared, *(f"{shared}/{name}" for name in SHARED_CLAUDE_DENIES)):
            needle = json.dumps(row).encode() + b","
            self.assertIn(needle, text, row)
            text = text.replace(needle, b"", 1)
        self.assertNotIn(shared.encode(), text)
        return text

    def test_the_omp_roles_settings_are_byte_identical_to_the_earlier_heads(self):
        """No round's row changes an omp role's settings: the worker's and the orchestrator's `srt-settings.json`
        rendered by this head equal, byte for byte, the ones each earlier head (EARLIER_HEADS) renders on the same
        scratch host, once exactly the U318 rows (without_shared_claude_rows), the credential-root deny pair (U353b,
        U353d; without_omp_credential_rows) and the store-root grants (U219; without_store_root_rows) are taken out. An
        earlier lever runs from its own tree (git archive of its `scripts/orchestrator` and manifest, so its self-check
        reads its own pin); a checkout without that commit skips it."""
        for head in EARLIER_HEADS:
            old_seat = self.earlier_lever(head)
            for role in ("worker", "orchestrator"):
                rendered = {}
                for label, seat in (("earlier head", old_seat), ("this head", test_hcom_seat.SEAT)):
                    run = subprocess.run(
                        [str(seat), role, "--seats-root", self.seats], cwd=self.repo, env=self.env,
                        capture_output=True, text=True, check=False,
                    )  # fmt: skip
                    self.assertEqual(run.returncode, 0, f"{label} {head[:8]} {role}: {run.stderr}")
                    rendered[label] = Path(self.seats, ".sandbox", role, "srt-settings.json").read_bytes()
                with self.subTest(head=head[:8], role=role):
                    this_head = self.without_store_root_rows(
                        self.without_omp_credential_rows(self.without_shared_claude_rows(rendered["this head"])), role
                    )
                    self.assertEqual(rendered["earlier head"], this_head)
                    self.assertIn(b'"allowRead":[', rendered["this head"])

    def test_two_launches_at_once_share_no_settings_file_and_each_slot_goes_with_its_dsh(self):
        """U251d P1 `:704`: every launch has its own sandbox, settings file and state slot; the Claude Code directory is
        the seats root's shared one (U318)."""
        procs = self.held_launch("--", "--version", count=2)
        sandboxes, states = self.slots()
        self.assertEqual(len(sandboxes), 2, sandboxes)
        self.assertEqual(sandboxes, states)
        for name in sandboxes:
            self.assertTrue(Path(self.seats, ".sandbox", name, "srt-settings.json").is_file(), name)
            self.assertTrue(Path(self.seats, ".sandbox", name, "bin/dsh").is_file(), name)
            self.assertTrue(Path(self.seats, ".state", name, "cwd").is_dir(), name)
            self.assertFalse(Path(self.seats, ".state", name, "claude").exists(), name)
            self.assertEqual(stat.S_IMODE(os.lstat(Path(self.seats, ".state", name)).st_mode), 0o700)
        records = self.dsh_calls()
        self.assertEqual(sorted(Path(record["env"]["HCOM_SEAT_SANDBOX"]).name for record in records), sandboxes)
        shared = str(Path(self.seats, ".state/claude"))
        self.assertEqual({record["env"]["CLAUDE_CONFIG_DIR"] for record in records}, {shared})
        self.assertTrue(Path(shared).is_dir() and not Path(shared).is_symlink())
        self.assertEqual(len({record["cwd"] for record in records}), 2)
        launches = [call for call in self.calls_of("srt") if call["argv"][2:4] == ["--", "/usr/bin/env"]]
        self.assertEqual(len({launch["argv"][1] for launch in launches}), 2, "two settings files")
        for status, out, err in self.release(procs):
            self.assertEqual((status, out), (0, "0.2.1-rc.5\n"), err)
        self.assertEqual(self.slots(), ([], []))
        # dsh's own status comes back, and a failing dsh leaves no slot either.
        (self.calls / "dsh-status").write_text("7")
        run = self.launch("--", "--version")
        self.assertEqual(run.returncode, 7, run.stderr)
        self.assertEqual(self.slots(), ([], []))

    def test_the_environment_reaching_dsh_is_the_listed_names_and_the_shims_exports(self):
        """U251d P1 `:146` and U251b P2 `:325`: nothing of the caller's environment reaches the shim, srt or dsh but
        the listed names and the shared Claude Code directory; the shim's own exports (that directory again, the AWS
        file names, the signing rows) ride as for every role; U312, U318: a caller's token is no input and none rides."""
        caller = {
            "SECRET_OF_THE_CALLER": "never", "NODE_OPTIONS": "--require /tmp/evil.js", "USER": "u272",
            "LANG": "C.UTF-8", "TERM": "xterm", "HCOM_TEAM": "repo",
        }  # fmt: skip
        run = self.launch("--profile", "thak", "--", "--version", **caller)
        self.assertEqual((run.returncode, run.stdout), (0, "0.2.1-rc.5\n"), run.stderr)
        (dsh,) = self.dsh_calls()
        env = dsh["env"]
        expected = {
            "HOME", "PATH", "DSH_HOME", "OMP_PROFILE", "USER", "LANG", "TERM", "UV_CACHE_DIR", "CLAUDE_CONFIG_DIR",
            "AWS_SHARED_CREDENTIALS_FILE", "AWS_CONFIG_FILE", "GIT_CONFIG_COUNT",
            "GIT_CONFIG_KEY_0", "GIT_CONFIG_VALUE_0", "GIT_CONFIG_KEY_1", "GIT_CONFIG_VALUE_1", "HCOM_SEAT_SANDBOX",
        }  # fmt: skip
        self.assertEqual(set(env) - BASH_OWN_NAMES - interpreter_own_names(), expected)
        self.assertEqual(
            {env["USER"], env["LANG"], env["TERM"], env["OMP_PROFILE"], env["DSH_HOME"]},
            {"u272", "C.UTF-8", "xterm", "dsh", str(self.dsh_home)},
        )
        self.assertTrue(env["PATH"].startswith(f"{self.tools}:/usr/bin:/bin:/usr/sbin:/sbin:"), env["PATH"])
        self.assertEqual(env["CLAUDE_CONFIG_DIR"], str(Path(self.seats, ".state/claude")))
        self.assertRegex(dsh["cwd"], rf"^{re.escape(self.seats)}/\.state/dsh-\d{{8}}-\d{{6}}-\d+/cwd$")
        self.assertEqual((env["AWS_SHARED_CREDENTIALS_FILE"], env["AWS_CONFIG_FILE"]), ("/dev/null", "/dev/null"))
        self.assertEqual(dsh["argv"], ["--profile", "thak", "--version"])
        # The canary and the launch srt saw the same reduced names (the version probe runs under the lever's own).
        version, canary, launch = self.calls_of("srt")
        self.assertEqual(version["argv"], ["--version"])
        for call in (canary, launch):
            self.assertNotIn("SECRET_OF_THE_CALLER", call["env"])
            self.assertNotIn("NODE_OPTIONS", call["env"])
            self.assertNotIn("HCOM_TEAM", call["env"])
        # U312, U318: a caller's token is no input and no token rides for any role: the name never reaches dsh.
        run = self.launch("--", "--version", CLAUDE_CODE_OAUTH_TOKEN=CALLER_OAUTH_VALUE, USER=None)
        self.assertEqual(run.returncode, 0, run.stderr)
        env = self.dsh_calls()[-1]["env"]
        self.assertNotIn("CLAUDE_CODE_OAUTH_TOKEN", env)
        self.assertNotIn(CALLER_OAUTH_VALUE, env.values())
        self.assertNotIn("USER", env)
        self.assertNotIn(CALLER_OAUTH_VALUE, run.stdout + run.stderr)

    def test_the_command_and_its_home_are_resolved_and_refused_like_a_tool(self):
        """`<DSH_HOME>/bin/dsh` must be an executable regular file under a clean, existing DSH_HOME; the dsh options
        belong to the dsh role alone; a DSH_HOME inside a protected path is refused by the overlap invariant; a tool
        planted under DSH_HOME never runs. Every refusal is exit 2 with nothing created or started."""
        spaced = Path(self.temp.name).resolve() / "dsh home"
        spaced.mkdir()
        planted_home = Path(self.temp.name).resolve() / "planted-home"
        (planted_home / "bin").mkdir(parents=True)
        (planted_home / "bin/dsh").write_text(FAKE_DSH.format(calls=str(self.calls)))
        (planted_home / "bin/dsh").chmod(0o755)
        marker = Path(self.temp.name) / "planted-ran"
        for tool in ("node", "python3"):
            (planted_home / "bin" / tool).write_text(f"#!/bin/sh\n: > {shlex.quote(str(marker))}\nexit 0\n")
            (planted_home / "bin" / tool).chmod(0o755)
        no_command = Path(self.temp.name).resolve() / "no-command"
        (no_command / "bin").mkdir(parents=True)
        not_executable = Path(self.temp.name).resolve() / "not-executable"
        (not_executable / "bin").mkdir(parents=True)
        (not_executable / "bin/dsh").write_text("#!/bin/sh\nexit 0\n")
        inside = self.repo / "dsh-home"
        (inside / "bin").mkdir(parents=True)
        (inside / "bin/dsh").write_text("#!/bin/sh\nexit 0\n")
        (inside / "bin/dsh").chmod(0o755)
        cases = [
            (["dsh", "--home", str(self.temp.name) + "/absent", "--", "--version"], {}, "DSH_HOME is not a directory"),
            (["dsh", "--home", str(spaced), "--", "--version"], {}, "is not a clean absolute path"),
            (["dsh", "--home", str(no_command), "--", "--version"], {}, "cannot resolve the dsh command to a physical executable file"),
            (["dsh", "--home", str(not_executable), "--", "--version"], {}, "cannot resolve the dsh command to a physical executable file"),
            (["dsh", "--home", str(self.dsh_home), "--profile", "bad name", "--", "--version"], {}, "profile 'bad name' is outside"),
            (["dsh", "--home", str(self.dsh_home), "--ext", str(self.bridge)], {}, "--ext is an option of the omp roles"),
            (["worker", "--profile", "thak"], {}, "--profile, --home and -- are options of the dsh and router roles"),
            (["worker", "--", "--version"], {}, "--profile, --home and -- are options of the dsh and router roles"),
            (["dsh", "--home", str(inside), "--", "--version"], {}, "lies inside the main checkout"),
            (["dsh", "--home", str(planted_home), "--", "--version"], {"PATH": f"{planted_home}/bin:{self.env['PATH']}"}, "lies under the seat write root"),
            (["dsh", "--", "--version"], {"DSH_HOME": str(self.temp.name) + "/absent"}, "DSH_HOME is not a directory"),
        ]  # fmt: skip
        for argv, env, message in cases:
            with self.subTest(argv=argv[1:]):
                run = self.seat(*argv, "--seats-root", self.seats, **env)
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertIn(message, run.stderr)
        self.assertFalse(Path(self.seats).exists())
        self.assertEqual(self.dsh_calls(), [])
        self.assertFalse(marker.exists(), "a planted node or python3 under DSH_HOME never ran")
        # The planted home launches once its bin is off the caller's PATH: the tools come from elsewhere, and the
        # planted files, under DSH_HOME, are never resolved or run.
        run = self.seat("dsh", "--home", str(planted_home), "--seats-root", self.seats, "--", "--version")
        self.assertEqual((run.returncode, run.stdout), (0, "0.2.1-rc.5\n"), run.stderr)
        self.assertFalse(marker.exists())
        # The environment's DSH_HOME is the default; --home wins over it.
        run = self.seat("dsh", "--seats-root", self.seats, "--", "--version", DSH_HOME=str(self.dsh_home))
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(self.dsh_calls()[-1]["env"]["DSH_HOME"], str(self.dsh_home))

    def test_a_canary_that_finds_the_sandbox_open_starts_no_dsh(self):
        """The dsh shim refuses as the omp shim does when the canary answers anything but the four words, and the
        per-launch slots go with the refusal."""
        for answer in (
            "write-open read-denied ssh-denied debug-denied",
            "write-denied read-denied ssh-denied",
            "write-denied read-denied ssh-denied debug-open",
        ):
            with self.subTest(answer=answer):
                (self.calls / "canary-answer").write_text(answer + "\n")
                run = self.launch("--", "--version")
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertIn("the sandbox does not hold", run.stderr)
                self.assertIn("dsh not started", run.stderr)
                self.assertEqual(self.dsh_calls(), [])
                self.assertEqual(self.slots(), ([], []))
        (self.calls / "canary-answer").unlink()
        run = self.launch("--", "--version")
        self.assertEqual((run.returncode, run.stdout), (0, "0.2.1-rc.5\n"), run.stderr)

    def test_srt_receives_the_canary_and_the_exec_argv_and_a_dry_run_creates_nothing(self):
        """The exec argv: `--settings <per-launch file> -- /usr/bin/env PATH=<seat path> <physical dsh> [--profile
        <name>] <args>`; the canary runs under the same file first; the dry run prints the foreground launch line
        with the environment names and no token, and makes no slot."""
        run = self.launch("--profile", "thak", "--", "--version", "--flag", USER="u272")
        self.assertEqual((run.returncode, run.stdout), (0, "0.2.1-rc.5\n"), run.stderr)
        version, canary, launch = self.calls_of("srt")
        self.assertEqual(version["argv"], ["--version"])
        settings = canary["argv"][1]
        self.assertRegex(settings, rf"^{re.escape(self.seats)}/\.sandbox/dsh-\d{{8}}-\d{{6}}-\d+/srt-settings\.json$")
        self.assertEqual(canary["argv"][:5], ["--settings", settings, "--", "/bin/sh", "-c"])
        self.assertEqual(launch["argv"][:4], ["--settings", settings, "--", "/usr/bin/env"])
        self.assertEqual(
            launch["argv"][4], f"PATH={self.tools}:/usr/bin:/bin:/usr/sbin:/sbin:{self.bindir}:{SYSTEM_PATH}"
        )
        self.assertEqual(launch["argv"][5:], [str(self.dsh.resolve()), "--profile", "thak", "--version", "--flag"])
        (dsh,) = self.dsh_calls()
        self.assertEqual(dsh["argv0"], str(self.dsh.resolve()))
        before = len(self.calls_of("srt"))
        run = self.launch("--dry-run", "--", "--version", USER="u272", CLAUDE_CODE_OAUTH_TOKEN=CALLER_OAUTH_VALUE)
        self.assertEqual(run.returncode, 0, run.stderr)
        line = shlex.split(run.stdout)
        self.assertEqual(line[:2], ["/usr/bin/env", "-i"])
        self.assertEqual(
            line[2:8],
            [f"HOME={self.home}", f"PATH={self.tools}:/usr/bin:/bin:/usr/sbin:/sbin", f"DSH_HOME={self.dsh_home}",
             "OMP_PROFILE=dsh", f"CLAUDE_CONFIG_DIR={Path(self.seats, '.state/claude')}", "USER=u272"],
        )  # fmt: skip
        self.assertRegex(line[8], rf"^{re.escape(self.seats)}/\.sandbox/dsh-\d{{8}}-\d{{6}}-\d+/bin/dsh$")
        self.assertEqual(line[9:], ["--version"])
        self.assertNotIn(CALLER_OAUTH_VALUE, run.stdout + run.stderr)
        self.assertEqual(len(self.calls_of("srt")), before + 1, "the dry run reads the srt version and starts nothing")
        self.assertEqual(len(self.dsh_calls()), 1)
        self.assertEqual(self.slots(), ([], []), "the dry run makes no per-launch slot")

    def test_the_router_settings_are_the_dsh_settings_but_the_loopback_grant_and_the_state_root(self):
        """U321: the router role is one more row of the role table, the dsh row with the loopback grant and the Router's
        state root. Its rendered settings, the per-launch name aside, equal the dsh role's with exactly five changes:
        `allowLocalBinding` true and `<DSH_HOME>/router-state` as allowWrite row 6, after `~/.omp/run` (U321), the
        credential root `<DSH_HOME>/router-credentials` as allowRead row 7 instead of the dsh row's denyRead row of it
        (U353; both rows deny writing it), and (U343i) the broker directory `<state slot>/broker` as one more
        `denyWrite` row, after every deny the dsh row renders and before the macOS patterns, in no grant list; every
        other row (the shared omp profile `~/.omp/profiles/dsh` among them, so the tagged positions hold), every other
        deny, the domain list and the rest are equal, and the dsh role's own settings keep the binding false and no
        broker row. dsh receives the fixed profile and the shared `OMP_PROFILE`; both roles' slots go when dsh exits."""
        rendered = {}
        for role in ("dsh", "router"):
            procs = self.held_launch("--", "--version", role=role)
            (name,) = self.slots()[0]
            self.assertRegex(name, rf"^{role}-\d{{8}}-\d{{6}}-\d+$")
            rendered[role] = self.without_launch_name(self.settings_of(name), name)
            ((status, out, err),) = self.release(procs)
            self.assertEqual((status, out), (0, "0.2.1-rc.5\n"), err)
            self.assertEqual(self.slots(), ([], []), f"the {role} slots are gone once dsh exited")
        dsh, router = rendered["dsh"], rendered["router"]
        home = self.home.resolve()
        state_root = f"{self.dsh_home}/router-state"
        broker_dir = f"{Path(self.seats).resolve()}/.state/<launch>/broker"
        patterns = [row for row in dsh["filesystem"]["denyWrite"] if "*" in row]
        broker_at = len(dsh["filesystem"]["denyWrite"]) - len(patterns)
        cred = f"{self.dsh_home}/router-credentials"
        expected = copy.deepcopy(dsh)
        expected["network"]["allowLocalBinding"] = True
        expected["filesystem"]["allowWrite"].insert(6, state_root)
        expected["filesystem"]["allowRead"].append(cred)
        expected["filesystem"]["denyRead"].remove(cred)
        expected["filesystem"]["denyWrite"].insert(broker_at, broker_dir)
        self.assertEqual(router, expected)
        self.assertIs(dsh["network"]["allowLocalBinding"], False)
        self.assertNotIn(state_root, json.dumps(dsh))
        self.assertNotIn("/broker", json.dumps(dsh), "the dsh row renders no broker row")
        self.assertEqual(
            router["filesystem"]["allowWrite"][3:7],
            [str(self.dsh_home), str(home / ".omp/profiles/dsh"), str(home / ".omp/run"), state_root],
        )
        self.assertNotIn(state_root, router["filesystem"]["allowRead"], "DSH_HOME, read row 3, already reads it")
        self.assertEqual(router["filesystem"]["denyWrite"].count(broker_dir), 1, "the broker row once, in denyWrite")
        for kind in ("allowRead", "allowWrite", "denyRead"):
            self.assertNotIn(broker_dir, router["filesystem"][kind], f"the broker row is in no {kind} list")
        # The flattened diff, U321's inserted row, U353's two rows and U343i's broker row taken out, is the one binding
        # value and nothing else.
        trimmed = copy.deepcopy(router)
        del trimmed["filesystem"]["allowWrite"][6]
        del trimmed["filesystem"]["allowRead"][7]
        trimmed["filesystem"]["denyRead"].insert(dsh["filesystem"]["denyRead"].index(cred), cred)
        del trimmed["filesystem"]["denyWrite"][broker_at]
        flat_dsh, flat_router = flatten(dsh), flatten(trimmed)
        diff = {
            key: (flat_dsh.get(key), flat_router.get(key))
            for key in sorted(set(flat_dsh) | set(flat_router))
            if flat_dsh.get(key) != flat_router.get(key)
        }
        self.assertEqual(diff, {"/network/allowLocalBinding": (False, True)})
        dsh_call, router_call = self.dsh_calls()
        self.assertEqual(dsh_call["argv"], ["--version"])
        self.assertEqual(router_call["argv"], ["--profile", "router", "--version"])
        self.assertEqual((dsh_call["env"]["OMP_PROFILE"], router_call["env"]["OMP_PROFILE"]), ("dsh", "dsh"))
        self.assertEqual((dsh_call["env"]["DSH_HOME"], router_call["env"]["DSH_HOME"]), (str(self.dsh_home),) * 2)

    def test_the_router_role_runs_the_router_profile_alone(self):
        """U321: the router role's grants exist for the Router, so the role accepts the DSH profile `router` alone
        (`--profile router` or none) and refuses any other by name, exit 2, before any tool is resolved or anything is
        made; the profile shape rule, the `--ext` refusal and the omp roles' refusal of the dsh options hold for it as
        for dsh."""
        cases = (
            (["router", "--profile", "thak"], "the router role runs the DSH profile 'router' alone; --profile 'thak' is refused"),
            (["router", "--profile", "dsh", "--dry-run"], "the router role runs the DSH profile 'router' alone; --profile 'dsh' is refused"),
            (["router", "--profile", "bad name"], "profile 'bad name' is outside"),
            (["router", "--ext", str(self.bridge)], "--ext is an option of the omp roles"),
            (["worker", "--profile", "router"], "--profile, --home and -- are options of the dsh and router roles"),
        )  # fmt: skip
        for args, message in cases:
            with self.subTest(args=args):
                run = self.seat(*args, "--seats-root", self.seats, "--home", str(self.dsh_home), "--", "--version")
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertIn(message, run.stderr)
        self.assertFalse(Path(self.seats).exists())
        self.assertEqual((self.calls_of("srt"), self.dsh_calls()), ([], []))

    def test_a_router_dry_run_prints_the_launch_line_with_the_router_profile_and_makes_no_slot(self):
        """U321: `hcom-seat router [--profile router] --dry-run -- <args>` prints the foreground launch line with the
        router per-launch shim, `OMP_PROFILE=dsh` and `--profile router` first among dsh's arguments, whether the
        profile was given or defaulted, reads the srt version and makes no seats root and no slot."""
        for args in (["--profile", "router"], []):
            with self.subTest(args=args):
                before = len(self.calls_of("srt"))
                run = self.seat("router", "--seats-root", self.seats, "--home", str(self.dsh_home), *args, "--dry-run",
                                "--", "--version", USER="u321")  # fmt: skip
                self.assertEqual(run.returncode, 0, run.stderr)
                line = shlex.split(run.stdout)
                self.assertEqual(line[:2], ["/usr/bin/env", "-i"])
                self.assertEqual(
                    line[2:8],
                    [f"HOME={self.home}", f"PATH={self.tools}:/usr/bin:/bin:/usr/sbin:/sbin", f"DSH_HOME={self.dsh_home}",
                     "OMP_PROFILE=dsh", f"CLAUDE_CONFIG_DIR={Path(self.seats, '.state/claude')}", "USER=u321"],
                )  # fmt: skip
                self.assertRegex(line[8], rf"^{re.escape(self.seats)}/\.sandbox/router-\d{{8}}-\d{{6}}-\d+/bin/dsh$")
                self.assertEqual(line[9:], ["--profile", "router", "--version"])
                self.assertEqual(
                    len(self.calls_of("srt")), before + 1, "the dry run reads the srt version and starts nothing"
                )
        self.assertFalse(Path(self.seats).exists(), "the dry run makes no seats root and no slot")
        self.assertEqual(self.dsh_calls(), [])

    def test_the_router_canary_refuses_like_the_dsh_roles_and_both_slots_go(self):
        """U321: the router shim is the dsh shim: a canary that finds the sandbox open starts no dsh, exit 2, and the
        per-launch slots go with the refusal; with the canary holding, the launch goes through and the slots go too."""
        (self.calls / "canary-answer").write_text("write-open read-denied ssh-denied debug-denied\n")
        run = self.seat("router", "--seats-root", self.seats, "--home", str(self.dsh_home), "--", "--version")
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertIn(
            "the sandbox does not hold (canary: write-open read-denied ssh-denied debug-denied); dsh not started",
            run.stderr,
        )
        self.assertEqual(self.dsh_calls(), [])
        self.assertEqual(self.slots(), ([], []))
        (self.calls / "canary-answer").unlink()
        run = self.seat("router", "--seats-root", self.seats, "--home", str(self.dsh_home), "--", "--version")
        self.assertEqual((run.returncode, run.stdout), (0, "0.2.1-rc.5\n"), run.stderr)
        (dsh,) = self.dsh_calls()
        self.assertEqual(dsh["argv"], ["--profile", "router", "--version"])
        self.assertEqual(self.slots(), ([], []))

    def test_the_dsh_settings_are_byte_identical_to_the_u318_head(self):
        """U321: the router row changes no byte of the dsh role's settings. The dsh `srt-settings.json` this head renders
        equals, byte for byte, the one the U318 head (DSH_EARLIER_HEADS) renders on the same scratch host, the
        per-launch name aside (without_launch_name), the two U353 rows taken out (without_credential_rows: the
        credential root's denyRead and denyWrite rows, the one change U353 makes to the dsh row) and the store root's
        denyWrite row taken out (U219c, without_dsh_store_root_row); the earlier lever
        runs from its own tree (earlier_lever)."""
        for head in DSH_EARLIER_HEADS:
            old_seat = self.earlier_lever(head)
            rendered = {}
            for label, seat in (("earlier head", old_seat), ("this head", test_hcom_seat.SEAT)):
                procs = self.held_launch("--", "--version", seat=seat)
                (name,) = self.slots()[0]
                settings = Path(self.seats, ".sandbox", name, "srt-settings.json").read_bytes()
                if label == "this head":
                    settings = self.without_dsh_store_root_row(self.without_credential_rows(settings))
                rendered[label] = self.without_launch_name(settings, name)
                ((status, out, err),) = self.release(procs)
                self.assertEqual((status, out), (0, "0.2.1-rc.5\n"), f"{label} {head[:8]}: {err}")
            with self.subTest(head=head[:8]):
                self.assertEqual(rendered["earlier head"], rendered["this head"])
                self.assertIn(b'"allowLocalBinding":false', rendered["this head"])

    def test_the_dsh_and_router_rows_deny_the_store_root_for_write_and_the_launch_makes_it(self):
        """U219c (verdict U219-985b7c04 P1 `:1981` and P2 `:1815`): the dsh and router rows carry the program store's
        root `<physical HOME>/.local/state/regime-store/<slug>` in `denyWrite` (the shape U353d gave the credential
        root: the held physical path, tagged, right before the credential root's row), in no grant list and in no
        `denyRead` row (the rows read nothing of it today and gain no read grant, U219c FORBIDDEN); a launch of either
        row that finds the root absent makes both components 0700 directories of this user before its settings file
        is written, since srt 0.0.81's Linux backend binds a deny only for a path that exists."""
        root = Path(self.store_root())
        cred = f"{self.dsh_home}/router-credentials"
        self.assertFalse(root.parent.exists(), "absent before the first launch")
        for role in ("dsh", "router"):
            with self.subTest(role=role):
                procs = self.held_launch("--", "--version", role=role)
                (name,) = self.slots()[0]
                fs = self.settings_of(name)["filesystem"]
                ((status, out, err),) = self.release(procs)
                self.assertEqual((status, out), (0, "0.2.1-rc.5\n"), err)
                self.assertEqual((fs["denyWrite"].count(str(root)), fs["denyRead"].count(str(root))), (1, 0), fs)
                self.assertEqual(
                    fs["denyWrite"].index(str(root)) + 1, fs["denyWrite"].index(cred), "before the credential row"
                )
                for key in ("allowRead", "allowWrite"):
                    self.assertEqual(
                        [row for row in fs[key] if row == str(root) or row.startswith(f"{root}/")], [], key
                    )
                for path in (root.parent, root):
                    self.assertTrue(path.is_dir() and not path.is_symlink(), path)
                    self.assertEqual(
                        (stat.S_IMODE(os.lstat(path).st_mode), os.lstat(path).st_uid), (0o700, os.getuid()), path
                    )
                self.assertEqual(self.slots(), ([], []))

    def test_a_router_state_root_that_is_a_link_or_a_file_refuses_and_a_linked_dsh_home_renders_inside_it(self):
        """U321b (verdict U321-fec87e14 P1 `:1551`, the auditor's `test_state_root_link_escapes_dsh_home`): round 1
        rendered `<DSH_HOME>/router-state` as spelled, so a link there pointing outside DSH_HOME (the auditor's
        `~/.config/autostart`) became allowWrite row 6 and the launch went through. The state root is held before the
        roots are rendered: a link refuses by name, exit 2, in a dry run too, before any tool is resolved, with no
        seats root, no settings file and nothing written at the link's target; a regular file refuses; a DSH_HOME that
        is itself a link resolves first, so the root renders as its physical path inside the physical DSH_HOME, and an
        absent root is made 0700 by the launch."""
        home = self.home.resolve()
        outside = home / ".config/autostart"
        outside.mkdir(parents=True)
        state_root = self.dsh_home / "router-state"
        state_root.symlink_to(outside)
        for args in ([], ["--dry-run"]):
            with self.subTest(case="a link outside DSH_HOME", args=args):
                run = self.seat(
                    "router", "--seats-root", self.seats, "--home", str(self.dsh_home), *args, "--", "--version"
                )
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertIn(
                    f"the router role's state root {state_root} is a symbolic link; it must be a real directory inside"
                    " DSH_HOME, or absent",
                    run.stderr,
                )
        self.assertTrue(state_root.is_symlink(), "the launch neither removed nor replaced the link")
        self.assertEqual(sorted(outside.iterdir()), [], "nothing was written at the link's target")
        state_root.unlink()
        state_root.write_text("not a directory\n")
        with self.subTest(case="a regular file"):
            run = self.seat("router", "--seats-root", self.seats, "--home", str(self.dsh_home), "--", "--version")
            self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
            self.assertIn(f"the router role's state root {state_root} exists and is not a directory", run.stderr)
        self.assertFalse(Path(self.seats).exists(), "no seats root, so no settings file")
        self.assertEqual((self.calls_of("srt"), self.dsh_calls()), ([], []))
        state_root.unlink()
        linked_home = Path(self.temp.name).resolve() / "linked-home"
        linked_home.symlink_to(self.dsh_home)
        with self.subTest(case="an absent state root, then a linked DSH_HOME"):
            procs = self.held_launch("--", "--version", role="router")
            (name,) = self.slots()[0]
            settings = self.settings_of(name)
            ((status, out, err),) = self.release(procs)
            self.assertEqual((status, out), (0, "0.2.1-rc.5\n"), err)
            self.assertEqual(settings["filesystem"]["allowWrite"][6], str(state_root))
            self.assertTrue(state_root.is_dir() and not state_root.is_symlink())
            self.assertEqual(stat.S_IMODE(state_root.stat().st_mode), 0o700, "an absent state root is made 0700")
            shutil.rmtree(state_root)
            procs = self.held_launch("--", "--version", role="router", home=linked_home)
            (name,) = self.slots()[0]
            settings = self.settings_of(name)
            ((status, out, err),) = self.release(procs)
            self.assertEqual((status, out), (0, "0.2.1-rc.5\n"), err)
            self.assertEqual(settings["filesystem"]["allowWrite"][3], str(self.dsh_home), "DSH_HOME renders physical")
            self.assertEqual(
                settings["filesystem"]["allowWrite"][6], str(state_root), "the state root renders physical, inside it"
            )
            self.assertNotIn(str(linked_home), json.dumps(settings))
            self.assertTrue(state_root.is_dir() and not state_root.is_symlink())
            self.assertEqual(stat.S_IMODE(state_root.stat().st_mode), 0o700)
            self.assertEqual(self.dsh_calls()[-1]["env"]["DSH_HOME"], str(self.dsh_home))
        self.assertEqual(self.slots(), ([], []))

    def test_the_passthrough_cannot_reselect_the_router_profile(self):
        """U321b (verdict U321-fec87e14 P1 `:316`, the auditor's `test_forwarded_profile_selectors_are_not_refused`): the
        fixed `--profile router` was placed before the verbatim dsh arguments and nothing held those, so `-- --profile
        thak` reached dsh as `--profile router --profile thak` and the restriction rested on dsh's option precedence.
        Each selector form among the verbatim arguments (`--profile <name>`, `--profile=<name>`, `-p <name>`,
        `-p<name>`) refuses by name, exit 2, in a dry run too, before any tool is resolved or anything is made; a
        passthrough without a selector keeps round 1's launch line, `--profile router` once and first; the dsh row,
        whose profile is not fixed, forwards a selector as before."""
        message = "the router role runs the DSH profile 'router' alone; the dsh argument {!r} selects a profile and is refused"
        for selector in (["--profile", "thak"], ["--profile=thak"], ["-p", "thak"], ["-pthak"]):
            for args in ([], ["--dry-run"], ["--profile", "router"]):
                with self.subTest(selector=selector, args=args):
                    run = self.seat("router", "--seats-root", self.seats, "--home", str(self.dsh_home), *args,
                                    "--", "--version", *selector)  # fmt: skip
                    self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                    self.assertIn(message.format(selector[0]), run.stderr)
        self.assertFalse(Path(self.seats).exists())
        self.assertEqual((self.calls_of("srt"), self.dsh_calls()), ([], []))
        run = self.seat("router", "--seats-root", self.seats, "--home", str(self.dsh_home), "--dry-run",
                        "--", "--version", "--flag", "-x", "value")  # fmt: skip
        self.assertEqual(run.returncode, 0, run.stderr)
        line = shlex.split(run.stdout)
        self.assertRegex(line[7], rf"^{re.escape(self.seats)}/\.sandbox/router-\d{{8}}-\d{{6}}-\d+/bin/dsh$")
        self.assertEqual(line[8:], ["--profile", "router", "--version", "--flag", "-x", "value"])
        self.assertEqual(line.count("--profile"), 1)
        run = self.launch("--", "--profile", "thak", "--version")
        self.assertEqual((run.returncode, run.stdout), (0, "0.2.1-rc.5\n"), run.stderr)
        (dsh,) = self.dsh_calls()
        self.assertEqual(dsh["argv"], ["--profile", "thak", "--version"], "the dsh row fixes no profile")
        self.assertEqual(self.slots(), ([], []))

    def debug_trap_hook(self, name, handler):
        """A BASH_ENV file installing `handler` (bash lines defining `u321c_hook`, called with the command bash is about
        to run) as the lever's DEBUG trap: top-level commands of hcom-seat alone (no `set -T`, so no function or
        subshell inherits it), the form of the round-2 auditor's race probe (verdict U321b-7dfaa839 P1 `:1567`).
        Returns the environment overrides: the hook, and `U321C_TRACE`, the file the handler records itself in."""
        hook = Path(self.temp.name) / f"{name}-hook.bash"
        trace = Path(self.temp.name) / f"{name}-trace"
        trace.write_text("")
        hook.write_text(f"{handler}\ntrap 'u321c_hook \"${{BASH_COMMAND}}\"' DEBUG\n")
        return {"BASH_ENV": str(hook), "U321C_TRACE": str(trace)}, trace

    def test_a_state_root_swapped_between_the_hold_and_the_render_grants_the_held_directory_alone(self):
        """U321c (verdict U321b-7dfaa839 P1 `:1567`, the auditor's DEBUG-trap race; the mechanism-change row of
        2026-11-07T02:25:00Z, form remove): round 2 held `<DSH_HOME>/router-state` physical and then `seat_write_roots`
        resolved it a second time, so a swap of the directory for a link to `~/.config/autostart` between the two
        reads, restored before the final check, rendered the outside path as allowWrite row 6 and the launch went
        through. Now the hold resolves the path once and the render prints the held value: the same swap, made by a
        DEBUG trap before the render and undone before the next command, changes nothing in the settings. Row 6 is the
        held physical directory, the outside path appears nowhere, and the launch goes through on the restored
        directory."""
        home = self.home.resolve()
        outside = home / ".config/autostart"
        outside.mkdir(parents=True)
        state_root = self.dsh_home / "router-state"
        state_root.mkdir(0o700)
        overrides, trace = self.debug_trap_hook(
            "race",
            textwrap.dedent(
                """\
                u321c_phase=0
                u321c_hook() {
                    case ${u321c_phase}:$1 in
                    0:seat_roots_out=*)
                        /bin/rmdir "${U321C_ROOT}" && /bin/ln -s "${U321C_OUTSIDE}" "${U321C_ROOT}" || exit 97
                        u321c_phase=1
                        builtin printf 'swapped before: %s\\n' "$1" >> "${U321C_TRACE}"
                        ;;
                    1:*)
                        /bin/rm "${U321C_ROOT}" && /bin/mkdir -m 700 "${U321C_ROOT}" || exit 98
                        u321c_phase=2
                        builtin printf 'restored before: %s\\n' "$1" >> "${U321C_TRACE}"
                        ;;
                    esac
                }
                """
            ),
        )
        overrides.update(U321C_ROOT=str(state_root), U321C_OUTSIDE=str(outside))
        procs = self.held_launch("--", "--version", role="router", **overrides)
        (name,) = self.slots()[0]
        settings = self.settings_of(name)
        ((status, out, err),) = self.release(procs)
        self.assertEqual((status, out), (0, "0.2.1-rc.5\n"), err)
        recorded = trace.read_text().splitlines()
        self.assertEqual(len(recorded), 2, recorded)
        self.assertRegex(
            recorded[0], r"^swapped before: seat_roots_out=\$\(seat_write_roots ", "the swap preceded the render"
        )
        self.assertTrue(recorded[1].startswith("restored before: "), recorded)
        self.assertEqual(settings["filesystem"]["allowWrite"][6], str(state_root), "row 6 is the held physical path")
        self.assertEqual(
            settings["filesystem"]["allowWrite"][3:7],
            [str(self.dsh_home), str(home / ".omp/profiles/dsh"), str(home / ".omp/run"), str(state_root)],
        )
        self.assertNotIn(str(outside), json.dumps(settings), "nothing outside DSH_HOME reaches the settings")
        for root in settings["filesystem"]["allowWrite"]:
            self.assertFalse(root.startswith(f"{home}/.config"), root)
        self.assertEqual(sorted(outside.iterdir()), [], "nothing was written at the link's target")
        self.assertTrue(state_root.is_dir() and not state_root.is_symlink())
        self.assertEqual(self.dsh_calls()[-1]["argv"], ["--profile", "router", "--version"])
        self.assertEqual(self.slots(), ([], []))

    def test_a_held_state_root_removed_before_the_sandbox_write_refuses_by_name_and_writes_no_settings(self):
        """U321c: the held value names a directory that existed when it was held; nothing in the launch resolves the
        path again, and the sandbox write derives nothing from it. A held directory removed after the hold (a DEBUG
        trap before `seat_sandbox_write`) refuses, exit 2, naming the state root; no settings file is written, so no
        grant of any kind reaches srt, and dsh does not start. The lever does not make the directory again (the
        7dfaa839 write made it anew and launched)."""
        state_root = self.dsh_home / "router-state"
        state_root.mkdir(0o700)
        overrides, trace = self.debug_trap_hook(
            "removal",
            textwrap.dedent(
                """\
                u321c_hook() {
                    case $1 in
                    seat_sandbox_write)
                        /bin/rmdir "${U321C_ROOT}" || exit 97
                        builtin printf 'removed before: %s\\n' "$1" >> "${U321C_TRACE}"
                        ;;
                    esac
                }
                """
            ),
        )
        run = self.seat(
            "router", "--seats-root", self.seats, "--home", str(self.dsh_home), "--", "--version",
            U321C_ROOT=str(state_root), **overrides,
        )  # fmt: skip
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertIn(f"the router role's state root {state_root} is not a real directory of this user", run.stderr)
        self.assertEqual(
            trace.read_text(), "removed before: seat_sandbox_write\n", "the trap removed the held directory"
        )
        self.assertFalse(state_root.exists() or state_root.is_symlink(), "the launch made no second directory")
        self.assertEqual(list(Path(self.seats).rglob("srt-settings.json")) if Path(self.seats).exists() else [], [])
        self.assertEqual(self.slots(), ([], []))
        self.assertEqual(self.dsh_calls(), [])

    def test_an_invalid_state_root_in_a_dry_run_makes_no_tool_directory_no_link_and_runs_no_host_git(self):
        """U321c (verdict U321b-7dfaa839 P3 `README.md:145`): round 2's hold ran after the private tool directory and
        the host git reads, so an invalid-state-root dry run made eight tool links and ran git three times before
        refusing. The hold is now one of the pre-launch checks: a link outside DSH_HOME or a regular file at
        `router-state` refuses, exit 2, with the private tool directory absent (so no link under it), zero host git
        calls (a logging git first on PATH), no seats root, no srt or dsh call. The contrast: a dry run with a valid
        absent state root goes through to the host git reads and (U321d) makes nothing, not the state root either."""
        home = self.home.resolve()
        outside = home / ".config/autostart"
        outside.mkdir(parents=True)
        state_root = self.dsh_home / "router-state"
        log = Path(self.temp.name) / "git-calls"
        wrapper = Path(self.temp.name) / "logging-git"
        wrapper.mkdir()
        real_git = shutil.which("git", path=SYSTEM_PATH)
        (wrapper / "git").write_text(f'#!/bin/sh\nprintf "%s\\n" "$*" >> "{log}"\nexec "{real_git}" "$@"\n')
        (wrapper / "git").chmod(0o755)
        path = f"{wrapper}:{self.env['PATH']}"
        cases = (
            ("a link outside DSH_HOME", lambda: state_root.symlink_to(outside),
             f"the router role's state root {state_root} is a symbolic link; it must be a real directory inside DSH_HOME, or absent"),
            ("a regular file", lambda: state_root.write_text("not a directory\n"),
             f"the router role's state root {state_root} exists and is not a directory"),
        )  # fmt: skip
        for label, plant, message in cases:
            plant()
            with self.subTest(case=label):
                run = self.seat("router", "--seats-root", self.seats, "--home", str(self.dsh_home), "--dry-run",
                                "--", "--version", PATH=path)  # fmt: skip
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertIn(message, run.stderr)
                self.assertFalse(self.tools.exists(), "the private tool directory is not made, so no link under it")
                self.assertFalse(log.exists(), "no host git call")
            state_root.unlink()
        self.assertEqual(sorted(outside.iterdir()), [], "nothing was written at the link's target")
        self.assertFalse(Path(self.seats).exists(), "no seats root")
        self.assertEqual((self.calls_of("srt"), self.dsh_calls()), ([], []))
        run = self.seat("router", "--seats-root", self.seats, "--home", str(self.dsh_home), "--dry-run",
                        "--", "--version", PATH=path)  # fmt: skip
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertFalse(state_root.exists() or state_root.is_symlink(), "a dry run makes no state root (U321d)")
        self.assertFalse(Path(self.seats).exists(), "the dry run still makes no seats root and no slot")
        self.assertTrue(log.exists(), "the valid dry run goes on to the host git reads through the logging git")

    def test_a_dsh_home_link_retargeted_between_the_hold_and_the_render_grants_the_held_home_alone(self):
        """U321d (verdict U321c-b80a4794 P1 `:630`, the auditor's parent-alias race; class containment-boundary, the
        first strike after the mechanism-change row of 2026-11-07T02:25:00Z, form remove): round 3 held
        `<DSH_HOME>/router-state` once but resolved DSH_HOME on its own at the hold, again at the render and again at
        the deny row, so a DSH_HOME link retargeted to `~/.config/autostart` during the hold and restored before the
        render launched with allowWrite row 3 at the real home and row 6 at `~/.config/autostart/router-state`. Now
        the home is resolved exactly once (`dsh_home_hold`) and every later use reads that variable: the same
        retarget, made by a DEBUG trap before `state_root_hold` and undone before the render, changes nothing. Rows 3
        to 6 name the held physical home, the outside path appears nowhere, nothing is written under it, the state
        root is made inside the held home, and dsh runs under `DSH_HOME=<held home>`."""
        home = self.home.resolve()
        outside = home / ".config/autostart"
        outside.mkdir(parents=True)
        linked_home = Path(self.temp.name).resolve() / "linked-home"
        linked_home.symlink_to(self.dsh_home)
        state_root = self.dsh_home / "router-state"
        overrides, trace = self.debug_trap_hook(
            "parent-alias",
            textwrap.dedent(
                """\
                u321d_phase=0
                u321c_hook() {
                    case ${u321d_phase}:$1 in
                    0:state_root_hold)
                        /bin/rm "${U321D_LINK}" && /bin/ln -s "${U321D_OUTSIDE}" "${U321D_LINK}" || exit 97
                        u321d_phase=1
                        builtin printf 'retargeted before: %s\\n' "$1" >> "${U321C_TRACE}"
                        ;;
                    1:seat_roots_out=*)
                        /bin/rm "${U321D_LINK}" && /bin/ln -s "${U321D_HOME}" "${U321D_LINK}" || exit 98
                        u321d_phase=2
                        builtin printf 'restored before: %s\\n' "$1" >> "${U321C_TRACE}"
                        ;;
                    esac
                }
                """
            ),
        )
        overrides.update(U321D_LINK=str(linked_home), U321D_OUTSIDE=str(outside), U321D_HOME=str(self.dsh_home))
        procs = self.held_launch("--", "--version", role="router", home=linked_home, **overrides)
        (name,) = self.slots()[0]
        settings = self.settings_of(name)
        ((status, out, err),) = self.release(procs)
        self.assertEqual((status, out), (0, "0.2.1-rc.5\n"), err)
        recorded = trace.read_text().splitlines()
        self.assertEqual(len(recorded), 2, recorded)
        self.assertEqual(recorded[0], "retargeted before: state_root_hold", "the retarget preceded the state root hold")
        self.assertRegex(
            recorded[1], r"^restored before: seat_roots_out=\$\(seat_write_roots ", "undone before the render"
        )
        self.assertEqual(
            settings["filesystem"]["allowWrite"][3:7],
            [str(self.dsh_home), str(home / ".omp/profiles/dsh"), str(home / ".omp/run"), str(state_root)],
            "rows 3 to 6 name the held physical home",
        )
        self.assertEqual(settings["filesystem"]["allowRead"][3], str(self.dsh_home))
        self.assertNotIn(str(outside), json.dumps(settings), "nothing outside the held home reaches the settings")
        self.assertNotIn(str(linked_home), json.dumps(settings), "the spelled link appears nowhere")
        for root in settings["filesystem"]["allowWrite"]:
            self.assertFalse(root.startswith(f"{home}/.config"), root)
        self.assertEqual(sorted(outside.iterdir()), [], "nothing was written at the retargeted link's target")
        self.assertTrue(
            state_root.is_dir() and not state_root.is_symlink(), "the state root is made inside the held home"
        )
        self.assertEqual(stat.S_IMODE(state_root.stat().st_mode), 0o700)
        self.assertEqual(self.dsh_calls()[-1]["env"]["DSH_HOME"], str(self.dsh_home))
        self.assertEqual(self.dsh_calls()[-1]["argv"], ["--profile", "router", "--version"])
        self.assertEqual(self.slots(), ([], []))

    def test_a_denied_dsh_home_in_a_router_dry_run_refuses_with_no_directory_made_under_it(self):
        """U321d (verdict U321c-b80a4794 P2 `:635`, the auditor's denied-home probe): round 3's hold made `router-state`
        before DSH_HOME's deny judgement, so `router --home ~/.ssh --dry-run` created `~/.ssh/router-state` and then
        refused the denied home, where the dsh role refused without a write. Now the hold writes nothing and the make
        runs after the judgement, in a real launch alone: the router role refuses `~/.ssh` by the judge's name, exit 2,
        in a dry run and in a launch, as the dsh role does, nothing appears under `~/.ssh`, no seats root exists, and
        the DEBUG-trap recorder shows the private tool directory's mkdir alone."""
        home = self.home.resolve()
        ssh = home / ".ssh"
        ssh.mkdir()
        hook = Path(self.temp.name) / "trace-hook.bash"
        hook.write_text('set -T\ntrap \'builtin printf "%s\\0" "$BASH_COMMAND" >> "$U272_TRACE"\' DEBUG\n')
        trace = Path(self.temp.name) / "trace"
        for role, args in (("router", ["--dry-run"]), ("router", []), ("dsh", ["--dry-run"])):
            with self.subTest(role=role, args=args):
                trace.write_text("")
                run = self.seat(role, "--seats-root", self.seats, "--home", str(ssh), *args, "--", "--version",
                                BASH_ENV=str(hook), U272_TRACE=str(trace))  # fmt: skip
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertIn(
                    f"allowRead row {ssh} is, contains or lies inside {ssh}, a row of its denyRead list", run.stderr
                )
                commands = trace.read_text().split("\0")[:-1]
                self.assertIn("settings_judge", " ".join(commands), "the refusal is the judge's")
                mkdirs = [c for c in commands if re.match(r"(/bin/)?mkdir\b", c)]
                self.assertTrue(mkdirs and all("tools_dir" in c for c in mkdirs), mkdirs)
                self.assertEqual(sorted(ssh.iterdir()), [], "nothing is made under the denied home")
        self.assertFalse(Path(self.seats).exists())
        self.assertEqual((self.calls_of("srt"), self.dsh_calls()), ([], []))

    def test_a_router_dry_run_with_an_absent_state_root_makes_nothing_and_prints_the_would_make_line(self):
        """U321d: a dry run of the router role with a valid, absent state root makes nothing (no `router-state`, no
        seats root, no slot; DSH_HOME keeps its one entry), prints the launch line, exit 0, and says on stderr what a
        launch would make: the state root, 0700, and (U343i) the broker directory `<state slot>/broker`, 0700. A
        launch then makes exactly those directories, 0700, the state root inside the held home after the judgement
        and the broker directory inside the per-launch state slot before the settings are written (so it stands,
        empty, while dsh runs and goes with the slot), and says nothing of the kind."""
        state_root = self.dsh_home / "router-state"
        seats = Path(self.seats).resolve()
        run = self.seat(
            "router", "--seats-root", self.seats, "--home", str(self.dsh_home), "--dry-run", "--", "--version"
        )
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertIn(
            f"hcom-seat: the router role's state root {state_root} does not exist; a launch creates it (0700)",
            run.stderr,
        )
        self.assertRegex(
            run.stderr,
            rf"hcom-seat: the router role's broker directory {re.escape(str(seats))}/\.state/router-\d{{8}}-\d{{6}}-\d+/broker"
            r" does not exist; a launch creates it \(0700\)",
        )
        self.assertRegex(
            run.stdout, rf" {re.escape(self.seats)}/\.sandbox/router-\d{{8}}-\d{{6}}-\d+/bin/dsh --profile router "
        )
        self.assertFalse(state_root.exists() or state_root.is_symlink(), "the dry run makes no state root")
        self.assertEqual(sorted(self.dsh_home.iterdir()), [self.dsh_home / "bin"], "DSH_HOME keeps its one entry")
        self.assertFalse(Path(self.seats).exists(), "no seats root and no slot")
        self.assertEqual(self.dsh_calls(), [])
        procs = self.held_launch("--", "--version", role="router")
        (name,) = self.slots()[0]
        settings = self.settings_of(name)
        broker_dir = seats / ".state" / name / "broker"
        self.assertTrue(broker_dir.is_dir() and not broker_dir.is_symlink(), "a launch makes the broker directory")
        self.assertEqual(stat.S_IMODE(broker_dir.stat().st_mode), 0o700)
        self.assertEqual(sorted(broker_dir.iterdir()), [], "empty: hcom-seat makes it and puts nothing in it")
        ((status, out, err),) = self.release(procs)
        self.assertEqual((status, out), (0, "0.2.1-rc.5\n"), err)
        self.assertNotIn("does not exist; a launch creates it", err)
        self.assertEqual(settings["filesystem"]["allowWrite"][6], str(state_root))
        self.assertIn(str(broker_dir), settings["filesystem"]["denyWrite"])
        self.assertTrue(state_root.is_dir() and not state_root.is_symlink(), "a launch makes the held state root")
        self.assertEqual(stat.S_IMODE(state_root.stat().st_mode), 0o700)
        self.assertEqual(self.slots(), ([], []), "the broker directory went with the state slot")

    def test_the_router_row_denies_its_broker_directory_for_write_as_a_tagged_row_and_the_judge_passes(self):
        """U343i (verdicts U343g-8a049561 P1 `acp-broker:1262` and U343h-eb648bcd P1 `acp-relay.py:284`, `acp-broker:963`;
        the mechanism-change row of 2026-11-10T06:20:28Z, form remove): the Router's write grant on the broker
        directory ceases to exist. The router row renders `<state slot>/broker` as one `denyWrite` row, after the
        project-file denies of its own directory and in no grant list, tagged `slot` like those denies (it lies inside
        allowWrite row 1 and allowRead row 1, the state slot, as the project-file denies lie inside row 0), so the
        lever's own judge passes the rendered tables with the tag (the dsh role's structural-tag count, 31 with U353,
        grows by one for the router role) and hits with the tag absent, naming the state-slot grant and the broker
        deny; the dsh row renders no such row."""
        rendered = {}
        for role in ("dsh", "router"):
            procs = self.held_launch("--", "--version", role=role)
            (name,) = self.slots()[0]
            rendered[role] = (name, self.settings_of(name)["filesystem"])
            ((status, out, err),) = self.release(procs)
            self.assertEqual((status, out), (0, "0.2.1-rc.5\n"), err)
        name, router = rendered["router"]
        home = self.home.resolve()
        seats = Path(self.seats).resolve()
        cwd, slot = str(seats / ".state" / name / "cwd"), str(seats / ".state" / name)
        broker = f"{slot}/broker"
        profile, profiles = str(home / ".omp/profiles/dsh"), str(home / ".omp/profiles")
        shared = str(seats / ".state/claude")
        dsh_home, cred = str(self.dsh_home), f"{self.dsh_home}/router-credentials"
        deny_read = router["denyRead"]
        deny_write = [row for row in router["denyWrite"] if "*" not in row]
        self.assertEqual(deny_write.count(broker), 1, deny_write)
        for kind in ("allowRead", "allowWrite", "denyRead"):
            self.assertNotIn(broker, router[kind], kind)
        project_rows = [ix for ix, row in enumerate(deny_write) if row.startswith(cwd + "/")]
        self.assertEqual(len(project_rows), 8)
        self.assertGreater(deny_write.index(broker), max(project_rows), "after the project-file denies")
        self.assertEqual([row for row in rendered["dsh"][1]["denyWrite"] if row.endswith("/broker")], [])
        tags = [(tag, kind, ix, path) for kind in ("allowRead", "allowWrite")
                for tag, ix, path in (("slot", 0, cwd), ("slot", 1, slot), ("slot", 2, shared), ("credential", 3, dsh_home), ("profile", 4, profile))]  # fmt: skip
        tags += [("slot", "denyWrite", ix, row) for ix, row in enumerate(deny_write) if row.startswith(cwd + "/")]
        tags += [("slot", "denyWrite", ix, row) for ix, row in enumerate(deny_write) if row.startswith(shared + "/")]
        tags += [
            ("slot", "denyRead", deny_read.index(row), row)
            for row in (str(home / ".local/state/omp-seats"), str(seats))
        ]
        tags += [("profile", "denyRead", deny_read.index(profiles), profiles)]
        # The credential root's rows (U353): the router row reads it, allowRead row 7, and denies writing it.
        tags += [
            ("credential", "allowRead", 7, cred),
            ("credential", "denyWrite", deny_write.index(cred), cred),
        ]
        self.assertEqual(len(tags), 31, "the dsh role's structural-tag count, the credential root's read for its deny")
        without = list(tags)
        tags.append(("slot", "denyWrite", deny_write.index(broker), broker))
        self.assertEqual(len(tags), 31 + 1, "the router role's one more tag, the broker deny")
        clear = self.judge_run(tags, router["allowRead"], router["allowWrite"], deny_read, deny_write)
        self.assertEqual((clear.returncode, clear.stdout), (0, ""), clear.stderr)
        hit = self.judge_run(without, router["allowRead"], router["allowWrite"], deny_read, deny_write)
        self.assertEqual(hit.returncode, 3, hit.stdout + hit.stderr)
        self.assertEqual(
            hit.stdout.splitlines(),
            [f"grant=allowRead row {slot}", f"deny={broker}, a row of its denyWrite list"],
            "without the tag the state slot's grant contains the broker deny",
        )
        self.assertEqual(self.slots(), ([], []))

    def judge_run(self, tags, allow_read, write, deny_read, deny_write):
        """Run the lever's own `settings_judge` (its text and the functions it reads) over the four lists with `tags`
        as the structural tags, each `(tag, kind, ix, path)` in the form `tag_row` takes: exit 0 and no output when
        every grant keeps clear of every deny it is not paired with; exit 3 with `grant=` and `deny=` lines on a hit."""
        text = test_hcom_seat.SEAT.read_text()
        names = ("refuse", "clean_path", "require_clean_path", "physical_path", "physical_each", "ancestors_of")
        names += (
            "identity_table",
            "ascii_lower",
            "within_ix",
            "tag_row",
            "row_tag",
            "store_root_judge",
            "settings_judge",
        )
        functions = "\n".join(
            text[text.index(f"\n{fn}() {{") : text.index("\n}\n", text.index(f"\n{fn}() {{")) + 3] for fn in names
        )
        stat_args = "stat_args=(-L -f '%d:%i')" if sys.platform == "darwin" else "stat_args=(-L -c '%d:%i')"
        lists = "\n".join(
            f"{var}=({' '.join(shlex.quote(row) for row in rows)})"
            for var, rows in (("allow_read", allow_read), ("write", write), ("deny_read", deny_read), ("deny_write", deny_write))
        )  # fmt: skip
        tagged = "\n".join(f"tag_row {tag} {kind} {ix} {shlex.quote(path)}" for tag, kind, ix, path in tags)
        # The store-root rule (U219c) is a launch's: with no root held, settings_judge's first step is inert here.
        script = f"set -euo pipefail\n{stat_args}\nstore_root_phys=''\n{functions}\n{lists}\n"
        script += f"row_tags=() row_tag_kinds=() row_tag_ixs=() row_tag_paths=()\n{tagged}\n"
        script += 'settings_judge || { printf "grant=%s\\ndeny=%s\\n" "${judge_grant}" "${judge_deny}"; exit 3; }\n'
        return subprocess.run(["/bin/bash", "-c", script], capture_output=True, text=True, check=False, timeout=60)

    def test_the_router_settings_carry_the_credential_root_as_a_read_grant_and_the_dsh_row_denies_it(self):
        """U353 (M-26 stage B): the Router's credential root `<DSH_HOME>/router-credentials`, where the operator places
        the agent account's gh login (`router-gh` sets `GH_CONFIG_DIR` under it), is one more cell of the router row,
        held like the state root (cred_root_hold). The router settings carry it as allowRead row 7, after the tool
        directory, and as a denyWrite row (no role writes it); the dsh settings deny it for read and for write and
        grant nothing at or under it; neither role grants a write there, and the omp roles deny the kit's root under
        `~/.dsh` for read and for write (U353b, U353d) and name it nowhere else. A launch of either foreground role
        makes the absent root 0700 after the judgement (U353d: the dsh row too, so the directory its deny names exists
        when srt reads the settings), and the fake dsh of each sees it in place."""
        cred = self.dsh_home / "router-credentials"
        rendered = {}
        for role in ("dsh", "router"):
            procs = self.held_launch("--", "--version", role=role)
            (name,) = self.slots()[0]
            rendered[role] = self.without_launch_name(self.settings_of(name), name)["filesystem"]
            self.assertTrue(
                cred.is_dir() and not cred.is_symlink(), f"the {role} launch makes the held credential root"
            )
            self.assertEqual(stat.S_IMODE(cred.stat().st_mode), 0o700)
            self.assertEqual(cred.stat().st_uid, os.geteuid())
            ((status, out, err),) = self.release(procs)
            self.assertEqual((status, out), (0, "0.2.1-rc.5\n"), err)
            self.assertNotIn("does not exist; a launch creates it", err)
            self.assertTrue(
                self.dsh_calls()[-1]["cred_root_dir"], f"dsh of the {role} role runs with the root in place"
            )
            if role == "dsh":
                self.assertEqual(
                    list(cred.iterdir()), [], "the dsh launch makes the root empty and places nothing in it"
                )
        dsh, router = rendered["dsh"], rendered["router"]
        self.assertEqual(router["allowRead"][7], str(cred))
        self.assertEqual(router["allowRead"][:7], dsh["allowRead"], "the dsh row's seven read grants come first")
        self.assertEqual(len(dsh["allowRead"]), 7)
        self.assertNotIn(str(cred), dsh["allowRead"])
        self.assertIn(str(cred), dsh["denyRead"])
        self.assertNotIn(str(cred), router["denyRead"])
        for role, lists in (("dsh", dsh), ("router", router)):
            with self.subTest(role=role):
                self.assertIn(str(cred), lists["denyWrite"], "no role writes the credential root")
                self.assertNotIn(str(cred), lists["allowWrite"])
                under = [row for row in lists["allowRead"] + lists["allowWrite"] if row.startswith(f"{cred}/")]
                self.assertEqual(under, [], "no grant lies under the credential root")
                self.assertEqual(lists["denyRead"].count(str(cred)) + lists["denyWrite"].count(str(cred)),
                                 2 if role == "dsh" else 1)  # fmt: skip
        self.assertEqual(self.slots(), ([], []))
        for role in ("worker", "orchestrator"):
            run = self.seat(role, "--seats-root", self.seats)
            self.assertEqual(run.returncode, 0, run.stderr)
            omp = self.settings_of(role)["filesystem"]
            self.assertEqual(omp["denyRead"].count(self.omp_credential_root()), 1, role)
            self.assertEqual(omp["denyWrite"].count(self.omp_credential_root()), 1, role)
            self.assertEqual(json.dumps(omp).count("router-credentials"), 2, role)

    def test_the_dsh_launch_makes_the_credential_root_before_dsh_runs_and_both_rows_hold_their_grants(self):
        """U353d (verdict U353-318f268d P1 `:2383`, the dsh row's half: `cred_root_phys` was resolved through the nearest
        existing ancestor and the dsh row denied a path that need not exist, which srt 0.0.81's Linux backend mounts
        nothing for; P2 `:2393`, the write side). Under a linked DSH_HOME the dsh launch makes `<DSH_HOME>/router-credentials`
        at its physical path, 0700, this user's, before dsh runs (the fake dsh sees the directory), and the rendered
        denyRead and denyWrite rows name that physical path once each; the router row keeps the read grant and the
        write deny of the same path. A dsh dry run with the root absent makes nothing and says what a launch would
        make, as the router row's does."""
        real_home = Path(self.temp.name).resolve() / "real-dsh-home"
        shutil.copytree(self.dsh_home, real_home)
        linked_home = Path(self.temp.name).resolve() / "linked-dsh-home"
        linked_home.symlink_to(real_home)
        cred = real_home / "router-credentials"
        run = self.seat("dsh", "--seats-root", self.seats, "--home", str(linked_home), "--dry-run", "--", "--version")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertIn(
            f"hcom-seat: the dsh role's credential root {cred} does not exist; a launch creates it (0700)", run.stderr
        )
        self.assertFalse(cred.exists() or cred.is_symlink(), "the dry run makes no credential root")
        self.assertEqual(sorted(real_home.iterdir()), [real_home / "bin"], "DSH_HOME keeps its one entry")
        self.assertFalse(Path(self.seats).exists())
        rendered = {}
        for role in ("dsh", "router"):
            procs = self.held_launch("--", "--version", role=role, home=linked_home)
            (name,) = self.slots()[0]
            rendered[role] = self.settings_of(name)["filesystem"]
            self.assertTrue(cred.is_dir() and not cred.is_symlink(), f"the {role} launch made the root")
            self.assertEqual(stat.S_IMODE(cred.stat().st_mode), 0o700)
            self.assertEqual(cred.stat().st_uid, os.geteuid())
            ((status, out, err),) = self.release(procs)
            self.assertEqual((status, out), (0, "0.2.1-rc.5\n"), err)
            record = self.dsh_calls()[-1]
            self.assertEqual(record["env"]["DSH_HOME"], str(real_home), "dsh runs under the held physical home")
            self.assertTrue(record["cred_root_dir"], f"dsh of the {role} role runs with the root in place")
        dsh, router = rendered["dsh"], rendered["router"]
        self.assertEqual((dsh["denyRead"].count(str(cred)), dsh["denyWrite"].count(str(cred))), (1, 1))
        self.assertNotIn(str(cred), dsh["allowRead"] + dsh["allowWrite"])
        self.assertEqual((router["allowRead"].count(str(cred)), router["denyWrite"].count(str(cred))), (1, 1))
        self.assertNotIn(str(cred), router["denyRead"] + router["allowWrite"])
        self.assertNotIn(str(linked_home / "router-credentials"), json.dumps(dsh) + json.dumps(router))
        self.assertEqual(self.slots(), ([], []))

    def test_a_credential_root_that_is_a_link_or_a_file_refuses_both_rows_before_anything_is_made(self):
        """U353: the credential root is held like the state root (U321b to U321d): a link at `<DSH_HOME>/router-credentials`
        (here into `~/.config/gh`, the operator's own gh login) refuses the router and the dsh row by name, exit 2, in a
        dry run too, before any tool is resolved, with no seats root, no settings file and nothing written at the
        link's target; a regular file there refuses too; a dry run of either role with the root absent says what a
        launch would make and makes nothing (U353d: the dsh row makes the root too)."""
        home = self.home.resolve()
        outside = home / ".config/gh"
        outside.mkdir(parents=True)
        cred = self.dsh_home / "router-credentials"
        cred.symlink_to(outside)
        for role in ("router", "dsh"):
            for args in ([], ["--dry-run"]):
                with self.subTest(case="a link outside DSH_HOME", role=role, args=args):
                    run = self.seat(
                        role, "--seats-root", self.seats, "--home", str(self.dsh_home), *args, "--", "--version"
                    )
                    self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                    self.assertIn(
                        f"the {role} role's credential root {cred} is a symbolic link; it must be a real directory"
                        " inside DSH_HOME, or absent",
                        run.stderr,
                    )
                    self.assertFalse(Path(self.seats).exists(), "no seats root and no slot")
                    self.assertEqual((self.calls_of("srt"), self.dsh_calls()), ([], []), "no tool was resolved")
                    self.assertEqual(list(outside.iterdir()), [], "nothing written at the link's target")
        cred.unlink()
        cred.write_text("")
        for role in ("router", "dsh"):
            with self.subTest(case="a regular file", role=role):
                run = self.seat(
                    role, "--seats-root", self.seats, "--home", str(self.dsh_home), "--dry-run", "--", "--version"
                )
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertIn(f"the {role} role's credential root {cred} exists and is not a directory", run.stderr)
        cred.unlink()
        run = self.seat(
            "router", "--seats-root", self.seats, "--home", str(self.dsh_home), "--dry-run", "--", "--version"
        )
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertIn(
            f"hcom-seat: the router role's credential root {cred} does not exist; a launch creates it (0700)",
            run.stderr,
        )
        self.assertFalse(cred.exists() or cred.is_symlink(), "the dry run makes no credential root")
        run = self.seat("dsh", "--seats-root", self.seats, "--home", str(self.dsh_home), "--dry-run", "--", "--version")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertIn(
            f"hcom-seat: the dsh role's credential root {cred} does not exist; a launch creates it (0700)", run.stderr
        )
        self.assertFalse(cred.exists() or cred.is_symlink(), "the dsh dry run makes no credential root either")
        self.assertFalse(Path(self.seats).exists())
        self.assertEqual(self.dsh_calls(), [])

    def test_the_dsh_settings_deny_every_git_hcom_and_record_path_for_read_and_write(self):
        """U272c P1 `hcom-seat:1876`: srt reads everything an explicit deny does not name, so removing a grant denied
        nothing. The dsh settings carry a denyRead and a denyWrite row for each path of the role's deny row, by its
        physical path: the checkout's git common directory, the `.git` entry of a linked worktree, the hcom store
        (here outside `~/.local/state/hcom`, as the program's `hcom-regime` is), every `~/.local/state/hcom-*`
        sibling store but the lever's own `hcom-seat` (a file of the name shape is skipped), the records directory and
        another seat's directory. The worker's settings deny none of them: its grants re-open the store and the
        common directory."""
        linked = Path(self.temp.name).resolve() / "linked"
        self.git("worktree", "add", "-q", "--detach", str(linked), "HEAD")
        state = self.home / ".local/state"
        sibling = state / "hcom-regime"
        sibling.mkdir(parents=True)
        (state / "hcom-note").write_text("")
        run = self.seat("worker", "--seats-root", self.seats)
        self.assertEqual(run.returncode, 0, run.stderr)
        worker = self.settings_of("worker")["filesystem"]
        procs = self.held_launch("--", "--version")
        (name,) = [entry for entry in self.slots()[0] if entry != "worker"]
        dsh = self.settings_of(name)["filesystem"]
        ((status, out, err),) = self.release(procs)
        self.assertEqual((status, out), (0, "0.2.1-rc.5\n"), err)
        checkout = self.repo.resolve()
        row = [str(checkout / ".git"), str(linked / ".git"), str(Path(self.seats, "worker/.git")), str(self.store.resolve()),
               str(sibling.resolve()), str(checkout / ".orchestration"), str(Path(self.seats, "worker"))]  # fmt: skip
        for path in row:
            with self.subTest(path=path):
                self.assertIn(path, dsh["denyRead"])
                self.assertIn(path, dsh["denyWrite"])
        self.assertEqual(
            dsh["denyRead"][-len(row) - 1 : -1], row, "the row in the lever's order, after the worker's denies"
        )
        self.assertEqual(
            dsh["denyRead"][-1], f"{self.dsh_home}/router-credentials", "the credential root's row last (U343l)"
        )
        for path in (str(self.tools.parent), str(state / "hcom-note")):
            self.assertNotIn(path, dsh["denyRead"], path)
        self.assertIn(str(self.tools), dsh["allowRead"], "the lever's own state directory is no store")
        for path in (str(checkout / ".git"), str(self.store.resolve())):
            self.assertNotIn(path, worker["denyRead"], "the worker's grants stay")
            self.assertIn(path, worker["allowRead"])
        self.assertEqual(self.slots(), (["worker"], ["worker"]))
        # The program's own spelling, `HCOM_DIR=~/.local/state/hcom-regime` (the verdict's case): the store is denied
        # once, as the store, not again as a sibling.
        procs = self.held_launch("--", "--version", HCOM_DIR=str(sibling))
        (name,) = [entry for entry in self.slots()[0] if entry != "worker"]
        dsh = self.settings_of(name)["filesystem"]
        ((status, out, err),) = self.release(procs)
        self.assertEqual((status, out), (0, "0.2.1-rc.5\n"), err)
        self.assertEqual(dsh["denyRead"].count(str(sibling.resolve())), 1, dsh["denyRead"])
        self.assertEqual(dsh["denyWrite"].count(str(sibling.resolve())), 1, dsh["denyWrite"])
        self.assertNotIn(str(sibling.resolve()), dsh["allowRead"])

    def test_a_dsh_home_that_is_or_holds_a_denied_path_refuses_before_any_mkdir(self):
        """U272c P1 `hcom-seat:1453`: a DSH_HOME whose physical path is, lies inside or contains a path of the deny table
        refuses by name, in a dry run too, before any directory is made: the checkout's `.git` (the overlap check's
        own-`.git` exemption admits it as a write root, so dsh could alter objects and refs; the judge names it by the
        first deny row it lies inside, the checkout), a directory inside it (the overlap invariant's own refusal,
        which runs first) and a directory holding the hcom store. bash's DEBUG trap records every command the launch
        ran; the only mkdir is the private tool directory's."""
        checkout = self.repo.resolve()
        common = checkout / ".git"
        holder = self.store.parent.resolve()
        hook = Path(self.temp.name) / "trace-hook.bash"
        hook.write_text('set -T\ntrap \'builtin printf "%s\\0" "$BASH_COMMAND" >> "$U272_TRACE"\' DEBUG\n')
        trace = Path(self.temp.name) / "trace"
        cases = (
            ("the checkout's .git", common, [],
             f"allowRead row {common} is, contains or lies inside {checkout}, a row of its denyRead list", "settings_judge"),
            ("inside the checkout's .git", common / "objects", [],
             f"write root {common / 'objects'} lies inside the main checkout {checkout}", "seat_overlap_check"),
            ("a directory holding the hcom store", holder, [],
             f"allowRead row {holder} is, contains or lies inside {self.store.resolve()}, a row of its denyRead list",
             "settings_judge"),
            ("the checkout's .git, dry run", common, ["--dry-run"],
             f"is, contains or lies inside {checkout}, a row of its denyRead list", "settings_judge"),
        )  # fmt: skip
        for label, home, args, message, check in cases:
            with self.subTest(case=label):
                trace.write_text("")
                run = self.seat("dsh", "--seats-root", self.seats, "--home", str(home), *args, "--", "--version",
                                BASH_ENV=str(hook), U272_TRACE=str(trace))  # fmt: skip
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertIn(message, run.stderr)
                commands = trace.read_text().split("\0")[:-1]
                self.assertIn(check, " ".join(commands), "the refusal is the named check's, recorded")
                mkdirs = [c for c in commands if re.match(r"(/bin/)?mkdir\b", c)]
                self.assertTrue(mkdirs and all("tools_dir" in c for c in mkdirs), mkdirs)
        self.assertFalse(Path(self.seats).exists())
        self.assertFalse((self.home / ".omp").exists())
        self.assertEqual(self.dsh_calls(), [])

    def test_a_hangup_to_a_held_launch_removes_both_slots(self):
        """U272c P2 `hcom-seat:2123`: a SIGHUP (a terminal hangup) or a SIGTERM to the launch's process group ends dsh,
        the shim and the launcher, whose trap removes both per-launch slots and then ends by the same signal, so the
        exit status names it."""
        for sig in (signal.SIGHUP, signal.SIGTERM):
            with self.subTest(signal=sig.name):
                (proc,) = self.held_launch("--", "--version", new_session=True)
                (name,) = self.slots()[0]
                self.assertEqual(self.slots(), ([name], [name]))
                os.killpg(proc.pid, sig)
                out, err = proc.communicate(timeout=60)
                (self.calls / "hold").unlink()
                self.assertEqual((proc.returncode, out), (-sig, ""), err)
                self.assertEqual(self.slots(), ([], []), err)

    def test_a_failing_or_malformed_date_refuses_the_launch_name(self):
        """U272c P2 `hcom-seat:256`: the clock producer that names the per-launch slot fails closed. A `/bin/date` that
        fails after plausible output, prints nothing, prints another shape, a stamp and more, or a stamp with a
        suffix refuses (exit 2) and names no stamp; the real clock prints the shape. The producer runs from the
        lever's own text with the clock's path replaced, as the identity check's stat is."""
        text = test_hcom_seat.SEAT.read_text()
        functions = "\n".join(
            text[text.index(f"{name}() {{") : text.index("\n}\n", text.index(f"{name}() {{")) + 3]
            for name in ("refuse", "utc_stamp")
        )
        self.assertIn("/bin/date", functions)
        clocks = Path(self.temp.name) / "clocks"
        clocks.mkdir()
        cases = {
            "fails after plausible output": "echo 20261106-120000\nexit 1",
            "prints nothing": "exit 0",
            "another shape": "echo 2026-11-06T12:00:00Z",
            "a stamp and more": "echo 20261106-120000\necho 20261106-120001",
            "a stamp with a suffix": "echo 20261106-120000x",
        }
        for n, (label, body) in enumerate(cases.items()):
            with self.subTest(clock=label):
                clock = clocks / f"date-{n}"
                clock.write_text(f"#!/bin/sh\n{body}\n")
                clock.chmod(0o755)
                script = f"set -euo pipefail\n{functions.replace('/bin/date', str(clock))}\n"
                script += 'stamp=$(utc_stamp) || exit 2\necho "named=${stamp}"\n'
                run = subprocess.run(["/bin/bash", "-c", script], capture_output=True, text=True, check=False)
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stdout + run.stderr)
                self.assertIn("cannot read the time", run.stderr)
        real = subprocess.run(
            ["/bin/bash", "-c", f"set -euo pipefail\n{functions}\nutc_stamp\n"], capture_output=True, text=True, check=False
        )  # fmt: skip
        self.assertEqual(real.returncode, 0, real.stderr)
        self.assertRegex(real.stdout, r"^\d{8}-\d{6}\n$")

    def test_a_dsh_home_under_an_inherited_deny_refuses_from_the_rendered_table_before_any_mkdir(self):
        """U272d P1 `hcom-seat:1660`: the refusal reads the deny table the role will run under (the worker's inherited
        denies among its rows), not the role's own deny row. A DSH_HOME at the scratch HOME's `.aws` or `.omp/agent`,
        inside `.aws`, or at a directory that holds what a linked deny path (`~/.kube -> <elsewhere>/aws`) physically
        names refuses (exit 2) naming the deny path, in a dry run too, before any directory is made (the DEBUG-trap
        recorder shows the tool directory's mkdir alone); each path named is a row of the settings a launch that goes
        through renders. Round 5 (U272f): the judge names the grant as the role's `allowRead` row."""
        home = self.home.resolve()
        for rel in (".aws/deeper", ".omp/agent"):
            (home / rel).mkdir(parents=True)
        elsewhere = Path(self.temp.name).resolve() / "elsewhere"
        (elsewhere / "aws").mkdir(parents=True)
        (home / ".kube").symlink_to(elsewhere / "aws")
        hook = Path(self.temp.name) / "trace-hook.bash"
        hook.write_text('set -T\ntrap \'builtin printf "%s\\0" "$BASH_COMMAND" >> "$U272_TRACE"\' DEBUG\n')
        trace = Path(self.temp.name) / "trace"
        cases = (
            ("~/.aws", home / ".aws", [], f"allowRead row {home / '.aws'} is, contains or lies inside {home / '.aws'},"),
            ("~/.omp/agent", home / ".omp/agent", [],
             f"allowRead row {home / '.omp/agent'} is, contains or lies inside {home / '.omp/agent'},"),
            ("inside ~/.aws", home / ".aws/deeper", [],
             f"allowRead row {home / '.aws/deeper'} is, contains or lies inside {home / '.aws'},"),
            ("holding what a linked deny names", elsewhere, [],
             f"allowRead row {elsewhere} is, contains or lies inside {home / '.kube'} ({elsewhere / 'aws'}),"),
            ("~/.aws, dry run", home / ".aws", ["--dry-run"], f"is, contains or lies inside {home / '.aws'},"),
        )  # fmt: skip
        for label, dsh_home, args, message in cases:
            with self.subTest(case=label):
                trace.write_text("")
                run = self.seat("dsh", "--seats-root", self.seats, "--home", str(dsh_home), *args, "--", "--version",
                                BASH_ENV=str(hook), U272_TRACE=str(trace))  # fmt: skip
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertIn(message, run.stderr)
                self.assertIn("a row of its denyRead list; the launch is refused before anything is made", run.stderr)
                commands = trace.read_text().split("\0")[:-1]
                self.assertIn("settings_judge", " ".join(commands), "the refusal is the judge's")
                mkdirs = [c for c in commands if re.match(r"(/bin/)?mkdir\b", c)]
                self.assertTrue(mkdirs and all("tools_dir" in c for c in mkdirs), mkdirs)
        self.assertFalse(Path(self.seats).exists())
        self.assertFalse((home / ".omp/profiles").exists())
        self.assertEqual(self.dsh_calls(), [])
        # Each path named is a row of the rendered settings of a launch that goes through: the rule's one source.
        procs = self.held_launch("--", "--version")
        (name,) = self.slots()[0]
        rendered = self.settings_of(name)["filesystem"]
        ((status, out, err),) = self.release(procs)
        self.assertEqual((status, out), (0, "0.2.1-rc.5\n"), err)
        for path in (home / ".aws", home / ".omp/agent", home / ".kube"):
            self.assertIn(str(path), rendered["denyRead"])
        self.assertEqual(self.slots(), ([], []))

    def test_records_that_are_a_link_into_dsh_home_refuse_the_home_and_are_denied_by_their_physical_path(self):
        """U272d P2 `hcom-seat:1635`: the records row `<checkout>/.orchestration` enters the deny table in its physical
        form, so a `.orchestration` that is a link into DSH_HOME refuses the DSH_HOME holding it (exit 2, naming the
        records' physical path) before any directory is made, and a `.orchestration` linked elsewhere is denied under
        the path the link names, for read and for write."""
        records = self.dsh_home / "records"
        records.mkdir()
        link = self.repo / ".orchestration"
        link.symlink_to(records)
        run = self.launch("--", "--version")
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertIn(f"allowRead row {self.dsh_home} is, contains or lies inside {records},", run.stderr)
        self.assertFalse(Path(self.seats).exists())
        self.assertEqual(self.dsh_calls(), [])
        link.unlink()
        elsewhere = Path(self.temp.name).resolve() / "records-elsewhere"
        elsewhere.mkdir()
        link.symlink_to(elsewhere)
        procs = self.held_launch("--", "--version")
        (name,) = self.slots()[0]
        rendered = self.settings_of(name)["filesystem"]
        ((status, out, err),) = self.release(procs)
        self.assertEqual((status, out), (0, "0.2.1-rc.5\n"), err)
        self.assertIn(str(elsewhere), rendered["denyRead"])
        self.assertIn(str(elsewhere), rendered["denyWrite"])
        self.assertNotIn(str(link), rendered["denyRead"])
        self.assertEqual(self.slots(), ([], []))

    def test_a_mode_000_directory_dsh_left_is_removed_and_a_slot_that_remains_fails_the_launch(self):
        """U272d P2 `hcom-seat:2215`: a directory dsh leaves with mode 000 (a nested one inside it too) kept `rm -rf`
        out of the state slot while the launch exited 0; the removal resets the modes first and both slots go, dsh's
        status returned. It fails closed: a slot the lever cannot remove (its parent `.state` made read-only while
        dsh runs) is named on stderr and the launch exits 2, not dsh's 0."""
        (self.calls / "leave-locked").touch()
        run = self.launch("--", "--version")
        (self.calls / "leave-locked").unlink()
        self.assertEqual((run.returncode, run.stdout), (0, "0.2.1-rc.5\n"), run.stderr)
        self.assertEqual(self.slots(), ([], []))
        procs = self.held_launch("--", "--version")
        (name,) = self.slots()[0]
        state = Path(self.seats, ".state")
        os.chmod(state, 0o555)
        try:
            ((status, out, err),) = self.release(procs)
        finally:
            os.chmod(state, 0o700)
        self.assertEqual((status, out), (2, "0.2.1-rc.5\n"), err)
        self.assertIn(f"the per-launch slot {state / name} remains after its removal", err)
        self.assertIn("dsh exited 0; the launch exits 2", err)
        self.assertEqual(self.slots(), ([], [name]))

    def test_a_profile_root_linked_to_a_denied_directory_refuses_before_any_mkdir(self):
        """U272e P1 `hcom-seat:1835`: the role renders `~/.omp/profiles/dsh` into allowWrite and allowRead, and round 4's
        refusal judged three inputs that did not include it, so a profile root linked to `~/.aws` was granted write.
        The judge reads every rendered grant: a profile root that is a link to the scratch HOME's `.aws` refuses
        (exit 2) naming the row, its physical path and the deny, in a dry run too, before any directory is made (the
        DEBUG-trap recorder shows the tool directory's mkdir alone); a link to another omp profile refuses as well
        (the `profile` tag carries only while the grant lies where it is rendered); a real profile directory goes
        through."""
        home = self.home.resolve()
        (home / ".aws").mkdir()
        (home / ".omp/profiles/orchestrator").mkdir(parents=True)
        profile = home / ".omp/profiles/dsh"
        hook = Path(self.temp.name) / "trace-hook.bash"
        hook.write_text('set -T\ntrap \'builtin printf "%s\\0" "$BASH_COMMAND" >> "$U272_TRACE"\' DEBUG\n')
        trace = Path(self.temp.name) / "trace"
        cases = (
            ("a link to ~/.aws", home / ".aws", [],
             f"allowRead row {profile} ({home / '.aws'}) is, contains or lies inside {home / '.aws'}, a row of its denyRead list"),
            ("a link to ~/.aws, dry run", home / ".aws", ["--dry-run"],
             f"allowRead row {profile} ({home / '.aws'}) is, contains or lies inside {home / '.aws'}, a row of its denyRead list"),
            ("a link to another profile", home / ".omp/profiles/orchestrator", [],
             f"allowRead row {profile} ({home / '.omp/profiles/orchestrator'}) is, contains or lies inside"
             f" {home / '.omp/profiles'}, a row of its denyRead list"),
        )  # fmt: skip
        for label, target, args, message in cases:
            with self.subTest(case=label):
                if profile.is_symlink():
                    profile.unlink()
                profile.symlink_to(target)
                trace.write_text("")
                run = self.launch(*args, "--", "--version", BASH_ENV=str(hook), U272_TRACE=str(trace))
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertIn(message, run.stderr)
                commands = trace.read_text().split("\0")[:-1]
                self.assertIn("settings_judge", " ".join(commands), "the refusal is the judge's")
                mkdirs = [c for c in commands if re.match(r"(/bin/)?mkdir\b", c)]
                self.assertTrue(mkdirs and all("tools_dir" in c for c in mkdirs), mkdirs)
        self.assertFalse(Path(self.seats).exists())
        self.assertTrue(profile.is_symlink(), "the launch neither removed nor replaced the link")
        self.assertEqual(sorted(p.name for p in (home / ".aws").iterdir()), [])
        self.assertEqual(self.dsh_calls(), [])
        profile.unlink()
        run = self.launch("--", "--version")
        self.assertEqual((run.returncode, run.stdout), (0, "0.2.1-rc.5\n"), run.stderr)
        self.assertTrue(profile.is_dir() and not profile.is_symlink())
        self.assertEqual(self.slots(), ([], []))

    def test_a_grant_row_under_any_deny_of_the_rendered_tables_refuses(self):
        """U272f: the judge's only source is the rendered tables, so a grant added under any deny of them refuses. The
        judge runs from the lever's own text over the tables a going launch rendered (its allowRead, allowWrite,
        denyRead and denyWrite, the macOS patterns aside) with the structural tags as the lever renders them, each
        naming one row by its list and position (U272g: the own cwd and state slot, rows 0 and 1 of both grant lists,
        the own profile, row 3 of both, the seats-root and project-file denies they overlap and the profiles deny; U353:
        DSH_HOME, row 3 of both grant lists, and the credential root's denyRead and denyWrite rows, tagged `credential`):
        the tables as rendered pass; for every deny path, one row added to allowWrite below it and one added to
        allowRead equal to it each hit, naming the added row and a deny it lies inside (a row equal to a tagged deny
        carries no tag: the tag names the deny's position, not its spelling); a row of the own profile's spelling at
        DSH_HOME's position hits; a tagged row that a link moves off its rendered path hits too."""
        procs = self.held_launch("--", "--version")
        (name,) = self.slots()[0]
        rendered = self.settings_of(name)["filesystem"]
        ((status, out, err),) = self.release(procs)
        self.assertEqual((status, out), (0, "0.2.1-rc.5\n"), err)
        home = self.home.resolve()
        seats = Path(self.seats).resolve()
        cwd, slot = str(seats / ".state" / name / "cwd"), str(seats / ".state" / name)
        profile, profiles = str(home / ".omp/profiles/dsh"), str(home / ".omp/profiles")
        deny_read = rendered["denyRead"]
        deny_write = [row for row in rendered["denyWrite"] if "*" not in row]
        shared = str(seats / ".state/claude")
        dsh_home, cred = str(self.dsh_home), f"{self.dsh_home}/router-credentials"
        for kind in ("allowRead", "allowWrite"):
            self.assertEqual([rendered[kind][i] for i in (0, 1, 2, 3, 4)], [cwd, slot, shared, dsh_home, profile], kind)
        tags = [(tag, kind, ix, path) for kind in ("allowRead", "allowWrite")
                for tag, ix, path in (("slot", 0, cwd), ("slot", 1, slot), ("slot", 2, shared), ("credential", 3, dsh_home), ("profile", 4, profile))]  # fmt: skip
        tags += [("slot", "denyWrite", ix, row) for ix, row in enumerate(deny_write) if row.startswith(cwd + "/")]
        # The eight configuration denies under the shared directory (U318), tagged like the project-file rows.
        tags += [("slot", "denyWrite", ix, row) for ix, row in enumerate(deny_write) if row.startswith(shared + "/")]
        tags += [
            ("slot", "denyRead", deny_read.index(row), row)
            for row in (str(home / ".local/state/omp-seats"), str(seats))
        ]
        tags += [("profile", "denyRead", deny_read.index(profiles), profiles)]
        # The credential root's two deny rows (U353), paired with the DSH_HOME grants they lie inside by construction.
        tags += [
            ("credential", "denyRead", deny_read.index(cred), cred),
            ("credential", "denyWrite", deny_write.index(cred), cred),
        ]
        self.assertEqual(len(tags), 10 + 8 + 8 + 2 + 1 + 2, tags)

        def judge(allow_read, write, deny_read, deny_write):
            return self.judge_run(tags, allow_read, write, deny_read, deny_write)

        clear = judge(rendered["allowRead"], rendered["allowWrite"], deny_read, deny_write)
        self.assertEqual((clear.returncode, clear.stdout), (0, ""), clear.stderr)
        denies = [(row, "denyRead") for row in deny_read] + [(row, "denyWrite") for row in deny_write]
        self.assertGreater(len(denies), 40, denies)
        for deny, kind in denies:
            # The deny a hit names is the first row in table order the added row overlaps: the deny itself, one above
            # it, or (for a row equal to it) one below it.
            related = [row for row, _ in denies
                       if Path(deny) == Path(row) or Path(row) in Path(deny).parents or Path(deny) in Path(row).parents]  # fmt: skip
            cases = [
                ("below it in allowWrite", f"{deny}/u272f-added", rendered["allowRead"], [*rendered["allowWrite"], f"{deny}/u272f-added"]),
                ("equal to it in allowRead", deny, [*rendered["allowRead"], deny], rendered["allowWrite"]),
            ]  # fmt: skip
            for label, added, allow_read, write in cases:
                with self.subTest(deny=deny, kind=kind, case=label):
                    hit = judge(allow_read, write, deny_read, deny_write)
                    self.assertEqual(hit.returncode, 3, hit.stdout + hit.stderr)
                    grant, named = hit.stdout.splitlines()
                    self.assertEqual(
                        grant, f"grant={'allowWrite' if 'allowWrite' in label else 'allowRead'} row {added}"
                    )
                    self.assertIn(
                        named.removeprefix("deny=").split(", a row of its ")[0].split(" (")[0], related, hit.stdout
                    )
        # The own profile's spelling at DSH_HOME's position (allowRead row 3): the tag names row 4 alone, so the row
        # hits the profiles deny like any other, where round 5's spelling-keyed tag exempted it.
        same = judge(
            [*rendered["allowRead"][:3], profile, *rendered["allowRead"][4:]],
            rendered["allowWrite"],
            deny_read,
            deny_write,
        )
        self.assertEqual(same.returncode, 3, same.stdout + same.stderr)
        self.assertEqual(
            same.stdout.splitlines(), [f"grant=allowRead row {profile}", f"deny={profiles}, a row of its denyRead list"]
        )
        # A tagged row moved by a link: the profile row is still at its position and spelled as rendered, so its tag
        # is found, and the exemption fails because its physical path is elsewhere.
        shutil.rmtree(home / ".omp/profiles/dsh")
        (home / ".omp/profiles/dsh").symlink_to(home / ".omp/profiles/orchestrator")
        (home / ".omp/profiles/orchestrator").mkdir()
        moved = judge(rendered["allowRead"], rendered["allowWrite"], deny_read, deny_write)
        self.assertEqual(moved.returncode, 3, moved.stdout + moved.stderr)
        self.assertIn(f"grant=allowRead row {profile} ({home / '.omp/profiles/orchestrator'})", moved.stdout)
        self.assertIn(f"deny={profiles}, a row of its denyRead list", moved.stdout)

    def test_a_termination_that_cannot_remove_a_slot_exits_2_naming_it(self):
        """U272e P2 `hcom-seat:2340`: when the slot removal failed under a signal, `set -e` ended the handler before the
        signal was restored, so SIGTERM with a read-only `.state` exited 1 with the slot behind. The handler reads
        the removal's status: the slot that remains is named and the launch exits 2 (not 1, not the signal's
        status); the sandbox slot, which could be removed, is gone."""
        (proc,) = self.held_launch("--", "--version", new_session=True)
        (name,) = self.slots()[0]
        state = Path(self.seats, ".state")
        os.chmod(state, 0o555)
        try:
            os.killpg(proc.pid, signal.SIGTERM)
            out, err = proc.communicate(timeout=60)
        finally:
            os.chmod(state, 0o700)
            (self.calls / "hold").unlink()
        self.assertEqual((proc.returncode, out), (2, ""), err)
        self.assertIn(f"the per-launch slot {state / name} remains after its removal", err)
        self.assertIn("ended by SIGTERM; the launch exits 2 because a per-launch slot remains", err)
        self.assertEqual(self.slots(), ([], [name]))

    def test_a_dsh_home_or_run_root_at_the_profiles_directory_refuses_while_the_own_profile_passes(self):
        """U272f P1 `hcom-seat:1863`: round 5 keyed the exemption tags by rendered spelling, so a DSH_HOME equal to the
        profiles directory, or a `~/.omp/run` linked to it, was rendered in that spelling, inherited the own-profile
        exemption and put the whole profiles directory into allowWrite. A tag now names one row by its list and
        position: a DSH_HOME at the scratch HOME's `.omp/profiles` (holding a working `bin/dsh`), a DSH_HOME equal to
        the own profile `~/.omp/profiles/dsh` (the exempted row's own spelling, at another position) and a `~/.omp/run`
        linked to the profiles directory each refuse (exit 2) naming the profiles deny, before any directory is made
        (the DEBUG-trap recorder shows the tool directory's mkdir alone); the own profile row still passes."""
        home = self.home.resolve()
        profiles = home / ".omp/profiles"
        (profiles / "bin").mkdir(parents=True)
        for path in (profiles / "bin/dsh", profiles / "dsh/bin/dsh"):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(FAKE_DSH.format(calls=str(self.calls)))
            path.chmod(0o755)
        run_root = home / ".omp/run"
        hook = Path(self.temp.name) / "trace-hook.bash"
        hook.write_text('set -T\ntrap \'builtin printf "%s\\0" "$BASH_COMMAND" >> "$U272_TRACE"\' DEBUG\n')
        trace = Path(self.temp.name) / "trace"
        cases = (
            ("DSH_HOME at the profiles directory", profiles, None,
             f"allowRead row {profiles} is, contains or lies inside {profiles}, a row of its denyRead list"),
            ("DSH_HOME at the profiles directory, dry run", profiles, "--dry-run",
             f"allowRead row {profiles} is, contains or lies inside {profiles}, a row of its denyRead list"),
            ("DSH_HOME equal to the own profile", profiles / "dsh", None,
             f"allowRead row {profiles / 'dsh'} is, contains or lies inside {profiles}, a row of its denyRead list"),
            ("~/.omp/run linked to the profiles directory", self.dsh_home, None,
             f"allowWrite row {profiles} is, contains or lies inside {profiles}, a row of its denyRead list"),
        )  # fmt: skip
        for label, dsh_home, option, message in cases:
            with self.subTest(case=label):
                if dsh_home == self.dsh_home:  # lint-comparisons: allow picks the fixture's own object, no path compare
                    run_root.symlink_to(profiles)
                trace.write_text("")
                run = self.seat("dsh", "--seats-root", self.seats, "--home", str(dsh_home), *([option] if option else []),
                                "--", "--version", BASH_ENV=str(hook), U272_TRACE=str(trace))  # fmt: skip
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertIn(message, run.stderr)
                self.assertIn("the launch is refused before anything is made", run.stderr)
                commands = trace.read_text().split("\0")[:-1]
                self.assertIn("settings_judge", " ".join(commands), "the refusal is the judge's")
                mkdirs = [c for c in commands if re.match(r"(/bin/)?mkdir\b", c)]
                self.assertTrue(mkdirs and all("tools_dir" in c for c in mkdirs), mkdirs)
        self.assertFalse(Path(self.seats).exists())
        self.assertTrue(run_root.is_symlink(), "the launch neither removed nor replaced the link")
        self.assertEqual(self.dsh_calls(), [])
        # The own profile row, at its own position, passes: the same launch goes through once `~/.omp/run` is a
        # directory again, with the profiles directory in no grant list but as the own profile row.
        run_root.unlink()
        procs = self.held_launch("--", "--version")
        (name,) = self.slots()[0]
        rendered = self.settings_of(name)["filesystem"]
        ((status, out, err),) = self.release(procs)
        self.assertEqual((status, out), (0, "0.2.1-rc.5\n"), err)
        for kind in ("allowRead", "allowWrite"):
            self.assertEqual(rendered[kind][4], str(profiles / "dsh"), kind)
            self.assertNotIn(str(profiles), rendered[kind], kind)
        self.assertIn(str(profiles), rendered["denyRead"])
        self.assertTrue(run_root.is_dir() and not run_root.is_symlink())
        self.assertEqual(self.slots(), ([], []))

    def test_an_unsearchable_state_parent_at_cleanup_exits_2_naming_the_slot(self):
        """U272f P2 `hcom-seat:2347`: `[[ -e ]]` and `[[ -L ]]` are both false for a slot whose parent cannot be
        searched, so a `.state` of mode 000 at cleanup made the lever read its slot as absent and exit 0 with the slot
        behind. The existence read is a status-checked stat: a failed read that is not ENOENT refuses (exit 2) naming
        the slot and the error, on the normal exit and under a signal alike; the sandbox slot, read and removed
        first, is gone."""
        state = Path(self.seats, ".state")
        procs = self.held_launch("--", "--version")
        (name,) = self.slots()[0]
        os.chmod(state, 0)
        try:
            ((status, out, err),) = self.release(procs)
        finally:
            os.chmod(state, 0o700)
        self.assertEqual((status, out), (2, "0.2.1-rc.5\n"), err)
        self.assertIn(f"cannot read whether the per-launch slot {state / name} exists (", err)
        self.assertIn("Permission denied", err)
        self.assertNotIn("remains after its removal", err, "a failed read is not read as a slot that was removed")
        self.assertEqual(self.slots(), ([], [name]))
        shutil.rmtree(state / name)
        (proc,) = self.held_launch("--", "--version", new_session=True)
        (name,) = self.slots()[0]
        os.chmod(state, 0)
        try:
            os.killpg(proc.pid, signal.SIGTERM)
            out, err = proc.communicate(timeout=60)
        finally:
            os.chmod(state, 0o700)
            (self.calls / "hold").unlink()
        self.assertEqual((proc.returncode, out), (2, ""), err)
        self.assertIn(f"cannot read whether the per-launch slot {state / name} exists (", err)
        self.assertEqual(self.slots(), ([], [name]))

    def test_the_profile_config_is_placed_replaced_or_kept_with_the_extension_at_its_allow_list_path(self):
        """U310: the dsh role's profile config row. The rendered overlay `~/.agents/omp/profiles/dsh.yml` is placed as
        the profile's own `~/.omp/profiles/dsh/agent/config.yml` before the launch (the file the gateway child reads for
        its providers), its extension entry rewritten to the canonical allow-list path when the overlay spells it
        through a link; a config that differs is replaced and the launch says so; an equal one is left alone (the
        DEBUG-trap recorder shows the one helper run after the write step began and nothing of the earlier rounds'
        bash write, and its inode and mtime stand); a dry run prints the decision and makes nothing (U310d)."""
        overlay = self.profiles / "dsh.yml"
        link = self.home / "link-to-bridge"
        link.symlink_to(self.bridge)
        overlay.write_text(DSH_OVERLAY.format(extension=link))
        expected = placed_overlay(self.bridge)
        run = self.launch("--dry-run", "--", "--version")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertIn(
            f"hcom-seat: the dsh profile config {self.profile_config} is absent; the launch places it from {overlay}",
            run.stderr,
        )
        self.assertFalse((self.home / ".omp").exists(), "a dry run places nothing")
        run = self.launch("--", "--version")
        self.assertEqual((run.returncode, run.stdout), (0, "0.2.1-rc.5\n"), run.stderr)
        self.assertIn(f"{self.profile_config} is absent; the launch places it from {overlay}", run.stderr)
        self.assertEqual(self.profile_config.read_text(), expected)
        agent = self.profile_config.parent
        self.assertTrue(agent.is_dir() and not agent.is_symlink() and not self.profile_config.is_symlink())
        self.assertEqual(stat.S_IMODE(agent.stat().st_mode), 0o700)
        self.assertEqual(stat.S_IMODE(self.profile_config.stat().st_mode), 0o600)
        self.assertEqual(sorted(p.name for p in agent.iterdir()), ["config.yml"], "no temporary file remains")
        self.profile_config.write_text("modelRoles:\n  default: stale/model\n")
        run = self.launch("--", "--version")
        self.assertEqual((run.returncode, run.stdout), (0, "0.2.1-rc.5\n"), run.stderr)
        self.assertIn(f"{self.profile_config} differs from {overlay}; the launch replaces it", run.stderr)
        self.assertEqual(self.profile_config.read_text(), expected)
        before = self.profile_config.stat()
        hook = Path(self.temp.name) / "trace-hook.bash"
        hook.write_text('set -T\ntrap \'builtin printf "%s\\0" "$BASH_COMMAND" >> "$U272_TRACE"\' DEBUG\n')
        trace = Path(self.temp.name) / "trace"
        trace.write_text("")
        run = self.launch("--", "--version", BASH_ENV=str(hook), U272_TRACE=str(trace))
        self.assertEqual((run.returncode, run.stdout), (0, "0.2.1-rc.5\n"), run.stderr)
        self.assertIn(f"{self.profile_config} equals {overlay}; the launch leaves it", run.stderr)
        commands = trace.read_text().split("\0")[:-1]
        self.assertIn("profile_config_write", commands, "the write step ran and the helper decided to leave the file")
        write_at = commands.index("profile_config_write")
        judge_at = commands.index("settings_judge")
        helper_runs = [i for i, c in enumerate(commands) if "profile_config_cmd[@]" in c]
        self.assertTrue(helper_runs, "the helper ran")
        self.assertTrue(all(judge_at < write_at < i for i in helper_runs), "the one helper run is the write (U310d)")
        gone = ("profile_config_tmp", "${tmp_name}", "exec 9>", "noclobber", "cmp -s")
        self.assertEqual([c for c in commands if any(word in c for word in gone)], [], "no bash write remains")
        shell_renames = ("/bin/mv -f",)
        self.assertEqual([c for c in commands[write_at:] if any(w in c for w in shell_renames)], [], "no shell rename")
        self.assertEqual(sorted(p.name for p in self.profile_config.parent.iterdir()), ["config.yml"])
        after = self.profile_config.stat()
        self.assertEqual((before.st_ino, before.st_mtime_ns), (after.st_ino, after.st_mtime_ns))
        self.assertEqual(self.profile_config.read_text(), expected)
        self.assertEqual(len(self.dsh_calls()), 3)
        self.assertEqual(self.slots(), ([], []))

    def test_a_linked_agent_directory_or_config_and_a_bad_overlay_refuse_before_any_mkdir(self):
        """U310: an `agent/` or `config.yml` that is a symbolic link refuses (exit 2) naming it, in a dry run too,
        before any directory is made (U310b: the recorder shows no mkdir at all, the private tool directory's included,
        and a fresh HOME gains no directory) and without following the link; an overlay that is absent, names no
        extension or names a directory outside the allow-list refuses the same way. Nothing reaches the link's target
        and no dsh starts."""
        home = self.home.resolve()
        overlay = self.profiles / "dsh.yml"
        elsewhere = Path(self.temp.name).resolve() / "elsewhere"
        elsewhere.mkdir()
        profile = home / ".omp/profiles/dsh"
        agent = profile / "agent"
        hook = Path(self.temp.name) / "trace-hook.bash"
        hook.write_text('set -T\ntrap \'builtin printf "%s\\0" "$BASH_COMMAND" >> "$U272_TRACE"\' DEBUG\n')
        trace = Path(self.temp.name) / "trace"
        inside = "the dsh role writes its profile config inside its profile only"

        def agent_link():
            profile.mkdir(parents=True)
            agent.symlink_to(elsewhere)

        def config_link():
            agent.mkdir(parents=True)
            self.profile_config.symlink_to(elsewhere / "config.yml")

        cases = (
            ("agent is a link", agent_link, [], f"{agent} is a symbolic link; {inside}"),
            ("agent is a link, dry run", agent_link, ["--dry-run"], f"{agent} is a symbolic link; {inside}"),
            ("config is a link", config_link, [], f"{self.profile_config} is a symbolic link; {inside}"),
            ("config is a link, dry run", config_link, ["--dry-run"], f"{self.profile_config} is a symbolic link; {inside}"),
            ("overlay absent", overlay.unlink, [], f"profile config overlay absent or a symbolic link: {overlay}"),
            ("overlay names no extension", lambda: overlay.write_text("modelRoles:\n  default: x/y\n"), [],
             f"the profile config overlay {overlay} names no extension; the gateway child needs the bridge route"),
            ("overlay names a directory outside the allow-list",
             lambda: overlay.write_text(DSH_OVERLAY.format(extension=elsewhere)), [],
             f"extension directory is not in the allow-list (claude.levers.extensions): {elsewhere}"),
        )  # fmt: skip
        for label, arrange, args, message in cases:
            with self.subTest(case=label):
                if agent.is_symlink():
                    agent.unlink()
                shutil.rmtree(profile, ignore_errors=True)
                overlay.write_text(DSH_OVERLAY.format(extension=self.bridge))
                arrange()
                trace.write_text("")
                run = self.launch(*args, "--", "--version", BASH_ENV=str(hook), U272_TRACE=str(trace))
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertIn(message, run.stderr)
                commands = trace.read_text().split("\0")[:-1]
                mkdirs = [c for c in commands if re.match(r"(/usr)?(/bin/)?(mkdir|mktemp)\b", c)]
                self.assertEqual(mkdirs, [], "a refusal of the profile config row makes nothing")
                self.assertFalse((self.home / ".local/state").exists(), "the private tool directory is not made")
                self.assertEqual(sorted(p.name for p in elsewhere.iterdir()), [], "nothing reaches the link's target")
                self.assertFalse(Path(self.seats).exists())
        self.assertEqual(self.dsh_calls(), [])

    def test_a_planted_temporary_name_is_never_opened_and_the_config_lands_beside_it(self):
        """U310b (the round-1 P1): the launcher writes through a name `mktemp` picks inside `agent/`, opened O_EXCL, so
        a link planted at the old predictable `config.yml.tmp.<launcher pid>` (planted by a wrapper that then `exec`s
        the launcher, so the pid is the launcher's own), at any other guessable `.config.yml.*` or `config.yml.tmp*`
        name, a dangling one, or a regular file there, is never opened: the link's target (a scratch default-profile
        config) keeps its bytes, inode and mtime through a placement and a replacement, every planted entry stands as
        planted, and the real config lands as a regular file equal to the overlay with no temporary file left beside
        it."""
        home = self.home.resolve()
        agent = home / ".omp/profiles/dsh/agent"
        agent.mkdir(parents=True)
        elsewhere = Path(self.temp.name).resolve() / "elsewhere"
        elsewhere.mkdir()
        default_config = elsewhere / "config.yml"
        default_config.write_text("modelRoles:\n  default: operator/default\n")
        before = default_config.stat()
        links = ["config.yml.tmp", ".config.yml.tmp", ".config.yml.aaaaaa", ".config.yml.XXXXXX", ".config.yml.000000"]
        for name in links:
            (agent / name).symlink_to(default_config)
        (agent / ".config.yml.zzzzzz").symlink_to(elsewhere / "missing")
        (agent / "config.yml.tmp.1").write_text("a planted regular file\n")
        pid_file = Path(self.temp.name) / "launcher-pid"
        wrapper = Path(self.temp.name) / "plant-then-exec.sh"
        wrapper.write_text(
            "#!/bin/bash\n"
            'ln -s "$1" "$2/config.yml.tmp.$$" || exit 97\n'
            'printf "%s\\n" "$$" > "$3" || exit 97\n'
            "shift 3\n"
            f'exec {shlex.quote(str(test_hcom_seat.SEAT))} "$@"\n'
        )
        wrapper.chmod(0o755)
        expected = placed_overlay(self.bridge)

        def planted():
            self.assertEqual(default_config.read_text(), "modelRoles:\n  default: operator/default\n")
            after = default_config.stat()
            self.assertEqual((before.st_ino, before.st_mtime_ns), (after.st_ino, after.st_mtime_ns))
            for name in [*links, f"config.yml.tmp.{pid}"]:
                self.assertTrue((agent / name).is_symlink(), name)
                self.assertEqual(os.readlink(agent / name), str(default_config), name)
            self.assertEqual(os.readlink(agent / ".config.yml.zzzzzz"), str(elsewhere / "missing"))
            self.assertEqual((agent / "config.yml.tmp.1").read_text(), "a planted regular file\n")
            self.assertTrue(self.profile_config.is_file() and not self.profile_config.is_symlink())
            self.assertEqual(self.profile_config.read_text(), expected)
            self.assertEqual(stat.S_IMODE(self.profile_config.stat().st_mode), 0o600)
            names = [*links, ".config.yml.zzzzzz", "config.yml", "config.yml.tmp.1", f"config.yml.tmp.{pid}"]
            self.assertEqual(sorted(p.name for p in agent.iterdir()), sorted(names), "no temporary file remains")
            self.assertEqual(sorted(p.name for p in elsewhere.iterdir()), ["config.yml"])

        argv = [str(wrapper), str(default_config), str(agent), str(pid_file), "dsh", "--seats-root", self.seats,
                "--home", str(self.dsh_home), "--", "--version"]  # fmt: skip
        run = subprocess.run(argv, cwd=self.repo, env=self.env, capture_output=True, text=True, check=False)
        self.assertEqual((run.returncode, run.stdout), (0, "0.2.1-rc.5\n"), run.stderr)
        pid = pid_file.read_text().strip()
        self.assertTrue(pid.isdigit() and (agent / f"config.yml.tmp.{pid}").is_symlink(), pid)
        self.assertIn(f"{self.profile_config} is absent; the launch places it", run.stderr)
        planted()
        self.profile_config.write_text("modelRoles:\n  default: stale/model\n")
        run = self.launch("--", "--version")
        self.assertEqual((run.returncode, run.stdout), (0, "0.2.1-rc.5\n"), run.stderr)
        self.assertIn(f"{self.profile_config} differs from", run.stderr)
        planted()
        self.assertEqual(len(self.dsh_calls()), 2)
        self.assertEqual(self.slots(), ([], []))

    def test_an_unreadable_config_an_unsearchable_directory_or_a_read_only_agent_refuses_naming_it(self):
        """U310b (the round-1 P2s and the auditor's probes), U310d: every read the placement decides on fails closed by
        name. A config dsh left unreadable refuses through the helper's open of it, whose line names the step and the
        errno, in a dry run too; an `agent/` that cannot be searched (mode 000, a linked config hidden inside) and a
        profile directory that cannot be searched refuse naming the directory instead of reading as absent, in a dry
        run too; an overlay that cannot be read refuses naming it; an `agent/` the launcher cannot write (mode 500)
        refuses at the helper's exclusive create naming it, with a stale config and with none. No temporary file
        remains, the config is never replaced by a refused launch, nothing reaches the link's target, no dsh starts and
        (U310c, the round-2 P2 at :2601) no per-launch slot remains after a refusal at the write."""
        home = self.home.resolve()
        overlay = self.profiles / "dsh.yml"
        elsewhere = Path(self.temp.name).resolve() / "elsewhere"
        elsewhere.mkdir()
        profile = home / ".omp/profiles/dsh"
        agent = profile / "agent"
        expected = placed_overlay(self.bridge)
        stale = "modelRoles:\n  default: stale/model\n"
        refused = f"the dsh profile config {self.profile_config} was not placed: profile-config-place: refused at"
        cannot_read = f"{refused} open-config: {self.profile_config}: cannot open it: Permission denied (EACCES)"
        no_temporary = f"{refused} create-temporary: {agent}/.config.yml."
        cannot_create = f"cannot create a temporary file in {agent}: Permission denied (EACCES)"

        def unreadable_config():
            agent.mkdir(parents=True)
            self.profile_config.write_text(expected)
            self.profile_config.chmod(0)

        def unsearchable_agent():
            agent.mkdir(parents=True)
            self.profile_config.symlink_to(elsewhere / "config.yml")
            agent.chmod(0)

        def unsearchable_profile():
            profile.mkdir(parents=True)
            profile.chmod(0)

        def read_only_agent_with_stale_config():
            agent.mkdir(parents=True)
            self.profile_config.write_text(stale)
            agent.chmod(0o500)

        def read_only_agent_without_config():
            agent.mkdir(parents=True)
            agent.chmod(0o500)

        def unlock():
            overlay.chmod(0o644)
            for directory in (profile, agent):
                if directory.is_dir() and not directory.is_symlink():
                    directory.chmod(0o700)
            if self.profile_config.is_file():
                self.profile_config.chmod(0o600)
            shutil.rmtree(profile, ignore_errors=True)

        cases = (
            ("the config cannot be read", unreadable_config, [], cannot_read, expected),
            ("the config cannot be read, dry run", unreadable_config, ["--dry-run"], cannot_read, expected),
            ("agent cannot be searched", unsearchable_agent, [],
             f"cannot search {agent}; the dsh profile config below it cannot be read", None),
            ("agent cannot be searched, dry run", unsearchable_agent, ["--dry-run"],
             f"cannot search {agent}; the dsh profile config below it cannot be read", None),
            ("the profile directory cannot be searched", unsearchable_profile, ["--dry-run"],
             f"cannot search {profile}; the dsh profile config below it cannot be read", None),
            ("the overlay cannot be read", lambda: overlay.chmod(0), [],
             f"cannot read the profile config overlay {overlay}", None),
            ("agent is read-only, a stale config", read_only_agent_with_stale_config, [], no_temporary, stale),
            ("agent is read-only, no config", read_only_agent_without_config, [], no_temporary, None),
        )  # fmt: skip
        for label, arrange, args, message, config_after in cases:
            with self.subTest(case=label):
                unlock()
                overlay.write_text(DSH_OVERLAY.format(extension=self.bridge))
                arrange()
                run = self.launch(*args, "--", "--version")
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertIn(message, run.stderr)
                if message == no_temporary:
                    self.assertIn(cannot_create, run.stderr)
                self.assertEqual(sorted(p.name for p in elsewhere.iterdir()), [], "nothing reaches the link's target")
                self.assertEqual(self.slots(), ([], []), "a refusal after the slots are made removes them")
                overlay.chmod(0o644)
                for directory in (profile, agent):
                    if directory.is_dir() and not directory.is_symlink():
                        directory.chmod(0o700)
                if agent.is_dir():
                    self.assertEqual(
                        [p.name for p in agent.iterdir() if p.name != "config.yml"], [], "no temporary file"
                    )
                if config_after is None:
                    self.assertFalse(self.profile_config.is_file() and not self.profile_config.is_symlink())
                else:
                    self.profile_config.chmod(0o600)
                    self.assertEqual(self.profile_config.read_text(), config_after, "a refused launch replaces nothing")
        self.assertEqual(self.dsh_calls(), [])

    def test_a_dry_run_reads_a_present_config_through_the_helper_and_writes_nothing(self):
        """U310d: the dry run's compare of a present config is the helper's `--dry-run` after settings_judge, a read
        through the held descriptor: a stale config inside an `agent/` the launcher cannot write prints the decision
        (rounds 2 and 3 needed a temporary file here and refused) and nothing is made or written; an equal one prints
        `equals`. The recorder shows the helper after the judge and no write step."""
        overlay = self.profiles / "dsh.yml"
        agent = self.profile_config.parent
        agent.mkdir(parents=True)
        self.addCleanup(agent.chmod, 0o700)
        stale = "modelRoles:\n  default: stale/model\n"
        hook = Path(self.temp.name) / "trace-hook.bash"
        hook.write_text('set -T\ntrap \'builtin printf "%s\\0" "$BASH_COMMAND" >> "$U272_TRACE"\' DEBUG\n')
        trace = Path(self.temp.name) / "trace"
        for config, line in ((stale, "differs from"), (placed_overlay(self.bridge), "equals")):
            with self.subTest(config=line):
                agent.chmod(0o700)
                self.profile_config.write_text(config)
                before = self.profile_config.stat()
                agent.chmod(0o500)
                trace.write_text("")
                run = self.launch("--dry-run", "--", "--version", BASH_ENV=str(hook), U272_TRACE=str(trace))
                self.assertEqual(run.returncode, 0, run.stderr)
                self.assertIn(f"hcom-seat: the dsh profile config {self.profile_config} {line} {overlay}", run.stderr)
                after = self.profile_config.stat()
                self.assertEqual(self.profile_config.read_text(), config, "a dry run writes nothing")
                self.assertEqual((before.st_ino, before.st_mtime_ns), (after.st_ino, after.st_mtime_ns))
                self.assertEqual(sorted(p.name for p in agent.iterdir()), ["config.yml"], "no temporary file")
                commands = trace.read_text().split("\0")[:-1]
                judge_at = commands.index("settings_judge")
                helper_runs = [i for i, c in enumerate(commands) if "profile_config_cmd[@]" in c]
                self.assertTrue(helper_runs and all(i > judge_at for i in helper_runs), "the helper follows the judge")
                self.assertIn("profile_config_compare", commands)
                self.assertNotIn("profile_config_write", commands)
                self.assertFalse(Path(self.seats).exists(), "a dry run makes no slot")
        self.assertEqual(self.dsh_calls(), [])

    def test_no_shell_step_runs_between_the_temporarys_creation_and_its_rename(self):
        """U310c's deterministic swap (the round-2 P1 at :982) adapted to the mechanism that ends the class (U310d): the
        temporary exists only inside the helper's one run, so a DEBUG trap that lists `agent/` before every shell
        command and swaps any `.config.yml.*` entry it finds for a link to a victim file never finds one; the config
        lands (placed, then replaced) with the victim's bytes, inode and mtime untouched, and the lever's text holds
        nothing of the round-3 write (`exec 9>`, `noclobber`, `tmp_refuse`, the `umask` read, `cmp`)."""
        home = self.home.resolve()
        agent = home / ".omp/profiles/dsh/agent"
        agent.mkdir(parents=True)
        elsewhere = Path(self.temp.name).resolve() / "elsewhere"
        elsewhere.mkdir()
        victim = elsewhere / "config.yml"
        victim_text = "modelRoles:\n  default: operator/default\n# the host file the swapped link points at\n"
        victim.write_text(victim_text)
        before = victim.stat()
        seen = Path(self.temp.name) / "swaps-seen"
        seen.write_text("")
        hook = Path(self.temp.name) / "swap-any-temporary.bash"
        hook.write_text(
            "set -T\n"
            'trap \'for e in "${U310_AGENT}"/.config.yml.*; do [[ -e ${e} || -L ${e} ]] || continue;'
            ' /bin/rm -f -- "${e}" && /bin/ln -s "${U310_VICTIM}" "${e}" && echo "hook: swapped ${e}" >> "${U310_SEEN}";'
            " done' DEBUG\n"
        )
        expected = placed_overlay(self.bridge)
        for config in (None, "modelRoles:\n  default: stale/model\n"):
            with self.subTest(config="absent" if config is None else "stale"):
                if config is not None:
                    self.profile_config.write_text(config)
                run = self.launch("--", "--version", BASH_ENV=str(hook), U310_AGENT=str(agent),
                                  U310_VICTIM=str(victim), U310_SEEN=str(seen))  # fmt: skip
                self.assertEqual((run.returncode, run.stdout), (0, "0.2.1-rc.5\n"), run.stderr)
                self.assertEqual(seen.read_text(), "", "no shell command ran while a temporary existed")
                self.assertEqual(self.profile_config.read_text(), expected)
                self.assertEqual(sorted(p.name for p in agent.iterdir()), ["config.yml"])
                after = victim.stat()
                self.assertEqual(victim.read_text(), victim_text)
                self.assertEqual((before.st_ino, before.st_mtime_ns), (after.st_ino, after.st_mtime_ns))
                self.assertEqual(self.slots(), ([], []))
        self.assertEqual(len(self.dsh_calls()), 2)
        text = test_hcom_seat.SEAT.read_text()
        for word in ("exec 9>", "noclobber", "tmp_refuse", "mask=$(umask)", "cmp -s", "profile_config_tmp", "tmp_name"):
            self.assertNotIn(word, text, "the round-3 bash write is gone, not kept beside the helper")

    def test_a_linked_profile_root_dry_run_writes_nothing_in_the_linked_profile(self):
        """U310c (the round-2 P2 at :1102): round 2 made the comparison temporary before settings_judge validated the
        profile boundary, so with `profiles/dsh` linked to `profiles/orchestrator` a dry run wrote inside
        `orchestrator/agent` before refusing. The compare now follows the judge: the dry run and the real launch
        refuse (exit 2) by the judge's row, the orchestrator profile's `agent/` keeps its entries and its mtime, the
        recorder shows no temporary file opened and no slot is made."""
        home = self.home.resolve()
        other = home / ".omp/profiles/orchestrator/agent"
        other.mkdir(parents=True)
        (other / "config.yml").write_text("modelRoles:\n  default: orchestrator/own\n")
        (home / ".omp/profiles/dsh").symlink_to(home / ".omp/profiles/orchestrator")
        hook = Path(self.temp.name) / "trace-hook.bash"
        hook.write_text('set -T\ntrap \'builtin printf "%s\\0" "$BASH_COMMAND" >> "$U272_TRACE"\' DEBUG\n')
        trace = Path(self.temp.name) / "trace"
        before = other.stat()
        for args in (["--dry-run"], []):
            with self.subTest(args=args):
                trace.write_text("")
                run = self.launch(*args, "--", "--version", BASH_ENV=str(hook), U272_TRACE=str(trace))
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertIn(
                    f"allowRead row {home / '.omp/profiles/dsh'} ({home / '.omp/profiles/orchestrator'}) is, contains"
                    f" or lies inside {home / '.omp/profiles'}, a row of its denyRead list",
                    run.stderr,
                )
                commands = trace.read_text().split("\0")[:-1]
                self.assertIn("settings_judge", commands)
                self.assertEqual([c for c in commands if "profile_config_cmd[@]" in c], [], "no helper run")
                self.assertEqual(sorted(p.name for p in other.iterdir()), ["config.yml"], "nothing written there")
                after = other.stat()
                self.assertEqual(before.st_mtime_ns, after.st_mtime_ns, "the linked profile's agent/ is untouched")
                self.assertEqual((other / "config.yml").read_text(), "modelRoles:\n  default: orchestrator/own\n")
                self.assertFalse(Path(self.seats).exists())
        self.assertEqual(self.dsh_calls(), [])

    def test_the_helpers_refusal_and_status_reach_the_launcher_and_no_slot_remains(self):
        """U310d: the helper's exit 2 and its stderr line (the step, the path, the errno) become the launcher's refusal;
        a helper run that exits with another status (the producer failing: 7, silent and with output) or prints no
        decision word refuses naming it (standing order 21); a helper whose digest differs from its pin, or none beside
        the lever, refuses naming it. The failing runs are pinned stand-in helpers beside a copy of the lever (the
        fixture's fake tools run under `python3` and the lever refuses a script in an interpreter's place, so the
        producer is varied, not the interpreter). Each case: exit 2, nothing on stdout, no slot, no temporary, no
        replacement, no dsh."""
        agent = self.profile_config.parent
        stale = "modelRoles:\n  default: stale/model\n"
        helper_name = "profile-config-place.py"
        tree = Path(self.temp.name).resolve() / "tree"
        (tree / "scripts/orchestrator").mkdir(parents=True)
        (tree / "home/dot_agents").mkdir(parents=True)
        for name in ("hcom-seat", "regime-env", "seat-login-preflight"):
            shutil.copy2(test_hcom_seat.ROOT / "scripts/orchestrator" / name, tree / "scripts/orchestrator" / name)
        manifest = (test_hcom_seat.ROOT / "home/dot_agents/agent-config.yaml").read_text()
        pin_line = next(line for line in manifest.splitlines() if line.startswith(f"      {helper_name}: "))
        tree_lever = tree / "scripts/orchestrator/hcom-seat"
        tree_helper = tree / "scripts/orchestrator" / helper_name
        tree_manifest = f"{tree}/scripts/orchestrator/../../home/dot_agents/agent-config.yaml"

        def tree_with(helper_text, pin=None):
            """The scratch tree's helper is `helper_text` (None: no helper) pinned to its own digest, or to `pin`."""

            def arrange():
                tree_helper.unlink(missing_ok=True)
                if helper_text is not None:
                    tree_helper.write_text(helper_text)
                    tree_helper.chmod(0o755)
                digest = pin or hashlib.sha256(tree_helper.read_bytes()).hexdigest()
                (tree / "home/dot_agents/agent-config.yaml").write_text(
                    manifest.replace(pin_line, f"      {helper_name}: {digest}")
                )
                self.lever = tree_lever

            return arrange

        real_helper = (test_hcom_seat.ROOT / "scripts/orchestrator" / helper_name).read_text()
        helper = f"the profile config helper {helper_name}"
        not_placed = f"the dsh profile config {self.profile_config} was not placed: profile-config-place: refused at"
        pin_differs = f" of {tree_helper} differs from the pin in {tree_manifest}; the helper is not the pinned one"
        cases = (
            ("the helper refuses (agent is read-only)", lambda: agent.chmod(0o500), None,
             f"{not_placed} create-temporary: ", "(EACCES)"),
            ("the helper exits 7 silently", tree_with("import sys\nsys.exit(7)\n"), stale,
             f"{helper} exited 7 for {self.profile_config}: no output", ""),
            ("the helper exits 7 with output", tree_with('import sys\nprint("boom", file=sys.stderr)\nsys.exit(7)\n'),
             None, f"{helper} exited 7 for {self.profile_config}: boom", ""),
            ("the helper prints no decision", tree_with('print("bogus")\n'), stale,
             f"{helper} printed no decision for {self.profile_config}: 'bogus'", ""),
            ("the helper's digest differs from its pin", tree_with(real_helper, pin="0" * 64), None,
             pin_differs, "hcom-seat: sha256 "),
            ("no helper beside the lever", tree_with(None, pin="0" * 64), stale,
             f"hcom-seat: {helper_name} unreadable beside this script: {tree_helper}", ""),
        )  # fmt: skip
        for label, arrange, config, message, detail in cases:
            with self.subTest(case=label):
                self.lever = test_hcom_seat.SEAT
                if agent.is_dir():
                    agent.chmod(0o700)
                shutil.rmtree(agent, ignore_errors=True)
                agent.mkdir(parents=True)
                if config is not None:
                    self.profile_config.write_text(config)
                arrange()
                run = self.launch("--", "--version")
                agent.chmod(0o700)
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertIn(message, run.stderr)
                if detail:
                    self.assertIn(detail, run.stderr)
                remaining = sorted(p.name for p in agent.iterdir())
                self.assertEqual(remaining, [] if config is None else ["config.yml"], "no temporary file remains")
                if config is not None:
                    self.assertEqual(self.profile_config.read_text(), config, "a refused launch replaces nothing")
                self.assertEqual(self.slots(), ([], []), "no per-launch slot remains after the refusal")
        self.assertEqual(self.dsh_calls(), [])

    def destination_swap_hook(self, extra=""):
        """The round-3 verdict's probe as a BASH_ENV DEBUG trap: right before the write command (the helper run here;
        `mv` of the held temporary at 792604f9) `config.yml` becomes a link to another profile's `agent/`."""
        hook = Path(self.temp.name) / "swap-destination.bash"
        hook.write_text(
            "set -T\n"
            "trap 'if [[ ${BASH_COMMAND} == *profile_config_cmd* || ${BASH_COMMAND} == */bin/mv\\ -f*config.yml* ]];"
            ' then if [[ ! -L ${U310_TARGET} ]]; then /bin/rm -f -- "${U310_TARGET}" &&'
            ' /bin/ln -s "${U310_OTHER}" "${U310_TARGET}" &&'
            ' echo "hook: swapped ${U310_TARGET} for a link to ${U310_OTHER}" >&2; fi;'
            f" {extra} fi' DEBUG\n"
        )
        return hook

    def test_a_destination_swapped_to_a_directory_link_before_the_write_is_refused_and_the_other_profile_untouched(
        self,
    ):
        """The round-3 verdict's P1 (`verdicts/U310c-792604f9.md`, hcom-seat:1057) as a test: a writer in `agent/`
        swaps `config.yml` for a link to another profile's `agent/` after the launcher's reading of it and before the
        act, and at 792604f9 the unsandboxed `mv` moved the config into `orchestrator/agent` and the launch returned 0.
        Now the helper's `O_NOFOLLOW` open of `config.yml` through its held descriptor refuses naming the link, the
        other profile keeps its one entry and its bytes, no temporary exists anywhere, no slot remains and no dsh
        starts; with no config and with a stale one."""
        home = self.home.resolve()
        agent = home / ".omp/profiles/dsh/agent"
        other = home / ".omp/profiles/orchestrator/agent"
        other.mkdir(parents=True)
        other_text = "modelRoles:\n  default: orchestrator/own\n"
        (other / "config.yml").write_text(other_text)
        hook = self.destination_swap_hook()
        for config in (None, "modelRoles:\n  default: stale/model\n"):
            with self.subTest(config="absent" if config is None else "stale"):
                shutil.rmtree(agent, ignore_errors=True)
                agent.mkdir(parents=True)
                if config is not None:
                    self.profile_config.write_text(config)
                run = self.launch("--", "--version", BASH_ENV=str(hook), U310_TARGET=str(self.profile_config),
                                  U310_OTHER=str(other))  # fmt: skip
                self.assertIn("hook: swapped", run.stderr, "the swap happened before the act")
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertIn(
                    f"the dsh profile config {self.profile_config} was not placed: profile-config-place: refused at"
                    f" open-config: {self.profile_config}: is a symbolic link; the dsh role writes its profile config"
                    " inside its profile only",
                    run.stderr,
                )
                self.assertEqual(
                    sorted(p.name for p in other.iterdir()), ["config.yml"], "the other profile is untouched"
                )
                self.assertEqual((other / "config.yml").read_text(), other_text)
                self.assertTrue(self.profile_config.is_symlink(), "the planted link stands, unfollowed")
                self.assertEqual(sorted(p.name for p in agent.iterdir()), ["config.yml"], "no temporary remains")
                self.assertEqual(self.slots(), ([], []), "no per-launch slot remains after the refusal")
        self.assertEqual(self.dsh_calls(), [])

    def test_a_source_and_destination_swap_places_nothing_of_the_attackers_in_the_other_profile(self):
        """The round-3 verdict's second full-fixture probe: at 792604f9 the temporary's path was the shell's `tmp_file`,
        so a trap swapped it for a file of attacker-chosen bytes and `config.yml` for a directory link right before
        `mv`, and the launch placed those bytes in `orchestrator/agent` and returned 0. Now the temporary's name never
        reaches the shell (the trap finds no `tmp_file` and no `.config.yml.*` entry to swap), attacker files planted
        at every guessable name stand unused, the destination swap refuses as before, and no file under the other
        profile holds the attacker's bytes."""
        home = self.home.resolve()
        agent = home / ".omp/profiles/dsh/agent"
        agent.mkdir(parents=True)
        other = home / ".omp/profiles/orchestrator/agent"
        other.mkdir(parents=True)
        (other / "config.yml").write_text("modelRoles:\n  default: orchestrator/own\n")
        attacker = "modelRoles:\n  default: attacker/model\n"
        planted = sorted([".config.yml.tmp", ".config.yml.0000000000000000", f"config.yml.tmp.{os.getpid()}"])
        for name in planted:
            (agent / name).write_text(attacker)
        hook = self.destination_swap_hook(
            'if [[ -n ${tmp_file:-} ]]; then /bin/rm -f -- "${tmp_file}" && printf "%s\\n" "${U310_ATTACK}" > "${tmp_file}"'
            ' && echo "hook: swapped the temporary ${tmp_file}" >&2; fi;'
            ' for e in "${U310_AGENT}"/.config.yml.*; do [[ -L ${e} || -f ${e} ]] || continue;'
            " if [[ ${e} == *.0000000000000000 || ${e} == *.tmp ]]; then continue; fi;"
            ' /bin/rm -f -- "${e}" && printf "%s\\n" "${U310_ATTACK}" > "${e}" && echo "hook: swapped the temporary ${e}" >&2; done;'
        )
        run = self.launch("--", "--version", BASH_ENV=str(hook), U310_TARGET=str(self.profile_config),
                          U310_OTHER=str(other), U310_AGENT=str(agent), U310_ATTACK=attacker)  # fmt: skip
        self.assertIn("hook: swapped", run.stderr, "the destination swap happened before the act")
        self.assertNotIn("hook: swapped the temporary", run.stderr, "no temporary was ever visible to the shell")
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertIn(f"refused at open-config: {self.profile_config}: is a symbolic link", run.stderr)
        self.assertEqual(sorted(p.name for p in other.iterdir()), ["config.yml"], "nothing landed in the other profile")
        self.assertNotIn("attacker", (other / "config.yml").read_text())
        self.assertEqual(sorted(p.name for p in agent.iterdir() if p.name != "config.yml"), planted)
        self.assertEqual(self.slots(), ([], []))
        self.assertEqual(self.dsh_calls(), [])

    def test_a_failed_umask_read_ends_no_launch_and_leaves_no_slot(self):
        """The round-3 verdict's third probe (P2 hcom-seat:1007): a `umask` whose read fails (status 7 with no argument,
        the set left working) ended the launch at 792604f9 with exit 7 through errexit and both per-launch slots
        behind. The write reads no mask any more (the helper creates its file 0600 through `O_CREAT` and `fchmod`):
        the launch places the config 0600 and ends with dsh's status, no slot behind; with a stale config too."""
        hook = Path(self.temp.name) / "umask-read-fails.bash"
        hook.write_text('umask() { if (($# == 0)); then return 7; fi; builtin umask "$@"; }\n')
        expected = placed_overlay(self.bridge)
        for config in (None, "modelRoles:\n  default: stale/model\n"):
            with self.subTest(config="absent" if config is None else "stale"):
                if config is not None:
                    self.profile_config.write_text(config)
                run = self.launch("--", "--version", BASH_ENV=str(hook))
                self.assertEqual((run.returncode, run.stdout), (0, "0.2.1-rc.5\n"), run.stderr)
                self.assertEqual(self.profile_config.read_text(), expected)
                self.assertEqual(stat.S_IMODE(self.profile_config.stat().st_mode), 0o600)
                self.assertEqual(sorted(p.name for p in self.profile_config.parent.iterdir()), ["config.yml"])
                self.assertEqual(self.slots(), ([], []), "no per-launch slot remains")
        self.assertEqual(len(self.dsh_calls()), 2)

    @unittest.skipIf(os.geteuid() == 0, "root reads a mode-000 file; the case needs an unreadable overlay")
    def test_an_unreadable_overlay_refuses_naming_it_on_linux_as_on_macos(self):
        """U310e: the CI failure of 28457a6a (run 42334203943, both Ubuntu legs): the overlay read was `$(< file)`,
        which bash 5.2 runs without a fork, so its failed redirection ended the launch by errexit with exit 1 and
        `line 1101: ...: Permission denied` before the `|| refuse` handler ran; macOS's bash 3.2 forks and the handler
        ran. The read is now `/bin/cat` with its status read: on both, exit 2 with the refusal naming the overlay, no
        bash error line, nothing created under HOME, no slot, no dsh; in a dry run too."""
        overlay = self.profiles / "dsh.yml"
        overlay.chmod(0)
        self.addCleanup(overlay.chmod, 0o644)
        for args in (["--dry-run"], []):
            with self.subTest(args=args):
                run = self.launch(*args, "--", "--version")
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertIn(f"hcom-seat: cannot read the profile config overlay {overlay}", run.stderr)
                self.assertNotIn(f"{self.lever}: line ", run.stderr, "no unhandled producer")
                self.assertFalse((self.home / ".omp").exists(), "nothing is made before the refusal")
                self.assertFalse((self.home / ".local/state/hcom-seat").exists())
                self.assertEqual(self.slots(), ([], []))
        self.assertEqual(self.dsh_calls(), [])

    def test_each_placement_producers_failure_refuses_naming_it_and_leaves_no_slot_or_temporary(self):
        """U310e (the round-4 verdict's P2 at hcom-seat:249, standing order 21): the four producers the round-4 head
        added to the placement, each injected to fail: the `sed` read of the helper's pin (a status 7 for the helper's
        pattern alone, the lever's own self-check untouched), the hash read of the helper (status 7 on the hash whose
        bytes are the helper's, helper_hash_hook; the lever's and regime-env's self-checks hash other bytes and pass),
        the `mkdir` of `agent/` (the profile directory made unwritable right before
        it, by a DEBUG trap) and the `umask` set of that subshell (status 7, armed by the same trap). Each: exit 2,
        nothing on stdout, the refusal naming the manifest, the helper or `agent/`, no `agent/` made, no slot behind,
        no dsh."""
        home = self.home.resolve()
        profile = home / ".omp/profiles/dsh"
        agent = profile / "agent"
        helper = test_hcom_seat.SEAT.parent / "profile-config-place.py"
        hooks = Path(self.temp.name) / "hooks"
        hooks.mkdir()
        helper_copy = test_hcom_seat.SEAT.parent / "profile-config-place.py"
        arm = 'case ${BASH_COMMAND} in *"/bin/mkdir \\"\\${agent}\\""*) %s ;; esac'
        hook_texts = {
            "sed": 'sed() { if [[ $* == *profile-config-place* ]]; then return 7; fi; command sed "$@"; }\n',
            "hash": helper_hash_hook("status=7"),
            "mkdir": "set -T\ntrap '" + arm % '/bin/chmod 0500 "${U310_PROFILE}"' + "' DEBUG\n",
            "umask": (
                "set -T\n"
                'umask() { if (($#)) && [[ -n ${U310_UMASK_FAILS:-} ]]; then return 7; fi; builtin umask "$@"; }\n'
                "trap '" + arm % "U310_UMASK_FAILS=1" + "' DEBUG\n"
            ),
        }
        cases = (
            ("the pin's sed read fails", "sed", "hcom-seat: cannot read ", "home/dot_agents/agent-config.yaml"),
            ("the helper's hash read fails", "hash", f"hcom-seat: cannot hash {helper}", ""),
            ("the mkdir of agent/ fails", "mkdir", f"hcom-seat: cannot create {agent}: ", "Permission denied"),
            ("the umask set fails", "umask",
             f"hcom-seat: cannot create {agent}: the umask set or the mkdir failed with no message", ""),
        )  # fmt: skip
        for label, name, message, detail in cases:
            with self.subTest(case=label):
                hook = hooks / f"{name}.bash"
                hook.write_text(hook_texts[name])
                try:
                    run = self.launch("--", "--version", BASH_ENV=str(hook), U310_HASH_TMP=str(hooks),
                                      U310_HELPER_PATH=str(helper_copy), U310_PROFILE=str(profile))  # fmt: skip
                finally:
                    if profile.is_dir():
                        profile.chmod(0o700)
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertIn(message, run.stderr)
                if detail:
                    self.assertIn(detail, run.stderr)
                self.assertFalse(agent.exists(), "no agent/ is made by a refused launch")
                self.assertEqual(self.slots(), ([], []), "no per-launch slot remains after the refusal")
                if name in ("mkdir", "umask"):
                    self.assertTrue(profile.is_dir(), "the refusal came after the profile directory was made")
                shutil.rmtree(home / ".omp", ignore_errors=True)
        self.assertEqual(self.dsh_calls(), [])

    def test_an_extension_path_holding_a_quote_and_a_trailing_space_is_placed_whole(self):
        """U310e (the round-4 verdict's P2 at hcom-seat:1117): the canonical extension path was written into the
        rendered YAML unquoted, so an allow-list entry resolving to a path with ` # ` placed a config whose extension
        was the part before the marker and the bridge route was lost while the launch returned 0. Each entry is now
        a single-quoted scalar with a `'` doubled: the bridge resolved through a link to a directory named with `'`
        and a trailing space lands whole, and PyYAML reads it back equal to the canonical path (a ` #` is refused by
        name since U310f, the control-character test below)."""
        real = Path(self.temp.name).resolve() / "bridge it's canonical "
        self.bridge.rename(real)
        self.bridge.symlink_to(real)
        run = self.launch("--", "--version")
        self.assertEqual((run.returncode, run.stdout), (0, "0.2.1-rc.5\n"), run.stderr)
        text = self.profile_config.read_text()
        self.assertEqual(text, placed_overlay(real))
        self.assertIn("  - '" + str(real).replace("'", "''") + "'\n", text)
        self.assertEqual(yaml_extensions(text), [str(real)])
        self.assertEqual(len(self.dsh_calls()), 1)

    def scratch_tree(self):
        """A copy of the lever under test laid out as the checkout is (its helper, regime-env and seat-login-preflight
        beside it, the manifest two levels up), so a test may rewrite the helper's entry without touching the tree it
        runs from; the pins hold, since the bytes are the same."""
        tree = Path(self.temp.name).resolve() / "tree"
        (tree / "scripts/orchestrator").mkdir(parents=True)
        (tree / "home/dot_agents").mkdir(parents=True)
        lever_dir = Path(self.lever).resolve().parent
        for name in ("hcom-seat", "regime-env", "seat-login-preflight", "profile-config-place.py"):
            shutil.copy2(lever_dir / name, tree / "scripts/orchestrator" / name)
        shutil.copy2(lever_dir.parent.parent / "home/dot_agents/agent-config.yaml", tree / "home/dot_agents")
        return tree

    def helper_copy_directories(self):
        """The entries of the lever's own `~/.local/state/hcom-seat` beside `tools`: the helper copy's per-launch
        directory while it exists (U310f), nothing once the launch has run or refused."""
        state = self.home / ".local/state/hcom-seat"
        return sorted(p.name for p in state.iterdir() if p.name != "tools") if state.is_dir() else []

    def test_a_helper_that_is_a_link_or_open_to_its_group_beside_the_lever_is_refused_before_it_is_read(self):
        """U310f (the round-5 verdict's P1 at hcom-seat:1273): at 384cd256 the lever hashed the helper's path and then
        executed the path, so a link at it whose target was replaced after the hash ran other Python. The path beside
        the lever is now held to the self-check's rules before anything reads it: a link there refuses by name even
        when its target holds the pinned bytes (the digest alone would pass), and so does a helper open to its group
        or to others; nothing is placed, no copy directory and no slot remains, no dsh starts, in a dry run too."""
        tree = self.scratch_tree()
        helper = tree / "scripts/orchestrator/profile-config-place.py"
        elsewhere = tree / "elsewhere"
        elsewhere.mkdir()
        target = elsewhere / "profile-config-place.py"
        helper.rename(target)
        helper.symlink_to(target)
        self.lever = tree / "scripts/orchestrator/hcom-seat"
        linked = (
            f"hcom-seat: profile-config-place.py beside this script is a symbolic link: {helper}; the helper runs from"
            " the lever's own directory only"
        )
        for args in (["--dry-run"], []):
            with self.subTest(case="a link at the helper's path", args=args):
                run = self.launch(*args, "--", "--version")
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertIn(linked, run.stderr)
                self.assertFalse(self.profile_config.exists(), "nothing is placed")
                self.assertEqual(self.helper_copy_directories(), [], "no copy directory remains")
                self.assertEqual(self.slots(), ([], []))
        helper.unlink()
        target.rename(helper)
        helper.chmod(0o664)
        with self.subTest(case="a helper open to its group"):
            run = self.launch("--", "--version")
            self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
            self.assertIn(
                "hcom-seat: profile-config-place.py beside this script is writable by its group or by others"
                f" (mode '664'): {helper}; the helper runs from the lever's own directory only",
                run.stderr,
            )
            self.assertFalse(self.profile_config.exists())
            self.assertEqual(self.helper_copy_directories(), [])
            self.assertEqual(self.slots(), ([], []))
        self.assertEqual(self.dsh_calls(), [])

    def test_the_helper_runs_from_the_levers_own_copy_so_a_rewrite_after_the_hash_runs_nothing(self):
        """U310f (the round-5 verdict's P1 at hcom-seat:1273, the hash-then-run window): the hash read is wrapped (the
        BASH_ENV form of the producer injections) so that right after the helper's digest is read, the helper's path
        beside the lever is replaced by a stand-in that writes a marker and prints `placed`. At 384cd256 the lever ran
        the path and the stand-in ran: the marker appeared, no config was placed and the launch returned 0. Now the
        path is read once, by the lever's copy in its own per-launch directory, the copy is what is hashed and what
        runs: the config lands from the pinned bytes, the marker never appears, the copy's directory is gone after
        the launch, and the rewrite of the path is measured to have happened (after the hash)."""
        tree = self.scratch_tree()
        helper = tree / "scripts/orchestrator/profile-config-place.py"
        self.lever = tree / "scripts/orchestrator/hcom-seat"
        scratch = Path(self.temp.name).resolve()
        marker = scratch / "ran-the-swapped-helper"
        swap_in = scratch / "swap-in.py"
        swap_text = f'open({str(marker)!r}, "w").write("ran")\nprint("placed")\n'
        swap_in.write_text(swap_text)
        hook = scratch / "swap-after-hash.bash"
        hook.write_text(helper_hash_hook('/bin/mv -f -- "${U310_SWAP_IN}" "${U310_HELPER_PATH}"'))
        run = self.launch("--", "--version", BASH_ENV=str(hook), U310_HASH_TMP=str(scratch),
                          U310_HELPER_PATH=str(helper), U310_SWAP_IN=str(swap_in))  # fmt: skip
        self.assertEqual((run.returncode, run.stdout), (0, "0.2.1-rc.5\n"), run.stderr)
        self.assertEqual(
            helper.read_text(), swap_text, "the path was rewritten right after the helper's digest was read"
        )
        self.assertFalse(marker.exists(), "the rewritten path never ran; the lever ran its own hashed copy")
        self.assertEqual(self.profile_config.read_text(), placed_overlay(self.bridge))
        self.assertIn(f"{self.profile_config} is absent; the launch places it from", run.stderr)
        self.assertEqual(self.helper_copy_directories(), [], "the copy's directory is removed once the helper ran")
        self.assertEqual(len(self.dsh_calls()), 1)
        self.assertEqual(self.slots(), ([], []))

    def test_an_extension_path_holding_a_control_character_or_a_comment_marker_is_refused_before_rendering(self):
        """U310f (the round-5 verdict's P2 at hcom-seat:1121): inside a single-quoted YAML scalar a line break folds
        into a space, so at 384cd256 an allow-list entry resolving to a directory named with a newline placed a config
        whose extension was another path while the launch returned 0. A canonical extension path holding a control
        character (a newline, a tab), a `#` after white space, or beginning with `-` is now refused by name before
        anything is rendered or made (nothing under `~/.omp` or `~/.local/state/hcom-seat`, no slot, no dsh), in a dry
        run too. A canonical path never begins with `-` (it is `pwd -P`), so that shape is held on the check itself,
        extracted from the lever's text with `refuse`."""
        root = Path(self.temp.name).resolve()
        current = self.bridge
        cases = (
            ("a newline", "bridge\ncanonical", "holds a control character"),
            ("a tab", "bridge\tcanonical", "holds a control character"),
            ("a comment marker after white space", "bridge # canonical", "holds a '#' after white space"),
        )
        for label, dirname, reason in cases:
            real = root / dirname
            current.rename(real)
            current = real
            if self.bridge.is_symlink():
                self.bridge.unlink()
            self.bridge.symlink_to(real)
            for args in (["--dry-run"], []):
                with self.subTest(case=label, args=args):
                    run = self.launch(*args, "--", "--version")
                    self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                    self.assertIn(
                        f"hcom-seat: the canonical extension path {reason} and is not rendered into the profile"
                        f" config: '{real}'",
                        run.stderr,
                    )
                    self.assertFalse((self.home / ".omp").exists(), "nothing is made before the refusal")
                    self.assertFalse((self.home / ".local/state/hcom-seat").exists())
                    self.assertEqual(self.slots(), ([], []))
        text = Path(self.lever).read_text()
        self.assertIn("rendered_path_check() {", text, "the lever carries the check")
        functions = "\n".join(
            text[text.index(f"{name}() {{") : text.index("\n}\n", text.index(f"{name}() {{")) + 3]
            for name in ("refuse", "rendered_path_check")
        )
        program = functions + "\nrendered_path_check 'the canonical extension path' \"$@\"\n"
        for label, path, expected in (
            ("a leading '-'", "-x/pi-claude-bridge", 2),
            ("a plain path", "/x/pi-claude-bridge", 0),
            ("a quote and a trailing space", "/x/bri'dge ", 0),
            ("a '#' without white space before it", "/x/bridge#1", 0),
        ):
            with self.subTest(case=label):
                run = subprocess.run(["/bin/bash", "-c", program, "_", path], env=self.env, capture_output=True,
                                     text=True, check=False)  # fmt: skip
                self.assertEqual(run.returncode, expected, run.stderr)
                if expected:
                    self.assertEqual(
                        run.stderr,
                        "hcom-seat: the canonical extension path begins with '-' and is not rendered into the"
                        f" profile config: '{path}'\n",
                    )
                else:
                    self.assertEqual(run.stderr, "")
        self.assertEqual(self.dsh_calls(), [])


if __name__ == "__main__":
    unittest.main()
