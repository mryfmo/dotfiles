---
name: adh-design-choice
description: "設計案の比較・技術実験・ADRを策定する。決定済み方式の局所実装には使わない。"
---

# 候補の比較と設計具体化

TaskPacketの目的・role・scope・完了条件に該当するときだけ使う。対象外なら他の入口または通常のtask実行へ戻る。このSkill自体は権限を付与しない。

[該当workflow](references/workflow.md)を読み、必要な根拠だけを取得する。全Skill・全資料の一括読込は不要。出力は候補比較、実験結果参照、ADR、仕様差分。全体の受け入れは固定された外部ゲートに従う。
