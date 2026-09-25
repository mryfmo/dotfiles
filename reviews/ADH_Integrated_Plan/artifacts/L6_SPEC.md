# L6 SPEC — 実装可能な契約の索引

本SPECは図だけでなく、入力、出力、エラー、所有者、取消、並行性、冪等性、耐久性、権限、観測、更新失効を定義する。[既存IC](../spec/03_INTEGRATED_CONTRACTS.md)、[文書graph IC13](../spec/08_DOCUMENT_GRAPH.md)、[guard IC14](../spec/09_GUARDRAILS.md)、[CHG](../spec/10_CHANGE_AND_REGATE.md)が本文である。

## 追加schema

[document-graph.schema.json](../contracts/document-graph.schema.json)：Node/Edge/Graphとref型。
[guardrails.schema.json](../contracts/guardrails.schema.json)：OperationIntent/GuardDecision/GuardQualification。
[model-execution.schema.json](../contracts/model-execution.schema.json)：TaskPacketの文書closure/guard参照。

これらはADHの契約であり公式native APIではない。実実装時は型/Schema/APIの一致をWP04/12で検査する。未知のnative methodを同名で発明しない。

## 設計した内部操作

`resolve_document_closure(task, baseline, actor)` はACLと適用版を確認した参照集合を返す。`evaluate_operation(intent, actor, policy, qualification)` はdecisionと根拠を返すが、Agentがその結果だけで権限を増やす経路を作らない。`enforce_and_dispatch` は有効判定・最新scope・永続intentを確認して実作用を開始する。`propose_change` は変更案を保存し、`resolve_impact` が失効候補を計算する。承認と適用は別である。

## 失敗時

未知の文書版/参照不正は422、権限違反403、対象hashやversion競合409、ガード故障/判断待ちは423等のsafe reasonを返す。詳細は既存API規約とIC14の分類に従う。配布用診断にsecretを含めない。GuardDecisionの有効期限後や対象変更後は再照合する。


## V4全体統合

既存IC01–14へIC15構成、IC16知識、IC17品質、IC18ライフサイクルを統合。stack-integration.schema.jsonは後続実装の機械契約で、状態真偽・実署名・ACLは操作実装で検査する。
