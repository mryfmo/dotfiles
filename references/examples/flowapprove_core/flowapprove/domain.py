"""純粋なドメイン規則。入出力・時計・乱数に触れない（UT の対象）。"""
from __future__ import annotations

import unicodedata
from datetime import datetime, timedelta
from enum import Enum
from urllib.parse import urlsplit


class State(str, Enum):
    DRAFT = "DRAFT"
    SUBMITTED = "SUBMITTED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    RETURNED = "RETURNED"
    WITHDRAWN = "WITHDRAWN"


TERMINAL = frozenset({State.APPROVED, State.REJECTED, State.WITHDRAWN})
DECISIONS = {"承認": State.APPROVED, "却下": State.REJECTED, "差戻し": State.RETURNED}

# (現状態, 出来事) -> 次状態。PRD 6章の状態表と1対1に対応する。
TRANSITIONS: dict[tuple[State, str], State] = {
    (State.DRAFT, "提出"): State.SUBMITTED,
    (State.SUBMITTED, "承認"): State.APPROVED,
    (State.SUBMITTED, "却下"): State.REJECTED,
    (State.SUBMITTED, "差戻し"): State.RETURNED,
    (State.RETURNED, "修正"): State.DRAFT,
    (State.DRAFT, "取消"): State.WITHDRAWN,
    (State.SUBMITTED, "取消"): State.WITHDRAWN,
    (State.RETURNED, "取消"): State.WITHDRAWN,
}
EVENTS = ("提出", "承認", "却下", "差戻し", "修正", "取消")


class NotAllowed(Exception):
    """状態表にない遷移。"""


def next_state(state: State, event: str) -> State:
    try:
        return TRANSITIONS[(state, event)]
    except KeyError:
        raise NotAllowed(f"{state.value} で {event} はできない") from None


# ---- 入力規則（PRD 10章） ----
MAX_LEN = {"製品名": 100, "利用バージョン": 50, "利用目的": 1000}
CLASSIFICATIONS = frozenset({"公開", "社内", "機密"})
REQUIRED = ("製品名", "提供元URL", "利用バージョン", "利用目的", "情報分類")


def normalize(text: str) -> str:
    """前後の空白を除き NFC に正規化する。文字数はこの結果のコードポイント数で数える。"""
    return unicodedata.normalize("NFC", text.strip())


def valid_url(url: str) -> bool:
    if len(url) > 2048:
        return False
    try:
        parts = urlsplit(url)
    except ValueError:
        return False
    return parts.scheme == "https" and bool(parts.hostname) and parts.username is None and parts.password is None


def violations(fields: dict[str, str]) -> list[str]:
    """入力規則に違反した項目名を、REQUIRED の順で返す。空リストなら提出できる。"""
    bad = []
    for name in REQUIRED:
        value = normalize(fields.get(name, ""))
        if not value:
            bad.append(name)
        elif name in MAX_LEN and len(value) > MAX_LEN[name]:
            bad.append(name)
        elif name == "提供元URL" and not valid_url(value):
            bad.append(name)
        elif name == "情報分類" and value not in CLASSIFICATIONS:
            bad.append(name)
    return bad


# ---- 決裁の拒否理由（FR-028 の優先順位） ----
class Refusal(str, Enum):
    NOT_FOUND = "対象なし"
    SELF = "自己決裁"
    CONFLICT = "競合"
    BAD_STATE = "決裁できない状態"
    INVALID = "入力不備"


def valid_reason(reason: str) -> bool:
    return 1 <= len(normalize(reason)) <= 1000


def decision_refusal(*, permitted: bool, is_self: bool, rev_matches: bool, state: State, reason: str) -> Refusal | None:
    """複数の拒否条件に当たるとき、FR-028 の順で最初に当たる理由だけを返す。"""
    if not permitted:
        return Refusal.NOT_FOUND
    if is_self:
        return Refusal.SELF
    if not rev_matches:
        return Refusal.CONFLICT
    if state is not State.SUBMITTED:
        return Refusal.BAD_STATE
    if not valid_reason(reason):
        return Refusal.INVALID
    return None


# ---- 期限（FR-021〜FR-023） ----
RETENTION = timedelta(days=90)
AUTO_WITHDRAW = timedelta(days=180)
NOTICE = timedelta(days=166)
RESEND_WINDOW = timedelta(hours=24)


def deletion_due(terminal_at: datetime, now: datetime) -> bool:
    return now - terminal_at >= RETENTION


def auto_withdraw_due(state: State, last_updated: datetime, now: datetime) -> bool:
    return state not in TERMINAL and now - last_updated >= AUTO_WITHDRAW


def notice_due(state: State, last_updated: datetime, now: datetime) -> bool:
    return state not in TERMINAL and NOTICE <= now - last_updated < AUTO_WITHDRAW
