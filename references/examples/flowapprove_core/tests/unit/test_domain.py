"""UT：ドメイン規則。small サイズ（入出力・時計・乱数・待ちなし）。テスト名は UT_SAMPLE.md の表と対応する。"""
from __future__ import annotations

import itertools
import unicodedata
from datetime import datetime, timedelta

import pytest
from hypothesis import given, strategies as st
from hypothesis.stateful import RuleBasedStateMachine, invariant, rule

from flowapprove.domain import (EVENTS, TERMINAL, TRANSITIONS, NotAllowed, Refusal, State, auto_withdraw_due,
                                decision_refusal, deletion_due, next_state, normalize, notice_due, valid_url, violations)

pytestmark = pytest.mark.small
VALID = {"製品名": "Example Editor", "提供元URL": "https://vendor.example/product", "利用バージョン": "1.2.3",
         "利用目的": "設計書の作成", "情報分類": "社内"}
T0 = datetime(2026, 1, 1)


# ---- 入力規則 ----
@pytest.mark.req("FR-003")
def test_valid_draft_has_no_violations():
    assert violations(VALID) == []


@pytest.mark.req("FR-004")
@pytest.mark.parametrize("name", ["製品名", "提供元URL", "利用バージョン", "利用目的", "情報分類"])
@pytest.mark.parametrize("blank", ["", "   ", "\u3000"])
def test_blank_required_field_is_reported(name, blank):
    assert violations({**VALID, name: blank}) == [name]


@pytest.mark.req("FR-003", "FR-004")
@pytest.mark.parametrize("name,limit", [("製品名", 100), ("利用バージョン", 50), ("利用目的", 1000)])
def test_length_boundary(name, limit):
    assert violations({**VALID, name: "あ" * limit}) == []
    assert violations({**VALID, name: "あ" * (limit + 1)}) == [name]


@pytest.mark.req("FR-003")
def test_length_is_counted_after_nfc_normalization():
    decomposed = "e\u0301" * 100                       # 200 コードポイントだが NFC では 100
    assert len(decomposed) == 200 and violations({**VALID, "製品名": decomposed}) == []


@pytest.mark.req("FR-003")
@given(st.text(max_size=300))
def test_length_rule_depends_only_on_normalized_text(text):
    expected_bad = not (1 <= len(unicodedata.normalize("NFC", text.strip())) <= 100)
    assert (("製品名" in violations({**VALID, "製品名": text})) is expected_bad)


@pytest.mark.req("FR-003")
@given(st.text(max_size=50))
def test_normalize_is_idempotent(text):
    assert normalize(normalize(text)) == normalize(text)


@pytest.mark.req("FR-004")
@pytest.mark.parametrize("url,ok", [
    ("https://vendor.example/product", True),
    ("http://vendor.example/product", False),                 # https でない
    ("https://user:secret@vendor.example/product", False),    # ユーザー情報を含む
    ("https://user@vendor.example/", False),
    ("not-a-url", False),
    ("https:///path-only", False),                            # ホストがない
    ("https://[broken", False),                               # 解析できない
    ("https://vendor.example/" + "a" * (2048 - 23), True),    # ちょうど 2048 文字
    ("https://vendor.example/" + "a" * (2048 - 22), False),   # 2049 文字
])
def test_url_rule(url, ok):
    assert valid_url(url) is ok


@pytest.mark.req("FR-004")
@pytest.mark.parametrize("value,ok", [("公開", True), ("社内", True), ("機密", True), ("極秘", False)])
def test_classification_is_a_closed_set(value, ok):
    assert violations({**VALID, "情報分類": value}) == ([] if ok else ["情報分類"])


@pytest.mark.req("FR-004")
def test_invalid_url_is_reported_as_the_url_field():
    """ミューテーションテストで見つかった穴：valid_url 単体は試験していたが、violations が URL 規則を呼ぶことを確かめていなかった。"""
    assert violations({**VALID, "提供元URL": "http://vendor.example/product"}) == ["提供元URL"]


@pytest.mark.req("FR-004")
def test_all_violations_are_reported_in_field_order():
    assert violations({}) == ["製品名", "提供元URL", "利用バージョン", "利用目的", "情報分類"]


# ---- 状態遷移 ----
@pytest.mark.req("FR-011", "FR-018", "FR-019", "FR-020")
@pytest.mark.parametrize("state,event", list(itertools.product(State, EVENTS)))
def test_transition_table_is_exhaustive(state, event):
    """状態×出来事の全 36 通り。表にある組だけが遷移し、それ以外は拒否される。"""
    if (state, event) in TRANSITIONS:
        assert next_state(state, event) is TRANSITIONS[(state, event)]
    else:
        with pytest.raises(NotAllowed):
            next_state(state, event)


class ApplicationLifecycle(RuleBasedStateMachine):
    """任意の順で出来事を与えても、終端状態からは動かない（FR-020）。"""

    def __init__(self):
        super().__init__()
        self.state, self.was_terminal = State.DRAFT, False

    @rule(event=st.sampled_from(EVENTS))
    def apply(self, event):
        before = self.state
        try:
            self.state = next_state(self.state, event)
        except NotAllowed:
            assert self.state is before
        if before in TERMINAL:
            assert self.state is before

    @invariant()
    def terminal_is_absorbing(self):
        self.was_terminal = self.was_terminal or self.state in TERMINAL
        assert not self.was_terminal or self.state in TERMINAL


test_terminal_states_are_absorbing = pytest.mark.req("FR-020")(ApplicationLifecycle.TestCase)


# ---- 拒否理由の優先順位 ----
ORDER = [Refusal.NOT_FOUND, Refusal.SELF, Refusal.CONFLICT, Refusal.BAD_STATE, Refusal.INVALID]


@pytest.mark.req("FR-028", "FR-002", "FR-012", "FR-013", "FR-020")
@pytest.mark.parametrize("flags", list(itertools.product([False, True], repeat=5)))
def test_refusal_precedence_decision_table(flags):
    """5つの拒否条件の全 32 通り。当たった条件のうち FR-028 の順で最初の理由だけが返る。"""
    not_permitted, is_self, stale, bad_state, bad_reason = flags
    got = decision_refusal(permitted=not not_permitted, is_self=is_self, rev_matches=not stale,
                           state=State.APPROVED if bad_state else State.SUBMITTED, reason="" if bad_reason else "規程を確認した")
    hit = [r for r, f in zip(ORDER, flags) if f]
    assert got is (hit[0] if hit else None)


@pytest.mark.req("FR-020")
@pytest.mark.parametrize("state", [s for s in State if s is not State.SUBMITTED])
def test_only_submitted_can_be_decided(state):
    assert decision_refusal(permitted=True, is_self=False, rev_matches=True, state=state, reason="x") is Refusal.BAD_STATE


@pytest.mark.req("FR-011")
@pytest.mark.parametrize("length,ok", [(0, False), (1, True), (1000, True), (1001, False)])
def test_reason_length_boundary(length, ok):
    got = decision_refusal(permitted=True, is_self=False, rev_matches=True, state=State.SUBMITTED, reason="あ" * length)
    assert (got is None) is ok


# ---- 期限 ----
@pytest.mark.req("FR-021")
@pytest.mark.parametrize("days,due", [(89, False), (90, True), (91, True)])
def test_deletion_due_boundary(days, due):
    assert deletion_due(T0, T0 + timedelta(days=days)) is due


@pytest.mark.req("FR-022", "FR-023")
@pytest.mark.parametrize("days,notice,withdraw", [(165, False, False), (166, True, False), (179, True, False), (180, False, True)])
def test_notice_and_auto_withdraw_boundaries(days, notice, withdraw):
    now = T0 + timedelta(days=days)
    assert notice_due(State.DRAFT, T0, now) is notice
    assert auto_withdraw_due(State.DRAFT, T0, now) is withdraw


@pytest.mark.req("FR-022")
@pytest.mark.parametrize("state", sorted(TERMINAL))
def test_terminal_applications_are_never_auto_withdrawn(state):
    late = T0 + timedelta(days=10_000)
    assert not auto_withdraw_due(state, T0, late) and not notice_due(state, T0, late)
