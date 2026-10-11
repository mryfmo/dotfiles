"""Task-file and contract-decorator queries for scripts/main-tests.sh (T128 INV-12).

task <task.md>       print the task id, its tier, its declared tests/unit modules,
                     the declared modules whose script is declared too and whose
                     changed scripts (read from stdin) all are (exempt), and each
                     declared design-tier script without its module
scripts              print the script paths among the paths read from stdin
contracts <module>...
                     print the unittest test-method ids that carry the contract decorator
dormant <module>     exit 1 when any contract decorator remains
run <result> [-v] <ids...>
                     run the tests and write {nonce, ran, failures, errors, skipped ids} to <result>;
                     the nonce arrives on fd 3, closed before any test module loads
result <result> <nonce> <expected> [<allowed skips>]
                     exit 1 unless <result> carries the nonce, no failure or error,
                     <expected> tests run (0: any count above zero), and no skip outside
                     the newline-separated <allowed skips>
"""

import ast
import json
import os
import re
import sys
import unittest
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
    # The output is tab- and line-delimited, so a value carrying either could forge a record.
    for value in (front["task_id"], *files):
        if re.search(r"[\t\n\r]", value):
            raise SystemExit(f"main-tests: {path} has a tab or line break in {value!r}")
    # A missing or unknown stamp is design tier, the strictest.
    tier = front.get("tier") if front.get("tier") in ("docs", "review") else "design"
    modules = [entry for entry in files if MODULE_PATH.fullmatch(entry)]
    scripts = [entry for entry in files if SCRIPT_PATH.match(entry) and not entry.endswith(DATA_SUFFIXES)]
    # Contract-only selection is keyed on the declared script; a module declared alone still runs as it is,
    # and so does one that any undeclared changed script maps to (a declared decoy of the same name).
    blocked = {module_for(changed) for changed in sys.stdin.read().splitlines() if changed and changed not in files}
    exempt = [module for module in modules if module in map(module_for, scripts) and module not in blocked]
    lines = [f"task_id\t{front['task_id']}", f"tier\t{tier}", *(f"module\t{module}" for module in modules)]
    lines += [f"exempt\t{module}" for module in exempt]
    if tier == "design":
        lines += [
            f"uncovered\t{script}\t{module_for(script)}" for script in scripts if module_for(script) not in modules
        ]
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
    """Test methods only: a decorated class contributes its own test methods, so an empty one contributes none."""
    tree, found = marked(path)
    stem = Path(path).stem
    ids = []
    for cls in (node for node in tree.body if isinstance(node, ast.ClassDef)):
        for item in cls.body:
            is_test = isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)) and item.name.startswith("test")
            if is_test and (cls in found or item in found):
                ids.append(f"{stem}.{cls.name}.{item.name}")
    return ids


def run(result: str, ids: list[str]) -> None:
    """Run main's tests in this process; only a result carrying the harness's nonce counts as a completed run."""
    chunks = []
    while chunk := os.read(3, 4096):
        chunks.append(chunk)
    os.close(3)  # before any test module loads
    nonce = b"".join(chunks).decode().strip()
    verbose = ids[:1] == ["-v"]
    names = ids[1:] if verbose else ids
    outcome = unittest.TextTestRunner(verbosity=2 if verbose else 1).run(
        unittest.TestLoader().loadTestsFromNames(names)
    )
    failures = len(outcome.failures) + len(outcome.unexpectedSuccesses)
    record = {
        "nonce": nonce,
        "ran": outcome.testsRun,
        "failures": failures,
        "errors": len(outcome.errors),
        "skipped": [test.id() for test, _ in outcome.skipped],
    }
    Path(result).write_text(json.dumps(record))
    sys.stdout.flush()
    sys.stderr.flush()
    # os._exit: no atexit handler a test module registered may rewrite the result after this point.
    os._exit(0 if outcome.wasSuccessful() else 1)


def check(result: str, nonce: str, expected: int, allowed: list[str]) -> str | None:
    """The reason the run does not count, or None."""
    try:
        record = json.loads(Path(result).read_text())
    except (OSError, ValueError):
        return "no result file"
    if not isinstance(record, dict) or record.get("nonce") != nonce:
        return "the result does not carry this run's nonce"
    ran = record.get("ran")
    if type(ran) is not int or ran <= 0 or (expected and ran != expected):
        return f"ran {ran}, expected {expected or 'more than 0'}"
    if record.get("failures") != 0 or record.get("errors") != 0:
        return f"{record.get('failures')} failures, {record.get('errors')} errors"
    # A test the PR's code skips never asserted anything; only main's dormant contracts may skip.
    skipped = record.get("skipped")
    if not isinstance(skipped, list):
        return f"skipped {skipped} is not a list of test ids"
    if outside := [test for test in skipped if test not in allowed]:
        return f"{len(outside)} skipped outside main's dormant contracts"
    return None


def main(argv: list[str]) -> int:
    match argv:
        case ["task", path]:
            print(*task(path), sep="\n")
        case ["scripts"]:
            print(*(line for line in sys.stdin.read().splitlines() if SCRIPT_PATH.match(line)), sep="\n")
        case ["contracts", *paths]:
            print(*(test for path in paths for test in contracts(path)), sep="\n")
        case ["dormant", path]:
            return 1 if marked(path)[1] else 0
        case ["run", result, *ids]:
            run(result, ids)
        case ["result", result, nonce, expected, *allowed]:
            if reason := check(result, nonce, int(expected), "\n".join(allowed).split()):
                print(f"main-tests: no complete unittest run ({reason})")
                return 1
        case _:
            print(__doc__, file=sys.stderr)
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
