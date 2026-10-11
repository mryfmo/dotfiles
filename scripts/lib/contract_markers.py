"""Task-file and contract-decorator queries for scripts/main-tests.sh (T128 INV-12).

task <task.md>       print the task id, its tier, its declared tests/unit modules,
                     and each declared design-tier script without its module
scripts              print the script paths among the paths read from stdin
contracts <module>   print the unittest ids that carry the contract decorator
dormant <module>     exit 1 when any contract decorator remains
"""

import ast
import re
import sys
from pathlib import Path

SCRIPT_PATH = re.compile(r"(scripts/|home/dot_local/bin/|install/|home/\.chezmoiscripts/|setup\.sh$)")
DATA_SUFFIXES = (".txt", ".json", ".md", ".yaml")
MODULE_PATH = re.compile(r"tests/unit/test_[^/]+\.py")


def module_for(script: str) -> str:
    """The repository's module naming: scripts/require-crit-review.py -> tests/unit/test_require_crit_review.py."""
    name = script.rsplit("/", 1)[-1].removeprefix("executable_")
    for suffix in (".tmpl", ".sh", ".py"):
        name = name.removesuffix(suffix)
    return f"tests/unit/test_{name.replace('-', '_')}.py"


def task(path: str) -> list[str]:
    import yaml

    text = Path(path).read_text()
    if not text.startswith("---\n") or "\n---\n" not in text[3:]:
        raise SystemExit(f"main-tests: {path} has no front matter")
    front = yaml.safe_load(text[4 : text.index("\n---\n", 3)])
    if not isinstance(front, dict) or not isinstance(front.get("task_id"), str):
        raise SystemExit(f"main-tests: {path} has no task_id")
    files = front.get("allowed_files")
    if not isinstance(files, list) or not all(isinstance(entry, str) for entry in files):
        raise SystemExit(f"main-tests: {path} has no allowed_files list")
    # A missing or unknown stamp is design tier, the strictest.
    tier = front.get("tier") if front.get("tier") in ("docs", "review") else "design"
    modules = [entry for entry in files if MODULE_PATH.fullmatch(entry)]
    lines = [f"task_id\t{front['task_id']}", f"tier\t{tier}", *(f"module\t{module}" for module in modules)]
    if tier == "design":
        for entry in files:
            if SCRIPT_PATH.match(entry) and not entry.endswith(DATA_SUFFIXES) and module_for(entry) not in modules:
                lines.append(f"uncovered\t{entry}\t{module_for(entry)}")
    return lines


def is_contract(decorator: ast.expr, names: set[str], modules: set[str]) -> bool:
    if isinstance(decorator, ast.Name):
        return decorator.id in names
    if isinstance(decorator, ast.Attribute):
        return decorator.attr == "contract" and isinstance(decorator.value, ast.Name) and decorator.value.id in modules
    if isinstance(decorator, ast.Call):
        func = decorator.func
        name = func.attr if isinstance(func, ast.Attribute) else getattr(func, "id", "")
        return name == "skipUnless" and any(
            isinstance(node, ast.Constant) and node.value == "REGIME_CONTRACT" for node in ast.walk(decorator)
        )
    return False


def marked(path: str) -> tuple[ast.Module, list[ast.AST]]:
    """Every class or function that carries `contract`, under any import alias, or the inline skipUnless."""
    tree = ast.parse(Path(path).read_text(), path)
    names, modules = set(), set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module == "regime_contract":
            names |= {alias.asname or "contract" for alias in node.names if alias.name in ("contract", "*")}
        elif isinstance(node, ast.Import):
            modules |= {alias.asname or alias.name for alias in node.names if alias.name == "regime_contract"}
    found = [
        node
        for node in ast.walk(tree)
        if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef))
        and any(is_contract(decorator, names, modules) for decorator in node.decorator_list)
    ]
    return tree, found


def contracts(path: str) -> list[str]:
    tree, found = marked(path)
    stem = Path(path).stem
    ids = []
    for cls in (node for node in tree.body if isinstance(node, ast.ClassDef)):
        if cls in found:
            ids.append(f"{stem}.{cls.name}")
        else:
            ids += [f"{stem}.{cls.name}.{item.name}" for item in cls.body if item in found]
    return ids


def main(argv: list[str]) -> int:
    match argv:
        case ["task", path]:
            print(*task(path), sep="\n")
        case ["scripts"]:
            print(*(line for line in sys.stdin.read().splitlines() if SCRIPT_PATH.match(line)), sep="\n")
        case ["contracts", path]:
            print(*contracts(path), sep="\n")
        case ["dormant", path]:
            return 1 if marked(path)[1] else 0
        case _:
            print(__doc__, file=sys.stderr)
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
