#!/usr/bin/env -S python3 -I
"""Refuse a brief that judges an open-ended input without naming the mechanism that closes it (regime-cutover U104).

`~/.local/bin/common/brief-check.py .orchestration/orchestrate/<program>/briefs/U<n>-<slug>.md`, run from the
checkout, reads one brief and prints one line. Exit 0: the brief's GOAL, CHANGE and CONTEXT hold no trigger term, or
its CLOSURE section names exactly one mechanism. Exit 1: a trigger term fired and the brief has no CLOSURE section, or
the CLOSURE section is not one mechanism name (`ast`, `parser-module`, `allowlist` or `remove`, optionally followed by
a colon and free text on the same line), or no GOAL, CHANGE or CONTEXT section was found at all, or one section
heading appears twice. Exit 2: usage, or a file that cannot be read or decoded; an unreadable brief is never read as
clean.

The script is a pinned lever (regime-cutover U31, round 3 of U104): `scripts/generate-agent-configs.py` writes the
same bytes to `home/dot_local/bin/common/executable_brief-check.py`, which chezmoi installs as
`~/.local/bin/common/brief-check.py`, and pins their sha256 under `claude.levers.sha256`; the orchestrator seat's
policy allows that path alone. Before anything else the file hashes itself and refuses to run (exit 2, nothing on
stdout) when the digest differs from its pin, so a repository without `scripts/orchestrator/` runs the same checked
copy and a rewritten copy judges no brief.

Thirteen `treadmill` and `premise` rows in the program's decisions share one shape (handoff
`02-audit-treadmill-analysis.md`): a hand-written reader over an open-ended input passed a fresh audit once per round
until, three or more rounds in, the mechanism changed to an AST walk, one strict parser module, an exact-form
allowlist, or removal. The trigger terms below are the words those briefs' GOAL, CHANGE and CONTEXT held. A section
is a line that is exactly its upper-case name; its body runs to the next such line, and a brief has one of each, so a
heading that appears twice is refused rather than merged (a merge would read `CLOSURE\nast\nCLOSURE\n` as `ast`).
Only SCOPE, FORBIDDEN and the other sections name paths and limits, so a term there fires nothing.
"""

import argparse
import hashlib
import os
import re
import sys

LEVER = "brief-check.py"
# The pin line of this lever in the manifest, read as text: the manifest is never parsed as YAML here.
PIN_LINE = re.compile(r"^      brief-check\.py: ([0-9a-f]{64})$")


def refuse(reason):
    """Print the refusal in the shell levers' words on stderr and exit 2; no brief was judged."""
    print(f"{LEVER}: refused: {reason}", file=sys.stderr)
    sys.exit(2)


def lever_self_check():
    """Refuse to run unless this file's sha256 equals its pin in the manifest beside it (regime-cutover U31).

    The physical directory of this file decides the manifest: the deployed `~/.agents/agent-config.yaml` when the
    directory is the physical `~/.local/bin/common`, else the checkout's `home/dot_agents/agent-config.yaml` two
    levels up; an unset or unresolvable HOME means the checkout manifest. The whole install path is resolved, not
    HOME alone, since an install reached through a symlinked `.local`, `bin` or `common` compared unequal and read
    the checkout manifest two levels up (round 5). The cwd decides nothing: the shebang runs
    `python3 -I` from PATH as the shell levers' `bash` comes from PATH, since `uv run` honoured a `.python-version`
    in the checkout the lever ran from and a planted interpreter answered before this check (round 4), and `-I`
    ignores `PYTHON*` variables, the user site and the script directory. Every read is checked and a failed one is
    a refusal, never a pass (preferences.md standing order 21).
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
    pins = [match.group(1) for match in map(PIN_LINE.match, lines) if match]
    if len(pins) != 1:
        refuse(f"no single sha256 pin for {LEVER} in {manifest}")
    try:
        with open(self_path, "rb") as handle:
            digest = hashlib.sha256(handle.read()).hexdigest()
    except OSError:
        refuse(f"cannot hash {self_path}")
    if digest != pins[0]:
        refuse(f"sha256 {digest} of {self_path} differs from the pin in {manifest}")


lever_self_check()

SECTIONS = (
    "GOAL",
    "SCOPE",
    "CHANGE",
    "CONTEXT",
    "ACCEPTANCE",
    "VERIFY",
    "TIMEBOX",
    "FORBIDDEN",
    "REPORT",
    "STANDING",
    "CLOSURE",
)
# The sections whose text says what the unit judges; SCOPE and FORBIDDEN name paths and limits, not the mechanism.
JUDGED = ("GOAL", "CHANGE", "CONTEXT")
# One row per term, (term, why a brief holding it must name its closing mechanism). A later unit adds a row.
TRIGGERS = (
    ("shell", "shell text has quoting, expansion and word-splitting forms no hand-written reader lists"),
    ("tokenize", "a hand-written tokenizer leaks on the next token form its author did not list"),
    ("tokenizer", "a hand-written tokenizer leaks on the next token form its author did not list"),
    ("parse", "hand parsing of an open-ended input is the shape of every treadmill row"),
    ("parser", "a hand-written parser is replaced by an AST walk or one strict parser module in the end"),
    ("regex", "a regular expression over an open-ended input matches forms its author did not list"),
    ("hook", "a hook runs on text its author does not control"),
    ("worktree", "worktree records and paths have forms git keeps adding (U95: ten rounds, then refusal)"),
    ("config", "a configuration file holds keys, includes and values its reader did not list"),
    ("path", "a path has symlink, case, encoding and quoting forms no string check closes"),
    ("process", "a process tree read as text changes under the reader"),
    ("signal", "signal delivery and handling have an open set of orderings"),
    ("supervisor", "a supervisor judges a live process's state from open-ended evidence"),
    ("curl", "fetched content is open-ended input"),
    ("wget", "fetched content is open-ended input"),
    ("heredoc", "here-document bodies carry every quoting and substitution form"),
    ("quote", "quoting rules differ by shell, by context and by the word's position"),
)
MECHANISMS = ("ast", "parser-module", "allowlist", "remove")
# The one regular expression over the brief (FORBIDDEN): the trigger terms as whole words, case-insensitive. One named
# group per table row, so the row whose reason is printed is the row the regex matched: `re.IGNORECASE` folds `ſhell`
# and a Kelvin-sign `hooK` onto their terms, and neither spelling has a `.lower()` form the table holds.
TRIGGER_WORD = re.compile(
    r"\b(?:" + "|".join(f"(?P<{term}>{re.escape(term)})" for term, _ in TRIGGERS) + r")\b", re.IGNORECASE
)
REASONS = dict(TRIGGERS)


def sections(text):
    """(name to body text, None), or (None, why) when one heading appears twice, naming it and both line numbers."""
    found = {}
    heading_line = {}
    current = None
    for number, line in enumerate(text.splitlines(), 1):
        name = line.rstrip()
        if name in SECTIONS:
            if name in found:
                return None, f"{name} appears twice (lines {heading_line[name]} and {number}); a brief has one of each"
            current = name
            found[current] = []
            heading_line[name] = number
        elif current is not None:
            found[current].append(line)
    return {name: "\n".join(body) for name, body in found.items()}, None


def first_trigger(found):
    """(section, term) of the first trigger term in a judged section, or None."""
    for name in JUDGED:
        match = TRIGGER_WORD.search(found.get(name, ""))
        if match:
            return name, match.lastgroup
    return None


def closure(body):
    """(mechanism, None) when the CLOSURE body is exactly one mechanism line, else (None, why it is not)."""
    lines = [line.strip() for line in body.splitlines() if line.strip()]
    if not lines:
        return None, "CLOSURE is empty"
    named = []
    for line in lines:
        name = line.split(":", 1)[0].rstrip()
        if name not in MECHANISMS:
            return None, f'CLOSURE line "{line}" names no mechanism ({", ".join(MECHANISMS)})'
        named.append(name)
    if len(named) != 1:
        return None, f"CLOSURE names {len(named)} mechanisms ({', '.join(named)}), not one"
    return named[0], None


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("brief", help="the brief file, .orchestration/orchestrate/<program>/briefs/U<n>-<slug>.md")
    args = parser.parse_args(argv)
    try:
        with open(args.brief, encoding="utf-8") as handle:
            text = handle.read()
    except (OSError, UnicodeDecodeError) as error:
        print(f"brief-check: cannot read {args.brief}: {error}", file=sys.stderr)
        return 2
    found, repeated = sections(text)
    if found is None:
        print(f"brief-check: {args.brief}: {repeated}")
        return 1
    if not any(name in found for name in JUDGED):
        print(f"brief-check: {args.brief} has no GOAL, CHANGE or CONTEXT section")
        return 1
    trigger = first_trigger(found)
    mechanism, fault = closure(found["CLOSURE"]) if "CLOSURE" in found else (None, "no CLOSURE section")
    if trigger is None:
        if fault is not None and "CLOSURE" in found:
            print(f"brief-check: {fault}")  # a CLOSURE the check cannot read is never read as clean
            return 1
        print("brief-check: no trigger term in GOAL, CHANGE or CONTEXT")
        return 0
    name, term = trigger
    if mechanism is None:
        print(f'brief-check: {name} holds "{term}" ({REASONS[term]}); {fault}')
        return 1
    print(f'brief-check: {name} holds "{term}"; closure: {mechanism}')
    return 0


if __name__ == "__main__":
    sys.exit(main())
