# 品質操作

採用projectのQualityPlanを解決し、対象・rule・toolchain・configが正本に一致するか確認する。check中に依存を取得しない。空対象でformatterを起動しない。

edit-fixは所有writerに限定。pre-commitはindex treeの一時copy、candidate/CIは凍結snapshotをcheck-onlyにする。自動git add、未信頼nested config、同file二重formatterを使わない。Python/Shell/型検査はOxc追加を理由に削除しない。

exit、timeout、signal、対象数、failed/skipped/unknown、実ログを保存する。PASSは候補情報で最終受け入れではない。失敗は原因を直して再検証する。変更後は古いsource/graph/receiptを流用しない。詳細は[品質仕様](../../../../spec/13_QUALITY_AND_TOOLCHAIN.md)。
