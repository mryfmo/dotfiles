---
task_id: dotfiles-T129-assets-omp-hcom-a01
round: 3
amendment: 5
status: source-approved-local-validated
---

Validated task-local observation: generate-agent-configs.py accepts pin/hash render fields but rejects a URL as a non-plain pin value. The task's fallback records the URL in assets.hcom.files and declares the matching updater constant; version and SHA256 values remain generated. No rule/skill/project-memory promotion.

[memory:failure] Match fake CLI output to real observed output before trusting a version-parser test. CI printed omp/18.11.3 while the fixture printed omp 18.11.3. Round3 preserves exact equality and removes only the known literal prefix once; foreign/repeated prefixes and suffixes still fail. Independent old-source RED and new-source GREEN confirm the distinction.
