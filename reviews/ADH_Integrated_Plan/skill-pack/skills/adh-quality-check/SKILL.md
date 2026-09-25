---
name: adh-quality-check
description: 担当変更のlint・format・型検査を行う。製品の合格認定や未知repoのHook実行には使わない。
---

# adh-quality-check

TaskPacketが参照する信頼済quality profileと担当snapshotを確認する。editの明示fixと、index/candidateのcheck-onlyを区別し、必須checkerを固定環境で実行する。

必要な詳細は[workflow](references/workflow.md)を参照する。無関係な全graph再構築や外部LLM起動、モデル/権限/検査基準の変更は行わない。未実装入口を実行できたと報告しない。
