# 15. モデル別の適合・評価・導入順

WP01で指定モデル・effortと本人資格、WP03で評価inventoryと観測、WP04でIC12契約、WP06で入口・profile・静的/実native単体適合を固める。初期の試験は既存公式CLIのbootstrapで行い、未実装adapterへ循環依存しない。

WP15/16でnativeの実surfaceへ接続し、WP17/18/25でTaskPacket・読了・原本・公開進捗を一つの経路へ組み込む。WP19/21/22/24で設計、独立review、修正、並列統合へ適用する。WP26は全組合せと未見ルーティングの資格、WP28は固定モデルの比較と実AI18run、WP30/31はpack更新・受入証跡と提出物を確定する。

各担当WPに該当MOの作業と検査を組み込み済み。最適化を後続の任意なcleanupへ先送りしない。同時にWP06でWP28の最終比較を要求して開発を循環させない。早期は部品適合、最終は全構成の効果と安全性で判定する。

比較は[評価規約](../evaluation/EXPERIMENT_PROTOCOL.md)に従う。モデル/effortを変える比較ではない。評価用予算を未承認で実行しない。未実行や効果不明を0件/改善済に変換しない。効率比較が失敗してもコード・資料・失敗runを保存し、指示資産の原因へ戻る。

最終acceptanceは従来要件と全MO/subcase、指定profileの資格、実AI/VM/native、同一RCの証拠が必要。『プロンプトが短くなった』だけでは運用開始を認めない。

## 共通ガードと文書評価
H00/H10/H01/H11に同じIC13の必要事実・AC/TESTと同じIC14の強制policyを適用する。比較で変えるのは情報の提示・model_guidanceだけ。旧input/run_matrix JSONの3.0 provenanceは入力固定履歴として保持し、実run manifestは3.1のpolicy・最終RCを束ねる。旧条件での結果を新ガードの認定に流用しない。


## V4の評価の独立性

旧48入力と72run matrixは入力byteを維持する。新12入力を別ファイルで追加し合計60とする。全armに同じ実強制ガード・知識/品質backend・資源を適用し、指示だけを比較する。K0/K1知識、Q0/Q1品質の比較は[統合評価規約](../evaluation/V4_INTEGRATION_PROTOCOL.md)で別に扱う。性能を改善するための要件/検査/モデル削減は禁止する。
