/**
 * The process boundary. One `GatewayClient` owns one long-lived gateway child (`omp auth-gateway stdio`),
 * writes one JSON line per request keyed by an increasing id, and resolves the reply line with the same id.
 * The child's stdout is parsed here exactly once; nothing downstream looks at its text.
 */
import { spawn as spawnChild } from 'node:child_process'
import { createInterface } from 'node:readline'

const STDERR_TAIL_BYTES = 4096

/** A failure of the boundary itself: spawning, readiness, protocol, exit or abort. `code` is DSH's taxonomy. */
export class GatewayError extends Error {
  constructor(message, code, options) {
    super(message, options)
    this.name = 'GatewayError'
    this.code = code
  }
}

/**
 * Copy the named variables out of an environment.
 * @param {readonly string[]} names
 * @param {Record<string, string | undefined>} [source]
 * @returns {Record<string, string>}
 */
export function pickEnv(names, source = process.env) {
  const env = {}
  for (const name of names) {
    const value = source[name]
    if (typeof value === 'string') env[name] = value
  }
  return env
}

export class GatewayClient {
  #command
  #args
  #env
  #cwd
  #readyTimeoutMs
  #spawn
  #child
  #ready
  #gate
  #pending = new Map()
  #nextId = 1
  #stderr = ''

  /**
   * @param {{command: string, args?: readonly string[], env?: Record<string, string>, cwd?: string, readyTimeoutMs?: number, spawn?: typeof spawnChild}} options
   */
  constructor({ command, args = [], env = {}, cwd, readyTimeoutMs = 30_000, spawn = spawnChild }) {
    this.#command = command
    this.#args = [...args]
    this.#env = { ...env }
    this.#cwd = cwd
    this.#readyTimeoutMs = readyTimeoutMs
    this.#spawn = spawn
  }

  /** Process id of the live child, or `undefined` when none is running. */
  get pid() {
    return this.#child?.pid
  }

  /** Requests written or queued whose reply line has not arrived. */
  get pendingCount() {
    return this.#pending.size
  }

  /**
   * Send one request line and resolve its reply line.
   * @param {string} path the gateway route, `/v1/messages` for a model turn.
   * @param {unknown} body the JSON body of the line.
   * @param {AbortSignal} [signal] aborting kills the child and rejects every pending request with code `ABORTED`.
   * @returns {Promise<{status: number, body: unknown}>}
   */
  request(path, body, signal) {
    return new Promise((resolve, reject) => {
      if (signal?.aborted) {
        reject(abortedError())
        return
      }
      let settled = false
      const settle = (done, value) => {
        if (settled) return
        settled = true
        signal?.removeEventListener('abort', onAbort)
        done(value)
      }
      const onAbort = () => {
        this.#fail(abortedError())
        this.#kill()
      }
      signal?.addEventListener('abort', onAbort, { once: true })
      let child
      try {
        child = this.#ensureChild()
      } catch (error) {
        settle(reject, new GatewayError(`omp-gateway: cannot spawn ${this.#command}: ${error.message}`, 'SPAWN', { cause: error }))
        return
      }
      const id = this.#nextId++
      this.#pending.set(id, { resolve: value => settle(resolve, value), reject: error => settle(reject, error) })
      this.#ready.then(
        () => {
          if (!settled) child.stdin.write(`${JSON.stringify({ id, path, body })}\n`)
        },
        error => {
          this.#pending.delete(id)
          settle(reject, error)
        },
      )
    })
  }

  /**
   * Close stdin and wait for the child to exit; the gateway exits at stdin EOF.
   * @returns {Promise<{code: number | null, signal: string | null} | undefined>} the exit facts, or `undefined` when no child was running.
   */
  close() {
    const child = this.#child
    if (child === undefined) return Promise.resolve(undefined)
    return new Promise(resolve => {
      child.once('close', (code, signal) => resolve({ code, signal }))
      child.stdin.end()
    })
  }

  #ensureChild() {
    if (this.#child !== undefined) return this.#child
    const child = this.#spawn(this.#command, this.#args, { cwd: this.#cwd, env: this.#env, stdio: ['pipe', 'pipe', 'pipe'] })
    this.#child = child
    this.#stderr = ''
    let resolveReady
    let rejectReady
    this.#ready = new Promise((resolve, reject) => {
      resolveReady = resolve
      rejectReady = reject
    })
    // Awaiters receive the rejection through `request()`; the promise itself must not become an unhandled rejection.
    this.#ready.catch(() => {})
    const timer = setTimeout(() => {
      this.#fail(new GatewayError(`omp-gateway: ${this.#command} printed no ready line within ${this.#readyTimeoutMs} ms`, 'NOT_READY'))
      this.#kill()
    }, this.#readyTimeoutMs)
    timer.unref?.()
    this.#gate = {
      open: false,
      resolve: value => {
        clearTimeout(timer)
        this.#gate.open = true
        resolveReady(value)
      },
      reject: error => {
        clearTimeout(timer)
        rejectReady(error)
      },
    }
    child.on('error', error => {
      if (this.#child !== child) return
      this.#fail(new GatewayError(`omp-gateway: cannot spawn ${this.#command}: ${error.message}`, 'SPAWN', { cause: error }))
      this.#forget(child)
    })
    // `close` rather than `exit`: the last reply lines are delivered before the streams close.
    child.on('close', (code, signal) => {
      if (this.#child !== child) return
      this.#fail(new GatewayError(`omp-gateway: gateway child exited (code ${code}, signal ${signal})${this.#stderrSuffix()}`, 'GATEWAY_EXIT'))
      this.#forget(child)
    })
    // A write after the child died surfaces through the `close` handler above.
    child.stdin.on('error', () => {})
    child.stderr.setEncoding('utf8')
    child.stderr.on('data', chunk => {
      this.#stderr = (this.#stderr + chunk).slice(-STDERR_TAIL_BYTES)
    })
    createInterface({ input: child.stdout, crlfDelay: Infinity }).on('line', line => {
      if (this.#child === child) this.#onLine(line)
    })
    return child
  }

  #onLine(line) {
    if (line.trim().length === 0) return
    let parsed
    try {
      parsed = JSON.parse(line)
    } catch (error) {
      this.#protocolFailure(`unparseable line from ${this.#command}: ${line.slice(0, 200)}`, error)
      return
    }
    if (parsed === null || typeof parsed !== 'object') {
      this.#protocolFailure(`non-object line from ${this.#command}`)
      return
    }
    if (!this.#gate.open) {
      if (parsed.ready === true) this.#gate.resolve(parsed)
      else this.#protocolFailure(`${this.#command} did not print its ready line first`)
      return
    }
    if (!Number.isInteger(parsed.id) || !Number.isInteger(parsed.status)) {
      this.#protocolFailure('reply line without an integer id and status')
      return
    }
    const entry = this.#pending.get(parsed.id)
    if (entry === undefined) {
      this.#protocolFailure(`reply id ${parsed.id} matches no pending request`)
      return
    }
    this.#pending.delete(parsed.id)
    entry.resolve({ status: parsed.status, body: parsed.body })
  }

  #protocolFailure(message, cause) {
    this.#fail(new GatewayError(`omp-gateway: ${message}`, 'PROTOCOL', cause === undefined ? undefined : { cause }))
    this.#kill()
  }

  #fail(error) {
    if (this.#gate !== undefined && !this.#gate.open) this.#gate.reject(error)
    const pending = [...this.#pending.values()]
    this.#pending.clear()
    for (const entry of pending) entry.reject(error)
  }

  #kill() {
    this.#child?.kill('SIGTERM')
  }

  #forget(child) {
    if (this.#child !== child) return
    this.#child = undefined
    this.#ready = undefined
    this.#gate = undefined
  }

  #stderrSuffix() {
    const tail = this.#stderr.trim()
    return tail.length === 0 ? '' : `; stderr: ${tail}`
  }
}

function abortedError() {
  return new GatewayError('omp-gateway: request aborted; the gateway child was killed', 'ABORTED')
}
