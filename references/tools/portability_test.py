#!/usr/bin/env python3
"""テンプレートだけから別名・別構成の最小プロジェクトを作り、kit_lint.py が通ることを確かめる。

「リンターがサンプル専用になっていないか」「テンプレートを埋めれば検査を通るか」
「任意節を節ごと削っても通るか」を確認するための試験。kit.toml は実物をコピーし、
パスに関わる値だけを書き換える（[vocab.*]・[ids]・[adr]・[gherkin]・[evidence] のキー名・
[tests] のコード検索先以外はそのまま。max_unique_step_ratio 等の閾値も実物のまま）。
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def fill(text: str, fixes: dict[str, str] | None = None) -> str:
    text = re.sub(r"^is_template: true\n", "", text, flags=re.MULTILINE)
    text = re.sub(
        r"^> 記入方法は .*\n", "", text, flags=re.MULTILINE
    )  # 指示書へのリンク行は利用者が消す行
    for a, b in (fixes or {}).items():
        text = text.replace(a, b)
    # {{a｜b｜c}} は最初の候補を採用する。それ以外の {{...}} は中身をそのまま残す（自由記述欄の代用）。
    return re.sub(r"\{\{(.*?)\}\}", lambda m: m.group(1).split("｜")[0], text)


def rewrite_kit_toml(text: str) -> str:
    subs = [
        (r"^prd = \[.*\]", 'prd = ["docs/product/payments.md"]'),
        (r"^adr = \[.*\]", 'adr = ["docs/decisions/ADR-*.md"]'),
        (r"^bdd = \[.*\]", 'bdd = ["docs/behaviour/*.md"]'),
        (r"^ut = \[.*\]", 'ut = ["docs/quality/ut_*.md"]'),
        (r"^ct = \[.*\]", 'ct = ["docs/quality/ct_*.md"]'),
        (r"^st = \[.*\]", 'st = ["docs/quality/st_*.md"]'),
        (r"^uat = \[.*\]", 'uat = ["docs/quality/uat_*.md"]'),
        (r"^other = \[.*\]", "other = []"),
        (r'^trace = ".*"', 'trace = "docs/TRACE.md"'),
        (r'^prd = "prd/PRD_TEMPLATE\.md"', 'prd = "tpl/PRD_TEMPLATE.md"'),
        (r'^adr = "adr/ADR_TEMPLATE\.md"', 'adr = "tpl/ADR_TEMPLATE.md"'),
        (r'^bdd = "bdd/BDD_TEMPLATE\.md"', 'bdd = "tpl/BDD_TEMPLATE.md"'),
        (r'^ut = "ut/UT_TEMPLATE\.md"', 'ut = "tpl/UT_TEMPLATE.md"'),
        (r'^ct = "ct/CT_TEMPLATE\.md"', 'ct = "tpl/CT_TEMPLATE.md"'),
        (r'^st = "st/ST_TEMPLATE\.md"', 'st = "tpl/ST_TEMPLATE.md"'),
        (r'^uat = "uat/UAT_TEMPLATE\.md"', 'uat = "tpl/UAT_TEMPLATE.md"'),
        (r'^project = ".*"', 'project = "examples/mini_project"'),
        (r"^code = \[.*\]", 'code = ["examples/mini_project/test_*.py"]'),
        (r"^inputs = \[.*\]", 'inputs = ["examples/mini_project/test_*.py"]'),
    ]
    for pat, rep in subs:
        text, n = re.subn(pat, rep, text, count=1, flags=re.MULTILINE)
        assert n == 1, f"kit.toml rewrite: pattern matched {n} times, expected 1: {pat}"
    return text


def run_kit_lint(t: Path, *args: str) -> dict:
    r = subprocess.run(
        [sys.executable, str(t / "tools/kit_lint.py"), *args],
        cwd=t,
        capture_output=True,
        text=True,
    )
    assert r.returncode in (0, 1), (
        f"kit_lint.py {args}: unexpected exit {r.returncode}\n{r.stdout}\n{r.stderr}"
    )
    import json as _json

    return _json.loads(r.stdout)


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        t = Path(tmp)
        for d in (
            "docs/product",
            "docs/decisions",
            "docs/behaviour",
            "docs/quality",
            "tools",
            "tpl",
            "examples/mini_project",
        ):
            (t / d).mkdir(parents=True)
        shutil.copy(ROOT / "tools/kit_lint.py", t / "tools")
        shutil.copy(ROOT / "tools/render_mermaid.py", t / "tools")

        tests = {
            "ut": "ut/UT_TEMPLATE.md",
            "ct": "ct/CT_TEMPLATE.md",
            "st": "st/ST_TEMPLATE.md",
            "uat": "uat/UAT_TEMPLATE.md",
        }
        # 各テンプレート自身も all_docs としてリンク検査の対象になる。GUIDE ファイルは複製せず、
        # GUIDE への案内行（記入方法は...）だけを剥がして未参照のリンクを作らない。
        for k in ("prd/PRD_TEMPLATE.md", "adr/ADR_TEMPLATE.md", "bdd/BDD_TEMPLATE.md", *tests.values()):
            text = re.sub(r"^> 記入方法は .*\n", "", (ROOT / k).read_text(encoding="utf-8"), flags=re.MULTILINE)
            (t / "tpl" / Path(k).name).write_text(text, encoding="utf-8")

        prd = fill(
            (ROOT / "prd/PRD_TEMPLATE.md").read_text(encoding="utf-8"),
            {"{{数値・単位・分位・期間}}": "p95 が 500ms 以下"},
        )
        prd = re.sub(
            r"^## \d+\. [^\n]*（任意）\n.*?(?=^## )", "", prd, flags=re.MULTILINE | re.DOTALL
        )  # 任意節を節ごと削除
        (t / "docs/product/payments.md").write_text(prd, encoding="utf-8")

        adr = fill(
            (ROOT / "adr/ADR_TEMPLATE.md").read_text(encoding="utf-8"),
            {"{{高｜中｜低}}": "低", "案{{X}}": "案A"},
        )
        (t / "docs/decisions/ADR-0001-something.md").write_text(adr, encoding="utf-8")

        # ステップ語彙の再利用率（実物の kit.toml の閾値 0.60）を満たすため、2つのシナリオの
        # 「もし」「ならば」に同じ語彙を割り当てる（実際の記入でも同じ語彙表を再利用するのが前提）。
        bdd_fixes = {
            "{{値 <入力> を伴う出来事}}": "1つの出来事",
            '{{結果 "<結果>" }}': "観察できる結果",
        }
        (t / "docs/behaviour/payments.md").write_text(
            fill((ROOT / "bdd/BDD_TEMPLATE.md").read_text(encoding="utf-8"), bdd_fixes),
            encoding="utf-8",
        )

        for kind, src in tests.items():
            (t / f"docs/quality/{kind}_payments.md").write_text(
                fill((ROOT / src).read_text(encoding="utf-8")), encoding="utf-8"
            )

        # UT-001／CT-001 の「テスト名」プレースホルダが埋まると `test_name` になる。
        # [tests] の各種チェック（E152 含む）を実際に走らせるための最小のテストコード。
        (t / "examples/mini_project/test_mini.py").write_text(
            "def test_name():\n    assert True\n",
            encoding="utf-8",
        )

        kit_text = rewrite_kit_toml((ROOT / "kit.toml").read_text(encoding="utf-8"))
        (t / "kit.toml").write_text(kit_text, encoding="utf-8")

        run_kit_lint(t, "trace")
        run_kit_lint(t, "extract")

        mermaid_dir = ROOT / ".mermaid/11/node_modules/mermaid"
        mermaid_note: str
        if not mermaid_dir.is_dir():
            mermaid_note = f"skipped: {mermaid_dir} not present (run npm install mermaid@11 under references/.mermaid/11 first)"
        else:
            probe = subprocess.run(
                [sys.executable, "-c", "import playwright"], capture_output=True
            )
            if probe.returncode != 0:
                mermaid_note = (
                    "skipped: playwright is not importable from this interpreter"
                )
            else:
                r = subprocess.run(
                    [
                        sys.executable,
                        str(t / "tools/render_mermaid.py"),
                        "--mermaid-dir",
                        str(mermaid_dir),
                        "--output",
                        str(t / "evidence/mermaid_render.json"),
                    ],
                    cwd=t,
                    capture_output=True,
                    text=True,
                )
                assert r.returncode == 0, (
                    f"render_mermaid.py failed (exit {r.returncode}):\n{r.stdout}\n{r.stderr}"
                )
                mermaid_note = f"rendered via {mermaid_dir}"

        rep = run_kit_lint(t, "check")
        out = {
            "status": rep["status"],
            "errors": rep["errors"],
            "warnings": rep["warnings"],
            "stats": {k: v for k, v in rep["stats"].items() if k != "docs_sha256"},
            "mermaid": mermaid_note,
            "note": "PRD・ADR・BDD・UT・CT・ST・UAT の全テンプレートのプレースホルダを機械的に埋め、PRD の任意節を全て削除した、"
            "別名・別ディレクトリ構成のプロジェクト。kit.toml は実物のコピー（パスのみ書き換え）。"
            "[tests] は最小のテストコード（test_name 関数1つ）で E152 まで検査する",
        }
    (ROOT / "evidence/portability_test.json").write_text(
        __import__("json").dumps(out, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(__import__("json").dumps(out, ensure_ascii=False, indent=2))
    return 0 if out["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
