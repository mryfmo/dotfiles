---
name: adh-failure-diagnosis
description: "観測済みの不具合・検査失敗の原因を調べ修正する。失敗のない一般レビューには使わない。"
---

# 不具合の原因分析と修正

TaskPacketの目的・role・scope・完了条件に該当するときだけ使う。対象外なら他の入口または通常のtask実行へ戻る。このSkill自体は権限を付与しない。

[該当workflow](references/workflow.md)を読み、必要な根拠だけを取得する。全Skill・全資料の一括読込は不要。出力は再現、原因仮説、修正、再検証、残課題。全体の受け入れは固定された外部ゲートに従う。
