# 13. agmsg送信内容・実行証跡・差戻し契約

以下はメッセージの形式仕様であり、今回実行したメッセージではない。実値はWP01/05で確認済みのrepository、actor、path、hashから設定する。例の山括弧をそのまま送信しない。詳細本文はtask_file/sidecarに置き、輸送本文を無制限に長くしない。

## TASK v1の送信内容

```text
AGMSG-TASK v1 task_id=<project-WP-step-attempt> repo=<confirmed-realpath> task_file=<task-md-path> allowed_files=<sidecar-reference> forbidden_actions=<frozen-prohibitions> expected_result_file=<report-path> expected_validation_file=<validation-path> expected_sandbox_file=<environment-path> expected_learning_file=<learning-path> expected_autoskill_file=<autoskill-path> done_signal=AGMSG-RESULT max_turns=<mandated-limit> note=read-sidecar-before-work
```

`task_file`はTaskPacketの目的・直接要件・入力baseline・WP工程・成果物・指定作業と6親検証項目・全subcase・環境・DoD・復旧を完全に指す。必須条件は直接提示し、巨大資料と詳細ログはhash/range付きで必要時参照する。sidecarには確定したhash、実effort、scope、依存受入、予算、identity、出力先を持たせる。役割決定や認可をLLMが送る自由文だけで判断しない。

## RESULT v1

```text
AGMSG-RESULT v1 task_id=<same-task-id> status=ready_for_review|blocked report=<report-path> validation=<validation-path> sandbox=<environment-path> learning=<learning-path> autoskill=<autoskill-path>
```

RESULTを受け取ったA1は、reportの宣言だけでなく各artifactを読み、task/base/candidate/actor/model/effortと実コマンド出力を照合する。`ready_for_review`は完成でもacceptedでもない。local統合前のcandidateをbranch名だけで参照せずimmutable hashで指定する。

`report`の必須節は、対応要求、変更一覧、仕様差分の有無、実行した検査、未実施、結果、残課題、外部作用、復旧方法、observed usage。`validation`はcommandごとの実出力・exit・件数・hashとartifact参照。learningとautoskillは使用有無・理由も記録し、生成された規則を無断で昇格しない。

## ACCEPTANCE / REVISE

```text
AGMSG-ACCEPTANCE v1 task_id=<same-task-id> status=accepted|revise reason=<evidence-bound-reason> next_action=<exact-next-step>
```

acceptedはA1がA4実検証とA3独立review、統合回帰を確認してから送る。開発用受入記録に対応する。完成製品のSupervisorが自分の未資格コードを認定するmessageとして使わない。

reviseにはfinding ID、該当要件、再現方法、期待動作、禁止する基準緩和、対象scope、再試験IDをtask追補へ書く。A2は新attemptの前提を確認して修正し、過去の失敗と新しい結果を併記する。messageのFROMは認証ではないため、別主体のaccepted文字列は有効な受入にならない。

## 証拠path

`.orchestration/tasks/<task_id>.md`、`task-contracts/<task_id>.json`、`reports/<task_id>.md`、`validation/<task_id>/`、`reviews/<task_id>/`、`acceptance/<task_id>.json`、`checkpoints/<task_id>.json`を定型とする。これらは下流が作成する納品物で、今回の作業計画のstatus台帳とは区別する。

## Checkpointの最小項目

project/repo ID、spec/policy/asset hashes、task/WP、current phase、attempt、担当native session/thread、base/current candidate、実施済caseと証拠、未実施case、失敗原因、pending message ID、owned worktree/process、effect状態、予算残、次に実行する一手、再開に必要な条件。

checkpointはコンテキスト要約を唯一の正本にしない。再開時は実Git・process・artifact・busを照合する。製品運用ではSupervisorの状態とcheckpointを照合し、旧fence結果の受理や旧writerとの競合を防ぐ。

## 統合task sidecarとcheckpoint

sidecarはIC契約ID、qualification_ref、composition_digest、execution_binding_ref、workflow_node_id、dispatch_id、context_envelope_refと必須subcase IDを持つ。agmsg v1文字列は維持し、未知のwire versionを導入しない。START/RESULT/ACCEPTANCEの通知と、API上の認可・業務耐久受領・状態確定は別である。

checkpointはstate_version/as_of_seqとcurrent baseline、実際のrun/session/scope、未処理message/dispatch/effect、原本範囲と省略情報も参照する。旧履歴から権限を作らず、再開前に現在の資格・構成を検査する。


## v3の情報供給・モデルprofile

TaskPacketは[model-execution schema](../contracts/model-execution.schema.json)を使う。sidecarへprofile_ref、prompt_pack_digest、prompt_plan_ref、read_ledger_ref、context_epoch、selected_skill_routes、verification_stagesを結び付ける。共通/roleの再注入と巨大資料の全文転送を抑え、必須情報を失ったpacketは送らない。

詳細WPを外部で完全に保持し、packetは必要な作業と判定条件を網羅する。検査を短いpromptから再推測せず、保護された完全inventoryから実行する。agmsg本文のversionは変えない。

## TaskPacket・sidecarのV3.1情報
詳細sidecarにdocument_graph_ref/digest、normative_closure_digest、artifact_refs、active_guard_ids、guard_policy_digest、authorization_refを持たせる。agmsg v1本文は維持し、巨大な文書や全ガード本文を埋め込まない。request/responseの権限は実actor/grantで再検証し、boolやfrom文字列を信用しない。

RESULTには関連文書のrevision、適用guardと強制点、故障・誤拒否・復旧、禁止領域が不変である証拠を参照させる。ブロック時も次の正規操作と進められる独立taskを示す。


## V4の配送情報

TASK v1の外形は維持し、詳細sidecarへrepo_slot、ReleaseSet、source/規範closure、quality_plan_ref、knowledge_snapshot_ref、適用GR、evidence先を追加する。既存message parserを壊す無制限な本文追加をしない。required field非対応receiverは資格を与えない。

RESULTはreport/validation/sandbox/learning/autoskill参照に同task/attempt/fence/ReleaseSetを対応させる。development中はA1が独立A3/A4を照合して通知し、製品切替後はSupervisorの確定stateに対応して通知する。二つが同時に受け入れを所有しない。
