# 出典と旧版の位置付け

本版は2026-09-13に提供済み設計・計画・追補を統合した文書baseline v3.0.0である。新しい上流checkout、本人認証、製品実行は実施していない。モデル名は利用者の要求値を継承し、稼働確認済みとはしない。

[input_provenance.json](input_provenance.json)は旧資料の同一性と非実行正本化を示す。[dsh_sources.json](dsh_sources.json)は統合契約の先行実装根拠、[prior_source_index.json](prior_source_index.json)は旧計画に記録された公式仕様等の参照先である。外部資料は対象版で確認し、計画と違う場合はCRで適合する。

[api_v1_snapshot.json](api_v1_snapshot.json)は旧13操作の保存比較用で、本番APIの正本ではない。本v3の27操作inventoryと契約規定を実装し、生成schemaをWP04で凍結する。旧62試験結果、旧本番風probeコードは本版へ取り込まない。

## DeepSeekの具体的な出典

- **DSH-S01** 責任分離・イベント・Profiles/Bundles — [docs/architecture.md](https://github.com/deepseek-ai/deepseek-harness/blob/c291e7961a515f6d7af9304e7fd1d257929aef26/docs/architecture.md)
- **DSH-S02** subagent能力・継続・所有権契約 — [packages/subagent/subagent/README.md](https://github.com/deepseek-ai/deepseek-harness/blob/c291e7961a515f6d7af9304e7fd1d257929aef26/packages/subagent/subagent/README.md)
- **DSH-S03** 失敗・callback・子process停止の防御規則 — [docs/defensive-patterns.md](https://github.com/deepseek-ai/deepseek-harness/blob/c291e7961a515f6d7af9304e7fd1d257929aef26/docs/defensive-patterns.md)
- **DSH-S04** 実エントリ・実世界の検証・記録再生 — [docs/testing.md](https://github.com/deepseek-ai/deepseek-harness/blob/c291e7961a515f6d7af9304e7fd1d257929aef26/docs/testing.md)
- **DSH-S05** 原本を残すtool-result圧縮 — [packages/compaction/compaction-tool-result-pruner/README.md](https://github.com/deepseek-ai/deepseek-harness/blob/c291e7961a515f6d7af9304e7fd1d257929aef26/packages/compaction/compaction-tool-result-pruner/README.md)
- **DSH-S06** dispatch前durability checkpoint実装 — [packages/session/session-checkpoint-policy/src/index.ts](https://github.com/deepseek-ai/deepseek-harness/blob/c291e7961a515f6d7af9304e7fd1d257929aef26/packages/session/session-checkpoint-policy/src/index.ts)
- **DSH-S07** 責任を持つ拡張・不変条件・文書の規則 — [packages/AGENTS.md](https://github.com/deepseek-ai/deepseek-harness/blob/c291e7961a515f6d7af9304e7fd1d257929aef26/packages/AGENTS.md)
- **DSH-S08** 投影・stateVersion・asOfSeq — [packages/session/session-projection/README.md](https://github.com/deepseek-ai/deepseek-harness/blob/c291e7961a515f6d7af9304e7fd1d257929aef26/packages/session/session-projection/README.md)
- **DSH-S09** Goal状態とprocess-local activation — [packages/goal/goal/README.md](https://github.com/deepseek-ai/deepseek-harness/blob/c291e7961a515f6d7af9304e7fd1d257929aef26/packages/goal/goal/README.md)
- **DSH-S10** 同一sessionでの継続driver — [packages/goal/goal-round-driver/README.md](https://github.com/deepseek-ai/deepseek-harness/blob/c291e7961a515f6d7af9304e7fd1d257929aef26/packages/goal/goal-round-driver/README.md)
- **DSH-S11** 新規child反復のRalph仕様 — [packages/workflow/tool-ralph/README.md](https://github.com/deepseek-ai/deepseek-harness/blob/c291e7961a515f6d7af9304e7fd1d257929aef26/packages/workflow/tool-ralph/README.md)
- **DSH-S12** workflow engine契約と隔離限界 — [packages/workflow/workflow-worker-thread/README.md](https://github.com/deepseek-ai/deepseek-harness/blob/c291e7961a515f6d7af9304e7fd1d257929aef26/packages/workflow/workflow-worker-thread/README.md)
- **DSH-S13** TeamsのCAS・DAG・durable mailboxと限界 — [packages/experimental/agent-team/README.md](https://github.com/deepseek-ai/deepseek-harness/blob/c291e7961a515f6d7af9304e7fd1d257929aef26/packages/experimental/agent-team/README.md)
- **DSH-S14** sandboxのfile-effect scopeとfull/partial — [docs/subsystems/sandbox.md](https://github.com/deepseek-ai/deepseek-harness/blob/c291e7961a515f6d7af9304e7fd1d257929aef26/docs/subsystems/sandbox.md)
- **DSH-S15** 上流調査・計画modeの承認と限界 — [packages/plan/plan-mode/README.md](https://github.com/deepseek-ai/deepseek-harness/blob/c291e7961a515f6d7af9304e7fd1d257929aef26/packages/plan/plan-mode/README.md)
- **DSH-S16** 意味的・設計・契約レビューSkill — [.agents/skills/dsh-code-review/SKILL.md](https://github.com/deepseek-ai/deepseek-harness/blob/c291e7961a515f6d7af9304e7fd1d257929aef26/.agents/skills/dsh-code-review/SKILL.md)
- **DSH-S17** 現在の公式Codex provider契約 — [packages/subagent/subagent-codex/src/index.ts](https://github.com/deepseek-ai/deepseek-harness/blob/c291e7961a515f6d7af9304e7fd1d257929aef26/packages/subagent/subagent-codex/src/index.ts)
- **DSH-S18** 現在の公式Claude Code provider契約 — [packages/subagent/subagent-claude-code/README.md](https://github.com/deepseek-ai/deepseek-harness/blob/c291e7961a515f6d7af9304e7fd1d257929aef26/packages/subagent/subagent-claude-code/README.md)
- **DSH-S19** Skills filesystem発見規則と制限 — [packages/skill/skill-filesystem/README.md](https://github.com/deepseek-ai/deepseek-harness/blob/c291e7961a515f6d7af9304e7fd1d257929aef26/packages/skill/skill-filesystem/README.md)
- **DSH-S20** base bundleの実効構成 — [packages/bundle/base/cordis.patch.yml](https://github.com/deepseek-ai/deepseek-harness/blob/c291e7961a515f6d7af9304e7fd1d257929aef26/packages/bundle/base/cordis.patch.yml)
- **DSH-S21** Ralph能力検査・固定loop実装 — [packages/workflow/tool-ralph/src/index.ts](https://github.com/deepseek-ai/deepseek-harness/blob/c291e7961a515f6d7af9304e7fd1d257929aef26/packages/workflow/tool-ralph/src/index.ts)
- **DSH-S22** 上流ライセンス表示 — [LICENSE](https://github.com/deepseek-ai/deepseek-harness/blob/c291e7961a515f6d7af9304e7fd1d257929aef26/LICENSE)

## 再利用の意味

既存一般設計をDeepSeekの独自発明とは表現しない。コードの直接依存追加は0件であり、本版は先行実装の契約・制限・試験観点を本製品設計へ統合したもの。直接vendoringは必要性・依存closure・license/notice・権限・停止・回帰を検証したCRだけで行う。


## v3モデル別資料

現在のモデル別調整の根拠は[MODEL_SOURCES.md](MODEL_SOURCES.md)と[機械可読資料索引](model_optimization_sources.json)。過去の出典索引は参照commit時点の履歴であり、現在の稼働資格はWP01で別途確認する。

## V3.1で追加確認した一次資料

[文書・ガードレールの一次資料一覧](DOCUMENT_GUARDRAIL_SOURCES.md)と[機械可読索引](document_guardrail_sources.json)を参照。旧出典は当時の入力provenanceとして保持する。公式資料の記載は本製品の実資格・実試験を代替しない。


## V4 source index

[V4根拠一覧](V4_SOURCES.md)、[入力ZIPのhash](v4_input_provenance.json)。過去資料は履歴の出典であり、実行上の別正本ではない。
