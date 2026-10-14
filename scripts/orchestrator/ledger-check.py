"""Read-only: the acceptance record has a ledger row for each Bot finding of the sweep and each audit finding.

`ledger-check.py <record.md> <sweep.json> <audit .last.md>...` (plan 007 T704; orch-audit.sh runs it on every audit):
a row is a record line `<id><TAB><class>`, the id a Bot review comment id of the sweep or `audit:<sha7>:<n>` for the
n-th `[P0]` to `[P3]` line of an audit named `*-audit-<sha7>.md*`. Prints `ledger rows <n>; findings <n>; gaps <n>`
and one `GAP <id>` line per missing row; exit 1 when a row is missing.
"""

import json
import re
import sys
from pathlib import Path


def main(record, sweep, *audits):
    rows = dict(re.findall(r"^((?:\d{6,}|audit:[0-9a-f]{7}:\d+))\t(\S+)$", Path(record).read_text(), re.MULTILINE))
    # Bot replies are rare, so a Bot-authored review comment stands for a top-level finding.
    need = [
        item["url"].rsplit("discussion_r", 1)[-1]
        for item in json.loads(Path(sweep).read_text())["items"]
        if item["source"] == "review_comment" and item.get("bot") and "discussion_r" in (item.get("url") or "")
    ]
    for path in audits:
        sha7 = re.search(r"-audit-([0-9a-f]{7})\.md", path).group(1)
        count = len(re.findall(r"^\[P[0-3]\]", Path(path).read_text(), re.MULTILINE))
        need += [f"audit:{sha7}:{n}" for n in range(1, count + 1)]
    gaps = [key for key in need if key not in rows]
    print(f"ledger rows {len(rows)}; findings {len(need)}; gaps {len(gaps)}", *(f"GAP {g}" for g in gaps), sep="\n")
    return 1 if gaps else 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
