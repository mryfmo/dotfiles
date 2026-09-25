# 全32作業単位 — V4

依存と実scopeが揃うものは並列可。統合は直列。移管元SI/DIは独立taskとして実行しない。

| WP | 内容 | 前提 | 作業数 | 親/内包検査 |
|---|---|---|---:|---:|
| [WP00](../work_packages/WP00.md) | 正本固定・過去コードの切離し・開発範囲の確定 | — | 10 | 6 / 1 |
| [WP01](../work_packages/WP01.md) | 指定モデル・公式認証・実行環境の資格確認 | WP00 | 10 | 6 / 2 |
| [WP02](../work_packages/WP02.md) | 実装前の仕様不足解消とインターフェース設計レビュー | WP00, WP01 | 10 | 6 / 4 |
| [WP03](../work_packages/WP03.md) | 開発repository・品質ゲート・証跡収集の土台 | WP02 | 10 | 6 / 6 |
| [WP04](../work_packages/WP04.md) | 本番schema・型・API・状態遷移契約の確定 | WP02, WP03 | 10 | 6 / 7 |
| [WP05](../work_packages/WP05.md) | 開発用agmsg協働・タスク割当・証跡引継ぎ | WP01, WP04 | 10 | 6 / 1 |
| [WP06](../work_packages/WP06.md) | Plugins・Skills・Rulesの固定と工程適合 | WP01, WP04, WP05 | 11 | 6 / 13 |
| [WP07](../work_packages/WP07.md) | SQLite永続化・migration・atomic event/outbox | WP03, WP04 | 9 | 6 / 4 |
| [WP08](../work_packages/WP08.md) | Baseline・Mandate・変更承認の権限管理 | WP04, WP07 | 9 | 6 / 9 |
| [WP09](../work_packages/WP09.md) | 内容スナップショット・artifact store・入力同一性 | WP04, WP07 | 10 | 6 / 5 |
| [WP10](../work_packages/WP10.md) | 依存DAG・排他claim・attempt/fence・公平な割当 | WP04, WP07, WP08 | 10 | 6 / 6 |
| [WP11](../work_packages/WP11.md) | 予算・clock・停止/再開・状態遷移の完備 | WP08, WP10 | 9 | 6 / 3 |
| [WP12](../work_packages/WP12.md) | 認証済制御API・UDS・VM間channel・認可 | WP04, WP08, WP10, WP11 | 9 | 6 / 3 |
| [WP13](../work_packages/WP13.md) | Linux VM配置・役割ユーザー・ネットワーク分離 | WP05, WP12 | 9 | 6 / 6 |
| [WP14](../work_packages/WP14.md) | Runner実装・子process停止・凍結・環境recipe | WP09, WP11, WP12, WP13 | 10 | 6 / 15 |
| [WP15](../work_packages/WP15.md) | Claude Code公式CLI adapter・正確なsession継続 | WP06, WP12, WP14 | 10 | 6 / 7 |
| [WP16](../work_packages/WP16.md) | Codex公式App Server adapter・thread/turn管理 | WP06, WP12, WP14 | 10 | 6 / 4 |
| [WP17](../work_packages/WP17.md) | 製品のagmsg通知bridge・outbox配送・整合 | WP05, WP07, WP12, WP15, WP16 | 10 | 6 / 9 |
| [WP18](../work_packages/WP18.md) | 調査・現状分析・出典/主張管理の上流工程 | WP06, WP08, WP09, WP10, WP15, WP17 | 11 | 6 / 9 |
| [WP19](../work_packages/WP19.md) | 比較・実験・仕様/ADR策定・計画生成 | WP10, WP14, WP18 | 10 | 6 / 5 |
| [WP20](../work_packages/WP20.md) | 独立Verifier・固定suite・署名service | WP08, WP09, WP12, WP14 | 10 | 6 / 10 |
| [WP21](../work_packages/WP21.md) | 独立Reviewer・仕様適合/品質の二段階審査 | WP15, WP16, WP19, WP20 | 10 | 6 / 6 |
| [WP22](../work_packages/WP22.md) | 修正閉ループ・再計画・異常終了復旧 | WP11, WP17, WP19, WP20, WP21 | 10 | 6 / 12 |
| [WP23](../work_packages/WP23.md) | 外部作用intent・冪等性・結果照合・補償 | WP12, WP14, WP22 | 9 | 6 / 7 |
| [WP24](../work_packages/WP24.md) | 並列開発・直列統合・下流失効と統合検証 | WP09, WP10, WP19, WP21, WP22, WP23 | 10 | 6 / 12 |
| [WP25](../work_packages/WP25.md) | 記憶・可観測性・進捗表示・監査ログ | WP09, WP17, WP18, WP22 | 10 | 6 / 13 |
| [WP26](../work_packages/WP26.md) | 本人Auth・全Plugins・実VMの統合資格試験 | WP15, WP16, WP17, WP20, WP21, WP25 | 10 | 6 / 22 |
| [WP27](../work_packages/WP27.md) | 自己ホスト切替・shadow運用・制御基盤自身の変更防護 | WP22, WP23, WP24, WP26 | 9 | 6 / 0 |
| [WP28](../work_packages/WP28.md) | 調査から成果物受入までの実AI全工程E2E | WP19, WP24, WP25, WP26, WP27 | 10 | 6 / 14 |
| [WP29](../work_packages/WP29.md) | 敵対的検証・障害復旧・負荷/容量・非機能受入 | WP23, WP24, WP26, WP27, WP28 | 10 | 6 / 10 |
| [WP30](../work_packages/WP30.md) | 成果物化・install/upgrade/rollback・backup/restore・利用手引 | WP25, WP27, WP28, WP29 | 10 | 6 / 11 |
| [WP31](../work_packages/WP31.md) | 最終全件再検証・独立監査・受入bundle確定 | WP30 | 10 | 6 / 8 |
