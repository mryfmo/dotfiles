import assert from 'node:assert/strict'
import { EventEmitter } from 'node:events'
import { mkdtempSync, readFileSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { createInterface } from 'node:readline'
import { PassThrough } from 'node:stream'
import { test } from 'node:test'
import { fileURLToPath } from 'node:url'
import { DEFAULT_ENV_NAMES, resolveConfig } from '../config.mjs'
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

/**
 * A fake `omp` that records: it prints the ready line and answers every request with the sorted names of its own
 * environment, so a test reads exactly what the child was spawned with. Darwin's libc adds `__CF_USER_TEXT_ENCODING`
 * to every child; it is no row of the plugin's and is dropped here.
 */
const RECORDER = [
  "import { createInterface } from 'node:readline'",
  "const out = line => process.stdout.write(JSON.stringify(line) + String.fromCharCode(10))",
  "out({ ready: true, version: 'recorder' })",
  "createInterface({ input: process.stdin }).on('line', text => {",
  '  const { id } = JSON.parse(text)',
  "  out({ id, status: 200, body: { env: Object.keys(process.env).filter(name => !name.startsWith('__CF_')).sort() } })",
  '})',
].join('\n')

async function recordedChildEnv(t, source, names = DEFAULT_ENV_NAMES) {
  const client = new GatewayClient({
    command: process.execPath,
    args: ['--input-type=module', '-e', RECORDER],
    env: pickEnv(names, source),
    readyTimeoutMs: 5000,
  })
  t.after(() => client.close())
  const reply = await client.request('/v1/messages', {})
  return reply.body.env
}

test('the child carries OMP_PROFILE when the plugin has it and not when it is unset', async t => {
  // The hcom-seat dsh role exports OMP_PROFILE=dsh (U272); the child must live in that profile, not the denied default.
  const launcher = { HOME: '/Users/operator', PATH: process.env.PATH, USER: 'operator', NOT_A_ROW: 'x' }
  assert.deepEqual(await recordedChildEnv(t, { ...launcher, OMP_PROFILE: 'dsh' }), ['HOME', 'OMP_PROFILE', 'PATH', 'USER'])
  assert.deepEqual(await recordedChildEnv(t, launcher), ['HOME', 'PATH', 'USER'])
})

test('the child carries CLAUDE_CONFIG_DIR when the launcher exported it and not when config.env omits it', async t => {
  // hcom-seat hands the dsh role CLAUDE_CONFIG_DIR=<seats-root>/.state/claude (U318) and denies ~/.claude; the bridge's
  // Claude child finds the seat login only through this name (U355, row g6). A config.env row that omits it still wins.
  const launcher = { HOME: '/Users/operator', PATH: process.env.PATH, USER: 'operator', CLAUDE_CONFIG_DIR: '/scratch/login', NOT_A_ROW: 'x' }
  assert.deepEqual(await recordedChildEnv(t, launcher), ['CLAUDE_CONFIG_DIR', 'HOME', 'PATH', 'USER'])
  const narrowed = resolveConfig({ env: ['HOME', 'PATH', 'USER'] })
  assert.deepEqual(await recordedChildEnv(t, launcher, narrowed.env), ['HOME', 'PATH', 'USER'])
})

/**
 * Every name srt injects into the child it sandboxes, read from @anthropic-ai/sandbox-runtime 0.0.81
 * `dist/sandbox/sandbox-utils.js` `generateProxyEnvVars` (:667-838): the runtime mark (:680), `TMPDIR` (:691), the
 * `CA_TRUST_VARS` (:649-665, pushed :698), the proxy names (:720-727, :749-750, :759-760), `GIT_CONFIG_PARAMETERS`
 * (:732) and the SOCKS branch (:785-830). The list is kept here, apart from `config.mjs`, so the boundary is pinned
 * by a source the plugin does not read.
 */
const SRT_INJECTED_NAMES = [
  'SANDBOX_RUNTIME', 'TMPDIR',
  'NODE_EXTRA_CA_CERTS', 'SSL_CERT_FILE', 'CURL_CA_BUNDLE', 'REQUESTS_CA_BUNDLE', 'PIP_CERT', 'GIT_SSL_CAINFO',
  'AWS_CA_BUNDLE', 'CARGO_HTTP_CAINFO', 'DENO_CERT', 'CLOUDSDK_CORE_CUSTOM_CA_CERTS_FILE', 'NIX_SSL_CERT_FILE',
  'NO_PROXY', 'no_proxy', 'HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy', 'GIT_CONFIG_PARAMETERS',
  'ALL_PROXY', 'all_proxy', 'GRPC_PROXY', 'grpc_proxy',
  'SRT_SSH_PROXY_COMMAND', 'GIT_SSH_COMMAND', 'FTP_PROXY', 'ftp_proxy', 'RSYNC_PROXY',
  'DOCKER_HTTP_PROXY', 'DOCKER_HTTPS_PROXY',
  'CLOUDSDK_PROXY_TYPE', 'CLOUDSDK_PROXY_ADDRESS', 'CLOUDSDK_PROXY_PORT', 'CLOUDSDK_PROXY_USERNAME', 'CLOUDSDK_PROXY_PASSWORD',
]

test('the child carries every name srt injects when the launcher holds them and not when config.env omits them', async t => {
  // Under srt the sandbox reaches the network through the proxy srt starts, and srt tells its child so only through
  // these names; a gateway child without them resolves DNS directly, which the sandbox denies (U364, row g6:
  // `network-outbound /private/var/run/mDNSResponder`). A config.env row that omits them still wins.
  const launcher = { HOME: '/Users/operator', PATH: process.env.PATH, USER: 'operator', NOT_A_ROW: 'x' }
  for (const name of SRT_INJECTED_NAMES) launcher[name] = `srt:${name}`
  assert.deepEqual(await recordedChildEnv(t, launcher), [...SRT_INJECTED_NAMES, 'HOME', 'PATH', 'USER'].sort())
  const narrowed = resolveConfig({ env: ['HOME', 'PATH', 'USER'] })
  assert.deepEqual(await recordedChildEnv(t, launcher, narrowed.env), ['HOME', 'PATH', 'USER'])
})
