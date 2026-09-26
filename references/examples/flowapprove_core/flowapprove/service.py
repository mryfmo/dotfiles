"""決裁サービス（CT の対象となるコンポーネント）。公開インターフェースは create / submit / edit /
decide / get / state_of / history / notifications。

永続化は Store の背後に隠す。参考実装ではメモリ上のフェイクを使い、1トランザクションで
状態・監査記録・通知・要求の結果を確定する（ADR-0002 案A）。トランザクション内の変更は
Application のコピーに対して行い、確定時（成功時）にだけ Store の該当エントリを差し替える。
呼び出し側が保持するオブジェクトへの別名（エイリアス）を経由した書き換えを防ぐため（G-06）。
"""
from __future__ import annotations

import copy
import threading
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime

from .domain import (AUDITED_REFUSALS, DECISIONS, REPLAY, RESEND_WINDOW, Refusal, State, decision_refusal,
                     is_editable, next_state, violations)


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
    violations: tuple[str, ...] = ()  # submit の入力規則違反（成功時・NOT_FOUND 時は空）


class TemporaryFailure(Exception):
    pass


IdempotencyKey = tuple[str, str, str, str]   # (actor, app_id, action, request_id) — PRD 10章「同じ決裁要求」


@dataclass
class Store:
    """メモリ上のフェイク。transaction() は全部成立か全部不成立かを保証する。"""
    apps: dict[str, Application] = field(default_factory=dict)
    audit: list[dict] = field(default_factory=list)
    notes: list[dict] = field(default_factory=list)
    results: dict[IdempotencyKey, tuple[Result, datetime]] = field(default_factory=dict)
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

    def sweep(self, now: datetime) -> None:
        """RESEND_WINDOW を過ぎた保存済みの決裁結果を削除する（G-02：無期限に増え続けない）。"""
        stale = [key for key, (_, at) in self.results.items() if now - at > RESEND_WINDOW]
        for key in stale:
            del self.results[key]


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

    def _visible(self, actor: str, app: Application) -> bool:
        """他組織や無許可の相手には申請が見えない（RULE-003／FR-002）。所有者本人、同じ
        組織の審査者、同じ組織の監査者（追跡用）だけが見られる。"""
        if app.owner == actor:
            return True
        return self.authz.has(actor, app.org, "審査者") or self.authz.has(actor, app.org, "監査者")

    # --- 申請者の操作 ---
    def create(self, actor: str, app_id: str, org: str, fields: dict[str, str]) -> None:
        """新規 DRAFT を申請者本人の所有で保存する。呼び出し側の Application は受け取らない
        （G-03：他人の申請に監査行を偽造できた原因は、呼び出し側が渡すオブジェクトを
        そのまま保存していたこと）。"""
        with self.store.transaction() as s:
            s.apps[app_id] = Application(app_id, org, actor, dict(fields))

    def submit(self, actor: str, app_id: str) -> Result:
        with self.store.transaction() as s:
            original = s.apps.get(app_id)
            if original is None or original.owner != actor:
                return Result(False, refusal=Refusal.NOT_FOUND.value)   # 存在しない・他人の申請は区別しない
            bad = violations(original.fields)
            if bad:
                return Result(False, original.state, violations=tuple(bad))
            app = copy.deepcopy(original)
            app.state = next_state(app.state, "提出")
            app.rev += 1
            s.append_audit(app=app.id, actor=actor, action="提出", content_version=app.content_version, at=self.clock())
            s.apps[app_id] = app
            return Result(True, app.state, rev=app.rev)

    def edit(self, actor: str, app_id: str, fields: dict[str, str]) -> Result:
        with self.store.transaction() as s:
            original = s.apps.get(app_id)
            if original is None or original.owner != actor:
                return Result(False, refusal=Refusal.NOT_FOUND.value)
            if not is_editable(original.state):
                return Result(False, original.state, Refusal.NOT_EDITABLE.value, original.rev)
            app = copy.deepcopy(original)
            app.fields.update(fields)
            if app.state is State.RETURNED:
                app.state = next_state(app.state, "修正")
                app.content_version += 1
            app.rev += 1
            s.apps[app_id] = app
            return Result(True, app.state, rev=app.rev)

    # --- 決裁 ---
    def decide(self, actor: str, app_id: str, action: str, reason: str, seen_rev: int | None, request_id: str) -> Result:
        try:
            with self.store.transaction() as s:
                now = self.clock()
                s.sweep(now)
                app = s.apps.get(app_id)
                permitted = app is not None and self.authz.has(actor, app.org, "審査者")
                key: IdempotencyKey = (actor, app_id, action, request_id)   # PRD 10章「同じ決裁要求」
                is_replay = permitted and key in s.results and now - s.results[key][1] <= RESEND_WINDOW
                verdict = decision_refusal(permitted=permitted, is_replay=is_replay,
                                           is_self=permitted and app.owner == actor,
                                           rev_matches=permitted and app.rev == seen_rev,
                                           state=app.state if permitted else State.DRAFT,
                                           action_valid=action in DECISIONS, reason=reason)
                if verdict == REPLAY:
                    return s.results[key][0]
                if verdict:
                    if app is not None and verdict in AUDITED_REFUSALS:   # FR-029
                        s.append_audit(app=app.id, actor=actor, action=verdict.value,
                                       content_version=app.content_version, at=now)
                    visible = verdict is not Refusal.NOT_FOUND
                    return Result(False, app.state if visible else None, verdict.value, app.rev if visible else None)
                new_app = copy.deepcopy(app)
                new_app.state = next_state(app.state, action)
                new_app.rev += 1
                s.append_audit(app=app.id, actor=actor, action=action, content_version=app.content_version, at=now)
                s.notes.append({"to": app.owner, "app": app.id, "kind": action, "at": now})
                result = Result(True, new_app.state, rev=new_app.rev)
                s.apps[app_id] = new_app
                s.results[key] = (result, now)
                return result
        except TemporaryFailure:
            return Result(False, refusal="一時的に処理不可")

    # --- 観察 ---
    def get(self, actor: str, app_id: str) -> Result:
        """state と rev を公開インターフェース越しに取得する（G-10：テストがストア内部を
        直接読まなくて済むように）。"""
        with self.store.transaction() as s:
            app = s.apps.get(app_id)
            if app is None or not self._visible(actor, app):
                return Result(False, refusal=Refusal.NOT_FOUND.value)
            return Result(True, app.state, rev=app.rev)

    def state_of(self, actor: str, app_id: str) -> State | None:
        with self.store.transaction() as s:
            app = s.apps.get(app_id)
            if app is None or not self._visible(actor, app):
                return None
            return app.state

    def history(self, actor: str, app_id: str, action: str) -> int | None:
        with self.store.transaction() as s:
            app = s.apps.get(app_id)
            if app is None or not self._visible(actor, app):
                return None
            return sum(1 for r in s.audit if r["app"] == app_id and r["action"] == action)

    def notifications(self, actor: str, to: str, app_id: str, kind: str) -> int | None:
        with self.store.transaction() as s:
            app = s.apps.get(app_id)
            if app is None or not self._visible(actor, app):
                return None
            return sum(1 for n in s.notes if (n["to"], n["app"], n["kind"]) == (to, app_id, kind))
