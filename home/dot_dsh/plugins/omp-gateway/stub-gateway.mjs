/**
 * Stub `omp auth-gateway stdio`: prints the measured ready line, then answers each JSON request line from
 * `fixtures.json`. The reply is chosen by a selector over the request (path, model, the last user text, a
 * pending tool result), never by a model call.
 *
 * Flags: `--fixtures <path>` (default `fixtures.json` beside this file), `--log <path>` (one JSON line per
 * answered request; default stderr). Fault knobs for the client tests: `--no-ready` (never prints the ready
 * line), `--reply-id-offset <n>` (answers with a wrong id), `--sleep-ms <n>` (delays every reply).
 */
import { appendFileSync, readFileSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { createInterface } from 'node:readline'
import { fileURLToPath } from 'node:url'

const here = dirname(fileURLToPath(import.meta.url))

/**
 * Pick the fixture key one request is answered with.
 * @param {{path?: string, body?: any}} request one parsed request line.
 * @param {{knownModels: string[]}} fixtures the loaded fixtures file.
 * @returns {'models' | 'unknown_path' | 'unknown_model' | 'text' | 'tool_use'}
 */
export function selectReply(request, fixtures) {
  const { path, body } = request
  if (path === '/v1/models') return 'models'
  if (path !== '/v1/messages') return 'unknown_path'
  if (!fixtures.knownModels.includes(body?.model)) return 'unknown_model'
  const blocks = lastContent(body)
  // The loop's follow-up after a tool call carries the tool result; the measured text reply ends that turn.
  if (blocks.some(block => block.type === 'tool_result')) return 'text'
  const text = blocks.filter(block => block.type === 'text').map(block => block.text).join('\n')
  if (/\bping tool\b/i.test(text) && Array.isArray(body.tools) && body.tools.length > 0) return 'tool_use'
  return 'text'
}

/** The last user text of a request, for the log line. */
export function lastUserText(body) {
  return lastContent(body).filter(block => block.type === 'text').map(block => block.text).join('\n')
}

function lastContent(body) {
  const last = Array.isArray(body?.messages) ? body.messages[body.messages.length - 1] : undefined
  if (last === undefined) return []
  if (typeof last.content === 'string') return [{ type: 'text', text: last.content }]
  return Array.isArray(last.content) ? last.content : []
}

/** Parse the stub's own flags. */
export function parseFlags(argv) {
  const flags = { fixtures: join(here, 'fixtures.json'), log: undefined, noReady: false, replyIdOffset: 0, sleepMs: 0 }
  for (let index = 0; index < argv.length; index += 1) {
    const flag = argv[index]
    const value = () => {
      index += 1
      if (index >= argv.length) throw new Error(`stub-gateway: ${flag} needs a value`)
      return argv[index]
    }
    if (flag === '--fixtures') flags.fixtures = value()
    else if (flag === '--log') flags.log = value()
    else if (flag === '--no-ready') flags.noReady = true
    else if (flag === '--reply-id-offset') flags.replyIdOffset = Number(value())
    else if (flag === '--sleep-ms') flags.sleepMs = Number(value())
    else throw new Error(`stub-gateway: unknown flag ${flag}`)
  }
  return flags
}

function main(argv) {
  const flags = parseFlags(argv)
  const fixtures = JSON.parse(readFileSync(flags.fixtures, 'utf8'))
  const log = record => {
    const line = `${JSON.stringify(record)}\n`
    if (flags.log === undefined) process.stderr.write(line)
    else appendFileSync(flags.log, line)
  }
  const reply = line => process.stdout.write(`${JSON.stringify(line)}\n`)
  const emit = line => (flags.sleepMs > 0 ? setTimeout(() => reply(line), flags.sleepMs) : reply(line))
  if (!flags.noReady) reply(fixtures.ready)
  createInterface({ input: process.stdin, crlfDelay: Infinity }).on('line', text => {
    if (text.trim().length === 0) return
    let request
    try {
      request = JSON.parse(text)
    } catch {
      // The real gateway's answer to a malformed line is unmeasured; the stub answers 400 so the client sees a reply.
      emit({ id: null, status: 400, body: { error: 'stub-gateway: invalid JSON line' } })
      return
    }
    const selector = selectReply(request, fixtures)
    const chosen = fixtures.replies[selector]
    log({ at: new Date().toISOString(), id: request.id, path: request.path, model: request.body?.model, selector, lastUserText: lastUserText(request.body).slice(0, 160) })
    emit({ id: request.id + flags.replyIdOffset, status: chosen.status, body: chosen.body })
  })
}
if (process.argv[1] !== undefined && fileURLToPath(import.meta.url) === process.argv[1]) main(process.argv.slice(2))
