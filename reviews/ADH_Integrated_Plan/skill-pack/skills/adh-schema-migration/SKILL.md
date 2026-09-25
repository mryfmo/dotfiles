---
name: adh-schema-migration
description: "DB migrationの追加・変更・適用試験を行う。SQLの説明や通常の検索には使わない。"
---

# schema migration

TaskPacketの目的・role・scope・完了条件に該当するときだけ使う。対象外なら他の入口または通常のtask実行へ戻る。このSkill自体は権限を付与しない。

[該当workflow](references/workflow.md)を読み、必要な根拠だけを取得する。全Skill・全資料の一括読込は不要。出力はmigration差分、旧データ保持、適用/復旧試験結果。全体の受け入れは固定された外部ゲートに従う。
