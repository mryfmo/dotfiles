# V4役割別Skills

旧8入口を維持し、adh-knowledge-contextとadh-quality-checkを統合した10入口。全入口を毎turn展開しない。共通の規範・guardはTaskPacketの適用部分を渡し、実強制はSupervisor/Runner/OS/Verifierが担う。

- [adh-requirements](skills/adh-requirements/SKILL.md): 未確定の要求・制約・矛盾を整理する。承認済みタスクの実装には使わない。
- [adh-design-choice](skills/adh-design-choice/SKILL.md): 設計案の比較・技術実験・ADRを策定する。決定済み方式の局所実装には使わない。
- [adh-task-implementation](skills/adh-task-implementation/SKILL.md): 割当済みタスクの機能を実装・検証する。要件策定や独立レビューには使わない。
- [adh-schema-migration](skills/adh-schema-migration/SKILL.md): DB migrationの追加・変更・適用試験を行う。SQLの説明や通常の検索には使わない。
- [adh-failure-diagnosis](skills/adh-failure-diagnosis/SKILL.md): 観測済みの不具合・検査失敗の原因を調べ修正する。失敗のない一般レビューには使わない。
- [adh-environment-repair](skills/adh-environment-repair/SKILL.md): 許可された開発・検証環境の不足を構築・復旧する。権限外の本番運用には使わない。
- [adh-independent-review](skills/adh-independent-review/SKILL.md): 別担当の凍結candidateを仕様・品質の両面でレビューする。実装者の自己承認には使わない。
- [adh-integration-review](skills/adh-integration-review/SKILL.md): 受入候補をローカル統合し統合検証を調整する。remote公開は含めない。
- [adh-knowledge-context](skills/adh-knowledge-context/SKILL.md): 要求・設計・検証の出典や変更影響を調べる。単純な整形や用語説明だけでは使わない。
- [adh-quality-check](skills/adh-quality-check/SKILL.md): 担当変更のlint・format・型検査を行う。製品の合格認定や未知repoのHook実行には使わない。

上流Plugin/Skillとの対応はregisters/component_catalog.jsonとspec/11_DISTRIBUTION_AND_COMPOSITION.md。入口の作成と、公式runtimeへの導入/発火/比較性能の成功は別である。上流機能を失わず、一般query名の衝突・二重発火・子model上書きを検査する。
