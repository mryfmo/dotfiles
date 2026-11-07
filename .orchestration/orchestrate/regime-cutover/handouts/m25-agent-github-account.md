# M-25 handout: the agent GitHub account and the push restriction on main

Written 2026-11-07T06:4xZ by the coordinator from PRD row M-25, ADR-003, ADR-009 and plan tasks T-M-25-01 to T-M-25-03. The operator does steps 1 and 2 once. Every later step is the kit's (the doctor row, the handout page in docs/, the scratch merge attempt, the Router credential placement in M-26).

## Measured today (2026-11-07T06:40Z)

| Fact | Value | Read |
| --- | --- | --- |
| Repository owner (admin) | `mryfmo` | `gh api repos/mryfmo/dotfiles --jq .owner.login` |
| Direct collaborators | `mryfmo` (admin), the coordinator's collaborator login (write) | `gh api 'repos/mryfmo/dotfiles/collaborators?affiliation=direct'` |
| The login the coordinator's `gh` and `pr-merge.sh` use | the coordinator's collaborator login (PR 713 and 715 `mergedBy`) | `gh api user --jq .login`; `gh pr view 715 --json mergedBy` |
| Ruleset `main integration gate` (24397953) | rules deletion, non_fast_forward, required_status_checks, pull_request (0 approvals); bypass actors none; no push restriction | `gh api repos/mryfmo/dotfiles/rulesets/24397953` |
| Classic branch protection on main | none (HTTP 404) | `gh api repos/mryfmo/dotfiles/branches/main/protection` |

So today any collaborator with write can merge a pull request whose checks pass. M-25 separates two rights: the agent account (the Router and the seats) can push branches and open pull requests and cannot merge; one named login merges, through `pr-merge.sh`.

## Step 1 (operator, once): create the agent account and grant write

1. Create a new GitHub user for the agent (its own email, 2FA on). Suggested name: `mryfmo-agent` or a name of the operator's choosing. The kit never learns its password; it learns one token (step 3 of M-26).
2. As `mryfmo` (the owner), invite it as a direct collaborator with the `Write` role, not `Maintain`, not `Admin`: GitHub, repository Settings, Collaborators, Add people. Accept the invitation from the agent account.
3. Proof the kit reads afterwards (run as any collaborator):

```
gh api repos/mryfmo/dotfiles/collaborators/<agent-login>/permission --jq .permission
```

Expected: `write`.

## Step 2 (operator, once): restrict who may update main

The ruleset form, since the repository already uses a ruleset and classic protection is absent. As `mryfmo`, add a new ruleset on `~DEFAULT_BRANCH` holding the one rule "Restrict updates" with the merge login as its one bypass actor ("Always"), and leave ruleset `main integration gate` (its four rules: deletion, non-fast-forward, the required status checks, the pull request requirement) without any bypass actor. A bypass actor applies to a whole ruleset, so adding the merge login to `main integration gate` would let that login bypass the required checks and the pull request requirement too (verdict U20-be49a626 P1); the separate update-only ruleset keeps those gates on every login. Which login is the merge login is the open decision below; the default is the coordinator's collaborator login.

Proof the kit reads afterwards:

```
gh api repos/mryfmo/dotfiles/rulesets --jq '.[] | [.id, .name]'; gh api repos/mryfmo/dotfiles/rulesets/24397953 --jq '[.bypass_actors[]? | [.actor_type, .actor_id, .bypass_mode]], [.rules[].type]'
```

Expected: a second ruleset beside `main integration gate`; the first command lists it, the second shows `main integration gate` with no bypass actor and its four rules unchanged; `gh api repos/mryfmo/dotfiles/rulesets/<new id>` shows the one `update` rule and one bypass actor (the merge login's user id).

The classic form (only if the ruleset form is unavailable on this plan): Settings, Branches, Add rule for `main`, "Restrict who can push to matching branches", the merge login alone. Proof: `gh api repos/mryfmo/dotfiles/branches/main/protection --jq '[.restrictions.users[].login]'` lists that login only.

## What the kit does after steps 1 and 2

- T-M-25-03: one merge attempt as the agent account on a scratch pull request, under a scratch `GH_CONFIG_DIR`; GitHub's refusal line is the evidence row.
- T-M-25-04 and 05: `docs/engagement-handout.md` gains the two reads above; `scripts/check-tools.sh` gains the doctor row `check_agent_github_account` with its bats cases.
- M-26 step 5: the agent account's token (fine-grained, this repository only, Contents read and write, Pull requests read and write, no Administration) is placed in the Router's credential root alone, mode 0700, by the operator on the Router host; the handout of M-26 names the exact path once U317 lands (U317b moved the Router state under `$DSH_HOME/router-state`).

## Open decision for the operator (default applied if nothing is said)

Which login is "the operator's login" that alone may update main. Default: the coordinator's collaborator login, because `pr-merge.sh` runs under it today and every merge row since the program began names it. Under this default the three identities are: `mryfmo` owns the repository and edits rulesets; the coordinator's collaborator login merges through the lever; the new agent account pushes branches for the Router and the seats and cannot merge. The operator can instead name `mryfmo` as the merge login; then the coordinator loses the merge right and every `pr-merge.sh` run becomes the operator's own step.

## Row 9 for reference (M-27 and M-18), not actionable yet

- M-18 asks the operator for one word only: after the GitHub Source has run a week in observe mode (M-26 task 15), whether it moves to auto (T-M-18-04). Keeping observe is a recorded skip, not a failure.
- M-27 asks the operator for two credentials, each placed in the Router credential root with mode 0600, after M-26 and M-18 land: a Slack app with Socket Mode, an app-level token with `connections:write` and a bot token (`slack.env`, T-M-27-01); a Microsoft tenant app registration with the Graph application permissions the Teams and Outlook Sources read with, and its client secret (`msgraph.env`, T-M-27-14), with admin consent in the tenant. The kit generates the app manifest JSON and the redirect URI before that step (08-purpose-and-goal.md, the human-steps table).
