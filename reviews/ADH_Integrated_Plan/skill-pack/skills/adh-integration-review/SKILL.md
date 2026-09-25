---
name: adh-integration-review
description: "受入候補をローカル統合し統合検証を調整する。remote公開は含めない。"
---

# ローカル直列統合

TaskPacketの目的・role・scope・完了条件に該当するときだけ使う。対象外なら他の入口または通常のtask実行へ戻る。このSkill自体は権限を付与しない。

[該当workflow](references/workflow.md)を読み、必要な根拠だけを取得する。全Skill・全資料の一括読込は不要。出力は統合順序、新snapshot、統合検証、失効/修正判断。全体の受け入れは固定された外部ゲートに従う。
