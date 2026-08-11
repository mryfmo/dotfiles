# T36 validation

Commands and results:

```text
$ test -s .ua/knowledge-graph.json
exit 0

$ python3 -c "import json; d=json.load(open('.ua/knowledge-graph.json')); print(type(d), len(str(d)))"
<class 'dict'> 577853
```

Inline graph validation passed with 0 issues and 0 warnings.

```text
file-level nodes: 704
functions: 301
classes: 17
edges: 632
layers: 7
tour steps: 9
fingerprint baseline: 689 files
```

`build-fingerprints.mjs` emitted a non-fatal JSON-parser warning for a shebang-bearing JSON-like source file, then completed with `Fingerprints baseline: 689 files`.
