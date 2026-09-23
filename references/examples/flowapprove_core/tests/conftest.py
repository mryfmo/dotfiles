"""追跡のための共通設定。

- Gherkin のタグ（@SCN-017 @FR-011 など）を pytest の `req` マーカーに写す。
- `--req FR-028` で、そのIDを確かめるテストだけを選べる。
- JUnit XML の各 testcase に `req` プロパティを書き出し、実行証跡からIDをたどれるようにする。
"""
from __future__ import annotations

import re

import pytest

ID = re.compile(r"[A-Z]+-\d{3,4}")


def pytest_bdd_apply_tag(tag, function):
    if ID.fullmatch(tag):
        pytest.mark.req(tag)(function)
        return True
    return None


def pytest_addoption(parser):
    parser.addoption("--req", action="append", default=[], help="このIDを確かめるテストだけを実行する（複数指定可）")


def pytest_collection_modifyitems(config, items):
    wanted = set(config.getoption("--req"))
    selected, deselected = [], []
    for item in items:
        ids = sorted({a for m in item.iter_markers("req") for a in m.args})
        size = next((s for s in ("small", "medium", "large") if item.get_closest_marker(s)), "unsized")
        item.user_properties += [("req", ",".join(ids)), ("size", size)]
        (selected if not wanted or wanted & set(ids) else deselected).append(item)
    if deselected:
        config.hook.pytest_deselected(items=deselected)
        items[:] = selected
