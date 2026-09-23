#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["gherkin-official>=29", "PyYAML>=6"]
# ///
"""PRD/ADR/BDD 文書キット用の汎用リンター（設定駆動）。

サンプル専用の決め打ち（件数・ファイル名）を持たない。kit.toml が指す任意の
PRD/ADR/BDD 文書を検査する。Gherkin は Cucumber 公式 parser で解析する。

  python tools/kit_lint.py check        全検査（終了コード 0=合格 / 1=不合格）。テスト設計書（UT・CT・ST・UAT）が
                                        kit.toml にあれば、その割当・由来・テスト名・実行証跡も検査する
  python tools/kit_lint.py trace        追跡表を生成して書き出す
  python tools/kit_lint.py extract      Markdown 内 Gherkin から .feature を生成
  python tools/kit_lint.py selftest     リンター自身の変異試験
文書検査であり、製品の試験ではない。
"""
from __future__ import annotations
import argparse, hashlib, json, os, re, shutil, sys, tempfile, tomllib
import importlib.metadata as im
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
import yaml
from gherkin.parser import Parser
from gherkin.pickles.compiler import Compiler
from gherkin.stream.id_generator import IdGenerator

FENCE = re.compile(r'^ {0,3}(`{3,}|~{3,})\s*([\w+-]*)\s*$')
EARS = {
    '常時': r'^システムは、.+$',
    'イベント': r'^.+とき、システムは.+$',
    '状態': r'^.+間、システムは.+$',
    '異常': r'^もし.+ならば、システムは.+$',
    'オプション': r'^.+場合、(.+とき、)?システムは.+$',
    '複合': r'^.+間、.+とき、システムは.+$',
}
EARS_END = re.compile(r'(なければならない|てはならない)。$')
ID = r'[A-Z]+-\d{3,4}'
TEST_KINDS = ('ut', 'ct', 'st', 'uat')
ITEM = re.compile(r'(UT|CT|E2E|UAT|PT|PER)-\d{3}')


@dataclass
class Doc:
    path: Path
    rel: str
    text: str
    meta: dict = field(default_factory=dict)
    fences: list = field(default_factory=list)   # (lang, line, code)
    prose: str = ''                              # フェンス内を空行にした本文


class Lint:
    def __init__(self, root: Path):
        self.root = root
        self.cfg = tomllib.loads((root / 'kit.toml').read_text(encoding='utf-8'))
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.stats: dict = {}

    def err(self, code, where, msg): self.errors.append(f'{code} {where}: {msg}')
    def warn(self, code, where, msg): self.warnings.append(f'{code} {where}: {msg}')

    # ---------- 読み込み ----------
    def load(self, path: Path) -> Doc:
        text = path.read_text(encoding='utf-8', errors='strict')
        d = Doc(path, str(path.relative_to(self.root)).replace('\\', '/'), text)
        if not text.endswith('\n'): self.err('E001', d.rel, '末尾改行がない')
        if text.startswith('---\n'):
            try:
                d.meta = yaml.safe_load(text.split('---\n', 2)[1]) or {}
            except Exception as e:
                self.err('E002', d.rel, f'front matter を解析できない: {e}')
        opener, buf, out = None, [], []
        for n, line in enumerate(text.splitlines(), 1):
            m = FENCE.match(line)
            if opener is None:
                if m: opener = (m[1], m[2], n); buf = []; out.append('')
                else: out.append(line)
            else:
                if m and m[1][0] == opener[0][0] and len(m[1]) >= len(opener[0]) and not m[2]:
                    d.fences.append((opener[1], opener[2], '\n'.join(buf) + '\n')); opener = None
                else: buf.append(line)
                out.append('')
        if opener: self.err('E003', f'{d.rel}:{opener[2]}', 'コードフェンスが閉じていない')
        d.prose = '\n'.join(out)
        return d

    def globs(self, key):
        seen, res = set(), []
        for pat in self.cfg['docs'].get(key, []):
            for p in sorted(self.root.glob(pat)):
                if p not in seen: seen.add(p); res.append(p)
        return res

    # ---------- Markdown 共通 ----------
    @staticmethod
    def sections(d: Doc) -> dict[str, str]:
        parts, cur = {}, None
        for line in d.prose.splitlines():
            m = re.match(r'^## (.+)$', line)
            if m: cur = m[1].strip(); parts[cur] = ''
            elif cur: parts[cur] += line + '\n'
        return parts

    @staticmethod
    def tables(block: str):
        res, rows = [], []
        for line in block.splitlines() + ['']:
            if line.strip().startswith('|'):
                rows.append([c.strip() for c in re.split(r'(?<!\\)\|', line.strip())[1:-1]])
            elif rows:
                if len(rows) >= 2 and all(re.fullmatch(r':?-{3,}:?', c) for c in rows[1]):
                    res.append((rows[0], rows[2:]))
                rows = []
        return res

    def check_markdown(self, docs: list[Doc]):
        anchors = {}
        for d in docs:
            ids = re.findall(r'<a id="([^"]+)"></a>', re.sub(r'`[^`\n]*`', '', d.prose))
            dup = {i for i in ids if ids.count(i) > 1}
            if dup: self.err('E010', d.rel, f'アンカー重複: {sorted(dup)}')
            anchors[d.rel] = set(ids)
            rows = []
            for n, line in enumerate(d.prose.splitlines() + [''], 1):
                if line.strip().startswith('|'):
                    rows.append((n, len(re.findall(r'(?<!\\)\|', line.strip())) - 1))
                else:
                    if rows and len({w for _, w in rows}) > 1:
                        self.err('E011', f'{d.rel}:{rows[0][0]}', '表の列数が不揃い')
                    rows = []
            levels = [len(m[1]) for m in re.finditer(r'^(#{1,6}) ', d.prose, re.M)]
            if levels.count(1) != 1: self.err('E012', d.rel, 'H1 はちょうど1つ')
            for a, b in zip(levels, levels[1:]):
                if b > a + 1: self.err('E013', d.rel, f'見出し階層が飛んでいる (H{a}→H{b})'); break
            if not d.meta.get('is_template') and re.search(r'\{\{.*?\}\}', re.sub(r'`[^`\n]*`', '', d.prose)):
                self.err('E014', d.rel, '未置換のプレースホルダ {{...}} が残っている')
        nlinks = 0
        for d in docs:
            for m in re.finditer(r'(?<!\!)\[[^\]]*\]\(([^)\s]+)\)', re.sub(r'`[^`\n]*`', '', d.prose)):
                href = m[1]
                if re.match(r'^[a-z][a-z0-9+.-]*:', href):
                    if not href.startswith(('https://', 'http://', 'mailto:')):
                        self.err('E015', d.rel, f'許可しないリンク種別: {href}')
                    continue
                nlinks += 1
                p, _, frag = href.partition('#')
                target = (d.path.parent / p).resolve() if p else d.path
                if not target.is_file(): self.err('E016', d.rel, f'リンク切れ: {href}'); continue
                trel = str(target.relative_to(self.root.resolve())).replace('\\', '/')
                if frag and frag not in anchors.get(trel, set()):
                    self.err('E017', d.rel, f'アンカーが存在しない（明示アンカーのみ可）: {href}')
        self.stats['relative_links'] = nlinks

    def check_template_conformance(self, d: Doc, tpl: Doc):
        th = [(h, '（任意）' in h) for h in self.sections(tpl)]
        dh = list(self.sections(d))
        allowed = [h for h, _ in th]
        for h, opt in th:
            if not opt and h not in dh: self.err('E020', d.rel, f'必須節がない: 「{h}」')
        for h in dh:
            if h not in allowed: self.err('E021', d.rel, f'テンプレートにない節: 「{h}」')
        if [h for h in dh if h in allowed] != [h for h in allowed if h in dh]:
            self.err('E022', d.rel, '節の順序がテンプレートと異なる')
        ts, ds = self.sections(tpl), self.sections(d)
        for h in dh:
            if h in ts:
                have = [tuple(hd) for hd, _ in self.tables(ds[h])]
                for hd, _ in self.tables(ts[h]):
                    if tuple(hd) not in have:
                        self.err('E023', d.rel, f'「{h}」にテンプレートの表がない: {" | ".join(hd)}')
        tk, dk = set(tpl.meta) - {'is_template'}, set(d.meta) - {'sample'}
        if tk != dk: self.err('E024', d.rel, f'front matter のキーがテンプレートと異なる: 不足{sorted(tk-dk)} 余分{sorted(dk-tk)}')

    # ---------- PRD ----------
    def parse_prd(self, d: Doc) -> dict:
        m = {'goals': set(), 'kpis': {}, 'ids': set(), 'fr': {}, 'nfr': {}, 'nvt': {}}
        for hd, rows in self.tables(d.prose):
            for r in rows:
                cell = re.sub(r'<a id="[^"]+"></a>', '', r[0]).strip()
                if not re.fullmatch(ID, cell): continue
                if cell in m['ids']: self.err('E030', d.rel, f'ID 重複: {cell}')
                m['ids'].add(cell)
                row = dict(zip(hd, r)); pre = cell.split('-')[0]
                if pre == 'GOAL': m['goals'].add(cell)
                elif pre in ('KPI', 'GRD'): m['kpis'][cell] = row
                elif pre == 'FR': m['fr'][cell] = row
                elif pre == 'NFR': m['nfr'][cell] = row
                elif pre == 'NVT': m['nvt'][cell] = row
        return m

    def check_prd(self, d: Doc, m: dict):
        used = set()
        for fid, row in m['fr'].items():
            stmt, typ = row.get('要求文', ''), row.get('型', '')
            if f'<a id="{fid}"></a>' not in d.prose: self.err('E031', d.rel, f'{fid}: 明示アンカーがない')
            if typ not in EARS: self.err('E032', d.rel, f'{fid}: 型が EARS の6種でない: 「{typ}」')
            elif not re.match(EARS[typ], stmt): self.err('E033', d.rel, f'{fid}: 要求文が「{typ}」の構文に合わない')
            if stmt.count('。') != 1 or not EARS_END.search(stmt):
                self.err('E034', d.rel, f'{fid}: 要求文は1文で「…なければならない。／…てはならない。」で終える（単一性）')
            if row.get('優先度') not in ('Must', 'Should', 'Could'): self.err('E035', d.rel, f'{fid}: 優先度が Must/Should/Could でない')
            src = set(re.findall(ID, row.get('根拠', '')))
            if not src: self.err('E036', d.rel, f'{fid}: 根拠IDがない')
            for s in src - m['ids']: self.err('E037', d.rel, f'{fid}: 根拠 {s} が文書内に存在しない')
            used |= src
            acc = set(re.findall(ID, row.get('受入', '')))
            if not acc: self.err('E038', d.rel, f'{fid}: 受入（RULE または NVT）がない')
            for s in {a for a in acc if a.startswith('NVT')} - set(m['nvt']): self.err('E039', d.rel, f'{fid}: {s} が検証計画にない')
        for g in sorted(m['goals'] - used): self.err('E040', d.rel, f'{g}: どの FR からも根拠として参照されていない')
        for kid, row in m['kpis'].items():
            means = row.get('計測手段', '')
            refs = set(re.findall(r'N?FR-\d{3}', means))
            if not refs and '外部：' not in means: self.err('E041', d.rel, f'{kid}: 計測手段（FR-ID または「外部：」）がない')
            for s in refs - set(m['fr']) - set(m['nfr']): self.err('E042', d.rel, f'{kid}: 計測手段 {s} が存在しない')
        for nid, row in m['nfr'].items():
            if f'<a id="{nid}"></a>' not in d.prose: self.err('E031', d.rel, f'{nid}: 明示アンカーがない')
            nv = set(re.findall(r'NVT-\d{3}', row.get('検証', '')))
            if not nv: self.err('E043', d.rel, f'{nid}: 検証計画 NVT がない')
            for s in nv - set(m['nvt']): self.err('E039', d.rel, f'{nid}: {s} が検証計画にない')
            if not re.search(r'\d', row.get('合格基準', '')): self.err('E044', d.rel, f'{nid}: 合格基準に数値がない')
        pr = [r.get('優先度') for r in m['fr'].values()]
        if len(pr) >= 10 and set(pr) == {'Must'}: self.warn('W045', d.rel, '全 FR が Must。優先順位付けになっていない')

    # ---------- BDD ----------
    def parse_bdd(self, d: Doc) -> dict:
        out = {'scenarios': [], 'rules': {}, 'features': [], 'steps': []}
        g = self.cfg.get('gherkin', {})
        for lang, line, code in d.fences:
            if lang != 'gherkin': continue
            where = f'{d.rel}:{line}'
            try:
                doc = Parser().parse(code); doc['uri'] = where
                pickles = Compiler(IdGenerator()).compile(doc)
            except Exception as e:
                self.err('E050', where, f'公式 Gherkin parser が拒否: {str(e)[:200]}'); continue
            feat = doc['feature']
            if g.get('language') and feat['language'] != g['language']:
                self.err('E051', where, f'言語が {g["language"]} でない: {feat["language"]}')
            if not re.search(r'^# language: ', code, re.M): self.err('E052', where, '「# language:」の明示がない')
            ft = [t['name'] for t in feat['tags'] if t['name'].startswith('@FEAT-')]
            if len(ft) != 1: self.err('E053', where, 'Feature に @FEAT-nnn タグがちょうど1つ必要')
            out['features'].append({'tag': ft[0][1:] if ft else '', 'code': code})
            for ch in feat['children']:
                if 'scenario' in ch: self.err('E054', where, f'Rule に属さないシナリオ: {ch["scenario"]["name"]}')
                if 'rule' not in ch: continue
                rule = ch['rule']
                rt = [t['name'][1:] for t in rule['tags'] if t['name'].startswith('@RULE-')]
                if len(rt) != 1: self.err('E055', where, f'Rule「{rule["name"]}」に @RULE-nnn タグがちょうど1つ必要'); continue
                if rt[0] in out['rules']: self.err('E056', where, f'RULE ID 重複: {rt[0]}')
                scs = [c['scenario'] for c in rule['children'] if 'scenario' in c]
                if not scs: self.err('E057', where, f'{rt[0]}: シナリオがない')
                out['rules'][rt[0]] = {'name': rule['name'], 'scn': [], 'req': set()}
                for sc in scs:
                    tags = [t['name'][1:] for t in sc['tags']]
                    sid = [t for t in tags if t.startswith('SCN-')]
                    req = [t for t in tags if re.match(r'N?FR-', t)]
                    if len(sid) != 1: self.err('E058', where, f'「{sc["name"]}」に @SCN-nnn がちょうど1つ必要'); continue
                    if not req: self.err('E059', where, f'{sid[0]}: @FR-nnn / @NFR-nnn タグがない')
                    kinds, last = [], None
                    for st in sc['steps']:
                        if st.get('keywordType') in ('Context', 'Action', 'Outcome'): last = st['keywordType']
                        kinds.append(last); out['steps'].append(st['text'])
                        for term in g.get('forbidden_terms', []):
                            if term in st['text']: self.err('E060', where, f'{sid[0]}: 実装・試験用語「{term}」がステップに混入')
                    if 'Action' not in kinds or 'Outcome' not in kinds:
                        self.err('E061', where, f'{sid[0]}: もし／ならば が揃っていない')
                    elif kinds.index('Outcome') < len(kinds) - 1 - kinds[::-1].index('Action'):
                        self.err('E062', where, f'{sid[0]}: ならば の後に もし が再登場（複数の振る舞いを1シナリオに詰めている）')
                    if len(sc['steps']) > g.get('max_steps', 7): self.warn('W063', where, f'{sid[0]}: ステップ数 {len(sc["steps"])}（推奨 3〜5）')
                    n = sum(1 for p in pickles if sc['id'] in p['astNodeIds'])
                    out['scenarios'].append({'id': sid[0], 'rule': rt[0], 'req': req, 'name': sc['name'], 'cases': n})
                    out['rules'][rt[0]]['scn'].append(sid[0]); out['rules'][rt[0]]['req'] |= set(req)
        ids = [s['id'] for s in out['scenarios']]
        for i in sorted({i for i in ids if ids.count(i) > 1}): self.err('E064', d.rel, f'SCN ID 重複: {i}')
        return out

    def check_cross(self, prd: Doc, pm: dict, bdds):
        rules, scn_by_req = {}, {}
        for d, b in bdds:
            rules |= b['rules']
            for s in b['scenarios']:
                for r in s['req']:
                    if r not in pm['fr'] and r not in pm['nfr']: self.err('E070', d.rel, f'{s["id"]}: 未知の要件タグ {r}')
                    scn_by_req.setdefault(r, []).append(s['id'])
        for fid, row in pm['fr'].items():
            want = {a for a in re.findall(ID, row.get('受入', '')) if a.startswith('RULE')}
            have = {rid for rid, r in rules.items() if fid in r['req']}
            for r in sorted(want - set(rules)): self.err('E071', prd.rel, f'{fid}: 受入 {r} が BDD に存在しない')
            if want != have:
                self.err('E072', prd.rel, f'{fid}: PRD の受入 {sorted(want)} と BDD タグから逆算した {sorted(have)} が不一致')
        for rid, r in rules.items():
            if not r['req']: self.err('E073', 'BDD', f'{rid}: どの要件にも結び付いていない')
        norm = lambda s: re.sub(r'\d+', 'N', re.sub(r'<[^>]+>', '<>', re.sub(r'"[^"]*"', '""', s)))
        steps = [norm(s) for _, b in bdds for s in b['steps']]
        if steps:
            ratio = len(set(steps)) / len(steps)
            self.stats |= {'steps': len(steps), 'unique_step_patterns': len(set(steps)), 'unique_step_ratio': round(ratio, 3)}
            mx = self.cfg.get('gherkin', {}).get('max_unique_step_ratio', 1.0)
            if ratio > mx: self.err('E074', 'BDD', f'ステップ文言の一回限り率 {ratio:.2f} > {mx}（語彙を再利用していない）')
        return rules, scn_by_req

    # ---------- ADR ----------
    def check_adr(self, d: Doc, pm: dict, all_adr: dict):
        vocab = self.cfg['adr']['statuses']
        st, aid = str(d.meta.get('status', '')), str(d.meta.get('id', ''))
        if st not in vocab: self.err('E080', d.rel, f'status が語彙 {vocab} にない: {st}')
        if not re.fullmatch(r'ADR-\d{4}', aid): self.err('E081', d.rel, 'id は ADR-nnnn')
        if not d.path.name.startswith(aid): self.err('E082', d.rel, 'ファイル名が id で始まっていない')
        for r in d.meta.get('addresses') or []:
            if r not in pm['fr'] and r not in pm['nfr']: self.err('E083', d.rel, f'addresses の {r} が PRD にない')
        if not d.meta.get('addresses'): self.err('E084', d.rel, 'addresses（関係する要件ID）が空')
        for other in d.meta.get('supersedes') or []:
            o = all_adr.get(other)
            if not o: self.err('E085', d.rel, f'supersedes の {other} が存在しない')
            elif o.meta.get('superseded-by') != aid or o.meta.get('status') != 'superseded':
                self.err('E086', d.rel, f'{other} 側に superseded-by: {aid} と status: superseded が必要（双方向）')
        if st == 'superseded' and not d.meta.get('superseded-by'): self.err('E087', d.rel, 'superseded なのに superseded-by がない')
        if d.meta.get('confidence') not in ('高', '中', '低'): self.err('E088', d.rel, 'confidence は 高/中/低')
        sec = self.sections(d)
        pick = lambda kw: next((v for k, v in sec.items() if kw in k), '')
        opts = re.findall(r'^[-*] \*\*(案[A-Z])\*\*', pick('検討した選択肢'), re.M)
        if len(opts) < 2: self.err('E089', d.rel, '選択肢が2つ未満')
        dec = pick('決定（')
        ch = re.search(r'採用：\*\*(案[A-Z])\*\*', dec)
        if not ch or ch[1] not in opts: self.err('E090', d.rel, '「採用：**案X**」が選択肢一覧と対応しない')
        if 'ため' not in dec: self.err('E091', d.rel, '決定に理由（…ため）がない')
        if '確認方法' not in dec: self.err('E094', d.rel, '確認方法（Confirmation）がない')
        pros = pick('長所・短所')
        for o in opts:
            blk = re.search(rf'^### {o}.*?(?=^### |\Z)', pros, re.M | re.S)
            if not blk: self.err('E092', d.rel, f'{o} の長所・短所がない')
            elif '短所' not in blk[0]: self.err('E093', d.rel, f'{o} に短所の記載がない（良いことだけの比較）')

    # ---------- テスト設計書（UT・CT・ST・UAT） ----------
    def check_vocab(self, d: Doc):
        for key, allowed in self.cfg.get('vocab', {}).get(str(d.meta.get('doc_type')), {}).items():
            if str(d.meta.get(key)) not in allowed:
                self.err('E025', d.rel, f'front matter の {key} が語彙 {allowed} にない: {d.meta.get(key)}')
        if d.meta.get('last_run') in ('passed', 'failed') and 'evidence' in d.meta:
            ev = str(d.meta.get('evidence'))
            if ev == 'なし' or not (d.path.parent / ev).is_file():
                self.err('E155', d.rel, f'last_run: {d.meta["last_run"]} なのに実行証跡がない: {ev}')

    def parse_tests(self, docs: dict[str, list[Doc]]) -> dict:
        t = {'items': {}, 'nvt': {}, 'feat': {}, 'by_kind': {k: 0 for k in TEST_KINDS}}
        for kind, ds in docs.items():
            for d in ds:
                for hd, rows in self.tables(d.prose):
                    for r in rows:
                        cell, row = r[0].strip(), dict(zip(hd, r))
                        if ITEM.fullmatch(cell):
                            if cell in t['items']: self.err('E140', d.rel, f'テスト項目のID重複: {cell}')
                            t['items'][cell] = {'kind': kind, 'doc': d, 'row': row}
                            if not cell.startswith('PER'): t['by_kind'][kind] += 1
                        elif re.fullmatch(r'NVT-\d{3}', cell): t['nvt'].setdefault(cell, []).append(d.rel)
                        elif re.fullmatch(r'FEAT-\d{3}', cell): t['feat'].setdefault(cell, []).append(d.rel)
        return t

    def check_tests(self, docs, t, pm, rules, scns, feats, adrs):
        known = pm['ids'] | set(rules) | scns | feats | {a.meta.get('id') for a in adrs} | set(t['items'])
        used = set()
        for tid, it in t['items'].items():
            d, row = it['doc'], it['row']
            if '由来' in row:
                src = set(re.findall(ID, row['由来'])); used |= src
                if not src: self.err('E141', d.rel, f'{tid}: 由来のIDがない')
                for x in sorted(src - known): self.err('E142', d.rel, f'{tid}: 由来 {x} が存在しない')
            for x in sorted(set(re.findall(r'SCN-\d{3}', row.get('通るシナリオ', ''))) - scns): self.err('E143', d.rel, f'{tid}: シナリオ {x} が BDD にない')
            for col, pre, code in (('ペルソナ', 'PER', 'E144'), ('主体', 'ACT', 'E145')):
                for x in re.findall(rf'{pre}-\d{{3}}', row.get(col, '')):
                    if x not in known: self.err(code, d.rel, f'{tid}: {col} {x} が存在しない')
        if docs['ct'] or docs['st']:
            for n in pm['nvt']:
                where = t['nvt'].get(n, [])
                if len(where) != 1: self.err('E146', 'テスト設計書', f'{n}: ちょうど1つの水準の文書に割り当てる（現在 {len(where)} 件: {where}）')
            for n in sorted(set(t['nvt']) - set(pm['nvt'])): self.err('E147', t['nvt'][n][0], f'{n} が PRD の検証計画にない')
            for f in sorted(feats - set(t['feat'])): self.err('E148', 'テスト設計書', f'{f}: BDD の機能が CT・ST のどの文書にも割り当てられていない')
            for f in sorted(set(t['feat']) - feats): self.err('E148', t['feat'][f][0], f'{f} が BDD にない')
            for a in adrs:
                if a.meta.get('status') == 'accepted' and a.meta.get('id') not in used:
                    self.err('E149', a.rel, 'accepted の設計判断を由来とするテスト項目が1件もない（確認方法が宙に浮いている）')
        for d in docs['uat']:
            goals = {g for tid, it in t['items'].items() if it['doc'] is d and tid.startswith('UAT') for g in re.findall(r'GOAL-\d{3}', it['row'].get('由来', ''))}
            for g in sorted(pm['goals'] - goals): self.err('E150', d.rel, f'{g}: 受入シナリオがない')
            for a in sorted(i for i in pm['ids'] if i.startswith('ACT-')):
                if a not in d.prose: self.err('E151', d.rel, f'{a}: ペルソナも対象外の理由もない')
        for d in (x for ds in docs.values() for x in ds):                      # 1章の「由来」に挙げたIDが、本文のどこにも出てこないのは設計の漏れ
            m = re.search(r'^\| 由来 \|([^\n]*)$', d.prose, re.M)
            if not m: continue
            line, rest = m.group(1), d.prose.replace(m.group(0), '')
            ids = set(re.findall(ID, line))
            for pre, a, b in re.findall(r'([A-Z]+)-(\d{3,4})〜\1-(\d{3,4})', line):
                ids |= {f'{pre}-{n:0{len(a)}d}' for n in range(int(a), int(b) + 1)}
            for x in sorted(ids):
                if x not in known: self.err('E142', d.rel, f'1章の由来 {x} が存在しない')
                elif not re.search(rf'{x}(?!\d)', rest): self.err('E157', d.rel, f'1章の由来 {x} が、本文のどのテスト項目・割当にも出てこない')
        tc = self.cfg.get('tests')
        if not tc: return
        code = '\n'.join(p.read_text(encoding='utf-8') for g in tc['code'] for p in sorted(self.root.glob(g)))
        for tid, it in t['items'].items():
            for name in re.findall(r'`([A-Za-z_][\w]*)`', it['row'].get('テスト名', '')):
                if not re.search(rf'\b{re.escape(name)}\b', code): self.err('E152', it['doc'].rel, f'{tid}: テスト名 {name} がテストコードにない')
        ev = self.root / tc['evidence']
        if not ev.is_file(): self.warn('W154', ev.name, 'テストの実行証跡がない（tools/run_examples.py を実行）'); return
        data = json.loads(ev.read_text(encoding='utf-8'))
        now = {p.relative_to(self.root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for g in tc['inputs'] for p in self.root.glob(g)
               if p.is_file() and '__pycache__' not in p.parts and 'mutants' not in p.parts}
        if data.get('inputs_sha256') != now: self.err('E153', ev.name, 'テストの実行証跡が現行のコード・テスト・.feature と不一致＝証跡が古い。再実行が必要')
        if data.get('status') != 'passed': self.err('E156', ev.name, '実行証跡が不合格')
        self.verified = data.get('verified_ids', {})
        for d in (x for ds in docs.values() for x in ds):                      # 文書に書いた実行結果の数値が、証跡と食い違っていないか
            lv = data.get('levels', {}).get(str(d.meta.get('doc_type')).upper())
            if not lv or (d.path.parent / str(d.meta.get('evidence'))).resolve() != ev.resolve(): continue
            want = [f"{lv['tests']}件"] + ([f"{data['mutation']['score_percent']}%"] if d.meta.get('doc_type') == 'ut' and data.get('mutation') else [])
            want += [f'{pct:g}%' for f, pct in lv.get('coverage_by_file', {}).items() if f in str(d.meta.get('target'))]
            for w in want:
                if w not in d.prose: self.err('E158', d.rel, f'直近の結果が実行証跡と食い違う（証跡の値 {w} が文書にない）')

    # ---------- 追跡表 ----------
    def build_trace(self, prd: Doc, pm, rules, scn_by_req, adrs, t=None) -> str:
        by = {}
        for a in adrs:
            for r in a.meta.get('addresses') or []: by.setdefault(r, []).append(a.meta['id'])
        j = lambda xs: ', '.join(sorted(set(xs))) or '—'
        href = os.path.relpath(prd.path, (self.root / self.cfg['docs']['trace']).parent).replace('\\', '/')   # 追跡表の置き場所からの相対パス
        t = t or {'items': {}, 'nvt': {}}
        ver = getattr(self, 'verified', {})
        def cond(ids): return j(tid for tid, it in t['items'].items() if not tid.startswith('PER') and set(ids) & set(re.findall(ID, it['row'].get('由来', ''))))
        def ran(ids): return j(l for i in ids for l in ver.get(i, {}).get('levels', []) if not ver[i]['failed'])
        L = ['<!-- 自動生成：python tools/kit_lint.py trace。手で編集しない（check が差分を不合格にする）。 -->',
             '# 追跡表：要件→ルール→シナリオ→設計判断→専用検証', '',
             'ルール・シナリオ・テスト条件は要件を**具体化**（specifies）するだけで、合格を意味しない。「合格した実行」の列だけが実行証跡に基づく。ただし、その要件を確かめるテストが1件以上合格したことを示すだけで、要件の全体が検証済みであることは意味しない。', '',
             '## 機能要件', '', '| 要件 | 優先度 | ルール | シナリオ | 設計判断 | 専用検証 | テスト条件 | 合格した実行 |', '|---|---|---|---|---|---|---|---|']
        for fid, row in pm['fr'].items():
            L.append(f'| [{fid}]({href}#{fid}) | {row.get("優先度", "")} | {j(r for r, v in rules.items() if fid in v["req"])} | {j(scn_by_req.get(fid, []))} | {j(by.get(fid, []))} | {j(a for a in re.findall(ID, row.get("受入", "")) if a.startswith("NVT"))} | {cond([fid] + [r for r, v in rules.items() if fid in v["req"]])} | {ran([fid])} |')
        L += ['', '## 非機能要件', '', '| 要件 | 品質特性 | 専用検証 | 割当先の文書 | テスト条件 | 設計判断 |', '|---|---|---|---|---|---|']
        for nid, row in pm['nfr'].items():
            nv = re.findall(r"NVT-[0-9]{3}", row.get("検証", ""))
            L.append(f'| [{nid}]({href}#{nid}) | {row.get("品質特性", "")} | {j(nv)} | {j(w for n in nv for w in t["nvt"].get(n, []))} | {cond([nid] + nv)} | {j(by.get(nid, []))} |')
        L += ['', '## ルール', '', '| ルール | 業務ルール | シナリオ | 要件 |', '|---|---|---|---|']
        for rid in sorted(rules):
            L.append(f'| {rid} | {rules[rid]["name"]} | {", ".join(rules[rid]["scn"])} | {j(rules[rid]["req"])} |')
        if t['items']:
            L += ['', '## テスト項目', '', '| ID | 水準 | 由来 |', '|---|---|---|']
            for tid, it in t['items'].items():
                if not tid.startswith('PER'): L.append(f'| {tid} | {it["kind"].upper()} | {j(re.findall(ID, it["row"].get("由来", "")))} |')
        return '\n'.join(L) + '\n'

    # ---------- Mermaid 証跡 ----------
    def check_mermaid(self, docs):
        blocks = {}
        for d in docs:
            i = 0
            for lang, line, code in d.fences:
                if lang != 'mermaid': continue
                i += 1; blocks[f'{d.rel}#{i}'] = hashlib.sha256(code.encode()).hexdigest()
                if re.search(r'(?im)^\s*click\b|<script|javascript:', code): self.err('E100', f'{d.rel}:{line}', 'Mermaid に click/script')
                if 'accTitle' not in code: self.err('E101', f'{d.rel}:{line}', 'Mermaid に accTitle（代替テキスト）がない')
        self.stats['mermaid_blocks'] = len(blocks)
        ev = self.root / self.cfg['evidence']['mermaid']
        if not ev.is_file(): self.warn('W102', ev.name, 'Mermaid 描画証跡がない（tools/render_mermaid.py を実行）'); return
        for run in json.loads(ev.read_text(encoding='utf-8'))['runs']:
            got = {r['key']: r['sha256'] for r in run['results'] if r['ok']}
            if got != blocks: self.err('E103', ev.name, f'描画証跡（Mermaid {run["mermaid_version"]}）が現行の図と不一致＝証跡が古い。再描画が必要')

    # ---------- 実行 ----------
    def run(self, write_trace=False, write_features=False) -> dict:
        tpl = {k: self.load(self.root / v) for k, v in self.cfg['templates'].items()}
        prds, adrs, bdds = ([self.load(p) for p in self.globs(k)] for k in ('prd', 'adr', 'bdd'))
        tdocs = {k: [self.load(p) for p in self.globs(k)] for k in TEST_KINDS}
        tflat = [d for ds in tdocs.values() for d in ds]
        special = {d.path for d in list(tpl.values()) + prds + adrs + bdds + tflat} | {self.root / self.cfg['docs']['trace']}
        others = [self.load(p) for p in self.globs('other') if p not in special]
        all_docs = list(tpl.values()) + prds + adrs + bdds + tflat + others
        for kind, ds in (('prd', prds), ('adr', adrs), ('bdd', bdds), *tdocs.items()):
            for d in ds: self.check_template_conformance(d, tpl[kind]); self.check_vocab(d)
        if len(prds) != 1:
            self.err('E110', 'kit.toml', '要件正本（PRD）はちょうど1件を指定する'); return self.report()
        prd = prds[0]; pm = self.parse_prd(prd); self.check_prd(prd, pm)
        parsed = [(d, self.parse_bdd(d)) for d in bdds]
        self.parse_bdd(tpl['bdd'])                       # テンプレートの Gherkin も公式 parser を通す
        rules, scn_by_req = self.check_cross(prd, pm, parsed)
        amap = {a.meta.get('id'): a for a in adrs}
        for a in adrs: self.check_adr(a, pm, amap)
        tests = self.parse_tests(tdocs)
        scns = {s['id'] for _, b in parsed for s in b['scenarios']}
        feats_ids = {f['tag'] for _, b in parsed for f in b['features'] if f['tag']}
        if tflat: self.check_tests(tdocs, tests, pm, rules, scns, feats_ids, adrs)
        trace = self.build_trace(prd, pm, rules, scn_by_req, adrs, tests)
        tpath = self.root / self.cfg['docs']['trace']
        if write_trace: tpath.write_text(trace, encoding='utf-8')
        if not tpath.is_file() or tpath.read_text(encoding='utf-8') != trace:
            self.err('E120', self.cfg['docs']['trace'], '追跡表が正本と不一致（trace を再生成）')
        feats = {f'{f["tag"]}.feature': f['code'] for _, b in parsed for f in b['features'] if f['tag']}
        fdir = self.root / self.cfg['docs']['features_dir']
        if write_features:
            fdir.mkdir(exist_ok=True)
            for old in fdir.glob('*.feature'): old.unlink()
            for n, c in feats.items(): (fdir / n).write_text(c, encoding='utf-8')
        have = {p.name: p.read_text(encoding='utf-8') for p in fdir.glob('*.feature')} if fdir.is_dir() else {}
        if have != feats: self.err('E121', self.cfg['docs']['features_dir'], '.feature が Markdown の Gherkin と不一致（extract を再実行。編集は片方向のみ）')
        if tpath.is_file(): all_docs.append(self.load(tpath))
        self.check_markdown(all_docs); self.check_mermaid(all_docs)
        self.stats |= {'documents': len(all_docs), 'fr': len(pm['fr']), 'nfr': len(pm['nfr']), 'rules': len(rules),
                       'scenarios': sum(len(b['scenarios']) for _, b in parsed),
                       'expanded_cases': sum(s['cases'] for _, b in parsed for s in b['scenarios']),
                       'adr': len(adrs), 'feature_files': len(feats), 'test_items': tests['by_kind'], 'personas': sum(1 for i in tests['items'] if i.startswith('PER')),
                       'docs_sha256': {d.rel: hashlib.sha256(d.text.encode()).hexdigest() for d in all_docs}}
        return self.report()

    def report(self) -> dict:
        return {'status': 'passed' if not self.errors else 'failed', 'errors': self.errors, 'warnings': self.warnings, 'stats': self.stats,
                'tools': {'python': sys.version.split()[0], 'gherkin-official': im.version('gherkin-official'), 'PyYAML': im.version('PyYAML')},
                'executed_at_utc': datetime.now(timezone.utc).isoformat(timespec='seconds'),
                'scope': '文書検査のみ。製品試験・承認ではない'}


MUTATIONS = [  # (名前, 対象, 置換前の正規表現, 置換後, 検出すべきコード)
    ('FRを2文にする', 'prd', r'(<a id="FR-001"></a>FR-001 \| [^|]+ \| [^|]+?)。', r'\1。さらに別の義務も負わなければならない。', 'E034'),
    ('FRの型と構文の不一致', 'prd', r'(<a id="FR-001"></a>FR-001 \| )[^|]+ \|', r'\1イベント |', 'E033'),
    ('存在しない根拠ID', 'prd', r'(<a id="FR-001"></a>FR-001 \|[^\n]*?)GOAL-\d{3}', r'\1GOAL-999', 'E037'),
    ('NFRの検証計画欠落', 'prd', r'(<a id="NFR-001"></a>NFR-001 \|[^\n]*?)NVT-\d{3}', r'\1なし', 'E043'),
    ('必須節の改名', 'prd', r'^## 5\. .*$', '## 5. 勝手な節', 'E020'),
    ('Gherkin構文破壊', 'bdd', r'^(\s+)ならば ', r'\1ナラバ ', 'E050'),
    ('SCN重複', 'bdd', r'@SCN-002', '@SCN-001', 'E064'),
    ('未知の要件タグ', 'bdd', r'(@SCN-001 )@FR-\d{3}', r'\1@FR-999', 'E070'),
    ('PRD受入とBDDタグの不一致', 'bdd', r'(@SCN-001 @FR-\d{3})', r'\1 @FR-020', 'E072'),
    ('試験用語の混入', 'bdd', r'(@SCN-001[^\n]*\n[^\n]*\n\s+前提 )', r'\1テストダブルの', 'E060'),
    ('ADR採用案が一覧にない', 'adr', r'採用：\*\*案[A-Z]\*\*', '採用：**案Z**', 'E090'),
    ('ADR addresses不正', 'adr', r'^addresses: \[', 'addresses: [FR-999, ', 'E083'),
    ('ADR status語彙外', 'adr', r'^status: .*$', 'status: "done"', 'E080'),
    ('リンク切れ', 'prd', r'\]\(\.\./adr/ADR-0001', '](../adr/ADR-9999', 'E016'),
    ('表の列数不揃い', 'prd', r'^(\| GOAL-001 \|)', r'\1 余分 |', 'E011'),
    ('図を変えると描画証跡が古くなる', 'prd', r'(accTitle: [^\n]+)', r'\1（変更）', 'E103'),
    ('追跡表の手修正', 'trace', r'\| Must \|', '| Should |', 'E120'),
    ('.feature の手修正', 'feature', r'ならば ', 'ならば  ', 'E121'),
    ('NVTの割当が1つでない', 'st', r'^\| NVT-001 \|', '| NVT-010 |', 'E146'),
    ('テスト項目の由来が存在しない', 'ut', r'(\| UT-001 \|[^\n]*?)FR-\d{3}', r'\1FR-999', 'E142'),
    ('設計書のテスト名がコードにない', 'ut', r'`test_valid_draft_has_no_violations`', '`test_renamed_only_in_doc`', 'E152'),
    ('テストコードを変えると実行証跡が古くなる', 'code', r'\Z', '\n# changed\n', 'E153'),
    ('目的に受入シナリオがない', 'uat', r'(\| UAT-\d{3} \|[^\n]*?)GOAL-001', r'\1GOAL-002', 'E150', 0),
    ('機能がどの水準にも割り当てられていない', 'ct', r'^\| FEAT-008 \|', '| 機能8 |', 'E148'),
    ('front matter の語彙外', 'st', r'^last_run: not_run', 'last_run: done', 'E025'),
    ('合格と書いて実行証跡がない', 'st', r'^last_run: not_run', 'last_run: passed', 'E155'),
    ('ペルソナの主体が存在しない', 'uat', r'(\| PER-001 \| )ACT-001', r'\1ACT-009', 'E145'),
    ('1章の由来が本文に出てこない', 'ct', r'^(\| 由来 \|[^\n]*)ADR-0002', r'\1ADR-0002・FR-025', 'E157'),
    ('文書の実行結果が証跡と食い違う', 'ct', r'29件', '30件', 'E158'),
    ('旅程が通るシナリオが存在しない', 'st', r'(\| E2E-001 \|[^\n]*?)SCN-001', r'\1SCN-999', 'E143'),
]


def selftest(root: Path) -> list[dict]:
    base = Lint(root); res = []
    fdir = root / base.cfg['docs']['features_dir']
    keys = {'prd': base.globs('prd')[0], 'bdd': base.globs('bdd')[0], 'adr': base.globs('adr')[0],
            'trace': root / base.cfg['docs']['trace'], 'feature': sorted(fdir.glob('*.feature'))[0]}
    keys |= {k: base.globs(k)[0] for k in TEST_KINDS if base.globs(k)}
    if base.cfg.get('tests'): keys['code'] = sorted(p for g in base.cfg['tests']['code'] for p in root.glob(g))[-1]
    for name, key, pat, rep, code, *rest in MUTATIONS:
        if key not in keys: res.append({'mutation': name, 'expect': code, 'status': 'skipped（対象の文書が無い）'}); continue
        with tempfile.TemporaryDirectory() as tmp:
            t = Path(tmp) / 'k'; shutil.copytree(root, t, ignore=shutil.ignore_patterns('node_modules', '_render', '__pycache__', 'mutants', '.hypothesis', '.pytest_cache'))
            f = t / keys[key].relative_to(root); s = f.read_text(encoding='utf-8')
            new, n = re.subn(pat, rep, s, count=rest[0] if rest else 1, flags=re.M | re.S)
            if n < 1: res.append({'mutation': name, 'expect': code, 'status': 'FIXTURE_MISSING'}); continue
            f.write_text(new, encoding='utf-8')
            errs = Lint(t).run()['errors']
            res.append({'mutation': name, 'expect': code, 'status': 'detected' if any(e.startswith(code) for e in errs) else 'MISSED'})
    return res


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('cmd', choices=['check', 'trace', 'extract', 'selftest'])
    ap.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    ap.add_argument('--json', type=Path, help='結果 JSON の出力先')
    a = ap.parse_args()
    if a.cmd == 'selftest':
        base = Lint(a.root).run()
        res = selftest(a.root)
        rep = {'status': 'passed' if base['status'] == 'passed' and all(r['status'] in ('detected', 'skipped（対象の文書が無い）') for r in res) else 'failed',
               'baseline': base['status'], 'mutations': res, 'executed_at_utc': base['executed_at_utc']}
        show = rep
    else:
        rep = Lint(a.root).run(write_trace=a.cmd == 'trace', write_features=a.cmd == 'extract')
        show = {**rep, 'stats': {k: v for k, v in rep['stats'].items() if k != 'docs_sha256'}}
    if a.json:
        a.json.parent.mkdir(parents=True, exist_ok=True)
        a.json.write_text(json.dumps(rep, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(show, ensure_ascii=False, indent=2))
    return 0 if rep['status'] == 'passed' else 1


if __name__ == '__main__':
    raise SystemExit(main())
