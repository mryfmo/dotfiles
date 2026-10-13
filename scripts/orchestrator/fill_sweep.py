"""fill_sweep.py <sweep.json> <pr-comments.json> [extra.tsv]: fill every sweep item's disposition (plan 007 T718).

A Bot thread takes the disposition of the orchestrator's latest reply in it (`fixed:<sha>` or
`not-applicable:<reason>; evidence=<command>` in backticks); extra.tsv (`id<TAB>disposition`) overrides or
adds; other items get the fixed rules below, each with a jq command that shows the item. A not-applicable
without the gate's grammar (one `; evidence=` between a non-empty reason and command) is never emitted but
listed as a gap. The sweep JSON is rewritten only when every item has a disposition; otherwise exit 1.
"""

import collections
import json
import re
import sys
from pathlib import Path

REPLY = re.compile(r"`((?:fixed:[0-9a-f]{7,40})|(?:not-applicable:[^`]+))`")
EVIDENCE = "; evidence="
RULES = {
    "own_reply": "the orchestrator disposition reply on a Bot thread, not a finding",
    "review": "review object without a finding",
    "codex_review": "review object; its findings are the inline threads, each dispositioned on its own",
    "issue_comment": "bot summary or onboarding comment, no finding",
    "annotation": "runner capacity notice, no finding",
    "status": "CI status, no finding",
}


def valid(disposition):
    """The gate's grammar: `fixed:<commit>`, or `not-applicable:<reason>; evidence=<command>` with one delimiter."""
    if re.fullmatch(r"fixed:[0-9a-f]{7,40}", disposition):
        return True
    body = disposition.removeprefix("not-applicable:")
    reason, _, command = body.partition(EVIDENCE)
    return body != disposition and body.count(EVIDENCE) == 1 and bool(reason.strip() and command.strip())


def main(argv):
    if len(argv) not in (2, 3):
        sys.exit(__doc__.splitlines()[0])
    sweep_path = argv[0]
    lines = Path(argv[2]).read_text().splitlines() if len(argv) == 3 else []
    extra = dict(line.split("\t")[:2] for line in lines if line.strip() and not line.startswith("#"))
    sweep = json.loads(Path(sweep_path).read_text())
    reply = {}
    for c in json.loads(Path(argv[1]).read_text()):
        bot = c["user"]["login"] == "chatgpt-codex-connector[bot]"
        if not bot and c.get("in_reply_to_id") and (m := REPLY.search(c["body"])):
            reply[str(c["in_reply_to_id"])] = m.group(1)  # the latest reply wins
    gaps = []
    for item in sweep["items"]:
        key = (item.get("url") or "").rsplit("#", 1)[-1]
        cid, source, body = key.replace("discussion_r", ""), item["source"], item.get("body") or ""
        if source == "review_comment" and not item.get("bot") and body.startswith("Disposition (orchestrator"):
            source = "own_reply"
        elif source == "review" and "Codex Review" in body:
            source = "codex_review"
        show = f"{EVIDENCE}jq '.items[] | select(.url == \"{item.get('url')}\")' {sweep_path}"
        rule = RULES.get(source)
        d = extra.get(cid) or (
            reply.get(cid) if source == "review_comment" else rule and f"not-applicable:{rule}{show}"
        )
        if d and valid(d):
            item["disposition"] = d
        else:
            gaps.append((key, item["source"], item.get("level"), d or "-", body[:80].replace("\n", " ")))
    print("items", len(sweep["items"]), "filled", len(sweep["items"]) - len(gaps), "gaps", len(gaps))
    for gap in gaps:
        print("GAP", *gap)
    print(
        "dispositions",
        collections.Counter(i["disposition"].split(":")[0] for i in sweep["items"] if i.get("disposition")),
    )
    if gaps:
        sys.exit(1)
    Path(sweep_path).write_text(json.dumps(sweep, indent=2, ensure_ascii=False) + "\n")
    print("written", sweep_path)


if __name__ == "__main__":
    main(sys.argv[1:])
