---
paths: **/*.py
---

このルールを使用するときには、回答時に 🧩 の絵文字をつけてください。

## GPU / Accelerator を使う Python スクリプト実行について

`torch` などで accelerator を使う可能性がある Python スクリプトを実行する場合は、OS と実行環境に合わせて device を明示してください。

### Ubuntu / Linux: CUDA

Ubuntu や Linux の NVIDIA GPU 環境では、まず `nvidia-smi` で空いている GPU を確認し、`CUDA_VISIBLE_DEVICES` を指定して実行してください。

```shell
nvidia-smi
CUDA_VISIBLE_DEVICES=0 uv run main.py
```

複数 GPU を使う場合も、意図しない GPU を占有しないように対象を明示してください。

```shell
CUDA_VISIBLE_DEVICES=0,1 uv run main.py
```

### macOS: MPS

Apple Silicon macOS では CUDA ではなく MPS backend を使います。`CUDA_VISIBLE_DEVICES` は使わず、スクリプト側で `mps` device を選択できるか確認してください。

```shell
uv run python - <<'PY'
import torch
print(torch.backends.mps.is_available())
print(torch.device("mps" if torch.backends.mps.is_available() else "cpu"))
PY
```

MPS 対応スクリプトでは、必要に応じて device 引数や環境変数で `mps` を明示してください。

```shell
uv run main.py --device mps
```

MPS 非対応の演算が含まれる場合は CPU fallback や精度差が起きることがあります。実験結果を比較するときは、CUDA / MPS / CPU のどの device で実行したかを記録してください。
