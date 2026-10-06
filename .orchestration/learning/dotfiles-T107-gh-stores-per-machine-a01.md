# Learning: dotfiles-T107-gh-stores-per-machine-a01

- **Model credentials on the axis the operator actually varies.** T103 keyed the human store by account role (owner versus work). The real variable is the machine: one human account per machine, plus one shared machine account. Asking "which account does this machine use?" before modelling would have avoided the third store.
- **A validation grep for removed names constrains the tests too.** "No match in tests/" rules out asserting the old names' absence by spelling them. Asserting the exact set of rendered `*_GH_CONFIG_DIR` variables is stricter and needs neither name.
