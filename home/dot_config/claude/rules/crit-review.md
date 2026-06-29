## Crit review workflow

- For plan reviews, code reviews, diff reviews, PR reviews, or any task explicitly described as a review, always use Crit.
- Rely on the Claude Code Crit plugin Plan Mode hook for plan review. Do not bypass the hook unless the user explicitly disables Crit for the current task.
- When `/crit` starts a review, wait until Crit finishes, address unresolved comments, reply in Crit, and start the next round when Crit asks for it.
