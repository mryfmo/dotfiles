# 操作者手順: 席の Claude Code 用 setup-token の発行と配置 (regime-cutover U551)

目的: 席(orchestrator / worker / dsh / router)の Claude Code 子プロセスを、共有 claude.ai login
(refresh token の回転で 11-07 以降 8 回失効)でも API key(U510、U512、退役)でもなく、
`claude setup-token` が印字する長期 OAuth token 1 つで動かす。token は host ごとに 1 ファイル
`<seats-root>/.state/claude-token`(0600、1 行)に置き、読むのは hcom-seat の shim だけ。shim が
`CLAUDE_CODE_OAUTH_TOKEN` として Claude 子の環境に渡し、sandbox の中ではファイル自体は読めない
(deny 行。`tests/unit/test_hcom_seat.py` が子の環境に値が届きファイルが deny されることを
fixture で確認。実 token での API 到達は配備後の検証で測る)。refresh token が無いので更新も回転も
起きない。
有効期限は 1 年(Claude Code 公式 docs の Authentication)。失効させるには claude.ai で account の
全 session を sign out する。

前提(agent 側で済ませる部分): U551 の head が merge され、`make deploy-kit` で
`~/.local/bin/common/seat-token-place` と新しい `hcom-seat`、`seat-login-preflight`、
`acp-broker` が配備されていること。`chezmoi apply` は各 role の
`~/.omp/profiles/<role>/agent/claude-bridge.json` から `claude-keyed` を指す
`provider.pathToClaudeCodeExecutable` 行を消す(modify script。他の key はそのまま)。
`claude-keyed` 自体の退役と modify script の削除は U553。

## 1. 人間がやること: token の発行 (自分の端末、ブラウザ)

自分のいつもの端末(席ではない)で次を 1 行実行する。

```sh
claude setup-token
```

ブラウザが開くので、席に使う claude.ai account で sign in し、同意する。端末に `sk-ant-oat01-` で
始まる 1 行の token が一度だけ印字される。クリップボードに残さず、次の手順 2 のプロンプトに貼る。

期待する結果: 端末に token 1 行。`~/.claude` の自分の login は変わらない(公式 docs: setup-token は
長期 token を印字するだけで login を置き換えない。配備後に `claude auth status` で確認する)。

## 2. 人間がやること: token の配置 (laptop のターミナル、1 回)

```sh
~/.local/bin/common/seat-token-place
```

`token: ` と出たら手順 1 の token を貼り付け(入力はエコーされない)、Enter。

できるもの: `~/.local/state/omp-seats/dotfiles/.state/claude-token`、mode 0600、1 行、
末尾は改行 1 つ。`.state` は 0700。端末の bracketed paste の印や前後の空白は placer が取り除く。

期待する結果(1 行、exit 0。`<seats-root>` は `~/.local/state/omp-seats/dotfiles` の絶対パス):

```
seat-token-place: placed <seats-root>/.state/claude-token (<n> characters, mode 0600)
```

`seat-token-place: refused: ...` の 1 行(exit 1)が出た場合、その行が理由を名指しする
(EOF、空、CSI 列だけ、形式外、2 行、chain や宛先の symlink、自分のものでない directory、
0600 でない既存の宛先)。token の内容は決して表示されず、何も書かれない。前のファイルがあれば
そのまま残る。手順 1 からやり直す。

## 3. 人間が実行する検証コマンド (結果は agent が判定できる)

```sh
~/.local/bin/common/seat-login-preflight --check
```

期待する結果: claude-bridge の各行が次の形(exit 0。`~` は絶対パスで印字される)。

```
orchestrator claude-bridge: token present (~/.local/state/omp-seats/dotfiles/.state/claude-token)
worker claude-bridge: token present (~/.local/state/omp-seats/dotfiles/.state/claude-token)
```

`token absent (<reason>)` なら理由がファイルと欠陥を名指しする(no <file>、mode 644、形式外、2 行、
CR)。手順 2 をやり直す。`make doctor` の Seat logins も同じ行を読む。

## 各行の根拠と事前実行 (第 5 条)

手順 1(期待: `sk-ant-oat01-` で始まる 1 行)

- source: Claude Code 公式 docs の Authentication、`CLAUDE_CODE_OAUTH_TOKEN` と
  `claude setup-token`
- dry-run: operator-only。ブラウザ同意が要り、agent は実 token を扱わない(第 59 条)

手順 2(期待: `placed <file> (<n> characters, mode 0600)`)

- source: `scripts/orchestrator/seat-token-place`(形は `TOKEN_FORM_RE`、0600 の一時ファイル経由、
  chain と宛先の symlink は拒否)
- dry-run: `tests/unit/test_remote_host_logins.py` の `SeatTokenPlaceTest`。fixture token の配置、
  bracketed paste、EOF / 空 / CSI だけ / 形式外 / 2 行 / link / 0644 の宛先の各注入は何も書かない

手順 3(期待: `token present (<file>)`)

- source: `scripts/orchestrator/seat-login-preflight` の `claude_token_state`(形だけ判定。
  `claude auth status` も API 呼び出しも無い)
- dry-run: `tests/unit/test_remote_host_logins.py` の `PreflightTest`、
  `tests/unit/test_runtime_health.py` の doctor 行、`tests/install/common/check_tools.bats`

## 補足

- 席の起動は `hcom-seat` が同じファイルを毎回判定する(`token_file_check`)。無い、link、0600 で
  ない、形式外、2 行のどれでも起動を拒否し、この handout の手順を名指しする。dry run も同じ。
- 旧 API key 経路の名残 `.state/anthropic/`(空の `api-key` を含む)はこの head ではどの lever も
  読まない(hcom-seat、seat-login-preflight、seat-token-place は U551a から、Router の `acp-broker`
  は U553 で token に移った。U551a だけを配備した host では main の `acp-broker` が U553 の配備まで
  これを読む)。この head の配備後に消してよい:
  `rm -r ~/.local/state/omp-seats/dotfiles/.state/anthropic`
- U510 の modify script を `chezmoi apply` した host では、`~/.omp/profiles/<role>/agent/` の
  `claude-bridge.json` に `provider.pathToClaudeCodeExecutable` 行が残りうる(この laptop には無い、
  実測 11-15)。この head の modify script が `chezmoi apply` でその行の byte だけを切り取る
  (他の byte はそのまま。key の綴りが JSON escape でも見つける。
  `tests/unit/test_generate_agent_configs.py`)。script が読めない JSON なら stderr に 1 行出して
  素通しするので、その時はその行を手で消す。bridge は同梱の Claude Code binary に戻る。
- token は 1 年で切れる。切れたら手順 1 と 2 をやり直す。
