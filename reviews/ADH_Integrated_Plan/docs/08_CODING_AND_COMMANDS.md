# 8. コーディング規約・品質コマンド・CI

## 開発規約

Pythonはuvのみを使い、Python3.13系列の採用patchをlockする。productionに未実装stub、空pass、常時成功mock、参考実装の縮小契約を登録しない。外部境界は入力validation、型、timeout、cancellation、資源解放を持つ。例外は意味ある分類へ変換し、失敗を握り潰して成功returnしない。

公開関数/moduleのdocstringは目的、入力、出力、失敗、並行性/所有権上の条件を記述する。重複した実装説明ではなく呼出側の契約にする。上流APIを自作の似た名前で呼ばない。ライブラリ依存を増やす場合は目的・license・供給元・保守・固定方法・代替を記録する。

制御対象コードと検証コードは別ownerでレビューする。実装者が自作testを通した結果だけで独立合格としない。テストはobservable behaviorをassertし、内部関数の呼出回数だけを正しさの基準にしない。

## planned command targets

次のq-* targetは **WP03で作成する開発用command契約**。本パッケージに実行scriptは含めていない。未作成targetを今すぐ実行可能と説明しない。WP03はこれら自体の失敗伝播、件数、artifact、env選択をテストする。

| Target | 必須処理 |
|---|---|
| q-format | uv run --locked ruff format --check . |
| q-lint | uv run --locked ruff check . |
| q-types | uv run --locked pyright（strict設定） |
| q-contract | schema/API/型/state/role正負caseとdrift検査 |
| q-unit | authored productionに対するunit＋coverage |
| q-integration | 実Git/SQLite/process/private serviceの統合 |
| q-security | secret/dependency scan＋認可/証拠/injection negative controls |
| q-native | 実公式binary、本人Auth、指定model/effort、assetsの資格試験 |
| q-vm | 実VM/OS/keys/egress/process isolation |
| q-e2e | WP28の6scenario×3回の実AI全工程 |
| q-ops | clean install/backup restore/upgrade rollback/uninstall |
| q-docs | 手引・spec・API・local links・manifestの一致、意味レビュー入力 |
| q-package | 再現package、SBOM、license、全hash、秘密検査 |
| q-release | 上記全必須を固定inventoryで実行・集計。未実施/skipで失敗 |

最初のlock作成は承認済み依存の取得を伴う。その後のCI/受入では`uv sync --locked --all-groups`を使い、`--frozen`や通常syncが違う意味を持つことを理解する。lockを更新してたまたま通すことはしない。commandはargv/working directory/toolchain digestと一緒に固定する。

pytestは0件収集や未実行を合格としない。pytest exit0でも全skip等は別集計で拒否する。coverageの行/分岐、case inventoryとの一致、xfailを含めて判定する。

## CI権限

forkや未信頼PRでAuth/署名鍵を渡さない。静的/非認証testと資格済runner上のnative/VM試験を分ける。Actions等の実行定義はcommit SHAと最小permissions、秘密を必要jobへだけ渡す。CIのpending/skippedをsuccessとしてリリース集計しない。

全suiteを毎回無条件に起動する必要はないが、実行したscopeを正確に示す。最終RCだけは全必須を同一候補で再実行する。役割/clock/snapshot/signer/基準の変更は常に重要境界として回帰対象にする。

## 実装へ組み込む不変条件

IC04の通知はcommit後、IC05の外部開始はintent commit後。IC08の停止は要求だけでなく静止まで待ち、timeoutとexit0を同時に記録する。observer例外の隔離と認可/永続化のfail-closedを混同しない。IC10の仕様・型・生成API・診断を同じ変更で更新し、IC11の実配布entryで退行を検出する。

安全重要比較のmutationは隔離copyへ行い元RCを汚さない。元RCと対照のhashを保存する。試験のport/path/processを所有者ごとに割り当て、単独でしか通らない試験をそのまま許容しない。


## model packの品質対象

prompt/Skill frontmatter/参照リンク/カタログ重複/schema/profile組合せ/ハッシュと読了epochを静的検査対象に含める。nativeの公開観測による振る舞い、stage別再検証、モデル固定、必要資料の保持を別試験にする。新規checkerの成功だけで実nativeの合格にしない。

## 文書・ガードの品質ゲート
q-docsにはJSON Schema/typed edge/版/要求意味保存/生成view再現/参照元の独立レビューを追加。q-securityとq-native/q-vmには操作別GRのnormal/deny/fault/recoverを追加する。policyと実行の境界は別テストで正規の直接入口も通し、wrapperだけの拒否を保証にしない。guard evaluatorの高リスク処理前失敗は停止、純subscriber例外は隔離と記録。新しい守るべき不変条件の試験を先に定義する。


## V4の共通品質入口

品質検査の規範はtrusted QualityPlan/inventoryで一つ、実行入口は編集・pre-commit・CI・Verifierで段階を分ける。`q-*`は本ハーネスが実装するコマンド契約で、上流CLIの既存コマンドではない。ADHは既存のRuff/Pyright strict/pytest、dotfilesはBats/unittest/Shell/asset/Crit等の適用検査を保持する。Oxc追加で削らない。

JS/TSはOxlint、MD等は形式資格を満たすOxfmt、残余ESLint/Prettier必要性は明示profileで判断。一file一formatter。chezmoi modifierの実言語、template原文/展開結果、署名済artifactの無変更を分類する。自動git addは禁止。index内容を別の一時作業領域でcheckし、元working treeをstashやfixで変更しない。
