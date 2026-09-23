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
  python tools/kit_lint.py extract      gherkin_source: markdown の BDD 文書について、Markdown 内 Gherkin から
                                        .feature を生成する（生成物には marker 行を付ける）。
                                        gherkin_source: feature の文書には手を出さない（E123、mirror を案内）
  python tools/kit_lint.py mirror       gherkin_source: feature の BDD 文書について、features/*.feature から
                                        Markdown のフェンスを書き戻す（marker 行は除く）
  python tools/kit_lint.py selftest     リンター自身の変異試験
文書検査であり、製品の試験ではない。
"""
from __future__ import annotations
import sys
if sys.version_info < (3, 11):
    sys.stderr.write(
        'kit_lint.py: Python 3.11 以上が必要（tomllib が標準ライブラリに加わったのは '
        f'3.11: https://docs.python.org/3/library/tomllib.html）。現在: {sys.version.split()[0]}\n'
    )
    raise SystemExit(2)
import argparse, hashlib, json, os, re, shutil, tempfile, tomllib
import importlib.metadata as im
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
import yaml
from gherkin.parser import Parser
from gherkin.pickles.compiler import Compiler
from gherkin.stream.id_generator import IdGenerator

FENCE = re.compile(r'^ {0,3}(`{3,}|~{3,})\s*([\w+-]*)\s*$')
MARKER_PREFIX = '# generated-by: kit_lint extract'


def _with_marker(code: str, source_rel: str) -> str:
    head, nl, rest = code.partition('\n')
    return head + nl + f'{MARKER_PREFIX} — do not edit; source: {source_rel}\n' + rest


def _has_marker(text: str) -> bool:
    _, _, rest = text.partition('\n')
    second, _, _ = rest.partition('\n')
    return second.startswith(MARKER_PREFIX)


def _strip_marker(text: str) -> str:
    head, nl, rest = text.partition('\n')
    second, nl2, tail = rest.partition('\n')
    return head + nl + tail if second.startswith(MARKER_PREFIX) else text


def _fence_ranges(text: str) -> list[tuple[int, int]]:
    """d.fences と同じ順序で、各フェンスの (開始行, 終了行) を0始まりの行番号で返す。"""
    lines = text.splitlines()
    ranges: list[tuple[int, int]] = []
    opener, start = None, 0
    for i, line in enumerate(lines):
        m = FENCE.match(line)
        if opener is None:
            if m: opener, start = (m[1], m[2]), i
        else:
            if m and m[1][0] == opener[0][0] and len(m[1]) >= len(opener[0]) and not m[2]:
                ranges.append((start, i)); opener = None
    return ranges
EARS = {
    '常時': r'^システムは、.+$',
    'イベント': r'^.+とき、システムは.+$',
    '状態': r'^.+間、システムは.+$',
    '異常': r'^もし.+ならば、システムは.+$',
    'オプション': r'^.+場合、(.+とき、)?システムは.+$',
    '複合': r'^.+間、.+とき、システムは.+$',
}
EARS_END = re.compile(r'(なければならない|てはならない)。$')
ID_KINDS = ('FR', 'NFR', 'GOAL', 'KPI', 'GRD', 'EVID', 'ACT', 'RISK', 'NVT', 'ADR', 'FEAT', 'RULE', 'SCN', 'Q', 'UT', 'CT', 'E2E', 'UAT', 'PT', 'PER')
ITEM_KINDS = ('UT', 'CT', 'E2E', 'UAT', 'PT', 'PER')
TEST_KINDS = ('ut', 'ct', 'st', 'uat')


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
        prefix = re.escape(str(self.cfg.get('ids', {}).get('prefix', '')))
        self.ID = prefix + r'(?:' + '|'.join(ID_KINDS) + r')-\d{3,4}'
        self.ITEM = re.compile(prefix + r'(?:' + '|'.join(ITEM_KINDS) + r')-\d{3}')
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
                try:
                    trel = str(target.relative_to(self.root.resolve())).replace('\\', '/')
                except ValueError:
                    self.err('E018', d.rel, f'ルート外へのリンク: {href}'); continue
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
                if not re.fullmatch(self.ID, cell): continue
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
            src = set(re.findall(self.ID, row.get('根拠', '')))
            if not src: self.err('E036', d.rel, f'{fid}: 根拠IDがない')
            for s in src - m['ids']: self.err('E037', d.rel, f'{fid}: 根拠 {s} が文書内に存在しない')
            used |= src
            acc = set(re.findall(self.ID, row.get('受入', '')))
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

    def check_cross(self, prds: list[Doc], pm: dict, bdds):
        where = ', '.join(sorted(p.rel for p in prds))
        rules, scn_by_req = {}, {}
        for d, b in bdds:
            rules |= b['rules']
            for s in b['scenarios']:
                for r in s['req']:
                    if r not in pm['fr'] and r not in pm['nfr']: self.err('E070', d.rel, f'{s["id"]}: 未知の要件タグ {r}')
                    scn_by_req.setdefault(r, []).append(s['id'])
        for fid, row in pm['fr'].items():
            want = {a for a in re.findall(self.ID, row.get('受入', '')) if a.startswith('RULE')}
            have = {rid for rid, r in rules.items() if fid in r['req']}
            for r in sorted(want - set(rules)): self.err('E071', where, f'{fid}: 受入 {r} が BDD に存在しない')
            if want != have:
                self.err('E072', where, f'{fid}: PRD の受入 {sorted(want)} と BDD タグから逆算した {sorted(have)} が不一致')
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
        if d.meta.get('last_run') in ('passed', 'failed'):
            ev = str(d.meta.get('evidence', ''))
            if not ev or ev == 'なし' or not (d.path.parent / ev).is_file():
                self.err('E155', d.rel, f'last_run: {d.meta["last_run"]} なのに実行証跡（evidence）がない: {ev!r}')

    def parse_tests(self, docs: dict[str, list[Doc]]) -> dict:
        t = {'items': {}, 'nvt': {}, 'feat': {}, 'by_kind': {k: 0 for k in TEST_KINDS}}
        for kind, ds in docs.items():
            for d in ds:
                for hd, rows in self.tables(d.prose):
                    for r in rows:
                        cell, row = r[0].strip(), dict(zip(hd, r))
                        if self.ITEM.fullmatch(cell):
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
                src = set(re.findall(self.ID, row['由来'])); used |= src
                if not src: self.err('E141', d.rel, f'{tid}: 由来のIDがない')
                for x in sorted(src - known): self.err('E142', d.rel, f'{tid}: 由来 {x} が存在しない')
            for x in sorted(set(re.findall(r'SCN-\d{3}', row.get('通るシナリオ', ''))) - scns): self.err('E143', d.rel, f'{tid}: シナリオ {x} が BDD にない')
            for x in re.findall(r'PER-\d{3}', row.get('ペルソナ', '')):
                if x not in known: self.err('E144', d.rel, f'{tid}: ペルソナ {x} が存在しない')
            for x in re.findall(r'ACT-\d{3}', row.get('主体', '')):
                if x not in known: self.err('E145', d.rel, f'{tid}: 主体 {x} が存在しない')
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
        if docs['uat']:
            goals = {g for tid, it in t['items'].items() if it['doc'] in docs['uat'] and tid.startswith('UAT') for g in re.findall(r'GOAL-\d{3}', it['row'].get('由来', ''))}
            where = ', '.join(sorted(d.rel for d in docs['uat']))
            for g in sorted(pm['goals'] - goals): self.err('E150', where, f'{g}: 受入シナリオがない（UAT 全文書の合算）')
            prose_all = '\n'.join(d.prose for d in docs['uat'])
            for a in sorted(i for i in pm['ids'] if i.startswith('ACT-')):
                if a not in prose_all: self.err('E151', where, f'{a}: ペルソナも対象外の理由もない（UAT 全文書の合算）')
        for d in (x for ds in docs.values() for x in ds):                      # 1章の「由来」に挙げたIDが、本文のどこにも出てこないのは設計の漏れ
            m = re.search(r'^\| 由来 \|([^\n]*)$', d.prose, re.M)
            if not m: continue
            line, rest = m.group(1), d.prose.replace(m.group(0), '')
            ids = set(re.findall(self.ID, line))
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

        def evidence_value(key):                                            # 'ut.total' / 'mutation.killed' 等のキーを証跡 JSON の値に解決する
            section, _, field = key.partition('.')
            if section == 'mutation':
                src, field = (data.get('mutation') or {}), {'total': 'mutants'}.get(field, field)
            else:
                src, field = data.get('levels', {}).get(section.upper(), {}), {'total': 'tests'}.get(field, field)
            return src.get(field)

        for d in (x for ds in docs.values() for x in ds):                      # 「実行結果」表の値が、証跡と数値で食い違っていないか
            lv = data.get('levels', {}).get(str(d.meta.get('doc_type')).upper())
            if not lv or (d.path.parent / str(d.meta.get('evidence'))).resolve() != ev.resolve(): continue
            for hd, rows in self.tables(d.prose):
                if hd != ['項目', '値', '証跡のキー']: continue
                for row in rows:
                    item, val, key = (row + ['', '', ''])[:3]
                    key = key.strip()
                    if not key: continue
                    have = evidence_value(key)
                    if have is None:
                        # doc_type の水準（lv）自体は証跡にあるので、キーが解決できないのは
                        # 証跡のキーの誤記・誤った節を指している（ST/UAT の not_run はここに来ない。
                        # lv が無い時点で上の continue で除外されている）。
                        self.err('E159', d.rel, f'{item}: 証跡のキー {key!r} を証跡から解決できない')
                        continue
                    m = re.match(r'-?\d+(?:\.\d+)?', val.strip())
                    ok = float(m.group()) == float(have) if m else val.strip() == str(have)
                    if not ok:
                        self.err('E158', d.rel, f'{item}: 文書の値「{val}」が証跡の値 {have}（キー: {key}）と一致しない')

    # ---------- 追跡表 ----------
    def build_trace(self, prds_pms: list[tuple[Doc, dict]], rules, scn_by_req, adrs, t=None) -> str:
        by = {}
        for a in adrs:
            for r in a.meta.get('addresses') or []: by.setdefault(r, []).append(a.meta['id'])
        j = lambda xs: ', '.join(sorted(set(xs))) or '—'
        t = t or {'items': {}, 'nvt': {}}
        ver = getattr(self, 'verified', {})
        def cond(ids): return j(tid for tid, it in t['items'].items() if not tid.startswith('PER') and set(ids) & set(re.findall(self.ID, it['row'].get('由来', ''))))
        def ran(ids): return j(l for i in ids for l in ver.get(i, {}).get('levels', []) if not ver[i]['failed'])
        L = ['<!-- 自動生成：python tools/kit_lint.py trace。手で編集しない（check が差分を不合格にする）。 -->',
             '# 追跡表：要件→ルール→シナリオ→設計判断→専用検証', '',
             'ルール・シナリオ・テスト条件は要件を**具体化**（specifies）するだけで、合格を意味しない。「合格した実行」の列だけが実行証跡に基づく。ただし、その要件を確かめるテストが1件以上合格したことを示すだけで、要件の全体が検証済みであることは意味しない。']
        multi = len(prds_pms) > 1
        for prd, pm in prds_pms:
            href = os.path.relpath(prd.path, (self.root / self.cfg['docs']['trace']).parent).replace('\\', '/')   # 追跡表の置き場所からの相対パス
            fr_title = '## 機能要件' + (f'（{prd.rel}）' if multi else '')
            nfr_title = '## 非機能要件' + (f'（{prd.rel}）' if multi else '')
            L += ['', fr_title, '', '| 要件 | 優先度 | ルール | シナリオ | 設計判断 | 専用検証 | テスト条件 | 合格した実行 |', '|---|---|---|---|---|---|---|---|']
            for fid, row in pm['fr'].items():
                L.append(f'| [{fid}]({href}#{fid}) | {row.get("優先度", "")} | {j(r for r, v in rules.items() if fid in v["req"])} | {j(scn_by_req.get(fid, []))} | {j(by.get(fid, []))} | {j(a for a in re.findall(self.ID, row.get("受入", "")) if a.startswith("NVT"))} | {cond([fid] + [r for r, v in rules.items() if fid in v["req"]])} | {ran([fid])} |')
            L += ['', nfr_title, '', '| 要件 | 品質特性 | 専用検証 | 割当先の文書 | テスト条件 | 設計判断 |', '|---|---|---|---|---|---|']
            for nid, row in pm['nfr'].items():
                nv = re.findall(r"NVT-[0-9]{3}", row.get("検証", ""))
                L.append(f'| [{nid}]({href}#{nid}) | {row.get("品質特性", "")} | {j(nv)} | {j(w for n in nv for w in t["nvt"].get(n, []))} | {cond([nid] + nv)} | {j(by.get(nid, []))} |')
        L += ['', '## ルール', '', '| ルール | 業務ルール | シナリオ | 要件 |', '|---|---|---|---|']
        for rid in sorted(rules):
            L.append(f'| {rid} | {rules[rid]["name"]} | {", ".join(rules[rid]["scn"])} | {j(rules[rid]["req"])} |')
        if t['items']:
            L += ['', '## テスト項目', '', '| ID | 水準 | 由来 |', '|---|---|---|']
            for tid, it in t['items'].items():
                if not tid.startswith('PER'): L.append(f'| {tid} | {it["kind"].upper()} | {j(re.findall(self.ID, it["row"].get("由来", "")))} |')
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
        if not prds:
            self.err('E110', 'kit.toml', '要件正本（PRD）を1件以上指定する'); return self.report()
        pms = [self.parse_prd(p) for p in prds]
        merged_ids: set[str] = set()
        for p, pm_ in zip(prds, pms):
            for cell in pm_['ids']:
                if cell in merged_ids: self.err('E030', p.rel, f'ID がほかの PRD と重複: {cell}')
                merged_ids.add(cell)
        pm = {'goals': set(), 'kpis': {}, 'ids': set(), 'fr': {}, 'nfr': {}, 'nvt': {}}
        for pm_ in pms:
            pm['goals'] |= pm_['goals']; pm['kpis'].update(pm_['kpis']); pm['ids'] |= pm_['ids']
            pm['fr'].update(pm_['fr']); pm['nfr'].update(pm_['nfr']); pm['nvt'].update(pm_['nvt'])
        for p, pm_ in zip(prds, pms): self.check_prd(p, pm_)
        parsed = [(d, self.parse_bdd(d)) for d in bdds]
        self.parse_bdd(tpl['bdd'])                       # テンプレートの Gherkin も公式 parser を通す
        tagmode: dict[str, tuple[str | None, str]] = {}
        for d, b in parsed:
            gs = d.meta.get('gherkin_source')
            if gs not in ('markdown', 'feature'):
                self.err('E124', d.rel, f'gherkin_source は markdown か feature のいずれかが必要: {gs!r}')
                gs = None
            for f in b['features']:
                if f['tag']: tagmode[f['tag']] = (gs, d.rel)
        rules, scn_by_req = self.check_cross(prds, pm, parsed)
        amap = {a.meta.get('id'): a for a in adrs}
        for a in adrs: self.check_adr(a, pm, amap)
        tests = self.parse_tests(tdocs)
        scns = {s['id'] for _, b in parsed for s in b['scenarios']}
        feats_ids = {f['tag'] for _, b in parsed for f in b['features'] if f['tag']}
        if tflat: self.check_tests(tdocs, tests, pm, rules, scns, feats_ids, adrs)
        trace = self.build_trace(list(zip(prds, pms)), rules, scn_by_req, adrs, tests)
        tpath = self.root / self.cfg['docs']['trace']
        if write_trace: tpath.write_text(trace, encoding='utf-8')
        if not tpath.is_file() or tpath.read_text(encoding='utf-8') != trace:
            self.err('E120', self.cfg['docs']['trace'], '追跡表が正本と不一致（trace を再生成）')
        feats = {f'{f["tag"]}.feature': f['code'] for _, b in parsed for f in b['features'] if f['tag']}
        fdir = self.root / self.cfg['docs']['features_dir']
        features_rel = self.cfg['docs']['features_dir']
        if write_features:
            fdir.mkdir(exist_ok=True)
            for name, code in feats.items():
                tag = name[:-len('.feature')]
                mode, src = tagmode.get(tag, (None, ''))
                if mode == 'markdown':
                    (fdir / name).write_text(_with_marker(code, src), encoding='utf-8')
                elif mode == 'feature':
                    self.err('E123', f'{features_rel}/{name}', 'gherkin_source: feature のため extract できない（mirror を実行）')
                # mode is None（front matter 不正）: E124 で既に報告済みなので書かない
            for p in list(fdir.glob('*.feature')):
                if p.name in feats: continue  # 既知のフェンスに対応する（markdown/feature どちらのモードでも extract の対象外）
                if _has_marker(p.read_text(encoding='utf-8')):
                    p.unlink()  # どのフェンスにも対応しない、かつて extract が生成したファイル＝安全に削除できる
        have = {p.name: _strip_marker(p.read_text(encoding='utf-8')) for p in fdir.glob('*.feature')} if fdir.is_dir() else {}
        for name, code in feats.items():
            tag = name[:-len('.feature')]
            mode, _src = tagmode.get(tag, (None, ''))
            if mode is None: continue  # E124 で既に報告済み
            if have.get(name) != code:
                msg = ('Markdown のフェンスが .feature と不一致（mirror を再実行。編集は片方向のみ）' if mode == 'feature'
                       else '.feature が Markdown の Gherkin と不一致（extract を再実行。編集は片方向のみ）')
                self.err('E121', f'{features_rel}/{name}', msg)
        if fdir.is_dir():
            for p in fdir.glob('*.feature'):
                if p.name in feats: continue
                if not _has_marker(p.read_text(encoding='utf-8')):
                    self.err('E122', f'{features_rel}/{p.name}', 'マーカーがない .feature（extract は削除しない。手動で確認する）')
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


def do_mirror(root: Path) -> dict:
    """gherkin_source: feature の BDD 文書について、Markdown のフェンスを
    features/*.feature の内容（マーカー行を除く）で書き戻す。それ以外は触らない。"""
    lint = Lint(root)
    bdds = [lint.load(p) for p in lint.globs('bdd')]
    fdir = root / lint.cfg['docs']['features_dir']
    changed = []
    for d in bdds:
        if d.meta.get('gherkin_source') != 'feature': continue
        b = lint.parse_bdd(d)
        ranges = _fence_ranges(d.text)
        if len(ranges) != len(d.fences): continue  # フェンス走査の不整合。安全のため何もしない
        lines = d.text.splitlines()
        edits = []
        gi = 0
        for (start, end), (lang, _line, _code) in zip(ranges, d.fences):
            if lang != 'gherkin': continue
            tag = b['features'][gi]['tag']; gi += 1
            if not tag: continue
            fpath = fdir / f'{tag}.feature'
            if not fpath.is_file():
                lint.err('E121', f"{lint.cfg['docs']['features_dir']}/{tag}.feature", 'mirror の対象の .feature が存在しない')
                continue
            new_code = _strip_marker(fpath.read_text(encoding='utf-8'))
            if not new_code.endswith('\n'): new_code += '\n'
            edits.append((start, end, new_code.splitlines()))
        for start, end, body_lines in sorted(edits, key=lambda e: -e[0]):
            lines[start + 1:end] = body_lines
        new_text = '\n'.join(lines) + '\n'
        if new_text != d.text:
            d.path.write_text(new_text, encoding='utf-8')
            changed.append(d.rel)
    return {'status': 'passed' if not lint.errors else 'failed', 'changed': changed, 'errors': lint.errors,
            'executed_at_utc': datetime.now(timezone.utc).isoformat(timespec='seconds')}


DELETE = '<DELETE-THIS-FILE>'  # 特殊センチネル：正規表現置換の代わりに対象ファイルを削除する変異用

MUTATIONS = [  # (名前, 対象, 置換前の正規表現, 置換後, 検出すべきコード)
    ('FRを2文にする', 'prd', r'(<a id="FR-001"></a>FR-001 \| [^|]+ \| [^|]+?)。', r'\1。さらに別の義務も負わなければならない。', 'E034'),
    ('FRの型と構文の不一致', 'prd', r'(<a id="FR-001"></a>FR-001 \| )[^|]+ \|', r'\1イベント |', 'E033'),
    ('存在しない根拠ID', 'prd', r'(<a id="FR-001"></a>FR-001 \|[^\n]*?)GOAL-\d{3}', r'\1GOAL-999', 'E037'),
    ('NFRの検証計画欠落', 'prd', r'(<a id="NFR-001"></a>NFR-001 \|[^\n]*?)NVT-\d{3}', r'\1なし', 'E043'),
    ('必須節の改名', 'prd', r'^## 5\. .*$', '## 5. 勝手な節', 'E020'),
    ('Gherkin構文破壊', 'bdd', r'ならば (申請者Aに受付番号と内容版 1 と提出日時が表示される)', r'ナラバ \1', 'E050'),
    ('SCN重複', 'bdd', r'@SCN-002', '@SCN-001', 'E064'),
    ('未知の要件タグ', 'bdd', r'(@SCN-001 )@FR-\d{3}', r'\1@FR-999', 'E070'),
    ('PRD受入とBDDタグの不一致', 'bdd', r'(@SCN-001 @FR-\d{3})', r'\1 @FR-020', 'E072'),
    ('試験用語の混入', 'bdd', r'(@SCN-001[^\n]*\n[^\n]*\n\s+前提 )', r'\1テストダブルの', 'E060'),
    ('BDDがpassedなのにevidenceがない', 'bdd', r'^evidence: "\.\./evidence/example_tests\.json"$', 'evidence: "なし"', 'E155'),
    ('ADR採用案が一覧にない', 'adr', r'採用：\*\*案[A-Z]\*\*', '採用：**案Z**', 'E090'),
    ('ADR addresses不正', 'adr', r'^addresses: \[', 'addresses: [FR-999, ', 'E083'),
    ('ADR status語彙外', 'adr', r'^status: .*$', 'status: "done"', 'E080'),
    ('リンク切れ', 'prd', r'\]\(\.\./adr/ADR-0001', '](../adr/ADR-9999', 'E016'),
    ('表の列数不揃い', 'prd', r'^(\| GOAL-001 \|)', r'\1 余分 |', 'E011'),
    ('図を変えると描画証跡が古くなる', 'prd', r'(accTitle: [^\n]+)', r'\1（変更）', 'E103'),
    ('追跡表の手修正', 'trace', r'(\[FR-001\]\([^|]*\) \| )Must', r'\1Should', 'E120'),
    ('.feature の手修正', 'feature', r'(@SCN-001[\s\S]*?)ならば ', r'\1ならば  ', 'E121'),
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
    ('文書の実行結果が証跡と食い違う', 'ut', r'\| UT件数 \| 125 \|', '| UT件数 | 126 |', 'E158'),
    ('証跡のキーが誤記で解決できない', 'ut', r'\| UT合格 \| 125 \| ut\.passed \|', '| UT合格 | 125 | ut.pased |', 'E159'),
    ('PRD内でIDが重複する', 'prd', r'<a id="FR-002"></a>FR-002', '<a id="FR-001"></a>FR-001', 'E030'),
    ('BDDのルールがどの要件にも結び付かない', 'bdd', r' @FR-00[34]', '', 'E073', 0),
    ('gherkin_sourceが不正な値', 'bdd', r'gherkin_source: markdown', 'gherkin_source: invalid_value', 'E124'),
    ('UATのペルソナが存在しない', 'uat', r'(\| UAT-001 \| )PER-001( \|)', r'\1PER-999\2', 'E144'),
    ('全FRがMustになる', 'prd', r'\| (?:Should|Could) \|', '| Must |', 'W045', 0),
    ('末尾に改行がない', 'adr', r'\n\Z', '', 'E001'),
    ('front matterが壊れている', 'adr', r'\A---\n', '---\nbroken: [\n', 'E002'),
    ('コードフェンスが閉じていない', 'adr', r'\Z', '\n```text\nunclosed\n', 'E003'),
    ('アンカー重複', 'prd', r'(<a id="FR-001"></a>)', r'\1\1', 'E010'),
    ('H1が複数になる', 'prd', r'(^# [^\n]*)$', r'\1\n\n# 重複するH1', 'E012'),
    ('見出し階層を飛ばす', 'prd', r'(^# [^\n]*\n)([\s\S]*?)(^## )', r'\1\2### ', 'E013'),
    ('未置換のプレースホルダが残る', 'prd', r'\Z', '\n{{未置換}}\n', 'E014'),
    ('許可しないリンク種別', 'prd', r'\Z', '\n[bad](ftp://example.com/x)\n', 'E015'),
    ('アンカーが存在しない', 'prd', r'\Z', '\n[bad](#no-such-anchor-xyz)\n', 'E017'),
    ('テンプレートにない節', 'prd', r'\Z', '\n## 手を加えた節\n\n本文。\n', 'E021'),
    ('節の順序が異なる', 'prd', r'(^## )1\. 要約(\n[\s\S]*?)(^## )2\. 背景・課題・根拠$', r'\g<1>2. 背景・課題・根拠\2\g<3>1. 要約', 'E022'),
    ('テンプレートの表が無い', 'prd', r'^\| 目的ID \| 対象者 \| 期待する変化 \| 根拠 \|$', '| 目的ID | 対象者 | 期待する変化2 | 根拠 |', 'E023'),
    ('front matterのキーがテンプレートと異なる', 'prd', r'\A---\n', '---\nbogus_extra_key: "x"\n', 'E024'),
    ('FRの明示アンカーが無い', 'prd', r'<a id="FR-001"></a>FR-001', 'FR-001', 'E031'),
    ('FRの型がEARSの6種でない', 'prd', r'(<a id="FR-001"></a>FR-001 \| )常時( \|)', r'\1不正な型\2', 'E032'),
    ('FRの優先度が語彙外', 'prd', r'(<a id="FR-001"></a>FR-001 \|[^\n]*\| )Must( \|)', r'\1不正\2', 'E035'),
    ('FRの根拠が無い', 'prd', r'(<a id="FR-001"></a>FR-001 \|[^\n]*\| Must \| )GOAL-002( \|)', r'\1\2', 'E036'),
    ('FRの受入が無い', 'prd', r'(<a id="FR-001"></a>FR-001 \|[^\n]*\| Must \| GOAL-002 \| )RULE-003、RULE-012、NVT-002( \|)', r'\1\2', 'E038'),
    ('FRの受入NVTが検証計画に無い', 'prd', r'(<a id="FR-001"></a>FR-001 \|[^\n]*\| Must \| GOAL-002 \| RULE-003、RULE-012、)NVT-002', r'\1NVT-999', 'E039'),
    ('GOALがどのFRからも参照されない', 'prd', r'(^\| GOAL-002 \|[^\n]*\n)', r'\1| GOAL-099 | ダミー | ダミー | EVID-001 |\n', 'E040'),
    ('KPIの計測手段が無い', 'prd', r'(\| KPI-001 \|[\s\S]*?)FR-026( \|)', r'\1\2', 'E041'),
    ('KPIの計測手段が存在しないFRを指す', 'prd', r'(\| KPI-002 \|[\s\S]*?)FR-003・FR-026', r'\1FR-999', 'E042'),
    ('NFRの合格基準に数値が無い', 'prd', r'(<a id="NFR-001"></a>NFR-001 \| 性能効率性 \| [^|]+\| )[^|]+(\| NVT-001 \|)', r'\1数値なし \2', 'E044'),
    ('PRDの受入にBDDに無いRULEを書く', 'prd', r'(<a id="FR-001"></a>FR-001 \|[^\n]*\| Must \| GOAL-002 \| )RULE-003', r'\1RULE-999、RULE-003', 'E071'),
    ('Gherkinの言語がkit.toml設定と異なる', 'kit', r'language = "ja"', 'language = "fr"', 'E051'),
    ('languageの明示が無い', 'bdd', r'# language: ja\n@FEAT-001', '# language:ja\n@FEAT-001', 'E052'),
    ('FEATタグが複数になる', 'bdd', r'@FEAT-001\n機能:', '@FEAT-001\n@FEAT-001\n機能:', 'E053'),
    ('Ruleに属さないシナリオ', 'bdd', r'(前提 組織Aに申請者Aと審査者Aがいる\n)(\n  @RULE-001)', r'\1\n  シナリオ: 迷子のシナリオ\n    前提 何かがある\n\2', 'E054'),
    ('RULEタグが複数になる', 'bdd', r'@RULE-001\n  ルール:', '@RULE-001\n  @RULE-999\n  ルール:', 'E055'),
    ('RULE_IDが重複する', 'bdd', r'^  @RULE-002$', '  @RULE-001', 'E056'),
    ('Ruleにシナリオが無い', 'bdd', r'(\n  @RULE-001\n  ルール:)', r'\n  @RULE-900\n  ルール: 空のルール\1', 'E057'),
    ('SCNタグが複数になる', 'bdd', r'@SCN-001 @FR-003\n    シナリオ:', '@SCN-001 @SCN-777 @FR-003\n    シナリオ:', 'E058'),
    ('シナリオに要件タグが無い', 'bdd', r'@SCN-001 @FR-003\n', '@SCN-001\n', 'E059'),
    ('もしステップが無い', 'bdd', r'(@SCN-001[\s\S]*?)      もし [^\n]+\n', r'\1', 'E061'),
    ('ならばの後にもしが再登場', 'bdd', r'(@SCN-001[\s\S]*?      ならば [^\n]+\n)', r'\1      もし 追加のもし\n', 'E062'),
    ('ADRのidがADR-nnnn形式でない', 'adr', r'id: "ADR-0001"', 'id: "ADR-1"', 'E081'),
    ('ADRのファイル名がidで始まらない', 'adr', r'id: "ADR-0001"', 'id: "ADR-9999"', 'E082'),
    ('ADRのaddressesが空', 'adr', r'addresses: \["FR-008", "FR-010", "FR-024"\]', 'addresses: []', 'E084'),
    ('ADRのsupersedesが存在しない', 'adr', r'supersedes: \[\]', 'supersedes: ["ADR-9999"]', 'E085'),
    ('supersedesが双方向でない', 'adr', r'supersedes: \[\]\nsuperseded-by: null', 'supersedes: ["ADR-0002"]\nsuperseded-by: null', 'E086'),
    ('supersededなのにsuperseded-byが無い', 'adr', r'^status: accepted$', 'status: superseded', 'E087'),
    ('confidenceが語彙外', 'adr', r'confidence: "中"', 'confidence: "unknown"', 'E088'),
    ('選択肢が2つ未満', 'adr', r'(- \*\*案A\*\*[^\n]*\n)- \*\*案B\*\*[^\n]*\n- \*\*案C\*\*[^\n]*\n- \*\*案D\*\*[^\n]*\n', r'\1', 'E089'),
    ('決定に理由が無い', 'adr', r'採用：\*\*案[A-Z]\*\*[\s\S]*?(?=\n### )', '採用：**案C**。', 'E091'),
    ('選択肢の長所短所が丸ごと無い', 'adr', r'### 案D[\s\S]*?(?=## 6\.)', '', 'E092'),
    ('短所の記載が無い', 'adr', r'(### 案A[\s\S]*?)- 短所：[^\n]*\n', r'\1', 'E093'),
    ('確認方法が無い', 'adr', r'### 4\.2 確認方法（Confirmation）', '### 4.2 検証手順', 'E094'),
    ('Mermaidにclickが混入', 'prd', r'(accTitle: [^\n]+)', r'\1\n    click X "test"', 'E100'),
    ('accTitleが無い', 'prd', r'accTitle: [^\n]+\n', '', 'E101'),
    ('PRDを1件も指定しない', 'kit', r'prd = \["prd/PRD_SAMPLE\.md"\]', 'prd = []', 'E110'),
    ('ステップの語彙再利用率の上限を割る', 'kit', r'max_unique_step_ratio = 0\.60', 'max_unique_step_ratio = 0.0', 'E074'),
    ('ステップ数上限を1にする', 'kit', r'max_steps = 7', 'max_steps = 1', 'W063'),
    ('テスト項目IDが重複する', 'ut', r'\| UT-002 \|', '| UT-001 |', 'E140'),
    ('テスト項目の由来が空', 'ut', r'(\| UT-001 \|[^\n]*\| 例示 \| )FR-003( \| )', r'\1\2', 'E141'),
    ('CTのNVTがPRDの検証計画に無い', 'ct', r'(\| NVT-010 \|[^\n]*\n)', r'\1| NVT-999 | ダミー | ダミー | ダミー | ダミー |\n', 'E147'),
    ('acceptedのADRを由来とするテスト項目が無い', 'ct', r'、ADR-0002', '', 'E149', 0),
    ('UATにACT対象外の理由が無い', 'prd', r'(\| ACT-005 \|[^\n]*\n)', r'\1| ACT-999 | ダミー | ダミー | ダミー |\n', 'E151'),
    ('実行証跡のstatusが不合格', 'evidence', r'"status": "passed"', '"status": "failed"', 'E156'),
    ('参考実装のMermaid描画証跡が無い', 'mermaid_evidence', DELETE, DELETE, 'W102'),
    ('実行証跡ファイルが無い', 'evidence', DELETE, DELETE, 'W154'),
    ('旅程が通るシナリオが存在しない', 'st', r'(\| E2E-001 \|[^\n]*?)SCN-001', r'\1SCN-999', 'E143'),
]


def selftest(root: Path) -> list[dict]:
    base = Lint(root); res = []
    fdir = root / base.cfg['docs']['features_dir']
    keys = {'prd': base.globs('prd')[0], 'bdd': base.globs('bdd')[0], 'adr': base.globs('adr')[0],
            'trace': root / base.cfg['docs']['trace'], 'feature': sorted(fdir.glob('*.feature'))[0],
            'kit': root / 'kit.toml'}
    keys |= {k: base.globs(k)[0] for k in TEST_KINDS if base.globs(k)}
    if base.cfg.get('tests'):
        keys['code'] = sorted(p for g in base.cfg['tests']['code'] for p in root.glob(g))[-1]
        keys['evidence'] = root / base.cfg['tests']['evidence']
    if (root / base.cfg['evidence']['mermaid']).is_file():
        keys['mermaid_evidence'] = root / base.cfg['evidence']['mermaid']
    for name, key, pat, rep, code, *rest in MUTATIONS:
        if key not in keys: res.append({'mutation': name, 'expect': code, 'status': 'skipped（対象の文書が無い）'}); continue
        with tempfile.TemporaryDirectory() as tmp:
            t = Path(tmp) / 'k'; shutil.copytree(root, t, ignore=shutil.ignore_patterns('node_modules', '_render', '__pycache__', 'mutants', '.hypothesis', '.pytest_cache'))
            if pat == DELETE:
                (t / keys[key].relative_to(root)).unlink()
                rep_ = Lint(t).run()
                errs = rep_['errors'] + rep_['warnings']
                res.append({'mutation': name, 'expect': code, 'status': 'detected' if any(e.startswith(code) for e in errs) else 'MISSED'})
                continue
            f = t / keys[key].relative_to(root); s = f.read_text(encoding='utf-8')
            if rest:
                # 明示的な count（0＝無制限）が指定された変異は、複数箇所への一括適用を意図している
                new, n = re.subn(pat, rep, s, count=rest[0], flags=re.M | re.S)
                if n < 1: res.append({'mutation': name, 'expect': code, 'status': 'FIXTURE_MISSING'}); continue
            else:
                # v2 の規則を復元：既定では正規表現はちょうど1箇所に一致しなければならない
                n_matches = len(re.findall(pat, s, flags=re.M | re.S))
                if n_matches < 1: res.append({'mutation': name, 'expect': code, 'status': 'FIXTURE_MISSING'}); continue
                if n_matches > 1: res.append({'mutation': name, 'expect': code, 'status': 'FIXTURE_AMBIGUOUS'}); continue
                new, n = re.subn(pat, rep, s, count=1, flags=re.M | re.S)
            f.write_text(new, encoding='utf-8')
            rep_ = Lint(t).run()
            errs = rep_['errors'] + rep_['warnings']
            res.append({'mutation': name, 'expect': code, 'status': 'detected' if any(e.startswith(code) for e in errs) else 'MISSED'})

    def _copy():
        tmp = tempfile.TemporaryDirectory()
        t = Path(tmp.name) / 'k'
        shutil.copytree(root, t, ignore=shutil.ignore_patterns('node_modules', '_render', '__pycache__', 'mutants', '.hypothesis', '.pytest_cache'))
        return tmp, t

    # gherkin_source: markdown/feature の3変異は、単純な正規表現置換の枠組みに収まらない
    # （extract/mirror の副作用と、ファイルの生存・不存在を確認する必要がある）ため個別に実装する。
    name = 'gherkin_source: feature で extract → E123'
    tmp, t = _copy()
    with tmp:
        bdd_path = Lint(t).globs('bdd')[0]
        text = bdd_path.read_text(encoding='utf-8')
        new_text, n = re.subn(r'^gherkin_source: markdown.*$', 'gherkin_source: feature', text, count=1, flags=re.M)
        if n < 1:
            res.append({'mutation': name, 'expect': 'E123', 'status': 'FIXTURE_MISSING'})
        else:
            bdd_path.write_text(new_text, encoding='utf-8')
            errs = Lint(t).run(write_features=True)['errors']
            res.append({'mutation': name, 'expect': 'E123', 'status': 'detected' if any(e.startswith('E123') for e in errs) else 'MISSED'})

    name = 'markdown モードでマーカーなし .feature が存在 → E122・削除されない'
    tmp, t = _copy()
    with tmp:
        fdir = t / Lint(t).cfg['docs']['features_dir']
        rogue = fdir / 'FEAT-900.feature'
        rogue.write_text('# language: ja\n@FEAT-900\n機能: 手動追加（対応するフェンスなし）\n', encoding='utf-8')
        errs = Lint(t).run(write_features=True)['errors']
        status = 'detected' if rogue.is_file() and any(e.startswith('E122') for e in errs) else 'MISSED'
        res.append({'mutation': name, 'expect': 'E122', 'status': status})

    name = 'feature モードで mirror 後にフェンスを手編集 → E121'
    tmp, t = _copy()
    with tmp:
        bdd_path = Lint(t).globs('bdd')[0]
        text = bdd_path.read_text(encoding='utf-8')
        new_text, n = re.subn(r'^gherkin_source: markdown.*$', 'gherkin_source: feature', text, count=1, flags=re.M)
        if n < 1:
            res.append({'mutation': name, 'expect': 'E121', 'status': 'FIXTURE_MISSING'})
        else:
            bdd_path.write_text(new_text, encoding='utf-8')
            do_mirror(t)
            text2 = bdd_path.read_text(encoding='utf-8')
            text3, n2 = re.subn(r'(@SCN-001[\s\S]*?)ならば ', r'\1ならば  ', text2, count=1)
            if n2 < 1:
                res.append({'mutation': name, 'expect': 'E121', 'status': 'FIXTURE_MISSING'})
            else:
                bdd_path.write_text(text3, encoding='utf-8')
                errs = Lint(t).run()['errors']
                res.append({'mutation': name, 'expect': 'E121', 'status': 'detected' if any(e.startswith('E121') for e in errs) else 'MISSED'})

    name = 'ルート外への相対リンク → E018'
    tmp, t = _copy()
    with tmp:
        # copytree は root（references/）の中身しか複製しないので、ルート外に実在するリンク先を
        # 用意するには複製先の兄弟ディレクトリに置く必要がある。
        (Path(tmp.name) / 'outside.md').write_text('# outside\n', encoding='utf-8')
        prd_path = Lint(t).globs('prd')[0]
        text = prd_path.read_text(encoding='utf-8')
        new_text, n = re.subn(r'\]\(\.\./adr/ADR-0001-ai-authority-boundary\.md\)', '](../../outside.md)', text, count=1)
        if n < 1:
            res.append({'mutation': name, 'expect': 'E018', 'status': 'FIXTURE_MISSING'})
        else:
            prd_path.write_text(new_text, encoding='utf-8')
            errs = Lint(t).run()['errors']
            res.append({'mutation': name, 'expect': 'E018', 'status': 'detected' if any(e.startswith('E018') for e in errs) else 'MISSED'})

    name = 'kit.tomlのprefix未設定でPAY-FR-001を書くと無視されず不合格になる'
    tmp, t = _copy()
    with tmp:
        prd_path = Lint(t).globs('prd')[0]
        text = prd_path.read_text(encoding='utf-8')
        new_text, n = re.subn(r'<a id="FR-001"></a>FR-001', '<a id="FR-001"></a>PAY-FR-001', text, count=1)
        if n < 1:
            res.append({'mutation': name, 'expect': 'E070', 'status': 'FIXTURE_MISSING'})
        else:
            prd_path.write_text(new_text, encoding='utf-8')
            errs = Lint(t).run()['errors']
            res.append({'mutation': name, 'expect': 'E070', 'status': 'detected' if any(e.startswith('E070') for e in errs) else 'MISSED'})

    name = '2つのPRDにまたがるFR-001の重複 → E030'
    tmp, t = _copy()
    with tmp:
        prd_path = Lint(t).globs('prd')[0]
        second = prd_path.parent / 'PRD_SAMPLE_2.md'
        second.write_text(prd_path.read_text(encoding='utf-8'), encoding='utf-8')
        kit_path = t / 'kit.toml'
        kit_text = kit_path.read_text(encoding='utf-8')
        new_kit, n = re.subn(
            r'prd = \["prd/PRD_SAMPLE\.md"\]',
            'prd = ["prd/PRD_SAMPLE.md", "prd/PRD_SAMPLE_2.md"]',
            kit_text,
            count=1,
        )
        if n < 1:
            res.append({'mutation': name, 'expect': 'E030', 'status': 'FIXTURE_MISSING'})
        else:
            kit_path.write_text(new_kit, encoding='utf-8')
            errs = Lint(t).run()['errors']
            res.append({'mutation': name, 'expect': 'E030', 'status': 'detected' if any(e.startswith('E030') for e in errs) else 'MISSED'})

    name = 'UATを2文書に分割してもcheckが通る'
    tmp, t = _copy()
    with tmp:
        uat_path = Lint(t).globs('uat')[0]
        original = uat_path.read_text(encoding='utf-8')
        keep_a, n_a = re.subn(r'^\| UAT-00[234567] \|[^\n]*\n', '', original, count=0, flags=re.M)
        keep_b, n_b = re.subn(r'^\| UAT-001 \|[^\n]*\n', '', original, count=1, flags=re.M)
        # 由来ペルソナ（PER-…）と探索セッション（PT-…）の表は両ファイルで重複させられないので、
        # 分割後のファイル側からは行を空にする（見出しと区切り行は残し、E023 の表判定は満たす）。
        keep_b = re.sub(r'^\| PER-\d{3} \|[^\n]*\n', '', keep_b, flags=re.M)
        keep_b = re.sub(r'^\| PT-\d{3} \|[^\n]*\n', '', keep_b, flags=re.M)
        keep_b = keep_b.replace('GOAL-001・GOAL-002、KPI-001、GRD-001・GRD-002、ACT-001〜ACT-004',
                                'GOAL-001・GOAL-002、KPI-001、GRD-001・GRD-002')
        if n_a < 1 or n_b < 1:
            res.append({'mutation': name, 'expect': 'E150', 'status': 'FIXTURE_MISSING'})
        else:
            uat_path.write_text(keep_a, encoding='utf-8')
            second = uat_path.parent / 'UAT_SAMPLE_2.md'
            second.write_text(keep_b, encoding='utf-8')
            kit_path = t / 'kit.toml'
            kit_text = kit_path.read_text(encoding='utf-8')
            new_kit, n = re.subn(
                r'uat = \["uat/UAT_SAMPLE\.md"\]',
                'uat = ["uat/UAT_SAMPLE.md", "uat/UAT_SAMPLE_2.md"]',
                kit_text,
                count=1,
            )
            if n < 1:
                res.append({'mutation': name, 'expect': 'E150', 'status': 'FIXTURE_MISSING'})
            else:
                kit_path.write_text(new_kit, encoding='utf-8')
                Lint(t).run(write_trace=True)  # 文書構成を分割したので trace を再生成してから check する（通常の運用手順どおり）
                rep_ = Lint(t).run()
                status = 'detected' if rep_['status'] == 'passed' else 'MISSED'
                res.append({'mutation': name, 'expect': 'passed', 'status': status})

    name = 'SHA-256のような文字列が本文にあってもIDとして誤検出されない'
    tmp, t = _copy()
    with tmp:
        prd_path = Lint(t).globs('prd')[0]
        text = prd_path.read_text(encoding='utf-8')
        new_text, n = re.subn(r'\Z', '\nSHA-256 のようなIDに見える文字列が本文にあっても検査に影響しない。\n', text, count=1)
        prd_path.write_text(new_text, encoding='utf-8')
        rep_ = Lint(t).run()
        status = 'detected' if rep_['status'] == 'passed' else 'MISSED'
        res.append({'mutation': name, 'expect': 'passed', 'status': status})

    return res


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('cmd', choices=['check', 'trace', 'extract', 'mirror', 'selftest'])
    ap.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    ap.add_argument('--json', type=Path, help='結果 JSON の出力先')
    a = ap.parse_args()
    if a.cmd == 'selftest':
        base = Lint(a.root).run()
        res = selftest(a.root)
        emitted = set(re.findall(r"self\.(?:err|warn)\('([EW]\d+)'", Path(__file__).read_text(encoding='utf-8')))
        covered = {m['expect'] for m in res}
        uncovered = sorted(emitted - covered)
        rep = {'status': 'passed' if base['status'] == 'passed' and not uncovered and all(r['status'] in ('detected', 'skipped（対象の文書が無い）') for r in res) else 'failed',
               'baseline': base['status'], 'uncovered_codes': uncovered, 'mutations': res, 'executed_at_utc': base['executed_at_utc']}
        show = rep
    elif a.cmd == 'mirror':
        rep = do_mirror(a.root)
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
