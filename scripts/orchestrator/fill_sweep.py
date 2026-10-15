"""fill_sweep.py <sweep.json> <pr-comments.json> [extra.tsv] --orchestrator-login <login>: fill the dispositions.

A Bot thread takes the disposition of the latest reply in it by <login> (`fixed:<sha>` or `not-applicable:<reason>;
evidence=<command>` in backticks); a reply by another login is printed as ignored-reply. extra.tsv
(`id<TAB>disposition`) overrides or adds, where the id is the URL's fragment or `item-<n>` (the item's index); a
fragment that more than one item shares (the annotations of one check run) takes no row and is named by its
`item-<n>`. Other items get the fixed rules below, each with a jq command that shows the item, except an annotation,
a status or a review off its NEUTRAL level and any item whose body has a P0 to P3 BADGE. A not-applicable without
the gate's grammar (one `; evidence=` between a non-empty reason and command) is never emitted but listed as a gap.
The sweep JSON is rewritten only when every item has a disposition; otherwise exit 1.
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
# A review that requests changes, approves or was dismissed is not neutral (the audit of 046901b).
NEUTRAL = {"annotation": "notice", "status": "success", "review": "commented", "codex_review": "commented"}
BADGE = re.compile(r"!\[P[0-3] Badge\]\(")  # the Bot's image form; a bare P0 in hidden metadata is not one
FLAG = "--orchestrator-login"


def valid(disposition):
    """The gate's grammar: `fixed:<commit>`, or `not-applicable:<reason>; evidence=<command>` with one delimiter."""
    if re.fullmatch(r"fixed:[0-9a-f]{7,40}", disposition):
        return True
    body = disposition.removeprefix("not-applicable:")
    reason, _, command = body.partition(EVIDENCE)
    return body != disposition and body.count(EVIDENCE) == 1 and bool(reason.strip() and command.strip())


def main(argv):
    at = argv.index(FLAG) if FLAG in argv else len(argv)
    login, argv = "".join(argv[at + 1 : at + 2]), argv[:at] + argv[at + 2 :]
    if len(argv) not in (2, 3) or FLAG in argv or not re.fullmatch(r"[A-Za-z0-9-]{1,39}", login):
        print(__doc__.splitlines()[0], file=sys.stderr)
        sys.exit(2)
    sweep_path = argv[0]
    lines = Path(argv[2]).read_text().splitlines() if len(argv) == 3 else []
    extra = dict(line.split("\t")[:2] for line in lines if line.strip() and not line.startswith("#"))
    sweep = json.loads(Path(sweep_path).read_text())
    reply = {}
    for c in json.loads(Path(argv[1]).read_text()):
        if c.get("in_reply_to_id") and c["user"]["login"] != login:
            print("ignored-reply", c["id"], c["user"]["login"])
        elif c.get("in_reply_to_id") and (m := REPLY.search(c["body"])):
            reply[str(c["in_reply_to_id"])] = m.group(1)  # the latest reply wins
    gaps = []
    keys = [(item.get("url") or "").rsplit("#", 1)[-1] for item in sweep["items"]]
    shared = {k for k, n in collections.Counter(keys).items() if n > 1}
    for n, (item, key) in enumerate(zip(sweep["items"], keys, strict=True)):
        cid, source, body = key.replace("discussion_r", ""), item["source"], item.get("body") or ""
        if key in shared:
            if cid in extra:
                print("shared-key", cid, f"item-{n}")
            key, cid = f"item-{n}", None
        if source == "review_comment" and item.get("author") == login and body.startswith("Disposition (orchestrator"):
            source = "own_reply"
        elif source == "review" and "Codex Review" in body:
            source = "codex_review"
        show = f"{EVIDENCE}jq '.items[] | select(.url == \"{item.get('url')}\")' {sweep_path}"
        if cid is None:
            show = f"{EVIDENCE}jq '.items[{n}]' {sweep_path}"
        level = item.get("level")
        rule = None if NEUTRAL.get(source, level) != level or BADGE.search(body) else RULES.get(source)
        d = (
            extra.get(f"item-{n}")
            or extra.get(cid)
            or (reply.get(cid) if source == "review_comment" else rule and f"not-applicable:{rule}{show}")
        )
        if d and valid(d):
            item["disposition"] = d
        else:
            gaps.append((key, item["source"], item.get("level"), d or "-", body[:80].replace("\n", " ")))
    print("items", len(sweep["items"]), "filled", len(sweep["items"]) - len(gaps), "gaps", len(gaps))
    for gap in gaps:
        print("GAP", *gap)
    counts = collections.Counter(i["disposition"].split(":")[0] for i in sweep["items"] if i.get("disposition"))
    print("dispositions", counts)
    if gaps:
        sys.exit(1)
    Path(sweep_path).write_text(json.dumps(sweep, indent=2, ensure_ascii=False) + "\n")
    print("written", sweep_path)


if __name__ == "__main__":
    main(sys.argv[1:])
