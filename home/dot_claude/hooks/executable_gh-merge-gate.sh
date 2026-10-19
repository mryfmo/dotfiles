#!/usr/bin/env bash
# @file gh-merge-gate.sh
# @brief Allow pinned accepted green merges, bare update-branch and bounded PR creation.
# @description
#   Merge and ready creation require the protected orchestrator_checkout primary repository.
#   Draft creation requires a pushed non-default head and a default or open-PR base; update-branch is bare.
#   Boundary merges also require pinned open ready default-branch PRs and green required checks.
#   Body files stay inside the invoking worktree; unrelated legacy acceptance formats supply no authority.
#   test_gate_closes_each_of_the_seven_review_classes covers argv-text-mismatch, JSON encoding,
#   fail-open-on-error and unbound-evidence; test_no_shell_metacharacter_input_is_allowed checks raw exclusions.
#   Gated words in prose ask. Fully variable-assembled names can remain invisible; permgate and the
#   auto-mode classifier are the next layer. Recognition executes no submitted command text.
# @stdin json The PreToolUse payload; its command is parsed and never executed.
# @stdout json One decision, or no output for unrelated commands.
# @set ${XDG_STATE_HOME:-~/.local/state}/claude/gh-merge-gate.log Decision log.
# @exitcode 0 Always; internal errors ask.
set -euo pipefail

bootstrap_ask() {
    printf '%s\n' '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"ask","permissionDecisionReason":"gh/pr merge/create/update-branch: trusted tools unavailable"}}'
    exit 0
}
trap bootstrap_ask ERR
[[ ${HOME:-} == /* && -r ${HOME}/.agents/agent-config.yaml ]] || bootstrap_ask
anchor_re='^orchestrator_checkout: (~/[^[:space:]]+)$' count=0 anchor=
while IFS= read -r line || [[ -n $line ]]; do
    if [[ $line =~ $anchor_re ]]; then
        anchor=${HOME}/${BASH_REMATCH[1]:2}
        ((count += 1))
    fi
done < "${HOME}/.agents/agent-config.yaml"
[[ $count == 1 ]] || bootstrap_ask
cd -P -- "$anchor" || bootstrap_ask
export PATH="${HOME}/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"
tools=()
for name in python3 jq gh git; do
    found=$(/usr/bin/env -i HOME="$HOME" PATH="$PATH" mise which "$name" 2> /dev/null || command -v "$name") || bootstrap_ask
    [[ $found == /* && $found != */shims/* ]] || bootstrap_ask
    tools+=("$found")
done
bin=$(/usr/bin/mktemp -d "${TMPDIR:-/tmp}/gh-gate.XXXXXX") || bootstrap_ask
trap '/bin/rm -rf -- "$bin"' EXIT
for i in 0 1 2 3; do
    names=(python3 jq gh git)
    /bin/ln -s -- "${tools[$i]}" "$bin/${names[$i]}"
done
export PATH=$bin
decide() {
    trap - ERR
    local output log=${XDG_STATE_HOME:-${HOME}/.local/state}/claude/gh-merge-gate.log
    local filter="{hookSpecificOutput:{hookEventName:\"PreToolUse\",permissionDecision:\$decision,permissionDecisionReason:\$reason}}"
    output=$("${tools[1]}" -n --arg decision "$1" --arg reason "gh-merge-gate: $2" \
        "$filter") || {
        output='{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"ask","permissionDecisionReason":"gh/pr merge/create/update-branch: jq missing or encoding failed"}}'
        set -- ask "gh/pr merge/create/update-branch: jq missing or encoding failed"
    }
    { /bin/mkdir -p "${log%/*}" && printf '%s\t%s\t%s\n' "$(/bin/date -u +%Y-%m-%dT%H:%M:%SZ)" "$1" "$2" >> "$log"; } 2> /dev/null || true
    printf '%s\n' "$output"
    exit 0
}
trap 'decide ask "unable to inspect gh/pr merge/create/update-branch: internal error"' ERR
export NO_COLOR=1 CLICOLOR=0 CLICOLOR_FORCE=0 GH_PAGER=cat
unset GH_FORCE_TTY
result=$(
    "${tools[0]}" -I -B /dev/fd/3 "${tools[@]}" 3<< 'PY'
import json, os, re, shlex, subprocess, sys, tempfile
from pathlib import Path
gated_words = ''
tools = dict(zip(('python3', 'jq', 'gh', 'git'), sys.argv[1:]))

class Ask(Exception):
    pass

def require(condition, reason):
    if not condition:
        raise Ask(reason)

def run(*args, data=None):
    return subprocess.run([tools[args[0]], *args[1:]], input=data, text=True, capture_output=True, check=True, timeout=30).stdout.strip()

def gh(*args):
    return run('gh', *args)

def api(endpoint):
    return json.loads(gh('api', endpoint))

def ref(value):
    require(isinstance(value, str) and re.fullmatch(r'[A-Za-z0-9._/-]+', value) and not value.startswith('-'), 'invalid branch')
    run('git', 'check-ref-format', '--branch', value)
    return value

def canonical_checkout(cwd, selected):
    manifest = (Path.home() / '.agents/agent-config.yaml').read_text()
    anchors = re.findall(r'^orchestrator_checkout: (~/[^\s\x00]+)$', manifest, re.M)
    require(len(anchors) == 1, 'missing or ambiguous checkout anchor')
    anchor = Path(anchors[0]).expanduser().resolve(strict=True)
    top = Path(run('git', 'rev-parse', '--show-toplevel')).resolve(strict=True)
    common = Path(run('git', 'rev-parse', '--path-format=absolute', '--git-common-dir')).resolve(strict=True)
    require(top == anchor and common == top / '.git' and (top / '.git').is_dir() and not (top / '.git').is_symlink(), 'requires canonical primary checkout')
    origin = run('git', 'remote', 'get-url', 'origin')
    match = re.fullmatch(r'(?:https://github\.com/|git@github\.com:|ssh://git@github\.com/)([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+?)(?:\.git)?/?', origin)
    actual = gh('repo', 'view', '--json', 'nameWithOwner', '--jq', '.nameWithOwner')
    require(match and match[1].lower() == actual.lower() == selected.lower(), 'repository identity mismatch')
    return top

def path_within(path, root, fold=False):
    return Path(str(path).casefold() if fold else path).is_relative_to(Path(str(root).casefold() if fold else root))

def case_insensitive(root):
    with tempfile.NamedTemporaryFile(prefix='.gh-Case-', dir=root) as probe:
        other = Path(probe.name).with_name(Path(probe.name).name.swapcase())
        return other.exists() and other.samefile(probe.name)

def safe_file(top, path, allow_empty=False, fold=False):
    require(path_within(path, top, fold), 'evidence outside checkout')
    require(all(not p.is_symlink() for p in (path, *path.parents) if path_within(p, top, fold)), 'symlink evidence path')
    require(path.is_file() and (allow_empty or path.stat().st_size > 0), 'missing regular evidence file')
    return path.read_text()

def accepted(top, nwo, base, head, pr=None):
    tasks = []
    for entry in compared_files(nwo, base, head):
        match = re.fullmatch(r'\.orchestration/([A-Za-z0-9][A-Za-z0-9._-]*)/task\.md', entry['filename'])
        if match and entry.get('status') != 'removed':
            tasks.append(match[1])
    require(len(tasks) == 1, 'comparison must name exactly one task copy')
    task = tasks[0]
    text = safe_file(top, top / '.orchestration/acceptance' / (task + '.md'))
    pieces = re.split(r'(?m)^---\r?$', text, maxsplit=2)
    require(len(pieces) == 3 and pieces[0] == '', 'invalid acceptance front matter')
    record = json.loads(run('jq', '-ce', '.', data=pieces[1]))
    require(isinstance(record, dict) and record.get('task') == task and record.get('head') == head
            and (pr is None or record.get('pr') == pr), 'acceptance identity mismatch')
    require(type(record.get('pr')) is int and record['pr'] > 0, 'missing acceptance PR')
    safe_file(top, top / '.orchestration/tasks' / (task + '.md'))
    dispatch = record.get('dispatch')
    require(isinstance(dispatch, list) and all(isinstance(line, str) for line in dispatch), 'invalid dispatch evidence')
    events = [line.split() for line in dispatch if line.startswith('AGMSG-ACCEPTANCE v1 ')]
    require(events and events[-1].count('task_id=' + task) == 1 and events[-1].count('status=accepted') == 1
            and sum(x.startswith('status=') for x in events[-1]) == 1, 'latest acceptance is not accepted')
    audit = top / f'.orchestration/validation/{task}-audit-{head[:7]}.md'
    safe_file(top, audit)
    last = safe_file(top, Path(str(audit) + '.last.md'))
    verdict = last.rstrip().splitlines()[-1]
    if verdict == 'Verdict: incorrect':
        count = len(re.findall(r'^.*\[P[0-3]\].*$', last, re.M))
        entries = record.get('audit_findings')
        require(count > 0 and isinstance(entries, list) and len(entries) == count, 'audit dispositions missing')
        numbers = []
        for entry in entries:
            require(isinstance(entry, dict) and set(entry) == {'n', 'reason', 'evidence'}
                    and all(isinstance(v, str) and v.strip() for v in entry.values())
                    and len(entry['reason'].strip()) >= 20, 'invalid audit disposition')
            numbers.append(entry['n'])
        require(sorted(numbers) == sorted(map(str, range(1, count + 1))), 'audit finding numbers mismatch')
    else:
        require(verdict == 'Verdict: correct', 'audit verdict is not correct')

def compared_files(nwo, base, head):
    files = api(f'repos/{nwo}/compare/{base}...{head}').get('files')
    require(isinstance(files, list) and 0 < len(files) < 300, 'records compare empty or incomplete')
    require(all(isinstance(entry, dict) and isinstance(entry.get('filename'), str) and entry['filename'] for entry in files), 'invalid comparison files')
    require(all(entry.get('status') in ('added', 'removed', 'modified', 'renamed', 'copied', 'changed', 'unchanged') for entry in files), 'invalid comparison status')
    return files

def records_only(nwo, base, head):
    for entry in compared_files(nwo, base, head):
        for key in ('filename', 'previous_filename'):
            value = entry.get(key)
            require((key == 'previous_filename' and value is None) or
                    (isinstance(value, str) and value.startswith('.orchestration/') and '..' not in value.split('/')), 'compare touches outside records')

def green(nwo, default, head):
    rules = api(f'repos/{nwo}/rules/branches/{default}')
    required = [check for rule in rules if rule['type'] == 'required_status_checks'
                for check in rule['parameters']['required_status_checks']]
    require(required, 'no required status checks')
    pages = json.loads(gh('api', '--paginate', '--slurp', f'repos/{nwo}/commits/{head}/check-runs?per_page=100'))
    runs = [entry for page in pages for entry in page['check_runs']]
    statuses = api(f'repos/{nwo}/commits/{head}/status?per_page=100')['statuses']
    for check in required:
        context, app = check['context'], check.get('integration_id')
        matching = [r for r in runs if r['name'] == context and (app in (None, -1) or r['app']['id'] == app)]
        if matching:
            newest = max(matching, key=lambda r: r['id'])
            require(newest['status'] == 'completed' and newest['conclusion'] == 'success'
                    and newest['head_sha'] == head, 'required check is not green')
        else:
            matching = [s for s in statuses if s['context'] == context]
            require(app in (None, -1) and matching and max(matching, key=lambda s: s['id'])['state'] == 'success', 'required check is missing')

def main():
    global gated_words
    payload = json.load(sys.stdin)
    command, cwd = payload['tool_input']['command'], payload['cwd']
    require(isinstance(command, str) and command.strip(), 'empty command')
    normalized = re.sub(r'\s+', ' ', command.translate({code: None for code in (34, 39, 92, 96)}))
    match = re.search(r'\bgh\b.*?\b(merge|create|update-branch)\b|\bpr (merge|create|update-branch)\b', normalized)
    if not match:
        return None
    gated_words = 'gh ' + match[1] if match[1] else 'pr ' + match[2]
    forbidden = ';&|<>()`$\\\n*?[]{}#~'
    require(not any(c in forbidden or (ord(c) < 32 and c not in ' \t') or ord(c) == 127 for c in command),
            'raw shell metacharacter or control character')
    words = shlex.split(command, comments=False, posix=True)
    require(len(words) >= 3 and words[:2] == ['gh', 'pr'], 'requires one gh pr command')
    sub = words[2]
    require(sub in ('merge', 'create', 'update-branch'), 'unsupported gh write or alias')
    options, pr = {}, None
    names = {'--repo': 'repo', '-R': 'repo'}
    names.update({'--base': 'base', '-B': 'base', '--head': 'head', '-H': 'head', '--title': 'title', '-t': 'title',
                  '--body': 'body', '-b': 'body', '--body-file': 'body-file', '-F': 'body-file'} if sub == 'create'
                 else {'--match-head-commit': 'sha'} if sub == 'merge' else {})
    flags = {'--draft': 'draft', '-d': 'draft', '--fill': 'fill', '-f': 'fill', '--fill-first': 'fill-first', '--fill-verbose': 'fill-verbose'} if sub == 'create' else {'--squash': 'squash', '-s': 'squash'} if sub == 'merge' else {}
    i = 3
    while i < len(words):
        word = words[i]; key, equal, value = word.partition('=')
        if key in names:
            if not equal:
                i += 1
                require(i < len(words), 'missing flag value')
                value = words[i]
            name = names[key]
            require(value and name not in options, 'missing or duplicate option')
            options[name] = value
        elif word in flags:
            require(flags[word] not in options, 'duplicate flag')
            options[flags[word]] = True
        else:
            require(sub != 'create' and pr is None and re.fullmatch(r'[1-9][0-9]*', word), 'unsupported argument')
            pr = int(word)
        i += 1
    selected = options.get('repo', '')
    require(not selected or re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', selected), 'invalid repository')
    require(sub == 'create' or pr is not None, 'missing PR number')
    if sub == 'update-branch':
        return 'allow', 'bare update-branch'
    require(isinstance(cwd, str) and Path(cwd).is_dir(), 'missing working directory')
    os.chdir(cwd)
    nwo = gh('repo', 'view', *([selected] if selected else []), '--json', 'nameWithOwner', '--jq', '.nameWithOwner')
    require(re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', nwo), 'invalid repository answer')
    require(not selected or selected.lower() == nwo.lower(), 'selected repository mismatch')
    default = ref(gh('repo', 'view', nwo, '--json', 'defaultBranchRef', '--jq', '.defaultBranchRef.name'))
    if sub == 'create':
        if 'body-file' in options:
            body = Path(options['body-file'])
            require(body != Path('-') and '..' not in body.parts and '.git' not in body.parts, 'unsafe body file path')
            body = body if body.is_absolute() else Path.cwd() / body
            top = Path(run('git', 'rev-parse', '--show-toplevel')).resolve(strict=True)
            resolved = body.resolve(strict=True)
            fold = case_insensitive(top)
            require(path_within(resolved, top, fold) and any(p.samefile(top) for p in resolved.parents), 'body outside worktree')
            metadata = run('git', 'rev-parse', '--path-format=absolute', '--git-dir', '--git-common-dir').splitlines()
            require(len(metadata) == 2 and all(not path_within(resolved, Path(p).resolve(strict=True), fold) for p in [*metadata, top / '.git']), 'body file is Git metadata')
            safe_file(top, body, allow_empty=True, fold=fold)
        base, head = ref(options.get('base')), ref(options.get('head'))
        require(head != default, 'head is default branch')
        sha = api(f'repos/{nwo}/branches/{head}')['commit']['sha']
        require(re.fullmatch(r'[0-9a-f]{40}', sha), 'head is not pushed')
        if base != default:
            count = gh('pr', 'list', '--repo', nwo, '--head', base, '--state', 'open', '--json', 'number', '--jq', 'length')
            require(re.fullmatch(r'[1-9][0-9]*', count), 'base is neither default nor open PR')
        if options.get('draft'):
            return 'allow', 'draft of pushed task branch'
        top = canonical_checkout(cwd, nwo)
        if head.startswith('orchestration/'):
            records_only(nwo, base, head)
        else:
            accepted(top, nwo, base, sha)
        return 'allow', 'ready creation with bound evidence'
    sha = options.get('sha', '')
    require(options.get('squash') and re.fullmatch(r'[0-9a-f]{40}', sha), 'requires pinned squash merge')
    top = canonical_checkout(cwd, nwo)
    view = json.loads(gh('pr', 'view', str(pr), '--repo', nwo, '--json', 'headRefOid,baseRefName,headRefName,state,isDraft'))
    require(view['state'] == 'OPEN' and view['isDraft'] is False and view['headRefOid'] == sha
            and view['baseRefName'] == default, 'PR is not pinned open ready default-branch head')
    green(nwo, default, sha)
    if view['headRefName'].startswith('orchestration/boundary-'):
        records_only(nwo, default, sha)
    else:
        accepted(top, nwo, default, sha, pr)
    return 'allow', 'pinned green merge with bound evidence'

try:
    answer = main()
except Ask as error:
    answer = 'ask', (gated_words or 'gh/pr merge/create/update-branch') + ': ' + str(error)
except Exception as error:
    answer = 'ask', (gated_words or 'gh/pr merge/create/update-branch') + ': check failed (' + type(error).__name__ + ')'
if answer is not None:
    print(json.dumps(answer))
PY
)
[[ -n $result ]] || exit 0
decision=$("${tools[1]}" -er '.[0] | select(. == "allow" or . == "ask")' <<< "$result")
reason=$("${tools[1]}" -er '.[1] | strings' <<< "$result")
decide "$decision" "$reason"
