# 目的とゴール(操作者確定、2026-11-06)

操作者が 2026-11-06 に確定したゴール。これ以外のゴールは無い。一字も変えない。

> omp を最下層に、DSH がワークフロー制御、dsh-superagent が Slack/Outlook/Teams/GitHub の受付、全体が Anthropic sandbox の中で動く。graphify、security skill、e2e、knowledge-work を統合した TechnoPro Agent Harness Kit として完成し、両ホストで他プロジェクトの開発を自律駆動する。

出典は操作者の言葉 2026-11-02 21:18Z(六点)、21:27Z と 21:37Z(三層と sandbox)、11-06 03:2xZ(上の一文を「目的とゴールはこれしかない」と確定)。

この文書の前版(同日 06:xxZ)は coordinator が自分で作った完了条件を目的として書いた誤りだった。前版の §2「提案する完了条件」と §8「ADR-009 は後の別判断」は撤回する。

## 1. ゴールの要素と今日の距離(実測、2026-11-06T08:19Z 更新)

| ゴールの要素 | 今日(実測) | 距離 | 確認コマンド |
| --- | --- | --- | --- |
| omp が最下層で agent、tool、skill の呼び出しを担う | omp 席は srt 下で動く(U85)。macOS のみ。Ubuntu に席も store も無し | 片側達成 | `hcom list -v`(ラップトップ)、`ssh <redacted> ls ~/.local/state/omp-seats`(無し) |
| DSH がワークフロー制御 | login 経由 route (d) が実 login で end to end 動作(U240 round 3、07:15Z と 08:17Z 実測、API key なし)。試験項目表 tests/dsh-login-route.tsv は 59 項目中 55 OK、4 pending(seat と profile 項目)。kit の thak profile(U227b 描画)でも実 turn が pong(08:18Z、3.6 s)。PR 679(adapter、監査 round 3 実行中)、PR 686(profile 行、監査 correct、P2 3 件の fix round U227c 実行中)、PR 687(dsh-srt 起動 lever、監査実行中) | route と profile は動作、PR 3 本が merge 待ち | tests/dsh-login-route.tsv、PR 679 686 687 |
| dsh-superagent が Slack/Outlook/Teams/GitHub の受付 | 未着手(M-26、M-27、M-18) | 未着手 | units.tsv に行なし |
| 全体が Anthropic sandbox の中 | omp 席は srt 下。DSH 用 launcher `dsh-srt`(U251、PR 687)が worker 席と同じ deny と domain list で dsh を srt 下に起動(実測: version、dump-config、canary、~/.ssh への書き込み拒否)。login 子プロセスの omp profile 読み取り行が残課題(U251 の finding) | lever は PR 待ち、実 login turn under srt は次 | PR 687 |
| graphify を統合(Understand-Anything から置換) | U224 PR 673、監査 round 4 で correct、sweep 済み、thread 0。CI の server leg 待ち | PR 待ち | `gh pr checks 673` |
| security skill を必須に | 全 unit に sweep 行(本日 10 本以上)。PRD は全 unit に修正済み。pr-merge.sh の gate 拡張は PR 680(監査 2 round correct、sweep 済み、CI は server leg のみ赤)。brief-check に CI gate 必須の規則を入れる U249 は PR 683(監査 correct、sweep 0 件) | 運用と文書は達成、lever 2 本が PR 待ち | PR 680 683 |
| e2e を e2e 検証時に必須に | 未着手(M-16 は「案件が無い」で blocked のまま) | 未着手 | plan INDEX M-16 |
| knowledge-work を DSH と omp の統合から呼べる | kwp skill は `~/.agents/skills/kwp-*`。DSH は既定で `~/.agents/skills` を読む(pinned source で確認)。実 turn での一覧は route 待ち | 一部 | `ls ~/.agents/skills | grep kwp` |
| 両ホストで他プロジェクトの開発を自律駆動 | server bootstrap leg の停止は原因特定: `install/ubuntu/server/setup_timezone.sh` が `/etc/localtime` を差し替えると runner 上で以後の出力が止まる(probe 681〜690 の二分で確定、機構は runner 側の推定)。修正 U254(runner 上と設定済みの時は変更しない)を実装中。これが main に入るまで全 PR の merge が止まっている | blocker 特定済み、修正 PR 待ち | decisions の ci 行(07:21Z〜08:14Z)、PR 681 685 690 |

本日 landed: U234(676)、U241(678)。PR 待ち: 673、674、680、683、686、687、679(すべて server leg の停止で merge 不可、U254 が解く)。probe(merge しない): 677、681、682、684、685、688、689、690。

## 2. 残す、変える、捨てる、新規(ゴールから逆算)

**残す。** omp 席と srt、hcom-seat、監査ゲート(`pr-audit.sh`、`pr-merge.sh`、ledger)、manifest 単一ソース、kwp skill の移植、security-audit skill の asset、両ホストの配備経路。

**変える。**
- ADR-009 を「proposed」から操作者決定の目標アーキテクチャにする。ADR-006 の「任意の第 4 席 vendor」「設計読み物」を書き直す。受入条件(R-52)は測定項目として残す。
- M-13 の結論。操作者の指示「graphify は Understand-Anything から置き換え」が決定。M-20 を開く。
- security sweep の適用範囲を「全 unit 必須」に戻す(PRD R-48、AGENTS.md の sweep 規則)。
- e2e を kit の必須 asset にし、e2e 検証を行う unit と案件で必須にする(PRD R-50、M-16 の blocked を解く)。
- 席の GitHub identity。ADR-009 の専用アカウント(M-25)に一本化し、U88 を M-25 に畳む。

**捨てる。** plan 025 v14(G3 を superseded で閉じる)。lever 磨きの unit(U215 から U222 の store move は「自律駆動」に要るので残すが、Phase 6 の後ろ)。Phase R の残骸整理は records-only 1 unit にまとめる。

**新規。** 無し。Phase 6 の M-21 から M-28 が既に操作者承認の計画にあり、未着手なだけ。

## 3. 順序(critical path)と担当

| 順 | 作業 | 担当 | 完了の証拠 |
| --- | --- | --- | --- |
| 1 | DSH を pin で導入(M-14 task 20、`update_deepseek_harness` 単独実行) | coordinator(第 30 条) | `~/.dsh/bin/dsh --version` が pin と一致 |
| 2 | M-21 spike。DSH を srt 下で 1 turn、canary、agentsHome | poteto-agent | decisions 行 3 本(canary、started/refused、agentsHome) |
| 3 | M-22 spike。dsh-subagent-acp が srt 下の `omp acp` を駆動 | poteto-agent | launch.log に canary 行の後に omp acp 開始行 |
| 4 | M-20 graphify 置換(M-13 行を操作者決定で上書き) | poteto-agent | Understand-Anything の asset、plugin、audience 行が消え、graphify が manifest の asset |
| 5 | PRD/ADR の修正(ADR-009 採用、security 全 unit、e2e 必須、identity を M-25 に) | coordinator | `check.py` pass、kit trail に design 行 |
| 6 | M-24 ACP seat shim lever | poteto-agent | R-44、R-45 の scenario が holds-today |
| 7 | M-25 専用 GitHub アカウントと branch protection | 操作者(アカウント作成)+ coordinator(doctor 行) | `mergedBy` が専用アカウントでない、seat token が merge 権を持たない |
| 8 | M-26 superagent fork、GitHub Source observe、Router を srt 下 | poteto-agent | would-accept 行が記録される |
| 9 | M-18 accept ladder、M-27 Slack 先行(Teams/Outlook は tenant 登録後) | poteto-agent + 操作者(tenant) | Source ごとの受付行 |
| 10 | Ubuntu で席を実走(M-10)。G-26 の doctor 3 項目 | 操作者(host step)+ coordinator | <redacted> に seats root と store、doctor exit 0 |

1 から 10 が Build。操作者の指示(2026-11-06、第 41 条)により、Build のあとは一度きりの受入ではなく、試験と修正のサイクルで完成を判定する。

**Verify-and-fix cycle(第 41 条)。**

1. ユースケースの導出。各コンポーネントの公式ドキュメント(omp、srt、DSH、dsh-superagent、graphify、security-audit-skill、e2e、knowledge-work-plugins、hcom、GitHub ruleset と Actions)と、dotfiles の趣旨と意図(README、AGENTS.md、manifest)からユースケースを書き出す。1 ユースケース 1 ファイル、store の `tests/` 配下。
2. 試験項目。各ユースケースを複数の側面(正常系、拒否系、境界、両ホスト、人手ゼロ)から覆う項目に分ける。項目ごとに実行コマンドと期待出力を書く。
3. 判定。項目を実行し、貼り付けた出力で OK か NG を記録する。
4. 修正。NG は fix unit になり、通常の loop(brief、席、監査、merge)で landed にする。
5. 再判定。全項目 OK になるまで 3 と 4 を繰り返す。ゴール文の最後の節「両ホストで他プロジェクトの開発を自律駆動する」は、他プロジェクトの 1 変更が受付から merge まで人手なしに流れるユースケースとしてこの表に入り、他の項目と同じく OK/NG で判定する。

## 4. 操作者だけができること

- M-25 の専用 GitHub アカウントの作成(fine-grained token、merge 権なし)。
- M-27 の Microsoft tenant app 登録。
- Ubuntu での sudo を要する host step と G-26 の 3 項目。
- Router の model route は操作者判断(2026-11-06)で login 経由のみ。PRD open question 15 は回答済み(U242)。

手順書は各 unit の着手時に 1 枚ずつ出す。
