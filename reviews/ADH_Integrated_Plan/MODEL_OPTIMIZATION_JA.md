# Fable-5.1／GPT-6 Astra 最適化統合版の要点

版4.0.0、2026-09-13。これは[統合正本](INTEGRATED_PLAN_JA.md)の要点表示で、別baselineや後付け指示ではない。

## 変更した実行設計

**完全な仕様は維持し、モデルには共通制約＋役割prompt＋当該TaskPacketを渡す。** 詳細な資料は関連箇所を必要時取得し、無関係な全体再読・全Skill展開・重複助言を減らす。必須検査と独立レビューは外側のゲートで維持する。

| 対象 | 組み込んだ調整 |
|---|---|
| Astra/xhigh | 適用範囲の狭いSkill入口、段階的参照、目的・許可・完了の明示、初回実装での停止防止、stage別検証 |
| Fable/high | 独立取得のまとめ実行、agmsg受領後の有用な統括作業、公開情報に基づく進捗、原文根拠、対象scope維持 |
| native履歴 | 正確なsession/thread再開、外側から内部thinking/history/KV cacheを書換えない、API専用仕様をCLI引数へ流用しない |
| モデル固定 | A1/A3=Fable/high、A2=Astra/xhighを、Skill/Hook/child/profileの実効上書きまで検査 |
| 文脈 | 初回全体理解とtask別読解を区別。新session/compaction/基準変更はReadLedgerの有効性を再評価 |
| 合否 | 短いpromptで要求・oracle・独立検証を省略しない。既存35MUSTと192基本条件を保持 |

## 実際に含めた指示資産

[共通実行契約](prompts/COMMON_CONTRACT.md)、[Fable統括](prompts/CLAUDE_LEAD.md)、[Astra実装](prompts/CODEX_WORKER.md)、[Fable独立レビュー](prompts/CLAUDE_REVIEWER.md)、[機械検証](prompts/VERIFIER_RUNBOOK.md)、[3役割profile](profiles/model_profiles.json)、[10Skill入口](skill-pack/README.md)を作成した。各Skillは同梱referencesへ分岐する。上流payload導入・有効化・Hook実動作は後続資格試験で確認する。

## 作業計画と評価

32WPを維持し、25WPにモデル最適化の具体作業を追加した。IC01–IC11にIC12を接続し、その詳細をMO01–MO12で規定した。既存192親caseの中へ、44既存subcaseを保ったまま36モデル別subcaseを追加して80とした。

[公開Skill評価48事例](evaluation/skill-routing-cases.json)には正例・近接負例がある。別途、独立A3がpack凍結後に未見群を作り、入力は試験時だけ渡しgoldは伏せる。

[72run比較計画](evaluation/run_matrix.json)はH00両方対照、H10Fableだけ、H01Astraだけ、H11両方最適化の4条件。同じモデル・effort・初期課題・oracle・権限・環境で6課題を各3反復する。H11の18runと製品18runは、最終条件が同じ場合だけ同じrunIDを共通参照し二重加算しない。

## 状態

作成済み：統合仕様、役割prompt、Skill入口/参照、schema、タスク例、作業と検証割当、比較入力/条件。

未実施：実本人Auth、モデル/Skill実動作、VM、全工程AI E2E、効率比較、製品運用受入。文書QAをそれらのPASSとして扱わない。改善目標や指示量上限は本計画の編集・受入設計値であり、公式保証値や実測値ではない。

開始は[START_HERE.md](START_HERE.md)。詳細は[モデル仕様](spec/06_MODEL_OPTIMIZATION.md)、[MO契約](spec/07_MODEL_CONTRACTS.md)、[評価規約](evaluation/EXPERIMENT_PROTOCOL.md)、[変更履歴](CHANGELOG_JA.md)。

## V3.1で保持・追加したこと

モデル・effort・10Skill入口・12MO・元比較入力を保持した。IC13は10文書の型付きclosure、IC14は24guardを追加したが、全文をpromptへ常時追加しない。TaskPacketは必須REQ/AC/SPEC/TESTと適用guard・権限参照を渡す。強制は既存Supervisor/Runner/native/OS/Verifierに置く。

旧V3の80子を保持し、本版は文書20子・guard96子を追加して196子。全18IC・12MO・10DG・24GRはNOT_IMPLEMENTED相当、全試験NOT_RUN。元72行列・48例のJSONは入力固定のため3.0provenanceのまま保持するが、実行は3.1のRC/同一policyで新資格確認する。


## V4でも維持する最適化

完全仕様をTaskPacketの必要情報へ投影し、Fable/highとAstra/xhighを固定する。生成設定の編集元はdotfiles adh profile。8既存＋2新Skillの10入口から必要なものだけを選ぶ。旧48公開入力に12を追加、72モデル比較の元セルは保持する。全armに同じknowledge/quality/guardを適用し最適化の効果を切り分ける。knowledge/qualityの効果は独立評価する。
