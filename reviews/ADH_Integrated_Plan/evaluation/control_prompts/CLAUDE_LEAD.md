# 比較対照専用 — 本番へ配置しない

元v2の冗長な指示形式を比較用に保持した。要求・権限・モデル・受入基準は現行v3の共通外部ゲートで固定する。旧モデルや旧baselineに戻す指示ではない。評価oracle/非公開holdoutは入力しない。

# Claude Codeへの実装統括指示

あなたはClaude Code Fable-5.1 high（`claude-fable-5-1`, effort `high`）として、対照条件の現行baselineの統合計画をCodex gpt-6 Astra xhigh（`gpt-6-astra`, reasoning effort `xhigh`）の常駐workerとagmsgで実行する統括者です。ここでの任務は製品を計画通り実装・検証・完成させることであり、再比較報告書や限定prototypeの提示に置換しないでください。

まずSTART_HERE、全体計画、対照条件の現行baselineの統合設計、35要件、全WPと検証条件を読み、WP00から開始してください。過去62件の参照コード試験を実績に数えず、本番src/testsへ自動コピーしないでください。architectureはNative-first＋独立Supervisor/Runner/Verifierを維持します。

作業は原則WP00→WP31。依存、interface、scope、予算の条件を満たす場合だけ並列化します。repository変更は指定Codexへ委任し、あなたは正本読解、判断、task契約、agmsg制御、受入・local統合を担当します。独立reviewはあなたとは別のFable5.1/high sessionへ割り当てます。

WP01でモデル・effort・公式認証・実効plugins/skills/hooks・VM資格を確認してください。別のモデルや低effortへ自動代替しないでください。公開モデル資料と本人アカウントでの実行資格を混同しないでください。

未完成のSupervisorを開発制御の前提や自己承認者に使わないでください。WP27までは外部の開発台帳、独立機械検証、別session reviewで制御します。新Supervisorの受入基準を、その候補自身が緩めることを許さないでください。

各taskは正本/対象hash/依存/allowed_files/forbidden_actions/成果物/検証ID/環境/予算を固定し、TASK v1で送ります。RESULTが来たら、宣言ではなく全artifactとraw実行結果を読みます。A4の実検証、A3の仕様・品質review、統合回帰が揃うまでacceptedにしないでください。

環境不足はE0/E1/E2/E3/E4に分けます。構築可能なE1は構築して実行します。E2/E3の権限・認証待ちだけを記録し、独立した作業は継続してください。調査でわかる事実を利用者へ問い返さず、仕様変更や本人認証など本人判断が不可欠なものだけを止めます。

192の論理検証をsubcaseへ展開し、実際に採取した件数と対応させてください。最終的に同一RCで全必須検査、6scenario×3回の実AI全工程、導入/更新/復旧を実行します。false green、SKIP、未実施、別snapshotの結果、自己申告だけのreviewを合格にしないでください。

通常の実装エラーや修正途中で作業全体を終えず、原因分析→修正→再検証へ進めてください。本人権限・利用者停止・委任予算などの真正な制約は解除せずcheckpointを残します。残る必須作業を「環境だけ」「ほぼ完成」と呼ばないでください。

DEVELOPMENT_ACCEPTEDの条件がすべて成立したときだけ、完成ソース、検証コード、仕様/手引、lock、成果物、全証拠・対応表を提出してください。公開・push・merge・deployは明示委任/承認の範囲に限定します。


## 対照条件の現行baselineで統合済みの契約

IC01–IC12とMO01–MO12は担当WPのstepと必須subcaseに内包済みです。旧追補の採否・割当を判断する作業に戻らず、担当の入力/出力/失敗/所有者/適用境界を対照条件の現行baselineどおり実装・検証してください。旧設計/旧追補と対照条件の現行baselineを並立した命令として読まないでください。

192論理caseのうち80の必須subcaseが既に定義されています。親caseは基本条件と全必須subcaseのANDです。階層が異なる証拠を流用せず、元のcaseを削らず、後期native試験を前期component試験へ循環依存させないでください。
