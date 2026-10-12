"""fill_sweep.py <sweep.json> <pr-comments.json> [extra.tsv] : fill every item's disposition.

review_comment items take the disposition from the orchestrator's reply in their thread
(`fixed:<sha>` or `not-applicable:<reason>` in backticks); extra.tsv (id<TAB>disposition)
overrides or adds. review/issue_comment/annotation/status items get fixed rules below.
Writes the JSON in place only when every item has a disposition; otherwise lists the gaps.
"""
import json, re, sys, collections
sweep_path, comments_path = sys.argv[1], sys.argv[2]
extra = {}
if len(sys.argv) > 3:
    for line in open(sys.argv[3]):
        if line.strip() and not line.startswith('#'):
            k, v = line.rstrip('\n').split('\t')[:2]
            extra[k] = v
sweep = json.load(open(sweep_path)); comments = json.load(open(comments_path))
pat = re.compile(r'`((?:fixed:[0-9a-f]{7,40})|(?:not-applicable:[^`]+))`')
reply = {}
for c in comments:
    if c['user']['login'] == 'chatgpt-codex-connector[bot]' or not c.get('in_reply_to_id'):
        continue
    m = pat.search(c['body'])
    if m:
        reply[str(c['in_reply_to_id'])] = m.group(1)  # the latest reply wins
gaps = []
for it in sweep['items']:
    key = (it.get('url') or '').rsplit('#', 1)[-1]
    cid = key.replace('discussion_r', '')
    d = None
    if cid in extra:
        d = extra[cid]
    elif it['source'] == 'review_comment' and not it.get('bot') and (it.get('body') or '').startswith('Disposition (orchestrator'):
        d = 'not-applicable:the orchestrator disposition reply on a Bot thread, not a finding'
    elif it['source'] == 'review_comment':
        d = reply.get(cid)
    elif it['source'] == 'review':
        body = it.get('body') or ''
        d = 'not-applicable:review object; its findings are the inline threads, each dispositioned on its own' if 'Codex Review' in body else 'not-applicable:review object without a finding'
    elif it['source'] == 'issue_comment':
        d = 'not-applicable:bot summary or onboarding comment, no finding'
    elif it['source'] == 'annotation':
        d = 'not-applicable:runner capacity notice, no finding'
    elif it['source'] == 'status':
        d = 'not-applicable:CI status, no finding'
    if d and not re.fullmatch(r'fixed:[0-9a-f]{7,40}|not-applicable:.+', d):
        d = None
    if d:
        it['disposition'] = d
    else:
        gaps.append((key, it['source'], it.get('level'), (it.get('body') or '')[:80].replace('\n', ' ')))
print('items', len(sweep['items']), 'filled', len(sweep['items']) - len(gaps), 'gaps', len(gaps))
for g in gaps:
    print('GAP', *g)
print('dispositions', collections.Counter(i['disposition'].split(':')[0] for i in sweep['items'] if i.get('disposition')))
if not gaps:
    json.dump(sweep, open(sweep_path, 'w'), indent=2, ensure_ascii=False)
    open(sweep_path, 'a').write('\n')
    print('written', sweep_path)
else:
    sys.exit(1)
