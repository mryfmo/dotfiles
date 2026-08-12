from __future__ import annotations

import sys
import tempfile
from pathlib import Path
from typing import Any

PROJECT_PACKAGE = Path(__file__).resolve().parents[1] / ".claude" / "contextdb"
if str(PROJECT_PACKAGE) not in sys.path:
    sys.path.insert(0, str(PROJECT_PACKAGE))

from contextdb.config import load_config
from contextdb.normalize import normalize_hook_payload
from contextdb.paths import project_paths
from contextdb.spool import drain_spool, spool_event
from contextdb.storage import ContextStore


class TempProject:
    def __init__(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="compactiondb-test-")
        self.root = Path(self.temp.name)
        self.paths = project_paths(explicit=self.root)
        self.config = load_config(self.paths)
        self.store = ContextStore(self.paths, self.config)

    def close(self) -> None:
        self.temp.cleanup()

    def event(self, payload: dict[str, Any], *, drain: bool = True) -> dict[str, Any]:
        payload = {"cwd": str(self.root), **payload}
        event = normalize_hook_payload(payload, self.paths, self.config)
        spool_event(self.paths, event)
        if drain:
            result = drain_spool(self.paths, self.config, blocking_lock=True)
            if result.error:
                raise RuntimeError(result.error)
        return event

    def count(self, table: str) -> int:
        conn = self.store.connect()
        try:
            return int(conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0])
        finally:
            conn.close()
