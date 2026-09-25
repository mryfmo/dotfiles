---
name: adh-environment-repair
description: "許可された開発・検証環境の不足を構築・復旧する。権限外の本番運用には使わない。"
---

# 環境不足の解消

TaskPacketの目的・role・scope・完了条件に該当するときだけ使う。対象外なら他の入口または通常のtask実行へ戻る。このSkill自体は権限を付与しない。

[該当workflow](references/workflow.md)を読み、必要な根拠だけを取得する。全Skill・全資料の一括読込は不要。出力は構築recipe、health、test、cleanup、外部待ち。全体の受け入れは固定された外部ゲートに従う。
