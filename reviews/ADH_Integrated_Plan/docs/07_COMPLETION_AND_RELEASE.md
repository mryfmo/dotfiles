# 7. 完了条件・最終受入・成果物

## 作業完了を三段階に分ける

**COMPONENT_VERIFIED**：そのWPの実装と指定階層の検査が通っただけ。全体完成ではない。

**INTEGRATION_QUALIFIED**：実Auth、実assets、実VM、各service間の動作が資格済profileで確認された。全工程AI開発の受入は別。

**DEVELOPMENT_ACCEPTED**：WP00–31、全R、全必須case、独立検証/独立review、統合/導入/運用試験、提出物一致が揃った状態。外部公開は別の権限であり、ここまでで本ユーザー向け完成成果物を提示できる。

REF_ONLY、MOCK_ONLY、PARTIAL、BLOCKED_ENV、BLOCKED_AUTH、BLOCKED_DECISION、NOT_QUALIFIEDは完成ではない。これらを『実質完成』『残りは環境だけ』『オールグリーン』と言い換えない。

## 各WPのDefinition of Done

1. 前提WPのaccepted記録と対象hashが有効。
2. 各WPの全指定作業（台帳にある全作業）とその成果物が完備し、MUSTとinterfaceを実装している。
3. 6個の論理検証項目と全展開subcaseが、要求階層の環境で実行されPASS。
4. 既知の受入阻害findingが解消され、修正後の独立再確認がある。
5. A4観測とA3レビューの対象snapshotが一致する。
6. local統合後の回帰が成功し、task/worklog/checkpointが最新。
7. 未実行/限界/外部待ちを隠さず、成果物manifestと実物が一致。

文書中心WP00–02は実行観測のない機械試験を捏造しない。DOCUMENT検査の署名/レビュー記録を残す。製品を作るためのWP受入と、製品自体が管理するtask acceptanceを区別する。

## 最終判定式

DEVELOPMENT_ACCEPTED = 全35MUST実装済
AND 全必須case実行済PASS
AND 実認証・全必須Plugins/Skills/Hooks・実VMが資格済
AND 指定model/effortが要求通り
AND 実AI全工程18run合格
AND 独立review受入阻害0
AND 統合suite/clean install/backup restore/upgrade rollback合格
AND source/spec/policy/environment/suite/contract/配布manifest一致
AND 必要な承認が有効。

1項目でも未充足なら全体未受入。検証済の部分は正確に提示し、必要な外部条件を具体化するが、完成と呼ばない。

## 完成成果物一覧（後続が作るもの）

| 成果物 | 必須内容 |
|---|---|
| 製品source repository | 完成src、型、error、migration、API、adapters、Runner、Verifier |
| 再現可能な依存 | uv.lock、native/OS/plugin payload lock、生成schemaの版 |
| 仕様書 | 要求、機能、外部/内部、architecture、ADR、変更履歴 |
| 実装/運用手順 | install、初回Auth、権限、使い方、復旧、update、uninstall |
| 完全test一式 | unit/contract/integration/security/native/VM/AI-E2E/opsとfixture |
| 受入証拠 | 実commandログ、JUnit等、署名receipt、review、NFR、資格manifest |
| artifact bundle | manifest、SHA256SUMS、SBOM、license notices、提出snapshot |
| 最終報告 | 実施/未実施/残余リスク、要求対応、environment、model、起動方法 |

試験ログに秘密を含めない。生成時のmodel reasoning全文を成果物の必須証拠にしない。説明用の短い推論要約・設計根拠と、ツール/検証の実観測を残す。

## 最後に変更したものも検証する

最終freeze後にコード・docs・契約・設定・lock・testが変われば新RC。軽微だからと未検証差分をZIPに混ぜない。受入用署名と管理記録はsource treeを変更しない外部artifactとして発行し、hashの自己参照循環を避ける。

## 人に返す最終報告の形式

結果は『受入済』か『未受入』を冒頭に記す。次に対象commit/6hash、モデル/effortと実native版、実環境、R対応、case階層別の実数、独立レビュー、起動方法、成果物へのリンク、未実施と残余リスクを示す。件数を合算して見せる場合もmockとnative、documentとtestを分ける。

公開許可がないなら開発完成を保持し公開待ちとする。外部push・PR作成/merge・publish・deploy・利用者HOME全体の変更は、単なる実装計画の提示で許可されたとはしない。

## 統合契約を含む完了判定

各WPの受入には、そのWPに割当済みICの作業と必須subcaseも含む。最終DEVELOPMENT_ACCEPTEDは18ICすべてが実装され、各正負subcaseが指定階層で成功したことを必要とする。DSH-S出典を読んだことやpackageがimportできることを、実装・動作・受入の代わりにしない。

192親case＋244内包subcase＋18実AI runは異なる粒度であり、合算してテスト総数と表示しない。過去22追補グループや62probe PASSを現在の製品合格数へ足さない。


## v4最適化の追加必須条件

全MO01–MO12、IC12、追加36subcaseと旧44、指定profile/Skill/rendererのnative資格、ルーティング、4arm比較、同じ最終H11 packの18製品runを満たす。サンドボックス・Worktree・並列化・独立検証・G0–G7はすべて維持する。

効果がNO_GAIN/INCONCLUSIVE/REGRESSIONならmodel最適化認定は未達とし、同じmodel/effortで修正/再評価する。文書に最適化と書いたことを実効改善と認定しない。最適性は評価集合に限定し、未知欠陥や一般的な最適を保証しない。

## V4の最終受入条件
35R・32WP・192親条件、既存80子を含む196子、18IC・12MO・10DG・24GRが全て同一RC/適用policyで対応し、実Auth/Plugins/VM/全工程E2Eと運用試験が成功して初めてDEVELOPMENT_ACCEPTEDにする。文書10分類の存在やgraphの連結だけを製品合格にしない。

固定benign集合の誤拒否/不要な人待ち0、固定危険/故障集合の禁止作用0、適用guardの未試験0、同一snapshot/actor/権限の照合不一致0。未知攻撃・未知欠陥の不在は主張しない。必須項目をN/Aで免除しない。ある操作に非適用なguardは理由を記録し、guard自体の全fixtureの実施は省略しない。


## V4の追加必須判定

DEVELOPMENT_ACCEPTEDには元35要求・32WP・192親と全244内包子・18IC・12MO・10DG・24GR、selected component catalog、10Skillの適合、旧48＋新12 routing入力と未見群、既存72モデル比較、実Auth/Plugins/VM/実AI/運用を要求する。全必要証拠が同ReleaseSetのdotfiles revisionとADH revisionへ対応すること。個別package成功を全体成功にしない。

SemanticaのACL/source/更新・復旧・効果、品質の対象漏れ/部分stage/Hook/CI/無変更、モデル/生成元/学習更新の一貫性を48統合子で確認する。fallbackで日常の許可作業を継続できてもSemantica製品適合が未実施なら最終受け入れはしない。提出対象は両repoの完全な変更とlock/仕様/試験/手引/実証跡/manifestである。remote push/PR/merge/deployは別委任。

文書QA、Schema正負例、グラフ整合を実製品試験へ加算しない。所有scopeが同じでもrevisionまたは候補hashが異なれば、新しく影響検査を行う。
