# Credential argv observation and repair

Resolved in correction round2. At source07c61e31, launch() placed preserved GH_TOKEN/GITHUB_TOKEN values into /usr/bin/env NAME=value argv. The synthetic-only observed subprocess-boundary assertion failed before repair (1test2.234s, no errors). No real token value was printed or added to evidence.

Source24d7f55fc0929239c4052a519fcc65a227f8f52dd49f0e9f4f91a1189da801b5 executes the already validated absolute binary with the unchanged clean env mapping. Tokens stay in that mapping and leave argv; all four combinations still reach gh exactly. Both29-test modules pass315/312. The restored-wrapper mutant is killed; final24/24/0. Fresh security-profile worker review independently ran six methods in8.756s exit0, no new finding. Final task/security audit and integration authority remain with the orchestrator; shared credentials/UID and parent/cache residuals remain.
