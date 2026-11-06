import assert from 'node:assert/strict'
import { test } from 'node:test'
import { DEFAULT_CONFIG, DEFAULT_ENV_NAMES, resolveConfig } from '../config.mjs'

test('resolveConfig fills every row from the defaults', () => {
  const config = resolveConfig()
  assert.deepEqual(config, {
    command: 'omp',
    args: ['auth-gateway', 'stdio'],
    env: [...DEFAULT_ENV_NAMES],
    cwd: undefined,
    providers: ['claude-bridge'],
    models: [],
    maxTokens: 4096,
    readyTimeoutMs: 30_000,
  })
  assert.deepEqual(config, { ...DEFAULT_CONFIG, env: [...DEFAULT_ENV_NAMES] })
  assert.ok(Object.isFrozen(config) && Object.isFrozen(config.args))
})

test('resolveConfig keeps explicit rows', () => {
  const config = resolveConfig({ command: '/usr/bin/node', args: ['stub.mjs'], env: ['HOME'], cwd: '/tmp', providers: ['claude-bridge', 'siwc'], models: ['claude-haiku-5-5'], maxTokens: 32, readyTimeoutMs: 1 })
  assert.deepEqual(config, { command: '/usr/bin/node', args: ['stub.mjs'], env: ['HOME'], cwd: '/tmp', providers: ['claude-bridge', 'siwc'], models: ['claude-haiku-5-5'], maxTokens: 32, readyTimeoutMs: 1 })
})

test('resolveConfig refuses malformed rows by name', () => {
  assert.throws(() => resolveConfig({ command: '' }), /config\.command must be a non-empty string/)
  assert.throws(() => resolveConfig({ args: 'auth-gateway stdio' }), /config\.args must be a list of strings/)
  assert.throws(() => resolveConfig({ env: [1] }), /config\.env must be a list of strings/)
  assert.throws(() => resolveConfig({ providers: [] }), /config\.providers must name at least one/)
  assert.throws(() => resolveConfig({ providers: [''] }), /config\.providers must name at least one/)
  assert.throws(() => resolveConfig({ maxTokens: 0 }), /config\.maxTokens must be a positive integer/)
  assert.throws(() => resolveConfig({ readyTimeoutMs: 1.5 }), /config\.readyTimeoutMs must be a positive integer/)
  assert.throws(() => resolveConfig([]), /config must be an object/)
})
