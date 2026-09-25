# 検証索引 — V4

全caseの規範はregisters/verification_cases.json。詳細は[全件](VERIFICATION_CATALOG.md)。

| ID | 内容 | tier | WP | 内包数 |
|---|---|---|---|---:|
| V00-01 | 入力hashの一致 | DOCUMENT | [WP00](../work_packages/WP00.md) | 0 |
| V00-02 | 35要件の保存 | DOCUMENT | [WP00](../work_packages/WP00.md) | 1 |
| V00-03 | 原本コードの非混入 | DOCUMENT | [WP00](../work_packages/WP00.md) | 0 |
| V00-04 | 既存ファイル保護 | LOCAL | [WP00](../work_packages/WP00.md) | 0 |
| V00-05 | 無断アーキテクチャ変更の拒否 | DOCUMENT | [WP00](../work_packages/WP00.md) | 0 |
| V00-06 | 履歴PASSの非継承 | DOCUMENT | [WP00](../work_packages/WP00.md) | 0 |
| V01-01 | モデル要求値の一致 | NATIVE_AUTH | [WP01](../work_packages/WP01.md) | 1 |
| V01-02 | 利用不可・effort不一致 | CONTRACT | [WP01](../work_packages/WP01.md) | 1 |
| V01-03 | 秘密非収集 | LOCAL | [WP01](../work_packages/WP01.md) | 0 |
| V01-04 | CLI版の固定 | NATIVE_KEYLESS | [WP01](../work_packages/WP01.md) | 0 |
| V01-05 | sandbox分類 | LOCAL | [WP01](../work_packages/WP01.md) | 0 |
| V01-06 | 予算なしの開始拒否 | CONTRACT | [WP01](../work_packages/WP01.md) | 0 |
| V02-01 | 正本と具体化の整合 | DOCUMENT | [WP02](../work_packages/WP02.md) | 1 |
| V02-02 | service契約両端 | DOCUMENT | [WP02](../work_packages/WP02.md) | 2 |
| V02-03 | 実験の事前判定 | DOCUMENT | [WP02](../work_packages/WP02.md) | 0 |
| V02-04 | 要求から検証への対応 | DOCUMENT | [WP02](../work_packages/WP02.md) | 1 |
| V02-05 | 自己レビューの排除 | DOCUMENT | [WP02](../work_packages/WP02.md) | 0 |
| V02-06 | 判断待ち範囲の限定 | DOCUMENT | [WP02](../work_packages/WP02.md) | 0 |
| V03-01 | 固定依存で再現 | STATIC | [WP03](../work_packages/WP03.md) | 1 |
| V03-02 | lint/type/formatは別判定 | STATIC | [WP03](../work_packages/WP03.md) | 1 |
| V03-03 | 0件収集・全skip | LOCAL | [WP03](../work_packages/WP03.md) | 1 |
| V03-04 | 子失敗の伝播 | LOCAL | [WP03](../work_packages/WP03.md) | 1 |
| V03-05 | coverageの分母 | STATIC | [WP03](../work_packages/WP03.md) | 0 |
| V03-06 | gateと証拠の対応 | CONTRACT | [WP03](../work_packages/WP03.md) | 2 |
| V04-01 | schema正負例 | CONTRACT | [WP04](../work_packages/WP04.md) | 3 |
| V04-02 | 署名の正規化 | CONTRACT | [WP04](../work_packages/WP04.md) | 0 |
| V04-03 | API旧操作の保存 | CONTRACT | [WP04](../work_packages/WP04.md) | 0 |
| V04-04 | role別receipt | CONTRACT | [WP04](../work_packages/WP04.md) | 1 |
| V04-05 | 全状態遷移の列挙 | CONTRACT | [WP04](../work_packages/WP04.md) | 0 |
| V04-06 | 型/API/schema一致 | STATIC | [WP04](../work_packages/WP04.md) | 3 |
| V05-01 | agmsg実送受信 | LOCAL | [WP05](../work_packages/WP05.md) | 1 |
| V05-02 | 重複・古いRESULT | LOCAL | [WP05](../work_packages/WP05.md) | 0 |
| V05-03 | 書込範囲衝突 | LOCAL | [WP05](../work_packages/WP05.md) | 0 |
| V05-04 | なりすましFROM | LOCAL | [WP05](../work_packages/WP05.md) | 0 |
| V05-05 | session交代から再開 | LOCAL | [WP05](../work_packages/WP05.md) | 0 |
| V05-06 | 自己ホスト禁止 | CONTRACT | [WP05](../work_packages/WP05.md) | 0 |
| V06-01 | installer固定とpayload固定 | LOCAL | [WP06](../work_packages/WP06.md) | 1 |
| V06-02 | 実効pluginの保持と確認 | LOCAL | [WP06](../work_packages/WP06.md) | 3 |
| V06-03 | Rules競合 | CONTRACT | [WP06](../work_packages/WP06.md) | 3 |
| V06-04 | worktree/dirty解析 | LOCAL | [WP06](../work_packages/WP06.md) | 1 |
| V06-05 | Skill欠損・shadow | LOCAL | [WP06](../work_packages/WP06.md) | 4 |
| V06-06 | 実Skill・Hook呼出 | NATIVE_AUTH | [WP06](../work_packages/WP06.md) | 1 |
| V07-01 | 実競合claimの原子性 | LOCAL | [WP07](../work_packages/WP07.md) | 0 |
| V07-02 | commit直前crash | LOCAL | [WP07](../work_packages/WP07.md) | 2 |
| V07-03 | commit直後crash | LOCAL | [WP07](../work_packages/WP07.md) | 2 |
| V07-04 | disk fullとbusy | LOCAL | [WP07](../work_packages/WP07.md) | 0 |
| V07-05 | migration失敗復旧 | LOCAL | [WP07](../work_packages/WP07.md) | 0 |
| V07-06 | NFS/多control接続拒否 | CONTRACT | [WP07](../work_packages/WP07.md) | 0 |
| V08-01 | 委任内と人承認の区別 | CONTRACT | [WP08](../work_packages/WP08.md) | 1 |
| V08-02 | worker正本変更拒否 | CONTRACT | [WP08](../work_packages/WP08.md) | 1 |
| V08-03 | 古い承認の再利用拒否 | LOCAL | [WP08](../work_packages/WP08.md) | 2 |
| V08-04 | 基準緩和の検出 | CONTRACT | [WP08](../work_packages/WP08.md) | 2 |
| V08-05 | 依存acceptance失効 | LOCAL | [WP08](../work_packages/WP08.md) | 3 |
| V08-06 | 公開権限の分離 | SECURITY | [WP08](../work_packages/WP08.md) | 0 |
| V09-01 | dirty状態を識別 | LOCAL | [WP09](../work_packages/WP09.md) | 1 |
| V09-02 | 凍結前後のwriter競合 | VM | [WP09](../work_packages/WP09.md) | 0 |
| V09-03 | symlink境界 | LOCAL | [WP09](../work_packages/WP09.md) | 2 |
| V09-04 | submodule/LFS | LOCAL | [WP09](../work_packages/WP09.md) | 0 |
| V09-05 | publish中断 | LOCAL | [WP09](../work_packages/WP09.md) | 1 |
| V09-06 | 秘密混入と欠落 | SECURITY | [WP09](../work_packages/WP09.md) | 1 |
| V10-01 | DAG cycleと不存在依存 | CONTRACT | [WP10](../work_packages/WP10.md) | 2 |
| V10-02 | 二重claim | LOCAL | [WP10](../work_packages/WP10.md) | 1 |
| V10-03 | 旧fenceと他task結果 | LOCAL | [WP10](../work_packages/WP10.md) | 0 |
| V10-04 | 期限切れheartbeat | LOCAL | [WP10](../work_packages/WP10.md) | 1 |
| V10-05 | scope重複 | LOCAL | [WP10](../work_packages/WP10.md) | 0 |
| V10-06 | 依存外作業の進行 | LOCAL | [WP10](../work_packages/WP10.md) | 2 |
| V11-01 | 予算上限の前後 | LOCAL | [WP11](../work_packages/WP11.md) | 0 |
| V11-02 | clock跳躍と再起動 | LOCAL | [WP11](../work_packages/WP11.md) | 1 |
| V11-03 | 実行中pause | VM | [WP11](../work_packages/WP11.md) | 0 |
| V11-04 | pauseとcandidateの競合 | LOCAL | [WP11](../work_packages/WP11.md) | 1 |
| V11-05 | 古い/他role resume | SECURITY | [WP11](../work_packages/WP11.md) | 0 |
| V11-06 | 上限と未完了の表示 | CONTRACT | [WP11](../work_packages/WP11.md) | 1 |
| V12-01 | 全operation認可matrix | CONTRACT | [WP12](../work_packages/WP12.md) | 1 |
| V12-02 | UDSの別ユーザー | SECURITY | [WP12](../work_packages/WP12.md) | 0 |
| V12-03 | mTLS境界 | VM | [WP12](../work_packages/WP12.md) | 1 |
| V12-04 | 冪等request | LOCAL | [WP12](../work_packages/WP12.md) | 0 |
| V12-05 | project間漏えい | SECURITY | [WP12](../work_packages/WP12.md) | 1 |
| V12-06 | 入力資源上限 | LOCAL | [WP12](../work_packages/WP12.md) | 0 |
| V13-01 | 3領域の実配置 | VM | [WP13](../work_packages/WP13.md) | 0 |
| V13-02 | workerから管理資産 | VM | [WP13](../work_packages/WP13.md) | 1 |
| V13-03 | 検証コードからAuth | VM | [WP13](../work_packages/WP13.md) | 2 |
| V13-04 | egress境界 | VM | [WP13](../work_packages/WP13.md) | 2 |
| V13-05 | 環境構築と後始末 | VM | [WP13](../work_packages/WP13.md) | 1 |
| V13-06 | 制約のあるhostの扱い | LOCAL | [WP13](../work_packages/WP13.md) | 0 |
| V14-01 | 子孫process停止 | VM | [WP14](../work_packages/WP14.md) | 3 |
| V14-02 | PID再利用 | LOCAL | [WP14](../work_packages/WP14.md) | 0 |
| V14-03 | 停止とpublish競合 | VM | [WP14](../work_packages/WP14.md) | 1 |
| V14-04 | 環境不足の自律構築 | VM | [WP14](../work_packages/WP14.md) | 3 |
| V14-05 | port/並列隔離 | VM | [WP14](../work_packages/WP14.md) | 3 |
| V14-06 | setup失敗の補償 | VM | [WP14](../work_packages/WP14.md) | 5 |
| V15-01 | 新規sessionと実効model | NATIVE_AUTH | [WP15](../work_packages/WP15.md) | 1 |
| V15-02 | exact session再開 | NATIVE_AUTH | [WP15](../work_packages/WP15.md) | 1 |
| V15-03 | stream破損・final欠落 | CONTRACT | [WP15](../work_packages/WP15.md) | 2 |
| V15-04 | 非対話permissionとHooks | NATIVE_AUTH | [WP15](../work_packages/WP15.md) | 1 |
| V15-05 | 中断と残存process | VM | [WP15](../work_packages/WP15.md) | 0 |
| V15-06 | Auth/model/policy変化 | NATIVE_AUTH | [WP15](../work_packages/WP15.md) | 2 |
| V16-01 | handshakeとschema | NATIVE_KEYLESS | [WP16](../work_packages/WP16.md) | 1 |
| V16-02 | Astra/xhighとcatalog | NATIVE_AUTH | [WP16](../work_packages/WP16.md) | 1 |
| V16-03 | thread再開と誤接続防止 | NATIVE_AUTH | [WP16](../work_packages/WP16.md) | 0 |
| V16-04 | approvalの未知要求 | CONTRACT | [WP16](../work_packages/WP16.md) | 1 |
| V16-05 | 通知・EOF・再接続 | CONTRACT | [WP16](../work_packages/WP16.md) | 1 |
| V16-06 | 実中断とchild清掃 | VM | [WP16](../work_packages/WP16.md) | 0 |
| V17-01 | 実bus往復とDB状態 | LOCAL | [WP17](../work_packages/WP17.md) | 1 |
| V17-02 | outbox再送 | LOCAL | [WP17](../work_packages/WP17.md) | 2 |
| V17-03 | 偽FROM/偽accepted | SECURITY | [WP17](../work_packages/WP17.md) | 1 |
| V17-04 | 古いcontract通知 | LOCAL | [WP17](../work_packages/WP17.md) | 2 |
| V17-05 | 宛先停止と回復 | LOCAL | [WP17](../work_packages/WP17.md) | 3 |
| V17-06 | 跨VMの保存境界 | VM | [WP17](../work_packages/WP17.md) | 0 |
| V18-01 | 一次資料と版 | AI_E2E | [WP18](../work_packages/WP18.md) | 1 |
| V18-02 | 架空出典拒否 | AI_E2E | [WP18](../work_packages/WP18.md) | 2 |
| V18-03 | 矛盾の保持 | AI_E2E | [WP18](../work_packages/WP18.md) | 1 |
| V18-04 | dirty現状の解析 | AI_E2E | [WP18](../work_packages/WP18.md) | 1 |
| V18-05 | source内命令の隔離 | SECURITY | [WP18](../work_packages/WP18.md) | 1 |
| V18-06 | 探索範囲の意味的網羅 | DOCUMENT | [WP18](../work_packages/WP18.md) | 3 |
| V19-01 | 複数案比較と採用理由 | AI_E2E | [WP19](../work_packages/WP19.md) | 3 |
| V19-02 | 未実行/失敗spike | AI_E2E | [WP19](../work_packages/WP19.md) | 1 |
| V19-03 | 承認済仕様の継承 | AI_E2E | [WP19](../work_packages/WP19.md) | 0 |
| V19-04 | 仕様とplanの矛盾 | AI_E2E | [WP19](../work_packages/WP19.md) | 0 |
| V19-05 | MUST未対応 | CONTRACT | [WP19](../work_packages/WP19.md) | 1 |
| V19-06 | 委任内の自律確定 | AI_E2E | [WP19](../work_packages/WP19.md) | 0 |
| V20-01 | 固定suiteの独立実行 | VM | [WP20](../work_packages/WP20.md) | 2 |
| V20-02 | signer鍵隔離 | VM | [WP20](../work_packages/WP20.md) | 1 |
| V20-03 | 署名/role/replay | SECURITY | [WP20](../work_packages/WP20.md) | 1 |
| V20-04 | artifact実在照合 | LOCAL | [WP20](../work_packages/WP20.md) | 1 |
| V20-05 | 偽PASS/skip/zero | VM | [WP20](../work_packages/WP20.md) | 4 |
| V20-06 | key rotation/revocation | LOCAL | [WP20](../work_packages/WP20.md) | 1 |
| V21-01 | 作者と別session | NATIVE_AUTH | [WP21](../work_packages/WP21.md) | 1 |
| V21-02 | 仕様不足の発見 | AI_E2E | [WP21](../work_packages/WP21.md) | 2 |
| V21-03 | 品質欠陥の発見 | AI_E2E | [WP21](../work_packages/WP21.md) | 0 |
| V21-04 | reviewerの書込禁止 | VM | [WP21](../work_packages/WP21.md) | 0 |
| V21-05 | 未解決指摘の偽close | CONTRACT | [WP21](../work_packages/WP21.md) | 1 |
| V21-06 | 承認待ち競合 | NATIVE_AUTH | [WP21](../work_packages/WP21.md) | 2 |
| V22-01 | 実AI修正循環 | AI_E2E | [WP22](../work_packages/WP22.md) | 3 |
| V22-02 | 環境不足とコード不備 | AI_E2E | [WP22](../work_packages/WP22.md) | 1 |
| V22-03 | 無限修正防止 | LOCAL | [WP22](../work_packages/WP22.md) | 1 |
| V22-04 | 強制終了から再開 | VM | [WP22](../work_packages/WP22.md) | 2 |
| V22-05 | 停止理由の保持 | LOCAL | [WP22](../work_packages/WP22.md) | 1 |
| V22-06 | 外待ちと独立進行 | AI_E2E | [WP22](../work_packages/WP22.md) | 4 |
| V23-01 | intentと実行の順序 | LOCAL | [WP23](../work_packages/WP23.md) | 1 |
| V23-02 | 成功直後通信断 | LOCAL | [WP23](../work_packages/WP23.md) | 2 |
| V23-03 | 同key異payload | CONTRACT | [WP23](../work_packages/WP23.md) | 2 |
| V23-04 | 補償可能と不可逆 | LOCAL | [WP23](../work_packages/WP23.md) | 1 |
| V23-05 | 権限外publish | SECURITY | [WP23](../work_packages/WP23.md) | 1 |
| V23-06 | 作用不明のまま再claim | LOCAL | [WP23](../work_packages/WP23.md) | 0 |
| V24-01 | 非重複並列と統合 | AI_E2E | [WP24](../work_packages/WP24.md) | 3 |
| V24-02 | 個別PASS・統合FAIL | AI_E2E | [WP24](../work_packages/WP24.md) | 1 |
| V24-03 | merge後receipt無効 | LOCAL | [WP24](../work_packages/WP24.md) | 2 |
| V24-04 | 同一file並列拒否 | LOCAL | [WP24](../work_packages/WP24.md) | 0 |
| V24-05 | 上流契約改訂 | LOCAL | [WP24](../work_packages/WP24.md) | 4 |
| V24-06 | 統合失敗時の回復 | LOCAL | [WP24](../work_packages/WP24.md) | 2 |
| V25-01 | memoryの旧baseline | LOCAL | [WP25](../work_packages/WP25.md) | 4 |
| V25-02 | 偽完了の記憶 | SECURITY | [WP25](../work_packages/WP25.md) | 3 |
| V25-03 | 相関IDの完全性 | LOCAL | [WP25](../work_packages/WP25.md) | 0 |
| V25-04 | 秘密redaction | SECURITY | [WP25](../work_packages/WP25.md) | 3 |
| V25-05 | 進捗なしheartbeat | LOCAL | [WP25](../work_packages/WP25.md) | 0 |
| V25-06 | 表示と実stateの一致 | CONTRACT | [WP25](../work_packages/WP25.md) | 3 |
| V26-01 | 両native全lifecycle | NATIVE_AUTH | [WP26](../work_packages/WP26.md) | 6 |
| V26-02 | 全plugin適合 | NATIVE_AUTH | [WP26](../work_packages/WP26.md) | 5 |
| V26-03 | 設定更新/Hook信頼の失効 | NATIVE_AUTH | [WP26](../work_packages/WP26.md) | 7 |
| V26-04 | 実VM境界全経路 | VM | [WP26](../work_packages/WP26.md) | 4 |
| V26-05 | 証拠の階層混同拒否 | CONTRACT | [WP26](../work_packages/WP26.md) | 0 |
| V26-06 | 再インストール再現 | VM | [WP26](../work_packages/WP26.md) | 0 |
| V27-01 | shadow無作用 | LOCAL | [WP27](../work_packages/WP27.md) | 0 |
| V27-02 | 二重authority拒否 | LOCAL | [WP27](../work_packages/WP27.md) | 0 |
| V27-03 | watermark境界のcrash | LOCAL | [WP27](../work_packages/WP27.md) | 0 |
| V27-04 | candidate自己認定拒否 | SECURITY | [WP27](../work_packages/WP27.md) | 0 |
| V27-05 | rollback後の再配送 | LOCAL | [WP27](../work_packages/WP27.md) | 0 |
| V27-06 | 必要承認の確認 | CONTRACT | [WP27](../work_packages/WP27.md) | 0 |
| V28-01 | U: 未確定要求から完成 | AI_E2E | [WP28](../work_packages/WP28.md) | 4 |
| V28-02 | B: 既存仕様の保持 | AI_E2E | [WP28](../work_packages/WP28.md) | 2 |
| V28-03 | E: 環境不足解消 | AI_E2E | [WP28](../work_packages/WP28.md) | 0 |
| V28-04 | R: テスト失敗から修正 | AI_E2E | [WP28](../work_packages/WP28.md) | 2 |
| V28-05 | I: 個別成功後の統合不具合 | AI_E2E | [WP28](../work_packages/WP28.md) | 0 |
| V28-06 | C: 中断/compaction後継続 | AI_E2E | [WP28](../work_packages/WP28.md) | 6 |
| V29-01 | prompt injection全経路 | SECURITY | [WP29](../work_packages/WP29.md) | 5 |
| V29-02 | 証拠偽装とkey侵害境界 | VM | [WP29](../work_packages/WP29.md) | 0 |
| V29-03 | 復旧fault matrix | VM | [WP29](../work_packages/WP29.md) | 1 |
| V29-04 | 旧writerとPID再利用 | VM | [WP29](../work_packages/WP29.md) | 1 |
| V29-05 | 負荷と資源上限 | PERFORMANCE | [WP29](../work_packages/WP29.md) | 3 |
| V29-06 | RPO/RTO/停止測定 | RELIABILITY | [WP29](../work_packages/WP29.md) | 0 |
| V30-01 | clean install起動 | OPS | [WP30](../work_packages/WP30.md) | 1 |
| V30-02 | CLIとAPI一致 | CONTRACT | [WP30](../work_packages/WP30.md) | 1 |
| V30-03 | backup/restore実試験 | OPS | [WP30](../work_packages/WP30.md) | 0 |
| V30-04 | 更新とrollback | OPS | [WP30](../work_packages/WP30.md) | 6 |
| V30-05 | 成果物manifest/SBOM | STATIC | [WP30](../work_packages/WP30.md) | 2 |
| V30-06 | uninstall副作用 | OPS | [WP30](../work_packages/WP30.md) | 1 |
| V31-01 | 全35要件の実証跡 | DOCUMENT | [WP31](../work_packages/WP31.md) | 1 |
| V31-02 | 全必須suite同一RC | RELEASE | [WP31](../work_packages/WP31.md) | 2 |
| V31-03 | 偽全greenの集計拒否 | CONTRACT | [WP31](../work_packages/WP31.md) | 2 |
| V31-04 | 独立監査と指摘解消 | DOCUMENT | [WP31](../work_packages/WP31.md) | 0 |
| V31-05 | 提出物同一性 | STATIC | [WP31](../work_packages/WP31.md) | 3 |
| V31-06 | 公開未承認の分離 | SECURITY | [WP31](../work_packages/WP31.md) | 0 |
