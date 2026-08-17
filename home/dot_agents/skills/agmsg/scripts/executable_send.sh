#!/usr/bin/env bash
set -euo pipefail

# @file send
# @brief Send one message through the agmsg SQLite store.
# @arg $1 string Team name.
# @arg $2 string Sender agent identity.
# @arg $3 string Recipient agent identity.
# @arg $4 string Message body.

TEAM="${1:?Usage: send.sh <team> <from> <to> <message>}"
FROM="${2:?Missing from agent}"
TO="${3:?Missing to agent}"
BODY="${4:?Missing message body}"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/lib/identifier.sh"
agmsg_validate_identifiers 'send.sh <team> <from> <to> <message>' "$TEAM" "$FROM" "$TO"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/lib/storage.sh"
DB="$(agmsg_db_path)"

if [ ! -f "$DB" ]; then
    bash "$SCRIPT_DIR/init-db.sh"
fi

# @description Quote one shell string as a SQLite text literal.
# @arg $1 string Value to quote.
sql_literal() {
    printf "'"
    printf '%s' "$1" | sed "s/'/''/g"
    printf "'"
}

TEAM_SQL="$(sql_literal "$TEAM")"
FROM_SQL="$(sql_literal "$FROM")"
TO_SQL="$(sql_literal "$TO")"
BODY_SQL="$(sql_literal "$BODY")"

sqlite3 "$DB" "INSERT INTO messages (team, from_agent, to_agent, body) VALUES ($TEAM_SQL, $FROM_SQL, $TO_SQL, $BODY_SQL);"

echo "Sent to $TO in team $TEAM"
