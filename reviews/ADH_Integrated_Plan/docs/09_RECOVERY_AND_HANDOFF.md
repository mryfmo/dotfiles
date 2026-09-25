# 9. 作業継続・差戻し・復旧・context引継ぎ

## checkpointの必須情報

最新checkpointにはsource lock、spec/baseline、実効model/effort、native/asset/環境lock、受入済WP、未受入WP、task/attempt、全branch/worktree/base/HEAD/dirty、未処理agmsg IDs、実process/runner、最後の実検査/結果artifact、未解決finding、次に行う具体操作、外部待ち・予算を残す。

保存場所は `.orchestration/checkpoints/<project>/<sequence>.json` と人向けMarkdown。checkpointを更新するために古い証拠を削除しない。metadataのversionとhashを使い、並列者が上書きしない。

## RESULTを受けたとき

A1はtask_file/contractを読み直し、対象branchとartifactを実際に取得する。A2のsummaryだけでreviewしない。実command出力と作成したと主張するcommit/結果IDを照合し、存在しないものは未実施扱い。失敗ならfindingsを具体的なlocation・条件・期待動作・再検証ID付きで返す。

## 失敗の戻し先

| 原因 | 戻す先 | 禁止 |
|---|---|---|
| 仕様読違い・抜け | 当該WPの契約読解/実装 | scopeを減らして完了 |
| API/schema差 | WP02/04/15/16の資格・契約 | 推測したparameterで進行 |
| Skill/Hook競合 | WP06/26 | Hook全無効化、モデル低下 |
| 環境不足E1 | WP13/14のrecipe | 実行せずskip |
| テスト失敗 | 対象実装＋WP22 | test削除/閾値緩和 |
| 統合不具合 | WP24 | 個別PASSの合算 |
| 証拠不一致 | WP09/20/21 | PASS文面への差替え |
| UNKNOWN effect | WP23 | 未実行と仮定して再送 |
| Auth/権限/予算/利用者停止 | 明示待機 | 勝手な代替・解除 |

## 安全に並列を増減する

worker追加は空いているaNNN identity、専用worktree、非重複scope、許可された並列予算がある場合だけ。worker終了はdelivery off、leave、process quiescence、未処理task回収の順。異なる作業領域の状態を一括resetしない。

## context圧縮/新session

新A1はcheckpoint→原本→実Git状態→未処理bus→証拠の順に照合する。完了済というmemoryだけで省略しない。同じtaskの継続ではexact native session ID、独立reviewではfresh contextを使用する。forkした会話に元作者の推論が入る場合、それを独立reviewと呼ばない。

## 上流の未確定事項

探索可能な事実は自分で取得する。操作者のみが決めるbudgetや外部権限が足りない場合、そのbindingだけ記録して待機し、独立に進められる作業は続ける。資料を全部読み直すだけで延々と停滞しない。採用済architectureは再比較せず実装へ進める。

## 統合した復旧順序

admissionを止める→commit済domainとcursorを確定→run/dispatch/message identityを照合→Runner資源の静止確認→外部effectを照会→現在の資格/構成/baseline/予算を確認→exact resume適合判定→必要なら認可済fresh handoff→未受入nodeだけ再開する。

Goal active、agmsg既読、exit0、古いsummaryのいずれも単独で再開許可にしない。workspaceが変わったのに旧sessionが旧cwdへ書くことを禁止する。projection cache削除や監査replayは配送・実装を再実行する操作ではない。


## v3のcontext復旧

同じhashの読了でも、session/epoch/compactionが変われば保持を仮定しない。必須制約、現在の状態、正確なIDと失敗根拠を再確認し、必要範囲を取得する。native履歴や内部thinkingを編集・他sessionへ転送せず、必要時は認可済み新runへ明示handoffする。相関IDや原本hashは短縮で失わない。

## ガード故障・誤検知・文書変更からの復旧
原因をTEST_FAILED/ENV_MISSING/AUTH_REQUIRED/POLICY_DENIED/GUARD_UNAVAILABLE/EFFECT_UNKNOWN/BUDGET/USER_STOPに分ける。正当な誤検知の修正は対象・期限・承認・回帰を持つCHGで行い、全guardをoffにしない。statusは失敗理由と次の許可行動を返す。独立taskは継続し、古いgrant/ALLOW/receiptを復旧時に再使用しない。

checkpointへgraph_revision/適用closure/guard policy/未解決decision/実強制qualificationを追加する。文書全体のhash変化だけで全taskを初期化しない。


## V4の縮退と引き継ぎ

checkpointにはReleaseSet、二repo revision、quality inventory、knowledge snapshot、source/規範closure、未ack dispatch、learning candidateを加える。Semantica unavailableは正本直接参照へ戻し、必須source欠落だけHOLD。quality tool不在は準備recipeへ戻すが検査をSKIPしない。任意UIの停止は本体task未完了と混同しない。誤検知修正は正式policy改訂と再資格を経る。

learningは候補→評価→承認→次release。記憶やautoskillにある「完了」を現状態に採用しない。過去ログ全体を自動commitせず、redaction済み・manifest指定成果物だけを管理する。
