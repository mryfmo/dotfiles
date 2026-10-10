"""The two high-risk path tiers, shared by scripts/validate-task.py and (from T124 wave 2a) the review gate.

The review tier decides whether a change needs review; it is a copy of the lists in
scripts/require-crit-review.py until wave 2a switches the gate to importing it
(tests/unit/test_validate_task.py keeps the two equal meanwhile). The design tier is
narrower and explicit: a task whose allowed files match it is a security task, which
needs a reviewed design. The task front-matter parser and the canonical design hash
live here too, because the gate imports them in wave 2a and runs without PyYAML.
"""

from __future__ import annotations

import hashlib
import json
import re

HIGH_RISK_PREFIXES = (
    ".codex/",
    ".claude/",
    "home/dot_agents/plugins/",
    "home/dot_agents/skills/",
    "home/dot_claude/",
    "home/dot_codex/",
    "home/dot_config/claude/",
    "home/dot_config/codex/",
    "home/dot_config/herdr/",
    "scripts/",
)

HIGH_RISK_FILES = {
    "AGENTS.md",
    "home/.chezmoiscripts/common/run_once_after_06-install-agent-assets.sh.tmpl",
    "home/dot_agents/agent-config.yaml",
    "home/dot_local/bin/common/executable_herdr-agents",
    "home/dot_zshrc",
    "tests/install/common/lifecycle.bats",
}

HIGH_RISK_TOKENS = (
    "ccgate",
    "crit",
    "agmsg",
    "herdr",
    "hook",
    "hooks",
    "plugin",
    "permission",
    "ponytail",
    "superpowers",
)

# The gate's low-risk suffixes: a task whose allowed files all end in one is prose (the `docs` tier).
LOW_RISK_SUFFIXES = (
    ".md",
    ".txt",
)

# Glob patterns (`**` crosses directories, `*` does not). The auth helpers are the files
# that handle a credential or a key: git's credential helper, the two gh login scripts and
# the machine SSH and GnuPG key setup. This module classifies tasks, so it is in the tier.
DESIGN_TIER = (
    "Makefile",  # its require-crit-review recipe carries the gate's REVIEW_TREE checks
    "install/**",
    "home/.chezmoiscripts/**",
    "setup.sh",
    "scripts/lib/github-release.sh",
    "scripts/update-agent-assets.sh",
    "scripts/upgrade-tools.sh",
    "home/dot_agents/agent-config.yaml",
    "scripts/validate-task.py",
    "scripts/require-crit-review.py",
    "scripts/agent-stop-gate.sh",
    "scripts/check-regime-boundary.sh",
    "scripts/lib/high_risk_paths.py",
    "scripts/generate-agent-configs.py",
    "home/dot_local/bin/common/executable_herdr-agents",
    "home/dot_local/bin/common/executable_permgate",
    # The one command the Claude sandbox excludes and the managed settings pre-allow.
    "home/dot_local/bin/common/executable_agmsg-dispatch",
    "home/dot_codex/**",
    ".claude/hooks/**",
    ".claude/contextdb/**",
    ".claude/settings.json",
    "home/dot_claude/hooks/**",
    "home/.chezmoitemplates/claude-settings-managed.json",
    "home/.chezmoitemplates/codex-config-managed.toml",
    "home/dot_claude/modify_private_settings.json",
    "home/dot_agents/permgate-policy.yaml",
    "home/dot_config/git/config.tmpl",
    "home/dot_local/bin/common/executable_setup-gh",
    "scripts/gh-auth.sh",
    "home/dot_local/bin/common/executable_provision-machine-key",
    "home/dot_local/bin/common/executable_setup-gpg",
)

# implementing_tasks decides which tasks a design authorizes, so it is reviewed and hashed too (T124 Amendment 6).
DESIGN_HASH_KEYS = ("invariants", "threat_model", "trust_anchors", "implementing_tasks")


def glob_regex(pattern: str) -> re.Pattern[str]:
    """Compile a path glob: `**/` and `**` cross directories, `*` and `?` stay inside one."""
    out = []
    i = 0
    while i < len(pattern):
        if pattern.startswith("**/", i):
            out.append("(?:.*/)?")
            i += 3
        elif pattern.startswith("**", i):
            out.append(".*")
            i += 2
        elif pattern[i] == "*":
            out.append("[^/]*")
            i += 1
        elif pattern[i] == "?":
            out.append("[^/]")
            i += 1
        else:
            out.append(re.escape(pattern[i]))
            i += 1
    return re.compile("".join(out) + r"\Z")


def in_review_tier(path: str) -> bool:
    """The gate's review requirement for one path (require-crit-review.py high_risk_reason)."""
    if path in HIGH_RISK_FILES or path.startswith(HIGH_RISK_PREFIXES):
        return True
    return any(token in " ".join(path.split("/")).lower().replace("_", "-") for token in HIGH_RISK_TOKENS)


def in_design_tier(path: str) -> bool:
    return any(glob_regex(pattern).match(path) for pattern in DESIGN_TIER)


def _glob_tokens(pattern: str) -> list[str]:
    tokens = []
    i = 0
    while i < len(pattern):
        piece = "**/" if pattern.startswith("**/", i) else "**" if pattern.startswith("**", i) else pattern[i]
        tokens.append(piece)
        i += len(piece)
    return tokens


class _GlobNFA:
    """An NFA over a glob's tokens; a state is (token index, inside the `.*` part of a `**/`)."""

    def __init__(self, pattern: str) -> None:
        self.tokens = _glob_tokens(pattern)

    def closure(self, states: frozenset) -> frozenset:
        out = set(states)
        todo = list(states)
        while todo:
            k, inside = todo.pop()
            if not inside and k < len(self.tokens) and self.tokens[k] in ("*", "**", "**/"):
                if (k + 1, False) not in out:  # each star may match nothing
                    out.add((k + 1, False))
                    todo.append((k + 1, False))
        return frozenset(out)

    def step(self, states: frozenset, ch: str) -> frozenset:
        out = set()
        for k, inside in states:
            piece = self.tokens[k] if k < len(self.tokens) else None
            if piece == "**/":  # `(?:.*/)?`: any characters, closed by a `/`
                out.add((k, True))
                if ch == "/":
                    out.add((k + 1, False))
            elif inside:
                continue
            elif piece == "**" or (piece == "*" and ch != "/"):
                out.add((k, False))
            elif (piece == "?" and ch != "/") or piece == ch:
                out.add((k + 1, False))
        return self.closure(frozenset(out))

    def accepts(self, states: frozenset) -> bool:
        return (len(self.tokens), False) in states


def globs_intersect(left: str, right: str) -> bool:
    """Whether some path matches both globs, whether or not it exists (a product of the two NFAs)."""
    a, b = _GlobNFA(left), _GlobNFA(right)
    # Every character the globs name, `/`, and one stand-in for any other character.
    alphabet = {ch for ch in left + right if ch not in "*?"} | {"/", "\0"}
    start = (a.closure(frozenset({(0, False)})), b.closure(frozenset({(0, False)})))
    seen, todo = {start}, [start]
    while todo:
        sa, sb = todo.pop()
        if a.accepts(sa) and b.accepts(sb):
            return True
        for ch in alphabet:
            nxt = (a.step(sa, ch), b.step(sb, ch))
            if nxt[0] and nxt[1] and nxt not in seen:
                seen.add(nxt)
                todo.append(nxt)
    return False


def may_touch_design_tier(entry: str) -> bool:
    """Whether a path or glob in a task's allowed files can name a design-tier file, existing or not."""
    return any(globs_intersect(entry, pattern) for pattern in DESIGN_TIER)


class FrontMatterError(ValueError):
    pass


def _scalar(text: str, line: int):
    if text in ("{}", "[]"):
        return {} if text == "{}" else []
    # A flow list of ids or paths reads the same in PyYAML; anything richer must be a block list.
    if re.fullmatch(r"\[\s*[A-Za-z0-9][A-Za-z0-9._/+-]*(?:\s*,\s*[A-Za-z0-9][A-Za-z0-9._/+-]*)*\s*\]", text):
        return [_scalar(item.strip(), line) for item in text[1:-1].split(",")]
    if text[0] == '"':
        try:
            return json.loads(text)
        except ValueError as error:
            raise FrontMatterError(f"line {line}: bad double-quoted string") from error
    if text[0] == "'":
        if len(text) < 2 or text[-1] != "'" or "'" in text[1:-1].replace("''", ""):
            raise FrontMatterError(f"line {line}: bad single-quoted string (double an inner quote)")
        return text[1:-1].replace("''", "'")
    # Anything YAML would read as another type, a flow collection, an alias or a comment is refused.
    if text[0] in "[{&*!|>%@`" or ": " in text or " #" in text or text.endswith(":"):
        raise FrontMatterError(f"line {line}: unsupported YAML in {text!r} (quote it)")
    # Plain scalars PyYAML reads as dates, YAML 1.1 booleans or floats must be quoted, so both parsers agree.
    if re.fullmatch(
        r"(?i:yes|no|on|off|y|n|true|false|null)|[0-9]{4}-[0-9]{2}-[0-9]{2}.*|[-+]?(?:[0-9][0-9_]*)?\.[0-9_]*(?:e[-+]?[0-9]+)?|[-+]?\.(?:inf|nan)|0[xo0-7].*",
        text,
    ) and text not in ("true", "false", "null"):
        raise FrontMatterError(f"line {line}: ambiguous plain scalar {text!r} (quote it)")
    if text in ("true", "false"):
        return text == "true"
    if text in ("null", "~"):
        return None
    if re.fullmatch(r"-?[0-9]+", text):
        return int(text)
    return text


def _block(lines: list[tuple[int, int, str]], start: int, indent: int):
    """Parse the block at `indent` from lines[start]; return (value, next index)."""
    first = lines[start][2]
    if first == "-" or first.startswith("- "):
        items = []
        i = start
        while i < len(lines) and lines[i][1] == indent and (lines[i][2] == "-" or lines[i][2].startswith("- ")):
            item = lines[i][2][2:].strip()
            if not item:
                raise FrontMatterError(f"line {lines[i][0]}: nested lists are not supported")
            items.append(_scalar(item, lines[i][0]))
            i += 1
        return items, i
    mapping = {}
    i = start
    while i < len(lines) and lines[i][1] == indent:
        number, _, text = lines[i]
        match = re.fullmatch(r"([A-Za-z0-9_.-]+):(?: (.*))?", text)
        if not match:
            raise FrontMatterError(f"line {number}: expected `key: value`, got {text!r}")
        key, value = match.group(1), (match.group(2) or "").strip()
        if key in mapping:
            raise FrontMatterError(f"line {number}: duplicate key {key!r}")
        i += 1
        if value:
            mapping[key] = _scalar(value, number)
        elif i < len(lines) and lines[i][1] > indent:
            mapping[key], i = _block(lines, i, lines[i][1])
        else:
            mapping[key] = None
    if i < len(lines) and lines[i][1] > indent:
        raise FrontMatterError(f"line {lines[i][0]}: unexpected indentation")
    return mapping, i


def parse_front_matter(text: str) -> dict | None:
    """Return the front matter between the leading `---` lines, or None when the file has none.

    It reads the YAML subset task files use (nested mappings, lists of scalars, plain and
    quoted scalars) and raises FrontMatterError on anything else, so it never guesses.
    """
    source = text.splitlines()
    if not source or source[0].rstrip() != "---":
        return None
    try:
        end = next(n for n in range(1, len(source)) if source[n].rstrip() == "---")
    except StopIteration:
        raise FrontMatterError("front matter has no closing `---`") from None
    lines = []
    for number in range(1, end):
        raw = source[number].rstrip()
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if "\t" in raw[: len(raw) - len(raw.lstrip())]:
            raise FrontMatterError(f"line {number + 1}: tab indentation")
        lines.append((number + 1, len(raw) - len(raw.lstrip(" ")), raw.strip()))
    if not lines:
        return {}
    if lines[0][1] != 0:
        raise FrontMatterError(f"line {lines[0][0]}: the front matter must start at column 0")
    data, i = _block(lines, 0, 0)
    if i != len(lines) or not isinstance(data, dict):
        raise FrontMatterError(f"line {lines[min(i, len(lines) - 1)][0]}: the front matter must be one mapping")
    return data


def canonical_design_hash(design: dict) -> str:
    """sha256 of the design task's invariants, threat_model, trust_anchors and implementing_tasks, key order and layout ignored."""
    missing = [key for key in DESIGN_HASH_KEYS if key not in design]
    if missing:
        raise KeyError(", ".join(missing))
    payload = json.dumps(
        {key: design[key] for key in DESIGN_HASH_KEYS}, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()
