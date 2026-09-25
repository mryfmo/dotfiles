# 既存ハーネス・OSS・Pluginsの統合配置

実際の製品起動資格は未取得。ここでは採用責任と選択の規範を定める。optionalを未導入でもよいことと、requiredを任意へ変更してよいことは別。

## CMP01: dotfiles / chezmoi

**kind:** existing_distribution

**decision:** RETAIN_ADAPT

**owner:** dotfiles release owner

**role:** 対象資産の配布、dry-run、適用、更新、doctor、remove

**not_owner:** 案件の管理DB、利用者資格情報、原本の保存

**implementation_paths:** dotfiles:home/, dotfiles:scripts/

**work_packages:** WP00, WP06, WP26, WP30

**source_ids:** V4-S01, V4-S03

**implementation_status:** PLANNED

**live_qualification:** NOT_RUN

## CMP02: mise / uv / project lock

**kind:** existing_toolchain

**decision:** RETAIN_ADAPT

**owner:** toolchain owner

**role:** 配布binaryとPython環境とproject依存を分離し完全lock

**not_owner:** 全HOMEのPython更新、check中の最新版取得

**implementation_paths:** dotfiles:home/dot_mise/, adh:integrations/semantica/, adh:pyproject.toml

**work_packages:** WP01, WP03, WP06, WP30

**source_ids:** V4-S01, V4-S05

**implementation_status:** PLANNED

**live_qualification:** NOT_RUN

## CMP03: Claude Code Fable-5.1 high

**kind:** official_runtime

**decision:** RETAIN_QUALIFY

**owner:** A1/A3 runtime adapter

**role:** 要求調査、設計提案、統括、別contextレビュー

**not_owner:** 独立検査の自己申告置換

**implementation_paths:** adh:src/adh/adapters/claude/

**work_packages:** WP01, WP15, WP21, WP26

**source_ids:** V4-S12, V4-S13

**implementation_status:** PLANNED

**live_qualification:** NOT_RUN

## CMP04: Codex GPT-6 Astra xhigh

**kind:** official_runtime

**decision:** RETAIN_QUALIFY

**owner:** A2 runtime adapter

**role:** 常駐worker、exact thread、実装と修正

**not_owner:** 自己受入、無断モデル切替

**implementation_paths:** adh:src/adh/adapters/codex/

**work_packages:** WP01, WP16, WP26

**source_ids:** V4-S11, V4-S01

**implementation_status:** PLANNED

**live_qualification:** NOT_RUN

## CMP05: Superpowers

**kind:** existing_plugin

**decision:** ADAPT

**owner:** workflow owner

**role:** 要求/比較/計画/TDD/仕様レビュー/品質レビューの方法論

**not_owner:** 第二のscheduler、無承認仕様変更

**implementation_paths:** adh:skill-pack/, dotfiles:scripts/update-agent-assets.sh

**work_packages:** WP02, WP06, WP18, WP19, WP21

**source_ids:** V4-S02

**implementation_status:** PLANNED

**live_qualification:** NOT_RUN

## CMP06: Ponytail

**kind:** existing_plugin

**decision:** ADAPT

**owner:** workflow owner

**role:** 既存再利用・最小の正しい変更

**not_owner:** 必須テスト/NFR/例外処理削除

**implementation_paths:** adh:skill-pack/, dotfiles:home/dot_config/codex/AGENTS.md

**work_packages:** WP06, WP21

**source_ids:** V4-S01

**implementation_status:** PLANNED

**live_qualification:** NOT_RUN

## CMP07: agmsg

**kind:** existing_transport

**decision:** RETAIN_ADAPT

**owner:** message bridge owner

**role:** TASK/RESULT/ACCEPTANCEの配送と通知

**not_owner:** 認証、DAGの二重管理、acceptedの自己確定

**implementation_paths:** dotfiles:home/dot_agents/skills/agmsg/, adh:src/adh/messaging/

**work_packages:** WP05, WP17, WP22

**source_ids:** V4-S02

**implementation_status:** PLANNED

**live_qualification:** NOT_RUN

## CMP08: Herdr / tmux / terminal panes

**kind:** existing_surface

**decision:** OPTIONAL_QUALIFIED

**owner:** operator surface owner

**role:** 操作・表示・常駐pane管理

**not_owner:** 完了認定、Runnerのlease管理

**implementation_paths:** dotfiles:home/dot_local/bin/common/, adh:docs/runbooks/

**work_packages:** WP05, WP06, WP26, WP30

**source_ids:** V4-S02, V4-S03

**implementation_status:** PLANNED

**live_qualification:** NOT_RUN

## CMP09: permgate / native permissions

**kind:** existing_enforcement_adapter

**decision:** ADAPT

**owner:** policy owner

**role:** 共通policyを各native受付へ接続し適用能力を検査

**not_owner:** LLM分類だけの権限拡大、Hookだけのsandbox保証

**implementation_paths:** dotfiles:home/dot_local/bin/common/executable_permgate, dotfiles:home/dot_agents/permgate-policy.yaml

**work_packages:** WP06, WP08, WP12, WP26, WP29

**source_ids:** V4-S01

**implementation_status:** PLANNED

**live_qualification:** NOT_RUN

## CMP10: Understand-Anything

**kind:** existing_analysis_plugin

**decision:** ADAPT

**owner:** code context owner

**role:** 実Worktreeの構造/依存をsource付きで解析

**not_owner:** 主repoへの暗黙redirect、要件確定

**implementation_paths:** adh:src/adh/context/ua_adapter/, dotfiles:scripts/update-agent-assets.sh

**work_packages:** WP06, WP09, WP18

**source_ids:** V4-S03

**implementation_status:** PLANNED

**live_qualification:** NOT_RUN

## CMP11: CompactionDB

**kind:** existing_memory

**decision:** ADAPT

**owner:** memory owner

**role:** 公開イベント・選別記憶・再開参照

**not_owner:** 正本/管理state/合否の独立改定

**implementation_paths:** dotfiles:vendor/compactiondb/, adh:src/adh/memory/

**work_packages:** WP06, WP22, WP25, WP30

**source_ids:** V4-S03

**implementation_status:** PLANNED

**live_qualification:** NOT_RUN

## CMP12: Semantica

**kind:** new_dependency

**decision:** ADOPT_SCOPED

**owner:** knowledge adapter owner

**role:** 構造化node/edgeの来歴付きquery/context/impact候補

**not_owner:** 権限/合否判定、独自LLM認証、全extras

**implementation_paths:** adh:integrations/semantica/, adh:src/adh/knowledge/contracts/

**work_packages:** WP01, WP04, WP18, WP25, WP26

**source_ids:** V4-S04, V4-S05, V4-S06

**implementation_status:** PLANNED

**live_qualification:** NOT_RUN

## CMP13: prek

**kind:** new_quality_runner

**decision:** ADOPT_SCOPED

**owner:** quality owner

**role:** 信頼済みcheck inventoryの軽量実行

**not_owner:** security sandbox、最終受入、未知repo自動Hook実行

**implementation_paths:** dotfiles:home/dot_mise/, adh:src/adh/quality/

**work_packages:** WP03, WP06, WP14, WP20, WP30

**source_ids:** V4-S07, V4-S08

**implementation_status:** PLANNED

**live_qualification:** NOT_RUN

## CMP14: Oxlint

**kind:** new_language_checker

**decision:** ADOPT_WHEN_APPLICABLE

**owner:** JS/TS quality owner

**role:** JS/TS lintと資格済み時のtype-aware検査

**not_owner:** Python/Shell検査、未確認の型検査置換

**implementation_paths:** adh:quality/, dotfiles:tools/quality/

**work_packages:** WP03, WP06, WP14, WP20

**source_ids:** V4-S10

**implementation_status:** PLANNED

**live_qualification:** NOT_RUN

## CMP15: Oxfmt / compatible Prettier

**kind:** new_formatter

**decision:** ADOPT_WITH_MIGRATION

**owner:** format owner

**role:** 対応形式を一file一formatterで明示fix/check

**not_owner:** 同fileの二重formatter、暗黙import並替、空path全体整形

**implementation_paths:** adh:quality/, dotfiles:home/dot_claude/hooks/executable_format-edited-files.py

**work_packages:** WP03, WP06, WP14, WP24

**source_ids:** V4-S09

**implementation_status:** PLANNED

**live_qualification:** NOT_RUN

## CMP16: Ruff / Pyright / existing ty / Vulture

**kind:** existing_python_quality

**decision:** RETAIN_SCOPED

**owner:** Python quality owner

**role:** ADH Pyright strict、Python lint/formatと承認済既存検査

**not_owner:** 一律の型検査削除、浮動uvx起動

**implementation_paths:** adh:pyproject.toml, dotfiles:home/dot_agents/skills/python-uv-workflow/

**work_packages:** WP03, WP06, WP14, WP20

**source_ids:** V4-S18

**implementation_status:** PLANNED

**live_qualification:** NOT_RUN

## CMP17: ShellCheck / shfmt / Bats / unittest

**kind:** existing_quality

**decision:** RETAIN

**owner:** shell/testing owner

**role:** 既存dotfiles回帰とShellの検査

**not_owner:** Oxcだけを全品質検査にすること

**implementation_paths:** dotfiles:Makefile, dotfiles:tests/, dotfiles:.github/workflows/

**work_packages:** WP03, WP20, WP30, WP31

**source_ids:** V4-S17

**implementation_status:** PLANNED

**live_qualification:** NOT_RUN

## CMP18: Crit

**kind:** existing_review_plugin

**decision:** ADAPT

**owner:** independent reviewer owner

**role:** レビュー観点・指摘・解消の記録

**not_owner:** UI待機の常時要求、receipt文面だけの承認

**implementation_paths:** dotfiles:scripts/require-crit-review.py, adh:src/adh/review/

**work_packages:** WP06, WP21, WP26

**source_ids:** V4-S02

**implementation_status:** PLANNED

**live_qualification:** NOT_RUN

## CMP19: AutoSkill / learning registries

**kind:** existing_workflow_assets

**decision:** ADAPT

**owner:** learning candidate owner

**role:** 候補→評価→承認→昇格→次runへ適用

**not_owner:** active ruleの自己書換え・基準緩和

**implementation_paths:** adh:src/adh/learning/, dotfiles:home/dot_agents/skills/agmsg-orchestration/

**work_packages:** WP06, WP25, WP30

**source_ids:** V4-S02

**implementation_status:** PLANNED

**live_qualification:** NOT_RUN

## CMP20: terminal-code / terminal-browser

**kind:** existing_operator_tools

**decision:** OPTIONAL_QUALIFIED

**owner:** operator surface owner

**role:** 選択時のみ編集/資料取得のUIとして利用

**not_owner:** 新LLMルータ、無許可通信、独立した仕様正本

**implementation_paths:** dotfiles:scripts/update-agent-assets.sh

**work_packages:** WP06, WP26, WP30

**source_ids:** V4-S03

**implementation_status:** PLANNED

**live_qualification:** NOT_RUN

## CMP21: ccstatusline / ccusage / status / staleness

**kind:** existing_observability

**decision:** OPTIONAL_QUALIFIED

**owner:** observability owner

**role:** 公開metadataに基づく表示、停滞候補の通知

**not_owner:** 非公開token推定、pane idleから完了認定

**implementation_paths:** dotfiles:home/dot_mise/, adh:src/adh/observability/

**work_packages:** WP06, WP25, WP30

**source_ids:** V4-S01

**implementation_status:** PLANNED

**live_qualification:** NOT_RUN

## CMP22: DeepSeek design and regression patterns

**kind:** prior_art

**decision:** INTEGRATED_DESIGN_NO_RUNTIME

**owner:** architecture owner

**role:** IC01–11の能力/投影/耐久/継続/所有権/文脈/検証

**not_owner:** 第二DSH loop、Cordis/Session DBの暗黙導入

**implementation_paths:** adh:src/adh/domain/, adh:src/adh/dispatch/, adh:src/adh/projections/

**work_packages:** WP04, WP07, WP14, WP22, WP25

**source_ids:** V4-S15

**implementation_status:** PLANNED

**live_qualification:** NOT_RUN

## CMP23: Supervisor / Baseline / Policy

**kind:** product_planned

**decision:** IMPLEMENT

**owner:** control owner

**role:** 承認基準、DAG、claim、grant、受入、予算、復旧

**not_owner:** モデルの内部履歴の加工

**implementation_paths:** adh:src/adh/domain/, adh:src/adh/scheduler/, adh:src/adh/storage/

**work_packages:** WP07, WP08, WP10, WP11, WP12, WP27

**source_ids:** V4-S15

**implementation_status:** PLANNED

**live_qualification:** NOT_RUN

## CMP24: Runner / Worktree / Linux VM

**kind:** product_planned

**decision:** IMPLEMENT

**owner:** runner owner

**role:** provision、単一writer、OS/通信/秘密境界、凍結とprocess静止

**not_owner:** Worktree=security、lease失効だけの再割当

**implementation_paths:** adh:src/adh/runner/, adh:deployment/

**work_packages:** WP09, WP13, WP14, WP24, WP29

**source_ids:** V4-S15, V4-S16

**implementation_status:** PLANNED

**live_qualification:** NOT_RUN

## CMP25: Independent Verifier / signer

**kind:** product_planned

**decision:** IMPLEMENT

**owner:** verification owner

**role:** 固定snapshotで独立実測し署名、失敗/skip/exitを別記録

**not_owner:** candidateへ署名鍵配布、fake PASS承認

**implementation_paths:** adh:src/adh/verifier/, adh:src/adh/review/

**work_packages:** WP20, WP21, WP26, WP31

**source_ids:** V4-S15

**implementation_status:** PLANNED

**live_qualification:** NOT_RUN

## CMP26: 10 artifacts / typed graph / TaskPacket

**kind:** specified_assets

**decision:** RETAIN_EXTEND

**owner:** document and context owner

**role:** 正本関係・該当closure・履歴・原本範囲を供給

**not_owner:** 全文毎turn注入、検索top-kでMUST欠落

**implementation_paths:** adh:contracts/, adh:src/adh/context/

**work_packages:** WP04, WP18, WP19, WP25

**source_ids:** V4-S11, V4-S12

**implementation_status:** PLANNED

**live_qualification:** NOT_RUN

## CMP27: MCP / independent model routers / unrelated dotfiles apps

**kind:** unselected_assets

**decision:** PRESERVE_OUTSIDE_ADH_PROFILE

**owner:** operator

**role:** 既存利用者資産は変更しない。ADH実効closureへ暗黙追加しない

**not_owner:** 今回の依存や制御経路への追加

**implementation_paths:** dotfiles:home/

**work_packages:** WP00, WP06, WP30

**source_ids:** V4-S01

**implementation_status:** PLANNED

**live_qualification:** NOT_RUN
