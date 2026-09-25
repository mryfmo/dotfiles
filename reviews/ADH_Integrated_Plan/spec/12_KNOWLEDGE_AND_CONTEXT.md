# 正本・UA・CompactionDB・Semantica・TaskPacketの統合仕様

規範はIC16とIC09/12/13/14。意味検索は認可ではなく、参照graphは正本の代わりではない。[V4-S04][V4-S05][V4-S06]

## 1. データの意味を分ける

正本のREQ/AC/ADR/SPEC/TEST/IPLAN/CHG/EVALと型付きedgeは、要求と検査の規範関係を持つ。UAは特定code snapshotの解析観測、CompactionDBは過去の記録・選別記憶、Semanticaはそれらの横断探索/影響候補を提供する。抽出・類似・因果候補を、明示契約のedgeへ自動昇格させない。学習が『approved』と述べても管理DBの承認は変わらない。

## 2. 初期採用範囲

ADH repositoryのintegrations/semanticaに一つのadapter実装と専用pyproject/uv.lockを置き、dotfilesにはそれを呼ぶ薄いwrapperだけを配る。初期は構造化入力からのContextGraph/KG構築、来歴query、明示依存の探索、限定context/exportを使う。外部LLM・embedding・新graph DB・MCP・全extrasを暗黙有効化しない。SDKがin-memoryであることとadapterの保存/再構築を混同しない。

非構造文書の意味抽出は指定nativeが出典付き候補を生成し、別schema/出典検査を経てcandidate relationとして投入する。semantic confidenceは数値範囲内でも正しさの証明ではない。秘密情報や第三者データを不用意に永続化せず、取得許可/保持/撤回を適用する。

## 3. 読み書き契約

入力はproject_id、trust_domain_id、source snapshot、baseline revision、ACL digest、adapter/schema/upstream revision、原本locator/range/hash、relation kind/statusを含む。正本IDをnamespace付きで保持。無効日付や範囲外timestampを常時有効に補完しない。

操作はingest/query/context/impact/verify/rebuild。これはADH adapterの操作名でありSemantica公式コマンドを捏造したものではない。自由なCypher/SPARQL、任意保存先、任意plugin importはAgentへ公開しない。queryは許可済project/baseline/snapshot、目的、上限、任意の明示IDを受け、source付き結果またはstale/unavailable/errorを返す。

## 4. ACL・版・来歴

候補抽出・rankingより先に許可subgraphへ制限する。不可nodeの名前・件数・pathを診断に漏らさない。cache keyはproject/trust/baseline/source/ACL/schema/adapter/upstreamを含め、HEADだけにしない。pathはrealpathと所有scopeへ正規化し、外部symlinkと別worktree混入を拒否する。

明示edgeと推定edgeの証拠は別種。関係がないという検索結果は、影響なしや検証不要の証拠にならない。必須closureはDocumentRegistryの型付き依存から取得する。Semanticaは関連資料、過去事例、反例候補の補完に使う。

## 5. 更新・縮退・保持

取込proposalは各workerが提出し、公開索引はproject単位の一writerだけが生成/検査/原子公開する。更新中は旧snapshotを読む。クラッシュ後は未公開版を破棄または原本照合して再構築し、部分graphを公開しない。公開済み版への可変上書きを禁止する。

破損/停止/古い索引では同じ必須closureの原本取得へ縮退できる。取得不能なら当該taskをHOLD。他の独立taskやcommit品質検査は継続する。最終受け入れに必要な知識adapterの実証試験は縮退で免除しない。

retentionは派生cacheと保護原本を区別する。保持削除は日時方向・境界・0・負数・withdrawn・法的保持相当の保留を検査し、protected evidenceを削除しない。deleteは認可されたmanifest対象のみ。削除/再構築履歴は残す。

## 6. TaskPacket

TaskPacketには役割promptを重複注入せず、当該REQ/AC/SPEC/検査/guardの必須条件、normative_closure_digest、source refs、使用したknowledge snapshot、quality_plan_ref、ReleaseSetを入れる。必須要件をtop-kに任せない。長文は原本rangeを取得できる短縮表示にし、中央のFAIL/例外・未解決件数は構造データで保持する。

ReadLedgerは読んだhash/range/context epochの記録であり理解の証明ではない。新session/compaction/基準変更後に再利用可否を評価する。公式native内部の履歴/KV cache/thinkingを外側から加工・復元したと主張しない。

## 7. 評価

既知関係の往復、誤引用、ACL負例、2worktree、並列更新crash、retention、索引無しの原本回帰、悪意approved文字列、指定nativeの正負Skillを試験する。K0=原本検索、K1=Semantica補助を同資料/質問で比較し、必要根拠の欠落・誤引用は0を固定fixture条件とする。時間・文脈量・未確定情報も全件報告し、graphの大きさだけを性能としない。
