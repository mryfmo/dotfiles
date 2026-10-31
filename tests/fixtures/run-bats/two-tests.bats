#!/usr/bin/env bats
# The two tests behind timing-stream.txt (tests/fixtures/run-bats/README.md); not a suite CI runs.

@test "[recorded] skipped" {
    skip "the directive follows the duration"
}

@test "[recorded] slow" {
    sleep 0.3
}
