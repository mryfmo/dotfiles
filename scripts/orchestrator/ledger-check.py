"""Read-only: the acceptance record has a ledger row for each Bot finding of the sweep and each audit finding.

`ledger-check.py <record.md> <sweep.json> <audit .last.md>...` (plan 007 T704; orch-audit.sh runs it on every audit):
a row is a record line `<id><TAB><class>`, the id a Codex Bot review comment or badged review of the sweep, or
`audit:<sha7>:<n>` for the n-th `[P0]` to `[P3]` line, bulleted or not, of an audit named `*-audit-<sha7>.md*` (the
sha7 of its first line `inherited-from: <sha7>` when present). Prints `ledger rows <n>; findings <n>; gaps <n>`
and one `GAP <id>` line per missing row; exit 1 when a row is missing.
"""

import json
import re
import sys
from pathlib import Path

BOT, BADGES = "chatgpt-codex-connector[bot]", tuple(f"![P{n} Badge]" for n in range(4))


def main(record, sweep, *audits):
    rows = dict(re.findall(r"^((?:\d{6,}|audit:[0-9a-f]{7}:\d+))\t(\S+)$", Path(record).read_text(), re.MULTILINE))
    # Bot replies are rare, so a Bot-authored review comment stands for a top-level finding.
    need = []
    for item in json.loads(Path(sweep).read_text())["items"]:
        url, body = item.get("url") or "", item.get("body") or ""
        # The Codex Bot only, as the gate's swept_finding_ids() counts: another bot's comment is not a finding.
        if item["source"] == "review_comment" and item.get("author") == BOT and "discussion_r" in url:
            need.append(url.rsplit("discussion_r", 1)[-1])
        elif item["source"] == "review" and item.get("author") == BOT and any(t in body for t in BADGES):
            need.append(url.rpartition("pullrequestreview-")[2])  # a badged review body, as the gate counts it
    for path in audits:
        text = Path(path).read_text()
        # An inherited audit (chain-integrate.sh) keeps the ids of the head it ran on, which its first line names.
        marker = re.match(r"inherited-from: ([0-9a-f]{7})\n", text)
        sha7 = marker.group(1) if marker else re.search(r"-audit-([0-9a-f]{7})\.md", path).group(1)
        count = len(re.findall(r"^\s*(?:[-*+]\s+)?\[P[0-3]\]", text, re.MULTILINE))
        need += [f"audit:{sha7}:{n}" for n in range(1, count + 1)]
    gaps = [key for key in need if key not in rows]
    print(f"ledger rows {len(rows)}; findings {len(need)}; gaps {len(gaps)}", *(f"GAP {g}" for g in gaps), sep="\n")
    return 1 if gaps else 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
