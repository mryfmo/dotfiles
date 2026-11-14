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

test('the model list names which rows were captured and which are derived, and every derived row stands in the list', () => {
  // U506b: the 2026-11-06 capture (U240) listed claude-fable-5-1; U506 replaced that row with the kit's model of
  // 2026-11-13, claude-fable-5-2, which no gateway had answered. The fixture says so under `derived`, beside the
  // capture note, so `measured` claims only what was measured.
  const ids = fixtures.replies.models.body.data.map(row => row.id)
  const derived = fixtures.derived?.models
  assert.equal(typeof derived?.note, 'string', 'derived.models.note says where the rows come from')
  assert.match(derived.note, /not captured/, 'the note says the rows were not captured')
  assert.ok(Array.isArray(derived.rows) && derived.rows.length > 0, 'derived.models.rows names the rows')
  for (const id of derived.rows) assert.ok(ids.includes(id), `${id} stands in the model list`)
  assert.ok(derived.rows.length < ids.length, 'at least one row is the captured one')
  assert.match(fixtures.measured.models, /derived/, 'the capture note points at the derived rows')
})

test('parseFlags reads the fixtures, log and fault knobs and refuses unknown flags', () => {
  const flags = parseFlags(['--fixtures', '/f.json', '--log', '/l.log', '--no-ready', '--reply-id-offset', '7', '--sleep-ms', '20'])
  assert.deepEqual(flags, { fixtures: '/f.json', log: '/l.log', noReady: true, replyIdOffset: 7, sleepMs: 20 })
  assert.throws(() => parseFlags(['--bogus']), /unknown flag --bogus/)
  assert.throws(() => parseFlags(['--log']), /--log needs a value/)
})
