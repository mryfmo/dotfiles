# モデル最適化の確認資料

確認日：2026-09-13。公開資料上の対応と本人環境での稼働資格は別である。本文をwebで確認した。HTTP本文の完全コピー・hashはこの配布物に含めず、後続WP01で採用版を取得し出典台帳へ固定する。

## OPT-S01

[OpenAI Developers: Rethinking skills and prompts for GPT-6 Astra](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra)

AstraのSkill説明、文脈、不要な手順、許可境界、完了指示を調整する際の指針。 適用面：Codex prompting。

## OPT-S02

[Anthropic: Prompting Claude Fable 5.1](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1)

Fableの公開進捗、独立ツール呼出、委任、作業範囲、履歴と成果物の扱いを調整する際の指針。 適用面：Model behavior; API examples are not CLI flags。

## OPT-S03

[Anthropic: Migrating to Claude Fable 5.1](https://platform.claude.com/docs/en/models/fable-5-1/migration-guide)

Messages APIの非互換設定と履歴条件。公式CLIが履歴を所有する構成と区別する。 適用面：Messages API versus native CLI。

## OPT-S04

[OpenAI: Build skills](https://learn.chatgpt.com/docs/build-skills)

Skillの段階的読込、カタログ、明示/暗黙呼出、配置とmetadata。 適用面：Codex skills。

## OPT-S05

[Anthropic: Extend Claude with skills](https://code.claude.com/docs/en/skills)

Skillのmodel/effort上書き、fork、native frontmatterの意味。 適用面：Claude Code Skills。

## OPT-S06

[OpenAI: Codex App Server](https://learn.chatgpt.com/docs/app-server)

model/effort catalog、スレッド・ターンと実schemaによる接続。 適用面：Codex App Server。

## OPT-S07

[Anthropic: Claude Code CLI reference](https://code.claude.com/docs/en/cli-reference)

CLI起動・effort・fallback・公開出力の指定を採用版で確認する基準。 適用面：Claude Code CLI。

## OPT-S08

[OpenAI: Prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching)

安定部分と変化部分の配置を考える参照。Codex内部cache操作を約束する根拠ではない。 適用面：API caching; no forced native internals。
