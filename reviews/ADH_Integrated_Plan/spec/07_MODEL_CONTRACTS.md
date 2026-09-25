# モデル別契約 MO01–MO12

以下はIC12と既存ICの具体化。採否・WP割当は決定済みで、すべて規範仕様である。検証はすべてNOT_RUN。正常系だけでなく反例と実nativeを含む。

## MO01：完全な正本とモデル向け指示の分離

責任：ContextProjectionService / Baseline Authority。要求：R01, R11, R12, R15, R18, R20, R27, R35。担当WP：WP00, WP02, WP03, WP04, WP06, WP17, WP20, WP31。

1. 要求・アーキテクチャー・必須検査は全量保存し、正本hash・制約IDを維持する。instructionの短縮は要件の削除を意味しない。

2. 指示項目をhard_requirement / enforced_policy / role_contract / model_guidance / task_dataへ分類する。最初の3種は意味を固定し、比較ではmodel_guidanceと重複表現・資料の提示方式だけを変える。task_dataの事実・要求は同一に保つ。model_guidanceは認可を与えない。

3. 同じ安全規則を各Skillへ複写しない。短い共通制約を一度、該当roleを一度、task packetを末尾へ配置する。監査者向け全文を毎ターン注入しない。

4. prompt/profile/renderer/catalogのdigestを既存effective policy/assets hashへ束ねる。既存の6種hashの意味・独立検証の固定suiteを減らさない。

出典となる公開契約：OPT-S01, OPT-S04（[索引](../sources/MODEL_SOURCES.md)）。本文の契約と試験条件はADHの決定。

## MO02：Astra向けの狭い発火条件と段階的Skill読込

責任：AssetCompiler / SkillRouter。要求：R14, R15, R18, R29, R33, R35。担当WP：WP03, WP04, WP06, WP16, WP26, WP28。

1. Skillの入口は一業務と適用条件を明示する短いdescription。領域名が一致するだけの広い発火や全タスクに適用する強調を除く。

2. rootは目的・入力・分岐・出力のrouterとし、詳細は同梱referencesへ置く。全referencesの一括読込を要求しない。

3. カタログ表示・適用判断・実本文ロード・実行効果を別に観測する。適用すべき事例と近接非適用事例を対にし、absence/duplicate/description truncationを検査する。

4. 8個のADH入口はqualified role profile内で上流Skillの入口と一対一で対応付ける。既存のSuperpowers等を全部残して両方を自動発火させない。機能を捨てず、採用入口・参照先・有効Hookを一意にする。

出典となる公開契約：OPT-S01, OPT-S04, OPT-S05（[索引](../sources/MODEL_SOURCES.md)）。本文の契約と試験条件はADHの決定。

## MO03：版付き読了台帳と必要箇所の文脈供給

責任：ContextProjectionService。要求：R01, R03, R04, R06, R12, R29, R34, R35。担当WP：WP00, WP04, WP05, WP09, WP17, WP18, WP25, WP28。

1. A1は初回に全要求・全IC・依存と完了条件を把握する。A2/A3は担当taskに必要な契約を読む。毎編集の全文再読ではなく、既読版・対象scope・関連差分を確認する。

2. ReadLedgerはactor、native session、context epoch、source digest、ranges、purposeを保持する。取得完了を理解の証明とみなさない。

3. 同じhashでも新session/compaction後の内容保持を仮定しない。必須制約とcurrent checkpointを再提示し、不明な関連本文は再取得する。過去eventを編集・削除しない。

4. task packetに必須要求・禁止条件・完了基準を直接含め、巨大な参考資料だけを参照化する。取得不能の必須根拠はUNKNOWNで当該判断を止め、独立作業を続ける。

出典となる公開契約：OPT-S01, OPT-S04（[索引](../sources/MODEL_SOURCES.md)）。本文の契約と試験条件はADHの決定。

## MO04：Astraの許可範囲内の完遂と検証の段階化

責任：CodexAdapter / RepairCoordinator。要求：R02, R18, R19, R20, R21, R23, R25, R32。担当WP：WP05, WP06, WP16, WP20, WP22, WP28。

1. task packetは編集・許可recipe・使い捨てfixtureの検査・修正・再検証を委任済み範囲として明記する。初回実装で人へ返す条件にしない。

2. workerのdoneは候補と必要証拠が揃ったready_for_review。外部の独立review/acceptanceと区別する。通常の失敗は原因分析して継続し、停止するのは本当に必要な判断・権限・予算・USER_STOP。

3. 開発中は影響検査、WP候補は指定inventory、独立Verifierは別環境、統合は新snapshot、最終RCは全件、と責任を固定する。毎編集の全suite実行は要求しない。

4. 同stage内の同snapshot/suite/envによる不要な繰返しは理由を記録する。独立性のための再実行・変更後の再試験・最終RC再検証をキャッシュで省略しない。

出典となる公開契約：OPT-S01, OPT-S06（[索引](../sources/MODEL_SOURCES.md)）。本文の契約と試験条件はADHの決定。

## MO05：Fableの独立読取・委任・統括作業の並列進行

責任：ClaudeAdapter / Scheduler。要求：R04, R12, R16, R17, R18, R31, R32。担当WP：WP05, WP10, WP14, WP15, WP17, WP19, WP28。

1. 結果の依存がない取得・分析はまとめて要求してよい。結果依存や同writerの変更は順序を守る。単にtool call数を減らすために巨大shellへまとめない。

2. agmsg dispatchは耐久受領を確認して返す。A1をworker完了まで強制blockせず、別の調査、次task準備、到着結果の照合を進める。

3. 依存がすべて待機中なら新しい作業を捏造せず、bus待機または状態照会で待つ。定期LLM呼出を進捗としない。

4. 並列数は既存DAG・allowed_files・CPU/メモリ/port・契約予算で制限し、Skillやmodel特性から新規workerを無制限にspawnしない。

出典となる公開契約：OPT-S02, OPT-S06, OPT-S07（[索引](../sources/MODEL_SOURCES.md)）。本文の契約と試験条件はADHの決定。

## MO06：Fableの公開進捗表示と非公開履歴の分離

責任：ClaudeAdapter / ProjectionService。要求：R18, R25, R30, R31, R35。担当WP：WP04, WP15, WP25, WP26。

1. 依頼の開始・実際の工程変化・重大な発見/待機を短く表示する。ツール出力が画面に見えるとは仮定しない。

2. 公式nativeから取得できる公開text/statusのみを利用する。APIのthinking.display betaをCLIへ勝手に渡さない。非公開thinking・encrypted contentの取得/変換/開示は求めない。

3. nativeが進捗textを公開しない場合はSupervisorの事実イベントをラベル付きで表示する。これはモデル思考の再現ではなくengine status。可観測性の限界を記録する。

4. heartbeat、長文、待機pollを成果進捗へ数えない。更新にはphase、完了事実、未完了、必要な判断を対応させる。

出典となる公開契約：OPT-S02, OPT-S07（[索引](../sources/MODEL_SOURCES.md)）。本文の契約と試験条件はADHの決定。

## MO07：Fable履歴の所有権・正確な再開・安定prefix

責任：ClaudeAdapter / ContextProjectionService。要求：R13, R15, R18, R24, R29, R31, R33, R35。担当WP：WP06, WP15, WP17, WP22, WP25, WP28, WP30。

1. 公式CLIのsession/historyをnativeが所有する。SupervisorはTaskPacketを新しい入力として渡し、過去のprefixやthinking blockを抽出して改変・再注入しない。公式が公開するtranscript/eventのread-only観測は別であり、秘密・非公開推論を収集しない。

2. model/profile/system/assetの意味変更は新runとして資格確認し、現在runを黙って書き換えない。exact resumeは同じbindingと有効構成でのみ行う。

3. 静的role指示と変化するtask資料を分離する。不要な時刻・乱数・巨大manifestを静的指示へ差し込まない。cache hit/内部context節約は公式観測がある場合だけ報告する。

4. Messages APIのadaptive thinking、forced tool_choice、binding-controls、mid-conversation betaはAPI固有。CLI設定として実装せず、unsupported指定をqualificationで排除する。必要な構造化出力は採用native surfaceとschemaを実証する。

出典となる公開契約：OPT-S03, OPT-S07, OPT-S08（[索引](../sources/MODEL_SOURCES.md)）。本文の契約と試験条件はADHの決定。

## MO08：Fable上流判断・変更範囲・出典表現の適合

責任：ResearchLead / IndependentReviewer。要求：R03, R04, R05, R07, R08, R09, R10, R12, R21, R27。担当WP：WP02, WP18, WP19, WP21, WP28。

1. 指定資料・重要なAPI/機能の事実は一次資料へ戻る。既知という感覚だけで現行動作を断言しない。引用と独自要約を区別する。

2. 依頼の目的・必須機能・制約・完了条件を先に固定し、要求全体をカバーする。小さな変更を全面再設計や無関係な品質改善へ拡張しない。

3. 最小差分はMUST/NFR/エラー経路/テスト削減の根拠にしない。Fableは計画・文書・レビューを担当し、ソース実装の変更はA2へ委任する。

4. 設計/レビュー出力は結論、根拠、対象location、未解決、次の判断を短く明確にし、私的推論全文を納品条件にしない。規範仕様の詳細は正本へ保存する。

出典となる公開契約：OPT-S02（[索引](../sources/MODEL_SOURCES.md)）。本文の契約と試験条件はADHの決定。

## MO09：role・Skill・subagentを通したmodel/effort固定

責任：QualificationService / AssetCompiler。要求：R13, R14, R15, R25, R33, R35。担当WP：WP01, WP04, WP06, WP15, WP16, WP26, WP30。

1. A1/A3=Fable-5.1 high、A2=GPT-6 Astra xhighを維持する。表示名、requested config、runtime受理、観測modelを別に記録する。非公開計算量をeffort値から推定しない。

2. Skill frontmatter、subagent profile、plugin内launch、fallback chain、managed/user/project設定の上書きを完全closureで調査する。より小さいモデル/effortへ暗黙変更しない。

3. model/effortは単一profile正本で宣言。Skill本文にnative未対応のfieldを増やさず、共通入口はmodel/effortを省略して資格済みsessionから継承する。forkがある場合は子の有効設定も確認する。

4. 利用不可は対象をBLOCKED/UNKNOWNにし、代替モデルで受入を作らない。最適化比較の全armも同一モデル/effortを使用する。

出典となる公開契約：OPT-S03, OPT-S05, OPT-S06, OPT-S07（[索引](../sources/MODEL_SOURCES.md)）。本文の契約と試験条件はADHの決定。

## MO10：上流Skillsの重複・承認・役割の一体適合

責任：AssetCompiler / IndependentReviewer。要求：R02, R14, R15, R16, R17, R18, R21, R25, R29。担当WP：WP05, WP06, WP10, WP21, WP24, WP26。

1. Superpowers/UA/Crit/Ponytail/agmsg/CompactionDBの機能をkeep/rewrite/route/reference-only/disabled-with-replacementで一つずつ対応させる。単純な全無効化と全有効重ね掛けを避ける。

2. 強制Skill呼出・毎taskの人承認・同じ制約の繰返しは、正本/Mandateを確認し、許可済の開発は継続できるよう適合する。安全な承認をUIクリックや利用者偽装で通さない。

3. fresh implementer方式と常駐worker方式を統一する際は実装/仕様レビュー/品質レビュー・独立contextの機能を維持する。review担当は作者sessionを継承しない。

4. 供給元commit、ローカル差分、理由、テスト、licenseを記録し、利用者HOMEではなく隔離した配布対象に適用する。MCP導入を前提にしない。

出典となる公開契約：OPT-S01, OPT-S04, OPT-S05（[索引](../sources/MODEL_SOURCES.md)）。本文の契約と試験条件はADHの決定。

## MO11：固定モデルの比較評価と効果・安全性の分離

責任：IndependentEvaluator / ReleaseAuthority。要求：R08, R15, R20, R21, R27, R32, R34, R35。担当WP：WP03, WP06, WP20, WP21, WP26, WP28, WP29, WP31。

1. H00対照、H10 Fableのみ最適化、H01 Astraのみ最適化、H11両者最適化の2×2設計。全armのコード・要求・oracle・native版・モデル/effort・権限・資源を固定する。

2. 各arm6scenario×3反復=18、合計72の実AI runを比較用に計画する。H11の18を既存製品18runと同一runとして利用する条件を明示し、別の成功件数として二重計上しない。予算は実行前にHが有限値を設定する。

3. プロンプト文字数だけでなく受入率、false complete、不要な停止、再読、重複tool/検査、時間、利用量を観測する。未観測値を0や推測値で埋めない。

4. 安全・品質ゲートを先に満たし、効率は副次判定にする。失敗runを捨てず、同条件・同oracleの全結果を報告する。少数回で一般的最適性や統計的非劣性を主張しない。

出典となる公開契約：OPT-S01, OPT-S02, OPT-S04（[索引](../sources/MODEL_SOURCES.md)）。本文の契約と試験条件はADHの決定。

## MO12：model packの版固定・差分更新・切戻し

責任：AssetAuthority / Operations。要求：R11, R15, R22, R25, R27, R33, R34, R35。担当WP：WP06, WP26, WP30, WP31。

1. 元v2からの差分をCR-MODEL-001として記録し、35要求/192基本条件/44統合subcaseを維持したままモデル最適化を追加する。

2. Profile・prompt・Skill router・reference・描画規則・native binding・評価条件を一つのpack digestで固定する。動作中のpackを黙って更新しない。

3. 更新は隔離候補→diff/静的検査→native/性能比較→安全品質→承認済切替。効率が悪化/不確実なら勝手に低effortへ下げず、packの修正または既資格packへの運用上の切戻しとする。

4. 文書作成と構造検査のPASS、native適合、行動評価、効果測定、製品完成の状態を別々に報告する。本配布物は文書・prompt・Skill定義であり製品コードを含まない。

出典となる公開契約：OPT-S04, OPT-S05, OPT-S06, OPT-S07（[索引](../sources/MODEL_SOURCES.md)）。本文の契約と試験条件はADHの決定。

## MO共通のV3.1適合

MO01/02/03/10ではIC13の型付きclosureから必要情報を選び、MO04–09ではIC14を短い制約として説明し、実際の強制は外側の責任者が担う。MO11/12の比較・更新では同一のguard policy/oracleを固定する。ガードの増加を口実に全体全文・全Skillを一括注入しない。モデル・effort・認証・既存80subcaseの削減や緩和はしない。
