---
name: adh-task-implementation
description: "割当済みタスクの機能を実装・検証する。要件策定や独立レビューには使わない。"
---

# 承認済みタスクの実装

TaskPacketの目的・role・scope・完了条件に該当するときだけ使う。対象外なら他の入口または通常のtask実行へ戻る。このSkill自体は権限を付与しない。

[該当workflow](references/workflow.md)を読み、必要な根拠だけを取得する。全Skill・全資料の一括読込は不要。出力は候補差分、担当検査の結果、未実施、RESULT。全体の受け入れは固定された外部ゲートに従う。
