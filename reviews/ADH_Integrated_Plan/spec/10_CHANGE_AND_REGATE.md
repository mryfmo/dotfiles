# CHGと再ゲート・ガード例外の統合契約

版4.0.0。変更統制は最後の工程ではなく、要求登録から運用終了まで適用する。

## 変更分類

| 区分 | 例 | 処理 |
|---|---|---|
| C0 説明/非規範 | 誤字・リンク修正、意味不変の表示 | 意味差分を確認し関連schema/link検査。権限/要件を変えない範囲では委任内 |
| C1 委任内実装 | バグ修正、API保持、テスト追加、承認recipe | task scopeと証拠を更新し影響検査。通常の人待ちは不要 |
| C2 契約/要求 | API、NFR、意味、受入閾値、architecture | CRと対象差分に結び付く必要承認。旧基準を保持して別候補 |
| C3 実効policy/資産 | Skill/Hook/model/version/permission/network | qualificationとregressionを候補環境で再実行。旧runは凍結構成 |
| C4 保護境界/外部作用 | secrets、公開、本番、権限拡大 | 明示したactor/target/payload/期限の承認。モデル自己承認不可 |

分類自体をLLMの自由文だけで確定しない。diffの対象とprotected paths/contract fieldsで構造確認し、意味が不確実ならA3が審査する。CRはrequested/proposed/approved/rejected/applied/verified/rolled_backを記録する。計画の本版への改訂は利用者が要求した文書改訂であり、runtimeの本番操作の承認ではない。

## 影響解析

変更nodeからrefines/specifies/depends_on/governed_by/verifiesの意味に従い、仕様、task、oracle、qualification、receiptの影響集合を求める。graph全体のdigest変化を即全taskの失効理由にしない。taskの凍結normative closure、適用policy、source、suite、環境、実model/assetで判断する。不明な関係は保守的に対象を広げる。

実行中のtargetへ影響する変更は新規admission停止→現在runの停止/照合→適用版の決定→再資格→再dispatch。脆弱な鍵/policy失効等の緊急変更では該当runも失効する。無影響taskを巻き添えに停止しない。既存合格記録はhistoricalとして保持し、current_valid=falseと理由を追記する。

## ガード例外

例外は『ガードなし』ではない。特定task、actor、operation、target、payload、最大回数、期限、補償条件を持つExceptionGrantとして必要なAuthorityが承認し、代替制御を同時に確定する。scopeを変える既定denyは無断で上書きしない。テスト不合格、架空証拠、別candidate、自己レビューの不正を例外承認でPASSへ変えない。

## 正常な修正ルート

通常TEST_FAILEDはrepair、ENV_MISSINGは許可recipe、AUTH_REQUIREDは本人認証待ち、POLICY_DENIEDは対象操作の拒否と安全な代替、GUARD_UNAVAILABLEは該当作用HOLD、EFFECT_UNKNOWNはBLOCKED_EFFECT、USER_STOPは明示再開待ち。拒否された同操作を表記だけ変えて繰り返さない。ガードの誤検知は証拠付き改訂と正負回帰で直す。

## 再ゲート

文書変化はG1–G3、計画/依存はG4、実装/テストはG5–G6、モデル/Hook/環境/policyはG0と関連G5–G6、公開はG7を対象にする。すべての変更でG0から全文作り直す必要はない。最終RCは全必須条件を同一candidateで再確認する。

後続はchange request、impact-set、approval/grant、invalidated evidence、revalidation inventory、rollback plan、actual outcomeを残す。結果を待つ間も独立作業を続ける。
