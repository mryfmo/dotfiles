#!/usr/bin/env python3
"""kit_lint.py の check_mermaid と render_mermaid.py が共有する、Mermaid フェンス抽出と
対象文書集合の決定ロジック。

どちらも stdlib のみに依存する（kit_lint.py の gherkin-official/PyYAML、
render_mermaid.py の playwright を、互いに引き込まないため）。フェンスの判定は
CommonMark のフェンスコードブロック定義に従う：開始行は行頭から3文字までのインデントを
許し、3個以上の連続する ` または ~ で始まる（4個以上のバッククォートも同様）。終了行は
同じ文字種・同じかそれ以上の長さで、情報文字列を持たない。この規則は kit_lint.py の
Doc.fences を構築する読み込みループと同一である。

対象文書集合（document_paths）は kit_lint.py の Lint.run() が all_docs を組み立てる手順
（テンプレート ∪ PRD ∪ ADR ∪ BDD ∪ UT/CT/ST/UAT ∪ other(重複除く) ∪ 追跡表）と同じ順序・
同じ重複排除規則を再現する。kit.toml の [docs] を変更したときは、この関数と
Lint.run() の両方を見直すこと（本ファイルが唯一の重複源）。
"""
from __future__ import annotations

import re
import tomllib
from pathlib import Path

FENCE = re.compile(r'^ {0,3}(`{3,}|~{3,})\s*([\w+-]*)\s*$')


def iter_fences(text: str):
    """(info string, 開始行(1始まり), フェンス内本文) を出現順に yield する。"""
    opener = None
    buf: list[str] = []
    start = 0
    for n, line in enumerate(text.splitlines(), 1):
        m = FENCE.match(line)
        if opener is None:
            if m:
                opener, start, buf = (m[1], m[2]), n, []
        elif m and m[1][0] == opener[0][0] and len(m[1]) >= len(opener[0]) and not m[2]:
            yield opener[1], start, '\n'.join(buf) + '\n'
            opener = None
        else:
            buf.append(line)


def mermaid_blocks(text: str):
    """本文中の mermaid フェンスだけを (開始行, フェンス内本文) で yield する。"""
    for lang, line, code in iter_fences(text):
        if lang == 'mermaid':
            yield line, code


def diagram_type(code: str) -> str | None:
    """フェンス本文の先頭の非空行・非ディレクティブ行（`%%` で始まる行）から、
    図の種類キーワード（flowchart／sequenceDiagram／stateDiagram-v2 等）を取り出す。
    該当する行が無ければ None。"""
    for line in code.splitlines():
        s = line.strip()
        if not s or s.startswith('%%'):
            continue
        m = re.match(r'[A-Za-z][\w-]*', s)
        return m.group(0) if m else None
    return None


def load_kit_config(root: Path) -> dict:
    return tomllib.loads((root / 'kit.toml').read_text(encoding='utf-8'))


def _globs(root: Path, cfg: dict, key: str) -> list[Path]:
    seen: set[Path] = set()
    res: list[Path] = []
    for pat in cfg['docs'].get(key, []):
        for p in sorted(root.glob(pat)):
            if p not in seen:
                seen.add(p)
                res.append(p)
    return res


def document_paths(root: Path, cfg: dict | None = None) -> list[Path]:
    """kit_lint.py の Lint.run() が対象にする文書パスの和集合を、同じ順序・同じ重複
    排除規則で返す：テンプレート ∪ PRD ∪ ADR ∪ BDD ∪ UT/CT/ST/UAT ∪
    other（前述のいずれとも重ならないものだけ）∪ 追跡表（存在すれば）。"""
    cfg = cfg or load_kit_config(root)
    tpl = [root / v for v in cfg['templates'].values()]
    prd, adr, bdd = (_globs(root, cfg, k) for k in ('prd', 'adr', 'bdd'))
    tdocs = [p for k in ('ut', 'ct', 'st', 'uat') for p in _globs(root, cfg, k)]
    trace = root / cfg['docs']['trace']
    special = set(tpl) | set(prd) | set(adr) | set(bdd) | set(tdocs) | {trace}
    other = [p for p in _globs(root, cfg, 'other') if p not in special]
    paths = tpl + prd + adr + bdd + tdocs + other
    if trace.is_file():
        paths.append(trace)
    return paths
