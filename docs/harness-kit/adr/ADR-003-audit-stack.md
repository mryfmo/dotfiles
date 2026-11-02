# ADR-003: Audit stack

Status: proposed
Date: 2026-11-02

## Context

The merge gate as it stands is described in `AGENTS.md` ("Agent Review Evidence", "Audit") and in the levers `home/dot_local/bin/common/executable_pr-audit.sh` and `executable_pr-merge.sh`. The eighth research file, `research/cloudflare-security-audit-skill.md`, had not landed when this stub was written.

## Decision

Written after the security-audit-skill research lands.

## Alternatives considered

Written with the decision.

## Consequences

Written with the decision.

## Verification

- `bdd/audit.feature`: `@R-11`, `@R-12`, `@R-13` describe the gate as it stands today; `@R-14` is the target this ADR will settle.
