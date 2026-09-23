"""決裁サービス（CT の対象となるコンポーネント）。公開インターフェースは submit / edit / decide / history / notifications。

永続化は Store の背後に隠す。参考実装ではメモリ上のフェイクを使い、1トランザクションで
状態・監査記録・通知・要求の結果を確定する（ADR-0002 案A）。
"""
from __future__ import annotations

import copy
import threading
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime

from .domain import RESEND_WINDOW, Refusal, State, decision_refusal, next_state, violations


@dataclass
class Application:
    id: str
    org: str
    owner: str
    fields: dict[str, str]
    state: State = State.DRAFT
    content_version: int = 1
    rev: int = 1                      # 更新の版。決裁の競合検出に使う


@dataclass(frozen=True)
class Result:
    ok: bool
    state: State | None = None        # 権限のない相手には状態も返さない
    refusal: str | None = None
    rev: int | None = None


class TemporaryFailure(Exception):
    pass


@dataclass
class Store:
    """メモリ上のフェイク。transaction() は全部成立か全部不成立かを保証する。"""
    apps: dict[str, Application] = field(default_factory=dict)
    audit: list[dict] = field(default_factory=list)
    notes: list[dict] = field(default_factory=list)
    results: dict[str, tuple[Result, datetime]] = field(default_factory=dict)
    audit_fault: bool = False         # 障害注入：監査記録を保存できない
    _lock: threading.RLock = field(default_factory=threading.RLock, repr=False)

    @contextmanager
    def transaction(self):
        with self._lock:
            snapshot = copy.deepcopy((self.apps, self.audit, self.notes, self.results))
            try:
                yield self
            except Exception:
                self.apps, self.audit, self.notes, self.results = snapshot
                raise

    def append_audit(self, **row):
        if self.audit_fault:
            raise TemporaryFailure("監査記録を保存できない")
        self.audit.append(row)


class Authz:
    """認可台帳のフェイク。処理する時点の登録内容で判定する。"""

    def __init__(self):
        self._grants: set[tuple[str, str, str]] = set()   # (主体, 組織, 役割)

    def grant(self, actor, org, role):
        self._grants.add((actor, org, role))

    def revoke(self, actor, org, role):
        self._grants.discard((actor, org, role))

    def has(self, actor, org, role) -> bool:
        return (actor, org, role) in self._grants


class DecisionService:
    def __init__(self, store: Store, authz: Authz, clock):
        self.store, self.authz, self.clock = store, authz, clock

    # --- 申請者の操作（CT の前提づくりにも使う） ---
    def submit(self, actor: str, app: Application) -> list[str]:
        bad = violations(app.fields)
        with self.store.transaction() as s:
            s.apps.setdefault(app.id, app)
            if app.owner != actor or bad:
                return bad or ["権限"]
            app.state = next_state(app.state, "提出")
            app.rev += 1
            s.append_audit(app=app.id, actor=actor, action="提出", content_version=app.content_version, at=self.clock())
        return []

    def edit(self, actor: str, app_id: str, fields: dict[str, str]) -> Result:
        with self.store.transaction() as s:
            app = s.apps[app_id]
            if app.owner != actor:
                return Result(False, refusal=Refusal.NOT_FOUND.value)
            if app.state is State.SUBMITTED:
                return Result(False, app.state, "提出済みのため編集不可", app.rev)
            app.fields.update(fields)
            if app.state is State.RETURNED:
                app.state = next_state(app.state, "修正")
                app.content_version += 1
            app.rev += 1
            return Result(True, app.state, rev=app.rev)

    # --- 決裁 ---
    def decide(self, actor: str, app_id: str, action: str, reason: str, seen_rev: int, request_id: str) -> Result:
        try:
            with self.store.transaction() as s:
                app = s.apps.get(app_id)
                permitted = app is not None and self.authz.has(actor, app.org, "審査者")
                if permitted and request_id in s.results:                    # 再送：認可を再検査した後でだけ結果を返す
                    saved, at = s.results[request_id]
                    if self.clock() - at <= RESEND_WINDOW:
                        return saved
                refusal = decision_refusal(permitted=permitted, is_self=permitted and app.owner == actor,
                                           rev_matches=permitted and app.rev == seen_rev,
                                           state=app.state if permitted else State.DRAFT, reason=reason)
                if refusal:
                    visible = refusal is not Refusal.NOT_FOUND
                    return Result(False, app.state if visible else None, refusal.value, app.rev if visible else None)
                app.state = next_state(app.state, action)
                app.rev += 1
                now = self.clock()
                s.append_audit(app=app.id, actor=actor, action=action, content_version=app.content_version, at=now)
                s.notes.append({"to": app.owner, "app": app.id, "kind": action, "at": now})
                result = Result(True, app.state, rev=app.rev)
                s.results[request_id] = (result, now)
                return result
        except TemporaryFailure:
            return Result(False, refusal="一時的に処理不可")

    # --- 観察 ---
    def state_of(self, app_id: str) -> State:
        return self.store.apps[app_id].state

    def history(self, app_id: str, action: str) -> int:
        return sum(1 for r in self.store.audit if r["app"] == app_id and r["action"] == action)

    def notifications(self, to: str, app_id: str, kind: str) -> int:
        return sum(1 for n in self.store.notes if (n["to"], n["app"], n["kind"]) == (to, app_id, kind))

