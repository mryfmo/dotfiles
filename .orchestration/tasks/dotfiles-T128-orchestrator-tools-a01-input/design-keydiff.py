"""design-keydiff.py <design.md>: print the hashed-key diff of the working copy against main's copy (C-15).

Inline form the orchestrator ran on 2026-10-12 before round 22; T718 promotes it with argument parsing and a test.
"""
import subprocess, sys, yaml, pathlib
def front(text): return yaml.safe_load(text.split("\n---\n")[0].split("---\n", 1)[1])
path = sys.argv[1]
main = subprocess.run(["git", "show", f"HEAD:{path}"], capture_output=True, text=True, check=True).stdout
a, b = front(main), front(pathlib.Path(path).read_text())
for k in ["threat_model", "trust_anchors", "invariants", "implementing_tasks", "premises", "supersedes", "reset_of", "design_review"]:
    if a.get(k) != b.get(k):
        if isinstance(a.get(k), dict) and isinstance(b.get(k), dict):
            print(k, sorted(x for x in set(a[k]) | set(b[k]) if a[k].get(x) != b[k].get(x)))
        else:
            print(k, "changed")
