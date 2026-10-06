# GitHub authentication for the two-seat regime: survey and recommendation (2026-10-05)

Question from the operator: the same person runs both seats on two machines, so why more than one `gh auth login`? What is the correct, persistent form, judged on security and on GitHub's own authentication model?

Written by the orchestrator seat from official documentation (fetched 2026-10-05) and local checks on the Linux host. Sources are listed at the end.

## 1. Facts that fix the design

| # | fact | source |
|---|---|---|
| F1 | A pull request author cannot approve their own pull request. | docs.github.com, "Approving a pull request with required reviews" |
| F2 | A personal access token "has the same capabilities ... that the owner of the token has"; it is the user, not a separate actor. | docs.github.com, "Managing your personal access tokens" |
| F3 | Merging a pull request through the REST API needs only `Contents: write` on a fine-grained token; opening and pushing need the same or less. | docs.github.com, REST "Merge a pull request" |
| F4 | GitHub recommends fine-grained PATs over classic ones; fine-grained tokens can be limited to named repositories and permissions, and may have an infinite lifetime for a personal account. | same page |
| F5 | GitHub Apps "are preferred to OAuth apps because they use fine-grained permissions, give more control over which repositories the app can access, and use short-lived tokens"; installation tokens expire after 1 hour; a GitHub App "can act independently of a user". | docs.github.com, "Differences between GitHub Apps and OAuth apps"; "Generating an installation access token" |
| F6 | For automation accounts GitHub says: "we recommend using a GitHub App instead"; one free machine account per person is tolerated by the Terms of Service ("no more than one free machine account in addition to your free Personal Account"). | docs.github.com, "Managing deploy keys" (Machine users); Terms of Service |
| F7 | `gh auth login` stores the OAuth token in the OS credential store and "will fallback to writing the token to a plain text file" when none is usable; `--insecure-storage` forces the file; `--with-token` imports an existing token from stdin (minimum scopes `repo`, `read:org`, `gist`). OAuth-app tokens are long-lived by default. | cli.github.com manual; docs.github.com, "Authorizing OAuth apps" |
| F8 | GitHub Free personal accounts work "with unlimited collaborators ... on unlimited private repositories". | docs.github.com, "GitHub's plans" |
| F9 | Ruleset pull-request options: required approvals; "require an approval from someone other than the last person to push"; dismiss stale approvals on new pushes; bypass actors are users, teams, roles or GitHub Apps. | docs.github.com, "Available rules for rulesets" |
| F10 | Codex CLI `workspace-write` restricts writes (Landlock) but not reads: the agent can read anything the user can read; a read-restricting mode is an open request (openai/codex #7657). | openai/codex issues; Codex docs |

Local checks (Linux host, 2026-10-05 18:3xZ):

- `~/.config/gh/hosts.yml` is readable from the Claude Bash sandbox and holds a plaintext `oauth_token` for the active account `moriya-fumio-thd` (scopes `gist, read:org, repo, workflow`); the second account `mryfmo` (the repository owner) is stored in the keyring (`gh auth status`). A Secret Service is running (`gnome-keyring-daemon --components=pkcs11,secrets`, `org.freedesktop.secrets` on the user bus), so the plaintext entry is a fallback from an earlier login, not a missing keyring.
- `~/.config/gh-worker` does not exist (T90 provisioning pending). Both checkouts use the HTTPS remote with `credential.helper = !gh auth git-credential`, so a worker pane's `GH_CONFIG_DIR` decides which identity pushes.

## 2. Why one identity is not enough

The merge gate the operator chose (one required approval, no self-approval, orchestrator merges) needs two GitHub actors (F1). A second token of the same user is the same actor (F2) and a repository-scoped PAT cannot stop merging either, since `Contents: write` is both the push permission and the merge permission (F3). So the worker needs a distinct identity: a machine account (F6, one tolerated) or a GitHub App (F5, GitHub's recommendation). A fine-grained PAT of the human account is therefore not an option for the worker; it is the right form for nothing in this design.

## 3. Why one login per machine was never the requirement

Tokens are not bound to a machine (F7). What is per machine is the *storage*: a keyring entry cannot be copied, a file can. Hence:

- The worker credential should never need a login on a second machine. As a file it is distributed by chezmoi-private (age-encrypted at rest, mode 0600 on disk) and imported with `gh auth login --with-token --insecure-storage` or written directly as `hosts.yml`.
- The orchestrator credential (merge-capable) should stay in the OS keyring (macOS Keychain, Linux Secret Service), which means one interactive login per machine for that account only. Moving it into a synced file would trade a login for a plaintext merge token on every host.

## 4. Threat model and what each layer buys

Both seats run as the same Unix user. Neither sandbox restricts reads (F10 for Codex; verified for the Claude Bash sandbox above), and same-uid processes can also read `/proc/<pid>/environ` and talk to the user's D-Bus Secret Service. So, within one OS user, a worker that *wants* the orchestrator token can get it from a plaintext file trivially, from an environment variable easily, and from an unlocked keyring with some effort. The sandboxes prevent accidents and keep the model-driven shell on the documented path; they are not a privilege boundary between seats. Consequences:

1. Server-side rules carry the real weight: required approval from a second identity, "approval of the most recent reviewable push", dismiss stale approvals, no bypass actor on the integrity ruleset (F9). A stolen worker credential then cannot merge; a stolen orchestrator credential still can, so its storage matters most.
2. Short-lived, repository-scoped worker credentials shrink the blast radius of the credential that *is* reachable by the model (F5): a 1-hour installation token limited to this repository versus a non-expiring OAuth token with `repo` on every repository of an account.
3. The strongest local separation available is a separate OS user for the worker seats; it is out of scope here and recorded as the upgrade path if the model-side threat is taken seriously.

## 5. Options for the worker identity

| | machine account + fine-grained PAT | GitHub App installation |
|---|---|---|
| GitHub's stance | tolerated (F6) | recommended (F5, F6) |
| token lifetime | chosen at creation; infinite allowed (F4) | 1 hour, minted from the app private key |
| scope | this repository, chosen permissions | this repository, chosen permissions |
| identity in PRs | `<machine-login>` | `<app-slug>[bot]` |
| account overhead | e-mail, password, 2FA (recommended; GitHub may require it), collaborator Write role (F8) | create app once, install on the repo once |
| secret to distribute | one `hosts.yml` (token) | one PEM private key |
| gh integration | native (`GH_CONFIG_DIR`, T90 as built) | token minting needed: `gh token` extension (Link-/gh-token) or a 40-line helper that caches a token for 50 minutes and serves `gh`/git through `GH_TOKEN` or a credential helper |
| rotation | manual; GitHub removes PATs unused for a year | automatic per hour; rotate the PEM on compromise |

## 6. Recommendation

1. **Worker identity: GitHub App** (owner `mryfmo`, installed on `mryfmo/dotfiles` only; permissions Contents RW, Pull requests RW, Metadata R, Checks R, Actions R, Commit statuses R). It is GitHub's recommended automation identity, its tokens are short-lived and repository-scoped, it needs no second account and no 2FA, and the only long-lived secret is one PEM that travels once through chezmoi-private. A worker task adds the minting helper (`herdr-agents` already sets `GH_CONFIG_DIR`; the helper writes a fresh token into that config dir or exports `GH_TOKEN` for the worker pane and refreshes it), its tests, `make doctor` checks, and the README. Until the helper lands, the **interim** form is the machine account + repository-scoped fine-grained PAT written to `~/.config/gh-worker/hosts.yml` and distributed by chezmoi-private, which the current code supports without change. Either way the worker never logs in again on any machine.
2. **Orchestrator identity: the repository owner's human account in the OS keyring**, one login per machine, no file copy. Linux hygiene now: the active `gh` account on the Linux host is the work account `moriya-fumio-thd` with a plaintext token in `hosts.yml`; switch the active account to `mryfmo` (`gh auth switch`), remove the plaintext entry (`gh auth logout --user moriya-fumio-thd`, then re-login into the keyring if that account is needed on this host at all), and confirm `hosts.yml` carries no `oauth_token`. The agent host should hold only the identity the regime uses.
3. **Rulesets, after the worker identity exists:** required approvals 1, require approval of the most recent reviewable push, dismiss stale approvals, no bypass actor on the integrity ruleset; the gate's role check (author ≠ merger, approval present) activates by itself once `hosts.yml` or the minted token exists.
4. **Login count that results:** orchestrator account, one keyring login per machine (Linux done, Mac once); worker identity, zero logins anywhere (one app creation or one PAT creation, ever).

## 7. Sources

- https://cli.github.com/manual/gh_auth_login , https://cli.github.com/manual/gh_auth_token
- https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens
- https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/authorizing-oauth-apps
- https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/differences-between-github-apps-and-oauth-apps
- https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app
- https://docs.github.com/en/apps/creating-github-apps/about-creating-github-apps/best-practices-for-creating-a-github-app
- https://docs.github.com/en/authentication/connecting-to-github-with-ssh/managing-deploy-keys (Machine users)
- https://docs.github.com/en/site-policy/github-terms/github-terms-of-service
- https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/approving-a-pull-request-with-required-reviews
- https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets
- https://docs.github.com/en/rest/pulls/pulls (Merge a pull request, fine-grained permissions)
- https://docs.github.com/en/get-started/learning-about-github/githubs-plans
- https://docs.github.com/en/authentication/securing-your-account-with-two-factor-authentication-2fa/about-mandatory-two-factor-authentication
- https://github.com/actions/create-github-app-token , https://github.com/Link-/gh-token , https://github.com/cli/cli/discussions/5095
- https://github.com/openai/codex/issues/7657

## 8. Operator decision (2026-10-05 18:50Z) and correction

The operator's position: the dotfiles install/update decrypts the credential files and leaves them in place; nothing else is needed. That is right, and section 6 overweighted the keyring: within one OS user a worker can reach a keyring token too (section 4), so a 0600 file decrypted by `chezmoi apply` gives up almost nothing and removes every per-machine login.

Resulting form, replacing section 6 items 1, 2 and 4:

- chezmoi-private holds two age-encrypted files, `~/.config/gh/hosts.yml` (the owner account `mryfmo`, from `gh auth token` once) and `~/.config/gh-worker/hosts.yml` (the worker identity). `chezmoi apply` writes both as mode 0600; `gh` reads a token that is present in `hosts.yml` directly, so no login happens on any machine, ever.
- Because the worker file is static, the worker identity is the machine account with a repository-scoped fine-grained PAT (infinite lifetime, F4); a GitHub App's 1-hour tokens do not fit a static file and are not needed.
- Linux hygiene stays: the file for this host should carry the owner account only; the work account's plaintext token leaves `~/.config/gh/hosts.yml`.
- Public-side task: README operator phase rewritten to "place the two encrypted files in chezmoi-private", `make doctor` verifies both files, their mode and the active login names, `gh auth setup-git` folded into the managed git config.

## 9. Verification pass (2026-10-05 19:05Z): what was checked, what was wrong, what stays untested

| claim | status | evidence |
|---|---|---|
| A token present in `hosts.yml` is used without any login, before the keyring | verified | `cli/cli` `internal/config/config.go`: `ActiveToken` resolves env (`GH_TOKEN`) → plain config `oauth_token` (`ghauth.TokenFromEnvOrConfig`) → keyring; `TokenForUser` reads `hosts.<host>.users.<user>.oauth_token`; `Login(..., secureStorage)` "will fall back to the plain text config file" |
| `GH_TOKEN` overrides stored credentials; `GH_CONFIG_DIR` selects the config directory | verified | `gh help environment` |
| Merge needs `Contents: write`; opening a PR needs `Pull requests: write` | verified | docs.github.com, "Permissions required for fine-grained personal access tokens" |
| chezmoi `encrypted_` encrypts the source file (age), `private_` strips group/world permissions | verified | chezmoi.io source-state attributes, age guide |
| GitHub recommends a GitHub App when acting "on behalf of an organization or another user" | verified | docs.github.com, "About authentication to GitHub" |
| An app can be installed only by the account that created it and is granted the selected repositories independent of collaboration | verified | docs.github.com, "Installing your own GitHub App" |
| **Section 8 said the worker uses a repository-scoped fine-grained PAT of the machine account** | **wrong, corrected** | docs.github.com lists among fine-grained PAT limitations "Using fine-grained personal access token to contribute to repositories where the user is an outside or repository collaborator" and "Calling the Checks API"; `mryfmo/dotfiles` is owned by another personal account, so the machine account is a collaborator there and its fine-grained PAT cannot contribute (nor run `gh pr checks`). The worker file therefore holds the machine account's **OAuth token from one `gh auth login`** (scopes `repo`, `read:org`, `gist`, optionally `workflow`; long-lived by default) or a **classic PAT** with `repo` and `read:org` (GitHub removes a classic PAT unused for a year; the worker uses it daily). The scope is broad only within the machine account, which holds nothing but this collaboration. |
| Codex `workspace-write` can read `~/.config/gh/hosts.yml` and reach the user's Secret Service | **untested** | the headless probe (`codex --profile express exec --sandbox workspace-write …` running `test -r`, `grep -c oauth_token`, `busctl --user list`) was refused by the Claude Code auto-mode classifier as credential exploration and was not retried; the read claim rests on openai/codex #7657 and the Codex documentation, the D-Bus claim on reasoning only. The operator can run that probe from a plain shell. |
| Claude Bash sandbox can read `~/.config/gh/hosts.yml` | verified | `test -r` inside the sandbox (section 1) |
| Linux host has a running Secret Service; `mryfmo` is in the keyring, the active `moriya-fumio-thd` token is in plaintext | verified | `busctl --user list`, `gh auth status`, `hosts.yml` key names |

Corrected final form (supersedes section 8's second bullet):

- `~/.config/gh/hosts.yml`: owner account `mryfmo`, produced once by `GH_CONFIG_DIR=<tmp> gh auth login --with-token --insecure-storage < token` (or by `gh auth login … --insecure-storage` itself) so the file has the exact layout gh writes (`hosts.github.com.users.<login>.oauth_token`, `user`, `git_protocol`); then `encrypted_private_hosts.yml` in chezmoi-private.
- `~/.config/gh-worker/hosts.yml`: machine account, same procedure, same encryption.
- Stricter alternative if a long-lived worker token is unacceptable: a GitHub App installed on the repository (1-hour tokens; needs the minting helper described in section 5).

## 10. Operator correction (2026-10-05 19:15Z): one credential store per account, nothing merged

Section 6 item 2 and section 8 told the operator to strip the work account from the Linux host. That was wrong: the work account is a legitimate identity on this host for other repositories; the defect was only that two accounts shared one `hosts.yml` with a global "active" switch, which is how the regime came to merge as the work account. The form that removes the ambiguity is one `GH_CONFIG_DIR` per account, each with its own age-encrypted `hosts.yml` in chezmoi-private:

| account | config dir | used by | selection |
|---|---|---|---|
| `mryfmo` (owner) | `~/.config/gh` (gh default) | orchestrator seat, personal repositories | nothing to set |
| `moriya-fumio-thd` (work) | `~/.config/gh-work` | work repositories | `GH_CONFIG_DIR` set per repository (direnv `.envrc` or the shell profile for the work tree) |
| machine account | `~/.config/gh-worker` | worker seats | set by `herdr-agents` (T90) |

`gh auth switch` is no longer used; each store holds exactly one user, so `gh auth status` and `gh auth git-credential` (the HTTPS helper reads the same `GH_CONFIG_DIR`) are unambiguous. The two seats still carry two different identities (section 2); nothing is shared between them.

## 11. Operator direction (2026-10-05 19:25Z): prompt for the GitHub login during setup, automate the rest

Agreed, with two fixed points:

- GitHub accepts no account password for Git or the API (removed 2021; docs.github.com "About authentication to GitHub": password authentication deprecated). The interactive form is `gh auth login`, which shows a one-time code in the TUI and completes in the browser with 2FA, or pastes a token with `--with-token`. The TUI prompt is therefore the device-code dialogue, not a password field.
- The README (line 162) and the Makefile (line 40) already define the operator phase as the interactive part run once per machine, including the `gh` logins, and `make update` as never prompting. `setup.sh` does not yet implement the `gh` part. The prompt therefore belongs in `setup.sh` and in an explicit interactive target (`make gh-auth`); `make update` keeps reporting (T102 does this for the worker store at seating) and never prompts.

Shape of the step, for each store in section 10's table (`~/.config/gh`, `~/.config/gh-work`, `~/.config/gh-worker`): if the store already holds a token (`GH_CONFIG_DIR=<dir> gh auth status`), skip; otherwise run `GH_CONFIG_DIR=<dir> gh auth login --hostname github.com --git-protocol https --insecure-storage`, `chmod 600 <dir>/hosts.yml`, `gh auth setup-git`. When chezmoi-private already provides the decrypted `hosts.yml`, the step prompts for nothing, so the encrypted files (sections 8–10) and the setup prompt are the same mechanism with and without a private source. Account *creation* (the machine account) stays a one-time manual step on github.com; GitHub does not allow automated registration.

## 12. Operator decision, final (2026-10-05 23:10Z): one store per account, file storage, no further revisiting

The operator confirmed the §10 form as the intended one and declined to reopen the keyring question. The Codex Bot's P1 on PR #288 (owner token in `~/.config/gh/hosts.yml` readable by worker seats) is dispositioned `not-applicable` with this record as the reason: the exposure is known (§4, §8, this section), the same-user boundary is not treated as a privilege boundary in this regime, and the server-side rules carry the protection. The orchestrator will not raise the keyring alternative again; a change of stance is the operator's to make.

## 13. Host finding (2026-10-06 01:15Z): this Linux host has no chezmoi-private configuration

`make update` prints `Warning: private chezmoi source/config not found. Skipping private dotfiles.` on this host (seen in the T82b, T103 and T104 deploy logs): `~/.local/share/chezmoi-private` exists but `~/.config/chezmoi-private/chezmoi.yaml` does not, so the private layer has never been applied here. The age settings seen earlier (`encryption: age`, identity `~/.config/age/key.txt`) belong to the public chezmoi config. Consequence for §8–§11: an `encrypted_private_hosts.yml` in chezmoi-private reaches this host only after the operator creates that config file (README private layer); until then `make gh-auth` is the path that fills the stores here. Operator-side item; recorded, not acted on.

## 14. Operator direction (2026-10-06): no credential copies anywhere; each machine obtains its own token from GitHub by logging in

GitHub never hands an existing credential back: a PAT is shown once at creation, an OAuth token is delivered once at authorization, and `gh auth token` only prints the local copy. "Fetching the user's credential from GitHub at clone/install/update" therefore means logging in, which mints a fresh token for that machine. That is the T103 flow as built: `setup.sh` and `make gh-auth` log in each empty store; `make update` never touches credentials. Consequently nothing is stored in any repository, encrypted or not: §8–§11's chezmoi-private route is withdrawn (it would copy one token to every host under one key and remove per-machine revocation). Each machine holds only its own tokens in its own stores; a lost machine costs one revocation (Settings → Applications → GitHub CLI, or `gh auth logout`). The README sentence about an `encrypted_private_hosts.yml` per store is removed in the next documentation task.

## 15. Operator fact (2026-10-06): one GitHub account per machine; the "work" store was a wrong assumption

| machine | OS user | GitHub account |
|---|---|---|
| MacBook Pro | `a0004262` | `moriya-fumio-thd` |
| Ubuntu `spark-9e8d` (this host, the regime host) | `moriya` | `moriya-fumio-thd` |
| MacBook Air | `mryfmo` | `mryfmo` |

So the human account is a property of the machine, not of the repository: on this host the intended account is `moriya-fumio-thd`, and the stray entry in `~/.config/gh` is `mryfmo` (keyring), not the work account as §6, §8 and §10 assumed. The three-store model of T103 is wrong in one place: there is no "work" store. The correct model has two stores on every machine: `~/.config/gh` holds that machine's human account (whichever it is; it is the merging account on that machine), and `~/.config/gh-worker` holds the one machine account the worker seats use everywhere. Both human accounts need write access to `mryfmo/dotfiles` (the repository owner already has it; `moriya-fumio-thd` already merges here), and the required-approval rule works on every machine because the PR author is always the machine account. Correction task: drop `work_gh_config_dir`/`WORK_GH_CONFIG_DIR`, rename the "owner" store to the machine's operator account in manifest, renderer, script, doctor, README and tests, and remove the chezmoi-private sentence (§14). Host hygiene on `spark-9e8d`: `gh auth logout --user mryfmo --hostname github.com` (operator's account, operator's command).

## 16. Decision A (operator, 2026-10-06): one account per machine for every seat; what still protects `main`, and what does not

Under A the orchestrator, the worker seats and the headless auditor on a machine all act as that machine's GitHub account (`moriya-fumio-thd` on spark-9e8d and the MacBook Pro, `mryfmo` on the MacBook Air). The auditor already is identity-less and read-only, so nothing changes there. The question is what replaces the actor separation that T90 wanted. Survey of the mechanisms, each checked against the official documentation on 2026-10-06:

| layer | mechanism | works with one account? | note |
|---|---|---|---|
| GitHub ruleset | pull request required; required status checks; conversation resolution required; linear history; block force pushes; restrict deletions | **yes** | these are actor-independent; the repository is public, so rulesets apply on the Free plan (`mryfmo/dotfiles` `private=false`) |
| GitHub ruleset | required approvals, "approval of the most recent push", Code Owners, bypass actors | **no** | all distinguish actors; with one account they either block everyone (author cannot approve own PR) or nobody |
| GitHub token permissions | fine-grained PAT without merge rights | **no** | merging needs only `Contents: write`, the same permission as pushing |
| GitHub identity | deploy key for the worker's pushes | partial, rejected | repository-scoped and account-free, but it cannot open PRs or read checks (no API), so the worker loses its autonomy |
| GitHub identity | GitHub App or machine account | works, **not A** | these are options B/C; the operator chose A |
| native denial in the seat (dotfiles principle 1) | Codex execpolicy: `gh pr merge` is already `forbidden` for every Codex seat (T63, `home/dot_codex/rules/default.rules:96`) | **yes** | extend to the API forms of a merge or auto-merge: `gh api -X PUT`, `gh api --method PUT`, `gh api graphql`; prefix rules cannot see a flag placed after the path, so the gate below stays the authority |
| native denial in the seat | Claude Code `permissions.deny` for the Claude *worker* seat: `Bash(gh pr merge:*)`, `Bash(gh api -X PUT:*)`, `Bash(gh api --method PUT:*)`, `Bash(gh api graphql:*)` | **yes** | deny rules hold over allow rules and apply to nested subcommands even in auto mode (code.claude.com permissions). They must live in the worker worktree's `.claude/settings.local.json`, written by `herdr-agents` when it seats a Claude worker, because the user-level settings also govern the orchestrator, which must merge. That file is Claude's permission policy, so the change routes to a Codex seat (routing rule) |
| integration gate | `make require-crit-review` with sweep, audit and acceptance evidence; merge only by the orchestrator through `gh pr merge --squash` | **yes** | unchanged; with one account it is the only place that knows which seat is acting, so it keeps the final word |
| attribution | per-seat SSH signing keys on the one account plus the "require signed commits" rule; agmsg history and acceptance records | **yes** | GitHub allows unlimited signing keys per account and shows "Verified"; `git log --show-signature` names the key, so a commit can be traced to the orchestrator pane, a worker seat or the human. Adding keys needs the `admin:ssh_signing_key` scope (a one-time re-login) or the web UI; recommended as a follow-up, not a precondition |
| residual | a deliberately misbehaving worker under the same OS user | **not closable under A** | server-side cannot tell the seats apart, and the same OS user can read every local credential; the native denials stop the accidental and the prompt-injected path, the gate and the records make the deliberate one visible after the fact. Closing it needs B (separate OS user) |

Resulting form, consistent with the dotfiles intent (same environment on macOS and Linux, denial at the native layer, autonomy to completion):

1. **Remove the role separation** (T90, T102, T103 surfaces): `GH_CONFIG_DIR` injection and token unsetting in `herdr-agents`, the gate's role check, the doctor's store findings and `check-tools.sh` identity check, the manifest store keys and their rendering, the `work`/`worker` stores. Keep one login per machine in gh's default directory, with `make gh-auth`/`setup.sh` logging it in only when empty.
2. **Native denial of merging in worker seats**: extend the Codex execpolicy; add the Claude worker-seat deny rules through `herdr-agents` (Codex-seat task, after step 1 is deployed so that a Codex seat has `gh`).
3. **Rulesets**: keep PR-only `main`, required checks, conversation resolution, linear history, force-push and deletion blocks; drop the required-approval rule and the bypass actor from the design (they cannot work under A); add "require signed commits" when the per-seat keys exist.
4. **Gate and records**: unchanged.

`gh auth logout --user mryfmo` on spark-9e8d remains the one host command (the operator's account).
