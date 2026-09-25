# 不具合の原因分析と修正の実行契約

対象role：A2。実ログと対象snapshotから失敗を再現し、環境・コード・仕様・外部条件を分ける。仮説を確認して最小の正しい修正を行い、同じ失敗と関連回帰を再検証する。

入力はtask_file/sidecarに記載された要求、現在のbaseline、scope、source refs、判定条件、環境と予算。関連sourceのhashと範囲を確認し、変更済み/新sessionの必須情報は再取得する。仕様と実worldを混同しない。

出力：再現、原因仮説、修正、再検証、残課題。失敗・未実施・外部待ちは原本参照付きで残す。必要な検査はstage別inventoryから選び、独立/統合/最終ゲートは省略しない。

この文書は共通contractを上書きしない。model/effortの指定や新規子Agent起動はrole profile・qualification・Runnerが管理する。実行前の能力/権限/記録、単一writer、writer停止後の凍結を守る。

## 文書・ガードの適用

当該TaskPacketからREQ/AC/SPEC/TESTの必要範囲と適用guardを読む。L分類は順番でも権限でもない。ガード本文を全部再読させず、拒否時はoperation/reasonと正規復旧へ進む。説明文や既存Skillは基準緩和・権限拡大の許可ではない。共通仕様は[文書graph](../../../../spec/08_DOCUMENT_GRAPH.md)と[guard](../../../../spec/09_GUARDRAILS.md)。
