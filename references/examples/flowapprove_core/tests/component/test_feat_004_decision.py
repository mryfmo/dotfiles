"""CT：決裁サービスを公開インターフェース越しに、BDD の FEAT-004 をそのまま実行する。

.feature は BDD_SAMPLE.md から生成されたもの（手で編集しない）。依存はプロセス内のフェイクに
差し替える（medium サイズ）。試験上の仕掛け（時計・同時到着・障害注入）はここに置き、Gherkin には書かない。
"""
from __future__ import annotations

import threading
from datetime import datetime, timedelta

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from flowapprove.domain import State
from flowapprove.service import Application, Authz, DecisionService, Store

pytestmark = [pytest.mark.medium, pytest.mark.req("FR-011", "FR-012", "FR-013", "FR-014", "FR-015", "FR-028", "ADR-0002")]
scenarios("FEAT-004.feature")

VALID = {"製品名": "Example Editor", "提供元URL": "https://vendor.example/product", "利用バージョン": "1.2.3",
         "利用目的": "設計書の作成", "情報分類": "社内"}
DEFAULT_REASON = "規程を確認した"


class World:
    def __init__(self):
        self.now = datetime(2026, 9, 1, 9, 0)
        self.store, self.authz = Store(), Authz()
        self.svc = DecisionService(self.store, self.authz, clock=lambda: self.now)
        self.results: list = []          # 直近の「もし」で得た応答
        self.opened_rev: dict[tuple[str, str], int] = {}
        self.last_request: dict | None = None
        self.seq = 0

    def new_request_id(self) -> str:
        self.seq += 1
        return f"req-{self.seq}"

    def decide(self, actor, app_id, action, reason=DEFAULT_REASON, seen_rev=None, request_id=None):
        seen = self.store.apps[app_id].rev if seen_rev is None else seen_rev
        self.last_request = dict(actor=actor, app_id=app_id, action=action, reason=reason, seen_rev=seen,
                                 request_id=request_id or self.new_request_id())
        result = self.svc.decide(**self.last_request)
        self.results = [result]
        return result


@pytest.fixture
def w() -> World:
    return World()


# ---------- 前提 ----------
@given("組織Aに申請者Aと審査者Aと審査者Cと監査者Aがいる")
def _org_a(w):
    for reviewer in ("審査者A", "審査者C"):
        w.authz.grant(reviewer, "組織A", "審査者")


@given("組織Bに審査者Bがいる")
def _org_b(w):
    w.authz.grant("審査者B", "組織B", "審査者")


@given(parsers.re(r'(?P<owner>申請者A|審査者A)が提出した申請 "(?P<app_id>[^"]+)" がある'))
def _submitted(w, owner, app_id):
    assert w.svc.submit(owner, Application(app_id, "組織A", owner, dict(VALID))) == []
    w.opened_rev[("審査者A", app_id)] = w.opened_rev[("審査者C", app_id)] = w.store.apps[app_id].rev


@given(parsers.re(r'審査者Aは申請 "(?P<app_id>[^"]+)" を承認済みである'))
def _approved(w, app_id):
    _submitted(w, "申請者A", app_id)
    assert w.decide("審査者A", app_id, "承認").ok


@given(parsers.re(r'申請 "(?P<app_id>[^"]+)" は審査者Aが開いた後に更新されている'))
def _updated_after_open(w, app_id):
    assert w.decide("審査者C", app_id, "差戻し", "情報が足りない").ok          # 差戻し→修正→再提出で版が進む
    assert w.svc.edit("申請者A", app_id, {"利用目的": "設計書と議事録の作成"}).ok
    assert w.svc.submit("申請者A", w.store.apps[app_id]) == []


@given("監査記録を保存できない障害が起きている")
def _audit_fault(w):
    w.store.audit_fault = True


@given("審査者Aはその承認の応答を受け取っていない")
def _response_lost(w):
    w.results = []                                                             # 応答を捨てる。要求の識別子は手元に残る


@given("審査者Aの審査権限は認可台帳で失効している")
def _revoked(w):
    w.authz.revoke("審査者A", "組織A", "審査者")


@given(parsers.re(r"承認から (?P<hours>\d+) 時間が経過している"))
def _hours_later(w, hours):
    w.now += timedelta(hours=int(hours))


# ---------- もし ----------
@when(parsers.re(r'(?P<actor>審査者[A-C])が申請 "(?P<app_id>[^"]+)" を理由 "(?P<reason>[^"]*)" で(?P<action>承認|却下|差戻し)する'))
def _decide(w, actor, app_id, reason, action):
    w.decide(actor, app_id, action, reason)


@when(parsers.re(r'審査者Aが申請 "(?P<app_id>[^"]+)" を「あ」を (?P<n>\d+) 個並べた理由で承認する'))
def _decide_with_reason_length(w, app_id, n):
    w.decide("審査者A", app_id, "承認", "あ" * int(n))


@when(parsers.re(r'(?P<actor>審査者[AC])が(?:承認の前に)?開いた時点の版を指定して申請 "(?P<app_id>[^"]+)" を(?P<action>承認|却下)する'))
def _decide_with_opened_rev(w, actor, app_id, action):
    w.decide(actor, app_id, action, seen_rev=w.opened_rev[(actor, app_id)])


@when(parsers.re(r'審査者Aの承認と審査者Cの却下が同じ版の申請 "(?P<app_id>[^"]+)" に同時に届く'))
def _concurrent(w, app_id):
    rev, gate, out = w.store.apps[app_id].rev, threading.Barrier(2), []

    def send(actor, action):
        gate.wait()                                                            # 2つの要求を同時に解放する
        out.append(w.svc.decide(actor, app_id, action, DEFAULT_REASON, rev, w.new_request_id()))

    threads = [threading.Thread(target=send, args=a) for a in (("審査者A", "承認"), ("審査者C", "却下"))]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    w.results = out


@when("審査者Aが同じ承認の要求を再送する")
def _resend(w):
    w.results = [w.svc.decide(**w.last_request)]


# ---------- ならば ----------
@then(parsers.re(r'申請 "(?P<app_id>[^"]+)" の状態は "(?P<state>[A-Z]+)" である'))
def _state_is(w, app_id, state):
    assert w.svc.state_of(app_id) is State(state)


@then(parsers.re(r'監査者Aは申請 "(?P<app_id>[^"]+)" の履歴に "(?P<action>[^"]+)" を (?P<n>\d+) 件確認できる'))
def _history(w, app_id, action, n):
    assert w.svc.history(app_id, action) == int(n)


@then(parsers.re(r'要求は "(?P<reason>[^"]+)" として拒否される'))
def _refused(w, reason):
    (result,) = w.results
    assert not result.ok and result.refusal == reason
    if reason == "対象なし":
        assert result.state is None and result.rev is None                     # 状態も版も明かさない


@then("審査者Aに再読込の案内が表示される")
def _reload_hint(w):
    (result,) = w.results
    assert result.refusal == "競合" and result.rev is not None                  # 現行の版を返し、再読込できる


@then(parsers.re(r"成立する決裁はちょうど (?P<n>\d+) 件である"))
def _exactly_n(w, n):
    assert sum(r.ok for r in w.results) == int(n)


@then(parsers.re(r'成立しなかった要求は "(?P<reason>[^"]+)" として拒否される'))
def _loser_refused(w, reason):
    assert [r.refusal for r in w.results if not r.ok] == [reason]


@then(parsers.re(r'申請 "(?P<app_id>[^"]+)" の状態は成立した決裁と一致する'))
def _state_matches_winner(w, app_id):
    (winner,) = [r for r in w.results if r.ok]
    assert w.svc.state_of(app_id) is winner.state


@then("審査者Aに最初の承認の結果が表示される")
def _first_result(w):
    (result,) = w.results
    assert result.ok and result.state is State.APPROVED
