# 工程・合否・学習・変更の統合ライフサイクル

規範はIC18。図や通知のdoneではなく、同一candidateに結び付いた独立証拠から確定する。[V4-S02][V4-S03]

## 状態の意味

配送ackは受領、native turn完了はその区間の終了、RESULTは候補提出、worklog doneは個別todoの終了、Crit reviewedは指摘処理、A4 PASSは所定suiteの成功、Supervisor ACCEPTEDは承認済み条件の照合結果。これらを同じ真偽値へ潰さない。

開発中のA1/A3/A4による受け入れと、製品Supervisorによる案件受け入れは異なる。WP27まではbootstrapが開発主体で、完成前のcandidateに自己認可をさせない。切替後もcontrol plane自身の更新は前版keeperと外部独立証拠で判定する。

## レビュー契約

A1は調査・割当・統合判断、A2は実装writer、A3は作者と独立のFable/high session、A4は固定検査の実行者。A1のRESULT確認は必須だが、設計作者自身の確認を独立設計レビューとは呼ばない。Crit UIはreserved human decisionに必要な場合だけ使い、通常のagent reviewを恒常的な人待ちへ接続しない。ReviewReceiptとCheckReceiptは別の型と発行者を持つ。

## 学習

CANDIDATE→EVALUATED→APPROVED→PROMOTED_TO_NEW_RELEASE、またはREJECTED/SUPERSEDED。各段階にsource/task/evidence、適用条件、元asset hash、新asset hash、独立評価、承認主体を持つ。モデルの提案だけでRules/Skills/Hooks/quality基準を編集しない。再利用価値がない場合はno-candidate reasonを記録し、無理にSkillを作らせない。

承認済みの改善は次runの構成へ適用する。活動中sessionの履歴/assetをその場で差し替えない。モデル最適化MOとSkill正負/未見評価、既存回帰、必要なE2Eを通す。候補にguard緩和・認可変更が含まれる場合は別のreserved approvalが必要。

## 変更影響

単なる表示誤字、動作変更、契約変更、品質rule変更、toolchain変更、graph再構築、policy/モデル変更を区別する。承認要件を下げず、確定的な依存関係から影響closureを計算する。Semanticaの推定影響は候補として調査する。影響不明を無影響としない。

対象sourceが変われば新candidate。quality rule/toolchain/必要Skillが変わればその対象の資格・結果を失効。索引だけの再構築は元source/意味が同じならコードreceiptまで自動失効させず、query/context品質の再確認を行う。外部公開は開発受入と分離する。

## 故障と復旧

認証/必須guard/原本が不足する対象はHOLD。侵害が疑われるscopeはQUARANTINE。任意UIや補助graph障害は原本参照/限定表示へ縮退。旧writer停止と作用照合が必要ならRECONCILINGに残し、lease失効だけで新writerへ渡さない。

誤拒否は監査可能な根拠と許可主体によるpolicy修正・再資格で解消する。危険作用を別表記へ変える、全guardを無効化する、モデルの安全拒否を回避する設計ではない。固定benign/危険/故障/正規復旧集合で、許可される作業が不必要に止まらないことと禁止作用が起きないことを両方確認する。

## 完成

個別DI/SI完了、ローカルHook green、署名形式valid、graph node数、全文読了、計画のQAを完成の代わりにしない。両repo ReleaseSet・全必要構成・35要求・WP/check・実native/VM/AI/運用・独立review・manifestが一致して初めてDEVELOPMENT_ACCEPTEDとする。未実施はその項目の必要条件を正確に残し、検証できた部分と区別する。
