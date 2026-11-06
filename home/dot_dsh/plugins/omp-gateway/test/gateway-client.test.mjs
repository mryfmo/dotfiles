import assert from 'node:assert/strict'
import { EventEmitter } from 'node:events'
import { mkdtempSync, readFileSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { createInterface } from 'node:readline'
import { PassThrough } from 'node:stream'
import { test } from 'node:test'
import { fileURLToPath } from 'node:url'
import { GatewayClient, GatewayError, pickEnv } from '../gateway-client.mjs'

const stub = fileURLToPath(new URL('../stub-gateway.mjs', import.meta.url))
const fixturesPath = fileURLToPath(new URL('../fixtures.json', import.meta.url))
const fixtures = JSON.parse(readFileSync(fixturesPath, 'utf8'))
const scratch = mkdtempSync(join(tmpdir(), 'omp-gateway-client-test-'))
let logs = 0

function stubClient(t, extraArgs = [], options = {}) {
  const log = join(scratch, `stub-${logs += 1}.log`)
  const client = new GatewayClient({
    command: process.execPath,
    args: [stub, '--fixtures', fixturesPath, '--log', log, ...extraArgs],
    env: pickEnv(['PATH']),
    readyTimeoutMs: 5000,
    ...options,
  })
  t.after(() => client.close())
  return { client, log }
}

async function until(predicate, label, timeoutMs = 5000) {
  const deadline = Date.now() + timeoutMs
  while (!predicate()) {
    if (Date.now() > deadline) throw new Error(`timed out waiting for ${label}`)
    await new Promise(resolve => setTimeout(resolve, 10))
  }
}

function alive(pid) {
  try {
    process.kill(pid, 0)
    return true
  } catch {
    return false
  }
}

/**
 * In-process children for the respawn and protocol-guard tests: each spawn prints the ready line (unless
 * `ready: false`), records the request lines it is written, and delivers `close` one macrotask after a kill, as a
 * real process does, so the window between the kill and the close is open to the next request.
 */
function fakeSpawn({ ready = true } = {}) {
  const children = []
  const spawn = () => {
    const child = Object.assign(new EventEmitter(), {
      pid: 1000 + children.length + 1,
      stdin: new PassThrough(),
      stdout: new PassThrough(),
      stderr: new PassThrough(),
      lines: [],
      killedWith: undefined,
      kill(signal) {
        this.killedWith = signal
        setImmediate(() => this.emit('close', null, signal))
        return true
      },
      reply(line) {
        this.stdout.write(`${JSON.stringify(line)}\n`)
      },
    })
    createInterface({ input: child.stdin }).on('line', line => child.lines.push(JSON.parse(line)))
    child.stdin.on('finish', () => setImmediate(() => child.emit('close', 0, null)))
    if (ready) child.reply({ ready: true, version: 'fake' })
    children.push(child)
    return child
  }
  return { spawn, children }
}

function fakeClient(t) {
  const { spawn, children } = fakeSpawn()
  const client = new GatewayClient({ command: 'fake-gateway', env: {}, readyTimeoutMs: 1000, spawn })
  t.after(() => client.close())
  return { client, children }
}

test('the ready line is consumed and concurrent replies are matched by id', async t => {
  const { client, log } = stubClient(t)
  const [text, tool] = await Promise.all([
    client.request('/v1/messages', fixtures.requests.text),
    client.request('/v1/messages', fixtures.requests.tool_use),
  ])
  assert.equal(text.status, 200)
  assert.deepEqual(text.body, fixtures.replies.text.body)
  assert.deepEqual(tool.body, fixtures.replies.tool_use.body)
  assert.equal(client.pendingCount, 0)
  const answered = readFileSync(log, 'utf8').trim().split('\n').map(line => JSON.parse(line))
  assert.deepEqual(answered.map(row => [row.id, row.selector]), [[1, 'text'], [2, 'tool_use']])
  assert.equal(answered[0].lastUserText, 'Reply with the single word pong.')
})

test('one long-lived child answers many request lines in order', async t => {
  const { client } = stubClient(t)
  const first = await client.request('/v1/models', {})
  const pid = client.pid
  const second = await client.request('/v1/models', {})
  const third = await client.request('/v1/messages', fixtures.requests.text)
  assert.ok(Number.isInteger(pid))
  assert.equal(client.pid, pid)
  assert.equal(first.status, 200)
  assert.equal(second.status, 200)
  assert.ok(Array.isArray(first.body.data) && first.body.data.length > 0)
  assert.equal(third.body.content[0].text, 'pong')
})

test('the child exits at stdin EOF and the next request respawns it', async t => {
  const { client } = stubClient(t)
  await client.request('/v1/messages', fixtures.requests.text)
  const pid = client.pid
  const exit = await client.close()
  assert.deepEqual(exit, { code: 0, signal: null })
  assert.equal(client.pid, undefined)
  await until(() => !alive(pid), 'the first child to be reaped')
  const again = await client.request('/v1/messages', fixtures.requests.text)
  assert.equal(again.status, 200)
  assert.notEqual(client.pid, pid)
})

test('an aborted signal kills the child and rejects the request with ABORTED', async t => {
  const { client } = stubClient(t, ['--sleep-ms', '10000'])
  const controller = new AbortController()
  const pending = client.request('/v1/messages', fixtures.requests.text, controller.signal)
  await until(() => client.pid !== undefined, 'the child to spawn')
  const pid = client.pid
  setTimeout(() => controller.abort(), 50)
  await assert.rejects(pending, error => error instanceof GatewayError && error.code === 'ABORTED')
  await until(() => client.pid === undefined && !alive(pid), 'the killed child to be reaped')
  assert.equal(client.pendingCount, 0)
})

test('an aborted request is followed by a fresh child on the next request', async t => {
  const { client, children } = fakeClient(t)
  const controller = new AbortController()
  const first = client.request('/v1/messages', fixtures.requests.text, controller.signal)
  await until(() => children[0]?.lines.length === 1, 'the first request to reach child 1')
  controller.abort()
  const second = client.request('/v1/messages', fixtures.requests.text)
  await assert.rejects(first, { code: 'ABORTED' })
  assert.equal(children.length, 2)
  assert.equal(children[0].killedWith, 'SIGTERM')
  await until(() => children[1].lines.length === 1, 'the second request to reach child 2')
  assert.equal(children[0].lines.length, 1)
  children[1].reply({ id: children[1].lines[0].id, status: 200, body: { from: 'child 2' } })
  assert.deepEqual(await second, { status: 200, body: { from: 'child 2' } })
  assert.equal(client.pid, children[1].pid)
  assert.equal(client.pendingCount, 0)
})

test('a protocol failure is followed by a fresh child on the next request', async t => {
  const { client, children } = fakeClient(t)
  const first = client.request('/v1/messages', fixtures.requests.text)
  await until(() => children[0]?.lines.length === 1, 'the first request to reach child 1')
  children[0].reply({ id: children[0].lines[0].id + 100, status: 200, body: {} })
  await assert.rejects(first, { code: 'PROTOCOL' })
  const second = client.request('/v1/messages', fixtures.requests.text)
  assert.equal(children.length, 2)
  assert.equal(children[0].killedWith, 'SIGTERM')
  await until(() => children[1].lines.length === 1, 'the second request to reach child 2')
  assert.equal(children[0].lines.length, 1)
  children[1].reply({ id: children[1].lines[0].id, status: 200, body: { from: 'child 2' } })
  assert.deepEqual(await second, { status: 200, body: { from: 'child 2' } })
  assert.equal(client.pid, children[1].pid)
})

for (const [guard, raw] of [
  ['a non-JSON line', 'not json at all'],
  ['an array line', '[]'],
  ['a string line', '"x"'],
  ['a reply line without a status', '{"id":1,"body":{}}'],
]) {
  test(`${guard} from the child is a protocol failure that kills the child`, async t => {
    const { client, children } = fakeClient(t)
    const pending = client.request('/v1/messages', fixtures.requests.text)
    await until(() => children[0]?.lines.length === 1, 'the request to reach the child')
    children[0].stdout.write(`${raw}\n`)
    await assert.rejects(pending, error => error instanceof GatewayError && error.code === 'PROTOCOL')
    assert.equal(children[0].killedWith, 'SIGTERM')
    assert.equal(client.pid, undefined)
    assert.equal(client.pendingCount, 0)
  })
}

test('a reply line before the ready line is a protocol failure that kills the child', async t => {
  const { spawn, children } = fakeSpawn({ ready: false })
  const client = new GatewayClient({ command: 'fake-gateway', env: {}, readyTimeoutMs: 1000, spawn })
  t.after(() => client.close())
  const pending = client.request('/v1/messages', fixtures.requests.text)
  children[0].reply({ id: 1, status: 200, body: {} })
  await assert.rejects(pending, error => error instanceof GatewayError && error.code === 'PROTOCOL' && /ready line first/.test(error.message))
  assert.equal(children[0].killedWith, 'SIGTERM')
  assert.equal(client.pid, undefined)
})

test('a request whose signal is already aborted never spawns a child', async t => {
  const { client } = stubClient(t)
  const controller = new AbortController()
  controller.abort()
  await assert.rejects(client.request('/v1/messages', fixtures.requests.text, controller.signal), { code: 'ABORTED' })
  assert.equal(client.pid, undefined)
})

test('a child that never prints the ready line is killed after readyTimeoutMs', async t => {
  const { client } = stubClient(t, ['--no-ready'], { readyTimeoutMs: 300 })
  const pending = client.request('/v1/messages', fixtures.requests.text)
  await until(() => client.pid !== undefined, 'the child to spawn')
  const pid = client.pid
  await assert.rejects(pending, error => error instanceof GatewayError && error.code === 'NOT_READY')
  await until(() => client.pid === undefined && !alive(pid), 'the silent child to be reaped')
})

test('a reply line with a mismatched id is a protocol failure that kills the child', async t => {
  const { client } = stubClient(t, ['--reply-id-offset', '100'])
  const pending = client.request('/v1/messages', fixtures.requests.text)
  await until(() => client.pid !== undefined, 'the child to spawn')
  const pid = client.pid
  await assert.rejects(pending, error => error instanceof GatewayError && error.code === 'PROTOCOL' && /matches no pending request/.test(error.message))
  await until(() => client.pid === undefined && !alive(pid), 'the misbehaving child to be reaped')
})

test('a child that exits before replying rejects the pending request with its exit facts', async t => {
  const { client } = stubClient(t, ['--sleep-ms', '10000'])
  const pending = client.request('/v1/messages', fixtures.requests.text)
  await until(() => client.pid !== undefined, 'the child to spawn')
  process.kill(client.pid, 'SIGKILL')
  await assert.rejects(pending, error => error instanceof GatewayError && error.code === 'GATEWAY_EXIT' && /signal SIGKILL/.test(error.message))
})

test('a command that cannot be spawned rejects with SPAWN', async t => {
  const client = new GatewayClient({ command: join(scratch, 'no-such-gateway'), args: [], env: {}, readyTimeoutMs: 1000 })
  t.after(() => client.close())
  await assert.rejects(client.request('/v1/messages', fixtures.requests.text), error => error instanceof GatewayError && error.code === 'SPAWN')
  await until(() => client.pid === undefined, 'the failed spawn to be forgotten')
})

test('pickEnv copies only the named variables that exist', () => {
  assert.deepEqual(pickEnv(['A', 'B', 'C'], { A: '1', C: '3', D: '4' }), { A: '1', C: '3' })
})
