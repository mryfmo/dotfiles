# 停止と再計画(操作者指示 2026-11-07 06:44Z: 「一旦、すべて停止して真の目的とゴールを思い出し、現在地を確認したうえで、最速で実装し、試験で問題を潰す計画をたてること」)

## 1. 真の目的とゴール(08-purpose-and-goal.md §0、一字も変えない)

> omp を最下層に、DSH がワークフロー制御、dsh-superagent が Slack/Outlook/Teams/GitHub の受付、全体が Anthropic sandbox の中で動く。graphify、security skill、e2e、knowledge-work を統合した TechnoPro Agent Harness Kit として完成し、両ホストで他プロジェクトの開発を自律駆動する。

完成の判定は第 41 条の試験表(store の `tests/*.tsv`)で、macOS で全行 OK、次に Ubuntu で同じ表が全行 OK(第 47 条)。

## 2. 現在地(実測 2026-11-07T06:44Z)

| 要素 | main にあるもの | 無いもの |
| --- | --- | --- |
| omp 最下層、srt 下の席 | 席、login 経路(U312、U318、U318b)、両ホストの `make update` 済(操作者報告、macOS は実測) | Ubuntu の seats root と store(行 11) |
| DSH がワークフロー制御 | dsh role(U272)、gateway 転送(U306)、harness build を srt 下で(U322、49f3c33c) | dsh role の omp profile provision(PR 708、U310、round 6 の head b2ba1204、main と競合中) |
| dsh-superagent の受付 | router role(U321、0249e534) | superagent asset と GitHub Source observe(PR 711、U317、main と競合中)、Router を srt 下で実走(stage B)、M-25 の account、M-18 の ladder 行、M-27 の Slack/Teams/Outlook |
| 全体が sandbox の中 | 席、dsh、harness build が srt 下 | M-24 の ACP seat shim(U343 が f1e356c9 をコミット済、PR 未)、U344(router 行が broker を起動) |
| graphify | 着地、laptop 退役済 | g14、g15 の操作者 2 行(trial-install、code-only) |
| security skill 必須 | gate 全 unit 化、sweep 全 unit | 無し(表 17 行 OK) |
| e2e | 無し | 他プロジェクトが案件を名指すまで pending(e2 から e9) |
| knowledge-work | kwp skill は `~/.agents/skills` | 実 turn での一覧は dsh の login route 待ち(g4 から g7) |
| 他プロジェクトの自律駆動 | 自律変更フロー 22/26 OK | f1 intake、f24 dedicated-account、f25 zero-touch-ladder、f26 seat-takes-task-live |

試験表: 10 表 215 行、OK 184、NG 1(g6: dsh role 下の実 turn で bridge route が 404、PR 708 が直す)、pending 30(上の「無いもの」に対応)。

開いている PR: 708(U310)、711(U317)、675(U227、保留、第 42 条)、626(dependabot)。走っていた worker 3 本(U310g、U317c、U343)は 06:44Z に停止指示、それぞれ一貫した head で止まる。

## 3. 最速の実装順(Build。第 49 条: head ごとに監査 1、掃討 1、CI を同時、揃った最初の head でマージ、修正ラウンド無し)

着地順は「他と重なるファイルが多い順」。重なりは hcom-seat(708)、updater(711)、manifest の pin 行(全部)。pin 行は手で merge せず `generate-agent-configs.py` で再生成する。

| 波 | 単位 | 内容 | 前提 | 完了の証拠 |
| --- | --- | --- | --- | --- |
| A1 | U310g → PR 708 | main 49f3c33c を merge、監査 1、掃討 1、CI、マージ、`make deploy-kit` | 無し | 708 merged、g6 が OK |
| A2 | U317c → PR 711 | main を merge、`/tmpdir` 改名、監査 1、掃討 1、CI、マージ | 無し(708 の後に main をもう一度 merge) | 711 merged、i2 の前提 |
| A3 | U343 → 新 PR | f1e356c9 を PR に、監査 1、掃討 1、CI、マージ。実 srt での scratch 計測は PR 前に待たず、着地後に s21 の表行で判定 | 無し | PR merged、s20 と s21 が OK |
| B1 | U344 | router 行が broker を起動、settings writer を一本化、R-44 と R-32 の scenario | A1、A3 | o20、s21 が OK |
| B2 | M-26 stage B | Router を `hcom-seat router` で srt 下に実走、GitHub Source observe、would-accept 行 | A2、U321(済) | i2、i3 が OK |
| B3 | M-18 | ladder の最初の行(off → observe)を records で | B2 | i6、f25 が OK |
| B4 | dsh login route | 708 配備後に g4、g5、g7 を表のコマンドで判定 | A1 配備 | g4 から g7 が OK |
| C(操作者、並行) | M-25 | account 作成と main の push 制限(handouts/m25-agent-github-account.md) | 無し、今から | f24 が OK |
| C(操作者、B2 の後) | M-27 Slack | Slack app と token を Router の資格情報ルートへ | B2 | i4 が OK |
| D | 行 10 | 残る pending を表のコマンドで判定、NG は fix unit(監査 1) | A から C | macOS 列 全行 OK(e2 から e9 と i5、i9 は案件と tenant 待ちとして表に残す) |
| E | 行 11 | Ubuntu: seats root、store、doctor(host step の handout 1 枚)、同じ表を実行 | D | Ubuntu 列 全行 OK |

## 4. 試験で問題を潰す(Fix。第 41 条の 3 から 5)

1. 着地と配備のたびに `python3 -I tests/check-tables.py tests/*.tsv` を回し、その単位が解くはずの行を表のコマンドで実行し、貼り付けた出力で OK か NG を書く。
2. NG 1 行が fix unit 1 本。brief は NG 行の command と expected をそのまま ACCEPTANCE にする。監査は 1 回、掃討は 1 回、修正ラウンドは無し(第 49 条)。
3. 監査の P0 と P1 だけは再現テスト 1 本で直す。P2 以下と filed は residual 行。
4. 操作者に渡すのは一回の行為だけ(第 48 条): M-25 の 2 手順、Slack の app、Ubuntu の host step、他プロジェクトの案件名(e2e)。

## 5. やらないこと

- 行 6 から 11 の外の unit、handout、調査。U333(docs を test で読む)は捨てる。
- 本文だけ、docs だけの指摘へのラウンド。
- main との競合の再 merge を減らすため、PR は上の順で一本ずつ着地し、次の PR は着地直後に main を一度だけ merge する。

## 6. 見積り(推測)

A の 3 本は監査 7 分、掃討 6 分、CI 約 20 分が並列で、merge は順番なので約 1 時間半。B は U344 と stage B が並列で約 2 時間。D と E は NG の数次第。
