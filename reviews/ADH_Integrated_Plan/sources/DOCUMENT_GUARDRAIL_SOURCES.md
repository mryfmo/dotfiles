# 文書体系・ガードレールの一次資料

確認日：2026-09-13。設計判断と閾値は本計画の規定でありベンダー保証ではない。OpenAI Agents SDKやC4専用ランタイムを新たな依存にしない。

- **DG-S01** [C4 model: Diagrams](https://c4model.com/diagrams) — C4は構造の拡大率。BRD/PRDとは同義でなく全4段必須でもない。
- **DG-S02** [Alistair Mavin: EARS](https://alistairmavin.com/ears/) — EARSはテキスト要求の軽量構文。形式証明や完全性保証ではない。
- **DG-S03** [Cucumber: Gherkin Reference](https://cucumber.io/docs/gherkin/reference/) — Given/When/Thenの期待と実際に比較するstep実装を区別する。
- **DG-S04** [Martin Fowler: Test Driven Development](https://martinfowler.com/bliki/TestDrivenDevelopment.html) — TDDはRed/Green/Refactorの開発反復であり文書レベルではない。
- **DG-S05** [Cognitect: Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) — ADRはcontext/decision/consequencesとstatusを保持する。
- **DG-S06** [NASA: Requirements Management](https://www.nasa.gov/reference/6-2-requirements-management/) — 要求と設計/試験の双方向追跡、変更影響、基準管理の根拠。
- **GR-S01** [OpenAI: Running Codex safely](https://openai.com/index/running-codex-safely/) — 管理設定・sandbox・network・approval・telemetryを組み合わせる。
- **GR-S02** [Codex: Agent approvals & security](https://learn.chatgpt.com/docs/agent-approvals-security) — 承認ポリシーとsandboxは別。worktree .git等保護、迂回リスクを採用版で再確認。
- **GR-S03** [Claude Code: Hooks reference](https://code.claude.com/docs/en/hooks) — Hookのevent・type・exit code・timeoutで拒否能力が違う。存在や非0終了だけではfail-closedを保証しない。
- **GR-S04** [Claude Code: Sandboxing](https://code.claude.com/docs/en/sandboxing) — Bashと子processのOS隔離とネットワーク境界。別ツールへの適用は個別確認。
- **GR-S05** [Claude Code: Permissions](https://code.claude.com/docs/en/permissions) — 権限の合成/範囲を実runtimeで検証。文章での禁止とは別。
- **GR-S06** [OpenAI: Guardrails and human review](https://developers.openai.com/api/docs/guides/agents/guardrails-approvals) — 入力/出力/tool検査と人の承認は別。高リスクでは実行前に検査完了を待つ。SDKの追加採用指示ではない。
- **GR-S07** [OpenAI: Evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices) — 評価を初期から継続し、正例/負例/未見群/全runを保存する。
- **GR-S08** [OpenAI: Rethinking skills and prompts for GPT-6 Astra](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra) — 適用範囲を絞り、必要時参照。文書体系やガードの全文を毎回注入しない。
- **GR-S09** [Anthropic: Prompting Claude Fable 5.1](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1) — 委任/並列取得/継続と公式履歴境界。今回の元モデル契約を維持。
- **GR-S10** [Claude Code: Skills](https://code.claude.com/docs/en/skills) — Skillは命令資産。設定/Hook/model等を含み得るので文書取得とは分離する。
