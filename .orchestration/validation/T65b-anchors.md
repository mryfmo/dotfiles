# T65b Pi v0.84.1 pinned-source anchor verification

Source ref for every row:
`https://raw.githubusercontent.com/earendil-works/pi/refs/tags/v0.84.1/`.
Files were fetched from that immutable tag and compared with the corresponding
v0.84.2 source cited by accepted T65/T66/T67 evidence. Result: no cited contract
changes semantically. The earlier T65 display references to
`settings-manager.ts:63` and `security.md:22` were stale line positions; the
same intended contracts are at v0.84.1 lines 68 and 29 respectively.

| Task | Pinned source | v0.84.1 lines | Verified contract | v0.84.2 comparison |
| --- | --- | ---: | --- | --- |
| T65 | [`settings-manager.ts`](https://raw.githubusercontent.com/earendil-works/pi/refs/tags/v0.84.1/packages/coding-agent/src/core/settings-manager.ts) | 68; 106; 904–912 | `DefaultProjectTrust` remains exactly `ask \| always \| never`; the global setting and accessor remain present. | Anchor text identical; v0.84.2 adds unrelated fullscreen/default-tools settings. |
| T65 | [`security.md`](https://raw.githubusercontent.com/earendil-works/pi/refs/tags/v0.84.1/packages/coding-agent/docs/security.md) | 18–29 | Non-interactive print/JSON/RPC shows no trust prompt; absent a saved decision, `ask` and `never` ignore protected project resources while `always` trusts them. | Entire file byte-identical. |
| T66/T67 | [`loader.ts`](https://raw.githubusercontent.com/earendil-works/pi/refs/tags/v0.84.1/packages/coding-agent/src/core/extensions/loader.ts) | 455–463; 490–515 | Loader imports the default export, requires a function, awaits the factory with `ExtensionAPI`, and returns an error on load/factory failure. | Entire file byte-identical. |
| T66 | [`types.ts`](https://raw.githubusercontent.com/earendil-works/pi/refs/tags/v0.84.1/packages/coding-agent/src/core/extensions/types.ts) | 1517–1518 | `ExtensionFactory` remains `(pi: ExtensionAPI) => void \| Promise<void>`. | Anchor text identical; one unrelated v0.84.2 comment shifts the line by one. |
| T66 | [`types.ts`](https://raw.githubusercontent.com/earendil-works/pi/refs/tags/v0.84.1/packages/coding-agent/src/core/extensions/types.ts) | 853–912 | `tool_call` still supplies typed bash/read/edit/write/grep/find/ls inputs plus the custom-tool fallback. | Anchor slice byte-identical. |
| T66 | [`types.ts`](https://raw.githubusercontent.com/earendil-works/pi/refs/tags/v0.84.1/packages/coding-agent/src/core/extensions/types.ts) | 1071–1074 | Handler result still supports `block?: boolean` and `reason?: string`. | Anchor slice byte-identical. |
| T66 | [`types.ts`](https://raw.githubusercontent.com/earendil-works/pi/refs/tags/v0.84.1/packages/coding-agent/src/core/extensions/types.ts) | 305–313 | Modes remain `tui`, `rpc`, `json`, `print`; `hasUI` remains true in TUI and RPC, so TUI-only confirmation remains required. | Anchor slice byte-identical. |
| T67 | [`quickstart.md`](https://raw.githubusercontent.com/earendil-works/pi/refs/tags/v0.84.1/packages/coding-agent/docs/quickstart.md) | 44–67; 130–157 | `/login`, Claude Pro/Max, ChatGPT Plus/Pro (Codex), `/model`/Ctrl+L, Shift+Tab, print, JSON, and RPC instructions remain. | Entire file byte-identical. |
| T67 | [`providers.md`](https://raw.githubusercontent.com/earendil-works/pi/refs/tags/v0.84.1/packages/coding-agent/docs/providers.md) | 15–35; 58–105 | Subscription names/terms notes and the documented provider credential-variable table remain. | Entire file byte-identical. |
| T67 | [`rpc.md`](https://raw.githubusercontent.com/earendil-works/pi/refs/tags/v0.84.1/packages/coding-agent/docs/rpc.md) | 9–76; 281–333; 832–880 | Provider/model options, LF JSONL prompt/response, thinking levels including model-dependent xhigh/max, and `agent_end` remain. | Cited slices byte-identical; v0.84.2 only documents an unrelated later `message_update.usage` addition. |
| T67 | [`extensions.md`](https://raw.githubusercontent.com/earendil-works/pi/refs/tags/v0.84.1/packages/coding-agent/docs/extensions.md) | 56–113 | Default-export extension form, `tool_call` blocking example, and explicit `--extension`/`-e` loading remain. | Quick-start slice byte-identical; later send-message docs differ. |
| T67 | [`main.ts`](https://raw.githubusercontent.com/earendil-works/pi/refs/tags/v0.84.1/packages/coding-agent/src/main.ts) | 780–788; 892–898 | Extension loader errors become error diagnostics; any runtime error exits status 1 before non-interactive execution. | Startup diagnostic slice byte-identical at v0.84.2 lines 784–902; unrelated UI setup shifts it by four lines. |

## Mechanical comparison evidence

The following comparisons passed:

```text
PASS settings trust union
PASS security whole file
PASS loader whole file
PASS extension types anchor slices
PASS quickstart whole file
PASS providers whole file
PASS RPC cited slices
PASS extensions quick-start slice
PASS startup diagnostics slice
```

No STOP condition was triggered.
