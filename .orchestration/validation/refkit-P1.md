# refkit-P1 validation

## sha256sum -c references/SHA256SUMS.txt (kit tree)

```text
$ cd references && sha256sum -c SHA256SUMS.txt
./00_README.md: OK
./01_ADVERSARIAL_REVIEW.md: OK
./02_RESEARCH_AND_DECISIONS.md: OK
./03_CONVENTIONS.md: OK
./04_TRACEABILITY.md: OK
./05_AI_AGENT_INSTRUCTIONS.md: OK
./06_TEST_STRATEGY.md: OK
./90_VALIDATION_REPORT.md: OK
./adr/ADR-0001-ai-authority-boundary.md: OK
./adr/ADR-0002-decision-consistency.md: OK
./adr/ADR_GUIDE.md: OK
./adr/ADR_TEMPLATE.md: OK
./bdd/BDD_GUIDE.md: OK
./bdd/BDD_SAMPLE.md: OK
./bdd/BDD_TEMPLATE.md: OK
./ct/CT_GUIDE.md: OK
./ct/CT_SAMPLE.md: OK
./ct/CT_TEMPLATE.md: OK
./evidence/example_tests.json: OK
./evidence/kit_lint_check.json: OK
./evidence/kit_lint_selftest.json: OK
./evidence/mermaid_render.json: OK
./evidence/portability_test.json: OK
./examples/flowapprove_core/.gitignore: OK
./examples/flowapprove_core/flowapprove/__init__.py: OK
./examples/flowapprove_core/flowapprove/domain.py: OK
./examples/flowapprove_core/flowapprove/service.py: OK
./examples/flowapprove_core/pyproject.toml: OK
./examples/flowapprove_core/tests/component/test_decision_component.py: OK
./examples/flowapprove_core/tests/component/test_feat_004_decision.py: OK
./examples/flowapprove_core/tests/conftest.py: OK
./examples/flowapprove_core/tests/unit/test_domain.py: OK
./features/FEAT-001.feature: OK
./features/FEAT-002.feature: OK
./features/FEAT-003.feature: OK
./features/FEAT-004.feature: OK
./features/FEAT-005.feature: OK
./features/FEAT-006.feature: OK
./features/FEAT-007.feature: OK
./features/FEAT-008.feature: OK
./kit.toml: OK
./prd/PRD_GUIDE.md: OK
./prd/PRD_SAMPLE.md: OK
./prd/PRD_TEMPLATE.md: OK
./st/ST_GUIDE.md: OK
./st/ST_SAMPLE.md: OK
./st/ST_TEMPLATE.md: OK
./tools/kit_lint.py: OK
./tools/portability_test.py: OK
./tools/render_mermaid.py: OK
./tools/run_examples.py: OK
./uat/UAT_GUIDE.md: OK
./uat/UAT_SAMPLE.md: OK
./uat/UAT_TEMPLATE.md: OK
./ut/UT_GUIDE.md: OK
./ut/UT_SAMPLE.md: OK
./ut/UT_TEMPLATE.md: OK
```

## sha256sum -c references/archive/SHA256SUMS.txt

```text
$ cd references/archive && sha256sum -c SHA256SUMS.txt
PRD_ADR_BDD.zip: OK
PRD_ADR_BDD_Kit_v2_20260919.zip: OK
PRD_ADR_BDD_TEST_Kit_v3_20260919.zip: OK
TestSuite.zip: OK
```

## Nested-zip byte-identity check (v2/v3 kit zip inside the outer flattened zips)

```text
$ unzip -p references/archive/PRD_ADR_BDD.zip PRD_ADR_BDD_Kit_v2_20260919.zip | sha256sum
$ sha256sum references/archive/PRD_ADR_BDD_Kit_v2_20260919.zip
d6853a24dfc8ec50798539c19eac2059773453690229192c128ba0180a9d2904  (both, confirmed identical)
$ unzip -p references/archive/TestSuite.zip PRD_ADR_BDD_TEST_Kit_v3_20260919.zip | sha256sum
$ sha256sum references/archive/PRD_ADR_BDD_TEST_Kit_v3_20260919.zip
ac98b8932823b7228bca684e050b050e052b188b385e09ed0b8f4e12a32f7caa  (both, confirmed identical)
```

## No dropped loose duplicates under references/

```text
$ find references -iname '*_TEST_SUITE.md' -o -iname '*DEVISIONS*' | grep -v '^references/archive'
(no output)
```

## Link scan (references/, expected zero DANGLING)

```text
$ cd references && python3 - <<'PY'
import re,glob,os
for p in sorted(glob.glob('**/*.md',recursive=True)):
    for m in re.finditer(r'\]\(([^)#\s]+)(#[^)]*)?\)',open(p,encoding='utf-8').read()):
        t=m.group(1)
        if t.startswith('http'): continue
        q=os.path.normpath(os.path.join(os.path.dirname(p),t))
        if not os.path.exists(q): print('DANGLING',p,'->',t)
PY
(no output; exit 0 -> zero DANGLING)
```

## uv run --python 3.12 --with gherkin-official --with PyYAML python tools/kit_lint.py check --json /tmp/refkit-baseline/kit_lint_check.json

```json
{
  "status": "passed",
  "errors": [],
  "warnings": [],
  "stats": {
    "steps": 172,
    "unique_step_patterns": 66,
    "unique_step_ratio": 0.384,
    "relative_links": 134,
    "mermaid_blocks": 20,
    "documents": 31,
    "fr": 28,
    "nfr": 9,
    "rules": 23,
    "scenarios": 41,
    "expanded_cases": 68,
    "adr": 2,
    "feature_files": 8,
    "test_items": {
      "ut": 18,
      "ct": 6,
      "st": 5,
      "uat": 11
    },
    "personas": 6,
    "docs_sha256": {
      "prd/PRD_TEMPLATE.md": "12b689646363120394cd83af94552c22f3028e5675d4cac4db37347501c1804a",
      "adr/ADR_TEMPLATE.md": "c37b19f43b0eb77a26ae622d1f5bf1658e2a31a9a7babaaad017ec28e00daee5",
      "bdd/BDD_TEMPLATE.md": "b5f1a4f8ed1bd572fe3279cfe36c3cbfaa50a122f48c90f409613d4affa94a61",
      "ut/UT_TEMPLATE.md": "7e74ce8bad88390adced719f369eb826b3e960d3a544e13ee92a1bfde6d9ce82",
      "ct/CT_TEMPLATE.md": "c773080e14c3d0ff89253e3ba6ee435557543dbb2b11045eeb5bb291754cda18",
      "st/ST_TEMPLATE.md": "ed989062dd0a9c5ac6da9995825f431d72a5aaa1842c70df7e0ca090c4cf40e8",
      "uat/UAT_TEMPLATE.md": "a30aa2c8325d60a802459ab3e4305afa7dd795adbef4cbc453a8ece3b9f40439",
      "prd/PRD_SAMPLE.md": "7a104f195fd3fb919370fb17ee8542150998813b21a4b30891a3e9c9f0fe759c",
      "adr/ADR-0001-ai-authority-boundary.md": "e63416ca8bcdbfc6b2c986fcac7f655019ccd778bc8397ef7595ee7cf5976a9d",
      "adr/ADR-0002-decision-consistency.md": "d6f461d6405756b44ebf6e4558b835c11688bcaf12343ca6b75cc1deae655c12",
      "bdd/BDD_SAMPLE.md": "ecffc79f56ebf98061f2ca3d751bf25d06953ca1942614ce48433ebf1a167dd8",
      "ut/UT_SAMPLE.md": "48658acb0a21ef8a1cec095556143ef99eb5adf62a12d6bb6f7e3f126363806a",
      "ct/CT_SAMPLE.md": "ee63558b4acd42bea146ce2aa80f5d0ad602093146f5eaaa6b8be87dd1388512",
      "st/ST_SAMPLE.md": "05a574c3de30e4647579beb77d3412e32dc9603d3221eb5b808eee923f0965d6",
      "uat/UAT_SAMPLE.md": "6d585bf6a46eb9e0a9163e19fa2033938679ffcc063c10e8a4155125c01bf32f",
      "00_README.md": "6c7ff364785c7ff85e8a4ac3fc03108b333ee656baa0360b933702d2ddfb7d70",
      "01_ADVERSARIAL_REVIEW.md": "c04237eadaa1bf80d5a5f31d990cb827e58f1466662f4f130a73dba6363c73b8",
      "02_RESEARCH_AND_DECISIONS.md": "0fa44ebb2c346e7f6eb4d9fad52727bc51fc1d0153d13048508153d0eac434b1",
      "03_CONVENTIONS.md": "f41b488bab13343766e839881ba6bb7fcc5288c51cb850b45bede3432636d763",
      "05_AI_AGENT_INSTRUCTIONS.md": "ac9e225a763de0f14e3f3575786211e3c9207ab952544398a13b859ff2c73ad5",
      "06_TEST_STRATEGY.md": "c009932a761d979e39bf2814c11d2faae8702e31b48b41a30a6af6b0721ef710",
      "90_VALIDATION_REPORT.md": "13305fa9d66e36bee04d088660830b8269e52882ca497f2fb3f76e290fb1a03c",
      "README.md": "14c14ca3a89592764862cb83ee396ce49f24cb121221a11d733519ea0856e6f9",
      "adr/ADR_GUIDE.md": "82e465e3ef069385f41d801262c02e1a1e855943aa76c0dcb4c1dc243b3be517",
      "bdd/BDD_GUIDE.md": "d943e6acf3f7ef65daec82acdb49268c61b056b587edf6bac602c913785ce1c4",
      "ct/CT_GUIDE.md": "c9282fba453a6636e620caeb096e966ca4106fb9d023d65f6b571bce771baa27",
      "prd/PRD_GUIDE.md": "dbbf9bcd802c524bcdf274ef56fdc9b72f5aaa5f6775a47f407444035c12d070",
      "st/ST_GUIDE.md": "5c00ed5679089e7b25150d062ee2454a30e1f58bb1e6c3333ba0dc9f0d80f1bb",
      "uat/UAT_GUIDE.md": "6383b889d3fda998a862e4220420da85172ab1b8e95f4a31807750e4d46eda37",
      "ut/UT_GUIDE.md": "f627663351e641698541876b11169d63d3e85c03c383e49a38e6e322e847a0d7",
      "04_TRACEABILITY.md": "fd6417758c7e05760aa11edcf32331e6ec9c3e490f707566f832255468cf63bb"
    }
  },
  "tools": {
    "python": "3.12.3",
    "gherkin-official": "42.0.1",
    "PyYAML": "6.0.3"
  },
  "executed_at_utc": "2026-09-23T09:23:57+00:00",
  "scope": "文書検査のみ。製品試験・承認ではない"
}
```

## uv run --python 3.12 --with gherkin-official --with PyYAML python tools/kit_lint.py selftest --json /tmp/refkit-baseline/kit_lint_selftest.json

```json
{
  "status": "passed",
  "baseline": "passed",
  "mutations": [
    {
      "mutation": "FRを2文にする",
      "expect": "E034",
      "status": "detected"
    },
    {
      "mutation": "FRの型と構文の不一致",
      "expect": "E033",
      "status": "detected"
    },
    {
      "mutation": "存在しない根拠ID",
      "expect": "E037",
      "status": "detected"
    },
    {
      "mutation": "NFRの検証計画欠落",
      "expect": "E043",
      "status": "detected"
    },
    {
      "mutation": "必須節の改名",
      "expect": "E020",
      "status": "detected"
    },
    {
      "mutation": "Gherkin構文破壊",
      "expect": "E050",
      "status": "detected"
    },
    {
      "mutation": "SCN重複",
      "expect": "E064",
      "status": "detected"
    },
    {
      "mutation": "未知の要件タグ",
      "expect": "E070",
      "status": "detected"
    },
    {
      "mutation": "PRD受入とBDDタグの不一致",
      "expect": "E072",
      "status": "detected"
    },
    {
      "mutation": "試験用語の混入",
      "expect": "E060",
      "status": "detected"
    },
    {
      "mutation": "ADR採用案が一覧にない",
      "expect": "E090",
      "status": "detected"
    },
    {
      "mutation": "ADR addresses不正",
      "expect": "E083",
      "status": "detected"
    },
    {
      "mutation": "ADR status語彙外",
      "expect": "E080",
      "status": "detected"
    },
    {
      "mutation": "リンク切れ",
      "expect": "E016",
      "status": "detected"
    },
    {
      "mutation": "表の列数不揃い",
      "expect": "E011",
      "status": "detected"
    },
    {
      "mutation": "図を変えると描画証跡が古くなる",
      "expect": "E103",
      "status": "detected"
    },
    {
      "mutation": "追跡表の手修正",
      "expect": "E120",
      "status": "detected"
    },
    {
      "mutation": ".feature の手修正",
      "expect": "E121",
      "status": "detected"
    },
    {
      "mutation": "NVTの割当が1つでない",
      "expect": "E146",
      "status": "detected"
    },
    {
      "mutation": "テスト項目の由来が存在しない",
      "expect": "E142",
      "status": "detected"
    },
    {
      "mutation": "設計書のテスト名がコードにない",
      "expect": "E152",
      "status": "detected"
    },
    {
      "mutation": "テストコードを変えると実行証跡が古くなる",
      "expect": "E153",
      "status": "detected"
    },
    {
      "mutation": "目的に受入シナリオがない",
      "expect": "E150",
      "status": "detected"
    },
    {
      "mutation": "機能がどの水準にも割り当てられていない",
      "expect": "E148",
      "status": "detected"
    },
    {
      "mutation": "front matter の語彙外",
      "expect": "E025",
      "status": "detected"
    },
    {
      "mutation": "合格と書いて実行証跡がない",
      "expect": "E155",
      "status": "detected"
    },
    {
      "mutation": "ペルソナの主体が存在しない",
      "expect": "E145",
      "status": "detected"
    },
    {
      "mutation": "1章の由来が本文に出てこない",
      "expect": "E157",
      "status": "detected"
    },
    {
      "mutation": "文書の実行結果が証跡と食い違う",
      "expect": "E158",
      "status": "detected"
    },
    {
      "mutation": "旅程が通るシナリオが存在しない",
      "expect": "E143",
      "status": "detected"
    }
  ],
  "executed_at_utc": "2026-09-23T09:23:58+00:00"
}
```

## uv run --python 3.12 --with gherkin-official --with PyYAML python tools/portability_test.py (exit 0)

```json
{
  "status": "passed",
  "errors": [],
  "warnings": [
    "W102 mermaid_render.json: Mermaid 描画証跡がない（tools/render_mermaid.py を実行）"
  ],
  "stats": {
    "steps": 7,
    "unique_step_patterns": 6,
    "unique_step_ratio": 0.857,
    "relative_links": 10,
    "mermaid_blocks": 10,
    "documents": 16,
    "fr": 1,
    "nfr": 1,
    "rules": 1,
    "scenarios": 2,
    "expanded_cases": 3,
    "adr": 1,
    "feature_files": 1,
    "test_items": {
      "ut": 1,
      "ct": 1,
      "st": 1,
      "uat": 2
    },
    "personas": 1
  },
  "note": "PRD・ADR・BDD・UT・CT・ST・UAT の全テンプレートのプレースホルダを機械的に埋め、PRD の任意節を全て削除した、別名・別ディレクトリ構成のプロジェクト（テストコードなし）"
}
```

## uv venv --python 3.12 references/examples/flowapprove_core/.venv

```text
Using CPython 3.12.3 interpreter at: /usr/bin/python3.12
Creating virtual environment at: examples/flowapprove_core/.venv
Activate with: source examples/flowapprove_core/.venv/bin/activate
```

## uv pip install --python references/examples/flowapprove_core/.venv pytest hypothesis pytest-bdd coverage mutmut

```text
Resolved 28 packages
Installed 28 packages: click 8.5.0, coverage 7.16.1, gherkin-official 29.0.0, hypothesis 6.168.0,
iniconfig 2.3.0, libcst 1.9.0, linkify-it-py 2.2.0, mako 1.4.1, markdown-it-py 4.2.0, markupsafe 3.0.3,
mdit-py-plugins 0.6.1, mdurl 0.1.2, mutmut 3.8.0, packaging 26.3, parse 1.22.1, parse-type 0.6.6,
platformdirs 4.11.8, pluggy 1.6.0, pygments 2.21.0, pytest 9.1.1, pytest-bdd 8.1.0, pyyaml 6.0.3,
rich 15.0.0, setproctitle 1.3.7, six 1.17.0, sortedcontainers 2.4.0, textual 8.2.8, typing-extensions 4.16.0
```

## uv pip list --python references/examples/flowapprove_core/.venv

```text
$ uv pip list --python examples/flowapprove_core/.venv
[2mUsing Python 3.12.3 environment at: examples/flowapprove_core/.venv[0m
Package           Version
----------------- -------
click             8.5.0
coverage          7.16.1
gherkin-official  29.0.0
greenlet          3.5.6
hypothesis        6.168.0
iniconfig         2.3.0
libcst            1.9.0
linkify-it-py     2.2.0
mako              1.4.1
markdown-it-py    4.2.0
markupsafe        3.0.3
mdit-py-plugins   0.6.1
mdurl             0.1.2
mutmut            3.8.0
packaging         26.3
parse             1.22.1
parse-type        0.6.6
platformdirs      4.11.8
playwright        1.63.0
pluggy            1.6.0
pyee              13.0.1
pygments          2.21.0
pytest            9.1.1
pytest-bdd        8.1.0
pyyaml            6.0.3
rich              15.0.0
setproctitle      1.3.7
six               1.17.0
sortedcontainers  2.4.0
textual           8.2.8
typing-extensions 4.16.0
```

## PATH=<venv>/bin:$PATH <venv>/bin/python tools/run_examples.py --mutation (exit 0)

```json
{
  "status": "passed",
  "UT": {
    "tests": 125,
    "passed": 125,
    "branch_coverage_percent": 44.4
  },
  "CT": {
    "tests": 29,
    "passed": 29,
    "branch_coverage_percent": 88.4
  },
  "mutation": {
    "target": "flowapprove/domain.py",
    "tests": "tests/unit",
    "mutants": 68,
    "killed": 67,
    "survived": [
      "flowapprove.domain.x_next_state__mutmut_1"
    ],
    "score_percent": 98.5
  },
  "verified_ids": 40
}
EXIT=0
```

## Restoring evidence/example_tests.json to v3's original bytes

```text
run_examples.py has no output-redirect option (writes ROOT/evidence/example_tests.json directly);
the tree was not yet committed/staged at this point, so git checkout -- could not be used (nothing
to restore from). Instead: copied the mutated file to /tmp/refkit-baseline/example_tests.json, then
overwrote references/evidence/example_tests.json with the original bytes re-extracted from
references/archive/PRD_ADR_BDD_TEST_Kit_v3_20260919.zip (prd_adr_bdd_test_kit_v3/evidence/example_tests.json).

$ sha256sum evidence/example_tests.json
f0c682ea13a4c79ec0c08f58ee2b8110405c1bd99504f9c5fb644794d1436e6c  evidence/example_tests.json  (matches SHA256SUMS.txt)
```

## npm install --prefix references/.mermaid/11 mermaid@11

```text

added 113 packages in 3s

4 packages are looking for funding
  run `npm fund` for details
```

## npm install --prefix references/.mermaid/12 mermaid@12

```text

added 117 packages in 2s

4 packages are looking for funding
  run `npm fund` for details
```

## npm ls --prefix references/.mermaid/11 mermaid

```text
11@ /home/moriya/Workspace/dotfiles-w1/references/.mermaid/11
└── mermaid@11.17.2

```

## npm ls --prefix references/.mermaid/12 mermaid

```text
12@ /home/moriya/Workspace/dotfiles-w1/references/.mermaid/12
└── mermaid@12.0.0

```

## node --version

```text
v26.9.0
```

## uv pip install --python references/examples/flowapprove_core/.venv playwright

```text
Resolved 4 packages
Installed 3 packages: greenlet 3.5.6, playwright 1.63.0, pyee 13.0.1
```

## <venv>/bin/python -m playwright install chromium (effect: playwright-chromium)

```text
Downloading Chrome for Testing 153.0.8010.12 (playwright chromium v1243)[2m from https://cdn.playwright.dev/builds/cft/153.0.8010.12/linux-arm64/chrome-linux-arm64.zip[22m
|                                                                                |   0% of 186.8 MiB
|■■■■■■■■                                                                        |  10% of 186.8 MiB
|■■■■■■■■■■■■■■■■                                                                |  20% of 186.8 MiB
|■■■■■■■■■■■■■■■■■■■■■■■■                                                        |  30% of 186.8 MiB
|■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■                                                |  40% of 186.8 MiB
|■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■                                        |  50% of 186.8 MiB
|■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■                                |  60% of 186.8 MiB
|■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■                        |  70% of 186.8 MiB
|■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■                |  80% of 186.8 MiB
|■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■        |  90% of 186.8 MiB
|■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■| 100% of 186.8 MiB
Chrome for Testing 153.0.8010.12 (playwright chromium v1243) downloaded to /home/moriya/.cache/ms-playwright/chromium-1243
Downloading FFmpeg (playwright ffmpeg v1011)[2m from https://cdn.playwright.dev/dbazure/download/playwright/builds/ffmpeg/1011/ffmpeg-linux-arm64.zip[22m
|                                                                                |   0% of 1.6 MiB
|■■■■■■■■                                                                        |  10% of 1.6 MiB
|■■■■■■■■■■■■■■■■                                                                |  20% of 1.6 MiB
|■■■■■■■■■■■■■■■■■■■■■■■■                                                        |  30% of 1.6 MiB
|■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■                                                |  40% of 1.6 MiB
|■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■                                        |  50% of 1.6 MiB
|■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■                                |  60% of 1.6 MiB
|■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■                        |  70% of 1.6 MiB
|■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■                |  80% of 1.6 MiB
|■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■        |  90% of 1.6 MiB
|■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■| 100% of 1.6 MiB
FFmpeg (playwright ffmpeg v1011) downloaded to /home/moriya/.cache/ms-playwright/ffmpeg-1011
Downloading Chrome Headless Shell 153.0.8010.12 (playwright chromium-headless-shell v1243)[2m from https://cdn.playwright.dev/builds/cft/153.0.8010.12/linux-arm64/chrome-headless-shell-linux-arm64.zip[22m
|                                                                                |   0% of 114.7 MiB
|■■■■■■■■                                                                        |  10% of 114.7 MiB
|■■■■■■■■■■■■■■■■                                                                |  20% of 114.7 MiB
|■■■■■■■■■■■■■■■■■■■■■■■■                                                        |  30% of 114.7 MiB
|■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■                                                |  40% of 114.7 MiB
|■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■                                        |  50% of 114.7 MiB
|■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■                                |  60% of 114.7 MiB
|■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■                        |  70% of 114.7 MiB
|■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■                |  80% of 114.7 MiB
|■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■        |  90% of 114.7 MiB
|■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■| 100% of 114.7 MiB
Chrome Headless Shell 153.0.8010.12 (playwright chromium-headless-shell v1243) downloaded to /home/moriya/.cache/ms-playwright/chromium_headless_shell-1243
```

## <venv>/bin/python tools/render_mermaid.py --mermaid-dir .../11/node_modules/mermaid --mermaid-dir .../12/node_modules/mermaid --output /tmp/refkit-baseline/mermaid_render.json (exit 0)

```text
Mermaid 11.17.2: 20/20 ok, negative test rejected=True
Mermaid 12.0.0: 20/20 ok, negative test rejected=True
EXIT=0

$ sha256sum evidence/mermaid_render.json (confirms tracked file untouched, --output used instead)
e66286f9ace80702531af859e94981b0b60ed5a8e892f8547624428ed38f3ed6  evidence/mermaid_render.json  (matches SHA256SUMS.txt)
```

## git status --short (before commit)

```text
 M .gitignore
?? .orchestration/autoskill/runs/refkit-P0-01.md
?? .orchestration/learning/refkit-P0-01.md
?? .orchestration/reports/refkit-P0-01.md
?? .orchestration/sandboxes/refkit-P0-01.md
?? .orchestration/validation/refkit-P0-01.md
?? references/
```

## git show --stat HEAD

```text
commit d3281dee4e5329fe5c95b162f7c9f4a92b3d3c5b
Author: Fumio Moriya <moriya.fumio@technopro.com>
Date:   Wed Sep 23 18:28:37 2026 +0900

    feat(references): import documentation kit v3 as the v4 baseline tree
    
    Replaces the flat, mixed-generation references/ layout (30 loose .md
    files that were a v2/v3 chimera, plus 4 zips) with the single v3 kit
    tree, extracted directly under references/ (references/00_README.md,
    references/prd/, references/tools/, etc.).
    
    Imported: prd_adr_bdd_test_kit_v3/ from
    PRD_ADR_BDD_TEST_Kit_v3_20260919.zip, verbatim (sha256sum -c
    references/SHA256SUMS.txt passes for all 58 files).
    
    Archived: all 4 distributed zips (v2 kit, v3 kit, and their
    flattened outer packagings PRD_ADR_BDD.zip / TestSuite.zip) under
    references/archive/, unchanged, with their own SHA256SUMS.txt and a
    Japanese README documenting provenance and the observed timestamp
    facts (kit entries stamped JST 2026-09-19 16:40 / 17:24-17:25; outer
    zips packaged 2026-09-23). Confirmed the nested kit zips inside the
    two outer zips are byte-identical to the standalone kit zips.
    
    Dropped: the 30 loose .md files that used to sit directly under
    references/ were not copied. They were all byte-identical copies of
    either the v2 or the v3 kit's own files (see the plan's provenance
    table), had ~95 broken relative links from flattening, and depended
    on files (03_CONVENTIONS.md, tools/, kit.toml, evidence/, etc.) that
    only exist inside the zips - keeping them added no information and
    reintroduced the v2/v3 chimera problem the plan calls out.
    
    Also: appended references/-scoped ignores for local toolchains and
    test artefacts (.mermaid/, example venv, mutants, __pycache__,
    .pytest_cache) to .gitignore, and added references/README.md
    explaining the directory's purpose and how to run the kit's own
    checks.
    
    This commit is import + measurement only; no kit document content
    was edited. Baseline reproduction of the kit's own validation
    (kit_lint, portability_test, the flowapprove_core example
    tests+mutation, and Mermaid rendering under both mermaid 11.x and
    12.x) was run separately on this machine; results, tool versions,
    and mismatches against the kit's own shipped report/evidence are in
    .orchestration/reports/refkit-P1.md and
    .orchestration/validation/refkit-P1.md. Reproducing that baseline
    did not change any tracked evidence file: evidence/example_tests.json
    was restored to its original v3 bytes after run_examples.py
    overwrote it (the tool has no output-redirect option), and
    evidence/mermaid_render.json was never touched because
    render_mermaid.py's --output flag was used to write elsewhere.
    
    Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>

 .gitignore                                         |    9 +
 references/00_README.md                            |   43 +
 references/01_ADVERSARIAL_REVIEW.md                |   61 +
 references/02_RESEARCH_AND_DECISIONS.md            |   74 +
 references/03_CONVENTIONS.md                       |  119 ++
 references/04_TRACEABILITY.md                      |  124 ++
 references/05_AI_AGENT_INSTRUCTIONS.md             |   95 +
 references/06_TEST_STRATEGY.md                     |  107 +
 references/90_VALIDATION_REPORT.md                 |   82 +
 references/README.md                               |   28 +
 references/SHA256SUMS.txt                          |   57 +
 references/adr/ADR-0001-ai-authority-boundary.md   |  105 +
 references/adr/ADR-0002-decision-consistency.md    |  111 +
 references/adr/ADR_GUIDE.md                        |   84 +
 references/adr/ADR_TEMPLATE.md                     |   87 +
 references/archive/PRD_ADR_BDD.zip                 |  Bin 0 -> 166869 bytes
 references/archive/PRD_ADR_BDD_Kit_v2_20260919.zip |  Bin 0 -> 109824 bytes
 .../archive/PRD_ADR_BDD_TEST_Kit_v3_20260919.zip   |  Bin 0 -> 205044 bytes
 references/archive/README.md                       |   31 +
 references/archive/SHA256SUMS.txt                  |    4 +
 references/archive/TestSuite.zip                   |  Bin 0 -> 266316 bytes
 references/bdd/BDD_GUIDE.md                        |  129 ++
 references/bdd/BDD_SAMPLE.md                       |  644 ++++++
 references/bdd/BDD_TEMPLATE.md                     |  124 ++
 references/ct/CT_GUIDE.md                          |   98 +
 references/ct/CT_SAMPLE.md                         |  118 ++
 references/ct/CT_TEMPLATE.md                       |   97 +
 references/evidence/example_tests.json             | 2185 ++++++++++++++++++++
 references/evidence/kit_lint_check.json            |   66 +
 references/evidence/kit_lint_selftest.json         |  157 ++
 references/evidence/mermaid_render.json            |  387 ++++
 references/evidence/portability_test.json          |   30 +
 references/examples/flowapprove_core/.gitignore    |    5 +
 .../flowapprove_core/flowapprove/__init__.py       |    5 +
 .../flowapprove_core/flowapprove/domain.py         |  128 ++
 .../flowapprove_core/flowapprove/service.py        |  148 ++
 .../examples/flowapprove_core/pyproject.toml       |   24 +
 .../tests/component/test_decision_component.py     |   83 +
 .../tests/component/test_feat_004_decision.py      |  185 ++
 .../examples/flowapprove_core/tests/conftest.py    |   37 +
 .../flowapprove_core/tests/unit/test_domain.py     |  178 ++
 references/features/FEAT-001.feature               |   77 +
 references/features/FEAT-002.feature               |   44 +
 references/features/FEAT-003.feature               |   85 +
 references/features/FEAT-004.feature               |  122 ++
 references/features/FEAT-005.feature               |   39 +
 references/features/FEAT-006.feature               |   51 +
 references/features/FEAT-007.feature               |   51 +
 references/features/FEAT-008.feature               |   29 +
 references/kit.toml                                |   62 +
 references/prd/PRD_GUIDE.md                        |  116 ++
 references/prd/PRD_SAMPLE.md                       |  247 +++
 references/prd/PRD_TEMPLATE.md                     |  150 ++
 references/st/ST_GUIDE.md                          |  121 ++
 references/st/ST_SAMPLE.md                         |  168 ++
 references/st/ST_TEMPLATE.md                       |  102 +
 references/tools/kit_lint.py                       |  597 ++++++
 references/tools/portability_test.py               |   78 +
 references/tools/render_mermaid.py                 |   83 +
 references/tools/run_examples.py                   |   78 +
 references/uat/UAT_GUIDE.md                        |  132 ++
 references/uat/UAT_SAMPLE.md                       |  107 +
 references/uat/UAT_TEMPLATE.md                     |   93 +
 references/ut/UT_GUIDE.md                          |  119 ++
 references/ut/UT_SAMPLE.md                         |  116 ++
 references/ut/UT_TEMPLATE.md                       |   81 +
 66 files changed, 8997 insertions(+)
```

## python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project

```text
$ python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "[memory:decision] references/ is the single v3-derived kit tree (v4 in progress); zips live in references/archive with SHA256SUMS; loose duplicates removed"
746ce0e8-4f37-475e-b548-fc3bb4fe724f
```
