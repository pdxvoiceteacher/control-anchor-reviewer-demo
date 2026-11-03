"""Bind focused extraction tests to the public checkout, not sibling installs."""
from __future__ import annotations

import hashlib
from importlib.metadata import version
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
for relative in ("src", "components/CoherenceLattice/python/src", "components/Sophia/python/src"):
    sys.path.insert(0, str(ROOT / relative))


def pytest_sessionstart(session):
    if sys.version_info < (3, 12):
        raise RuntimeError("Python 3.12 or later is required")
    if version("jsonschema") != "4.26.0":
        raise RuntimeError("This extraction qualifies jsonschema==4.26.0")


def pytest_sessionfinish(session, exitstatus):
    manifest = json.loads((ROOT / "SOURCE_MANIFEST.json").read_text(encoding="utf-8"))
    identities = {row["path"]: row["candidate_sha256"]
                  for group in ("copied_files", "new_or_adapted_files") for row in manifest[group]}
    paths = set()
    for name, module in tuple(sys.modules.items()):
        if name.split(".")[0] not in {"triadicbrain", "coherence", "sophia"}:
            continue
        origin = getattr(module, "__file__", None)
        if origin is None:
            raise RuntimeError(f"Unbound project module: {name}")
        path = Path(origin).resolve()
        if not path.is_relative_to(ROOT):
            raise RuntimeError(f"Project module came from outside the public checkout: {name}")
        relative = path.relative_to(ROOT).as_posix()
        if hashlib.sha256(path.read_bytes()).hexdigest() != identities.get(relative):
            raise RuntimeError(f"Project source identity mismatch: {relative}")
        paths.add(relative)
    print(f"\nVerified {len(paths)} imported project modules against the public source manifest.")
