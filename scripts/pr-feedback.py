#!/usr/bin/env python3
"""Collect every piece of GitHub feedback on a pull request head into one JSON document.

Usage: pr-feedback.py <pr-number> [--repo owner/name] [--json <out>] [--require-codex-review]

Items cover issue comments, reviews, inline review comments (with their
thread's resolution state), non-passing check runs, every check-run
annotation at any level, and every commit status on the PR head. Each item
carries an empty `disposition` to fill with `fixed:<commit>` or
`not-applicable:<reason>` before integration; scripts/require-crit-review.py
checks the filled file through PR_FEEDBACK_EVIDENCE. Passing check runs are
listed under `checks` only. `codex_review` is the latest Codex review summary
the connector posted (null when none); --require-codex-review exits 1 unless
it is a completed review of the PR head.
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import subprocess
import sys
from collections import Counter
from collections.abc import Callable
from pathlib import Path
from typing import Any

PASSING_CONCLUSIONS = {"success", "neutral", "skipped"}
CODEX_BOT = "chatgpt-codex-connector[bot]"
CODEX_SUMMARY_MARKER = "<!-- codex-pull-request-review-summary -->"
CODEX_REVIEW_META = re.compile(r"<!-- codex-security-review:v1 (\{.*?\}) -->", re.S)
THREADS_QUERY = """
query($owner: String!, $name: String!, $number: Int!, $cursor: String) {
  repository(owner: $owner, name: $name) {
    pullRequest(number: $number) {
      reviewThreads(first: 100, after: $cursor) {
        pageInfo { hasNextPage endCursor }
        nodes {
          id
          isResolved
          isOutdated
          comments(first: 100) {
            pageInfo { hasNextPage endCursor }
            nodes { databaseId }
          }
        }
      }
    }
  }
}
"""
THREAD_COMMENTS_QUERY = """
query($id: ID!, $cursor: String) {
  node(id: $id) {
    ... on PullRequestReviewThread {
      comments(first: 100, after: $cursor) {
        pageInfo { hasNextPage endCursor }
        nodes { databaseId }
      }
    }
  }
}
"""

Fetch = Callable[[str, bool], Any]
GraphQL = Callable[[str, dict[str, Any]], Any]


def gh_env() -> dict[str, str]:
    """Environment for gh that never colours output, even under CLICOLOR_FORCE panes."""
    env = {
        key: value
        for key, value in os.environ.items()
        if key not in {"CLICOLOR_FORCE", "GH_FORCE_TTY"}
    }
    env["NO_COLOR"] = "1"
    return env


def gh(args: list[str]) -> str:
    result = subprocess.run(
        ["gh", *args], capture_output=True, text=True, check=False, env=gh_env()
    )
    if result.returncode != 0:
        sys.exit(f"gh {' '.join(args[:2])} failed: {result.stderr.strip()}")
    return result.stdout


def gh_fetch(path: str, paginate: bool = False) -> Any:
    """Return the JSON for a REST path; paginated responses become a list of pages."""
    if paginate:
        return json.loads(gh(["api", "--paginate", "--slurp", path]))
    return json.loads(gh(["api", path]))


def gh_graphql(query: str, variables: dict[str, Any]) -> Any:
    args = ["api", "graphql", "-f", f"query={query}"]
    for key, value in variables.items():
        if value is not None:
            args.extend(["-F", f"{key}={value}"])
    return json.loads(gh(args))


def require_auth() -> None:
    result = subprocess.run(
        ["gh", "auth", "status"],
        capture_output=True,
        text=True,
        check=False,
        env=gh_env(),
    )
    if result.returncode != 0:
        print(
            "pr-feedback: gh is not authenticated; run `gh auth login`", file=sys.stderr
        )
        raise SystemExit(2)


def flatten(pages: Any, key: str | None = None) -> list[Any]:
    """Merge `gh api --paginate --slurp` pages into one list."""
    merged: list[Any] = []
    for page in pages:
        merged.extend(page[key] if key else page)
    return merged


def is_bot(actor: dict[str, Any] | None) -> bool:
    if not actor:
        return False
    login = str(actor.get("login") or actor.get("slug") or "")
    return actor.get("type") == "Bot" or login.endswith("[bot]") or "slug" in actor


def item(
    source: str,
    actor: dict[str, Any] | None,
    level: str,
    body: str | None,
    url: str | None,
    path: str | None = None,
    line: int | None = None,
    **extra: Any,
) -> dict[str, Any]:
    return {
        "source": source,
        "author": (actor or {}).get("login") or (actor or {}).get("slug") or "",
        "bot": is_bot(actor),
        "level": level,
        "path": path,
        "line": line,
        "body": body or "",
        "url": url,
        **extra,
        "disposition": "",
    }


def thread_states(
    repo: str, number: int, graphql: GraphQL
) -> dict[int, dict[str, bool]]:
    """Map each review comment id to its thread's resolved and outdated state."""
    owner, name = repo.split("/", 1)
    states: dict[int, dict[str, bool]] = {}
    cursor = None
    while True:
        data = graphql(
            THREADS_QUERY,
            {"owner": owner, "name": name, "number": number, "cursor": cursor},
        )
        threads = data["data"]["repository"]["pullRequest"]["reviewThreads"]
        for thread in threads["nodes"]:
            state = {"resolved": thread["isResolved"], "outdated": thread["isOutdated"]}
            comments = thread["comments"]
            while True:
                for comment in comments["nodes"]:
                    states[comment["databaseId"]] = state
                if not comments["pageInfo"]["hasNextPage"]:
                    break
                page = graphql(
                    THREAD_COMMENTS_QUERY,
                    {"id": thread["id"], "cursor": comments["pageInfo"]["endCursor"]},
                )
                comments = page["data"]["node"]["comments"]
        if not threads["pageInfo"]["hasNextPage"]:
            return states
        cursor = threads["pageInfo"]["endCursor"]


def codex_review(comments: list[dict[str, Any]]) -> dict[str, Any] | None:
    """Return the latest Codex review summary the connector posted, or None.

    The connector keeps one summary comment per PR and edits it in place; its
    `codex-security-review:v1` marker carries the reviewed head. Only the
    connector's own comments count, so a pasted marker cannot fake a review.
    """
    for comment in reversed(comments):
        body = comment.get("body") or ""
        if (comment.get("user") or {}).get("login") != CODEX_BOT or CODEX_SUMMARY_MARKER not in body:
            continue
        match = CODEX_REVIEW_META.search(body)
        try:
            meta = json.loads(match.group(1)) if match else {}
        except ValueError:
            meta = {}
        return {
            "head_sha": meta.get("headSha"),
            "summary_comment_id": comment["id"],
            "blocking_threshold": meta.get("blockingSeverityThreshold"),
            "status": meta.get("status"),
        }
    return None


def codex_review_error(document: dict[str, Any]) -> str | None:
    """Explain why the document has no completed Codex review of its head, if it has none."""
    review = document.get("codex_review")
    head = document.get("head_sha")
    if not review:
        return f"no Codex review summary on PR #{document.get('pr')}; comment `@codex review` and wait for it"
    if review.get("head_sha") != head:
        return f"the Codex review summary is for {review.get('head_sha')}, not the PR head {head}; comment `@codex review`"
    if review.get("status") != "completed":
        return f"the Codex review of {head} is {review.get('status')!r}, not completed; wait for it"
    return None


def collect(
    repo: str, number: int, fetch: Fetch = gh_fetch, graphql: GraphQL = gh_graphql
) -> dict[str, Any]:
    pull = fetch(f"repos/{repo}/pulls/{number}", False)
    sha = pull["head"]["sha"]
    items: list[dict[str, Any]] = []

    issue_comments = flatten(fetch(f"repos/{repo}/issues/{number}/comments", True))
    for comment in issue_comments:
        items.append(
            item(
                "issue_comment",
                comment["user"],
                "comment",
                comment["body"],
                comment["html_url"],
            )
        )
    for review in flatten(fetch(f"repos/{repo}/pulls/{number}/reviews", True)):
        items.append(
            item(
                "review",
                review["user"],
                review["state"].lower(),
                review["body"],
                review["html_url"],
                commit=review.get("commit_id"),
            )
        )
    states = thread_states(repo, number, graphql)
    for comment in flatten(fetch(f"repos/{repo}/pulls/{number}/comments", True)):
        state = states.get(comment["id"], {"resolved": False, "outdated": False})
        items.append(
            item(
                "review_comment",
                comment["user"],
                "comment",
                comment["body"],
                comment["html_url"],
                comment["path"],
                comment.get("line") or comment.get("original_line"),
                **state,
            )
        )

    checks = []
    for run in flatten(
        fetch(f"repos/{repo}/commits/{sha}/check-runs", True), "check_runs"
    ):
        conclusion = run.get("conclusion") or run.get("status")
        checks.append(
            {"name": run["name"], "conclusion": conclusion, "url": run["html_url"]}
        )
        output = run.get("output") or {}
        if conclusion not in PASSING_CONCLUSIONS:
            summary = " ".join(
                part for part in (output.get("title"), output.get("summary")) if part
            )
            items.append(
                item(
                    "check_run",
                    run.get("app"),
                    conclusion,
                    f"{run['name']}: {summary}".strip(),
                    run["html_url"],
                    check=run["name"],
                )
            )
        if output.get("annotations_count"):
            for annotation in flatten(
                fetch(f"repos/{repo}/check-runs/{run['id']}/annotations", True)
            ):
                message = " ".join(
                    part
                    for part in (annotation.get("title"), annotation["message"])
                    if part
                )
                items.append(
                    item(
                        "annotation",
                        run.get("app"),
                        annotation["annotation_level"],
                        message,
                        run["html_url"],
                        annotation.get("path"),
                        annotation.get("start_line"),
                        check=run["name"],
                    )
                )

    # The statuses list keeps creators and is newest first; keep each context's latest.
    latest: dict[str, dict[str, Any]] = {}
    for status in flatten(fetch(f"repos/{repo}/commits/{sha}/statuses", True)):
        latest.setdefault(status["context"], status)
    for status in latest.values():
        items.append(
            item(
                "status",
                status.get("creator"),
                status["state"],
                f"{status['context']}: {status.get('description') or ''}".strip(),
                status.get("target_url"),
                check=status["context"],
            )
        )

    return {
        "repo": repo,
        "pr": number,
        "head_sha": sha,
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(
            timespec="seconds"
        ),
        "codex_review": codex_review(issue_comments),
        "checks": checks,
        "items": items,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("pr", type=int, help="pull request number")
    parser.add_argument("--repo", help="owner/name; defaults to the current repository")
    parser.add_argument(
        "--json", type=Path, help="write the document here instead of stdout"
    )
    parser.add_argument(
        "--require-codex-review",
        action="store_true",
        help="exit 1 unless a completed Codex review summary exists for the PR head",
    )
    args = parser.parse_args(argv)

    require_auth()
    repo = (
        args.repo
        or gh(
            ["repo", "view", "--json", "nameWithOwner", "-q", ".nameWithOwner"]
        ).strip()
    )
    document = collect(repo, args.pr)
    text = json.dumps(document, indent=2, ensure_ascii=False) + "\n"
    if args.json:
        args.json.write_text(text)
    else:
        sys.stdout.write(text)
    counts = Counter(
        f"{entry['source']}:{entry['level']}" for entry in document["items"]
    )
    summary = ", ".join(f"{key}={value}" for key, value in sorted(counts.items()))
    print(
        f"pr-feedback: {repo}#{args.pr} head {document['head_sha'][:7]}: {len(document['items'])} items ({summary})",
        file=sys.stderr,
    )
    if args.require_codex_review:
        error = codex_review_error(document)
        if error:
            print(f"pr-feedback: {error}", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
