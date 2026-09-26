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
EDITABLE = frozenset({State.DRAFT, State.RETURNED})
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


def is_editable(state: State) -> bool:
    """FR-005：編集できるのは DRAFT・RETURNED のときだけ。それ以外（SUBMITTED を含む
    終端状態）は編集を拒否する。"""
    return state in EDITABLE


# ---- 入力規則（PRD 10章） ----
MAX_LEN = {"製品名": 100, "利用バージョン": 50, "利用目的": 1000}
CLASSIFICATIONS = frozenset({"公開", "社内", "機密"})
REQUIRED = ("製品名", "提供元URL", "利用バージョン", "利用目的", "情報分類")


def normalize(text: str) -> str:
    """前後の空白を除き NFC に正規化する。文字数はこの結果のコードポイント数で数える。"""
    return unicodedata.normalize("NFC", text.strip())


URL_MAX_LEN = 2048


def valid_url(url: str) -> bool:
    if len(url) > URL_MAX_LEN:
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
    NOT_EDITABLE = "編集できない状態"   # FR-005：DRAFT・RETURNED 以外での編集要求
    INVALID = "入力不備"
    BAD_REQUEST = "入力不備"        # INVALID の別名。決裁対象の action 自体が不正なとき用（意図を読み手に示す）


# FR-029：この4つとして拒否された要求は、要求者・対象申請・拒否理由・時刻を対象申請の
# 組織の監査記録に残さなければならない（対象が存在しない場合を除く。§NVT-010）。
AUDITED_REFUSALS = frozenset({Refusal.NOT_FOUND, Refusal.SELF, Refusal.CONFLICT, Refusal.BAD_STATE})

REPLAY = "再送"    # 拒否理由ではなく、呼び出し側が保存済みの結果をそのまま返すべきという合図。
                   # Refusal に含めないのは、再送は本人には拒否として見えない（元の結果が
                   # 成功でも失敗でもそのまま返る）ため。


REASON_MAX_LEN = 1000


def valid_reason(reason: str) -> bool:
    return 1 <= len(normalize(reason)) <= REASON_MAX_LEN


def decision_refusal(*, permitted: bool, is_replay: bool, is_self: bool, rev_matches: bool, state: State,
                     action_valid: bool, reason: str) -> Refusal | str | None:
    """FR-028 の優先順位（対象なし・再送・自己決裁・競合・決裁できない状態・入力不備）で、
    最初に当たる項目を返す。'再送'（REPLAY）は拒否理由ではなく、呼び出し側が保存済みの
    結果を返すべきことを示す合図。該当なしは None（決裁を進めてよい）。"""
    if not permitted:
        return Refusal.NOT_FOUND
    if is_replay:
        return REPLAY
    if is_self:
        return Refusal.SELF
    if not rev_matches:
        return Refusal.CONFLICT
    if state is not State.SUBMITTED:
        return Refusal.BAD_STATE
    if not action_valid:
        return Refusal.BAD_REQUEST
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
