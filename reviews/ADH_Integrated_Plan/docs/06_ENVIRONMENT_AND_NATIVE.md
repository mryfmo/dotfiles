# 6. 環境準備・公式runtime・モデル資格

## 検証環境の区分

| 区分 | 意味 | 実行責任と対応 |
|---|---|---|
| E0 | 現在のsandbox内で実行可能 | A2/A4が直ちに実行。読解/schema/Git/SQLite/recorded protocol等 |
| E1 | sandbox内で依存や私設serviceを構築すれば可能 | A2が承認recipeを用意して構築し、A4が再現。『環境なし』で終わらない |
| E2 | 公式本人Auth/課金・利用枠/指定modelが必要 | Hが公式認証、A1がprofile確認、A2/A4が実行。mockで代用不可 |
| E3 | Linux VM、OS管理、仮想化/ネット設定権限が必要 | Hの委任下でRunner環境を構築し実試験。container/local testは代替証拠にならない |
| E4 | 実機/社内外の特定service/公開権限が必要 | その項目だけ保留。scope外実機を勝手に接続しない |

全必須caseについて環境区分と構築手順を台帳に保持する。E0/E1の残作業をE2/E3が未準備という理由で停止しない。E2/E3を実行しないまま完成と報告もしない。

## 固定するモデル

| 用途 | 要求model ID | effort |
|---|---|---|
| A1、調査/設計/計画、独立A3 | `claude-fable-5-1` | `high` |
| A2実装/デバッグ/検証コード作成 | `gpt-6-astra` | `xhigh` |

このmodel IDとeffortは利用者指定と旧計画から継承する要求値である。本v4の文書統合時に本人資格や最新公開状況を実測したわけではない。Codexでは`model/list`を全page取得し、該当modelとsupportedReasoningEffortsを確認する。APIでxhighが存在することだけをCodexの実効設定の証拠にしない。Claudeはinit/runtime metadataと設定、実smokeの結果を照合し、modelの自己申告には頼らない。

nativeに実効effortの観測方法がない場合、要求flagと実効設定のどこまで確認できたかを分ける。観測不能をconfirmedとしない。要求と異なるfallbackは許可しない。

## 基本コマンドの位置付け

以下は公式CLIの資格確認に使う例。使用前に実binaryの`--help`と対応版を確認する。Auth bytesを出力しない。

```sh
claude --version
codex --version
claude --help
codex app-server --help
codex app-server generate-json-schema --out .orchestration/qualification/codex-schema
```

対話の起動設定例は `claude --model claude-fable-5-1 --effort high`、Codexは `codex --model gpt-6-astra -c 'model_reasoning_effort="xhigh"'`。配布するrole profileの正本は一箇所に置き、launcherごとに異なる値をhardcodeしない。後者の起動例はApp Server messageの代わりではなく、開発bootstrapの対話worker用である。

製品Claude adapterは資格済print/stream-jsonとexact session resume。Codexはstdio App Serverでinitialize応答を受けてからinitialized、threadとturnを進める。記載のAPI名は公式schemaで再確認する。WebSocketや未認証listenerを追加しない。

## plugin管理の注意

Codex App Serverのplugin/list/read/installがunderDevelopmentならproduction pathへ依存させない。公式CLIのplugin管理、実ファイル、許可されたskills/hooks discovery、実smokeで適合を確認する。Hook発火は対話と非対話で異なる可能性があるため、両方を一律とみなさず採用モードで検証する。

`--disable-slash-commands`等で必須Skillを無効化した状態を正常なハーネスとしない。全権限bypassで承認待ちを解消しない。承認済scope内を継続可能にするpolicyと、reserved decisionを待つ経路を分ける。

## 実環境bindingと未決事項の違い

repository絶対path、本人Auth状態、利用可能VM host/CPU、native patch version、有限budget値は開始環境から取得する。これらは設計をworker任せにする空欄ではなく、取得者・方法・確認条件・不足時の状態をWP01で定めた外部bindingである。

CLI patchは元dotfiles pinを候補にするが、その古い版で指定model/Hookが未対応なら未改変公式版の候補を隔離環境で検証しlockする。silent updateも、動かない旧版への固執も避ける。対象版差分は記録し、全qualificationを通す。

Linux guestの対応CPU/platformは資格済manifestで固定する。未検証architectureをサポート済と表示しない。ホストがmacOSでVM作成不能なら、資格済Linux VMへの接続経路を明示的に用意する。host名/権限を推測して外部変更をしない。


### 実効effortの確認範囲

ここで確認するeffortは、採用版の公式runtimeが受理した有効設定である。起動引数だけでなく、configuration precedence、catalog、runtimeの設定応答/metadata、smokeの非エラーを組み合わせて確認する。提供元が非公開の内部計算量まで観測したと宣言しない。

runtimeが実effortを直接返さない場合は、`configuration_confirmed`と`backend_compute_not_exposed`を分ける。認定対象は前者。別model/effortが選択された可能性を解消できないときはUNKNOWNとして資格を与えない。モデル自身へ名前を質問した返答を観測値に使わない。

## 一体化した資格と領域

同じnative実行をIC01資格・IC02実行binding・IC03実効構成・IC05 intent・IC06継続許可に束ねる。資料で存在するとされた能力と、実binary/構成/アカウントで観測できた能力を分ける。必要な内部Hook観測が未提供ならUNKNOWNとし、外側のprobeで内部毎toolの制御を保証したと表示しない。

writer側read/write/shellが同じExecutionBindingであることと、Verifierが別scope/uidにあることを両方試験する。検証をwriterと同じ領域に寄せることは統合ではない。原本source digestで両者を結ぶ。


## model/effortのSkill内上書きとAPI境界

Skill frontmatterとsubagent、plugin内部launch、fallback chainまで検査する。指定model/effortを外れるoverrideは拒否する。profile宣言はADH内部データでnative設定へ直接コピーしない。Claude Messages APIのbeta/thinking/tool_choiceをCLIへ勝手に渡さない。履歴は公式CLIに保持させる。公開進捗が得られない経路はengine statusと区別して表示する。

現在の資格確認は[モデルsource索引](../sources/MODEL_SOURCES.md)を起点に、採用binary/schema/設定の実挙動を確認する。内部計算量や非公開provider補助モデルを観測したとは主張しない。

## native guard qualification
公式binaryの採用版についてevent×handler type×対話/非対話/app-server×許可/拒否/失敗/timeout/不正出力を試験する。Hook非0終了やmissing executableが自動的に操作を拒否するという仮定を置かない。sandbox/OS/networkの別境界を実測する。未観測の内部操作を完全仲介済と表現しない。安全性が担保できない高リスク経路は権限を渡さず専用Runnerへ分離する。

文書のモデル要求値は変更しない。実環境で利用可能かは従来通り本人資格で確認し、後続が確認できない設定を発明しない。


## V4環境と配布

dotfilesの既存global PythonとADH coreのPython3.13を混同しない。Semanticaは専用uv環境と最小extrasで実install資格を得る。初期は外部model/embedding/graph DB/MCPなし。prekは固定配布、Oxcはprojectの既存package lockを使用する。正確な版はWP01/06で実取得・資格確認し記録する。最新版番号やwheel存在を推測しない。

品質は準備済み環境でnetworkなし再実行可能にし、Hook実行中のnpx/uvx自動取得を置かない。Fable/Astraの子session/Skill/Hookまで指定を確認し、E2Eをexpressへ落とさない。実行境界はwriterとVerifierを分離し、same-sourceとsame-identityを混同しない。
