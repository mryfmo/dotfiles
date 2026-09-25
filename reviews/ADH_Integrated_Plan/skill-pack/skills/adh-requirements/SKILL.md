---
name: adh-requirements
description: "未確定の要求・制約・矛盾を整理する。承認済みタスクの実装には使わない。"
---

# 未確定要求の調査

TaskPacketの目的・role・scope・完了条件に該当するときだけ使う。対象外なら他の入口または通常のtask実行へ戻る。このSkill自体は権限を付与しない。

[該当workflow](references/workflow.md)を読み、必要な根拠だけを取得する。全Skill・全資料の一括読込は不要。出力は要求台帳、重要な矛盾、出典、未確定判断。全体の受け入れは固定された外部ゲートに従う。
