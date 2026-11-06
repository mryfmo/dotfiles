# 操作者手順: DSH の model route 鍵と、席の GitHub identity(2026-11-06)

どちらも操作者にしかできない作業です。coordinator はそれぞれの完了を実測で確認し、店に記録します。

## 1. (撤回、2026-11-06T05:46:33Z) DSH の model route 鍵

操作者の判断「Ollama Cloud の API key は dotfiles の Claude Code + Codex OAuth に反する」により、この手順は撤回します。DSH の model route は既存の login route(Claude login、Sign in with ChatGPT)経由で設計し直します(U238)。鍵は置かないでください。

## 2. 席の GitHub identity(M-25 と U88)

今日、席は操作者の GitHub token で動き、`pr-merge.sh` 以外に merge を止めるのは omp の文字列 deny だけです。PRD open question 13 の既定は「専用 user に branch への write のみ、`main` の merge 権なし」です。手順は 3 段です。

1. GitHub で machine account を 1 つ作り(名前は自由、例 `mryfmo-seat`)、`mryfmo/dotfiles` に Write 権限の collaborator として招待し、受諾する。
2. その account で fine-grained personal access token を作る。Resource owner はその account、Repository access は `mryfmo/dotfiles` のみ、Permissions は Contents: Read and write、Pull requests: Read and write、Metadata: Read。Administration と Workflows は付けない。期限は 90 日。
3. token をラップトップに置く。

```sh
mkdir -p ~/.config/gh-seat && chmod 700 ~/.config/gh-seat
printf '%s\n' '<fine-grained token>' > ~/.config/gh-seat/token
chmod 600 ~/.config/gh-seat/token
```

coordinator の確認と後続。token の scope を `gh api user` と `gh api repos/mryfmo/dotfiles` で読み、席の shim が `GH_TOKEN` にこの token を渡す unit(U88 を M-25 に畳んだもの)を brief します。ruleset は `required_approving_review_count: 1` に上げられるようになります(席が author、操作者が approver、merge は操作者 login の `pr-merge.sh`)。それまで ruleset は変えません。

## 3. 今は不要なもの

- Microsoft tenant app 登録(M-27 の Teams と Outlook)。Slack 先行の既定のため後回し。
- Ubuntu の host step。M-10 の席実走の brief を出すときに手順を別紙で出します。
