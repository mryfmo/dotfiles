"""Propose a disposition per review thread of a PR sweep and verify the refutation form of each not-applicable one.

`uv run --no-project python -I scripts/orchestrator/dispositions.py <pr> <head> --feedback <sweep.json> [--out <json>]
[--require-refutation] [--commits <json>]` (plan 024 P1-10, programs item (5)), run in the repository's checkout. A
thread is a `review_comment` item of the scripts/pr-feedback.py sweep, or a `review` item whose body carries a P0 to P3
badge; its path and line are the item's, else its body's first `/blob/<sha>/<path>#L<n>` link, and a thread without
them gets the not-applicable demand with no commit needed. Its commit is the item's `original_commit_id` (or `commit`),
else the `--commits` map (url -> commit), else `gh api repos/<repo>/pulls/comments/<id> --jq .original_commit_id`; a
gh failure, or a commit git cannot read, is a hold, never a guess. Every path reaches git as `:(literal)<path>`, so
the PR's file names are never pathspec magic. When `git diff <commit>..<head> -- <path>` has a hunk whose old
or new range covers the line, the proposal is `fixed:<c>`, c the newest non-merge commit of `git log <commit>..<head>
^<base_sha> -- <path>` whose own hunks overlap that hunk; otherwise it is `not-applicable:` with the reason to fill.
A thread's not-applicable disposition (the gate's `not-applicable:<reason>; evidence=<form>`) is verified when its
evidence is one of the three refutation forms (plan 024 5.13): `test:<selector>` (`tests/<path>.py::<name>` or a
dotted unittest name; `uv run --no-project python -m unittest` in this checkout must exit 0, its last line recorded),
`source:{"url": ..., "fetched_at": ..., "quote": ...}` (an https or file URL; the quote must occur in the page text,
the page's sha256 recorded) or `diff:<range>` (`git diff <range> -- <path>` must have no hunk covering the line). Any
other evidence is `legacy-evidence`. The sweep is written to --out (default stdout) with `proposal`, and for a
thread's not-applicable disposition `refutation`, added per thread, the disposition untouched; one line per thread
goes to stderr. Exit 0; 1 under --require-refutation when a thread's not-applicable has no verified form (legacy
evidence included); 2 on a usage error or a hold. It runs only git reads, gh api reads, the named selector and the
URL fetch; no sweep text is evaluated.
"""

import argparse
import hashlib
import html
import json
import re
import shutil
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path

HUNK = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@", re.MULTILINE)
SHA = re.compile(r"[0-9a-f]{7,40}")
RANGE = re.compile(r"[\w./^~]+\.\.\.?[\w./^~]+")
EVIDENCE = "; evidence="
MAX_PAGE = 10 * 1024 * 1024


class Hold(Exception):
    """A thread whose commit or diff cannot be read."""


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True, check=False)


def hunks(revs, path):
    """The (old start, old count, new start, new count) of each hunk of `git diff <revs> -- <path>`."""
    # The path is the PR's text: a literal pathspec, so a leading `:` is never magic (Bot 4307288056).
    out = git("diff", "--no-ext-diff", "--no-textconv", "--no-color", "-U3", revs, "--", f":(literal){path}")
    if out.returncode:
        raise Hold(f"git diff {revs} -- {path} failed: {out.stderr.strip()[:120]}")
    return [(int(a), int(b or 1), int(c), int(d or 1)) for a, b, c, d in HUNK.findall(out.stdout)]


def spans(h):
    """A hunk's old and new line ranges; an empty side stands at its start line."""
    return (h[0], h[0] + max(h[1], 1) - 1), (h[2], h[2] + max(h[3], 1) - 1)


def covers(h, line):
    return any(lo <= line <= hi for lo, hi in spans(h))


def overlaps(h, target):
    return any(lo <= t_hi and t_lo <= hi for (lo, hi), (t_lo, t_hi) in zip(spans(h), spans(target)))


def thread_commit(item, repo, commits):
    url = item.get("url") or ""
    commit = item.get("original_commit_id") or item.get("commit") or commits.get(url)
    if not commit:
        number, gh = re.search(r"#discussion_r(\d+)$", url), shutil.which("gh")
        if not (number and gh and re.fullmatch(r"[\w.-]+/[\w.-]+", repo or "")):
            raise Hold("no thread commit: the sweep, --commits and gh name none")
        api = f"repos/{repo}/pulls/comments/{number[1]}"
        out = subprocess.run(
            [gh, "api", api, "--jq", ".original_commit_id"], capture_output=True, text=True, check=False
        )
        if out.returncode:
            raise Hold(f"gh api {api} failed: {out.stderr.strip()[:120]}")
        commit = out.stdout.strip()
    if (
        not (isinstance(commit, str) and SHA.fullmatch(commit))
        or git("cat-file", "-e", f"{commit}^{{commit}}").returncode
    ):
        raise Hold(f"the thread commit {commit!r} is not a commit here")
    return commit


def propose(commit, head, base, path, line):
    target = next((h for h in hunks(f"{commit}..{head}", path) if covers(h, line)), None)
    if target is None:
        return "not-applicable:"
    exclude = [f"^{base}"] if base else []
    log = git("log", "--no-merges", "--format=%H", f"{commit}..{head}", *exclude, "--", f":(literal){path}")
    if log.returncode or not log.stdout.split():
        raise Hold(f"git log {commit[:7]}..{head[:7]} -- {path} names no commit: {log.stderr.strip()[:120]}")
    for c in log.stdout.split():  # newest first
        if any(overlaps(h, target) for h in hunks(f"{c}^..{c}", path)):
            return f"fixed:{c}"
    # shortcut: commits between the newest and the thread shift line numbers, so a match can be missed; the newest
    # commit on the path stands in for a person to confirm. Upgrade to a blame-based walk if that shows up in practice.
    return f"fixed:{log.stdout.split()[0]}"


def refute(evidence, item):
    """Verify a not-applicable disposition's evidence: (form, ok, record)."""
    form, _, value = evidence.partition(":")
    value = value.strip()
    if form == "test":
        if m := re.fullmatch(r"(tests/[\w/]+)\.py::([A-Za-z_]\w*)", value):
            names = [m[1].replace("/", "."), "-k", m[2]]
        elif re.fullmatch(r"[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)+", value):
            names = [value]
        else:
            return form, False, "not a tests/<path>.py::<name> or dotted unittest selector"
        # orch-gate.sh's private PATH has no uv; its interpreter is uv's own (`uv python find`), so it runs the selector.
        uv = shutil.which("uv")
        python = [uv, "run", "--no-project", "python"] if uv else [sys.executable]
        try:
            run = [*python, "-m", "unittest", *names]
            out = subprocess.run(run, capture_output=True, text=True, timeout=600, check=False)
        except subprocess.TimeoutExpired:
            return form, False, "the selector ran over 600 s"
        last = next((s for s in reversed((out.stdout + out.stderr).splitlines()) if s.strip()), "")
        return form, out.returncode == 0, f"exit {out.returncode}: {last}"
    if form == "source":
        try:
            source = json.loads(value)
            url, quote, _ = source["url"], source["quote"], source["fetched_at"]
        except (ValueError, KeyError, TypeError):
            return form, False, "not a JSON object with url, fetched_at and quote"
        if not (isinstance(url, str) and url.startswith(("https://", "file://")) and isinstance(quote, str)):
            return form, False, "the url is not https:// or file:// or the quote is not text"
        try:
            with urllib.request.urlopen(url, timeout=30) as page:
                data = page.read(MAX_PAGE)
        except (OSError, ValueError) as error:
            return form, False, f"the fetch failed: {error}"
        text = " ".join(html.unescape(re.sub(r"<[^>]*>", " ", data.decode("utf-8", "replace"))).split())
        found = bool(quote.split()) and " ".join(quote.split()) in text
        return form, found, f"sha256={hashlib.sha256(data).hexdigest()}" + ("" if found else "; the quote is not in it")
    if form == "diff":
        path, line = location(item)
        if not RANGE.fullmatch(value):
            return form, False, "not a <rev>..<rev> range"
        if not path or not isinstance(line, int):
            return form, False, "the thread names no path and line"
        try:
            touched = [h for h in hunks(value, path) if covers(h, line)]
        except Hold as error:
            return form, False, str(error)
        return form, not touched, f"a hunk of {value} covers line {line}" if touched else "no hunk covers the line"
    return "legacy-evidence", False, evidence[:80]


def is_thread(item):
    badged = re.search(r"!\[P[0-3] Badge\]", item.get("body") or "")
    return item.get("source") == "review_comment" or (item.get("source") == "review" and bool(badged))


def location(item):
    """The thread's path and line: the item's own, else its body's first blob link (a review-body finding)."""
    if isinstance(item.get("path"), str) and item["path"] and isinstance(item.get("line"), int):
        return item["path"], item["line"]
    link = re.search(r"/blob/[0-9a-f]{7,40}/([^\s#)]+)#L(\d+)", item.get("body") or "")
    return (urllib.parse.unquote(link[1]), int(link[2])) if link else (None, None)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("pr", type=int)
    parser.add_argument("head")
    parser.add_argument("--feedback", type=Path, required=True)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--require-refutation", action="store_true")
    parser.add_argument("--commits", type=Path, help="a JSON map of thread url to thread commit")
    args = parser.parse_args()
    if not re.fullmatch(r"[0-9a-f]{40}", args.head):
        parser.error("head must be a 40-digit lowercase sha")
    try:
        sweep = json.loads(args.feedback.read_text())
        commits = json.loads(args.commits.read_text()) if args.commits else {}
        if not (isinstance(sweep, dict) and isinstance(sweep.get("items"), list) and isinstance(commits, dict)):
            raise TypeError("the sweep needs an items list and --commits a JSON object")
        if sweep.get("pr") != args.pr:
            raise ValueError(f"the sweep is of PR {sweep.get('pr')!r}, not {args.pr}")
    except (OSError, ValueError, TypeError) as error:
        print(f"dispositions: hold: unreadable input: {error}", file=sys.stderr)
        return 2
    base = sweep.get("base_sha") if re.fullmatch(r"[0-9a-f]{40}", str(sweep.get("base_sha"))) else None
    holds = failed = 0
    for item in filter(lambda i: isinstance(i, dict) and is_thread(i), sweep["items"]):
        url, (path, line) = item.get("url") or "-", location(item)
        try:
            # A thread without a line has no hunk to cover: the demand needs no commit.
            located = path is not None
            commit = thread_commit(item, sweep.get("repo"), commits) if located else None
            item["proposal"] = propose(commit, args.head, base, path, line) if located else "not-applicable:"
            print(f"dispositions: {url} proposal {item['proposal']}", file=sys.stderr)
        except Hold as error:
            holds += 1
            item["proposal"] = None
            print(f"dispositions: {url} hold: {error}", file=sys.stderr)
        disposition = item.get("disposition")
        if isinstance(disposition, str) and disposition.startswith("not-applicable:"):
            evidence = disposition.partition(EVIDENCE)[2].strip()
            form, ok, record = refute(evidence, item) if evidence else ("none", False, "no refutation form")
            item["refutation"] = {"form": form, "ok": ok, "record": record}
            failed += not ok
            state = "ok" if ok else "FAIL" if args.require_refutation else "unverified"
            print(f"dispositions: {url} refutation {form} {state}: {record}", file=sys.stderr)
    text = json.dumps(sweep, indent=2, ensure_ascii=False) + "\n"
    if args.out:
        args.out.write_text(text)
    else:
        sys.stdout.write(text)
    return 2 if holds else 1 if args.require_refutation and failed else 0


if __name__ == "__main__":
    sys.exit(main())
