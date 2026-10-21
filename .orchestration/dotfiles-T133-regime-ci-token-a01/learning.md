# Learning triage: dotfiles-T133-regime-ci-token-a01

These are candidates only; nothing is promoted.

1. [memory:failure] A task text can describe code that does not exist, such as "extend the minimal environment". Before editing, measure the premise against the base (here `git log --all -S` on the file) and ask with the measured facts. Implementing the literal sentence would have introduced a behaviour change, an environment allowlist, that the text never stated.
2. [memory:failure] Every `env -i` command run inside the Claude sandbox needs the sandbox proxy variables whenever a child may touch the network (uv's pyyaml revalidation). This is the second task in two days where the prescribed command failed without them. Put the proxy pass-through in every such command when the text is written.
3. [memory:decision] When a test proves secrecy, have it assert presence first. Here the secrecy test asserts the token reaches the child before asserting its absence from argv and output, so dropping the credential cannot pass it.
