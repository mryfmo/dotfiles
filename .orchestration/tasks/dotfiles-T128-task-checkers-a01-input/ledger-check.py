"""ledger-check.py <record.md> <sweep.json> <audit .last.md>... : every Bot top-level finding of the sweep and
every [P line of the given audits must have a class row in the record's ledger block (id<TAB>class or
audit:<sha7>:<n><TAB>class). Exit 1 and list the gaps otherwise."""
import json, re, sys, pathlib
record, sweep = pathlib.Path(sys.argv[1]).read_text(), json.load(open(sys.argv[2]))
rows = dict(re.findall(r'^((?:\d{6,}|audit:[0-9a-f]{7}:\d+))\t(\S+)$', record, flags=re.M))
need = []
for it in sweep['items']:
    url = it.get('url') or ''
    if it['source'] == 'review_comment' and it.get('bot') and 'discussion_r' in url:
        need.append(url.rsplit('discussion_r', 1)[-1])
# replies by the Bot are rare; top-level is approximated by bot authorship (the fill marks the orchestrator's replies)
for path in sys.argv[3:]:
    m = re.search(r'-audit-([0-9a-f]{7})\.md', path)
    sha7 = m.group(1)
    text = pathlib.Path(path).read_text()
    n = len(re.findall(r'^\[P[0-3]\]', text, flags=re.M))
    need += [f'audit:{sha7}:{i}' for i in range(1, n + 1)]
gaps = [k for k in need if k not in rows]
print(f'ledger rows {len(rows)}; findings {len(need)}; gaps {len(gaps)}')
for g in gaps: print('GAP', g)
sys.exit(1 if gaps else 0)
