# 目的とゴール(操作者確定、2026-11-06)

操作者が 2026-11-06 に確定したゴール。これ以外のゴールは無い。一字も変えない。

> omp を最下層に、DSH がワークフロー制御、dsh-superagent が Slack/Outlook/Teams/GitHub の受付、全体が Anthropic sandbox の中で動く。graphify、security skill、e2e、knowledge-work を統合した TechnoPro Agent Harness Kit として完成し、両ホストで他プロジェクトの開発を自律駆動する。

出典は操作者の言葉 2026-11-02 21:18Z(六点)、21:27Z と 21:37Z(三層と sandbox)、11-06 03:2xZ(上の一文を「目的とゴールはこれしかない」と確定)。

この文書の前版(同日 06:xxZ)は coordinator が自分で作った完了条件を目的として書いた誤りだった。前版の §2「提案する完了条件」と §8「ADR-009 は後の別判断」は撤回する。

## 1. ゴールの要素と今日の距離(実測、2026-11-06T18:45Z 更新)

| ゴールの要素 | 今日(実測) | 距離 | 確認コマンド |
| --- | --- | --- | --- |
| omp が最下層で agent、tool、skill の呼び出しを担う | omp 席は srt 下で動く(U85)。macOS のみ。Ubuntu に席も store も無し | 片側達成 | `hcom list -v`(ラップトップ)、`ssh <redacted> ls ~/.local/state/omp-seats`(無し) |
| DSH がワークフロー制御 | adapter plugin(PR 679)、thak profile 行(PR 686、703: API key 行を全て disabled)が main と laptop に到達。DSH は manifest の model で claude-bridge route を使い、API key 行も Ollama 行も無い(d20 実測 OK)。srt 起動は hcom-seat の `dsh` role(U272、PR 697、6 round の監査、laptop に配備済み)。kit の Claude Code hook は bridge 下では設計上走らない(U298 実測、coverage 表を修正) | route、profile、封じ込め lever が main と laptop に到達。role 下の実 login turn が次 | `hcom list -v`、`tests/dsh-workflow-turn.tsv` |
| dsh-superagent が Slack/Outlook/Teams/GitHub の受付 | 未着手(M-26、M-27、M-18) | 未着手 | units.tsv に行なし |
| 全体が Anthropic sandbox の中 | omp 席は srt 下。DSH は hcom-seat の `dsh` role で srt 下に起動(PR 697、laptop に配備済み): per-launch slot、git/hcom/records の物理 path を deny、rendered grant 全件を rendered deny 全件と照合する refusal。実測: store、common dir、records、~/.aws、~/.omp/profiles が拒否、--version 0.2.1-rc.5。残差: lever が計算しない git directory | laptop は lever 到達、role 下の実 login turn が次。Ubuntu 未 | `tests/sandbox-write-denies.tsv` |
| graphify を統合(Understand-Anything から置換) | U224 PR 673 が main に到達。laptop では 15:12Z に `retire_understand_anything`(updater の single-step)で plugin を退役済み(`claude plugin list` に無いことを実測) | laptop 達成、Ubuntu 未 | `git log origin/main --oneline -- home/dot_agents/agent-config.yaml` |
| security skill を必須に | pr-merge.sh の gate 全 unit 化(U244、PR 680、8f31cf5c)と brief-check の CI gate 必須(U249、PR 683、386a01c5)が main に到達。hcom-orchestration skill も全 unit sweep に修正済み | lever は main、配備は次回 make update | `git log origin/main --oneline` |
| e2e を e2e 検証時に必須に | 未着手(M-16 は「案件が無い」で blocked のまま) | 未着手 | plan INDEX M-16 |
| knowledge-work を DSH と omp の統合から呼べる | kwp skill は `~/.agents/skills/kwp-*`。DSH は既定で `~/.agents/skills` を読む(pinned source で確認)。実 turn での一覧は route 待ち | 一部 | `ls ~/.agents/skills | grep kwp` |
| 両ホストで他プロジェクトの開発を自律駆動 | 本日 main に入った unit: U234、U234b、U241、U254、U224、U226、U240 系、U249、U227 系、U244、records sync 45。開いている PR: 696(U241c、監査 correct、CI 待ち)、697(U272 hcom-seat の dsh role、監査中)、698(U276 `make deploy-kit`、監査中)。試験表(第 41 条、第 47 条): `tests/` に 9 表(U274)。配備(deploy-kit 3 回、updater の single-step 2 回)と表の修正(U290)の後、OK 128、NG 1(f23 = ruleset の操作者 handout)。d22 は U298 の測定で期待値を実測値(kit の hook は bridge 下では設計上 inactive)に直して OK、pending 27 は operator 行と未着手行。§3 の順序 3 以降(M-22、M-24 から M-27、M-10)は未着手 | Build の順序 1 から 2 まで。試験表あり。配備待ち | `gh pr list --state open`、`python3 -I .orchestration/orchestrate/regime-cutover/tests/check-tables.py .orchestration/orchestrate/regime-cutover/tests/*.tsv` |

本日 landed: 676、678、691、673、674、679、694、683、686、680、695、696、698、699、700、702、701、704、705、703、697(U272、6 round、mechanism change 1 回)。開いている PR: 無し。撤回: 687。follow-up(予約): U240d、U227d、U244b、U254b、U283d、U280c、U301。

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
| 10 | macOS で Verify-and-fix cycle(下記)を全項目 OK にする | coordinator + poteto-agent | `tests/*.tsv` の全行 verdict=OK(macOS 列) |
| 11 | Ubuntu で席を実走(M-10)。G-26 の doctor 3 項目。macOS で OK になった同じ試験表を Ubuntu で実行 | 操作者(host step)+ coordinator | <redacted> に seats root と store、doctor exit 0、同じ表の Ubuntu 列が全行 OK |

1 から 9 が macOS 上の Build。操作者の指示(2026-11-06、第 41 条と第 47 条)により、Build のあとは一度きりの受入ではなく、試験と修正のサイクルで完成を判定し、そのサイクルは macOS で先に全項目 OK にしてから、同じ試験表を Ubuntu で実行する(10 と 11)。試験表は Build を待たずに今から書き始め、main に入った要素から順に macOS で判定する。未 Build の要素(superagent、e2e)は「未着手」行として表に載せ、Build が landed になった時点で判定に変わる。

**Verify-and-fix cycle(第 41 条)。**

1. ユースケースの導出。各コンポーネントの公式ドキュメント(omp、srt、DSH、dsh-superagent、graphify、security-audit-skill、e2e、knowledge-work-plugins、hcom、GitHub ruleset と Actions)と、dotfiles の趣旨と意図(README、AGENTS.md、manifest)からユースケースを書き出す。1 ユースケース 1 ファイル、store の `tests/` 配下。
2. 試験項目。各ユースケースを複数の側面(正常系、拒否系、境界、両ホスト、人手ゼロ)から覆う項目に分ける。項目ごとに実行コマンドと期待出力を書く。
3. 判定。項目を実行し、貼り付けた出力で OK か NG を記録する。
4. 修正。NG は fix unit になり、通常の loop(brief、席、監査、merge)で landed にする。
5. 再判定。全項目 OK になるまで 3 と 4 を繰り返す。ゴール文の最後の節「両ホストで他プロジェクトの開発を自律駆動する」は、他プロジェクトの 1 変更が受付から merge まで人手なしに流れるユースケースとしてこの表に入り、他の項目と同じく OK/NG で判定する。

## 4. 人間の作業(第 48 条: agent でできる部分は agent、人間は一回の行為だけ)

| 項目 | agent がやる部分 | 人間にしかできない部分 | 回数 | 状態 |
| --- | --- | --- | --- | --- |
| macOS への配備 | `make deploy-kit`(U276、PR 698 merged、kit の path だけを chezmoi apply、二側 drift は拒否)を merge 後に coordinator が実行し、適用一覧を記録。初回 13:33Z に 39 target を適用(understand-* skill 退役、omp-gateway plugin、thak profile、brief-check、pr-merge)、Codex と Claude の設定は無変更(digest 実測)。退役 target の verify で exit 2 になる欠陥は U276d が修正中 | 無し。`make update`(tool upgrade、private source、herdr reload)は操作者の任意の定期作業に格下げ | 毎 merge(agent) | 稼働(exit code の修正待ち) |
| G-26 の 3 項目(laptop doctor) | (1) 操作者の live Codex allow rules と notify 行を source に取り込む PR、(2) 未 pin の Claude Code plugin を manifest に pin する PR | (3) `make gh-auth`(gh の login を OS keyring から gh のファイルへ移す。credential の移動は第 30 条で人間) | 一回 | 未着手(U277 予定) |
| G1 Claude login(bridge 子プロセス) | 必要になった時に正確なコマンドを handout に書き、実行後に PONG を測って確認 | ブラウザで login する | token 失効ごと | PASSED 2026-10-23 |
| M-25 専用 GitHub アカウント | 権限一覧、fine-grained token の scope、branch protection の設定値を handout に書く。作成後に `gh api` で権限と merge 権の不在を検証 | アカウント作成(規約同意、メール認証、2FA)と token 発行 | 一回 | 未着手 |
| M-27 Microsoft tenant app | app registration の manifest JSON と redirect URI を生成。登録後に token 取得を検証 | tenant への登録と admin consent | 一回 | 未着手 |
| Ubuntu host step(M-10、G-26 相当) | sudo 不要の全手順を ssh 経由で実行(seats root、store、doctor)。sudo が要る手順は一つの冪等 script にまとめる | その script を `sudo` で一回実行。操作者が望めばその script だけの NOPASSWD 行を一回入れると以後の host step は全て agent(安全性の trade-off は操作者判断、既定は入れない) | 一回(以後 agent) | 未着手 |
| Router の model route | 決定済み(login 経由のみ、U242) | 無し | 済 | 済 |
| main の ruleset に pull_request rule(f23) | 測定と handout(`handouts/ruleset-pull-request-rule.md`、承認 0 件の形) | ruleset の編集一回 | 一回 | handout 済、未実施 |

手順書は各項目の着手時に 1 枚ずつ出す。1 枚に書くのは、人間が打つコマンドか押す場所、期待する結果、agent が実行後に走らせる検証コマンド、の三つだけ。
