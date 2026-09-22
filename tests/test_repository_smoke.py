from __future__ import annotations

import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INTEGRATION_DIR = ROOT / "custom_components" / "myhome"
MANIFEST = INTEGRATION_DIR / "manifest.json"


def test_python_sources_parse() -> None:
    """All integration Python modules must be valid for the CI Python version."""
    failures: list[str] = []

    for path in sorted(INTEGRATION_DIR.rglob("*.py")):
        try:
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except (SyntaxError, UnicodeError) as err:
            failures.append(f"{path.relative_to(ROOT)}: {err}")

    assert not failures, "\n".join(failures)


def test_manifest_basics() -> None:
    """Keep the custom integration manifest structurally sane."""
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    assert manifest["domain"] == "myhome"
    assert manifest["name"]
    assert manifest["version"]
    assert manifest["config_flow"] is True
    assert manifest["iot_class"]
    assert isinstance(manifest.get("requirements"), list)
