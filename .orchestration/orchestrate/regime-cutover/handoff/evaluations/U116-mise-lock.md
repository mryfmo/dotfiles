# U116 mise.lock evaluation (plan P-36, research V4-9)

Measured 2026-10-29 (UTC) with `mise 2026.10.19 macos-arm64 (2026-10-24)` on the macOS host, every mise command under a scratch HOME; the dry runs pasted below are the round-11 re-take of the same date (2026-10-29T16:15:31Z to 2026-10-29T16:15:47Z, a scratch home and an output directory made by `tempfile.mkdtemp` under `$TMPDIR` and named in a receipt), taken by the one script this file holds with the config discovery variables of round 11 in the environment of every mise call; `scan`, `check` and the seventeen injections were run the same UTC day with the script as pasted.

## Question

Should CI and the hosts install the versions one committed `mise.lock` records, instead of each resolving `latest` on its own clock? If yes, where would that lockfile live under chezmoi, given that `home/dot_mise/config.toml` is the global mise config and renders byte for byte to `~/.config/mise/config.toml`?

The plan row P-36 (`handoff/05-remediation-plan.md:116`) asks for a decisions row with the measured output of `mise lock --global --dry-run`. The earlier row of `decisions.tsv` (`2026-10-28T09:40:00Z`, phase `plan-P-36`) records "defer with a condition" and names `handoff/research/05-eval-mise-lock.md` as its evidence, a file the store does not hold. This file is that evidence, measured again under a scratch HOME so a reader can rerun it.

## Commands run

One procedure, `U116-procedure.py`, pasted once below and run from `$TMPDIR` as `python3 -I U116-procedure.py <subcommand>`; every other fenced block in this file is one such invocation (an `sh` block of one line) followed by its output (a `text` block) or the content of a file the procedure wrote. Every output is a round-11 run of the script as pasted: `prepare` and `run` were re-taken because round 11 changes the environment of every mise call (the config discovery variables described under The procedure) and the way every scratch path is made, and `scan`, `check` and the seventeen `inject` runs follow over the same output directory. Each pasted output ends with the line `exit=<status>`, the process status as the harness that ran the command reported it, appended under the output; it is not printed by the procedure. `$TMPDIR` on this host is `/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/`; the procedure prints that prefix (in its `/var` and `/private/var` spellings) as `$TMPDIR/` and the random suffix `mkdtemp` gives each scratch directory as `<tmp>`, so a line such as `$TMPDIR/U116-home-<tmp>/cwd` names this run's directory and reads the same on every run. The files mise wrote are pasted as mise wrote them: under `ENV`, `HOME` is the scratch home, so mise's `~` in a pasted output (`~/.config/mise/mise.lock` in (b), (c) and (d), `~/.config/mise/config.toml` in `h-config-ls.txt`) is the scratch home, and `h-config-ls-json.txt` names the same file by its full path, with this run's suffix. No pasted output holds the login name or the real home directory: the procedure writes the real mise paths in `~` form itself, its listings carry no owner column, and every string it prints passes through its `redact` function.

Rounds 1 to 8 (commits `e0a1526a`, `b5281d6b`, `8b1b9088`, `fb8118c1`, `188312bf`, `a3efa54a`, `31be35ac`, `1c99f9fc`, each on this branch) took the same dry runs, first from shell blocks and then from a growing set of `python3 -I` scripts, and each audit found one more place of the same class: a producer whose status nobody read (the token reader; the pattern writer and the file lister inside process substitutions; the redact-list reader of the brief's own ACCEPTANCE 5; the two `date` stamps and the `cat` of a receipt inside the bash runner), a predicate that turned a failed read into an absence (`os.path.lexists` on the lockfile path; the `test -e` of ACCEPTANCE 6), a wrapper that turned a failed launch into a success (the brief's `perl -e 'alarm 900; exec @ARGV'`), or a diagnostic printed raw (the lookup's exception text naming a path under the real home; a missing `git` raising a traceback out of the positive-control script). The ROUND 9 AMENDMENT shrank the surface to one place: the eight scripts and seven shell blocks of round 8 were replaced by one script (`524cbf15`), and the measured numbers of rounds 5 to 8 (258, 149, 36, the same 36 versions) were re-taken by it; the older blocks remain in the history of the branch, not in this file. The round-9 audit (`verdicts/U116-524cbf15.md`) found three more places (the planted-token injection wrote the live token under `/tmp` for the length of the scan, the redaction table was computed at module level before `main()`'s boundary, and the PR body's network row named no control), and round 10 (`792fa05e`) answered each: a synthetic marker, `arm()` as the first statement inside the boundary with a `HOME`/`USER` fallback, and a row naming its controls. The round-10 audit (`verdicts/U116-792fa05e.md`) found two more. First, the injection fixtures lived under one fixed path, `/tmp/U116-inject-9`, reused across runs without an ownership or symlink check, so a symlink pre-created at its `out-timeout/a-version.txt` was followed by the write-mode `open` in `timed` and its target truncated: the isolation the file claimed did not hold for a path another process could plant. Second, `MISE_TRUSTED_CONFIG_PATHS`, the one mise variable the environment carried, marks a config trusted and restricts nothing, and `mise lock --help` itself says `--global` covers the global and system config lockfiles, so the claim that no other config could be read rested on `HOME` and the cwd alone. Round 11 answers both where they are. No scratch path is fixed: each scratch home, output directory and fixture tree is a `tempfile.mkdtemp` directory under `$TMPDIR` (mode 0700, a random name), made by the run that uses it and either named in a receipt the script writes and reads back or removed when its case ends; every file the procedure makes is opened by one `create` function with `O_CREAT|O_EXCL|O_NOFOLLOW` and mode 0600, so a path that exists or a symlink waiting at it is a refusal and never a write through it (the `create-symlink` injection below). And the environment of every mise call carries the config discovery variables the vendor's two configuration pages give, set so that the scratch copy is the only config mise can load; the pasted `mise config ls` (run `h`) shows that file alone, and the `planted-config` injection shows configs planted where mise would otherwise look staying unlisted, with a control under the round-10 variable set where they are listed.

### The procedure

`U116-procedure.py` has five subcommands. `prepare` refuses when the receipt `$TMPDIR/U116-prepare.receipt.txt` exists (a new re-take starts by removing it; the directories it names stay), makes a scratch home and an output directory with `tempfile.mkdtemp(prefix=..., dir=$TMPDIR)` (mode 0700, a random suffix no other run shares), makes the scratch home's nine directories one by one with `os.mkdir(..., 0o700)` (the four XDG trees, `cwd`, and `etc/mise`), copies `home/dot_mise/config.toml` from the worktree in-process, writes the receipt (`scratch=...` and `out=...`) and reads it back through `load_receipt` (opened with `O_NOFOLLOW`, `fstat` a regular file of this user with no group or other bits, exactly the two keys, each value a directory of this user directly under `$TMPDIR` with the matching prefix), then writes `real-before.txt`, a listing of the real `~/.config/mise` and its entries and of the other four real mise directories (mode, size, modification time, path in `~` form) taken with `os.scandir` and `os.lstat`. `run` reads the receipt, resolves `mise` once from `PATH` by a lookup that asks `os.lstat` entry by entry (`FileNotFoundError` moves on, any other `OSError` refuses, no entry at all refuses naming mise), changes to the scratch `cwd` (an empty directory inside the scratch home that is also the ceiling of mise's parent-directory walk: with a cwd under the real home, mise read the real `~/.config/mise/config.toml` as a project config in round 1, and with the scratch home itself as cwd the scratch copy was also a project config of that directory), prints `ENV`, and launches each of the nine mise commands (CHANGE 2 (a) to (f), `mise lock --help` for CHANGE 1, and `mise config ls` with and without `--json` as the evidence of which config files mise loaded) through `run([mise, ...], 900, env=ENV, ...)` with stdout and stderr to `<name>.txt`, writing `<name>.receipt.txt` (`start`, `end`, `elapsed`, `exit`) from its own clock and the returncode, read back and printed from the read-back bytes; after the last call it writes the scratch `.config/mise` listing, `real-after.txt`, `g-none-written.txt` from `check_lock` (an `os.lstat` of the scratch `mise.lock` path, `FileNotFoundError` the only absence, any other `OSError` a refusal, a result `WRITTEN`) and `scratch-tree.txt` (an `os.walk` four levels deep whose errors raise, each path through `redact`). `scan` reads the receipt, the token from `gh auth token` (status, output and timeout read; an empty token refuses) and every non-comment, non-empty line of the coordinator's `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/redact-words.txt` in-process (the path and the count printed, zero patterns a refusal), derives the absolute prefix of home directories on this host from the real home, lists the `.txt` files of the output directory with `os.scandir` (a count other than 23 refuses) and counts the three classes over each of them and over this file and the PR body, printing only counts and `scan clean (<n> files, 0 matches)` when every count is 0, `scan FOUND` and exit 1 otherwise. `check` reads the receipt, runs `git diff --name-only 6fd09e96..HEAD` in the worktree and `prettier --check --ignore-path /dev/null` on this file, prints the six level-two headings with their line numbers and whether they are the six of CHANGE 4 in order, counts the six-field tab-separated lines whose second field is `plan-P-36`, runs `check_lock`, prints `real-before.txt` and `real-after.txt` and whether they are equal and free of a `mise.lock` line, and prints the forms counts of each document: fenced blocks by kind, `sh` blocks off the one-line form, lines inside `sh` blocks holding a command substitution, a process substitution or a pipe, lines inside the `python` block calling an error-swallowing predicate or a `.get(` lookup or opening an `except` clause other than `except FileNotFoundError:` whose body neither refuses nor raises, lines in either kind of block whose word in command position is a wrapper process, and lines of the `python` block that print or write outside the bodies of `emit` and `refuse`; it prints `check ok` and exits 0 only when every one of those is as required, `check FAILED` and 1 otherwise. `inject <name>` is one of seventeen named failure injections; each makes its own fixture directory with `mkdtemp` (removed when the case ends, however it ends), patches this process (`PATH`, one global, `os.lstat` for one path, or one function: `token_bytes` replaced by a synthetic marker, `getpass.getuser` made to raise) or plants fixtures under that directory, and then calls the targeted subcommand's own function, so the exit status is that code path's own.

The environment of every mise call, `ENV`, is built by `environment(scratch)` and printed by `run`. It holds the variable set of CHANGE 1 (`HOME`, `PATH`, `TMPDIR`, the four XDG variables pointed inside the scratch home, `MISE_TRUSTED_CONFIG_PATHS` naming the scratch copy) and the config discovery variables of <https://mise.jdx.dev/configuration.html> and <https://mise.jdx.dev/configuration/settings.html>, read 2026-10-29 and quoted under Measured facts: `MISE_GLOBAL_CONFIG_FILE` names the scratch copy (the page: "When set, mise reads and writes only this file", and it "also turns off the override files"), `MISE_CONFIG_DIR` the scratch `.config/mise`, `MISE_SYSTEM_CONFIG_FILE` a file that does not exist inside the scratch home (`etc/mise/none.toml`; "When set, mise reads and writes only this file") and `MISE_SYSTEM_CONFIG_DIR` its directory, `MISE_CEILING_PATHS` the scratch `cwd` itself in both spellings ("The search stops at a ceiling directory, which is not searched itself", and mise compares the resolved `/private/var` spelling, so the `/var` spelling alone did not match in a probe), `MISE_IGNORED_CONFIG_PATHS` the real `~/.config/mise` and `/etc/mise` in both spellings ("Config files and directories mise does not load"), `MISE_OVERRIDE_CONFIG_FILENAMES` one name no file carries (`U116-none.toml`; the brief's round-11 task asked for an empty value, which this mise reads as unset, as the `planted-config` injection's second control shows, so the variable carries a sentinel and the ceiling is the control that excludes project config) and `MISE_OVERRIDE_TOOL_VERSIONS_FILENAMES` the page's `none`. Not set, and why: `MISE_ENV`, `MISE_AUTO_ENV` and `MISE_ENV_CONF_D` select environment overlays (unset selects none, `auto_env` defaults to `false` in this release, and a single global file has no overlay files), `MISE_GLOBAL_CONFIG_ROOT` is the template root for the global config (its default, `$HOME`, is the scratch home), `MISE_DEFAULT_CONFIG_FILENAME` names a file mise would create (nothing is created), and `MISE_NO_CONFIG` would drop the scratch config too.

Three functions carry the properties the amendments ask for. `main()` is the only entry; its body is one `try` whose `except BaseException` refuses with the exception's class and text and exits 2; the one thing it re-raises is a `SystemExit` the script raised itself, with code 0, 1 or 2 (a success, a measured failure such as `scan FOUND` or `check FAILED`, a refusal `refuse` has already printed), so no traceback and no second refusal line can leave the process. `run(argv, timeout, ...)` is the only launch point: it refuses any argv whose command is not `mise`, `gh`, `git` or `prettier`, calls `subprocess.run` with `check=False`, the timeout and stdin closed (so a prompt fails instead of waiting out the timeout), and turns `TimeoutExpired`, `FileNotFoundError`, `PermissionError` and every other `OSError` into a refusal naming the argv; `timed` wraps it for the mise calls so that a refused launch, or a refused output path, still gets its receipt, reading `exit=refused`, written and printed as the refusal unwinds through the `finally` clause (the receipt therefore follows the refusal line in the output). `emit` and `refuse` are the only two functions that print, both through `redact`, which replaces each registered `mkdtemp` name with `<prefix><tmp>`, `$TMPDIR` in both spellings with `$TMPDIR/`, the real home directory (both spellings) with `~` and the login name with `<user>`; the home and login pairs are built by `arm()`, the first statement of `main()`'s `try`, from `expanduser("~")` (else `HOME`) and `getpass.getuser()` (else `USER`), with a refusal when neither spelling exists and the home pairs installed before the login name is looked up, so a lookup that fails is one redacted refusal and not a traceback; `configure()` adds the `$TMPDIR` pairs after requiring `$TMPDIR` to be a directory of this user not writable by group or others (the receipt's one fixed name lives there), and `scratch_dir` and `load_receipt` add each `mkdtemp` name. Module level holds constants and `def`s only, and nothing there can raise. Every file the script makes goes through `create(path)`, `os.open(path, O_WRONLY|O_CREAT|O_EXCL|O_NOFOLLOW, 0o600)`, and every directory through `mkdtemp` or `os.mkdir(path, 0o700)` inside one; the two fixed paths the script holds, the worktree `/tmp/dotfiles-wt/U116` and the PR body beside it, are the brief's inputs, read and never written. Nothing else in the script prints or writes to stdout or stderr. There is no shell anywhere, no wrapper process, no `os.path.exists`-class predicate, no `dict.get` with a default; absence is decided only by `os.lstat` or `open` raising `FileNotFoundError`. The script, byte for byte the file that took every run and injection below:

```python
# U116 procedure, round 11 (brief CHANGE 1, 2 and 4; the ROUND 4 to ROUND 9
# amendments; the round-9 and round-10 verdicts). One file, five
# subcommands, run as `python3 -I U116-procedure.py <subcommand> [name]`
# from $TMPDIR:
#   prepare        a fresh scratch HOME and a fresh output directory, both
#                  tempfile.mkdtemp under $TMPDIR, named in a receipt this
#                  script writes and reads back; the config copy; the
#                  before listing of the real mise directories
#   run            the dry runs under the scratch HOME with receipts, the
#                  config listing, the after listings, the none-written
#                  file, the scratch tree
#   scan           the token, the redact words and the absolute home prefix
#                  over every output file and the two documents
#   check          ACCEPTANCE 1 (the diff against the merge base), 3
#                  (prettier), 2 (the six headings), 4 (the draft row), 6
#                  (none-written, the before and after listings) and the
#                  forms counts over the two documents
#   inject <name>  one failure injection, patched in this process, running
#                  the same code path as the subcommand it targets
# main() is the only entry. Its body is one try whose except BaseException
# refuses with the exception's class and text (exit 2); the one thing it
# re-raises is a SystemExit this script raised itself (code 0, 1 or 2: a
# success, a measured failure, a refusal already printed), so no traceback
# leaves the process. Every external command (mise, gh, git, prettier,
# nothing else) starts through run(argv, timeout): subprocess.run with
# check=False, the timeout, stdin closed, a launch that raises refused with
# the redacted argv. Every string that reaches stdout passes through
# redact() inside emit() or refuse(); nothing else prints. The redaction
# table is built by arm() as the first statement of main()'s try, from the
# real home (expanduser, else HOME) and the login name (getpass, else
# USER), refusing when neither spelling exists; configure() adds $TMPDIR
# in both spellings, and every mkdtemp name is added as it is made or read
# from the receipt, so a scratch path prints as $TMPDIR/U116-home-<tmp>.
# Every file question is asked of os.lstat, os.scandir or open:
# FileNotFoundError alone is absence, any other OSError is a refusal. Every
# file this script makes is opened by create(): O_CREAT|O_EXCL|O_NOFOLLOW,
# mode 0600, so an existing path or a symlink at the path is a refusal,
# never a write through it; every directory is mkdtemp (0700) or
# os.mkdir(..., 0o700) inside one. No fixed scratch path: the one fixed
# name is the receipt, $TMPDIR/U116-prepare.receipt.txt, under a directory
# this script requires to be this user's and not writable by others. No
# shell, no wrapper process, no lookup with a default on a required key.
import ast
import datetime
import getpass
import io
import keyword
import os
import secrets
import shlex
import shutil
import stat
import subprocess
import sys
import tempfile
import time
import tokenize

# The brief's worktree and PR body: inputs this script reads, never
# scratch, never written by it.
WORKTREE = "/tmp/dotfiles-wt/U116"
RELATIVE = ".orchestration/orchestrate/regime-cutover/handoff/evaluations/U116-mise-lock.md"
EVALUATION = f"{WORKTREE}/{RELATIVE}"
PR_BODY = "/tmp/dotfiles-wt/U116-pr-body.md"
DOCUMENTS = (EVALUATION, PR_BODY)
MERGE_BASE = "6fd09e96"
SOURCE_CONFIG = f"{WORKTREE}/home/dot_mise/config.toml"
# The coordinator's list; the path is printed in this form, never expanded.
REDACT_LIST = "~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/redact-words.txt"
HEADINGS = ("## Question", "## Commands run", "## Measured facts", "## Recommendation", "## Draft decisions row", "## Left out")
SUBCOMMANDS = ("prepare", "run", "scan", "check", "inject")
COMMANDS = ("mise", "gh", "git", "prettier")
EXITS = (0, 1, 2)
PLATFORMS = "linux-x64,linux-arm64,macos-x64,macos-arm64"
TIMEOUT = 900
# The scratch home's directories, made one by one with os.mkdir(..., 0o700)
# inside the mkdtemp: the four XDG trees, the cwd every mise call runs in
# (and the ceiling of its parent-directory walk), and the directory the
# system config variables point into.
SUBDIRS = (".config", ".config/mise", ".local", ".local/share", ".cache", ".local/state", "cwd", "etc", "etc/mise")
# The mkdtemp prefixes; the receipt names one directory of each of the
# first two.
HOME_PREFIX = "U116-home-"
OUT_PREFIX = "U116-out-"
INJECT_PREFIX = "U116-inject-"
RECEIPT_NAME = "U116-prepare.receipt.txt"
RECEIPT_KEYS = (("scratch", HOME_PREFIX), ("out", OUT_PREFIX))
# The .txt files prepare and run write: the before listing; 9 outputs and 9
# receipts; the scratch listing, the after listing, the none-written file
# and the scratch tree. A different count means the directory was not
# walked or the output set changed, so scan refuses.
EXPECTED_FILES = 23
# The runs of CHANGE 2 (a) to (f), `mise lock --help` for CHANGE 1, and
# `mise config ls` twice (the table, and --json for the full path) as the
# evidence of which config files mise loaded under ENV.
RUNS = (
    ("a-version", ["--version"]),
    ("help-lock", ["lock", "--help"]),
    ("b-lock-dry-run", ["lock", "--global", "--dry-run"]),
    ("c-lock-dry-run-4-platforms", ["lock", "--global", "--dry-run", "--platform", PLATFORMS]),
    ("d-lock-bump-json", ["lock", "--global", "--dry-run", "--bump", "--json"]),
    ("e-npm-package-manager", ["settings", "get", "npm.package_manager"]),
    ("f-minimum-release-age", ["settings", "get", "minimum_release_age"]),
    ("h-config-ls", ["config", "ls"]),
    ("h-config-ls-json", ["config", "ls", "--json"]),
)
# The variable set of CHANGE 1 (round 1 to round 10); the planted-config
# injection runs its negative control with these alone.
CHANGE_1_KEYS = ("HOME", "PATH", "TMPDIR", "XDG_CONFIG_HOME", "XDG_DATA_HOME", "XDG_CACHE_HOME", "XDG_STATE_HOME", "MISE_TRUSTED_CONFIG_PATHS")
# The configs the planted-config injection writes, relative to its scratch
# home: the cwd's parent, the cwd itself, a .tool-versions in the cwd, and
# the file the system config directory variable would otherwise name.
PLANTS = (
    ("mise.toml", b'[tools]\nnode = "20"\n'),
    ("cwd/mise.toml", b'[tools]\nnode = "16"\n'),
    ("cwd/.tool-versions", b"node 14\n"),
    ("etc/mise/config.toml", b'[tools]\nnode = "18"\n'),
)
# The real mise directories, written in this form, never expanded.
REAL_DIRS = ("~/.config/mise", "~/.local/share/mise", "~/.cache/mise", "~/.local/state/mise", "~/Library/Caches/mise")
INJECTIONS = (
    "missing-mise", "missing-gh", "missing-git", "missing-prettier", "lookup-permission", "run-timeout",
    "lock-notadirectory", "lock-permission", "lock-missing", "txt-count", "redact-comment-only", "missing-out",
    "planted-token", "user-lookup", "forms-producer", "create-symlink", "planted-config",
)
# Injections that need no receipt: they patch this process alone or build
# their own scratch home.
STANDALONE = ("user-lookup", "forms-producer", "planted-config")
# The forms the check counts, spelled apart so this script holds none of
# them as text.
FENCE = chr(96) * 3
MARKS = ("$" + "(", "<" + "(", chr(124))
SHELL = ("sh", "bash")
PYTHON = ("python", "python3", "py")
TEXT = ("text",)
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
PRINTS = ("pri" + "nt(", ".wri" + "te(")
WRAPPERS = tuple("".join(parts) for parts in (("pe", "rl"), ("time", "out"), ("xa", "rgs"), ("no", "hup"), ("ni", "ce"), ("set", "sid")))
FLAGGED = {"env": "-i", "ba" + "sh": "-c", "sh": "-c"}
SHELL_BREAKS = (";", "&&", "||", "&", chr(124))
QUIET = (tokenize.NL, tokenize.NEWLINE, tokenize.COMMENT, tokenize.INDENT, tokenize.DEDENT)
RUN_CALL = ["subprocess", ".", "run", "("]
FORM = ["python3", "-I", "U116-procedure.py"]

# Set by configure() from the environment, inside main()'s try, and by
# set_scratch() from the receipt or from a fresh mkdtemp; the injections
# patch some of them in this process.
COMMAND = "procedure"
TMPDIR = HOME = PATH = SCRATCH = OUT = CWD = CONFIG = LOCK = ""
ENV = {}
# Set by arm() as the first statement of main()'s try: the real home
# directory and the strings redact() replaces. Empty until then, so a
# refusal before arm() finishes prints its text as is (arm() builds the
# home pair before it looks up the login name, so a login-name refusal is
# already home-redacted). configure() adds the $TMPDIR pairs and
# register_temp() the mkdtemp names.
HOME_DIR = ""
REDACTIONS = ()
TMP_PAIRS = ()
TEMP_NAMES = ()
SYNTHETIC = "U116-SYNTHETIC-TOKEN-"
TOKEN_SOURCE = "gh auth token"  # the planted-token injection names its marker here


def home_string():
    # The real home directory: expanduser("~") when it expanded to an
    # absolute path, else HOME when it is set, else a refusal (expanduser
    # returns "~" unchanged when HOME is unset and the UID has no passwd
    # entry).
    expanded = os.path.expanduser("~")
    if expanded.startswith("/"):
        return os.path.realpath(expanded)
    if "HOME" in os.environ and os.environ["HOME"].startswith("/"):
        return os.environ["HOME"]
    refuse("home directory unknown: ~ did not expand and HOME is unset")


def login_name():
    # The login name: getpass.getuser(), else USER when it is set, else a
    # refusal. getpass raises OSError (KeyError before Python 3.13) when no
    # name variable is set and the UID has no passwd entry.
    try:
        return getpass.getuser()
    except (OSError, KeyError) as exc:
        if "USER" in os.environ and os.environ["USER"]:
            return os.environ["USER"]
        refuse(f"login name unknown: {type(exc).__name__}: {exc}; USER is unset")


def arm():
    # The strings redact() replaces, longest first so a home path is
    # replaced before the login name inside it: the real home directory in
    # both spellings (the resolved path of ~, and HOME when it is set) as
    # ~, and the login name (getpass, and USER when it is set) as <user>.
    # Called inside main()'s try; the home pairs are installed before the
    # login name is looked up.
    global HOME_DIR, REDACTIONS
    HOME_DIR = home_string()
    homes = [HOME_DIR]
    if "HOME" in os.environ:
        homes.append(os.environ["HOME"])
    pairs = [(home, "~") for home in homes if len(home) > 1]
    REDACTIONS = tuple(dict.fromkeys(pairs))
    users = [login_name()]
    if "USER" in os.environ:
        users.append(os.environ["USER"])
    pairs += [(user, "<user>") for user in users if user]
    pairs.sort(key=lambda pair: len(pair[0]), reverse=True)
    REDACTIONS = tuple(dict.fromkeys(pairs))


def spellings(path):
    # A path as given and as the kernel resolves it (on macOS /var and /etc
    # are symlinks into /private, and mise compares the resolved form).
    return tuple(dict.fromkeys((path, os.path.realpath(path))))


def register_temp(path, prefix):
    # A mkdtemp name, made by this process or read from the receipt, so
    # that redact() prints it as <prefix><tmp>.
    global TEMP_NAMES
    name = os.path.basename(path)
    if not name.startswith(prefix) or len(name) == len(prefix):
        refuse(f"{path} is not a {prefix} mkdtemp name")
    TEMP_NAMES = tuple(dict.fromkeys(TEMP_NAMES + ((name, prefix + "<tmp>"),)))


def redact(text):
    for literal, replacement in TEMP_NAMES + TMP_PAIRS + REDACTIONS:
        text = text.replace(literal, replacement)
    return text


def emit(text):
    # The one place a result line is printed.
    print(redact(text), flush=True)


def refuse(text):
    # The one place a refusal is printed; exit 2.
    print(redact(f"{COMMAND} REFUSED: {text}"), flush=True)
    sys.exit(2)


def run(argv, timeout, env=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE):
    # The one launch point. A command outside the four this procedure
    # names, or a launch that raises (TimeoutExpired, FileNotFoundError,
    # PermissionError, any other OSError), is a refusal naming the argv.
    # stdin is closed, so a prompt (a trust prompt, say) fails instead of
    # waiting out the timeout.
    if os.path.basename(argv[0]) not in COMMANDS:
        refuse(f"{argv} is not one of {COMMANDS}")
    try:
        return subprocess.run(argv, env=env, timeout=timeout, check=False, stdin=subprocess.DEVNULL, stdout=stdout, stderr=stderr)
    except (subprocess.TimeoutExpired, OSError) as exc:
        refuse(f"{argv} did not complete: {type(exc).__name__}: {exc}")


def require_env(name):
    try:
        return os.environ[name]
    except KeyError:
        refuse(f"{name} is unset")


def require_private_dir(path, forbidden, label):
    # A directory of this user: os.lstat (a symlink is not a directory),
    # S_ISDIR, the owner this process's UID, none of the forbidden mode
    # bits set.
    try:
        info = os.lstat(path)
    except FileNotFoundError:
        refuse(f"{label} {path} is missing")
    except OSError as exc:
        refuse(f"cannot read {label} {path}: {exc}")
    if not stat.S_ISDIR(info.st_mode):
        refuse(f"{label} {path} is not a directory ({stat.filemode(info.st_mode)})")
    if info.st_uid != os.getuid():
        refuse(f"{label} {path} is owned by uid {info.st_uid}, not {os.getuid()}")
    if info.st_mode & forbidden:
        refuse(f"{label} {path} has mode {stat.filemode(info.st_mode)}; bits {oct(forbidden)} must be clear")


def configure():
    global TMPDIR, HOME, PATH, TMP_PAIRS
    TMPDIR = require_env("TMPDIR")
    HOME = require_env("HOME")
    PATH = require_env("PATH")
    # The receipt's directory: this user's, and not writable by group or
    # others, so its one fixed name cannot be planted by another user.
    require_private_dir(TMPDIR, stat.S_IWGRP | stat.S_IWOTH, "TMPDIR")
    # Longest spelling first, so /private/var/... is replaced before the
    # /var/... inside it.
    pairs = dict.fromkeys((spelling.rstrip("/") + "/", "$TMPDIR/") for spelling in spellings(TMPDIR.rstrip("/")))
    TMP_PAIRS = tuple(sorted(pairs, key=lambda pair: len(pair[0]), reverse=True))


def real(shown):
    return os.path.join(HOME, shown[2:])


def environment(scratch):
    # The whole environment of every mise call: the variable set of CHANGE
    # 1 (HOME, PATH, TMPDIR, the four XDG variables inside the scratch
    # home, MISE_TRUSTED_CONFIG_PATHS), plus the config discovery variables
    # of https://mise.jdx.dev/configuration.html and
    # https://mise.jdx.dev/configuration/settings.html, so that the scratch
    # copy is the only config mise can load: the global config is that one
    # file (MISE_GLOBAL_CONFIG_FILE, which also turns off the override
    # files), the global directory is the scratch one (MISE_CONFIG_DIR),
    # the system config is one file that does not exist inside the scratch
    # home (MISE_SYSTEM_CONFIG_FILE, MISE_SYSTEM_CONFIG_DIR), the
    # parent-directory walk for project config stops at the cwd itself
    # (MISE_CEILING_PATHS, in both spellings; a ceiling directory is not
    # searched), the real ~/.config/mise and /etc/mise are ignored even if
    # something still named them (MISE_IGNORED_CONFIG_PATHS), and the
    # project file names are one name no file carries and no
    # .tool-versions (the override filename variables; this mise ignores
    # an empty MISE_OVERRIDE_CONFIG_FILENAMES, so the value is a sentinel,
    # and the doc's `none` for the tool-versions one).
    config = os.path.join(scratch, ".config", "mise", "config.toml")
    system_dir = os.path.join(scratch, "etc", "mise")
    return {
        "HOME": scratch,
        "PATH": PATH,
        "TMPDIR": TMPDIR,
        "XDG_CONFIG_HOME": os.path.join(scratch, ".config"),
        "XDG_DATA_HOME": os.path.join(scratch, ".local", "share"),
        "XDG_CACHE_HOME": os.path.join(scratch, ".cache"),
        "XDG_STATE_HOME": os.path.join(scratch, ".local", "state"),
        "MISE_TRUSTED_CONFIG_PATHS": config,
        "MISE_CONFIG_DIR": os.path.join(scratch, ".config", "mise"),
        "MISE_GLOBAL_CONFIG_FILE": config,
        "MISE_SYSTEM_CONFIG_DIR": system_dir,
        "MISE_SYSTEM_CONFIG_FILE": os.path.join(system_dir, "none.toml"),
        "MISE_CEILING_PATHS": os.pathsep.join(spellings(os.path.join(scratch, "cwd"))),
        "MISE_IGNORED_CONFIG_PATHS": os.pathsep.join(spellings(real(REAL_DIRS[0])) + spellings("/etc/mise")),
        "MISE_OVERRIDE_CONFIG_FILENAMES": "U116-none.toml",
        "MISE_OVERRIDE_TOOL_VERSIONS_FILENAMES": "none",
    }


def set_scratch(scratch, out):
    global SCRATCH, OUT, CWD, CONFIG, LOCK, ENV
    SCRATCH = scratch
    OUT = out
    CWD = os.path.join(scratch, "cwd")
    CONFIG = os.path.join(scratch, ".config", "mise", "config.toml")
    LOCK = os.path.join(scratch, ".config", "mise", "mise.lock")
    ENV = environment(scratch)


def scratch_dir(prefix):
    # A fresh directory under $TMPDIR, mode 0700, with a random name mkdtemp
    # chooses; registered so it prints as <prefix><tmp>.
    path = tempfile.mkdtemp(prefix=prefix, dir=TMPDIR)
    register_temp(path, prefix)
    return path


def mkdir(path):
    os.mkdir(path, 0o700)


def create(path):
    # The one way this script makes a file: O_EXCL refuses a path that
    # exists, O_NOFOLLOW a symlink at the path (FileExistsError or OSError
    # to the boundary, exit 2), mode 0600. Returns a binary handle.
    return os.fdopen(os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600), "wb")


def read_file(path):
    with open(path, "rb") as handle:
        return handle.read()


def read_private(path, hint):
    # A file this script wrote: opened without following a symlink, then
    # fstat must show a regular file of this user with no group or other
    # bits.
    try:
        descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    except FileNotFoundError:
        refuse(f"{path} is missing; {hint}")
    except OSError as exc:
        refuse(f"cannot read {path}: {exc}")
    with os.fdopen(descriptor, "rb") as handle:
        info = os.fstat(handle.fileno())
        if not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid() or info.st_mode & 0o077:
            refuse(f"{path} is not a private regular file of this user ({stat.filemode(info.st_mode)}, uid {info.st_uid})")
        return handle.read()


def write_file(path, text):
    data = text if isinstance(text, bytes) else text.encode()
    with create(path) as handle:
        shutil.copyfileobj(io.BytesIO(data), handle)


def out_path(name):
    return os.path.join(OUT, name)


def receipt_path():
    return os.path.join(TMPDIR, RECEIPT_NAME)


def load_receipt():
    # The receipt prepare wrote: exactly the two lines scratch=... and
    # out=..., each naming a mkdtemp directory of this user directly under
    # $TMPDIR with the matching prefix.
    path = receipt_path()
    text = read_private(path, "run prepare first").decode()
    fields = {}
    for line in text.splitlines():
        key, separator, value = line.partition("=")
        if separator != "=" or key not in dict(RECEIPT_KEYS) or key in fields:
            refuse(f"{path} holds an unexpected line: {line}")
        fields[key] = value
    if sorted(fields) != sorted(dict(RECEIPT_KEYS)):
        refuse(f"{path} holds {sorted(fields)}, expected {sorted(dict(RECEIPT_KEYS))}")
    for key, prefix in RECEIPT_KEYS:
        value = fields[key]
        if os.path.normpath(os.path.dirname(value)) != os.path.normpath(TMPDIR):
            refuse(f"{key}={value} is not directly under $TMPDIR")
        register_temp(value, prefix)
        require_private_dir(value, stat.S_IRWXG | stat.S_IRWXO, key)
    set_scratch(fields["scratch"], fields["out"])


def require_file(path, hint):
    try:
        with open(path, "rb") as handle:
            handle.read(1)
    except FileNotFoundError:
        refuse(f"{path} is missing; {hint}")
    except OSError as exc:
        refuse(f"cannot read {path}: {exc}")


def resolve(name, path):
    # The first PATH entry holding `name`, asked of os.lstat entry by
    # entry: FileNotFoundError moves to the next entry, any other OSError
    # is a refusal with its text, no entry at all is a refusal naming it.
    # The executable bit is not tested; a file that cannot be executed is
    # left for the launch to raise PermissionError.
    entries = [entry for entry in path.split(os.pathsep) if entry]
    for number, entry in enumerate(entries, 1):
        candidate = os.path.join(entry, name)
        try:
            os.lstat(candidate)
        except FileNotFoundError:
            continue
        except OSError as exc:
            refuse(f"cannot read {candidate}: {exc}")
        emit(f"{name}={candidate} (PATH entry {number} of {len(entries)})")
        return candidate
    refuse(f"{name} not found on PATH ({len(entries)} entries searched)")


def stamp():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def when(seconds):
    return datetime.datetime.fromtimestamp(seconds).strftime("%Y-%m-%dT%H:%M:%S")


def stat_or_absent(path):
    # os.lstat, with FileNotFoundError the only answer read as absence.
    try:
        return os.lstat(path)
    except FileNotFoundError:
        return None


def describe(path, shown):
    info = stat_or_absent(path)
    if info is None:
        return f"missing {shown}"
    return f"{stat.filemode(info.st_mode)} {info.st_size:>6} {when(info.st_mtime)} {shown}"


def listing(directory, shown):
    # The directory and every entry in it, one line each, by os.scandir and
    # os.lstat; a missing directory is one line.
    lines = [describe(directory, shown)]
    if stat_or_absent(directory) is None:
        return lines
    with os.scandir(directory) as entries:
        names = sorted(entry.name for entry in entries)
    return lines + [describe(os.path.join(directory, name), f"{shown}/{name}") for name in names]


def real_listing():
    # The real ~/.config/mise with its entries, and the other real mise
    # directories themselves (mode, size, mtime).
    lines = listing(real(REAL_DIRS[0]), REAL_DIRS[0])
    for shown in REAL_DIRS[1:]:
        lines.append(describe(real(shown), shown))
    return "\n".join(lines) + "\n"


def raise_error(exc):
    # os.walk ignores a directory it cannot read unless told otherwise.
    raise exc


def scratch_tree(depth=4):
    # The scratch home four levels deep, each path through redact so the
    # file reads $TMPDIR/U116-home-<tmp>/...
    lines = []
    for root, dirs, files in os.walk(SCRATCH, onerror=raise_error):
        rel = os.path.relpath(root, SCRATCH)
        level = 0 if rel == "." else rel.count(os.sep) + 1
        if level >= depth:
            dirs[:] = []
        lines.append(redact(root))
        lines.extend(redact(os.path.join(root, entry)) for entry in files)
    lines.sort()
    return "\n".join(lines) + "\n"


def check_lock():
    # The none-written test: os.lstat on the lockfile path, absent only
    # when it raises FileNotFoundError, any other error a refusal with its
    # text, a result a written lockfile.
    try:
        os.lstat(LOCK)
    except FileNotFoundError:
        return "none-written"
    except OSError as exc:
        refuse(f"cannot read {LOCK}: {exc}")
    return "WRITTEN"


def timed(name, argv, timeout):
    # One mise call with ENV as its whole environment, stdout and stderr to
    # <name>.txt (made by create(), so a file or symlink already at that
    # path is a refusal before the launch); the receipt <name>.receipt.txt
    # is written from this process's clock and the returncode, read back
    # and emitted from the read-back bytes. When the launch refuses inside
    # run(), or create() refuses the output path, the receipt is still
    # written and emitted, reading exit=refused, as the refusal unwinds
    # through the finally clause.
    start = stamp()
    began = time.monotonic()
    status = "refused"
    try:
        with create(out_path(f"{name}.txt")) as handle:
            status = run(argv, timeout, env=ENV, stdout=handle, stderr=subprocess.STDOUT).returncode
    finally:
        path = out_path(f"{name}.receipt.txt")
        write_file(path, f"start={start} end={stamp()} elapsed={round(time.monotonic() - began)}s exit={status}\n")
        text = read_file(path).decode().strip()
        if not text:
            refuse(f"{name}.receipt.txt is empty after it was written")
        emit(f"{name}: {text}")
    return status


def make_scratch(scratch):
    # The scratch home's directories and the config copy, inside a
    # directory mkdtemp made.
    for subdir in SUBDIRS:
        mkdir(os.path.join(scratch, subdir))
    data = read_file(SOURCE_CONFIG)
    write_file(os.path.join(scratch, ".config", "mise", "config.toml"), data)
    return len(data)


def prepare():
    receipt = receipt_path()
    try:
        os.lstat(receipt)
    except FileNotFoundError:
        pass
    else:
        refuse(f"{receipt} exists already; a new re-take starts by removing it (the directories it names stay)")
    scratch = scratch_dir(HOME_PREFIX)
    out = scratch_dir(OUT_PREFIX)
    emit(f"mkdtemp: {scratch} and {out} (mode 0700)")
    size = make_scratch(scratch)
    emit(f"mkdir: {' '.join(SUBDIRS)} under {scratch} (mode 0700)")
    emit(f"copy: {size} bytes to {scratch}/.config/mise/config.toml")
    write_file(receipt, f"scratch={scratch}\nout={out}\n")
    load_receipt()
    emit(f"receipt: {receipt} names scratch={SCRATCH} out={OUT} (written, read back, both directories this user's)")
    text = real_listing()
    write_file(out_path("real-before.txt"), text)
    emit(f"real-before: {len(text.splitlines())} lines to {OUT}/real-before.txt")
    return 0


def emit_env():
    emit("env (the whole environment of every mise call):")
    for key in ENV:
        value = f"<{len(ENV[key].split(os.pathsep))} entries, inherited>" if key == "PATH" else ENV[key]
        emit(f"  {key}={value}")


def dry_runs():
    require_file(CONFIG, "run prepare first")
    require_private_dir(OUT, stat.S_IRWXG | stat.S_IRWXO, "out")
    mise = resolve("mise", os.environ["PATH"])
    # The cwd is an empty directory inside the scratch home and the ceiling
    # of mise's parent-directory walk: with a cwd under the real home, mise
    # read the real ~/.config/mise/config.toml as a project config (round
    # 1, attempt 1); with the scratch home itself as cwd, the scratch copy
    # was also a project config of that directory.
    os.chdir(CWD)
    emit(f"cwd={CWD}")
    emit_env()
    failed = 0
    for name, args in RUNS:
        if timed(name, [mise, *args], TIMEOUT) != 0:
            failed += 1
    scratch_mise = os.path.join(SCRATCH, ".config", "mise")
    write_file(out_path("g-scratch-after.txt"), "\n".join(listing(scratch_mise, redact(scratch_mise))) + "\n")
    write_file(out_path("real-after.txt"), real_listing())
    outcome = check_lock()
    write_file(out_path("g-none-written.txt"), outcome + "\n")
    emit(f"g-none-written: {outcome}")
    failed += outcome != "none-written"
    write_file(out_path("scratch-tree.txt"), scratch_tree())
    emit(f"runs={len(RUNS)} failed={failed}")
    return 1 if failed else 0


def token_bytes():
    proc = run(["gh", "auth", "token"], 60)
    if proc.returncode != 0:
        refuse(f"gh auth token exited {proc.returncode}")
    token = proc.stdout.strip()
    if not token:
        refuse("gh auth token returned an empty token")
    return token


def read_token():
    token = token_bytes()
    emit(f"token from {TOKEN_SOURCE} patterns=1")
    return token


def read_redact_words():
    words = []
    for line in read_file(os.path.expanduser(REDACT_LIST)).splitlines():
        word = line.strip()
        if word and not word.startswith(b"#"):
            words.append(word)
    emit(f"redact list {REDACT_LIST} patterns={len(words)}")
    if not words:
        refuse(f"redact list {REDACT_LIST} holds no pattern")
    return words


def home_prefix():
    # The absolute prefix every home directory on this host shares, derived
    # from the real home arm() resolved, so the literal never appears in
    # this script.
    return (os.path.dirname(HOME_DIR) + "/").encode()


def list_outputs():
    files = []
    with os.scandir(OUT) as entries:
        for entry in entries:
            if not entry.name.endswith(".txt"):
                continue
            if not stat.S_ISREG(os.lstat(entry.path).st_mode):
                refuse(f"{entry.path} is not a regular file")
            files.append(entry.path)
    files.sort()
    if len(files) != EXPECTED_FILES:
        refuse(f"found {len(files)} .txt files, expected {EXPECTED_FILES}")
    return files


def count_matches(path, shown, classes):
    data = read_file(path)
    line = shown
    total = 0
    for name, patterns in classes:
        count = sum(data.count(pattern) for pattern in patterns)
        line += f" {name}={count}"
        total += count
    emit(line)
    return total


def scan():
    # Three classes over every output file and both documents: the token,
    # the redact words and the absolute home prefix; only counts leave the
    # process. The token and the redact words reach no command line and no
    # file.
    classes = [("token", [read_token()]), ("redact", read_redact_words()), ("homeprefix", [home_prefix()])]
    outputs = list_outputs()
    total = 0
    for path in outputs:
        total += count_matches(path, f"{os.path.basename(OUT)}/{os.path.basename(path)}", classes)
    for path in DOCUMENTS:
        total += count_matches(path, path, classes)
    files = len(outputs) + len(DOCUMENTS)
    if total:
        emit(f"scan FOUND ({files} files, {total} matches)")
        return 1
    emit(f"scan clean ({files} files, 0 matches)")
    return 0


def indent_of(text):
    return len(text) - len(text.lstrip(" "))


def fence_of(text):
    # (fence length, info string) for a line that opens or closes a
    # backtick fence; None for any other line.
    stripped = text.lstrip(" ")
    if not stripped.startswith(FENCE):
        return None
    length = len(stripped) - len(stripped.lstrip(FENCE[0]))
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


def raw_print_sites(block):
    # Lines of a Python block that print or write outside the bodies of
    # emit and refuse, by the line ranges ast gives those two functions.
    tree = ast.parse("\n".join(block) + "\n")
    allowed = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name in ("emit", "refuse"):
            allowed.update(range(node.lineno, node.end_lineno + 1))
    return sum(1 for number, text in enumerate(block, 1) if number not in allowed and any(mark in text for mark in PRINTS))


def on_form(block):
    # True for a block of exactly one line `python3 -I U116-procedure.py
    # <subcommand>` with one name behind inject and nothing behind the rest.
    if len(block) != 1:
        return False
    words = block[0].split(" ")
    if words[: len(FORM)] != FORM:
        return False
    rest = words[len(FORM) :]
    if not rest or rest[0] not in SUBCOMMANDS:
        return False
    return len(rest) == (2 if rest[0] == "inject" else 1)


def forms(path):
    # The forms counts of one document: fenced block counts by kind, sh
    # blocks off the one-line form, and the four line classes. Returns the
    # result line, the count of what must be zero, and the python-blocks
    # count (judged by the caller).
    lines = read_file(path).decode().split("\n")
    state = None  # None outside a fence; else (kind, fence length)
    block = []
    counts = {"python": 0, "sh": 0, "text": 0, "other": 0, "off-form": 0, "producer": 0, "swallow": 0, "wrapper": 0, "raw-print": 0}
    for text in lines:
        fence = fence_of(text)
        if state is None:
            if fence is not None:
                length, info = fence
                kind = "sh" if info in SHELL else "python" if info in PYTHON else "text" if info in TEXT else "other"
                counts[kind] += 1
                state = (kind, length)
                block = []
            continue
        kind, length = state
        if fence is not None and fence[1] == "" and fence[0] >= length:
            if kind == "sh":
                counts["producer"] += sum(1 for line in block if any(mark in line for mark in MARKS))
                counts["wrapper"] += shell_wrapper_lines(block)
                counts["off-form"] += not on_form(block)
            if kind == "python":
                counts["swallow"] += sum(1 for line in block if any(name in line for name in NAMES))
                counts["swallow"] += sum(1 for index in range(len(block)) if swallows(block, index))
                counts["wrapper"] += python_wrapper_lines(block)
                counts["raw-print"] += raw_print_sites(block)
            state = None
            continue
        block.append(text)
    if state is not None:
        raise ValueError(f"{path} ends inside a fenced block")
    line = (
        f"{path} python-blocks={counts['python']} sh-blocks={counts['sh']} sh-blocks-off-form={counts['off-form']}"
        f" text-blocks={counts['text']} other-blocks={counts['other']} producer-lines={counts['producer']}"
        f" swallow-lines={counts['swallow']} wrapper-lines={counts['wrapper']} raw-print-sites={counts['raw-print']}"
    )
    bad = counts["other"] + counts["off-form"] + counts["producer"] + counts["swallow"] + counts["wrapper"] + counts["raw-print"]
    return line, bad, counts["python"]


def check():
    failures = 0
    proc = run(["git", "-C", WORKTREE, "diff", "--name-only", f"{MERGE_BASE}..HEAD"], 60)
    names = proc.stdout.decode().split()
    emit(f"git diff --name-only {MERGE_BASE}..HEAD exit={proc.returncode} paths={len(names)}")
    for name in names:
        emit(f"  {name}")
    failures += proc.returncode != 0 or names != [RELATIVE]
    proc = run(["prettier", "--check", "--ignore-path", "/dev/null", EVALUATION], 120, stderr=subprocess.STDOUT)
    emit(f"prettier --check --ignore-path /dev/null {RELATIVE} exit={proc.returncode}")
    for line in proc.stdout.decode().splitlines():
        emit(f"  {line}")
    failures += proc.returncode != 0
    lines = read_file(EVALUATION).decode().split("\n")
    found = [(number, text) for number, text in enumerate(lines, 1) if text.startswith("## ")]
    for number, text in found:
        emit(f"{number}:{text}")
    ordered = [text for number, text in found] == list(HEADINGS)
    emit(f"headings={len(found)} order={'ok' if ordered else 'MISMATCH'}")
    failures += not ordered
    rows = sum(1 for text in lines if len(text.split("\t")) == 6 and text.split("\t")[1] == "plan-P-36")
    emit(f"draft-rows={rows}")
    failures += rows != 1
    outcome = check_lock()
    emit(f"g-none-written: {outcome}")
    failures += outcome != "none-written"
    before = read_file(out_path("real-before.txt")).decode()
    after = read_file(out_path("real-after.txt")).decode()
    for label, text in (("real-before.txt", before), ("real-after.txt", after)):
        emit(f"{label}:")
        for line in text.splitlines():
            emit(f"  {line}")
    same = before == after
    lock_lines = [line for line in before.splitlines() + after.splitlines() if line.endswith("/mise.lock")]
    emit(f"real-dirs before=after: {'same' if same else 'DIFFER'}; mise.lock lines={len(lock_lines)}")
    failures += (not same) + len(lock_lines)
    for path in DOCUMENTS:
        line, bad, python_blocks = forms(path)
        emit(line)
        failures += bad != 0
        failures += python_blocks != (1 if path == EVALUATION else 0)
    emit("check ok" if not failures else f"check FAILED ({failures} items)")
    return 1 if failures else 0


def patch_lstat(blocked, error):
    # os.lstat replaced for one path: it raises the named error there (or
    # for None returns this script's own stat result, standing in for a
    # written lockfile) and answers every other path as before.
    real_lstat = os.lstat

    def injected(path, *args, **kwargs):
        if path != blocked:
            return real_lstat(path, *args, **kwargs)
        if error is None:
            return real_lstat(__file__)
        kind, errno, text = error
        raise kind(errno, text, path)

    os.lstat = injected


def config_listing(label, mise):
    # One `mise config ls` under ENV, through timed(); the output lines are
    # emitted indented and returned for comparison.
    name = f"config-ls-{label}"
    timed(name, [mise, "config", "ls"], TIMEOUT)
    lines = read_file(out_path(f"{name}.txt")).decode().splitlines()
    emit(f"{name}.txt ({len(lines)} lines):")
    for line in lines:
        emit(f"  {line}")
    return lines


def inject(name):
    # Each case patches this process (PATH, a global, os.lstat, a function)
    # or builds fixtures under a fresh mkdtemp directory, then runs the
    # subcommand's own function, so the exit status is that code path's
    # own; nothing lands in the receipt's output directory and the real
    # mise is never touched. The fixture directory is removed when the
    # case ends, however it ends. No case writes a credential: the
    # planted-token case replaces the token class with a synthetic marker
    # and never calls gh.
    if name not in INJECTIONS:
        refuse(f"unknown injection {name}")
    if name not in STANDALONE:
        load_receipt()
    root = scratch_dir(INJECT_PREFIX)
    emit(f"fixtures: {root} (removed when this case ends)")
    try:
        return inject_case(name, root)
    finally:
        shutil.rmtree(root)


def inject_case(name, root):
    global OUT, TIMEOUT, EXPECTED_FILES, REDACT_LIST, TOKEN_SOURCE, ENV, token_bytes
    empty = os.path.join(root, "empty")
    mkdir(empty)
    if name == "missing-mise":
        os.environ["PATH"] = empty
        emit(f"case {name}: PATH={empty}; run")
        return dry_runs()
    if name == "missing-gh":
        os.environ["PATH"] = empty
        emit(f"case {name}: PATH={empty}; scan")
        return scan()
    if name == "missing-git":
        os.environ["PATH"] = empty
        emit(f"case {name}: PATH={empty}; check")
        return check()
    if name == "missing-prettier":
        only_git = os.path.join(root, "only-git")
        mkdir(only_git)
        os.symlink(resolve("git", os.environ["PATH"]), os.path.join(only_git, "git"))
        os.environ["PATH"] = only_git
        emit(f"case {name}: PATH={only_git} (a symlink to git alone); check")
        return check()
    if name == "lookup-permission":
        entry = os.path.join(HOME, "bin")
        blocked = os.path.join(entry, "mise")
        patch_lstat(blocked, (PermissionError, 13, "Permission denied"))
        os.environ["PATH"] = entry + os.pathsep + os.environ["PATH"]
        emit(f"case {name}: PATH starts with {entry}; os.lstat of {blocked} raises PermissionError; run")
        return dry_runs()
    if name == "run-timeout":
        sleeper = os.path.join(root, "sleeper")
        mkdir(sleeper)
        # /bin/wait4path blocks until its argument exists as a path; the
        # argument is `--version`, so the fake mise never returns.
        os.symlink("/bin/wait4path", os.path.join(sleeper, "mise"))
        os.environ["PATH"] = sleeper + os.pathsep + os.environ["PATH"]
        OUT = os.path.join(root, "out")
        mkdir(OUT)
        TIMEOUT = 2
        emit(f"case {name}: PATH starts with {sleeper} (mise is a symlink to /bin/wait4path); OUT={OUT}; TIMEOUT=2; run")
        return dry_runs()
    if name in ("lock-notadirectory", "lock-permission", "lock-missing"):
        errors = {
            "lock-notadirectory": (NotADirectoryError, 20, "Not a directory"),
            "lock-permission": (PermissionError, 13, "Permission denied"),
            "lock-missing": (FileNotFoundError, 2, "No such file or directory"),
        }
        patch_lstat(LOCK, errors[name])
        emit(f"case {name}: os.lstat of {LOCK} raises {errors[name][0].__name__}; check_lock")
        outcome = check_lock()
        emit(f"g-none-written: {outcome}")
        return 0 if outcome == "none-written" else 1
    if name == "txt-count":
        EXPECTED_FILES -= 1
        emit(f"case {name}: EXPECTED_FILES={EXPECTED_FILES}; scan")
        return scan()
    if name == "redact-comment-only":
        comments = [line for line in read_file(os.path.expanduser(REDACT_LIST)).splitlines() if line.startswith(b"#")]
        REDACT_LIST = os.path.join(root, "redact-comment-only.txt")
        write_file(REDACT_LIST, b"\n".join(comments) + b"\n")
        emit(f"case {name}: REDACT_LIST={REDACT_LIST} ({len(comments)} comment lines, nothing else); scan")
        return scan()
    if name == "missing-out":
        OUT = os.path.join(root, "no-such-out")
        emit(f"case {name}: OUT={OUT}; scan")
        return scan()
    if name == "planted-token":
        # The token class is a synthetic marker (a fixed prefix and 16
        # random hex digits), never the live token: token_bytes is replaced
        # in this process, so gh auth token is not called. The marker is
        # appended to a copy of one output file among copies under the
        # fixture directory (never the receipt's output directory), the
        # scan runs over the copy set, and the directory is removed when
        # the case ends.
        marker = (SYNTHETIC + secrets.token_hex(8)).encode()

        def synthetic():
            return marker

        token_bytes = synthetic
        TOKEN_SOURCE = "the synthetic marker"
        copies = list_outputs()
        target = "a-version.txt"
        for path in copies:
            data = read_file(path)
            if os.path.basename(path) == target:
                data += marker + b"\n"
            write_file(os.path.join(root, os.path.basename(path)), data)
        OUT = root
        emit(f"case {name}: the token class is the marker {marker.decode()} (gh is not called); {len(copies)} copies under {root}, the marker appended to the copy of {target}; scan")
        return scan()
    if name == "user-lookup":
        # getpass.getuser raises OSError, as it does for a UID without a
        # passwd entry when no name variable is set; USER is removed so the
        # fallback has nothing; arm() runs again as main() ran it and
        # refuses. The table from the first arm() stays, so the refusal is
        # redacted; before the first arm() the same text holds no path.

        def unmapped():
            raise OSError("No username set in the environment")

        getpass.getuser = unmapped
        if "USER" in os.environ:
            del os.environ["USER"]
        emit(f"case {name}: getpass.getuser raises OSError; USER unset; arm")
        arm()
        emit(f"arm: {len(REDACTIONS)} redactions")
        return 0
    if name == "forms-producer":
        copy = os.path.join(root, "forms-producer.md")
        lines = read_file(EVALUATION).decode().split("\n")
        index = lines.index(FENCE + "sh")
        lines.insert(index + 1, "true " + "$" + "(true)")
        write_file(copy, "\n".join(lines))
        emit(f"case {name}: {copy} is this file with `{lines[index + 1]}` inserted at line {index + 2}, inside its first sh block; forms")
        line, bad, python_blocks = forms(copy)
        emit(line)
        return 1 if bad else 0
    if name == "create-symlink":
        # A symlink waits at the output path timed() will create (the
        # round-10 verdict's first finding: a write-mode open followed it
        # and truncated its target). create() refuses it with
        # FileExistsError before any launch, the receipt reads exit=refused,
        # and the target's size is the same before and after.
        target = os.path.join(root, "target.txt")
        write_file(target, b"the symlink's target: 46 bytes that must stay\n")
        out = os.path.join(root, "out")
        mkdir(out)
        link = os.path.join(out, "a-version.txt")
        os.symlink(target, link)
        OUT = out
        mise = resolve("mise", os.environ["PATH"])
        emit(f"case {name}: {link} is a symlink to {target} ({os.lstat(target).st_size} bytes); OUT={out}; timed a-version")
        try:
            return timed("a-version", [mise, "--version"], TIMEOUT)
        finally:
            emit(f"target after: {os.lstat(target).st_size} bytes; the link is still a symlink: {stat.S_ISLNK(os.lstat(link).st_mode)}")
    if name == "planted-config":
        # A fresh scratch home of its own; `mise config ls` under ENV before
        # and after configs are planted where mise would look without the
        # discovery variables (the cwd's parent, the cwd, a .tool-versions,
        # the system config directory); the two listings must be the same.
        # The negative control runs the same listing with the CHANGE 1
        # variables alone, where the planted files are read, so the case
        # cannot pass vacuously.
        scratch = scratch_dir(HOME_PREFIX)
        try:
            make_scratch(scratch)
            set_scratch(scratch, root)
            mise = resolve("mise", os.environ["PATH"])
            os.chdir(CWD)
            emit(f"case {name}: scratch={scratch} (removed when this case ends); cwd={CWD}; config ls before, plant, config ls after, then the control")
            before = config_listing("before", mise)
            for relative, text in PLANTS:
                write_file(os.path.join(scratch, relative), text)
            emit(f"planted: {', '.join(relative for relative, text in PLANTS)} under {scratch}")
            after = config_listing("after", mise)
            discovery = ENV
            ENV = {key: discovery[key] for key in CHANGE_1_KEYS}
            emit(f"control: ENV reduced to {', '.join(CHANGE_1_KEYS)}")
            control = config_listing("control", mise)
            # The second control: the discovery variables with the ceiling
            # removed and the override filename variable empty, the value
            # the brief asked for; this mise reads an empty value as unset,
            # so the planted mise.toml files are listed, which is why ENV
            # carries a sentinel name instead.
            ENV = {key: discovery[key] for key in discovery if key != "MISE_CEILING_PATHS"}
            ENV["MISE_OVERRIDE_CONFIG_FILENAMES"] = ""
            emit("control: ENV without MISE_CEILING_PATHS and with MISE_OVERRIDE_CONFIG_FILENAMES empty")
            empty = config_listing("empty-override", mise)
            ENV = discovery
            unchanged = before == after
            detected = control != before
            ignored = empty != before
            emit(f"config ls under ENV: {'unchanged' if unchanged else 'CHANGED'}; under the CHANGE 1 variables alone: {'the planted configs are listed' if detected else 'NOT DETECTED'}; with the empty override value: {'planted files listed, so the empty value is ignored' if ignored else 'unchanged'}")
            return 0 if unchanged and detected else 1
        finally:
            os.chdir(TMPDIR)
            shutil.rmtree(scratch)
    refuse(f"unknown injection {name}")


def main():
    global COMMAND
    try:
        argv = sys.argv[1:]
        if argv:
            COMMAND = " ".join(argv)
        arm()
        if not argv or argv[0] not in SUBCOMMANDS:
            refuse(f"usage: python3 -I U116-procedure.py {'|'.join(SUBCOMMANDS)} [name]")
        if len(argv) != (2 if argv[0] == "inject" else 1):
            refuse("inject takes one name; the other subcommands take none")
        configure()
        if argv[0] == "inject":
            sys.exit(inject(argv[1]))
        if argv[0] != "prepare":
            load_receipt()
        sys.exit({"prepare": prepare, "run": dry_runs, "scan": scan, "check": check}[argv[0]]())
    except BaseException as exc:
        if isinstance(exc, SystemExit) and exc.code in EXITS:
            raise
        refuse(f"{type(exc).__name__}: {exc}")


if __name__ == "__main__":
    main()
```

### `prepare`

```sh
python3 -I U116-procedure.py prepare
```

```text
mkdtemp: $TMPDIR/U116-home-<tmp> and $TMPDIR/U116-out-<tmp> (mode 0700)
mkdir: .config .config/mise .local .local/share .cache .local/state cwd etc etc/mise under $TMPDIR/U116-home-<tmp> (mode 0700)
copy: 6962 bytes to $TMPDIR/U116-home-<tmp>/.config/mise/config.toml
receipt: $TMPDIR/U116-prepare.receipt.txt names scratch=$TMPDIR/U116-home-<tmp> out=$TMPDIR/U116-out-<tmp> (written, read back, both directories this user's)
real-before: 6 lines to $TMPDIR/U116-out-<tmp>/real-before.txt
exit=0
```

`real-before.txt`, the listing of the real `~/.config/mise` and its entries and of the other four real mise directories (mode, size, modification time, path), taken before any mise call. mise on macOS keeps its cache under `~/Library/Caches/mise`, so `~/.cache/mise` does not exist on this host:

```text
drwxr-xr-x     96 2026-10-26T23:40:46 ~/.config/mise
-rw-r--r--   6962 2026-10-26T23:40:46 ~/.config/mise/config.toml
drwxr-xr-x    256 2026-10-29T19:43:40 ~/.local/share/mise
missing ~/.cache/mise
drwxr-xr-x    256 2026-10-29T18:57:51 ~/.local/state/mise
drwxr-xr-x   1536 2026-10-29T18:57:42 ~/Library/Caches/mise
```

### `run`

```sh
python3 -I U116-procedure.py run
```

```text
mise=~/.local/bin/mise (PATH entry 51 of 55)
cwd=$TMPDIR/U116-home-<tmp>/cwd
env (the whole environment of every mise call):
  HOME=$TMPDIR/U116-home-<tmp>
  PATH=<55 entries, inherited>
  TMPDIR=$TMPDIR/
  XDG_CONFIG_HOME=$TMPDIR/U116-home-<tmp>/.config
  XDG_DATA_HOME=$TMPDIR/U116-home-<tmp>/.local/share
  XDG_CACHE_HOME=$TMPDIR/U116-home-<tmp>/.cache
  XDG_STATE_HOME=$TMPDIR/U116-home-<tmp>/.local/state
  MISE_TRUSTED_CONFIG_PATHS=$TMPDIR/U116-home-<tmp>/.config/mise/config.toml
  MISE_CONFIG_DIR=$TMPDIR/U116-home-<tmp>/.config/mise
  MISE_GLOBAL_CONFIG_FILE=$TMPDIR/U116-home-<tmp>/.config/mise/config.toml
  MISE_SYSTEM_CONFIG_DIR=$TMPDIR/U116-home-<tmp>/etc/mise
  MISE_SYSTEM_CONFIG_FILE=$TMPDIR/U116-home-<tmp>/etc/mise/none.toml
  MISE_CEILING_PATHS=$TMPDIR/U116-home-<tmp>/cwd:$TMPDIR/U116-home-<tmp>/cwd
  MISE_IGNORED_CONFIG_PATHS=~/.config/mise:/etc/mise:/private/etc/mise
  MISE_OVERRIDE_CONFIG_FILENAMES=U116-none.toml
  MISE_OVERRIDE_TOOL_VERSIONS_FILENAMES=none
a-version: start=2026-10-29T16:15:31Z end=2026-10-29T16:15:37Z elapsed=6s exit=0
help-lock: start=2026-10-29T16:15:37Z end=2026-10-29T16:15:37Z elapsed=0s exit=0
b-lock-dry-run: start=2026-10-29T16:15:37Z end=2026-10-29T16:15:46Z elapsed=10s exit=0
c-lock-dry-run-4-platforms: start=2026-10-29T16:15:46Z end=2026-10-29T16:15:46Z elapsed=0s exit=0
d-lock-bump-json: start=2026-10-29T16:15:46Z end=2026-10-29T16:15:46Z elapsed=0s exit=0
e-npm-package-manager: start=2026-10-29T16:15:46Z end=2026-10-29T16:15:47Z elapsed=0s exit=0
f-minimum-release-age: start=2026-10-29T16:15:47Z end=2026-10-29T16:15:47Z elapsed=0s exit=0
h-config-ls: start=2026-10-29T16:15:47Z end=2026-10-29T16:15:47Z elapsed=0s exit=0
h-config-ls-json: start=2026-10-29T16:15:47Z end=2026-10-29T16:15:47Z elapsed=0s exit=0
g-none-written: none-written
runs=9 failed=0
exit=0
```

Each output file of the run, with its receipt as the procedure printed it.

(a) `mise --version`, `a-version.txt`, receipt `start=2026-10-29T16:15:31Z end=2026-10-29T16:15:37Z elapsed=6s exit=0`:

```text
2026.10.19 macos-arm64 (2026-10-24)
```

`mise lock --help`, `help-lock.txt`, receipt `start=2026-10-29T16:15:37Z end=2026-10-29T16:15:37Z elapsed=0s exit=0`; the eight lines CHANGE 1 asks for are the first eight; the file is pasted whole, 183 lines:

```text
Create or refresh lockfile versions, checksums, and download URLs

Operates on the current config root, including tools declared by tasks.
Existing matching locked versions are preserved unless `--bump` re-resolves
their requests. This command does not install tools; `--dry-run` previews
changes.

`mise lock TOOL@VERSION` locks that exact version. When the version falls
outside the configured request, such as `tiny@3.0.1` with `tiny = "2"`, mise
also updates the request in mise.toml to match.

Usage: mise lock [FLAGS] [TOOL]…

Arguments:
  [TOOL]…  Tools to lock, such as `node python`; defaults to every configured
           tool and every tool a task needs

           Use `tool@version` to lock an exact version. If it falls outside the
           configured
           request, mise.toml is updated to match.

Flags:
  -g, --global                    Lock only the global and system config
                                  lockfiles

                                  These are ~/.config/mise/mise.lock and the
                                  system config's lockfile. By
                                  default, only the current project's config
                                  root is locked.
  -j, --jobs <JOBS>               How many jobs to run in parallel; defaults to
                                  the `jobs` setting

                                  Values below 1 are treated as 1.
                                  [env: MISE_JOBS]
  -n, --dry-run                   Show what would change, without writing
                                  anything
  -p, --platform <PLATFORM>       Platforms to lock, comma-separated, such as
                                  `linux-x64,macos-arm64`

                                  Defaults to the `lockfile_platforms` setting
                                  plus the current platform when
                                  that setting is configured, else the platforms
                                  already in the lockfile, else
                                  a common set for a new lockfile.
      --bump                      Re-resolve version requests against the latest
                                  available versions

                                  By default, `mise lock` refreshes metadata for
                                  the currently locked versions.
                                  With this flag, requests such as "latest",
                                  "lts", or prefixes such as "24" are
                                  re-resolved against the latest matching remote
                                  versions, so the lockfile
                                  advances without installing anything. `--bump`
                                  never modifies config files:
                                  exact versions resolve to themselves and stay
                                  unchanged (use
                                  `mise upgrade --bump` to rewrite pins in
                                  mise.toml). If the remote versions
                                  cannot be fetched, it fails rather than keep
                                  the locked version.
      --json                      Output version changes as JSON

                                  Prints an array of objects describing lockfile
                                  version changes:
                                  name, backend, lockfile, old_versions,
                                  new_versions.
                                  Version lists keep config/lockfile order; they
                                  are not sorted.
                                  Only version-level changes are reported:
                                  checksum and URL refreshes for
                                  unchanged versions produce no entries, so
                                  `mise lock --json` prints `[]`
                                  when no version changed, even though it still
                                  updates the lockfile.
                                  Suppresses the human-readable output. Combine
                                  with `--dry-run` to
                                  detect available updates without writing the
                                  lockfile.
      --local                     Update mise.local.lock, for tools in
                                  mise.local.toml, instead of mise.lock
      --minimum-release-age <AGE>  Only lock versions released before a date or
                                  at least a duration ago

                                  Takes a date such as `2024-06-01` or a
                                  duration such as `90d` or `1y`.
                                  Overrides the `minimum_release_age` setting
                                  and tool option. It filters only
                                  requests that are not exact, such as "24" or
                                  "latest"; exact versions such
                                  as "24.11.0" are not filtered. Existing
                                  matching lockfile entries are kept;
                                  this flag alone does not downgrade them.
      --upgrade                   Upgrade lockfiles to the latest format

                                  mise keeps an existing lockfile at its format
                                  version during normal updates,
                                  so collaborators on an older mise can still
                                  read it. This flag rewrites it in
                                  the newest format, which adds request
                                  bindings, dependency-graph sidecars,
                                  and packslip repository IDs. It processes
                                  every configured tool and cannot be
                                  combined with tool arguments. See
                                  https://mise.jdx.dev/dev-tools/mise-lock-reference.html#format-versions.
      --sidecars                  List native dependency sidecars instead of
                                  updating lockfiles

                                  Backends such as npm and pypi keep a tool's
                                  locked dependency graph in a
                                  sidecar directory next to mise.lock; see
                                  https://mise.jdx.dev/dev-tools/mise-lock-reference.html#native-dependency-sidecars.
                                  For each existing lockfile in scope, prints
                                  the sidecar directory mise keeps
                                  its dependency graphs in and every sidecar
                                  directory the lockfile references.
                                  Nothing is resolved, installed, or written.
                                  Paths are relative to the current directory
                                  when they are inside it,
                                  and absolute otherwise, such as the sidecars
                                  of a symlinked lockfile.
                                  Combine with `--json` for machine-readable
                                  output, or with `--local`
                                  and `--global` to choose the lockfiles.
  -h, --help                      Print help

Global flags:
  -C, --cd <DIR>                  Run as if mise were started in DIR
  -E, --env <ENV>                 Load the `mise.<ENV>.toml` config files (same
                                  as MISE_ENV)

                                  Repeat the flag or separate names with commas
                                  to load several environments.
  -q, --quiet                     Suppress non-error messages
                                  [env: MISE_QUIET]
  -v, --verbose                   Show extra output (use -vv for even more)
  -y, --yes                       Answer yes to all confirmation prompts
      --raw                       Connect tasks and install commands directly to
                                  the terminal

                                  Commands then run one at a time. Same as
                                  `MISE_RAW=1` or the `raw` setting.
      --locked                    Require download URLs from the lockfile when
                                  installing

                                  Installing fails when the lockfile has no
                                  pre-resolved URL for a tool on the current
                                  platform, so mise does not call the GitHub or
                                  aqua registry APIs to find one. Same as
                                  `MISE_LOCKED=1` or the `locked` setting.
      --silent                    Suppress all task output and mise non-error
                                  messages

Examples:
    Create or refresh the project lockfile
    $ mise lock

    Refresh only node and python
    $ mise lock node python

    Lock an exact version; mise.toml keeps a request such as "24"
    $ mise lock node@24.11.0

    Lock only the linux-x64 platform
    $ mise lock --platform linux-x64

    Show what would change
    $ mise lock --dry-run

    Re-resolve requests such as "latest" or "24" to the latest matching versions
    $ mise lock --bump

    List available updates as JSON without writing
    $ mise lock --bump --dry-run --json

    Lock versions released before 2024-01-01 for requests that are not exact
    $ mise lock --minimum-release-age 2024-01-01

    Update mise.local.lock
    $ mise lock --local

    Update only the global lockfiles
    $ mise lock --global
```

(b) `mise lock --global --dry-run`, `b-lock-dry-run.txt`, receipt `start=2026-10-29T16:15:37Z end=2026-10-29T16:15:46Z elapsed=10s exit=0` (`~` in the first line is the scratch home, `HOME` of `ENV`):

```text
→ Targeting 7 platform(s) for ~/.config/mise/mise.lock: linux-arm64, linux-arm64-musl, linux-x64, linux-x64-musl, macos-arm64, macos-x64, windows-x64
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

(c) `mise lock --global --dry-run --platform linux-x64,linux-arm64,macos-x64,macos-arm64`, `c-lock-dry-run-4-platforms.txt`, receipt `start=2026-10-29T16:15:46Z end=2026-10-29T16:15:46Z elapsed=0s exit=0`:

```text
→ Targeting 4 platform(s) for ~/.config/mise/mise.lock: linux-arm64, linux-x64, macos-arm64, macos-x64
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

(d) `mise lock --global --dry-run --bump --json`, `d-lock-bump-json.txt`, receipt `start=2026-10-29T16:15:46Z end=2026-10-29T16:15:46Z elapsed=0s exit=0`:

```text
[
  {
    "name": "node",
    "backend": "core:node",
    "lockfile": "~/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "26.12.1"
    ]
  },
  {
    "name": "rust",
    "backend": "core:rust",
    "lockfile": "~/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "1.99.1"
    ]
  },
  {
    "name": "python",
    "backend": "core:python",
    "lockfile": "~/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "3.15.2"
    ]
  },
  {
    "name": "age",
    "backend": "aqua:FiloSottile/age",
    "lockfile": "~/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "1.3.2"
    ]
  },
  {
    "name": "bun",
    "backend": "core:bun",
    "lockfile": "~/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "1.4.4"
    ]
  },
  {
    "name": "chezmoi",
    "backend": "aqua:twpayne/chezmoi",
    "lockfile": "~/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "2.73.3"
    ]
  },
  {
    "name": "dotenvx",
    "backend": "aqua:dotenvx/dotenvx",
    "lockfile": "~/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "2.38.2"
    ]
  },
  {
    "name": "cargo:eza",
    "backend": "cargo:eza",
    "lockfile": "~/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "0.23.5"
    ]
  },
  {
    "name": "fd",
    "backend": "aqua:sharkdp/fd",
    "lockfile": "~/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "10.5.0"
    ]
  },
  {
    "name": "jq",
    "backend": "aqua:jqlang/jq",
    "lockfile": "~/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "1.8.2"
    ]
  },
  {
    "name": "hugo-extended",
    "backend": "aqua:gohugoio/hugo/hugo-extended",
    "lockfile": "~/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "0.168.0"
    ]
  },
  {
    "name": "uv",
    "backend": "aqua:astral-sh/uv",
    "lockfile": "~/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "0.13.5"
    ]
  },
  {
    "name": "yazi",
    "backend": "aqua:sxyazi/yazi",
    "lockfile": "~/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "26.9.1"
    ]
  },
  {
    "name": "aqua:micro-editor/micro",
    "backend": "aqua:micro-editor/micro",
    "lockfile": "~/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "2.0.15"
    ]
  },
  {
    "name": "aqua:mikefarah/yq",
    "backend": "aqua:mikefarah/yq",
    "lockfile": "~/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "4.54.1"
    ]
  },
  {
    "name": "aqua:watchexec/watchexec",
    "backend": "aqua:watchexec/watchexec",
    "lockfile": "~/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "2.8.0"
    ]
  },
  {
    "name": "npm:@anthropic-ai/claude-code",
    "backend": "npm:@anthropic-ai/claude-code",
    "lockfile": "~/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "2.1.310"
    ]
  },
  {
    "name": "npm:@openai/codex",
    "backend": "npm:@openai/codex",
    "lockfile": "~/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "0.164.0"
    ]
  },
  {
    "name": "npm:@anthropic-ai/sandbox-runtime",
    "backend": "npm:@anthropic-ai/sandbox-runtime",
    "lockfile": "~/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "0.0.81"
    ]
  },
  {
    "name": "npm:bash-language-server",
    "backend": "npm:bash-language-server",
    "lockfile": "~/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "5.8.1"
    ]
  },
  {
    "name": "npm:ccstatusline",
    "backend": "npm:ccstatusline",
    "lockfile": "~/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "2.2.32"
    ]
  },
  {
    "name": "npm:ccusage",
    "backend": "npm:ccusage",
    "lockfile": "~/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "20.0.37"
    ]
  },
  {
    "name": "npm:pyright",
    "backend": "npm:pyright",
    "lockfile": "~/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "1.1.414"
    ]
  },
  {
    "name": "npm:fast-cli",
    "backend": "npm:fast-cli",
    "lockfile": "~/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "6.0.0"
    ]
  },
  {
    "name": "npm:prettier",
    "backend": "npm:prettier",
    "lockfile": "~/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "3.9.10"
    ]
  },
  {
    "name": "npm:pnpm",
    "backend": "npm:pnpm",
    "lockfile": "~/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "12.8.1"
    ]
  },
  {
    "name": "github:x-motemen/ghq",
    "backend": "github:x-motemen/ghq",
    "lockfile": "~/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "1.11.2"
    ]
  },
  {
    "name": "github:d-kuro/gwq",
    "backend": "github:d-kuro/gwq",
    "lockfile": "~/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "0.1.2"
    ]
  },
  {
    "name": "github:cli/cli",
    "backend": "github:cli/cli",
    "lockfile": "~/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "2.103.2"
    ]
  },
  {
    "name": "github:ogulcancelik/herdr",
    "backend": "github:ogulcancelik/herdr",
    "lockfile": "~/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "0.9.5"
    ]
  },
  {
    "name": "cargo:pueue",
    "backend": "cargo:pueue",
    "lockfile": "~/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "4.0.4"
    ]
  },
  {
    "name": "http:bats",
    "backend": "http:bats",
    "lockfile": "~/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "1.14.0"
    ]
  },
  {
    "name": "http:gcloud",
    "backend": "http:gcloud",
    "lockfile": "~/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "590.0.0"
    ]
  },
  {
    "name": "http:shellcheck",
    "backend": "http:shellcheck",
    "lockfile": "~/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "0.11.0"
    ]
  },
  {
    "name": "http:shfmt",
    "backend": "http:shfmt",
    "lockfile": "~/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "3.14.1"
    ]
  },
  {
    "name": "http:ruff",
    "backend": "http:ruff",
    "lockfile": "~/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "0.17.2"
    ]
  }
]
```

(e) `mise settings get npm.package_manager`, `e-npm-package-manager.txt`, receipt `start=2026-10-29T16:15:46Z end=2026-10-29T16:15:47Z elapsed=0s exit=0`:

```text
npm
```

(f) `mise settings get minimum_release_age`, `f-minimum-release-age.txt`, receipt `start=2026-10-29T16:15:47Z end=2026-10-29T16:15:47Z elapsed=0s exit=0`:

```text
72h
```

(h) `mise config ls`, `h-config-ls.txt`, receipt `start=2026-10-29T16:15:47Z end=2026-10-29T16:15:47Z elapsed=0s exit=0`: the config files mise loaded under `ENV`, lowest precedence first; one file, the scratch copy, shown by mise relative to `HOME` (the scratch home):

```text
~/.config/mise/config.toml  node, rust, python, age, bun, chezmoi, dotenvx, cargo:eza, fd, jq, hugo-extended, uv, yazi, aqua:micro-editor/micro, aqua:mikefarah/yq, aqua:watchexec/watchexec, npm:@anthropic-ai/claude-code, npm:@openai/codex, npm:@anthropic-ai/sandbox-runtime, npm:bash-language-server, npm:ccstatusline, npm:ccusage, npm:pyright, npm:fast-cli, npm:prettier, npm:pnpm, github:x-motemen/ghq, github:d-kuro/gwq, github:cli/cli, github:ogulcancelik/herdr, cargo:pueue, http:bats, http:gcloud, http:shellcheck, http:shfmt, http:ruff
```

(h) `mise config ls --json`, `h-config-ls-json.txt`, receipt `start=2026-10-29T16:15:47Z end=2026-10-29T16:15:47Z elapsed=0s exit=0`: the same one file by its full path (this run's `mkdtemp` suffix), `"override": false`:

```text
[
  {
    "path": "/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home-x7nejo4d/.config/mise/config.toml",
    "tools": [
      "node",
      "rust",
      "python",
      "age",
      "bun",
      "chezmoi",
      "dotenvx",
      "cargo:eza",
      "fd",
      "jq",
      "hugo-extended",
      "uv",
      "yazi",
      "aqua:micro-editor/micro",
      "aqua:mikefarah/yq",
      "aqua:watchexec/watchexec",
      "npm:@anthropic-ai/claude-code",
      "npm:@openai/codex",
      "npm:@anthropic-ai/sandbox-runtime",
      "npm:bash-language-server",
      "npm:ccstatusline",
      "npm:ccusage",
      "npm:pyright",
      "npm:fast-cli",
      "npm:prettier",
      "npm:pnpm",
      "github:x-motemen/ghq",
      "github:d-kuro/gwq",
      "github:cli/cli",
      "github:ogulcancelik/herdr",
      "cargo:pueue",
      "http:bats",
      "http:gcloud",
      "http:shellcheck",
      "http:shfmt",
      "http:ruff"
    ],
    "override": false
  }
]
```

(g) `g-scratch-after.txt`, the scratch `.config/mise` after all runs (no `mise.lock`; the path through `redact`):

```text
drwx------     96 2026-10-30T01:15:31 $TMPDIR/U116-home-<tmp>/.config/mise
-rw-------   6962 2026-10-30T01:15:31 $TMPDIR/U116-home-<tmp>/.config/mise/config.toml
```

(g) `real-after.txt`, the real mise directories after all runs, byte for byte `real-before.txt` (`check` below compares them):

```text
drwxr-xr-x     96 2026-10-26T23:40:46 ~/.config/mise
-rw-r--r--   6962 2026-10-26T23:40:46 ~/.config/mise/config.toml
drwxr-xr-x    256 2026-10-29T19:43:40 ~/.local/share/mise
missing ~/.cache/mise
drwxr-xr-x    256 2026-10-29T18:57:51 ~/.local/state/mise
drwxr-xr-x   1536 2026-10-29T18:57:42 ~/Library/Caches/mise
```

`g-none-written.txt`, from `check_lock` after the last call:

```text
none-written
```

`scratch-tree.txt`, what the scratch home holds after the run, four directory levels deep, each path through `redact`:

```text
$TMPDIR/U116-home-<tmp>
$TMPDIR/U116-home-<tmp>/.cache
$TMPDIR/U116-home-<tmp>/.cache/mise
$TMPDIR/U116-home-<tmp>/.cache/mise/bun
$TMPDIR/U116-home-<tmp>/.cache/mise/bun/remote_versions-f28b6.msgpack.z
$TMPDIR/U116-home-<tmp>/.cache/mise/cargo-eza
$TMPDIR/U116-home-<tmp>/.cache/mise/cargo-eza/remote_versions-cfe45.msgpack.z
$TMPDIR/U116-home-<tmp>/.cache/mise/cargo-pueue
$TMPDIR/U116-home-<tmp>/.cache/mise/cargo-pueue/remote_versions-711b5.msgpack.z
$TMPDIR/U116-home-<tmp>/.cache/mise/github
$TMPDIR/U116-home-<tmp>/.cache/mise/github-cli-cli
$TMPDIR/U116-home-<tmp>/.cache/mise/github-cli-cli/remote_versions-fbf2d.msgpack.z
$TMPDIR/U116-home-<tmp>/.cache/mise/github/https-api-github-com-astral-sh-uv-latest-75f152cbb3234e33-hosted-2-2f6a0.msgpack.z
$TMPDIR/U116-home-<tmp>/.cache/mise/github/https-api-github-com-cli-cli-latest-c422894432b07a75-hosted-2-2f6a0.msgpack.z
$TMPDIR/U116-home-<tmp>/.cache/mise/github/https-api-github-com-cli-cli-versions-fdcb0a0009af6507-2f6a0.msgpack.z
$TMPDIR/U116-home-<tmp>/.cache/mise/github/https-api-github-com-d-kuro-gwq-latest-6c17f18eaf4e3a2b-hosted-2-2f6a0.msgpack.z
$TMPDIR/U116-home-<tmp>/.cache/mise/github/https-api-github-com-dotenvx-dotenvx-latest-851010c943271a76-hosted-2-2f6a0.msgpack.z
$TMPDIR/U116-home-<tmp>/.cache/mise/github/https-api-github-com-filo-sottile-age-latest-5aaeb641c690722-hosted-2-2f6a0.msgpack.z
$TMPDIR/U116-home-<tmp>/.cache/mise/github/https-api-github-com-gohugoio-hugo-latest-7e8a758b278d01f5-hosted-2-2f6a0.msgpack.z
$TMPDIR/U116-home-<tmp>/.cache/mise/github/https-api-github-com-jqlang-jq-latest-bdd9320085deaae5-hosted-2-2f6a0.msgpack.z
$TMPDIR/U116-home-<tmp>/.cache/mise/github/https-api-github-com-micro-editor-micro-latest-e2cefac8305717dd-hosted-2-2f6a0.msgpack.z
$TMPDIR/U116-home-<tmp>/.cache/mise/github/https-api-github-com-mikefarah-yq-latest-a3188cde7430c1ee-hosted-2-2f6a0.msgpack.z
$TMPDIR/U116-home-<tmp>/.cache/mise/github/https-api-github-com-ogulcancelik-herdr-latest-b515115e6d3664ca-hosted-2-2f6a0.msgpack.z
$TMPDIR/U116-home-<tmp>/.cache/mise/github/https-api-github-com-sharkdp-fd-latest-a69cff9e0d9ad20b-hosted-2-2f6a0.msgpack.z
$TMPDIR/U116-home-<tmp>/.cache/mise/github/https-api-github-com-sxyazi-yazi-latest-29d17fd18245505c-hosted-2-2f6a0.msgpack.z
$TMPDIR/U116-home-<tmp>/.cache/mise/github/https-api-github-com-twpayne-chezmoi-latest-ab43663cda310c28-hosted-2-2f6a0.msgpack.z
$TMPDIR/U116-home-<tmp>/.cache/mise/github/https-api-github-com-watchexec-watchexec-latest-130a48c37d16befe-hosted-2-2f6a0.msgpack.z
$TMPDIR/U116-home-<tmp>/.cache/mise/github/https-api-github-com-x-motemen-ghq-latest-1d789ce64118519b-hosted-2-2f6a0.msgpack.z
$TMPDIR/U116-home-<tmp>/.cache/mise/http-bats
$TMPDIR/U116-home-<tmp>/.cache/mise/http-gcloud
$TMPDIR/U116-home-<tmp>/.cache/mise/http-ruff
$TMPDIR/U116-home-<tmp>/.cache/mise/http-shellcheck
$TMPDIR/U116-home-<tmp>/.cache/mise/http-shfmt
$TMPDIR/U116-home-<tmp>/.cache/mise/latest-version.releases-v1
$TMPDIR/U116-home-<tmp>/.cache/mise/npm-anthropic-ai-claude-code
$TMPDIR/U116-home-<tmp>/.cache/mise/npm-anthropic-ai-claude-code/latest_version-999a7.msgpack.z
$TMPDIR/U116-home-<tmp>/.cache/mise/npm-anthropic-ai-claude-code/remote_versions-999a7.msgpack.z
$TMPDIR/U116-home-<tmp>/.cache/mise/npm-anthropic-ai-sandbox-runtime
$TMPDIR/U116-home-<tmp>/.cache/mise/npm-anthropic-ai-sandbox-runtime/latest_version-dab3a.msgpack.z
$TMPDIR/U116-home-<tmp>/.cache/mise/npm-anthropic-ai-sandbox-runtime/remote_versions-dab3a.msgpack.z
$TMPDIR/U116-home-<tmp>/.cache/mise/npm-bash-language-server
$TMPDIR/U116-home-<tmp>/.cache/mise/npm-bash-language-server/latest_version-1b050.msgpack.z
$TMPDIR/U116-home-<tmp>/.cache/mise/npm-bash-language-server/remote_versions-1b050.msgpack.z
$TMPDIR/U116-home-<tmp>/.cache/mise/npm-fast-cli
$TMPDIR/U116-home-<tmp>/.cache/mise/npm-fast-cli/latest_version-81575.msgpack.z
$TMPDIR/U116-home-<tmp>/.cache/mise/npm-fast-cli/remote_versions-81575.msgpack.z
$TMPDIR/U116-home-<tmp>/.cache/mise/npm-meta
$TMPDIR/U116-home-<tmp>/.cache/mise/npm-meta/origin-3c364d36b2d92b17
$TMPDIR/U116-home-<tmp>/.cache/mise/npm-meta/origin-3c364d36b2d92b17/@anthropic-ai__claude-code.json
$TMPDIR/U116-home-<tmp>/.cache/mise/npm-meta/origin-3c364d36b2d92b17/@anthropic-ai__sandbox-runtime.json
$TMPDIR/U116-home-<tmp>/.cache/mise/npm-meta/origin-3c364d36b2d92b17/@openai__codex.json
$TMPDIR/U116-home-<tmp>/.cache/mise/npm-meta/origin-3c364d36b2d92b17/bash-language-server.json
$TMPDIR/U116-home-<tmp>/.cache/mise/npm-meta/origin-3c364d36b2d92b17/fast-cli.json
$TMPDIR/U116-home-<tmp>/.cache/mise/npm-meta/origin-3c364d36b2d92b17/pyright.json
$TMPDIR/U116-home-<tmp>/.cache/mise/npm-openai-codex
$TMPDIR/U116-home-<tmp>/.cache/mise/npm-openai-codex/latest_version-50bdb.msgpack.z
$TMPDIR/U116-home-<tmp>/.cache/mise/npm-openai-codex/remote_versions-50bdb.msgpack.z
$TMPDIR/U116-home-<tmp>/.cache/mise/npm-pyright
$TMPDIR/U116-home-<tmp>/.cache/mise/npm-pyright/latest_version-30d9a.msgpack.z
$TMPDIR/U116-home-<tmp>/.cache/mise/npm-pyright/remote_versions-30d9a.msgpack.z
$TMPDIR/U116-home-<tmp>/.cache/mise/python
$TMPDIR/U116-home-<tmp>/.cache/mise/python/remote_versions-ee8bb.msgpack.z
$TMPDIR/U116-home-<tmp>/.cache/mise/uv
$TMPDIR/U116-home-<tmp>/.cache/mise/uv/remote_versions-3ed32.msgpack.z
$TMPDIR/U116-home-<tmp>/.cache/mise/versions-index
$TMPDIR/U116-home-<tmp>/.cache/mise/versions-index/index.v1
$TMPDIR/U116-home-<tmp>/.cache/mise/versions-index/index.v1.validated
$TMPDIR/U116-home-<tmp>/.config
$TMPDIR/U116-home-<tmp>/.config/mise
$TMPDIR/U116-home-<tmp>/.config/mise/config.toml
$TMPDIR/U116-home-<tmp>/.local
$TMPDIR/U116-home-<tmp>/.local/share
$TMPDIR/U116-home-<tmp>/.local/state
$TMPDIR/U116-home-<tmp>/.local/state/mise
$TMPDIR/U116-home-<tmp>/.local/state/mise/incomplete-installs
$TMPDIR/U116-home-<tmp>/.local/state/mise/incomplete-installs/.migrated
$TMPDIR/U116-home-<tmp>/.local/state/mise/tracked-configs
$TMPDIR/U116-home-<tmp>/.local/state/mise/tracked-configs/4e3778c4ab72697
$TMPDIR/U116-home-<tmp>/cwd
$TMPDIR/U116-home-<tmp>/etc
$TMPDIR/U116-home-<tmp>/etc/mise
```

### `scan`

Run from `$TMPDIR` with this file as committed (the worktree copy, which is the committed bytes once ACCEPTANCE 1 shows the tree clean) and the PR body `/tmp/dotfiles-wt/U116-pr-body.md`. Three classes over all 25 files: the token, the five words of the coordinator's redact list (the login name among them, so a path under the real home would count), and the absolute prefix of home directories on this host, which is the brief's `grep -c` of ACCEPTANCE 5 as a count the procedure takes itself.

```sh
python3 -I U116-procedure.py scan
```

```text
token from gh auth token patterns=1
redact list ~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/redact-words.txt patterns=5
U116-out-<tmp>/a-version.receipt.txt token=0 redact=0 homeprefix=0
U116-out-<tmp>/a-version.txt token=0 redact=0 homeprefix=0
U116-out-<tmp>/b-lock-dry-run.receipt.txt token=0 redact=0 homeprefix=0
U116-out-<tmp>/b-lock-dry-run.txt token=0 redact=0 homeprefix=0
U116-out-<tmp>/c-lock-dry-run-4-platforms.receipt.txt token=0 redact=0 homeprefix=0
U116-out-<tmp>/c-lock-dry-run-4-platforms.txt token=0 redact=0 homeprefix=0
U116-out-<tmp>/d-lock-bump-json.receipt.txt token=0 redact=0 homeprefix=0
U116-out-<tmp>/d-lock-bump-json.txt token=0 redact=0 homeprefix=0
U116-out-<tmp>/e-npm-package-manager.receipt.txt token=0 redact=0 homeprefix=0
U116-out-<tmp>/e-npm-package-manager.txt token=0 redact=0 homeprefix=0
U116-out-<tmp>/f-minimum-release-age.receipt.txt token=0 redact=0 homeprefix=0
U116-out-<tmp>/f-minimum-release-age.txt token=0 redact=0 homeprefix=0
U116-out-<tmp>/g-none-written.txt token=0 redact=0 homeprefix=0
U116-out-<tmp>/g-scratch-after.txt token=0 redact=0 homeprefix=0
U116-out-<tmp>/h-config-ls-json.receipt.txt token=0 redact=0 homeprefix=0
U116-out-<tmp>/h-config-ls-json.txt token=0 redact=0 homeprefix=0
U116-out-<tmp>/h-config-ls.receipt.txt token=0 redact=0 homeprefix=0
U116-out-<tmp>/h-config-ls.txt token=0 redact=0 homeprefix=0
U116-out-<tmp>/help-lock.receipt.txt token=0 redact=0 homeprefix=0
U116-out-<tmp>/help-lock.txt token=0 redact=0 homeprefix=0
U116-out-<tmp>/real-after.txt token=0 redact=0 homeprefix=0
U116-out-<tmp>/real-before.txt token=0 redact=0 homeprefix=0
U116-out-<tmp>/scratch-tree.txt token=0 redact=0 homeprefix=0
/tmp/dotfiles-wt/U116/.orchestration/orchestrate/regime-cutover/handoff/evaluations/U116-mise-lock.md token=0 redact=0 homeprefix=0
/tmp/dotfiles-wt/U116-pr-body.md token=0 redact=0 homeprefix=0
scan clean (25 files, 0 matches)
exit=0
```

### `check`

Run from `$TMPDIR` against the worktree. ACCEPTANCE 1 here is the diff against the merge base `6fd09e96`, the commit this branch was cut from (the local `origin/main` has moved three commits past it, every one a change main received after the merge base and none touched by this branch; `git status --porcelain` is pasted by hand in the PR body). The forms line of this file reads `python-blocks=1` and `sh-blocks=21` (the four subcommands and the seventeen injections), each on the one-line form, and every line class 0; the PR body holds `text` blocks alone.

```sh
python3 -I U116-procedure.py check
```

```text
git diff --name-only 6fd09e96..HEAD exit=0 paths=1
  .orchestration/orchestrate/regime-cutover/handoff/evaluations/U116-mise-lock.md
prettier --check --ignore-path /dev/null .orchestration/orchestrate/regime-cutover/handoff/evaluations/U116-mise-lock.md exit=0
  Checking formatting...
  All matched files use Prettier code style!
5:## Question
11:## Commands run
2858:## Measured facts
2912:## Recommendation
2918:## Draft decisions row
2935:## Left out
headings=6 order=ok
draft-rows=1
g-none-written: none-written
real-before.txt:
  drwxr-xr-x     96 2026-10-26T23:40:46 ~/.config/mise
  -rw-r--r--   6962 2026-10-26T23:40:46 ~/.config/mise/config.toml
  drwxr-xr-x    256 2026-10-29T19:43:40 ~/.local/share/mise
  missing ~/.cache/mise
  drwxr-xr-x    256 2026-10-29T18:57:51 ~/.local/state/mise
  drwxr-xr-x   1536 2026-10-29T18:57:42 ~/Library/Caches/mise
real-after.txt:
  drwxr-xr-x     96 2026-10-26T23:40:46 ~/.config/mise
  -rw-r--r--   6962 2026-10-26T23:40:46 ~/.config/mise/config.toml
  drwxr-xr-x    256 2026-10-29T19:43:40 ~/.local/share/mise
  missing ~/.cache/mise
  drwxr-xr-x    256 2026-10-29T18:57:51 ~/.local/state/mise
  drwxr-xr-x   1536 2026-10-29T18:57:42 ~/Library/Caches/mise
real-dirs before=after: same; mise.lock lines=0
/tmp/dotfiles-wt/U116/.orchestration/orchestrate/regime-cutover/handoff/evaluations/U116-mise-lock.md python-blocks=1 sh-blocks=21 sh-blocks-off-form=0 text-blocks=36 other-blocks=0 producer-lines=0 swallow-lines=0 wrapper-lines=0 raw-print-sites=0
/tmp/dotfiles-wt/U116-pr-body.md python-blocks=0 sh-blocks=0 sh-blocks-off-form=0 text-blocks=6 other-blocks=0 producer-lines=0 swallow-lines=0 wrapper-lines=0 raw-print-sites=0
check ok
exit=0
```

### Injections

Seventeen `inject` runs, from `$TMPDIR`, each making its own fixture directory with `mkdtemp` under `$TMPDIR` (printed as `$TMPDIR/U116-inject-<tmp>`, removed when the case ends) and patching the process in memory or planting fixtures there, then running the targeted subcommand's own function; nothing lands in the receipt's output directory, and the real mise, `gh`, `git` and `prettier` are never touched. Thirteen exit 2 with a redacted refusal and no success line; the `FileNotFoundError` lock case exits 0 printing `none-written`, the planted token exits 1 with `scan FOUND`, the planted producer line exits 1 as a counted failure, and the planted configs exit 0 with `config ls` unchanged under `ENV` and changed under the two controls.

`mise` absent: `PATH` is one empty directory under the fixture tree and the `run` path starts; the lookup refuses before any receipt exists.

```sh
python3 -I U116-procedure.py inject missing-mise
```

```text
fixtures: $TMPDIR/U116-inject-<tmp> (removed when this case ends)
case missing-mise: PATH=$TMPDIR/U116-inject-<tmp>/empty; run
inject missing-mise REFUSED: mise not found on PATH (1 entries searched)
exit=2
```

`gh` absent: `PATH` is one empty directory and the `scan` path starts; `run()` refuses the launch with the argv, before any pattern line.

```sh
python3 -I U116-procedure.py inject missing-gh
```

```text
fixtures: $TMPDIR/U116-inject-<tmp> (removed when this case ends)
case missing-gh: PATH=$TMPDIR/U116-inject-<tmp>/empty; scan
inject missing-gh REFUSED: ['gh', 'auth', 'token'] did not complete: FileNotFoundError: [Errno 2] No such file or directory: 'gh'
exit=2
```

`git` absent: `PATH` is one empty directory and the `check` path starts; the first external command refuses, before any result line.

```sh
python3 -I U116-procedure.py inject missing-git
```

```text
fixtures: $TMPDIR/U116-inject-<tmp> (removed when this case ends)
case missing-git: PATH=$TMPDIR/U116-inject-<tmp>/empty; check
inject missing-git REFUSED: ['git', '-C', '/tmp/dotfiles-wt/U116', 'diff', '--name-only', '6fd09e96..HEAD'] did not complete: FileNotFoundError: [Errno 2] No such file or directory: 'git'
exit=2
```

`prettier` absent: `PATH` is one directory holding a symlink to the real `git` alone (the lookup's own `git=` line comes first) and the `check` path starts; the diff line prints, then the prettier launch refuses.

```sh
python3 -I U116-procedure.py inject missing-prettier
```

```text
fixtures: $TMPDIR/U116-inject-<tmp> (removed when this case ends)
git=/opt/homebrew/bin/git (PATH entry 39 of 55)
case missing-prettier: PATH=$TMPDIR/U116-inject-<tmp>/only-git (a symlink to git alone); check
git diff --name-only 6fd09e96..HEAD exit=0 paths=1
  .orchestration/orchestrate/regime-cutover/handoff/evaluations/U116-mise-lock.md
inject missing-prettier REFUSED: ['prettier', '--check', '--ignore-path', '/dev/null', '/tmp/dotfiles-wt/U116/.orchestration/orchestrate/regime-cutover/handoff/evaluations/U116-mise-lock.md'] did not complete: FileNotFoundError: [Errno 2] No such file or directory: 'prettier'
exit=2
```

`PermissionError` on the lookup: `os.lstat` is replaced in this process so that `<real home>/bin/mise`, first on `PATH`, raises `PermissionError(13, 'Permission denied', <that path>)`; the `run` path starts and `resolve` meets the error on its first entry. The refusal names `~/bin/mise` twice, from the message and from the exception text, and the real home nowhere; the case line passes through the same `redact`.

```sh
python3 -I U116-procedure.py inject lookup-permission
```

```text
fixtures: $TMPDIR/U116-inject-<tmp> (removed when this case ends)
case lookup-permission: PATH starts with ~/bin; os.lstat of ~/bin/mise raises PermissionError; run
inject lookup-permission REFUSED: cannot read ~/bin/mise: [Errno 13] Permission denied: '~/bin/mise'
exit=2
```

`TimeoutExpired` on a run: a directory under the fixture tree holding `mise` as a symlink to `/bin/wait4path` (which blocks until its argument exists as a path; the argument is `--version`, so it never returns) is first on `PATH`, `OUT` points at a directory under the fixture tree so nothing lands in the receipt's output directory, `TIMEOUT` is 2, and the `run` path starts (its `ENV` lines are this run's environment, printed as `run` prints them). `run()` refuses with the argv and the error's text; the receipt, written and emitted as the refusal unwinds through `timed`'s `finally`, reads `exit=refused`. No shell script stands in for mise.

```sh
python3 -I U116-procedure.py inject run-timeout
```

```text
fixtures: $TMPDIR/U116-inject-<tmp> (removed when this case ends)
case run-timeout: PATH starts with $TMPDIR/U116-inject-<tmp>/sleeper (mise is a symlink to /bin/wait4path); OUT=$TMPDIR/U116-inject-<tmp>/out; TIMEOUT=2; run
mise=$TMPDIR/U116-inject-<tmp>/sleeper/mise (PATH entry 1 of 56)
cwd=$TMPDIR/U116-home-<tmp>/cwd
env (the whole environment of every mise call):
  HOME=$TMPDIR/U116-home-<tmp>
  PATH=<55 entries, inherited>
  TMPDIR=$TMPDIR/
  XDG_CONFIG_HOME=$TMPDIR/U116-home-<tmp>/.config
  XDG_DATA_HOME=$TMPDIR/U116-home-<tmp>/.local/share
  XDG_CACHE_HOME=$TMPDIR/U116-home-<tmp>/.cache
  XDG_STATE_HOME=$TMPDIR/U116-home-<tmp>/.local/state
  MISE_TRUSTED_CONFIG_PATHS=$TMPDIR/U116-home-<tmp>/.config/mise/config.toml
  MISE_CONFIG_DIR=$TMPDIR/U116-home-<tmp>/.config/mise
  MISE_GLOBAL_CONFIG_FILE=$TMPDIR/U116-home-<tmp>/.config/mise/config.toml
  MISE_SYSTEM_CONFIG_DIR=$TMPDIR/U116-home-<tmp>/etc/mise
  MISE_SYSTEM_CONFIG_FILE=$TMPDIR/U116-home-<tmp>/etc/mise/none.toml
  MISE_CEILING_PATHS=$TMPDIR/U116-home-<tmp>/cwd:$TMPDIR/U116-home-<tmp>/cwd
  MISE_IGNORED_CONFIG_PATHS=~/.config/mise:/etc/mise:/private/etc/mise
  MISE_OVERRIDE_CONFIG_FILENAMES=U116-none.toml
  MISE_OVERRIDE_TOOL_VERSIONS_FILENAMES=none
inject run-timeout REFUSED: ['$TMPDIR/U116-inject-<tmp>/sleeper/mise', '--version'] did not complete: TimeoutExpired: Command '['$TMPDIR/U116-inject-<tmp>/sleeper/mise', '--version']' timed out after 2 seconds
a-version: start=2026-10-29T16:18:50Z end=2026-10-29T16:18:52Z elapsed=2s exit=refused
exit=2
```

`NotADirectoryError` on the lock `lstat`: `os.lstat` is replaced for the lockfile path alone and `check_lock`, the one none-written test `run` and `check` share, is called. It refuses with the error's text instead of reading absence (the round-8 verdict's second finding: the shell `test -e` form reported `none-written` here).

```sh
python3 -I U116-procedure.py inject lock-notadirectory
```

```text
fixtures: $TMPDIR/U116-inject-<tmp> (removed when this case ends)
case lock-notadirectory: os.lstat of $TMPDIR/U116-home-<tmp>/.config/mise/mise.lock raises NotADirectoryError; check_lock
inject lock-notadirectory REFUSED: cannot read $TMPDIR/U116-home-<tmp>/.config/mise/mise.lock: [Errno 20] Not a directory: '$TMPDIR/U116-home-<tmp>/.config/mise/mise.lock'
exit=2
```

`PermissionError` on the lock `lstat`: the same, with `PermissionError`; a refusal.

```sh
python3 -I U116-procedure.py inject lock-permission
```

```text
fixtures: $TMPDIR/U116-inject-<tmp> (removed when this case ends)
case lock-permission: os.lstat of $TMPDIR/U116-home-<tmp>/.config/mise/mise.lock raises PermissionError; check_lock
inject lock-permission REFUSED: cannot read $TMPDIR/U116-home-<tmp>/.config/mise/mise.lock: [Errno 13] Permission denied: '$TMPDIR/U116-home-<tmp>/.config/mise/mise.lock'
exit=2
```

`FileNotFoundError` on the lock `lstat`: the one answer read as absence; `check_lock` returns `none-written` and the process exits 0.

```sh
python3 -I U116-procedure.py inject lock-missing
```

```text
fixtures: $TMPDIR/U116-inject-<tmp> (removed when this case ends)
case lock-missing: os.lstat of $TMPDIR/U116-home-<tmp>/.config/mise/mise.lock raises FileNotFoundError; check_lock
g-none-written: none-written
exit=0
```

A `.txt` count off by one: `EXPECTED_FILES` is lowered from 23 to 22 in this process and the `scan` path starts; it refuses after the two pattern lines and before any per-file line.

```sh
python3 -I U116-procedure.py inject txt-count
```

```text
fixtures: $TMPDIR/U116-inject-<tmp> (removed when this case ends)
case txt-count: EXPECTED_FILES=22; scan
token from gh auth token patterns=1
redact list ~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/redact-words.txt patterns=5
inject txt-count REFUSED: found 23 .txt files, expected 22
exit=2
```

A comment-only redact list: the comment lines of the coordinator's list (one line) are written to a file under the fixture tree, `REDACT_LIST` points at it, and the `scan` path starts; it prints `patterns=0` and refuses.

```sh
python3 -I U116-procedure.py inject redact-comment-only
```

```text
fixtures: $TMPDIR/U116-inject-<tmp> (removed when this case ends)
case redact-comment-only: REDACT_LIST=$TMPDIR/U116-inject-<tmp>/redact-comment-only.txt (1 comment lines, nothing else); scan
token from gh auth token patterns=1
redact list $TMPDIR/U116-inject-<tmp>/redact-comment-only.txt patterns=0
inject redact-comment-only REFUSED: redact list $TMPDIR/U116-inject-<tmp>/redact-comment-only.txt holds no pattern
exit=2
```

A missing output directory: `OUT` points at a path under the fixture tree that does not exist and the `scan` path starts; `os.scandir` raises `FileNotFoundError`, which reaches the boundary in `main()` and is refused with its class and text.

```sh
python3 -I U116-procedure.py inject missing-out
```

```text
fixtures: $TMPDIR/U116-inject-<tmp> (removed when this case ends)
case missing-out: OUT=$TMPDIR/U116-inject-<tmp>/no-such-out; scan
token from gh auth token patterns=1
redact list ~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/redact-words.txt patterns=5
inject missing-out REFUSED: FileNotFoundError: [Errno 2] No such file or directory: '$TMPDIR/U116-inject-<tmp>/no-such-out'
exit=2
```

A planted token: the token class is replaced in this process by a synthetic marker, `U116-SYNTHETIC-TOKEN-` and 16 hex digits from `secrets.token_hex`, so `gh auth token` is not called and no credential exists in the process (the run repeats unchanged with `gh` absent from `PATH`); the 23 output files are copied into the fixture tree (never the receipt's output directory), each copy made by `create` like every other file, the copy of `a-version.txt` with the marker as its last line, `OUT` points at the copies and the `scan` path starts; it counts `token=1` on that file, reports `scan FOUND` and exits 1. The case line names the marker; its hex digits differ on every run, so a re-run shows another value and the marker pasted here matches nothing a later scan looks for. The fixture tree is removed by `shutil.rmtree` in the `finally` clause of `inject`, which encloses the copies, the `emit` of the case line and the scan, so it runs whether `emit` or `scan` returns or raises.

```sh
python3 -I U116-procedure.py inject planted-token
```

```text
fixtures: $TMPDIR/U116-inject-<tmp> (removed when this case ends)
case planted-token: the token class is the marker U116-SYNTHETIC-TOKEN-b8cb495fd1b2d28f (gh is not called); 23 copies under $TMPDIR/U116-inject-<tmp>, the marker appended to the copy of a-version.txt; scan
token from the synthetic marker patterns=1
redact list ~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/redact-words.txt patterns=5
U116-inject-<tmp>/a-version.receipt.txt token=0 redact=0 homeprefix=0
U116-inject-<tmp>/a-version.txt token=1 redact=0 homeprefix=0
U116-inject-<tmp>/b-lock-dry-run.receipt.txt token=0 redact=0 homeprefix=0
U116-inject-<tmp>/b-lock-dry-run.txt token=0 redact=0 homeprefix=0
U116-inject-<tmp>/c-lock-dry-run-4-platforms.receipt.txt token=0 redact=0 homeprefix=0
U116-inject-<tmp>/c-lock-dry-run-4-platforms.txt token=0 redact=0 homeprefix=0
U116-inject-<tmp>/d-lock-bump-json.receipt.txt token=0 redact=0 homeprefix=0
U116-inject-<tmp>/d-lock-bump-json.txt token=0 redact=0 homeprefix=0
U116-inject-<tmp>/e-npm-package-manager.receipt.txt token=0 redact=0 homeprefix=0
U116-inject-<tmp>/e-npm-package-manager.txt token=0 redact=0 homeprefix=0
U116-inject-<tmp>/f-minimum-release-age.receipt.txt token=0 redact=0 homeprefix=0
U116-inject-<tmp>/f-minimum-release-age.txt token=0 redact=0 homeprefix=0
U116-inject-<tmp>/g-none-written.txt token=0 redact=0 homeprefix=0
U116-inject-<tmp>/g-scratch-after.txt token=0 redact=0 homeprefix=0
U116-inject-<tmp>/h-config-ls-json.receipt.txt token=0 redact=0 homeprefix=0
U116-inject-<tmp>/h-config-ls-json.txt token=0 redact=0 homeprefix=0
U116-inject-<tmp>/h-config-ls.receipt.txt token=0 redact=0 homeprefix=0
U116-inject-<tmp>/h-config-ls.txt token=0 redact=0 homeprefix=0
U116-inject-<tmp>/help-lock.receipt.txt token=0 redact=0 homeprefix=0
U116-inject-<tmp>/help-lock.txt token=0 redact=0 homeprefix=0
U116-inject-<tmp>/real-after.txt token=0 redact=0 homeprefix=0
U116-inject-<tmp>/real-before.txt token=0 redact=0 homeprefix=0
U116-inject-<tmp>/scratch-tree.txt token=0 redact=0 homeprefix=0
/tmp/dotfiles-wt/U116/.orchestration/orchestrate/regime-cutover/handoff/evaluations/U116-mise-lock.md token=0 redact=0 homeprefix=0
/tmp/dotfiles-wt/U116-pr-body.md token=0 redact=0 homeprefix=0
scan FOUND (25 files, 1 matches)
exit=1
```

An unmapped UID: `getpass.getuser` is replaced in this process by a function raising `OSError` (the error it raises when no name variable is set and the UID has no passwd entry), `USER` is removed from the environment so the fallback has nothing, and `arm()`, the function `main()` runs first inside its `try`, is called again. `login_name` refuses with the error's text and `USER is unset`, exit 2, no traceback; the table the first `arm()` built stays, so the refusal passes through the same `redact` (before the first `arm()` the same text holds no path and no name). With `USER` present the fallback returns it and `arm()` completes; the home directory falls back from `expanduser("~")` to `HOME` the same way and refuses when neither exists.

```sh
python3 -I U116-procedure.py inject user-lookup
```

```text
fixtures: $TMPDIR/U116-inject-<tmp> (removed when this case ends)
case user-lookup: getpass.getuser raises OSError; USER unset; arm
inject user-lookup REFUSED: login name unknown: OSError: No username set in the environment; USER is unset
exit=2
```

The `check` subcommand's own injection: a copy of this file under the fixture tree with the line `true $(true)` inserted inside its first `sh` block, and the forms counts over that copy. The planted line counts once under `producer-lines` and makes that block two lines, so it counts once under `sh-blocks-off-form` too; the exit status is 1, a measured failure.

```sh
python3 -I U116-procedure.py inject forms-producer
```

```text
fixtures: $TMPDIR/U116-inject-<tmp> (removed when this case ends)
case forms-producer: $TMPDIR/U116-inject-<tmp>/forms-producer.md is this file with `true $(true)` inserted at line 1279, inside its first sh block; forms
$TMPDIR/U116-inject-<tmp>/forms-producer.md python-blocks=1 sh-blocks=21 sh-blocks-off-form=1 text-blocks=36 other-blocks=0 producer-lines=1 swallow-lines=0 wrapper-lines=0 raw-print-sites=0
exit=1
```

A symlink at an output path (the round-10 verdict's first finding): under the fixture tree, `target.txt` is written with 46 bytes, an output directory is made, `a-version.txt` inside it is made a symlink to the target, `OUT` points at that directory and `timed('a-version', [mise, '--version'], TIMEOUT)`, the function the verdict named, is called with the real `mise` resolved. `create` refuses the output path with `FileExistsError` before any launch (`O_EXCL`; `O_NOFOLLOW` refuses the same path when it is a symlink to a file that is then created); the receipt reads `exit=refused`, the case's `finally` prints the target's size after the attempt and that the link is still a symlink, and the boundary prints the refusal, exit 2. The target keeps its 46 bytes.

```sh
python3 -I U116-procedure.py inject create-symlink
```

```text
fixtures: $TMPDIR/U116-inject-<tmp> (removed when this case ends)
mise=~/.local/bin/mise (PATH entry 51 of 55)
case create-symlink: $TMPDIR/U116-inject-<tmp>/out/a-version.txt is a symlink to $TMPDIR/U116-inject-<tmp>/target.txt (46 bytes); OUT=$TMPDIR/U116-inject-<tmp>/out; timed a-version
a-version: start=2026-10-29T16:18:53Z end=2026-10-29T16:18:53Z elapsed=0s exit=refused
target after: 46 bytes; the link is still a symlink: True
inject create-symlink REFUSED: FileExistsError: [Errno 17] File exists: '$TMPDIR/U116-inject-<tmp>/out/a-version.txt'
exit=2
```

Planted configs (the round-10 verdict's second finding): a scratch home of its own, made as `prepare` makes one and removed when the case ends, with the real `mise` resolved and the cwd its `cwd`; `mise config ls` under `ENV` before anything is planted lists the scratch copy alone (as `~/.config/mise/config.toml`, `~` being the scratch home). Four configs are then planted where mise would look without the discovery variables: `mise.toml` at the cwd's parent (the scratch home), `mise.toml` and `.tool-versions` in the cwd itself, and `config.toml` in the directory `MISE_SYSTEM_CONFIG_DIR` names (where `MISE_SYSTEM_CONFIG_FILE` names `none.toml` instead). `mise config ls` under `ENV` again lists the scratch copy alone, byte for byte the first listing. Two controls follow so the case cannot pass vacuously: under the CHANGE 1 variables alone (the round-10 environment), the same command lists the parent's `mise.toml`, the cwd's `.tool-versions` and the cwd's `mise.toml` after the scratch copy; and under `ENV` with `MISE_CEILING_PATHS` removed and `MISE_OVERRIDE_CONFIG_FILENAMES` set to the empty string the brief's task asked for, the two planted `mise.toml` files are listed, so this mise reads an empty value as unset and the ceiling, not the override name, is the control that excludes project config. The case exits 0 only when the `ENV` listings are equal and the first control differs.

```sh
python3 -I U116-procedure.py inject planted-config
```

```text
fixtures: $TMPDIR/U116-inject-<tmp> (removed when this case ends)
mise=~/.local/bin/mise (PATH entry 51 of 55)
case planted-config: scratch=$TMPDIR/U116-home-<tmp> (removed when this case ends); cwd=$TMPDIR/U116-home-<tmp>/cwd; config ls before, plant, config ls after, then the control
config-ls-before: start=2026-10-29T16:18:53Z end=2026-10-29T16:18:53Z elapsed=0s exit=0
config-ls-before.txt (1 lines):
  ~/.config/mise/config.toml  node, rust, python, age, bun, chezmoi, dotenvx, cargo:eza, fd, jq, hugo-extended, uv, yazi, aqua:micro-editor/micro, aqua:mikefarah/yq, aqua:watchexec/watchexec, npm:@anthropic-ai/claude-code, npm:@openai/codex, npm:@anthropic-ai/sandbox-runtime, npm:bash-language-server, npm:ccstatusline, npm:ccusage, npm:pyright, npm:fast-cli, npm:prettier, npm:pnpm, github:x-motemen/ghq, github:d-kuro/gwq, github:cli/cli, github:ogulcancelik/herdr, cargo:pueue, http:bats, http:gcloud, http:shellcheck, http:shfmt, http:ruff
planted: mise.toml, cwd/mise.toml, cwd/.tool-versions, etc/mise/config.toml under $TMPDIR/U116-home-<tmp>
config-ls-after: start=2026-10-29T16:18:53Z end=2026-10-29T16:18:53Z elapsed=0s exit=0
config-ls-after.txt (1 lines):
  ~/.config/mise/config.toml  node, rust, python, age, bun, chezmoi, dotenvx, cargo:eza, fd, jq, hugo-extended, uv, yazi, aqua:micro-editor/micro, aqua:mikefarah/yq, aqua:watchexec/watchexec, npm:@anthropic-ai/claude-code, npm:@openai/codex, npm:@anthropic-ai/sandbox-runtime, npm:bash-language-server, npm:ccstatusline, npm:ccusage, npm:pyright, npm:fast-cli, npm:prettier, npm:pnpm, github:x-motemen/ghq, github:d-kuro/gwq, github:cli/cli, github:ogulcancelik/herdr, cargo:pueue, http:bats, http:gcloud, http:shellcheck, http:shfmt, http:ruff
control: ENV reduced to HOME, PATH, TMPDIR, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_CACHE_HOME, XDG_STATE_HOME, MISE_TRUSTED_CONFIG_PATHS
config-ls-control: start=2026-10-29T16:18:53Z end=2026-10-29T16:18:53Z elapsed=0s exit=0
config-ls-control.txt (4 lines):
  $TMPDIR/U116-home-<tmp>/.config/mise/config.toml  node, rust, python, age, bun, chezmoi, dotenvx, cargo:eza, fd, jq, hugo-extended, uv, yazi, aqua:micro-editor/micro, aqua:mikefarah/yq, aqua:watchexec/watchexec, npm:@anthropic-ai/claude-code, npm:@openai/codex, npm:@anthropic-ai/sandbox-runtime, npm:bash-language-server, npm:ccstatusline, npm:ccusage, npm:pyright, npm:fast-cli, npm:prettier, npm:pnpm, github:x-motemen/ghq, github:d-kuro/gwq, github:cli/cli, github:ogulcancelik/herdr, cargo:pueue, http:bats, http:gcloud, http:shellcheck, http:shfmt, http:ruff
  $TMPDIR/U116-home-<tmp>/mise.toml                 node
  $TMPDIR/U116-home-<tmp>/cwd/.tool-versions        node
  $TMPDIR/U116-home-<tmp>/cwd/mise.toml             node
control: ENV without MISE_CEILING_PATHS and with MISE_OVERRIDE_CONFIG_FILENAMES empty
config-ls-empty-override: start=2026-10-29T16:18:53Z end=2026-10-29T16:18:53Z elapsed=0s exit=0
config-ls-empty-override.txt (3 lines):
  $TMPDIR/U116-home-<tmp>/.config/mise/config.toml  node, rust, python, age, bun, chezmoi, dotenvx, cargo:eza, fd, jq, hugo-extended, uv, yazi, aqua:micro-editor/micro, aqua:mikefarah/yq, aqua:watchexec/watchexec, npm:@anthropic-ai/claude-code, npm:@openai/codex, npm:@anthropic-ai/sandbox-runtime, npm:bash-language-server, npm:ccstatusline, npm:ccusage, npm:pyright, npm:fast-cli, npm:prettier, npm:pnpm, github:x-motemen/ghq, github:d-kuro/gwq, github:cli/cli, github:ogulcancelik/herdr, cargo:pueue, http:bats, http:gcloud, http:shellcheck, http:shfmt, http:ruff
  $TMPDIR/U116-home-<tmp>/mise.toml                 node
  $TMPDIR/U116-home-<tmp>/cwd/mise.toml             node
config ls under ENV: unchanged; under the CHANGE 1 variables alone: the planted configs are listed; with the empty override value: planted files listed, so the empty value is ignored
exit=0
```

## Measured facts

### From the outputs

| Run                                           | Platforms       | Tools | Entries mise would write             | Elapsed | Exit |
| --------------------------------------------- | --------------- | ----- | ------------------------------------ | ------- | ---- |
| (b) default platform set                      | 7               | 36    | 258                                  | 10 s    | 0    |
| (c) the four platforms the `http:` tables pin | 4               | 36    | 149                                  | 0 s     | 0    |
| (d) `--bump --json`                           | 7 (same target) | 36    | 36 objects, all `old_versions` empty | 0 s     | 0    |

- **Platforms.** With no `lockfile_platforms` setting and no existing lockfile, mise targets `linux-arm64, linux-arm64-musl, linux-x64, linux-x64-musl, macos-arm64, macos-x64, windows-x64` (first line of (b)). That is the vendor's new-lockfile set from the reference page, and it matches the "7 platforms" of row 233.
- **Entries.** (b) lists 258 `✓` lines: 36 tools times 7 platforms is 252, and bun adds six more keys (`linux-x64-baseline`, `linux-x64-musl-baseline`, `macos-x64-baseline`, `windows-x64-baseline`, and `linux-arm64-musl` and `linux-x64-musl` listed a second time). (c) lists 149: 144 plus bun's `linux-arm64-musl`, `linux-x64-baseline`, `linux-x64-musl`, `linux-x64-musl-baseline` and `macos-x64-baseline`. Counted over the two pasted files by their `✓` lines; both counts are the ones rounds 5 to 10 recorded, and the `✓` lines of (b), (c) and the objects of (d) are byte for byte the round-9 lines, so the config discovery variables of round 11 changed no entry.
- **Backends.** Every one of the 36 tools resolved, each to the version rounds 7 to 10 resolved (the one move since round 5, `python@3.15.1` to `python@3.15.2` between rounds 5 and 6, stands; no version moved between rounds 7 and 11): 4 core (`node`, `rust`, `python`, `bun`), 11 aqua (`age`, `chezmoi`, `dotenvx`, `fd`, `jq`, `hugo-extended`, `uv`, `yazi`, `micro`, `yq`, `watchexec`; the backend names come from the `backend` field of (d)), 10 npm, 4 github, 2 cargo, 5 http. No line reports a failure, a skipped platform or a rate limit, and no run needed `MISE_GITHUB_TOKEN`.
- **What a bump would move today.** Nothing moves: every object in (d) has `"old_versions": []`, because no lockfile exists. The 36 `new_versions` equal the versions (b) resolved, so today's bump PR would be the first write of the file, not an update. The exact pins resolve to themselves (`npm:ccstatusline@2.2.32`, `npm:ccusage@20.0.37`, `npm:prettier@3.9.10`, `npm:pnpm@12.8.1`, the five `http:` tools), as the vendor says for `--bump`.
- **Elapsed.** (b) took 10 s wall time; this is the one measured number of this table the round-11 re-take moved (round 9 measured 3 s, round 7 2 s, round 6 4 s, round 5 5 s, the round-1 run that rounds 1 to 4 pasted 8 s), every count in this section being unchanged. The number is network latency at that minute, not mise's work: two takes of the same hour with earlier bytes of this script (not pasted; their scratch directories stay under `$TMPDIR`) measured 4 s and 2 s for (b), and in the pasted take `mise --version`, which resolves nothing, itself took 6 s. (c) and (d) returned in under a second because mise reused the version lists (b) had cached under the scratch `~/.cache/mise` (the `remote_versions-*.msgpack.z` files in the scratch tree). The brief's estimate of "about 36 tools per platform over the network" taking minutes did not hold: mise resolves a version once per tool, not once per platform, and the dry run downloads no artifact.
- **Config discovery.** `h-config-ls.txt` and `h-config-ls-json.txt`, taken under `ENV` after the dry runs, list one config file, the scratch copy (`"override": false`, 36 tools), so the lock runs read that file and nothing else; the `planted-config` injection repeats the listing in a scratch home of its own with four configs planted where mise would otherwise look and gets the same one line, while its two controls list the planted files. Three things the measurement settled: mise compares the ceiling against the resolved path (`/private/var/...` on this host), so `MISE_CEILING_PATHS` carries both spellings and the `/var` spelling alone did not match in a probe; this mise reads an empty `MISE_OVERRIDE_CONFIG_FILENAMES` as unset (the second control), so the variable carries a sentinel name and the ceiling is the control that excludes project config; and with the discovery variables set, mise prints the global paths relative to `HOME` (`~/.config/mise/mise.lock` in the first line of (b), where rounds 5 to 10 pasted the full `/private/var/...` path), `~` being the scratch home, which `h-config-ls-json.txt` confirms by the full path. The `--help` text of `mise lock` says `--global` locks "the global and system config lockfiles"; under `ENV` the system config is `MISE_SYSTEM_CONFIG_FILE`, a path that does not exist, so the only lockfile (b) targets is the scratch one.
- **Hosts contacted.** No packet capture was taken. The cache file names show `api.github.com` (sixteen `github/https-api-github-com-*` entries), the mise versions index (`versions-index/index.v1`) and an npm registry origin (`npm-meta/origin-*`, which in this run holds one metadata file for each of the six unheld `npm:` tools and none for the four held ones). All are in the brief's host list. The scratch tree is the round-9 tree line for line apart from four differences: a `bun/remote_versions-*` cache entry where round 9 had a `node/remote_versions-*` one (which version list mise cached under its own name and which under the versions index), the name of the `tracked-configs` entry, and the two directories round 11 adds to the scratch home, `cwd` and `etc/mise`. Whether any other host was contacted is unverified; what bounds the set is the configuration and the environment, not an observation: the scratch config names only backends whose hosts are in the brief's list (core, aqua, npm, github and cargo tools, and `http:` URLs on `github.com` and `storage.googleapis.com`), the config discovery variables of `ENV` (`MISE_GLOBAL_CONFIG_FILE`, `MISE_CONFIG_DIR`, `MISE_SYSTEM_CONFIG_FILE`, `MISE_SYSTEM_CONFIG_DIR`, `MISE_CEILING_PATHS`, `MISE_IGNORED_CONFIG_PATHS`, the two override filename variables) leave that file the only config mise can load, which `h-config-ls` and the `planted-config` injection show, and the environment of every call is `ENV` and nothing else, so no other mise config, plugin or registry setting is consulted.
- **Nothing written.** The scratch `.config/mise` holds `config.toml` alone after the runs, and `none-written` printed, from an `os.lstat` whose only absence is `FileNotFoundError`. The real `~/.config/mise` holds the same single entry before and after (`config.toml`, 6962 bytes, modified 2026-10-26T23:40:46, no `mise.lock`), and `check` reports `real-before.txt` and `real-after.txt` equal with no `mise.lock` line. The modification times of the real `~/.local/share/mise`, `~/.local/state/mise` and `~/Library/Caches/mise` are identical before and after the run and are the stamps rounds 6 to 10 recorded; nothing moved between round 7 and this run, and this unit's runs hand mise an environment of `ENV` alone, every mise directory and config variable pointed inside the scratch home and the real `~/.config/mise` and `/etc/mise` listed as ignored. mise wrote only under the scratch home: version-list caches under `.cache/mise` and the `tracked-configs` and `incomplete-installs` directories under `.local/state/mise`.
- **Settings.** `npm.package_manager` is `npm` and `minimum_release_age` is `72h` in the copy, as `config.toml:112-113` and `:107` set them.
- **Attempt 1 (round 1, not re-taken).** With the shell's cwd under the real home, mise read the real `~/.config/mise/config.toml` as an untrusted project config and stopped with `Config files in ~/.config/mise/config.toml are not trusted`; the three `mise lock` runs exited 1 in 0 seconds and the file was opened, not changed (its listing and modification time are unchanged in every round since). The five error lines are pasted in the round-1 commit `e0a1526a`, not here, because a repeat would open the real file on purpose, which the brief's SCOPE forbids. This is the one way the unit touched a real mise path, and it is a property of mise's config discovery, not of `HOME`; since round 11 the procedure changes to a `cwd` that is also the ceiling of that walk and ignores the real directory by name.

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
- <https://mise.jdx.dev/configuration.html>, read 2026-10-29 for the config discovery variables: "mise loads config in this order, and a later file overrides an earlier one: 1. System config in `/etc/mise`. 2. Global config in `~/.config/mise`. 3. Config files in every directory from the filesystem root down to the current directory. The search starts below the nearest `ceiling_paths` directory when one is set; files in the ceiling directory itself are not loaded. 4. Global override files (`config.override.toml`), which beat everything above". On the global directory: "It lives in `~/.config/mise` (`MISE_CONFIG_DIR`), normally in `config.toml`." On one file: "`global_config_file` (`MISE_GLOBAL_CONFIG_FILE`) replaces all of these files with one file. It also turns off the override files." On the system config: "It lives in `/etc/mise` (`MISE_SYSTEM_CONFIG_DIR`) and accepts the same file names as the global directory, such as `/etc/mise/config.toml`. `system_config_file` (`MISE_SYSTEM_CONFIG_FILE`) replaces them with a single file." On the listing: "`mise config` lists the files mise loaded, lowest precedence first: later files override earlier ones." (<https://mise.jdx.dev/cli/config/ls.html>: "List config files currently in use, from lowest to highest precedence".)
- <https://mise.jdx.dev/configuration/settings.html>, the same day: "Settings with the miserc badge decide which config files mise loads, so mise reads them before any `mise.toml`: `env`, `auto_env`, `env_conf_d`, `ceiling_paths`, `ignored_config_paths`, `override_config_filenames` and `override_tool_versions_filenames`." and "Settings with the env only badge name the config files themselves, so they work only as environment variables: `default_config_filename`, `default_tool_versions_filename`, `global_config_file`, `global_config_root` and `system_config_file`." `global_config_file`: "When unset, mise reads `config.toml`, `conf.d/*.toml` and the other config files in `~/.config/mise` (or `MISE_CONFIG_DIR`), and global writes such as `mise use -g` go to `config.toml` there. When set, mise reads and writes only this file." `system_config_file`: "When unset, mise reads `conf.d/*.toml`, `config.toml`, `mise.toml` and their environment and `.local` variants in `/etc/mise` (or `MISE_SYSTEM_CONFIG_DIR`), and writes such as `mise config set --system` go to `config.toml` there. When set, mise reads and writes only this file." `ceiling_paths`: "By default, mise looks for config files in the current directory and every parent up to the filesystem root. The search stops at a ceiling directory, which is not searched itself: with `MISE_CEILING_PATHS=/home/user`, `/home/user/projects/app/mise.toml` loads but `/home/user/mise.toml` does not." `ignored_config_paths`: "Config files and directories mise does not load." "Entries are paths or glob patterns, including `**`. A path without glob characters also matches everything under it." `override_config_filenames`: "Project config filenames that mise looks for instead of `mise.toml`, `.mise.toml` and the other standard names." "In each directory, mise loads only files with these names, and environment-specific files such as `mise.development.toml` still load." `override_tool_versions_filenames`: "Set it to `none` to stop reading `.tool-versions` files". `trusted_config_paths`: "Directories whose config files mise trusts without asking." "They override trust prompts you declined and `mise trust --ignore`, but `ignored_config_paths` still stops configs from loading." The page lists no setting that makes an empty `override_config_filenames` mean "no names"; the measurement above shows this mise treats it as unset.

### The five V4-9 answers

**Where the lock lives under chezmoi.** The dry run names its target as `<HOME>/.config/mise/mise.lock`, beside the global config (first line of (b)), and the reference page puts the global sidecars in `~/.config/mise/locks/`. Under chezmoi the source would be `home/dot_mise/mise.lock` with a `home/dot_config/mise/mise.lock.tmpl` include, the same shape as the config today; both files are forbidden by `test_supply_chain_policy.py:419-420`, and `.chezmoiremove:21` deletes the rendered `~/.config/mise/mise.lock` on every apply. The vendor's command table says `mise upgrade` updates `mise.lock`, so a host `mise upgrade` rewrites the rendered file, and chezmoi then reports that file as drift until the next apply deletes or replaces it. With the embedded installer the sidecar directory `~/.config/mise/locks/` would need the same treatment.

**Whether `make update` becomes `mise lock --bump` in a PR followed by `mise install --locked` on hosts.** Today `scripts/upgrade-tools.sh:318` runs `mise upgrade --yes <tool>` per unheld tool on the host, which is exactly the command that would rewrite the lock. The lockfile workflow replaces that step with a scheduled `mise lock --bump --minimum-release-age 72h` (run (d) shows the shape of its output: one JSON object per moved tool) that opens a PR, and hosts run `mise install --locked` from the applied lock. `README.md:250-255` records the present trade-off on purpose, and `test_supply_chain_policy.py:464-466` forbids `--locked` in the three lifecycle files. The change is therefore a workflow decision for the operator (hosts stop upgrading on their own), not a CI fix, as research 4.4 says.

**How the CI copy step would carry `mise.lock` and `.mise/locks/`.** `test.yaml:259-261` copies one file into `RUNNER_TEMP/statusline-mise/mise.toml`. With a lock, the step also copies `mise.lock` beside it and, under the embedded installer, the sidecar directory as `.mise/locks/` (the project layout the reference page gives for a `mise.lock` beside `mise.toml`). mise-action does not add `--locked` here: it adds the flag when a lockfile sits in the working directory or its parents, and `test.yaml:263-270` runs it with `install: false` on the checkout, not on the copy. The four `mise -C … install` lines at `test.yaml:276-279` would carry `--locked` themselves.

**Whether `package_manager = "npm"` or the embedded installer is wanted.** Run (e) confirms `npm`. Under that setting the lock records the version only, so the npm supply-chain gain of the lockfile (the replayed dependency graph) does not apply to the ten `npm:` tools, which include the two agent CLIs. The embedded installer would record the graph, but `scripts/update-agent-assets.sh:148` repairs the agent CLIs with `MISE_NPM_PACKAGE_MANAGER=npm`, `tests/unit/test_runtime_health.py:347` asserts that call, and the npm cooldown work of U89 and U114 (`~/.npmrc` `min-release-age`, the publish-time check in `upgrade-tools.sh`) is built on npm's own behaviour. Switching the installer is its own unit with its own measurement (the ccstatusline and ccusage graphs under aube are listed under Left out).

**The 72 h policy moves to the bump schedule.** The lockfile page states that a locked version installs even when newer than `minimum_release_age`, and the npm page adds that for a locked graph the cutoff applies when the graph is resolved. Run (f) confirms the config's `72h`. Under a lock, the host no longer applies the cooldown at install time; the `--minimum-release-age 72h` flag of `mise lock --bump` (in the help text above) applies it when the bump resolves, so the policy holds only if every bump run carries that flag and no one hand-edits the lock.

## Recommendation

**defer.** The measured output agrees with row 233 of `decisions.tsv` (`2026-10-28T09:40:00Z`, phase `plan-P-36`): the same 7 platforms and 36 tools, nothing written, and the lock is technically ready (every backend resolved in 10 s, no token, no failure). What the dry run adds is the entry counts (258 and 149), the fact that today's bump would be a first write and not a move, and the attempt-1 finding about mise's config discovery. None of this changes the facts the deferral rests on: the tree forbids the lock in three places by policy, `make update` would rewrite it on every host run, the CI copy carries one file, `package_manager = "npm"` records the version only, and the 72 h cooldown would move from install time to the bump schedule.

The condition that would change the recommendation to `adopt` is an operator decision, recorded in `decisions.tsv`, to stop unattended host upgrades (`upgrade-tools.sh:318`) and take every unheld version from a scheduled `mise lock --bump --minimum-release-age 72h` PR, with `mise install --locked` on hosts and in `test.yaml:276-279`, plus a decision on the npm installer. The condition that would change it to `reject` is a decision to keep the present `latest` behind the cooldown as the permanent policy, in which case the lockfile settings test and `.chezmoiremove:21` are the complete record and this question closes. Absent either, the no-lock policy stands as `README.md:199-202` and `:250-255` describe it.

## Draft decisions row

| field    | value                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| ts       | 2026-10-29T16:15:47Z                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| phase    | plan-P-36                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| decision | mise.lock evaluation measured (plan P-36, research V4-9): defer; corrects the evidence of the 2026-10-28T09:40:00Z row, whose file handoff/research/05-eval-mise-lock.md was never written. Measured 2026-10-29 under a scratch HOME with mise 2026.10.19: `mise lock --global --dry-run` targets 7 platforms and 36 tools and would write 258 entries (36 x 7 plus 6 bun variant keys); the 4-platform set the http tables pin gives 149 entries; `--bump --dry-run --json` lists 36 first-time entries and no move; every backend (4 core, 11 aqua, 10 npm, 4 github, 2 cargo, 5 http) resolved in 10 s without a GitHub token; no lockfile written, the real ~/.config/mise unchanged. The condition stands: an operator decision to stop host-side `mise upgrade` (scripts/upgrade-tools.sh:318) and take versions from a scheduled `mise lock --bump --minimum-release-age 72h` PR, with `mise install --locked` on hosts and in the CI copy step (.github/workflows/test.yaml:259-261), and the npm installer question settled first |
| why      | the plan's acceptance asks for the measured output on record; the dry run changed no fact row 233 rests on: the tree's policy (README.md:199-202 and 250-255, home/.chezmoiremove:21, tests/unit/test_supply_chain_policy.py:404-421 and 464-466) forbids the lock and `--locked`, `make update` would rewrite the rendered lock on every run (vendor table: `mise upgrade` updates mise.lock), npm.package_manager=npm records the version only (the dependency graph needs the embedded installer, which scripts/update-agent-assets.sh:148 and tests/unit/test_runtime_health.py:347 do not use), and a locked version bypasses minimum_release_age so the 72 h policy would move to the bump schedule; one new fact: with a cwd under the real home, mise's parent-directory walk reads the real ~/.config/mise/config.toml as a project config                                                                                                                                                                                        |
| evidence | handoff/evaluations/U116-mise-lock.md                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| result   | proposed; the coordinator records                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |

The same row as one line with literal tab separators:

```text
2026-10-29T16:15:47Z	plan-P-36	mise.lock evaluation measured (plan P-36, research V4-9): defer; corrects the evidence of the 2026-10-28T09:40:00Z row, whose file handoff/research/05-eval-mise-lock.md was never written. Measured 2026-10-29 under a scratch HOME with mise 2026.10.19: `mise lock --global --dry-run` targets 7 platforms and 36 tools and would write 258 entries (36 x 7 plus 6 bun variant keys); the 4-platform set the http tables pin gives 149 entries; `--bump --dry-run --json` lists 36 first-time entries and no move; every backend (4 core, 11 aqua, 10 npm, 4 github, 2 cargo, 5 http) resolved in 10 s without a GitHub token; no lockfile written, the real ~/.config/mise unchanged. The condition stands: an operator decision to stop host-side `mise upgrade` (scripts/upgrade-tools.sh:318) and take versions from a scheduled `mise lock --bump --minimum-release-age 72h` PR, with `mise install --locked` on hosts and in the CI copy step (.github/workflows/test.yaml:259-261), and the npm installer question settled first	the plan's acceptance asks for the measured output on record; the dry run changed no fact row 233 rests on: the tree's policy (README.md:199-202 and 250-255, home/.chezmoiremove:21, tests/unit/test_supply_chain_policy.py:404-421 and 464-466) forbids the lock and `--locked`, `make update` would rewrite the rendered lock on every run (vendor table: `mise upgrade` updates mise.lock), npm.package_manager=npm records the version only (the dependency graph needs the embedded installer, which scripts/update-agent-assets.sh:148 and tests/unit/test_runtime_health.py:347 do not use), and a locked version bypasses minimum_release_age so the 72 h policy would move to the bump schedule; one new fact: with a cwd under the real home, mise's parent-directory walk reads the real ~/.config/mise/config.toml as a project config	handoff/evaluations/U116-mise-lock.md	proposed; the coordinator records
```

## Left out

- A real `mise lock --global` write, on any host or in the worktree. Every `mise lock` above carries `--dry-run`.
- `mise install --locked` on any host, so the install side of the workflow is unmeasured.
- The ccstatusline and ccusage dependency graphs under the embedded installer. Run (e) shows the npm installer, under which the lock records the version only, and the unit did not switch the installer.
- The Ubuntu host. Every command ran on the macOS host; the `linux-*` platform entries above come from mise's own resolution, not from a Linux run.
- A network capture. The hosts contacted are read from mise's cache file names; the controls that bound the set are named under Hosts contacted.
- A repeat of round 1's attempt 1 (the cwd under the real home). Its five error lines stay in the round-1 commit; a repeat would open the real `~/.config/mise/config.toml` on purpose.
- The handoff `README.md` row for `evaluations/`, which the coordinator writes.
- A repeat of the probe that chose the ceiling spelling and the override sentinel. Its two findings are re-taken inside the `planted-config` injection (the ceiling in both spellings excludes the planted configs; the empty override value is ignored), so the probe's own output is not pasted.
