#!/usr/bin/env -S python3 -I
"""Refuse a brief that judges an open-ended input without naming its closing form and its trust boundary (regime-cutover
U104, U121).

`~/.local/bin/common/brief-check.py .orchestration/orchestrate/<program>/briefs/U<n>-<slug>.md`, run from the
checkout, reads one brief. Exit 0, printing nothing: the brief's GOAL, CHANGE and CONTEXT hold no trigger term, or
its CLOSURE section names exactly one form and its TRUST section names what the unit trusts. Exit 1, one reason per
line on stdout: a trigger term fired and there is no CLOSURE section, or CLOSURE names zero, two or more forms or a
word outside `ast`, `parser-module`, `allowlist` and `remove`; a trigger term fired and there is no TRUST section, or
it is under 40 characters, or it holds neither `trusted` nor `trusts`; CLOSURE names `allowlist` or `ast` while CHANGE
holds `denylist`, `forbidden words` or `list of commands` (a denylist dressed as a form); or no GOAL, CHANGE or
CONTEXT section was found at all. Exit 2, nothing on stdout: usage, a file that cannot be read or decoded, or a
section heading that appears twice; a brief the check cannot read is never read as clean.

The script is a pinned lever (regime-cutover U31, round 3 of U104): `scripts/generate-agent-configs.py` writes the
same bytes to `home/dot_local/bin/common/executable_brief-check.py`, which chezmoi installs as
`~/.local/bin/common/brief-check.py`, and pins their sha256 under `claude.levers.sha256`; the orchestrator seat's
policy allows that path alone. Before anything else the file hashes itself and refuses to run (exit 2, nothing on
stdout) when the digest differs from its pin, so a repository without `scripts/orchestrator/` runs the same checked
copy and a rewritten copy judges no brief.

The data shape: a brief is a sequence of upper-case section headings, each a line that is exactly its name (plus the
`WORKER RULES (...)` line, whose body names shells, paths and hooks as rules, not as the thing judged), each followed
by its text; `sections` parses it into one `dict[str, str]` and refuses a heading that appears twice (a merge would
read `CLOSURE\nast\nCLOSURE\n` as `ast`). The trigger terms are one tuple of (term, reason) rows: the words the
thirteen treadmill rows of the program's `handoff/02-audit-treadmill-analysis.md` and U109 and U112 held in GOAL,
CHANGE and CONTEXT before three or more rounds found the form. The forms are one tuple of four. A later unit adds a
term by adding a row. Only SCOPE, FORBIDDEN and the other sections name paths and limits, so a term there fires
nothing.
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
    "CLOSURE",
    "TRUST",
    "REPORT",
    "STANDING",
)
# The one heading that carries a parenthesised note: `WORKER RULES (standing orders ...)`.
WORKER_RULES = "WORKER RULES"
# The sections whose text says what the unit judges; SCOPE and FORBIDDEN name paths and limits, not the form.
JUDGED = ("GOAL", "CHANGE", "CONTEXT")
# One row per term, (term, why a brief holding it must name its closing form and its trust boundary). A term is
# matched as a whole word, any case; a space in a term also matches a hyphen (`fail-closed`); a term ending in `*`
# matches every word that begins with it (`tokenize`, `tokenizer`, `tokenization`). A later unit adds a row.
TRIGGERS = (
    ("shell", "shell text has quoting, expansion and word-splitting forms no hand-written reader lists"),
    ("tokeniz*", "a hand-written tokenizer leaks on the next token form its author did not list"),
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
    ("bound", "a bound over an open-ended input is a check whose cases its author listed (U109: 24 rounds)"),
    ("refuse", "a refusal decides on evidence read from an open-ended input"),
    ("fail closed", "a fail-closed read decides on a producer's output, an open-ended input (U112: 18 rounds)"),
    ("untrusted", "untrusted input is open-ended by definition"),
    ("sandbox", "a sandbox boundary is judged from paths, mounts and probes the reader did not list"),
    ("lint", "a lint over text is a hand-written reader unless it walks the language's own tree"),
    ("rule", "a rule over text has cases its author did not list"),
    ("allowlist", "an allowlist closes only as an exact-form table; written as prose it is a denylist"),
    ("denylist", "a denylist over an open-ended input never closes (research/04 entries 14 and 15)"),
    ("walk", "a walk over a tree or a directory meets node kinds its author did not list"),
    ("census", "a census of a scope is complete only against a closed set"),
)
# The four closing forms; a CLOSURE names exactly one.
FORMS = ("ast", "parser-module", "allowlist", "remove")
# A CLOSURE naming one of these forms while CHANGE holds one of the phrases below is a denylist dressed as a form.
DRESSED_FORMS = ("ast", "allowlist")
DRESSED_PHRASES = ("denylist", "forbidden words", "list of commands")
# The TRUST section names what the unit trusts and does not read: at least this many characters, one of these words.
TRUST_WORDS = ("trusted", "trusts")
TRUST_MINIMUM = 40


def word_pattern(terms):
    """One regex over the terms, each a whole word, any case, with one named group per row (`t<index>`).

    One group per row, so the row whose reason is printed is the row the regex matched: `re.IGNORECASE` folds
    `ſhell` and a Kelvin-sign `hooK` onto their terms, and neither spelling has a `.lower()` form the table holds.
    """
    alternatives = []
    for index, term in enumerate(terms):
        stem = term.endswith("*")
        body = "[ -]".join(re.escape(part) for part in term.rstrip("*").split(" "))
        alternatives.append(rf"(?P<t{index}>\b{body}" + ("" if stem else r"\b") + ")")
    return re.compile("|".join(alternatives), re.IGNORECASE)


TRIGGER_WORD = word_pattern([term for term, _ in TRIGGERS])
# The reason by the term as a reason line names it, without a stem's `*`.
REASONS = {term.rstrip("*"): reason for term, reason in TRIGGERS}
DRESSED_WORD = word_pattern(DRESSED_PHRASES)
TRUST_WORD = word_pattern(TRUST_WORDS)


def matched_term(pattern, terms, text):
    """The row of `terms` the first match in `text` belongs to, stripped of a stem `*`, or None."""
    match = pattern.search(text)
    if match is None:
        return None
    return terms[int(match.lastgroup[1:])].rstrip("*")


class BriefError(Exception):
    """The text is not a brief in the grammar, so nothing is judged (exit 2)."""


def heading(line):
    """The section name when `line` is a heading, else None."""
    name = line.rstrip()
    if name in SECTIONS:
        return name
    if name.startswith(WORKER_RULES + " (") and name.endswith(")"):
        return WORKER_RULES
    return None


def sections(text):
    """The brief as name to body text; a heading that appears twice raises BriefError naming both lines."""
    found = {}
    heading_line = {}
    current = None
    for number, line in enumerate(text.splitlines(), 1):
        name = heading(line)
        if name is not None:
            if name in found:
                raise BriefError(
                    f"{name} appears twice (lines {heading_line[name]} and {number}); a brief has one of each"
                )
            current = name
            found[current] = []
            heading_line[name] = number
        elif current is not None:
            found[current].append(line)
    return {name: "\n".join(body) for name, body in found.items()}


def first_trigger(found):
    """(section, term) of the first trigger term in a judged section, or None."""
    for name in JUDGED:
        term = matched_term(TRIGGER_WORD, [term for term, _ in TRIGGERS], found.get(name, ""))
        if term is not None:
            return name, term
    return None


def closure(body):
    """(form, None) when the CLOSURE body is exactly one form line, else (None, why it is not)."""
    lines = [line.strip() for line in body.splitlines() if line.strip()]
    if not lines:
        return None, "CLOSURE is empty"
    named = []
    for line in lines:
        name = line.split(":", 1)[0].rstrip()
        if name not in FORMS:
            return None, f'CLOSURE line "{line}" names no form ({", ".join(FORMS)})'
        named.append(name)
    if len(named) != 1:
        return None, f"CLOSURE names {len(named)} forms ({', '.join(named)}), not one"
    return named[0], None


def trust(body):
    """None when the TRUST body names what the unit trusts, else why it does not."""
    text = " ".join(body.split())
    if len(text) < TRUST_MINIMUM:
        return f"TRUST is {len(text)} characters, under {TRUST_MINIMUM}"
    if matched_term(TRUST_WORD, TRUST_WORDS, text) is None:
        return "TRUST names nothing as trusted (no word `trusted` or `trusts`)"
    return None


def judge(found):
    """The reasons the parsed brief is refused, one per line; empty when it passes."""
    if not any(name in found for name in JUDGED):
        return ["no GOAL, CHANGE or CONTEXT section"]
    reasons = []
    trigger = first_trigger(found)
    form, fault = closure(found["CLOSURE"]) if "CLOSURE" in found else (None, "no CLOSURE section")
    if trigger is None:
        if fault is not None and "CLOSURE" in found:
            reasons.append(fault)  # a CLOSURE the check cannot read is never read as clean
    else:
        section, term = trigger
        if form is None:
            reasons.append(f'{section} holds "{term}" ({REASONS[term]}); {fault}')
        trust_fault = trust(found["TRUST"]) if "TRUST" in found else "no TRUST section"
        if trust_fault is not None:
            reasons.append(f'{section} holds "{term}"; {trust_fault}')
    if form in DRESSED_FORMS:
        phrase = matched_term(DRESSED_WORD, DRESSED_PHRASES, found.get("CHANGE", ""))
        if phrase is not None:
            reasons.append(f'CLOSURE names {form} and CHANGE holds "{phrase}": a denylist dressed as a form')
    return reasons


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
    try:
        found = sections(text)
    except BriefError as error:
        print(f"brief-check: cannot read {args.brief}: {error}", file=sys.stderr)
        return 2
    reasons = judge(found)
    for reason in reasons:
        print(f"brief-check: {args.brief}: {reason}")
    return 1 if reasons else 0


if __name__ == "__main__":
    sys.exit(main())
