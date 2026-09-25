# 4. 実装前に解消する仕様の具体化 C01–C12

C01–C12は本v4に統合した具体化であり、IC01–IC18と一体で適用する。WP02は内部整合と実環境bindingの確認、WP04は本番型/schemaへの実装である。何を採用するかやどのWPへ回すかを後から決める工程ではない。旧probeに合わせて完成条件を削らない。

| ID | 具体化 | 適用WP・受入 |
|---|---|---|
| C01 | 参照コードを製品入力にしない。I01–I15の意図を本番testへ移す | WP00/03/31 |
| C02 | 同じreceipt schemaにtest観測とreview観測を強制しない。共通headerにtask/run/attempt/fence/challenge/6hash、CheckReceiptにcommand観測、ReviewReceiptにrubric/findingsを持つ | WP04/20/21 |
| C03 | 全project/task/run状態表を定義。PAUSING、PAUSED_USER/BUDGET/AUTH、RECONCILING、BLOCKED_EFFECT、FAILED、SUPERSEDEDを省略しない | WP04/10/11/22/23 |
| C04 | 旧13APIを維持し、project開始/状態/停止/再開、heartbeat、effect、artifact、approval、qualificationを明示追加 | WP04/12/30 |
| C05 | requested modelをFable5.1/high、Astra/xhighで固定し、観測/未確認と版を分離。元profileの低価格モデルへ戻さない | WP01/06/15/16/26 |
| C06 | 制御UDSとVM間mTLS、provisioning SSHを区分。本文のroleやagmsg FROMでは認可しない | WP12/13/17 |
| C07 | symlink/submodule/LFSの本番policyを定義。内部linkは内容として保持、外部link拒否、submodule固定commitとhydrated LFSを照合 | WP09/14 |
| C08 | source/spec/policy+assets/environment/test-suite/task-contractの六hashを別々に保持。runtime observationと署名trust identityを結び付ける | WP04/09/20/21 |
| C09 | phase完了の失効規則を定義。baseline/contract/sourceの変化で影響結果を失効し、古いreceiptを新candidateへ流用しない | WP08/24/31 |
| C10 | 開発bootstrapと製品自己ホストを分離。候補Supervisorが自己認定する循環を禁止 | WP05/27 |
| C11 | Qゲートと検証階層・status・期待case数を先に固定。過去62件、mock、SKIPをnative/全工程成功の代わりにしない | WP03/26/28/31 |
| C12 | 有限予算の外部binding、clock epoch、旧writerの停止確認、作用UNKNOWNの照合を組み合わせる | WP01/11/14/22/23 |

## 共通必須データ

TaskContract: project_id/task_id/WP/phase/baseline_id/spec_hash/policy_hash/contract_hash/required_requirements/required_checks/dependencies/write_scope/environment_recipe/budget_ref。

RunManifest: actor_id/role/run_id/attempt/fence/requested_and_observed_model/effort/native_binary_version_and_digest/session_or_thread_id/environment_digest/asset_lock_digest/deadline/trace_id。

CheckReceipt: 共通header、issuer/key_id、check definition hash、実argv/cwd、exit/signal/timeout、collected/executed/failed/skipped/xfail、log/result artifacts、開始終了時刻。review artifactは必須にしない。

ReviewReceipt: 共通header、独立session/identity、rubric hash、検査対象requirements、findings（ID/severity/location/根拠/status）、未検証項目、review artifact digest。存在しないcommand実行を捏造しない。

AcceptanceはCheckReceiptとReviewReceiptの両方、対象一致、issuer/role、実artifact、未充足条件を検査する。署名の正しさだけでは合格しない。

## schemaとprotocolの扱い

本製品のOpenAPI/JSON Schemaは本件の契約。公式Claude/Codex wireは固定binaryから採取する別契約。generate-json-schemaの出力とWeb上の最新版が違えば、実際に採用するbinaryのものを正とし互換試験を行う。新しいAPIを使うためだけにpreview endpointを無断で有効化しない。

正規化は署名用test vectorを凍結して決定する。少なくともJSON重複key/NaN/Infinity/曖昧な数値を拒否し、UTF-8、文字列、integer境界、key順序を一致させる。Pythonのjson.dumpsを使う場合もRFC8785準拠と誤表示しない。別canonicalizationにするならWP02の具体化記録と全署名testが必要。

## 検査対象の特殊ファイル

symbolic linkを一般ファイルとして外部へdereferenceしない。内部targetの存在・正規化を確認してlink情報を保持する。submoduleはgitlinkだけを収録したまま全source収録と呼ばない。LFS pointerだけで実データがない状態をPASSにしない。E2Eに必要な生成物はrecipeから再生成し、source artifactと別manifestにする。秘密やAuthが必須sourceに混ざっている場合は無言除外で成功させず、入力修正へ戻す。

## 同じ本番契約へ統合する項目

IC01のOperationCapability、IC02のExecutionBinding、IC03のEffectiveComposition、IC04のProjectionCursor、IC05のDispatchIntent、IC06のGoal/ExecutionAuthorization、IC07のWorkflowNode/MessageReceipt、IC08のRunOutcome、IC09のContextEnvelope、IC10のDecisionDossier、IC11のTestExecutionを同じ型体系とAPIに反映する。新しい独立DB、独立Goal loop、追補専用authorityは作らない。

一覧のフィールド・正常・失敗・適用限界はspec/03_INTEGRATED_CONTRACTS.mdが規範である。既存TaskContract/RunManifest/Receiptのidentityを利用し、別名のtask/sessionを複製しない。ContextProjectionは原本参照、Projectionは状態表示であり別型にする。


## v4のモデル契約のbinding

IC12/MO01–MO12と[model-execution.schema.json](../contracts/model-execution.schema.json)は本版で確定した追加契約。field・役割・評価方法の採否を未決事項に戻さない。実装クラス配置と採用版nativeへの具体対応はWP02/04で記録する。受入基準を変える場合だけ別CRとする。

## C13：文書graphと操作別guardの具体化（本版で決定済み）
IC13/DG01–10の分類・typed refs・要求/AC/TEST・closure・CHGと、IC14/GR01–24の強制点・actor・結果・故障・復旧を本版の契約として使う。実装時には実path/handler/native版/OS backendへbindingし、採否を再び未定に戻さない。意味が変わる仕様変更はCRへ分離する。


## V4では取込判断を後続へ残さない

IC15の配布/構成、IC16の知識、IC17の品質、IC18の学習/再gateは採用済み仕様。追加の「Semanticaを使うか」比較ではなく、指定する契約への実適合を行う。未実装のservice/APIは実装予定と記録し、正確なCLI flagと対応版は実binaryでbindingする。実際に成立しない外部仕様との差はCRへ分離する。
