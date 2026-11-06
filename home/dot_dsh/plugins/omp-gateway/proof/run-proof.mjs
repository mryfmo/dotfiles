#!/usr/bin/env node
/**
 * Composition proof: a scratch `DSH_HOME`, a scratch profile that links this plugin (and the ping tool) the way
 * `dsh plugin add link:<dir>` would, and two headless `dsh` turns against the stub gateway.
 *
 * Usage: node proof/run-proof.mjs [--home <dir>] [--dsh <path>] [--command <cmd>] [--args <json list>] [--cwd <dir>]
 *   --command omp --args '["auth-gateway","stdio"]' runs the same two turns against the real gateway.
 */
import { spawnSync } from 'node:child_process'
import { existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, symlinkSync, writeFileSync } from 'node:fs'
import { homedir, tmpdir } from 'node:os'
import { dirname, join, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const proofDir = dirname(fileURLToPath(import.meta.url))
const pluginDir = resolve(proofDir, '..')
const pingToolDir = join(proofDir, 'ping-tool')
const flags = parseFlags(process.argv.slice(2))
const home = flags.home ?? mkdtempSync(join(tmpdir(), 'u240-dsh-home-'))
const profileDir = join(home, 'profiles', 'omp-proof')
const cwd = join(home, 'cwd')
const stubLog = join(home, 'stub.log')
const dsh = flags.dsh ?? join(homedir(), '.dsh', 'bin', 'dsh')
const command = flags.command ?? process.execPath
const args = flags.args ?? [join(pluginDir, 'stub-gateway.mjs'), '--fixtures', join(pluginDir, 'fixtures.json'), '--log', stubLog]

mkdirSync(join(profileDir, 'node_modules'), { recursive: true })
mkdirSync(cwd, { recursive: true })
rmSync(stubLog, { force: true })
link(join(profileDir, 'node_modules', 'dsh-omp-gateway'), pluginDir)
link(join(profileDir, 'node_modules', 'u240-ping-tool'), pingToolDir)
writeFileSync(join(profileDir, 'package.json'), `${JSON.stringify({
  name: 'dsh-profile-omp-proof',
  private: true,
  dsh: { manifestVersion: 1, profile: { bundles: ['@deepseek-ai/dsh-base', '@deepseek-ai/dsh-headless'] } },
  dependencies: { 'dsh-omp-gateway': `link:${pluginDir}`, 'u240-ping-tool': `link:${pingToolDir}` },
}, null, 2)}\n`)
// YAML reads JSON, so the patch layer is written as JSON to keep the quoting exact.
const patch = [
  { id: 'llm-deepseek', disabled: true },
  { id: 'llm-deepseek-account', disabled: true },
  { id: 'bash-sandbox', disabled: true },
  { id: 'session-log-deepseek', config: { enabled: false } },
  { id: 'agent-default-model', config: { provider: 'claude-bridge', model: 'claude-haiku-5-5' } },
  { insert: [{ id: 'omp-gateway', name: 'dsh-omp-gateway', config: { command, args, env: ['HOME', 'PATH'], ...flags.cwd === undefined ? {} : { cwd: flags.cwd } } }] },
]
writeFileSync(join(profileDir, 'cordis.patch.yml'), `${JSON.stringify(patch, null, 2)}\n`)

console.log(`DSH_HOME=${home}`)
console.log(`profile=${profileDir}`)
console.log(`gateway command=${command} args=${JSON.stringify(args)}`)
console.log(`dsh=${dsh} cwd=${cwd}`)

const pong = turn('turn 1: pong', ['--profile', 'omp-proof', 'Reply with the single word pong.'])
const ping = turn('turn 2: ping tool (--json)', ['--profile', 'omp-proof', '--patch', join(proofDir, 'ping-tool.patch.yml'), '--json', 'Call the ping tool with word=pong and nothing else.'])

console.log('\n=== stub log (one line per answered request) ===')
console.log(existsSync(stubLog) ? readFileSync(stubLog, 'utf8').trimEnd() : '(no stub log: the gateway was not the stub)')
process.exitCode = pong.status === 0 && ping.status === 0 ? 0 : 1

function turn(title, dshArgs) {
  console.log(`\n=== ${title} ===`)
  console.log(`$ DSH_HOME=${home} ${dsh} ${dshArgs.map(quote).join(' ')}`)
  const result = spawnSync(dsh, dshArgs, { cwd, env: { ...process.env, DSH_HOME: home }, encoding: 'utf8', timeout: 180_000 })
  writeFileSync(join(home, `${title.split(':')[0].replace(/\s+/g, '-')}.stdout`), result.stdout ?? '')
  writeFileSync(join(home, `${title.split(':')[0].replace(/\s+/g, '-')}.stderr`), result.stderr ?? '')
  console.log('--- stdout ---')
  console.log((result.stdout ?? '').trimEnd())
  console.log('--- stderr ---')
  console.log((result.stderr ?? '').trimEnd())
  console.log(`--- exit ${result.status} ${result.signal ?? ''} ${result.error ? result.error.message : ''}`.trimEnd())
  return result
}

function link(path, target) {
  rmSync(path, { force: true })
  symlinkSync(target, path)
}

function quote(arg) {
  return /^[\w./=-]+$/.test(arg) ? arg : `'${arg.replace(/'/g, "'\\''")}'`
}

function parseFlags(argv) {
  const parsed = { home: undefined, dsh: undefined, command: undefined, args: undefined, cwd: undefined }
  for (let index = 0; index < argv.length; index += 1) {
    const flag = argv[index]
    const value = argv[index + 1]
    if (value === undefined) throw new Error(`run-proof: ${flag} needs a value`)
    index += 1
    if (flag === '--home') parsed.home = resolve(value)
    else if (flag === '--dsh') parsed.dsh = resolve(value)
    else if (flag === '--command') parsed.command = value
    else if (flag === '--args') parsed.args = JSON.parse(value)
    else if (flag === '--cwd') parsed.cwd = resolve(value)
    else throw new Error(`run-proof: unknown flag ${flag}`)
  }
  return parsed
}
