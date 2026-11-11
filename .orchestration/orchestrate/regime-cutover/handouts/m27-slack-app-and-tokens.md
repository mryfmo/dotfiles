# M-27 handout: the Slack app and its two tokens (table row i4)

Written 2026-11-10T22:4xZ by the coordinator (standing order 48: the human does the one act a human must; standing order 51: the gate is announced the moment it opens). The operator does the three steps below once, at any time; nothing of the kit has to land first. The kit's part (the Slack Source of the superagent fork, the `slack.env` reader, the table row i4) is a unit the coordinator opens as soon as the tokens exist. Until then row i4 stays pending and nothing else waits on it.

## What the kit will read

One file, `~/.dsh/router-credentials/slack.env`, mode 0600, in the Router's credential root (the same root as the GitHub token's `gh/hosts.yml`), with two lines:

```
SLACK_APP_TOKEN=xapp-...
SLACK_BOT_TOKEN=xoxb-...
```

The app-level token (`xapp-`) opens the Socket Mode connection, so the Router needs no inbound URL and no public listener (R-45: the Router stays inside its sandbox and binds nothing but its loopback port). The bot token (`xoxb-`) reads the configured channel and posts the accepted row's receipt.

## Step 1 (operator, once): create the app from the manifest

1. Open `https://api.slack.com/apps` signed in to the workspace the Router should listen in, and choose **Create New App**; the dialog "Create an app" offers **From a manifest** and **From scratch** (the labels as seen on 2026-11-10T23:5xZ); press **From a manifest**, pick the workspace (step 1 of 3), paste the manifest (step 2), review and **Create** (step 3):

```json
{
  "display_information": { "name": "TechnoPro Agent Harness Router" },
  "features": { "bot_user": { "display_name": "harness-router", "always_online": false } },
  "oauth_config": {
    "scopes": { "bot": ["app_mentions:read", "channels:history", "channels:read", "chat:write", "groups:history", "groups:read"] }
  },
  "settings": {
    "socket_mode_enabled": true,
    "event_subscriptions": { "bot_events": ["app_mention", "message.channels", "message.groups"] },
    "org_deploy_enabled": false,
    "token_rotation_enabled": false
  }
}
```

2. On the app's "Basic Information" page, under "App-Level Tokens", generate a token named `router-socket` with the scope `connections:write`. Copy it (it begins with `xapp-`).
3. On "Install App", install the app to the workspace and copy the "Bot User OAuth Token" (it begins with `xoxb-`).
4. In Slack, invite the bot into the one channel the Router should read (`/invite @harness-router`), and tell the coordinator the channel's name.

## Step 2 (operator, once): place the two tokens on this host

In your own terminal on this host (the tokens never go through the agent):

```sh
mkdir -p ~/.dsh/router-credentials && chmod 700 ~/.dsh/router-credentials
umask 077 && printf 'SLACK_APP_TOKEN=%s\nSLACK_BOT_TOKEN=%s\n' '<xapp-...>' '<xoxb-...>' > ~/.dsh/router-credentials/slack.env
chmod 600 ~/.dsh/router-credentials/slack.env
```

## Step 3 (operator, once): say the channel name and that the file exists

One message to the coordinator with the channel name. The kit then reads (never printing a token):

```sh
test -f ~/.dsh/router-credentials/slack.env && stat -f '%Lp' ~/.dsh/router-credentials/slack.env
```

Expected: `600`. The coordinator opens the M-27 unit (the Slack Source in the superagent fork, reading the two names above from the Router's credential root alone; the admission row for the channel in `router-settings-apply`; row i4's command: one message in the channel becomes one accepted row and one TASK, a message outside the channel is not accepted).

## Teams and Outlook (rows i5 and i9), not actionable by the operator alone

They need a Microsoft tenant app registration with Graph application permissions and admin consent (`msgraph.env`, T-M-27-14). The kit generates the registration's manifest and redirect URI when that unit opens; the tenant's administrator grants consent. The coordinator asks for that step only when the Slack Source has landed, so the two Sources share one credential reader.

## Screen by screen (added 2026-11-10T23:4xZ at the operator's request)

| # | Where you are | What you do |
| --- | --- | --- |
| 1 | `https://api.slack.com/apps`, signed in to the target workspace | press the green **Create New App** |
| 2 | the dialog "Create an app" (seen 2026-11-10T23:5xZ: two choices, **From a manifest** and **From scratch**) | press **From a manifest** |
| 3 | "Pick a workspace to develop your app" (Step 1 of 3; the dropdown is empty until you are signed in: the page says "You'll need to sign in to your Slack account to create an application") | choose the workspace, **Next** |
| 4 | the manifest step (Step 2 of 3; not seen without a sign-in, described by the official doc docs.slack.dev/app-manifests/configuring-apps-with-app-manifests) | press **JSON**, delete the sample, paste the manifest from Step 1 above, **Next** |
| 5 | the review step (Step 3 of 3; the doc: "Review and verify that the configuration you entered matches the summary and click Create") | **Create** |
| 6 | **Basic Information** (opens after Create); scroll to **App-Level Tokens** | **Generate Token and Scopes**; Token Name `router-socket`; **Add Scope** `connections:write`; **Generate**; **Copy** the `xapp-...` value into a note on your own machine (it is not shown again); **Done** |
| 7 | left menu **Install App** | **Install to <workspace>**, then **Allow**; **Copy** the **Bot User OAuth Token** (`xoxb-...`) |
| 8 | Slack itself, the channel the Router should read (make `#harness-intake` if none) | send `/invite @harness-router`; "added an integration" confirms it |
| 9 | your own terminal | run the four lines of Step 2 with the two values pasted in; the last line prints `600 /Users/<you>/.dsh/router-credentials/slack.env` |
| 10 | this chat | one message with the channel name |

If screen 4 says the manifest is invalid, check the **JSON** tab is selected. If screen 7 asks for an administrator's approval before **Allow**, the workspace requires app approval; say so and the gate waits for the administrator.


## The one-link form (official doc, "Sharing manifests")

The creation flow can be entered with the manifest already filled in: `https://api.slack.com/apps?new_app=1&manifest_json=<URL-encoded manifest>`. The encoded link for this manifest is in `/tmp/slack-create-app-url.txt` on the coordinator's host (738 characters); opening it signed in goes straight to "Pick a workspace" with the manifest prefilled, so screens 2 and 4 are skipped.
