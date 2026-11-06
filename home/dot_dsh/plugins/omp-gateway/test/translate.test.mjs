import assert from 'node:assert/strict'
import { readFileSync } from 'node:fs'
import { test } from 'node:test'
import { toChunks, toError, toMessagesBody, TranslationError } from '../translate.mjs'

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

test('toMessagesBody maps a loop-built history: system row, tool call, tool result, developer row dropped', () => {
  const body = toMessagesBody({
    provider: 'claude-bridge',
    model: 'claude-haiku-5-5',
    messages: [
      { role: 'system', content: [{ type: 'text', text: 'You are a coding agent.' }] },
      { role: 'user', content: [{ type: 'text', text: 'Call the ping tool with word=pong and nothing else.' }] },
      { role: 'developer', content: [{ type: 'tool-addition', toolName: 'ping' }] },
      { role: 'assistant', content: [{ type: 'tool-call', id: 'toolu_1', name: 'ping', arguments: '{"word":"pong"}' }] },
      { role: 'tool', toolCallId: 'toolu_1', content: [{ type: 'text', text: 'pong from host' }] },
      { role: 'tool', toolCallId: 'toolu_2', isError: true, content: [{ type: 'text', text: 'no such tool' }] },
    ],
  }, { maxTokens: 1234 })
  assert.equal(body.system, 'You are a coding agent.')
  assert.equal(body.max_tokens, 1234)
  assert.deepEqual(body.messages, [
    { role: 'user', content: [{ type: 'text', text: 'Call the ping tool with word=pong and nothing else.' }] },
    { role: 'assistant', content: [{ type: 'tool_use', id: 'toolu_1', name: 'ping', input: { word: 'pong' } }] },
    { role: 'user', content: [
      { type: 'tool_result', tool_use_id: 'toolu_1', content: 'pong from host' },
      { type: 'tool_result', tool_use_id: 'toolu_2', content: 'no such tool', is_error: true },
    ] },
  ])
})

test('toMessagesBody keeps a model id that already names its provider and forwards one-shot fields', () => {
  const body = toMessagesBody({
    provider: 'claude-bridge',
    model: 'claude-bridge/claude-haiku-5-5',
    system: 'Be terse.',
    temperature: 0.2,
    stop: ['END'],
    messages: [{ role: 'user', content: [{ type: 'text', text: 'hi' }, { type: 'image', attachment: {} }] }],
  })
  assert.equal(body.model, 'claude-bridge/claude-haiku-5-5')
  assert.equal(body.system, 'Be terse.')
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
