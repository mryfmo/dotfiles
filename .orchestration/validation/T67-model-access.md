# T67 Pi model-access operator procedure and result form

Run this procedure only after the orchestrator has installed Pi `0.84.1` and
deployed the accepted permgate extension. Do not paste subscription tokens,
API keys, callback URLs, or the contents of `~/.pi/agent/auth.json` into this
form.

Pinned references:

- [Pi v0.84.1 quickstart: subscription login and model controls](https://github.com/earendil-works/pi/blob/v0.84.1/packages/coding-agent/docs/quickstart.md#authenticate)
- [Pi v0.84.1 providers: subscription names and terms-relevant notes](https://github.com/earendil-works/pi/blob/v0.84.1/packages/coding-agent/docs/providers.md#subscriptions)
- [Pi v0.84.1 RPC: thinking-level names and model-dependent exposure](https://github.com/earendil-works/pi/blob/v0.84.1/packages/coding-agent/docs/rpc.md#set_thinking_level)
- [Pi v0.84.1 extensions: explicit `--extension` loading](https://github.com/earendil-works/pi/blob/v0.84.1/packages/coding-agent/docs/extensions.md#quick-start)

## Operator procedure

1. Open a terminal in a disposable scratch directory. Confirm the pinned
   binary before authentication:

   ```bash
   pi --version
   ```

   Continue only when the single output line is `0.84.1`.

2. Start the interactive UI from the scratch directory:

   ```bash
   pi
   ```

3. In Pi, enter `/login`. In the provider picker choose the exact UI path
   **Claude Pro/Max**, then complete the provider/browser flow. Pi's pinned
   provider documentation says this subscription route uses Anthropic extra
   usage billed per token rather than Claude plan limits; include that fact in
   the terms judgment below.

4. Enter `/model` (equivalently press `Ctrl+L`). Search for `fable`, record
   every matching provider/model ID exactly as displayed, and select the
   intended Fable-family candidate if one is present.

5. Press `Shift+Tab` repeatedly until the thinking label wraps to the first
   value. Record the distinct labels in order. The pinned RPC vocabulary is
   `off`, `minimal`, `low`, `medium`, `high`, `xhigh`, and `max`; `xhigh` and
   `max` appear only when the selected model supports them. Record the label
   that supplies the desired xhigh-equivalent, or `none`.

6. Enter `/login` again. In the provider picker choose the exact UI path
   **ChatGPT Plus/Pro (Codex)**, then complete the provider/browser flow. The
   pinned provider documentation requires a ChatGPT Plus or Pro subscription
   and links OpenAI's Codex-for-OSS endorsement.

7. Enter `/model` (or `Ctrl+L`). Search for `gpt-5.6`, record every matching
   provider/model ID exactly as displayed, and select the intended candidate
   if one is present.

8. Repeat the `Shift+Tab` cycle and record the distinct thinking labels for
   that model. The pinned RPC documentation specifically notes that some
   models, including GPT-5.6, expose both `xhigh` and `max`; record what this
   installed catalog actually shows.

9. Outside Pi, use an already-configured documented credential environment
   variable and run the headless lane. Set only provider/model selectors on
   this command line; never put the credential value in the command or form:

   ```bash
   PI_CHECK_PROVIDER=anthropic PI_CHECK_MODEL='<exact-model-id>' pi-model-access-check
   ```

   Another provider from the pinned provider table is acceptable. A missing
   credential produces `SKIP`; any `FAIL` or missing `agent_end` blocks T68.

10. Paste only the checker's PASS/SKIP/FAIL and `RPC envelope KINDS` lines into
    the result form. Review the applicable provider terms yourself, complete
    the judgment, and choose future Pi models. This form records an operator
    decision, not a legal conclusion and not an automatic model-profile edit.

## Result form

- Operator:
- Date/time and timezone:
- `pi --version` output:
- Scratch directory used:

### Anthropic subscription lane

- `/login` → **Claude Pro/Max** completed: yes / no
- Fable-family listed: yes / no
- Exact Fable-family provider/model IDs:
- Selected candidate:
- Thinking labels observed in cycle order:
- xhigh-equivalent label: xhigh / max / other / none
- Notes (no credentials):

### OpenAI subscription lane

- `/login` → **ChatGPT Plus/Pro (Codex)** completed: yes / no
- GPT-5.6 family listed: yes / no
- Exact GPT-5.6 provider/model IDs:
- Selected candidate:
- Thinking labels observed in cycle order:
- xhigh-equivalent label: xhigh / max / other / none
- Notes (no credentials):

### Operator terms-of-use judgment

- Anthropic third-party harness/extra-usage terms reviewed: yes / no
- OpenAI ChatGPT subscription/Codex terms reviewed: yes / no
- Comfortable proceeding with Pi for this experiment: yes / no
- Constraints or rationale (no account data or credentials):

### Future `model_profiles.pi` choices

These are proposed values for a later task; do not edit the manifest during
T67.

| Profile | Provider | Exact model ID | Thinking level | Rationale |
| --- | --- | --- | --- | --- |
| express |  |  |  |  |
| standard |  |  |  |  |
| review |  |  |  |  |
| deep |  |  |  |  |
| security |  |  |  |  |

### Headless gate for T68

- `PI_CHECK_PROVIDER` (name only):
- `PI_CHECK_MODEL`:
- Documented credential variable name (never its value):
- Checker transcript:

  ```text
  PASTE PASS/SKIP/FAIL AND RPC envelope KINDS LINES ONLY
  ```

- Headless RPC `agent_end`: PASS / FAIL / SKIP
- T68 gate: OPEN / BLOCKED
- If blocked, non-secret reason:

## Extension-load evidence rationale

The checker passes the deployed `permgate.ts` through Pi's explicit
`--extension` option for both model calls. In pinned v0.84.1, the extension
loader imports the module and awaits its factory before returning success;
startup collects loader errors as fatal diagnostics and exits with status 1.
Therefore a completed RPC prompt through `agent_end` is a positive load signal
for the explicitly named file, while a load failure cannot be reported as a
successful check. See the pinned
[loader implementation](https://github.com/earendil-works/pi/blob/v0.84.1/packages/coding-agent/src/core/extensions/loader.ts#L490-L515)
and [startup diagnostic gate](https://github.com/earendil-works/pi/blob/v0.84.1/packages/coding-agent/src/main.ts#L784-L902).
