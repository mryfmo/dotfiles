"""UT：ドメイン規則。small サイズ（入出力・時計・乱数・待ちなし）。テスト名は UT_SAMPLE.md の表と対応する。"""
from __future__ import annotations

import itertools
from datetime import datetime, timedelta

import pytest
from hypothesis import given, strategies as st
from hypothesis.stateful import RuleBasedStateMachine, invariant, rule

from flowapprove.domain import (AUTO_WITHDRAW, DECISIONS, EDITABLE, EVENTS, MAX_LEN, NOTICE, REASON_MAX_LEN,
                                RETENTION, REPLAY, TERMINAL, URL_MAX_LEN, NotAllowed, Refusal, State,
                                auto_withdraw_due, decision_refusal, deletion_due, is_editable, next_state,
                                normalize, notice_due, valid_url, violations)

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


NORMALIZE_EXAMPLES = [
    ("caf\u00e9", "caf\u00e9"),               # 既に合成済み（NFC）の é：変化なし
    ("cafe\u0301", "caf\u00e9"),               # e + 結合アクセント（分解形）→ NFC で合成される
    ("\u3000ようこそ\u3000", "ようこそ"),        # 全角空白（U+3000）の前後は取り除く
    ("  hello  ", "hello"),                    # 半角空白も同様
    ("", ""),
]


@pytest.mark.req("FR-003")
@pytest.mark.parametrize("text,expected", NORMALIZE_EXAMPLES)
def test_normalize_examples(text, expected):
    """normalize の性質を、normalize 自身を呼ばずに書いた具体例で確認する（以前の
    プロパティテストは unicodedata.normalize を再実装しており、normalize 自体の
    バグを見つけられなかった）。"""
    assert normalize(text) == expected


@pytest.mark.req("FR-003")
@given(st.text(max_size=300))
def test_length_rule_depends_only_on_normalized_text(text):
    expected_bad = not (1 <= len(normalize(text)) <= MAX_LEN["製品名"])
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
    ("https://vendor.example/" + "a" * (URL_MAX_LEN - 23), True),    # ちょうど上限
    ("https://vendor.example/" + "a" * (URL_MAX_LEN - 22), False),   # 上限+1
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


# ---- 境界カタログ（UT_GUIDE §7：mutmut はモジュール水準の定数を変異しないため、
# PRD から書き写した期待値と実装の定数を直接突き合わせる。定数を±1変えるとここか、
# 対応する既存の境界値テストのいずれかが落ちる） ----
BOUNDARY_CATALOG: dict[str, tuple[str, int]] = {
    "MAX_LEN[製品名]": ("PRD 10章 入力規則", 100),
    "MAX_LEN[利用バージョン]": ("PRD 10章 入力規則", 50),
    "MAX_LEN[利用目的]": ("PRD 10章 入力規則", 1000),
    "URL_MAX_LEN": ("PRD 10章 入力規則", 2048),
    "REASON_MAX_LEN": ("PRD 10章 入力規則・FR-011", 1000),
    "RETENTION（日）": ("FR-021", 90),
    "NOTICE（日）": ("FR-023", 166),
    "AUTO_WITHDRAW（日）": ("FR-022", 180),
}


@pytest.mark.req("FR-003", "FR-004", "FR-011", "FR-021", "FR-022", "FR-023")
def test_boundary_catalog_matches_domain_constants():
    assert BOUNDARY_CATALOG["MAX_LEN[製品名]"][1] == MAX_LEN["製品名"]
    assert BOUNDARY_CATALOG["MAX_LEN[利用バージョン]"][1] == MAX_LEN["利用バージョン"]
    assert BOUNDARY_CATALOG["MAX_LEN[利用目的]"][1] == MAX_LEN["利用目的"]
    assert BOUNDARY_CATALOG["URL_MAX_LEN"][1] == URL_MAX_LEN
    assert BOUNDARY_CATALOG["REASON_MAX_LEN"][1] == REASON_MAX_LEN
    assert BOUNDARY_CATALOG["RETENTION（日）"][1] == RETENTION.days
    assert BOUNDARY_CATALOG["NOTICE（日）"][1] == NOTICE.days
    assert BOUNDARY_CATALOG["AUTO_WITHDRAW（日）"][1] == AUTO_WITHDRAW.days


# ---- 状態遷移 ----
# PRD 0.5.0 6章の状態表を書き起こした期待値。next_state・TRANSITIONS は経由しない
# （実装から独立に期待値を持つ。G-07：以前のテストは TRANSITIONS 自身を期待値に
# 使っており、表から1行消しても合格し続けた）。
STATE_TABLE_v0_5_0: dict[tuple[State, str], State | None] = {
    (State.DRAFT, "提出"): State.SUBMITTED,
    (State.DRAFT, "承認"): None,
    (State.DRAFT, "却下"): None,
    (State.DRAFT, "差戻し"): None,
    (State.DRAFT, "修正"): None,
    (State.DRAFT, "取消"): State.WITHDRAWN,
    (State.SUBMITTED, "提出"): None,
    (State.SUBMITTED, "承認"): State.APPROVED,
    (State.SUBMITTED, "却下"): State.REJECTED,
    (State.SUBMITTED, "差戻し"): State.RETURNED,
    (State.SUBMITTED, "修正"): None,
    (State.SUBMITTED, "取消"): State.WITHDRAWN,
    (State.APPROVED, "提出"): None,
    (State.APPROVED, "承認"): None,
    (State.APPROVED, "却下"): None,
    (State.APPROVED, "差戻し"): None,
    (State.APPROVED, "修正"): None,
    (State.APPROVED, "取消"): None,
    (State.REJECTED, "提出"): None,
    (State.REJECTED, "承認"): None,
    (State.REJECTED, "却下"): None,
    (State.REJECTED, "差戻し"): None,
    (State.REJECTED, "修正"): None,
    (State.REJECTED, "取消"): None,
    (State.RETURNED, "提出"): None,
    (State.RETURNED, "承認"): None,
    (State.RETURNED, "却下"): None,
    (State.RETURNED, "差戻し"): None,
    (State.RETURNED, "修正"): State.DRAFT,
    (State.RETURNED, "取消"): State.WITHDRAWN,
    (State.WITHDRAWN, "提出"): None,
    (State.WITHDRAWN, "承認"): None,
    (State.WITHDRAWN, "却下"): None,
    (State.WITHDRAWN, "差戻し"): None,
    (State.WITHDRAWN, "修正"): None,
    (State.WITHDRAWN, "取消"): None,
}


@pytest.mark.req("FR-011", "FR-018", "FR-019", "FR-020")
@pytest.mark.parametrize("state,event", list(STATE_TABLE_v0_5_0))
def test_transition_table_is_exhaustive(state, event):
    """状態×出来事の全36通り。表にある組だけが遷移し、それ以外は拒否される。"""
    expected = STATE_TABLE_v0_5_0[(state, event)]
    if expected is None:
        with pytest.raises(NotAllowed):
            next_state(state, event)
    else:
        assert next_state(state, event) is expected


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


# ---- 編集可否（FR-005） ----
@pytest.mark.req("FR-005")
@pytest.mark.parametrize("state", sorted(EDITABLE, key=lambda s: s.value))
def test_editing_is_allowed_in_draft_and_returned(state):
    assert is_editable(state)


@pytest.mark.req("FR-005")
@pytest.mark.parametrize("state", [s for s in State if s not in EDITABLE])
def test_editing_is_refused_outside_draft_and_returned(state):
    """DRAFT・RETURNED 以外（SUBMITTED を含む）はすべて編集できない。"""
    assert not is_editable(state)


# ---- 拒否理由の優先順位（FR-028） ----
@pytest.mark.req("FR-028", "FR-002", "FR-012", "FR-013", "FR-015", "FR-020")
@pytest.mark.parametrize("flags", list(itertools.product([False, True], repeat=6)))
def test_refusal_precedence_decision_table(flags):
    """6つの条件（対象なし・再送・自己決裁・競合・決裁できない状態・入力不備）の全64通り。
    期待値は FR-028 の文をそのまま if/elif に書き起こしたもので、decision_refusal
    自身の実装や共通の順序リストからは計算しない。"""
    not_permitted, is_replay, is_self, stale, bad_state, bad_input = flags
    got = decision_refusal(
        permitted=not not_permitted, is_replay=is_replay, is_self=is_self, rev_matches=not stale,
        state=State.APPROVED if bad_state else State.SUBMITTED,
        action_valid=not bad_input, reason="" if bad_input else "規程を確認した",
    )
    if not_permitted:
        expected = Refusal.NOT_FOUND
    elif is_replay:
        expected = REPLAY
    elif is_self:
        expected = Refusal.SELF
    elif stale:
        expected = Refusal.CONFLICT
    elif bad_state:
        expected = Refusal.BAD_STATE
    elif bad_input:
        expected = Refusal.INVALID
    else:
        expected = None
    assert got == expected


@pytest.mark.req("FR-020")
@pytest.mark.parametrize("state", [s for s in State if s is not State.SUBMITTED])
def test_only_submitted_can_be_decided(state):
    assert decision_refusal(permitted=True, is_replay=False, is_self=False, rev_matches=True,
                            state=state, action_valid=True, reason="x") is Refusal.BAD_STATE


@pytest.mark.req("FR-011")
@pytest.mark.parametrize("length,ok", [(0, False), (1, True), (1000, True), (1001, False)])
def test_reason_length_boundary(length, ok):
    got = decision_refusal(permitted=True, is_replay=False, is_self=False, rev_matches=True,
                           state=State.SUBMITTED, action_valid=True, reason="あ" * length)
    assert (got is None) is ok


@pytest.mark.req("FR-028")
@pytest.mark.parametrize("action", ["取消", "提出", "でたらめ"])
def test_invalid_action_is_bad_request(action):
    assert action not in DECISIONS
    got = decision_refusal(permitted=True, is_replay=False, is_self=False, rev_matches=True,
                           state=State.SUBMITTED, action_valid=action in DECISIONS, reason="規程を確認した")
    assert got is Refusal.BAD_REQUEST


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
