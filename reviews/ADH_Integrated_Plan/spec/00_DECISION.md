# 統合決定 — ADH V4

版4.0.0 / 2026-09-13。利用者要求によりV3.1と2種類のSemantica/prek/Oxc計画を一つの実装正本へ改訂する。今回の成果物は仕様・作業計画・指示資産・データ契約・検証入力であり、製品実装コードではない。

## 採用する全体像

**dotfilesを配布・構成・更新の基盤、公式Claude Code/Codexを推論・開発の実行主体、単一Supervisorを工程/権限/受入の正本とする。** Superpowers/Ponytail/Crit等は方法論とレビュー、UA/CompactionDB/Semanticaは役割を分けた根拠供給、prek/Oxcと既存checkerは共通品質経路、Runnerは実行境界を所有する。DeepSeek由来のIC01–11、モデル最適化MO01–12、文書DG01–10、ガードGR01–24を同じ開始・継続・変更・受入へ接続する。

既存/新規の都合だけでなく、公式認証・ネイティブ拡張・全工程自律・独立検証という要件に基づく選定である。DeepSeekを無価値と判定したわけではなく、その先行実装と制限を契約へ採用する。一方、第二のDSH loop/Session DB/Cordis runtimeを必須にはしない。直接コード再利用はライセンスと依存closure・実役割が適合するものに限り、採用数や実証済み能力を誇張しない。

## 一つの製品、一つの受け入れ、二つの変更対象

実装対象は (D) 既存mryfmo/dotfilesの限定変更と、(A) autonomous-dev-harnessの完成実装。両方をReleaseSetで一緒に受け入れる。dotfilesに本体のコピーを置かず、配布manifest・設定生成・薄いlauncher・project opt-inを置く。ADHにSupervisor/Runner/知識adapter/quality dispatcher/独立検証を一度だけ実装する。コード配置を一repoへ勝手に変更しない。両repoの関係はspec/11_DISTRIBUTION_AND_COMPOSITION.mdを正本とする。

## 維持する条件

35原要求の本文を保持する。32WP、192親検査、既存196必須subcaseは削除しない。V4では4内部契約と48必須subcaseを統合し、18IC・244内包子とする。旧36＋24の追加検査は移管対応済みで、独立した別合格数ではない。SOURCEや固定評価入力に残る過去版は来歴であり、実行正本の版ではない。

Fable-5.1/high（A1/A3）・GPT-6 Astra/xhigh（A2）・agmsgを維持する。値は要求であり、本人環境の能力を文書だけで資格済みにしない。実行資格を満たさない場合にモデルやeffortを無断代替しない。

Python3.13/uvのADH core、SQLite local WALの単一control host、Linux VMの信頼領域分離、Worktreeの単一writer、有限予算、独立Verifier/Reviewerを維持。知識SDKは別uv環境に置き、解析依存をcoreやglobal Pythonへ混在させない。新しい外部LLM/embedding/MCP/graph DB/SaaSを初期必須依存にしない。

## 統合の定義

構成・データ・権限・品質・状態・更新の各責任に、一つの編集正本または確定主体を割り当てる。同じtask/attempt/ReleaseSetと対象snapshotを、取込→TaskPacket→実行→品質→独立検証→統合→来歴更新へ渡す。相互参照だけを追加して後続へ再設計を委ねない。

旧V3.1と別添SI/DI計画は履歴の入力に限る。このZIPだけで実装と検証を開始できる。バージョン/絶対path/本人認証/有限予算など実環境値はWP01で取得する明確なbindingであり、設計選択を空欄にしたものではない。

## 検証と状態

作成済み指示資産と仕様の整合を検査する。全WP=PLANNED、全製品検査=NOT_RUN、製品受入=NOT_STARTED。実native/Plugins/Semantica/prek/Oxc/VM/AI E2E・性能の成功を今回の文書QAから推定しない。調査範囲はsources/v4_sources.jsonに明記し、上流全ファイルを新たに実行監査したとは言わない。
