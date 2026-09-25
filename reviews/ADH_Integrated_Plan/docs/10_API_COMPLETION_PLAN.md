# 10. 本番API・データ契約の実装範囲

本章はAPI実装を添付するものではなく、WP04/12/30で完成させるAPIの作業範囲を固定する。旧13操作を保存する。実装時の完全schemaはWP04で生成し、全入力/出力/認可/状態変化/error/idempotencyを埋める。

## 保存する13操作

| Method/path | operationId |
|---|---|
| POST /v1/projects | createProject |
| POST /v1/projects/{project_id}/proposals | proposeDesign |
| POST /v1/projects/{project_id}/baselines | publishBaseline |
| POST /v1/tasks | createTask |
| GET /v1/tasks/{task_id} | getTask |
| POST /v1/tasks/{task_id}/claim | claimTask |
| POST /v1/tasks/{task_id}/candidate | submitCandidate |
| POST /v1/tasks/{task_id}/accept | acceptCandidate |
| POST /v1/tasks/{task_id}/reject | rejectCandidate |
| POST /v1/tasks/{task_id}/pause | pauseTask |
| POST /v1/tasks/{task_id}/resume | resumeTask |
| POST /v1/tasks/{task_id}/reconcile | reconcileTask |
| GET /v1/events | getEvents |

## 明示追加する操作

| Method/path | operationId | 主な義務 |
|---|---|---|
| GET /v1/projects/{project_id} | getProject | phase/未充足MUST/予算/待機理由/次行動 |
| POST /v1/projects/{project_id}/run | startProject | Mandate/資格/予算確認後だけadmission |
| POST /v1/projects/{project_id}/pause | pauseProject | 新admission停止→全owned run停止確認 |
| POST /v1/projects/{project_id}/resume | resumeProject | actor/version/理由/baseline/予算照合 |
| GET /v1/projects/{project_id}/acceptance | getProjectAcceptance | 全WPではなく対象製品task/requirementの証拠対応 |
| POST /v1/tasks/{task_id}/heartbeat | heartbeatTask | owner/fence/lease期限を検査 |
| GET /v1/runs/{run_id} | getRun | native session、attempt、資格状態、diagnostic |
| POST /v1/effects | registerEffect | intent/target/idempotency/query/compensation |
| POST /v1/effects/{effect_id}/reconcile | reconcileEffect | 実作用照会、UNKNOWN維持、証拠 |
| GET /v1/artifacts/{digest} | getArtifact | actor/project認可、digestとsize照合 |
| POST /v1/approvals | registerApproval | 対象operation/hash/actor/期限/mandate版 |
| POST /v1/qualifications | registerQualification | 実native/asset/VM結果への参照 |
| GET /v1/qualifications/{qualification_id} | getQualification | 実績/未実施/失効条件 |
| POST /v1/releases | requestRelease | 開発受入と公開権限を分離 |

合計27操作を最低実装範囲とする。上記の状態APIを追加することで旧機能を削らない。仕様上必要な追加操作が判明すれば、WP02/04の変更台帳に記録し全consumer/testを更新する。HTTP requestで受取ったroleをそのまま認可主体にしない。

## エラーと同時実行

400=形式、401=未認証、403=権限、409=version/fence/hash/冪等衝突、422=必須条件/証拠不足、423=停止/照合待ち、429=負荷/予算、503=backend。retryableフラグと安全なreason codeを付け、stderrに秘密があればredacted診断参照へ置き換える。

同一Idempotency-Keyと同payloadは同じ結果。異payloadは409。副作用とDB状態のexactly-onceを混同しない。pagination/event cursorは未読欠落・重複へ対処し、project scopeを越えて読めない。

## 新しいAPIを乱立させない統合

27操作を維持し、既存入力/出力にICの参照と契約を結び付ける。startProject/claimTaskはqualificationとbindingを照合、candidate/acceptはsource/検証scopeを照合、getProject/getEventsはstate_version/as_of_seq、getArtifactはACL付きrange/provenance、registerQualificationはobserved capabilityとcompositionを扱う。

監査replayやcache再構成は管理操作でありAgentに任意実行権限を与えない。内部関数のoperation名を、存在する公開HTTP endpointと誤表示しない。nativeのschemaは本製品OpenAPIへ混ぜない。

## V3.1で追加するADH操作と拒否境界
[operation inventory](../contracts/operation_inventory.json)は旧27操作を保持し、getDocumentGraph、proposeChange、assessChangeImpact、getRunGuardDecisionsの4操作を追加した。これらは本製品が後続で実装する契約であり公式CLIのコマンドではない。graph/status取得にも認証・ACL・秘密除去を適用する。

guard evaluateは内部serviceであり、modelに任意のALLOWや署名を発行させるAPIを公開しない。認証済み既存registerApprovalでgrantを作る場合もaction/target/expiryへ限定する。文書承認と公開承認を混同しない。


## V4操作の統合

[operation_inventory](../contracts/operation_inventory.json)を唯一の公開操作一覧とする。既存操作を削除せず、knowledge query/ingest/rebuild、quality plan/run/status、learning候補、release登録/activateを追加した。データは[stack schema](../contracts/stack-integration.schema.json)に接続。権限は既存管理APIと同じ認証済みchannel・actor/grant/target照合で扱い、新たな未認証RESTやMCPを開かない。Semantica公式subcommandと本APIを混同しない。
