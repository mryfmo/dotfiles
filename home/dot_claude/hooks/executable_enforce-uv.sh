#!/bin/bash

# @file home/dot_claude/hooks/executable_enforce-uv.sh
# @brief Block direct Python and pip commands in favor of `uv`.
# @description
#   Emit PreToolUse permissionDecision deny for direct `pip` or `python` usage;
#   other input exits successfully without output. Contract verified 2026-10-05.
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

# @description Append one trimmed simple command to SEGMENTS; an empty one is skipped.
# @arg $1 string The text between two separators.
# @set SEGMENTS array The simple commands found so far.
function add_segment() {
    local segment="$1"
    segment="${segment#"${segment%%[![:space:]]*}"}"
    segment="${segment%"${segment##*[![:space:]]}"}"
    if [[ -n "$segment" ]]; then
        SEGMENTS+=("$segment")
    fi
}

# @description Split a command line into its simple commands at the unquoted separators `&&`, `||`, `;`, `|`,
#   `&` and newlines, the way Claude Code splits a compound command before matching it, so `cd x && python y.py`
#   is judged by its `python y.py` part. Quotes and backslash escapes are kept in the segment text, and an `&` or `|`
#   that is part of a redirection (`2>&1`, `>&2`, `<&3`, `&>file`, `>|file`) stays in it. A comment (an unquoted `#`
#   that starts a word)
#   runs to the end of its line, and a here-document body (`<<WORD`, `<<-WORD`, `<<'WORD'`, `<<"WORD"`, up to its
#   terminator line) is data: neither yields a segment.
# @arg $1 string The command line.
# @set SEGMENTS array The simple commands, in order.
function split_segments() {
    local line="$1" current="" quote="" char prev i j rest body delimiter strip escaped=-1
    local -a delimiters=() strips=()
    SEGMENTS=()
    for ((i = 0; i < ${#line}; i++)); do
        char=${line:i:1}
        if [[ -n "$quote" ]]; then
            current+=$char
            if [[ "$char" == "$quote" ]]; then
                quote=""
            elif [[ "$char" == "\\" && "$quote" == '"' ]]; then
                current+=${line:i+1:1}
                i=$((i + 1))
            fi
            continue
        fi
        # The character before this one; a backslash-escaped one is part of a word, never an operator or a blank.
        prev=""
        if ((i > 0)); then
            prev=${line:i-1:1}
        fi
        if ((i - 1 == escaped)); then
            prev="\\"
        fi
        case "$char" in
        "'" | '"')
            quote=$char
            current+=$char
            ;;
        "\\")
            current+=$char${line:i+1:1}
            i=$((i + 1))
            escaped=$i
            ;;
        '#')
            if [[ -z "$prev" || "$prev" == [[:space:]\;\&\|\(\)] ]]; then
                # A comment: skip to the newline, which the next turn of the loop handles as a separator.
                rest=${line:i}
                if [[ "$rest" != *$'\n'* ]]; then
                    break
                fi
                body=${rest%%$'\n'*}
                i=$((i + ${#body} - 1))
            else
                current+=$char
            fi
            ;;
        '<')
            if [[ "${line:i:3}" == "<<<" ]]; then
                current+="<<<"
                i=$((i + 2))
            elif [[ "${line:i:2}" == "<<" ]]; then
                j=$((i + 2))
                strip=""
                if [[ "${line:j:1}" == "-" ]]; then
                    strip=1
                    j=$((j + 1))
                fi
                while [[ "${line:j:1}" == [[:blank:]] ]]; do
                    j=$((j + 1))
                done
                delimiter=""
                if [[ "${line:j:1}" == "'" || "${line:j:1}" == '"' ]]; then
                    char=${line:j:1}
                    rest=${line:j+1}
                    delimiter=${rest%%"$char"*}
                    j=$((j + ${#delimiter} + 2))
                else
                    while ((j < ${#line})) && [[ "${line:j:1}" != [[:space:]\;\&\|\<\>\(\)] ]]; do
                        delimiter+=${line:j:1}
                        j=$((j + 1))
                    done
                    delimiter=${delimiter//\\/}
                fi
                current+=${line:i:j-i}
                delimiters+=("$delimiter")
                strips+=("$strip")
                i=$((j - 1))
            else
                current+=$char
            fi
            ;;
        '&')
            if [[ "$prev" == [\<\>] || "${line:i+1:1}" == ">" ]]; then
                # Part of a redirection (`2>&1`, `>&2`, `<&3`, `&>file`, `&>>file`), not a separator.
                current+=$char
            else
                add_segment "$current"
                current=""
            fi
            ;;
        '|')
            if [[ "$prev" == ">" ]]; then
                # `>|file` is the clobbering redirection, not a pipe.
                current+=$char
            else
                add_segment "$current"
                current=""
            fi
            ;;
        ';' | $'\n')
            add_segment "$current"
            current=""
            if [[ "$char" == $'\n' && ${#delimiters[@]} -gt 0 ]]; then
                # The here-document bodies follow this newline, one after another, each up to its terminator.
                for ((j = 0; j < ${#delimiters[@]}; j++)); do
                    while ((i < ${#line})); do
                        rest=${line:i+1}
                        body=${rest%%$'\n'*}
                        i=$((i + ${#body} + 1))
                        if [[ -n "${strips[j]}" ]]; then
                            body=${body#"${body%%[!$'\t']*}"}
                        fi
                        if [[ "$body" == "${delimiters[j]}" ]]; then
                            break
                        fi
                    done
                done
                delimiters=()
                strips=()
            fi
            ;;
        *)
            current+=$char
            ;;
        esac
    done
    add_segment "$current"
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
        split_segments "$command"
        for segment in "${SEGMENTS[@]}"; do
            classify_segment "$segment"
        done
    fi

    exit 0
}

main
