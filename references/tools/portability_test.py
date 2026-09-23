#!/usr/bin/env python3
"""テンプレートだけから別名・別構成の最小プロジェクトを作り、kit_lint.py が通ることを確かめる。

「リンターがサンプル専用になっていないか」「テンプレートを埋めれば検査を通るか」
「任意節を節ごと削っても通るか」を確認するための試験。
"""
from __future__ import annotations
import json, re, shutil, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def fill(text: str, fixes: dict[str, str]) -> str:
    text = re.sub(r'^is_template: true\n', '', text, flags=re.M)
    text = re.sub(r'^> 記入方法は .*\n', '', text, flags=re.M)      # 指示書へのリンク行は利用者が消す行
    for a, b in fixes.items(): text = text.replace(a, b)
    return re.sub(r'\{\{(.*?)\}\}', r'\1', text)


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        t = Path(tmp)
        for d in ('docs/product', 'docs/decisions', 'docs/behaviour', 'tools', 'tpl'): (t / d).mkdir(parents=True)
        shutil.copy(ROOT / 'tools/kit_lint.py', t / 'tools')
        tests = {'ut': 'ut/UT_TEMPLATE.md', 'ct': 'ct/CT_TEMPLATE.md', 'st': 'st/ST_TEMPLATE.md', 'uat': 'uat/UAT_TEMPLATE.md'}
        for k in ('prd/PRD_TEMPLATE.md', 'adr/ADR_TEMPLATE.md', 'bdd/BDD_TEMPLATE.md', *tests.values(),
                  *(f'{d}/{d.upper()}_GUIDE.md' for d in ('prd', 'adr', 'bdd', 'ut', 'ct', 'st', 'uat')), '03_CONVENTIONS.md', '06_TEST_STRATEGY.md'):
            dst = t / ('tpl' if 'TEMPLATE' in k or 'GUIDE' in k else '.') / Path(k).name
            shutil.copy(ROOT / k, dst)
        prd = fill((ROOT / 'prd/PRD_TEMPLATE.md').read_text(encoding='utf-8'), {'{{数値・単位・分位・期間}}': 'p95 が 500ms 以下'})
        prd = re.sub(r'^## \d+\. [^\n]*（任意）\n.*?(?=^## )', '', prd, flags=re.M | re.S)   # 任意節を節ごと削除
        (t / 'docs/product/payments.md').write_text(prd, encoding='utf-8')
        adr = fill((ROOT / 'adr/ADR_TEMPLATE.md').read_text(encoding='utf-8'), {'{{高｜中｜低}}': '低', '案{{X}}': '案A'})
        (t / 'docs/decisions/ADR-0001-something.md').write_text(adr, encoding='utf-8')
        (t / 'docs/behaviour/payments.md').write_text(fill((ROOT / 'bdd/BDD_TEMPLATE.md').read_text(encoding='utf-8'), {}), encoding='utf-8')
        (t / 'docs/quality').mkdir()
        for kind, src in tests.items():
            (t / f'docs/quality/{kind}_payments.md').write_text(fill((ROOT / src).read_text(encoding='utf-8'), {}), encoding='utf-8')
        (t / 'kit.toml').write_text('''[docs]
prd = ["docs/product/payments.md"]
adr = ["docs/decisions/ADR-*.md"]
bdd = ["docs/behaviour/*.md"]
ut = ["docs/quality/ut_*.md"]
ct = ["docs/quality/ct_*.md"]
st = ["docs/quality/st_*.md"]
uat = ["docs/quality/uat_*.md"]
other = ["03_CONVENTIONS.md"]
trace = "docs/TRACE.md"
features_dir = "features"
[templates]
prd = "tpl/PRD_TEMPLATE.md"
adr = "tpl/ADR_TEMPLATE.md"
bdd = "tpl/BDD_TEMPLATE.md"
ut = "tpl/UT_TEMPLATE.md"
ct = "tpl/CT_TEMPLATE.md"
st = "tpl/ST_TEMPLATE.md"
uat = "tpl/UAT_TEMPLATE.md"
[adr]
statuses = ["proposed", "accepted", "rejected", "deprecated", "superseded"]
[gherkin]
language = "ja"
[evidence]
mermaid = "evidence/mermaid_render.json"
''', encoding='utf-8')
        for cmd in ('trace', 'extract', 'check'):
            r = subprocess.run([sys.executable, str(t / 'tools/kit_lint.py'), cmd], capture_output=True, text=True)
        rep = json.loads(r.stdout)
        out = {'status': rep['status'], 'errors': rep['errors'], 'warnings': rep['warnings'],
               'stats': {k: v for k, v in rep['stats'].items() if k != 'docs_sha256'},
               'note': 'PRD・ADR・BDD・UT・CT・ST・UAT の全テンプレートのプレースホルダを機械的に埋め、PRD の任意節を全て削除した、別名・別ディレクトリ構成のプロジェクト（テストコードなし）'}
    (ROOT / 'evidence/portability_test.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if out['status'] == 'passed' else 1


if __name__ == '__main__':
    raise SystemExit(main())
