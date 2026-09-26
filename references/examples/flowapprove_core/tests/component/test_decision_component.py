"""CT：BDD では観察しにくいコンポーネント固有の性質。テスト名は CT_SAMPLE.md の表と対応する。"""
from __future__ import annotations

import threading
from datetime import datetime

import pytest

from flowapprove.domain import State
from flowapprove.service import Authz, DecisionService, Store

pytestmark = pytest.mark.medium
VALID = {"製品名": "Example Editor", "提供元URL": "https://vendor.example/product", "利用バージョン": "1.2.3",
         "利用目的": "設計書の作成", "情報分類": "社内"}


def make(audit_fault=False):
    store, authz = Store(), Authz()
    for reviewer, org in (("審査者A", "組織A"), ("審査者C", "組織A"), ("審査者B", "組織B")):
        authz.grant(reviewer, org, "審査者")
    svc = DecisionService(store, authz, clock=lambda: datetime(2026, 9, 1))
    svc.create("申請者A", "APP-001", "組織A", dict(VALID))
    assert svc.submit("申請者A", "APP-001").ok
    store.audit_fault = audit_fault
    return svc, store


def snapshot(store):
    """障害注入テスト専用：ロールバックの完全性は公開インターフェースだけでは観測でき
    ない内部状態（保存済み結果の件数など）を含むため、ここだけは直接読む。"""
    app = store.apps["APP-001"]
    return (app.state, app.rev, len(store.audit), len(store.notes), len(store.results))


@pytest.mark.req("FR-014", "NVT-010", "ADR-0002")
def test_audit_failure_rolls_back_every_write():
    """NVT-010：監査記録の保存で失敗したら、状態・通知・要求の結果のどれも残らない。"""
    svc, store = make(audit_fault=True)
    before = snapshot(store)
    rev = svc.get("審査者A", "APP-001").rev
    result = svc.decide("審査者A", "APP-001", "承認", "規程を確認した", rev, "req-1")
    assert result.refusal == "一時的に処理不可" and snapshot(store) == before
    store.audit_fault = False                                                  # 復旧後は同じ要求で成立する
    assert svc.decide("審査者A", "APP-001", "承認", "規程を確認した", rev, "req-1").ok


@pytest.mark.req("FR-015", "FR-016", "ADR-0002")
def test_same_request_id_sent_concurrently_decides_and_notifies_once():
    svc, store = make()
    rev, gate, out = svc.get("審査者A", "APP-001").rev, threading.Barrier(8), []

    def send():
        gate.wait()
        out.append(svc.decide("審査者A", "APP-001", "承認", "規程を確認した", rev, "req-same"))

    threads = [threading.Thread(target=send) for _ in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert all(r.ok and r.state is State.APPROVED for r in out)                # 全員が最初と同じ結果を受け取る
    assert svc.history("審査者A", "APP-001", "承認") == 1
    assert svc.notifications("審査者A", "申請者A", "APP-001", "承認") == 1


# ---- CT-003：決裁の認可決定表（G-12：主体ごとに意味のある入力を使う。以前は
# 5主体×失効の有無の10通りのうち8通りが「そもそも権限を持ったことがない相手を
# 失効させる」という無意味な重複だった） ----
CT003_TABLE = [
    # (名前, 主体, 認可台帳への操作, 期待される許可)
    ("同じ組織の有効な審査者", "審査者A", ("grant", "組織A", "審査者"), True),
    ("同じ組織の失効した審査者", "審査者A", ("revoke", "組織A", "審査者"), False),
    ("他組織の有効な審査者", "審査者B", ("grant", "組織B", "審査者"), False),          # 組織が違う
    ("申請者本人（審査者の資格なし）", "申請者A", None, False),
    ("同じ組織の運用者（審査者ではない役割）", "運用者A", ("grant", "組織A", "運用者"), False),
    ("AI処理主体（いかなる資格も無い）", "AI処理主体", None, False),
]


@pytest.mark.req("FR-001", "FR-002", "NVT-002")
@pytest.mark.parametrize("name,actor,authz_op,allowed", CT003_TABLE, ids=[row[0] for row in CT003_TABLE])
def test_authorization_decision_table_for_decide(name, actor, authz_op, allowed):
    """NVT-002 のうち決裁操作の分岐。許可されるのは、失効していない同じ組織の審査者だけ。"""
    svc, store = make()
    if authz_op:
        op, org, role = authz_op
        getattr(svc.authz, op)(actor, org, role)
    rev = svc.get("審査者A", "APP-001").rev
    result = svc.decide(actor, "APP-001", "承認", "規程を確認した", rev, "req-1")
    assert result.ok is allowed
    if not allowed:
        assert (result.refusal, result.state, result.rev) == ("対象なし", None, None)
        assert svc.state_of("審査者C", "APP-001") is State.SUBMITTED   # 審査者Cはこの表のどの行でも変更されない


@pytest.mark.req("FR-008", "ADR-0001")
def test_ai_principal_has_no_path_to_decide():
    """ADR-0001 の確認：AI処理主体に審査者の資格が無い限り、決裁は成立しない。"""
    svc, store = make()
    assert not svc.authz.has("AI処理主体", "組織A", "審査者")
    rev = svc.get("審査者A", "APP-001").rev
    assert not svc.decide("AI処理主体", "APP-001", "承認", "自動承認", rev, "req-ai").ok
    assert svc.history("審査者A", "APP-001", "承認") == 0


# ---- G-01：編集できない状態（FR-005） ----
@pytest.mark.req("FR-005")
@pytest.mark.parametrize("action,expected_state", [("承認", State.APPROVED), ("却下", State.REJECTED)])
def test_edit_is_refused_after_decision(action, expected_state):
    svc, store = make()
    rev = svc.get("審査者A", "APP-001").rev
    assert svc.decide("審査者A", "APP-001", action, "規程を確認した", rev, "req-1").ok
    before = svc.get("審査者A", "APP-001")
    result = svc.edit("申請者A", "APP-001", {"利用目的": "書き換え"})
    assert not result.ok and result.refusal == "編集できない状態" and result.state is expected_state
    after = svc.get("審査者A", "APP-001")
    assert after.state is before.state and after.rev == before.rev              # 内容も版も変わらない


# ---- G-02：冪等キーは (主体, 申請, 操作, 要求識別子) ----
@pytest.mark.req("FR-015")
def test_replay_is_scoped_to_actor_app_and_action():
    """別主体・別申請・別操作が同じ要求識別子を使っても、再送とはみなされず通常どおり
    評価される（以前はグローバルな request_id だけで再送を判定していたため、審査者Cが
    審査者Aの決裁結果を横取りできた）。"""
    svc, store = make()
    svc.create("申請者A", "APP-002", "組織A", dict(VALID))
    assert svc.submit("申請者A", "APP-002").ok
    rev1 = svc.get("審査者A", "APP-001").rev
    first = svc.decide("審査者A", "APP-001", "承認", "規程を確認した", rev1, "req-shared")
    assert first.ok and first.state is State.APPROVED

    # 別の主体（審査者C）が同じ request_id で別申請（APP-002）を却下 → 再送ではなく通常評価
    rev2 = svc.get("審査者C", "APP-002").rev
    other_app = svc.decide("審査者C", "APP-002", "却下", "却下", rev2, "req-shared")
    assert other_app.ok and other_app.state is State.REJECTED

    # 別の主体（審査者C）が同じ request_id で同じ申請（APP-001）を操作 → 再送ではなく通常評価
    # （現行の版を渡しても APP-001 は既に APPROVED なので「決裁できない状態」になる。
    # SCN-047 と同じ組合せ）
    current_rev = svc.get("審査者C", "APP-001").rev
    same_app_other_actor = svc.decide("審査者C", "APP-001", "却下", "却下", current_rev, "req-shared")
    assert not same_app_other_actor.ok and same_app_other_actor.refusal == "決裁できない状態"

    # 別の操作（審査者A自身が却下を試みる）でも同じ request_id は再送にならない
    # （現行の版を渡しても既に APPROVED のため「決裁できない状態」。承認の結果は横取りされない）
    same_actor_other_action = svc.decide("審査者A", "APP-001", "却下", "却下", current_rev, "req-shared")
    assert not same_actor_other_action.ok and same_actor_other_action.refusal == "決裁できない状態"

    # 本来の（主体・申請・操作・識別子）が一致する再送だけが最初の結果を返す
    replay = svc.decide("審査者A", "APP-001", "承認", "別の理由", 999, "req-shared")
    assert replay == first


@pytest.mark.req("FR-015")
def test_replay_window_evicts_via_sweep():
    """RESEND_WINDOW を過ぎた保存済み結果は sweep で削除され、以後は新しい要求として
    扱われる（版が古ければ競合になる）。"""
    now = datetime(2026, 9, 1, 9, 0)
    clock = {"t": now}
    store, authz = Store(), Authz()
    authz.grant("審査者A", "組織A", "審査者")
    svc = DecisionService(store, authz, clock=lambda: clock["t"])
    svc.create("申請者A", "APP-001", "組織A", dict(VALID))
    assert svc.submit("申請者A", "APP-001").ok
    rev = svc.get("審査者A", "APP-001").rev
    first = svc.decide("審査者A", "APP-001", "承認", "規程を確認した", rev, "req-1")
    assert first.ok
    assert ("審査者A", "APP-001", "承認", "req-1") in store.results
    from datetime import timedelta
    clock["t"] = now + timedelta(hours=25)
    replay = svc.decide("審査者A", "APP-001", "承認", "規程を確認した", rev, "req-1")
    assert not replay.ok and replay.refusal == "競合"                            # 期限切れ後は新規要求として評価される
    assert ("審査者A", "APP-001", "承認", "req-1") not in store.results          # sweep で削除済み


# ---- G-03／G-04：偽装監査行と存在オラクルの排除 ----
@pytest.mark.req("FR-002", "FR-014")
def test_submit_does_not_forge_audit_rows_for_foreign_applications():
    """攻撃者が他人の申請オブジェクトを模して submit しても、保存済みの申請は変わらず、
    偽の監査行も残らない（以前は setdefault が呼び出し側のオブジェクトを素通りさせ、
    所有者検査の前に監査記録を書いていた）。"""
    svc, store = make()
    before_fields = dict(store.apps["APP-001"].fields)
    before_audit = list(store.audit)
    result = svc.submit("攻撃者", "APP-001")
    assert not result.ok and result.refusal == "対象なし"
    assert store.apps["APP-001"].fields == before_fields                        # 内容は変わらない
    assert store.audit == before_audit                                          # 偽の監査行が増えていない


@pytest.mark.req("FR-002")
def test_missing_and_foreign_app_id_are_indistinguishable():
    """存在しない申請と、他人が所有する申請は、edit・submit・decide のいずれでも
    byte-identical な Result を返す（存在の有無を推測できるオラクルにしない）。"""
    svc, store = make()
    rev = svc.get("審査者A", "APP-001").rev

    assert svc.edit("攻撃者", "APP-999", {"利用目的": "x"}) == svc.edit("攻撃者", "APP-001", {"利用目的": "x"})
    assert svc.submit("攻撃者", "APP-999") == svc.submit("攻撃者", "APP-001")
    assert (svc.decide("攻撃者", "APP-999", "承認", "x", rev, "req-x")
            == svc.decide("攻撃者", "APP-001", "承認", "x", rev, "req-x"))


@pytest.mark.req("FR-028")
def test_decide_with_invalid_action_is_bad_request():
    svc, store = make()
    rev = svc.get("審査者A", "APP-001").rev
    result = svc.decide("審査者A", "APP-001", "でたらめ", "規程を確認した", rev, "req-1")
    assert not result.ok and result.refusal == "入力不備"
    assert svc.state_of("審査者A", "APP-001") is State.SUBMITTED                 # 状態は変わらない


# ---- G-06：トランザクションはコピーに対して変更し、確定時にだけ入れ替える ----
@pytest.mark.req("FR-014")
def test_failed_transaction_does_not_mutate_the_original_object_in_place():
    """ロールバックが起きる前に取得しておいた Application 参照は、トランザクション
    失敗後も変更前の値のまま（コピーに対して変更し、成立したときだけ差し替えるため）。"""
    svc, store = make(audit_fault=True)
    held_reference = store.apps["APP-001"]
    before_state, before_rev = held_reference.state, held_reference.rev
    rev = svc.get("審査者A", "APP-001").rev
    result = svc.decide("審査者A", "APP-001", "承認", "規程を確認した", rev, "req-1")
    assert result.refusal == "一時的に処理不可"
    assert held_reference.state == before_state and held_reference.rev == before_rev


# ---- G-05：観察系（state_of・history・notifications）の認可 ----
@pytest.mark.req("FR-001", "FR-002")
def test_observers_return_none_for_unauthorized_actors():
    svc, store = make()
    assert svc.state_of("攻撃者", "APP-001") is None
    assert svc.history("攻撃者", "APP-001", "提出") is None
    assert svc.notifications("攻撃者", "申請者A", "APP-001", "承認") is None
    # 権限があれば同じ問い合わせが通常どおり答えを返す
    assert svc.state_of("審査者A", "APP-001") is State.SUBMITTED
    assert svc.history("審査者A", "APP-001", "提出") == 1


@pytest.mark.req("FR-005")
def test_edit_succeeds_on_a_fresh_draft_without_going_through_returned():
    svc, store = make()
    svc.create("申請者A", "APP-003", "組織A", dict(VALID))     # SUBMITTED を経由しない DRAFT
    result = svc.edit("申請者A", "APP-003", {"利用目的": "下書きの推敲"})
    assert result.ok and result.state is State.DRAFT and result.rev == 2
    assert svc.get("申請者A", "APP-003").rev == 2               # content_version は増えない（DRAFT 中の編集）


@pytest.mark.req("FR-003", "FR-004")
def test_submit_reports_violations_for_an_incomplete_draft():
    svc, store = make()
    svc.create("申請者A", "APP-003", "組織A", {"製品名": "Only Name"})
    result = svc.submit("申請者A", "APP-003")
    assert not result.ok and result.violations == ("提供元URL", "利用バージョン", "利用目的", "情報分類")
    assert svc.state_of("申請者A", "APP-003") is State.DRAFT     # 状態は変わらない
