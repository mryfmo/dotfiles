#!/usr/bin/env bash
# The fixture scripts/ci/shfmt_json_contract.py parses with the pinned shfmt: every node kind and field the
# repository's walkers over `shfmt -ln bash --to-json` read is produced here at least once (backquotes in the sibling
# contract-backquotes, which the formatting gate would rewrite here), so a parser whose JSON no longer matches the
# node table is refused before any real file is read. tests/unit/test_shfmt_json_contract.py pins the captured tree
# (contract.json) and the line of the one nested command substitution below.
dir=$(cd "$(dirname "$0")" && pwd -P) || exit 2
name=$(basename "$0")
printf '%s\n' "double $name" 'single' $'dollar\n' $"locale" a\ b
count=${#name}
item=${list[index]}
words=(one two)
words+=(three)
cat << 'EOF'
$(quoted body)
EOF
cat << EOF 2> /dev/null
unquoted $(basename "$0") body
EOF
f() {
    sort "$dir" | uniq -c
}
total=$((count + 1))
diff <(sort a) <(sort b)
[[ $name == x ]] && echo "$total"
[[ $name != y || $name = z ]] || exit 0
: "${TMPDIR:-}" "${jq:-}"
case $name in
@(a|b)) ;;
esac
(
    true
)
# producer-status-check (U112): the tested positions of an assignment, `[[ ! -s file ]]`, and a `read` from a file.
if ! first=$(pwd -P); then
    exit 1
elif first=$(printf y); then
    :
fi
while first=$(printf x); do
    break
done
[[ ! -s "$dir/err" ]] || exit 1
read -r first < "$dir/file"
echo "$first"
# producer-status-check (U112 round 2): every way stderr moves, so the redirect spellings the lint reads are in the tree.
git ls-files > "$dir/list" 2>> "$dir/err" 2>| "$dir/err" 2>&1 &> "$dir/out" &>> "$dir/out" >&"$dir/out" || exit 1
# producer-status-check (U112 round 4): the `||` branches that handle a tested read's status, so the function name, the
# block and the `$?` the lint reads are in the tree.
refuse() {
    echo "$1" >&2
    exit 2
}
first=$(printf z) || refuse 'no z'
first=$(printf z) || status=$?
first=$(printf z) || { exit 1; }
# producer-status-check (U112 round 6): a negated, a background and a coprocess read, so the statement flags and the
# coprocess clause the lint reads are in the tree.
! first=$(printf n) || exit 1
first=$(printf b) || exit 1 &
coproc { first=$(printf c); } || exit 1
# producer-status-check (U112 round 9): a refusal body that writes by `1>&2`, so the descriptor spelling the grammar
# reads is in the tree.
fail() {
    echo "$1" 1>&2
    exit 1
}
first=$(printf w) || fail 'no w'
# producer-status-check (U112 round 13): a descriptor spelled `02`, the move `1>&2-` and a `<&`, so the decimal
# reading of the descriptor and both dup operators the lint reads are in the tree.
git ls-files > "$dir/list" 2> "$dir/err" 02>&1 1>&2- <&0 || exit 1
# producer-status-check (U112 round 14): the one `source` shape rule f accepts, so the parameter and the two literals
# the rule reads are in the tree.
. "${LEVER_DIR}/git-isolated.sh"
. "${LEVER_DIR}/read-lib.sh"
# producer-status-check (U112 round 17): a declaration whose argument is a quoted assignment word, so the variant and
# the arguments the lint reads on a DeclClause are in the tree.
export 'FIRST=1'
