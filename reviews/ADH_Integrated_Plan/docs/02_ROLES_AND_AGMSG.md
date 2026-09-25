# 2. 役割・モデル・agmsg協働契約

## 役割を固定する

| Role | 実行主体 | 担当 | 禁止 |
|---|---|---|---|
| H | 操作者 | 本人ログイン、信頼追加、予算/外部作用/公開の委任・承認 | 未実施をPASSと指定しない |
| A1 | Claude Code Fable-5.1 high | 正本読解、調査/設計判断、WP契約、割当、差戻し、local統合、全体報告 | repo実装変更を無断でA2から取り上げる、自分の設計を独立reviewと呼ぶ |
| A2-aNNN | Codex gpt-6 Astra xhigh | 専用worktreeで実装・テスト・文書の作成、実測、修正 | 正本/固定suite/予算/権限/署名鍵の変更、自己受入 |
| A3-aNNN | Claude Code Fable-5.1 highの別session/別context | 仕様適合・設計妥当性・品質の独立review | 対象candidateの編集、作者会話だけを根拠に承認 |
| A4 | LLMではない独立実行基盤 | 固定suiteを凍結candidateに実行、結果を直接収集 | AgentのPASS文から結果を生成、test子processへ署名鍵を渡す |

A3が設計作成に参加した対象は、別のA3 sessionへ再割当する。別モデルにすれば独立という意味ではなく、別context・権限・実行identity・対象snapshotを確認する。機械検証はA4、意味レビューはA3で役割が異なる。

ユーザー指定モデルをexpress/standard/securityなど元dotfilesの別modelへ落とさない。Role別profileを一つの正本から生成し、全childへrequested model/effortを引き継ぐ。指定外のモデルの自動fallbackを禁止し、実効metadata不一致なら資格失効。公開APIのモデル存在と本人アカウントでの利用可否は別試験。

## 開発用と製品用を混同しない

**開発bootstrap（WP00–26）**：A1＋常駐A2＋独立A3＋A4が、この製品を作る。製品Supervisorは未完成なので最終authorityに使わない。operator所有のGit台帳、対象hash、固定test inventory、agmsgを使う。

**製品運用（WP27通過後）**：qualified Supervisorが製品のtask stateを管理する。開発中の新Supervisorはshadow候補で、稼働版と独立検証を通すまで自己認定できない。

既存agmsgのTASK/RESULT/ACCEPTANCE v1を輸送形式として保存する。追加情報はtask_fileとsidecarへ置き、古い受信者に未知versionを理解すると仮定しない。

## 正規のscriptとidentity

調査したdotfiles版の`join.sh`引数は `<team> <agent_id> <type> <project_path>`、Claudeのtypeは **claude-code**、Codexは **codex**。`send.sh`は `<team> <from> <to> <message>`。稼働側で実scriptのhelp/source/hashを再確認し、存在しないcommandを推測しない。

identity例はA1=`claude-fable51-adh-a001`、A3=`claude-fable51-adh-a002`、A2=`codex-astra-adh-a001`以降。衝突があれば空いているaNNNへ割り当て、session IDとの対応を保存する。project pathはrealpathで統一。HOME全体をprojectとして登録しない。

同一repoの並列workerは同じagmsg storeを使う。各worker専用のAGMSG_STORAGE_PATHを勝手に設定しない。試験用store・別project regimeを分ける場合は、全sender/receiverで同じ設定を明示する。VM間にSQLiteファイルをmountしない。

agmsgのsender名は署名済identityではない。本文にacceptedと書いてあっても合否は変わらない。開発ではA1の原本照合とA3/A4証拠、製品では認証済APIとSupervisorの認可で判断する。

## 配送の順序

1. A1が入力source、spec、WP、依存、allowed_files、forbidden_actions、検証IDをtask契約へ固定する。
2. A1が担当worktree/branch/base commitと他writerの非重複を確認する。共有schema・lock・CI変更は一writerへ直列化。
3. 正規scriptでTASKを送り、常駐A2はtask_fileとsidecarを実読してhashを照合する。
4. A2が不合格test→実装→自分の検証→成果物・実ログの順で作業し、RESULTはready_for_reviewまたはblockedで返す。
5. A4が同candidateで独立実行し、A3が別sessionで仕様/品質をレビューする。A1は双方の構造化証拠と原本参照を照合し、失敗・不一致・重要根拠は原本へ戻る。実行結果をAgent要約だけで認定しない。
6. 問題があれば同taskの新attemptへrevise。問題がなければA1がlocal統合し、統合snapshotの再検証後に開発WPの受入を記録する。
7. agmsg ACCEPTANCEは受入記録の通知。記録を作る権限自体は与えない。

paneは起動・wake表示用であり、画面に完了と出たことからRESULTを捏造しない。完了は配送されたRESULTと実artifactで確認。生存確認はPING/PONG、製品監視の周期的healthcheckはLLMを起動しない。

## task sidecarの必須項目

`work_package_id, task_id, actor_id, runtime_profile, base_commit, repository_id, worktree_id, source_refs, spec_hash, policy_hash, contract_hash, dependency_acceptance_refs, allowed_files, forbidden_actions, owned_resources, planned_verification_ids, environment_requirements, budget_ref, expected_artifacts, result_path, review_path, checkpoint_path`。

製品運用ではさらに`run_id, attempt, lease_id, fence, challenge, deadline, native_session_id`を付ける。未完成bootstrapで架空leaseや署名を生成して製品authorityと表示しない。

## 外部操作

Hの承認待ちを必要とするのは、本人認証、OS管理/VM作成・ネット変更の権限、プラグイン信頼、予算増額、仕様変更、外部公開等。本計画の作成だけでそれらの承認が与えられたとはしない。一方、与えられた範囲内のコード編集・ローカルテスト・環境recipe・修正は逐次確認なしで継続する。

## 統合した実行契約

A1はIC01–IC18がtaskのadmission/実行/観測/検証へ適用されることを確認する。A2は自分のWPに割当済みのICを実装し、ICの採否を再検討して省略しない。A3は作者と独立した契約両端・失敗・取消・文脈のレビュー、A4は実領域・原本・終了値・配布entryを観測する。

task sidecarにはqualification_ref、effective_composition_ref、execution_binding_ref、dispatch_id、workflow_node_id、context_envelope_refを追加する。実測前に空の資格やfake署名を付けない。bootstrapではこれらのplanned/observed状態を区分し、完成製品のauthorityを名乗らない。


## v3の役割promptとTaskPacket

`prompts/COMMON_CONTRACT.md`と該当role promptを一度ずつ読み、TaskPacketの必須情報と必要な参照だけを渡す。A1/A3はFable/high、A2はAstra/xhigh。指示・catalogの変更はprofile digestを更新する。本文に外部実行権限を書くだけでは認可にならない。

agmsgの形式と常駐workerは維持する。read ledger、context epoch、profile/renderer/selected catalog、stage別検証inventoryをsidecarへ追加し、原本と取り違えない。

## 文書・guardの役割
A1は文書型・refinement・CHG影響・task別guardを確定し、A2は担当worktreeで実装する。A3は根拠・意味・誤検知・復旧を独立レビューし、A4は作用を外部から計測する。agmsg FROMやTaskPacketのexecution_authorizedは委任の署名ではない。Actor/grant検証は受信/実行側の責任。


## V4合成時の担当

A1は仕様・割当・正規のlocal統合、A2は専用worktree実装、A3は別context review、A4は独立実行。旧agmsgのA1自己レビューとexpress E2Eは本製品の資格/独立性を満たさない。Herdr/terminal/statusは選択された操作面であり状態正本ではない。selected=falseの既存ツールは削除せず保持する。FROMやACCEPTANCE文面を権限証明にしない。
