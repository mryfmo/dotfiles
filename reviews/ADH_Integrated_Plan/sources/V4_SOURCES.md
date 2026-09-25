# V4の根拠と参照範囲

確認範囲・未検証をv4_sources.jsonに記録。source確認は採用環境での実証ではない。旧DSH/MO/DG/GRの根拠は既存索引を保持する。

## V4-S01: dotfiles canonical agent configuration

https://github.com/mryfmo/dotfiles/blob/fdfa5f042e2e00a27a8320e5f37f749c422e8d91/home/dot_agents/agent-config.yaml

確認方法: GitHub.fetch_file / 2026-09-13

生成正本、旧profile、permissionsと編集Hookを確認。実HOME適用状態は未確認。

## V4-S02: agmsg orchestration contract

https://github.com/mryfmo/dotfiles/blob/fdfa5f042e2e00a27a8320e5f37f749c422e8d91/home/dot_agents/skills/agmsg-orchestration/SKILL.md

確認方法: GitHub.fetch_file / 2026-09-13

常駐worker・worktree・配送・express E2E・自己受入規則を確認しV4で適合する。

## V4-S03: dotfiles asset lifecycle

https://github.com/mryfmo/dotfiles/blob/fdfa5f042e2e00a27a8320e5f37f749c422e8d91/scripts/update-agent-assets.sh

確認方法: GitHub.fetch_file / 2026-09-13

terminal-code/browser、CompactionDB、Herdrも配布対象。未成功の同期を資格済と扱わない。

## V4-S04: Semantica plugin hooks

https://github.com/semantica-agi/semantica/blob/7057387775ecdf74c14e38d0067fd8e1267eaaf8/plugins/hooks/hooks.json

確認方法: GitHub.fetch_file / 2026-09-13

provenance echoを実来歴検証と扱わない。

## V4-S05: Semantica dependency and feature contract

https://github.com/semantica-agi/semantica/blob/7057387775ecdf74c14e38d0067fd8e1267eaaf8/pyproject.toml

確認方法: prior_connected_source_carried_forward / 2026-09-13

本体/Plugin/依存版を別識別。選択機能の実install資格は後続。

## V4-S06: Semantica query Skill

https://github.com/semantica-agi/semantica/blob/7057387775ecdf74c14e38d0067fd8e1267eaaf8/plugins/skills/query/SKILL.md

確認方法: prior_connected_source_carried_forward / 2026-09-13

HOME共通graphとpipの例をproject-scoped/uvへ適合する。

## V4-S07: prek security

https://prek.j178.dev/security/

確認方法: web_or_connector_read_this_turn / 2026-09-13

Hookとproject設定は実行コードである。信頼・pin・CIを分離。

## V4-S08: prek configuration

https://prek.j178.dev/reference/configuration/

確認方法: web_or_connector_read_this_turn / 2026-09-13

Hook優先順位と単一Hook内require_serialの範囲を確認。

## V4-S09: Oxfmt usage

https://oxc.rs/docs/guide/usage/formatter.html

確認方法: web_or_connector_read_this_turn / 2026-09-13

採用版と形式対応を資格確認し、一file一formatter/check-onlyを設計。

## V4-S10: Oxlint type-aware lint

https://oxc.rs/docs/guide/usage/linter/type-aware.html

確認方法: prior_official_source_carried_forward / 2026-09-13

通常lintと型検査を区別。既存検査を互換性未確認で削除しない。

## V4-S11: Astra prompting and skills

https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra

確認方法: web_or_connector_read_this_turn / 2026-09-13

短い適用条件・必要時詳細・重複指示抑制を維持する。

## V4-S12: Fable 5.1 prompting

https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1

確認方法: web_or_connector_read_this_turn / 2026-09-13

独立取得・委任後作業・scope・完遂を役割へ適用。API専用設定をCLIへ発明しない。

## V4-S13: Fable 5.1 migration

https://platform.claude.com/docs/en/models/fable-5-1/migration-guide

確認方法: web_or_connector_read_this_turn / 2026-09-13

公式nativeが所有する履歴と外側TaskPacketを分ける。

## V4-S14: Article supplied by user

https://nansystem.com/prek-oxlint-oxfmt-pre-commit/

確認方法: web_or_connector_read_this_turn / 2026-09-13

導入動機として参照。技術契約は公式資料、速度倍率は本環境で保証しない。

## V4-S15: DeepSeek architecture

https://github.com/deepseek-ai/deepseek-harness/blob/c291e7961a515f6d7af9304e7fd1d257929aef26/docs/architecture.md

確認方法: prior_source_pack_carried_forward / 2026-09-13

IC01–11の先行実装根拠を継承。直接runtime依存は追加しない。

## V4-S16: Git worktree

https://git-scm.com/docs/git-worktree

確認方法: prior_official_source_carried_forward / 2026-09-13

git common-dirやHook配置とOS認可を区別。

## V4-S17: dotfiles CI

https://github.com/mryfmo/dotfiles/blob/fdfa5f042e2e00a27a8320e5f37f749c422e8d91/.github/workflows/test.yaml

確認方法: prior_connected_source_carried_forward / 2026-09-13

品質設定/lockのみの変更も必須job評価へ接続。

## V4-S18: dotfiles Python workflow

https://github.com/mryfmo/dotfiles/blob/fdfa5f042e2e00a27a8320e5f37f749c422e8d91/home/dot_agents/skills/python-uv-workflow/references/python-uv-rules.md

確認方法: prior_connected_source_carried_forward / 2026-09-13

pre-commit例のpin欠落・formatter fix・型検査の役割をV4で具体化。
