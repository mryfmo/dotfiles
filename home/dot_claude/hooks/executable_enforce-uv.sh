#!/bin/bash

# @file home/dot_claude/hooks/executable_enforce-uv.sh
# @brief Block direct Python and pip commands in favor of `uv`.
# @description
#   Emit PreToolUse permissionDecision deny for direct `pip` or `python` usage;
#   other input exits successfully without output. Contract verified 2026-10-05.
#   Advisory, not a boundary: it nudges toward uv. A Bash line is parsed by shfmt (on PATH from the mise config)
#   into its syntax tree, and every simple command in it is judged on its own text; when shfmt is absent or cannot
#   parse the line, the hook decides nothing and exits 0 (fail open).
# @see https://code.claude.com/docs/en/hooks#pretooluse-decision-control

# @description Encode the denial reason from stdin using the current hook contract.
# @stdout PreToolUse deny JSON with the original multiline reason.
function deny_command() {
    jq -Rsc '{hookSpecificOutput: {hookEventName: "PreToolUse", permissionDecision: "deny", permissionDecisionReason: rtrimstr("\n")}}'
}

# @description Emit the `uv` replacement message for `pip install`.
# @arg $1 string Parsed `pip` subcommand beginning with `install`.
function handle_pip_install() {
    local pip_cmd="$1"
    local packages
    packages=$(echo "$pip_cmd" | sed 's/install//' | sed 's/--[^ ]*//g' | xargs)

    # -r requirements.txt
    if [[ "$pip_cmd" =~ -r\ .*\.txt ]]; then
        local req_file
        req_file=$(echo "$pip_cmd" | sed -n 's/.*-r \([^ ]*\).*/\1/p')
        deny_command <<- EOF
		📋 requirements.txtからインストール:

		✅ 推奨方法:
		uv add -r $req_file

		これにより:
		• requirements.txt内のすべての依存関係をpyproject.tomlに追加
		• uv.lockファイルを自動生成/更新
		• 仮想環境を自動的に同期

		💡 制約ファイルがある場合:
		uv add -r $req_file -c constraints.txt

		📌 注意: この方法が最も確実で、バージョン指定も正しく処理されます
		EOF
        exit 0
    fi

    # 開発依存関係
    if [[ "$pip_cmd" =~ --dev ]] || [[ "$pip_cmd" =~ -e ]]; then
        deny_command <<- EOF
		🔧 開発依存関係をインストール:

		uv add --dev $packages

		編集可能インストール: uv add -e .
		EOF
        exit 0
    fi

    # 通常のインストール
    deny_command <<- EOF
	📦 パッケージをインストール:

	uv add $packages

	💾 'uv add' はpyproject.tomlに依存関係を保存します
	🔒 uv.lockで再現可能な環境を保証

	💡 特殊なケース:
	• URLからのインストール: パッケージを手動でダウンロードしてから追加
	• 開発版: uv add --dev $packages
	• ローカルパッケージ: uv add -e ./path/to/package
	EOF
    exit 0
}

# @description Emit the `uv remove` replacement message for `pip uninstall`.
# @arg $1 string Parsed `pip` subcommand beginning with `uninstall`.
function handle_pip_uninstall() {
    local pip_cmd="$1"
    local packages
    packages=$(echo "$pip_cmd" | sed 's/uninstall//' | sed 's/-y//g' | xargs)
    deny_command <<- EOF
	🗑️ パッケージを削除:

	uv remove $packages

	✨ 依存関係も自動的にクリーンアップされます
	EOF
    exit 0
}

# @description Explain the `uv` alternatives for `pip list` and `pip freeze`.
function handle_pip_list() {
    deny_command <<- 'EOF'
	📊 パッケージ一覧を確認:

	• プロジェクト依存関係: cat pyproject.toml
	• ロックファイル詳細: cat uv.lock
	• インストール済み一覧: uv tree
	• requirements.txt形式でエクスポート: uv export --format requirements-txt

	💡 'uv tree'はプロジェクトの依存関係ツリーを表示します
	EOF
    exit 0
}

# @description Fall back to a generic `uv` recommendation for other pip commands.
# @arg $1 string Parsed `pip` subcommand.
function handle_pip_other() {
    local pip_cmd="$1"
    deny_command <<- EOF
	🔀 pipコマンドをuvで実行:

	uv $pip_cmd

	💡 パッケージのインストール/削除には 'uv add/remove' を使用してください
	EOF
    exit 0
}

# @description Handle `python -m pip ...` by mapping it to the right `uv` advice.
# @arg $1 string Parsed module arguments after `python -m pip`.
function handle_python_m_pip() {
    local pip_cmd="$1"

    # Parse pip install commands
    if [[ "$pip_cmd" =~ ^install ]]; then
        local packages
        packages=$(echo "$pip_cmd" | sed 's/install//' | sed 's/--[^ ]*//g' | xargs)
        if [[ "$pip_cmd" =~ -r\ .*\.txt ]]; then
            local req_file
            req_file=$(echo "$pip_cmd" | sed -n 's/.*-r \([^ ]*\).*/\1/p')
            deny_command <<- EOF
			📋 requirements.txtからインストール:

			✅ 推奨方法:
			uv add -r $req_file

			💡 これによりすべての依存関係がpyproject.tomlに追加されます
			EOF
        else
            deny_command <<- EOF
			📦 パッケージをインストール:

			uv add $packages

			💡 'uv add' はpyproject.tomlに依存関係を保存します
			EOF
        fi
    else
        deny_command <<- EOF
		🔀 pipコマンドをuvで実行:

		uv $pip_cmd

		💡 パッケージ管理には 'uv add/remove' を使用してください
		EOF
    fi
    exit 0
}

# @description Rewrite `python -m module` invocations to `uv run`.
# @arg $1 string Module invocation after `python -m`.
function handle_python_m_module() {
    local module="$1"
    deny_command <<- EOF
	uvでモジュールを実行:

	uv run python -m $module

	🔄 uvは自動的に環境を同期してから実行します。
	EOF
    exit 0
}

# @description Rewrite direct Python execution to `uv run`.
# @arg $1 string The simple command as written (interpreter and arguments, quotes kept).
function handle_python_run() {
    local segment="$1"
    deny_command <<- EOF
	uvでPythonを実行:

	uv run $segment

	✅ 仮想環境のアクティベーションは不要です！
	EOF
    exit 0
}

# @description Collect the simple commands of a Bash line from shfmt's syntax tree (`shfmt -ln bash --to-json`):
#   every statement whose command is a call (`CallExpr`), in tree order, nested ones (in a pipeline, a list, a
#   subshell, `$(...)`) included, each as its source text from the statement's start to its end offset, so the
#   suggestion keeps its quotes and redirections. Comments and here-document bodies are no statements, and quoting,
#   escapes and line continuations are shfmt's, not this script's.
# @arg $1 string The command line.
# @set SEGMENTS array The simple commands, in order.
# @exitcode 0 The line parsed.
# @exitcode 1 shfmt or jq is absent, or the line does not parse.
function split_segments() {
    local line="$1" tree spans start end
    SEGMENTS=()
    command -v shfmt > /dev/null 2>&1 || return 1
    tree=$(printf '%s' "$line" | shfmt -ln bash --to-json 2> /dev/null) || return 1
    spans=$(jq -r '.. | objects | select(.Cmd.Type? == "CallExpr") | "\(.Pos.Offset) \(.End.Offset)"' <<< "$tree") || return 1
    # shfmt's offsets count bytes, so slice the line byte-wise.
    local LC_ALL=C
    while read -r start end; do
        if [[ -n "$start" && -n "$end" ]]; then
            SEGMENTS+=("${line:start:end-start}")
        fi
    done <<< "$spans"
}

# @description Emit the deny for one simple command that runs pip or Python directly; return for any other.
# @arg $1 string One simple command.
function classify_segment() {
    local segment="$1"
    case "$segment" in
    # ===== pip関連コマンド =====
    pip\ * | pip3\ *)
        # pipコマンドの詳細な解析
        local pip_cmd
        pip_cmd=$(echo "$segment" | sed -E 's/^pip[0-9]? *//' | xargs)

        case "$pip_cmd" in
        install\ *)
            handle_pip_install "$pip_cmd"
            ;;
        uninstall\ *)
            handle_pip_uninstall "$pip_cmd"
            ;;
        list* | freeze*)
            handle_pip_list
            ;;
        *)
            handle_pip_other "$pip_cmd"
            ;;
        esac
        ;;

    # ===== 直接的なPython実行の処理 =====
    python* | py\ *)
        # -m オプションの特別処理
        local args
        args=$(echo "$segment" | sed -E 's/^python[0-9]? //' | xargs 2> /dev/null)
        if [[ "$args" =~ ^-m ]]; then
            local module
            module=${args/-m /}

            case "$module" in
            pip\ *)
                local pip_cmd
                pip_cmd=${module/pip /}
                handle_python_m_pip "$pip_cmd"
                ;;
            *)
                handle_python_m_module "$module"
                ;;
            esac
        fi

        # 基本的なPython実行: the command as written, so `python3 -c 'print(1)'` keeps its quotes.
        handle_python_run "$segment"
        ;;
    esac
}

# @description Read hook input JSON, classify each simple command of a Bash call, and emit a decision.
function main() {
    local input
    input=$(cat)

    # Validate input
    if [ -z "$input" ]; then
        exit 0
    fi

    # Extract fields with error handling
    local tool_name
    tool_name=$(echo "$input" | jq -r '.tool_name' 2> /dev/null || echo "")
    local command
    command=$(echo "$input" | jq -r '.tool_input.command // ""' 2> /dev/null || echo "")

    if [[ "$tool_name" == "Bash" ]]; then
        local segment
        # Advisory: a line shfmt cannot parse (or no shfmt) gets no decision.
        split_segments "$command" || exit 0
        for segment in "${SEGMENTS[@]}"; do
            classify_segment "$segment"
        done
    fi

    exit 0
}

main
