# 1. 目的・正本・変更禁止事項

## 今回の納品の位置付け

これは後続の **Claude Code Fable-5.1 high + Codex gpt-6 Astra xhigh + agmsg** に渡す実装・検証の実行計画である。製品の中途実装、参考kernel、デモソースは含めない。全WPの実装状態はPLANNED、全検証項目はNOT_RUNで開始する。今回の計画整合性検査と、後続の製品検証を混同しない。

本v4の統合設計が唯一の設計baselineである。Native実行・開発方法論とDSH由来のIC01–IC18を同じservice/状態/受入経路へ統合済み。35MUST、32WP、192論理項目を維持し、80必須subcaseを各担当へ割当済み。後続は追補の採否/割当をやり直さず実装へ進む。過去62試験は履歴で、この実装の合格ではない。

## 完成させる製品

専用repository `autonomous-dev-harness` の公式Claude/Codex + native Plugins/Skills/Rulesを実行主体とし、独立Supervisor、Runner、Verifier/Reviewer、証拠・成果物管理を組み合わせる。要求調査、現状分析、比較、技術実験、仕様/アーキテクチャ/機能策定、実装計画、実装、独立検証、修正、復旧、統合、受入を一貫して扱う。

最終状態の正本はSupervisorの管理DB。認証は本人の未改変公式製品。agmsgは必須の協働輸送だが認証・合否の正本ではない。UA、CompactionDB、SDD台帳は参照・投影であり承認済み仕様より優先しない。

## 入力優先順位と変更手続

| 優先 | 入力 | 扱い |
|---|---|---|
| 1 | 利用者の明示要求・承認・委任・安全上の制約 | 実装都合で変更しない |
| 2 | 本v4のspec/・contracts/requirements.json・registers/・作業/検証契約 | 一つのbaseline。内部矛盾は勝手に優先を選ばずCRとして解決 |
| 3 | 対象版の実公式CLI/API/OS仕様 | 外部の実挙動。相違を捏造で埋めず、資格確認とCRで適合 |
| 4 | 役割別Rules・Plugins・Skills | 本v4で統合した優先・権限の範囲で動作。MUSTを緩和しない |
| 5 | 旧設計・旧計画・旧追補・過去probe | 履歴/出典のみ。並立した実行正本にはしない |

これはネイティブ製品内部の優先順位を変更できるという主張ではない。実効HOME/設定/skill scopeを調整し、期待する優先が実動作に現れることをWP06/26で検証する。

技術的な誤記や外部API差は、黙って迂回しない。CRに根拠、影響R/WP/case、提案差分、検証、必要権限を残す。委任内の実装具体化はA1が記録しA3が独立確認。仕様緩和、architecture変更、モデル変更、追加課金、公開操作は操作者判断を必要とする。依存しない作業は止めない。

## 旧成果物の扱い

| 旧項目 | 後続での取扱い |
|---|---|
| 旧`DESIGN_JA.md` | 本v4へ統合済み。旧版の読み合わせを実行前提にしない |
| 旧API13操作 | 保存する基礎契約。本計画で不足操作を追加、WP04で完全schemaへ確定 |
| `reference-kernel.sql` / `reference-receipt.schema.json` | 本番採用不可。過去の不変条件を試験要求へ移す |
| `src/adh/kernel.py`等の旧probe | 本番srcへコピー不可。再利用するなら機能単位の根拠・適合・全検証が必要 |
| 旧62件のPASS | historicalのみ。今回の進捗・coverage・受入に加算しない |
| 過去レビューの再現11件 | 修正確認用の反例として再実装し、今回RCで実行 |

## 固定する範囲

Python3.13系列、uv lock、型付きdomain、SQLite local WAL単一control host、JSON Schema、Ed25519、管理API HTTP/UDS、VM間の認証済channelを維持。管理・本人native実行・独立検証をLinux VMの異なる信頼領域へ置く。Temporal、別DB、汎用MCP、独自LLM認証/ルータ、DSH最終制御は追加しない。

公開SaaS、資格情報の他利用者への仲介、無制限の本番操作、無承認remote push/merge/publish/deployは範囲外。local branch作成・local統合は本計画の開発作業に含む。新たな機能/プラットフォームを追加する場合は別CRであり、必要機能を減らす理由にしない。

## 文書とガードの固定範囲
本4.0のIC13/14、DG01–10、GR01–24は統合済み必須仕様。R01–35を維持し、10分類を別のアーキテクチャー階層や新プラットフォームへ拡張しない。利用者の要求と適用安全policyの矛盾は範囲を分けて記録する。規則の強さをL番号で決めない。


## V4の実装対象

dotfilesの限定改修とADH本体を同じReleaseSetで納品する。旧SI/DIは本版WPへ移管済みで、別実装計画として並走しない。元35要求・192親・196子の条件は保持し、V4の48子を内包する。実際の対象pathは各WPのrepository_targetsをdispatch時にscopeへ展開する。
