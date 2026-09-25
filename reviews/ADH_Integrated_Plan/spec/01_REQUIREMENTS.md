# 要求・機能範囲と35MUST

要求本文の正本は[requirements.json](../contracts/requirements.json)。旧版とbyte同一で保持する。IC01–IC18は新しい別要求集合ではなく、この35要求を実装可能な内部契約へ具体化するもの。

未確定要求から始める案件は、資料調査・現状分析・候補比較・技術検証・仕様/アーキテクチャー/機能策定を自律工程に含める。承認済み仕様がある案件では適用条件と矛盾を確認して継承し、候補を作るためだけに再設計しない。仕様変更の必要性を発見した場合はCRに分離し、承認前に実装へ混ぜない。

| ID | 要件 | MUST本文 | Gate |
|---|---|---|---|
| R01 | 要求・制約の正本 | 入力資料、要求ID、必須/任意、禁止変更、受入項目を版付きで保持する | G0 |
| R02 | 委任範囲 | 調査・技術選択・実装等の自動決定範囲をAutonomyMandateで定義する | G0 |
| R03 | 調査根拠 | 一次資料の版・取得時点・locator・内容hashを記録する | G1 |
| R04 | 広さと深さ | 重要論点を分解し依存元/依存先/代替/反例/障害経路まで調べる | G1 |
| R05 | 事実と不確実性 | 事実/推論/仮定/未検証を区別し、重大矛盾を未解決のまま確定しない | G1 |
| R06 | 現状snapshot | mainへ勝手に移動せず、対象worktree/HEAD/index/working/untrackedを識別する | G1 |
| R07 | 候補比較 | 成立する複数案と不採用理由、判断が変わる条件を残す | G2 |
| R08 | 技術実験 | 採用上重要な仮説に最小実験と事前の判定基準を設ける | G2 |
| R09 | 仕様策定 | 機能一覧・外部/内部仕様・データ・異常時動作・NFRを確定する | G3 |
| R10 | 設計判断 | ADRを要求・根拠・候補・実験に連結する | G3 |
| R11 | 凍結baseline | 確定済み仕様とテスト契約をworkerが緩和できない | G3 |
| R12 | 計画網羅 | MUST→ADR→task→checkの欠落/重複/矛盾を検出する | G4 |
| R13 | native Auth | 未改変の公式Claude Code/Codexで本人認証を保持する | G0 |
| R14 | native拡張 | Plugins/Skills/Rules/Hooksを公式runtimeで実行し有効状態を確認する | G0 |
| R15 | 実効構成固定 | CLI/model/skill/plugin/policyの版とhashを実行ごとに束ねる | G0 |
| R16 | 作業隔離 | 一つの作業領域に同時writerは一つ。試行間も隔離する | G4 |
| R17 | 並列整合 | 依存DAG、所有権、fenceで二重着手と古い結果を防ぐ | G4 |
| R18 | 実装自律 | 承認範囲で調査・編集・build・test・修正を逐次指示なしで進める | G5 |
| R19 | 環境準備 | 既存環境可/構築すれば可/外部実機必須を区分し前二者を自動実行する | G5 |
| R20 | 独立検証 | 実装者の報告ではなく別検証環境で固定suiteを実行する | G5 |
| R21 | 独立レビュー | 別session/権限で仕様適合性と品質を確認する | G5 |
| R22 | 証拠署名 | snapshot・契約・環境・policy・suite・試行に署名結果を結び付ける | G5 |
| R23 | 修正閉ループ | 不合格をready for repairへ戻し原因を分類する | G5 |
| R24 | 復旧 | lease失効だけで再実行せず旧process停止と副作用を照合する | G5 |
| R25 | 明示停止尊重 | 人の停止・権限不足・予算上限を自動解除しない | G5 |
| R26 | 統合検証 | 各task合格を足し合わせず統合snapshotで再試験する | G6 |
| R27 | 成果物完全性 | 起動手順/仕様/コード/試験/依存/manifest/残課題を照合する | G6 |
| R28 | 開発完了と公開分離 | 外部push/merge/publish/deployは別の委任・承認に従う | G7 |
| R29 | 記憶正本分離 | UA/CompactionDB/SDDは派生・参照、仕様/進捗を独立に確定しない | G1-G6 |
| R30 | prompt injection境界 | Web/README/tool outputを命令権限に昇格させない | G1-G6 |
| R31 | 可観測性 | project/task/run/session/attempt/traceを関連付け秘密を除去する | G0-G7 |
| R32 | 有限予算 | 回数・時間・並列・利用量の予算を外部に保持、上限で完了にしない | G0-G7 |
| R33 | 更新検証 | payloadまで固定し、候補更新に契約・回帰・E2Eを要求する | G0 |
| R34 | 再現可能性 | 基準・snapshot・環境・suiteから検証を再実行できる | G5-G6 |
| R35 | 境界の誠実性 | モック/抽出関数/実CLI/実機の結果を混同せず未実施を明示する | G0-G7 |

## 開発機能の全体

G0=本人認証・モデル/effort・構成・環境・委任の資格。G1=要求/一次資料/現状snapshot/重要論点の調査。G2=候補比較・反例・事前oracle付き技術実験。G3=仕様/ADRの委任内確定または必要な承認とbaseline凍結。G4=依存/担当/検査/環境を持つ実装DAG。G5=実装・独立検証・レビュー・修正/復旧。G6=統合snapshotで起動/E2Eと成果物受入。G7=別途の公開委任に基づく外部反映。

すべてを一つの開発workflowで扱い、G0以前の資格確認やG1調査を、未作成のG3 solution baselineへ循環依存させない。InputBaseline（利用者要求/委任）とSolutionBaseline（確定設計）を区別し、各nodeが必要とするbaseline種類を契約に記載する。


## モデル最適化の追跡

MO01–MO12は新しい別要求を持ち込むのではなく、既存要求のモデル別の具体化である。requirements.jsonの35本文は元版とbyte同一。各要求からモデル契約と具体subcaseへの対応を[台帳](../registers/requirement_traceability.json)に保持する。

## 文書化と強制の対応

[10分類](../artifacts/README.md)は本製品の35要求をBRD/PRD/REQ/AC/ARCH+ADR/SPEC/TEST/IPLAN/CHG/EVALとして役割別に整理する。[構造化要求](../registers/structured_requirements.json)は元Rの意味を維持するEARS型refinementで、[AC](../registers/acceptance_scenarios.json)は代表例と検査参照を持つ。例だけですべての要求を証明したとみなさない。

[24GR](../registers/guardrails.json)は元要求の安全・品質・継続の実施条件であり追加モデルの判定に委ねない。ガードは正規作業の通過、禁止作用の拒否、ガード自体の故障、正規復旧まで試験する。対応は[要求台帳](../registers/requirement_traceability.json)。
