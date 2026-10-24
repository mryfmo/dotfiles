#!/usr/bin/env python3
"""One fake for `gh` and `git` in the worktree-gc tests; the test symlinks it under both names.

Every call appends its argv as one JSON line to `$FAKE_CALLS/<tool>`. `git` then runs the real git at `$FAKE_REAL_GIT`,
so the scratch repository is real and the log shows every git argv the lever used. `gh` answers only
`pr list --state merged --json number,headRefOid` with `--head <branch>` or `--search <sha>`, from `$FAKE_GH_MERGED`,
a comma-separated list of `<number>:<branch>:<headRefOid>` (an empty branch for a pull request matched by sha only);
`FAKE_GH_FAIL=1` makes it fail as gh does without a network.
"""

import json
import os
import sys

tool = os.path.basename(sys.argv[0])
argv = sys.argv[1:]
with open(os.path.join(os.environ["FAKE_CALLS"], tool), "a", encoding="utf-8") as calls:
    calls.write(json.dumps(argv) + "\n")

if tool == "git":
    os.execv(os.environ["FAKE_REAL_GIT"], ["git", *argv])
if os.environ.get("FAKE_GH_FAIL"):
    print("error connecting to api.github.com", file=sys.stderr)
    sys.exit(1)
if argv[:3] != ["pr", "list", "--state"] or argv[3:6] != ["merged", "--json", "number,headRefOid"]:
    sys.exit(f"fake-gh: unsupported command {argv}")
selector, value = argv[6], argv[7]
rows = [entry.split(":") for entry in os.environ.get("FAKE_GH_MERGED", "").split(",") if entry]
matched = [
    {"number": int(number), "headRefOid": oid}
    for number, branch, oid in rows
    if (selector == "--head" and branch == value) or (selector == "--search" and oid.startswith(value))
]
print(json.dumps(matched))
