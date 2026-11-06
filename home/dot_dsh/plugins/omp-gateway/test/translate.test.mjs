import assert from 'node:assert/strict'
import { readFileSync } from 'node:fs'
import { test } from 'node:test'
import { SYSTEM_BLOCK_TAG, toChunks, toError, toMessagesBody, TranslationError } from '../translate.mjs'

const fixtures = JSON.parse(readFileSync(new URL('../fixtures.json', import.meta.url), 'utf8'))

test('toMessagesBody reproduces the measured text request', () => {
  const body = toMessagesBody({
    provider: 'claude-bridge',
    model: 'claude-haiku-5-5',
    maxTokens: 32,
    messages: [{ role: 'user', content: [{ type: 'text', text: 'Reply with the single word pong.' }] }],
  })
  const measured = fixtures.requests.text
  assert.equal(body.model, measured.model)
  assert.equal(body.max_tokens, measured.max_tokens)
  assert.deepEqual(body.messages, [{ role: 'user', content: [{ type: 'text', text: measured.messages[0].content }] }])
  assert.equal(body.system, undefined)
  assert.equal(body.tools, undefined)
  assert.equal(body.stream, undefined)
})

test('toMessagesBody reproduces the measured tool declaration', () => {
  const body = toMessagesBody({
    provider: 'claude-bridge',
    model: 'claude-haiku-5-5',
    maxTokens: 32,
    tools: [{
      name: 'ping',
      description: 'Answer with the current host name of the caller.',
      parameters: { type: 'object', properties: { word: { type: 'string' } }, required: ['word'] },
    }],
    messages: [{ role: 'user', content: [{ type: 'text', text: 'Call the ping tool with word=pong and nothing else.' }] }],
  })
  assert.deepEqual(body.tools, fixtures.requests.tool_use.tools)
})

test('toMessagesBody maps a loop-built history: tool call, tool result, developer row dropped', () => {
  const body = toMessagesBody({
    provider: 'claude-bridge',
    model: 'claude-haiku-5-5',
    messages: [
      { role: 'user', content: [{ type: 'text', text: 'Call the ping tool with word=pong and nothing else.' }] },
      { role: 'developer', content: [{ type: 'tool-addition', toolName: 'ping' }] },
      { role: 'assistant', content: [{ type: 'tool-call', id: 'toolu_1', name: 'ping', arguments: '{"word":"pong"}' }] },
      { role: 'tool', toolCallId: 'toolu_1', content: [{ type: 'text', text: 'pong from host' }] },
      { role: 'tool', toolCallId: 'toolu_2', isError: true, content: [{ type: 'text', text: 'no such tool' }] },
    ],
  }, { maxTokens: 1234 })
  assert.equal(body.max_tokens, 1234)
  assert.deepEqual(body.messages, [
    { role: 'user', content: [{ type: 'text', text: 'Call the ping tool with word=pong and nothing else.' }] },
    { role: 'assistant', content: [{ role: undefined, type: 'tool_use', id: 'toolu_1', name: 'ping', input: { word: 'pong' } }].map(({ role, ...block }) => block) },
    { role: 'user', content: [
      { type: 'tool_result', tool_use_id: 'toolu_1', content: 'pong from host' },
      { type: 'tool_result', tool_use_id: 'toolu_2', content: 'no such tool', is_error: true },
    ] },
  ])
})

const systemBlock = text => ({ type: 'text', text: `<${SYSTEM_BLOCK_TAG}>\n${text}\n</${SYSTEM_BLOCK_TAG}>` })

test('toMessagesBody folds the system prompt into the first user turn as a tagged leading block and sends no system field', () => {
  const body = toMessagesBody({
    provider: 'claude-bridge',
    model: 'claude-haiku-5-5',
    system: 'You are a coding agent.',
    messages: [{ role: 'user', content: [{ type: 'text', text: 'Reply with the single word pong.' }] }],
  })
  assert.equal(SYSTEM_BLOCK_TAG, 'dsh-system')
  assert.equal(Object.hasOwn(body, 'system'), false)
  assert.deepEqual(body.messages, [{ role: 'user', content: [
    systemBlock('You are a coding agent.'),
    { type: 'text', text: 'Reply with the single word pong.' },
  ] }])
})

test('toMessagesBody inserts a user message holding the block alone when the history starts with an assistant turn', () => {
  const body = toMessagesBody({
    provider: 'claude-bridge',
    model: 'claude-haiku-5-5',
    system: 'You are a coding agent.',
    messages: [
      { role: 'assistant', content: [{ type: 'text', text: 'How can I help?' }] },
      { role: 'user', content: [{ type: 'text', text: 'Reply with the single word pong.' }] },
    ],
  })
  assert.equal(Object.hasOwn(body, 'system'), false)
  assert.deepEqual(body.messages, [
    { role: 'user', content: [systemBlock('You are a coding agent.')] },
    { role: 'assistant', content: [{ type: 'text', text: 'How can I help?' }] },
    { role: 'user', content: [{ type: 'text', text: 'Reply with the single word pong.' }] },
  ])
})

test('toMessagesBody sends the user message unchanged and no system field when the request has no system text', () => {
  const body = toMessagesBody({
    provider: 'claude-bridge',
    model: 'claude-haiku-5-5',
    system: '',
    messages: [{ role: 'user', content: [{ type: 'text', text: 'Reply with the single word pong.' }] }],
  })
  assert.equal(Object.hasOwn(body, 'system'), false)
  assert.deepEqual(body.messages, [{ role: 'user', content: [{ type: 'text', text: 'Reply with the single word pong.' }] }])
})

test('toMessagesBody folds a system-role message from the middle of the history into the same leading block, in order', () => {
  const body = toMessagesBody({
    provider: 'claude-bridge',
    model: 'claude-haiku-5-5',
    system: 'You are a coding agent.',
    messages: [
      { role: 'user', content: [{ type: 'text', text: 'hi' }] },
      { role: 'assistant', content: [{ type: 'text', text: 'hello' }] },
      { role: 'system', content: [{ type: 'text', text: 'Answer in one word.' }] },
      { role: 'user', content: [{ type: 'text', text: 'Reply with the single word pong.' }] },
    ],
  })
  assert.equal(Object.hasOwn(body, 'system'), false)
  assert.deepEqual(body.messages, [
    { role: 'user', content: [systemBlock('You are a coding agent.\n\nAnswer in one word.'), { type: 'text', text: 'hi' }] },
    { role: 'assistant', content: [{ type: 'text', text: 'hello' }] },
    { role: 'user', content: [{ type: 'text', text: 'Reply with the single word pong.' }] },
  ])
  assert.equal(body.messages.some(message => message.role === 'system'), false)
})

test('toMessagesBody keeps a model id that already names its provider and forwards one-shot fields', () => {
  const body = toMessagesBody({
    provider: 'claude-bridge',
    model: 'claude-bridge/claude-haiku-5-5',
    temperature: 0.2,
    stop: ['END'],
    messages: [{ role: 'user', content: [{ type: 'text', text: 'hi' }, { type: 'image', attachment: {} }] }],
  })
  assert.equal(body.model, 'claude-bridge/claude-haiku-5-5')
  assert.equal(body.temperature, 0.2)
  assert.deepEqual(body.stop_sequences, ['END'])
  assert.deepEqual(body.messages[0].content, [{ type: 'text', text: 'hi' }, { type: 'text', text: '[image attachment omitted]' }])
})

test('toChunks turns the measured text reply into text chunks, usage and a stop finish', () => {
  assert.deepEqual([...toChunks(fixtures.replies.text.body)], [
    { type: 'block-start', index: 0, blockType: 'text' },
    { type: 'text-delta', index: 0, text: 'pong' },
    { type: 'block-end', index: 0, block: { type: 'text', text: 'pong' } },
    { type: 'usage', usage: { inputTokens: 2, outputTokens: 4, cacheReadTokens: 0, cacheWriteTokens: 2453, totalTokens: 2459 } },
    { type: 'finish', reason: { kind: 'stop' } },
  ])
})

test('toChunks turns the measured tool_use reply into one whole-argument tool-call block and a tool-calls finish', () => {
  assert.deepEqual([...toChunks(fixtures.replies.tool_use.body)], [
    { type: 'block-start', index: 0, blockType: 'tool-call' },
    { type: 'tool-call-delta', index: 0, id: 'toolu_01HEFTqeaFVnJLV8YpvEypFV', name: 'ping', argumentsDelta: '{"word":"pong"}' },
    { type: 'block-end', index: 0, block: { type: 'tool-call', id: 'toolu_01HEFTqeaFVnJLV8YpvEypFV', name: 'ping', arguments: '{"word":"pong"}' } },
    { type: 'usage', usage: { inputTokens: 2, outputTokens: 57, cacheReadTokens: 0, cacheWriteTokens: 2923, totalTokens: 2982 } },
    { type: 'finish', reason: { kind: 'tool-calls' } },
  ])
})

test('toChunks maps max_tokens and an unknown stop reason, and rejects a body without content', () => {
  const chunks = [...toChunks({ content: [], stop_reason: 'max_tokens' })]
  assert.deepEqual(chunks, [{ type: 'finish', reason: { kind: 'max-tokens' } }])
  assert.deepEqual([...toChunks({ content: [], stop_reason: 'something_new' })], [{ type: 'finish', reason: { kind: 'stop' } }])
  assert.throws(() => [...toChunks({ error: 'nope' })], error => error instanceof TranslationError && error.code === 'INVALID_RESPONSE')
})

test('toError maps the measured unknown-model line', () => {
  const { status, body } = fixtures.replies.unknown_model
  assert.deepEqual(toError(status, body), {
    code: 'INVALID_REQUEST',
    status: 404,
    message: 'omp-gateway: HTTP 404: No available model matches "openai-siwc/gpt-6-astra"',
  })
})

test('toError maps the measured unknown-path line', () => {
  const { status, body } = fixtures.replies.unknown_path
  assert.deepEqual(toError(status, body), { code: 'INVALID_REQUEST', status: 404, message: 'omp-gateway: HTTP 404: No route: POST /v1/models' })
})

test('toError maps the rest of the status taxonomy', () => {
  assert.equal(toError(401, { error: 'login required' }).code, 'AUTH')
  assert.equal(toError(402, {}).code, 'QUOTA')
  assert.equal(toError(429, { error: { message: 'slow down', type: 'rate_limit_error' } }).code, 'RATE_LIMIT')
  assert.equal(toError(503, { error: { message: 'busy', type: 'overloaded_error' } }).code, 'SERVER')
  assert.equal(toError(500, 'plain text').message, 'omp-gateway: HTTP 500: "plain text"')
})
