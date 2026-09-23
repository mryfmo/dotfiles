---
doc_type: ut
sample: true
id: "TEST-UT-001"
title: "FlowApprove：ドメイン規則（入力規則・状態遷移・拒否理由・期限）"
status: draft
version: "0.2.0"
owner: "（架空）技術責任者"
updated: "2026-09-19"
requirements: "../prd/PRD_SAMPLE.md 版0.4.0"
bdd: "../bdd/BDD_SAMPLE.md 版0.4.0"
target: "../examples/flowapprove_core/flowapprove/domain.py（参考実装。版は証跡のハッシュで特定）"
automation: implemented
last_run: passed
evidence: "../evidence/example_tests.json"
---
# UT 設計：FlowApprove のドメイン規則

> **記入例。** 対象は、UT と CT の記入例を実際に実行できるようにするための最小の参考実装であり、製品ではない。下の「直近の結果」は、この参考実装に対して実際に実行した結果である。組織名と合意者は架空。テンプレートは [UT_TEMPLATE.md](UT_TEMPLATE.md)。

## 1. 対象と正本

| 項目 | 内容 |
|---|---|
| 対象 | 入力規則（正規化・長さ・URL・情報分類）、状態遷移、決裁の拒否理由の優先順位、保存期限と自動取消の判定。いずれも入出力を持たない純粋な関数 |
| 対象外 | 認可台帳の参照、トランザクション、同時実行、再送、通知（CT で確かめる）。画面（E2E）。FR-005（提出前後の編集拒否）はP6でUTに追加予定。FR-009（AI応答のタイムアウト時の扱い）はCTで代役のタイムアウトを注入して確かめる（未実装）。FR-026（時刻の記録）はNVT-011（CTで実施予定、現時点は未自動化）で確かめる |
| 由来 | FR-003・FR-004・FR-011・FR-018〜FR-023・FR-028、RULE-001・RULE-017・RULE-018・RULE-019・RULE-023 |
| テストコードの場所 | `examples/flowapprove_core/tests/unit/test_domain.py` |
| 実行方法 | `python tools/run_examples.py --mutation`（内部で pytest・coverage.py・mutmut を実行） |

## 2. この水準で確かめること・上へ送ること

| 観点 | UT で確かめる | 上の水準へ送る（送り先と理由） |
|---|---|---|
| 入力規則の境界と組合せ | 必須5項目×空白3種、長さの境界3項目、URL 9例、情報分類、正規化の性質 | BDD の SCN-002〜SCN-005 を CT で代表例として実行 |
| 状態遷移 | 状態6×出来事6の全36通り、終端状態から動かないこと | 遷移に伴う監査記録と通知は CT |
| 拒否理由の優先順位 | 5条件の全32通り | BDD では SCN-041・SCN-042 の2例だけ。組合せを Gherkin に書くと読めなくなる |
| 期限 | 89・90日、165・166・179・180日の境界 | 時間の経過による削除と自動取消の実行は CT と ST（NVT-009） |
| 認可・永続化・同時実行 | — | CT。認可台帳と保存先が要るため |

## 3. テスト設計

| ID | 対象 | 確かめる振る舞い | 技法 | 由来 | テスト名 |
|---|---|---|---|---|---|
| UT-001 | `violations` | 5項目が有効な下書きには違反が無い | 例示 | FR-003 | `test_valid_draft_has_no_violations` |
| UT-002 | `violations` | 必須5項目のどれが空・空白・全角空白でも、その項目名だけが報告される | 同値分割 | FR-004、RULE-001 | `test_blank_required_field_is_reported` |
| UT-003 | `violations` | 製品名100・利用バージョン50・利用目的1000文字は通り、1文字超えると報告される | 境界値 | FR-003、FR-004 | `test_length_boundary` |
| UT-004 | `violations` | 分解形で200コードポイントの文字列が、正規化後100文字として通る | 例示 | FR-003、SCN-004 | `test_length_is_counted_after_nfc_normalization` |
| UT-005 | `violations` | 任意の文字列について、長さの判定は正規化後の文字数だけで決まる | プロパティ | FR-003 | `test_length_rule_depends_only_on_normalized_text` |
| UT-006 | `normalize` | 正規化を2回かけても結果が変わらない | プロパティ | FR-003 | `test_normalize_is_idempotent` |
| UT-007 | `valid_url` | https 以外、ユーザー情報つき、ホストなし、解析不能、2049文字は不可。2048文字は可 | 同値分割・境界値 | FR-004、SCN-005 | `test_url_rule` |
| UT-008 | `violations` | 不正な URL が「提供元URL」として報告される | 例示（ミューテーションテストで見つかった穴） | FR-004 | `test_invalid_url_is_reported_as_the_url_field` |
| UT-009 | `violations` | 情報分類は公開・社内・機密だけが通り、それ以外は「情報分類」として報告される | 同値分割 | FR-004 | `test_classification_is_a_closed_set` |
| UT-010 | `violations` | 複数の違反は項目の定義順に全件報告される | 例示 | FR-004 | `test_all_violations_are_reported_in_field_order` |
| UT-011 | `next_state` | 状態×出来事の全36通りで、状態表にある組だけが遷移し、他は拒否される | 状態遷移（全数） | FR-011、FR-018、FR-019、FR-020 | `test_transition_table_is_exhaustive` |
| UT-012 | `next_state` | どんな順で出来事を与えても、終端状態に入った後は状態が変わらない | 状態機械のプロパティ | FR-020、RULE-017 | `test_terminal_states_are_absorbing` |
| UT-013 | `decision_refusal` | 5つの拒否条件の全32通りで、当たった条件のうち優先順位が最も高い理由だけが返る | 決定表（全数） | FR-028、RULE-023、FR-002、FR-012、FR-013 | `test_refusal_precedence_decision_table` |
| UT-014 | `decision_refusal` | SUBMITTED 以外の5状態はすべて「決裁できない状態」になる | 同値分割 | FR-020、RULE-017 | `test_only_submitted_can_be_decided` |
| UT-015 | `decision_refusal` | 理由は0文字と1001文字が不可、1文字と1000文字が可 | 境界値 | FR-011、SCN-018 | `test_reason_length_boundary` |
| UT-016 | `deletion_due` | 終端から89日は対象外、90日から削除対象 | 境界値 | FR-021、RULE-018 | `test_deletion_due_boundary` |
| UT-017 | `notice_due`・`auto_withdraw_due` | 165日は何も起きず、166〜179日は予告、180日で自動取消 | 境界値 | FR-022、FR-023、RULE-019 | `test_notice_and_auto_withdraw_boundaries` |
| UT-018 | `auto_withdraw_due` | 終端状態の申請は、どれだけ時間が経っても自動取消にも予告にもならない | 同値分割 | FR-022 | `test_terminal_applications_are_never_auto_withdrawn` |

## 4. テストダブルと決定性

| 依存 | 扱い | 理由 |
|---|---|---|
| ドメイン内の関数どうし | 実物 | 速く決定的。置き換えると、呼び出しの形に縛られたテストになる |
| 現在時刻 | 引数で渡す（関数は時計を読まない） | 期限の境界を実時間で待たずに確かめる |
| プロパティベーステストの乱数 | Hypothesis が失敗例を最小化して保存・再現する。再現性が保証されるのは `conftest.py` にプロファイル `kit`（乱数の固定とデータベース設定）を追加した後（6章）で、本参考実装には未導入 | 失敗を再現できる（プロファイル `kit` 導入後） |
| 認可台帳・保存先 | UT では触れない | small を保つ。CT で確かめる |

## 5. 十分性の基準

| 指標 | 基準 | 測り方 | 基準に届かないとき |
|---|---|---|---|
| 由来の網羅 | 1章の由来のすべてに、3章のテスト条件がある | `kit_lint.py check` と追跡表 | テスト条件を足すか、2章に送り先を書く |
| 分岐カバレッジ | `domain.py` で 95% 以上。未テストの箇所を見つける手段であって目的ではない | coverage.py（分岐） | 未実行の分岐を読み、要るテストか不要なコードかを判断 |
| ミューテーションスコア | `domain.py` で 90% 以上。生き残りは全件を確認する | mutmut | テストを強めるか、理由を書いて受け入れる |
| 実行時間 | UT 全体の所要時間は証跡 `durations` を参照 | 実行記録 | 遅いテストを分割するか CT へ移す |

## 6. 実行と証跡

| 項目 | 内容 |
|---|---|
| 実行の契機 | 保存時とプルリクエスト。ミューテーションテストはプルリクエストで対象モジュールだけ |
| 大きさの宣言 | small。モジュール全体に `pytest.mark.small` を付けている |
| 不安定なテストの扱い | 再実行で合格にしない。現時点で不安定なテストは無い |
| 証跡 | [evidence/example_tests.json](../evidence/example_tests.json)。テストごとの結果・大きさ・確かめたIDと、対象コード・テストコードの SHA-256 を含む |

| 項目 | 値 | 証跡のキー |
|---|---|---|
| UT件数 | 125 | ut.total |
| UT合格 | 125 | ut.passed |
| UT分岐カバレッジ（全体） | 44.4% | ut.branch_coverage_percent |
| ミューテーション対象 | 68 | mutation.total |
| ミューテーション検出 | 67 | mutation.killed |
| ミューテーションスコア | 98.5% | mutation.score_percent |

ミューテーションテストの経過：初回は68件中5件が生き残った。3件は「`violations` が URL 規則を呼んでいること」を確かめるテストが無かったため（UT-008 を追加）、1件は情報分類のテストが「違反があるか」だけを見て項目名を確かめていなかったため（UT-009 を強化）。残る1件は `next_state` の例外メッセージの文言を変えるもので、文言は仕様ではないため受け入れた。分岐カバレッジは初回から100%だったが、この4件の弱さは示さなかった。

## 7. コード例（任意）

```python
@pytest.mark.req("FR-028", "FR-002", "FR-012", "FR-013", "FR-020")
@pytest.mark.parametrize("flags", list(itertools.product([False, True], repeat=5)))
def test_refusal_precedence_decision_table(flags):
    """5つの拒否条件の全 32 通り。当たった条件のうち FR-028 の順で最初の理由だけが返る。"""
    not_permitted, is_self, stale, bad_state, bad_reason = flags
    got = decision_refusal(permitted=not not_permitted, is_self=is_self, rev_matches=not stale,
                           state=State.APPROVED if bad_state else State.SUBMITTED,
                           reason="" if bad_reason else "規程を確認した")
    hit = [r for r, f in zip(ORDER, flags) if f]
    assert got is (hit[0] if hit else None)
```

期待値（`ORDER`）は FR-028 の文から書き起こしたもので、実装から写していない。

## 8. 変更履歴

| 版 | 日付 | 変更内容と理由 | 影響ID | 合意者 |
|---|---|---|---|---|
| 0.1.0 | 2026-09-19 | 初稿。設計の過程で、提出前の申請への決裁要求の扱いと、自己決裁の優先順位が要件に無いことを発見し、PRD 0.4.0 で是正 | FR-020・FR-028 | 未合意（架空例） |
| 0.2.0 | 2026-09-19 | ミューテーションテストの結果を受けて UT-008 を追加、UT-009 を強化 | UT-008・UT-009 | 未合意（架空例） |
