---
name: adh-independent-review
description: "別担当の凍結candidateを仕様・品質の両面でレビューする。実装者の自己承認には使わない。"
---

# 独立レビュー

TaskPacketの目的・role・scope・完了条件に該当するときだけ使う。対象外なら他の入口または通常のtask実行へ戻る。このSkill自体は権限を付与しない。

[該当workflow](references/workflow.md)を読み、必要な根拠だけを取得する。全Skill・全資料の一括読込は不要。出力は要件別確認、finding、修正確認、ReviewObservation。全体の受け入れは固定された外部ゲートに従う。
