# モデル別最適化の追跡
状態は全てSPECIFIED_NOT_IMPLEMENTED。指示資産の作成済みと、機械的な実装・native適合・実測効果を混同しない。
| MO | 仕様 | 対応WP | 必須subcase | 根拠 |
|---|---|---|---|---|
| MO01 | 完全な正本とモデル向け指示の分離 | WP00, WP02, WP03, WP04, WP06, WP17, WP20, WP31 | V04-06-M01, V17-04-M01, V31-03-M01 | OPT-S01, OPT-S04 |
| MO02 | Astra向けの狭い発火条件と段階的Skill読込 | WP03, WP04, WP06, WP16, WP26, WP28 | V06-05-M01, V06-06-M01, V26-02-M01 | OPT-S01, OPT-S04, OPT-S05 |
| MO03 | 版付き読了台帳と必要箇所の文脈供給 | WP00, WP04, WP05, WP09, WP17, WP18, WP25, WP28 | V18-06-M01, V25-01-M01, V28-02-M01 | OPT-S01, OPT-S04 |
| MO04 | Astraの許可範囲内の完遂と検証の段階化 | WP05, WP06, WP16, WP20, WP22, WP28 | V16-02-M01, V22-01-M01, V28-04-M01 | OPT-S01, OPT-S06 |
| MO05 | Fableの独立読取・委任・統括作業の並列進行 | WP05, WP10, WP14, WP15, WP17, WP19, WP28 | V05-01-M01, V15-01-M01, V28-01-M01 | OPT-S02, OPT-S06, OPT-S07 |
| MO06 | Fableの公開進捗表示と非公開履歴の分離 | WP04, WP15, WP25, WP26 | V15-03-M01, V25-06-M01, V26-01-M01 | OPT-S02, OPT-S07 |
| MO07 | Fable履歴の所有権・正確な再開・安定prefix | WP06, WP15, WP17, WP22, WP25, WP28, WP30 | V15-02-M01, V15-06-M01, V28-06-M01 | OPT-S03, OPT-S07, OPT-S08 |
| MO08 | Fable上流判断・変更範囲・出典表現の適合 | WP02, WP18, WP19, WP21, WP28 | V19-01-M01, V21-02-M01, V28-02-M02 | OPT-S02 |
| MO09 | role・Skill・subagentを通したmodel/effort固定 | WP01, WP04, WP06, WP15, WP16, WP26, WP30 | V01-01-M01, V06-03-M01, V26-03-M01 | OPT-S03, OPT-S05, OPT-S06, OPT-S07 |
| MO10 | 上流Skillsの重複・承認・役割の一体適合 | WP05, WP06, WP10, WP21, WP24, WP26 | V06-03-M02, V21-06-M01, V24-01-M01 | OPT-S01, OPT-S04, OPT-S05 |
| MO11 | 固定モデルの比較評価と効果・安全性の分離 | WP03, WP06, WP20, WP21, WP26, WP28, WP29, WP31 | V03-06-M01, V28-06-M02, V31-02-M01 | OPT-S01, OPT-S02, OPT-S04 |
| MO12 | model packの版固定・差分更新・切戻し | WP06, WP26, WP30, WP31 | V30-04-M01, V30-05-M01, V31-05-M01 | OPT-S04, OPT-S05, OPT-S06, OPT-S07 |
