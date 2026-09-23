#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["playwright>=1.50"]
# ///
"""全 Markdown の ```mermaid を、公式 npm 配布物 mermaid.min.js で解析・描画する（オフライン）。

準備:  npm install mermaid@<version>   （例: 12.0.0 と 11.14.0 の両方）
実行:  python tools/render_mermaid.py --mermaid-dir <node_modules/mermaid> [--mermaid-dir ...]
結果は evidence/mermaid_render.json に、図ごとのソース SHA-256 付きで記録する。
kit_lint.py check がこの SHA-256 と現行の図を照合し、古い証跡を不合格にする。
"""
from __future__ import annotations
import argparse, hashlib, json, re, sys
from datetime import datetime, timezone
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
JS = """async ({id, code}) => {
  document.body.innerHTML = '';
  const t = await mermaid.parse(code);
  const r = await mermaid.render(id, code);
  document.body.innerHTML = r.svg;
  const s = document.querySelector('svg'); const b = s.getBBox();
  if (b.width <= 0 || b.height <= 0) throw Error('empty svg');
  if (document.querySelector('.error-icon')) throw Error('error diagram');
  return {type: t.diagramType, width: Math.round(b.width), height: Math.round(b.height),
          has_title: !!s.querySelector('title')};
}"""


def blocks():
    for md in sorted(ROOT.rglob('*.md')):
        if 'node_modules' in md.parts: continue
        text = md.read_text(encoding='utf-8'); i = 0
        for m in re.finditer(r'^```mermaid\n(.*?)^```\s*$', text, re.S | re.M):
            i += 1
            yield f'{md.relative_to(ROOT).as_posix()}#{i}', m.group(1)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--mermaid-dir', type=Path, action='append', required=True, help='npm の mermaid パッケージのディレクトリ')
    ap.add_argument('--png-dir', type=Path, help='目視確認用 PNG の出力先（任意）')
    ap.add_argument('--output', type=Path, default=ROOT / 'evidence' / 'mermaid_render.json')
    a = ap.parse_args()
    runs, ok_all = [], True
    with sync_playwright() as p:
        br = p.chromium.launch(headless=True, args=['--no-sandbox'])
        for mdir in a.mermaid_dir:
            ver = json.loads((mdir / 'package.json').read_text())['version']
            js = (mdir / 'dist' / 'mermaid.min.js').read_bytes()
            pg = br.new_page(viewport={'width': 1600, 'height': 1200})
            pg.set_content('<!doctype html><html lang="ja"><head><meta charset="utf-8"></head><body></body></html>')
            pg.add_script_tag(content=js.decode('utf-8'))
            pg.evaluate("() => mermaid.initialize({startOnLoad: false, securityLevel: 'strict'})")
            res = []
            for n, (key, code) in enumerate(blocks()):
                row = {'key': key, 'sha256': hashlib.sha256(code.encode()).hexdigest()}
                try:
                    row |= {'ok': True, **pg.evaluate(JS, {'id': f'd{n}', 'code': code})}
                    if a.png_dir:
                        out = a.png_dir / ver; out.mkdir(parents=True, exist_ok=True)
                        pg.locator('svg').first.screenshot(path=str(out / (re.sub(r'[/#.]', '_', key) + '.png')))
                except Exception as e:
                    row |= {'ok': False, 'error': str(e)[:300]}
                res.append(row)
            neg = pg.evaluate("async () => { try { await mermaid.parse('flowchart LR\\n A[\"x'); return false } catch (e) { return true } }")
            runs.append({'mermaid_version': ver, 'mermaid_min_js_sha256': hashlib.sha256(js).hexdigest(), 'chromium': br.version,
                         'invalid_diagram_rejected': neg, 'diagrams': len(res), 'failed': [r['key'] for r in res if not r['ok']], 'results': res})
            ok_all &= neg and all(r['ok'] for r in res)
            print(f'Mermaid {ver}: {sum(r["ok"] for r in res)}/{len(res)} ok, negative test rejected={neg}')
            pg.close()
        br.close()
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps({'status': 'passed' if ok_all else 'failed', 'executed_at_utc': datetime.now(timezone.utc).isoformat(timespec='seconds'),
                                    'scope': '図の構文解析と描画のみ。図の意味の正しさ・全ホストでの表示は保証しない', 'runs': runs}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return 0 if ok_all else 1


if __name__ == '__main__':
    raise SystemExit(main())
