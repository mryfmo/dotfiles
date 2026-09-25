# 3. 開始手順・作業順序・ブートストラップ

## 開始時に実行すること

A1は初回にSTART_HERE、本章、35要求、全体設計・全IC/MO、WBSの依存と完了条件を把握する。各WP詳細はdispatch前に読む。既存の過去成果物だけを見て作業内容を縮小しない。起動cwdとrepository identityを照合し、明示された作業場所内に専用repositoryを作るか、既存の正しい対象を使用する。同名という理由だけで既存repoを置換しない。

先にWP00の入力台帳を作り、WP01で指定model/effortと本人Auth・agmsgの状態を確認する。次にWP02で仕様の具体化をレビューし、WP03で品質ゲートと実行証跡収集を用意する。WP04契約が凍結されるまでは機能実装を広げない。WP05で開発タスク配送と証拠引継ぎを確立する。

## 基本の直列順

**WP00 → WP01 → WP02 → WP03 → WP04 → WP05 → WP06 → WP07 → WP08 → WP09 → WP10 → WP11 → WP12 → WP13 → WP14 → WP15 → WP16 → WP17 → WP18 → WP19 → WP20 → WP21 → WP22 → WP23 → WP24 → WP25 → WP26 → WP27 → WP28 → WP29 → WP30 → WP31**。

この順は有効なtopological orderであり、必ずこの順だけに固定する必要はない。並列化は`work_packages.json`の依存と実際の書込範囲に基づく。早く終わっただけでは前提WPをacceptedにしない。

| 実装phase | 対象 | 次へ進む条件 |
|---|---|---|
| P0 入力・資格・仕様確定 | WP00–02 | 正本、requested/observed model、前提、具体化が確認済み |
| P1 開発基盤・契約・配送 | WP03–05 | 固定quality inventory、本番契約、独立reviewとagmsg往復が成立 |
| P2 拡張・状態・実行領域 | WP06–14 | assets、DB、authority、snapshot、scheduler、API、VM、Runnerが各受入条件を満たす |
| P3 Native・上流・独立検証 | WP15–21 | 公式接続、調査/設計workflow、Verifier/Reviewerが同candidateで成立 |
| P4 修正・復旧・統合・観測 | WP22–25 | 未完了を適切に戻す/照合する循環が成立 |
| P5 統合資格・自己ホスト | WP26–27 | 実Auth/全assets/実VM合格、単一authorityで安全切替 |
| P6 全工程・敵対的受入 | WP28–29 | 実AI全工程、障害・境界・負荷試験が合格 |
| P7 成果物・最終判定 | WP30–31 | clean install/restore/upgradeと同一RC全検証が合格 |

## 並列化できる例

WP04/05後のWP06（asset）とWP07（store）は独立scopeなら並列可。WP07後のWP08（authority）とWP09（snapshot）も同様。WP14後はWP15（Claude）とWP16（Codex）、WP20（Verifier）を、資源・検証環境の上限内で並列化できる。

ただし、同じcontracts、uv.lock、Makefile、CI、共通fixtureを更新する場合は直列化する。directoryが違ってもinterfaceを同時変更するなら契約ownerが先に更新し、consumerは新hashを入力として再開する。workersを増やすために共通schemaを各branchで別々に改変しない。

## 一WPの実施サイクル

契約読解 → 依存/環境/対象hash確認 → 再現fixtureと失敗するassertion → 本番コード実装 → 局所静的/動作検証 → 全WP対象case → A4独立検証 → A3独立レビュー → 指摘修正 → 再検証 → local統合 → 統合回帰 → WP受入。

REDの理由は、予定した未実装behaviorであることを確認する。依存未導入や無関係なsyntax errorをREDの証拠にしない。既存behaviorを置換しない作業は、before/after回帰とnegative controlを使う。

## ブートストラップの循環を避ける

WP03/05の開発補助ツールはA1/A3/A4で検証し、開発実行の証跡を保存するが、完成製品と呼ばない。WP07以降でSupervisorを作っていても、そのcandidateに自分の変更の受入を決めさせない。実native/VMの試験前に本番DB・署名鍵へ権限を渡さない。自己ホストはWP27のshadow、watermark、独立承認、rollbackを通してから。

## 止まる場合の扱い

AUTH/MODEL unavailable、利用者停止、予算未委任、VM権限なし等は原因と必要条件を記録する。E0/E1の残作業は継続する。部分完了報告は許すが、全体DONE/オールグリーンと報告しない。環境や権限がないという理由でテストをskipして合格させない。

## 継続時

contextが圧縮された、sessionが変わった、通信が切れた場合は最新checkpoint、Git状態、agmsg未処理通知、実processとartifactを照合する。会話中の『終わったはず』を根拠にしない。再開先は最初の未受入WP/attemptとし、完了WPを全部やり直すのでも、未実施項目を飛ばすのでもない。


## 前提が未完成の段階での試験方法

WP00–02の資格確認・契約反例は、既存CLI、手動で監督されたcommand、静的表照合、隔離fixtureを使う。未実装の製品APIを呼ぶことを前提にしない。WP03でcollectorを作った後、同じ資格情報を移さず観測記録を取り直す。WP05以前の小さな作業指示は既存agmsgを直接使い、未完成の製品bridgeへ依存しない。

WP06の実Hooks/Skills資格確認も公式CLIを直接起動するため、製品adapterの完成を待つ循環はない。WP15/16/26で、同じ機能が製品adapter経由でも働くことを再検証する。WP18/19の上流工程レビューは開発用A3とA4で実施でき、製品のReviewService完成後はWP21/28で再実行する。

WP22では副作用のない処理と、作用が不明なら閉じたまま待つ経路を先に実装する。実外部作用の照合はWP23の合格が前提で、それまでは自動再送を許可しない。各WPのcomponent合格は後続統合試験を免除しない。未実装依存をmockで接続した経路はCONTRACTとして記録し、NATIVE_AUTH/VM/AI_E2Eへ昇格させない。


### 早期VM試験の準備

WP09/11のcomponent試験は製品Runnerの完成前に行うため、WP01で資格確認する隔離Linux test VMへ監督されたfixture processを置く。未準備ならE3としてそのcaseを保留する。VMを構築できる権限・hostがある場合はWP01で必要最小のtest VMを準備し、製品の管理/worker/verifier本番配置はWP13で別に実装する。

同様にWP08の認可はdomain単位の試験で、HTTP/OS境界の合格はWP12/13が担当する。component試験と統合試験を分離することで、未完成のserviceへの循環依存と、mockを本物と見せる誤りを避ける。

## 統合契約の作成・利用順

WP02/04でIC01–IC18の型と責任を確定し、WP06（構成）・WP07（状態/intent/inbox）・WP09（sourceと領域）を土台にする。WP10/11はDAGと目標/許可、WP14–17はRunner/native/配送の同一開始経路を実装する。WP18/19はこの経路で上流の並列調査・実験・仕様確定を動かし、WP20/21/22は独立検証・意味レビュー・修正、WP24/25は統合/投影/文脈へ接続する。

各ICのcomponent試験は担当WPで完結し、実native/VM/AI_E2Eのsubcaseは後期WPへ割当済み。IC全体が後期試験を持つことを理由に、前期WPを循環依存させない。WP18→WP10とWP25→WP09の直接consumer依存を明示したが、既存の有効なtopological順を変更しない。

完成済の旧v1実装がある場合は、影響するIC/step/subcaseを差分台帳から再開し、既存証拠はhash/環境/契約一致を確認するまでREQUALIFICATION_REQUIREDとする。計画配布時点では実装状態を引き継がず、全件PLANNED/NOT_RUNである。

## 外部待ちがあっても進める準備lane

WPのdependenciesは受入・統合を解放する前提を示す。本人AuthやVMが待ちでも、A1が必要な設計入力・scope・予算を確認したE0/E1 subtaskはpreparation_only=trueとして別記録で先行できる。内容は資料読解、固定契約の型/試験fixture、現在環境で実行可能な部品実装・局所検証、承認recipe準備に限定し、未実装serviceを本物として起動したとは扱わない。

先行作業はPREPARED_ONLYで、親WPのacceptedや依存解放を発生させない。依存WPの確定成果物とhashが揃った時点で差分照合と必要再試験を行う。未確定の契約に依存する本番動作、外部作用、未委任課金、native/VM実資格は先行不可。この区分により、全体を止めることと依存を飛ばして合格にすることの両方を避ける。


## v4のモデル適合を行う順序

WP01の実資格→WP03の評価inventory→WP04のIC12/schema→WP06のprompt/Skill適合→WP15/16の公式surface→WP17/18/25の情報供給→WP26の全native資格→WP28の比較/全工程→WP30/31のpack配布と認定。WP06単体資格は既存native bootstrapで行い、WP15/16完了に循環依存させない。実評価予算が未承認なら課金laneを待機し、独立したE0/E1を進める。

## ブートストラップ中の強制
WP00–05でも既存native sandbox/権限/専用worktree/保護Git設定を有効にする。まだない製品Policy engineに自分の変更を承認させない。WP04はIC13/14の型とoracle、WP06は実拡張適合、WP07–17は実強制、WP26以降は全native/VM/製品資格を担当する。遅い実環境試験をWP04の完了前提へ逆向き追加しない。

調査資料の並列取得も依存DAGで扱う。対象scopeに既知違反があるtaskは止め、正当な独立taskは継続する。全体順序/32依存は維持する。


## V4の準備laneと依存

WP01は現nativeと本人資格、WP03/05は独立した開発用runner/busでbootstrapする。未実装のSemanticaやquality dispatcherに初期開発を依存させない。WP06は配布・Skill/Hook構成を先に検査し、知識実装が必要な実Hook/ACL試験はWP18以降のWP26へ割り当てる。WP14でquality/Runner、WP18でSemantica接続、WP20/21で独立検証、WP24で直列統合、WP26で全合成、WP27で自己ホスト移管、WP28/29で実AI/障害、WP30/31で運用と受け入れ。

二repoの並列変更はrepository slotをscopeに含める。共通schema/generator/lock/CIのownerは一つ。展開済scopeと全依存・資源予算が揃わない並列実行はしない。新SI/DI単位を別queueへ登録しない。
