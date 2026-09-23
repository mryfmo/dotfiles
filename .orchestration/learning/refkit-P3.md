# refkit-P3: 学びの候補（トリアージ、round 2 で追記）

round 1 の候補（既存の RULE-ID の安易な転用、新規 ID の追加が波及するチェックの予測）に加え、round 2 で得た候補：

## 候補 3: グローバル PostToolUse フォーマッタは `.md` 全文を対象にする

**観察**: このリポジトリ（`~/.claude/settings.json`）には `Write|Edit|MultiEdit` にマッチする PostToolUse フックがあり、編集対象ファイルへ `npx prettier@2 --write` を実行する。1 文字の差分を狙って `Edit` を呼んでも、フォーマッタは表の桁揃えや CJK/Latin 境界のスペーシングをファイル全体に対して再計算するため、意図しない大きな diff になる。
**一般化できる点**: `allowed_files` が「1 行だけ」「1 セルだけ」のように厳格な差分制約を課すタスクで Markdown を編集する場合、`Edit`/`Write`/`MultiEdit` ツールではなく `Bash` から直接ファイルを書き換える（Python の `str.replace` 等）ことで、フックの対象（ツール呼び出しの種別）自体を外し、意図しない全文整形を避けられる。着手前に `git diff --stat` で差分規模を確認する習慣も有効。
**昇格の判断**: 判定者に一任。汎用的に有用な知見のため、ルール昇格の優先度は高いと考える。

## 候補 4: 「禁止された生成物への言及」だけでも regenerate とみなされる

**観察**: `references/04_TRACEABILITY.md` を `kit_lint.py trace` で再生成してコミットしたことが、`forbidden_actions` の `regenerate-04-features-evidence` に該当すると判定された。task_file 側の「E120/E121 以外が 0 であること」という検証要求と、`forbidden_actions` の「04 を再生成しない」という制約は、両方を厳密に満たすことができない場合がある（04 を再生成しなければ E120 が残る）。
**一般化できる点**: 検証要求と禁止事項が矛盾しうる場合は、禁止事項を優先し、検証要求側の例外（E120 等）を acceptance 側に明示的に確認する。
**昇格の判断**: 判定者に一任。

## AutoSkill

使用していない（round 1・round 2 とも、既存の `kit_lint.py`・`contextdb_cli.py`・標準シェルツールのみで完了）。
