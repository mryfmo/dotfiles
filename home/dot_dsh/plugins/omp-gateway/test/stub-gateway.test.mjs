import assert from 'node:assert/strict'
import { readFileSync } from 'node:fs'
import { test } from 'node:test'
import { parseFlags, selectReply } from '../stub-gateway.mjs'

const fixtures = JSON.parse(readFileSync(new URL('../fixtures.json', import.meta.url), 'utf8'))
const model = fixtures.knownModels[0]

test('selectReply keys the measured replies on path, model and the last user content', () => {
  const cases = [
    [{ id: 1, path: '/v1/models' }, 'models'],
    [{ id: 1, path: '/v1/other', body: {} }, 'unknown_path'],
    [{ id: 1, path: '/v1/messages', body: { model: 'openai-siwc/gpt-6-astra', messages: [] } }, 'unknown_model'],
    [{ id: 1, path: '/v1/messages', body: fixtures.requests.text }, 'text'],
    [{ id: 2, path: '/v1/messages', body: fixtures.requests.tool_use }, 'tool_use'],
    [{ id: 3, path: '/v1/messages', body: { model, tools: [], messages: [{ role: 'user', content: 'Call the ping tool now.' }] } }, 'text'],
    [{ id: 4, path: '/v1/messages', body: { model, tools: [{ name: 'ping' }], messages: [
      { role: 'user', content: [{ type: 'text', text: 'Call the ping tool with word=pong and nothing else.' }] },
      { role: 'assistant', content: [{ type: 'tool_use', id: 'toolu_1', name: 'ping', input: { word: 'pong' } }] },
      { role: 'user', content: [{ type: 'tool_result', tool_use_id: 'toolu_1', content: 'host' }] },
    ] } }, 'text'],
  ]
  for (const [request, expected] of cases) assert.equal(selectReply(request, fixtures), expected, JSON.stringify(request))
})

test('every selector names a fixture reply with a status and a body', () => {
  for (const key of ['models', 'unknown_path', 'unknown_model', 'text', 'tool_use']) {
    assert.ok(Number.isInteger(fixtures.replies[key].status), key)
    assert.ok(fixtures.replies[key].body !== undefined, key)
  }
})

test('parseFlags reads the fixtures, log and fault knobs and refuses unknown flags', () => {
  const flags = parseFlags(['--fixtures', '/f.json', '--log', '/l.log', '--no-ready', '--reply-id-offset', '7', '--sleep-ms', '20'])
  assert.deepEqual(flags, { fixtures: '/f.json', log: '/l.log', noReady: true, replyIdOffset: 7, sleepMs: 20 })
  assert.throws(() => parseFlags(['--bogus']), /unknown flag --bogus/)
  assert.throws(() => parseFlags(['--log']), /--log needs a value/)
})
