/** Configuration rows of the omp-gateway plugin, normalised once at the cordis boundary. */

/**
 * Every name srt injects into the child it sandboxes, in the order @anthropic-ai/sandbox-runtime 0.0.81 pushes them
 * (`dist/sandbox/sandbox-utils.js`, `generateProxyEnvVars` :667-838): the runtime mark (:680), the temporary directory
 * (:691), the `CA_TRUST_VARS` set when TLS termination is on (:649-665, pushed :698), the proxy names (:720-727,
 * :749-750, :759-760), `GIT_CONFIG_PARAMETERS` when the proxy has auth (:732), and the SOCKS branch (:785-830).
 * `TMPDIR` is already a row above and is left out here.
 */
export const SRT_INJECTED_ENV_NAMES = Object.freeze([
  'SANDBOX_RUNTIME',
  'NODE_EXTRA_CA_CERTS', 'SSL_CERT_FILE', 'CURL_CA_BUNDLE', 'REQUESTS_CA_BUNDLE', 'PIP_CERT', 'GIT_SSL_CAINFO',
  'AWS_CA_BUNDLE', 'CARGO_HTTP_CAINFO', 'DENO_CERT', 'CLOUDSDK_CORE_CUSTOM_CA_CERTS_FILE', 'NIX_SSL_CERT_FILE',
  'NO_PROXY', 'no_proxy', 'HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy', 'GIT_CONFIG_PARAMETERS',
  'ALL_PROXY', 'all_proxy', 'GRPC_PROXY', 'grpc_proxy',
  'SRT_SSH_PROXY_COMMAND', 'GIT_SSH_COMMAND', 'FTP_PROXY', 'ftp_proxy', 'RSYNC_PROXY',
  'DOCKER_HTTP_PROXY', 'DOCKER_HTTPS_PROXY',
  'CLOUDSDK_PROXY_TYPE', 'CLOUDSDK_PROXY_ADDRESS', 'CLOUDSDK_PROXY_PORT', 'CLOUDSDK_PROXY_USERNAME', 'CLOUDSDK_PROXY_PASSWORD',
])

/**
 * Environment names handed to the gateway child when the row `env` is omitted. The list is the child's boundary: a
 * name absent here never reaches `omp auth-gateway stdio`, whatever the plugin's own environment holds. `USER` stays
 * (measured 2026-11-06: without it the login answers 502). `OMP_PROFILE` rides when the launcher sets it, so the
 * child lives in the profile the launcher names (the hcom-seat dsh role: `~/.omp/profiles/dsh`, U272) instead of the
 * default `~/.omp/agent`, which that role denies (U306, the g6 failure `SQLITE_AUTH: authorization denied`).
 * `CLAUDE_CONFIG_DIR` rides for the same reason: hcom-seat hands the dsh role the shared seat login
 * `<seats-root>/.state/claude` under that name and denies the operator's `~/.claude` (U318), so without it the
 * bridge's Claude child looks for a login it cannot read and never answers (U355, the g6 failure `request aborted`).
 * The name carries a path, never a token. `SRT_INJECTED_ENV_NAMES` ride because the dsh role runs under srt, whose
 * sandbox reaches the network only through the proxy srt starts and tells its child so through these names; a
 * gateway child without them resolves DNS directly, which the sandbox denies (U364, the g6 failure
 * `network-outbound /private/var/run/mDNSResponder`). They carry a loopback proxy URL with a per-process auth token
 * srt minted for this child, and no value of the launcher's own.
 */
export const DEFAULT_ENV_NAMES = Object.freeze([
  'HOME', 'PATH', 'USER', 'LOGNAME', 'SHELL', 'LANG', 'LC_ALL', 'TERM', 'TMPDIR',
  'XDG_CONFIG_HOME', 'XDG_DATA_HOME', 'XDG_CACHE_HOME', 'XDG_STATE_HOME', 'OMP_PROFILE', 'CLAUDE_CONFIG_DIR',
  ...SRT_INJECTED_ENV_NAMES,
])

export const DEFAULT_CONFIG = Object.freeze({
  command: 'omp',
  args: Object.freeze(['auth-gateway', 'stdio']),
  env: DEFAULT_ENV_NAMES,
  cwd: undefined,
  providers: Object.freeze(['claude-bridge']),
  models: Object.freeze([]),
  maxTokens: 4096,
  readyTimeoutMs: 30_000,
})

/**
 * Normalise a raw `config:` block.
 * @param {Record<string, unknown>} [raw]
 * @returns {{command: string, args: readonly string[], env: readonly string[], cwd: string | undefined, providers: readonly string[], models: readonly string[], maxTokens: number, readyTimeoutMs: number}}
 */
export function resolveConfig(raw = {}) {
  if (raw === null || typeof raw !== 'object' || Array.isArray(raw)) {
    throw new TypeError('omp-gateway: config must be an object')
  }
  const command = optional(raw, 'command', DEFAULT_CONFIG.command, nonEmptyString)
  const args = optional(raw, 'args', DEFAULT_CONFIG.args, stringList)
  const env = optional(raw, 'env', DEFAULT_CONFIG.env, stringList)
  const cwd = optional(raw, 'cwd', DEFAULT_CONFIG.cwd, nonEmptyString)
  const providers = optional(raw, 'providers', DEFAULT_CONFIG.providers, stringList)
  if (providers.length === 0 || providers.some(provider => provider.length === 0)) {
    throw new TypeError('omp-gateway: config.providers must name at least one non-empty provider route')
  }
  const models = optional(raw, 'models', DEFAULT_CONFIG.models, stringList)
  const maxTokens = optional(raw, 'maxTokens', DEFAULT_CONFIG.maxTokens, positiveInteger)
  const readyTimeoutMs = optional(raw, 'readyTimeoutMs', DEFAULT_CONFIG.readyTimeoutMs, positiveInteger)
  return Object.freeze({
    command,
    args: Object.freeze([...args]),
    env: Object.freeze([...env]),
    cwd,
    providers: Object.freeze([...providers]),
    models: Object.freeze([...models]),
    maxTokens,
    readyTimeoutMs,
  })
}

function optional(raw, key, fallback, check) {
  const value = raw[key]
  if (value === undefined || value === null) return fallback
  if (!check(value)) throw new TypeError(`omp-gateway: config.${key} ${check.expected}`)
  return value
}

function nonEmptyString(value) {
  return typeof value === 'string' && value.length > 0
}
nonEmptyString.expected = 'must be a non-empty string'

function stringList(value) {
  return Array.isArray(value) && value.every(item => typeof item === 'string')
}
stringList.expected = 'must be a list of strings'

function positiveInteger(value) {
  return Number.isInteger(value) && value > 0
}
positiveInteger.expected = 'must be a positive integer'
