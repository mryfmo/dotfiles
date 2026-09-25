# モデル別最適化の統合仕様 — v4.0.0

## 決定と適用面

本版は「モデル名を設定する計画」から「指定モデルで動く指示・Skills・文脈供給・比較評価まで含む統合仕様」へ改訂する。A1/A3はFable-5.1 high、A2はGPT-6 Astra xhighのまま固定する。努力量を下げる最適化、認証の転用、権限拡大、MUSTや検証の削減は行わない。

モデル固有の仕様と行動指針の確認資料は[sources](../sources/MODEL_SOURCES.md)。以降のデータ構造、数値目標、割当、検証基準は本計画が決定したもので、ベンダーの性能保証ではない。取得した公開仕様と本人のnative実行資格は別に検証する。

本配布物には完成した役割別promptと10個のSkill入口/参照文書を含む。これらは製品の中途実装ではなく後続が使う指示資産である。指示資産の内容を作成したこと、native適合が通ること、比較で効果が出ることを別状態にする。

## 1. 一つの正本と二つの読み方

規範は35要求、IC01–IC18、MO01–MO12、WP00–31、192親caseと内包subcaseにある。完全な仕様は保持する。一方、モデルに渡す文章は役割・task・版に合わせて選択する。全体計画を小さくするのではなく、毎回の重複注入を減らす。

| 分類 | 変更/処理の所有者 | モデルへの提示 |
|---|---|---|
| hard_requirement | Baseline Authority | 当該taskの要求と受入条件を省略せず提示 |
| enforced_policy | Supervisor/Runner/Verifier | 短い許可・禁止範囲を提示。実際の拒否はコード/OSで強制 |
| role_contract | A1/A2/A3/A4の固定分担 | 共通＋該当役割のみ、一context epochに一度 |
| model_guidance | qualification済model pack | Fable/Astraの役割に合う最小の追加指示 |
| task_data | 原本付きContextEnvelope | 必須事実は本文、長文根拠はhash付き参照と必要範囲 |

A1の初回は全要求・全体構造・依存・完了条件を把握する。個別タスクのA2/A3には担当契約・入出力の両端・関連全要求を渡す。全体の責任を理解することを、毎編集で全文を再読することと混同しない。初回通読と既読再利用は両立する。

## 2. 指示組み立て契約（IC12）

入力：qualified ModelExecutionProfile、Baseline、TaskContract、ExecutionBinding、ReadLedger、SkillCatalogView、固定検証inventory、利用可能context予算。

出力：PromptPlanとTaskPacket。PromptPlanはどのsource/digest/rangeをどのslotへ置くか、未掲載の参照先、必要なskill入口、表示先、固定suite参照を保持する。bootstrapはA1が同じ形式で作成し、未完成compilerへ依存しない。製品化後は既存assets/context serviceの責任として実装し、別のLLMや第二のSupervisorを追加しない。

並びは共通制約→役割prompt→task-specific packet。nativeの既定system promptを空へ置換せず、採用版で確認した追加入力・設定方法を使う。Skill本文は必要時にnativeが読み込む。不要な日時/乱数を安定promptへ埋め込まない。request ID/challenge等の機械metadataは保護sidecarに保持する。

同じ段落の強調を各Skillへ複写しない。promptのhashだけでなく、有効Skill/Hook/rendererもpolicy/assets hashへ連結する。TaskPacketが短くても、合否は完全なsuite inventoryで決定する。

### 著者側の初期目標値

これらは本計画の編集目標でありnativeの上限値ではない。Skill descriptionは160 Unicode code points以内、root SKILL.mdは1,800 UTF-8 bytes以内、common＋roleは6,144 bytes以内を初期目標にする。超えた場合は重複・適用範囲をreviewし、情報を無条件に切り詰めない。必要な契約・例外条件は保持し、承認付きの理由で編集目標を超過してよい。

nativeのcontext容量・skills catalog予算は採用版で測定する。古い固定値を仕様として当てはめず、実効catalogが必要な入口を含むかを検査する。モデル内部token数・KV cache・thinkingは外側から完全制御できると主張しない。

## 3. 各モデルへの実行方針

### Astra/xhigh — 実装worker

目的、入力、scope、完了基準、許可された反復を明示し、途中の細かな作業方法はモデルへ委ねる。必須の状態順序・安全境界・固定検査は維持する。Skillは狭い発火条件の入口を用い、必要なreferencesのみを取得する。単なる説明・誤字修正に新規設計工程を起動しない。

ローカルの使い捨てfixtureに対する実装・検査・原因修正が委任されていることを明示する。初回コードを返して停止せず、候補と証拠が揃うまで進む。実機・権限・認証・予算・USER_STOPは真正な境界として守る。ready_for_reviewは候補でありacceptedではない。

### Fable/high — 統括・調査/設計・独立review

独立取得と結果依存の操作を区別する。agmsgの耐久受領後は別の有用な統括作業を続け、結果到着後にjoinする。writer競合や未確定仕様を並列化で隠さない。公開進捗は実発見・工程・停止原因に基づき表示する。内部推論を表示する要件はない。

要求全体の網羅と範囲維持を両立する。小変更を全面再設計にしない一方、必須の異常時動作・NFR・文書・検証を省略しない。原文の引用と独自要約を区別し、根拠へ戻れる形で設計/レビューを残す。A1は実装者にならず、A2への委任規則を維持する。

## 4. ReadLedgerとcontext epoch

ReadLedgerはsource_digest、range、reader role/session、epoch、取得時点、purposeを保持する。source取得の記録は理解の証明ではない。本文hash・関連scope・同じcontext epochが一致し、必要情報が保持される場合だけ再読省略を検討する。

新session、native compaction、構成/仕様変更、参照先変更、取得失敗では再評価する。新sessionのA3へ作者の読了/推論を移植しない。compaction後はcurrent goals、必須制約、未解決、正確なtask/worktree/session ID、原本参照を外部checkpointから再確認する。nativeが何を保持したか不明なら関連必須本文を再取得する。

原本ログの中間にあるFAIL、例外条項、未充足MUSTを短縮で落とさない。観測値は機械抽出し、要約とは別に署名対象へ持たせる。長文を保存してあるだけでモデルが読んだことにしない。

## 5. APIとnative CLIの責任境界

Messages APIのbeta、thinking表示、tool_choiceなどをClaude Codeの引数として捏造しない。公式CLIが履歴を所有するので、Supervisorは過去historyや内部thinkingを加工しない。既存のexact session再開を使い、構成が変わったら新runと認可済handoffで接続する。

Fableの公開progressを採用CLIが返す場合はその経路を使う。返さない場合はSupervisorの工程イベントをorigin=engineとして表示する。非公開thinkingを解読・転送して補完しない。表示の実現と内部観測の範囲は資格manifestに残す。

Codexは採用版のApp Server schema・model/list・skills/hooksの実効状態を確認する。APIに同名modelやeffortがあることだけで実Codexの資格としない。未知/開発中のsurfaceを本番に無断導入しない。

指定model固定はA1/A2/A3として委任する作業に対する要件である。ベンダー内部の不可視な安全分類器やルーティング補助まで同じモデルで動くと主張しない。委任workerのsilent fallback・low effort overrideは検出・拒否する。

### Fable-5.1のAPI変更をnativeへ誤適用しないための確認表

以下はOPT-S03のMessages API条件を識別するための表であり、API直呼びbackendを新設する指示ではない。Claude Code/公式SDKが管理する履歴はそのruntimeへ任せる。

| 公開仕様の範囲 | このNative-first構成での扱い | 負例 |
|---|---|---|
| Adaptive thinkingが常時有効、disabled/manual指定は非対応 | highの公式有効設定を確認し、SupervisorはAPI thinking設定を追加しない | APIのthinking無効化やmanual予算をCLI設定に混入する |
| forced tool_choiceのany/toolは非対応 | 構造化結果が必要なら採用CLI/SDKが提供する正式surfaceで適合試験を行う | 未対応のforced-tool引数を発明して結果schemaを強制する |
| Assistant prefillは非対応 | TaskPacketは通常の新入力として渡す | assistant prefixを外側で書き足す |
| 過去prefixとthinking blockの結び付き | exact native session再開を使い、公式runtimeの履歴管理を壊さない | 古い履歴を書き換えて以前のthinking blockを再注入する |
| thinking.display等のAPI向け表示機能 | public native出力の有無を実版で確認。ない場合はengine状態を明示して表示する | API betaを未対応CLI flagに転記、内部推論を公開更新として復元する |

これらの適用はMO06/MO07の負例とWP15/26で確認する。公開APIの非互換を、公式CLIが利用不能だという意味へ広げない。

## 6. Skills統合は品質工程を残して行う

元プラグインごとにkeep/rewrite/route/reference-only/disabled-with-replacementの台帳を作成する。採用した入口の名前・scope・role・body・Hook・依存runtime・licenseを記録する。元のSkillとADH入口が同じ用途で競合して自動発火する構成は資格不合格。

独立reviewを単なる自己点検へ落とさない。nativeにない「常駐worker制御」をfrontmatterへ発明せず、agmsgとRunnerで実装する。変更後も必要な設計、TDD、原因分析、レビュー機能が実行できることを試す。Skill metadataは権限ではなく、強制される認可を置き換えない。

## 7. 検証の段階と重複の扱い

| stage | 実行する検査 | 再実行理由 |
|---|---|---|
| development | 変更に関連する検査・必要な負例 | source/仮説が変わった、原因が不明、再現確認 |
| wp-candidate | WPの全指定case/subcaseと必要回帰 | 候補hash・env・suite変更 |
| independent | A4の別領域実行とA3の独立意味review | 独立性の確保。workerの実行では代替不可 |
| integration | 統合snapshotの起動/API/E2E | 複数変更の接続による新候補 |
| release | 同一RCの全必須inventory | 最終提出物に対する完全再確認 |

同stage、同source/env/suiteで根拠のない重複だけを減らす。特定のバグが小さいからという理由で安全ゲートを省略しない。既存のcoverage・negative control・実AI/VM/native・RC条件は維持する。

## 8. 実行状態と変更管理

文書資産はAUTHORED、schema/参照/構造検査はDOCUMENT_QA、native適合はNATIVE_QUALIFIED、行動評価はBEHAVIOR_QUALIFIED、改善効果はEFFECT_EVALUATED、製品はDEVELOPMENT_ACCEPTEDと区別する。今回の配布時点でnative以降は未実施。

モデル最適化はCR-MODEL-001として本v4へ統合済み。A1/A2が旧版＋追補を読み合わせて採否を決め直す作業は不要。必要な実環境bindingのみWP01で確認する。性能が不十分なら同じmodel/effort・同じ要求で指示資産を改良し再評価する。基準緩和や無断モデル変更で「最適化成功」にしない。

具体的な実験・集計・採用条件は[評価規約](../evaluation/EXPERIMENT_PROTOCOL.md)、全MO仕様と対応は[MO台帳](../registers/model_optimization_contracts.json)、本番schemaは[契約](../contracts/model-execution.schema.json)を参照する。

## 文書体系・ガードとモデル最適化の両立

IC13の文書graphとIC14のguardを使用するが、10文書または24GR全文を各turnに追加しない。短い共通契約と役割指示は保ち、TaskPacketに適用MUST・必要なAC/SPEC/TEST・active_guard_ids・短い停止/復旧条件と参照を入れる。既読/取得記録は理解の証拠ではなく、圧縮後の文脈保持を保証しない。

model_guidanceは比較可能だが、安全policy・必要oracle・適用する文書内容はすべてのH00/H10/H01/H11で同一。ガードを無効化した高速実行を最適化成功にしない。[文書/ガード評価規約](../evaluation/DOCUMENT_GUARDRAIL_PROTOCOL.md)を既存モデル評価へ接続する。
