# U116 mise.lock evaluation (plan P-36, research V4-9)

Measured 2026-10-29 (UTC) with `mise 2026.10.19 macos-arm64 (2026-10-24)` on the macOS host, every mise command under a scratch HOME; the runs pasted below are the round-7 re-take of the same date, and round 8 (same date) re-took no run: it routed every printed string of every pasted script through one `redact` function and re-ran the injections, the scan and the forms check.

## Question

Should CI and the hosts install the versions one committed `mise.lock` records, instead of each resolving `latest` on its own clock? If yes, where would that lockfile live under chezmoi, given that `home/dot_mise/config.toml` is the global mise config and renders byte for byte to `~/.config/mise/config.toml`?

The plan row P-36 (`handoff/05-remediation-plan.md:116`) asks for a decisions row with the measured output of `mise lock --global --dry-run`. The earlier row of `decisions.tsv` (`2026-10-28T09:40:00Z`, phase `plan-P-36`) records "defer with a condition" and names `handoff/research/05-eval-mise-lock.md` as its evidence, a file the store does not hold. This file is that evidence, measured again under a scratch HOME so a reader can rerun it.

## Commands run

Every output below is pasted whole from the file the command wrote under `$TMPDIR/U116-out-5/`, the round-7 re-take of every run (the ROUND 7 AMENDMENT of the brief: the pasted runner is the one that ran, and it launches mise itself). One substitution applies to the three pasted `ls -la` blocks, because the store refuses the login name: the owner column reads `<user>`. Nothing else was edited; no other pasted output holds the login name or the home directory, because the runner writes the real mise paths in `~` form itself. `$TMPDIR` on this host is `/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/`; mise prints it through its `/private` alias. One block, marked as such, is older: the attempt-1 error of round 1, which round 7 did not repeat. Round 8 re-took no run: it added a `redact` function to every pasted script (every string that reaches stdout or stderr, refusals, receipts and exception texts included, passes through it; the real home directory in both its spellings becomes `~` and the login name `<user>`), after the round-7 audit found that the runner's `resolve_mise` printed a raw exception text holding a path under the real home (verdict P2 on `31be35ac`). The round-7 outputs under `U116-out-5/` stand: the only printed strings the change alters are diagnostics, and none of the pasted runs printed one (the resolved mise path was already written in `~` form; every other printed line is a receipt, a count or a `$TMPDIR` path). The injections, the scan and the forms check are re-run with the round-8 scripts and pasted from those runs.

### The scratch home and the config copy (CHANGE 1)

One `python3 -I` script, `/tmp/U116-prepare-7.py`, run from `/tmp` with the invocation below; the script as pasted is `/tmp/U116-prepare-8.py`, the round-7 script with the round-8 `redact` function and its four `print` sites (the refusal and three result lines) routed through it, nothing else, and it was not run again: it refuses when `U116-home-5` exists, and the three round-7 lines below hold no string `redact` changes. It refuses when `U116-home-5` or `U116-out-5` exists already (`os.lstat`, `FileNotFoundError` the one acceptable answer; neither existed), makes the four scratch directories and the output directory, copies the config in-process and writes the before listing of the real `~/.config/mise` to `real-before.txt` from one `subprocess.run` of `/bin/ls` whose status it reads and prints. Rounds 1 to 6 ran the four commands of CHANGE 1 under `bash`; this round runs no shell for them, so no wrapper word stands anywhere in the procedure. The script as pasted, the round-7 invocation and its printed output:

```python
#!/usr/bin/env python3
# U116 scratch home and config copy, round 7 (brief CHANGE 1), with the
# round-8 redact() on every printed string. One
# python3 -I process, no shell: the four directories are made and the
# config is copied in this process, and the before listing of the real
# ~/.config/mise is one subprocess.run of /bin/ls with its status read and
# its output written to real-before.txt. A scratch home or output
# directory that exists already is a refusal (this round wants fresh
# ones), decided by os.lstat raising FileNotFoundError; any other error
# anywhere is a refusal (exit 2) with its text, through redact().
import getpass
import os
import subprocess
import sys


def redactions():
    # The strings redact() replaces, longest first so a home path is
    # replaced before the login name inside it: the real home directory in
    # both spellings (the resolved path of ~, and HOME when it is set) as
    # ~, and the login name (getpass, and USER when it is set) as <user>.
    # The optional variables are read by membership and index, not by a
    # lookup with a default.
    homes = [os.path.realpath(os.path.expanduser("~"))]
    if "HOME" in os.environ:
        homes.append(os.environ["HOME"])
    users = [getpass.getuser()]
    if "USER" in os.environ:
        users.append(os.environ["USER"])
    pairs = [(home, "~") for home in homes if len(home) > 1] + [(user, "<user>") for user in users if user]
    pairs.sort(key=lambda pair: len(pair[0]), reverse=True)
    return tuple(dict.fromkeys(pairs))


REDACTIONS = redactions()


def redact(text):
    # Every string that reaches stdout or stderr passes through here,
    # refusals and receipts included.
    for literal, replacement in REDACTIONS:
        text = text.replace(literal, replacement)
    return text


def refuse(message):
    print(redact(f"prepare REFUSED: {message}"))
    sys.exit(2)


def require_env(name):
    try:
        return os.environ[name]
    except KeyError:
        refuse(f"{name} is unset")


TMPDIR = require_env("TMPDIR")
REAL_HOME = require_env("HOME")
SCRATCH = os.path.join(TMPDIR, "U116-home-5")
OUT = os.path.join(TMPDIR, "U116-out-5")
SOURCE = "/tmp/dotfiles-wt/U116/home/dot_mise/config.toml"
REAL_MISE_DIR = os.path.join(REAL_HOME, ".config", "mise")
SUBDIRS = (".config/mise", ".local/share", ".cache", ".local/state")


def main():
    for path in (SCRATCH, OUT):
        try:
            os.lstat(path)
        except FileNotFoundError:
            continue
        refuse(f"$TMPDIR/{os.path.basename(path)} exists already")
    for subdir in SUBDIRS:
        os.makedirs(os.path.join(SCRATCH, subdir))
    os.makedirs(OUT)
    print(redact("mkdir: $TMPDIR/U116-home-5 (.config/mise .local/share .cache .local/state) and $TMPDIR/U116-out-5"))
    with open(SOURCE, "rb") as source:
        data = source.read()
    with open(os.path.join(SCRATCH, ".config", "mise", "config.toml"), "wb") as target:
        target.write(data)
    print(redact(f"copy: {len(data)} bytes to $TMPDIR/U116-home-5/.config/mise/config.toml"))
    with open(os.path.join(OUT, "real-before.txt"), "wb") as handle:
        proc = subprocess.run(
            ["/bin/ls", "-la", REAL_MISE_DIR],
            stdout=handle,
            stderr=subprocess.STDOUT,
            check=False,
            timeout=60,
        )
    print(redact(f"ls-before: /bin/ls -la ~/.config/mise exit={proc.returncode} to $TMPDIR/U116-out-5/real-before.txt"))
    sys.exit(1 if proc.returncode else 0)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # any raised step is a refusal
        refuse(f"{type(exc).__name__}: {exc}")
```

```sh
cd /tmp
python3 -I /tmp/U116-prepare-7.py > /tmp/U116-round7/prepare.txt 2>&1; echo "prepare-exit=$?"
```

```text
prepare-exit=0
mkdir: $TMPDIR/U116-home-5 (.config/mise .local/share .cache .local/state) and $TMPDIR/U116-out-5
copy: 6962 bytes to $TMPDIR/U116-home-5/.config/mise/config.toml
ls-before: /bin/ls -la ~/.config/mise exit=0 to $TMPDIR/U116-out-5/real-before.txt
```

`/bin/ls -la ~/.config/mise` before, `real-before.txt`:

```text
total 16
drwxr-xr-x   3 <user>  staff    96 Oct 26 23:40 .
drwxr-xr-x  24 <user>  staff   768 Oct 16 17:44 ..
-rw-r--r--@  1 <user>  staff  6962 Oct 26 23:40 config.toml
```

### The runner

Every mise command of the pasted run went through the `python3 -I` script `/tmp/U116-run-7.py`; the script pasted below is `/tmp/U116-run-8.py`, the same script with the round-8 `redact` function in place of its `tilde` helper and every `print` site routed through it (the `diff` between the two is the `redact` block, the removed `tilde`, three comments and the twelve lines that print or refuse). It launches mise itself. The binary is resolved once, at the top of the script, by `resolve_mise`: a lookup over the entries of `PATH` that asks `os.lstat` for `<entry>/mise`, moves to the next entry on `FileNotFoundError` alone, refuses on any other `OSError` with its text, and refuses naming mise when no entry holds one. It does not test the executable bit: a mise that cannot be executed is left to the launch, which raises `PermissionError`. Each call is `subprocess.run([mise, ...], env=ENV, timeout=900, check=False, stdout=<the output file>, stderr=subprocess.STDOUT)`, where `ENV` is a dict holding exactly the variables of CHANGE 1 (`HOME`, `PATH`, `TMPDIR`, the four XDG variables and `MISE_TRUSTED_CONFIG_PATHS`) and nothing else, so the deadline and the environment belong to the process that reads the status. A launch that raises, be it `subprocess.TimeoutExpired`, `FileNotFoundError`, `PermissionError` or any other `OSError`, first writes a receipt reading `exit=refused`, then refuses (exit 2) with the error's class and text; a launch that returns writes its return code into the receipt. The start and end stamps and the elapsed seconds come from the `datetime` and `time` modules, and every receipt (`<name>.receipt.txt`) is written, read back and printed from the read-back bytes (an empty receipt is a refusal). Rounds 1 to 6 started every mise call through the brief's `env -i … perl -e 'alarm 900; exec @ARGV' mise …` form; when `exec` fails, because mise is absent or not executable, perl falls through its one-line program and exits 0, so that runner would have recorded a success for a command that never ran (verdict P2 on `a3efa54a`). The wrapper words left the argv list of the round-6 script as committed at `a3efa54a`: `/usr/bin/env` with `-i` at its lines 169 and 170, and `perl` with `-e` and `alarm 900; exec @ARGV` at lines 179 to 181; the first set of injections below shows the three ways the launch now refuses instead. Everything else stands from round 6: no command substitution, no process substitution, no pipeline, no predicate that turns a failed read into an absence (every file question is asked of `os.lstat` or `open`, `FileNotFoundError` alone means absence, any other `OSError` is a refusal with its text, `TMPDIR`, `PATH` and `HOME` are read by index with a missing variable a refusal, and the scratch-tree walk passes an `onerror` that raises); a non-zero exit or a lockfile that appears is exit 1 after every receipt is written. Every string that reaches stdout or stderr passes through `redact`: `refuse` calls it, the receipt line and every other `print` call it, and an exception's text is formatted into the refusal message and so passes through it. `redact` replaces the real home directory, in both its spellings (`os.path.realpath(os.path.expanduser('~'))` and `HOME` when set), with `~` and the login name (`getpass.getuser()` and `USER` when set) with `<user>`, longest string first; the optional variables are read by membership and index, not by a lookup with a default, so the forms check's second count stays 0. The round-7 `tilde` helper covered the candidate path of `resolve_mise` and the launch error's text, but not the exception text of a refused `os.lstat` in that lookup, which names the same path again, so a `PermissionError` there printed a path under the real home (verdict P2 on `31be35ac`); the second injection section below shows that refusal now. Its cwd is the scratch home (the attempt-1 lesson below). The script as pasted, the round-7 invocation from `/tmp` and its printed output, which is the receipt of every run (none of its lines holds a string `redact` changes; the resolved mise path was written in `~` form by `tilde`, as `redact` writes it in the injection runs below):

```python
#!/usr/bin/env python3
# U116 dry runs under the scratch HOME, round 8 (brief CHANGE 1 and 2; the
# ROUND 5 to ROUND 7 amendments; round 8 adds redact()). One python3 -I
# process that launches mise itself. The mise binary is resolved once, below, from PATH by a
# lookup that refuses when no entry holds it; every call is
# subprocess.run([mise, ...]) with the variable set of CHANGE 1 as its
# whole environment, timeout=900, check=False and the output file as
# stdout (stderr merged), so the deadline and the environment belong to
# this process and no wrapper stands between it and mise. A launch that
# raises (TimeoutExpired, FileNotFoundError, PermissionError or any other
# OSError) first gets a receipt reading exit=refused, then is a refusal
# (exit 2) with the error's text; a launch that returns gets its
# returncode in the receipt. Every receipt is written, read back and
# printed from the read-back bytes. Every file question is asked of
# os.lstat or open: FileNotFoundError alone means absence, any other
# OSError is a refusal with its text. Every string that reaches stdout or
# stderr, refusals, receipts and exception texts included, passes through
# redact(): the real home directory becomes ~ and the login name <user>.
import datetime
import getpass
import os
import stat
import subprocess
import sys
import time


def redactions():
    # The strings redact() replaces, longest first so a home path is
    # replaced before the login name inside it: the real home directory in
    # both spellings (the resolved path of ~, and HOME when it is set) as
    # ~, and the login name (getpass, and USER when it is set) as <user>.
    # The optional variables are read by membership and index, not by a
    # lookup with a default.
    homes = [os.path.realpath(os.path.expanduser("~"))]
    if "HOME" in os.environ:
        homes.append(os.environ["HOME"])
    users = [getpass.getuser()]
    if "USER" in os.environ:
        users.append(os.environ["USER"])
    pairs = [(home, "~") for home in homes if len(home) > 1] + [(user, "<user>") for user in users if user]
    pairs.sort(key=lambda pair: len(pair[0]), reverse=True)
    return tuple(dict.fromkeys(pairs))


REDACTIONS = redactions()


def redact(text):
    # Every string that reaches stdout or stderr passes through here,
    # refusals and receipts included.
    for literal, replacement in REDACTIONS:
        text = text.replace(literal, replacement)
    return text


def refuse(message):
    print(redact(f"run REFUSED: {message}"))
    sys.exit(2)


def require_env(name):
    # A missing variable is a refusal, not a default.
    try:
        return os.environ[name]
    except KeyError:
        refuse(f"{name} is unset")


TMPDIR = require_env("TMPDIR")
PATH = require_env("PATH")
REAL_HOME = require_env("HOME")
SCRATCH = os.path.join(TMPDIR, "U116-home-5")
OUT = os.path.join(TMPDIR, "U116-out-5")
CONFIG = os.path.join(SCRATCH, ".config", "mise", "config.toml")
LOCK = os.path.join(SCRATCH, ".config", "mise", "mise.lock")
PLATFORMS = "linux-x64,linux-arm64,macos-x64,macos-arm64"
TIMEOUT = 900

# The whole environment of every call: the variable set of CHANGE 1 and
# nothing else (no inherited variable reaches mise).
ENV = {
    "HOME": SCRATCH,
    "PATH": PATH,
    "TMPDIR": TMPDIR,
    "XDG_CONFIG_HOME": os.path.join(SCRATCH, ".config"),
    "XDG_DATA_HOME": os.path.join(SCRATCH, ".local", "share"),
    "XDG_CACHE_HOME": os.path.join(SCRATCH, ".cache"),
    "XDG_STATE_HOME": os.path.join(SCRATCH, ".local", "state"),
    "MISE_TRUSTED_CONFIG_PATHS": CONFIG,
}

# The runs of CHANGE 2 (a) to (f), plus the first eight lines of
# `mise lock --help` that CHANGE 1 asks for; each output file is pasted whole.
RUNS = (
    ("a-version", ["--version"]),
    ("help-lock", ["lock", "--help"]),
    ("b-lock-dry-run", ["lock", "--global", "--dry-run"]),
    ("c-lock-dry-run-4-platforms", ["lock", "--global", "--dry-run", "--platform", PLATFORMS]),
    ("d-lock-bump-json", ["lock", "--global", "--dry-run", "--bump", "--json"]),
    ("e-npm-package-manager", ["settings", "get", "npm.package_manager"]),
    ("f-minimum-release-age", ["settings", "get", "minimum_release_age"]),
)

# The real mise directories whose modification times are read before and
# after the runs; written in this form, never expanded, so no home path
# reaches the output.
REAL_DIRS = (
    "~/.config/mise",
    "~/.local/share/mise",
    "~/.cache/mise",
    "~/.local/state/mise",
    "~/Library/Caches/mise",
)


def real(path):
    # ~/x in REAL_DIRS to the real path, by the HOME read above.
    return os.path.join(REAL_HOME, path[2:])


def resolve_mise(path):
    # The first PATH entry holding a `mise`, asked of os.lstat entry by
    # entry: FileNotFoundError moves to the next entry, any other OSError
    # is a refusal with its text, and no entry at all is a refusal naming
    # mise. The executable bit is not tested here: a mise that cannot be
    # executed is left for the launch to raise PermissionError, which is a
    # refusal with that text. Both the refusal and the resolved path print
    # through redact() (verdict P2 on 31be35ac: the raw exception text
    # named a path under the real home).
    entries = [entry for entry in path.split(os.pathsep) if entry]
    for number, entry in enumerate(entries, 1):
        candidate = os.path.join(entry, "mise")
        try:
            os.lstat(candidate)
        except FileNotFoundError:
            continue
        except OSError as exc:
            refuse(f"cannot read {candidate}: {exc}")
        print(redact(f"mise={candidate} (PATH entry {number} of {len(entries)})"))
        return candidate
    refuse(f"mise not found on PATH ({len(entries)} entries searched)")


MISE = resolve_mise(PATH)


def mise_argv(args):
    return [MISE, *args]


def stamp():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def write(name, data):
    path = os.path.join(OUT, name)
    with open(path, "wb") as handle:
        handle.write(data if isinstance(data, bytes) else data.encode())


def read_back(name):
    # The receipt is printed from these bytes, not from the variables that
    # wrote it; an unreadable receipt raises, an empty one is a refusal.
    with open(os.path.join(OUT, name), "rb") as handle:
        data = handle.read()
    if not data.strip():
        refuse(f"{name} is empty after it was written")
    return data.decode().rstrip("\n")


def require_file(path, hint):
    # open proves the file is there and readable; absence and any other
    # error are both refusals, told apart by their text.
    try:
        with open(path, "rb") as handle:
            handle.read(1)
    except FileNotFoundError:
        refuse(f"{path} is missing; {hint}")
    except OSError as exc:
        refuse(f"cannot read {path}: {exc}")


def require_dir(path, hint):
    try:
        mode = os.lstat(path).st_mode
    except FileNotFoundError:
        refuse(f"{path} is missing; {hint}")
    except OSError as exc:
        refuse(f"cannot read {path}: {exc}")
    if not stat.S_ISDIR(mode):
        refuse(f"{path} is not a directory")


def raise_error(exc):
    # os.walk ignores a directory it cannot read unless told otherwise.
    raise exc


def receipt(name, start, began, status):
    elapsed = round(time.monotonic() - began)
    write(f"{name}.receipt.txt", f"start={start} end={stamp()} elapsed={elapsed}s exit={status}\n")
    print(redact(f"{name}: {read_back(f'{name}.receipt.txt')}"))


def timed(name, argv, timeout=TIMEOUT):
    # Runs argv with ENV as its whole environment, stdout and stderr to
    # <name>.txt, writes and prints <name>.receipt.txt, returns the exit
    # status. A launch that raises, be it TimeoutExpired,
    # FileNotFoundError, PermissionError or any other OSError, writes
    # exit=refused into the receipt first and then refuses with the
    # error's class and text.
    start = stamp()
    began = time.monotonic()
    try:
        with open(os.path.join(OUT, f"{name}.txt"), "wb") as handle:
            proc = subprocess.run(
                argv,
                env=ENV,
                timeout=timeout,
                check=False,
                stdout=handle,
                stderr=subprocess.STDOUT,
            )
    except (subprocess.TimeoutExpired, OSError) as exc:
        receipt(name, start, began, "refused")
        refuse(f"{name} did not complete: {type(exc).__name__}: {exc}")
    receipt(name, start, began, proc.returncode)
    return proc.returncode


def real_mtimes(name):
    lines = []
    for directory in REAL_DIRS:
        try:
            mtime = os.lstat(real(directory)).st_mtime
        except FileNotFoundError:
            lines.append(f"missing {directory}")
            continue
        when = datetime.datetime.fromtimestamp(mtime).strftime("%Y-%m-%dT%H:%M:%S")
        lines.append(f"{when} {directory}")
    write(name, "\n".join(lines) + "\n")


def scratch_tree(name, depth=4):
    lines = []
    for root, dirs, files in os.walk(SCRATCH, onerror=raise_error):
        rel = os.path.relpath(root, SCRATCH)
        level = 0 if rel == "." else rel.count(os.sep) + 1
        if level >= depth:
            dirs[:] = []
        prefix = "$TMPDIR/U116-home-5" if rel == "." else f"$TMPDIR/U116-home-5/{rel}"
        lines.append(prefix)
        for entry in files:
            lines.append(f"{prefix}/{entry}")
    lines.sort()
    write(name, "\n".join(lines) + "\n")


def check_lock():
    # The none-written check. os.lstat on the lockfile path: absent only
    # when it raises FileNotFoundError; any other error is a refusal with
    # its text; a result means a lockfile was written. Returns the failure
    # count for the summary line.
    try:
        os.lstat(LOCK)
    except FileNotFoundError:
        write("g-none-written.txt", "none-written\n")
        print(redact("g-none-written: none-written"))
        return 0
    except OSError as exc:
        refuse(f"cannot read {LOCK}: {exc}")
    write("g-none-written.txt", "WRITTEN\n")
    print(redact("g-none-written: WRITTEN"))
    return 1


def main():
    require_file(CONFIG, "run the CHANGE 1 preparation first")
    require_dir(OUT, "run the CHANGE 1 preparation first")
    # The cwd sits inside the scratch home: with a cwd under the real home,
    # mise's parent-directory walk reads the real ~/.config/mise/config.toml
    # as a project config (round 1, attempt 1).
    os.chdir(SCRATCH)
    print(redact("cwd=$TMPDIR/U116-home-5"))
    real_mtimes("real-dirs-mtime-before.txt")
    failed = 0
    for name, args in RUNS:
        if timed(name, mise_argv(args)) != 0:
            failed += 1
    for name, path in (("g-scratch-after", os.path.join(SCRATCH, ".config", "mise")), ("g-real-after", real("~/.config/mise"))):
        if timed(name, ["/bin/ls", "-la", path]) != 0:
            failed += 1
    failed += check_lock()
    real_mtimes("real-dirs-mtime-after.txt")
    scratch_tree("scratch-tree.txt")
    print(redact(f"runs={len(RUNS) + 2} failed={failed}"))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # any raised step is a refusal, never a summary line
        refuse(f"{type(exc).__name__}: {exc}")
```

```sh
cd /tmp
python3 -I /tmp/U116-run-7.py > /tmp/U116-round7/run.txt 2>&1; echo "run-exit=$?"
```

```text
run-exit=0
mise=~/.local/bin/mise (PATH entry 51 of 55)
cwd=$TMPDIR/U116-home-5
a-version: start=2026-10-29T13:23:49Z end=2026-10-29T13:23:50Z elapsed=0s exit=0
help-lock: start=2026-10-29T13:23:50Z end=2026-10-29T13:23:50Z elapsed=0s exit=0
b-lock-dry-run: start=2026-10-29T13:23:50Z end=2026-10-29T13:23:52Z elapsed=2s exit=0
c-lock-dry-run-4-platforms: start=2026-10-29T13:23:52Z end=2026-10-29T13:23:52Z elapsed=0s exit=0
d-lock-bump-json: start=2026-10-29T13:23:52Z end=2026-10-29T13:23:52Z elapsed=0s exit=0
e-npm-package-manager: start=2026-10-29T13:23:52Z end=2026-10-29T13:23:52Z elapsed=0s exit=0
f-minimum-release-age: start=2026-10-29T13:23:52Z end=2026-10-29T13:23:52Z elapsed=0s exit=0
g-scratch-after: start=2026-10-29T13:23:52Z end=2026-10-29T13:23:52Z elapsed=0s exit=0
g-real-after: start=2026-10-29T13:23:52Z end=2026-10-29T13:23:52Z elapsed=0s exit=0
g-none-written: none-written
runs=9 failed=0
```

### Injected failures into the runner's mise lookup and launch

In memory, as the ROUND 7 AMENDMENT asks, re-run in round 8 against the round-8 runner: `/tmp/U116-inject-8.py` (the round-7 script with the runner path and its directories renamed and its two printed lines routed through `redact`, nothing else) sets `PATH` in its own process, then loads `/tmp/U116-run-8.py` above as a module, so the runner's own `resolve_mise` runs against that `PATH`; for the two fake cases it points the runner's output directory at `/tmp/U116-inject-8-out` (so nothing lands in `U116-out-5`) and calls the runner's `timed` on `mise --version`. The fakes are written by the injection script itself with `open` and `os.chmod`, a `mise` that sleeps for 30 s with the executable bit set and a `mise` without the executable bit; the real mise is never touched. The script catches nothing, so the process exit status is the runner's own and the shell line after each call is its exit line. First, a `PATH` of one empty directory: the lookup refuses before any receipt exists. Second, the sleeping fake first on `PATH` under `timeout=2`: the receipt reads `exit=refused`, then the refusal carries `TimeoutExpired` and its text. Third, the fake without the executable bit first on `PATH`: the lookup finds it (it tests presence, not mode), the launch raises `PermissionError`, the receipt reads `exit=refused`, then the refusal carries that text. No receipt of these three runs reads `exit=0`; under the round-6 form the second and third cases were perl exiting 0 after a failed `exec`. Every line of the three outputs passed through `redact`; none held a string it changes, so they read as in round 7 apart from the round-8 directory names and the stamps. The script, the three commands from `/tmp`, and their outputs in that order:

```python
#!/usr/bin/env python3
# In-memory injections into the round-8 runner's mise lookup and launch
# (the ROUND 7 AMENDMENT, re-run in round 8). Sets PATH in this process,
# then loads /tmp/U116-run-8.py as a module so the runner's own resolve_mise runs
# against that PATH; for the two fake cases, points the runner's output
# directory at a scratch directory (nothing lands in U116-out-5) and calls
# its timed function on `mise --version`, with timeout=2 for the sleeping
# fake. The fakes are written here by open and os.chmod; the real mise is
# never touched. No exception is caught: the process exit status is the
# runner's own, a refusal exits 2, and a timed call that returns is
# reported and exits 1, so the shell line after each call is its exit
# line. Its own two printed lines pass through redact() too.
import getpass
import importlib.util
import os
import sys

RUNNER = "/tmp/U116-run-8.py"
OUT = "/tmp/U116-inject-8-out"
EMPTY = "/tmp/U116-inject-8-empty"
FAKES = {
    "sleep": ("/tmp/U116-inject-8-sleep", b"#!/bin/sh\nexec sleep 30\n", 0o755),
    "noexec": ("/tmp/U116-inject-8-noexec", b"#!/bin/sh\nexit 0\n", 0o644),
}


def redactions():
    # The strings redact() replaces, longest first so a home path is
    # replaced before the login name inside it: the real home directory in
    # both spellings (the resolved path of ~, and HOME when it is set) as
    # ~, and the login name (getpass, and USER when it is set) as <user>.
    # The optional variables are read by membership and index, not by a
    # lookup with a default.
    homes = [os.path.realpath(os.path.expanduser("~"))]
    if "HOME" in os.environ:
        homes.append(os.environ["HOME"])
    users = [getpass.getuser()]
    if "USER" in os.environ:
        users.append(os.environ["USER"])
    pairs = [(home, "~") for home in homes if len(home) > 1] + [(user, "<user>") for user in users if user]
    pairs.sort(key=lambda pair: len(pair[0]), reverse=True)
    return tuple(dict.fromkeys(pairs))


REDACTIONS = redactions()


def redact(text):
    # Every string that reaches stdout or stderr passes through here,
    # refusals and receipts included.
    for literal, replacement in REDACTIONS:
        text = text.replace(literal, replacement)
    return text

case = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
os.makedirs(EMPTY, exist_ok=True)
if case == "no-mise":
    os.environ["PATH"] = EMPTY
else:
    directory, body, mode = FAKES[case]
    os.makedirs(directory, exist_ok=True)
    fake = os.path.join(directory, "mise")
    with open(fake, "wb") as handle:
        handle.write(body)
    os.chmod(fake, mode)
    os.environ["PATH"] = directory + os.pathsep + os.environ["PATH"]
print(redact(f"case {case}: PATH starts with {os.environ['PATH'].split(os.pathsep)[0]}"))
spec = importlib.util.spec_from_file_location("runner", RUNNER)
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)  # resolve_mise runs here; no-mise refuses inside
runner.OUT = OUT
deadline = 2 if case == "sleep" else runner.TIMEOUT
code = runner.timed(f"inject-{case}", runner.mise_argv(["--version"]), timeout=deadline)
print(redact(f"inject-{case} returned exit {code}: the launch did not refuse"))
sys.exit(1)
```

```sh
python3 -I /tmp/U116-inject-8.py no-mise; echo "exit=$?"
python3 -I /tmp/U116-inject-8.py sleep; echo "exit=$?"
python3 -I /tmp/U116-inject-8.py noexec; echo "exit=$?"
```

```text
case no-mise: PATH starts with /tmp/U116-inject-8-empty
run REFUSED: mise not found on PATH (1 entries searched)
exit=2
case sleep: PATH starts with /tmp/U116-inject-8-sleep
mise=/tmp/U116-inject-8-sleep/mise (PATH entry 1 of 56)
inject-sleep: start=2026-10-29T13:53:45Z end=2026-10-29T13:53:47Z elapsed=2s exit=refused
run REFUSED: inject-sleep did not complete: TimeoutExpired: Command '['/tmp/U116-inject-8-sleep/mise', '--version']' timed out after 2 seconds
exit=2
case noexec: PATH starts with /tmp/U116-inject-8-noexec
mise=/tmp/U116-inject-8-noexec/mise (PATH entry 1 of 56)
inject-noexec: start=2026-10-29T13:53:48Z end=2026-10-29T13:53:48Z elapsed=0s exit=refused
run REFUSED: inject-noexec did not complete: PermissionError: [Errno 13] Permission denied: '/tmp/U116-inject-8-noexec/mise'
exit=2
```

### Injected failure into the runner's mise lookup: a refused `os.lstat` under the real home (round 8)

The round-7 audit injected a `PermissionError` into the `os.lstat` of `resolve_mise` and read a path under the real home in the refusal (verdict P2 on `31be35ac`): `tilde` rewrote the candidate path in the message, but the exception's own text names the same path again and reached the output raw. In memory: `/tmp/U116-inject-8-lookup.py` builds, from the real home string of its own process, a `PATH` whose first entry is `<real home>/bin`, replaces `os.lstat` so that the one path `<real home>/bin/mise` raises `PermissionError(13, 'Permission denied', <that path>)` and every other path is answered as before, then loads `/tmp/U116-run-8.py` above as a module, so the runner's own `resolve_mise` meets the error on its first entry. Nothing on disk is touched; the real home string is never written into any file by this script. The script catches nothing, so the exit status is the runner's own. The refusal names `~/bin/mise` twice, once from the message and once from the exception text, and the real home nowhere; the script's own first line passes through its own `redact` the same way. The script, the command from `/tmp` (its output to a file, so the scan can count over the text), the exit line and then the file:

```python
#!/usr/bin/env python3
# In-memory injection into the round-8 runner's mise lookup (verdict P2 on
# 31be35ac). Builds, from the real home string of this process, a PATH
# whose first entry is <real home>/bin, replaces os.lstat so that the one
# path <real home>/bin/mise raises PermissionError(13, 'Permission
# denied', <that path>) and every other path is answered as before, then
# loads /tmp/U116-run-8.py as a module, so the runner's own resolve_mise
# meets the error on its first entry. Nothing on disk is touched; the real
# home string reaches this process's output only through the runner's
# redact() (the refusal) and this script's redact() (its own first line).
# No exception is caught: the process exit status is the runner's own, a
# refusal exits 2, and a lookup that returns is reported and exits 1, so
# the shell line after the call is its exit line.
import getpass
import importlib.util
import os
import sys

RUNNER = "/tmp/U116-run-8.py"
HOME = os.environ["HOME"]
ENTRY = os.path.join(HOME, "bin")
BLOCKED = os.path.join(ENTRY, "mise")


def redactions():
    # The strings redact() replaces, longest first so a home path is
    # replaced before the login name inside it: the real home directory in
    # both spellings (the resolved path of ~, and HOME when it is set) as
    # ~, and the login name (getpass, and USER when it is set) as <user>.
    # The optional variables are read by membership and index, not by a
    # lookup with a default.
    homes = [os.path.realpath(os.path.expanduser("~"))]
    if "HOME" in os.environ:
        homes.append(os.environ["HOME"])
    users = [getpass.getuser()]
    if "USER" in os.environ:
        users.append(os.environ["USER"])
    pairs = [(home, "~") for home in homes if len(home) > 1] + [(user, "<user>") for user in users if user]
    pairs.sort(key=lambda pair: len(pair[0]), reverse=True)
    return tuple(dict.fromkeys(pairs))


REDACTIONS = redactions()


def redact(text):
    # Every string that reaches stdout or stderr passes through here,
    # refusals and receipts included.
    for literal, replacement in REDACTIONS:
        text = text.replace(literal, replacement)
    return text


real_lstat = os.lstat


def injected_lstat(path, *args, **kwargs):
    if path == BLOCKED:
        raise PermissionError(13, "Permission denied", path)
    return real_lstat(path, *args, **kwargs)


os.lstat = injected_lstat
os.environ["PATH"] = ENTRY + os.pathsep + os.environ["PATH"]
print(redact(f"case lookup-permission: PATH starts with {ENTRY}; os.lstat of {BLOCKED} raises PermissionError"))
spec = importlib.util.spec_from_file_location("runner", RUNNER)
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)  # resolve_mise runs here and meets the error on entry 1
print(redact(f"resolve_mise returned {runner.MISE}: the lookup did not refuse"))
sys.exit(1)
```

```sh
cd /tmp
python3 -I /tmp/U116-inject-8-lookup.py > /tmp/U116-round8/inject-lookup.txt 2>&1; echo "exit=$?"
```

```text
exit=2
case lookup-permission: PATH starts with ~/bin; os.lstat of ~/bin/mise raises PermissionError
run REFUSED: cannot read ~/bin/mise: [Errno 13] Permission denied: '~/bin/mise'
```

The scan's `redact` class over that file: a copy of `/tmp/U116-scan.py` (the script under Redaction and credential scan below) with the PR body's entry in `DOCUMENTS` replaced by the file, `sed 's|^    "/tmp/dotfiles-wt/U116-pr-body.md",$|    "/tmp/U116-round8/inject-lookup.txt",|' /tmp/U116-scan.py > /tmp/U116-scan-lookup.py; diff /tmp/U116-scan.py /tmp/U116-scan-lookup.py; python3 -I /tmp/U116-scan-lookup.py; echo "exit=$?"` from the worktree, counts `token=0 redact=0` over it; the login name is one of the five words of the redact list, so a path under the real home would count:

```text
35c35
<     "/tmp/dotfiles-wt/U116-pr-body.md",
---
>     "/tmp/U116-round8/inject-lookup.txt",
token from gh auth token patterns=1
redact list ~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/redact-words.txt patterns=5
U116-out-5/a-version.receipt.txt token=0
U116-out-5/a-version.txt token=0
U116-out-5/b-lock-dry-run.receipt.txt token=0
U116-out-5/b-lock-dry-run.txt token=0
U116-out-5/c-lock-dry-run-4-platforms.receipt.txt token=0
U116-out-5/c-lock-dry-run-4-platforms.txt token=0
U116-out-5/d-lock-bump-json.receipt.txt token=0
U116-out-5/d-lock-bump-json.txt token=0
U116-out-5/e-npm-package-manager.receipt.txt token=0
U116-out-5/e-npm-package-manager.txt token=0
U116-out-5/f-minimum-release-age.receipt.txt token=0
U116-out-5/f-minimum-release-age.txt token=0
U116-out-5/g-none-written.txt token=0
U116-out-5/g-real-after.receipt.txt token=0
U116-out-5/g-real-after.txt token=0
U116-out-5/g-scratch-after.receipt.txt token=0
U116-out-5/g-scratch-after.txt token=0
U116-out-5/help-lock.receipt.txt token=0
U116-out-5/help-lock.txt token=0
U116-out-5/real-before.txt token=0
U116-out-5/real-dirs-mtime-after.txt token=0
U116-out-5/real-dirs-mtime-before.txt token=0
U116-out-5/scratch-tree.txt token=0
/tmp/dotfiles-wt/U116/.orchestration/orchestrate/regime-cutover/handoff/evaluations/U116-mise-lock.md token=0 redact=0
/tmp/U116-round8/inject-lookup.txt token=0 redact=0
scan clean (25 files, 0 matches)
exit=0
```

### Injected failures into the runner's none-written check

In memory, as the ROUND 6 AMENDMENT asks, re-run against the round-8 runner: `/tmp/U116-inject-8-lock.py` (the round-6 script with the runner path and its output directory changed and its one printed line routed through `redact`, nothing else) loads `/tmp/U116-run-8.py` above as a module, points its output directory at `/tmp/U116-inject-8-lock-out` (so nothing lands in `U116-out-5`), replaces `os.lstat` for the lockfile path alone and calls `check_lock`. The injection script catches nothing, so the process exit status is the check's own and the shell line after each call is its exit line; the first printed line of each run is the runner's own resolution of mise at module load. First, `os.lstat` raises `PermissionError`: the check refuses with the error's text and exits `2` instead of writing `none-written` (the round-5 script printed `none-written` and exited 0 here). Second, it raises `FileNotFoundError`: the check writes and prints `none-written` and returns 0. Third, the positive control, it returns a stat result (the runner file's own): the check prints `WRITTEN` and returns 1. The script, the three commands from `/tmp`, and their outputs in that order:

```python
#!/usr/bin/env python3
# In-memory injection into the corrected runner's none-written check (the
# ROUND 6 AMENDMENT, re-run in round 8). Loads /tmp/U116-run-8.py as a module, points its
# output directory at a scratch directory, replaces os.lstat for the
# lockfile path alone with one that raises the named error (or, for the
# positive control, returns a stat result), and calls check_lock. No
# exception is caught here: the process exit status is the check's own, a
# refusal exits 2 and a normal return exits with the check's failure
# count, so the shell line after each call is the exit line. Its one
# printed line passes through redact().
import getpass
import importlib.util
import os
import sys

RUNNER = "/tmp/U116-run-8.py"
OUT = "/tmp/U116-inject-8-lock-out"
ERRORS = {
    "permission": (PermissionError, 13, "Permission denied"),
    "missing": (FileNotFoundError, 2, "No such file or directory"),
    "present": None,
}


def redactions():
    # The strings redact() replaces, longest first so a home path is
    # replaced before the login name inside it: the real home directory in
    # both spellings (the resolved path of ~, and HOME when it is set) as
    # ~, and the login name (getpass, and USER when it is set) as <user>.
    # The optional variables are read by membership and index, not by a
    # lookup with a default.
    homes = [os.path.realpath(os.path.expanduser("~"))]
    if "HOME" in os.environ:
        homes.append(os.environ["HOME"])
    users = [getpass.getuser()]
    if "USER" in os.environ:
        users.append(os.environ["USER"])
    pairs = [(home, "~") for home in homes if len(home) > 1] + [(user, "<user>") for user in users if user]
    pairs.sort(key=lambda pair: len(pair[0]), reverse=True)
    return tuple(dict.fromkeys(pairs))


REDACTIONS = redactions()


def redact(text):
    # Every string that reaches stdout or stderr passes through here,
    # refusals and receipts included.
    for literal, replacement in REDACTIONS:
        text = text.replace(literal, replacement)
    return text

case = sys.argv[1]
error = ERRORS[case]
spec = importlib.util.spec_from_file_location("runner", RUNNER)
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)
os.makedirs(OUT, exist_ok=True)
runner.OUT = OUT
real_lstat = os.lstat


def injected_lstat(path, *args, **kwargs):
    if path != runner.LOCK:
        return real_lstat(path, *args, **kwargs)
    if error is None:
        return real_lstat(RUNNER)  # any present file stands in for a written lockfile
    kind, errno, text = error
    raise kind(errno, text, path)


os.lstat = injected_lstat
print(redact(f"injected os.lstat for {runner.LOCK}: {case}"))
sys.exit(runner.check_lock())
```

```sh
python3 -I /tmp/U116-inject-8-lock.py permission; echo "exit=$?"
python3 -I /tmp/U116-inject-8-lock.py missing; echo "exit=$?"
python3 -I /tmp/U116-inject-8-lock.py present; echo "exit=$?"
```

```text
mise=~/.local/bin/mise (PATH entry 51 of 55)
injected os.lstat for /var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home-5/.config/mise/mise.lock: permission
run REFUSED: cannot read /var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home-5/.config/mise/mise.lock: [Errno 13] Permission denied: '/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home-5/.config/mise/mise.lock'
exit=2
mise=~/.local/bin/mise (PATH entry 51 of 55)
injected os.lstat for /var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home-5/.config/mise/mise.lock: missing
g-none-written: none-written
exit=0
mise=~/.local/bin/mise (PATH entry 51 of 55)
injected os.lstat for /var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home-5/.config/mise/mise.lock: present
g-none-written: WRITTEN
exit=1
```

### `mise lock --help`, first eight lines

From `help-lock.txt` of the runner (receipt `start=2026-10-29T13:23:50Z end=2026-10-29T13:23:50Z elapsed=0s exit=0`), the first eight of its 183 lines:

```text
Create or refresh lockfile versions, checksums, and download URLs

Operates on the current config root, including tools declared by tasks.
Existing matching locked versions are preserved unless `--bump` re-resolves
their requests. This command does not install tools; `--dry-run` previews
changes.

`mise lock TOOL@VERSION` locks that exact version. When the version falls
```

### Attempt 1 of round 1: cwd under the real home (not the measured run, not re-taken)

In round 1 (commit `e0a1526a`) the bash runner was first started from the coordinator checkout `~/Workspace/dotfiles`, with `HOME` and the four XDG variables pointed at the scratch home. The three `mise lock` runs exited 1 in 0 seconds:

```text
mise ERROR error parsing config file: ~/.config/mise/config.toml
mise ERROR Config files in ~/.config/mise/config.toml are not trusted.
Trust them with `mise trust`. See https://mise.jdx.dev/cli/trust.html for more information.
mise ERROR Version: 2026.10.19 macos-arm64 (2026-10-24)
mise ERROR Run with --verbose or MISE_VERBOSE=1 for more information
```

The (c) and (d) runs printed the same five lines; their files are `attempt1-cwd-checkout/c-lock-dry-run-4-platforms.txt` and `attempt1-cwd-checkout/d-lock-bump-json.txt` under `$TMPDIR/U116-out/`, the round-1 output directory. The `settings get` runs (e) and (f) printed `npm` and `72h` and exited 0. Round 7 did not repeat the attempt: a repeat would open the real `~/.config/mise/config.toml` on purpose, which the brief's SCOPE forbids, so the lesson is applied instead. This block is the one pasted output in this section that does not come from `U116-out-5/`; the document is scanned whole below, so the scan covers it.

Reading: the error names the real `~/.config/mise/config.toml`, although `HOME` pointed elsewhere. mise walks the parent directories of the cwd for project config files, and `.config/mise/config.toml` is one of the names it looks for, so the real home directory, an ancestor of the checkout, supplied a project config that the scratch trust store does not know (inferred from the path in the error and from the fact that the same command succeeds from a cwd outside the real home). mise refused to load it and did not write to it. Lesson for the next rerun: the cwd of a scratch-HOME mise run must sit outside the real home. The runner above changes to the scratch home before its first call.

### The measured run (round 7), cwd `$TMPDIR/U116-home-5`

Each run below names its output file and its receipt, both written by the runner above.

(a) `mise --version`, `a-version.txt`, receipt `start=2026-10-29T13:23:49Z end=2026-10-29T13:23:50Z elapsed=0s exit=0`

```text
2026.10.19 macos-arm64 (2026-10-24)
```

(b) `mise lock --global --dry-run`, `b-lock-dry-run.txt`, receipt `start=2026-10-29T13:23:50Z end=2026-10-29T13:23:52Z elapsed=2s exit=0`

```text
→ Targeting 7 platform(s) for /private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home-5/.config/mise/mise.lock: linux-arm64, linux-arm64-musl, linux-x64, linux-x64-musl, macos-arm64, macos-x64, windows-x64
→ Processing 36 tool(s): node@26.12.1, rust@1.99.1, python@3.15.2, age@1.3.2, bun@1.4.4, chezmoi@2.73.3, dotenvx@2.38.2, cargo:eza@0.23.5, fd@10.5.0, jq@1.8.2, hugo-extended@0.168.0, uv@0.13.5, yazi@26.9.1, aqua:micro-editor/micro@2.0.15, aqua:mikefarah/yq@4.54.1, aqua:watchexec/watchexec@2.8.0, npm:@anthropic-ai/claude-code@2.1.310, npm:@openai/codex@0.164.0, npm:@anthropic-ai/sandbox-runtime@0.0.81, npm:bash-language-server@5.8.1, npm:ccstatusline@2.2.32, npm:ccusage@20.0.37, npm:pyright@1.1.414, npm:fast-cli@6.0.0, npm:prettier@3.9.10, npm:pnpm@12.8.1, github:x-motemen/ghq@1.11.2, github:d-kuro/gwq@0.1.2, github:cli/cli@2.103.2, github:ogulcancelik/herdr@0.9.5, cargo:pueue@4.0.4, http:bats@1.14.0, http:gcloud@590.0.0, http:shellcheck@0.11.0, http:shfmt@3.14.1, http:ruff@0.17.2
→ Dry run - would update:
  ✓ node@26.12.1 for linux-arm64
  ✓ node@26.12.1 for linux-arm64-musl
  ✓ node@26.12.1 for linux-x64
  ✓ node@26.12.1 for linux-x64-musl
  ✓ node@26.12.1 for macos-arm64
  ✓ node@26.12.1 for macos-x64
  ✓ node@26.12.1 for windows-x64
  ✓ rust@1.99.1 for linux-arm64
  ✓ rust@1.99.1 for linux-arm64-musl
  ✓ rust@1.99.1 for linux-x64
  ✓ rust@1.99.1 for linux-x64-musl
  ✓ rust@1.99.1 for macos-arm64
  ✓ rust@1.99.1 for macos-x64
  ✓ rust@1.99.1 for windows-x64
  ✓ python@3.15.2 for linux-arm64
  ✓ python@3.15.2 for linux-arm64-musl
  ✓ python@3.15.2 for linux-x64
  ✓ python@3.15.2 for linux-x64-musl
  ✓ python@3.15.2 for macos-arm64
  ✓ python@3.15.2 for macos-x64
  ✓ python@3.15.2 for windows-x64
  ✓ age@1.3.2 for linux-arm64
  ✓ age@1.3.2 for linux-arm64-musl
  ✓ age@1.3.2 for linux-x64
  ✓ age@1.3.2 for linux-x64-musl
  ✓ age@1.3.2 for macos-arm64
  ✓ age@1.3.2 for macos-x64
  ✓ age@1.3.2 for windows-x64
  ✓ bun@1.4.4 for linux-arm64
  ✓ bun@1.4.4 for linux-arm64-musl
  ✓ bun@1.4.4 for linux-arm64-musl
  ✓ bun@1.4.4 for linux-x64
  ✓ bun@1.4.4 for linux-x64-baseline
  ✓ bun@1.4.4 for linux-x64-musl
  ✓ bun@1.4.4 for linux-x64-musl-baseline
  ✓ bun@1.4.4 for linux-x64-musl
  ✓ bun@1.4.4 for macos-arm64
  ✓ bun@1.4.4 for macos-x64
  ✓ bun@1.4.4 for macos-x64-baseline
  ✓ bun@1.4.4 for windows-x64
  ✓ bun@1.4.4 for windows-x64-baseline
  ✓ chezmoi@2.73.3 for linux-arm64
  ✓ chezmoi@2.73.3 for linux-arm64-musl
  ✓ chezmoi@2.73.3 for linux-x64
  ✓ chezmoi@2.73.3 for linux-x64-musl
  ✓ chezmoi@2.73.3 for macos-arm64
  ✓ chezmoi@2.73.3 for macos-x64
  ✓ chezmoi@2.73.3 for windows-x64
  ✓ dotenvx@2.38.2 for linux-arm64
  ✓ dotenvx@2.38.2 for linux-arm64-musl
  ✓ dotenvx@2.38.2 for linux-x64
  ✓ dotenvx@2.38.2 for linux-x64-musl
  ✓ dotenvx@2.38.2 for macos-arm64
  ✓ dotenvx@2.38.2 for macos-x64
  ✓ dotenvx@2.38.2 for windows-x64
  ✓ cargo:eza@0.23.5 for linux-arm64
  ✓ cargo:eza@0.23.5 for linux-arm64-musl
  ✓ cargo:eza@0.23.5 for linux-x64
  ✓ cargo:eza@0.23.5 for linux-x64-musl
  ✓ cargo:eza@0.23.5 for macos-arm64
  ✓ cargo:eza@0.23.5 for macos-x64
  ✓ cargo:eza@0.23.5 for windows-x64
  ✓ fd@10.5.0 for linux-arm64
  ✓ fd@10.5.0 for linux-arm64-musl
  ✓ fd@10.5.0 for linux-x64
  ✓ fd@10.5.0 for linux-x64-musl
  ✓ fd@10.5.0 for macos-arm64
  ✓ fd@10.5.0 for macos-x64
  ✓ fd@10.5.0 for windows-x64
  ✓ jq@1.8.2 for linux-arm64
  ✓ jq@1.8.2 for linux-arm64-musl
  ✓ jq@1.8.2 for linux-x64
  ✓ jq@1.8.2 for linux-x64-musl
  ✓ jq@1.8.2 for macos-arm64
  ✓ jq@1.8.2 for macos-x64
  ✓ jq@1.8.2 for windows-x64
  ✓ hugo-extended@0.168.0 for linux-arm64
  ✓ hugo-extended@0.168.0 for linux-arm64-musl
  ✓ hugo-extended@0.168.0 for linux-x64
  ✓ hugo-extended@0.168.0 for linux-x64-musl
  ✓ hugo-extended@0.168.0 for macos-arm64
  ✓ hugo-extended@0.168.0 for macos-x64
  ✓ hugo-extended@0.168.0 for windows-x64
  ✓ uv@0.13.5 for linux-arm64
  ✓ uv@0.13.5 for linux-arm64-musl
  ✓ uv@0.13.5 for linux-x64
  ✓ uv@0.13.5 for linux-x64-musl
  ✓ uv@0.13.5 for macos-arm64
  ✓ uv@0.13.5 for macos-x64
  ✓ uv@0.13.5 for windows-x64
  ✓ yazi@26.9.1 for linux-arm64
  ✓ yazi@26.9.1 for linux-arm64-musl
  ✓ yazi@26.9.1 for linux-x64
  ✓ yazi@26.9.1 for linux-x64-musl
  ✓ yazi@26.9.1 for macos-arm64
  ✓ yazi@26.9.1 for macos-x64
  ✓ yazi@26.9.1 for windows-x64
  ✓ aqua:micro-editor/micro@2.0.15 for linux-arm64
  ✓ aqua:micro-editor/micro@2.0.15 for linux-arm64-musl
  ✓ aqua:micro-editor/micro@2.0.15 for linux-x64
  ✓ aqua:micro-editor/micro@2.0.15 for linux-x64-musl
  ✓ aqua:micro-editor/micro@2.0.15 for macos-arm64
  ✓ aqua:micro-editor/micro@2.0.15 for macos-x64
  ✓ aqua:micro-editor/micro@2.0.15 for windows-x64
  ✓ aqua:mikefarah/yq@4.54.1 for linux-arm64
  ✓ aqua:mikefarah/yq@4.54.1 for linux-arm64-musl
  ✓ aqua:mikefarah/yq@4.54.1 for linux-x64
  ✓ aqua:mikefarah/yq@4.54.1 for linux-x64-musl
  ✓ aqua:mikefarah/yq@4.54.1 for macos-arm64
  ✓ aqua:mikefarah/yq@4.54.1 for macos-x64
  ✓ aqua:mikefarah/yq@4.54.1 for windows-x64
  ✓ aqua:watchexec/watchexec@2.8.0 for linux-arm64
  ✓ aqua:watchexec/watchexec@2.8.0 for linux-arm64-musl
  ✓ aqua:watchexec/watchexec@2.8.0 for linux-x64
  ✓ aqua:watchexec/watchexec@2.8.0 for linux-x64-musl
  ✓ aqua:watchexec/watchexec@2.8.0 for macos-arm64
  ✓ aqua:watchexec/watchexec@2.8.0 for macos-x64
  ✓ aqua:watchexec/watchexec@2.8.0 for windows-x64
  ✓ npm:@anthropic-ai/claude-code@2.1.310 for linux-arm64
  ✓ npm:@anthropic-ai/claude-code@2.1.310 for linux-arm64-musl
  ✓ npm:@anthropic-ai/claude-code@2.1.310 for linux-x64
  ✓ npm:@anthropic-ai/claude-code@2.1.310 for linux-x64-musl
  ✓ npm:@anthropic-ai/claude-code@2.1.310 for macos-arm64
  ✓ npm:@anthropic-ai/claude-code@2.1.310 for macos-x64
  ✓ npm:@anthropic-ai/claude-code@2.1.310 for windows-x64
  ✓ npm:@openai/codex@0.164.0 for linux-arm64
  ✓ npm:@openai/codex@0.164.0 for linux-arm64-musl
  ✓ npm:@openai/codex@0.164.0 for linux-x64
  ✓ npm:@openai/codex@0.164.0 for linux-x64-musl
  ✓ npm:@openai/codex@0.164.0 for macos-arm64
  ✓ npm:@openai/codex@0.164.0 for macos-x64
  ✓ npm:@openai/codex@0.164.0 for windows-x64
  ✓ npm:@anthropic-ai/sandbox-runtime@0.0.81 for linux-arm64
  ✓ npm:@anthropic-ai/sandbox-runtime@0.0.81 for linux-arm64-musl
  ✓ npm:@anthropic-ai/sandbox-runtime@0.0.81 for linux-x64
  ✓ npm:@anthropic-ai/sandbox-runtime@0.0.81 for linux-x64-musl
  ✓ npm:@anthropic-ai/sandbox-runtime@0.0.81 for macos-arm64
  ✓ npm:@anthropic-ai/sandbox-runtime@0.0.81 for macos-x64
  ✓ npm:@anthropic-ai/sandbox-runtime@0.0.81 for windows-x64
  ✓ npm:bash-language-server@5.8.1 for linux-arm64
  ✓ npm:bash-language-server@5.8.1 for linux-arm64-musl
  ✓ npm:bash-language-server@5.8.1 for linux-x64
  ✓ npm:bash-language-server@5.8.1 for linux-x64-musl
  ✓ npm:bash-language-server@5.8.1 for macos-arm64
  ✓ npm:bash-language-server@5.8.1 for macos-x64
  ✓ npm:bash-language-server@5.8.1 for windows-x64
  ✓ npm:ccstatusline@2.2.32 for linux-arm64
  ✓ npm:ccstatusline@2.2.32 for linux-arm64-musl
  ✓ npm:ccstatusline@2.2.32 for linux-x64
  ✓ npm:ccstatusline@2.2.32 for linux-x64-musl
  ✓ npm:ccstatusline@2.2.32 for macos-arm64
  ✓ npm:ccstatusline@2.2.32 for macos-x64
  ✓ npm:ccstatusline@2.2.32 for windows-x64
  ✓ npm:ccusage@20.0.37 for linux-arm64
  ✓ npm:ccusage@20.0.37 for linux-arm64-musl
  ✓ npm:ccusage@20.0.37 for linux-x64
  ✓ npm:ccusage@20.0.37 for linux-x64-musl
  ✓ npm:ccusage@20.0.37 for macos-arm64
  ✓ npm:ccusage@20.0.37 for macos-x64
  ✓ npm:ccusage@20.0.37 for windows-x64
  ✓ npm:pyright@1.1.414 for linux-arm64
  ✓ npm:pyright@1.1.414 for linux-arm64-musl
  ✓ npm:pyright@1.1.414 for linux-x64
  ✓ npm:pyright@1.1.414 for linux-x64-musl
  ✓ npm:pyright@1.1.414 for macos-arm64
  ✓ npm:pyright@1.1.414 for macos-x64
  ✓ npm:pyright@1.1.414 for windows-x64
  ✓ npm:fast-cli@6.0.0 for linux-arm64
  ✓ npm:fast-cli@6.0.0 for linux-arm64-musl
  ✓ npm:fast-cli@6.0.0 for linux-x64
  ✓ npm:fast-cli@6.0.0 for linux-x64-musl
  ✓ npm:fast-cli@6.0.0 for macos-arm64
  ✓ npm:fast-cli@6.0.0 for macos-x64
  ✓ npm:fast-cli@6.0.0 for windows-x64
  ✓ npm:prettier@3.9.10 for linux-arm64
  ✓ npm:prettier@3.9.10 for linux-arm64-musl
  ✓ npm:prettier@3.9.10 for linux-x64
  ✓ npm:prettier@3.9.10 for linux-x64-musl
  ✓ npm:prettier@3.9.10 for macos-arm64
  ✓ npm:prettier@3.9.10 for macos-x64
  ✓ npm:prettier@3.9.10 for windows-x64
  ✓ npm:pnpm@12.8.1 for linux-arm64
  ✓ npm:pnpm@12.8.1 for linux-arm64-musl
  ✓ npm:pnpm@12.8.1 for linux-x64
  ✓ npm:pnpm@12.8.1 for linux-x64-musl
  ✓ npm:pnpm@12.8.1 for macos-arm64
  ✓ npm:pnpm@12.8.1 for macos-x64
  ✓ npm:pnpm@12.8.1 for windows-x64
  ✓ github:x-motemen/ghq@1.11.2 for linux-arm64
  ✓ github:x-motemen/ghq@1.11.2 for linux-arm64-musl
  ✓ github:x-motemen/ghq@1.11.2 for linux-x64
  ✓ github:x-motemen/ghq@1.11.2 for linux-x64-musl
  ✓ github:x-motemen/ghq@1.11.2 for macos-arm64
  ✓ github:x-motemen/ghq@1.11.2 for macos-x64
  ✓ github:x-motemen/ghq@1.11.2 for windows-x64
  ✓ github:d-kuro/gwq@0.1.2 for linux-arm64
  ✓ github:d-kuro/gwq@0.1.2 for linux-arm64-musl
  ✓ github:d-kuro/gwq@0.1.2 for linux-x64
  ✓ github:d-kuro/gwq@0.1.2 for linux-x64-musl
  ✓ github:d-kuro/gwq@0.1.2 for macos-arm64
  ✓ github:d-kuro/gwq@0.1.2 for macos-x64
  ✓ github:d-kuro/gwq@0.1.2 for windows-x64
  ✓ github:cli/cli@2.103.2 for linux-arm64
  ✓ github:cli/cli@2.103.2 for linux-arm64-musl
  ✓ github:cli/cli@2.103.2 for linux-x64
  ✓ github:cli/cli@2.103.2 for linux-x64-musl
  ✓ github:cli/cli@2.103.2 for macos-arm64
  ✓ github:cli/cli@2.103.2 for macos-x64
  ✓ github:cli/cli@2.103.2 for windows-x64
  ✓ github:ogulcancelik/herdr@0.9.5 for linux-arm64
  ✓ github:ogulcancelik/herdr@0.9.5 for linux-arm64-musl
  ✓ github:ogulcancelik/herdr@0.9.5 for linux-x64
  ✓ github:ogulcancelik/herdr@0.9.5 for linux-x64-musl
  ✓ github:ogulcancelik/herdr@0.9.5 for macos-arm64
  ✓ github:ogulcancelik/herdr@0.9.5 for macos-x64
  ✓ github:ogulcancelik/herdr@0.9.5 for windows-x64
  ✓ cargo:pueue@4.0.4 for linux-arm64
  ✓ cargo:pueue@4.0.4 for linux-arm64-musl
  ✓ cargo:pueue@4.0.4 for linux-x64
  ✓ cargo:pueue@4.0.4 for linux-x64-musl
  ✓ cargo:pueue@4.0.4 for macos-arm64
  ✓ cargo:pueue@4.0.4 for macos-x64
  ✓ cargo:pueue@4.0.4 for windows-x64
  ✓ http:bats@1.14.0 for linux-arm64
  ✓ http:bats@1.14.0 for linux-arm64-musl
  ✓ http:bats@1.14.0 for linux-x64
  ✓ http:bats@1.14.0 for linux-x64-musl
  ✓ http:bats@1.14.0 for macos-arm64
  ✓ http:bats@1.14.0 for macos-x64
  ✓ http:bats@1.14.0 for windows-x64
  ✓ http:gcloud@590.0.0 for linux-arm64
  ✓ http:gcloud@590.0.0 for linux-arm64-musl
  ✓ http:gcloud@590.0.0 for linux-x64
  ✓ http:gcloud@590.0.0 for linux-x64-musl
  ✓ http:gcloud@590.0.0 for macos-arm64
  ✓ http:gcloud@590.0.0 for macos-x64
  ✓ http:gcloud@590.0.0 for windows-x64
  ✓ http:shellcheck@0.11.0 for linux-arm64
  ✓ http:shellcheck@0.11.0 for linux-arm64-musl
  ✓ http:shellcheck@0.11.0 for linux-x64
  ✓ http:shellcheck@0.11.0 for linux-x64-musl
  ✓ http:shellcheck@0.11.0 for macos-arm64
  ✓ http:shellcheck@0.11.0 for macos-x64
  ✓ http:shellcheck@0.11.0 for windows-x64
  ✓ http:shfmt@3.14.1 for linux-arm64
  ✓ http:shfmt@3.14.1 for linux-arm64-musl
  ✓ http:shfmt@3.14.1 for linux-x64
  ✓ http:shfmt@3.14.1 for linux-x64-musl
  ✓ http:shfmt@3.14.1 for macos-arm64
  ✓ http:shfmt@3.14.1 for macos-x64
  ✓ http:shfmt@3.14.1 for windows-x64
  ✓ http:ruff@0.17.2 for linux-arm64
  ✓ http:ruff@0.17.2 for linux-arm64-musl
  ✓ http:ruff@0.17.2 for linux-x64
  ✓ http:ruff@0.17.2 for linux-x64-musl
  ✓ http:ruff@0.17.2 for macos-arm64
  ✓ http:ruff@0.17.2 for macos-x64
  ✓ http:ruff@0.17.2 for windows-x64
```

(c) `mise lock --global --dry-run --platform linux-x64,linux-arm64,macos-x64,macos-arm64`, `c-lock-dry-run-4-platforms.txt`, receipt `start=2026-10-29T13:23:52Z end=2026-10-29T13:23:52Z elapsed=0s exit=0`

```text
→ Targeting 4 platform(s) for /private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home-5/.config/mise/mise.lock: linux-arm64, linux-x64, macos-arm64, macos-x64
→ Processing 36 tool(s): node@26.12.1, rust@1.99.1, python@3.15.2, age@1.3.2, bun@1.4.4, chezmoi@2.73.3, dotenvx@2.38.2, cargo:eza@0.23.5, fd@10.5.0, jq@1.8.2, hugo-extended@0.168.0, uv@0.13.5, yazi@26.9.1, aqua:micro-editor/micro@2.0.15, aqua:mikefarah/yq@4.54.1, aqua:watchexec/watchexec@2.8.0, npm:@anthropic-ai/claude-code@2.1.310, npm:@openai/codex@0.164.0, npm:@anthropic-ai/sandbox-runtime@0.0.81, npm:bash-language-server@5.8.1, npm:ccstatusline@2.2.32, npm:ccusage@20.0.37, npm:pyright@1.1.414, npm:fast-cli@6.0.0, npm:prettier@3.9.10, npm:pnpm@12.8.1, github:x-motemen/ghq@1.11.2, github:d-kuro/gwq@0.1.2, github:cli/cli@2.103.2, github:ogulcancelik/herdr@0.9.5, cargo:pueue@4.0.4, http:bats@1.14.0, http:gcloud@590.0.0, http:shellcheck@0.11.0, http:shfmt@3.14.1, http:ruff@0.17.2
→ Dry run - would update:
  ✓ node@26.12.1 for linux-arm64
  ✓ node@26.12.1 for linux-x64
  ✓ node@26.12.1 for macos-arm64
  ✓ node@26.12.1 for macos-x64
  ✓ rust@1.99.1 for linux-arm64
  ✓ rust@1.99.1 for linux-x64
  ✓ rust@1.99.1 for macos-arm64
  ✓ rust@1.99.1 for macos-x64
  ✓ python@3.15.2 for linux-arm64
  ✓ python@3.15.2 for linux-x64
  ✓ python@3.15.2 for macos-arm64
  ✓ python@3.15.2 for macos-x64
  ✓ age@1.3.2 for linux-arm64
  ✓ age@1.3.2 for linux-x64
  ✓ age@1.3.2 for macos-arm64
  ✓ age@1.3.2 for macos-x64
  ✓ bun@1.4.4 for linux-arm64
  ✓ bun@1.4.4 for linux-arm64-musl
  ✓ bun@1.4.4 for linux-x64
  ✓ bun@1.4.4 for linux-x64-baseline
  ✓ bun@1.4.4 for linux-x64-musl
  ✓ bun@1.4.4 for linux-x64-musl-baseline
  ✓ bun@1.4.4 for macos-arm64
  ✓ bun@1.4.4 for macos-x64
  ✓ bun@1.4.4 for macos-x64-baseline
  ✓ chezmoi@2.73.3 for linux-arm64
  ✓ chezmoi@2.73.3 for linux-x64
  ✓ chezmoi@2.73.3 for macos-arm64
  ✓ chezmoi@2.73.3 for macos-x64
  ✓ dotenvx@2.38.2 for linux-arm64
  ✓ dotenvx@2.38.2 for linux-x64
  ✓ dotenvx@2.38.2 for macos-arm64
  ✓ dotenvx@2.38.2 for macos-x64
  ✓ cargo:eza@0.23.5 for linux-arm64
  ✓ cargo:eza@0.23.5 for linux-x64
  ✓ cargo:eza@0.23.5 for macos-arm64
  ✓ cargo:eza@0.23.5 for macos-x64
  ✓ fd@10.5.0 for linux-arm64
  ✓ fd@10.5.0 for linux-x64
  ✓ fd@10.5.0 for macos-arm64
  ✓ fd@10.5.0 for macos-x64
  ✓ jq@1.8.2 for linux-arm64
  ✓ jq@1.8.2 for linux-x64
  ✓ jq@1.8.2 for macos-arm64
  ✓ jq@1.8.2 for macos-x64
  ✓ hugo-extended@0.168.0 for linux-arm64
  ✓ hugo-extended@0.168.0 for linux-x64
  ✓ hugo-extended@0.168.0 for macos-arm64
  ✓ hugo-extended@0.168.0 for macos-x64
  ✓ uv@0.13.5 for linux-arm64
  ✓ uv@0.13.5 for linux-x64
  ✓ uv@0.13.5 for macos-arm64
  ✓ uv@0.13.5 for macos-x64
  ✓ yazi@26.9.1 for linux-arm64
  ✓ yazi@26.9.1 for linux-x64
  ✓ yazi@26.9.1 for macos-arm64
  ✓ yazi@26.9.1 for macos-x64
  ✓ aqua:micro-editor/micro@2.0.15 for linux-arm64
  ✓ aqua:micro-editor/micro@2.0.15 for linux-x64
  ✓ aqua:micro-editor/micro@2.0.15 for macos-arm64
  ✓ aqua:micro-editor/micro@2.0.15 for macos-x64
  ✓ aqua:mikefarah/yq@4.54.1 for linux-arm64
  ✓ aqua:mikefarah/yq@4.54.1 for linux-x64
  ✓ aqua:mikefarah/yq@4.54.1 for macos-arm64
  ✓ aqua:mikefarah/yq@4.54.1 for macos-x64
  ✓ aqua:watchexec/watchexec@2.8.0 for linux-arm64
  ✓ aqua:watchexec/watchexec@2.8.0 for linux-x64
  ✓ aqua:watchexec/watchexec@2.8.0 for macos-arm64
  ✓ aqua:watchexec/watchexec@2.8.0 for macos-x64
  ✓ npm:@anthropic-ai/claude-code@2.1.310 for linux-arm64
  ✓ npm:@anthropic-ai/claude-code@2.1.310 for linux-x64
  ✓ npm:@anthropic-ai/claude-code@2.1.310 for macos-arm64
  ✓ npm:@anthropic-ai/claude-code@2.1.310 for macos-x64
  ✓ npm:@openai/codex@0.164.0 for linux-arm64
  ✓ npm:@openai/codex@0.164.0 for linux-x64
  ✓ npm:@openai/codex@0.164.0 for macos-arm64
  ✓ npm:@openai/codex@0.164.0 for macos-x64
  ✓ npm:@anthropic-ai/sandbox-runtime@0.0.81 for linux-arm64
  ✓ npm:@anthropic-ai/sandbox-runtime@0.0.81 for linux-x64
  ✓ npm:@anthropic-ai/sandbox-runtime@0.0.81 for macos-arm64
  ✓ npm:@anthropic-ai/sandbox-runtime@0.0.81 for macos-x64
  ✓ npm:bash-language-server@5.8.1 for linux-arm64
  ✓ npm:bash-language-server@5.8.1 for linux-x64
  ✓ npm:bash-language-server@5.8.1 for macos-arm64
  ✓ npm:bash-language-server@5.8.1 for macos-x64
  ✓ npm:ccstatusline@2.2.32 for linux-arm64
  ✓ npm:ccstatusline@2.2.32 for linux-x64
  ✓ npm:ccstatusline@2.2.32 for macos-arm64
  ✓ npm:ccstatusline@2.2.32 for macos-x64
  ✓ npm:ccusage@20.0.37 for linux-arm64
  ✓ npm:ccusage@20.0.37 for linux-x64
  ✓ npm:ccusage@20.0.37 for macos-arm64
  ✓ npm:ccusage@20.0.37 for macos-x64
  ✓ npm:pyright@1.1.414 for linux-arm64
  ✓ npm:pyright@1.1.414 for linux-x64
  ✓ npm:pyright@1.1.414 for macos-arm64
  ✓ npm:pyright@1.1.414 for macos-x64
  ✓ npm:fast-cli@6.0.0 for linux-arm64
  ✓ npm:fast-cli@6.0.0 for linux-x64
  ✓ npm:fast-cli@6.0.0 for macos-arm64
  ✓ npm:fast-cli@6.0.0 for macos-x64
  ✓ npm:prettier@3.9.10 for linux-arm64
  ✓ npm:prettier@3.9.10 for linux-x64
  ✓ npm:prettier@3.9.10 for macos-arm64
  ✓ npm:prettier@3.9.10 for macos-x64
  ✓ npm:pnpm@12.8.1 for linux-arm64
  ✓ npm:pnpm@12.8.1 for linux-x64
  ✓ npm:pnpm@12.8.1 for macos-arm64
  ✓ npm:pnpm@12.8.1 for macos-x64
  ✓ github:x-motemen/ghq@1.11.2 for linux-arm64
  ✓ github:x-motemen/ghq@1.11.2 for linux-x64
  ✓ github:x-motemen/ghq@1.11.2 for macos-arm64
  ✓ github:x-motemen/ghq@1.11.2 for macos-x64
  ✓ github:d-kuro/gwq@0.1.2 for linux-arm64
  ✓ github:d-kuro/gwq@0.1.2 for linux-x64
  ✓ github:d-kuro/gwq@0.1.2 for macos-arm64
  ✓ github:d-kuro/gwq@0.1.2 for macos-x64
  ✓ github:cli/cli@2.103.2 for linux-arm64
  ✓ github:cli/cli@2.103.2 for linux-x64
  ✓ github:cli/cli@2.103.2 for macos-arm64
  ✓ github:cli/cli@2.103.2 for macos-x64
  ✓ github:ogulcancelik/herdr@0.9.5 for linux-arm64
  ✓ github:ogulcancelik/herdr@0.9.5 for linux-x64
  ✓ github:ogulcancelik/herdr@0.9.5 for macos-arm64
  ✓ github:ogulcancelik/herdr@0.9.5 for macos-x64
  ✓ cargo:pueue@4.0.4 for linux-arm64
  ✓ cargo:pueue@4.0.4 for linux-x64
  ✓ cargo:pueue@4.0.4 for macos-arm64
  ✓ cargo:pueue@4.0.4 for macos-x64
  ✓ http:bats@1.14.0 for linux-arm64
  ✓ http:bats@1.14.0 for linux-x64
  ✓ http:bats@1.14.0 for macos-arm64
  ✓ http:bats@1.14.0 for macos-x64
  ✓ http:gcloud@590.0.0 for linux-arm64
  ✓ http:gcloud@590.0.0 for linux-x64
  ✓ http:gcloud@590.0.0 for macos-arm64
  ✓ http:gcloud@590.0.0 for macos-x64
  ✓ http:shellcheck@0.11.0 for linux-arm64
  ✓ http:shellcheck@0.11.0 for linux-x64
  ✓ http:shellcheck@0.11.0 for macos-arm64
  ✓ http:shellcheck@0.11.0 for macos-x64
  ✓ http:shfmt@3.14.1 for linux-arm64
  ✓ http:shfmt@3.14.1 for linux-x64
  ✓ http:shfmt@3.14.1 for macos-arm64
  ✓ http:shfmt@3.14.1 for macos-x64
  ✓ http:ruff@0.17.2 for linux-arm64
  ✓ http:ruff@0.17.2 for linux-x64
  ✓ http:ruff@0.17.2 for macos-arm64
  ✓ http:ruff@0.17.2 for macos-x64
```

(d) `mise lock --global --dry-run --bump --json`, `d-lock-bump-json.txt`, receipt `start=2026-10-29T13:23:52Z end=2026-10-29T13:23:52Z elapsed=0s exit=0`

```text
[
  {
    "name": "node",
    "backend": "core:node",
    "lockfile": "/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home-5/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "26.12.1"
    ]
  },
  {
    "name": "rust",
    "backend": "core:rust",
    "lockfile": "/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home-5/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "1.99.1"
    ]
  },
  {
    "name": "python",
    "backend": "core:python",
    "lockfile": "/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home-5/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "3.15.2"
    ]
  },
  {
    "name": "age",
    "backend": "aqua:FiloSottile/age",
    "lockfile": "/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home-5/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "1.3.2"
    ]
  },
  {
    "name": "bun",
    "backend": "core:bun",
    "lockfile": "/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home-5/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "1.4.4"
    ]
  },
  {
    "name": "chezmoi",
    "backend": "aqua:twpayne/chezmoi",
    "lockfile": "/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home-5/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "2.73.3"
    ]
  },
  {
    "name": "dotenvx",
    "backend": "aqua:dotenvx/dotenvx",
    "lockfile": "/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home-5/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "2.38.2"
    ]
  },
  {
    "name": "cargo:eza",
    "backend": "cargo:eza",
    "lockfile": "/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home-5/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "0.23.5"
    ]
  },
  {
    "name": "fd",
    "backend": "aqua:sharkdp/fd",
    "lockfile": "/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home-5/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "10.5.0"
    ]
  },
  {
    "name": "jq",
    "backend": "aqua:jqlang/jq",
    "lockfile": "/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home-5/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "1.8.2"
    ]
  },
  {
    "name": "hugo-extended",
    "backend": "aqua:gohugoio/hugo/hugo-extended",
    "lockfile": "/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home-5/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "0.168.0"
    ]
  },
  {
    "name": "uv",
    "backend": "aqua:astral-sh/uv",
    "lockfile": "/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home-5/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "0.13.5"
    ]
  },
  {
    "name": "yazi",
    "backend": "aqua:sxyazi/yazi",
    "lockfile": "/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home-5/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "26.9.1"
    ]
  },
  {
    "name": "aqua:micro-editor/micro",
    "backend": "aqua:micro-editor/micro",
    "lockfile": "/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home-5/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "2.0.15"
    ]
  },
  {
    "name": "aqua:mikefarah/yq",
    "backend": "aqua:mikefarah/yq",
    "lockfile": "/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home-5/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "4.54.1"
    ]
  },
  {
    "name": "aqua:watchexec/watchexec",
    "backend": "aqua:watchexec/watchexec",
    "lockfile": "/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home-5/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "2.8.0"
    ]
  },
  {
    "name": "npm:@anthropic-ai/claude-code",
    "backend": "npm:@anthropic-ai/claude-code",
    "lockfile": "/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home-5/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "2.1.310"
    ]
  },
  {
    "name": "npm:@openai/codex",
    "backend": "npm:@openai/codex",
    "lockfile": "/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home-5/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "0.164.0"
    ]
  },
  {
    "name": "npm:@anthropic-ai/sandbox-runtime",
    "backend": "npm:@anthropic-ai/sandbox-runtime",
    "lockfile": "/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home-5/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "0.0.81"
    ]
  },
  {
    "name": "npm:bash-language-server",
    "backend": "npm:bash-language-server",
    "lockfile": "/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home-5/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "5.8.1"
    ]
  },
  {
    "name": "npm:ccstatusline",
    "backend": "npm:ccstatusline",
    "lockfile": "/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home-5/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "2.2.32"
    ]
  },
  {
    "name": "npm:ccusage",
    "backend": "npm:ccusage",
    "lockfile": "/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home-5/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "20.0.37"
    ]
  },
  {
    "name": "npm:pyright",
    "backend": "npm:pyright",
    "lockfile": "/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home-5/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "1.1.414"
    ]
  },
  {
    "name": "npm:fast-cli",
    "backend": "npm:fast-cli",
    "lockfile": "/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home-5/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "6.0.0"
    ]
  },
  {
    "name": "npm:prettier",
    "backend": "npm:prettier",
    "lockfile": "/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home-5/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "3.9.10"
    ]
  },
  {
    "name": "npm:pnpm",
    "backend": "npm:pnpm",
    "lockfile": "/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home-5/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "12.8.1"
    ]
  },
  {
    "name": "github:x-motemen/ghq",
    "backend": "github:x-motemen/ghq",
    "lockfile": "/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home-5/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "1.11.2"
    ]
  },
  {
    "name": "github:d-kuro/gwq",
    "backend": "github:d-kuro/gwq",
    "lockfile": "/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home-5/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "0.1.2"
    ]
  },
  {
    "name": "github:cli/cli",
    "backend": "github:cli/cli",
    "lockfile": "/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home-5/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "2.103.2"
    ]
  },
  {
    "name": "github:ogulcancelik/herdr",
    "backend": "github:ogulcancelik/herdr",
    "lockfile": "/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home-5/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "0.9.5"
    ]
  },
  {
    "name": "cargo:pueue",
    "backend": "cargo:pueue",
    "lockfile": "/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home-5/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "4.0.4"
    ]
  },
  {
    "name": "http:bats",
    "backend": "http:bats",
    "lockfile": "/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home-5/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "1.14.0"
    ]
  },
  {
    "name": "http:gcloud",
    "backend": "http:gcloud",
    "lockfile": "/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home-5/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "590.0.0"
    ]
  },
  {
    "name": "http:shellcheck",
    "backend": "http:shellcheck",
    "lockfile": "/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home-5/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "0.11.0"
    ]
  },
  {
    "name": "http:shfmt",
    "backend": "http:shfmt",
    "lockfile": "/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home-5/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "3.14.1"
    ]
  },
  {
    "name": "http:ruff",
    "backend": "http:ruff",
    "lockfile": "/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home-5/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "0.17.2"
    ]
  }
]
```

(e) `mise settings get npm.package_manager`, `e-npm-package-manager.txt`, receipt `start=2026-10-29T13:23:52Z end=2026-10-29T13:23:52Z elapsed=0s exit=0`

```text
npm
```

(f) `mise settings get minimum_release_age`, `f-minimum-release-age.txt`, receipt `start=2026-10-29T13:23:52Z end=2026-10-29T13:23:52Z elapsed=0s exit=0`

```text
72h
```

(g) `/bin/ls -la "$TMPDIR/U116-home-5/.config/mise"` after all runs, `g-scratch-after.txt`, receipt `start=2026-10-29T13:23:52Z end=2026-10-29T13:23:52Z elapsed=0s exit=0`

```text
total 16
drwxr-xr-x@ 3 <user>  staff    96 Oct 29 22:23 .
drwxr-xr-x@ 3 <user>  staff    96 Oct 29 22:23 ..
-rw-r--r--@ 1 <user>  staff  6962 Oct 29 22:23 config.toml
```

(g) `/bin/ls -la ~/.config/mise` after all runs, `g-real-after.txt`, receipt `start=2026-10-29T13:23:52Z end=2026-10-29T13:23:52Z elapsed=0s exit=0`

```text
total 16
drwxr-xr-x   3 <user>  staff    96 Oct 26 23:40 .
drwxr-xr-x  24 <user>  staff   768 Oct 16 17:44 ..
-rw-r--r--@  1 <user>  staff  6962 Oct 26 23:40 config.toml
```

### Further checks

`g-none-written.txt`, written by the runner's `check_lock` after its last call from an in-process `os.lstat` of `$TMPDIR/U116-home-5/.config/mise/mise.lock`, `FileNotFoundError` the only absence (the second set of injections above shows the other two outcomes):

```text
none-written
```

The brief's ACCEPTANCE 6 test, run after the runner:

```sh
test ! -e "$TMPDIR/U116-home-5/.config/mise/mise.lock" && echo none-written
```

```text
none-written
```

The before and after listings of the real `~/.config/mise` both come from `/bin/ls -la` (the before one from the preparation script, the after one from the runner) and are byte for byte equal: `cmp "$TMPDIR/U116-out-5/real-before.txt" "$TMPDIR/U116-out-5/g-real-after.txt"; echo "exit=$?"`

```text
exit=0
```

Modification times of the real mise directories, read in-process by the runner with `os.lstat` before its first mise call (`real-dirs-mtime-before.txt`) and after its last (`real-dirs-mtime-after.txt`), the paths written in `~` form by the script; a directory that is absent is written as `missing` on `FileNotFoundError`, and any other error would have been a refusal. mise on macOS keeps its cache under `~/Library/Caches/mise`, so `~/.cache/mise` does not exist on this host.

```text
2026-10-26T23:40:46 ~/.config/mise
2026-10-29T19:43:40 ~/.local/share/mise
missing ~/.cache/mise
2026-10-29T18:57:51 ~/.local/state/mise
2026-10-29T18:57:42 ~/Library/Caches/mise
```

```text
2026-10-26T23:40:46 ~/.config/mise
2026-10-29T19:43:40 ~/.local/share/mise
missing ~/.cache/mise
2026-10-29T18:57:51 ~/.local/state/mise
2026-10-29T18:57:42 ~/Library/Caches/mise
```

Redaction and credential scan, round 8 (standing orders 21 and 22; the ROUND 4 to ROUND 7 amendments of the brief of 2026-10-29). The script is the round-7 one with the round-8 `redact` function and its six `print` sites (the refusal, the two pattern lines, the per-file line and the two result lines) routed through it, and its header comment; its file set is the round-7 one, because round 8 re-took no run (`DIRS` is the single directory `U116-out-5`; `EXPECTED_FILES` stays 23, the `.txt` files the preparation and the runner wrote, listed in the clean run below: 9 outputs, 9 receipts, the before listing, the none-written file, the two mtime files and the scratch tree; the injection runs above write under `/tmp` and are not in this set); nothing else changed. Everything else stands from rounds 4 to 7: one `python3 -I` script, `/tmp/U116-scan.py`, run as `python3 -I /tmp/U116-scan.py` from the worktree, whose only external command is `gh auth token`, with its exit status, output and timeout read; two pattern classes, the token and every non-comment, non-empty line of the coordinator's `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/redact-words.txt`, read in-process, with the path and the pattern count printed and zero patterns a refusal; two file sets, the 23 `.txt` files for the token (no run needed `MISE_GITHUB_TOKEN`, so none was set) and the two documents that cite this scan, this file as committed (the worktree copy, which is the committed bytes once ACCEPTANCE 1 shows the tree clean) and the PR body `/tmp/dotfiles-wt/U116-pr-body.md`, for both classes. The raw outputs are not scanned for the redact words: the three `ls -la` listings hold the login name in the owner column, which the substitution named at the top of this section replaces on paste; the positive control after the injected failures shows what the class finds there. The script prints one line per file with the count of each class applied to it, and `scan clean (25 files, 0 matches)` only when every count is 0; a `.txt` count other than 23, an empty pattern list or any exception is exit `2` before any clean line. Neither the script nor its invocation holds a process substitution, a command substitution, a pipeline or a wrapper process. The script, then its output:

```python
#!/usr/bin/env python3
# Fail-closed redaction and credential scan, round 8 (standing orders 21
# and 22; brief amendments of 2026-10-29). One process whose only external
# command is `gh auth token`, with its exit status, output and timeout
# read. Two pattern classes: the token, and every non-comment, non-empty
# line of the coordinator's redact list, read in-process. Two file sets:
# the 23 .txt outputs of the round-7 dry runs (token class), and the two
# documents that cite this scan (both classes). Any exception, an empty
# pattern list or a .txt count other than the stated one is exit 2 before
# a clean line can print. Every file question is asked of os.lstat or
# open, with any error a refusal. The token and the redact words stay in
# this process: they reach no command line and no file. Every printed
# line, refusals included, passes through redact().
import getpass
import os
import stat
import subprocess
import sys

# The .txt files the round-7 preparation and runner wrote under
# U116-out-5: 9 outputs, 9 receipts, the before listing, the none-written
# file, the two mtime files and the scratch tree. A different count means
# the directory was not walked or the output set changed, so refuse.
EXPECTED_FILES = 23

DIRS = ("U116-out-5",)

# The coordinator's list; the path is printed in this form, never expanded.
REDACT_LIST = "~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/redact-words.txt"

# The committed evaluation file (the worktree copy; ACCEPTANCE 1 shows the
# worktree clean, so these are the committed bytes) and the PR body.
DOCUMENTS = (
    "/tmp/dotfiles-wt/U116/.orchestration/orchestrate/regime-cutover/handoff/evaluations/U116-mise-lock.md",
    "/tmp/dotfiles-wt/U116-pr-body.md",
)


def redactions():
    # The strings redact() replaces, longest first so a home path is
    # replaced before the login name inside it: the real home directory in
    # both spellings (the resolved path of ~, and HOME when it is set) as
    # ~, and the login name (getpass, and USER when it is set) as <user>.
    # The optional variables are read by membership and index, not by a
    # lookup with a default.
    homes = [os.path.realpath(os.path.expanduser("~"))]
    if "HOME" in os.environ:
        homes.append(os.environ["HOME"])
    users = [getpass.getuser()]
    if "USER" in os.environ:
        users.append(os.environ["USER"])
    pairs = [(home, "~") for home in homes if len(home) > 1] + [(user, "<user>") for user in users if user]
    pairs.sort(key=lambda pair: len(pair[0]), reverse=True)
    return tuple(dict.fromkeys(pairs))


REDACTIONS = redactions()


def redact(text):
    # Every string that reaches stdout or stderr passes through here,
    # refusals and receipts included.
    for literal, replacement in REDACTIONS:
        text = text.replace(literal, replacement)
    return text


def refuse(message):
    print(redact(f"scan REFUSED: {message}"))
    sys.exit(2)


def require_env(name):
    try:
        return os.environ[name]
    except KeyError:
        refuse(f"{name} is unset")


def read_token():
    try:
        proc = subprocess.run(
            ["gh", "auth", "token"],
            capture_output=True,
            text=True,
            check=False,
            timeout=60,
        )
    except subprocess.TimeoutExpired:
        refuse("gh auth token timed out after 60 s")
    except OSError as exc:
        refuse(f"gh auth token could not start: {exc}")
    if proc.returncode != 0:
        refuse(f"gh auth token exited {proc.returncode}")
    token = proc.stdout.strip().encode()
    if not token:
        refuse("gh auth token returned an empty token")
    print(redact("token from gh auth token patterns=1"))
    return token


def read_redact_words():
    words = []
    with open(os.path.expanduser(REDACT_LIST), "rb") as handle:
        for line in handle:
            word = line.strip()
            if word and not word.startswith(b"#"):
                words.append(word)
    print(redact(f"redact list {REDACT_LIST} patterns={len(words)}"))
    if not words:
        refuse(f"redact list {REDACT_LIST} holds no pattern")
    return words


def list_outputs():
    files = []
    for directory in DIRS:
        with os.scandir(directory) as entries:
            for entry in entries:
                if not entry.name.endswith(".txt"):
                    continue
                path = f"{directory}/{entry.name}"
                # os.lstat raises on any error; a .txt that is not a
                # regular file is a refusal, not a skipped entry.
                if not stat.S_ISREG(os.lstat(path).st_mode):
                    refuse(f"{path} is not a regular file")
                files.append(path)
    files.sort()
    if len(files) != EXPECTED_FILES:
        refuse(f"found {len(files)} .txt files, expected {EXPECTED_FILES}")
    return files


def count_matches(path, classes):
    with open(path, "rb") as handle:
        data = handle.read()
    line = path
    total = 0
    for name, patterns in classes:
        count = sum(data.count(pattern) for pattern in patterns)
        line += f" {name}={count}"
        total += count
    print(redact(line))
    return total


def main():
    tmpdir = require_env("TMPDIR")
    token_class = ("token", [read_token()])
    redact_class = ("redact", read_redact_words())
    os.chdir(tmpdir)
    outputs = list_outputs()
    total = 0
    for path in outputs:
        total += count_matches(path, [token_class])  # raw outputs: token only
    for path in DOCUMENTS:
        total += count_matches(path, [token_class, redact_class])
    files = len(outputs) + len(DOCUMENTS)
    if total:
        print(redact(f"scan FOUND ({files} files, {total} matches)"))
        sys.exit(1)
    print(redact(f"scan clean ({files} files, 0 matches)"))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # any raised step is a refusal, never a clean line
        refuse(f"{type(exc).__name__}: {exc}")
```

```text
token from gh auth token patterns=1
redact list ~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/redact-words.txt patterns=5
U116-out-5/a-version.receipt.txt token=0
U116-out-5/a-version.txt token=0
U116-out-5/b-lock-dry-run.receipt.txt token=0
U116-out-5/b-lock-dry-run.txt token=0
U116-out-5/c-lock-dry-run-4-platforms.receipt.txt token=0
U116-out-5/c-lock-dry-run-4-platforms.txt token=0
U116-out-5/d-lock-bump-json.receipt.txt token=0
U116-out-5/d-lock-bump-json.txt token=0
U116-out-5/e-npm-package-manager.receipt.txt token=0
U116-out-5/e-npm-package-manager.txt token=0
U116-out-5/f-minimum-release-age.receipt.txt token=0
U116-out-5/f-minimum-release-age.txt token=0
U116-out-5/g-none-written.txt token=0
U116-out-5/g-real-after.receipt.txt token=0
U116-out-5/g-real-after.txt token=0
U116-out-5/g-scratch-after.receipt.txt token=0
U116-out-5/g-scratch-after.txt token=0
U116-out-5/help-lock.receipt.txt token=0
U116-out-5/help-lock.txt token=0
U116-out-5/real-before.txt token=0
U116-out-5/real-dirs-mtime-after.txt token=0
U116-out-5/real-dirs-mtime-before.txt token=0
U116-out-5/scratch-tree.txt token=0
/tmp/dotfiles-wt/U116/.orchestration/orchestrate/regime-cutover/handoff/evaluations/U116-mise-lock.md token=0 redact=0
/tmp/dotfiles-wt/U116-pr-body.md token=0 redact=0
scan clean (25 files, 0 matches)
exit=0
```

Injected failures (standing order 21), each exiting `2` with its refusal line before any clean line. Injections 2, 3 and 5 run a copy of the script written by `sed … > copy`, and the `diff` against the original is the first lines of each paste, so the single changed line is visible and the original is never edited.

First, `gh` replaced by an executable that exits `1`, first on `PATH`: `mkdir -p /tmp/U116-fake-gh && printf '#!/bin/sh\nexit 1\n' > /tmp/U116-fake-gh/gh && chmod +x /tmp/U116-fake-gh/gh && PATH=/tmp/U116-fake-gh:$PATH python3 -I /tmp/U116-scan.py; echo "exit=$?"`:

```text
scan REFUSED: gh auth token exited 1
exit=2
```

Second, the redact list path pointed at a missing file: `sed 's|^REDACT_LIST = .*|REDACT_LIST = "/tmp/U116-no-such-list.txt"|' /tmp/U116-scan.py > /tmp/U116-scan-missing-list.py; diff /tmp/U116-scan.py /tmp/U116-scan-missing-list.py; test ! -e /tmp/U116-no-such-list.txt && echo "no such file"; python3 -I /tmp/U116-scan-missing-list.py; echo "exit=$?"`. `open` raises and the exception's text is the refusal:

```text
29c29
< REDACT_LIST = "~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/redact-words.txt"
---
> REDACT_LIST = "/tmp/U116-no-such-list.txt"
no such file
token from gh auth token patterns=1
scan REFUSED: FileNotFoundError: [Errno 2] No such file or directory: '/tmp/U116-no-such-list.txt'
exit=2
```

Third, the list replaced by a comment-only copy, the header line of the store's file alone: `grep '^#' ~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/redact-words.txt > /tmp/U116-redact-comment-only.txt; sed 's|^REDACT_LIST = .*|REDACT_LIST = "/tmp/U116-redact-comment-only.txt"|' /tmp/U116-scan.py > /tmp/U116-scan-comment-list.py; cat /tmp/U116-redact-comment-only.txt; diff /tmp/U116-scan.py /tmp/U116-scan-comment-list.py; python3 -I /tmp/U116-scan-comment-list.py; echo "exit=$?"`. The list reads, prints zero patterns and refuses:

```text
# Words records-sync.sh refuses to publish (U101). Never copied.
29c29
< REDACT_LIST = "~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/redact-words.txt"
---
> REDACT_LIST = "/tmp/U116-redact-comment-only.txt"
token from gh auth token patterns=1
redact list /tmp/U116-redact-comment-only.txt patterns=0
scan REFUSED: redact list /tmp/U116-redact-comment-only.txt holds no pattern
exit=2
```

Fourth, the output directory renamed away and renamed back: `mv "$TMPDIR/U116-out-5" "$TMPDIR/U116-out-5.away" && python3 -I /tmp/U116-scan.py; echo "exit=$?"; mv "$TMPDIR/U116-out-5.away" "$TMPDIR/U116-out-5"; ls -d "$TMPDIR/U116-out-5" > /dev/null && echo "restored"`. `os.scandir` raises:

```text
token from gh auth token patterns=1
redact list ~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/redact-words.txt patterns=5
scan REFUSED: FileNotFoundError: [Errno 2] No such file or directory: 'U116-out-5'
exit=2
restored
```

Fifth, the count constant off by one: `sed 's/^EXPECTED_FILES = 23$/EXPECTED_FILES = 22/' /tmp/U116-scan.py > /tmp/U116-scan-22.py; diff /tmp/U116-scan.py /tmp/U116-scan-22.py; python3 -I /tmp/U116-scan-22.py; echo "exit=$?"`:

```text
24c24
< EXPECTED_FILES = 23
---
> EXPECTED_FILES = 22
token from gh auth token patterns=1
redact list ~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/redact-words.txt patterns=5
scan REFUSED: found 23 .txt files, expected 22
exit=2
```

Positive control, not a failure injection but proof that the redact class matches real data: a copy in which the raw outputs are scanned for both classes, `sed 's/count_matches(path, \[token_class\])  # raw outputs: token only/count_matches(path, [token_class, redact_class])/' /tmp/U116-scan.py > /tmp/U116-scan-control.py; diff /tmp/U116-scan.py /tmp/U116-scan-control.py; python3 -I /tmp/U116-scan-control.py; echo "exit=$?"`. It finds the login name in the owner column of the three `ls -la` listings (3 matches each, 9 in all), reports `scan FOUND` and exits `1`; only counts leave the process, never the matched text. The two documents count 0 for both classes:

```text
155c155
<         total += count_matches(path, [token_class])  # raw outputs: token only
---
>         total += count_matches(path, [token_class, redact_class])
token from gh auth token patterns=1
redact list ~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/redact-words.txt patterns=5
U116-out-5/a-version.receipt.txt token=0 redact=0
U116-out-5/a-version.txt token=0 redact=0
U116-out-5/b-lock-dry-run.receipt.txt token=0 redact=0
U116-out-5/b-lock-dry-run.txt token=0 redact=0
U116-out-5/c-lock-dry-run-4-platforms.receipt.txt token=0 redact=0
U116-out-5/c-lock-dry-run-4-platforms.txt token=0 redact=0
U116-out-5/d-lock-bump-json.receipt.txt token=0 redact=0
U116-out-5/d-lock-bump-json.txt token=0 redact=0
U116-out-5/e-npm-package-manager.receipt.txt token=0 redact=0
U116-out-5/e-npm-package-manager.txt token=0 redact=0
U116-out-5/f-minimum-release-age.receipt.txt token=0 redact=0
U116-out-5/f-minimum-release-age.txt token=0 redact=0
U116-out-5/g-none-written.txt token=0 redact=0
U116-out-5/g-real-after.receipt.txt token=0 redact=0
U116-out-5/g-real-after.txt token=0 redact=3
U116-out-5/g-scratch-after.receipt.txt token=0 redact=0
U116-out-5/g-scratch-after.txt token=0 redact=3
U116-out-5/help-lock.receipt.txt token=0 redact=0
U116-out-5/help-lock.txt token=0 redact=0
U116-out-5/real-before.txt token=0 redact=3
U116-out-5/real-dirs-mtime-after.txt token=0 redact=0
U116-out-5/real-dirs-mtime-before.txt token=0 redact=0
U116-out-5/scratch-tree.txt token=0 redact=0
/tmp/dotfiles-wt/U116/.orchestration/orchestrate/regime-cutover/handoff/evaluations/U116-mise-lock.md token=0 redact=0
/tmp/dotfiles-wt/U116-pr-body.md token=0 redact=0
scan FOUND (25 files, 9 matches)
exit=1
```

No-producer, no-swallow and no-wrapper check (the ROUND 5 AMENDMENT, extended by the ROUND 6 and ROUND 7 amendments): one file, `/tmp/U116-forms.py`, run as `python3 -I /tmp/U116-forms.py; echo "exit=$?"` from the worktree, reads this file and the PR body in-process and counts three classes of line per document; round 8 routed its two `print` sites (the per-document line and the refusal) through `redact` and changed nothing else in it. Inside fenced `sh` or `bash` blocks: lines that hold a dollar-paren command substitution, a process substitution or a pipe character. Inside fenced `python` blocks: lines that call one of the names the ROUND 6 AMENDMENT lists (`os.path.exists`, `os.path.lexists`, `os.path.isfile`, `os.path.isdir`, `os.path.islink`, `os.path.ismount`, `os.access`, `shutil.which`, any `.exists(`, `.is_file(`, `.is_dir(` or `.is_symlink(` method, which covers `pathlib.Path` and `os.DirEntry`, and any `.get(` lookup, which covers a dictionary default on a required key) and lines that open an `except` clause other than the one-line `except FileNotFoundError:` whose body holds no line beginning `refuse(` or `raise`. Inside both kinds of block, the third count of the ROUND 7 AMENDMENT: lines whose word in command position is a wrapper process, `perl`, `timeout`, `xargs`, `nohup`, `nice` or `setsid` by its basename, or `env` followed by `-i`, or `bash` or `sh` followed by `-c`. For a shell line, read with `shlex`, command position is the first word of each simple command (after `;`, `&&`, `||`, `&` or the pipe character; leading `NAME=value` words skipped; a redirection operator and the word after it are not command words). For a Python block, read with `tokenize`, it is the first string element of a list literal (a subscript is told apart by the token before the bracket) or the first word of a string handed to `subprocess.run`; the string elements after it are read too, an f-string as its source text, so `env -i` counts with its flag, and behind `env` the next command word, its options and `NAME=value` words skipped, is tested again and counted on its own line. A list whose first element is a name rather than a string, such as the runner's `[MISE, *args]`, has no literal to test; `MISE` is what `resolve_mise` returned. A fence of three or more backticks opens a block and a bare fence at least as long closes it, so the four-backtick fences around this script and around its positive control's script (both hold triple backticks in their text) count as `python` blocks too. It prints the block counts and the three line counts per document; exit 0 when every line count is 0, exit 1 when any is not, exit 2 on any exception (a block `shlex` or `tokenize` cannot read included) or a document that ends inside a fence. The PR body's fenced blocks are all `text`, so its block counts are 0. Run against the round-6 file as committed at `a3efa54a`, the third count is 2, the lines named under The runner above (169, `/usr/bin/env` followed by `-i`, and 179, `perl` behind them); the positive control below pastes that run. The script, then its output:

````python
#!/usr/bin/env python3
# No-producer, no-swallow and no-wrapper check (the ROUND 5, ROUND 6 and
# ROUND 7 amendments). Reads the two documents in this process and
# counts, per document, three classes of line. Inside fenced sh or bash
# blocks: lines that hold a dollar-paren command substitution, a process
# substitution or a pipe character. Inside fenced python blocks: lines
# that call one of the predicates the ROUND 6 AMENDMENT names (an
# existence or type test that returns False on any error, a lookup with a
# default; spelled apart below), and lines that open an except clause
# other than the narrow FileNotFoundError one whose body neither refuses
# nor raises. Inside both kinds of block: lines whose word in command
# position is a wrapper process of the ROUND 7 list. In a shell line,
# read with shlex, command position is the first word of each simple
# command (after `;`, `&&`, `||`, `&` or the pipe character; leading
# NAME=value words skipped). In a Python block, read with tokenize, it is
# the first string element of a list literal or the first word of a
# string handed to subprocess.run; the string elements after it are read
# too, so env -i, bash -c and sh -c count with their flag, and behind env
# the next command word (its options and NAME=value words skipped) is
# tested again and counted on its own line. Prints the block counts and
# the three line counts per document; exit 0 when every line count is 0,
# exit 1 when any is not, exit 2 on any exception (a block that shlex or
# tokenize cannot read included) or on a document that ends inside a
# fence, before a result line for that document. Every printed line,
# refusals included, passes through redact().
import ast
import getpass
import io
import keyword
import os
import shlex
import sys
import tokenize

DOCUMENTS = (
    "/tmp/dotfiles-wt/U116/.orchestration/orchestrate/regime-cutover/handoff/evaluations/U116-mise-lock.md",
    "/tmp/dotfiles-wt/U116-pr-body.md",
)
# Spelled apart so this script, pasted into the evaluation file, does not
# hold the forms it counts.
MARKS = ("$" + "(", "<" + "(", chr(124))
SHELL = ("sh", "bash")
PYTHON = ("python", "python3", "py")
NAMES = tuple(
    ".".join(parts) + "("
    for parts in (
        ("os", "path", "exists"),
        ("os", "path", "lexists"),
        ("os", "path", "isfile"),
        ("os", "path", "isdir"),
        ("os", "path", "islink"),
        ("os", "path", "ismount"),
        ("os", "access"),
        ("shutil", "which"),
        ("", "exists"),
        ("", "is_file"),
        ("", "is_dir"),
        ("", "is_symlink"),
        ("", "get"),
    )
)
NARROW = "except FileNotFoundError:"
REFUSALS = ("refuse(", "raise")
# The wrapper words of the ROUND 7 AMENDMENT, matched against the basename
# of the word in command position; env, bash and sh count when the word
# after them is the listed flag. Spelled apart like MARKS above.
WRAPPERS = tuple("".join(parts) for parts in (("pe", "rl"), ("time", "out"), ("xa", "rgs"), ("no", "hup"), ("ni", "ce"), ("set", "sid")))
FLAGGED = {"env": "-i", "ba" + "sh": "-c", "sh": "-c"}
SHELL_BREAKS = (";", "&&", "||", "&", chr(124))
QUIET = (tokenize.NL, tokenize.NEWLINE, tokenize.COMMENT, tokenize.INDENT, tokenize.DEDENT)
RUN_CALL = ["subprocess", ".", "run", "("]


def redactions():
    # The strings redact() replaces, longest first so a home path is
    # replaced before the login name inside it: the real home directory in
    # both spellings (the resolved path of ~, and HOME when it is set) as
    # ~, and the login name (getpass, and USER when it is set) as <user>.
    # The optional variables are read by membership and index, not by a
    # lookup with a default.
    homes = [os.path.realpath(os.path.expanduser("~"))]
    if "HOME" in os.environ:
        homes.append(os.environ["HOME"])
    users = [getpass.getuser()]
    if "USER" in os.environ:
        users.append(os.environ["USER"])
    pairs = [(home, "~") for home in homes if len(home) > 1] + [(user, "<user>") for user in users if user]
    pairs.sort(key=lambda pair: len(pair[0]), reverse=True)
    return tuple(dict.fromkeys(pairs))


REDACTIONS = redactions()


def redact(text):
    # Every string that reaches stdout or stderr passes through here,
    # refusals and receipts included.
    for literal, replacement in REDACTIONS:
        text = text.replace(literal, replacement)
    return text


def refuse(message):
    print(redact(f"check REFUSED: {message}"))
    sys.exit(2)


def indent_of(text):
    return len(text) - len(text.lstrip(" "))


def fence_of(text):
    # (fence length, info string) for a line that opens or closes a
    # backtick fence; None for any other line.
    stripped = text.lstrip(" ")
    if not stripped.startswith("```"):
        return None
    length = len(stripped) - len(stripped.lstrip("`"))
    return length, stripped[length:].strip().split(" ")[0]


def swallows(block, index):
    # True when block[index] opens an except clause other than the narrow
    # one and no line of its body starts with refuse( or raise.
    head = block[index].strip()
    if not (head == "except:" or head.startswith("except ")):
        return False
    if head == NARROW:
        return False
    indent = indent_of(block[index])
    for later in block[index + 1 :]:
        if not later.strip():
            continue
        if indent_of(later) <= indent:
            break
        if later.strip().startswith(REFUSALS):
            return False
    return True


def is_assignment(word):
    return "=" in word and word.split("=")[0].isidentifier()


def wrapper_indices(words, start=0):
    # Indices into words of every wrapper in command position: the first
    # word behind the NAME=value words (its basename against the list, or
    # env, bash or sh with its flag next), and behind env, its options and
    # NAME=value words skipped, the next command word again.
    index = start
    while index < len(words) and is_assignment(words[index]):
        index += 1
    if index >= len(words):
        return []
    head = os.path.basename(words[index])
    flagged = head in FLAGGED and index + 1 < len(words) and words[index + 1] == FLAGGED[head]
    found = [index] if head in WRAPPERS or flagged else []
    if head == "env":
        index += 1
        while index < len(words) and words[index].startswith("-"):
            index += 1
        found += wrapper_indices(words, index)
    return found


def shell_wrapper_lines(block):
    # Lines of a shell block holding a simple command whose word in
    # command position is a wrapper. A redirection operator and the word
    # after it are not command words.
    found = 0
    for text in block:
        lexer = shlex.shlex(text, posix=True, punctuation_chars=True)
        lexer.whitespace_split = True
        commands = [[]]
        skip = False
        for token in lexer:
            if token in SHELL_BREAKS or token in ("(", ")"):
                commands.append([])
                skip = False
            elif all(char in "<>&" for char in token):
                skip = True
            elif skip:
                skip = False
            else:
                commands[-1].append(token)
        if any(wrapper_indices(words) for words in commands):
            found += 1
    return found


def string_elements(tokens, index):
    # The run of string elements that starts at tokens[index] and
    # continues over commas: (text, line) pairs, an f-string read as its
    # source text, a bytes literal decoded. Stops at the first other token.
    elements = []
    position = index
    while position < len(tokens):
        current = tokens[position]
        if current.type == tokenize.STRING:
            value = ast.literal_eval(current.string)
            elements.append((value.decode() if isinstance(value, bytes) else value, current.start[0]))
            position += 1
        elif current.type == tokenize.FSTRING_START:
            start = position
            while tokens[position].type != tokenize.FSTRING_END:
                position += 1
            elements.append(("".join(piece.string for piece in tokens[start + 1 : position]), current.start[0]))
            position += 1
        else:
            break
        if position < len(tokens) and tokens[position].string == ",":
            position += 1
        else:
            break
    return elements


def opens_list(tokens, index):
    # True when tokens[index] is a `[` that opens a list literal rather
    # than a subscript: the token before it is not a name (keywords
    # aside), a closing bracket or a string.
    if tokens[index].string != "[":
        return False
    if index == 0:
        return True
    earlier = tokens[index - 1]
    if earlier.type in (tokenize.STRING, tokenize.FSTRING_END) or earlier.string in (")", "]"):
        return False
    return not (earlier.type == tokenize.NAME and not keyword.iskeyword(earlier.string))


def python_wrapper_lines(block):
    # Lines of a Python block holding a wrapper in command position: in a
    # list literal whose first element is a string, or in the string
    # handed to subprocess.run.
    source = "\n".join(block) + "\n"
    tokens = [token for token in tokenize.generate_tokens(io.StringIO(source).readline) if token.type not in QUIET]
    lines = set()
    for index, token in enumerate(tokens):
        if index == 0 or token.type not in (tokenize.STRING, tokenize.FSTRING_START):
            continue
        if opens_list(tokens, index - 1):
            elements = string_elements(tokens, index)
            words = [text for text, line in elements]
            for found in wrapper_indices(words):
                lines.add(elements[found][1])
        elif [item.string for item in tokens[max(0, index - 4) : index]] == RUN_CALL:
            elements = string_elements(tokens, index)
            if elements and wrapper_indices(shlex.split(elements[0][0])):
                lines.add(elements[0][1])
    return len(lines)


def count(path):
    with open(path, encoding="utf-8") as handle:
        lines = handle.read().split("\n")
    state = None  # None outside a fence; else (kind, fence length)
    block = []
    shell_blocks = python_blocks = producer = swallow = wrapper = 0
    for text in lines:
        fence = fence_of(text)
        if state is None:
            if fence is not None:
                length, info = fence
                kind = "shell" if info in SHELL else "python" if info in PYTHON else "other"
                shell_blocks += kind == "shell"
                python_blocks += kind == "python"
                state = (kind, length)
                block = []
            continue
        kind, length = state
        if fence is not None and fence[1] == "" and fence[0] >= length:
            if kind == "shell":
                producer += sum(1 for line in block if any(mark in line for mark in MARKS))
                wrapper += shell_wrapper_lines(block)
            if kind == "python":
                swallow += sum(1 for line in block if any(name in line for name in NAMES))
                swallow += sum(1 for index in range(len(block)) if swallows(block, index))
                wrapper += python_wrapper_lines(block)
            state = None
            continue
        block.append(text)
    if state is not None:
        raise ValueError(f"{path} ends inside a fenced block")
    print(redact(f"{path} shell-blocks={shell_blocks} producer-lines={producer} python-blocks={python_blocks} swallow-lines={swallow} wrapper-lines={wrapper}"))
    return producer + swallow + wrapper


def main():
    total = sum(count(path) for path in DOCUMENTS)
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        refuse(f"{type(exc).__name__}: {exc}")
````

```text
/tmp/dotfiles-wt/U116/.orchestration/orchestrate/regime-cutover/handoff/evaluations/U116-mise-lock.md shell-blocks=7 producer-lines=0 python-blocks=8 swallow-lines=0 wrapper-lines=0
/tmp/dotfiles-wt/U116-pr-body.md shell-blocks=0 producer-lines=0 python-blocks=0 swallow-lines=0 wrapper-lines=0
exit=0
```

Its positive control: `/tmp/U116-forms-inject-8.py` (the round-7 script with its printed lines and `SystemExit` messages routed through `redact`, nothing else) writes `/tmp/U116-forms-control.md`, a copy of this file with two lines inserted after its first `sh` fence (a pipeline, `true`, a pipe, `true`; and `timeout 5 true`) and two after its first `python` fence (a call of the second name of the ROUND 6 list on the lockfile path; and a `subprocess.run` list whose first element is `perl`, with the round-6 arguments behind it), writes `/tmp/U116-forms-r6.md`, the round-6 file as committed at `a3efa54a`, from one `subprocess.run` of `git show` whose status it reads, and writes `/tmp/U116-forms-control.py`, the check with its two document paths replaced in-process by those two files; it prints what it inserted and replaced. The check over those two files then counts, in the injected copy, one producer line, one swallow line and two wrapper lines, and in the round-6 file as committed, no producer line, no swallow line and the two wrapper lines of its runner, and exits `1`. The injection script, the two commands from the worktree, and their outputs:

````python
#!/usr/bin/env python3
# Positive control for the no-producer, no-swallow and no-wrapper check.
# Writes three files. /tmp/U116-forms-control.md is a copy of the
# evaluation file with two lines inserted after its first sh fence (a
# pipeline, and a timeout-wrapped command) and two after its first python
# fence (an error-swallowing predicate call, and a subprocess.run list
# whose first element is perl). /tmp/U116-forms-r6.md is the round-6 file
# as committed at a3efa54a, written from one subprocess.run of git show
# with its status read, the file whose wrapper lines the ROUND 7
# AMENDMENT names. /tmp/U116-forms-control.py is the check with its two
# document paths replaced by those two files. Prints what it inserted and
# replaced. Any failure raises; nothing here is caught. The injected
# lines are spelled apart below so that this script, pasted into the
# evaluation file, holds none of the forms the check counts. Every
# printed line and every SystemExit message passes through redact().
import getpass
import os
import subprocess
import sys

WORKTREE = "/tmp/dotfiles-wt/U116"
RELATIVE = ".orchestration/orchestrate/regime-cutover/handoff/evaluations/U116-mise-lock.md"
SOURCE = f"{WORKTREE}/{RELATIVE}"
CHECK = "/tmp/U116-forms.py"
CONTROL_MD = "/tmp/U116-forms-control.md"
ROUND6_MD = "/tmp/U116-forms-r6.md"
CONTROL_PY = "/tmp/U116-forms-control.py"
PR_BODY = "/tmp/dotfiles-wt/U116-pr-body.md"
PIPE = chr(124)
WRAPPED = "time" + "out 5 true\n"
SWALLOW = "if os.path." + "lexists(LOCK):\n"
PERL = 'subprocess.run(["pe' + 'rl", "-e", "alarm 900; exec @ARGV", "mise", "--version"])\n'
INJECTED = {
    "```sh": [f"true {PIPE} true\n", WRAPPED],
    "```python": [SWALLOW, PERL],
}


def redactions():
    # The strings redact() replaces, longest first so a home path is
    # replaced before the login name inside it: the real home directory in
    # both spellings (the resolved path of ~, and HOME when it is set) as
    # ~, and the login name (getpass, and USER when it is set) as <user>.
    # The optional variables are read by membership and index, not by a
    # lookup with a default.
    homes = [os.path.realpath(os.path.expanduser("~"))]
    if "HOME" in os.environ:
        homes.append(os.environ["HOME"])
    users = [getpass.getuser()]
    if "USER" in os.environ:
        users.append(os.environ["USER"])
    pairs = [(home, "~") for home in homes if len(home) > 1] + [(user, "<user>") for user in users if user]
    pairs.sort(key=lambda pair: len(pair[0]), reverse=True)
    return tuple(dict.fromkeys(pairs))


REDACTIONS = redactions()


def redact(text):
    # Every string that reaches stdout or stderr passes through here,
    # refusals and receipts included.
    for literal, replacement in REDACTIONS:
        text = text.replace(literal, replacement)
    return text

with open(SOURCE, encoding="utf-8") as handle:
    lines = handle.readlines()
for fence, inserts in INJECTED.items():
    for index, line in enumerate(lines):
        if line.rstrip("\n") == fence:
            for offset, text in enumerate(inserts, 1):
                lines.insert(index + offset, text)
                print(redact(f"{CONTROL_MD}: inserted at line {index + offset + 1}: {text.rstrip()}"))
            break
    else:
        raise SystemExit(redact(f"no {fence} fence found"))
with open(CONTROL_MD, "w", encoding="utf-8") as handle:
    handle.writelines(lines)

with open(ROUND6_MD, "wb") as handle:
    proc = subprocess.run(
        ["git", "-C", WORKTREE, "show", f"a3efa54a:{RELATIVE}"],
        stdout=handle,
        stderr=subprocess.PIPE,
        check=False,
        timeout=60,
    )
if proc.returncode != 0:
    raise SystemExit(redact(f"git show exited {proc.returncode}: {proc.stderr.decode()}"))
print(redact(f"{ROUND6_MD}: git show a3efa54a:{RELATIVE} exit=0"))

with open(CHECK, encoding="utf-8") as handle:
    check = handle.read()
for old, new in ((SOURCE, CONTROL_MD), (PR_BODY, ROUND6_MD)):
    if check.count(f'    "{old}",\n') != 1:
        raise SystemExit(redact(f"{CHECK} does not name {old} once"))
    check = check.replace(f'    "{old}",\n', f'    "{new}",\n')
    print(redact(f"{CONTROL_PY}: {old} replaced by {new}"))
with open(CONTROL_PY, "w", encoding="utf-8") as handle:
    handle.write(check)
sys.exit(0)
````

```sh
python3 -I /tmp/U116-forms-inject-8.py; echo "exit=$?"
python3 -I /tmp/U116-forms-control.py; echo "exit=$?"
```

```text
/tmp/U116-forms-control.md: inserted at line 122: true | true
/tmp/U116-forms-control.md: inserted at line 123: timeout 5 true
/tmp/U116-forms-control.md: inserted at line 20: if os.path.lexists(LOCK):
/tmp/U116-forms-control.md: inserted at line 21: subprocess.run(["perl", "-e", "alarm 900; exec @ARGV", "mise", "--version"])
/tmp/U116-forms-r6.md: git show a3efa54a:.orchestration/orchestrate/regime-cutover/handoff/evaluations/U116-mise-lock.md exit=0
/tmp/U116-forms-control.py: /tmp/dotfiles-wt/U116/.orchestration/orchestrate/regime-cutover/handoff/evaluations/U116-mise-lock.md replaced by /tmp/U116-forms-control.md
/tmp/U116-forms-control.py: /tmp/dotfiles-wt/U116-pr-body.md replaced by /tmp/U116-forms-r6.md
exit=0
/tmp/U116-forms-control.md shell-blocks=7 producer-lines=1 python-blocks=8 swallow-lines=1 wrapper-lines=2
/tmp/U116-forms-r6.md shell-blocks=4 producer-lines=0 python-blocks=4 swallow-lines=0 wrapper-lines=2
exit=1
```

What the scratch home holds after the run, `scratch-tree.txt`, written by the runner from an in-process walk of `$TMPDIR/U116-home-5` four directory levels deep (the files inside a fourth-level directory included; a directory the walk cannot read raises instead of being skipped), the prefix written as `$TMPDIR`:

```text
$TMPDIR/U116-home-5
$TMPDIR/U116-home-5/.cache
$TMPDIR/U116-home-5/.cache/mise
$TMPDIR/U116-home-5/.cache/mise/cargo-eza
$TMPDIR/U116-home-5/.cache/mise/cargo-eza/remote_versions-cfe45.msgpack.z
$TMPDIR/U116-home-5/.cache/mise/cargo-pueue
$TMPDIR/U116-home-5/.cache/mise/cargo-pueue/remote_versions-711b5.msgpack.z
$TMPDIR/U116-home-5/.cache/mise/github
$TMPDIR/U116-home-5/.cache/mise/github-cli-cli
$TMPDIR/U116-home-5/.cache/mise/github-cli-cli/remote_versions-fbf2d.msgpack.z
$TMPDIR/U116-home-5/.cache/mise/github/https-api-github-com-astral-sh-uv-latest-75f152cbb3234e33-hosted-2-2f6a0.msgpack.z
$TMPDIR/U116-home-5/.cache/mise/github/https-api-github-com-cli-cli-latest-c422894432b07a75-hosted-2-2f6a0.msgpack.z
$TMPDIR/U116-home-5/.cache/mise/github/https-api-github-com-cli-cli-versions-fdcb0a0009af6507-2f6a0.msgpack.z
$TMPDIR/U116-home-5/.cache/mise/github/https-api-github-com-d-kuro-gwq-latest-6c17f18eaf4e3a2b-hosted-2-2f6a0.msgpack.z
$TMPDIR/U116-home-5/.cache/mise/github/https-api-github-com-dotenvx-dotenvx-latest-851010c943271a76-hosted-2-2f6a0.msgpack.z
$TMPDIR/U116-home-5/.cache/mise/github/https-api-github-com-filo-sottile-age-latest-5aaeb641c690722-hosted-2-2f6a0.msgpack.z
$TMPDIR/U116-home-5/.cache/mise/github/https-api-github-com-gohugoio-hugo-latest-7e8a758b278d01f5-hosted-2-2f6a0.msgpack.z
$TMPDIR/U116-home-5/.cache/mise/github/https-api-github-com-jqlang-jq-latest-bdd9320085deaae5-hosted-2-2f6a0.msgpack.z
$TMPDIR/U116-home-5/.cache/mise/github/https-api-github-com-micro-editor-micro-latest-e2cefac8305717dd-hosted-2-2f6a0.msgpack.z
$TMPDIR/U116-home-5/.cache/mise/github/https-api-github-com-mikefarah-yq-latest-a3188cde7430c1ee-hosted-2-2f6a0.msgpack.z
$TMPDIR/U116-home-5/.cache/mise/github/https-api-github-com-ogulcancelik-herdr-latest-b515115e6d3664ca-hosted-2-2f6a0.msgpack.z
$TMPDIR/U116-home-5/.cache/mise/github/https-api-github-com-sharkdp-fd-latest-a69cff9e0d9ad20b-hosted-2-2f6a0.msgpack.z
$TMPDIR/U116-home-5/.cache/mise/github/https-api-github-com-sxyazi-yazi-latest-29d17fd18245505c-hosted-2-2f6a0.msgpack.z
$TMPDIR/U116-home-5/.cache/mise/github/https-api-github-com-twpayne-chezmoi-latest-ab43663cda310c28-hosted-2-2f6a0.msgpack.z
$TMPDIR/U116-home-5/.cache/mise/github/https-api-github-com-watchexec-watchexec-latest-130a48c37d16befe-hosted-2-2f6a0.msgpack.z
$TMPDIR/U116-home-5/.cache/mise/github/https-api-github-com-x-motemen-ghq-latest-1d789ce64118519b-hosted-2-2f6a0.msgpack.z
$TMPDIR/U116-home-5/.cache/mise/http-bats
$TMPDIR/U116-home-5/.cache/mise/http-gcloud
$TMPDIR/U116-home-5/.cache/mise/http-ruff
$TMPDIR/U116-home-5/.cache/mise/http-shellcheck
$TMPDIR/U116-home-5/.cache/mise/http-shfmt
$TMPDIR/U116-home-5/.cache/mise/latest-version.releases-v1
$TMPDIR/U116-home-5/.cache/mise/node
$TMPDIR/U116-home-5/.cache/mise/node/remote_versions-73876.msgpack.z
$TMPDIR/U116-home-5/.cache/mise/npm-anthropic-ai-claude-code
$TMPDIR/U116-home-5/.cache/mise/npm-anthropic-ai-claude-code/latest_version-999a7.msgpack.z
$TMPDIR/U116-home-5/.cache/mise/npm-anthropic-ai-claude-code/remote_versions-999a7.msgpack.z
$TMPDIR/U116-home-5/.cache/mise/npm-anthropic-ai-sandbox-runtime
$TMPDIR/U116-home-5/.cache/mise/npm-anthropic-ai-sandbox-runtime/latest_version-dab3a.msgpack.z
$TMPDIR/U116-home-5/.cache/mise/npm-anthropic-ai-sandbox-runtime/remote_versions-dab3a.msgpack.z
$TMPDIR/U116-home-5/.cache/mise/npm-bash-language-server
$TMPDIR/U116-home-5/.cache/mise/npm-bash-language-server/latest_version-1b050.msgpack.z
$TMPDIR/U116-home-5/.cache/mise/npm-bash-language-server/remote_versions-1b050.msgpack.z
$TMPDIR/U116-home-5/.cache/mise/npm-fast-cli
$TMPDIR/U116-home-5/.cache/mise/npm-fast-cli/latest_version-81575.msgpack.z
$TMPDIR/U116-home-5/.cache/mise/npm-fast-cli/remote_versions-81575.msgpack.z
$TMPDIR/U116-home-5/.cache/mise/npm-meta
$TMPDIR/U116-home-5/.cache/mise/npm-meta/origin-3c364d36b2d92b17
$TMPDIR/U116-home-5/.cache/mise/npm-meta/origin-3c364d36b2d92b17/@anthropic-ai__claude-code.json
$TMPDIR/U116-home-5/.cache/mise/npm-meta/origin-3c364d36b2d92b17/@anthropic-ai__sandbox-runtime.json
$TMPDIR/U116-home-5/.cache/mise/npm-meta/origin-3c364d36b2d92b17/@openai__codex.json
$TMPDIR/U116-home-5/.cache/mise/npm-meta/origin-3c364d36b2d92b17/bash-language-server.json
$TMPDIR/U116-home-5/.cache/mise/npm-meta/origin-3c364d36b2d92b17/fast-cli.json
$TMPDIR/U116-home-5/.cache/mise/npm-meta/origin-3c364d36b2d92b17/pyright.json
$TMPDIR/U116-home-5/.cache/mise/npm-openai-codex
$TMPDIR/U116-home-5/.cache/mise/npm-openai-codex/latest_version-50bdb.msgpack.z
$TMPDIR/U116-home-5/.cache/mise/npm-openai-codex/remote_versions-50bdb.msgpack.z
$TMPDIR/U116-home-5/.cache/mise/npm-pyright
$TMPDIR/U116-home-5/.cache/mise/npm-pyright/latest_version-30d9a.msgpack.z
$TMPDIR/U116-home-5/.cache/mise/npm-pyright/remote_versions-30d9a.msgpack.z
$TMPDIR/U116-home-5/.cache/mise/python
$TMPDIR/U116-home-5/.cache/mise/python/remote_versions-ee8bb.msgpack.z
$TMPDIR/U116-home-5/.cache/mise/uv
$TMPDIR/U116-home-5/.cache/mise/uv/remote_versions-3ed32.msgpack.z
$TMPDIR/U116-home-5/.cache/mise/versions-index
$TMPDIR/U116-home-5/.cache/mise/versions-index/index.v1
$TMPDIR/U116-home-5/.cache/mise/versions-index/index.v1.validated
$TMPDIR/U116-home-5/.config
$TMPDIR/U116-home-5/.config/mise
$TMPDIR/U116-home-5/.config/mise/config.toml
$TMPDIR/U116-home-5/.local
$TMPDIR/U116-home-5/.local/share
$TMPDIR/U116-home-5/.local/state
$TMPDIR/U116-home-5/.local/state/mise
$TMPDIR/U116-home-5/.local/state/mise/incomplete-installs
$TMPDIR/U116-home-5/.local/state/mise/incomplete-installs/.migrated
$TMPDIR/U116-home-5/.local/state/mise/tracked-configs
$TMPDIR/U116-home-5/.local/state/mise/tracked-configs/dcb01309670eb950
```

## Measured facts

### From the outputs

| Run                                           | Platforms       | Tools | Entries mise would write             | Elapsed | Exit |
| --------------------------------------------- | --------------- | ----- | ------------------------------------ | ------- | ---- |
| (b) default platform set                      | 7               | 36    | 258                                  | 2 s     | 0    |
| (c) the four platforms the `http:` tables pin | 4               | 36    | 149                                  | 0 s     | 0    |
| (d) `--bump --json`                           | 7 (same target) | 36    | 36 objects, all `old_versions` empty | 0 s     | 0    |

- **Platforms.** With no `lockfile_platforms` setting and no existing lockfile, mise targets `linux-arm64, linux-arm64-musl, linux-x64, linux-x64-musl, macos-arm64, macos-x64, windows-x64` (first line of (b)). That is the vendor's new-lockfile set from the reference page, and it matches the "7 platforms" of row 233.
- **Entries.** (b) lists 258 `✓` lines: 36 tools times 7 platforms is 252, and bun adds six more keys (`linux-x64-baseline`, `linux-x64-musl-baseline`, `macos-x64-baseline`, `windows-x64-baseline`, and `linux-arm64-musl` and `linux-x64-musl` listed a second time). (c) lists 149: 144 plus bun's `linux-arm64-musl`, `linux-x64-baseline`, `linux-x64-musl`, `linux-x64-musl-baseline` and `macos-x64-baseline`. Counted with `grep -c '^  ✓'` on the two files.
- **Backends.** Every one of the 36 tools resolved, each to the version round 6 resolved an hour earlier (the one move between rounds 5 and 6, `python@3.15.1` to `python@3.15.2`, stands; no version moved between rounds 6 and 7): 4 core (`node`, `rust`, `python`, `bun`), 11 aqua (`age`, `chezmoi`, `dotenvx`, `fd`, `jq`, `hugo-extended`, `uv`, `yazi`, `micro`, `yq`, `watchexec`; the backend names come from the `backend` field of (d)), 10 npm, 4 github, 2 cargo, 5 http. No line reports a failure, a skipped platform or a rate limit, and no run needed `MISE_GITHUB_TOKEN`.
- **What a bump would move today.** Nothing moves: every object in (d) has `"old_versions": []`, because no lockfile exists. The 36 `new_versions` equal the versions (b) resolved, so today's bump PR would be the first write of the file, not an update. The exact pins resolve to themselves (`npm:ccstatusline@2.2.32`, `npm:ccusage@20.0.37`, `npm:prettier@3.9.10`, `npm:pnpm@12.8.1`, the five `http:` tools), as the vendor says for `--bump`.
- **Elapsed.** (b) took 2 s wall time; this is the one measured number of this table the round-7 re-take moved (round 6 measured 4 s, round 5 5 s, the round-1 run that rounds 1 to 4 pasted 8 s), every count in this section being unchanged. (c) and (d) returned in under a second because mise reused the version lists (b) had cached under the scratch `~/.cache/mise` (the `remote_versions-*.msgpack.z` files in the scratch tree). The brief's estimate of "about 36 tools per platform over the network" taking minutes did not hold: mise resolves a version once per tool, not once per platform, and the dry run downloads no artifact.
- **Hosts contacted.** No packet capture was taken. The cache file names show `api.github.com` (sixteen `github/https-api-github-com-*` entries), the mise versions index (`versions-index/index.v1`) and an npm registry origin (`npm-meta/origin-*`, which in this run holds one metadata file for each of the six unheld `npm:` tools and none for the four held ones). All are in the brief's host list. Whether any other host was contacted is unverified.
- **Nothing written.** The scratch `~/.config/mise` holds `config.toml` alone before and after, and `none-written` printed. The real `~/.config/mise` holds the same single entry before and after (`config.toml`, 6962 bytes, dated Oct 26 23:40, no `mise.lock`), and `cmp` under Further checks reports the before and after listings byte for byte equal. The modification times of the real `~/.config/mise`, `~/.local/share/mise`, `~/Library/Caches/mise` and `~/.local/state/mise` are identical before and after the run; the `~/.config/mise` stamp is the one every round recorded. All five stamps are the ones round 6 recorded (three of them later than round 5's, each a change that happened before the round-6 run started, as that round's before file showed); nothing moved between round 6 and this run, and this unit's runs hand mise an environment of the CHANGE 1 variables alone, every mise directory variable pointed inside the scratch home. mise wrote only under the scratch home: version-list caches under `.cache/mise` and the `tracked-configs` and `incomplete-installs` directories under `.local/state/mise`.
- **Settings.** `npm.package_manager` is `npm` and `minimum_release_age` is `72h` in the copy, as `config.toml:112-113` and `:107` set them.
- **Attempt 1 (round 1, not re-taken).** With the cwd under the real home, mise read the real `~/.config/mise/config.toml` as an untrusted project config and stopped. The file was opened, not changed (its listing and mtime are unchanged). This is the one way the unit touched a real mise path, and it is a property of mise's config discovery, not of `HOME`.

### From the tree

1. `tests/unit/test_supply_chain_policy.py:444-462` renders `home/dot_config/mise/config.toml.tmpl` with chezmoi and asserts the result equals `home/dot_mise/config.toml` byte for byte.
2. `home/dot_mise/config.toml:3-43` requests `latest` for every tool that is not held; `:26-36` hold ccstatusline, ccusage, prettier and pnpm at exact versions with a one-line reason above each; `:46-103` hold the five `http:` tools with per-platform URL and sha256 tables at `:60-64`, `:73-77`, `:86-90` and `:99-103`.
3. `README.md:199-202` states that only a held tool commits a version and that there is no `mise.lock`; `README.md:250-255` names the trade-off (machines may differ in tool versions, CI tests the latest safe versions) and that the applied file no longer turns on lockfile mode for other projects.
4. `home/.chezmoiremove:21` is `.config/mise/mise.lock`: chezmoi deletes the rendered lockfile on every apply.
5. `tests/unit/test_supply_chain_policy.py:404-421` asserts that `lockfile`, `locked` and `lockfile_platforms` are absent from `[settings]` (`:408-409`), that `home/dot_mise/mise.lock` and `home/dot_config/mise/mise.lock.tmpl` do not exist (`:419-420`) and that `.chezmoiremove` lists the rendered lock (`:421`). `:464-466` asserts that `install/common/mise.sh`, `Makefile` and `scripts/update-agent-assets.sh` contain no `--locked`.
6. `.github/workflows/test.yaml:259-261` copies `home/dot_mise/config.toml` alone to `RUNNER_TEMP/statusline-mise/mise.toml`; `:263-270` runs `jdx/mise-action` with `install: false`; `:276-279` installs node, the statusline tools, ruff and prettier with `mise -C "${RUNNER_TEMP}/statusline-mise" install …`.
7. `scripts/upgrade-tools.sh:318` runs `mise upgrade --yes <tool>` for each tool that is neither an `http:` pin nor held.
8. `scripts/update-agent-assets.sh:148` repairs a broken agent CLI with `MISE_NPM_PACKAGE_MANAGER=npm mise install --force <tool>`, and `tests/unit/test_runtime_health.py:249` and `:347` assert that exact call with the npm installer.

### From the vendor pages, read 2026-10-29

- <https://mise.jdx.dev/dev-tools/mise-lock.html>: "`mise.lock` records the exact versions that the requests in `mise.toml` resolved to, with download URLs and checksums where the backend provides them. Commit it next to `mise.toml` so every machine and CI job installs the same tools." "`mise install --locked` fails instead of resolving a version when the lockfile has no matching entry, which catches an incomplete lockfile in CI". On the setting: "`true` in a config file: mise creates lockfiles and keeps them up to date." and "only `lockfile = true` in a config file turns on automatic creation." On graphs: "Format version 2 and later lock the transitive dependencies of npm and PyPI tools, not only their top-level version. mise stores each graph in the package manager's own format, `aube-lock.yaml` for npm tools installed with embedded aube and `uv.lock` for PyPI tools when uv 0.12.10 or newer is installed, in a sidecar directory (`.mise/locks/` by default)." The dotfiles section: "If `~/.config/mise/config.toml` is a symlink into a dotfiles repository, such as `~/dotfiles/mise.toml`, `mise lock` run inside the repository reports that there is nothing to lock, because mise treats the file as global config. Run `mise lock --global` from inside the repository to write `~/dotfiles/mise.lock`. From other directories mise reads and writes `~/.config/mise/mise.lock`, so also symlink that path to `~/dotfiles/mise.lock`. Sidecars follow the symlink target." On the cooldown: "A version recorded in `mise.lock` installs even when it is newer than `minimum_release_age`; the cutoff applies only when mise selects a new version." On CI: "`jdx/mise-action` adds `--locked` itself when the repository has a `mise.lock`." The command table lists `mise upgrade` and `mise upgrade node` as updating `mise.lock` ("Yes"), and the backend table lists "npm (embedded aube) and pypi (uv)" as recording "The version, plus a dependency graph in format version 2 and later" and "cargo, dotnet, gem, go, spinel, core:dotnet, core:rust" as "The top-level version only".
- <https://mise.jdx.dev/dev-tools/mise-lock-reference.html>: format versions 0 (no field), 1 (`specifiers`), 2 ("npm and PyPI dependency graphs in sidecar directories"), 3 (`repository_ids` for packslip tools); "New lockfiles use version 3." Platform keys: "`mise lock` writes these keys for a new lockfile, plus the current platform's: `linux-x64`, `linux-x64-musl`, `linux-arm64`, `linux-arm64-musl`, `macos-x64`, `macos-arm64` and `windows-x64`." and "Bun adds `-baseline` on x64 CPUs without AVX2". Sidecar location for the global lockfile: "`~/.config/mise/mise.lock` (global) | `~/.config/mise/locks/`". "If `mise.lock` is a symlink, mise resolves sidecar paths relative to the symlink's target and writes new sidecars beside it."
- <https://mise.jdx.dev/dev-tools/backends/npm.html>: "With the embedded aube installer, `mise.lock` records each npm tool's full dependency graph (lockfile format 2 or later, which new lockfiles use)." "Other installers cannot replay an embedded-aube graph; use embedded aube, or refresh the lockfile for the installer you select." The installer table maps `npm` to `npm install -g`. "For a locked graph, the cutoff applies when the graph is resolved; installs replay the committed dependencies." No sentence on the page says what the lock records under `package_manager = "npm"`; "version only" follows from the two sentences above (the graph exists only for embedded aube) and from the backend table on the lockfile page, so research 4.2's "inferred" label stays, with these two sentences as its basis.
- <https://mise.jdx.dev/cli/lock.html> and `mise lock --help` above: `--minimum-release-age <AGE>` is documented as "Only lock versions released before a date or at least a duration ago", "It filters only requests that are not exact". `--platform` "Defaults to the `lockfile_platforms` setting plus the current platform when that setting is configured, else the platforms already in the lockfile, else a common set for a new lockfile." `--bump`: "If the remote versions cannot be fetched, it fails rather than keep the locked version."
- <https://raw.githubusercontent.com/jdx/mise-action/main/README.md>: "With a committed `mise.lock`, mise verifies cached downloads against lockfile checksums before use, so a poisoned or stale cache cannot change what gets installed." "If a repo mise lock file such as `mise.lock` is present in the working directory or one of its parents, this action automatically runs `mise install --locked`." "If you provide `mise_toml` or `tool_versions` inputs, the action does not automatically force locked mode."

### The five V4-9 answers

**Where the lock lives under chezmoi.** The dry run names its target as `<HOME>/.config/mise/mise.lock`, beside the global config (first line of (b)), and the reference page puts the global sidecars in `~/.config/mise/locks/`. Under chezmoi the source would be `home/dot_mise/mise.lock` with a `home/dot_config/mise/mise.lock.tmpl` include, the same shape as the config today; both files are forbidden by `test_supply_chain_policy.py:419-420`, and `.chezmoiremove:21` deletes the rendered `~/.config/mise/mise.lock` on every apply. The vendor's command table says `mise upgrade` updates `mise.lock`, so a host `mise upgrade` rewrites the rendered file, and chezmoi then reports that file as drift until the next apply deletes or replaces it. With the embedded installer the sidecar directory `~/.config/mise/locks/` would need the same treatment.

**Whether `make update` becomes `mise lock --bump` in a PR followed by `mise install --locked` on hosts.** Today `scripts/upgrade-tools.sh:318` runs `mise upgrade --yes <tool>` per unheld tool on the host, which is exactly the command that would rewrite the lock. The lockfile workflow replaces that step with a scheduled `mise lock --bump --minimum-release-age 72h` (run (d) shows the shape of its output: one JSON object per moved tool) that opens a PR, and hosts run `mise install --locked` from the applied lock. `README.md:250-255` records the present trade-off on purpose, and `test_supply_chain_policy.py:464-466` forbids `--locked` in the three lifecycle files. The change is therefore a workflow decision for the operator (hosts stop upgrading on their own), not a CI fix, as research 4.4 says.

**How the CI copy step would carry `mise.lock` and `.mise/locks/`.** `test.yaml:259-261` copies one file into `RUNNER_TEMP/statusline-mise/mise.toml`. With a lock, the step also copies `mise.lock` beside it and, under the embedded installer, the sidecar directory as `.mise/locks/` (the project layout the reference page gives for a `mise.lock` beside `mise.toml`). mise-action does not add `--locked` here: it adds the flag when a lockfile sits in the working directory or its parents, and `test.yaml:263-270` runs it with `install: false` on the checkout, not on the copy. The four `mise -C … install` lines at `test.yaml:276-279` would carry `--locked` themselves.

**Whether `package_manager = "npm"` or the embedded installer is wanted.** Run (e) confirms `npm`. Under that setting the lock records the version only, so the npm supply-chain gain of the lockfile (the replayed dependency graph) does not apply to the ten `npm:` tools, which include the two agent CLIs. The embedded installer would record the graph, but `scripts/update-agent-assets.sh:148` repairs the agent CLIs with `MISE_NPM_PACKAGE_MANAGER=npm`, `tests/unit/test_runtime_health.py:347` asserts that call, and the npm cooldown work of U89 and U114 (`~/.npmrc` `min-release-age`, the publish-time check in `upgrade-tools.sh`) is built on npm's own behaviour. Switching the installer is its own unit with its own measurement (the ccstatusline and ccusage graphs under aube are listed under Left out).

**The 72 h policy moves to the bump schedule.** The lockfile page states that a locked version installs even when newer than `minimum_release_age`, and the npm page adds that for a locked graph the cutoff applies when the graph is resolved. Run (f) confirms the config's `72h`. Under a lock, the host no longer applies the cooldown at install time; the `--minimum-release-age 72h` flag of `mise lock --bump` (in the help text above) applies it when the bump resolves, so the policy holds only if every bump run carries that flag and no one hand-edits the lock.

## Recommendation

**defer.** The measured output agrees with row 233 of `decisions.tsv` (`2026-10-28T09:40:00Z`, phase `plan-P-36`): the same 7 platforms and 36 tools, nothing written, and the lock is technically ready (every backend resolved in 2 s, no token, no failure). What the dry run adds is the entry counts (258 and 149), the fact that today's bump would be a first write and not a move, and the attempt-1 finding about mise's config discovery. None of this changes the facts the deferral rests on: the tree forbids the lock in three places by policy, `make update` would rewrite it on every host run, the CI copy carries one file, `package_manager = "npm"` records the version only, and the 72 h cooldown would move from install time to the bump schedule.

The condition that would change the recommendation to `adopt` is an operator decision, recorded in `decisions.tsv`, to stop unattended host upgrades (`upgrade-tools.sh:318`) and take every unheld version from a scheduled `mise lock --bump --minimum-release-age 72h` PR, with `mise install --locked` on hosts and in `test.yaml:276-279`, plus a decision on the npm installer. The condition that would change it to `reject` is a decision to keep the present `latest` behind the cooldown as the permanent policy, in which case the lockfile settings test and `.chezmoiremove:21` are the complete record and this question closes. Absent either, the no-lock policy stands as `README.md:199-202` and `:250-255` describe it.

## Draft decisions row

| field    | value                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ts       | 2026-10-29T13:29:01Z                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| phase    | plan-P-36                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| decision | mise.lock evaluation measured (plan P-36, research V4-9): defer; corrects the evidence of the 2026-10-28T09:40:00Z row, whose file handoff/research/05-eval-mise-lock.md was never written. Measured 2026-10-29 under a scratch HOME with mise 2026.10.19: `mise lock --global --dry-run` targets 7 platforms and 36 tools and would write 258 entries (36 x 7 plus 6 bun variant keys); the 4-platform set the http tables pin gives 149 entries; `--bump --dry-run --json` lists 36 first-time entries and no move; every backend (4 core, 11 aqua, 10 npm, 4 github, 2 cargo, 5 http) resolved in 2 s without a GitHub token; no lockfile written, the real ~/.config/mise unchanged. The condition stands: an operator decision to stop host-side `mise upgrade` (scripts/upgrade-tools.sh:318) and take versions from a scheduled `mise lock --bump --minimum-release-age 72h` PR, with `mise install --locked` on hosts and in the CI copy step (.github/workflows/test.yaml:259-261), and the npm installer question settled first |
| why      | the plan's acceptance asks for the measured output on record; the dry run changed no fact row 233 rests on: the tree's policy (README.md:199-202 and 250-255, home/.chezmoiremove:21, tests/unit/test_supply_chain_policy.py:404-421 and 464-466) forbids the lock and `--locked`, `make update` would rewrite the rendered lock on every run (vendor table: `mise upgrade` updates mise.lock), npm.package_manager=npm records the version only (the dependency graph needs the embedded installer, which scripts/update-agent-assets.sh:148 and tests/unit/test_runtime_health.py:347 do not use), and a locked version bypasses minimum_release_age so the 72 h policy would move to the bump schedule; one new fact: with a cwd under the real home, mise's parent-directory walk reads the real ~/.config/mise/config.toml as a project config                                                                                                                                                                                       |
| evidence | handoff/evaluations/U116-mise-lock.md                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| result   | proposed; the coordinator records                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |

The same row as one line with literal tab separators:

```text
2026-10-29T13:29:01Z	plan-P-36	mise.lock evaluation measured (plan P-36, research V4-9): defer; corrects the evidence of the 2026-10-28T09:40:00Z row, whose file handoff/research/05-eval-mise-lock.md was never written. Measured 2026-10-29 under a scratch HOME with mise 2026.10.19: `mise lock --global --dry-run` targets 7 platforms and 36 tools and would write 258 entries (36 x 7 plus 6 bun variant keys); the 4-platform set the http tables pin gives 149 entries; `--bump --dry-run --json` lists 36 first-time entries and no move; every backend (4 core, 11 aqua, 10 npm, 4 github, 2 cargo, 5 http) resolved in 2 s without a GitHub token; no lockfile written, the real ~/.config/mise unchanged. The condition stands: an operator decision to stop host-side `mise upgrade` (scripts/upgrade-tools.sh:318) and take versions from a scheduled `mise lock --bump --minimum-release-age 72h` PR, with `mise install --locked` on hosts and in the CI copy step (.github/workflows/test.yaml:259-261), and the npm installer question settled first	the plan's acceptance asks for the measured output on record; the dry run changed no fact row 233 rests on: the tree's policy (README.md:199-202 and 250-255, home/.chezmoiremove:21, tests/unit/test_supply_chain_policy.py:404-421 and 464-466) forbids the lock and `--locked`, `make update` would rewrite the rendered lock on every run (vendor table: `mise upgrade` updates mise.lock), npm.package_manager=npm records the version only (the dependency graph needs the embedded installer, which scripts/update-agent-assets.sh:148 and tests/unit/test_runtime_health.py:347 do not use), and a locked version bypasses minimum_release_age so the 72 h policy would move to the bump schedule; one new fact: with a cwd under the real home, mise's parent-directory walk reads the real ~/.config/mise/config.toml as a project config	handoff/evaluations/U116-mise-lock.md	proposed; the coordinator records
```

## Left out

- A real `mise lock --global` write, on any host or in the worktree. Every `mise lock` above carries `--dry-run`.
- `mise install --locked` on any host, so the install side of the workflow is unmeasured.
- The ccstatusline and ccusage dependency graphs under the embedded installer. Run (e) shows the npm installer, under which the lock records the version only, and the unit did not switch the installer.
- The Ubuntu host. Every command ran on the macOS host; the `linux-*` platform entries above come from mise's own resolution, not from a Linux run.
- A network capture. The hosts contacted are read from mise's cache file names.
- A repeat of round 1's attempt 1 (the cwd under the real home). Its five error lines stay pasted from the round-1 run; a repeat would open the real `~/.config/mise/config.toml` on purpose.
- The handoff `README.md` row for `evaluations/`, which the coordinator writes.
