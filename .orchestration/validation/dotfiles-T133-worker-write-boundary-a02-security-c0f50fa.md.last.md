Reviewed [PR #431](https://github.com/mryfmo/dotfiles/pull/431) at `c0f50fa1383416240ad28959dbc4635afa777175`. Found three gaps in the claimed startup controls.

1. **P1 · High confidence — AWS credential-process selectors bypass screening.**  
   `home/dot_claude-worker/modify_private_settings.json:194` accepts `CLAUDE_CODE_USE_BEDROCK`, `AWS_CONFIG_FILE`, `AWS_SHARED_CREDENTIALS_FILE` and `AWS_PROFILE`, allowing settings to select a worker-controlled `credential_process`. The complete preflight accepted this combination in an in-memory probe. Claude uses the AWS credential chain, whose process provider executes the configured command; that execution happens through authentication rather than the sandboxed Bash tool. This defeats K02’s executable-source screening claim. Reject these selectors or inspect their referenced configuration before trust. [Claude authentication](https://code.claude.com/docs/en/amazon-bedrock), [AWS process provider](https://docs.aws.amazon.com/AWSJavaScriptSDK/v3/latest/Package/-aws-sdk-credential-providers/)

2. **P1 · High confidence — S04 inspects the wrong main checkout for other repositories.**  
   `home/dot_claude-worker/modify_private_settings.json:254` always screens the fixed dotfiles anchor’s local settings, although `herdr-agents --add-worker … [DIR]` accepts other repositories. A hook in `<DIR>/.claude/settings.local.json` was absent from the inventory and passed the complete preflight. Claude worktrees load their own main checkout’s local settings, so that hook remains executable after launch. Pass the validated repository main root into screening, or refuse unsupported roots. [Worktree settings location](https://code.claude.com/docs/en/settings#where-claude-code-keeps-the-local-file-in-a-git-repository)

3. **P2 · High confidence — Object-form plugin commands escape content inspection.**  
   `home/dot_claude-worker/modify_private_settings.json:292` follows only string/list component references; documented `commands` mappings containing `source` or inline `content` pass recursive screening without Markdown inspection. Both `{"source":"./extra/payload.md"}` and inline dynamic-shell content passed the complete preflight; the referenced file was missing from S21. Plugin disabling mitigates immediate execution, but S15/S21 explicitly promise payload refusal even for disabled plugins. Inspect these forms or reject them. [Plugin command mappings](https://code.claude.com/docs/en/plugins/manifest-reference#commands)

The probes executed the reviewed screening functions with virtual filesystem inputs; no payloads or live workers ran. `git diff --check` passed, and no files were changed.

📝 まとめ: 指定差分と threat_table の監査を完了し、P1 を2件、P2 を1件報告しました。受け入れ判断は orchestrator に委ねます。

Not checked: live enforcement and test-suite execution; GitHub CI was unavailable because `gh` could not connect. Runtime consequences above follow the documented loading behavior.

Verdict: incorrect