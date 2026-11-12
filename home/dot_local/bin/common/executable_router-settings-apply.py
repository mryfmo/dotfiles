#!/usr/bin/env -S python3 -I
"""Make the dsh-superagent Router's settings store equal to the kit's GitHub Source row: the repository, the accept
mode, the observe admission cell and the allowed-sender list (regime-cutover U353, M-26 stage B; U416; U465).

This file is the Python body of `router-settings-apply` and is run by that bash entry alone (regime-cutover U465d, the
mechanism-change row of 2026-11-11T11:54:59Z, form remove: three rounds re-implemented in Python a rule the kit holds in
one place, and each copy diverged from it, verdicts/U465-e6a9a84f.md P1 `:400` and `:457`). The entry owns the
environment: it sources the pinned `regime-env` (the slug, the hcom store's origin binding, the store root held
component by component), resolves the program store by `store_resolve` (the shell levers' one rule: the derived store
when it exists, else the checkout's `.orchestration/orchestrate/<program>`, a linked worktree refused), names the
Source rendering beside the manifest, checks this file's pin, and runs
`python3 -I router-settings-apply.py --store <store> --source <router-source.json> [--profile <cordis.patch.yml>]
[--wait <seconds>] [--dry-run]`. This body resolves nothing: `--store` and `--source` are required, and each is held
by ledger-row.py's path rule before anything else (a clean absolute path, every component `os.lstat`ed and no link, a
link refused naming the component; the store a directory of this user, the rendering a regular file of this user).

The Router learns its Sources from the settings store under `stateDir`, never from the plugin config (upstream
`src/deployment.ts:33-44` refuses `repository` there, naming the Source as where it moved), so the values the kit
renders as comments in `home/dot_dsh/profiles/router/cordis.patch.yml` reach the Router through this lever alone:

- The Source row (the manifest's `assets.dsh-superagent.sources.github`) reaches this body as the generator's
  rendering of it, `router-source.json` beside the manifest (`~/.agents/router-source.json` for the installed copy,
  the checkout's `home/dot_agents/router-source.json` for the checkout's; U465c): one JSON object holding
  `generated_by` and `source`, the row complete (U465d: the generator applies the defaults once, so every field is
  present): `repository` (`owner/name`), `accept_mode`, `accept_mode_row`, `accept_mode_auto_row` (a timestamp or
  null), `observe_admission` (`inferred` or `ignore`) and `allowed`. This body reads no YAML: the generator (PyYAML)
  is the kit's one reader of the manifest, `make render-check` holds the rendering to the manifest, the output index
  pins the deployed copy's sha256 for the doctor, and the JSON is read with a pairs hook that refuses a key named
  twice at any depth (verdict U465-db9a5e94 P1 `:407`). A rendering that is absent, not JSON, not that object, or
  whose row misses a key, names an unknown key or a value of the wrong type is a refusal naming the file, never a
  fallback to the manifest (standing order 21). The rendered router profile's `webserver` row gives the port (its
  host must be `127.0.0.1`, the only host this lever ever connects to). The Source's `cli` is the physical path of
  `router-gh` beside this file, the `gh` wrapper whose `GH_CONFIG_DIR` is `<DSH_HOME>/router-credentials/gh` (upstream
  docs/006-deployment.md "Agent GitHub account").
- `GET settings` at `http://127.0.0.1:<port>/orchestrator/api/settings` with the `x-orchestrator-request: 1` header
  (upstream `src/app/http.ts:75-78`: the host `127.0.0.1:<port>` and that header, else 403) gives each block's current
  `value` and `revision`. For a block whose value differs from the kit's, `PUT settings/<block>` carries
  `{"value": <the whole block>, "revision": <the revision read>}` (upstream `src/app/http.ts:196-202`, `src/app/settings.ts:148-151`:
  a stale revision is 409). The three blocks, `source:github` saved last and `eval` and `policy` in the order the
  direction of the mode change fixes (below):
  - `source:github`: `{"enabled": true, "config": {<the current config>, "repository": <repository>, "cli": <router-gh>,
    "observePulls": true}}` (`src/sources/github.ts:25-28`, the Source's config keys). `observePulls` is the observe
    path: the notifications poll (`src/sources/github.ts:304`, `notifications?all=true`) needs a classic token with the
    `notifications` scope, which the M-25 handout's fine-grained token does not carry, while the repository stream
    (`src/sources/github.ts:174`, `issues?state=all`, read when `observeIssues || observePulls`) receives every new pull
    request with the token's `Pull requests` permission and runs whether or not the notifications poll fails (`:282-286`).
  - `eval`: the current eval block with `mode` set to the accept mode (`src/policy.ts:83-87`): `off`, `observe`, or
    `auto` by a two-key proof (U465, U465b, U465c): the row carries `accept_mode_auto_row` (a decisions.tsv timestamp,
    the M-18 ladder's second row, distinct from `accept_mode_row`), and the given store's `decisions.tsv` holds
    exactly one row with that `ts` whose grammar is the auto row's and no other's: phase `M-18` and a decision that
    begins with the fixed marker `accept rung auto for <repository>` (the row's repository), alone or continued after a
    separator (verdict U465-db9a5e94 P1 `:517`: the first rung's row mentions `auto`, so a word test admitted it once
    `accept_mode_row` was rewritten). The decisions file must be a regular file of this user under the given store
    (the ledger-row.py form). The store is read for an `auto` row alone. `auto` without the manifest row, a row that
    is no timestamp, the row beside another mode, the row equal to `accept_mode_row`, a row the store does not hold
    (a fabricated timestamp), two rows, a row of another phase or whose decision does not begin with the marker, and a
    store that cannot be read (standing order 21) are each a refusal naming the row and the file: the rung is admitted
    by the operator's dated row and by nothing else.
  - `policy`: the current block with the github Source's admission cell `sources.github.admission.pulls.unlistedUnaddressed`
    set to the row's `observe_admission` (`src/policy.ts:76-84`, `src/admission.ts:13`) and its `allowed` list set
    to the row's `allowed` ids as `{"id": <login>}` rows (`src/sources/github.ts:72`: an id is `[A-Za-z0-9-]+`;
    U465), its `rules` and every other row, cell and Source carried as read. Without the cell the observe rung records
    nothing: upstream's default for the cell is `ignore`, so every unlisted human's pull request falls to
    `not_a_member` before any assessment (`src/policy.ts:192-210`; measured on the i2 probes, decisions
    2026-11-10T04:08:19Z), while `inferred` makes it a candidate that observe mode can only record as an ignore
    Decision with `audit.would_accept` (`src/policy.ts:55-57`), never accept. The allowed list is the Source's
    identity set (a listed login's mention is `explicit`, accepted in every mode; an unlisted login's message is
    refused `not_a_member`), so it is a function of the mode (U465b): the row's ids in `auto`, `[]` in `off` and
    `observe` whatever the row says (the asset validator refuses a listed login beside those modes, so the manifest
    cannot carry a dormant grant); the kit's row replaces the store's list, never merges with it, so no entry the
    panel made survives a run (R-45: the Router is granted nothing beyond the kit's rows). The committed list is
    [mryfmo] since the decisions row of 2026-11-12T00:08:25Z (U469).
- A block already equal to the kit's is not written: a second run PUTs nothing (`unchanged`). After a save the Router
  answers `restarting: true` while setup is pending or a setup field changed (`src/app/settings.ts:176`), and the API is
  unavailable for a moment; when another save follows the one that reported it, this lever polls `GET settings` until
  the Router answers again, for at most `--wait` seconds (default 60), and reads every block's revision afresh.
- The order of the `eval` and `policy` saves follows the direction of the mode change (regime-cutover U469c, verdict
  U469-25a395ab P1 `:1492`), so at every point between PUTs the store is at least as restrictive as it was before the
  run or will be after it. Toward `auto` (the row's mode is `auto` and the store's is not) `policy` is saved first and
  `eval` after it: a failed policy PUT (a 409, a 403, an unreachable port) leaves the store at its safe mode beside the
  policy it had, never at `auto` beside a policy whose admission cell or empty list sends an unlisted sender's pull
  request to assessment, where a rule match is an accept. Away from `auto`, and whenever the store already holds the
  row's mode, `eval` is saved first, so the store never polls under `auto` beside a widened policy. `save_order` holds
  the rule once and main() iterates the order it returns. A policy save changes `policyVersion` and restarts nothing
  (measured 2026-11-10T03:03Z, `restarting: false`), so no wait precedes the save after it.
- `source:github` is saved last in both directions (regime-cutover U353b, verdict U353-8791100f P2 `:401`): a store
  whose mode is `auto` would otherwise poll under `auto` from the Source's restart until the mode and the policy are
  written, so both are in place before the Source is enabled or its setup fields change.
- Saving `source:github` runs the Router's account probe first (`src/app/settings.ts:167`, `src/app/setup.ts:61-66`,
  `src/deployment.ts:87-105`: `<cli> api user`, then `repos/<name>` for push); without the agent account's login in the
  credential root the Router answers 400 with `setup.code` `agentCliSignedOut` and saves nothing. This lever names that
  refusal, with `eval` and `policy` already saved, and exits 2: the token is the operator's step
  (docs/engagement-handout.md), after which the coordinator runs the entry again.

Output: one line per block on stdout, `<block> saved (revision <n>[, restarting])` or `<block> unchanged (revision <n>)`.
Exit 0 when the three blocks hold the kit's values. With `--dry-run` the two given paths, the rendering, the profile
and the wrapper are held to their forms as in a run, the inputs and the values a run would write are printed (`store
<path>`, `source <path>`, `eval.mode <mode>`, `allowed <JSON list of ids>`, `admission.pulls.unlistedUnaddressed
<cell>`, `repository <owner/name>`, `cli <path>`) and the Management API is not called: nothing is read from it or
written to it. Every refusal is one line on stderr, `router-settings-apply: <reason>`, and exit 2: a store or a
rendering path that is not clean and absolute, reached through a link, or not a directory (a regular file) of this
user, a rendering or profile that cannot be read or lacks its row, a rendering naming a key twice or outside the
generator's form, `auto` without its dated row or with a row the store's decisions.tsv does not hold as described
above, a store whose decisions file cannot be read, an `observe_admission` outside its two words, an `allowed` that
is no list of ids, a sender id outside its grammar or repeated, a wrapper that is no executable file, a port that
answers nothing (`unreachable`, naming `127.0.0.1:<port>`), a 403 (naming the header), a 409 (naming the revision), a
400 with `setup` (naming the code and its text), a 3xx (naming its Location; never followed), any other status, or a
settings view without the `github` Source, the `eval` block or the `policy` block. The option grammar is exact names,
each at most once (U465e, verdict U465-9c0244e0 P1 `:126`: argparse expanded `--sto` and let a caller's value after
the entry's two win): a call without `--store` or `--source`, with an abbreviated option, or with `--store` or
`--source` given twice is argparse's refusal naming the option (exit 2, the usage on stderr). Nothing is written to
any file; the only network peer is `127.0.0.1:<port>`: the opener is built by hand (U353b, verdict P2 `:268`) with an
empty proxy table, so a proxy named in the environment or the system settings is not consulted, and without a
redirect handler, so a 3xx is a refusal and no request leaves the loopback port.

Before anything else the file hashes itself against its `claude.levers.sha256.router-settings-apply.py` pin in the
manifest beside it (the deployed `~/.agents/agent-config.yaml` for the copy under the physical `~/.local/bin/common`,
else the checkout's `home/dot_agents/agent-config.yaml` two levels up) and refuses to run (exit 2, nothing on stdout)
when the digest differs, in brief-check.py's form: the pin block is the one part of the manifest this body reads, by
that reader; the entry checks the same pin before it runs this file (the acp-broker and acp-relay.py pair's shape).
Standing order 21: every producer's status is read; a read that fails is a refusal, never a pass.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import sys
import time
import urllib.error
import urllib.request

LEVER = "router-settings-apply"
LEVER_SCRIPT = "router-settings-apply.py"
WRAPPER = "router-gh"
HOST = "127.0.0.1"
HEADER = "x-orchestrator-request"
API = "/orchestrator/api/"
SOURCE_BLOCK = "source:github"
EVAL_BLOCK = "eval"
ACCEPT_MODES_APPLIED = ("off", "observe", "auto")
# The M-18 ladder's row timestamps (decisions.tsv `ts`): `auto` is admitted by `accept_mode_auto_row` alone (U465).
LADDER_ROW = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
# A sender id of the github Source's allowed list, a GitHub login (src/sources/github.ts:72; U465).
SENDER_ID = re.compile(r"^[A-Za-z0-9-]+$")
POLICY_BLOCK = "policy"
# The one policy cell this lever writes (U416): the pulls row's unlistedUnaddressed cell of the github Source's admission
# table (src/admission.ts), from the row's observe_admission, whose two words are the cell's values short of explicit.
ADMISSION_SOURCE = "github"
ADMISSION_ROW = "pulls"
ADMISSION_CELL = "unlistedUnaddressed"
OBSERVE_ADMISSIONS_APPLIED = ("inferred", "ignore")
# The generator's rendering of the Source row (U465c): `router-source.json` beside the manifest, an object of exactly
# these two keys whose `source` is the row with every one of its keys (U465d: the generator applies the defaults, so a
# rendering missing a key is not its rendering).
SOURCE_LABEL = "assets.dsh-superagent.sources.github"
RENDERING_KEYS = ("generated_by", "source")
SOURCE_ROW_KEYS = (
    "repository",
    "accept_mode",
    "accept_mode_row",
    "accept_mode_auto_row",
    "observe_admission",
    "allowed",
)
# The auto admission's second key (U465b, U465c): `accept_mode_auto_row` must name a row of the given store's
# decisions.tsv (header `ts phase decision why evidence result`) of the ladder's phase whose decision begins with the
# auto marker for the row's repository; the marker may stand alone or continue after a character outside the
# repository grammar, so `owner/name-fork` is another repository, not this one.
DECISIONS = "decisions.tsv"
DECISIONS_HEADER = ("ts", "phase", "decision")
LADDER_PHASE = "M-18"
AUTO_MARKER = "accept rung auto for {repository}"
REPOSITORY_CHARACTER = re.compile(r"[A-Za-z0-9_.-]")
# The two paths the entry gives, named in the refusals of their holds.
STORE_WHAT = "program store"
SOURCE_WHAT = "rendered Source row"
# The levers block of the manifest, read as text by indentation alone, never parsed as YAML (brief-check.py's reader):
# a mapping key is a bare `<key>:` line; a pin is `<name>: <64 hex>` at the one indentation the first pin fixes.
MAPPING_KEY = re.compile(r"^(\S+):$")
LEVER_PIN = re.compile(r"^(\S+): ([0-9a-f]{64})$")
LEVERS_KEYS = ("claude", "levers", "sha256")
REPOSITORY = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
# The webserver row as scripts/generate-agent-configs.py renders it (DSH_ROUTER_WEBSERVER), host first, then port.
WEBSERVER_ROW = re.compile(r"^- id: webserver\n  config:\n    host: (\S+)\n    port: (\d+)\n", re.MULTILINE)


class Refusal(Exception):
    """One refusal line; main prints it and exits 2."""


def refuse_to_run(reason: str) -> None:
    """The self-check's refusal, in the shell levers' words on stderr: exit 2 and nothing was read or written."""
    print(f"{LEVER_SCRIPT}: refused: {reason}", file=sys.stderr)
    sys.exit(2)


def lever_directory() -> str:
    return os.path.realpath(os.path.dirname(os.path.abspath(__file__)))


def manifest_beside(directory: str) -> str:
    """The manifest the pin comes from: the deployed one for the installed copy, else the checkout's."""
    home = os.environ.get("HOME", "")
    if home and os.path.isdir(home) and directory == os.path.realpath(os.path.join(home, ".local/bin/common")):
        return os.path.join(home, ".agents/agent-config.yaml")
    return os.path.join(directory, "../../home/dot_agents/agent-config.yaml")


def lever_self_check() -> None:
    """Refuse to run unless this file's sha256 equals its pin in the manifest beside it (regime-cutover U31; U317b)."""
    directory = lever_directory()
    self_path = os.path.join(directory, os.path.basename(__file__))
    manifest = manifest_beside(directory)
    if not os.access(manifest, os.R_OK):
        refuse_to_run(f"manifest unreadable: {manifest}")
    try:
        with open(manifest, "rb") as handle:
            lines = handle.read().decode("utf-8", "replace").splitlines()
    except OSError:
        refuse_to_run(f"cannot read {manifest}")
    pins = [digest for name, digest in manifest_levers(lines, manifest) if name == LEVER_SCRIPT]
    if len(pins) != 1:
        refuse_to_run(f"no single sha256 pin for {LEVER_SCRIPT} in {manifest}")
    try:
        with open(self_path, "rb") as handle:
            digest = hashlib.sha256(handle.read()).hexdigest()
    except OSError:
        refuse_to_run(f"cannot hash {self_path}")
    if digest != pins[0]:
        refuse_to_run(f"sha256 {digest} of {self_path} differs from the pin in {manifest}")


def manifest_levers(lines: list[str], manifest: str) -> tuple[tuple[str, str], ...]:
    """The `(name, sha256)` pins under the manifest's `claude.levers.sha256` mapping, in file order (brief-check.py,
    U136): the mapping keys are walked by indentation, so `levers:` counts only under the top-level `claude:` and
    `sha256:` only under that `levers:`; inside the block, blank and comment lines are skipped, the entries share the
    indentation of the first pin, and the list ends at the first line indented less. An entry that is not
    `<name>: <64 hex>` is a refusal naming the line; no entry at all is the missing-block refusal."""
    pins: list[tuple[str, str]] = []
    keys: list[tuple[int, str]] = []  # the open mapping keys as (indentation, key), outermost first
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
                refuse_to_run(f"line {number} of {manifest} is not a `<name>: <sha256>` pin under claude.levers.sha256")
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
        refuse_to_run(f"no claude.levers.sha256 block in {manifest}")
    return tuple(pins)


def held_path(path: str, what: str, leaf: str) -> str:
    """ledger-row.py's path rule applied to a path the entry gives (U465d): a clean absolute path (no `.`, `..`, a
    repeated or a trailing separator), every component from the root down `os.lstat`ed in order, a status that cannot
    be read a refusal naming the component (standing order 21), a symbolic link refused naming the component, a parent
    that is not a directory refused; the leaf a directory (`leaf` "directory") or a regular file (`leaf` "regular
    file") of this user. The entry passes physical paths (`pwd -P` forms), so a link anywhere in the chain means the
    tree changed under the entry and nothing is read through it. Returns the path."""
    if not os.path.isabs(path) or os.path.normpath(path) != path:
        raise Refusal(f"the {what} {path} is not a clean absolute path; the entry passes physical paths")
    parts = path.split(os.sep)[1:]
    current = os.sep
    status = None
    for index, part in enumerate(parts):
        current = os.path.join(current, part)
        try:
            status = os.lstat(current)
        except OSError as error:
            raise Refusal(
                f"{current} could not be examined: {error.strerror}; the {what} {path} is given as a path this lever "
                "can prove, or not at all"
            ) from None
        if stat.S_ISLNK(status.st_mode):
            raise Refusal(
                f"{current} is a symbolic link; the {what} {path} is reached through real directories alone, and "
                "nothing is read through a link"
            )
        if index < len(parts) - 1 and not stat.S_ISDIR(status.st_mode):
            raise Refusal(f"{current} is not a directory; the {what} {path} is reached through real directories alone")
    is_leaf = stat.S_ISDIR if leaf == "directory" else stat.S_ISREG
    if status is None or not is_leaf(status.st_mode) or status.st_uid != os.geteuid():
        raise Refusal(f"{path} is not a {leaf} of this user; the {what} is read only as one")
    return path


def read_lines(path: str, what: str) -> list[str]:
    try:
        with open(path, "rb") as handle:
            return handle.read().decode("utf-8", "replace").splitlines()
    except OSError as error:
        raise Refusal(f"{what} {path} could not be read: {error}") from None


def unique_pairs(path: str):
    """The `object_pairs_hook` of the rendering's reader (U465c): a key named twice in one object is a refusal naming
    it. The generator writes each key once, so such a file is not its rendering; json.loads alone would keep the last
    value, as yaml.safe_load did for the manifest's repeated keys (verdict U465-4ae6f8c0 P1 `:279`)."""

    def hook(pairs: list[tuple[str, object]]) -> dict[str, object]:
        found: dict[str, object] = {}
        for key, value in pairs:
            if key in found:
                raise Refusal(
                    f"the rendered Source row {path} names the key {key!r} twice; the generator writes each key once, "
                    "so this file is not its rendering and is not read"
                )
            found[key] = value
        return found

    return hook


def source_row(path: str, store: str) -> tuple[str, str, str, list[str]]:
    """The rendering's repository, accept mode, observe admission and allowed sender ids, each held to its form: the
    file is one JSON object of `generated_by` and `source`, the row names no key twice, no unknown key and every key
    (the generator applies the defaults, U465d), every cell but `allowed` and `accept_mode_auto_row` is a non-empty
    string; `auto` needs `accept_mode_auto_row` (a decisions.tsv timestamp, the M-18 ladder's second row, distinct
    from `accept_mode_row`), that row belongs to `auto` alone (null otherwise) and must exist in the given store's
    decisions.tsv in the auto row's grammar (ladder_row); a third word for the cell is refused, and `inferred` beside
    `auto` (U469b: the cell is `ignore` there, so an unlisted sender falls to not_a_member before any assessment); the
    allowed list must be a list of GitHub logins, none repeated (by case: GitHub logins differing by case alone are
    one login). The list returned is the row's; policy_allowed decides what the mode lets the policy carry."""
    what = f"the rendered Source row {path}"
    label = SOURCE_LABEL
    text = "\n".join(read_lines(path, "the rendered Source row"))
    try:
        data = json.loads(text, object_pairs_hook=unique_pairs(path))
    except json.JSONDecodeError as error:
        raise Refusal(f"{what} is not JSON: {error}") from None
    if (
        not isinstance(data, dict)
        or tuple(sorted(data)) != tuple(sorted(RENDERING_KEYS))
        or not isinstance(data["generated_by"], str)
    ):
        raise Refusal(f"{what} is not the generator's rendering (an object holding generated_by and source alone)")
    row = data["source"]
    if not isinstance(row, dict):
        raise Refusal(f"{what} holds no {label} object")
    unknown = sorted(set(row) - set(SOURCE_ROW_KEYS))
    if unknown:
        raise Refusal(f"{label} in {path} has unknown key(s) {unknown}; the row admits {list(SOURCE_ROW_KEYS)}")
    for key in SOURCE_ROW_KEYS:
        if key not in row:
            raise Refusal(
                f"{what} names no {label}.{key}; the generator renders every key of the row, so this file is not its "
                "rendering"
            )
    for key, value in row.items():
        if key == "allowed" or (key == "accept_mode_auto_row" and value is None):
            continue
        if not isinstance(value, str) or not value:
            raise Refusal(f"{label}.{key} in {path} is not a non-empty string: {value!r}")
    if not REPOSITORY.fullmatch(row["repository"]):
        raise Refusal(f"{label}.repository {row['repository']!r} in {path} is not owner/name")
    mode = row["accept_mode"]
    if mode not in ACCEPT_MODES_APPLIED:
        raise Refusal(
            f"{label}.accept_mode {mode!r} in {path} is not one of {', '.join(ACCEPT_MODES_APPLIED)} (src/policy.ts:84)"
        )
    if not LADDER_ROW.fullmatch(row["accept_mode_row"]):
        raise Refusal(
            f"{label}.accept_mode_row {row['accept_mode_row']!r} in {path} is not a decisions.tsv timestamp "
            "(YYYY-MM-DDTHH:MM:SSZ)"
        )
    auto_row = row["accept_mode_auto_row"]
    if mode == "auto" and auto_row is None:
        raise Refusal(
            f"{label}.accept_mode 'auto' in {path} needs accept_mode_auto_row (the M-18 ladder's second row "
            "timestamp) beside accept_mode_row; the mode stays observe until that row is written"
        )
    if auto_row is not None and not LADDER_ROW.fullmatch(auto_row):
        raise Refusal(
            f"{label}.accept_mode_auto_row {auto_row!r} in {path} is not a decisions.tsv timestamp (YYYY-MM-DDTHH:MM:SSZ)"
        )
    if auto_row is not None and mode != "auto":
        raise Refusal(f"{label}.accept_mode_auto_row in {path} belongs to accept_mode auto alone, not {mode!r}")
    if auto_row is not None and auto_row == row["accept_mode_row"]:
        raise Refusal(
            f"{label}.accept_mode_auto_row {auto_row!r} in {path} is the accept_mode_row itself; the ladder's second "
            "row is not its first"
        )
    if row["observe_admission"] not in OBSERVE_ADMISSIONS_APPLIED:
        raise Refusal(
            f"{label}.observe_admission {row['observe_admission']!r} in {path} is not "
            f"{' or '.join(OBSERVE_ADMISSIONS_APPLIED)}; the {ADMISSION_ROW} row's {ADMISSION_CELL} cell takes those two "
            "words alone (explicit would accept an unlisted sender's pull request in observe mode)"
        )
    if mode == "auto" and row["observe_admission"] == "inferred":
        # U469b (verdict U469-02ea959b P1): the generator's rule in its words; inferred lets an unlisted sender's pull
        # request reach assessment, where a rule match is an accept under auto.
        raise Refusal(
            f"{label}.observe_admission 'inferred' in {path} belongs to accept_mode observe alone; under auto the cell "
            "is 'ignore' so an unlisted sender falls to not_a_member"
        )
    allowed = row["allowed"]
    if not isinstance(allowed, list) or not all(isinstance(sender, str) for sender in allowed):
        raise Refusal(f"{label}.allowed in {path} is not a list of sender ids: {allowed!r}")
    seen: set[str] = set()
    for sender in allowed:
        if not SENDER_ID.fullmatch(sender):
            raise Refusal(
                f"{label}.allowed in {path} names {sender!r}, which is not a sender id of the form [A-Za-z0-9-]+"
            )
        if sender.lower() in seen:
            raise Refusal(
                f"{label}.allowed in {path} repeats {sender!r} (GitHub logins that differ by case alone are one login)"
            )
        seen.add(sender.lower())
    if auto_row is not None:
        ladder_row(auto_row, row["repository"], path, label, store)
    return row["repository"], mode, row["observe_admission"], allowed


def policy_allowed(mode: str, allowed: list[str]) -> list[str]:
    """The ids written into policy.sources.github.allowed, a function of the mode (U465b, verdict U465-4ae6f8c0 P1
    `:516`): the row's list in `auto`, empty in `off` and `observe`, since a listed login's mention is `explicit`
    and accepted in every mode (src/policy.ts), so a list beside observe would open an accept path without the auto
    row."""
    return list(allowed) if mode == "auto" else []


def begins_with_marker(decision: str, marker: str) -> bool:
    """The auto row's decision grammar (U465c): the marker, alone or continued after a character outside the repository
    grammar (a colon, a space), so a marker continued into a longer repository name is not this repository's."""
    if not decision.startswith(marker):
        return False
    rest = decision[len(marker) :]
    return not rest or REPOSITORY_CHARACTER.match(rest) is None


def ladder_row(ts: str, repository: str, source: str, label: str, store: str) -> None:
    """The auto admission's second key (U465b, verdict U465-4ae6f8c0 P1 `:319`; U465c, verdict U465-db9a5e94 P1
    `:517`): the rendering's `accept_mode_auto_row` names a row the operator wrote in the given store's decisions.tsv,
    so the file is read whole and `auto` is admitted only when exactly one row's `ts` cell is the rendering's, its
    phase is the ladder's and its decision begins with the auto marker for the row's repository; the file is held as a
    regular file of this user (no link) before it is read, and a file that cannot be read or does not start with the
    decisions header is a refusal (standing order 21), never a pass. Rows are the file's lines split on tabs, as the
    store's tables are written. The store is the entry's (U465d): this body derives nothing from it."""
    path = os.path.join(store, DECISIONS)
    key = f"{label}.accept_mode_auto_row {ts!r} in {source}"
    marker = AUTO_MARKER.format(repository=repository)
    proof = (
        f"auto is admitted by one dated row the operator wrote there (phase {LADDER_PHASE}, its decision beginning "
        f"{marker!r}) and by nothing else"
    )
    try:
        status = os.lstat(path)
    except OSError as error:
        raise Refusal(f"{key} cannot be proven: {path} could not be read: {error}") from None
    if stat.S_ISLNK(status.st_mode):
        raise Refusal(
            f"{path} is a symbolic link; the decisions file is a regular file of this user under the store, and nothing "
            "is read through a link"
        )
    if not stat.S_ISREG(status.st_mode) or status.st_uid != os.geteuid():
        raise Refusal(f"{path} is not a regular file of this user, so no row of it proves {key}")
    try:
        with open(path, "rb") as handle:
            lines = handle.read().decode("utf-8", "replace").splitlines()
    except OSError as error:
        raise Refusal(f"{key} cannot be proven: {path} could not be read: {error}") from None
    rows = [line.split("\t") for line in lines if line]
    if not rows or tuple(rows[0][: len(DECISIONS_HEADER)]) != DECISIONS_HEADER:
        raise Refusal(
            f"{path} does not start with the decisions header ({', '.join(DECISIONS_HEADER)}, ...), so no row of it "
            f"proves {key}"
        )
    found = [cells for cells in rows[1:] if cells[0] == ts]
    if len(found) != 1:
        count = "no row" if not found else f"{len(found)} rows"
        raise Refusal(f"{key} names {count} of {path}; {proof}")
    cells = found[0] + ["", ""]  # a short row has an empty phase and decision, each refused below
    if cells[1] != LADDER_PHASE:
        raise Refusal(f"the row {ts} of {path} is of phase {cells[1]!r}, not {LADDER_PHASE}; {proof}")
    if not begins_with_marker(cells[2], marker):
        raise Refusal(f"the row {ts} of {path} does not begin its decision with {marker!r}; {proof}")


def webserver_port(profile: str) -> int:
    """The rendered router profile's webserver port; its host must be the loopback address this lever connects to."""
    text = "\n".join(read_lines(profile, "the router profile")) + "\n"
    match = WEBSERVER_ROW.search(text)
    if match is None:
        raise Refusal(f"the router profile {profile} names no webserver host and port in the rendered form")
    if match.group(1) != HOST:
        raise Refusal(f"the router profile {profile} binds the webserver to {match.group(1)}, not {HOST}")
    port = int(match.group(2))
    if not 1 <= port <= 65535:
        raise Refusal(f"the router profile {profile} names the webserver port {port}, outside 1 to 65535")
    return port


def wrapper_path(directory: str) -> str:
    """The physical path of router-gh beside this file, an executable regular file."""
    path = os.path.join(directory, WRAPPER)
    if os.path.islink(path) or not os.path.isfile(path) or not os.access(path, os.X_OK):
        raise Refusal(f"the gh wrapper {path} is not an executable file beside this lever")
    return path


def loopback_opener() -> urllib.request.OpenerDirector:
    """An opener that speaks to the loopback port alone (regime-cutover U353b): urllib's default opener honours the
    environment's and the system's proxy settings for a loopback host too and follows a redirect wherever it points,
    so it is built by hand here: an empty proxy table, the http handler, and the error processor that turns every
    status outside 2xx into an HTTPError (a 3xx included, no redirect handler being present); no https, file or ftp
    handler, so nothing but `http://127.0.0.1:<port>` can be opened through it."""
    opener = urllib.request.OpenerDirector()
    for handler in (
        urllib.request.ProxyHandler({}),
        urllib.request.HTTPHandler(),
        urllib.request.HTTPDefaultErrorHandler(),
        urllib.request.HTTPErrorProcessor(),
    ):
        opener.add_handler(handler)
    return opener


class Api:
    """The Management API at one loopback port: GET and PUT with the header, each answer read whole as JSON."""

    def __init__(self, port: int, wait: float) -> None:
        self.port = port
        self.wait = wait
        self.base = f"http://{HOST}:{port}{API}"
        self.opener = loopback_opener()

    def where(self) -> str:
        return f"the Management API at {HOST}:{self.port}"

    def request(self, method: str, route: str, body: dict | None = None) -> dict:
        data = None if body is None else json.dumps(body).encode()
        headers = {HEADER: "1"}
        if data is not None:
            headers["content-type"] = "application/json"
        request = urllib.request.Request(self.base + route, data=data, method=method, headers=headers)
        label = f"{method} {route}"
        try:
            with self.opener.open(request, timeout=30) as response:  # the loopback host alone, no proxy, no redirect
                text = response.read().decode("utf-8", "replace")
                status = response.status
        except urllib.error.HTTPError as error:
            text = error.read().decode("utf-8", "replace")
            raise Refusal(self.describe(label, error.code, text, error.headers.get("location"))) from None
        except (urllib.error.URLError, OSError) as error:
            reason = getattr(error, "reason", error)
            raise Refusal(f"{self.where()} is unreachable for {label}: {reason}") from None
        try:
            answer = json.loads(text)
        except json.JSONDecodeError as error:
            raise Refusal(f"{self.where()} answered {status} to {label} with no JSON object: {error}") from None
        if not isinstance(answer, dict):
            raise Refusal(f"{self.where()} answered {status} to {label} with no JSON object")
        return answer

    def describe(self, label: str, code: int, text: str, location: str | None = None) -> str:
        """One refusal for a status outside 2xx: the 403 names the header, the 409 the revision, the 400 its setup code,
        a 3xx its Location (never followed: the lever speaks to the loopback port alone)."""
        try:
            answer = json.loads(text)
        except json.JSONDecodeError:
            answer = {}
        error = answer.get("error", text.strip()) if isinstance(answer, dict) else text.strip()
        if 300 <= code < 400:
            return (
                f"{self.where()} answered {code} to {label}: a redirect to {location or 'no Location'} is not followed; "
                f"this lever speaks to {HOST}:{self.port} alone"
            )
        if code == 403:
            return f"{self.where()} answered 403 to {label}: the {HEADER} header or the Host was not accepted ({error})"
        if code == 409:
            return f"{self.where()} answered 409 to {label}: the revision read was stale ({error})"
        setup = answer.get("setup") if isinstance(answer, dict) else None
        if code == 400 and isinstance(setup, dict):
            return (
                f"{self.where()} answered 400 to {label}: setup {setup.get('code')}: {setup.get('detail', error)}; the "
                f"agent account's gh login under the credential root {WRAPPER} names is the operator's step "
                "(docs/engagement-handout.md), after which this lever runs again"
            )
        return f"{self.where()} answered {code} to {label}: {error}"

    def settings(self) -> dict:
        return self.request("GET", "settings")

    def settings_after_restart(self) -> None:
        """Poll GET settings until the restarted Router answers, for at most `wait` seconds; a 403 refuses at once."""
        deadline = time.monotonic() + self.wait
        while True:
            try:
                self.settings()
                return
            except Refusal as refusal:
                if "unreachable" not in str(refusal) and " answered 5" not in str(refusal):
                    raise
                if time.monotonic() >= deadline:
                    raise Refusal(
                        f"{self.where()} did not answer within {self.wait:g} s after its restart: {refusal}"
                    ) from None
                time.sleep(1)


def block_views(settings: dict, where: str) -> dict[str, tuple[dict, int]]:
    """The github Source's, the eval block's and the policy block's (value, revision) from a settings view, keyed by
    block name, each refused when absent."""
    sources = settings.get("sources")
    github = (
        next((s for s in sources if isinstance(s, dict) and s.get("id") == "github"), None)
        if isinstance(sources, list)
        else None
    )
    if github is None or not isinstance(github.get("value"), dict) or not isinstance(github.get("revision"), int):
        raise Refusal(f"{where} answered GET settings without the Source github (its value and revision)")
    blocks = settings.get("blocks")
    views: dict[str, tuple[dict, int]] = {SOURCE_BLOCK: (github["value"], github["revision"])}
    for name in (EVAL_BLOCK, POLICY_BLOCK):
        block = blocks.get(name) if isinstance(blocks, dict) else None
        if (
            not isinstance(block, dict)
            or not isinstance(block.get("value"), dict)
            or not isinstance(block.get("revision"), int)
        ):
            raise Refusal(f"{where} answered GET settings without the {name} block (its value and revision)")
        views[name] = (block["value"], block["revision"])
    return views


def save_order(current_mode: object, requested_mode: str) -> tuple[str, str, str]:
    """The order of the three saves, from the direction of the mode change (U469c, verdict U469-25a395ab P1): toward
    `auto` (the row asks `auto` and the store holds another mode) the policy block (the admission cell and the allowed
    list) is saved before the eval block, so a failed policy PUT leaves the store at its safe mode; away from `auto`,
    and when the store already holds the row's mode, the eval block is saved first (U353b), so the store never polls
    under `auto` beside a widened policy. The Source is last in both: at every point between PUTs the store is at least
    as restrictive as one of the run's two ends."""
    if requested_mode == "auto" and current_mode != "auto":
        return (POLICY_BLOCK, EVAL_BLOCK, SOURCE_BLOCK)
    return (EVAL_BLOCK, POLICY_BLOCK, SOURCE_BLOCK)


def desired_source(current: dict, repository: str, cli: str) -> dict:
    config = current.get("config") if isinstance(current.get("config"), dict) else {}
    return {"enabled": True, "config": {**config, "repository": repository, "cli": cli, "observePulls": True}}


def desired_eval(current: dict, mode: str) -> dict:
    return {**current, "mode": mode}


def desired_policy(current: dict, cell: str, allowed: list[str]) -> dict:
    """The policy block as read with the github Source's `pulls.unlistedUnaddressed` cell set to `cell` and its
    `allowed` list set to the row's ids as `{"id": <login>}` rows (replaced, never merged: the kit's row is the
    Source's one identity set); the rules, the other rows and cells and every other Source's entry unchanged."""
    sources = current.get("sources") if isinstance(current.get("sources"), dict) else {}
    github = sources.get(ADMISSION_SOURCE) if isinstance(sources.get(ADMISSION_SOURCE), dict) else {}
    admission = github.get("admission") if isinstance(github.get("admission"), dict) else {}
    row = admission.get(ADMISSION_ROW) if isinstance(admission.get(ADMISSION_ROW), dict) else {}
    entry = {
        **github,
        "allowed": [{"id": sender} for sender in allowed],
        "admission": {**admission, ADMISSION_ROW: {**row, ADMISSION_CELL: cell}},
    }
    return {**current, "rules": current.get("rules", []), "sources": {**sources, ADMISSION_SOURCE: entry}}


def apply_block(api: Api, block: str, current: dict, desired: dict, revision: int) -> bool:
    """PUT `block` when it differs; print the line; True when the Router restarts after the save."""
    if json.dumps(current, sort_keys=True) == json.dumps(desired, sort_keys=True):
        print(f"{block} unchanged (revision {revision})")
        return False
    answer = api.request("PUT", f"settings/{block}", {"value": desired, "revision": revision})
    saved = answer.get("revision")
    restarting = answer.get("restarting") is True
    print(f"{block} saved (revision {saved}{', restarting' if restarting else ''})")
    return restarting


class Once(argparse.Action):
    """Store the option's value and refuse its second occurrence by name (U465e): the entry gives `--store` and
    `--source` once each, and argparse's last-wins rule would otherwise let a caller's exact flag after them choose
    the store the body proves or the row it reads."""

    def __call__(self, parser, namespace, values, option_string=None):
        if getattr(namespace, self.dest) is not None:
            parser.error(f"{option_string} is given more than once; the entry gives it once, and a repeat is refused")
        setattr(namespace, self.dest, values)


def main(argv: list[str]) -> int:
    # Exact option names only (U465e): with abbreviations `--sto <dir>` passed the entry's exact-flag refusal and
    # overrode the resolved store.
    parser = argparse.ArgumentParser(
        prog=LEVER_SCRIPT,
        allow_abbrev=False,
        description=(
            "the Python body of router-settings-apply, run by that entry alone: write the kit's GitHub Source row, "
            "accept mode, observe admission cell and allowed-sender list into the Router's settings store"
        ),
    )
    directory = lever_directory()
    parser.add_argument(
        "--store",
        required=True,
        action=Once,
        help="the program store the entry resolved (regime-env and store_resolve), a physical path; read for an auto row alone; once",
    )
    parser.add_argument(
        "--source",
        required=True,
        action=Once,
        help="the generator's rendering of the Source row, router-source.json beside the manifest, a physical path; once",
    )
    parser.add_argument(
        "--profile",
        default=None,
        help="the rendered router cordis.patch.yml (default: $DSH_HOME/profiles/router/cordis.patch.yml, DSH_HOME defaulting to ~/.dsh)",
    )
    parser.add_argument(
        "--wait",
        type=float,
        default=60.0,
        help="seconds to wait for the Router after a save that restarts it (default 60)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="hold the two paths, read the rendering, the profile and the wrapper, print the inputs and the values a run would write, and call the Management API not at all",
    )
    args = parser.parse_args(argv[1:])
    profile = args.profile
    if profile is None:
        dsh_home = os.environ.get("DSH_HOME") or os.path.join(os.environ.get("HOME", ""), ".dsh")
        profile = os.path.join(dsh_home, "profiles/router/cordis.patch.yml")
    try:
        store = held_path(args.store, STORE_WHAT, "directory")
        source = held_path(args.source, SOURCE_WHAT, "regular file")
        repository, mode, cell, allowed = source_row(source, store)
        senders = policy_allowed(mode, allowed)
        port = webserver_port(profile)
        cli = wrapper_path(directory)
        if args.dry_run:
            print(f"dry run: nothing is read from or written to the Management API at {HOST}:{port}")
            print(f"store {store}")
            print(f"source {source}")
            print(f"eval.mode {mode}")
            print(f"allowed {json.dumps(senders)}")
            print(f"admission.{ADMISSION_ROW}.{ADMISSION_CELL} {cell}")
            print(f"repository {repository}")
            print(f"cli {cli}")
            return 0
        api = Api(port, args.wait)
        views = block_views(api.settings(), api.where())
        order = save_order(views[EVAL_BLOCK][0].get("mode"), mode)
        refusals: list[str] = []
        for position, block in enumerate(order):
            current, revision = views[block]
            if block == EVAL_BLOCK:
                desired = desired_eval(current, mode)
            elif block == POLICY_BLOCK:
                desired = desired_policy(current, cell, senders)
            else:
                desired = desired_source(current, repository, cli)
            try:
                restarting = apply_block(api, block, current, desired, revision)
            except Refusal as refusal:
                # The Source's 400 before the token (setup agentCliSignedOut) is named after the saves before it; every
                # other refusal, on any block, ends the run here with nothing written after it.
                if block != SOURCE_BLOCK or " answered 400 " not in str(refusal):
                    raise
                refusals.append(str(refusal))
                break
            # A save that restarts the Router (setup pending, or a setup field changed) is followed by the wait and a
            # fresh read of every revision when another save follows it; after the last save nothing waits.
            if restarting and position + 1 < len(order):
                api.settings_after_restart()
                views = block_views(api.settings(), api.where())
    except Refusal as refusal:
        print(f"{LEVER}: {refusal}", file=sys.stderr)
        return 2
    for refusal in refusals:
        print(f"{LEVER}: {refusal}", file=sys.stderr)
    return 2 if refusals else 0


if __name__ == "__main__":
    lever_self_check()
    sys.exit(main(sys.argv))
