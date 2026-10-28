#!/bin/bash

# @file home/dot_claude/hooks/executable_enforce-uv.sh
# @brief Block direct Python and pip commands in favor of `uv`.
# @description
#   Emit PreToolUse permissionDecision deny for direct `pip` or `python` usage;
#   other input exits successfully without output. Contract verified 2026-10-05.
#   Advisory, not a boundary: it nudges toward uv. A Bash line is parsed by shfmt (on PATH from the mise config)
#   into its syntax tree, and every simple command in it is judged on its own text. shfmt's JSON must match the
#   pinned node table of scripts/ci/shfmt_json_contract.py (regime-cutover U105). Every read of a producer keeps
#   its three outcomes apart (standing order 21): what it found is judged; an empty result (a line with no simple
#   command) is no decision, exit 0 without output; a failed read is a blocking error, exit 2 with the probe and
#   the status on stderr, never a silent "no decision". Failed reads: no shfmt on PATH, shfmt exiting nonzero (a
#   line it cannot parse included), a JSON that does not match the table, jq exiting nonzero or printing another
#   shape, a tree whose statements the walk cannot see. The one fail-open left is a deployed copy that finds no
#   contract module (contract_module): it decides nothing, exit 0.
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

# @description Print the path of scripts/ci/shfmt_json_contract.py: relative to this file in the dotfiles checkout
#   (home/dot_claude/hooks/), else under the chezmoi source directory the deployed copy came from.
# @stdout The module path.
# @exitcode 1 No module found there.
function contract_module() {
    local here candidate source
    case ${BASH_SOURCE[0]} in
    */*) here=${BASH_SOURCE[0]%/*} ;;
    *) here=. ;;
    esac
    candidate="${here}/../../../scripts/ci/shfmt_json_contract.py"
    if [[ -f ${candidate} ]]; then
        printf '%s\n' "${candidate}"
        return 0
    fi
    source=$(chezmoi source-path 2> /dev/null) || return 1
    candidate="${source}/../scripts/ci/shfmt_json_contract.py"
    [[ -f ${candidate} ]] || return 1
    printf '%s\n' "${candidate}"
}

# @description Judge one probe's read of a producer. The status and every non-empty output line are checked: a
#   status 0 with output of the given shape is a found result, a status 0 without output an empty one, and anything
#   else is a failed read, named in REFUSAL for main to report (exit 2).
# @arg $1 string The probe, as the refusal names it ("jq counting the statements the tree lists").
# @arg $2 int The tool's exit status.
# @arg $3 string The tool's output.
# @arg $4 string An extended regular expression every non-empty output line must match.
# @arg $5 string What a line of that shape is called ("a count").
# @set REFUSAL string On return 2, why the line cannot be judged.
# @exitcode 0 Found or empty.
# @exitcode 2 A failed read.
function read_or_refuse() {
    local probe="$1" status="$2" output="$3" shape="$4" called="$5" row
    if ((status != 0)); then
        REFUSAL="${probe} exited ${status}; the line cannot be judged"
        return 2
    fi
    while IFS= read -r row; do
        if [[ -n "$row" && ! "$row" =~ $shape ]]; then
            REFUSAL="${probe} printed '${row}', not ${called}; the line cannot be judged"
            return 2
        fi
    done <<< "$output"
}

# @description Collect the simple commands of a Bash line from shfmt's syntax tree (`shfmt -ln bash --to-json`):
#   every statement whose command is a call (`CallExpr`), in tree order, nested ones (in a pipeline, a list, a
#   subshell, `$(...)`) included, each as its source text from the statement's start to its end offset, so the
#   suggestion keeps its quotes and redirections. Comments and here-document bodies are no statements, and quoting,
#   escapes and line continuations are shfmt's, not this script's. Before the walk, the contract module proves the
#   parser still produces these nodes; a line whose tree lists statements the walk then cannot see is refused too.
#   Each probe's three outcomes (regime-cutover U105 round 5); a failed read is named by read_or_refuse or here:
#   | probe                                | found           | empty                           | failed read (return 2)                     |
#   | command -v shfmt                     | a path          |                                 | no shfmt on PATH                           |
#   | shfmt -ln bash --to-json on the line | the tree        |                                 | nonzero status (a parse error too), no tree |
#   | contract_module                      | the module path | none installed: return 1 (open) |                                            |
#   | python3 -I on the module (contract)  | status 0        |                                 | 2: the JSON does not match; other: named   |
#   | jq: statements the tree lists        | a count         | 0                               | nonzero status, or no count printed        |
#   | jq: statement nodes the walk sees    | a count         | 0 (refused when any was listed) | nonzero status, or no count printed        |
#   | jq: the call statements' offsets     | start-end lines | none: no segment, no decision   | nonzero status, or a line of another shape |
# @arg $1 string The command line.
# @set SEGMENTS array The simple commands, in order.
# @set REFUSAL string On return 2, why the line cannot be judged.
# @exitcode 0 The line parsed; SEGMENTS holds its simple commands, possibly none.
# @exitcode 1 No contract module is installed beside this file or under the chezmoi source: the documented fail-open.
# @exitcode 2 A failed read, a contract mismatch, or a tree whose statements the walk cannot see: main exits 2.
function split_segments() {
    local line="$1" tree spans start end module listed visited status
    SEGMENTS=()
    REFUSAL=""
    if ! command -v shfmt > /dev/null 2>&1; then
        REFUSAL="shfmt is not on PATH, so no Bash line can be judged; home/dot_mise/config.toml installs the pinned one"
        return 2
    fi
    tree=$(printf '%s' "$line" | shfmt -ln bash --to-json)
    read_or_refuse "shfmt parsing the line" "$?" "" "" "" || return 2
    if [[ -z "$tree" ]]; then
        REFUSAL="shfmt printed no tree for the line; the line cannot be judged"
        return 2
    fi
    module=$(contract_module) || return 1
    python3 -I "$module"
    status=$?
    if ((status == 2)); then
        REFUSAL="shfmt's JSON does not match the pinned node table; no Bash line can be judged"
        return 2
    elif ((status != 0)); then
        REFUSAL="python3 -I ${module} exited ${status} proving the contract; the line cannot be judged"
        return 2
    fi
    # The statements the tree lists against the statement nodes the walk can see: a renamed field would leave the
    # walk empty and the line silently undecided.
    listed=$(jq -r '.Stmts // [] | length' <<< "$tree")
    read_or_refuse "jq counting the statements the tree lists" "$?" "$listed" '^[0-9]+$' "a count" || return 2
    visited=$(jq -r '[.. | objects | select(has("Cmd"))] | length' <<< "$tree")
    read_or_refuse "jq counting the statement nodes the walk sees" "$?" "$visited" '^[0-9]+$' "a count" || return 2
    if ((listed > 0 && visited == 0)); then
        REFUSAL="shfmt's tree lists ${listed} statement(s) but the walk saw none; the line cannot be judged"
        return 2
    fi
    spans=$(jq -r '.. | objects | select(.Cmd.Type? == "CallExpr") | "\(.Pos.Offset) \(.End.Offset)"' <<< "$tree")
    read_or_refuse "jq reading the call statements' offsets" "$?" "$spans" '^[0-9]+ [0-9]+$' "an offset pair" || return 2
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
        local segment parsed=0
        split_segments "$command" || parsed=$?
        # 1 is the one fail-open: no contract module on this host, so no decision. Any other failure is a refusal,
        # reported the way a contract mismatch is: the tool call is blocked and the reason reaches the caller.
        if ((parsed == 1)); then
            exit 0
        elif ((parsed != 0)); then
            echo "enforce-uv: ${REFUSAL}" >&2
            exit 2
        fi
        for segment in "${SEGMENTS[@]}"; do
            classify_segment "$segment"
        done
    fi

    exit 0
}

main
