/**
 * Pure translations between DSH's `LlmAdapter` vocabulary and the gateway's Anthropic messages
 * bodies. No process code lives here; `GatewayClient` owns the child and parses its lines.
 */

/**
 * Tag of the text block that carries DSH's system text inside the first user turn. One constant, so the test
 * and any later reader of a gateway line share the name with the writer.
 */
export const SYSTEM_BLOCK_TAG = 'dsh-system'

/**
 * Map one DSH request into an Anthropic messages body.
 * @param {object} options DSH `GenerateOptions`: provider, model, messages, system, tools, maxTokens, temperature, stop.
 * @param {{maxTokens?: number}} [defaults] plugin-level fallbacks for fields the request leaves unset.
 * @returns {object} the body of one `{"path":"/v1/messages"}` gateway line. It never carries `system`: see {@link foldSystem}.
 */
export function toMessagesBody(options, defaults = {}) {
  const system = []
  if (typeof options.system === 'string' && options.system.length > 0) system.push(options.system)
  const messages = []
  for (const message of options.messages ?? []) {
    switch (message.role) {
      case 'system': {
        const text = textOf(message.content)
        if (text.length > 0) system.push(text)
        break
      }
      case 'user':
        append(messages, 'user', userContent(message.content))
        break
      case 'assistant':
        append(messages, 'assistant', assistantContent(message.content))
        break
      case 'tool':
        append(messages, 'user', [toolResult(message)])
        break
      default:
        // Developer rows carry tool bookkeeping the gateway never sees; the request's `tools` field is complete.
        break
    }
  }
  const body = {
    // The measured turns addressed the model as `<provider>/<model>`; a model id that already carries a slash is sent as is.
    model: options.model.includes('/') ? options.model : `${options.provider}/${options.model}`,
    max_tokens: options.maxTokens ?? defaults.maxTokens ?? 4096,
    messages,
  }
  if (system.length > 0) foldSystem(messages, system)
  if (Array.isArray(options.tools) && options.tools.length > 0) {
    body.tools = options.tools.map(tool => ({
      name: tool.name,
      description: tool.description,
      input_schema: tool.parameters,
    }))
  }
  if (typeof options.temperature === 'number') body.temperature = options.temperature
  if (Array.isArray(options.stop) && options.stop.length > 0) body.stop_sequences = [...options.stop]
  return body
}

/**
 * Map one Anthropic message into the DSH chunk sequence: per block `block-start`, one delta, `block-end`;
 * then `usage`, then `finish`.
 * @param {object} message the `body` of a status-200 gateway reply line.
 * @returns {Generator<object>} DSH `StreamChunk` values.
 */
export function* toChunks(message) {
  if (message === null || typeof message !== 'object' || !Array.isArray(message.content)) {
    throw new TranslationError('omp-gateway: gateway reply is not a message with a content array', 'INVALID_RESPONSE')
  }
  // DSH's taxonomy (`@deepseek-ai/dsh-llm` EMPTY_RESPONSE_CODE): an empty assistant message would end the turn with
  // nothing for the loop to act on, so a degenerate completion is a failure the retry policy may repeat.
  if (message.content.length === 0) {
    throw new TranslationError(`omp-gateway: gateway reply ${message.id ?? '(no id)'} carries no content blocks`, 'EMPTY_RESPONSE')
  }
  for (const [index, block] of message.content.entries()) {
    switch (block?.type) {
      case 'text':
        yield { type: 'block-start', index, blockType: 'text' }
        yield { type: 'text-delta', index, text: block.text }
        yield { type: 'block-end', index, block: { type: 'text', text: block.text } }
        break
      case 'thinking':
        yield { type: 'block-start', index, blockType: 'reasoning' }
        yield { type: 'reasoning-delta', index, text: block.thinking }
        yield { type: 'block-end', index, block: { type: 'reasoning', text: block.thinking } }
        break
      case 'tool_use': {
        const args = JSON.stringify(block.input ?? {})
        yield { type: 'block-start', index, blockType: 'tool-call' }
        yield { type: 'tool-call-delta', index, id: block.id, name: block.name, argumentsDelta: args }
        yield { type: 'block-end', index, block: { type: 'tool-call', id: block.id, name: block.name, arguments: args } }
        break
      }
      default:
        // A block kind the pinned seam has no vocabulary for is dropped rather than guessed at.
        break
    }
  }
  if (message.usage !== null && typeof message.usage === 'object') yield { type: 'usage', usage: toUsage(message.usage) }
  yield { type: 'finish', reason: toFinishReason(message.stop_reason) }
}

/**
 * Map a non-200 gateway reply into the adapter's failure record. The adapter turns it into an `LlmError`.
 * @param {number} status the reply's HTTP status.
 * @param {unknown} body the reply body: `{error: {message, type}}` or `{error: "<text>"}`.
 * @returns {{code: string, message: string, status: number}}
 */
export function toError(status, body) {
  const error = body !== null && typeof body === 'object' ? body.error : undefined
  const detail = typeof error === 'string'
    ? error
    : error !== null && typeof error === 'object' && typeof error.message === 'string'
      ? error.message
      : JSON.stringify(body)
  const type = error !== null && typeof error === 'object' && typeof error.type === 'string' ? error.type : ''
  return { code: codeFor(status, type), status, message: `omp-gateway: HTTP ${status}: ${detail}` }
}

/** Thrown by {@link toChunks} for a 200 reply whose body is not a message, or a message with no content blocks. */
export class TranslationError extends Error {
  constructor(message, code) {
    super(message)
    this.name = 'TranslationError'
    this.code = code
  }
}

const CODE_BY_TYPE = Object.freeze({
  authentication_error: 'AUTH',
  permission_error: 'AUTH',
  rate_limit_error: 'RATE_LIMIT',
  invalid_request_error: 'INVALID_REQUEST',
  not_found_error: 'INVALID_REQUEST',
  overloaded_error: 'SERVER',
  api_error: 'SERVER',
})

function codeFor(status, type) {
  if (Object.hasOwn(CODE_BY_TYPE, type)) return CODE_BY_TYPE[type]
  if (status === 401 || status === 403) return 'AUTH'
  if (status === 402) return 'QUOTA'
  if (status === 429) return 'RATE_LIMIT'
  if (status >= 500) return 'SERVER'
  return 'INVALID_REQUEST'
}

const STOP_REASONS = Object.freeze({
  tool_use: Object.freeze({ kind: 'tool-calls' }),
  max_tokens: Object.freeze({ kind: 'max-tokens' }),
})

function toFinishReason(stopReason) {
  return Object.hasOwn(STOP_REASONS, stopReason) ? STOP_REASONS[stopReason] : { kind: 'stop' }
}

function toUsage(usage) {
  const count = value => (Number.isFinite(value) ? value : 0)
  const inputTokens = count(usage.input_tokens)
  const outputTokens = count(usage.output_tokens)
  const result = { inputTokens, outputTokens }
  if (Number.isFinite(usage.cache_read_input_tokens)) result.cacheReadTokens = usage.cache_read_input_tokens
  if (Number.isFinite(usage.cache_creation_input_tokens)) result.cacheWriteTokens = usage.cache_creation_input_tokens
  result.totalTokens = inputTokens + outputTokens + (result.cacheReadTokens ?? 0) + (result.cacheWriteTokens ?? 0)
  return result
}

function append(messages, role, content) {
  if (content.length === 0) return
  const last = messages[messages.length - 1]
  // Anthropic alternates roles; consecutive same-role rows (a tool result after a tool result) share one message.
  if (last !== undefined && last.role === role) last.content.push(...content)
  else messages.push({ role, content })
}

/**
 * Prepend the collected system text to the first user turn as one tagged text block. The gateway's
 * pi-claude-bridge runs a request without `system` on Claude Code's preset prompt and throws on a `system` that
 * matches no prompt captured from a pi session (`prompt-capture.ts` `resolveOrDerive`); a DSH client has no pi
 * session, so `system` is never sent and the instructions travel here as the first thing the model reads.
 * The block is built from `options.system` and `system`-role rows only, never from user content.
 */
function foldSystem(messages, system) {
  const block = { type: 'text', text: `<${SYSTEM_BLOCK_TAG}>\n${system.join('\n\n')}\n</${SYSTEM_BLOCK_TAG}>` }
  const first = messages[0]
  if (first !== undefined && first.role === 'user') first.content.unshift(block)
  else messages.unshift({ role: 'user', content: [block] })
}

function textOf(blocks) {
  return (Array.isArray(blocks) ? blocks : [])
    .filter(block => block?.type === 'text' && typeof block.text === 'string')
    .map(block => block.text)
    .join('\n')
}

function userContent(blocks) {
  const content = []
  for (const block of Array.isArray(blocks) ? blocks : []) {
    if (block?.type === 'text') content.push({ type: 'text', text: block.text })
    else if (block?.type === 'image' || block?.type === 'file') content.push({ type: 'text', text: `[${block.type} attachment omitted]` })
  }
  return content
}

function assistantContent(blocks) {
  const content = []
  for (const block of Array.isArray(blocks) ? blocks : []) {
    if (block?.type === 'text' && block.text.length > 0) content.push({ type: 'text', text: block.text })
    else if (block?.type === 'tool-call') content.push({ type: 'tool_use', id: block.id, name: block.name, input: parseArguments(block.arguments) })
  }
  return content
}

function parseArguments(raw) {
  if (typeof raw !== 'string' || raw.trim().length === 0) return {}
  try {
    const parsed = JSON.parse(raw)
    return parsed !== null && typeof parsed === 'object' && !Array.isArray(parsed) ? parsed : {}
  } catch {
    // The arguments were emitted by toChunks from a JSON object; anything else is history the gateway cannot take.
    return {}
  }
}

function toolResult(message) {
  const result = { type: 'tool_result', tool_use_id: message.toolCallId, content: textOf(message.content) }
  if (message.isError === true) result.is_error = true
  return result
}
