"""task-consistency-check.py <task.md>...: mechanical cross-field checks of a format-2 task file before dispatch.
C1 task_id equals the file name. C2 allowed_files covers .orchestration/<task_id>/** (the task copy and evidence) and
names no other task's .orchestration/<id>/ directory. C3 when reset_of is non-empty, a threat_table row names every
reset_of id's task.md and the task's own. C4 every allowed_files entry is named by a threat_table row (path prefix before any glob). C5 no residual binds a predecessor's hash ("the <pred> file's hash") instead of the task's own.
C6 design_review.receipt is the design file's current design_review.receipt. C7 one row per non-path control name and per orchestrator effect name (the SKILL row unit). C8 (code tasks) every *_EVIDENCE input the body names and origin/main does not yet read has a threat row. C10 (docs tasks) a quoted rule sentence naming a script on origin/main carries no `=`/character-class literal absent from the script and its tests. C9 (docs tasks) a quoted rule sentence that names a script, an *_EVIDENCE variable, a check id or the classes: field must find it on origin/main or carry once/until.
Exit 1 with one line per failure."""
import re, sys, pathlib, fnmatch, subprocess
try:
    import yaml
except ImportError:
    print('needs pyyaml: run with uv run --no-project --with pyyaml'); sys.exit(2)
rc = 0
for arg in sys.argv[1:]:
    p = pathlib.Path(arg); text = p.read_text()
    fm = yaml.safe_load(text.split('\n---\n', 1)[0].lstrip('-\n'))
    tid = fm.get('task_id'); suffix = tid.rsplit('-', 1)[-1]
    fails = []
    if tid != p.stem: fails.append(f'C1 task_id {tid} != file {p.stem}')
    allowed = fm.get('allowed_files') or []
    own_dir = f'.orchestration/{tid}/'
    if not any(a.startswith(own_dir) for a in allowed): fails.append(f'C2 allowed_files lacks {own_dir}**')
    for a in allowed:
        m = re.match(r'\.orchestration/([^/]+)/', a)
        if m and m.group(1) != tid: fails.append(f'C2 allowed_files names another task directory: {a}')
    rows = fm.get('threat_table') or []
    rowtext = '\n'.join((r.get('control') or '') + ' ' + (r.get('disposition') or '') for r in rows)
    reset_of = fm.get('reset_of') or []
    if reset_of:
        for rid in reset_of + [tid]:
            s = rid.rsplit('-', 1)[-1]
            if not re.search(rf'(?:{re.escape(rid)}|-{s})/task\.md', rowtext): fails.append(f'C3 no threat_table row names {rid} task.md')
    for a in allowed:
        base = a.split('*')[0].rstrip('/')
        if rows and base not in rowtext: fails.append(f'C4 allowed path has no threat_table row naming it: {a}')
    # C6: the task points at the design's current receipt
    dr = fm.get('design_review') or {}
    if dr.get('design') and dr.get('receipt'):
        dpath = pathlib.Path(dr['design'])
        if dpath.exists():
            dfm = yaml.safe_load(dpath.read_text().split('\n---\n', 1)[0].lstrip('-\n'))
            cur = ((dfm.get('design_review') or {}).get('receipt'))
            if cur and cur != dr['receipt']: fails.append(f"C6 design_review.receipt {dr['receipt']} is not the design's current receipt {cur}")
    for r in rows:
        m = re.search(r'names the (a\d\d) file\'s hash', r.get('disposition') or '')
        if m and m.group(1) != suffix: fails.append(f'C5 residual binds the {m.group(1)} hash, the task is {suffix}: {r.get("control")[:60]}')
    controls = ' || '.join((r.get('control') or '') for r in rows).lower()
    for name in ('task metadata', 'metadata separators', 'in-process effects', 'workflow and interpreter or environment inputs', 'new or renamed scripts',
                 'orchestrator effect merge', 'orchestrator effect update-branch', 'orchestrator effect forced worker removal'):
        if rows and name not in controls: fails.append(f'C7 threat_table has no row named for: {name}')
    # C7b: one row per allowed_files entry: a control that names two entries combines rows (T703 a01 thread 4247933544)
    prefixes = [re.sub(r'(/\*\*|/\*|\*)$', '', e) for e in (fm.get('allowed_files') or []) if isinstance(e, str)]
    nonpath = ('in-process effects', 'task metadata', 'metadata separators', 'workflow and interpreter', 'new or renamed scripts', 'orchestrator effect')
    for r in rows or []:
        if (r.get('control') or '').lstrip('"').startswith(nonpath): continue  # a non-path control may describe several files
        hit = [e for e in prefixes if e and e in (r.get('control') or '')]
        if len(hit) > 1: fails.append(f'C7b one row names {len(hit)} allowed_files entries ({", ".join(hit)}); one row per entry')
    # C8: a code task that names a new *_EVIDENCE input has a threat row for it (C-19)
    if fm.get('kind') == 'code':
        body8 = text.split('\n---\n', 1)[1] if '\n---\n' in text else ''
        for var in sorted(set(re.findall(r'\b[A-Z][A-Z0-9]+(?:_[A-Z0-9]+)*_EVIDENCE\b', body8))):
            # existing inputs (already read by a script on origin/main) are not "added" inputs
            if subprocess.run(['git', 'grep', '-q', var, 'origin/main', '--', 'scripts', 'Makefile', 'home'], capture_output=True).returncode == 0: continue
            if rows and var not in ' '.join((r.get('control') or '') for r in rows): fails.append(f'C8 the task adds input {var} but no threat row controls it')
    # C10: a quoted rule sentence that names a script present on origin/main states only output the script or its tests carry (C-25)
    if fm.get('kind') == 'docs':
        body10 = text.split('\n---\n', 1)[1] if '\n---\n' in text else ''
        for sent in re.findall(r'"([^"]{20,})"', body10):
            for scr in set(re.findall(r'scripts/[\w./-]+\.(?:sh|py)', sent)):
                if subprocess.run(['git', 'cat-file', '-e', f'origin/main:{scr}'], capture_output=True).returncode: continue
                m = re.search(r'\b(once|until)\b', sent, re.I)
                if m and scr in sent[m.start():]: continue  # the script is named inside its own landing clause
                test = f'tests/unit/test_{pathlib.Path(scr).stem.replace("-", "_")}.py'
                for lit in set(re.findall(r'`([^`]*(?:=|\[[^\]]+\])[^`]*)`', sent)):
                    if subprocess.run(['git', 'grep', '-qF', lit, 'origin/main', '--', scr, test], capture_output=True).returncode:
                        fails.append(f'C10 rule sentence names {scr} beside the literal `{lit}`, which neither the script nor {test} carries on origin/main: "{sent[:60]}…"')
    # C9: a quoted rule sentence names a mechanism as present only if it is on origin/main or carries its landing condition
    if fm.get('kind') == 'docs':
        import subprocess
        body = text.split('\n---\n', 1)[1] if '\n---\n' in text else ''
        for sent in re.findall(r'"([^"]{20,})"', body):
            if re.search(r'\b(once|until)\b', sent): continue
            names = set(re.findall(r'(scripts/[\w./-]+|\b[A-Z][A-Z_]{3,}_EVIDENCE\b|task-consistency-check C\d|\bC\d\b of the task-consistency check|\bclasses:)', sent))
            for n in names:
                probe = n.replace('task-consistency-check ', 'scripts/task-consistency-check.py#').split('#')[0] if n.startswith('task-consistency-check') else n
                if probe.startswith('scripts/'):
                    ok = subprocess.run(['git', 'cat-file', '-e', f'origin/main:{probe}'], capture_output=True).returncode == 0
                elif probe.endswith('_EVIDENCE'):
                    ok = subprocess.run(['git', 'grep', '-q', probe, 'origin/main', '--', 'scripts', 'Makefile'], capture_output=True).returncode == 0
                elif probe == 'classes:':
                    ok = subprocess.run(['git', 'grep', '-q', '^classes:', 'origin/main', '--', '.orchestration/learning/mistakes'], capture_output=True).returncode == 0
                else:
                    ok = False
                if not ok: fails.append(f'C9 rule sentence names {n} as present but it is not on origin/main and the sentence has no landing condition: "{sent[:70]}…"')
    print(f'{p.name}: {"OK" if not fails else "FAIL"}')
    for f in fails: print('  ' + f)
    rc |= 1 if fails else 0
sys.exit(rc)
