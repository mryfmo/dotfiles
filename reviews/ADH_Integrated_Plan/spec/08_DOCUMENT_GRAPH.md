# 文書グラフ・要求から実証拠への契約（IC13）

版4.0.0。10分類はソフトウェア開発の成果物種別であり、10階層の技術アーキテクチャー、実行順序、10個のAgent/Skill、権限の優先度ではない。CHGとEVALはG0からG7まで横断する。C4のContext/Container/ComponentはARCHの拡大率であり、BRD/PRD/SPECと一対一対応させない。[一次資料](../sources/DOCUMENT_GUARDRAIL_SOURCES.md)

## 情報の正本

`contracts/requirements.json`の35MUSTは内容もIDも保持する。構造化要求はその具体化、ACは期待動作、TESTは実行方法、runtime Evidenceは実測結果である。参照があることと、内容が妥当であることは別。重要な主張・設計判断はA3が原本と実験を確認する。製品ソース・step definitions・BDD runnerは今回含まない。

人向け通読版・一覧は生成表示であり、別々に手編集しない。`registers/authority_map.json`が正本/生成物を区別する。本文の矛盾は『下層が詳細だから優先』で解消せず、該当baselineに戻って変更提案を分離する。図の数・文書数・リンク数で網羅性を判定しない。

## 10分類の運用

BRD（目的）→PRD（製品能力）→REQ（構造化要求）→AC/BDD（外部期待）という説明関係を持つ。ARCH+ADRは構成/決定理由、SPECは実装契約、TESTはfixture/判定/試験実装、IPLANは依存と実行計画。CHGは変更・影響・再ゲート、EVALは要求適合と事業目的の両面を管理する。ARCHとSPECは反復して整合させ、TDDは各実装task内のRed/Green/Refactorで行う。TEST全部の完成をIPLAN開始の前提にしない。

入力済み承認仕様はそのまま継承する。BRD/PRDを作るためにユーザー要求を再決定しない。欠落する事業数値は未設定と明記し、ROIやSLAを捏造しない。必要のないC4 Code図や専門用語を追加すること自体を完了条件にしない。

## NodeとEdge

各nodeはid、artifact_type、revision、lifecycle、normative、owner、path/selector、content_digest、source/review/approvalへの参照を持つ。lifecycleは本文からmodelが自己付与せずAuthorityが決める。計画配布ではSPECIFIED_NOT_IMPLEMENTEDであり、runtimeの承認署名は存在しない。

edgeは `refines / specifies / motivates / verifies / planned_implementation / planned_verification / depends_on / governed_by / derives_from / supersedes` を区別する。`planned_implementation`を`implements`、`planned_verification`を`verified_by`と誤表示しない。要求から実装commitや実行証拠へのedgeは後続が実データで追加する。schema検査だけで実装済のedgeを発行しない。

文書の相互参照にcycleがあることとtask DAGのcycleは別。`depends_on`のtask部分と`supersedes`は循環禁止、verifies/refines等はrelation別の定義で検査する。すべてのedgeを一括topological sortしない。参照存在、型、方向、revision、owner、適用baselineの整合を検査し、意味の誤結合はA3の責任範囲とする。

## TaskPacketへの投影

全体の文書は保持するが、Agentへ毎回10冊全部を注入しない。A1の初回全体理解、A2の当該契約読解、A3の独立レビューを区別する。TaskPacketへ目的、MUST本文、scope、必須AC/SPEC、重要な禁止とactive guardの短い理由、検査inventory、停止/再開条件を必須として入れる。出典・候補・長いログはpath/範囲/ACL付き参照にする。

TaskPacketにdocument_graph_ref、document_graph_digest、normative_closure_digest、artifact_refs、active_guard_ids、guard_policy_digest、authorization_refを保持する。`execution_authorized`というboolやLLM生成のrefだけでは権限を与えない。実認可はIC14の実施点で照合する。全graphのdigestは監査用、受け入れ失効は対象taskの凍結したnormative closureと適用policyを基準とする。無関係な文書の誤字修正で全taskを失効させない。

source fileとnode本文のhashは必要なら別に保持する。canonical recordは本版の固定JSON表現（UTF-8、sort_keys、最小separator、NaNなし）を用い、RFC8785完全準拠と呼ばない。本文改変が同じhashを保つなどの仮定は置かない。read ledgerは取得記録であり理解の証明ではない。compaction/new session/rebindは有効性を再評価し、unknownを既読扱いしない。

## 変更・再ゲート

CHGは変更requestのactor、reason、before/after digest、変更分類、影響node/task/receipt、委任/承認、再検証、rollbackを持つ。影響解析が不明なら検証範囲を保守的に広げる。承認済み仕様の変更は署名済範囲へ束ね、意図せず影響する下流を新しい正本へ混在させない。過去合格履歴は保持しcurrent-validを失効する。

## 永続化・構成

DocumentRegistry/GraphResolverは既存Supervisor/Context/Evidence serviceのモジュールとし、第二DB・Graph DB・新LLMルータ・追加常駐daemonを要求しない。既存SQLiteにnode/revision/edge/checkpointの所有tableを追加する。型付き参照と状態の認可をR01–R35と同じ開始/受け入れ経路へ統合する。

## 後続の完成条件

10分類の索引と正本が対応し、35MUSTからSPEC/AC/TEST/WPへ漏れなく辿れ、重大な意味矛盾0、参照/版の不一致0、CHGに基づく失効が正しく、TaskPacketが必須制約を落とさず既存モデル比較を通ること。BDD構文、リンク、schema、文書QAだけを製品合格にしない。

<a id="dg01"></a>
## DG01：10分類は直列工程でもC4階層でもない

担当：DocumentRegistry。要求：R01, R09, R10, R12。

規範：10分類をsource/view別に登録。C4はARCH図の粒度、EVAL/CHGは全工程参照として初期から登録。

拒否・反証：PRD=Container固定、10文書全文必読、L10完成後しか評価しない循環を検出。検査割当：V02-01, V02-04。

<a id="dg02"></a>
## DG02：要求IDとEARSの意味保存

担当：Requirements/Reviewer。要求：R01, R05, R09, R12。

規範：35原要求をbyte維持しEARS refinementのtrigger/state/response/観測条件を対応付ける。

拒否・反証：EARS整形の過程で例外/非機能/対象範囲を削る、単位未定義で確定することを拒否。検査割当：V00-02, V19-05。

<a id="dg03"></a>
## DG03：期待仕様・oracle・試験定義・実証拠の分離

担当：Verifier/Reviewer。要求：R20, R22, R34, R35。

規範：ACから独立oracleと固定caseへの参照があり、未実施resultを含めず期待仕様を保存。

拒否・反証：BDD文だけ、固定出力文字列、学習対象の自己採点でPASSにすることを拒否。検査割当：V04-04, V20-05。

<a id="dg04"></a>
## DG04：版・status・意味付き参照グラフ

担当：DocumentRegistry/Resolver。要求：R01, R10, R11, R12, R34。

規範：文書nodeのid/revision/status/hash/ACLとtyped edgeを検査し、R→SPEC→WP→TESTが辿れる。

拒否・反証：参照切れ、同ID別本文、supersededをcurrent、future revisionや未承認sourceをnormativeにすることを拒否。検査割当：V04-01, V18-02。

<a id="dg05"></a>
## DG05：タスク依存DAGと文書グラフを混同しない

担当：Scheduler/Graph。要求：R12, R17, R18。

規範：依存taskはDAG、文書のverifies等の相互参照は許可し、依存受入後だけnodeを実行。

拒否・反証：文書の相互参照を理由に全停止、または循環taskを実行してしまうことを検出。検査割当：V10-01, V10-06。

<a id="dg06"></a>
## DG06：TaskPacketは関連閉包と必須制約を保持

担当：Context/Qualification。要求：R01, R02, R12, R29, R30。

規範：要求・scope・active guard・AC/SPECとrevisionを必須文脈にし、根拠は必要時参照にする。

拒否・反証：全10冊注入、重要禁止をoptionalリンクだけにする、別taskのgrantを取得することを拒否。検査割当：V17-04, V18-06。

<a id="dg07"></a>
## DG07：変更・失効・再ゲートは全工程に横断

担当：Change Authority。要求：R01, R11, R24, R33。

規範：CRの対象hash・種類・impact閉包・承認主体・再ゲートを確定し、無影響taskは継続。

拒否・反証：semantic変更を誤字として旧合格を維持、変更の度に全task無期限停止を拒否。検査割当：V08-05, V24-05。

<a id="dg08"></a>
## DG08：証拠・調査・実験の由来を失わない

担当：Research/Architect。要求：R03, R04, R05, R07, R08, R10。

規範：claim→source revision→experiment→ADRを記録し、実験NOT_RUNは判断の未検証項目として残す。

拒否・反証：リンク件数/長文だけで十分とし、失敗実験を成功ADRへ書換えることを拒否。検査割当：V19-01, V19-02。

<a id="dg09"></a>
## DG09：役割・モデル別の必要時取得と評価

担当：Context/Evaluator。要求：R14, R15, R18, R29, R34。

規範：同モデル/effort/課題/guardでTaskPacket関連取得が要求を落とさず完遂することを測る。

拒否・反証：最適化を口実にguardや必須oracleを外す、旧ReadLedgerを全セッションへ流用することを検出。検査割当：V28-01, V28-06。

<a id="dg10"></a>
## DG10：単一正本・生成表示・再現可能な配布

担当：Release/Document tooling。要求：R01, R27, R31, R34, R35。

規範：authority mapに従いJSON台帳から人向け表示を生成、graph指紋・manifestと版を照合。

拒否・反証：通読版だけを編集して正本と乖離、過去PASSや計画QAを製品PASSへ流用することを拒否。検査割当：V31-01, V31-03。
