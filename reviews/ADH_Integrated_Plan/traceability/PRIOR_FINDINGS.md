# 先行レビュー所見の処置

すべて未実装・未検証。仕様に処置を決めたことと問題を修正したことは別。

| 所見 | 内容 | WP | 親検査 |
|---|---|---|---|
| F01 | Codex共通の品質免除規則 | WP06, WP19, WP21 | V06-03, V19-04, V21-02 |
| F02 | UA source-root/dirty鮮度 | WP06, WP09, WP18 | V06-04, V09-01, V18-04 |
| F03 | Crit自律reviewとUI承認の競合 | WP06, WP21, WP26 | V06-03, V06-06, V21-06, V26-02 |
| F04 | SDD品質機能と常駐workerの適合 | WP05, WP06, WP21 | V06-03, V06-06, V21-01 |
| F05 | installerとpayload固定の差 | WP01, WP06, WP30 | V01-04, V06-01, V30-04 |
| F06 | file一致と実capabilityの差 | WP01, WP06, WP26 | V06-02, V26-02, V26-03 |
| F07 | 外部adapter能力の誤った組合せ | WP01, WP15, WP16, WP26 | V01-02, V15-02, V16-02, V16-03 |
| F08 | 構造化evidenceと実行証拠の混同 | WP04, WP20, WP31 | V04-04, V20-04, V20-05 |
| F09 | Skill本文互換とnative plugin互換の差 | WP06, WP15, WP16, WP26 | V06-02, V26-02 |
| F10 | 上流根拠から受入までの連結 | WP18, WP19, WP28, WP31 | V18-06, V19-05, V31-02 |
| F11 | permgate自身/生成元の小変更を必須reviewから漏らさない | WP06, WP21, WP29 | V15-04, V23-03, V29-01 |
| F12 | ローカルreview receiptと環境変数bypassを独立承認にしない | WP08, WP20, WP21, WP31 | V20-05, V22-04, V31-05 |
| F13 | agent-fanoutの共有writer/full-autoをADH経路に混入させない | WP05, WP06, WP10, WP26 | V06-05, V14-05, V15-04, V24-05 |
| F14 | 権限分類の非有限confidenceと暗黙shadow LLM呼出 | WP06, WP11, WP29 | V06-01, V15-04, V29-01 |
| F15 | 裸.envと別言語/外部helper経由の保護漏れ | WP06, WP13, WP14, WP29 | V14-06, V15-04, V26-04, V29-01 |
| F16 | 旧profile・express E2E・片側生成物のdrift | WP01, WP05, WP06, WP26 | V06-02, V26-01, V26-02 |
| F17 | Semanticaのecho来歴・全HOME graph・保持境界 | WP18, WP25, WP26, WP29 | V18-04, V25-01, V25-02, V26-02 |
| F18 | 品質Hookの二重formatter・特殊形式・config-only CI漏れ | WP03, WP14, WP24, WP30 | V06-03, V06-04, V14-06, V30-02 |
