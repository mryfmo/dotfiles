#!/usr/bin/env bash
# @file ruleset-request.sh
# @brief Display the desired integration ruleset and its live diff without changing GitHub.
# @option --expected <file> Read the expected JSON from a file.
# @example bash scripts/orchestrator/ruleset-request.sh
set -euo pipefail

# @description Share the GET-only comparison with ruleset-verify.sh.
# @arg $1 string Either request or verify, fixed by the calling script.
# @option --expected <file> Read the expected JSON from a file.
# @option --progress <file> In verify mode, timestamp an existing ledger after equality.
compare_ruleset() {
    local mode=$1 expected='' progress='' root repo live seen=' '
    shift
    while (($#)); do
        [[ $# -ge 2 && $seen != *" $1 "* ]] || return 2
        seen+="$1 "
        case $1 in
        --expected) expected=$2 ;;
        --progress)
            [[ $mode == verify ]] || return 2
            progress=$2
            ;;
        *) return 2 ;;
        esac
        shift 2
    done
    root=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd -P)
    repo=$(gh repo view --json nameWithOwner --jq .nameWithOwner)
    [[ $repo =~ ^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$ ]] || return 2
    live=$(gh api "repos/$repo/rulesets/24397953")
    printf '%s\n' "$live" | python3 -I -B /dev/fd/3 "$mode" "$root" "$expected" "$progress" 3<< 'PY'
import difflib, json, os, stat, sys, tempfile
from datetime import datetime, timezone
from pathlib import Path

mode, root, expected_file, progress_file = sys.argv[1:]
contexts = ['validate', 'test (ubuntu-24.04, server)', 'test (ubuntu-24.04, client)',
            'test (macos-14, client)', 'public-bootstrap (ubuntu-24.04, server)',
            'public-bootstrap (ubuntu-24.04, client)', 'public-bootstrap (macos-14, client)']
expected = json.loads(Path(expected_file).read_text()) if expected_file else {
    'id': 24397953, 'name': 'main integration gate', 'target': 'branch', 'enforcement': 'active',
    'conditions': {'ref_name': {'exclude': [], 'include': ['~DEFAULT_BRANCH']}}, 'bypass_actors': [],
    'rules': [{'type': 'deletion'}, {'type': 'non_fast_forward'}, {'type': 'required_status_checks',
              'parameters': {'strict_required_status_checks_policy': False, 'do_not_enforce_on_create': False,
                             'required_status_checks': [{'context': c, 'integration_id': 15368} for c in contexts]}}]}

def canonical(value):
    value = dict(value)
    for key in ('node_id', 'source_type', 'source', 'created_at', 'updated_at', 'current_user_can_bypass', '_links'):
        value.pop(key, None)
    value.setdefault('bypass_actors', [])
    for rule in value['rules']:
        if rule['type'] == 'required_status_checks':
            rule['parameters']['required_status_checks'].sort(key=lambda check: json.dumps(check, sort_keys=True))
    value['rules'] = sorted(value['rules'], key=lambda rule: (rule['type'], json.dumps(rule, sort_keys=True)))
    return value

missing = object()
def encoded(value):
    return '<missing>' if value is missing else json.dumps(value, sort_keys=True)

def differences(want, got, path='ruleset'):
    if isinstance(want, dict) and isinstance(got, dict):
        return [entry for key in sorted(want.keys() | got.keys())
                for entry in differences(want.get(key, missing), got.get(key, missing), path + '.' + key)]
    if isinstance(want, list) and isinstance(got, list):
        return [entry for i in range(max(len(want), len(got))) for entry in differences(
            want[i] if i < len(want) else missing, got[i] if i < len(got) else missing, f'{path}[{i}]')]
    return [] if encoded(want) == encoded(got) else [f'{path}: expected {encoded(want)}, live {encoded(got)}']

expected, live = canonical(expected), canonical(json.load(sys.stdin))
diff = differences(expected, live)
if mode == 'request':
    print(json.dumps(expected, sort_keys=True, indent=2))
    print(''.join(difflib.unified_diff(json.dumps(expected, sort_keys=True, indent=2).splitlines(True),
                                    json.dumps(live, sort_keys=True, indent=2).splitlines(True),
                                    fromfile='expected', tofile='live')), end='\n')
    print('\n'.join(diff))
    raise SystemExit(0)
if diff:
    print('\n'.join(diff))
    raise SystemExit(1)
if not progress_file or not Path(progress_file).exists():
    print('verified ruleset 24397953; no progress updated')
    raise SystemExit(0)
root = Path(root)
progress = Path(progress_file).absolute()
assert progress.resolve().is_relative_to(root) and not progress.is_symlink(), 'unsafe progress path'
original = progress.read_bytes()
lines = original.decode().splitlines(keepends=True)
header = lines[0].rstrip('\r\n').split('\t')
assert len(header) == len(set(header)) and all(key in header for key in ('id', 'evidence', 'updated_jst')), 'progress header'
indexes = {key: [i for i, line in enumerate(lines[1:], 1) if line.split('\t')[header.index('id')] == key] for key in ('D1', 'D2')}
assert all(len(rows) == 1 for rows in indexes.values()), 'expected unique D1 and D2 anchors'
now = datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')
for key, rows in indexes.items():
    i = rows[0]
    fields = lines[i].rstrip('\r\n').split('\t')
    assert len(fields) == len(header) and fields[header.index('id')] == key, 'progress row anchor'
    fields[header.index('evidence')], fields[header.index('updated_jst')] = 'verified ' + now, now
    lines[i] = '\t'.join(fields) + ('\r\n' if lines[i].endswith('\r\n') else '\n' if lines[i].endswith('\n') else '')
assert progress.read_bytes() == original, 'progress changed during verification'
fd, temporary = tempfile.mkstemp(dir=progress.parent)
try:
    with os.fdopen(fd, 'wb') as output:
        output.write(''.join(lines).encode())
        os.fchmod(output.fileno(), stat.S_IMODE(progress.stat().st_mode))
    os.replace(temporary, progress)
finally:
    if os.path.exists(temporary):
        os.unlink(temporary)
print('verified ruleset 24397953; updated D1 and D2 at ' + now)
PY
}

if [[ ${BASH_SOURCE[0]} == "$0" ]]; then
    compare_ruleset request "$@"
fi
