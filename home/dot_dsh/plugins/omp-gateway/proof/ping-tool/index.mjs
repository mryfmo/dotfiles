/** The `ping` tool of the composition proof: the measured tool_use reply calls it with `{"word":"pong"}`. */
import { hostname } from 'node:os'
import { defineTool } from '@deepseek-ai/dsh-tools'

export const name = 'u240-ping-tool'
export const inject = ['tools']

export function apply(ctx) {
  ctx.tools.register(defineTool({
    name: 'ping',
    description: 'Answer with the current host name of the caller.',
    parameters: {
      word: { type: 'string', required: true, description: 'Echoed back beside the host name.' },
    },
    output: {
      schema: { type: 'string' },
      render: (_args, value) => [{ type: 'text', text: value }],
    },
    async execute(args) {
      return `${args.word} from ${hostname()}`
    },
  }))
}
