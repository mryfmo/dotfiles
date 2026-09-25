# V4開始・作業順序・二repo引継ぎ

## 準備と入力

START_HERE→設計の責任・正本・完了→component catalog→全体WBSをA1が初回把握する。A2はTaskPacketと該当契約/変更範囲/検査を読み、既読の変更なし資料を全量再読しない。read省略を未読の読了宣言にしない。

実rootはWP00で確認し `dotfiles` と `adh` のrepository_id/realpath/HEAD/dirtyを記録する。未作成ADHの場所は操作者の委任を確認して作成する。既存ユーザーデータを上書きしない。

## 作業順序

1. WP00–02: 正本・現行差分・実model資格・必要環境・契約を固定する。component未選択は理由を記録する。
2. WP03–06: 開発用品質runnerとagmsg、schema、配布源と10Skillの適合を実装する。現native資格と将来knowledge実装試験を混同しない。
3. WP07–14: state/event/outbox、権限、source snapshot、DAG/所有権、予算、API、実VM、Runner/qualityを実装する。
4. WP15–21: 両native adapter、agmsg bridge、Semanticaによる根拠供給、上流仕様策定、独立Verifier/Reviewerを実装する。
5. WP22–25: 失敗分類、作用照合、並列/統合、学習/記憶/traceを接続する。
6. WP26–29: 実Auth/全selected assets/VM、shadow切替、実AI全工程、セキュリティ/故障/容量/比較を実施する。
7. WP30–31: 同じ二repo ReleaseSetでclean install/upgrade/rollback/restore、旧回帰と全受け入れを照合し、完成成果物を提出する。

各WPは前提→必要な負例/再現→実装→局所試験→全担当case→A4→別context A3→修正→直列統合→回帰→受け入れ。親PASSで内包未実施を隠さない。

## 並列化

許可されるのはaccepted依存・非重複scope・専用worktree/identity・有限資源が揃うtaskのみ。WP06/07、WP08/09、前提成立後WP15/16等を並列化できる。knowledgeとquality開発はWP18と関連担当が依存成立後に分離scopeで進める。署名/共通schema/lock/設定generator変更は調整して一writer。Herdrのpane数を完遂率とみなさない。

## 二repo変更の納品

dotfiles側は設定・generator・asset lifecycle・薄いwrapperと該当既存テスト、ADH側は実装と契約。candidate pairをReleaseSetへ記録し、pair全体でqualificationを実行する。Git commit2件は分散transactionではない。active pointer変更は配布側で原子的に行い、未成功なら旧pairへ戻す。保留中にremote push/mergeしない。

## 再開

最新checkpointのinput/spec/profile/ReleaseSet/source、実Git、未ack bus、実process、quality/knowledge generation、未解決findingを照合する。ユーザー停止・予算・権限・不明外部作用を勝手にREADYへ戻さない。独立作業は続ける。

## 終了基準

両repoの全実装・全必要試験・運用・独立レビューが同候補に揃うまでDEVELOPMENT_ACCEPTEDではない。実行不能条件は対象case/tier/不足権限/回避不能理由/次の操作を明記し、mockを実証に替えない。範囲内で構築可能な環境は構築する。
