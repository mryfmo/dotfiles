#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["pytest>=8", "hypothesis>=6", "pytest-bdd>=8", "coverage>=7", "mutmut>=3"]
# ///
"""参考実装（examples/flowapprove_core）の UT・CT を実行し、実行証跡を evidence/example_tests.json に書く。

証跡には、テストごとの結果・サイズ・確かめたID（req）と、対象コード・テストコード・.feature の
SHA-256 を記録する。kit_lint.py check がこのハッシュを現行ファイルと照合し、古い証跡を不合格にする。
  python tools/run_examples.py [--mutation]
"""
from __future__ import annotations
import argparse, hashlib, json, re, shutil, subprocess, sys, tempfile, tomllib
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def inputs(cfg) -> dict[str, str]:
    files = sorted({p for g in cfg['tests']['inputs'] for p in ROOT.glob(g) if p.is_file() and '__pycache__' not in p.parts and 'mutants' not in p.parts})
    return {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--mutation', action='store_true', help='mutmut によるミューテーションテストも実行する')
    a = ap.parse_args()
    cfg = tomllib.loads((ROOT / 'kit.toml').read_text(encoding='utf-8'))
    proj = ROOT / cfg['tests']['project']
    out = {'executed_at_utc': datetime.now(timezone.utc).isoformat(timespec='seconds'),
           'scope': '参考実装（ドメイン中核と決裁サービス）に対する UT・CT の実行結果。製品全体の試験ではない',
           'tools': {k: version(k) for k in ('pytest', 'hypothesis', 'pytest-bdd', 'coverage')} | {'python': sys.version.split()[0]},
           'inputs_sha256': inputs(cfg), 'levels': {}, 'verified_ids': {}}
    with tempfile.TemporaryDirectory() as tmp:
        for level, path in (('UT', 'tests/unit'), ('CT', 'tests/component')):
            xml, cov = Path(tmp) / f'{level}.xml', Path(tmp) / f'{level}.json'
            r = subprocess.run([sys.executable, '-m', 'coverage', 'run', f'--data-file={tmp}/.cov{level}', '-m', 'pytest', path, '-q',
                                f'--junitxml={xml}'], cwd=proj, capture_output=True, text=True)
            subprocess.run([sys.executable, '-m', 'coverage', 'json', f'--data-file={tmp}/.cov{level}', '-o', str(cov)], cwd=proj, capture_output=True)
            cases = []
            for tc in ET.parse(xml).getroot().iter('testcase'):
                props = {p.get('name'): p.get('value') for p in tc.iter('property')}
                bad = any(tc.find(t) is not None for t in ('failure', 'error', 'skipped'))
                cases.append({'name': tc.get('name'), 'file': tc.get('classname'), 'passed': not bad, 'size': props.get('size'),
                              'req': [x for x in (props.get('req') or '').split(',') if x]})
            totals = json.loads(cov.read_text())['totals']
            files = {k: round(v['summary']['percent_covered'], 1) for k, v in json.loads(cov.read_text())['files'].items()}
            out['levels'][level] = {'exit_code': r.returncode, 'tests': len(cases), 'passed': sum(c['passed'] for c in cases),
                                    'branch_coverage_percent': round(totals['percent_covered'], 1), 'coverage_by_file': files,
                                    'functions': sorted({re.sub(r'\[.*$', '', c['name']) for c in cases}), 'cases': cases}
            for c in cases:                                      # 未実行・失敗・スキップは verifies を発行しない
                for rid in c['req']:
                    e = out['verified_ids'].setdefault(rid, {'levels': [], 'passed': 0, 'failed': 0})
                    e['passed' if c['passed'] else 'failed'] += 1
                    if level not in e['levels']: e['levels'].append(level)
    if a.mutation:
        shutil.rmtree(proj / 'mutants', ignore_errors=True)
        subprocess.run(['mutmut', 'run'], cwd=proj, capture_output=True, text=True, timeout=1800)
        res = subprocess.run(['mutmut', 'results', '--all', 'true'], cwd=proj, capture_output=True, text=True).stdout
        rows = re.findall(r'^\s*(\S+): (\w+)', res, re.M)
        killed = sum(1 for _, s in rows if s == 'killed'); survived = sorted(n for n, s in rows if s == 'survived')
        out['mutation'] = {'tool': f'mutmut {version("mutmut")}', 'target': 'flowapprove/domain.py', 'tests': 'tests/unit',
                           'mutants': len(rows), 'killed': killed, 'survived': survived,
                           'score_percent': round(100 * killed / len(rows), 1) if rows else None}
        shutil.rmtree(proj / 'mutants', ignore_errors=True)
    ok = all(v['exit_code'] == 0 and v['tests'] == v['passed'] for v in out['levels'].values())
    out = {'status': 'passed' if ok else 'failed', **out}
    (ROOT / cfg['tests']['evidence']).write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'status': out['status'], **{k: {x: v[x] for x in ('tests', 'passed', 'branch_coverage_percent')} for k, v in out['levels'].items()},
                      'mutation': {k: v for k, v in out.get('mutation', {}).items() if k != 'tool'}, 'verified_ids': len(out['verified_ids'])}, ensure_ascii=False, indent=2))
    return 0 if ok else 1


if __name__ == '__main__':
    raise SystemExit(main())
