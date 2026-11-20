#!/usr/bin/env -S python3 -I -S
"""Refuse a plan or status handout that lacks the program's goal sentence (regime-cutover U649, standing order 61).

The operator fixed the purpose and goal as one sentence (2026-11-06, `handoff/08-purpose-and-goal.md`) and twice on
2026-11-20 corrected coordinator reports that presented added work (orders 59 and 60) as the goal; text in the skill
did not hold. This check puts the anchor in a lever the coordinator runs before a handout is written:
`handout-check.py <store> [<file>...]` reads the goal sentence as `program-status.py` does (the first Markdown quote
line, `> ...`, of `<store>/handoff/08-purpose-and-goal.md`, read whole and stripped of its `> ` prefix; a `>` alone
opens the line and one space after it goes with the prefix) and holds every file given, else every
`<store>/handouts/plan-*.md` and `<store>/handouts/status-*.md` in name order, to contain the sentence verbatim on one
line. It judges nothing else about a file (TRUST of the brief: the handoff file is the one source of the sentence).

Exit 0 with `handout-check: ok <file>` per file and the last line `handout-check: <n> files, ok` on stdout when every
file holds the sentence (no file matched is `0 files, ok`: a store without a plan or status handout yet is not a
malformed one). Exit 1 with one stderr line per failing file, `handout-check: <file> lacks the goal sentence on one
line`, after the passing files' `ok` lines on stdout, when any file lacks it: a sentence altered by one character,
split over two lines or absent alike. Exit 2 with one stderr line, `handout-check.py: refused: <reason>`, and nothing
on stdout for every refusal (standing order 21: a failed read is never a pass): the self pin (below), a store that is
no directory, the handoff file missing, unreadable or not UTF-8, no quote line in it, a quote line that is empty,
holds a tab, a control character or a line separator or is more than 1024 bytes long (program-status.py's refusals,
spelled the same), a `handouts` directory that is missing or cannot be listed when no file is given, a matching entry
that is not a regular file (a directory, a symbolic link), and a file given or matched that is missing, unreadable or
not UTF-8; every file is read before anything prints, so a refusal prints nothing. Every file is read byte-exact and
the sentence is sought in each line of the text as given, so a CRLF handout whose line holds it passes and nothing is
normalised. One sanitiser folds every line boundary `str.splitlines` knows inside a path into a space, so one refusal
and one failing file are one line each. Nothing is written and no mode is changed.

Installed as `~/.local/bin/common/handout-check.py` under its bare name, mode 0644, as `sweep-scope.py` and
`ledger.py` are (the generator's `LEVER_MODULES`), and run as `python3 -I -S ~/.local/bin/common/handout-check.py
<store> [<file>...]`, never by path: `scripts/generate-agent-configs.py` writes the same bytes to
`home/dot_local/bin/common/handout-check.py` and pins their sha256 under `claude.levers.sha256`. Before anything else
the file hashes itself against that pin in brief-check.py's form, read from the deployed manifest
`~/.agents/agent-config.yaml` when its physical directory is the physical `~/.local/bin/common`, else from the
checkout's `home/dot_agents/agent-config.yaml` two levels up, and refuses to run on a difference, so a rewritten copy
checks nothing.
"""

import argparse
import hashlib
import os
import re
import stat
import sys

LEVER = "handout-check.py"
PROGRAM = "handout-check"
# The levers block of the manifest, read as text by indentation alone, never parsed as YAML (brief-check.py, U136).
MAPPING_KEY = re.compile(r"^(\S+):$")
LEVER_PIN = re.compile(r"^(\S+): ([0-9a-f]{64})$")
LEVERS_KEYS = ("claude", "levers", "sha256")

# The goal sentence's source and bounds, program-status.py's (standing order 61, U649): the first Markdown quote line
# of the handoff file, one line of at most GOAL_MAX_BYTES bytes with no tab, control character or line separator.
GOAL_FILE = os.path.join("handoff", "08-purpose-and-goal.md")
GOAL_MAX_BYTES = 1024
GOAL_WHY = "the goal sentence is read from its first Markdown quote line"
CONTROL = re.compile(r"[\x00-\x1f\x7f-\x9f\u2028\u2029]")
# The handouts the default checks: `<store>/handouts/plan-*.md` and `status-*.md`, regular files, in name order.
HANDOUTS_DIR = "handouts"
HANDOUT_PREFIXES = ("plan-", "status-")
HANDOUT_SUFFIX = ".md"
# The line boundaries `str.splitlines` knows; `one_line` replaces each with a space in every printed path.
LINE_BREAK = re.compile(r"[\n\r\x0b\x0c\x1c\x1d\x1e\x85\u2028\u2029]")


def one_line(text):
    """`text` with every line boundary `str.splitlines` knows a space: the one sanitiser of every refusal and every
    printed line, so a path that holds one cannot add a line."""
    return LINE_BREAK.sub(" ", text)


def refuse(reason):
    """One stderr line in the levers' words, exit 2; nothing was printed."""
    print(f"{LEVER}: refused: {one_line(reason)}", file=sys.stderr)
    sys.exit(2)


def lever_self_check():
    """Refuse to run unless this file's sha256 equals its pin in the manifest beside it (regime-cutover U31).

    The physical directory of this file decides the manifest: the deployed `~/.agents/agent-config.yaml` when the
    directory is the physical `~/.local/bin/common`, else the checkout's `home/dot_agents/agent-config.yaml` two
    levels up; an unset or unresolvable HOME means the checkout manifest. The pin is the block's `handout-check.py`
    entry: one entry is the pin, none or two is a refusal. Every read is checked and a failed one is a refusal, never
    a pass (preferences.md standing order 21); the reader is brief-check.py's, spelled the same.
    """
    directory = os.path.realpath(os.path.dirname(os.path.abspath(__file__)))
    self_path = os.path.join(directory, os.path.basename(__file__))
    home = os.environ.get("HOME", "")
    if home and os.path.isdir(home) and directory == os.path.realpath(os.path.join(home, ".local/bin/common")):
        manifest = os.path.join(home, ".agents/agent-config.yaml")
    else:
        manifest = os.path.join(directory, "../../home/dot_agents/agent-config.yaml")
    if not os.access(manifest, os.R_OK):
        refuse(f"manifest unreadable: {manifest}")
    try:
        with open(manifest, "rb") as handle:
            lines = handle.read().decode("utf-8", "replace").splitlines()
    except OSError:
        refuse(f"cannot read {manifest}")
    pins = [digest for name, digest in manifest_levers(lines, manifest) if name == LEVER]
    if len(pins) != 1:
        refuse(f"no single sha256 pin for {LEVER} in {manifest}")
    try:
        with open(self_path, "rb") as handle:
            digest = hashlib.sha256(handle.read()).hexdigest()
    except OSError:
        refuse(f"cannot hash {self_path}")
    if digest != pins[0]:
        refuse(f"sha256 {digest} of {self_path} differs from the pin in {manifest}")


def manifest_levers(lines, manifest):
    """The `(name, sha256)` pins under the manifest's `claude.levers.sha256` mapping, in file order (brief-check.py,
    U136): the mapping keys are walked by indentation, so `levers:` counts only under the top-level `claude:` and
    `sha256:` only under that `levers:`; inside the block, blank and comment lines are skipped, the entries share the
    indentation of the first pin, and the list ends at the first line indented less. An entry that is not
    `<name>: <64 hex>` is a refusal naming the line; no entry at all is the missing-block refusal."""
    pins = []
    keys = []  # the open mapping keys as (indentation, key), outermost first
    block = None  # the indentation of the `sha256:` key once the path is open
    entries = None  # the indentation of the pin lines, fixed by the first
    for number, line in enumerate(lines, 1):
        text = line.lstrip(" ")
        if not text or text.startswith("#"):
            continue
        indent = len(line) - len(text)
        if block is not None:
            if indent <= block or (entries is not None and indent < entries):
                break
            match = LEVER_PIN.match(text)
            if match is None or (entries is not None and indent != entries):
                refuse(f"line {number} of {manifest} is not a `<name>: <sha256>` pin under claude.levers.sha256")
            entries = indent
            pins.append((match.group(1), match.group(2)))
            continue
        while keys and indent <= keys[-1][0]:
            keys.pop()
        match = MAPPING_KEY.match(text)
        if match and (keys or indent == 0):
            keys.append((indent, match.group(1)))
            if tuple(key for _, key in keys) == LEVERS_KEYS:
                block = indent
    if not pins:
        refuse(f"no claude.levers.sha256 block in {manifest}")
    return tuple(pins)


lever_self_check()


def read_text(path, why):
    """The whole file as strict UTF-8, byte-exact (`newline=""`: no CRLF or CR is turned into a newline); a file that
    is missing, unreadable or not UTF-8 is a refusal naming it, the missing one with `why` it is read."""
    try:
        with open(path, encoding="utf-8", newline="") as handle:
            return handle.read()
    except FileNotFoundError:
        refuse(f"{path} is missing; {why}")
    except OSError as error:
        refuse(f"cannot read {path}: {error.strerror}")
    except UnicodeDecodeError as error:
        refuse(f"{path} is not UTF-8: {error.reason}")


def goal_sentence(store):
    """The goal sentence (standing order 61, U649): the first Markdown quote line (`> ...`) of
    `<store>/handoff/08-purpose-and-goal.md`, read whole and stripped of its `> ` prefix (a `>` alone opens the line;
    one space after it is the prefix's and goes). A missing, unreadable or non-UTF-8 file, a file with no quote line,
    and a quote line that is empty, holds a tab, a control character or a line separator, or is more than 1024 bytes
    long are refusals naming the file and the line (order 21), so the goal line is always one line of bounded length
    and the sentence a handout check can hold a file to."""
    path = os.path.join(store, GOAL_FILE)
    for number, line in enumerate(read_text(path, GOAL_WHY).split("\n"), 1):
        if not line.startswith(">"):
            continue
        sentence = line[1:].removeprefix(" ")
        if "\t" in sentence:
            refuse(f"line {number} of {path}, the goal sentence, holds a tab")
        if CONTROL.search(sentence):
            refuse(f"line {number} of {path}, the goal sentence, holds a control character")
        if not sentence:
            refuse(f"line {number} of {path} is an empty quote line; {GOAL_WHY}")
        size = len(sentence.encode("utf-8"))
        if size > GOAL_MAX_BYTES:
            refuse(f"line {number} of {path}, the goal sentence, is {size} bytes, more than {GOAL_MAX_BYTES}")
        return sentence
    refuse(f"{path} holds no Markdown quote line (`> ...`); {GOAL_WHY}")


def handout_files(store):
    """Every `<store>/handouts/plan-*.md` and `status-*.md`, regular files in name order; a `handouts` directory that
    is missing or cannot be listed, and a matching entry that is not a regular file, are refusals naming them."""
    directory = os.path.join(store, HANDOUTS_DIR)
    try:
        names = sorted(os.listdir(directory))
    except FileNotFoundError:
        refuse(f"{directory} is missing; the plan and status handouts are read from it")
    except OSError as error:
        refuse(f"cannot list {directory}: {error.strerror}")
    files = []
    for name in names:
        if not (name.startswith(HANDOUT_PREFIXES) and name.endswith(HANDOUT_SUFFIX)):
            continue
        path = os.path.join(directory, name)
        try:
            status = os.lstat(path)
        except OSError as error:
            refuse(f"cannot stat {path}: {error.strerror}")
        if not stat.S_ISREG(status.st_mode):
            refuse(f"{path} is not a regular file; a plan or status handout is one")
        files.append(path)
    return files


def holds_on_one_line(text, sentence):
    """Whether one line of `text`, split on `\\n` alone, contains `sentence` verbatim; the sentence holds no line
    boundary (the reader refuses one), so a sentence split over two lines is not found."""
    return any(sentence in line for line in text.split("\n"))


def parser():
    top = argparse.ArgumentParser(prog=LEVER, description=__doc__.splitlines()[0])
    top.add_argument("store", help="the program store directory (handoff/08-purpose-and-goal.md, handouts/)")
    top.add_argument(
        "files", nargs="*", help="the handouts to check; none means every handouts/plan-*.md and status-*.md"
    )
    return top


def main(argv=None):
    args = parser().parse_args(sys.argv[1:] if argv is None else list(argv))
    store = os.path.realpath(args.store)
    try:
        status = os.lstat(store)
    except OSError as error:
        refuse(f"the store {store} cannot be read: {error.strerror}")
    if not stat.S_ISDIR(status.st_mode):
        refuse(f"the store {store} is not a directory")
    sentence = goal_sentence(store)
    files = list(args.files) if args.files else handout_files(store)
    # Every file is read before anything prints, so a refusal on the last file prints nothing.
    results = [
        (path, holds_on_one_line(read_text(path, "it was given or matched as a handout"), sentence)) for path in files
    ]
    for path, holds in results:
        if holds:
            print(f"{PROGRAM}: ok {one_line(path)}")
    failing = [path for path, holds in results if not holds]
    for path in failing:
        print(f"{PROGRAM}: {one_line(path)} lacks the goal sentence on one line", file=sys.stderr)
    if failing:
        return 1
    print(f"{PROGRAM}: {len(results)} files, ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
