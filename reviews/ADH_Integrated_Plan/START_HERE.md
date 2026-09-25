# START HERE — 統合正本 V4.0.0

このZIP一つで、dotfiles既存ハーネス/OSS/Plugins、ADH V3.1改善、Semantica、prek/Oxlint/Oxfmtを実装する。旧版や別追加計画の読み合わせは不要。任務は完全な実装・検証・完成であり、試作コード・再比較報告への置換ではない。

A1/A3=Claude Code Fable-5.1 high、A2=Codex GPT-6 Astra xhigh、agmsgで協働。値は要求であり本人資格はWP01で検証する。無断fallbackなし。

## 読み方

A1は初回に[決定](spec/00_DECISION.md)、[全体構造](spec/02_ARCHITECTURE.md)、[component](docs/17_COMPONENT_CATALOG.md)、[作業索引](docs/00_WBS_INDEX.md)、[完了](docs/07_COMPLETION_AND_RELEASE.md)を把握する。詳細は[通読版](INTEGRATED_PLAN_JA.md)。以後はTaskPacketと関連・変更した契約を読み、全員へ全文や全Skillsを毎turn注入しない。

[共通](prompts/COMMON_CONTRACT.md)と該当する[A1](prompts/CLAUDE_LEAD.md)/[A2](prompts/CODEX_WORKER.md)/[A3](prompts/CLAUDE_REVIEWER.md)/[A4](prompts/VERIFIER_RUNBOOK.md)を使用する。

## 開始と実装

1. WP00でdotfilesとADHの実repo/path/HEAD/dirty/既存ファイルと本V4チェックサム・35要求を固定する。過去QA/62試験は製品実績に含めない。
2. WP01で現native/本人Auth/model/effort/VM/資源を確認。WP02/04で18IC・12MO・10DG・24GRを実環境へbindingし、本V4に決まった責任・採用範囲を再解釈しない。
3. WP03/05は既存agmsg/独立検証でbootstrapする。未完成SupervisorやSemanticaへ初期開発を依存させない。WP06で生成正本・全selected資産と10入口を適合する。
4. WP07–25で制御・隔離・公式接続・knowledge/quality・学習を担当scopeで実装。毎WPは負例/再現→実装→局所/必須検査→A4/独立A3→修正→直列統合→回帰。
5. 依存/実scope/Worktree/予算が揃う独立taskだけ並列化する。共有schema/generator/lock/統合は一writer。二repoは同ReleaseSetで受け入れる。
6. WP26–31で実Auth/全selected assets/VM/実AI/運用/全回帰を確認し、完成ソース・全試験・手引・証拠・ReleaseSetを提出する。

## 境界

モデル設定の編集元はdotfiles adh profile、profiles/model_profiles.jsonは要求/検査view。Semanticaは参照、prekは検査runner。どちらも権限やACCEPTEDを作れない。knowledge低下は正本へ戻り、必須情報不足だけHOLD。formatterは明示fix、commit/CI/Verifierはcheck-only。学習の昇格は検証/承認後の次release。

E0/E1は自律実行・構築する。真正な本人Auth/権限/予算/停止は対象だけ保留して独立作業を続ける。回避目的のモデル変更・全権限化・基準緩和をしない。

## 完成

35R・32WPの全作業・192親/244内包子・18IC・12MO・10DG・24GR・選択component・10Skill・実Auth/VM/AI/運用・同RC/ReleaseSetの証拠一致が必要。旧72runと製品18runは条件一致時だけ同run IDを共有。旧48＋新12Skill入力、未見群、knowledge/qualityの独立評価も規約に従う。

本ZIPは仕様・計画・指示資産・評価入力。製品コード/installer/実製品PASSは含まない。全WP=PLANNED、全実行検証=NOT_RUN。
