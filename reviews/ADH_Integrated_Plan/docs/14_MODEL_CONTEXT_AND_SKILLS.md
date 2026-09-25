# 14. 実行時に読む情報とSkillsの選択

## 初回と継続を分ける

A1は初回にSTART_HERE、要求、アーキテクチャー、全IC/MOの責任、WBS依存、完了条件を把握する。各WPの詳細は担当をdispatchする前に確認する。A2はTaskPacketと当該WP、入出力の相手契約、該当要求/検査を読む。A3は作者とは独立にレビュー対象の全scopeを確認する。A4は固定suiteとtier・oracleを読む。

継続taskではReadLedgerと現在のcontext epochを確認し、変わった・未読・保持不明の関連情報だけを再取得する。全計画と通読版を同時に読み、同じ本文を二重注入しない。短いTaskPacketから正本へ辿れなければ当該作業を開始しない。

## TaskPacketの必須本文

目的、直接対応する要求と例外/NFR、入力契約、禁止範囲、現在のtask状態、候補の完了条件、stage別検証ID、許可済み環境操作、真正な停止条件を本文に置く。巨大なログ、過去議論、参考資料だけを参照へ回す。各参照はpath/source ID、digest、範囲、取得方法、必要理由、必須/補助を持つ。

初回のA1がまだSupervisorを作っている段階でも、この情報は既存agmsgのtask_file/sidecarで作成できる。PromptCompiler完成をbootstrapの前提にしない。

## Skill選択

[8入口](../registers/skill_routes.json)から、roleとtaskの種類に合う入口だけを選ぶ。必要なSkillがない場合、存在しないコマンドを呼ばない。通常のtask実行で処理できるなら共通/role契約に従う。必須の専門機能が必要なら資格済みassetを取得するまで該当判断を保留する。

上流Skillの名前と説明、ADH入口、native namespace、有効HookはWP06の台帳で一意に対応させる。Skillを使わない負例も試験する。Skillの説明が短いことと、その機能が実行できることは別に確認する。

## 既存資料と評価controlの分離

通常実行の入力はprompts/とprofiles/model_profiles.json。evaluation/control_promptsは比較試験専用でありcatalogへ配置しない。旧モデル向け指示や全面再読の対照条件が、本番promptへ混ざらないことを検査する。

詳細仕様は[モデル最適化](../spec/06_MODEL_OPTIMIZATION.md)。最適化は仕様削減ではなく、同じ要求のための情報配置と実行補助の改善である。

## V3.1文書投影との整合
TaskPacketの要求・AC/SPEC/TESTとactiveGRは必須。出典や長い根拠は必要時参照とし、10文書・24GR全文を毎回展開しない。通常編集に再設計Skillを誤発火させず、危険操作の許可をSkill選択に依存させない。実効role/model/effortは既存MOのまま。


## V4の情報選択

既存8Skillに2入口を追加したが、必須文脈や24GRを全量注入しない。正本closureから必須条件、SemanticaからACL範囲の補足根拠を得る。余分な長文を減らしてもsource、失敗件数、未解決MUSTを保持する。ReadLedgerはhash/epoch/roleで再評価する。

同じroleを維持した10Skillの選択・非選択・native effectを確認し、上流全Skillとの二重発火を排除する。profile JSONは要求view、runtimeはdotfilesの生成元を使用する。
