"""CT：BDD では観察しにくいコンポーネント固有の性質。テスト名は CT_SAMPLE.md の表と対応する。"""
from __future__ import annotations

import itertools
import threading
from datetime import datetime

import pytest

from flowapprove.domain import State
from flowapprove.service import Application, Authz, DecisionService, Store

pytestmark = pytest.mark.medium
VALID = {"製品名": "Example Editor", "提供元URL": "https://vendor.example/product", "利用バージョン": "1.2.3",
         "利用目的": "設計書の作成", "情報分類": "社内"}


def make(audit_fault=False):
    store, authz = Store(), Authz()
    for reviewer, org in (("審査者A", "組織A"), ("審査者C", "組織A"), ("審査者B", "組織B")):
        authz.grant(reviewer, org, "審査者")
    svc = DecisionService(store, authz, clock=lambda: datetime(2026, 9, 1))
    assert svc.submit("申請者A", Application("APP-001", "組織A", "申請者A", dict(VALID))) == []
    store.audit_fault = audit_fault
    return svc, store


def snapshot(store):
    app = store.apps["APP-001"]
    return (app.state, app.rev, len(store.audit), len(store.notes), len(store.results))


@pytest.mark.req("FR-014", "NVT-010", "ADR-0002")
def test_audit_failure_rolls_back_every_write():
    """NVT-010：監査記録の保存で失敗したら、状態・通知・要求の結果のどれも残らない。"""
    svc, store = make(audit_fault=True)
    before = snapshot(store)
    result = svc.decide("審査者A", "APP-001", "承認", "規程を確認した", store.apps["APP-001"].rev, "req-1")
    assert result.refusal == "一時的に処理不可" and snapshot(store) == before
    store.audit_fault = False                                                  # 復旧後は同じ要求で成立する
    assert svc.decide("審査者A", "APP-001", "承認", "規程を確認した", store.apps["APP-001"].rev, "req-1").ok


@pytest.mark.req("FR-015", "FR-016", "ADR-0002")
def test_same_request_id_sent_concurrently_decides_and_notifies_once():
    svc, store = make()
    rev, gate, out = store.apps["APP-001"].rev, threading.Barrier(8), []

    def send():
        gate.wait()
        out.append(svc.decide("審査者A", "APP-001", "承認", "規程を確認した", rev, "req-same"))

    threads = [threading.Thread(target=send) for _ in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert all(r.ok and r.state is State.APPROVED for r in out)                # 全員が最初と同じ結果を受け取る
    assert svc.history("APP-001", "承認") == 1 and svc.notifications("申請者A", "APP-001", "承認") == 1


@pytest.mark.req("FR-001", "FR-002", "NVT-002")
@pytest.mark.parametrize("actor,revoked", list(itertools.product(["審査者A", "審査者B", "申請者A", "運用者A", "AI処理主体"], [False, True])))
def test_authorization_decision_table_for_decide(actor, revoked):
    """NVT-002 のうち決裁操作の分岐。許可されるのは、失効していない同じ組織の審査者だけ。"""
    svc, store = make()
    if revoked:
        svc.authz.revoke(actor, "組織A", "審査者")
    result = svc.decide(actor, "APP-001", "承認", "規程を確認した", store.apps["APP-001"].rev, "req-1")
    allowed = actor == "審査者A" and not revoked
    assert result.ok is allowed
    if not allowed:
        assert (result.refusal, result.state, result.rev) == ("対象なし", None, None)
        assert svc.state_of("APP-001") is State.SUBMITTED


@pytest.mark.req("FR-008", "ADR-0001")
def test_ai_principal_has_no_path_to_decide():
    """ADR-0001 の確認：AI処理主体に審査者の資格が無い限り、決裁は成立しない。"""
    svc, store = make()
    assert not svc.authz.has("AI処理主体", "組織A", "審査者")
    assert not svc.decide("AI処理主体", "APP-001", "承認", "自動承認", store.apps["APP-001"].rev, "req-ai").ok
    assert svc.history("APP-001", "承認") == 0
