"""追跡のための共通設定。

- Gherkin のタグ（@SCN-017 @FR-011 など）を pytest の `req` マーカーに写す。
- `--req FR-028` で、そのIDを確かめるテストだけを選べる。
- JUnit XML の各 testcase に `req` プロパティを書き出し、実行証跡からIDをたどれるようにする。
- Hypothesis のプロファイル `kit`：`derandomize=True`（Python・Hypothesis・テスト関数を
  変えない限り、@given のテストは毎回同じ入力集合で再実行される。hypothesis 6.168 の
  実装は「derandomize=True は database=None を意味する」ため database を明示できない
  （hypothesis.errors.InvalidArgument。本機で実際に確認した）。失敗例の保存は
  derandomize なしの実行のときだけ既定の `DirectoryBasedExampleDatabase`（`.hypothesis/`）
  が受け持つ。これにより UT_SAMPLE §4 が要求する再現性が本参考実装でも成立する
  （hypothesis のドキュメントに従う。sources §6）。
"""
from __future__ import annotations

import re

import pytest
from hypothesis import settings

ID = re.compile(r"[A-Z]+-\d{3,4}")

settings.register_profile("kit", derandomize=True)
settings.load_profile("kit")


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
