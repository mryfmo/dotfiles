# Plan 024 再計画: install-ppa-resilience a02（2026-10-22 06:5x UTC、INV-6 reset による設計差し戻し）

> 経緯: `dotfiles-T133-install-ppa-resilience-a01`（PR #454）は RESULT 4 回すべてに所見が付き、plan 006 S2（INV-6: revise 2 回で停止し「著者以外の文脈」が設計に戻す）で停止した。この文書は a01 の著者（orchestrator 席）とは別の計画文脈が書く。本文（task text）は書かず、コードも触らない。
> 表記: 時刻は UTC。数値には観測日時・対象 head・コマンド・保存先を付け、保存のない値は「未検証」と書く。home path は `~`、利用者名は `<user>`。
> 対象: PR #454 最終 head `460b91a5de63719e1cf45447442e506bafca676e`（`git -C .claude/worktrees/orchestrator-review rev-parse HEAD`、06:35Z）、merge-base `d06d94fd`。差分 `git diff --numstat d06d94fd..460b91a5`（06:35Z）: `install/ubuntu/client/ghostty.sh` +47/−4、`tests/install/ubuntu/client/ghostty.bats` +157/−2、`run_after_06-client-install-ghostty.sh.tmpl` +13、`run_once_50-client-install-misc.sh.tmpl` −3、記録 9 ファイル。以下の `file:line` はすべてこの head のもの。

## 1. 問題の記述

4 ラウンドの所見を類型で並べると、1 つの設計判断「`apt-get update`/`install` の診断文を分類して PPA 単独障害を見分ける」（`ghostty.sh:52-66` `ppa_step`）の症状が 6 類型、その判断を置いた「位置」の症状が 3 類型になる。記録は `.orchestration/acceptance/dotfiles-T133-install-ppa-resilience-a01.md` の行 id。

| 類型 | 行 id | 何が起きたか（head とその行） |
| --- | --- | --- |
| apt-update-exit-zero-outage | audit:44134e3:1、local:44134e3:1 | 44134e3 は exit 100 だけを見た。実際の 503 では `apt-get update` は `W: Failed to fetch … 503` と `W: Some index files failed to download` を出して exit 0 だった（job 119482260780 の log 2744-2745 行、`gh run view --job 119482260780 --log`、06:47Z 取得、保存先なし（再実行可）） |
| mixed-fetch-failure-fatal | audit:44134e3:2、local:44134e3:3 | Launchpad の fetch 行が 1 行あれば全体を成功にした |
| non-fetch-error-masking | audit:e6b645f:1、local:e6b645f:2 | fetch 行だけを見るので hook 失敗や `E:` を隠した。460b91a5 は `ghostty.sh:61` の catch-all で塞ぐ |
| per-URL versus summary forms | local:059a40c:1（P1） | apt は per-URL 行と summary 行（`E: Unable to fetch some archives`）の両方を出す。`ghostty.sh:60` に summary の列挙を追加 |
| locale | local:059a40c:3 | 翻訳された診断文は一致しない。`ghostty.sh:54` に `LC_ALL=C LANG=C` |
| dpkg-status-semantics | audit:e6b645f:2、local:e6b645f:1 | `dpkg -s` の exit は導入完了ではない。`ghostty.sh:75` を `db:Status-Status` に |
| retry-after-skip | audit:44134e3:3、local:44134e3:2 | 呼び出し元が `run_once_` で、skip 成功後は再実行されない。`run_after_06` へ移動 |
| dependency-phase refresh ordering | audit:460b91a:1、local:460b91a:1 | `ghostty.sh:32` の無条件 `apt-get update` は PPA を含む全ソースを `ppa_step` の外で更新する。PPA 設定済みの既存機では障害が `set -e`（`ghostty.sh:13`）で retry 行なしに落ちうる |
| chezmoi run_once ordering | audit:460b91a:2、local:460b91a:2 | misc の `run_once_` は内容が変わったので既存機で再実行されるが、先行していた ghostty の refresh が消え、`misc.sh:34` は update なしで `apt-get install` する |
| （規程）in-scope-revise-deferral、evidence-verbatim、INV-6 | audit:44134e3:4-5、audit:e6b645f:3-4、audit:460b91a:3 | orchestrator 側。本計画の対象外（第 7 節 J-6） |

診断文分類の 6 類型は、各ラウンドで分類器に規則を 1 つ足すたびに次の抜けが見つかる形で現れた（44134e3 → e6b645f → 059a40c → 460b91a、`ghostty.bats:13-51` の FAIL モードは update/pool/archive から warn/mixed/otherppa/hook/summary/locale へ増えた）。分類器の網羅性には上限がない（apt の文言は版と翻訳で変わる）ので、これは実装の欠陥ではなく設計の欠陥である。

## 2. 根本原因

- 仕様（a01 本文 Item 1、`.orchestration/tasks/dotfiles-T133-install-ppa-resilience-a01.md:41`）: 「PPA が到達不能なら skip して exit 0、他の失敗は従来どおり失敗」を「apt exit 100 with a fetch failure for the PPA host」と、apt の出力文で定義した。約束（利用者から見える振る舞い）と手段（出力文の分類）を同じ文で書いたため、以後の amendment 3〜5 はすべて手段の修繕になった。
- 設計: 「1 回の system-wide `apt-get update` の結果から PPA の失敗を切り出せる」と仮定した。apt は複数ソースの失敗を 1 つの exit code にまとめるので、ソースを混ぜた時点で exit code では帰属できず、文の分類が必然になった。さらに PPA を system-wide の sources に加えたまま（`ghostty.sh:40` は `add-apt-repository -y`、`-n` なし）、自分の依存段階（`ghostty.sh:32`）も他スクリプトも PPA を含めて refresh する位置関係を設計しなかった。
- 実装: `ppa_step`（`ghostty.sh:52-66`）は出力を 1 行ずつ `case` で分類し、`[EW]: Failed to fetch <PPA>`（58 行）、`Err:`（59 行）、summary（60 行）、catch-all（61 行）を持つ。`LC_ALL=C` は sudo の env_check に依存する（48-49 行のコメント）。これは apt の内部文言への結合で、apt 側の変更で黙って壊れる。
- 検証: fixture は apt の出力文を模倣する（`ghostty.bats:23-47`）ので、「分類器が fixture の文を分類できる」ことしか示せない。最初の fixture `update`（23 行）は `E: … 503` と exit 100 を返すが、実 CI では同じ 503 が `W:` と exit 0 だった（第 1 節 1 行目）。つまり fixture が apt の実際の振る舞いと食い違っても検証は緑になる。live test（`ghostty.bats:85-98`）は 8 回の CI すべてで「the PPA answered」分岐だった（validation.md 16, 37, 82, 111, 132, 159, 182, 211 行）ので、障害経路は実機で一度も通っていない。

結論: 根本原因は「apt の診断文を分類して障害を帰属する」設計である。exit code だけで帰属できる設計は apt の文書化された interface で組める（第 3 節）。

## 3. 公式ドキュメントに基づく本質的な方法

原則: **帰属はコマンドの範囲（scope）で決め、文は読まない。** 「PPA しか触らないコマンド」が失敗したら PPA の障害、「ローカルしか触らないコマンド」が失敗したら致命。apt にはそのための設定項目がある。

### 3.1 根拠（引用。fetched_at は `date -u`）

1. apt-get(8) `https://manpages.debian.org/trixie/apt/apt-get.8.en.html`（2026-10-22T06:38Z、06:45Z）
   - 「apt-get returns zero on normal operation, decimal 100 on error.」
   - `--no-list-cleanup`: 「This option is on by default; use --no-list-cleanup to turn it off. When it is on, apt-get will automatically manage the contents of /var/lib/apt/lists to ensure that obsolete files are erased. The only reason to turn it off is if you frequently change your sources list. Configuration Item: APT::Get::List-Cleanup.」
   - `-d, --download-only`: 「Download only; package files are only retrieved, not unpacked or installed. Configuration Item: APT::Get::Download-Only.」
   - `--no-download`: 「Disables downloading of packages. This is best used with --ignore-missing to force APT to use only the .debs it has already downloaded. Configuration Item: APT::Get::Download.」
   - FILES: 「Configuration Item: Dir::Etc::SourceList.」「Configuration Item: Dir::Etc::SourceParts.」
2. apt.conf(5) `https://manpages.debian.org/trixie/apt/apt.conf.5.en.html`、`https://manpages.ubuntu.com/manpages/noble/en/man5/apt.conf.5.html`（06:38Z、06:45Z）
   - 「All of the APT tools take an -o option which allows an arbitrary configuration directive to be specified on the command line.」
   - Dir: 「sourcelist gives the location of the sourcelist and main is the default configuration file」
   - Acquire::Retries: 「Number of retries to perform. If this is non-zero APT will retry failed files the given number of times.」（既定値の記載なし。noble の既定は未検証: a02 の CI で `apt-config dump | grep -i retries` を貼る）
   - `APT::Update::Error-Mode` は両ページに**ない**（検索結果「Error-Mode absent」）。apt のソースで補う（4）。
3. sources.list(5) `https://manpages.debian.org/trixie/apt/sources.list.5.en.html`（06:38Z、06:45Z）
   - deb822 `Enabled`: 「…it is usually easier to add the field "Enabled: no" to the stanza to disable the entry.」「Removing the field or setting it to yes re-enables it.」（前半は文の途中からの引用）
   - 「Filenames need to have either the extension .list or .sources depending on the contained format.」
4. apt ソース `https://raw.githubusercontent.com/Debian/apt/main/apt-pkg/update.cc`（06:45Z、06:47Z）、`…/apt-pkg/sourcelist.cc`（06:45Z）、`…/methods/basehttp.cc`（06:47Z）
   - update.cc: `std::string errorModeS = _config->Find("APT::Update::Error-Mode", "persistent");` … `else if (errorModeS == "any") errorMode = ErrorMode::Any;`
   - update.cc: `case pkgAcquire::Item::StatTransientNetworkError: if (errorMode == ErrorMode::Any) Failed = true; else TransientNetworkFailure = true;` … `else if (TransientNetworkFailure == true) Res = _error->Warning(_("Some index files failed to download. …")); else if (Failed == true) Res = _error->Error(…)`
   - basehttp.cc: `constexpr unsigned int TransientCodes[] = { 500, … 502, … 503, // Service Unavailable … 599 }` → `Fail(true)`。つまり既定では 503 は Warning で exit 0（第 1 節の CI log と一致）、`Error-Mode=any` では Error で exit 100。
   - sourcelist.cc: `string Main = _config->FindFile("Dir::Etc::sourcelist", "/dev/null"); string Parts = _config->FindDir("Dir::Etc::sourceparts", "/dev/null");` と `bool pkgSourceList::ReadAppend(string const &File) { if (flExtension(File) == "sources") return ParseFileDeb822(File); else return ParseFileOldStyle(File); }` → `.sources`（deb822）1 ファイルを `Dir::Etc::sourcelist` に渡せる。
5. add-apt-repository(1) `https://manpages.ubuntu.com/manpages/noble/en/man1/add-apt-repository.1.html`（06:38Z、06:45Z）
   - 「add-apt-repository is a script which adds an external APT repository to either /etc/apt/sources.list or a file in /etc/apt/sources.list.d/ or removes an already existing repository.」
   - `-n, --no-update`: 「After adding the repository, do not update the package cache.」 `-y, --yes`: 「Assume yes to all queries.」
   - `-r, --remove`: 「Remove the specified repository. This first will disable (comment out) the matching line(s), and then any modified file(s) under sources.list.d/ will be removed if they contain only empty and commented lines.」
   - 書くファイル名は記載なし（未検証: a02 の CI で `ls /etc/apt/sources.list.d` を貼る）。
6. chezmoi `https://www.chezmoi.io/reference/application-order/`、`https://www.chezmoi.io/user-guide/use-scripts-to-perform-actions/`、`https://www.chezmoi.io/reference/source-state-attributes/`（06:38Z）
   - 「Run `run_before_` scripts in alphabetical order.」「Update entries in the target state (files, directories, externals, scripts, symlinks, etc.) in alphabetical order of their target name.」「Run `run_after_` scripts in alphabetical order.」
   - `run_`: 「These scripts are executed every time you run `chezmoi apply`.」 `run_once_`: 「These scripts are executed once for each unique version of the content.」「the script will not run again unless the content itself changes.」 `run_onchange_`: 「These scripts are only executed if their content has changed since the last time they were run successfully.」
   - 「scripts in this directory are executed as normal scripts, without creating a corresponding directory in the target state.」（`.chezmoiscripts`）

### 3.2 方法（exit code だけで帰属する）

1. 冪等: `dpkg-query -W -f '${db:Status-Status}'` が `installed` なら何もせず 0（a01 の `ghostty.sh:75` を踏襲。`dependencies.sh:65-66` と同じ考え）。
2. 依存段階は条件付き: `software-properties-common` が `installed` でないときだけ、従来どおり system-wide `apt-get update` と `install`（致命）。既存機では走らないので、PPA を含む refresh が gate の前に起きない（dependency-phase refresh ordering を根から消す）。
3. PPA の登録は冪等に: `/etc/apt/sources.list.d/*.sources` と `*.list` から PPA の URI を持つファイルを探し、なければ `add-apt-repository -y -n`。`-n` なので add-apt-repository は update しない。失敗（Launchpad API 不達など）は skip + retry 行。登録後も見つからなければ設定異常として致命（障害ではない）。
4. **PPA 限定 refresh = gate**: `apt-get update -o Dir::Etc::sourcelist=<そのファイル> -o Dir::Etc::sourceparts=- -o APT::Get::List-Cleanup=0 -o APT::Update::Error-Mode=any`。読むソースはこの 1 ファイルだけなので、非 0 はその PPA の index が得られなかったことを意味し、文を読む必要がない。`Error-Mode=any` で transient（503、DNS、オフライン）も exit 100 になる。`List-Cleanup=0` がないと他ソースの lists が消える（引用 1）。非 0 → skip + retry 行、exit 0。
5. gate 通過後だけ従来の system-wide `apt-get update`（main の `ghostty.sh:44` と同じ位置、従来どおり致命）。障害中はここに来ない。
6. 取得と導入を分ける: `apt-get install -y --download-only ghostty` の非 0 は「取得できなかった」（PPA pool の 503 = #378 の場合、または依存の archive 404）→ skip + retry 行。続く `apt-get install -y --no-download ghostty` はネットワークを使わないので、非 0 は dpkg/ローカルの失敗 → 従来どおり致命。
7. retry 行は段階を名指しし理由は apt の出力に委ねる（例 `ghostty not installed: its PPA index could not be refreshed (apt's output above); the next make update retries`）。文を解釈しないので locale 類型は消える。`LC_ALL=C` は不要。
8. 位置: `run_after_06-client-install-ghostty.sh.tmpl` は a01 のまま（毎 apply、引用 6）。`misc.sh` は自分で `apt-get update` してから install する（`tailscale.sh:40-41`、`docker.sh:68-71` と同形）。隣のスクリプトの副作用に依存しない。

### 3.3 退けた代替案

- 分類器の精緻化（a01 の路線）: 第 1 節のとおり終わりがなく、fixture が apt の実挙動と乖離しても緑になる。
- 障害時に PPA を無効化/削除（`Enabled: no` の書き換え、`add-apt-repository --remove`）: a01 の約束「removes nothing」に反し、再有効化に Launchpad API が要り、`.list`/`.sources` の 2 形式を書き換えることになる。方法 2 と 4 で「gate の前に PPA を含む refresh が起きない」ので不要。他スクリプトの refresh は fresh 機では PPA 登録前の `run_once_`（10 docker、50 misc、53 tailscale）、既存機では `upgrade-tools.sh:477` の `apt-get update || return` で、既定の Error-Mode では 503 は W: で exit 0（引用 4）。残余: 管理者が `APT::Update::Error-Mode any` を設定した機では system-wide refresh が落ちる（従来どおり、threat row に残余として記す）。
- `Acquire::Retries` の明示: Launchpad の障害は時間単位で、retry は遅延させるだけ。既定値が未検証なので a02 では設定せず CI で既定を記録する。
- add-apt-repository を捨てて deb822 と鍵を自前で書く（`docker.sh:53-60` 型）: ファイル名が確定し `software-properties-common` も不要になるが、PPA の鍵指紋の固定は supply-chain 方針（`tests/unit/test_supply_chain_policy.py`）の別設計。a01 本文の「Keep DEPENDENCY_PACKAGES」にも反する。第 7 節 J-4。
- 一本の `apt-get install -y ghostty` の失敗を全部 skip: dpkg のローカル失敗を毎回「retry」と報告し続ける。方法 6 の分割は 1 行の差で約束を守る。
- `apt-get indextargets` で PPA のファイルを特定: 文書は「Detailed documentation is omitted here」で、出力の field を読むことになる。URI による `grep -l` のほうが単純。

## 4. a02 の仕様（atomic items）

共通: 新 task `dotfiles-T133-install-ppa-resilience-a02`、`allowed_files` は a01 の 4 ファイル + `install/ubuntu/client/misc.sh` + `tests/install/ubuntu/client/misc.bats` + 自分の `.orchestration/<id>/**`。fresh branch を main から（第 7 節 J-1）。Caps は a01 本文と同じ「at most 110 changed lines outside `tests/` and `.orchestration/` and at most 160 under `tests/`」（`scripts/orchestrator/regime-ci.py:81` がこの文を読む）。見積り: 外側 ≈ ghostty.sh +45/−6、template 13+3、misc.sh +1 ≈ 68/110。tests ≈ 150/160。含意: fixture は 1 つの `APT_FAKES` と `FAIL` 選択子にまとめ、a01 の文形 fixture 6 本（warn/mixed/otherppa/hook/summary/locale）は分類器とともに消す。gate の引数検査は I-3 の test に同居させ、独立 test を増やさない。misc.bats の追加は 8 行以内。Red/green は a01 と同じく GitHub Actions `test (ubuntu-24.04, client)` の run URL（`scripts/run_unit_test.sh:36`）。

| # | 作業 | 検証条件（selector と fixture） | 検証内容 | 完了条件 | 動かす指標 |
| --- | --- | --- | --- | --- | --- |
| I-1 | `installed <pkg>` ヘルパー（`db:Status-Status`）。`install_ghostty` 冒頭の skip と、依存段階の条件化に使う | `tests/install/ubuntu/client/ghostty.bats::the dependency phase runs only when software-properties-common is absent`、fixture `APT_FAKES` の `SPC`（既定 `installed`）と `STATUS` | `SPC=` 空で `apt-get update` → `install -y software-properties-common` が gate の前に記録される。既定では gate の前に `-o Dir::Etc::sourcelist=` を持たない `apt-get update` が 1 件もない。既存の `an installed ghostty is left as it is`（apt 呼び出し 0）と `a half-configured ghostty is installed, not skipped` を維持 | 3 test 緑、red は main の installer で `SPC` 既定時に system-wide update が記録されること | dependency-phase refresh ordering 類型の行が a02 で 0 |
| I-2 | `GHOSTTY_PPA_URL` で `${APT_SOURCES_DIR:-/etc/apt/sources.list.d}/*.sources *.list` を `grep -lF`。なければ `add-apt-repository -y -n`。失敗 → retry 行で 0。登録後も見つからなければ 1 行出して致命 | `::a failed PPA registration never fails the apply`（`FAIL=ppa-add`: fake が非 0、ファイルを書かない）、`::an existing PPA source is not re-added`（fake の source file を事前作成） | 前者: exit 0、retry 行、`apt-get` は依存段階のみ。後者: `calls.log` に `add-apt-repository` がない | 2 test 緑、red は main の installer | add-apt-repository の内部 update が消える（`-n`） |
| I-3 | gate: `apt-get update -o Dir::Etc::sourcelist=<file> -o Dir::Etc::sourceparts=- -o APT::Get::List-Cleanup=0 -o APT::Update::Error-Mode=any`。非 0 → retry 行で 0 | `::an unreachable PPA never fails the apply`（`FAIL=ppa-update`: fake apt-get は `-o Dir::Etc::sourcelist=` を含む update だけ 100 を返す） | exit 0、retry 行、その update の argv に 4 つの `-o` がある、その後に update/install の記録がない | 緑、red は main（exit 100） | apt-update-exit-zero-outage、mixed、non-fetch、summary、locale の 5 類型が設計上発生しない |
| I-4 | gate 後: 従来の system-wide `apt-get update`（致命）→ `install -y --download-only`（非 0 → retry 行で 0）→ `install -y --no-download`（非 0 → 致命） | `::a failed PPA package download never fails the apply`（`FAIL=download`）、`::a failed local install stays fatal`（`FAIL=install`: `--no-download` が 100）、既存 `::a non-PPA apt failure still fails the apply`（`FAIL=archive`、`SPC=` 空） | download: exit 0、retry 行、`--no-download` 呼び出しなし。install: exit 100、retry 行なし。archive: 非 0、retry 行なし | 3 test 緑、red は main | #378 型（pool のみ 503）が retry 行で終わる |
| I-5 | `misc.sh` `install_misc` に `sudo apt-get update` を 1 行（`tailscale.sh:40-41` と同形） | `tests/install/ubuntu/client/misc.bats::install_misc refreshes the index before installing`（fake `sudo` が `$*` を記録） | 記録の 1 行目が `apt-get update`、2 行目が `apt-get install -y …` | 緑、red は main | chezmoi run_once ordering 類型の行が 0 |
| I-6 | live test `::ghostty` は a01 の分岐のまま、`RETRY_LINE` は前置き `ghostty not installed:` と末尾 `the next make update retries` の 2 部分一致に。構造 test `::the ghostty step is a guarded run_after_ script and the misc run_once_ script no longer includes it` を維持。shdoc（英語）、`bash -n`、`shellcheck`、`shfmt -d` | 上記 2 selector | CI の live 実行で分岐名が出る。どちらの分岐でも exit 0 | 両 test 緑 | required check が Launchpad に依存しない |
| I-7 | 証跡: validation.md に CI live job から `ls /etc/apt/sources.list.d`、gate の apt 出力（`Hit:`/`Get:`/`Err:` 行に PPA host 以外がないこと）、`apt-config dump \| grep -i retries`、分岐行、`dpkg -s ghostty` を貼る。threat table に `APT_SOURCES_DIR`（利用者環境から読む。変えても自分の sudo apt が読むファイルが変わるだけ）、Post-Invoke hook の失敗が gate を落とす残余（Ubuntu 同梱 hook は `\|\| true` で終わる。未検証）、`Error-Mode any` 設定機の残余を行として持つ | — | 実行したコマンドだけを出力付きで | 監査が claims と diff を突き合わせられる | evidence-verbatim の行が 0 |

## 5. STOP 条件

- S1: a02 の PR で同じ類型の所見が 3 回（reviewer・Bot・auditor を問わず）→ 停止。4 回目はしない。この文書の第 2 節を再検討してから再開する。
- S2（INV-6）: revise 2、amendment 2、question 2、RESULT 後 2 head での Bot P0/P1、2 head での audit P0-P1 のいずれかで停止し、a02 の著者以外の文脈が設計に戻す。
- ラウンドの数え方: 最初の RESULT 以後の RESULT はすべて revise として数える（460b91a5 の audit P2(3): 「RESULTs minus one」。Worker Playbook step 15 の fix round と呼んでも閾値は下がらない）。amendment は dispatch 後の本文変更すべて。送信前に `scripts/regime-counters.sh <task>` の出力を記録に貼る。
- 設計の再検討を要する所見（新しい類型で、第 3 節の原則「文を読まない」に反する修正を求めるもの）は 1 件目で止めて操作者に出す。patch で応えない。

## 6. ドリフト点検（a01 の約束と a02 の挙動）

| 場面 | a01 の約束 | a02 でどう満たすか |
| --- | --- | --- |
| index の障害（InRelease 503） | ghostty を skip、retry 行、apply は続く、次の apply で再試行 | I-3 の gate が exit 100 → retry 行、exit 0。`run_after_` なので次の apply が再試行（引用 6） |
| pool だけの障害（#378） | 同上 | I-4 の `--download-only` が非 0 → retry 行、exit 0 |
| 登録時に Launchpad API 不達 | 同上 | I-2 → retry 行、exit 0 |
| 他の失敗は従来どおり致命 | archive の依存導入、dpkg の失敗 | I-1 の依存段階、I-4 の system-wide update と `--no-download` は致命。範囲の原則により「取得」段階の archive 404 は retry 扱い（第 7 節 J-2） |
| 既存機（PPA 設定済み、障害中） | 他の手順は落ちない | 依存段階が走らないので gate まで PPA を含む refresh なし。gate で skip |
| 既存機（misc の `run_once_` が再実行） | misc の導入が落ちない | I-5 で refresh してから install |
| fresh 機 | 全部入る | 順: `run_once_before_50` deps → `run_once_10` docker → `run_once_50` misc（refresh+install）→ … → `run_after_05` zed → `run_after_06` ghostty（依存段階 → 登録 → gate → update → download → install） |
| 導入済み機 | 何もしない | `installed` で即 0。apt 呼び出し 0（ネットワークなし） |
| 半導入（half-configured） | 導入をやり直す | `installed` でないので全段階を通る |
| required check | Launchpad に依存しない | live test はどちらの分岐でも exit 0。fake test はネットワークに触れない |
| removes nothing、PACKAGES/DEPENDENCY_PACKAGES、`sudo --preserve-env`、shdoc | 維持 | 維持（`--remove` は使わない） |

## 7. 操作者判断（各項に推奨既定）

- J-1 PR #454 を close し、a02 を main からの fresh branch で起こす。既定: する。理由: a01 本文は方法ごと置き換わり、#454 の tests cap は 159/160 で尽きている。流用する fixture（packages、live、structural、installed、half-configured、archive）はコピーする。
- J-2 帰属の規則を「host 別」から「段階別」に改める（取得段階の失敗は host を問わず retry、導入段階と依存段階は致命）。既定: 認める。理由: exit code で判定できる唯一の線で、retry 行は段階だけを言い、理由は apt の出力に委ねる。
- J-3 `misc.sh` の refresh 1 行を a02 に含める。既定: 含める。代替は follow-up へ advisory 行で送ること。
- J-4 add-apt-repository を使い続ける。既定: 使い続ける。鍵指紋を固定して deb822 を自前で書く案は supply-chain 方針の別タスク。
- J-5 `APT_SOURCES_DIR` の env 既定を test の seam として認める。既定: 認め、threat row を残余で持つ。代替: fake が `ghostty_source_file` 関数を上書きする（SUT の関数を test が差し替える形で弱い）。
- J-6 記録の処置は orchestrator 側: follow-up stub が持つ local:44134e3:1-3、e6b645f:1-2、059a40c:2-3、460b91a:1-2 は a02 の設計で消えるので a02 の acceptance で supersede、local:45fb80f:1（oracle-is-sut-output）だけ follow-up に残す。460b91a5 の audit P2(3)（INV-6 の数え方）は a01 の記録への処置で、本計画は数え方を第 5 節に採る。
- J-7 席: a01 と同じく Claude 席（Codex 席は push 不可、D-024-36）。audit は `audit` profile。本文は a02 の著者が別に書き、anchor review を 1 ラウンド受ける。
