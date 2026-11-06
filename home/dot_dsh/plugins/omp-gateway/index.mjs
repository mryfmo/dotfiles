/**
 * DSH `LlmAdapter` plugin over a child `omp auth-gateway stdio`.
 *
 * A DSH turn on a configured provider route (default `claude-bridge`) becomes one `/v1/messages` line to the
 * child, and the child's non-streaming reply becomes the chunk sequence of the final message. The plugin
 * reads, stores and passes no credential: the login stays inside omp, which reads its own settings from the
 * environment names listed in `env`.
 *
 * Loaded by a profile as an out-of-tree package: a `dependencies` row of the profile `package.json` pointing
 * at this directory (`link:`) and a patch row `name: dsh-omp-gateway`.
 */
import { homedir } from 'node:os'
import { LlmAdapter, LlmError } from '@deepseek-ai/dsh-llm'
import { resolveConfig } from './config.mjs'
import { GatewayClient, GatewayError, pickEnv } from './gateway-client.mjs'
import { toChunks, toError, toMessagesBody, TranslationError } from './translate.mjs'

export const name = 'omp-gateway'
export const inject = ['llm']

export class OmpGatewayAdapter extends LlmAdapter {
  #client
  #config

  /**
   * @param {GatewayClient} client the boundary that owns the gateway child.
   * @param {ReturnType<typeof resolveConfig>} config normalised configuration.
   */
  constructor(client, config) {
    super()
    this.#client = client
    this.#config = config
  }

  providerInfo(provider) {
    return { id: provider, name: `${provider} via omp auth-gateway` }
  }

  listModels(provider) {
    return Promise.resolve(this.#config.models.map(id => ({ provider, id, name: id })))
  }

  async *stream(options) {
    const body = toMessagesBody(options, { maxTokens: this.#config.maxTokens })
    let reply
    try {
      reply = await this.#client.request('/v1/messages', body, options.signal)
    } catch (error) {
      throw error instanceof GatewayError ? new LlmError(error.message, error.code, { cause: error }) : error
    }
    if (reply.status !== 200) {
      const failure = toError(reply.status, reply.body)
      throw new LlmError(failure.message, failure.code, httpStatusOption(failure.status))
    }
    try {
      yield* toChunks(reply.body)
    } catch (error) {
      throw error instanceof TranslationError ? new LlmError(error.message, error.code, { cause: error }) : error
    }
  }
}

/**
 * Mount the adapter for every configured provider route.
 * @param {import('@deepseek-ai/cordis').Context} ctx
 * @param {Record<string, unknown>} raw the patch row's `config:` block.
 */
export function apply(ctx, raw) {
  const config = resolveConfig(raw)
  const client = new GatewayClient({
    command: config.command,
    args: config.args,
    env: pickEnv(config.env),
    cwd: config.cwd ?? homedir(),
    readyTimeoutMs: config.readyTimeoutMs,
  })
  ctx.llm.registerAdapter([...config.providers], new OmpGatewayAdapter(client, config))
  ctx.effect(() => () => client.close())
}

function httpStatusOption(status) {
  return Number.isInteger(status) && status >= 100 && status <= 599 ? { status } : {}
}
