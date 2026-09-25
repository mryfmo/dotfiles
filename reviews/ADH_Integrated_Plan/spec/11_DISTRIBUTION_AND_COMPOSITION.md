# 配布・設定・OSS・Pluginsの統合仕様

規範はIC15。詳細資産一覧はregisters/component_catalog.json。対象は採用ハーネスclosureであり、端末の全アプリを強制移行する指示ではない。[V4-S01][V4-S02][V4-S03]

## 1. 編集正本の一意性

本番のモデルと拡張profileはdotfilesの`home/dot_agents/agent-config.yaml`のADH専用profileへ一度記載し、既存generatorがnative設定とlauncherへ展開する。A1/A3はclaude-fable-5-1/high、A2はgpt-6-astra/xhighを要求制約として照合する。旧express/standard/deep等は利用者の他用途として維持できるが、ADH開始/E2E/childで選択しない。

本ZIPのprofiles/model_profiles.jsonは要求の検査viewと役割promptの対応表であり、独立したruntime編集元ではない。要求→source declaration→生成物→native解決結果→実probeの順に照合する。相違したら自動で片方へ上書きせず新runを保留し、正本変更または生成修復を記録する。workerはsystem promptやnative履歴を独自置換しない。

## 2. 配布単位

ReleaseSetはdotfiles source候補、ADH source候補、要求/仕様、asset closure、quality/knowledge toolchain、選択platformをdigestで結ぶ。コード変更が片方だけでも他方の使用版を含める。両repoを同時commitする仕組みはないので、stage済の互換pairを検査してactive pointerを切り替え、旧pairを保管する。

更新順は取得候補→hash/license/依存closure→隔離install→schema/contract/原本/回帰→実native資格→組合せsmoke→承認範囲確認→新run用active化。既存runは元manifestと実行資産を使い続けるか安全停止する。既存cacheを上書きした後に『旧版継続』と表示しない。

node/uv等はtoolchainごとに固定する。ADH coreはPython3.13/uv、Semanticaは独立lockを持つ3.13環境を第一対象として実installで資格確認する。不適合なら勝手にcore Pythonを変えず、変更影響をCRにする。dotfiles global PythonをADHの必須版に一括変更しない。

## 3. 資産適合表

| 資産 | 維持する能力 | 是正/接続 |
|---|---|---|
| Superpowers | 要求整理、比較、設計、TDD、review | 一つのIPLAN/taskへ接続。汎用全発火・自己schedulerを置かない |
| Ponytail | 再利用・小さな正しい差分 | NFR・エラー動作・既存契約を削らない |
| Crit | 指摘管理・設計/品質レビュー | A3独立reviewと人のreserved承認を分離。ローカルreceiptだけでacceptしない |
| UA | 実code構造 | source_root/artifact_root分離、dirty/untracked含むfingerprint |
| CompactionDB | 記録・記憶・再開参照 | 管理stateから完了を投影。rsync失敗をmanifest成功にしない |
| agmsg | 常駐workerとTASK/RESULT通知 | messageは輸送、同repo共通store、跨VM bridge、E2Eはadh profile |
| permgate | native許可リクエスト適合 | 未知/NaN/Inf入力、UTF-8、環境由来の作用を検査。分類器は助言のみ |
| Semantica | 来歴検索/影響候補 | 最小SDK、project限定、no implicit LLM/MCP。上流echo hookは除外し代替契約を実装 |
| prek/Oxc | 品質実行・lint/format | project opt-in、check/fix分離、既存言語検査の維持 |
| Herdr/terminal/status | 選択UIと運用補助 | core authorityなし。未知自動Skillの混入を資格検査 |
| AutoSkill | 改善候補 | 候補/評価/承認/昇格の順。active rulesを自己更新しない |

## 4. PluginとSkillの同等性

shared assetsを全HOMEへ単純コピーする方式ではない。10入口のどれが上流のどの動作を受け持つかをmappingし、入口をまとめても必須の仕様review/品質review/停止/出典確認を残す。起動時にはselected source、版、優先順位、enabled/trusted/probedを区別する。上流の全Skillとwrapperを両方無条件に発火させない。

付属HooksやAgentsにmodel/effortが書かれていれば実効設定へ反映され得るためclosure全体を監査。必須資産の欠損はその機能を必要とするrunの資格失効。非選択の既存ユーザーassetは削除しない。必須のbusiness effect probeが後期WP所有の場合、前期の配置検査を製品合格とはせずcomponent statusのみ記録する。

## 5. 既存ハーネスの具体修正

permgateのpolicy/実装/生成元を常時review対象に追加し、role/commit/diffに結び付けた独立チェックを行う。CRIT_REVIEW=off等のlocal回避があっても最終検証で素通りさせない。裸の`.env`と子processのcredential経路を検査する。git diff等の許可は環境や外部helperによる作用を含むため、実行worldと読み取り能力を別確認する。

format-edited-filesは浮動uvx/npxから認可済み固定quality経路へ変更。Python/Markdownだけをsuffixで機械分類せず、chezmoi modifier/shebang/templateとrender後を扱う。project_doc_fallbackでA1用命令がA2へ重複注入される場合はrole解決を修正する。共通手引のuv運用は維持し、旧pre-commit例の未固定revや全test毎commitをprofileに合わせる。

## 6. 正規運用と非対象

init/update/doctor/upgrade/removeは既存導線に統合する。global hooksPathや全chezmoi applyで他projectへ無断適用しない。インストールした資産だけをreverse manifestで戻す。Optionalなtode/browser/paneを選択して実装した場合はfresh sessionとrestoreを試験する。MCP、Hermes全runtime、未知のAgent framework、独自認証routerは追加しない。

観測していない最新番号や配布hashは創作せず、WP01/06で試験した値をlockへ記録する。これは資格確認の作業であり、後続に基本構成の再比較を求めるものではない。
