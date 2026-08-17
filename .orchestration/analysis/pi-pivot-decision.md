# Pi 転換決定 — 第 3 エージェント廃止と思想・機能の中核吸収

- 作成: 2026-08-17(オーケストレータ: Claude Code / Fable-5 xhigh)
- operator 裁定: 「pi を第 3 エージェントにしている箇所は削除したうえで、pi の思想や
  機能を活かして現在の Claude Code + Codex の AI エージェント構成とハーネスに
  組み入れる方針に転換」
- 根拠検証: 4 系統の一次ソース検証(docs 全 27 ページ・v0.84.1/main 二重照合・
  16 主張ファクトチェック・実運用パターン調査)。詳細は本書 §1。
- 対応計画: `.orchestration/tasks/PLAN-pi-pivot.md`

## 1. 決定に至った検討(要旨)

1. **課金構造の非対称(決定打)**: Claude Pro/Max のサードパーティハーネス利用は
   「extra usage からのトークン課金でプラン枠を消費しない」(providers.md:35、
   実クォータ枯渇 400 で実証)。Fable-5 を Pi で使う構成は本ユーザーには経済的に
   不合理。残る存続理由は「gpt-5.6 同一購読での対 Codex ハーネス効率」一点に収斂し、
   未検証のままそれを待つ価値より、撤去+知見吸収の確実な価値が上回る。
2. **駆動アーキテクチャの実態**: RPC 直結は E2E 5 ラウンドで実証済みだが、公式
   rpc.md に安定性保証はなく、Earendil 自身の運用前例(pi-chat)は tmux 常駐
   ワーカー+状態ファイルであり、我々の herdr/agmsg 常駐 Codex 構成を追認する。
   「Pi でなければ得られない駆動」は存在しない。
3. **π-A(統一 LLM レーン)の需要不在**: pi-ai は実在の資産(週間 DL 299 万)だが、
   体制の LLM 需要(probe 採点・permgate shadow)は既存経路で充足しており、
   40 プロバイダ統一が解く問題を我々は持たない。
4. **恒久価値は既に中核へ回収済み**: permgate 決定プロトコル/workspace-write 層/
   strict パス解決、send.sh SQL 注入と codex レシーバ信頼境界の脆弱性修正、
   「文字列合成でなく第一級ツール」の教訓 — いずれもハーネス非依存の共有資産。

## 2. 削除・維持の棚卸し(git 履歴 #133=93872d3 / #134=03a01c2 の実差分から導出)

### 2a. 純 Pi ファイル(全削除)

- `home/dot_pi/**`(settings.json、extensions/{permgate,contextdb,agmsg}.ts、.gitkeep)
- `home/dot_local/bin/common/executable_agmsg-pi-worker`(400 行)
- `home/dot_local/bin/common/executable_pi-model-access-check`(486 行)
- `home/dot_local/bin/common/executable_pi-session-evidence`(205 行)
- mise ピン行(config.toml 1 行+lock 4 行 — ペア規約で独立 chore)
- テスト: `pi_*.test.mjs`・`pi_*_types.d.ts`・`test_pi_*.py`・
  `test_agmsg_pi_worker.py`・`fixtures/pi_sessions/**`

### 2b. 混在ファイル(外科的部分処理 — hunk 単位の判断)

| ファイル | Pi 由来の差分 | 処置 |
|---|---|---|
| `executable_permgate`(+47/+146) | `pi` プロバイダ=決定プロトコル+workspace-write 層+strict 解決+sensitive-read | **機構は全維持**、プロバイダ名 `pi`→`cli` に改名(中立な機械可読レーンとして恒久化) |
| `permgate-policy.yaml`(+4/+15) | pi 節 | `cli` 節へ改名(workspace_write/read_deny_patterns 維持) |
| `test_permgate.py`(+79/+305) | pi レーンテスト | 維持・改名追従 |
| `join.sh`(+6) | `pi` 型ホワイトリスト | **削除**(呼び出し元消滅) |
| `whoami.sh`(+29) | shdoc 化+pi 型記載 | shdoc 維持・pi 型記載のみ削除 |
| `check-inbox.sh`(+62) | ブリッジ用 env 制御+shdoc | env 制御は削除(YAGNI)・shdoc 維持 |
| `SKILL.md`(+2) | pi ワーカー節 | 削除 |
| `validate-agent-assets.py`(+37/+21) | pi-assets カテゴリ | 削除(対象ファイル消滅) |
| `tests/unit/test_validate_agent_assets.py`(混在) | pi-assets フィクスチャ/テスト(validate_pi_assets 呼び出し・拡張ハッシュ参照の範囲) | pi 固有のヘルパ/テストのみ削除、他カテゴリのテストは維持(PR #135 レビューで補正) |

### 2c. 共有資産(Pi 経由で獲得・全維持)

- `send.sh`(+23): SQL 安全化+`test_agmsg_send.py` — 全呼び出し元を守る恒久修正
- `executable_contextdb-codex-notify`(+15)+`test_contextdb_codex_notify.py`:
  信頼ランタイム化(T48 期の脆弱性修正)
- 以前の計画由来: recovery_injected(T54)、manifest/remove(T57-58)、staleness 等

### 2d. ランタイム側の撤去(orchestrator chore)

- `mise uninstall` と配備済み `~/.local/bin` の該当 3 スクリプト・`~/.pi` の管理生成物
  (**`~/.pi/agent/auth.json` は operator 資格情報のため残置** — 処分は operator 判断)
- agmsg identity `pi-standard-dot` の leave.sh、スクラッチ `~/Workspace/pi-e2e`

## 3. 吸収対象(pi の思想・機能 → CC+Codex ハーネス)

| 由来                     | 吸収内容                                                                                                                                                                |
| ------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 決定プロトコル(T66)      | permgate の機械可読レーンを `pi` 名から中立名 `cli` へ改名して恒久化(将来の任意呼び出し元用)。workspace-write 層・strict 解決・センシティブ read 拒否はそのまま共有基盤 |
| 第一級ツールの教訓(T68b) | send.sh 本体に識別子文法検証を内蔵し、pi ツール境界にあった防御を**全呼び出し元**(Codex ワーカー含む)へ一般化                                                           |
| コスト第一級主義         | 受入記録(ACCEPTANCE)にタスク単位のトークン/コスト概算欄を規約追加(Pi のセッション会計思想の運用移植)                                                                    |
| 最小固定部思想(<1k)      | ハーネスが常時注入する文脈(rules/CLAUDE.md/スニペット)のトークン実測監査と削減提案(context diet)。Databricks 知見「ハーネス効率がコストを 2 倍動かす」の自前適用        |
| 既回収済み               | model-visible=logged(T54)、逆写像/manifest(T57-58)、trusted-runtime レシーバ(T68c)、SQL 安全化 — 維持のみ                                                               |

## 4. 判断の但し書き

- 撤去は `remove-agent-asset`/mise/chezmoi の既存逆写像で完結し、コストは沈まない。
- 将来 gpt-5.6 同一購読の A/B を行いたくなった場合、再導入は T65〜T70 の受入済み
  タスク仕様と本書で再現可能(知識は保存される)。
