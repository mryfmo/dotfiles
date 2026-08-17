#!/usr/bin/env bash

# @file identifier
# @brief Validate agmsg team and agent identifiers.

AGMSG_IDENTIFIER_PATTERN='^[a-z0-9][a-z0-9_-]{0,63}$'

# @description Reject identifiers outside the shared grammar with a usage error.
# @arg $1 string Command usage text without the "Usage:" prefix.
# @arg $@ string One or more identifiers to validate.
agmsg_validate_identifiers() {
    local usage="$1"
    shift
    local identifier
    for identifier in "$@"; do
        if [[ ! "$identifier" =~ $AGMSG_IDENTIFIER_PATTERN ]]; then
            printf 'Usage: %s (identifiers must match %s)\n' "$usage" "$AGMSG_IDENTIFIER_PATTERN" >&2
            return 1
        fi
    done
}
