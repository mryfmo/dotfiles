# M-21 task 06 rerun: one DSH turn under srt on the kit profile (coordinator procedure)

Preconditions, each measured before the run: U227 merged and its patch deployed to `~/.dsh/profiles/thak/cordis.patch.yml` (`grep -n -A3 '^- id: agent-default-model'` shows the ollama-cloud row); `~/.config/dsh/ollama-api-key` present, mode 0600, one line (the operator's step in `operator-steps-dsh-route-and-seat-identity.md`); `~/.dsh/bin/dsh --version` prints the manifest pin.

Run from the coordinator's terminal, outside every seat, with a disposable `DSH_HOME` under `$TMPDIR` (the spike of 2026-11-06T03:4xZ, same settings shape):

1. `BASE=$(mktemp -d "${TMPDIR:-/tmp}/dsh-spike.XXXXXX")`; `SPIKE=$BASE/dsh-home`; copy `~/.dsh/profiles/thak` to `$SPIKE/profiles/thak`.
2. Write `$BASE/settings/srt-settings.json` from a worker seat's settings: the credential denies kept, the settings directory read-denied, `allowRead` = `$SPIKE` and `~/.dsh`, `allowWrite` = `$SPIKE`, `/private/tmp/claude`, `~/.npm/_logs`, `network.allowedDomains` = the seat's list plus `ollama.com`, no `allowNestedUserNamespaces`.
3. Canary, verbatim from `hcom-seat`: `srt --settings $BASE/settings/srt-settings.json -- /bin/sh -c '<the probe of hcom-seat:1782-1785>' canary $BASE/canary $BASE/settings/srt-settings.json ~/.ssh` must print `write-denied read-denied ssh-denied` and leave no canary file. Record the line.
4. Withdrawn 2026-11-06 (the operator's login-only rule, frame row 05:46:33Z): no API key is read or passed. The turn under srt now goes through the login route of U238 and the `dsh-srt` launcher of U251 (PR 687); its measurement is the `seat` item of `tests/dsh-login-route.tsv`.
   Paste the last stdout line and the exit code into the decisions row (phase `M-21`): started and answered, or refused with its line.
5. `dsh --profile thak --dump-config` under the same srt: confirm `agent-default-model` is the ollama-cloud row and the skill roots (`agentsHome` default `~/.agents`); a later turn asking the model to list its skills proves R-51 (the kwp-* skills visible to DSH).
6. Remove `$BASE`; `git status --porcelain` outside the store unchanged.

The key never appears in a row, a file of the store or a PR body.
