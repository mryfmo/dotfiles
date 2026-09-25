# 品質処理の統合仕様 — prek / Oxc / 既存検査

規範はIC17。品質ルールの正本は承認済みproject QualityPlanと固定check inventory。Git Hook、編集Hook、CLI、CI、Verifierは同じ計画を用途別に利用する。[V4-S07][V4-S08][V4-S09][V4-S10][V4-S17]

## 1. 実装と配置

dispatcherの本体はADH src/adh/qualityに一つだけ実装し、dotfilesのagent-qualityとformat-edited-filesはthin consumerとする。prekはmiseで配布する固定binary。Oxcはprojectの既存package managerのdevDependenciesとlockを使う。dotfiles自身のJS/文書品質に必要なNode依存はtools/qualityへ隔離し、全案件へ同版を強制しない。

初期の新規project品質定義は明示`.pre-commit-config.yaml`を採用する。既に承認済みprek.toml等があるprojectは無断置換せず、一意なprofileとして登録・互換試験する。同directoryに競合形式を二重生成しない。未知nested configを自動探索実行せず、明示root/config/binaryを使う。

## 2. 書込みと対象の違い

| stage | source basis | mode | 何を保証するか |
|---|---|---|---|
| edit | owned working tree | checkまたは明示fix | task scope内の迅速な欠陥発見・修正 |
| pre-commit | index treeの一時snapshot | check only | 実コミット対象を検査し元index/working不変 |
| candidate | 凍結candidate | check only | 独立Verifierが固定suiteを実行 |
| integration | 統合後の新snapshot | check only | 単体では分からない接続不具合を検出 |
| release | 最終ReleaseSetとsource | check only | すべての必須条件・証拠・提出物を照合 |

同一snapshot/stage/suite/環境に対する理由なしの反復を抑えるが、独立性・統合後・設定変更後に必要な検査は省略しない。履歴キャッシュのPASSにはsame-input証明と期限が必要。

## 3. 部分stage

ステージ済ファイル名だけをworking treeの内容で検査してはいけない。indexのtreeをprivate領域へmaterializeし、実際にcommitされる内容をcheckする。元indexを書き換えず、一時checkoutへsourceと必要configを固定する。別processのstage変化を開始/終了digestで検出し再検査する。

自動git addは禁止。元の未ステージ変更を一時stashする方式には依存しない。既存Hookとの共存は明示dispatcherを経由し、未信頼hookを無断chainしない。成功・失敗・signal・timeoutのいずれでも元差分が消えないことを実Gitで検査する。

## 4. 言語・形式

JS/TS/JSX/TSXはOxlint。型検査/TS対応が資格済になるまで既存tsc等を維持し、未対応ESLint規則だけ残余laneへ分ける。PythonはRuff＋ADH Pyright strict。既存dotfilesのty/Vulture/unittest等は適用範囲を登録し、重複か欠落かを診断行列で判定する。ShellはShellCheck/shfmt/Batsを保持。

Oxfmtは採用版で実対応が確認できた形式に限る。特にMarkdown/MDXとstandalone/npmの差は実fixtureで確認し、黙ってskipされる配布形態を必須MDの検査に使わない。既存Prettier pluginや設定差は先に比較し、一file一formatterを守る。

`.json`という名のPython modifier、拡張子なしscript、chezmoi `.tmpl`は実言語/生成元を明示分類し、template sourceとrender後を別検査する。vendor/生成コード/署名済証拠/固定goldは整形対象にせず、完全性検査を行う。import順序など意味の変わり得る自動sortはopt-inで回帰を通す。

## 5. 実行・依存・並列

準備段階にのみlockで依存取得する。Hook/check経路の`npx`/`uvx`自動latest downloadは置かない。argv配列・NUL区切り一覧・先頭ハイフン保護・length制限・chunk件数照合を使用する。空対象でformatterを引数なし起動しない。

pre-commitとCIに自動fixを置かないため原則read-only checkを並列実行できるが、可変cache/log/tmp/portはjobごとに分離する。fixとreadが同treeを扱う場合はRunner所有lockで順序化。prekのpriorityやrequire_serialは補助であり、process/VM全体の排他を保証するものではない。

## 6. 合否とガード

exit_code、signal、timeout、対象数、検査数、failed/skipped/unknown、入力と出力digestを独立して収集する。exit0であっても必須対象0/全skip/未対応checker/対象変更をPASSにしない。frontendの条件で禁止操作を隠すだけでなく、executorが権限・対象・policyを再照合する。

CIは保護されたsuite/rule baselineを別の信頼源から読み、candidateの設定変更だけで検査が減ることを防ぐ。ローカル`--no-verify`やSKIPを許可した結果があっても、最終inventoryで必須検証を再実行する。config/lockだけの変更も必須jobがfinal statusを出す。

## 7. 更新と効果

format/fixはソース変更なのでsnapshot/関連graph/receiptを更新する。旧hashの署名を添えたまま出荷しない。固定ファイル集合・同等rule・同じ型条件でQ0旧互換toolchain/Q1新経路を比較する。cold/warmとsetup時間を区別し、速度のためのrule削除は不合格。第三者の倍率は参考であり、本環境の実証値ではない。
