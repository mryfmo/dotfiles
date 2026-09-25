# L7 TEST — 検査定義・判定器・証拠

TDDはこの文書の次に置く別フェーズではなく、担当task内でRED→GREEN→REFACTORを繰り返す開発方式。[DG-S04](../sources/DOCUMENT_GUARDRAIL_SOURCES.md)。最初から全テスト実装を完成させなければIPLANを書けないという依存を作らない。

## 正本

[192親検証と全内包subcase](../registers/verification_cases.json)が検査条件の正本。従来の親PASS条件と80子を維持し、本版の文書20＋guard96を加えた196子を内包する。親と子は異なる粒度なので合計388という実テスト件数を主張しない。

ACの期待を、外部black-box検査・状態不変条件・contract検査・故障注入・実native/VM試験に具体化する。fixture/oracle/test runnerは後続が実装する。今回の文書上のGherkin例にはstep definitionsがなく、実行済みBDD試験ではない。

## 実行結果の分離

計画のoracle_ref、実装されたtest、実行command、exit code、collected/run/failed/skipped、環境hash、candidate hash、署名receiptを別項目にする。終了0でも0件や全skipなら未充足。LLMのPASS文ではなくA4の実観測で判定する。未対応・未実施はNOT_RUN/BLOCKEDのまま残す。

## ガードの試験

各GRに正常許可、禁止/攻撃、故障/迂回、正規復旧を定義する。正当な作業が進むこともMUSTである。Hook失敗時にnativeが進むケースでは、OSまたは保護された実行受付の別強制点で危険作用が0であることを観測する。モデルの反省文を合格条件にしない。


## V4全体統合

元192親と196子を保持し48統合子を内包。fixtures・実順序・oracle・required tierは各WPへ割当済み。新knowledge/quality評価はモデル比較と別の要因として扱う。
